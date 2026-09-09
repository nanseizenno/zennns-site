---
title: "TPCA / PCN 与既有工业自动化技术和工程方法的关系"
summary: "从 Target State Entry 出发，说明 TPCA / PCN 与 FMEA、STPA、RCA、Process Mining、状态机、SFC、Interlock、安全控制、MES / WCS、AI 分析等既有技术之间的工程分工。"
description: "说明在既有工业自动化方法和控制机制各自承担原有职责的情况下，TPCA / PCN 如何围绕 Target State Entry 组织状态迁移前判定、控制和履历。"
date: 2026-07-04
lastmod: 2026-09-09
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.3"
citation_url: "https://zennns.com/zh/notes/tpca-existing-theories/"
draft: false
weight: 1
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## TPCA / PCN 与既有工业自动化技术和工程方法的关系

工业自动化领域已经形成了大量成熟方法和控制机制。状态机、SFC、Interlock、安全控制、报警管理、MES / WCS 主要服务于状态管理、顺序控制、安全、任务和资源协调；FMEA、STPA、RCA、Process Mining 则分别用于风险分析、安全分析、原因分析和过程履历分析。

TPCA / PCN 不替代这些方法。

它关注的是另一个工程位置：当系统准备进入一个明确的 Target State Entry 时，如何把分散在不同设备和系统中的相关状态组织起来，形成一次完整的状态迁移前判定、控制和履历。

基本关系如下：

```text
Current State
    ↓
Target State Entry / PCN
    ↓
Target State
```

在 PCN 内部，与本次 Target State Entry 直接相关的状态被接入以下处理链：

