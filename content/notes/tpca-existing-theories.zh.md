---
title: "TPCA / PCN 与既有工业自动化方法和控制机制的关系"
summary: "说明 TPCA / PCN 与 FMEA、STPA、RCA、Process Mining、状态机、SFC、Interlock、安全控制、报警管理、MES / WCS、AI 分析及形式化验证之间的边界关系。"
description: "说明 TPCA / PCN 并不替代既有工业自动化方法和控制机制，而是以明确的目标状态入口为对象，将分散存在的状态、条件、许可、执行链、判定结果和控制输出组织为可判定、可控制、可记录和可追溯的前置控制节点。"
date: 2026-07-04
lastmod: 2026-08-20
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.2"
citation_url: "https://zennns.com/zh/notes/tpca-existing-theories/"
draft: false
weight: 1
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## TPCA / PCN 与既有工业自动化方法和控制机制的关系

基础概念可参见：

- [核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)
- [为什么状态迁移条件必须显式化？](/zh/notes/explicit-state-transition-conditions/)
- [TPCA / PCN 建立在什么工程基础上？——五个基础工程共识](/zh/notes/engineering-foundations-of-tpca-pcn/)
- [TPCA / PCN 面对已有技术分歧，它站在哪里？——三个典型工程争议](/zh/notes/engineering-positions-of-tpca-pcn/)

---

## 1. 本文讨论什么

工业自动化并不缺少状态、状态迁移、Ready、Interlock、安全许可、报警、超时、资源约束和异常处理。

状态机和 SFC 可以定义状态、步骤及迁移条件。

PLC、机器人控制器和设备程序本身包含大量 Interlock、Handshake、Ready 和顺序控制逻辑。

安全 PLC、安全继电器和安全回路负责危险动作限制和安全许可。

MES、WCS 和群控系统也会进行任务、资源、路径、站点、权限和执行条件判断。

因此，TPCA / PCN 的成立并不依赖“既有工业自动化系统没有状态迁移条件判断”这一前提。

TPCA / PCN 关注的是：

> **对于一个明确的目标状态入口，原本分散在不同设备、系统和控制机制中的状态判断，能否被组织成一个统一的前置判定、控制和履历对象。**

例如，一个机器人进入抓取阶段之前，现场可能已经存在：

- 视觉识别结果；
- Robot Ready；
- 安全区域许可；
- PLC Interlock；
- 上位系统许可；
- 下游可接收状态；
- 返回路径状态。

这些状态本身并不新。

PCN 进一步围绕这一次状态迁移明确：

- 当前状态是什么；
- 目标状态是什么；
- 哪些状态属于条件；
- 哪些状态属于许可；
- 进入以后执行链能否继续接续；
- 当前状态是否仍然有效；
- 多个判定结果同时存在时应进入哪一条控制路径；
- 本次判定和执行结果如何形成履历。

因此，TPCA / PCN 的重点是把一次明确的目标状态迁移判定本身变成工程对象。

---

## 2. 与 FMEA、STPA、RCA、Process Mining 的关系

这些方法都具有把复杂工程问题结构化的特点，但处理对象和使用阶段不同。FMEA、STPA、RCA 与 Process Mining 的基本定位可分别参见 ASQ 的 FMEA 公开说明、MIT 的 STPA Handbook 页面、ASQ 的 RCA 说明以及 van der Aalst 的 Process Mining 专著。[1][2][3][4]

| 方法 | 主要处理对象 |
|---|---|
| FMEA | 潜在失效模式、影响、原因及控制措施 |
| STPA / STAMP | 安全控制结构、控制约束和危险场景 |
| RCA | 已经发生的问题及其原因链 |
| Process Mining | 基于事件日志还原的实际流程、偏差、等待和瓶颈 |
| TPCA / PCN | 明确目标状态入口上的运行时前置判定与控制 |

FMEA 主要回答：

> 什么可能失效？

STPA / STAMP 主要关注：

> 哪些控制关系可能产生危险状态？

RCA 主要回答：

> 已经发生的问题为什么发生？

Process Mining 主要回答：

> 实际流程是怎么运行的，哪里出现等待、返工或偏差？

TPCA / PCN 关注的是：

> **系统现在准备进入这个目标状态，当前是否具备进入条件；如果不能进入，应进入哪一条控制路径。**

这些方法可以作用于同一个工程系统，但处理的是不同阶段的问题。

例如，FMEA 可以识别某个许可信号失效的风险。

STPA 可以分析某项安全许可缺失可能形成的不安全控制关系。

PCN 则在实际运行时，把相关许可作为本次目标状态进入前的状态变量参与判定。

