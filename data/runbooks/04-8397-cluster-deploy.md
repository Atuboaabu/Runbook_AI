# 8397 仪表开发包部署

**状态：已发布** · **平台：8397** · **范围：开发样机** · **负责人：新平台预研组**

1. 执行 `cluster-device identify`，确认平台为 8397、样机为开发模式。
2. 检查应用清单中的 `target_platform` 为 `8397`。
3. 执行 `cluster-deploy push --platform 8397 --bundle cluster-dev`。
4. 使用 `cluster-display probe` 检查仪表屏连接状态。
5. 执行 `cluster-app start digital-cluster`。

验证要求：启动阶段无崩溃；测试画面完整；模拟车速信号变化时指针平滑更新。若平台、样机模式或显示拓扑任一项不明确，停止部署并向平台负责人确认。

本文不包含系统镜像、BSP 或安全分区更新。所有工具为虚构测试接口。
