"""Core library functions for running Python functions dynamically."""

import ast
import importlib.util
from pathlib import Path
from typing import Any
import sys

_MISSING = object()


def load_module(path: str | Path):
    """Load a Python module from a file path safely."""
    file_path = Path(path).resolve()
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    if file_path.suffix != ".py":
        raise ValueError(f"Target file must be a Python (.py) file: {path}")

    spec = importlib.util.spec_from_file_location("target", str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load Python file: {path}")

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_fn(path: str | Path, func: str, *args: Any, **kwargs: Any) -> Any:
    """Run FUNC from the Python file PATH with the given arguments and return its result."""
    if func.startswith("_"):
        raise PermissionError(f"Access to private function '{func}' is not allowed")

    mod = load_module(path)
    if not hasattr(mod, func):
        raise AttributeError(f"'{func}' not found in {path}")

    fn = getattr(mod, func)
    if not callable(fn):
        raise TypeError(f"'{func}' in {path} is not callable")

    return fn(*args, **kwargs)


def parse_literal(value: Any) -> Any:
    """Safely parse literal expressions using ast.literal_eval."""
    if not isinstance(value, str):
        return value
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value
