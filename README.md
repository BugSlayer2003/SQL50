# SQL LeetCode Practice

这个仓库用来记录我的 SQL LeetCode 练习。每道题都尽量保留：

- 题目对应的建表和测试数据
- 可本地运行的 SQL 解法
- 预期输出校验
- 适合复盘的清晰格式

本地 runner 使用 Python 自带的 SQLite，不需要额外安装数据库服务。正式提交到 LeetCode 时，如果题目要求 MySQL，少数函数可能需要按 MySQL 语法微调。

## Solved Problems

| ID | Problem | Topic | File |
| --- | --- | --- | --- |
| 1767 | Find the Subtasks That Did Not Execute | Recursive CTE, anti join | [`SQL1767`](./SQL1767) |

## Run Locally

在 VS Code 里打开要练的 SQL 文件，然后按：

```text
Ctrl + Shift + B
```

也可以在终端运行：

```powershell
py .\scripts\run_sql.py .\SQL1767
```

## File Format

每道题建议分三段：

```sql
-- @setup
-- 建表和插入测试数据

-- @solution
-- 你的最终 SELECT 写这里

-- @expected unordered
-- col1 | col2
-- 1    | a
```

`-- @expected unordered` 表示结果顺序无所谓。需要严格顺序时写成 `-- @expected`。

## VS Code 扩展

这个目录已经写好了推荐扩展，VS Code 可能会提示安装：

- `LeetCode.vscode-leetcode`：VS Code 里的 LeetCode 扩展，适合拉题目和提交答案。
- `mtxr.sqltools` + `mtxr.sqltools-driver-sqlite`：查看 SQLite 表和连接数据库用。

本地 runner 和 LeetCode 扩展是两条线：runner 负责离线练习和快速问答，LeetCode 扩展负责正式提交。

## Notes

LeetCode SQL 多数题按 MySQL 写。本地这里先用 SQLite，SELECT、JOIN、GROUP BY、CTE、窗口函数都能练；少数 MySQL 专属函数需要改成 SQLite 写法，或者之后再加一个 MySQL/Docker 版本。
