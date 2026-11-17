# Review 4: Step 2, Commands (fix round 1)

## Fix brief criteria (2-commands-fix1.md)

| Criterion | Status | Evidence |
|---|---|---|
| R-004 Number input: only optional sign + ASCII digits 0-9 after `strip()` are converted; otherwise text passed on, storage gives field-naming message, data unchanged | met (code) | `reorder/cli.py:10` `_WHOLE_NUMBER = re.compile(r"[+-]?[0-9]+")`, `cli.py:17` `fullmatch(text.strip())`, else text returned unchanged (`cli.py:19`). Trial: `save B-1 --min 1 --reorder 1_0 --supplier Acme` gave `Reorder quantity must be a whole number 1 or more`, exit 1; `--min "５"` (U+FF15) gave `Minimum stock must be a whole number 0 or more`, exit 1; `--min " 5 "` saved with minimum stock 5, exit 0. |
| Fix 1 tests: `--reorder 1_0` refused, `--min ５` refused (message names field, exit 1, data unchanged), `--min " 5 "` works | not met | `test_r004_underscore_in_reorder_is_refused` (`tests/test_cli.py:90-91`) and `test_r004_spaces_around_number_are_allowed` (`:96-99`) are correct. But `test_r004_full_width_digit_in_min_is_refused` (`:93-94`) passes the ASCII text `"Ff15"` (checked with `od -c`: bytes `F f 1 5`), not the full-width digit `５` / `"５"`. `Ff15` is refused by any conversion, including the old plain `int()`, so this test does not check the fixed defect. See finding 1. |
| R-005 / Fix 2: `configure_output(*streams)` in `cli.py` reconfigures to `encoding="utf-8"`, `errors="replace"`, one-line comment why | met | `cli.py:22-25`; docstring "Write in UTF-8 and never fail on a character (a pipe on Windows uses cp1252)." |
| `__main__.py` calls it with `sys.stdout`, `sys.stderr` before `main()` | met | `reorder/__main__.py:3-4`. |
| Fix 2 test: cp1252 `TextIOWrapper(BytesIO())` streams, writing `Łódź` and `Müller` does not raise and gives UTF-8 bytes; no subprocess | met | `test_r005_output_is_utf_8_and_never_fails` (`test_cli.py:143-151`) uses `"Łódź Müller"` on both streams and compares with `text.encode("utf-8")`; no subprocess in the file. |
| R-010 Standard library only | met | `cli.py` imports `argparse`, `re`, `sys`, `reorder.storage`; `__main__.py` `sys`, `reorder.cli`; tests `contextlib`, `io`, `unittest`. |
| How to verify 1: `python -m unittest -v` all pass | met | Ran in project root: `Ran 33 tests ... OK` (13 storage + 20 CLI). |
| How to verify 2: trial in scratch copy | met | `save L-1 ... --supplier "Łódź" > out.txt`: exit 0, no traceback, `out.txt` = `Saved L-1: ... supplier Łódź`. `show L-1 > out.txt`: exit 0, four lines, UTF-8 bytes of `Łódź` present (`305 201 303 263 d 305 272`). `--reorder 1_0`: field message, exit 1. `list | od -c`: UTF-8 bytes for `Müller` and `Łódź`. |
| How to verify 3: no `reorder.db` in root; `__pycache__` removed | met | Before my test run, `find` listed no `.pyc` and no `reorder.db`. I removed the caches my test run made and my scratch copy, `reorder.db` and `out.txt`; final `find` shows none. |
| Only listed files changed; `storage.py`, `test_storage.py`, `docs/decisions/` untouched | met | Project is untracked in git, so change times were compared: `reorder/cli.py`, `reorder/__main__.py`, `docs/architecture.md` (20:09:50) and `tests/test_cli.py` (20:10:18) are after the fix brief (20:09:32). `storage.py`, `test_storage.py` (20:01:19), `docs/decisions/0001` (19:57) and `.gitignore` (20:05) are older. |

## Original step-2 brief criteria (2-commands.md)

