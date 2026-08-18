---
title: "为什么 Ready 不够？"
summary: "说明为什么设备 Ready、机器人 Ready 或下游 Ready 只能代表局部可运行状态，不能直接等同于系统可以进入目标状态。"
date: 2026-07-04
lastmod: 2026-08-18
author: "全野南政 / Nansei Zenno"
document_type: "工程问题"
question_type: "单元与现场执行问题"
version: "Public Question Version 1.1"
citation_title: "为什么 Ready 不够？"
citation_url: "https://zennns.com/zh/questions/why-ready-is-not-enough/"
draft: false
ShowReadingTime: false
ShowToc: true
TocOpen: true
---

一条产线停了很久。

机器人显示 Ready，PLC 条件也基本成立，但就是不抓取。最后查到，视觉识别结果虽然曾经 OK，但时间戳已经超时，当前结果已经不能再作为抓取依据。

另一个现场里，机器人 Ready，但区域许可没有成立。

还有一种情况，下游设备 Ready，但真正进入交接以后，下游承接链路并没有准备好。

表面上看都是：

> “Ready 了，为什么还不动？”

实际上，Ready 只说明局部对象处于某种可运行状态，并不能直接证明这一次状态迁移已经成立。

---

## 1. Ready 能说明什么

Ready 通常表示某个设备、机构、程序或模块已经具备局部运行条件。

例如：

- 机器人处于自动模式；
- 伺服已上电；
- 设备无主要报警；
- 程序可执行；
- 机构已回到待机位置；
- 某个下游设备返回 Ready；
- 通信对象在线。

这些状态都很重要。

但 Ready 主要回答的是：

> **这个对象现在能不能运行？**

而系统真正进入下一阶段时，还需要继续判断：

> **当前条件是否成立？**

> **系统是否被允许进入？**

> **进入以后执行链能不能继续接下去？**

---

## 2. Ready 之外，还需要看 C / A / E

对于一个明确的 Target State Entry，可以把相关状态分成三类。

### C：Condition

表示目标状态进入前的对象、识别、数据、任务和前序条件。

例如：

- 工件是否存在；
- 视觉结果是否有效；
- 位置是否满足；
- 任务参数是否完整；
- 前序状态是否真实完成。

### A：Authority

表示系统是否允许进入目标状态。

例如：

- 安全许可；
- 区域许可；
- 上位系统放行；
- 资源锁；
- 人工确认；
- 对方设备许可。

关键 A 不成立时，即使设备 Ready，也不能进入目标状态。

### E：Execution Chain

表示进入目标状态以后，整个执行链是否能够继续接续。

例如：

- 机器人路径是否可达；
- 夹爪是否可用；
- 下游是否可承接；
- 返回路径是否可用；
- 异常分流路径是否可用；
- 结果是否能够回写。

因此：

> **Ready 更适合作为 C、A 或 E 中的一个输入，而不是状态迁移成立的最终结论。**

---

## 3. 状态值成立，也不代表当前仍然有效

很多现场问题不是 Ready 本身错误，而是相关状态已经失去当前有效性。

例如：

- 视觉结果曾经 OK，但已经超时；
- 下游 Ready 长时间没有刷新；
- 区域许可在动作前已经撤销；
- 多个设备状态不同步；
- 系统仍处于切换过程中。

所以目标状态进入前，还需要从 S / D / B 判断结构完整性、动态时序有效性和控制边界。

PCN 将这些结果组织成：

```text
Current State
→ Target State
→ C/A/E Mapping
→ S/D/B Evaluation
→ CAE-SDB Result
→ Arbitration
→ Multipath Control
→ PCN Trace
```

---

## 4. Ready 不够，缺的是完整的目标状态入口判定

Ready、Interlock、Handshake、Alarm 都是现场已经存在的重要机制。

PCN 不是为了替代它们。

它增加的是一个明确的状态迁移入口：

> 当前在哪里？

> 准备进入哪里？

> 这次迁移真正依赖哪些状态？

> 哪些属于条件、许可和执行链？

> 当前状态是否仍然有效？

> 最终为什么允许进入，或者为什么没有进入？

这样，现场看到的就不再只是：

> “Ready 了，但还是不动。”

而可以进一步知道：

> **到底是条件没成立、许可没成立，还是执行链接不下去。**

---

## 工程结论

Ready 很重要，但 Ready 不够。

它通常只代表某个设备、机构或模块的局部可运行状态。

对于复杂自动化系统，真正能不能进入下一阶段，还需要同时确认：

- C：条件是否成立；
- A：关键许可是否成立；
- E：执行链是否能够接续；
- 相关状态当前是否完整、有效并处于可接受边界内。

因此：

> **Ready 是状态迁移判定的输入之一，不是目标状态进入的最终结论。**

这就是 TPCA / PCN 为什么把问题放到明确 Target State Entry 上重新组织的原因。

---

## 进一步阅读

- [为什么 PLC Ready 仍不能运行？](/zh/questions/why-plc-ready-does-not-run/)
- [为什么 Ready 成立，系统仍可能被许可和执行链阻断？](/zh/questions/why-authority-is-more-critical-than-ready/)
- [为什么报警越来越多，排查时间没有明显缩短？](/zh/questions/why-alarms-do-not-reduce-troubleshooting/)
- [自动化执行单元前置判定案例](/zh/cases/automation-execution-unit-pre-control/)
- [Concepts｜核心概念](/zh/concepts/)

---

## 文档信息

题目："为什么 Ready 不够？"  
文档类型：工程问题  
问题类型：单元与现场执行问题  
版本：Public Question Version 1.1  
首次发布日期：2026-07-04  
最后更新：2026-08-18  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/questions/why-ready-is-not-enough/
