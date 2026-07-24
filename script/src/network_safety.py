"""Network helpers for requests whose URLs come from untrusted content."""

from __future__ import annotations

import ipaddress
import os
import socket
import sys
from dataclasses import dataclass
from urllib.parse import urljoin, urlsplit

import requests
from requests.adapters import HTTPAdapter
from urllib3.connection import DummyConnection, HTTPConnection, HTTPSConnection
from urllib3.connectionpool import HTTPConnectionPool, HTTPSConnectionPool
from urllib3.exceptions import ConnectTimeoutError, NewConnectionError
from urllib3.util.timeout import Timeout

REDIRECT_STATUS_CODES = {301, 302, 303, 307, 308}
TRUSTED_ARXIV_HOSTS = frozenset({"arxiv.org", "export.arxiv.org"})


class UnsafeUrlError(ValueError):
    """Raised when a URL can reach a non-public network address."""


@dataclass(frozen=True)
class _ValidatedTarget:
    url: str
    scheme: str
    hostname: str
    port: int
    endpoints: tuple


def _is_public_address(address: str) -> bool:
    ip = ipaddress.ip_address(address.split("%", 1)[0])
    mapped = getattr(ip, "ipv4_mapped", None)
    if mapped is not None:
        ip = mapped
    return bool(
        ip.is_global
        and not ip.is_private
        and not ip.is_loopback
        and not ip.is_link_local
        and not ip.is_multicast
        and not ip.is_reserved
        and not ip.is_unspecified
    )


def _canonical_hostname(hostname: str) -> str:
    value = str(hostname or "").rstrip(".")
    if not value or "%" in value:
        raise UnsafeUrlError("URL hostname is empty or contains a scope identifier")
    try:
        literal = ipaddress.ip_address(value)
    except ValueError:
        try:
            return value.encode("idna").decode("ascii").lower()
        except UnicodeError as exc:
            raise UnsafeUrlError("URL hostname is not valid IDNA") from exc
    return str(literal)


def _endpoint_from_address(address, port, family=None, socktype=None, proto=None):
    raw_address = str(address or "").split("%", 1)[0]
    try:
        ip = ipaddress.ip_address(raw_address)
    except ValueError as exc:
        raise UnsafeUrlError(f"URL resolved to an invalid address: {address}") from exc
    if not _is_public_address(str(ip)):
        raise UnsafeUrlError(f"URL resolves to a non-public address: {ip}")

    expected_family = socket.AF_INET6 if ip.version == 6 else socket.AF_INET
    if family is not None and family != expected_family:
        raise UnsafeUrlError(f"URL resolver returned a mismatched address family for: {ip}")
    family = expected_family
    socktype = socktype or socket.SOCK_STREAM
    if socktype != socket.SOCK_STREAM:
        raise UnsafeUrlError("URL resolver returned a non-stream socket")
    proto = proto or socket.IPPROTO_TCP
    sockaddr = (str(ip), port, 0, 0) if family == socket.AF_INET6 else (str(ip), port)
    return family, socktype, proto, sockaddr


