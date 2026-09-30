---
title: "为什么 PCN Trace 是一种新的工程数据？"
summary: "说明 PCN Trace 如何以一次 Target State Entry 为数据组织单位，将输入状态、CAE-SDB 判定结果、控制仲裁、多路径控制、执行结果和时间信息 T 关联为一条状态迁移判定履历，并说明其分析与改善价值。"
description: "从设备数据、生产数据和报警履历的区别出发，说明 PCN Trace 如何以一次 Target State Entry 为数据组织单位，并通过 CAE-SDB 状态迁移判定语义，将判定依据、控制选择和执行结果关联为可比较、可追溯的工程履历。"
date: 2026-07-14
lastmod: 2026-09-18
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.7"
citation_url: "https://zennns.com/zh/notes/why-pcn-trace-is-engineering-data/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## 为什么 PCN Trace 是一种新的工程数据？

制造现场已经积累了大量数据。

PLC 记录设备状态和报警，MES 保存生产履历，WCS 保存任务和调度记录，设备平台还会持续采集温度、电流、位置、节拍和运行时间。

这些数据通常围绕设备、任务、工单、报警或事件进行整理。

PCN Trace（状态迁移判定履历）增加了另一个数据组织对象：

> **一次 Target State Entry（目标状态入口）对应的状态迁移判定。**

对于一次明确的 Target State Entry，PCN Trace 将本次判定使用的状态、C / A / E Mapping（状态映射）、S / D / B Evaluation（判定）、CAE-SDB Result（CAE-SDB 判定结果）、Arbitration（控制仲裁）结果、Multipath Control（多路径控制）、Execution Result（执行结果）以及时间信息 T 关联起来。

CAE-SDB 为来自不同设备和系统、但与同一 Target State Entry 相关的状态建立统一的状态迁移判定语义。

PCN Trace 在此基础上，将判定依据、控制选择和实际执行结果保持在同一条状态迁移履历中。

本文所说的“新的工程数据”，不是指履历记录这种形式本身是新的，也不是增加新的传感器数据类型，而是增加了一种新的工程数据组织对象：

> **把一次目标状态入口的判定、控制和执行过程作为可以持续记录、比较、统计和分析的数据对象。**

基础概念可参见：

- [Concepts｜核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)
- [为什么是 CAE-SDB？——目标状态入口前的双轴结构化分析方法](/zh/notes/why-cae-sdb/)
- [状态迁移如何形成可分析的工程数据？——从 Target State Entry、CAE-SDB 到 PCN Trace](/zh/notes/how-state-transition-becomes-engineering-data/)

---

## 1. PCN Trace 与传统工程数据的区别

制造现场常见的数据大致可以分为设备状态、生产品质、事件报警和 MES / WCS 运行记录几类。

设备侧会记录运行、停止、Ready（就绪）、位置、转速、温度、电流、压力和能耗；生产侧会记录产量、良率、节拍、OEE、不良数量和停机时间；报警与事件系统会记录报警发生、复位、设备启停、工序开始结束、任务完成或失败；MES / WCS 则会保存任务生成、任务分配、Waiting（等待）、Blocked（阻塞）、Pending（待处理）、资源占用、路径和站点状态。

这些数据能够说明某个设备、任务或工程过程在某个时刻处于什么状态。

例如，现场可能已经保存：

```text
Robot Ready（机器人就绪） = TRUE
安全许可 = TRUE
视觉结果 = OK
下游 Ready（就绪） = FALSE
机器人未动作
```

从这些记录中，可以确认各系统当时的局部状态。

但如果需要继续回答：

> **为什么当时没有进入抓取阶段？**

仅有这些状态值还不够，还需要知道：

- 当时准备进入哪个 Target State；
- 哪些状态与这一次 Target State Entry 直接相关；
- 这些状态在本次迁移中分别承担什么作用；
- 对这些状态执行了什么判定；
- 最终为什么选择当前控制路径；
- 执行以后实际发生了什么。

PCN Trace 围绕这一次 Target State Entry，把这些内容放到同一个状态迁移上下文中。

它与普通运行日志的主要区别，是数据组织单位不同。

传统设备和生产数据通常以设备、事件、任务、工单等为主要记录单位。

PCN Trace 以一次 Target State Entry 的状态迁移判定为主要记录单位，用于回答：

> **本次判定使用了哪些状态，形成了什么判定结果，为什么选择这条控制路径，执行以后发生了什么。**

---

## 2. PCN Trace 记录哪些内容

一个 PCN 对应一个明确的 Target State Entry。

PCN 在系统进入目标状态之前取得相关状态，完成状态映射、判定、控制仲裁和多路径控制，并记录后续执行结果。

一条 PCN Trace 围绕明确的目标状态入口，关联以下内容：

- Current State（当前状态）；
- Target State（目标状态）；
- Target State Entry（目标状态入口）；
- 与本次迁移相关的主要状态；
- C / A / E Mapping；
- S / D / B Evaluation；
- CAE-SDB Result；
- 时间信息 T；
- Arbitration Result；
- Multipath Control；
- Execution Result；
- Trace ID。

