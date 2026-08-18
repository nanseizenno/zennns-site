---
title: "为什么 PLC Ready 仍不能运行？"
summary: "说明为什么 PLC Ready、HMI 条件 OK 或设备无报警，并不代表自动化执行单元已经具备进入目标物理执行阶段的完整条件。"
date: 2026-07-04
lastmod: 2026-08-18
author: "全野南政 / Nansei Zenno"
document_type: "工程问题"
question_type: "单元与现场执行问题"
version: "Public Question Version 1.1"
citation_title: "为什么 PLC Ready 仍不能运行？"
citation_url: "https://zennns.com/zh/questions/why-plc-ready-does-not-run/"
draft: false
ShowReadingTime: false
ShowToc: true
TocOpen: true
---

设备“不动作”。

HMI 上 PLC Ready 已经成立，机器人没有报警，伺服已上电，主要条件也都显示 OK。

现场第一反应往往是查梯形图、步进状态和输出点。

但最后发现，PLC Ready 本身并没有错。

真正的问题是：

> **PLC Ready 成立，只能说明 PLC 侧某些局部条件已经满足，并不等于当前目标阶段已经具备完整进入条件。**

---

## 1. PLC Ready 能说明什么

PLC Ready 通常是一个汇总状态。

它可能包含：

- 自动模式成立；
- 设备无主要报警；
- 伺服已上电；
- 机构处于待机位置；
- 上一动作完成；
- 基础通信正常；
- 部分 Interlock 已成立。

这些状态都很重要。

但它们主要回答：

> **本机现在有没有执行基础？**

而自动化执行单元真正进入下一阶段时，还需要回答：

> **当前对象条件是否成立？**

> **关键许可是否成立？**

> **进入以后执行链能不能接下去？**

---

## 2. Ready 成立以后，还可能缺什么

对于一个明确的目标状态入口，问题通常可以从三个方向继续看。

### C：Condition

对象或数据条件可能没有真正成立。

例如：

- 工件未到位；
- 视觉结果已经过期；
- 工件 ID 不一致；
- 参数缺失；
- 前序完成状态不可信。

### A：Authority

关键许可可能没有成立。

例如：

- 安全许可未成立；
- 区域许可未成立；
- 上位系统未放行；
- 人工确认未完成；
- 对方设备未给出交接许可。

关键 A 不成立时，即使其他条件正常，也不能进入目标阶段。

### E：Execution Chain

进入目标阶段以后，执行链可能接不下去。

例如：

- 下游无法承接；
- 正常投放位不可用；
- 返回路径不可用；
- 异常排出路径不可用；
- 结果回写链路不可用。

这也是为什么：

> **E 不等于设备 Ready。**

Ready 可以是 E 的一个输入，但不能代表整个执行链已经成立。

---

## 3. 还要确认这些状态当前是否有效

有些问题不是“状态值不对”，而是状态本身已经失去有效性。

例如：

- 视觉结果超时；
- 下游状态长期未刷新；
- 许可刚刚被撤销；
- 多个设备状态不同步；
- 系统仍处于切换过程中。

因此，Target State 的前置判定不能只看布尔值。

还需要结合 S / D / B，对结构完整性、动态时序有效性和控制边界进行判断。

---

## 4. PCN 增加的是目标阶段入口上的完整判定

PCN 把与本次状态迁移相关的状态重新组织到一个明确入口上：

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

这样，现场看到的就不再只是：

> “PLC Ready 了，为什么还不动？”

而可以进一步知道：

> 当前到底是条件没有成立、许可没有成立，还是执行链没有接续。

---

## 工程结论

PLC Ready 很重要，但它不是目标阶段进入的最终结论。

在复杂自动化执行单元中，PLC Ready 成立以后，仍然需要确认：

- C：对象和数据条件是否成立；
- A：关键许可是否成立；
- E：进入后的执行链是否能够接续；
- 相关状态是否仍然完整、有效并处于可接受边界内。

因此：

> **PLC Ready 只能说明局部准备状态，不能替代目标物理执行阶段进入前的完整判定。**

这就是 PCN 在 PLC / HMI 和自动化执行单元中的工程位置。

---

## 进一步阅读

- [为什么 Ready 不够？](/zh/questions/why-ready-is-not-enough/)
- [为什么 Ready 成立，系统仍可能被许可和执行链阻断？](/zh/questions/why-authority-is-more-critical-than-ready/)
- [为什么报警越来越多，排查时间没有明显缩短？](/zh/questions/why-alarms-do-not-reduce-troubleshooting/)
- [自动化执行单元前置判定案例](/zh/cases/automation-execution-unit-pre-control/)
- [Concepts｜核心概念](/zh/concepts/)

---

## 文档信息

题目："为什么 PLC Ready 仍不能运行？"  
文档类型：工程问题  
问题类型：单元与现场执行问题  
版本：Public Question Version 1.1  
首次发布日期：2026-07-04  
最后更新：2026-08-18  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/questions/why-plc-ready-does-not-run/
