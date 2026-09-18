---
title: "TPCA / PCN 与既有工业自动化技术和工程方法的关系"
summary: "从状态与顺序控制、许可与安全约束、生产协同系统以及分析改善方法等层面，说明 TPCA、PCN 与 PCN Trace 在既有工业自动化体系中的工程位置与分工关系。"
description: "说明 TPCA 如何组织状态迁移前置控制设计、PCN 如何在具体目标状态入口承载相应运行过程，以及二者与 PLC、状态机、SFC、Interlock、安全控制、MES / WCS、Process Mining、RCA、FMEA、STPA 和 AI 分析等既有技术的工程关系。"
date: 2026-08-18
lastmod: 2026-09-18
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.2"
citation_title: "TPCA / PCN 与既有工业自动化技术和工程方法的关系"
citation_url: "https://zennns.com/zh/notes/tpca-existing-theories/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

# TPCA / PCN 与既有工业自动化技术和工程方法的关系

工业自动化系统已经形成了大量成熟技术。

PLC 能够执行设备控制和顺序逻辑，IEC 61131-3 对可编程控制器编程语言以及 SFC 等结构元素给出了标准化定义；状态机及其扩展形式长期用于描述复杂离散事件系统中的状态与迁移关系。[1][2] Interlock、Handshake 和安全控制负责不同层面的许可与约束，其中功能安全系统具有独立且明确的安全职责。[3] MES / WCS 管理任务、资源与协同过程，报警管理、RCA、FMEA、STPA、Process Mining、统计分析和 AI 又从不同角度支持风险分析、问题分析和持续改善。[4][5][6][7][8]

在这样的既有技术体系中，TPCA、PCN 和 PCN Trace 分别位于哪里？

TPCA 以明确的目标状态入口（Target State Entry）为工程对象，用于组织一次状态迁移所涉及的状态、判定和控制关系。

PCN（Pre-Control Node）是这一设计在具体 Target State Entry 上的工程承载节点，在运行过程中执行相应的前置判定与控制，并取得执行结果、形成 PCN Trace。

PCN Trace 则将一次状态迁移相关的判定依据、判定结果、控制选择和执行结果保持在同一个状态迁移语义链中，形成可追溯、可进一步分析的状态迁移履历。

TPCA / PCN 与既有 PLC、状态机、SFC、Interlock、安全控制、MES / WCS 以及后续分析方法形成工程分工，并通过现有系统提供的状态、许可和执行能力完成实际工程部署。

---

## 1. 状态与顺序控制：PLC、状态机与 SFC

PLC 程序、状态机和 SFC 已经能够表达设备状态、动作顺序、状态转换和具体控制逻辑，并承担自动化系统中的实际执行控制。IEC 61131-3 将 SFC 定义为用于组织程序和功能块内部结构的顺序功能图元素；Statecharts 等状态机扩展则进一步处理层级、并发和通信等复杂状态表达问题。[1][2]

这些技术说明，状态表达与状态迁移本身已经具有成熟的工程基础。TPCA 所增加的关注点，是把需要进行前置控制设计的具体 Target State Entry 显式化：

```text
Current State
      ↓
Target State Entry
      ↓
Target State
```

围绕这一入口，工程师可以整理本次状态迁移涉及的条件、许可、执行链接续关系、状态有效性以及后续可选择的控制路径。

因此，状态机和 SFC 可以继续承担状态表达、顺序控制和具体执行；TPCA 则从状态迁移设计角度，将需要重点管理的 Target State Entry 作为明确的工程对象。

当这一设计进入实际运行时，可以由相应 PCN 承担该入口的状态取得、前置判定、控制结果组织和履历形成。

这种分工使既有控制体系继续执行实际状态迁移，同时使“这一次状态迁移应该如何设计，以及为什么当前能够进入或不能进入”成为可以显式组织的工程问题。

---

## 2. 许可与安全约束：Interlock、Handshake 与安全控制

工业自动化系统中的许可与约束已经存在于多种成熟机制中。

安全回路、安全 PLC、Interlock、设备间 Handshake、区域许可、资源占用许可和上位系统许可，都可能参与一次状态迁移。IEC 61508 对电气、电子及可编程电子安全相关系统执行安全功能时需要考虑的基本要求进行了系统规定，为功能安全责任边界提供了成熟的工程基础。[3]

