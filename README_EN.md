# 🛡️ Static Audit for Python Projects

This script performs a **basic static audit** of a Python project using popular tools for code quality checks, security analysis, and maintainability metrics.

## 🔍 What does it do?

It automatically runs the following tools:

- `flake8` – checks for PEP8 style violations and syntax errors.
- `bandit` – scans for common security issues in Python code.
- `pip-audit` – analyzes dependencies for known vulnerabilities (CVEs).
- `radon` – computes cyclomatic complexity and maintainability index.
- `black` – verifies code formatting according to Black standards.
- `isort` – checks if imports are correctly sorted.

The output is printed to the console and saved as a text file named:
```
audit_report_YYYYMMDD_HHMMSS.txt
```

## ⚙️ Installation

Make sure you have Python 3 installed, then install the required tools:

```bash
pip install flake8 bandit pip-audit radon black isort
```

## ▶️ Usage

```bash
python audit.py /path/to/your/project
```

- If no path is specified, the script analyzes the current directory.
- A text report will be automatically generated in the working directory.

### Example:

```bash
python audit.py ~/projects/my_app/
```

## 🧾 Sample Output

```
===== FLAKE8 (LINTER PEP8 & ERRORS) =====
Output:
main.py:10:1: F401 'os' imported but unused

[FAILED/WARNING] Flake8 exited with code 1. Check output above.

===== RADON - CYCLOMATIC COMPLEXITY =====
Output:
main.py - A (1.00)
utils.py - B (4.00)

[PASSED] Radon ran successfully.
```

## ⚠️ Limitations

- This is **not** a complete security or compliance audit.
- It does **not** check CI/CD pipelines, runtime behavior, or permission issues.
- May produce false positives or negatives.
- Requires external tools to be installed and available in your PATH.

## 📄 License

Distributed under the MIT License – see [LICENSE](LICENSE) for details.
