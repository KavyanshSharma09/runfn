import subprocess, sys, pathlib

SAMPLE = str(pathlib.Path(__file__).parent.parent / "sample.py")

def run(*args):
    return subprocess.run(
        [sys.executable, "-m", "runfn.cli", SAMPLE, *args],
        capture_output=True, text=True,
    )

def test_result():
    assert "Result: 7" in run("add", "2", "5").stdout

def test_pass():
    r = run("add", "2", "5", "--expect=7")
    assert "PASS" in r.stdout and r.returncode == 0

def test_fail_exit_code():
    r = run("add", "2", "5", "--expect=8")
    assert "FAIL" in r.stdout and r.returncode == 1

def test_string_kwarg():
    r = run("greet", "--name=Sam", "--expect=Hello Sam")
    assert "PASS" in r.stdout

def test_time():
    assert "Time:" in run("add", "2", "5", "--time_it").stdout

def test_missing_function():
    assert run("nope").returncode == 2

def test_no_return():
    r = run("say_hi", "Sam")
    assert "Hi Sam" in r.stdout
    assert "no return value" in r.stdout and r.returncode == 0

def test_expect_none_passes():
    r = run("say_hi", "Sam", "--expect=None")
    assert "PASS" in r.stdout and r.returncode == 0

def test_expect_value_but_no_return_fails():
    r = run("say_hi", "Sam", "--expect=5")
    assert "returned nothing" in r.stdout and r.returncode == 1

def test_private_attribute_blocked():
    r = run("_private_func")
    assert r.returncode == 2
    assert "private" in r.stdout or "private" in r.stderr

def test_non_callable_blocked():
    r = run("SECRET_CONSTANT")
    assert r.returncode == 2
    assert "not callable" in r.stdout or "not callable" in r.stderr

def test_non_py_file_blocked():
    license_file = str(pathlib.Path(__file__).parent.parent / "LICENSE")
    r = subprocess.run(
        [sys.executable, "-m", "runfn.cli", license_file, "add"],
        capture_output=True, text=True,
    )
    assert r.returncode == 2
    assert "must be a Python (.py) file" in r.stdout or "must be a Python (.py) file" in r.stderr
