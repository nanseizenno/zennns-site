---
title: "TPCA / PCN 与既有工业自动化技术和工程方法的关系"
summary: "从状态迁移入口判定、许可与安全约束、生产协同系统、运行履历及后续分析等层面，说明 TPCA、PCN 与 PCN Trace 在既有工业自动化体系中的工程位置与分工关系。"
description: "说明 TPCA 如何围绕 Target State Entry 组织状态迁移前置控制设计，CAE-SDB 相比传统迁移条件如何保留更多工程结构，以及 PCN、PCN Trace 与 PLC、状态机、SFC、Interlock、安全控制、MES / WCS、RCA、FMEA、STPA、Process Mining 和 AI 分析等既有技术的工程关系。"
date: 2026-08-18
lastmod: 2026-09-25
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.3"
citation_title: "TPCA / PCN 与既有工业自动化技术和工程方法的关系"
citation_url: "https://zennns.com/zh/notes/tpca-existing-theories/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

# TPCA / PCN 与既有工业自动化技术和工程方法的关系

工业自动化系统已经形成了成熟的状态控制、顺序控制、许可控制、安全控制、生产协同和运行分析技术。

PLC 执行设备控制和顺序逻辑，IEC 61131-3 对可编程控制器编程语言以及 SFC 等结构元素给出了标准化定义；状态机及其扩展形式长期用于描述复杂离散事件系统中的状态与迁移关系。[1][2] Interlock、Handshake、Permissive 和安全控制承担不同层面的迁移约束和许可功能，其中功能安全系统具有独立且明确的安全职责。[3]

MES / WCS、机器人控制器、AGV / AMR 和设备控制系统分别掌握任务、资源、设备、移动主体和执行状态。FMEA、STPA、RCA、报警管理、Process Mining、统计分析和 AI 则用于风险分析、问题分析、运行比较和持续改善。[4][5][6][7][8]

TPCA / PCN 位于这一既有工程体系中的状态迁移前置控制位置。

TPCA 以明确的目标状态入口（Target State Entry）为工程对象，组织一次状态迁移涉及的相关状态、判定关系和控制路径。

PCN（Pre-Control Node）是对应具体 Target State Entry 的工程承载节点，在运行过程中取得相关状态，执行前置判定与控制，并取得执行结果、形成 PCN Trace。

PCN Trace 将一次状态迁移的输入状态、判定依据、判定结果、控制选择和执行结果保持在同一状态迁移语义中，形成可追溯、可比较的运行履历。

TPCA / PCN 与既有 PLC、状态机、SFC、Interlock、安全控制、MES / WCS 等共同构成实际工程系统；后续分析方法可以继续利用运行过程中形成的 PCN Trace。

---

## 1. 状态迁移入口判定：状态机、SFC 与 CAE-SDB

PLC 程序、状态机和 SFC 已经能够表达设备状态、动作顺序、状态转换和具体控制逻辑，并承担自动化系统中的实际执行控制。

IEC 61131-3 将 SFC 作为组织程序和功能块内部结构的顺序功能图元素；Statecharts 等状态机扩展进一步支持层级、并发和通信等复杂状态表达。[1][2]

在这些控制结构中，一次状态迁移通常由当前状态、迁移条件以及目标状态构成。工程实现中，一个 Transition Condition 可以由多个设备状态、完成条件、许可、联锁和逻辑表达式共同决定，最终形成允许或禁止迁移的结果。

TPCA 进一步把状态迁移入口本身作为明确的工程对象。

围绕一个 Target State Entry，首先确定本次状态迁移需要观察哪些相关状态，再根据这些状态在当前入口中的工程作用进行 C / A / E Mapping。

- **C = Condition**  
  进入目标状态前需要成立的现场条件、对象条件、识别条件、数据条件、任务条件、参数条件等。

- **A = Authority**  
  系统在目标状态入口处是否允许本次迁移，包括安全许可、上位许可、区域许可、人工确认、权限、资源锁和对方设备许可等。

- **E = Execution Chain**  
  进入目标状态以后，整个执行链是否能够继续接续，包括本体设备、末端执行机构、下游承接、替代路径、回退路径、异常排出以及结果回写等。

C / A / E 描述的是状态相对于本次 Target State Entry 所承担的**迁移功能角色**。

同一个现场状态在不同 Target State Entry 中，可以根据其与当前状态迁移的实际关系承担不同角色。

在此基础上，再从 S / D / B 三类判定性质对相关状态进行评价：

- **S = Structure**  
  判断所需信号、接口、映射关系、许可来源、路径、角色及执行链边界是否已经定义、接入并可观测。

- **D = Dynamics**  
  判断当前状态在时序上是否有效，包括超时、未刷新、延迟、不同步、许可撤销、状态切换等动态问题。

- **B = Boundary**  
  判断置信度、容量、时间窗口、次数、偏差等是否处于预先规定的控制边界内。

CAE-SDB 由两个维度组成：

| 维度 | 内容 |
|---|---|
| 状态迁移功能角色 | C / A / E |
| 状态判定性质 | S / D / B |

