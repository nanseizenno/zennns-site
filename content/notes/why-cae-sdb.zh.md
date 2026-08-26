---
title: "为什么是 CAE-SDB？——状态迁移功能角色与状态验证的双轴结构"
summary: "说明 CAE 与 SDB 在明确目标状态入口前的作用分工。CAE 用于映射相关状态在状态迁移中的功能角色，分别对应条件、许可和执行链；SDB 用于组织结构完整性、动态时序有效性和边界验证，并可复用已有成熟工程验证机制。"
description: "说明 TPCA / PCN 中 CAE-SDB 的双轴结构。CAE 作为状态迁移功能角色轴，将与目标状态进入有关的状态映射为 C 条件、A 许可和 E 执行链；SDB 作为状态验证轴，从 S 结构完整性、D 动态时序有效性和 B 边界三个性质进行验证。CAE-SDB 判定结果进一步进入控制仲裁、多路径控制与 PCN Trace。"
date: 2026-08-25
lastmod: 2026-08-26
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

TPCA / PCN 关注系统由当前状态进入明确目标状态之前的前置判定。

在这一工程位置，系统通常已经具有设备 Ready、视觉结果、安全许可、任务状态、服务健康状态、数据库状态等多种状态信息。各状态分别存在，并不能直接形成对同一目标状态入口的完整判定。

需要判定的问题是：

> 本次 Target State Entry 是否成立？

CAE-SDB 分别处理状态的功能角色和状态的验证性质。

```text
CAE：状态在本次迁移中承担什么功能角色？

SDB：状态是否能够作为本次迁移的有效判定依据？
```

当前定义如下：

```text
C = Condition         条件
A = Authority         许可
E = Execution Chain   执行链

S = Structure         结构完整性
D = Dynamics          动态时序有效性
B = Boundary          边界
```

CAE 构成状态迁移功能角色轴，SDB 构成状态验证轴。两者组合，用于形成明确 Target State Entry 前的结构化判定。

---

## 1. CAE：状态迁移功能角色

CAE 不按 PLC、机器人、MES、数据库或 API 等信号来源划分状态，而是根据状态在本次 Target State Entry 中承担的工程作用进行映射。

C、A、E 分别回答以下问题：

```text
C：具不具备？
A：允不允许？
E：接不接得住？
```

其功能位置可表示为：

```text
进入前                Target State Entry                进入后
  │                           │                           │
  C                           A                           E
条件                         许可                       执行链
```

“进入前—入口—进入后”用于说明 C、A、E 在状态迁移中的功能位置，不表示 E 在系统进入目标状态后才进行判断。C、A、E 均在目标状态入口之前进入 PCN 的前置判定。

### 1.1 C：Condition

C 用于判断进入目标状态所需的事实条件是否已经具备。

典型条件包括：

* 工件是否存在；
* 对象和位置是否正确；
* 识别结果是否已经取得；
* 请求参数是否完整；
* 前序工序或业务状态是否完成；
* 必要数据是否存在。

C 所描述的是与本次目标状态进入直接相关的条件状态。

### 1.2 A：Authority

A 用于判断系统是否被允许进入目标状态。

典型许可包括：

* 安全许可；
* 区域许可；
* 上位系统放行；
* 资源锁；
* 审批状态；
* 用户或租户权限；
* 预算许可。

关键 A 可以构成独立必要约束。对于不可绕过的关键许可，即使 C 与 E 均成立，只要关键 A 不成立，系统仍不得进入当前目标状态。

### 1.3 E：Execution Chain

E 用于判断系统进入目标状态后，完成该目标状态所依赖的必要执行链是否能够继续接续。

E 不等于单个设备或服务的 Ready。

例如：

```text
Robot Ready = TRUE
```

只能说明机器人自身处于相应就绪状态，不能据此确认夹爪、下游承接、异常排出和结果回写链均能够继续。

同样：

```text
Service Healthy = TRUE
```

不能据此确认数据库、消息队列、下游 API、Callback 和业务回写链均能够正常接续。

E 可以包括本体设备、末端执行机构、下游承接、备用或回退路径、异常处理路径、结果上传及回写链路等。

CAE 的作用，是将分散状态按本次状态迁移中的功能角色进行组织，使不同设备和系统中的状态能够采用一致的迁移关系进行描述。

---

## 2. SDB：状态验证轴

完成 C/A/E 功能角色映射后，还需要判断相关状态是否能够作为本次 Target State Entry 的有效判定依据。

例如：

```text
VisionOK = TRUE
```

还需要确认：