def _resolve_public_target(url: str, resolver=None) -> _ValidatedTarget:
    value = str(url or "").strip()
    if not value or any(ord(char) < 32 for char in value) or "\\" in value:
        raise UnsafeUrlError("URL is empty or contains unsafe characters")

    try:
        parsed = urlsplit(value)
        raw_hostname = parsed.hostname
        explicit_port = parsed.port
    except ValueError as exc:
        raise UnsafeUrlError(f"Invalid URL: {exc}") from exc

    scheme = parsed.scheme.lower()
    if scheme not in {"http", "https"} or not raw_hostname:
        raise UnsafeUrlError("Only absolute HTTP(S) URLs are allowed")
    if parsed.username is not None or parsed.password is not None:
        raise UnsafeUrlError("URLs containing user information are not allowed")

    hostname = _canonical_hostname(raw_hostname)
    if explicit_port is not None and explicit_port < 1:
        raise UnsafeUrlError("URL port must be between 1 and 65535")
    port = explicit_port if explicit_port is not None else (443 if scheme == "https" else 80)
    try:
        literal = ipaddress.ip_address(hostname)
    except ValueError:
        literal = None

    if literal is not None:
        endpoints = (_endpoint_from_address(str(literal), port),)
    else:
        resolver = resolver or socket.getaddrinfo
        try:
            records = resolver(hostname, port, type=socket.SOCK_STREAM)
        except (OSError, UnicodeError) as exc:
            raise UnsafeUrlError(f"URL hostname could not be resolved: {hostname}") from exc

        endpoints_list = []
        seen = set()
        for record in records:
            if not record or len(record) < 5 or not record[4]:
                raise UnsafeUrlError(f"URL hostname returned an invalid DNS record: {hostname}")
            family, socktype, proto = record[:3]
            if family not in {socket.AF_INET, socket.AF_INET6}:
                raise UnsafeUrlError(f"URL hostname returned an unsupported address family: {hostname}")
            endpoint = _endpoint_from_address(record[4][0], port, family, socktype, proto)
            key = (endpoint[0], endpoint[3])
            if key not in seen:
                seen.add(key)
                endpoints_list.append(endpoint)
        if not endpoints_list:
            raise UnsafeUrlError(f"URL hostname resolved to no addresses: {hostname}")
        endpoints = tuple(endpoints_list)

    return _ValidatedTarget(value, scheme, hostname, port, endpoints)


def validate_public_http_url(url: str, resolver=None) -> str:
    """Validate that an HTTP(S) URL resolves exclusively to public IPs."""
    return _resolve_public_target(url, resolver=resolver).url


def configured_http_proxy(environ=None):
    """Return the configured HTTP(S) proxy without logging or exposing it."""
    values = environ if environ is not None else os.environ
    for key in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        value = str(values.get(key, "") or "").strip()
        if not value:
            continue
        try:
            parsed = urlsplit(value)
        except ValueError:
            continue
        if parsed.scheme.lower() in {"http", "https"} and parsed.hostname:
            return value
    return None


def is_trusted_https_url(url: str, allowed_hosts) -> bool:
    """Return whether a URL is HTTPS and belongs to an exact trusted host."""
    try:
        parsed = urlsplit(str(url or "").strip())
        hostname = _canonical_hostname(parsed.hostname)
    except (TypeError, ValueError, UnsafeUrlError):
        return False
    normalized_hosts = {_canonical_hostname(host) for host in allowed_hosts}
    return bool(
        parsed.scheme.lower() == "https"
        and parsed.username is None
        and parsed.password is None
        and hostname in normalized_hosts
    )


class _PinnedConnectionMixin:
    """Connect to prevalidated socket addresses without another DNS lookup."""

    def __init__(self, *args, **kwargs):
        endpoints = kwargs.pop("pinned_endpoints", None)
        if not endpoints:
            raise ValueError("pinned_endpoints must not be empty")
        self._pinned_endpoints = tuple(endpoints)
        super().__init__(*args, **kwargs)

    def _new_conn(self):
        last_error = None
        for family, socktype, proto, sockaddr in self._pinned_endpoints:
            sock = None
            try:
                sock = socket.socket(family, socktype, proto)
                for option in self.socket_options or ():
                    sock.setsockopt(*option)
                if self.timeout is not Timeout.DEFAULT_TIMEOUT:
                    sock.settimeout(self.timeout)
                if self.source_address:
                    sock.bind(self.source_address)
                sock.connect(sockaddr)
                sys.audit("http.client.connect", self, self.host, self.port)
                return sock
            except OSError as exc:
                last_error = exc
                if sock is not None:
                    sock.close()

        if isinstance(last_error, socket.timeout):
            raise ConnectTimeoutError(
                self,
                f"Connection to {self.host} timed out. (connect timeout={self.timeout})",
            ) from last_error
        raise NewConnectionError(
            self,
            f"Failed to establish a pinned connection to {self.host}: {last_error}",
        ) from last_error