传统 Transition Condition、Guard、Interlock 或 Permissive 继续决定具体状态迁移是否成立。

TPCA / CAE-SDB 增加的是入口前的结构化表达：明确准备进入什么目标状态、本次需要观察哪些状态、这些状态承担什么工程角色、需要从什么性质进行判定，以及当前应进入哪一条合法控制路径。

TPCA 关注的是将原本可能被压缩在单一 Transition Condition、Ready、Interlock 或布尔结果中的状态迁移关系显式组织出来。

PCN 在运行过程中承载这一结构，取得实际状态、完成判定与控制，并形成对应运行履历。

---

## 2. 许可与安全约束：Interlock、Handshake 与安全控制

工业自动化系统中的许可与约束已经存在于多种成熟机制中。

安全回路、安全 PLC、Interlock、设备间 Handshake、区域许可、资源占用许可和上位系统许可，都可能参与一次状态迁移。IEC 61508 对电气、电子及可编程电子安全相关系统执行安全功能时需要考虑的基本要求进行了系统规定，为功能安全责任边界提供了成熟的工程基础。[3]

这些既有机制继续承担各自原有职责，并作为具体 Target State Entry 的状态来源。

常见许可包括：

- 安全许可；
- 区域许可；
- 设备间许可；
- 资源占用许可；
- 上位系统许可；
- 人工确认。

在 TPCA 中，A（Authority）用于组织本次 Target State Entry 的许可关系。

关键安全许可、上位许可、区域许可、资源锁、人工确认等可以构成独立必要约束。关键 A 未成立时，即使 C 和 E 均成立，本次状态迁移仍然不能被允许。

因此，C、A、E 分别回答三个不同问题：

| 变量域 | 基本问题 |
|---|---|
| C | 条件是否具备 |
| A | 是否被允许进入 |
| E | 进入以后能否继续接续 |

安全相关判断与安全功能仍由既有安全 PLC、安全继电器、安全回路及相应安全体系负责。

PCN 取得这些系统提供的许可状态，在 Target State Entry 前尊重其判定结果，并将其纳入本次状态迁移的前置控制。

---

## 3. 生产与协同系统：MES、WCS、机器人与设备控制系统

复杂制造系统中的状态通常分布在多个系统中。

MES 管理生产任务和生产过程，WCS 负责物流任务、调度和资源协调，PLC 与机器人控制器掌握设备和动作状态，AGV / AMR 提供移动主体状态，安全系统提供相关许可，上下游设备维护自身的运行和承接状态。

一次状态迁移可能同时依赖这些不同来源。

TPCA 在设计阶段首先确定本次准备进入什么目标状态，以及判断这个入口需要观察哪些工程状态。

随后，来自不同系统的状态按照本次 Target State Entry 中的实际作用进入 C / A / E Mapping 和 S / D / B Evaluation。

TPCA 不需要重新定义 MES、WCS、PLC、机器人控制器和安全系统已有的数据对象。

它增加的是一个以状态迁移为中心的数据组织视角：原有系统继续提供各自数据，PCN 只抽取与当前 Target State Entry 直接相关的状态，并在当前入口下完成映射、判定和控制。

PCN 作为具体入口上的工程承载节点，在运行过程中取得这些相关状态，执行前置判定和控制，并取得 Execution Result。

MES、WCS、PLC、机器人控制器、安全系统和其他既有系统继续承担各自的任务管理、调度、设备控制和安全职责。

这样，分布在不同系统中的状态可以围绕同一次状态迁移形成统一的工程语义。

---

## 4. 风险、故障与原因分析：FMEA、STPA、RCA 与报警管理

FMEA、STPA、RCA 和报警管理分别服务于不同的工程阶段和分析目的。

IEC 60812 将 FMEA / FMECA 定义为识别失效模式及其局部和整体影响的方法，并可进一步用于失效处理优先级判断。[4]

Leveson 提出的系统理论安全方法从系统约束、控制关系和复杂社会技术系统角度开展危险与安全分析，为 STPA 提供理论基础。[5]

RCA 通过事件事实、因果因素和根因分析寻找能够降低问题重复发生可能性的改善措施。[6]

报警管理围绕报警的识别、设计、运行、维护和变更等生命周期活动建立管理体系。[7]

这些方法主要服务于风险识别、事故分析、原因分析和改善活动。

PCN 在运行过程中产生的是一次明确状态迁移的实际运行事实，包括 Target State Entry、相关状态、CAE-SDB 判定、控制结果、执行结果和 PCN Trace。

PCN Trace 将一次状态迁移相关的输入、判定、控制和执行结果保持在同一个工程上下文中。

后续开展 RCA、FMEA、STPA、报警复盘或其他工程改善时，可以把这些已经结构化的状态迁移履历作为运行事实来源之一。

---

## 5. 运行履历与后续分析

TPCA / PCN 在执行状态迁移前置控制的同时，会持续形成具有工程语义的 PCN Trace。

一个 PCN Trace 围绕同一次 Target State Entry 保存：

