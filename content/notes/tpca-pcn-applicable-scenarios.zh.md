---
title: "TPCA / PCN 适用场景分析"
summary: "从 Target State Entry（目标状态入口）是否明确、相关状态是否可观测、判定结果是否能够连接实际控制、以及是否能够形成 PCN Trace（状态迁移判定履历）四个方面，说明 TPCA / PCN 的适用条件和工程边界。"
description: "说明 TPCA / PCN 的适用场景与工程边界，并给出 Target State Entry、状态可观测性、控制连接和履历形成四项基本判断条件。"
date: 2026-07-05
lastmod: 2026-09-09
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.4"
citation_url: "https://zennns.com/zh/notes/tpca-pcn-applicable-scenarios/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

# TPCA / PCN 适用场景分析

TPCA / PCN 将明确的 Target State Entry（目标状态入口）作为可以独立设计、判定、控制和记录的工程对象。

因此，判断一个对象是否适合设置 PCN，首先要确认这个目标状态入口本身能否成立。

基本上可以先看四点：

```text
Target State Entry（目标状态入口）明确
→ 相关状态可观测
→ 判定结果能够连接实际控制
→ 可以设计形成 PCN Trace（状态迁移判定履历）的结构
```

PCN（Pre-Control Node，前置控制节点）设置在明确的目标状态入口之前。

实际工程中，更需要判断的是：

> **这里是否存在一个值得独立设计、判定、控制和记录的 Target State Entry。**

---

## 1. 判断 PCN 是否适用的四个条件

### 1.1 Target State Entry（目标状态入口）明确

首先需要能够明确 Current State（当前状态）和 Target State（目标状态）。

```text
Current State（当前状态）
    ↓
Target State Entry（目标状态入口） / PCN
    ↓
Target State（目标状态）
```

例如：

- 等待抓取 → 抓取阶段；
- 任务已分配 → 开始搬送；
- 保全完成 → 恢复自动运行；
- 质量确认完成 → 进入下一工序。

如果目标状态入口本身无法明确，PCN 的判定对象和控制边界也难以稳定定义。

### 1.2 相关状态可观测

与本次 Target State Entry 直接相关的主要状态，需要能够由系统取得、记录或可靠确认。

状态可能来自 PLC、机器人控制器、安全系统、MES / WCS、视觉系统、质量系统、HMI、扫码系统以及其他设备或软件接口。

数据来源可以不同，但这些状态必须能够对应到当前目标状态入口，并实际参与本次判定。

### 1.3 判定结果能够连接实际控制

PCN 的判定结果需要连接到当前 Target State Entry 的实际控制。

典型控制结果可以包括允许进入、等待、重新确认、重试、替代路径、人工确认、禁止进入和安全锁定等。

如果判定结果只用于分析、报表或事后说明，而不进入实际控制，则更接近分析用途，不属于 PCN 的主要控制对象。

### 1.4 可以设计形成 PCN Trace 的结构

一次 Target State Entry 至少应能够记录本次使用了哪些状态、形成了什么判定结果、选择了什么控制路径，以及执行结果如何。

这些内容形成 PCN Trace 后，才能按目标状态入口进行后续追踪、比较和改善。

因此，PCN 的基本适用条件可以概括为：

> **明确的目标状态入口 + 可观测的相关状态 + 能够进入控制的判定 + 可追踪的履历结构。**

---

## 2. 代表性的适用场景

### 2.1 自动化执行单元

机器人抓取、检测、压装、搬送交接、上下料以及正常路径与异常路径切换，通常都具有比较明确的物理执行阶段。

这类场景中，Current State、Target State 和物理执行阶段边界容易确定，因此目标物理执行阶段进入前是典型的 PCN 配置位置。

相关案例：

- [自动化执行单元前置判定案例](/zh/cases/automation-execution-unit-pre-control/)

### 2.2 MES / WCS 与多设备协同

AGV / AMR 群控、任务执行、资源使用、路径与站点协调、下游接收以及多设备协同状态迁移，也可以形成明确的 Target State Entry。

这类场景的特点是，单个设备或系统可能没有明显故障，但任务、许可、资源和执行状态共同决定一次协同状态迁移。

只要目标状态入口明确，相关状态能够被观测，就可以作为 PCN 的工程对象进行整理。

相关案例：

- [MES / WCS 协同停滞诊断模块案例](/zh/cases/collaborative-stagnation-diagnosis/)