* 该状态是否已经正确定义并接入；
* 该结果是否对应当前工件；
* 该结果是否已经超时或失效；
* 当前值是否仍处于本次允许边界内。

S、D、B 分别对应：

```text
S：结构建立了吗？
D：当前状态有效吗？
B：当前状态在界内吗？
```

SDB 使用的底层检查机制在现有自动化系统和软件系统中已经普遍存在。SDB 的作用是按照统一的验证性质对这些机制进行组织。

### 2.1 S：Structure

S 用于判断支撑本次迁移判定所需的工程结构是否已经建立。

主要检查对象包括：

* 信号或字段是否定义；
* 接口是否接入；
* 映射关系是否正确；
* 许可来源是否明确；
* 执行链关系是否定义；
* 必要对象是否可观测。

在自动化系统中，这些内容通常体现在 I/O 配置、变量定义、通信映射和设备参数中；在软件系统中，可以表现为 Schema、Contract、Configuration、Dependency Definition 或 Permission Mapping。

### 2.2 D：Dynamics

D 用于判断当前取得的状态是否仍具有本次 Target State Entry 的判定效力。

典型检查内容包括：

* 是否超时；
* 是否长时间未刷新；
* 是否发生抖动；
* 是否存在冲突或不同步；
* 许可是否已经撤销；
* 缓存或 Token 是否已经过期；
* 对象版本是否已经变化。

相关实现可采用 Timer、Timeout、Timestamp、Heartbeat、Debounce、Freshness、Version Check、Synchronization 等现有机制。

因此：

```text
状态存在 ≠ 状态当前有效
```

### 2.3 B：Boundary

B 用于判断当前有效状态是否处于本次迁移预先定义的工程边界内。

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

例如，某尺寸允许范围为：

```text
19.90 mm ～ 20.10 mm
```

则：

```text
20.06 mm → 在界内
20.18 mm → 超出边界
```

B 判断状态与预定义边界之间的位置关系。等待、回流、人工确认、安全锁定等属于后续控制动作，不属于 B 本身。

S、D、B 是三类验证性质，不要求 Runtime 必须严格按照 S → D → B 的固定顺序依次执行。实际 Runtime 可以根据规则采用短路或其他执行方式，具体实现方式不改变 S/D/B 的定义。

---

## 3. CAE 与 SDB 的组合关系

CAE 与 SDB 分别描述状态迁移中的功能角色和验证性质。

以视觉结果过期为例。如果视觉结果用于证明当前工件满足抓取条件，则该状态在本次迁移中的功能角色属于 C；如果该结果已经失去时间有效性，则需要进行 D 判定，并可形成：

```text
C-D
```

C-D 表示本次目标状态进入所依赖的条件状态在动态时序有效性方面存在判定结果。

同类组合还包括：

```text
A-D：本次迁移所需的许可状态发生动态失效

E-B：本次迁移所依赖的执行链状态达到预定义承接边界

C-S：本次迁移所需的条件状态缺少必要结构定义或接入
```

因此：

```text
CAE：说明状态为什么参与本次迁移

SDB：说明状态需要从哪一种验证性质进行判定
```

CAE-SDB 不是设备分类表，也不是将现场信号静态划分为九种固定标签。其判定对象是一次明确 Target State Entry 前，与本次状态迁移有关的状态关系。

---

## 4. PCN 对现有工程机制的组织

CAE-SDB 所使用的底层判断，大部分已经存在于现有工程系统中。

在 PLC 或自动化控制系统中，典型机制包括：

```text
S：信号定义、接口映射、配置检查

D：去抖、超时、时间窗、心跳、稳定性判断

B：上下限、范围、阈值、允许窗口
```

在业务系统或后端服务中，典型机制包括：

```text
S：Schema、Contract、Dependency、Permission Mapping

D：TTL、Timeout、Heartbeat、Version、Freshness

B：Rate Limit、Quota、Amount Limit、Capacity、Retry Limit
```

因此，PCN 不需要重新实现定时器、比较指令、接口检查或范围判断等底层机制。

PCN 需要明确以下工程关系：

```text
本次 Target State Entry 是什么？

哪些状态与本次迁移有关？

这些状态分别承担什么 C / A / E 角色？

需要进行哪些 S / D / B 验证？

多个判定结果之间如何进行 Arbitration？

当前 Target State Entry 允许哪些 Multipath Control？

本次判定和控制依据是什么？

相关结果如何形成 Trace？
```

其基本处理关系为：

```text
Current State
     ↓
Target State
     ↓
Target State Entry / PCN
     ↓
CAE Mapping
     ↓
SDB Evaluation
     ↓
CAE-SDB Result
     ↓
Arbitration
     ↓
Multipath Control
     ↓
PCN Trace
```