这些既有机制继续保持各自原有职责，并可以成为与具体 Target State Entry 有关的状态来源。

例如：

```text
安全许可
区域许可
设备间许可
资源占用许可
上位系统许可
```

在 TPCA 的状态迁移设计中，与系统是否允许进入目标状态有关的状态可以进入 A（Authority）等工程关系进行组织。关键 A 作为独立必要约束处理；关键许可未成立时，不允许进入相应目标状态。

当相应设计由 PCN 承载运行时，PCN 根据实际取得的状态执行相应判断和控制。安全相关的判断与执行仍由既有安全体系承担。

由此，与本次状态迁移有关的许可可以和条件状态、执行链接续状态共同围绕明确的 Target State Entry 形成工程关系，同时保持既有 Interlock、Handshake 和安全控制原有的责任边界。

---

## 3. 生产与协同系统：MES、WCS、机器人与设备控制系统

复杂制造系统中的状态通常分布在不同系统中。

MES 管理生产任务和生产过程，WCS 负责物流任务、调度和资源协调，PLC 与机器人控制器掌握设备和动作状态，AGV / AMR 提供移动主体状态，安全系统提供相关许可，上下游设备则分别维护自身的运行和承接状态。

一次状态迁移可能同时依赖这些不同来源。

```text
MES / WCS
     │
Robot / PLC
     │
AGV / AMR
     │
Safety
     │
Downstream
     ↓
Target State Entry
```

TPCA 在设计阶段围绕明确的 Target State Entry，确定哪些状态与本次迁移有关，以及这些状态如何进入相应的判定和控制关系。

PCN 则作为具体入口上的工程承载节点，在运行过程中取得相关状态，执行 C / A / E 映射、S / D / B 判定以及后续控制，并取得相应执行结果。

MES、WCS、PLC、机器人控制器和安全系统继续承担各自原有的任务管理、调度、设备控制和安全职责。

对于跨越多个设备或多个 PCN 的问题，则按照实际系统层级、共享资源和协同关系进行处理。

这种结构使局部状态迁移能够具有明确的设计对象和运行承载单元，同时保留与上位系统、周边设备和其他节点之间的工程协同。

---

## 4. 风险、故障与原因分析：FMEA、STPA、RCA 与报警管理

FMEA、STPA、RCA 和报警管理分别服务于不同的工程阶段和分析目的。

IEC 60812 将 FMEA / FMECA 定义为系统识别失效模式及其局部和整体影响的方法，并可进一步用于失效处理优先级判断。[4] Leveson 提出的系统理论安全方法则从系统约束、控制关系和复杂社会技术系统角度开展危险与安全分析，为 STPA 提供理论基础。[5]

RCA 关注事件发生以后“发生了什么、如何发生以及为什么发生”，并通过数据收集、因果因素整理、根因识别和改善建议来降低重复发生的可能性。[6] 报警管理则围绕报警的识别、设计、运行、维护和变更等生命周期活动建立管理体系。[7]

这些方法解决的问题不同，也处于不同的工程阶段。PCN 在运行过程中围绕一次明确的状态迁移形成相应的运行事实。

公开层面的基本关系可以表示为：

```text
Target State Entry
→ Pre-Control
→ Control Path
→ Execution Result
→ PCN Trace
```

PCN Trace 将一次状态迁移相关的判定依据、判定结果、控制选择和执行结果保持在同一个状态迁移语义链中。

因此，当现场进一步开展原因分析、履历比较或工程改善时，可以把一次明确的状态迁移及其运行履历作为分析对象之一。

FMEA、STPA、RCA 和报警管理继续按照各自方法和适用阶段发挥作用；PCN Trace 则为运行阶段增加一种围绕状态迁移组织的工程数据。

---

## 5. 运行数据分析：Process Mining、统计分析与 AI

工业系统已经能够产生大量日志、事件、报警和生产履历。Process Mining、统计分析和 AI 可以利用这些数据识别流程特征、异常模式和改善机会。

Process Mining 的基本对象是事件数据。相关研究强调，事件需要具有时间信息，并与活动、资源及相应流程实例建立关联；在此基础上可以进行流程发现、一致性检查以及其他流程分析。[8] 因此，分析能力不仅取决于算法，也取决于数据在进入分析以前如何被组织。