---

## 3. 与状态机、SFC、Interlock、安全控制和报警管理的关系

### 3.1 状态机、SFC 与 PCN

状态机和 SFC 本来就可以定义状态、迁移及顺序组织。状态图 / Statecharts 的经典形式化工作可参见 Harel；SFC 的工业标准化背景可参见 IEC 61131-3，公开说明可参见 PLCopen。[5][6]

状态机和 SFC 本来就可以定义：

- 状态；
- 步骤；
- 动作；
- 迁移；
- 迁移条件；
- 状态之间的执行关系。

TPCA / PCN 不替代状态机，也不重新实现一套顺序控制。

例如，一个既有迁移条件可以写成：

```text
Vision_OK
AND Robot_Ready
AND Safety_OK
AND Downstream_Ready
```

这个逻辑本身可以正常控制设备。

PCN 进一步围绕本次目标状态进入，对这些状态进行结构化组织：

```text
当前状态
→ 目标状态
→ 多源状态信号
→ C/A/E 状态映射
→ S/D/B 判定
→ CAE-SDB 判定结果
→ 控制仲裁
→ 多路径控制
→ PCN Trace
```

因此，更准确的关系是：

> **状态机和 SFC 负责状态及迁移逻辑；PCN 以明确的目标状态入口为对象，把决定本次迁移的多源状态进一步组织、判定、仲裁并记录。**

PCN 可以嵌入既有状态机、SFC 或 PLC 控制程序中，也可以作为其周边判定模块存在。

---

### 3.2 Interlock 与 PCN

Interlock 是工业控制中的成熟机制。

它可以组合多个状态，对某一动作或阶段进入进行限制。

TPCA / PCN 不要求把现有 Interlock 全部改写。

对于同一个 Interlock NG，PCN 进一步判断它在当前目标状态入口中的工程含义，例如：

- 条件不成立；
- 关键许可不成立；
- 下游执行链无法接续；
- 状态已经超时；
- 当前状态进入控制边界。

因此，PCN 关注的不只是：

```text
Interlock = FALSE
```

还包括：

> **为什么当前状态迁移不能成立，以及系统下一步应进入什么控制路径。**

---

### 3.3 安全控制与 PCN

安全 PLC、安全继电器、安全门、光栅、急停和安全扫描器负责实现安全功能。机械安全相关控制系统的设计原则可参见 ISO 13849-1。[7]

PCN 可以读取安全系统提供的许可状态，并把关键安全许可作为目标状态进入前的必要约束。

例如：

```text
条件成立
许可不成立
执行链可接续
```

关键许可不成立时，不允许进入目标状态。

因此二者的工程分工是：

> **安全系统负责安全功能本身，PCN 把安全许可作为目标状态进入前的关键许可状态参与完整判定。**

---

### 3.4 报警管理、故障诊断与 PCN

报警管理本身已有成熟标准体系。IEC 62682 与 ISA-18.2 共同构成过程工业报警管理的重要标准体系，公开说明可参见 ISA 的 ISA-18.2 资料。[8]

报警管理可以处理：

- 报警定义；
- 报警优先级；
- 报警响应；
- 报警履历；
- 报警生命周期。

故障诊断进一步分析：

- 故障模式；
- 故障原因；
- 故障传播；
- 故障位置。

PCN 关注的是：

> **这些报警、故障或异常状态，对当前目标状态进入有什么实际影响。**

例如，同样是通信异常：

在一个状态迁移入口上，可能意味着识别结果已经无法确认有效；

在另一个入口上，可能意味着上位许可无法确认；

在另一个入口上，又可能意味着结果回写链路无法继续。

因此：

> **报警管理负责管理异常，故障诊断负责分析故障，PCN 负责判断这些状态对当前目标状态进入的影响，并形成对应控制路径。**

---

## 4. 与 MES / WCS、AI 分析和形式化验证的关系

### 4.1 MES / WCS 与 PCN

MES、WCS 和群控系统本身已经包含大量任务、资源、执行和信息交换机制。制造运营与企业控制系统之间的信息模型和集成边界，可参见 ISA-95 / IEC 62264 系列。[9]

MES、WCS 和群控系统本身已经包含大量：

- 任务条件；
- 资源约束；
- 路径状态；
- 站点状态；
- 车辆状态；
- 资源锁；
- 权限和许可；
- 调度规则；
- 可执行性判断。

PCN 不替代这些功能。

它关注的是：

> **某个关键任务、协同状态或执行路径真正进入下一状态之前，能否把分散在多个系统中的相关状态整理成一个明确的状态迁移判定对象。**

