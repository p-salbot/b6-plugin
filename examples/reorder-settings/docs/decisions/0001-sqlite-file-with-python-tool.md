# 0001 The reorder settings live in one SQLite file, used through a small Python tool

Date: 2026-11-17

## Decision

The data is stored in a single SQLite database file on the owner's PC and is read and written only through a small Python command-line tool. The data is not edited in Excel.

## Reason

SQLite gives all-or-nothing saving and can enforce rules (no duplicate items, no invalid values) without extra code, which fixes the lost-item problem of the old tool. It needs no Access, comes with Python, and is widely known, so another person can maintain it.

## Alternative considered

- Plain CSV file with a Python tool: rejected because safe saving would have to be built by hand, and editing the file in Excel can quietly damage the data (for example, leading zeros in item numbers).
- Keep Access and only fix and document the VBA: rejected because others would still need Access and VBA skills, which is the main problem.

## What would change it

Several people needing to work with the data at the same time, or the data needing to live inside another system.