在进入具体分析方法以前，TPCA 首先关注：

> **需要观察哪一次状态迁移，以及应当围绕这次迁移组织什么工程事实？**

当 Target State Entry 被明确，并由相应 PCN 承载实际运行以后，可以持续形成与具体状态迁移对应的 PCN Trace。

由此形成：

```text
Target State Entry
        ↓
PCN
        ↓
PCN Trace
        ↓
统计 / Process Mining / AI / 工程分析
        ↓
问题发现与工程改善
```

PCN Trace 可以直接支持围绕状态迁移的统计、比较和 AI 辅助分析；当按照具体流程分析方法所要求的事件结构、关联标识和时间关系进一步组织后，也可以作为 Process Mining 等流程分析的数据来源。

Process Mining 可以继续从事件日志和流程数据中发现实际流程关系，统计方法可以比较频度、时间和变化趋势，AI 可以辅助进行模式提取、履历比较、改善候选整理和工程报告生成。

在这一关系中，分析方法可以根据问题和数据特点选择。

> **先决定看什么，再决定怎么看，最后才决定使用什么方法进行分析。**

TPCA 明确需要被工程化描述的状态迁移，PCN 在实际运行中形成相应的状态迁移履历，后续分析方法再从这些运行事实中提取进一步的工程价值。

相关讨论可继续阅读：

[状态迁移如何形成可分析的工程数据？——从 Target State Entry、CAE-SDB 到 PCN Trace](/zh/notes/how-state-transition-becomes-engineering-data/)

---

## 6. TPCA、PCN 与既有技术的整体工程关系

综合来看，可以从状态迁移设计、运行与执行、分析与改善三个层面理解 TPCA、PCN 与既有工业自动化技术之间的关系。

```text
状态迁移设计
────────────────────────

工程对象 / 状态迁移需求
        ↓
TPCA
        ↓
Target State Entry
        ↓
相关状态
→ CAE-SDB
→ Arbitration
→ Multipath Control


运行与执行
────────────────────────

PLC / Robot / MES / WCS / Safety
        ↕
状态、许可与执行能力
        ↕
PCN
        ↓
前置判定与控制结果
        ↓
Execution Result
        ↓
PCN Trace


分析与改善
────────────────────────

PCN Trace
        ↓
规则 / 统计 / RCA / Process Mining / AI
        ↓
分析、比较与改善候选
        ↓
工程确认与修改
        ↓
新的运行结果与 Trace
```

上图表示的是工程职责和信息关系，并不代表固定的软件层级、物理部署位置或严格的顺序处理结构。

TPCA 属于状态迁移前置控制的架构与设计方法层；PCN 是部署在具体 Target State Entry 上的工程实现单元。实际系统中，PCN 可以根据对象和系统架构与 PLC、MES / WCS、机器人、安全系统及其他控制对象进行工程连接。

PCN Trace 则来自实际运行过程，并为后续分析、比较和改善提供围绕状态迁移组织的工程事实。

---

## 总结

工业自动化系统已经拥有成熟的状态控制、顺序控制、安全联锁、任务调度、设备控制和分析方法。[1][3][4][7][8]

TPCA 在其中明确 Target State Entry 这一工程对象，并围绕具体状态迁移组织相关状态、判定和控制设计。

PCN 将相应设计承载到具体 Target State Entry 的运行过程中，取得实际状态、执行前置判定与控制，并通过执行结果形成 PCN Trace。

因此，整体工程关系可以概括为：

> **既有系统提供状态、许可和执行能力；TPCA 围绕明确的 Target State Entry 组织状态迁移的判定与控制设计；PCN 将相应设计承载到具体状态迁移入口的运行过程中，并通过 PCN Trace 形成可追溯、可进一步分析的状态迁移履历。**

在此基础上，规则、统计、RCA、Process Mining、AI 及其他工程方法可以继续利用这些运行事实开展问题分析、比较和改善。

---

## 参考文献

以下文献用于说明本文涉及的主要既有技术及其原有工程职责。引用目的在于为状态控制、功能安全、风险分析、原因分析、报警管理和流程分析等技术建立外部工程锚点，并不表示 TPCA / PCN 来源于这些方法，也不表示这些方法之间具有统一的层级关系。