例如：

```text
MES 已产生任务
WCS 已存在任务记录
设备在线
车辆在线
没有明显报警
```

但任务仍然没有进入有效执行。

此时还需要继续判断：

- 任务条件是否仍然有效；
- 调度或资源许可是否成立；
- 资源锁是否已经释放；
- 路径是否能够继续；
- 下游是否能够承接；
- 当前状态是否已经过期；
- 执行链是否存在阻塞。

因此：

> **MES / WCS 继续承担任务、资源和调度功能；PCN 可以在关键状态迁移入口增加结构化前置判定、控制和履历。**

---

### 4.2 AI 与数据分析

AI 和数据分析可以用于：

- 履历比较；
- 模式分析；
- 趋势分析；
- 聚类；
- 候选改善方向生成；
- 报告整理。

TPCA / PCN 不依赖 AI 才能成立。

PCN 的运行时判定建立在明确的工程状态、许可、规则和控制边界之上。

PCN Trace 积累以后，AI 可以进一步辅助分析：

- 哪些状态迁移入口长期出现相似问题；
- 哪些判定结果反复出现；
- 哪些控制路径经常触发；
- 哪些工程修改以后，运行结果发生了明显变化。

因此：

> **PCN 负责运行时前置判定和控制，AI 更适合用于 PCN Trace 之后的比较分析和改善支持。**

---

### 4.3 形式化验证和运行时验证

形式化验证、模型检查和运行时验证同样会处理状态、性质和运行事件。模型检查的经典体系可参见 Clarke 等人的《Model Checking》，运行时验证的基本定位可参见 Leucker 与 Schallhart 的综述。[10][11]

形式化验证、模型检查和运行时验证同样会处理：

- 状态；
- 状态迁移；
- 约束；
- 性质；
- 运行事件。

这些方向与 TPCA / PCN 存在邻接关系。

形式化方法通常关注：

> 系统或模型是否满足预先定义的性质。

PCN 关注：

> 现场这一次具体目标状态迁移现在是否能够发生；如果不能发生，应进入哪一条工程控制路径。

因此：

> **形式化验证主要验证模型或性质，PCN 主要形成明确目标状态入口上的运行时前置判定与控制。**

形式化验证或运行时验证的结果，也可以作为 PCN 的输入状态之一。

---

## 5. TPCA / PCN 真正增加的是什么

如果把工业自动化中的各个元素单独拆开：

- Condition 不是新概念；
- Authority 不是新概念；
- Ready 不是新概念；
- 状态迁移不是新概念；
- Interlock 不是新概念；
- 报警不是新概念；
- 超时不是新概念；
- 等待、重试、回流和降级也不是新概念。

TPCA / PCN 的技术重点不在于发明这些单独元素，而在于：

> **围绕一个明确的目标状态入口，把原本分散的状态输入、许可关系、执行链接续性、判定结果、控制优先关系、控制路径和履历组织成一个完整工程对象。**

其基本工程链为：

```text
当前状态
→ 目标状态
→ PCN
→ 多源状态信号
→ C/A/E 状态映射
→ S/D/B 判定
→ CAE-SDB 判定结果
→ 控制仲裁
→ 多路径控制
→ PCN Trace
```

决定一次状态迁移的状态可能分别存在于：

```text
PLC
机器人
视觉系统
安全系统
MES
WCS
下游设备
资源锁
人工确认
```

PCN 将这些分散状态围绕同一个目标状态入口组织起来。

因此，TPCA / PCN 增加的是：

> **一个可以被独立设计、判定、控制、记录和追溯的状态迁移入口工程对象。**

---

## 6. 与既有自动化体系的工程分工

TPCA / PCN 与既有自动化体系之间可以形成明确分工。

| 既有对象 | 主要职责 | 与 PCN 的关系 |
|---|---|---|
| PLC / 状态机 / SFC | 顺序控制、状态和动作执行 | 提供并执行状态迁移逻辑，PCN 可嵌入其中或与其协同 |
| Interlock / Handshake | 动作限制、设备间条件协调 | 作为 PCN 的输入和既有控制约束 |
| 安全系统 | 安全功能、安全许可、危险动作限制 | 向 PCN 提供关键许可状态 |
| 报警与故障诊断 | 异常管理、故障定位和原因分析 | 异常结果可以进入 PCN 判定 |
| MES / WCS | 任务、资源、调度、生产协同 | 提供上位状态并接收诊断或控制结果 |
| AI / 数据分析 | 履历分析、模式识别、辅助改善 | 基于 PCN Trace 进行后续分析 |
| TPCA / PCN | 状态迁移入口前的结构化判定与多路径控制 | 组织多源状态，形成判定、仲裁、控制和履历 |

