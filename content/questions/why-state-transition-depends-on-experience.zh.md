---
title: "为什么状态迁移设计长期依赖个人经验？"
summary: "说明为什么复杂自动化项目中的状态迁移判断长期依赖少数熟悉系统的工程师，以及如何通过 PCN 把这些隐含判断转化为可复用的工程结构。"
date: 2026-07-04
lastmod: 2026-08-18
author: "全野南政 / Nansei Zenno"
document_type: "工程问题"
question_type: "状态迁移设计问题"
version: "Public Question Version 1.1"
citation_title: "为什么状态迁移设计长期依赖个人经验？"
citation_url: "https://zennns.com/zh/questions/why-state-transition-depends-on-experience/"
draft: false
ShowReadingTime: false
ShowToc: true
TocOpen: true
---

很多自动化项目上线以后，真正懂系统的人往往只有少数几个工程师。

设备能运行，程序能维护，HMI 也有状态。

但一旦现场出现：

- Ready 了却不动作；
- Waiting 很久却不知道在等什么；
- 报警很多但不知道先查哪个；
- MES / WCS 有记录却解释不了停滞；

最后通常还是要找熟悉项目的人。

因为他知道：

> 这个 Ready 只代表本机状态。  
> 这个 Waiting 实际在等上位许可。  
> 这个报警是后续现象。  
> 这个视觉结果已经过期。  
> 这个下游 Ready 不代表真正可承接。

这些判断很有价值。

问题在于：

> **它们经常只存在于工程师脑中，而没有成为状态迁移设计的一部分。**

---

## 1. 为什么状态迁移特别容易依赖经验

一个动作能不能进入下一阶段，通常不会只看一个信号。

例如机器人准备进入抓取阶段，现场可能同时涉及：

- 工件存在；
- 视觉结果有效；
- 位置满足；
- 机器人 Ready；
- 安全许可；
- 区域许可；
- 上位放行；
- 下游承接；
- 返回路径；
- 结果回写。

这些状态又可能分散在：

- PLC；
- 机器人控制器；
- 视觉系统；
- HMI；
- 安全系统；
- MES / WCS；
- 设备接口；
- 调试记录；

之中。

系统能运行，不代表这些状态迁移条件已经被统一表达。

很多时候，真正把它们串起来的是熟悉项目的工程师。

---

## 2. 经验依赖会带来什么问题

个人经验本身不是问题。

问题是状态迁移判断只存在于个人经验中。

这样会带来几个直接结果：

- 同类设备，不同工程师设计的等待和异常逻辑不一致；
- 新人接手后，需要重新读程序和问老工程师；
- 项目复制到新产线时，相同边界重新讨论；
- 现场问题解决以后，只留下报警和处理结果；
- 同类问题下一次发生时，仍然需要重新排查。

所以真正难以复用的，往往不是 PLC 程序本身，而是：

> **为什么这个状态可以进入，为什么那个状态不能进入。**

---

## 3. 需要显式化的是一次状态迁移判断

要降低这种依赖，首先要把判断对象明确下来。

例如：

```text
Current State:
Waiting for Pick

Target State:
Picking
```

然后继续明确：

- 进入 Picking 前需要哪些状态；
- 哪些属于 C：Condition；
- 哪些属于 A：Authority；
- 哪些属于 E：Execution Chain；
- 这些状态是否完整、有效并处于可接受边界；
- 多个判定结果出现时，最终如何形成控制路径；
- 本次判定是否留下 Trace。

这样，原本依赖工程师脑中检查顺序的内容，就开始变成一个可维护的工程结构。

---

## 4. PCN 把经验落到具体入口

PCN 的作用，不是替代有经验的工程师。

它更像是把工程师长期积累的判断方式，落到一个明确的 Target State Entry 上。

基本链条为：

```text
Current State
→ Target State
→ PCN
→ C/A/E Mapping
→ S/D/B Evaluation
→ CAE-SDB Result
→ Arbitration
→ Multipath Control
→ PCN Trace
```

这样以后，项目不再只知道：

> “这个条件要记得检查。”

而可以进一步明确：

> 这个条件属于哪个状态迁移入口？  
> 在这次迁移中属于 C、A 还是 E？  
> 当前是否有效？  
> 出现问题以后系统进入哪条路径？  
> 这次判断能不能被追溯？

经验开始从“个人知道”变成“系统可以表达”。

---

## 5. 从个人经验到工程资产

状态迁移判断一旦被结构化，就可以进一步形成：

- PCN 模板；
- HMI 诊断结构；
- 状态迁移检查表；
- Trace 履历；
- 同类设备复用规则；
- 项目交接资料。

工程师经验仍然重要。

但经验的价值不应该只体现在：

> “这个人来了就能查出来。”

更高价值的状态是：

> **这个人把判断结构留下来了，其他工程师和后续项目可以继续使用。**

---

## 工程结论

状态迁移设计长期依赖个人经验，真正的原因是：

> **决定 Current State 能否进入 Target State 的条件、许可、执行链和状态有效性，长期分散在不同程序、设备和人的经验中。**

PCN 的作用，是把这些判断集中到明确的状态迁移入口上，使其逐步变成：

- 可表达；
- 可检查；
- 可记录；
- 可复用；
- 可交接；
- 可改善；

的工程结构。

这样，工程经验不会消失。

它只是从：

> **“熟悉项目的人知道怎么判断”**

逐步转变为：

> **“系统本身能够说明这次状态迁移是怎样判断的”。**

---

## 进一步阅读

- [为什么状态迁移条件必须显式化？](/zh/notes/explicit-state-transition-conditions/)
- [为什么 PCN 是 TPCA 的最小工程单元？](/zh/notes/pcn-minimum-engineering-unit/)
- [为什么 Ready 不够？](/zh/questions/why-ready-is-not-enough/)
- [为什么报警越来越多，排查时间没有明显缩短？](/zh/questions/why-alarms-do-not-reduce-troubleshooting/)
- [Concepts｜核心概念](/zh/concepts/)

---

## 文档信息

题目："为什么状态迁移设计长期依赖个人经验？"  
文档类型：工程问题  
问题类型：状态迁移设计问题  
版本：Public Question Version 1.1  
首次发布日期：2026-07-04  
最后更新：2026-08-18  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/questions/why-state-transition-depends-on-experience/
