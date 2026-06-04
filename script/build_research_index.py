import sys

from src.cli import main


if __name__ == "__main__":
    print(
        "[DEPRECATED] Use `python script/paperbrain.py index ...` instead of `python script/build_research_index.py ...`.",
        file=sys.stderr,
    )
    raise SystemExit(main(["index"] + sys.argv[1:]))
