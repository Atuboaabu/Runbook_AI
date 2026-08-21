# Nova 服务本地开发环境搭建

> 示例数据。适用环境：本地开发；负责人：林默；状态：已发布；更新日期：2026-07-12

新人首次开发 Nova 用户服务时，先安装 Python 3.12 和 uv。复制 `.env.example` 为 `.env.local`，将 `APP_ENV` 设置为 `local`。执行 `uv sync` 安装依赖，再运行 `docker compose up -d postgres redis`。

使用 `uv run alembic upgrade head` 初始化数据库，最后执行 `uv run python -m nova.api`。访问 `http://localhost:8080/health`，返回 `{"status":"ok"}` 表示启动成功。

本地启动失败时先检查 5432 和 6379 端口。该手顺不得用于测试或生产环境。