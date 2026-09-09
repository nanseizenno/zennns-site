---
title: "为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构"
summary: "说明在目标状态入口之前，C / A / E 如何按本次状态迁移中的作用整理相关状态，S / D / B 又如何分别从结构完整性、动态时序有效性和控制边界进行判定。通过双轴结构，可统一表示在哪个状态变量域确认了哪一类判定结果。"
description: "说明 TPCA / PCN 中 CAE-SDB 的双轴结构，以及 C / A / E 状态变量域与 S / D / B 判定性质之间的关系。"
date: 2026-08-25
lastmod: 2026-09-09
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.1"
citation_url: "https://zennns.com/zh/notes/why-cae-sdb/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## 为什么是 CAE-SDB？

在制造和自动化系统中，即使设备已经 Ready，也可能因为安全许可、视觉结果、下游接收状态或上位系统许可等原因，无法进入下一执行阶段。

这类状态迁移前判定需要先把两个问题分开。

```text
第一轴：这个状态在本次状态迁移中代表什么。

第二轴：从什么角度判定这个状态。
```

TPCA / PCN 将系统从 Current State 准备进入 Target State 的入口定义为 Target State Entry。与这个入口直接相关的状态，可能来自设备 Ready、视觉识别、安全系统、任务状态、下游设备或上位系统。

CAE-SDB 用两条轴整理这些状态：

```text
C / A / E：状态变量域

S / D / B：判定性质
```

C / A / E 表示相关状态在本次迁移中的作用，S / D / B 表示对这些状态采用哪一类判定。

这样，同一个状态可以根据工程需要分别进行 S、D、B 判定；不同设备和系统即使使用不同的信号名称和实现方式，判定结果仍可以用 C-S、A-D、E-B 等统一形式记录，并继续进入 Arbitration、Multipath Control 和 PCN Trace。

当前定义为：

```text
C = Condition         条件状态
A = Authority         许可状态
E = Execution Chain   执行链状态

S = Structure         结构完整性
D = Dynamics          动态时序有效性
B = Boundary          控制边界
```

双轴组合后，可以明确回答：**哪个状态变量域出现了哪一种判定结果。**

---

## 1. 为什么要分成两条轴

以机器人进入抓取阶段为例，现场可能同时使用以下状态：

```text
VisionOK = TRUE
SafetyPermission = TRUE
RobotReady = TRUE
DownstreamAvailable = TRUE
```

这些状态都与当前 Target State Entry 有关，但在本次状态迁移中的作用并不相同。VisionOK 与抓取条件有关，SafetyPermission 与进入许可有关，RobotReady 和 DownstreamAvailable 则与进入抓取阶段后的执行链接续有关。

另一方面，即使 `VisionOK = TRUE`，也不能只看这个布尔值本身。工程上还需要确认信号及对象映射是否已经定义、结果是否对应当前工件、结果是否仍在有效时间内，以及置信度、位置偏差等是否处于预先定义的范围。

因此，状态本身承担什么作用，和这个状态应从什么角度进行判定，是两个不同的问题。

CAE-SDB 将前者放在 C / A / E 轴上，将后者放在 S / D / B 轴上。

```text
状态在本次迁移中的作用
C / A / E

        ×

状态的判定性质
S / D / B
```

---

## 2. C / A / E：整理状态在本次迁移中的作用

C / A / E 是三个状态变量域，用于根据相关状态在当前 Target State Entry 中的工程作用进行整理。

```text
C：进入目标状态所需的前提条件

A：是否允许进入目标状态

E：进入目标状态后所需的执行链
```

从功能位置看，可以理解为：

```text
进入前                Target State Entry                进入后

  │                           │                           │

  C                           A                           E

条件状态                    许可状态                 执行链状态
```

C、A、E 都在进入目标状态之前由 PCN 获取和判定。E 不是进入目标状态以后才检查，而是在进入前确认当前 Target State 所要求的执行链是否能够继续。

### 2.1 C：Condition / 条件状态

C 处理的是进入目标状态所需的前提条件。

在自动化单元中，典型内容包括工件是否存在、对象和位置姿态是否满足要求、视觉结果是否已经取得、前序工序是否完成；在数字系统中，也可以是请求参数是否完整、必要数据是否存在等。

C 回答的是：

> 当前是否具备进入这个目标状态的前提条件。

### 2.2 A：Authority / 许可状态

A 处理的是系统是否被允许进入目标状态。

安全许可、区域许可、上位系统许可、资源锁、审批状态、用户权限或人工确认，都可以根据当前 Target State Entry 中的工程作用映射到 A。

