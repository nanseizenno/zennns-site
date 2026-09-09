---
title: "为什么 PCN Trace 是一种新的工程数据？"
summary: "说明 PCN Trace 如何把一次目标状态入口中使用的输入状态、CAE-SDB 判定结果、控制仲裁、多路径控制、执行结果和时间信息 T 关联为一条状态迁移判定履历，并说明其分析与改善价值。"
description: "从设备数据、生产数据和报警履历的区别出发，说明 PCN Trace 以目标状态入口为单位记录判定、控制和执行结果的结构，以及其在 PLC / HMI、MES / WCS 和制造 DX 中的应用。"
date: 2026-07-14
lastmod: 2026-09-09
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.6"
citation_url: "https://zennns.com/zh/notes/why-pcn-trace-is-engineering-data/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## 为什么 PCN Trace 是一种新的工程数据？

制造现场已经积累了大量数据。PLC 记录设备状态和报警，MES 保存生产履历，WCS 保存任务和调度记录，设备平台还会持续采集温度、电流、位置、节拍和运行时间。

这些数据通常围绕设备、任务、工单、报警或事件进行整理。

PCN Trace（状态迁移判定履历）增加了另一个记录对象：

> **一次 Target State Entry（目标状态入口）对应的状态迁移判定。**

对于一次明确的目标状态入口，PCN Trace 将本次判定使用的状态、CAE-SDB Result（CAE-SDB 判定结果）、Arbitration（控制仲裁）结果、Multipath Control（多路径控制）、Execution Result（执行结果）以及时间信息 T 关联起来。

基本关系可以表示为：

```text
判定使用的状态
→ CAE-SDB Result（CAE-SDB 判定结果）
→ Arbitration（控制仲裁）
→ Multipath Control（多路径控制）
→ Execution Result（执行结果）
```

这些内容不是分别保存后再由工程师事后拼接，而是作为同一次目标状态入口的判定履历进行关联。

本文所说的“新的工程数据”，并不是指履历记录本身是新的，也不是指增加新的传感器数据类型，而是指：

> **把一次目标状态入口的判定、控制和执行结果作为独立的数据对象，持续记录、比较、统计和分析。**

基础概念可参见：

- [Concepts｜核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)
- [为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)

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

从这些记录中，可以确认各系统当时的局部状态。但如果需要进一步回答“为什么当时没有进入抓取阶段”，还需要知道这些状态在本次目标状态入口中分别承担什么作用、经过了什么判定、最终为什么选择了当前控制路径。

PCN Trace 围绕这一次目标状态入口，把这些内容放到同一个判定上下文中。

例如可以同时关联当前状态、目标状态、主要输入状态、C / A / E Mapping（状态映射）、S / D / B Evaluation（判定）、CAE-SDB 判定结果、控制仲裁结果、多路径控制、执行结果和时间信息 T。

两类数据的主要区别可以概括为：

```text
传统设备 / 生产数据：
以设备、事件、任务、工单等为主要记录单位

PCN Trace：
以一次目标状态入口的状态迁移判定为主要记录单位
```

因此，PCN Trace 更适合回答：

> **本次判定使用了哪些状态，形成了什么判定结果，为什么选择这条控制路径，执行以后发生了什么。**

---

## 2. PCN Trace 记录哪些内容

一个 PCN 对应一个明确的目标状态入口。

基本关系如下：

```text
Current State（当前状态）
    ↓
Target State Entry（目标状态入口） / PCN
    ↓
Target State（目标状态）
```

PCN 在进入目标状态之前获取相关状态，并形成：

```text
相关状态
→ C / A / E Mapping（状态映射）
→ S / D / B Evaluation（判定）
→ CAE-SDB Result（CAE-SDB 判定结果） + T
→ Arbitration（控制仲裁）
→ Multipath Control（多路径控制）
→ Execution Result（执行结果）
→ PCN Trace（状态迁移判定履历）
```

一条 PCN Trace 可以关联以下信息。

| 项目 | 记录内容 |
|---|---|
| PCN | 对应哪个目标状态入口 |
| Current State（当前状态） | 判定时系统所处的当前状态 |
| Target State（目标状态） | 本次准备进入的目标状态 |
| 主要输入状态 | 本次判定实际使用的相关状态 |
| 时间信息 T | 状态、判定、控制和执行对应的时间信息 |
| C / A / E Mapping（状态映射） | 各输入状态在本次迁移中的工程作用 |
| S / D / B Evaluation（判定） | 对相关状态执行的判定 |
| CAE-SDB Result（CAE-SDB 判定结果） | 本次形成的结构化判定结果 |
| Arbitration Result（控制仲裁结果） | 对多个判定结果和关键约束进行仲裁后的结果 |
| Multipath Control（多路径控制） | 本次选定的控制路径 |
| Execution Result（执行结果） | 控制执行后的实际结果 |
| Trace ID（履历标识） | 识别本次状态迁移判定的标识 |