```text
相关状态
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

本文不展开介绍各类既有技术本身，只说明它们与 TPCA / PCN 在工程系统中的职责关系。

基础概念可参见：

- [Concepts｜核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)

---

## 1. 与分析和诊断方法的关系

FMEA、STPA、RCA 和 Process Mining 都可以用于复杂工程问题分析，但处理对象和使用位置并不相同。

| 方法 | 主要对象 |
|---|---|
| FMEA | 潜在失效模式、影响、原因和控制措施 |
| STPA / STAMP | 安全控制结构、控制约束和危险场景 |
| RCA | 已发生问题及其原因关系 |
| Process Mining | 基于事件日志还原的实际流程、偏差、等待和瓶颈 |
| TPCA / PCN | 明确 Target State Entry 上的状态迁移前判定、控制和履历 |

例如某项许可状态出现问题时，FMEA 可以分析与该许可相关的失效模式及影响，STPA 可以分析其安全控制结构和约束，RCA 可以用于追查已经发生的问题原因，Process Mining 可以从事件日志中观察这种问题对流程等待或偏差的影响。

PCN 所处的位置不同。它在实际运行中读取这项许可状态，并判断它在本次 Target State Entry 中是否属于 A：Authority，以及当前是否满足进入要求。

因此，这些方法可以同时用于同一个系统，但承担的工程任务不同。分析方法用于识别风险、原因或流程问题，PCN 则把运行时状态放回当前 Target State Entry 中进行判定和控制。

STPA / STAMP 的公开资料可参见 MIT 的 STPA Handbook，Process Mining 可参见 van der Aalst 的相关体系资料。[1][2]

---

## 2. 与状态机、SFC、Interlock 和安全控制的关系

### 2.1 状态机和 SFC

状态机和 SFC 用于组织状态、步骤、动作和迁移关系，是工业控制中成熟的顺序控制方法。

例如设备原有的迁移条件可以写成：

```text
Vision_OK
AND Robot_Ready
AND Safety_OK
AND Downstream_Ready
```

这样的逻辑可以继续作为设备控制条件使用。TPCA / PCN 并不要求重新实现一套状态机，也不要求把现有 SFC 改写成新的控制结构。

PCN 关注其中某一个明确的 Target State Entry。它把与这次迁移有关的状态对应起来，并继续形成 CAE-SDB Result、Arbitration、Multipath Control 和 PCN Trace。

因此，状态机和 SFC 主要负责状态及顺序关系，PCN 负责 Target State Entry 单位的前置判定、控制和履历。

IEC 61131-3 及 PLCopen 的公开资料可作为 SFC 和 PLC 编程语言体系的参考。[3]

### 2.2 Interlock / Handshake

Interlock 和 Handshake 用于构成设备动作条件和设备间协同条件。

这些既有条件可以直接作为 PCN 的相关状态或既有约束使用。对于当前 Target State Entry，PCN 进一步区分某个状态在本次迁移中承担的是 Condition、Authority 还是 Execution Chain，并按需要执行 Structure、Dynamics 或 Boundary 判定。

例如，同一个 Handshake 状态可能表示对方设备允许接收，也可能只是表示接口在线。两者在当前 Target State Entry 中的工程含义并不相同。

PCN 的作用不是替代 Interlock 或 Handshake，而是把这些已有状态放回明确的状态迁移入口中，说明它们为什么参与本次判定。

### 2.3 安全控制

安全 PLC、安全继电器、安全门、光栅、急停和安全扫描器等用于实现机械安全功能。

PCN 可以读取安全系统输出的许可状态，并将关键安全许可作为当前 Target State Entry 中与 A：Authority 有关的状态。关键 A 不成立时，即使其他 C 和 E 状态均满足，也不得允许进入目标状态。

安全系统负责安全功能本身，PCN 不替代安全回路或安全控制逻辑。PCN 只是把安全许可作为本次 Target State Entry 的必要约束，与其他相关状态一起参与前置判定。

机械安全相关控制系统的设计原则可参见 ISO 13849-1。[4]

### 2.4 报警管理和故障诊断

报警管理和故障诊断用于处理异常状态、故障原因、响应和履历。

这些结果也可以作为 PCN 的相关状态使用，但其工程含义仍取决于当前 Target State Entry。

例如，同样是通信异常，如果影响的是视觉结果有效性，可能进入 C 相关判定；如果影响上位系统许可，可能进入 A；如果影响后续结果回写，则可能与 E 有关。

PCN 并不重新定义报警或故障，而是确认这些异常对当前状态迁移入口实际产生什么影响。

---

## 3. 与 MES / WCS 和 AI 的关系

### 3.1 MES / WCS

MES、WCS 和群控系统本身已经承担任务、资源、路径、站点、调度和执行状态等管理功能。

例如现场可能已经看到：

```text
MES：任务已生成
WCS：存在任务记录
设备：在线
车辆：在线
```

但对于一个具体 Target State Entry，这些信息未必已经足够。还可能需要确认任务状态是否仍然有效、必要许可是否成立、资源锁是否允许进入、路径是否可用、下游是否能够接收，以及进入 Target State 后的 Execution Chain 是否能够继续。

MES / WCS 继续承担原有的任务、资源和调度功能。PCN 则针对其中重要的 Target State Entry，把分散在多个系统中的相关状态放到同一次状态迁移判定中。

制造运营与企业系统、控制系统之间的集成边界，可参见 ISA-95 / IEC 62264 系列。[5]

### 3.2 AI / 数据分析

AI 和数据分析更适合用于 PCN Trace 形成后的履历分析。

长期运行后，可以基于 Trace 比较不同入口的运行情况，识别重复问题、提取模式、比较工程修改前后的结果，并辅助整理改善候选和工程报告。

PCN 本身负责 Target State Entry 上的运行时前置判定和控制。AI 不直接替代这部分工程规则，而是利用已有履历做后续分析和改善支持。

两者分别处于不同的工程位置：PCN 面向当前这一次状态迁移，AI 主要面向已经形成的历史数据。

---

## 4. TPCA / PCN 在整个工程体系中的位置

TPCA / PCN 使用的很多单项状态和控制概念，在既有工业自动化中本来就存在，例如 Condition、Authority、Ready、Interlock、安全许可、报警、超时、等待、重试和降级运行。

TPCA / PCN 的重点不在于重新定义这些单项机制，而在于把它们围绕一个明确的 Target State Entry 组织到同一个工程关系中：

```text
Current State
    ↓
