---
title: "Engineering Questions"
draft: false
ShowReadingTime: false
---

## 工程问题

## 从这些问题开始

如果你正在思考以下问题，可以从对应文章开始阅读。

## 单元执行问题
1. [为什么 Ready 不够？](/zh/questions/why-ready-is-not-enough/)  
   设备已经 Ready，但系统仍不能稳定进入下一阶段。

2. [为什么 Waiting 越来越难排查？](/zh/questions/why-waiting-is-hard-to-trace/)  
   MES / WCS / HMI 显示 Waiting、Pending、Blocked，但停滞原因仍需要人工追查。

3. [为什么 PLC Ready 仍不能运行？](/zh/questions/why-plc-ready-does-not-run/)  
   PLC 条件看似成立，执行机构却没有动作，或进入后立即卡滞。


5. [为什么报警越来越多，排查时间没有明显缩短？](/zh/questions/why-alarms-do-not-reduce-troubleshooting/)  
   报警能指出设备或信号异常，却未必能解释状态迁移失败的原因。

## 多系统联动问题
4. [为什么 MES / WCS 能记录，却不能解释停滞？](/zh/questions/why-mes-records-but-cannot-explain/)  
   系统能记录事件、任务和状态，但不能说明协同停滞的结构原因。
   
7. [为什么资源锁、区域许可和下游许可比 Ready 更关键？](/zh/questions/why-authority-is-more-critical-than-ready/)  
   设备 Ready 并不代表系统可以进入下一状态。关键许可、资源锁、区域许可和下游承接未成立时，系统仍应阻断、等待或进入人工确认路径。

8. [为什么任务存在，不代表任务可以执行？](/zh/questions/why-task-exists-but-cannot-execute/)  
   MES / WCS / API / AI 调用中，任务已经生成，并不代表目标执行路径已经成立。进入前仍需要判断条件、许可和执行链是否可接续。

9. [为什么系统记录很多状态，却不能形成协同判断？](/zh/questions/why-status-records-cannot-form-coordination-judgment/)  
   多个系统都在记录状态，但如果缺少统一的 C/A/E 映射和 S/D/B 判定，就难以说明协同停滞来自结构缺失、动态异常还是控制边界。


## 状态迁移设计问题
6. [为什么状态迁移设计长期依赖个人经验？](/zh/questions/why-state-transition-depends-on-experience/)  
   状态迁移条件、异常边界和执行链设计在不同项目、不同工程师之间缺少统一标准。
   
