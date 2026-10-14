# Static Code Analysis – Reflection

## 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, style violations, and maintainability problems early in development.

## 2. What did Pylint, Bandit, and Flake8 identify?

Pylint identified code-quality problems such as missing docstrings, poor naming, unused variables, and unsafe coding practices. Bandit detected security risks including `eval()`, MD5 hashing, insecure random-number generation, and shell execution. Flake8 identified formatting issues, unused imports, long lines, and incorrect exception handling.

## 3. Which issues were most important, and how were they fixed?

The most important issues were unsafe expression evaluation, weak hashing, shell command execution, and insecure token generation. These were addressed by using a validated numeric multiplier, SHA-256, ordinary Python output, and the `secrets` module. Other fixes included safer file handling, improved exception handling, and removal of unused code.

## 4. How does static analysis improve software quality?

Static analysis helps developers detect problems before deployment. It improves readability, consistency, maintainability, and security. Running the tools again after applying fixes also provides evidence that the code has improved.