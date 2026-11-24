"""runfn: Run any Python function from the terminal or programmatically."""

from runfn.core import load_module, parse_literal, run_fn

run = run_fn

__version__ = "0.1.0"
__all__ = ["run", "run_fn", "load_module", "parse_literal", "__version__"]
