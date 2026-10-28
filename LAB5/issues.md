# Lab 5 – Issues Found in `support_ticket_tracker.py`

Line numbers refer to the **original** file. Sorted by severity (high/medium first).
Results: Pylint **5.00 → 9.85/10**, Flake8 **12 → 0** warnings, Bandit **2 → 0** issues.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Use of `eval()` (Bandit B307, Pylint W0123) | Security (Medium) | 91–92 | `eval()` executes arbitrary code; a "demo" gated only by an env var is an injection risk if the string ever becomes dynamic. | Removed the unsafe demo block (and the then-unused `os` import). If parsing was needed, use `ast.literal_eval`. |
| Crash on unknown ticket id (`KeyError`) | Bug (High) | 29–31, 66–67, 70–71 | Entering id `99` at the prompt crashes the program with a traceback; `update_status` and `is_open` crash the same way. No tool flags this. | Check `ticket_id in TICKETS` first; functions return `False`/`None`, and `main()` prints "No ticket with id …". Renamed to `close_ticket` and made it use `update_status`. |
| Mutable default argument `audit_log=[]` (Pylint W0102) | Bug (Medium) | 10 | The list is created once and shared across every call, so audit entries from unrelated calls leak together. | Default to `None`, create a new list inside the function. |
| Bare `except:` + `pass` (Bandit B110, Flake8 E722, Pylint W0702) | Security/Bug (Low–Medium) | 22–26 | Swallows every error (even `KeyboardInterrupt`) silently, hiding real problems. | Replaced by an explicit `if ticket_id not in TICKETS: return False` check (earlier commit used `except KeyError`). |
| Duplicate ticket ids after reload | Bug (Medium) | 12 | `ticket_id = len(TICKETS) + 1` collides if tickets are loaded from file with gaps (e.g. ids 1 and 3 → new id `3` overwrites ticket 3). | Use `max(existing ids, default=0) + 1`. |
| File handles not closed safely, no encoding (Pylint R1732, W1514) | Quality (Medium) | 46–48, 53–55 | `open()`/`close()` leaks the handle if `write` raises; encoding depends on the OS default. | `with open(..., encoding="utf-8")` and `json.dump` / `json.load`. |
| `global TICKETS` (Pylint W0603) | Design (Medium) | 52 | Rebinding a module global in a function is hard to reason about. | Mutate in place: `TICKETS.clear()` then `TICKETS.update(loaded)`. |
| Unused argument `notify` (W0613) | Quality (Low) | 20 | Parameter is never used, which misleads callers. | Removed it. |
| Unused imports `sys`, `random` (Flake8 F401, Pylint W0611) | Style (Low) | 4–5 | Dead imports. | Removed. |
| Unused variable `count` (Flake8 F841, Pylint W0612) | Quality (Low) | 84 | Assigned, never used. | Removed. |
| `!= None` comparison (Flake8 E711, Pylint C0121/R1714) | Style/Bug (Low) | 37 | Should use identity. Also `priority` was tested by truthiness while `status` by `None`, which is inconsistent. | `is not None` for both filters. |
| Lines > 79 chars (Flake8 E501, Pylint C0301) | Style (Low) | 10, 14, 63, 71, 79, 80 | Hard to read and review. | Wrapped arguments, dict literal split over lines. |
| Trailing whitespace (Flake8 W291, Pylint C0303) | Style (Low) | 84 | Stray spaces. | Removed. |
| Function name `closeTicket` (Pylint C0103) | Style (Low) | 66 | Not snake_case, inconsistent with other functions. | Renamed `close_ticket`. |
| Missing docstrings (Pylint C0114/C0116) | Style (Low) | 1, all functions | No documentation. | Added module and function docstrings. |
| f-string / `%` in logging and string building (C0209, W1203) | Style (Low) | 16, 85 | `%` formatting; f-string in logging evaluates eagerly. | f-string for the audit message; lazy `logging.info("... %d", n)`. |
| Simplifiable if/else, `len()` truthiness (R1703, R1705, C1802) | Quality (Low) | 60, 71–74 | Verbose code returning `True`/`False`. | `return ticket is not None and ticket["status"] in OPEN_STATUSES`; `if not TICKETS`. |
| Too many arguments (R0913/R0917) | Design (Low) | 10 | 6 args in `create_ticket`. | Partly mitigated by making optional args keyword-only. **Left as is** (9.85/10 is above the 9.5 target). |
