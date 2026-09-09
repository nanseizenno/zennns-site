---
title: "多个 PCN 如何形成状态迁移前置控制网络？"
summary: "说明多个 Target State Entry 及其对应的 PCN，如何通过状态迁移、许可、资源、执行和状态更新等依赖关系形成 PCN Network。"
description: "说明 PCN Network 的定义、PCN 之间的工程依赖关系、Runtime、PCN Trace 的分析价值以及代表性应用形态。"
date: 2026-07-04
lastmod: 2026-09-09
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.4"
citation_url: "https://zennns.com/zh/notes/pcn-network-structure/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## 多个 PCN 如何形成状态迁移前置控制网络？

一个 PCN（Pre-Control Node / 前置控制节点）对应一个明确的 Target State Entry。

复杂工程系统中通常同时存在多个 Target State Entry。这些入口可能连续发生，也可能并行、分支、循环，或者相互依赖。将各 Target State Entry 对应的 PCN 按实际状态迁移关系和工程依赖关系连接起来，就形成 PCN Network。

PCN Network 可以定义为：

> **由多个 Target State Entry、对应的 PCN，以及它们之间的状态迁移、许可、资源、执行和状态更新等依赖关系构成的工程关系结构。**

基础概念可参见：

- [Concepts｜核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)

---

## 1. PCN Network 的节点是 Target State Entry / PCN

PCN Network 的节点对象，不是设备本身，也不是控制器本身，而是具有独立设计、判定、控制和记录价值的 Target State Entry。

例如：

| 状态迁移 | 对应 PCN |
|---|---|
| 机器人等待 → 抓取阶段 | 抓取前 PCN |
| 放置完成 → 压装阶段 | 压装前 PCN |
| 待检测 → 检测阶段 | 检测前 PCN |
| 任务已生成 → 执行状态 | 任务执行前 PCN |
| AGV 到站 → 站点接收状态 | 站点接收前 PCN |
| 保全解除 → 自动运行恢复 | 自动运行恢复前 PCN |

设备、PLC、机器人控制器、MES、WCS、质量系统等负责提供各 PCN 判定所需的状态。PCN 的设置单位由 Target State Entry 的位置决定，而不是由设备数量或控制器数量决定。

因此，一台复杂设备内部可以有多个 PCN，一条生产线也可以围绕多个关键入口配置 PCN。跨 MES / WCS 与现场设备的状态迁移、包含人工确认或质量放行的状态迁移，只要存在明确的 Target State Entry，同样可以纳入 PCN Network。

---

## 2. PCN 之间通过哪些工程关系连接

PCN Network 中的连接关系来自实际状态迁移和工程依赖。常见关系包括状态推进、许可依赖、资源依赖、执行依赖和状态更新依赖。

### 2.1 状态推进关系

一个状态迁移完成后，系统形成新的 Current State，并由该状态继续进入后续 Target State Entry。

例如：

```text
等待抓取
→ 抓取前 PCN
→ 抓取完成

抓取完成
→ 放置前 PCN
→ 放置完成

放置完成
→ 后续阶段 PCN
→ 后续执行
```

这里的每个 PCN 都对应不同的 Target State Entry。前一个迁移完成后形成新的状态事实，后一个 PCN 再基于新的 Current State 进行判定。

### 2.2 许可依赖关系

某个 PCN 使用的许可状态，可能来自其他设备、上位系统、人员操作或前序状态迁移结果。

例如，质量放行、区域进入许可、上位系统执行许可、对方设备接收许可、人工确认等，都可以成为相应 PCN 中与 A：Authority 有关的状态。

这些许可不一定由当前 PCN 所在设备产生，但会直接影响当前 Target State Entry 是否能够进入。

### 2.3 资源依赖关系

多个 PCN 可能同时依赖同一个共享资源，例如共享路径、缓存区、自动门、电梯、工装、站点或共享执行机构。

这类资源的状态可能同时影响多个 Target State Entry，因此不能只从单个 PCN 的局部状态理解。PCN Network 用于表示这些入口之间通过共享资源形成的依赖关系。

### 2.4 执行依赖关系

进入 Target State 之后，执行链是否能够继续，可能依赖其他设备、路径或下游系统。

例如，下游设备是否能够接收、代替路径是否可用、异常处理路径是否可用、结果发送链路是否正常、后续工序是否能够接续等，都可以成为相应 PCN 中与 E：Execution Chain 有关的状态。

这里仍然需要绑定当前 Target State Entry。某条替代路径或异常处理路径是否可用，应作为其对应候选目标路径的判定依据，不能反向证明当前 Target State 的 E 已经成立。

### 2.5 状态更新依赖关系

某个 PCN 的执行结果或状态变化，可能需要写回 PLC、MES、WCS、质量系统或其他上位系统。更新后的状态又可能成为后续 PCN 的输入。

例如：

```text
工序完成
→ MES / PLC / WCS 状态更新
→ 后续 PCN 获取更新后的状态
→ 判定下一个 Target State Entry
```

状态更新依赖描述的是后续 PCN 使用状态的来源和更新关系，也是 PCN Network 中的重要连接关系。

---

## 3. PCN Network 可以形成不同结构

PCN Network 的结构取决于实际状态迁移和依赖关系，可以是连续、并行、分支、循环、相互依赖，也可以跨越多个系统层级。

连续关系可以表示为：

```text
PCN-A
→ State Transition
→ PCN-B
→ State Transition
→ PCN-C
```

并行或分支关系则可能由同一个前序状态进入不同的 Target State Entry。

```text
          → PCN-B
PCN-A
          → PCN-C
```

状态类型本身也可以形成循环。例如：

```text
A → B → C → A
```

