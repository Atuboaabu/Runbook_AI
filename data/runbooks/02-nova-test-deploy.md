# Nova 服务部署到测试环境

适用系统：Nova 用户服务  
适用环境：test  
作者：周青  
最后更新：2026-06-28  
状态：已发布

前置条件：代码已合并到 `develop`，CI 的 unit-test 和 security-scan 均通过。

在 CI 页面选择 `deploy-test`，输入镜像标签和变更单编号后执行。发布完成后运行 `runbookctl status nova --env test`，确认两个实例均为 Ready。然后请求 `https://nova.test.example.invalid/health`，响应中的版本必须与镜像标签一致。

若健康检查连续三次失败，执行 `runbookctl rollback nova --env test --to previous`，并在研发故障频道登记。