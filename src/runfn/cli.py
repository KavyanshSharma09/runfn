"""CLI entry point for runfn."""

from pathlib import Path
import sys
import time
from typing import Any

import fire

from runfn.core import _MISSING, load_module, parse_literal, run_fn


def run(path: str, func: str, *args: Any, expect: Any = _MISSING, time_it: bool = False, **kwargs: Any) -> None:
    """Run FUNC from the Python file PATH with the given arguments."""
    if func.startswith("_"):
        print(f"Error: Access to private function '{func}' is not allowed")
        sys.exit(2)

    try:
        mod = load_module(path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(2)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"Error loading module {path}: {e}")
        sys.exit(2)

    if not hasattr(mod, func):
        print(f"Error: '{func}' not found in {path}")
        sys.exit(2)

    fn = getattr(mod, func)
    if not callable(fn):
        print(f"Error: '{func}' in {path} is not callable")
        sys.exit(2)

    start = time.perf_counter()
    try:
        result = fn(*args, **kwargs)
    except Exception as e:
        print(f"Error running '{func}': {e}")
        sys.exit(1)
    elapsed = time.perf_counter() - start

    if result is None:
        print("Result: None (function has no return value)")
    else:
        print(f"Result: {result!r}")

    failed = False
    if expect is not _MISSING:
        expected = parse_literal(expect)
        if result == expected:
            print("PASS")
        else:
            note = ", but the function returned nothing" if result is None else ""
            print(f"FAIL (expected {expected!r}{note})")
            failed = True

    if time_it:
        print(f"Time: {elapsed * 1000:.3f} ms")

    if failed:
        sys.exit(1)


def main() -> None:
    fire.Fire(run)


if __name__ == "__main__":
    main()