例如：

```text
PCN：抓取入口

Current State（当前状态）：等待抓取

Target State（目标状态）：抓取阶段

CAE-SDB Result（CAE-SDB 判定结果）：C-D

判定内容：视觉识别结果超出有效时间

Arbitration Result（控制仲裁结果）：优先执行重新识别

Multipath Control（多路径控制）：重新识别

Execution Result（执行结果）：取得新的视觉识别结果

Trace ID（履历标识）：PCN-XXXX-XXXX
```

这里真正需要保留的是：

```text
输入状态
→ 判定结果
→ 控制选择
→ 执行结果
```

这四部分属于同一次目标状态入口的完整判定履历。

本文公开到 PCN Trace 的基本组成和工程作用。详细字段结构、存储方式、索引、版本绑定和回放机制属于具体产品实现范围。

---

## 3. PCN Trace 积累后可以看什么

PCN Trace 持续积累以后，可以按目标状态入口对判定结果、控制结果和执行结果进行统计和比较。

例如，某些 CAE-SDB 判定结果长期集中出现时，可以直接缩小工程检查范围。

| Trace 中反复出现的结果 | 主要检查方向 |
|---|---|
| C-S 集中 | 条件状态所需的信号、接口、映射和对象定义 |
| C-D 持续 | 数据刷新、同步、时间有效性、识别结果有效性 |
| C-B 高频 | 条件值、置信度、位置偏差、时间等控制边界 |
| A-S 集中 | 许可来源、权限接口、资源许可结构 |
| A-D 持续 | 许可更新、同步、撤销和状态切换 |
| A-B 高频 | 许可范围、时间窗口和相关控制边界 |
| E-S 集中 | 当前执行链所需的下游、接口及结果回写结构 |
| E-D 持续 | 下游接收、执行链、资源状态和系统间时序 |
| E-B 高频 | 容量、等待时间、资源利用范围等控制边界 |
| 某一 Multipath Control（多路径控制）高频出现 | 对应入口的控制条件、优先关系和候选路径 |
| 某类 Result（结果）与 Execution Result（执行结果）长期组合出现 | 控制路径与实际执行结果之间的关系 |

例如，某个 PCN 长期出现与视觉结果有效性有关的 C-D，可以优先检查识别结果的更新、同步和有效时间设置。改善后继续记录同一 PCN 的 Trace，即可比较 C-D 的出现频率、相关控制路径和实际执行结果是否发生变化。

改善过程可以表示为：

```text
PCN 运行
    ↓
PCN Trace
    ↓
统计与比较
    ↓
确定状态迁移上的改善对象
    ↓
工程修改
    ↓
重新运行
    ↓
新的 PCN Trace
    ↓
改善前后比较
```

因此，PCN Trace 不只用于事后追查，也可以用于持续确认状态迁移条件、许可、执行链、控制边界和控制路径的运行表现。

---

## 4. PCN Trace 在 PLC / HMI、MES / WCS 和制造 DX 中的使用

### 4.1 PLC / HMI

PLC / HMI 原本已经能够显示信号、Ready（就绪）、Interlock（联锁）、Alarm（报警）、顺序状态和设备状态。

增加 PCN Trace 后，可以进一步把当前状态、目标状态、目标状态入口、时间信息 T、CAE-SDB 判定结果、控制仲裁结果、多路径控制、执行结果和 Trace ID（履历标识）放到同一个状态迁移上下文中。

例如 HMI 可以显示：

```text
Target State（目标状态）：抓取阶段

CAE-SDB Result（CAE-SDB 判定结果）：C-D

判定内容：视觉识别结果超出有效时间

Arbitration Result（控制仲裁结果）：优先重新识别

Multipath Control（多路径控制）：重新识别
```

这样，现场人员可以直接看到当前不能进入哪个目标状态、判定落在哪个 CAE-SDB 位置，以及系统为什么采用当前控制路径。

### 4.2 MES / WCS

MES / WCS 通常已经保存任务、车辆、站点、路径、资源，以及 Waiting（等待）、Blocked（阻塞）、Pending（待处理）等运行状态。

