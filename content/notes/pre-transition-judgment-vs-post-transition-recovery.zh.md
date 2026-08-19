---
title: "从迁移后恢复到迁移前判定"
summary: "讨论复杂自动化系统中，为什么部分 Timeout、Retry、Abort、Rollback 和人工恢复，本可以在目标状态进入前被识别和分流，以及 PCN 如何把部分迁移后补偿前移为状态迁移入口判定。"
description: "从状态机、SFC 与现场异常恢复逻辑出发，讨论状态迁移入口判定与迁移后补偿之间的关系。说明 PCN 不替代状态机，也不消灭必要的 Recovery，而是将可在目标状态进入前识别的问题前移处理，减少可避免的迁移后补偿。"
date: 2026-08-19
lastmod: 2026-08-19
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.0"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

状态机、SFC、Interlock、Handshake 和顺序控制本身并没有问题。

它们可以定义系统有哪些状态、状态之间如何迁移，以及满足什么条件后执行 Transition。

但在复杂自动化系统中，还有一个容易被分散到程序各处的问题：

> **这一次具体的状态迁移，在当前时刻、当前对象和当前系统状态下，是否真的应该发生？**

## 1. 有些异常，本来在进入目标状态前就已经存在

例如一个自动化单元准备从等待阶段进入搬送阶段。

程序可能规定：

```text
WAIT
→ TRANSFER
→ COMPLETE
````

但在真正进入 `TRANSFER` 之前，现场实际上还可能存在：

* 下游已经不能接收；
* 识别结果已经超时；
* 上位许可已经撤销；
* 返回路径正在切换；
* 某个必要状态没有刷新；
* 当前条件处于允许与禁止之间的边界。

如果这些问题没有在迁移入口被充分处理，系统可能先进入目标状态，随后才发现无法继续。

于是程序开始出现：

```text
TRANSFER
→ Wait
→ Timeout
→ Retry
→ Abort
→ Rollback
→ Reset
```

这些逻辑并不一定都是错误的。

问题在于：

> **其中一部分，本来可以在进入 `TRANSFER` 之前就被识别。**

## 2. 迁移后的 Recovery 并不都具有相同性质

制造现场不可能取消 Recovery。

设备已经开始动作以后，可能突然发生急停、执行器故障、传感器失效或其他新的运行异常。

这种情况下，Abort、Safe State、Recovery、Reset 都是必要的。

但还有另一类情况：

> 目标状态尚未进入时，阻止该迁移所需要的信息实际上已经存在，只是没有在同一个迁移入口被组织起来进行判定。

这类问题如果仍然先进入目标状态，再依靠 Timeout、Retry、Abort、Rollback 或人工恢复进行处理，称为：

**可避免的迁移后补偿（Avoidable Post-entry Compensation）。**

因此，需要区分：

```text
必要的运行中恢复 ≠ 可避免的迁移后补偿 
```

前者是运行过程中新的异常造成的。

后者则可能来自状态迁移入口判定不足。

## 3. PCN 把判定位置向前移动

TPCA / PCN 并不替代状态机。

状态机仍然负责描述：

```text
Current State → Target State
```

PCN 关注的是两者之间真正执行迁移之前的入口：

```text
Current State
        ↓
Transition Request
        ↓
       PCN
        ↓
 Target State
```

PCN 在目标状态进入前读取与本次迁移有关的多源状态，将其组织为条件状态、许可状态和执行链状态，并进一步判断结构完整性、动态时序有效性和控制边界。

最终结果也不只是：

```text
True / False
```

而可以进入不同控制路径：

```text
Allow
Wait
Recheck
Return
Coordinate
Degrade
Manual Confirm
Prohibit
Safety Lock
```

因此，原本可能在进入目标状态以后才通过 Timeout 或 Rollback 暴露的问题，可以在迁移入口提前被识别和分流。

## 4. 重点不是减少所有 Recovery

PCN 的目标不是让自动化程序“不再需要 Recovery”。

真正不可预测的运行异常仍然必须由既有设备控制、安全控制和恢复逻辑处理。

PCN 试图减少的是另一部分复杂度：

> **已经可以在目标状态进入前识别，却仍然被推迟到进入以后处理的问题。**

因此可以把两种控制思路简单区分为：

```text
迁移后补偿：

进入目标状态
→ 发现无法继续
→ Timeout / Retry / Abort / Rollback
→ Recovery
```

和：

```text
迁移前判定：

准备进入目标状态
→ PCN 前置判定
→ Allow / Wait / Return / Degrade / Prohibit
→ 再决定是否进入
```

二者合理的关系是：

> **能够前置判断的问题，在迁移前处理；只有真正发生在执行过程中的新异常，才留给运行中 Recovery。**

## 5. 从“状态迁移条件”到“状态迁移入口”

复杂自动化程序中，真正值得进一步显式化的，不只是 Transition Condition。

还包括：

> **一次具体状态迁移请求本身。**

同一个：

```text
State A → State B
```

可以在不同时间、不同工件、不同任务、不同许可状态和不同下游条件下重复发生。

因此，状态图上的同一条 Transition，并不意味着每一次实际迁移都具有相同的工程条件。

PCN 的作用，就是把每一次具体的 Target State Entry 作为一个独立工程判定对象。

这也是从“迁移后恢复”向“迁移前判定”移动的核心：

> **不是取消状态机，也不是取消异常恢复，而是在真正进入目标状态之前，把原本分散在程序、设备和系统中的判断集中到明确的状态迁移入口。**

这样，Recovery 可以更多地用于处理真正发生在运行过程中的异常，而不是不断补偿那些本来可以在进入之前发现的问题。

---

本文讨论的是 TPCA / PCN 与状态机、SFC 和异常恢复逻辑之间的工程边界，不代表所有 Timeout、Retry、Rollback 或 Recovery 都属于冗余逻辑。

具体能够减少多少迁移后补偿、程序分支和人工恢复，需要通过同一自动化对象在传统实现与 PCN 前置判定实现之间进行对比验证。

## 文档信息
题目：“从迁移后恢复到迁移前判定”  
文档类型：技术札记 
版本：Public Note Version 1.0  
首次发布日期：2026-08-19  
作者：全野南政 / Nansei Zenno 