class _PinnedHTTPConnection(_PinnedConnectionMixin, HTTPConnection):
    pass


if HTTPSConnection is DummyConnection:
    _PinnedHTTPSConnection = DummyConnection
else:

    class _PinnedHTTPSConnection(_PinnedConnectionMixin, HTTPSConnection):
        pass


class _PinnedHTTPConnectionPool(HTTPConnectionPool):
    ConnectionCls = _PinnedHTTPConnection


class _PinnedHTTPSConnectionPool(HTTPSConnectionPool):
    ConnectionCls = _PinnedHTTPSConnection


def _origin_from_url(url):
    try:
        parsed = urlsplit(url)
        scheme = parsed.scheme.lower()
        hostname = _canonical_hostname(parsed.hostname)
        explicit_port = parsed.port
        if explicit_port is not None and explicit_port < 1:
            raise UnsafeUrlError("URL port must be between 1 and 65535")
        port = explicit_port if explicit_port is not None else (443 if scheme == "https" else 80)
    except (TypeError, ValueError) as exc:
        raise UnsafeUrlError(f"Invalid request URL: {exc}") from exc
    return scheme, hostname, port


class _PinnedHTTPAdapter(HTTPAdapter):
    """Requests adapter backed by one origin-specific, DNS-pinned pool."""

    def __init__(self, target):
        self._target = target
        super().__init__(pool_connections=1, pool_maxsize=1, max_retries=0, pool_block=True)
        pool_type = _PinnedHTTPSConnectionPool if target.scheme == "https" else _PinnedHTTPConnectionPool
        pool_kwargs = {
            "maxsize": 1,
            "block": True,
            "pinned_endpoints": target.endpoints,
        }
        if target.scheme == "https":
            pool_kwargs["assert_hostname"] = target.hostname
            pool_kwargs["server_hostname"] = target.hostname
        self._pinned_pool = pool_type(target.hostname, target.port, **pool_kwargs)

    def _assert_same_origin(self, url):
        if _origin_from_url(url) != (self._target.scheme, self._target.hostname, self._target.port):
            raise UnsafeUrlError("Pinned adapter cannot be reused for another origin")

    def get_connection(self, url, proxies=None):
        """Requests 2.31 connection hook."""
        self._assert_same_origin(url)
        return self._pinned_pool

    def get_connection_with_tls_context(self, request, verify, proxies=None, cert=None):
        """Requests 2.32+ connection hook."""
        self._assert_same_origin(request.url)
        return self._pinned_pool

    def add_headers(self, request, **kwargs):
        """Let urllib3 generate Host from the pool's original hostname."""
        for key in list(request.headers):
            if str(key).lower() == "host":
                del request.headers[key]

    def close(self):
        self._pinned_pool.close()
        super().close()


def _without_host_header(headers):
    if headers is None:
        return None
    return {key: value for key, value in headers.items() if str(key).lower() != "host"}


def _request_pinned_once(method, target, **kwargs):
    if not kwargs.get("verify", True):
        raise ValueError("HTTPS certificate verification cannot be disabled")

    request_kwargs = dict(kwargs)
    request_kwargs.pop("allow_redirects", None)
    request_kwargs.pop("proxies", None)
    if "headers" in request_kwargs:
        request_kwargs["headers"] = _without_host_header(request_kwargs["headers"])

    session = requests.Session()
    session.trust_env = False
    session.proxies.clear()
    adapter = _PinnedHTTPAdapter(target)
    for default_adapter in session.adapters.values():
        default_adapter.close()
    session.adapters.clear()
    session.mount(f"{target.scheme}://", adapter)
    try:
        response = session.request(
            method,
            target.url,
            allow_redirects=False,
            proxies={},
            **request_kwargs,
        )
    except Exception:
        session.close()
        raise

    original_close = response.close
    session_closed = False

    def close_response_and_session():
        nonlocal session_closed
        try:
            return original_close()
        finally:
            if not session_closed:
                session_closed = True
                session.close()

    response.close = close_response_and_session
    return response


