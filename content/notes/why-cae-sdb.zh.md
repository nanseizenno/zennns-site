---
title: "为什么是 CAE-SDB？——目标状态入口前的双轴结构化分析方法"
summary: "CAE-SDB 是 TPCA / PCN 中用于目标状态入口前复杂状态判定的核心分析方法。C / A / E 用于整理条件、许可和执行链三类状态迁移角色，S / D / B 用于判断结构完整性、动态时序有效性和控制边界。"
description: "说明 TPCA / PCN 中 CAE-SDB 核心分析方法的双轴结构，以及 C / A / E 状态变量域与 S / D / B 判定性质如何形成结构化判定结果。"
date: 2026-08-25
lastmod: 2026-09-13
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

**CAE-SDB 是 TPCA / PCN 中用于 Target State Entry 前复杂状态判定的核心结构化分析方法。**

在制造和自动化系统中，一次状态迁移往往同时受到设备状态、安全许可、视觉结果、任务状态、下游承接和上位系统状态等多个因素影响。

这些状态来自不同设备和系统，但在一次明确的状态迁移中，需要回答两个不同的问题：

```text
第一轴：这个状态在本次状态迁移中承担什么作用？

第二轴：应从什么性质判定这个状态？
```

CAE-SDB 将这两个问题分别整理为：

```text
C / A / E：状态迁移功能角色

S / D / B：状态判定性质
```

其中：

```text
C = Condition         条件状态
A = Authority         许可状态
E = Execution Chain   执行链状态

S = Structure         结构完整性
D = Dynamics          动态时序有效性
B = Boundary          控制边界
```

通过 **C / A / E × S / D / B** 的双轴结构，可以明确表示：

> **哪个状态变量域，出现了哪一种判定结果。**

这些结构化结果进一步进入 Arbitration、Multipath Control 和 PCN Trace，形成从状态分析到控制与履历的工程闭环。

---

## 1. 为什么需要两条轴

TPCA / PCN 将系统从 Current State 准备进入 Target State 的工程入口定义为 Target State Entry。

以机器人进入抓取阶段为例，现场可能同时存在：

```text
VisionOK = TRUE
SafetyPermission = TRUE
RobotReady = TRUE
DownstreamAvailable = TRUE
```

这些状态都与当前 Target State Entry 有关，但承担的工程作用不同。

`VisionOK` 与进入抓取阶段所需条件有关。

`SafetyPermission` 决定当前是否允许进入。

`RobotReady` 与 `DownstreamAvailable` 则参与判断进入抓取阶段以后，执行链是否能够继续。

另一方面，一个状态即使当前值为 TRUE，也仍然需要确认：

```text
相关信号和接口是否已经正确建立；
状态是否仍属于当前对象和当前周期；
状态是否仍在有效时间内；
相关数值是否仍处于允许范围。
```

因此：

```text
状态在本次迁移中的作用

        ×

状态当前应接受什么性质的判定
```

是两个相互独立的问题。

CAE-SDB 将前者整理为 C / A / E，将后者整理为 S / D / B。

---

## 2. C / A / E：状态迁移功能角色

C / A / E 用于根据状态在当前 Target State Entry 中承担的工程作用进行整理。

```text
C：进入目标状态所需的条件

A：是否允许进入目标状态

E：进入目标状态以后执行链能否继续
```

可以将其理解为一次状态迁移中的三个不同功能位置：

```text
进入前                Target State Entry                进入后

  │                           │                           │

  C                           A                           E

条件状态                    许可状态                 执行链状态
```

C、A、E 均在进入 Target State 之前由 PCN 获取和判定。

### 2.1 C：Condition｜条件状态

C 表示进入目标状态之前需要成立的条件状态。

典型内容包括：

- 工件是否存在；
- 对象、位置、姿态是否满足要求；
- 视觉或检测结果是否已经取得；
- 前序工序是否完成；
- 请求参数是否完整；
- 必要数据是否存在。

