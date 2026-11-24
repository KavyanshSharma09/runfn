import ast
import importlib.util
from pathlib import Path
import sys
import time

import fire

_MISSING = object()


def _load(path):
    file_path = Path(path).resolve()
    if not file_path.is_file():
        print(f"Error: File not found: {path}")
        sys.exit(2)
    if file_path.suffix != ".py":
        print(f"Error: Target file must be a Python (.py) file: {path}")
        sys.exit(2)

    try:
        spec = importlib.util.spec_from_file_location("target", str(file_path))
        if spec is None or spec.loader is None:
            print(f"Error: Cannot load Python file: {path}")
            sys.exit(2)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:
        print(f"Error loading module {path}: {e}")
        sys.exit(2)


def _parse(value):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value


def run(path, func, *args, expect=_MISSING, time_it=False, **kwargs):
    """Run FUNC from the Python file PATH with the given arguments."""
    if func.startswith("_"):
        print(f"Error: Access to private function '{func}' is not allowed")
        sys.exit(2)

    mod = _load(path)
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
        expected = _parse(expect) if isinstance(expect, str) else expect
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


def main():
    fire.Fire(run)


if __name__ == "__main__":
    main()
