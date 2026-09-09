---
title: "TPCA / PCN 如何看待既有技术中的工程论点？——三个代表性工程论点"
summary: "从显式规则控制与 AI 辅助、局部判定与系统协同、保守阻断与约束条件下继续处理三个论点出发，整理 TPCA / PCN 的基本技术定位。"
description: "整理 TPCA / PCN 在控制与 AI、PCN 配置、关键许可及约束条件下继续处理等方面的基本技术定位。"
date: 2026-08-18
lastmod: 2026-09-09
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.2"
citation_url: "https://zennns.com/zh/notes/engineering-positions-of-tpca-pcn/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## TPCA / PCN 如何看待既有技术中的工程论点？

在复杂工程系统中，控制方式和系统构成通常不能仅依据一种思路确定。

例如，常见的工程论点包括：

- 是以明确规定的控制规则为主，还是在多大范围内使用 AI / 数据驱动方法；
- 是将判定和控制集中在单一位置，还是分布到局部节点；
- 当系统出现异常或能力下降时，是阻止进入目标状态，还是在既定约束范围内继续处理。

TPCA / PCN 并不对这些技术路线一概进行优劣评价，而是以 Target State Entry 为中心，将不同技术的职责配置到相应的工程位置。

本文从以下三个论点整理 TPCA / PCN 的基本技术定位。

```text
1. 显式规则控制与 AI 辅助

2. 局部判定与系统协同

3. 保守阻断与约束条件下继续处理
```

---

## 1. 显式规则控制与 AI 辅助

在安全相关系统和高可靠系统中，重要约束、判定依据和变更内容能够被确认，是系统设计和运行管理中的重要要求。

另一方面，AI / 数据驱动方法适合从大量历史数据中提取模式，并辅助整理改善候选。

当机器学习应用于安全关键系统时，除模型性能外，还需要考虑安全保证、可验证性和可接受风险等问题。[1]

### TPCA / PCN 的定位

TPCA / PCN 对 Target State Entry 的关键判定与控制，以工程规则、许可、约束和判定条件能够被明确确认的结构为基础。

例如：

- C / A / E 状态映射；
- S / D / B 判定；
- 关键 A 的必要约束；
- Arbitration；
- Multipath Control。

这些内容作为工程规则进行管理，并应能够进行确认和变更管理。

AI 可以用于基于 PCN Trace 及相关历史数据的后续分析。

代表性用途包括：

- 发现重复问题；
- 履历比较；
- 模式提取；
- 整理改善候选；
- 比较执行结果；
- 辅助生成工程报告。

因此，TPCA / PCN 中的基本职责关系可以整理为：

> **Target State Entry 的判定与控制依据明确规定的工程规则和约束执行，AI 用于辅助履历分析和工程改善。**

---

## 2. 局部判定与系统协同

在大规模系统中，可以将信息和控制集中到一个位置，也可以将局部判定和控制分布到多个节点。

在分布式控制和分层控制中，局部控制与上层协调相结合的系统结构已得到广泛研究。[2]

### TPCA / PCN 的定位

TPCA / PCN 对一个明确的 Target State Entry 配置一个 PCN。

PCN 以与该 Target State Entry 直接相关的状态为对象，形成以下判定与控制关系：

```text
Current State
→ Target State
→ 相关状态
→ C / A / E
→ S / D / B
→ CAE-SDB Result
→ Arbitration
→ Multipath Control
```

对于跨越多个 PCN 的问题，则按照实际系统层级和协同结构处理。

例如：

- 共享资源；
- 跨多个设备的许可；
- MES / WCS 调度；
- 多主体协同；
- 上下游之间的执行依赖。

因此，TPCA / PCN 的基本结构可以概括为：

> **明确每个 Target State Entry 对应 PCN 的责任范围，跨越多个 PCN 的关系则按照实际系统层级进行协同处理。**

PCN 的节点化，是为了在明确局部判定责任的同时，为与上位系统及周边节点进行协同提供明确的工程单元。

---

## 3. 保守阻断与约束条件下继续处理

当系统发生异常或能力下降时，并不一定适合采用完全相同的控制方式。

如果与安全有关的重要约束未成立，则需要阻止系统进入 Target State。

另一方面，如果系统的剩余能力或可利用路径已经明确，也可能存在在限定条件下继续处理、重新尝试、降级运行或切换替代路径等处理方式。

故障容错控制领域已经形成了根据故障后的剩余能力和系统约束重新配置控制，以维持安全性和可用性的相关方法。[3]

### TPCA / PCN 的定位

TPCA / PCN 首先将与当前 Target State Entry 相关的状态整理为 C / A / E，并执行必要的 S / D / B 判定。

关键 A 作为独立的必要约束处理。

当关键许可未成立时，即使 C 和 E 均满足，也不得允许进入 Target State。

对于其他条件不满足、动态状态问题或控制边界问题，则根据相应判定结果以及预先定义的控制规则进行 Arbitration，并连接到 Multipath Control。

代表性的控制路径例如包括：

```text
Allow
Wait
Recheck
Retry
Degrade
Manual Confirm
Prohibit
Safety Lock
```

这里的重点不是简单地在“停止”和“继续”之间进行二选一。

> **关键约束必须得到保证；对于其他状态，则根据允许的控制边界和可利用路径进行分流处理。**

这构成 TPCA / PCN 的基本控制思路。

---

## 总结

针对上述三个工程论点，TPCA / PCN 的技术定位可以整理如下。

### 显式规则控制与 AI 辅助

> **Target State Entry 的判定与控制依据明确规定的工程规则和约束执行，AI 用于辅助履历分析和工程改善。**

### 局部判定与系统协同

> **明确每个 Target State Entry 对应 PCN 的责任范围，跨越多个 PCN 的关系则按照实际系统层级进行协同处理。**

### 保守阻断与约束条件下继续处理

> **关键约束作为独立必要条件处理，其他状态则根据判定结果和控制规则连接到多个控制路径。**

TPCA / PCN 并不以将现有安全控制、AI、分布式控制和故障容错控制统一成一种方法为目标。

其关注点是将 Target State Entry 设定为明确的工程位置，并围绕该入口整理所需状态、许可、执行链、判定性质和控制路径，从而明确既有技术在一次状态迁移中的作用位置。

---

## 参考文献与外部资料

本文引用以下三项资料，用于说明相关工程论点的技术背景。

1. **GOODLOE A E.**  
   *Assuring Safety-Critical Machine Learning Enabled Systems: Challenges and Promise.*  
   NASA Technical Reports Server, Document ID 20220011814, 2022.  
   https://ntrs.nasa.gov/citations/20220011814

2. **SCATTOLINI R.**  
   Architectures for Distributed and Hierarchical Model Predictive Control: A Review.  
   *Journal of Process Control*, 2009, 19(5): 723–731.  
   DOI: 10.1016/j.jprocont.2009.03.001  
   https://www.sciencedirect.com/science/article/pii/S0959152409000353

3. **BLANKE M, KINNAERT M, LUNZE J, STAROSWIECKI M.**  
   *Diagnosis and Fault-Tolerant Control*. 3rd ed.  
   Berlin, Heidelberg: Springer, 2016.  
   DOI: 10.1007/978-3-662-47943-8  
   https://link.springer.com/book/10.1007/978-3-662-47943-8

---

## 文档信息

题目：TPCA / PCN 如何看待既有技术中的工程论点？——三个代表性工程论点  
文档类型：技术札记  
版本：Public Note Version 1.2  
首次发布日期：2026-08-18  
最后更新：2026-09-09  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/engineering-positions-of-tpca-pcn/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