C 回答：

> **当前是否具备进入这个目标状态的条件？**

### 2.2 A：Authority｜许可状态

A 表示系统当前是否允许进入目标状态。

典型内容包括：

- 安全许可；
- 区域许可；
- 上位系统许可；
- 对方设备许可；
- 资源锁；
- 用户权限；
- 人工确认。

关键 A 可以构成独立必要约束。

当关键许可未成立时，即使 C 与 E 已经满足，本次 Target State Entry 仍不得放行。

A 回答：

> **当前是否允许进入这个目标状态？**

### 2.3 E：Execution Chain｜执行链状态

E 表示进入 Target State 后，当前目标阶段所需要的执行链是否能够继续接续。

例如机器人进入抓取阶段时，相关状态可能包括：

- 机器人运行准备状态；
- 机器人路径可达状态；
- 夹爪或末端执行机构状态；
- 下游接收状态；
- 对方设备承接状态；
- 结果上传或回写链路状态。

因此，一个单体设备的 Ready 可以作为 E 的输入之一，E 关注的是整个目标执行链接续性。

E 回答：

> **进入当前 Target State 后，这一执行链是否能够继续？**

E 必须绑定当前 Target State Entry。

替代路径、回流路径、异常路径等如果形成新的候选状态迁移，应在对应 Target State Entry 下重新进行判定。

---

## 3. S / D / B：状态判定性质

完成 C / A / E Mapping 后，PCN 根据当前 Target State Entry 已定义的判定规则，对相关状态执行 S / D / B Evaluation。

```text
S：结构是否建立完整？

D：当前状态是否仍然有效？

B：当前状态是否仍在界内？
```

### 3.1 S：Structure｜结构完整性

S 用于确认本次状态迁移判定所需要的工程结构是否已经建立。

典型检查内容包括：

- 必要信号是否定义；
- 接口是否接入；
- 对象与状态之间的映射关系是否明确；
- 许可来源是否确定；
- 相关路径是否定义；
- 执行链边界是否明确；
- 必要状态是否可观测。

S 回答：

> **本次判定所依赖的结构是否已经定义、接入并可观测？**

### 3.2 D：Dynamics｜动态时序有效性

D 用于确认已经存在的状态，当前是否仍能够作为本次 Target State Entry 的有效判定依据。

典型问题包括：

- 超时；
- 未刷新；
- 抖动；
- 冲突；
- 延迟；
- 不同步；
- 低置信度；
- 许可撤销；
- 状态切换。

例如：

```text
VisionOK = TRUE
```

如果该结果对应上一件工件，则不能继续用于当前抓取入口。

状态值虽然存在，但已经失去当前状态迁移的动态有效性。

D 回答：

> **这个状态当前还能否作为本次 Target State Entry 的有效判定依据？**

### 3.3 B：Boundary｜控制边界

B 用于确认相关状态是否处于预先定义的允许范围、阈值或控制边界以内。

典型边界包括：

```text
Min / Max
Threshold
Tolerance
Range
Time Window
Quota
Capacity
Rate Limit
Retry Limit
```

例如尺寸允许范围为：

```text
19.90 mm ～ 20.10 mm
```

则：

```text
20.06 mm → 范围内
20.18 mm → 范围外
```

B 回答：

> **当前状态是否仍处于这个 Target State Entry 已定义的控制边界内？**

D 与 B 分别处理两个不同的问题：

```text
D：这个状态现在是否仍然有效？

B：这个有效状态现在是否仍然在允许范围内？
```

例如：

```text
视觉结果属于上一件工件
→ D

视觉结果属于当前工件，但位置偏差超出允许范围
→ B
```

---

## 4. C / A / E 与 S / D / B 如何组合

两条轴组合后形成 CAE-SDB 双轴判定结构。