### 2.3 制造 DX 与跨系统状态迁移

质量放行后的下一工序进入、工序切换、异常处理后的状态迁移、保全完成后的自动运行恢复、人工确认后的自动运行恢复，以及 MES、质量系统、设备和下游系统之间的状态迁移，也属于常见对象。

这类场景通常已经存在大量数据，但“能否进入下一阶段”的判断分散在多个系统或人员环节中。

PCN 可以把这些状态重新对应到一个明确的目标状态入口，形成同一工程上下文下的判定、控制和履历。

相关案例：

- [生产 DX 状态迁移条件设计与履历分析案例](/zh/cases/production-dx-state-transition/)

### 2.4 数字系统中的明确执行入口

TPCA / PCN 也可以用于具有明确 Target State Entry 和可控制执行路径的数字系统。

例如高成本服务调用、Tool Call（工具调用）、API 执行、自动部署执行以及其他明确的数字执行入口。

判断重点仍然相同：

> **是否存在一个实际会执行、并且能够根据判定结果进行控制的 Target State Entry。**

### 2.5 包含人工确认的系统

人的参与本身并不排除 PCN。

如果人工确认结果已经成为系统可以读取和记录的明确状态，例如 HMI 人工确认、扫码结果、质量放行、保全解除或恢复确认，就可以参与当前 Target State Entry 的判定。

关键不是“有没有人参与”，而是这个结果是否已经成为可靠的工程状态，并能够进入实际控制和履历。

---

## 3. TPCA / PCN 的适用边界

TPCA / PCN 的适用边界主要由四个因素决定：

```text
Target State Entry（目标状态入口）
可观测性
可控制性
可追踪性
```

如果目标状态入口无法明确、主要状态无法观测、判断高度依赖未记录的主观信息、判定结果不能连接实际控制，或者无法设计形成 PCN Trace 的履历结构，就很难作为 PCN 的主要工程对象。

普通会议、组织决策、单纯统计报表以及不进入控制的 BI 分析，往往不满足这些条件。

即使包含人工确认，只要确认结果能够被系统记录为明确状态，并实际参与目标状态入口控制，仍然可以纳入 PCN。

因此，适用边界不是由行业名称决定，而是由目标状态入口是否能够稳定形成可观测、可判定、可控制、可追踪的工程结构决定。

---

## 4. 一个简化的适用性检查

面对新的应用对象，可以先检查四个问题。

### 1. 能否明确 Target State Entry

是否能够定义：

```text
Current State（当前状态）
    ↓
Target State Entry（目标状态入口）
    ↓
Target State（目标状态）
```

### 2. 相关状态能否观测

本次状态迁移需要的主要状态，是否能够从系统中取得、记录或可靠确认。

### 3. 判定结果能否连接控制

判定结果是否会实际影响当前 Target State Entry 的控制路径。

### 4. 能否形成 PCN Trace

输入状态、判定结果、控制结果和执行结果，是否能够围绕同一次状态迁移形成履历。

简化后可以写成：

```text
Target State Entry
→ Observable State（可观测状态）
→ Control（控制）
→ Trace（履历）
```

这四项成立后，再进一步设计：

```text
相关状态
→ C / A / E Mapping（状态映射）
→ S / D / B Evaluation（判定）
→ CAE-SDB Result（CAE-SDB 判定结果） + T
→ Arbitration（控制仲裁）
→ Multipath Control（多路径控制）
→ PCN Trace（状态迁移判定履历）
```

详细定义可参见：

- [Concepts｜核心概念](/zh/concepts/)

---

## 工程结论

TPCA / PCN 的适用边界可以概括为：

> **存在明确的 Target State Entry，并且能够对该入口进行观测、判定和控制，同时可以设计形成 PCN Trace 的履历结构，就具备将其作为 PCN 工程对象进行设计的基础。**

选择 PCN 时，真正需要确认的是：

> **这里是否存在一个值得独立设计、判定、控制和记录的 Target State Entry。**

如果答案明确，就可以继续进入具体的 PCN 设计。

---

## 进一步阅读

- [Concepts｜核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)
- [应用案例](/zh/cases/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)

---

## 文档信息

题目：TPCA / PCN 适用场景分析  
文档类型：技术札记  
版本：Public Note Version 1.4  
首次发布日期：2026-07-05  
最后更新：2026-09-09  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/tpca-pcn-applicable-scenarios/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
