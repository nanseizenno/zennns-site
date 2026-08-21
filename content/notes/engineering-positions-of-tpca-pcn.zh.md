---
title: "TPCA / PCN 面对已有技术分歧，它站在哪里？——三个典型工程争议"
summary: "从确定性控制与 AI、集中控制与分布式自治、保守阻断与受控继续三个典型工程争议出发，说明 TPCA / PCN 的基本技术立场。"
description: "结合系统安全、强化学习、分布式控制、故障容错与 Graceful Degradation 等代表性研究，说明 TPCA / PCN 在运行时控制、节点部署、时间信息、异常处置和后续目标状态选择方面的工程立场与架构选择。"
date: 2026-08-18
lastmod: 2026-08-21
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.1"
citation_url: "https://zennns.com/zh/notes/engineering-positions-of-tpca-pcn/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## TPCA / PCN 面对已有技术分歧，它站在哪里？

复杂工程系统中的架构选择通常不存在脱离应用条件的唯一答案。

例如：

- 运行时控制应以确定性规则为主，还是引入 AI / 数据驱动方法；
- 系统应采用集中式控制，还是将判断分布到局部节点；
- 状态异常或能力下降后，应立即阻断，还是在满足约束的条件下受控继续。

这些问题分别对应安全保证、系统复杂度、自治能力、可用性和故障容错等不同工程目标。

TPCA / PCN 不试图证明其中某一种技术路线在所有场景下具有绝对优势。

本页关注的是：

> **面对这些长期存在的技术分歧，TPCA / PCN 将不同技术职责放在什么工程位置，并采用什么架构边界。**

---

## 1. 运行时确定性控制与 AI / 数据驱动分析

在安全相关和高可靠工程系统中，明确的控制约束、可验证性、可追溯性和变更管理具有重要作用。

Leveson 提出的 STAMP / STPA 是系统安全领域具有代表性的系统理论方法。其分析重点从单一部件失效扩展到控制结构、控制约束、不安全控制动作及反馈关系等系统层问题。[1]

另一方面，强化学习等方法强调通过状态、动作、反馈和奖励形成策略。Sutton 与 Barto 的工作系统总结了强化学习的基本问题、算法和学习型智能体框架，是学习型决策方法的重要代表。[2]

当机器学习进入安全关键系统后，模型性能之外还需要考虑安全保证、认证和可接受风险等问题。Goodloe 对 Machine Learning Enabled Systems 的安全保证挑战进行了专门讨论，并指出传统安全保证过程与机器学习系统之间仍存在需要进一步研究的问题。[3]

### TPCA / PCN 的工程立场

TPCA / PCN 将**运行时确定性控制**与**AI 辅助分析**区分为不同职责。

PCN Runtime 面向当前目标状态入口，承担在线状态处理、结构化判定、控制仲裁和控制输出。对于关键控制关系，应优先保证：

- 判定逻辑可明确描述；
- 关键约束可验证；
- 规则和配置可版本管理；
- 控制结果可追溯；
- 工程变更可以按照既有流程审核和确认。

PCN Trace 则记录一次状态迁移判定中的当前状态、目标状态、关键输入、CAE-SDB Result、时间信息 T、控制仲裁、多路径控制和执行结果。

在这一基础上，AI 更适合开展：

- 履历比较；
- 模式识别；
- 重复问题发现；
- 时间序列和持续状态分析；
- 改善候选整理；
- 控制结果效果比较；
- 工程报告生成。

因此，本体系的基本边界是：

> **AI 可以辅助发现问题和提出改善候选，但不绕过 PCN 及既有安全与控制机制直接承担现场确定性控制职责。**

这里的 T 仅表示与状态和判定结果一起保留的时间信息，用于确定事件先后关系、支持动态时序有效性判断并形成可追溯的 PCN Trace。工业数据模型和分布式系统研究中，将状态值、事件与时间信息关联已有成熟工程基础。[8][9]

这并不否定未来 AI 在工业控制中的进一步应用，而是明确当前 TPCA / PCN 的工程责任边界。

---

## 2. 集中式控制与分布式自治

集中式控制能够获取较完整的全局信息，有利于统一协调任务、资源、优先级和系统级约束。

但随着系统规模扩大，集中式架构也可能面临通信负担增加、逻辑复杂度上升、模块耦合增强以及局部修改影响范围扩大等问题。

分布式和分层控制则将部分决策分配到局部节点，并通过节点之间的信息交换实现系统协同。

Scattolini 对大型系统中的去中心化、分布式和分层模型预测控制架构进行了综述和分类，比较了不同架构的基本原理、适用范围、优点与局限。[4]

Ren 与 Beard 则围绕多主体系统的信息一致性与协同控制，系统讨论了基于邻接信息交换的分布式一致性方法及其在多车辆协同控制中的应用。[5]

