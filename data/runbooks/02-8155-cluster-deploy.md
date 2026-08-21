# 8155 开发板仪表应用部署手顺

平台：8155  
系统：QNX 仪表域  
环境：实验室开发板  
状态：已发布

部署前确认车辆模拟台处于驻车状态，目标板平台标识为 8155。执行 `cluster-device identify`，输出必须同时包含 `platform=8155` 和 `mode=development`。

使用 `cluster-deploy push --platform 8155 --app digital-cluster` 上传应用包，再执行 `cluster-deploy restart --app digital-cluster`。部署过程不得覆盖系统镜像或 BSP。

验证项目：仪表主界面正常显示；车速、转速、档位三个模拟信号能够刷新；应用日志中不存在连续重启。失败时使用 `cluster-deploy rollback --app digital-cluster` 恢复上一开发包。

以上部署工具和输出为虚构测试接口。