PCN 的工程作用，是围绕明确的状态迁移入口，对原本分散在不同程序、设备和系统中的判断机制进行组织，并将判定结果、控制结果及其依据形成可追溯的工程履历。

这些判断机制本身大多来自成熟工程实践。PCN 所增加的是面向 Target State Entry 的统一组织关系。

---

## 5. CAE-SDB 的适用对象

PLC 是 CAE-SDB 较容易落地的工程对象之一，但不是其适用边界。

具备以下条件的系统，可以作为 TPCA / PCN 的候选对象：

```text
明确的 Current State

明确的 Target State Entry

可观测的迁移相关状态

进入目标状态前的判定需求

可以定义的后续控制路径
```

### 5.1 自动化执行单元

例如：

```text
Waiting Stage → Pick Stage

C：目标存在、位姿成立

A：安全许可、区域许可、上位放行

E：机器人、夹爪、下游承接、异常路径
```

### 5.2 业务系统

例如：

```text
订单待提交 → 正式提交

C：参数完整、业务对象存在、前序流程完成

A：用户权限、审批、预算许可

E：数据库可写、库存服务可承接、消息可发布
```

### 5.3 API 或 AI 工具调用

例如：

```text
C：请求目标明确、参数完整、必要上下文存在

A：联网、知识库、工具和租户授权成立

E：模型、工具链、目标 API 和返回链路可用
```

不同领域可以采用各自已有的 S/D/B 验证机制。

CAE-SDB 描述的是面向明确 Target State Entry 的状态功能角色组织与状态验证结构，不限定具体控制器类型。

---

## 6. CAE-SDB Result、控制仲裁与 PCN Trace

CAE-SDB Evaluation 输出结构化判定结果，不直接等同于最终控制动作。

其关系为：

```text
CAE-SDB Result
        ↓
   Arbitration
        ↓
 Multipath Control
        ↓
    PCN Trace
```

一次 Target State Entry 可能同时产生多个判定结果。Arbitration 根据关键许可、安全约束、控制优先级、边界规则和合法候选路径形成最终控制结果。

代表性的 Multipath Control 包括：

```text
允许进入
等待
重识别
重采样
重试
回流
下游协调
资源释放
降级
人工确认
禁止进入
安全锁定
异常隔离
```

CAE-SDB Result 与控制动作之间不存在固定的一一对应关系。

例如：

```text
C-D ≠ WAIT

E-B ≠ RETURN

A-S ≠ SAFETY LOCK
```

CAE-SDB Result 记录本次前置判定中状态所对应的功能角色及验证性质；Multipath Control 表示经过控制仲裁后实际采用的控制路径。

PCN Trace 用于记录本次 Current State、Target State、参与判断的状态、CAE Mapping、SDB Evaluation、Arbitration Result、Multipath Control、时间信息和执行结果。

这些记录可用于现场排查、工程交接、规则审查、版本比较和后续改善。

---

## 7. 当前边界

CAE-SDB 是当前 TPCA / PCN 用于 Target State Entry 前置判定的工程结构。

现阶段不主张已经通过数学方法证明 C/A/E 或 S/D/B 在所有工程系统中不存在扩展空间。

后续验证可以继续检查以下两类问题：

```text
是否存在 C / A / E 之外，
同时又是明确 Target State Entry 不可缺少的第四种独立迁移功能角色？

是否存在 S / D / B 之外，
同时又是参与本次迁移判定状态不可缺少的第四种独立验证性质？
```

如果在跨行业、跨设备或跨系统验证中持续出现现有结构无法自然表达的对象，应作为新的理论问题处理。

现阶段主要验证以下三个方面：

```text
CAE 是否能够稳定组织 Target State Entry 所需的迁移功能角色；

SDB 是否能够稳定组织各领域已有的状态验证逻辑；

二者组合后是否能够持续支撑 Arbitration、Multipath Control 和 Trace。
```

---

## 参考文献与外部依据

以下资料用于说明状态建模、工业状态值及时间信息、复杂系统事件顺序等已有工程基础。

这些资料用于提供相邻工程背景，不表示既有框架与 CAE-SDB 存在一一对应关系，也不用于证明 CAE-SDB 的完备性。

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

题目：为什么是 CAE-SDB？——状态迁移功能角色与状态验证的双轴结构

文档类型：技术札记

版本：Public Note Version 1.1

首次发布日期：2026-08-25

最后更新：2026-08-26

作者：全野南政 / Nansei Zenno

当前 URL：https://zennns.com/zh/notes/why-cae-sdb/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