例如，对于“进入抓取阶段”这一 Target State Entry，PCN Trace 可以保留本次判定使用的相关状态、形成的 CAE-SDB 判定结果、控制仲裁后选择的控制路径，以及执行后的实际结果。

关键不是单独保存这些字段，而是保持输入状态、判定结果、控制选择和执行结果之间的对应关系。

这些信息共同构成同一次 Target State Entry 的状态迁移判定履历。

### 2.1 CAE-SDB 为什么是 PCN Trace 的判定语义基础

PCN Trace 不是把 PLC、机器人、MES / WCS、安全系统和下游设备中的状态重新集中保存一次。

与同一 Target State Entry 相关的状态，首先通过 C / A / E Mapping 明确其在本次状态迁移中的功能角色：

- **C = Condition**：进入目标状态所需条件是否具备；
- **A = Authority**：当前是否允许进入目标状态；
- **E = Execution Chain**：进入目标状态以后执行链是否能够继续接续。

随后，再通过 S / D / B Evaluation 对相关状态执行已经定义的判定：

- **S = Structure**：判定所需结构是否已经建立；
- **D = Dynamics**：当前状态是否仍然有效；
- **B = Boundary**：当前状态是否仍处于预先定义的允许边界内。

在这个结构下，PCN Trace 保存的内容就不只是原始状态值，还包括：

- 对应哪一次 Target State Entry；
- 哪些状态参与了判定；
- 这些状态承担什么迁移功能角色；
- 对这些状态执行了什么判定；
- 形成了什么 CAE-SDB Result；
- 为什么选择当前控制路径；
- 最终得到什么 Execution Result。

CAE-SDB 为与同一 Target State Entry 相关的异构状态建立统一的状态迁移判定语义。

PCN Trace 再将这种判定语义与控制选择和执行结果保持在同一条履历中。

如果缺少这一层结构化判定，Trace 很容易重新变成状态值、报警和事件的汇总，而难以直接说明一次状态迁移为什么形成当前结果。

因此：

> **CAE-SDB 是 PCN Trace 形成状态迁移判定语义的基础。**

本文公开到 PCN Trace 的基本组成和工程作用。详细字段结构、存储方式、索引、版本绑定和回放机制属于具体产品实现范围。

---

## 3. PCN Trace 积累后可以看什么

PCN Trace 持续积累以后，可以按 Target State Entry 对判定结果、控制结果和执行结果进行统计和比较。

例如：

- 某类 C-D 长期集中出现时，可以检查条件状态相关的数据刷新、同步和有效时间；
- A-D 长期集中出现时，可以检查许可更新、撤销和状态切换；
- E-D 长期集中出现时，可以检查下游接收、资源状态和系统间时序；
- 某类控制路径反复出现时，可以继续比较其对应的执行结果；
- 工程修改前后，可以比较相同 PCN 的判定结果、控制路径和执行结果是否发生变化。

这里关注的不是单独某个信号，而是同一类状态迁移中反复出现的判定结果、控制路径，以及它们最终对应的执行结果。

PCN Trace 首先提供稳定、可比较的状态迁移履历。

在此基础上，可以根据实际问题继续进行规则统计、趋势分析、跨 Trace 比较、模式归纳或报告整理。

大语言模型可以辅助履历比较、模式归纳和改善候选整理，但其输入是已经形成的结构化状态迁移履历，不作为现场状态迁移许可的直接来源。

工程修改仍由工程师结合设备、工艺、安全、生产和维护要求进行确认。

修改实施以后继续生成新的 PCN Trace，就可以比较修改前后的运行情况。

这样，PCN Trace 除了用于事后追查，也可以成为持续工程改善的比较基础。

---

## 4. PCN Trace 在 PLC / HMI、MES / WCS 和制造 DX 中的使用

### 4.1 PLC / HMI

PLC / HMI 原本已经能够显示信号、Ready（就绪）、Interlock（联锁）、Alarm（报警）、顺序状态和设备状态。

增加 PCN Trace 后，可以把 Current State、Target State、Target State Entry、时间信息 T、CAE-SDB 判定结果、控制仲裁结果、多路径控制、执行结果和 Trace ID（履历标识）放到同一个状态迁移上下文中。

例如 HMI 可以显示：

```text
Target State（目标状态）：抓取阶段

CAE-SDB Result（CAE-SDB 判定结果）：C-D

判定内容：视觉识别结果超出有效时间

Arbitration Result（控制仲裁结果）：优先重新识别

Multipath Control（多路径控制）：重新识别
```

现场人员可以直接看到当前不能进入哪个目标状态、判定落在哪个 CAE-SDB 位置，以及系统为什么采用当前控制路径。

### 4.2 MES / WCS

MES / WCS 通常已经保存任务、车辆、站点、路径、资源，以及 Waiting（等待）、Blocked（阻塞）、Pending（待处理）等运行状态。

PCN Trace 可以把这些信息对应到具体 Target State Entry，形成一次完整的状态迁移判定履历。

