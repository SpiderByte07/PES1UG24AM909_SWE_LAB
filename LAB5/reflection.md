# Lab 5 – Reflection

**1. Which issues were the easiest to fix, and which were the hardest?**
The easiest were the mechanical ones: unused imports and variables, trailing whitespace, `!= None`, and renaming `closeTicket`. Flake8 gives the exact line and the fix is obvious. The hardest were the ones that need a design decision, such as replacing the bare `except`/`pass` (what should happen when the id is unknown?) and avoiding `global` in `load_tickets`. The `KeyError` crash was also hard because no tool reported it, so I only found it by running the program with input `99`.

**2. Did the static analysis tools report any false positives?**
Nothing was strictly wrong, but some warnings are judgement calls. Pylint's "too many arguments" (R0913) on `create_ticket` is a design opinion: the arguments all belong to a ticket, so I kept them. The Bandit `eval` finding was valid in principle, but the code only ran when an environment variable was set, so the real risk was low. I still removed it because there was no reason to keep it.

**3. How would you integrate static analysis into a real development workflow?**
Run Flake8 and Pylint as a pre-commit hook so style problems never reach the repo. Run all three tools in CI (GitHub Actions) on every pull request, and fail the build on Bandit medium/high findings or a Pylint score below a threshold. Keep configuration in the repo (`.pylintrc`, `setup.cfg`/`tox.ini`) so the whole team uses the same rules, and use targeted `# pylint: disable=` comments with a reason when a warning is deliberately ignored.

**4. What tangible improvements did you see in code quality, readability, and security?**
The Pylint score rose from 5.00 to 9.85, Flake8 went from 12 warnings to 0, and Bandit went from 2 findings to 0. Security improved because `eval` and the silent `except: pass` are gone. Reliability improved because the program no longer crashes on an unknown ticket id, the audit log is no longer shared between calls, and ids no longer collide after loading from file. Readability improved with docstrings, consistent snake_case names, shorter lines and `with` blocks for files. Static analysis does not find everything, though: the crash and the id collision came from running and thinking about the code, not from the tools.