这一关系的重点不是技术替代，而是把原本分散在不同工程层级中的状态判断，围绕明确的状态迁移入口重新组织。

---

## 小结

TPCA / PCN 并不是因为工业自动化缺少状态机、Interlock、安全控制、报警或调度系统才存在。

这些机制本身已经成熟。

TPCA / PCN 关注的是：

> **当多个已有机制共同决定一次状态迁移时，如何把这次目标状态进入前的判断本身变成一个明确的工程对象。**

其基本结构为：

```text
当前状态
→ 目标状态
→ PCN
→ C/A/E 状态映射
→ S/D/B 判定
→ CAE-SDB 判定结果
→ 控制仲裁
→ 多路径控制
→ PCN Trace
```

既有系统继续提供状态、条件、许可、安全、调度和执行能力。

TPCA / PCN 则围绕一个明确的状态迁移入口，把这些能力组织成可判定、可控制和可追溯的前置控制结构。

这就是 TPCA / PCN 与既有工业自动化方法和控制机制之间的基本关系。

---


## 参考文献与外部依据

本节参考文献主要用于说明本文所比较的**既有工业自动化方法、标准和理论的原始定位**。

考虑到部分 IEC / ISO 标准正文需要购买或在部分地区访问受限，下面优先提供**可公开访问的官方机构页面、学术出版页面或稳定书目页面**。正式标准号仍在条目中保留，便于进一步检索。

这些资料不是 TPCA / PCN 的理论来源，也不用于直接证明 TPCA / PCN 的专利新颖性、创造性或法律上的权利边界。

1. **ASQ — What is FMEA? Failure Mode & Effects Analysis**  
   公开说明 FMEA 的基本对象、用途和分析方式。正式标准可进一步参见 IEC 60812:2018。  
   https://asq.org/quality-resources/fmea

2. **MIT Partnership for Systems Approaches to Safety and Security — Books and Handbooks**  
   页面提供 *STPA Handbook* 的公开入口，并介绍 STPA / CAST 相关资料。  
   https://psas.scripts.mit.edu/home/books-and-handbooks/

3. **ASQ — What is Root Cause Analysis (RCA)?**  
   用于说明 RCA 作为问题发生后的原因分析方法的基本定位。  
   https://asq.org/quality-resources/root-cause-analysis

4. **Wil van der Aalst — *Process Mining: Data Science in Action*, 2nd ed., Springer, 2016**  
   Process Mining 的代表性系统专著。  
   DOI: 10.1007/978-3-662-49851-4  
   https://link.springer.com/book/10.1007/978-3-662-49851-4

5. **David Harel — “Statecharts: A Visual Formalism for Complex Systems,” 1987**  
   状态图 / Statecharts 的经典论文。  
   DOI: 10.1016/0167-6423(87)90035-9  
   https://doi.org/10.1016/0167-6423(87)90035-9

6. **PLCopen — IEC 61131-3**  
   公开说明 IEC 61131-3 的编程语言体系，并明确说明 SFC 用于组织 PLC 程序与功能块中的步骤和迁移。正式标准可进一步参见 IEC 61131-3。  
   https://www.plcopen.org/standards/logic/iec-61131-3/

7. **ISO 13849-1:2023 — Safety of machinery — Safety-related parts of control systems**  
   ISO 官方摘要页，用于说明机械安全相关控制系统的设计原则。  
   https://www.iso.org/standard/73481.html

8. **ISA — ISA-18.2, Management of Alarm Systems for the Process Industries**  
   ISA 对报警管理标准体系的公开说明，并说明 ISA-18.2 与 IEC 62682 的关系。  
   https://www.isa.org/intech/2020/september-october/isa-18-2-management-of-alarm-systems-for-the-proce

9. **ISA — ISA-95 Series of Standards: Enterprise-Control System Integration**  
   ISA 官方公开页面，说明 ISA-95 / IEC 62264 的层级、对象和企业系统与制造控制系统之间的信息集成边界。  
   https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard

10. **Martin Leucker, Christian Schallhart — “A brief account of runtime verification,” 2009**  
    运行时验证的代表性综述。  
    DOI: 10.1016/j.jlap.2008.08.004  
    https://doi.org/10.1016/j.jlap.2008.08.004

## 文档信息

题目："TPCA / PCN 与既有工业自动化方法和控制机制的关系"  
文档类型：技术札记  
版本：Public Note Version 1.2  
首次发布日期：2026-07-04  
最后更新：2026-08-20  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/tpca-existing-theories/