在协同停滞分析中，除了确认某个任务是否处于 Waiting，还可以继续查看：

- Waiting 出现在什么 Target State Entry；
- 哪些条件和许可参与了判定；
- 当前 Execution Chain 中哪些状态影响了进入；
- 形成了什么 CAE-SDB Result；
- 最终选择了什么 Multipath Control；
- 对应的 Execution Result 如何。

这样，MES / WCS 原有的任务和资源数据就可以与具体的状态迁移判定履历建立对应关系。

### 4.3 制造 DX

制造 DX 通常基于设备数据、生产数据和事件数据进行可视化、分析和改善。

对于状态迁移问题，需要先明确观察的是哪一个 Target State Entry。

随后，CAE-SDB 为与这一入口相关的异构状态建立统一的状态迁移判定语义，PCN Trace 再将判定、控制和执行结果持续保存为状态迁移履历。

PCN Trace 由此增加了“状态迁移判定”这一类分析对象。

设备 / 生产数据和 PCN Trace 的主要区别如下。

| 项目 | 设备 / 生产数据 | PCN Trace |
|---|---|---|
| 主要记录对象 | 设备、工程、任务、生产结果 | 一次 Target State Entry 的状态迁移判定 |
| 主要确认内容 | 系统发生了什么 | 使用了哪些状态、形成了什么判定、选择了什么控制、结果如何 |
| 数据组织单位 | 设备、时间、任务、工单、事件 | PCN、Target State Entry、Current State、Target State、T |
| 主要分析对象 | 稼动、性能、质量、异常、产量 | C / A / E、S / D / B、CAE-SDB Result、Arbitration、Multipath Control、Execution Result |
| 主要改善对象 | 设备、工程、保全、生产过程 | 状态迁移条件、许可、执行链、控制边界、控制路径 |
| 改善确认 | OEE、节拍、产量、报警、质量等 | 改善后 Trace 中判定、控制和执行结果的变化 |

这样，制造 DX 除了设备和生产数据，还可以把状态迁移本身作为具有明确工程语义、可长期比较和分析的数据对象。

### 4.4 与 PCN Network（PCN 网络）结合

单个 PCN Trace 记录一次 Target State Entry 的状态迁移判定履历。

多个 PCN 的履历持续积累后，还可以进一步分析不同目标状态入口之间的状态影响关系。

相关内容参见：

- [多个 PCN 如何形成状态迁移前置控制网络？](/zh/notes/pcn-network-structure/)
- [为什么 OEE 之后还需要 PCN？](/zh/notes/why-oee-pcn/)

---

## 总结

制造现场已经持续记录设备数据、生产数据、任务数据、报警数据和事件数据。

PCN Trace 将这些状态信息放回一次明确的 Target State Entry 中，并把状态映射、判定结果、控制仲裁、多路径控制、执行结果和时间信息保持在同一条状态迁移履历中。

它带来的核心变化，是增加了一个以 Target State Entry 为中心的数据组织单位。

CAE-SDB 为这一入口相关的异构状态提供统一的状态迁移判定语义，PCN Trace 则继续保持判定依据、控制选择和实际执行结果之间的对应关系。

本文所说的“新的工程数据”，可以概括为：

> **把一次 Target State Entry 对应的状态迁移判定作为可以持续记录、比较、统计和分析的数据对象。**

通过 PCN Trace，可以确认本次判定使用了哪些状态、这些状态在本次迁移中承担什么作用、形成了什么 CAE-SDB 判定结果、经过什么控制仲裁、选择了哪条多路径控制，以及最终得到什么执行结果。

长期积累以后，还可以比较不同 Target State Entry 上反复出现的问题、判定结果分布、控制路径选择趋势、执行结果以及工程修改前后的变化。

> **PCN Trace 的价值不在于多保存几个字段，而在于把判定依据、判定结果、控制选择和执行结果保持在同一个状态迁移语义中。**

---

## 进一步阅读

- [Concepts｜核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)
- [为什么是 CAE-SDB？——目标状态入口前的双轴结构化分析方法](/zh/notes/why-cae-sdb/)
- [状态迁移如何形成可分析的工程数据？——从 Target State Entry、CAE-SDB 到 PCN Trace](/zh/notes/how-state-transition-becomes-engineering-data/)
- [为什么 OEE 之后还需要 PCN？](/zh/notes/why-oee-pcn/)
- [多个 PCN 如何形成状态迁移前置控制网络？](/zh/notes/pcn-network-structure/)
- [为什么智能算法与物理执行控制之间，需要状态迁移前置控制？](/zh/notes/why-production-lines-still-need-deterministic-control/)
- [TPCA 的状态迁移单向性——为什么真实工程系统不存在状态回退？](/zh/notes/tpca-unidirectional-state-transition/)

---

## 文档信息

题目：为什么 PCN Trace 是一种新的工程数据？  
文档类型：技术札记  
版本：Public Note Version 1.7  
首次发布日期：2026-07-14  
最后更新：2026-09-18  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/why-pcn-trace-is-engineering-data/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