| 状态变量域 | S：结构完整性 | D：动态时序有效性 | B：控制边界 |
|---|---|---|---|
| C：条件状态 | C-S | C-D | C-B |
| A：许可状态 | A-S | A-D | A-B |
| E：执行链状态 | E-S | E-D | E-B |

这些坐标表示：

```text
哪个状态变量域

×

出现了哪一种判定结果
```

例如：

```text
C-D：条件状态存在动态时序有效性问题
A-D：许可状态存在动态时序有效性问题
E-B：执行链状态超出预先定义的控制边界
C-S：条件状态所需结构尚未完整建立
```

同一个状态变量域可以接受多种判定。

例如视觉识别结果映射到 C 后，可以分别检查：

```text
C-S
识别结果接口和对象映射是否已经建立

C-D
识别结果是否仍属于当前工件并处于有效时间内

C-B
置信度、位置偏差等是否处于允许范围
```

同一种判定性质也可以作用于不同变量域：

```text
C-D：视觉结果过期

A-D：许可已经撤销

E-D：下游状态长时间未刷新
```

CAE-SDB Result 只能在相应规则已经定义、输入具备判定依据，并完成实际 Evaluation 后形成。

时间信息 T 与相关状态和判定结果一起保留。

---

## 5. 从 CAE-SDB Result 到控制与履历

CAE-SDB 完成 Target State Entry 前的结构化状态判定。

基本工程关系为：

```text
Current State
    ↓
Target State
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
Execution Result
    ↓
PCN Trace
```

一次 Target State Entry 中可以同时产生多个 CAE-SDB Result。

例如：

```text
C-D
A-B
E-D
```

这些结果与时间信息 T 一起进入 Arbitration。

Arbitration 根据关键许可、安全约束、预先定义的控制规则及当前合法控制路径处理优先关系。

随后形成针对本次 Target State Entry 的 Multipath Control。

代表性的控制路径包括：

```text
允许进入
等待
重识别
重采样
重定位
重试
回流
异常分流
下游协调
资源释放
降级执行
人工确认
禁止进入
安全锁定
异常隔离
增强记录
```

CAE-SDB Result 与控制路径之间不采用固定的一一对应关系。

同一个判定结果在不同 Target State Entry、不同风险条件及不同控制规则下，可以形成不同的合法控制路径。

PCN Trace 用于记录本次状态迁移中的主要状态、判定结果、控制结果和执行结果。

长期履历可以进一步用于比较：

- 哪些 Target State Entry 反复出现问题；
- 哪些 C / A / E 状态域问题出现频率较高；
- 哪些 S / D / B 判定性质反复出现；
- 不同控制路径最终产生了什么执行结果。

---

## 6. 方法边界与当前范围

CAE-SDB 当前用于 TPCA / PCN 中 Target State Entry 前的结构化状态判定。

当前主要关注三个问题：

```text
C / A / E 是否能够稳定整理状态迁移中的主要功能角色；

S / D / B 是否能够稳定整理状态所需要的主要判定性质；

CAE-SDB Result 是否能够持续连接后续 Arbitration、
Multipath Control 和 PCN Trace。
```

当前公开定义不主张已经通过数学方法证明 C / A / E 或 S / D / B 对所有工程系统具有形式上的完备性。

如果后续在不同设备、系统或行业中持续出现现有 C / A / E 无法自然表示的独立状态迁移角色，或出现 S / D / B 无法自然表示的独立判定性质，应作为新的候选结构单独验证。

因此，CAE-SDB 当前首先作为一种面向工程状态迁移前判定的结构化分析方法使用，其适用范围通过持续的工程案例、PoC 和跨对象应用进一步验证。

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

题目：为什么是 CAE-SDB？——目标状态入口前的双轴结构化分析方法  
文档类型：技术札记  
版本：Public Note Version 1.1  
首次发布日期：2026-08-25  
最后更新：2026-09-13  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/why-cae-sdb/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