但实际运行中的状态实例不会返回到过去。再次进入状态类型 A 时，会形成新的 State Instance：

```text
A₁ → B₁ → C₁ → A₂
```

A₁ 与 A₂ 属于同一 State Type，但属于不同的运行实例。返工、回流、恢复、重新投入等工艺路径可以形成状态类型上的循环，但运行履历仍然沿时间方向继续生成。

关于这一点，可参见：

- [TPCA 的状态迁移单向性——为什么真实工程系统不存在状态回退？](/zh/notes/tpca-unidirectional-state-transition/)

PCN Network 也可以跨越 PLC、机器人、MES、WCS、质量系统等不同系统。这里关注的不是 PCN 部署在哪台设备上，而是系统中有哪些 Target State Entry，以及这些入口之间存在什么工程关系。

---

## 4. PCN Network 与 Runtime

每个 PCN 都在自己的 Target State Entry 上获取相关状态，并完成在线判定和控制。PCN Runtime 用于支撑单个 PCN 的在线运行。

PCN Network 则位于更上层，描述多个 Target State Entry / PCN 之间的状态迁移和依赖关系。

因此，不同 PCN 可以部署在不同位置，例如 PLC / HMI、工业控制器、边缘控制器、WCS、MES 或软件服务。各 PCN 的 Runtime 根据具体对象和平台进行实现，Network 只要求这些节点之间的状态推进、许可、资源、执行和状态更新关系能够被明确。

Runtime 的内部生命周期、PCN 间通信协议、同步方式、完整接口定义以及完整 Arbitration 规则属于工程实现内容，本公开札记不展开。

---

## 5. PCN Network 与 PCN Trace

单个 PCN 会形成一次 Target State Entry 对应的 PCN Trace，其中记录本次状态迁移使用的状态、判定结果、控制结果和执行结果。

当多个 PCN 的 Trace 与 Network 中的依赖关系对应起来后，就可以分析单个入口之外的系统级问题。

例如：

```text
PCN-A
许可更新延迟
    ↓
PCN-B
Wait 时间延长
```

也可能出现：

```text
PCN-C
占用共享资源
    ↓
PCN-D / PCN-E
在 Target State Entry 等待
```

这类问题如果只看单个 PCN，通常只能看到“当前入口在等待”。结合 PCN Network 后，可以进一步判断等待是否来自前序许可更新、共享资源占用、执行链依赖或状态更新延迟。

长期积累后，可以分析哪些 Target State Entry 问题频发、哪些 PCN 之间反复出现许可依赖、哪些共享资源持续影响多个入口、哪些状态更新关系经常出现延迟，以及工程修改以后相关 PCN 的判定和执行结果发生了什么变化。

因此，PCN Network 为 PCN Trace 补充了节点之间的关系信息，使履历分析能够从单个 Target State Entry 扩展到系统级依赖关系。

PCN Trace 的详细说明参见：

- [为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)

---

## 6. 三种代表性的 PCN Network 形态

### 6.1 自动化执行单元

一个自动化执行单元内部可以有多个主要 Target State Entry。

例如：

```text
等待
→ 抓取前 PCN
→ 抓取

抓取完成
→ 放置前 PCN
→ 放置

放置完成
→ 后续阶段 PCN
→ 后续执行
```

这类 Network 中，PCN 之间主要体现状态推进、许可和执行链依赖。

### 6.2 MES / WCS 与多设备协同

MES / WCS 与多设备协同时，Target State Entry 往往跨系统存在。

例如：

```text
任务生成
→ 任务执行前 PCN
→ 执行

到达站点
→ 站点接收前 PCN
→ 交接

执行完成
→ 状态更新
→ 后续 PCN
```

任务、资源、路径、站点、许可、Execution Chain 和状态更新之间的关系，都可以在 PCN Network 中进行整理。

### 6.3 生产 DX 与跨系统状态迁移

设备、人员、MES、质量系统和保全系统之间也存在大量明确的状态迁移入口。

例如：

```text
质量确认
→ 下一工序前 PCN
→ 工序进入

保全解除
→ 自动运行恢复前 PCN
→ 运行恢复

作业指示切换
→ 目标生产状态前 PCN
→ 新生产状态
```

这类场景的特点是状态和许可来源分散在多个系统，但每次状态迁移仍然可以围绕明确的 Target State Entry 进行组织。

---

## 总结

一个 PCN 对应一个明确的 Target State Entry。

多个 PCN 按实际状态迁移关系以及许可、资源、执行和状态更新等工程依赖连接后，形成 PCN Network。

PCN Network 主要处理以下关系：

```text
状态推进
许可依赖
资源依赖
执行依赖
状态更新依赖
```

它可以形成连续、并行、分支、循环以及跨系统结构。各 PCN Runtime 负责自己的在线判定和控制，PCN Network 负责描述多个 Target State Entry 之间的关系。

当 PCN Trace 与 Network 关系结合后，可以进一步分析多个入口之间的问题传递、共享资源影响、许可依赖和状态更新影响。

因此，PCN Network 可以看作：

> **将多个 Target State Entry 分别定义为 PCN，并按实际状态迁移和工程依赖关系连接起来，用于系统级设计、确认和分析的关系结构。**

---

## 相关技术札记

- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)
- [TPCA 的状态迁移单向性——为什么真实工程系统不存在状态回退？](/zh/notes/tpca-unidirectional-state-transition/)
- [为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)
- [TPCA / PCN 适用场景分析](/zh/notes/tpca-pcn-applicable-scenarios/)

---

## 文档信息

题目：多个 PCN 如何形成状态迁移前置控制网络？  
文档类型：技术札记  
版本：Public Note Version 1.4  
首次发布日期：2026-07-04  
最后更新：2026-09-09  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/pcn-network-structure/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
