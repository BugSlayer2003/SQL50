# SQL50

SQL practice repository for LeetCode database problems.

Each solution is organized so it can be reviewed and run locally:

- Problem setup data
- SQL solution
- Expected output check
- Notes-friendly file structure for interview preparation

The local runner uses Python's built-in SQLite module, so no database server is required. Most LeetCode SQL problems are written for MySQL; common SQL patterns such as joins, grouping, CTEs, and window functions can still be practiced locally here. MySQL-specific functions may need small syntax changes before final LeetCode submission.

## Study Plan

| Study Plan | Local Checklist |
| --- | --- |
| LeetCode SQL 50 | [`SQL50/index.md`](./SQL50/index.md) |

Each SQL50 file includes an offline prompt summary and table schema, so you can practice locally without opening the LeetCode website. Use the LeetCode extension only when you want official online testing or submission.

## Solved Problems

| ID | Problem | Topic | File |
| --- | --- | --- | --- |
| 1767 | Find the Subtasks That Did Not Execute | Recursive CTE, anti join | [`SQL1767`](./SQL1767) |

## Run Locally

Open a SQL practice file in VS Code and press:

```text
Ctrl + Shift + B
```

Or run it from PowerShell:

```powershell
py .\scripts\run_sql.py .\SQL1767
```

## File Format

Each problem file can use three sections:

```sql
-- @setup
-- Create tables and insert test data.

-- @solution
-- Write the final SELECT here.

-- @expected unordered
-- col1 | col2
-- 1    | a
```

Use `-- @expected unordered` when row order does not matter. Use `-- @expected` when exact row order matters.

## VS Code

Recommended extensions are listed in `.vscode/extensions.json`:

- `LeetCode.vscode-leetcode`
- `mtxr.sqltools`
- `mtxr.sqltools-driver-sqlite`

The local runner is for fast offline practice. The LeetCode extension is for official online testing and final submission.
