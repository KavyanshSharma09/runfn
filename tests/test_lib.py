from pathlib import Path
import pytest
import runfn

SAMPLE = str(Path(__file__).parent.parent / "sample.py")


def test_library_import():
    assert hasattr(runfn, "run")
    assert hasattr(runfn, "run_fn")
    assert runfn.__version__ == "0.1.0"


def test_library_call():
    val = runfn.run(SAMPLE, "add", 3, 4)
    assert val == 7


def test_library_greet():
    val = runfn.run(SAMPLE, "greet", name="Sam")
    assert val == "Hello Sam"


def test_library_missing_func():
    with pytest.raises(AttributeError):
        runfn.run(SAMPLE, "not_existing")


def test_library_private_func_blocked():
    with pytest.raises(PermissionError):
        runfn.run(SAMPLE, "_private_func")


def test_library_non_callable():
    with pytest.raises(TypeError):
        runfn.run(SAMPLE, "SECRET_CONSTANT")


def test_library_non_py_file():
    license_file = str(Path(__file__).parent.parent / "LICENSE")
    with pytest.raises(ValueError):
        runfn.run(license_file, "add")