def request_public_url(
    method: str,
    url: str,
    *,
    max_redirects: int = 5,
    resolver=None,
    **kwargs,
):
    """Request a public URL, pinning DNS and revalidating every redirect."""
    request_method = str(method or "").upper()
    if request_method not in {"GET", "HEAD"}:
        raise ValueError("request_public_url only supports GET and HEAD")

    current_url = str(url or "").strip()
    seen = set()
    max_redirects = max(0, int(max_redirects))
    request_kwargs = dict(kwargs)
    request_kwargs.pop("allow_redirects", None)

    for redirect_count in range(max_redirects + 1):
        target = _resolve_public_target(current_url, resolver=resolver)
        if current_url in seen:
            raise requests.TooManyRedirects("Redirect loop detected")
        seen.add(current_url)

        response = _request_pinned_once(request_method, target, **request_kwargs)
        if response.status_code not in REDIRECT_STATUS_CODES:
            return response

        location = response.headers.get("Location") if getattr(response, "headers", None) else None
        if not location:
            return response

        response.close()
        next_url = urljoin(current_url, location)
        if redirect_count >= max_redirects:
            raise requests.TooManyRedirects(f"Exceeded {max_redirects} redirects")
        current_url = next_url

    raise requests.TooManyRedirects(f"Exceeded {max_redirects} redirects")


def request_trusted_https_url(
    method: str,
    url: str,
    *,
    allowed_hosts,
    max_redirects: int = 5,
    **kwargs,
):
    """Request a fixed trusted HTTPS service through the configured environment proxy.

    Every redirect is checked against the same exact hostname allowlist. This helper is
    intentionally separate from ``request_public_url`` so arbitrary URLs remain
    DNS-pinned and proxy-free.
    """
    request_method = str(method or "").upper()
    if request_method not in {"GET", "HEAD"}:
        raise ValueError("request_trusted_https_url only supports GET and HEAD")
    if not kwargs.get("verify", True):
        raise ValueError("HTTPS certificate verification cannot be disabled")

    normalized_hosts = frozenset(_canonical_hostname(host) for host in allowed_hosts)
    if not normalized_hosts:
        raise ValueError("allowed_hosts must not be empty")

    current_url = str(url or "").strip()
    seen = set()
    max_redirects = max(0, int(max_redirects))
    request_kwargs = dict(kwargs)
    request_kwargs.pop("allow_redirects", None)
    session = requests.Session()

    def attach_session_close(response):
        original_close = response.close
        session_closed = False

        def close_response_and_session():
            nonlocal session_closed
            try:
                return original_close()
            finally:
                if not session_closed:
                    session_closed = True
                    session.close()

        response.close = close_response_and_session
        return response

    try:
        for redirect_count in range(max_redirects + 1):
            if not is_trusted_https_url(current_url, normalized_hosts):
                raise UnsafeUrlError("Trusted request URL must remain HTTPS on an allowed host")
            if current_url in seen:
                raise requests.TooManyRedirects("Redirect loop detected")
            seen.add(current_url)

            response = session.request(
                request_method,
                current_url,
                allow_redirects=False,
                **request_kwargs,
            )
            if response.status_code not in REDIRECT_STATUS_CODES:
                return attach_session_close(response)

            location = response.headers.get("Location") if getattr(response, "headers", None) else None
            if not location:
                return attach_session_close(response)

            response.close()
            next_url = urljoin(current_url, location)
            if redirect_count >= max_redirects:
                raise requests.TooManyRedirects(f"Exceeded {max_redirects} redirects")
            current_url = next_url
    except Exception:
        session.close()
        raise

    session.close()
    raise requests.TooManyRedirects(f"Exceeded {max_redirects} redirects")
