import socket
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main as pipeline  # noqa: E402
from src.network_safety import (  # noqa: E402
    TRUSTED_ARXIV_HOSTS,
    UnsafeUrlError,
    _PinnedHTTPAdapter,
    _PinnedHTTPConnection,
    _resolve_public_target,
    configured_http_proxy,
    request_public_url,
    request_trusted_https_url,
    validate_public_http_url,
)


def resolver_for(addresses):
    def resolve(host, port, type=socket.SOCK_STREAM):
        return [(socket.AF_INET6 if ":" in address else socket.AF_INET, type, 6, "", (address, port)) for address in addresses]

    return resolve


class FakeResponse:
    def __init__(self, status_code=200, headers=None, chunks=None, url="https://public.example/file.pdf"):
        self.status_code = status_code
        self.headers = headers or {}
        self.chunks = list(chunks or [])
        self.url = url
        self.closed = False
        self.iterated = False

    def iter_content(self, chunk_size=8192):
        self.iterated = True
        yield from self.chunks

    def close(self):
        self.closed = True


class PublicUrlValidationTest(unittest.TestCase):
    def test_rejects_non_public_literal_addresses_and_unsafe_schemes(self):
        urls = [
            "http://127.0.0.1/admin",
            "http://[::1]/admin",
            "http://10.0.0.1/",
            "http://172.16.0.1/",
            "http://192.168.1.1/",
            "http://169.254.169.254/latest/meta-data/",
            "http://0.0.0.0/",
            "http://224.0.0.1/",
            "http://192.0.2.1/",
            "http://100.64.0.1/",
            "file:///etc/passwd",
            "ftp://public.example/file.pdf",
            "https://user:secret@public.example/file.pdf",
            "http://public.example:0/file.pdf",
        ]
        for url in urls:
            with self.subTest(url=url), self.assertRaises(UnsafeUrlError):
                validate_public_http_url(url)

    def test_requires_every_dns_answer_to_be_public(self):
        self.assertEqual(
            validate_public_http_url(
                "https://public.example/file.pdf",
                resolver=resolver_for(["93.184.216.34", "8.8.8.8"]),
            ),
            "https://public.example/file.pdf",
        )
        for addresses in (["10.0.0.1"], ["93.184.216.34", "127.0.0.1"]):
            with self.subTest(addresses=addresses), self.assertRaises(UnsafeUrlError):
                validate_public_http_url(
                    "https://public.example/file.pdf",
                    resolver=resolver_for(addresses),
                )

    def test_blocks_private_redirect_before_second_request(self):
        first = FakeResponse(status_code=302, headers={"Location": "http://127.0.0.1/admin"})
        calls = []

        def requester(method, target, **kwargs):
            calls.append(target.url)
            return first

        with patch("src.network_safety._request_pinned_once", side_effect=requester), \
             self.assertRaises(UnsafeUrlError):
            request_public_url(
                "GET",
                "https://public.example/start",
                resolver=resolver_for(["93.184.216.34"]),
            )

        self.assertEqual(calls, ["https://public.example/start"])
        self.assertTrue(first.closed)

    def test_follows_and_revalidates_public_relative_redirect(self):
        first = FakeResponse(status_code=302, headers={"Location": "/final"})
        final = FakeResponse(status_code=200)
        responses = iter([first, final])
        calls = []

        def requester(method, target, **kwargs):
            calls.append(target.url)
            return next(responses)

        with patch("src.network_safety._request_pinned_once", side_effect=requester):
            response = request_public_url(
                "HEAD",
                "https://public.example/start",
                resolver=resolver_for(["93.184.216.34"]),
            )

        self.assertIs(response, final)
        self.assertEqual(calls, ["https://public.example/start", "https://public.example/final"])
        self.assertTrue(first.closed)