[1] IEC. *IEC 61131-3:2025, Programmable controllers – Part 3: Programming languages*. International Electrotechnical Commission, 2025.  
用于说明可编程控制器编程语言以及 SFC 的标准化工程基础。IEC 61131-3:2025 定义 ST、LD、FBD，并将 SFC 作为组织程序和功能块内部结构的顺序功能图元素。  
https://webstore.iec.ch/en/publication/68533

[2] Harel, D. “Statecharts: A Visual Formalism for Complex Systems.” *Science of Computer Programming*, Vol. 8, No. 3, 1987, pp. 231–274. DOI: 10.1016/0167-6423(87)90035-9.  
用于说明状态机及其扩展在复杂离散事件系统中的状态表达基础。该文通过层级、并发和通信扩展传统状态图，是复杂状态迁移表达的重要经典文献。  
https://doi.org/10.1016/0167-6423(87)90035-9

[3] IEC. *IEC 61508-1:2010, Functional safety of electrical/electronic/programmable electronic safety-related systems – Part 1: General requirements*. International Electrotechnical Commission, 2010.  
用于说明功能安全系统具有独立的安全功能、生命周期和工程责任要求。本文据此保持安全控制与 TPCA / PCN 前置判定之间的职责边界。  
https://webstore.iec.ch/en/publication/5515

[4] IEC. *IEC 60812:2018, Failure modes and effects analysis (FMEA and FMECA)*. International Electrotechnical Commission, 2018.  
用于说明 FMEA / FMECA 的工程定位：系统识别失效模式、影响及必要处理，并可根据后果严重度等因素支持处理优先级判断。  
https://webstore.iec.ch/en/publication/26359

[5] Leveson, N. G. *Engineering a Safer World: Systems Thinking Applied to Safety*. MIT Press, 2012.  
用于说明基于系统理论的安全分析基础。该书提出 STAMP，并以系统控制、约束和复杂交互关系为核心讨论危险分析、安全设计和运行安全，是 STPA 方法的重要理论基础。  
https://mitpress.mit.edu/9780262016629/engineering-a-safer-world/

[6] Rooney, J. J., and Vanden Heuvel, L. N. “Root Cause Analysis for Beginners.” *Quality Progress*, Vol. 37, No. 7, 2004, pp. 45–53.  
用于说明 RCA 的基本工程目的：通过识别事件发生的事实、过程和根本原因，形成能够降低重复发生可能性的改善措施。  
https://asq.org/-/media/ASQ-Supplemental-Media-Import/E/9/0/5/7/ar_19550.pdf

[7] ISA. *ANSI/ISA-18.2-2016, Management of Alarm Systems for the Process Industries*. International Society of Automation, 2016.  
用于说明报警管理的工程边界。ISA-18.2 围绕报警的识别、合理化、设计、实施、运行、维护和变更等活动建立生命周期管理框架。  
https://www.isa.org/standards-and-publications/isa-standards/isa-18-series-of-standards

[8] van der Aalst, W. M. P. *Process Mining: Data Science in Action*. 2nd ed., Springer, 2016. DOI: 10.1007/978-3-662-49851-4.  
用于说明 Process Mining 以事件数据为基础，通过流程发现、一致性检查及其他分析方法研究实际流程行为。该文献也说明了事件数据的结构与质量对流程分析的重要性。  
https://doi.org/10.1007/978-3-662-49851-4

---

## 进一步阅读

- [Concepts｜核心概念](/zh/concepts/)
- [为什么是 CAE-SDB？——目标状态入口前的双轴结构化分析方法](/zh/notes/why-cae-sdb/)
- [状态迁移如何形成可分析的工程数据？——从 Target State Entry、CAE-SDB 到 PCN Trace](/zh/notes/how-state-transition-becomes-engineering-data/)
- [为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)
- [应用案例](/zh/cases/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

---

## 文档信息

题目：TPCA / PCN 与既有工业自动化技术和工程方法的关系  
文档类型：技术札记  
版本：Public Note Version 1.2  
首次发布日期：2026-08-18  
最后更新：2026-09-18  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/tpca-existing-theories/
