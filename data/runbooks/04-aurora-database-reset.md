# Aurora 本地数据库重置

**状态：已发布** · **环境：仅限本地** · **负责人：陈屿**

1. 停止 Aurora API。
2. 执行 `docker compose stop postgres`。
3. 删除名为 `aurora_pgdata_local` 的 Docker volume。
4. 执行 `docker compose up -d postgres`。
5. 运行 `make migrate seed`。
6. 使用测试账号 `demo@example.invalid` 登录验证。

此操作会清空全部本地数据，无法恢复。禁止在 test、staging 或 production 环境执行。若不确定当前环境，先运行 `printenv APP_ENV`，只有输出 `local` 时才可继续。