- Current State；
- Target State；
- Target State Entry；
- 相关状态；
- C / A / E Mapping；
- S / D / B Evaluation；
- Arbitration；
- Control Result；
- Execution Result；
- Time Information。

这些信息来自同一个状态迁移过程，因此具有明确的上下文关系。

后续可以直接分析：

- 某类 Target State Entry 的进入成功率；
- 某类 C / A / E 问题的发生频度；
- 不同设备之间相同 PCN 的差异；
- 不同时间区间的判定结果变化；
- 等待持续时间；
- 恢复时间；
- 重复出现的阻断模式；
- 控制路径使用频度。

当多个 PCN 按实际工程依赖进一步连接时，还可以形成跨节点的状态迁移履历。

上游 PCN 的 Execution Result 如果形成新的工程状态事实，并成为下游 PCN 的相关输入，下游 PCN 会按照自己的 Target State Entry 重新执行 C / A / E Mapping 和 S / D / B Evaluation。

在这个基础上，可以继续分析：

- 阻断传播路径；
- 恢复传播路径；
- 受影响 PCN；
- 传播时间；
- 重复传播模式；
- 上下游状态关联。

这些关系在 PCN 运行过程中已经被结构化保存，因此很多基础分析可以直接通过查询、统计、比较、时间分析和关系遍历完成。

Process Mining、统计分析、图分析、RCA 和 AI 可以根据具体问题继续作为后续分析工具使用。

其中，Process Mining 适合从大量事件履历中发现流程变体、分析流程行为和一致性；统计方法适合比较频度、时间和变化趋势；AI 可以辅助进行履历归纳、模式提取和改善候选整理。[8]

这些分析方法位于 PCN Trace 之后。

工程顺序是：先明确需要观察的状态迁移，通过 TPCA / PCN 形成结构化运行事实，再根据实际问题选择分析方法。

因此，TPCA / PCN 的数据价值首先来自状态迁移结构本身。

分析工具负责利用这些已经具有明确语义和关联关系的数据继续提取工程价值。

相关讨论可继续阅读：

[状态迁移如何形成可分析的工程数据？——从 Target State Entry、CAE-SDB 到 PCN Trace](/zh/notes/how-state-transition-becomes-engineering-data/)

---

## 6. TPCA、PCN 与既有技术的整体工程关系

TPCA / PCN 与既有工业自动化技术之间，可以按照状态迁移设计、运行执行、运行履历和后续分析四个层面理解。

| 层面 | 主要对象 | 主要作用 |
|---|---|---|
| 状态迁移设计 | Target State Entry、相关状态、C / A / E、S / D / B、Arbitration、Multipath Control | 明确一次状态迁移入口需要观察和判定什么 |
| 运行与执行 | PLC、Robot、MES、WCS、Safety、PCN | 由既有系统提供状态、许可和执行能力，PCN 执行入口前判定和控制 |
| 运行履历 | Execution Result、PCN Trace、PCN Network Trace | 保存单节点及跨节点状态迁移事实 |
| 分析与改善 | 查询、比较、统计、图分析、RCA、Process Mining、AI | 基于结构化运行事实开展问题分析和改善 |

这张表表示工程职责与信息关系，不表示固定的软件层级、物理部署位置或严格的软件处理顺序。

状态机、SFC、Transition Condition、Interlock 和 Permissive 等既有机制继续承担实际状态表达、迁移控制和许可控制。

TPCA / CAE-SDB 关注这些迁移条件在一个明确 Target State Entry 中如何被结构化组织。

PCN 将相应设计承载到实际运行过程。

PCN Trace 则把运行过程中产生的状态迁移判定、控制与执行结果保存为具有明确工程语义的履历。

后续分析工具再根据具体问题使用这些运行事实。

---

## 总结

工业自动化系统已经拥有成熟的状态控制、顺序控制、联锁、许可、安全控制、任务调度、设备控制以及各种分析方法。[1][3][4][7][8]

TPCA / PCN 关注其中一个具体工程对象：

> **系统准备进入一个明确目标状态时，这一次状态迁移需要观察哪些状态，这些状态在迁移中承担什么功能角色，又需要从哪些性质进行判定。**

传统状态机、SFC、Interlock、Permissive 和其他控制机制继续承担实际状态迁移与设备控制。

TPCA 将一次 Target State Entry 的相关状态、判定和控制关系显式组织起来；PCN 将这一结构承载到实际运行；PCN Trace 将运行过程中形成的状态迁移事实持续保存。

这些运行数据带有明确的状态迁移语义和关联关系，可以继续用于比较、统计、追溯和工程分析。

TPCA / PCN 的工程价值首先来自状态迁移结构本身；后续采用何种分析工具，根据具体问题选择。

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
用于说明 Process Mining 以事件数据为基础，通过流程发现、一致性检查及其他分析方法研究实际流程行为。  
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
版本：Public Note Version 1.3  
首次发布日期：2026-08-18  
最后更新：2026-09-25  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/tpca-existing-theories/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