PCN Trace 可以把这些信息继续对应到具体的目标状态入口，形成一次完整的状态迁移判定记录。

在协同停滞分析中，不只是看某个任务是否处于 Waiting（等待），还可以继续确认 Waiting 出现在什么入口、哪些许可参与了判定、当前 Execution Chain（执行链）中哪个状态影响了进入，以及最终选择了什么 Multipath Control（多路径控制）。

这样，MES / WCS 原有任务和资源数据就可以与具体的状态迁移判定履历对应起来。

### 4.3 制造 DX

制造 DX 通常基于设备数据、生产数据和事件数据做可视化、分析和改善。

PCN Trace 增加的是状态迁移判定这一类分析对象：

```text
状态迁移前判定
→ PCN Trace
→ 状态迁移模式分析
→ 工程改善
→ 重新运行
→ Trace 比较
```

设备 / 生产数据和 PCN Trace 的主要区别如下。

| 项目 | 设备 / 生产数据 | PCN Trace |
|---|---|---|
| 主要记录对象 | 设备、工程、任务、生产结果 | 一次目标状态入口的状态迁移判定 |
| 主要确认内容 | 系统发生了什么 | 使用了哪些状态、形成了什么判定、选择了什么控制、结果如何 |
| 数据组织单位 | 设备、时间、任务、工单、事件 | PCN、Target State Entry（目标状态入口）、Current State（当前状态）、Target State（目标状态）、T |
| 主要分析对象 | 稼动、性能、质量、异常、产量 | C / A / E、S / D / B、CAE-SDB Result（判定结果）、Arbitration（控制仲裁）、Multipath Control（多路径控制）、Execution Result（执行结果） |
| 主要改善对象 | 设备、工程、保全、生产过程 | 状态迁移条件、许可、执行链、控制边界、控制路径 |
| 改善确认 | OEE、节拍、产量、报警、质量等 | 改善后 Trace 中判定、控制和执行结果的变化 |

这样，状态迁移判定本身也可以成为制造 DX 的分析对象。

### 4.4 与 PCN Network（PCN 网络）结合

单个 PCN Trace 记录一次目标状态入口的判定履历。多个 PCN 的 Trace 与 PCN Network（PCN 网络）中的状态推进、许可、资源、执行和状态更新关系对应起来后，可以进一步分析多个目标状态入口之间的问题传递。

相关说明参见：

- [多个 PCN 如何形成状态迁移前置控制网络？](/zh/notes/pcn-network-structure/)
- [为什么 OEE 之后还需要 PCN？](/zh/notes/why-oee-pcn/)

---

## 总结

制造现场已经持续记录设备数据、生产数据、任务数据、报警数据和事件数据。

PCN Trace 的不同之处在于，它把这些状态信息放回一次明确的目标状态入口中，并形成：

```text
相关状态
→ C / A / E Mapping（状态映射）
→ S / D / B Evaluation（判定）
→ CAE-SDB Result（CAE-SDB 判定结果） + T
→ Arbitration（控制仲裁）
→ Multipath Control（多路径控制）
→ Execution Result（执行结果）
→ PCN Trace（状态迁移判定履历）
```

本文所说的“新的工程数据”，指的是：

> **把一次目标状态入口对应的状态迁移判定作为可以持续记录、比较、统计和分析的数据对象。**

通过 PCN Trace，可以确认本次判定使用了哪些状态、形成了什么 CAE-SDB 判定结果、经过什么控制仲裁、选择了哪条多路径控制，以及最终得到什么执行结果。

长期积累以后，还可以比较不同目标状态入口上反复出现的问题、判定结果分布、控制路径选择趋势、执行结果及工程修改前后的变化。

PCN Trace 的价值不在于多保存几个字段，而在于把判定依据、判定结果、控制选择和执行结果保持在同一个状态迁移语义链中。

---

## 进一步阅读

- [Concepts｜核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)
- [为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)
- [为什么 OEE 之后还需要 PCN？](/zh/notes/why-oee-pcn/)
- [多个 PCN 如何形成状态迁移前置控制网络？](/zh/notes/pcn-network-structure/)
- [TPCA 的状态迁移单向性——为什么真实工程系统不存在状态回退？](/zh/notes/tpca-unidirectional-state-transition/)

---

## 文档信息

题目：为什么 PCN Trace 是一种新的工程数据？  
文档类型：技术札记  
版本：Public Note Version 1.6  
首次发布日期：2026-07-14  
最后更新：2026-09-09  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/why-pcn-trace-is-engineering-data/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
