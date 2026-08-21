# QNX 仪表应用开发环境初始化

> 示例项目资料｜适用平台：8155、8295、8397｜状态：已发布｜负责人：座舱基础组｜更新日期：2026-07-18

在 Linux 开发机安装团队批准版本的 QNX SDP，并通过项目提供的环境脚本加载编译变量。确认 `QNX_HOST` 与 `QNX_TARGET` 已设置后，执行项目封装命令 `cluster-toolchain doctor`。

拉取仪表应用代码后运行 `cluster-build configure --platform <8155|8295|8397> --variant dev`，再执行 `cluster-build compile`。三个平台必须分别生成构建目录，禁止复用 CMake 缓存。

验证时检查目标产物为 AArch64 QNX 可执行文件，并确认构建清单记录了平台、变体、提交号和工具链版本。文中的 `cluster-*` 命令为本项目虚构封装命令。