这些研究说明，大规模系统中的控制架构通常需要在全局协调能力、局部自治能力、通信依赖和系统复杂度之间进行权衡。

### TPCA / PCN 的工程立场

TPCA / PCN 采用：

> **局部目标状态入口的判定节点化，跨节点协同问题分层处理。**

一个 PCN 对应一个明确的目标状态入口。

该 PCN 负责组织与本次状态迁移直接相关的状态，并完成本节点的前置判定和控制输出。

多个 PCN 按实际状态迁移关系以及必要的许可、资源和执行依赖关系连接后，可以形成 PCN Network。

当问题涉及：

- 多个 PCN；
- 共享资源；
- 跨节点许可；
- 群体执行能力；
- MES / WCS 调度；
- 多主体协同停滞；

则由相应的协同层、调度层或更高层工程逻辑进行处理。

因此，TPCA / PCN 并不预设所有判定必须集中到单一中央控制器，也不要求各节点完全自治。

其架构选择可以概括为：

> **目标状态入口在局部形成明确 PCN，跨节点关系按照实际系统层级进行协调。**

PCN Network 可以存在状态类型上的循环关系。

例如某个生产流程可能反复出现：

```text
等待
→ 执行
→ 检测
→ 再次等待
```

但实际运行中的状态实例仍然沿时间方向持续生成。

因此：

> **状态类型关系可以循环，实际状态实例不存在时间回退。**

这一点使 PCN Network 既可以表达循环工艺、返工、回流和重新投入等实际工程结构，又不需要把系统解释为“回到过去的状态实例”。

这一结构的重点不是“分布式”这一名称本身，而是让每一次状态迁移判定具有明确的工程责任边界，同时保留系统级协同能力。

---

## 3. 保守阻断与受控继续

安全相关系统首先需要保证不可越过的关键约束。

当关键安全条件或必要许可无法确认时，不能仅以生产效率或运行连续性为理由继续进入目标状态。

另一方面，故障容错控制研究表明，系统发生故障以后，控制目标并不一定只有“保持完全正常”或“立即完全停止”两种选择。

Blanke、Kinnaert、Lunze 和 Staroswiecki 的故障诊断与容错控制研究系统讨论了故障检测、故障容纳、控制重构及系统可重构性等问题。其基本目标之一，是在故障发生后根据系统剩余能力和约束调整控制策略，以兼顾安全性和可用性。[6]

Graceful Degradation（渐进式降级）研究也关注系统能力下降后的受约束运行。Edwards 与 Lee 在空中交通控制场景中研究了系统退化的成因、相互作用以及预防和缓解策略，强调复杂系统在性能或能力下降时仍需要维持安全与韧性。[7]

这些研究并不意味着所有异常都应继续运行，而是说明：

> **异常状态后的工程处理可以存在多种受约束路径。**

### TPCA / PCN 的工程立场

TPCA / PCN 不预先将所有异常统一映射为“停止”，也不将“继续运行”作为优先目标。

其基本原则是：

> **先形成结构化判定，再根据关键约束和完整判定结果进行控制仲裁，并确定后续目标状态或目标执行路径。**

其中，关键 Authority 可以构成独立必要约束。

例如，关键安全许可不成立时，即使其他 Condition 和 Execution Chain 状态均满足，也不得进入目标状态。

对于其他异常、退化或边界状态，则不将某一个 CAE-SDB Result 机械地映射为固定控制动作。

基本关系为：

```text
CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ New Target State / Target Path
```

其中：

- CAE-SDB Result 用于描述本次目标状态入口形成的结构化判定结果；
- T 用于标识本次状态和判定所处的时间位置；
- Arbitration 根据关键许可、控制约束和多个判定结果处理控制优先关系；
- Multipath Control 最终确定系统下一步进入的目标状态或目标执行路径。

代表性控制路径可以包括：

- Allow；
- Wait；
- Recheck；
- Retry；
- Return；
- Degrade；
- Manual Confirm；
- Prohibit；
- Safety Lock；
- 其他预先定义的处理路径。

这些名称用于描述不同工程用途的控制路径。

从 TPCA 的状态迁移视角看，无论是 Retry、Return、Degrade 还是 Safety Lock，实际控制都表现为：

```text
Current State
→ New Target State / Target Path
```

即使新的目标状态与历史某一状态具有相同或相似的工程内容，由于发生时间和迁移历史不同，仍属于新的状态实例。

因此，TPCA / PCN 在“保守阻断”与“受控继续”之间的选择，不由单一异常标签直接决定，也不存在通过控制路径“回到过去状态”的处理逻辑。

系统始终基于当前状态和当前判定，选择下一目标状态。

---