Target State Entry / PCN
    ↓
Target State

PCN 内部：
相关状态
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

既有系统与 PCN 的主要分工如下。

| 既有对象 | 主要职责 | 与 PCN 的关系 |
|---|---|---|
| PLC / 状态机 / SFC | 状态管理、顺序控制、动作执行 | 提供本次 Target State Entry 所需状态，并执行相应控制逻辑 |
| Interlock / Handshake | 动作条件和设备间协同条件 | 作为相关状态或既有约束参与判定 |
| 安全系统 | 安全功能、安全许可、危险动作限制 | 提供与关键 A 有关的许可状态 |
| 报警管理 / 故障诊断 | 异常管理、故障状态和原因分析 | 其结果可作为相关状态参与判定 |
| MES / WCS | 任务、资源、调度和生产协同 | 提供上位状态、许可和资源信息，并可使用 PCN 判定或履历结果 |
| AI / 数据分析 | 履历分析、模式提取、改善支持 | 使用 PCN Trace 进行后续分析 |
| TPCA / PCN | Target State Entry 上的结构化判定、控制仲裁、多路径控制和履历 | 将多源相关状态按同一个状态迁移入口组织为完整工程关系 |

这样，既有设备控制、安全控制、任务管理、调度、诊断和分析机制可以继续承担原有职责，PCN 则负责把与某个 Target State Entry 直接相关的状态连接到同一判定和控制上下文中。

---

## 总结

工业自动化已经有状态机、SFC、Interlock、安全控制、报警管理、故障诊断、MES / WCS、FMEA、STPA、RCA 和 Process Mining 等成熟技术。

TPCA / PCN 不替代这些技术，也不要求改变它们原有的工程职责。

它把这些系统提供的状态、许可、诊断结果、任务信息和资源信息，对应到一个明确的 Target State Entry，并形成：

```text
相关状态
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

这样，一次 Target State Entry 可以作为统一的设计、判定、控制和记录对象进行管理。

既有技术继续负责设备控制、安全、任务、调度、诊断和分析；PCN 负责把与本次状态迁移直接相关的状态组织到同一个前置判定和控制结构中。

---

## 参考文献与外部资料

本文以下列资料作为既有技术定位的代表性参考。

1. **MIT Partnership for Systems Approaches to Safety and Security — Books and Handbooks**  
   *STPA Handbook* 及 STPA / CAST 相关公开资料。  
   https://psas.scripts.mit.edu/home/books-and-handbooks/

2. **Wil van der Aalst — *Process Mining: Data Science in Action*, 2nd ed., Springer, 2016**  
   Process Mining 的代表性体系资料。  
   DOI: 10.1007/978-3-662-49851-4  
   https://link.springer.com/book/10.1007/978-3-662-49851-4

3. **PLCopen — IEC 61131-3**  
   IEC 61131-3 的 PLC 编程语言体系及 SFC 相关公开资料。  
   https://www.plcopen.org/standards/logic/iec-61131-3/

4. **ISO 13849-1:2023 — Safety of machinery — Safety-related parts of control systems**  
   机械安全相关控制系统设计原则的 ISO 官方页面。  
   https://www.iso.org/standard/73481.html

5. **ISA — ISA-95 Series of Standards: Enterprise-Control System Integration**  
   ISA-95 / IEC 62264 关于企业系统与制造控制系统集成边界的官方资料。  
   https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard

---

## 文档信息

题目：TPCA / PCN 与既有工业自动化技术和工程方法的关系  
文档类型：技术札记  
版本：Public Note Version 1.3  
首次发布日期：2026-07-04  
最后更新：2026-09-09  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/tpca-existing-theories/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