| Criterion | Status | Evidence |
|---|---|---|
| R-001 show / not found only | met | `cli.py:46-55`; tests `test_r001_*` pass (stderr exactly `Item 'X-1' not found.\n`, stdout empty). |
| R-002 save then show; save again replaces, one row | met | `cli.py:58-65`; tests `test_r002_*` pass. |
| R-004 empty item/supplier, min >= 0, reorder >= 1, field message, data unchanged | met | Tests `test_r004_*` pass (empty supplier, empty item, `-1`, `abc`, `0`, `1.5`, `1_0`, new bad item not stored); trials above. Test gap for `５` see finding 1. |
| R-005 `O'Brien` exact; other special characters work | met | `test_r005_apostrophe_in_supplier_is_kept`; trial outputs of `Łódź`/`Müller` in UTF-8. |
| R-006 sorted aligned table; `No items.` | met | `cli.py:68-79`; `test_r006_*` pass. |
| R-007 case-insensitive show and update | met | `test_r007_*` pass. |
| R-010 standard library | met | See above. |
| Design: `main(argv=None, store=None)`, opens/closes default store | met | `cli.py:85-98`. |
| Design: `__main__.py` only calls `main()` and exits | met | `__main__.py:1-4`; the added `configure_output` call is required by the fix brief. |
| Design: argparse sub-commands, required options | met | `cli.py:28-43`. |
| Design: numbers read as text, own conversion, field message | met | `cli.py:13-19`, `37-39` (no `type=`). |
| Design: output formats | met | Tests compare exact strings (`test_cli.py:32-37`, `49-50`). |
| Design: errors to stderr exit 1, usage exit 2, success exit 0 | met | Tests and trials; the earlier crash after save is gone (trial `save ... Łódź > out.txt` exit 0). |
| Tests: unittest only, in-memory store, named after requirements | met | `test_cli.py:12-151`. |
| `.gitignore` has `reorder.db`, `__pycache__/`, existing line | met | Unchanged since review 3 (20:05). |
| `docs/architecture.md` Command line row, only what is in code | met | See Architecture check. |

## Earlier findings

| Finding | Resolved? | Evidence |
|---|---|---|
| 1. `--min`/`--reorder` conversion too lenient (`1_0`, full-width digits) | resolved in code; test incomplete | `cli.py:10-19` and trials (`1_0`, `５` both refused, exit 1). The required full-width test does not use a full-width digit (finding 1 below). |
| 2. Output with special characters crashes when redirected/piped on Windows | resolved | `configure_output` (`cli.py:22-25`) called in `__main__.py:3`; trials `save`/`show`/`list` to file and pipe: exit 0, UTF-8 bytes, no traceback; test `test_r005_output_is_utf_8_and_never_fails` passes. |
| 3. Label "Reorder quantity" vs "Reorder qty" | resolved (accepted, no fix needed) | Accepted by the main chat; unchanged and still as described. |
| 4. Not-found message repeats spaces | resolved (accepted, no fix needed) | Accepted by the main chat; `cli.py:49` unchanged. |

## Architecture check

Matches. The "Command line" row (`docs/architecture.md:12`) now says `__main__.py` calls `configure_output` so standard output and error are always UTF-8 and replace a character instead of failing (`cli.py:22-25`, `__main__.py:3`), and that `--min`/`--reorder` are converted only if, after trimming, they are an optional sign and the digits 0-9 (`cli.py:10-19`). No plans described. Other rows unchanged and still correct.

## Findings

1. `tests/test_cli.py:93-94`: `test_r004_full_width_digit_in_min_is_refused` passes `minimum="Ff15"` (plain ASCII letters and digits, verified with `od -c`), not the full-width digit `５` (`"５"`) the fix brief asks for. The test would also pass with the old plain `int()` code, so it does not guard the fix. Fix: use `minimum="５"` (escape keeps the file ASCII and readable).
2. Note: `ctx/plans/2026-11-17-reorder-cli/scratch/.gitignore` exists now with the single line `*` (`od -c`: `* \n`). Its change time (20:10:43) is after the worker's last file (20:10:18), which fits the main chat's rewrite; I found no evidence that the worker deleted it, so no finding against the worker.

## Verdict

FIX