## 小结

上述三个工程争议对应 TPCA / PCN 的三项基本技术立场。

### 运行时确定性控制与 AI

> **PCN Runtime 承担运行时前置判定与确定性控制职责；AI 主要基于包含状态、判定结果、时间信息 T、控制输出和执行结果的 PCN Trace 开展辅助分析。**

### 集中式控制与分布式自治

> **目标状态入口的判定通过 PCN 节点化；跨节点资源、许可和协同问题按照实际系统层级处理。状态类型关系可以循环，但实际状态实例沿时间方向持续生成。**

### 保守阻断与受控继续

> **不预先将异常统一定义为停止或继续，而是在结构化判定基础上，通过控制仲裁确定后续目标状态或目标执行路径。**

TPCA / PCN 不替代系统安全、强化学习、分布式控制或故障容错理论。

这些理论和方法分别解决安全分析、学习型决策、多主体协同、故障容错与退化运行等不同问题。

TPCA / PCN 关注的是：

> **当这些不同技术要求共同参与一次目标状态进入时，如何将它们放到明确的工程位置，并围绕同一个目标状态入口形成可判定、可控制和可记录的工程关系。**

其基本工程关系可以进一步概括为：

```text
Target State Entry
→ PCN
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ New Target State / Target Path
→ PCN Trace
```

---

## 参考文献与外部依据

以下资料用于说明本文涉及的系统安全、学习型决策、分布式控制、故障容错、渐进式降级以及状态时间信息与事件顺序等已有技术背景。

这些资料用于说明 TPCA / PCN 所面对的既有工程分歧及其工程基础，**不构成 TPCA / PCN 的理论来源说明，也不用于直接证明相关专利的新颖性或创造性。**

1. **LEVESON N G.**  
   *Engineering a Safer World: Systems Thinking Applied to Safety*.  
   Cambridge, MA: MIT Press, 2012.  
   https://mitpress.mit.edu/9780262297301/engineering-a-safer-world/

2. **SUTTON R S, BARTO A G.**  
   *Reinforcement Learning: An Introduction*. 2nd ed.  
   Cambridge, MA: MIT Press, 2018.  
   https://mitpress.mit.edu/9780262039246/reinforcement-learning/

3. **GOODLOE A E.**  
   *Assuring Safety-Critical Machine Learning Enabled Systems: Challenges and Promise*.  
   NASA Technical Reports Server, Document ID 20220011814, 2022.  
   https://ntrs.nasa.gov/citations/20220011814

4. **SCATTOLINI R.**  
   Architectures for Distributed and Hierarchical Model Predictive Control: A Review.  
   *Journal of Process Control*, 2009, 19(5): 723–731.  
   DOI: 10.1016/j.jprocont.2009.03.001  
   https://www.sciencedirect.com/science/article/pii/S0959152409000353

5. **REN W, BEARD R W.**  
   *Distributed Consensus in Multi-vehicle Cooperative Control: Theory and Applications*.  
   London: Springer, 2008.  
   DOI: 10.1007/978-1-84800-015-5  
   https://link.springer.com/book/10.1007/978-1-84800-015-5

6. **BLANKE M, KINNAERT M, LUNZE J, STAROSWIECKI M.**  
   *Diagnosis and Fault-Tolerant Control*. 3rd ed.  
   Berlin, Heidelberg: Springer, 2016.  
   DOI: 10.1007/978-3-662-47943-8  
   https://link.springer.com/book/10.1007/978-3-662-47943-8

7. **EDWARDS T, LEE P U.**  
   Designing Graceful Degradation into Complex Systems: The Interaction Between Causes of Degradation and the Association with Degradation Prevention and Recovery.  
   AIAA Aviation Forum, 2018. NASA Technical Reports Server, Document ID 20180006863.  
   https://ntrs.nasa.gov/citations/20180006863

8. **OPC Foundation.**  
   *OPC Unified Architecture — Part 4: Services, DataValue.*  
   OPC UA Specification.  
   DataValue 将 Value、StatusCode 与 SourceTimestamp、ServerTimestamp 等信息关联，用于表示工业数据值及其时间信息。  
   https://reference.opcfoundation.org/specs/OPC-10000-4/7.11

9. **LAMPORT L.**  
   Time, Clocks, and the Ordering of Events in a Distributed System.  
   *Communications of the ACM*, 1978, 21(7): 558–565.  
   DOI: 10.1145/359545.359563  
   https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/

---

## 文档信息

题目：TPCA / PCN 面对已有技术分歧，它站在哪里？——三个典型工程争议  
文档类型：技术札记  
版本：Public Note Version 1.1  
首次发布日期：2026-08-18  
最后更新：2026-08-21  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/engineering-positions-of-tpca-pcn/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