class DnsPinnedTransportTest(unittest.TestCase):
    def test_connection_uses_validated_sockaddr_without_resolving_again(self):
        target = _resolve_public_target(
            "http://public.example/paper",
            resolver=resolver_for(["93.184.216.34"]),
        )
        fake_socket = MagicMock()
        connection = _PinnedHTTPConnection(
            host=target.hostname,
            port=target.port,
            timeout=1,
            pinned_endpoints=target.endpoints,
        )

        with patch("src.network_safety.socket.socket", return_value=fake_socket), \
             patch("src.network_safety.socket.getaddrinfo") as second_resolution:
            connected_socket = connection._new_conn()

        self.assertIs(connected_socket, fake_socket)
        second_resolution.assert_not_called()
        fake_socket.connect.assert_called_once_with(("93.184.216.34", 80))

    def test_https_pool_keeps_hostname_for_sni_and_certificate_matching(self):
        target = _resolve_public_target(
            "https://public.example/paper",
            resolver=resolver_for(["93.184.216.34"]),
        )
        adapter = _PinnedHTTPAdapter(target)
        try:
            connection = adapter._pinned_pool._new_conn()
            self.assertEqual(adapter._pinned_pool.host, "public.example")
            self.assertEqual(adapter._pinned_pool.assert_hostname, "public.example")
            self.assertEqual(connection.host, "public.example")
            self.assertEqual(connection.assert_hostname, "public.example")
            self.assertEqual(connection.server_hostname, "public.example")
            prepared = MagicMock(headers={"Host": "93.184.216.34", "Accept": "application/pdf"})
            adapter.add_headers(prepared)
            self.assertNotIn("Host", prepared.headers)
            self.assertEqual(prepared.headers["Accept"], "application/pdf")
        finally:
            adapter.close()

    def test_http_connection_generates_host_header_from_original_hostname(self):
        target = _resolve_public_target(
            "http://public.example/paper",
            resolver=resolver_for(["93.184.216.34"]),
        )
        sent = []

        class RecordingSocket:
            def sendall(self, data):
                sent.append(data)

        connection = _PinnedHTTPConnection(
            host=target.hostname,
            port=target.port,
            timeout=1,
            pinned_endpoints=target.endpoints,
        )
        with patch.object(connection, "_new_conn", return_value=RecordingSocket()):
            connection.request("HEAD", "/paper")

        wire_data = b"".join(sent)
        self.assertIn(b"Host: public.example\r\n", wire_data)
        self.assertNotIn(b"Host: 93.184.216.34", wire_data)

    def test_default_transport_disables_environment_proxies_and_host_override(self):
        sessions = []

        class FakeSession:
            def __init__(self):
                self.trust_env = True
                self.proxies = {"https": "http://environment-proxy.invalid"}
                self.adapters = {}
                self.mounts = []
                self.request_kwargs = None
                self.closed = False
                sessions.append(self)

            def mount(self, prefix, adapter):
                self.adapters[prefix] = adapter
                self.mounts.append((prefix, adapter))

            def request(self, method, url, **kwargs):
                self.request_kwargs = kwargs
                return FakeResponse(status_code=200, url=url)

            def close(self):
                self.closed = True
                for _, adapter in self.mounts:
                    adapter.close()

        with patch("src.network_safety.requests.Session", FakeSession):
            response = request_public_url(
                "GET",
                "https://public.example/paper",
                resolver=resolver_for(["93.184.216.34"]),
                headers={"Host": "127.0.0.1", "Accept": "application/pdf"},
            )

        self.assertEqual(len(sessions), 1)
        session = sessions[0]
        self.assertFalse(session.trust_env)
        self.assertEqual(session.proxies, {})
        self.assertEqual(session.request_kwargs["proxies"], {})
        self.assertFalse(session.request_kwargs["allow_redirects"])
        self.assertNotIn("Host", session.request_kwargs["headers"])
        self.assertEqual(session.request_kwargs["headers"]["Accept"], "application/pdf")
        response.close()
        self.assertTrue(session.closed)

    def test_redirect_is_resolved_again_and_pinned_to_its_own_address(self):
        addresses = {
            "first.example": "93.184.216.34",
            "second.example": "8.8.8.8",
        }

        def resolver(host, port, type=socket.SOCK_STREAM):
            return resolver_for([addresses[host]])(host, port, type=type)

        first = FakeResponse(status_code=302, headers={"Location": "https://second.example/final"})
        final = FakeResponse(status_code=200)
        responses = iter([first, final])
        pinned = []

        def fake_pinned_request(method, target, **kwargs):
            pinned.append((target.hostname, target.endpoints[0][3][0]))
            return next(responses)

        with patch("src.network_safety._request_pinned_once", side_effect=fake_pinned_request):
            response = request_public_url(
                "GET",
                "https://first.example/start",
                resolver=resolver,
            )

        self.assertIs(response, final)
        self.assertEqual(
            pinned,
            [("first.example", "93.184.216.34"), ("second.example", "8.8.8.8")],
        )
        self.assertTrue(first.closed)

    def test_https_certificate_verification_cannot_be_disabled(self):
        for verify in (False, 0, ""):
            with self.subTest(verify=verify), self.assertRaisesRegex(ValueError, "cannot be disabled"):
                request_public_url(
                    "GET",
                    "https://public.example/paper",
                    resolver=resolver_for(["93.184.216.34"]),
                    verify=verify,
                )


