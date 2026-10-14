# Static Code Analysis – Issues Report

## 1. Overview

The original hospital patient management program was analyzed using Pylint, Bandit, and Flake8. The tools identified maintainability problems, potential security vulnerabilities, and formatting violations.

## 2. Issues Identified and Fixes Applied

| Issue | Severity | Tool | Fix Applied |
|---|---|---|---|
| Use of `os.system()` to execute a shell command | High | Bandit | Removed shell execution and used a normal Python print statement. |
| Use of MD5 hashing | High | Bandit | Replaced MD5 with SHA-256. |
| Use of `eval()` | Medium | Pylint, Bandit | Replaced expression evaluation with a validated numeric multiplier. |
| Insecure pseudo-random token generation | Low | Bandit | Replaced `random.randint()` with `secrets.randbelow()`. |
| Bare `except` with `pass` | Low | Pylint, Flake8 | Replaced broad exception handling with an explicit patient lookup and return value. |
| Mutable default list argument | Medium | Pylint | Changed the default to `None` and initialized the list inside the function. |
| Missing docstrings | Low | Pylint | Added module and function docstrings. |
| Unused imports and variables | Low | Pylint, Flake8 | Removed unused imports and variables. |
| Missing file encoding and context manager | Low | Pylint | Used `with open(..., encoding="utf-8")`. |
| Naming and formatting violations | Low | Pylint, Flake8 | Used snake_case names and corrected line lengths and final newline. |
| Hardcoded access key printed to the terminal | High – manual security observation | Manual review | Removed the hardcoded key and its print statement. |

*Severity labels are based on the tool findings where available; the manual observation is separately identified.*

## 3. Verification

After modifying the program, all three static analysis tools were run again against the corrected Python file.

- **Pylint:** Score above 9.5/10.
- **Bandit:** Zero reported security findings.
- **Flake8:** Zero reported violations.

## 4. Conclusion

The fixes improved code readability, maintainability, formatting, and security. Re-running the tools helped verify that the reported issues were addressed.