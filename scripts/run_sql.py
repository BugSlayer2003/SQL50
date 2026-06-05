from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from collections import Counter
from pathlib import Path


SECTION_PREFIX = "-- @"


def parse_sections(sql_text: str) -> dict[str, tuple[str, str]]:
    sections: dict[str, tuple[list[str], str]] = {}
    current = "solution"

    for raw_line in sql_text.splitlines():
        stripped = raw_line.strip()
        if stripped.lower().startswith(SECTION_PREFIX):
            header = stripped[len(SECTION_PREFIX) :].strip()
            if not header:
                continue
            name, _, options = header.partition(" ")
            current = name.lower()
            sections.setdefault(current, ([], options.strip().lower()))
            continue

        lines, options = sections.setdefault(current, ([], ""))
        lines.append(raw_line)
        sections[current] = (lines, options)

    return {name: ("\n".join(lines).strip(), options) for name, (lines, options) in sections.items()}


def strip_comment_prefix(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("--"):
            line = stripped[2:].lstrip()
        lines.append(line)
    return "\n".join(lines).strip()


def has_sql_statement(text: str) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("--"):
            return True
    return False


def parse_expected(text: str) -> tuple[list[str], list[tuple[str, ...]]]:
    clean = strip_comment_prefix(text)
    if not clean:
        return [], []

    rows = [
        [cell.strip() for cell in row]
        for row in csv.reader(clean.splitlines(), delimiter="|")
        if row and any(cell.strip() for cell in row)
    ]
    if not rows:
        return [], []
    return rows[0], [tuple(row) for row in rows[1:]]


def fetch_result(connection: sqlite3.Connection, solution_sql: str) -> tuple[list[str], list[tuple[str, ...]]]:
    cursor = connection.execute(solution_sql)
    headers = [description[0] for description in cursor.description or []]
    rows = []
    for row in cursor.fetchall():
        rows.append(tuple("NULL" if value is None else str(value) for value in row))
    return headers, rows


def print_table(headers: list[str], rows: list[tuple[str, ...]]) -> None:
    if not headers:
        print("(query returned no columns)")
        return

    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    def fmt(values: list[str] | tuple[str, ...]) -> str:
        return " | ".join(str(value).ljust(widths[index]) for index, value in enumerate(values))

    print(fmt(headers))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(fmt(row))
    print(f"\n{len(rows)} row(s)")


def compare(
    actual_headers: list[str],
    actual_rows: list[tuple[str, ...]],
    expected_headers: list[str],
    expected_rows: list[tuple[str, ...]],
    unordered: bool,
) -> bool:
    if actual_headers != expected_headers:
        return False
    if unordered:
        return Counter(actual_rows) == Counter(expected_rows)
    return actual_rows == expected_rows


def run_file(path: Path) -> int:
    sql_text = path.read_text(encoding="utf-8")
    sections = parse_sections(sql_text)

    setup_sql = sections.get("setup", ("", ""))[0]
    solution_sql = sections.get("solution", ("", ""))[0].strip().rstrip(";")
    expected_sql, expected_options = sections.get("expected", ("", ""))

    if not has_sql_statement(solution_sql):
        print(f"No solution SQL found in {path}")
        print("Put your final SELECT under the '-- @solution' section.")
        return 2

    connection = sqlite3.connect(":memory:")
    try:
        if setup_sql:
            connection.executescript(setup_sql)
        headers, rows = fetch_result(connection, solution_sql)
    except sqlite3.Error as error:
        print(f"SQLite error while running {path}:")
        print(error)
        return 1
    finally:
        connection.close()

    print(f"\n== {path} ==")
    print_table(headers, rows)

    if expected_sql:
        expected_headers, expected_rows = parse_expected(expected_sql)
        unordered = "unordered" in expected_options
        ok = compare(headers, rows, expected_headers, expected_rows, unordered)
        mode = "unordered" if unordered else "ordered"
        print(f"\nExpected check ({mode}): {'PASS' if ok else 'FAIL'}")
        if not ok:
            print("\nExpected:")
            print_table(expected_headers, expected_rows)
            return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a LeetCode-style SQL practice file with SQLite.")
    parser.add_argument("file", type=Path, help="Path to the SQL practice file.")
    args = parser.parse_args()

    if not args.file.exists():
        print(f"File not found: {args.file}")
        return 2

    return run_file(args.file)


if __name__ == "__main__":
    sys.exit(main())