其中，关键 A 可以构成独立必要约束。关键许可未成立时，即使 C 和 E 都满足，也不得允许进入当前 Target State。

A 回答的是：

> 当前是否允许进入这个目标状态。

### 2.3 E：Execution Chain / 执行链状态

E 处理的是进入当前 Target State 后，该阶段所需要的执行链能否继续。

`RobotReady = TRUE` 只能说明机器人本体具备一定的运行准备条件。对抓取阶段而言，还可能需要确认机器人路径、夹爪、下游接收、对方设备状态，以及结果上传或回写链路是否能够支持本次目标状态后的继续执行。

E 因此不等于 Ready，也不等于某一个单体设备状态。

E 回答的是：

> 进入当前 Target State 后，这一执行链是否能够继续。

这里的 E 必须绑定当前 Target State Entry。其他替代路径、回流路径或异常处理路径，应作为各自候选 Target State Entry 的执行链条件处理，不能因为替代路径可用，就直接判定当前 Target State 的 E 已成立。

---

## 3. S / D / B：从什么角度判定状态

完成 C / A / E Mapping 后，PCN 对相关状态执行当前 Target State Entry 已经定义且具备判定依据的 S / D / B Evaluation。

S / D / B 不表示设备类别，也不表示控制动作，而是三种判定性质：

```text
S：判定所需结构是否完整。

D：当前状态是否仍可作为本次判定依据。

B：当前状态是否处于预先定义的控制边界内。
```

### 3.1 S：Structure / 结构完整性

S 用于确认本次状态迁移判定所需要的工程结构是否已经建立。

例如，必要信号或字段是否定义，接口是否已经连接，状态和对象之间的映射是否明确，许可来源是否清楚，执行链关系及边界是否定义，以及必要状态是否能够被观测。

S 关注的是：

> 本次判定所依赖的结构是否已经定义、接入并可观测。

### 3.2 D：Dynamics / 动态时序有效性

D 用于确认一个已经存在的状态，当前是否仍可以作为本次 Target State Entry 的有效判定依据。

典型问题包括超时、长时间未刷新、过期、抖动、冲突、延迟、不同步、版本不一致、许可撤销以及状态切换过程。

例如：

```text
VisionOK = TRUE
```

如果这个结果属于上一件工件，就不能继续用于当前抓取入口的判定。状态值虽然存在，但已经失去本次状态迁移的有效性。

D 关注的是：

> 这个状态当前还能不能用于本次 Target State Entry 的判定。

### 3.3 B：Boundary / 控制边界

B 用于确认状态是否仍处于预先定义的允许范围、阈值或控制边界内。

常见边界包括 Min / Max、Threshold、Tolerance、Range、Time Window、Quota、Capacity、Rate Limit 和 Retry Limit。

例如某尺寸允许范围为：

```text
19.90 mm ～ 20.10 mm
```

则：

```text
20.06 mm → 范围内
20.18 mm → 范围外
```

B 关注的是：

> 当前状态是否仍处于这个 Target State Entry 已定义的控制边界内。

D 与 B 的区别在工程上需要保持清楚。D 判断的是状态当前是否仍有效，B 判断的是有效状态是否位于允许范围内。

例如，视觉结果属于上一件工件或已经过期，属于 D；视觉结果属于当前工件，但置信度或位置偏差超出设定范围，则属于 B。

---

## 4. C / A / E 与 S / D / B 如何组合

两条轴组合后，可以形成以下判定坐标。

| 状态变量域 | S：结构完整性 | D：动态时序有效性 | B：控制边界 |
|---|---|---|---|
| C：条件状态 | C-S | C-D | C-B |
| A：许可状态 | A-S | A-D | A-B |
| E：执行链状态 | E-S | E-D | E-B |

这个表表示的是：

```text
哪个状态变量域

×

出现了哪一种判定结果
```

例如，视觉识别结果被映射到 C，并且确认其有效时间已经超出，则可以形成 `C-D`。这里表达的是：条件状态在动态时序有效性方面出现了结果。

同理，许可已经撤销，可以形成 A-D；执行链状态超出预先定义的容量或范围，可以形成 E-B；条件状态所需信号或接口没有建立，可以形成 C-S。

同一个状态变量域可以分别接受 S、D、B 判定。以视觉结果为例，S 可以确认识别结果及对象对应关系是否建立，D 可以确认结果是否仍属于当前工件且未过期，B 可以确认置信度或位置偏差是否处于允许范围。