class TrustedProxyTransportTest(unittest.TestCase):
    class FakeSession:
        def __init__(self, responses):
            self.responses = iter(responses)
            self.calls = []
            self.closed = False

        def request(self, method, url, **kwargs):
            self.calls.append((method, url, kwargs))
            return next(self.responses)

        def close(self):
            self.closed = True

    def test_trusted_arxiv_redirect_stays_on_allowlist(self):
        first = FakeResponse(status_code=302, headers={"Location": "https://arxiv.org/pdf/2605.25802.pdf"})
        final = FakeResponse(status_code=200)
        session = self.FakeSession([first, final])

        with patch("src.network_safety.requests.Session", return_value=session):
            response = request_trusted_https_url(
                "GET",
                "https://export.arxiv.org/pdf/2605.25802.pdf",
                allowed_hosts=TRUSTED_ARXIV_HOSTS,
            )

        self.assertEqual([call[1] for call in session.calls], [
            "https://export.arxiv.org/pdf/2605.25802.pdf",
            "https://arxiv.org/pdf/2605.25802.pdf",
        ])
        self.assertTrue(first.closed)
        self.assertFalse(session.closed)
        response.close()
        self.assertTrue(session.closed)

    def test_trusted_arxiv_redirect_rejects_other_hosts(self):
        first = FakeResponse(status_code=302, headers={"Location": "https://example.com/file.pdf"})
        session = self.FakeSession([first])

        with patch("src.network_safety.requests.Session", return_value=session), \
             self.assertRaises(UnsafeUrlError):
            request_trusted_https_url(
                "GET",
                "https://arxiv.org/pdf/2605.25802.pdf",
                allowed_hosts=TRUSTED_ARXIV_HOSTS,
            )

        self.assertEqual(len(session.calls), 1)
        self.assertTrue(first.closed)
        self.assertTrue(session.closed)

    def test_edge_proxy_selection_prefers_https_and_ignores_socks(self):
        environment = {
            "HTTP_PROXY": "http://http-proxy.test:8080",
            "HTTPS_PROXY": "http://https-proxy.test:8081",
            "ALL_PROXY": "socks5://socks-proxy.test:1080",
        }
        self.assertEqual(configured_http_proxy(environment), "http://https-proxy.test:8081")
        self.assertIsNone(configured_http_proxy({"HTTPS_PROXY": "socks5://proxy.test:1080"}))


class PdfDownloadLimitTest(unittest.TestCase):
    def test_pdf_download_rejects_private_target_before_request(self):
        with tempfile.TemporaryDirectory() as tmp, patch("src.network_safety.requests.Session") as session:
            with self.assertRaises(pipeline.PDFUnsafeUrlError):
                pipeline.download_pdf(
                    "http://169.254.169.254/latest/meta-data/file.pdf",
                    "Paper",
                    destination_folder=tmp,
                    retries=1,
                )

        session.assert_not_called()

    def test_rejects_declared_oversized_pdf_without_writing(self):
        response = FakeResponse(headers={"Content-Length": "4096"}, chunks=[b"%PDF-1.4\n"])
        with tempfile.TemporaryDirectory() as tmp, \
             patch("main.request_public_url", return_value=response), \
             patch("main.time.sleep"):
            with self.assertRaises(pipeline.PDFDownloadTooLargeError):
                pipeline.download_pdf(
                    "https://public.example/file.pdf",
                    "Paper",
                    destination_folder=tmp,
                    retries=1,
                    max_bytes=2048,
                )
            self.assertEqual(list(Path(tmp).glob("*.pdf*")), [])

        self.assertFalse(response.iterated)
        self.assertTrue(response.closed)

    def test_rejects_stream_that_exceeds_limit_and_removes_partial_file(self):
        response = FakeResponse(chunks=[b"%PDF-1.4\n" + b"x" * 1500, b"y" * 1000])
        with tempfile.TemporaryDirectory() as tmp, \
             patch("main.request_public_url", return_value=response), \
             patch("main.time.sleep"):
            with self.assertRaises(pipeline.PDFDownloadTooLargeError):
                pipeline.download_pdf(
                    "https://public.example/file.pdf",
                    "Paper",
                    destination_folder=tmp,
                    retries=1,
                    max_bytes=2048,
                )
            self.assertEqual(list(Path(tmp).glob("*.pdf*")), [])

        self.assertTrue(response.iterated)
        self.assertTrue(response.closed)

    def test_accepts_pdf_at_exact_limit_and_closes_response(self):
        payload = b"%PDF-1.4\n" + b"x" * (2048 - len(b"%PDF-1.4\n"))
        response = FakeResponse(headers={"Content-Length": "2048"}, chunks=[payload])
        with tempfile.TemporaryDirectory() as tmp, patch("main.request_public_url", return_value=response):
            result = pipeline.download_pdf(
                "https://public.example/file.pdf",
                "Paper",
                destination_folder=tmp,
                retries=1,
                max_bytes=2048,
            )
            expected = Path(tmp) / pipeline._safe_pdf_filename(
                "Paper",
                "https://public.example/file.pdf",
            )
            self.assertEqual(result, str(expected))
            self.assertEqual(Path(result).stat().st_size, 2048)
            self.assertFalse(Path(f"{result}.part").exists())

        self.assertTrue(response.closed)

    def test_arxiv_pdf_uses_trusted_proxy_aware_transport(self):
        payload = b"%PDF-1.4\n" + b"x" * 2048
        response = FakeResponse(chunks=[payload])
        with tempfile.TemporaryDirectory() as tmp, \
             patch("main.PDF_CACHE_DIR", str(Path(tmp) / "cache")), \
             patch("main.PDF_COOLDOWN_PATH", str(Path(tmp) / "cache" / "cooldown.json")), \
             patch("main.request_trusted_https_url", return_value=response) as trusted, \
             patch("main.request_public_url") as public:
            result = pipeline.download_pdf(
                "https://arxiv.org/pdf/2605.25802.pdf",
                "Paper",
                destination_folder=tmp,
                retries=1,
            )

        self.assertTrue(Path(result).name.endswith(".pdf"))
        trusted.assert_called_once()
        public.assert_not_called()


if __name__ == "__main__":
    unittest.main()
