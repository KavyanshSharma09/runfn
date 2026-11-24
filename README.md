# runfn

Run any function in a Python file straight from the terminal, check its output, and time it. No edits to your code required. Built with [Google Fire](https://github.com/google/python-fire).

---

## Features

- **Zero-Boilerplate:** Run any function directly from any `.py` file without writing CLI wrappers or `if __name__ == '__main__':` blocks.
- **Output Assertions:** Use `--expect=VALUE` to assert expected results (supports literal values like numbers, booleans, lists, dicts, strings, and `None`).
- **Execution Timing:** Benchmark execution time in milliseconds with `--time_it`.
- **Built-in Safety:** Prevents invocation of private/internal attributes (`_...`), verifies callables, and checks file extensions.
- **CI/CD Friendly:** Deterministic exit codes for easy integration into test pipelines and scripts.

---

## Installation

```bash
pip install runfn
```

For development and running tests locally:

```bash
pip install -e ".[dev]"
```

---

## Usage

### As a Python Library

```python
import runfn

# Call any function dynamically and get its return value
result = runfn.run("myfile.py", "add", 2, 5)
print(result)  # 7

# With keyword arguments
greeting = runfn.run("myfile.py", "greet", name="Sam")
print(greeting)  # 'Hello Sam'
```

### From the Command Line (CLI)

```bash
runfn myfile.py add 2 5
# Output:
# Result: 7
```

### Keyword Arguments

```bash
runfn myfile.py greet --name=Sam
# Output:
# Result: 'Hello Sam'
```

### Assertions (`--expect`)

Compare the returned value against an expected literal:

```bash
runfn myfile.py add 2 5 --expect=7
# Output:
# Result: 7
# PASS

runfn myfile.py add 2 5 --expect=8
# Output:
# Result: 7
# FAIL (expected 8)
```

Functions returning `None` can also be checked:

```bash
runfn myfile.py log_message "Hello" --expect=None
# Output:
# Result: None (function has no return value)
# PASS
```

### Execution Timing (`--time_it`)

Measure execution time of your function call:

```bash
runfn myfile.py add 2 5 --expect=7 --time_it
# Output:
# Result: 7
# PASS
# Time: 0.042 ms
```

---

## Exit Codes

| Exit Code | Meaning |
| :--- | :--- |
| **0** | Success (function ran and any `--expect` assertion passed). |
| **1** | Function execution failed or `--expect` assertion failed. |
| **2** | CLI / Target error (file not found, invalid `.py` extension, function not found, private attribute access, or non-callable). |

---

## Limitations & Safety

- **CLI Flag Collision:** When using the CLI (`runfn ...`), target functions cannot have parameters named `expect` or `time_it` because these are reserved runner flags. *(This restriction does not apply when importing `runfn` as a Python library).*
- **Private Attribute Protection:** Functions or attributes starting with `_` and non-callable attributes cannot be called.
- **File Type Validation:** Only valid `.py` files can be executed.
- **CLI Type Parsing:** The CLI automatically parses numbers, booleans, and collections (via Google Fire). To pass literal strings that look like numbers or booleans, enclose them in nested quotes (e.g. `' "123" '`).

---

## Running Tests

Run the test suite with `pytest`:

```bash
pytest
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