反过来，同一种判定性质也可以应用到不同变量域。例如：

```text
C-D：视觉结果过期

A-D：许可已经撤销

E-D：下游状态长时间未刷新
```

需要注意的是，C-S、A-D、E-B 等结果只能在相应规则已经配置、当前输入具备判定依据，并且实际完成 S / D / B Evaluation 后形成。不能仅根据现场现象直接给出 CAE-SDB Result。

时间信息 T 与状态和判定结果一起保留。

---

## 5. CAE-SDB Result 如何进入控制和履历

CAE-SDB 的职责是把与 Target State Entry 有关的状态按双轴结构完成判定，并把结果交给后续控制处理。

基本关系如下：

```text
当前状态
    ↓
目标状态
    ↓
Target State Entry / PCN
    ↓
C / A / E Mapping
    ↓
S / D / B Evaluation
    ↓
CAE-SDB Result + T
    ↓
Arbitration
    ↓
Multipath Control
    ↓
执行结果
    ↓
PCN Trace
```

一次 Target State Entry 中可能同时出现多个 CAE-SDB Result。例如 C-D、A-B、E-D 可以在同一次判定中同时出现。

这些结果与时间信息 T 一起进入 Arbitration。Arbitration 根据关键许可、安全约束、预先定义的控制规则以及当前允许的控制路径处理优先关系。关键 A 未成立时，仍作为独立必要约束处理。

经过 Arbitration 后，再形成针对本次 Target State Entry 的 Multipath Control。代表性控制路径可以是允许进入、等待、重识别、重采样、重定位、重试、回流、异常分流、下游协调、资源释放、降级执行、人工确认、禁止进入、安全锁定、异常隔离或增强记录。

CAE-SDB Result 与控制路径之间不存在固定的一一对应关系。相同的判定结果，在不同 Target State Entry、不同安全约束和不同控制规则下，可以产生不同的合法控制路径。

替代、回流、退避等路径都属于后续候选 Target State 或 Target Path。它们是否可用，需要在对应入口下重新判定，不能直接用于证明当前 Target State 可以进入。

PCN Trace 用于记录本次状态迁移的主要状态、判定、控制和执行信息。长期积累后，可以比较某个 Target State Entry 中哪些变量域、哪些判定性质反复出现问题，以及相应控制路径和执行结果如何变化。

---

## 6. 当前验证范围

CAE-SDB 是当前 TPCA / PCN 中用于 Target State Entry 前置判定的结构化逻辑。

现阶段主要验证三件事：C / A / E 是否能够稳定整理 Target State Entry 所需的状态迁移角色；S / D / B 是否能够稳定整理各类状态所需要的判定性质；CAE-SDB Result 是否能够持续连接到 Arbitration、Multipath Control 和 PCN Trace。

当前并不主张已经通过数学方法证明 C / A / E 或 S / D / B 在所有工程系统中不存在扩展空间。

如果后续在不同设备、系统或行业中，持续出现现有 C / A / E 无法自然表达的独立状态迁移角色，或者出现 S / D / B 无法自然表达的独立判定性质，应单独进行验证，而不是直接扩大当前定义。

---

## 参考文献与外部资料

以下资料用于说明状态建模、工业状态信息和复杂系统事件时序等相关工程基础，不表示这些既有理论与 CAE-SDB 存在一一对应关系，也不用于证明 CAE-SDB 的完备性。

1. **HAREL D.**  
   *Statecharts: A Visual Formalism for Complex Systems.*  
   *Science of Computer Programming*, 1987, 8(3): 231–274.  
   DOI: 10.1016/0167-6423(87)90035-9  
   https://www.sciencedirect.com/science/article/pii/0167642387900359

2. **OPC Foundation.**  
   *OPC Unified Architecture — Part 4: Services.*  
   OPC UA DataValue 将 Value、StatusCode、SourceTimestamp、ServerTimestamp 等信息关联，可作为理解工业状态值、状态质量和时间信息关系的参考。  
   https://reference.opcfoundation.org/specs/OPC-10000-4/full

3. **LAMPORT L.**  
   *Time, Clocks, and the Ordering of Events in a Distributed System.*  
   *Communications of the ACM*, 1978, 21(7): 558–565.  
   DOI: 10.1145/359545.359563  
   https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/

---

## 文档信息

题目：为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构  
文档类型：技术札记  
版本：Public Note Version 1.1  
首次发布日期：2026-08-25  
最后更新：2026-09-09  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/why-cae-sdb/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
