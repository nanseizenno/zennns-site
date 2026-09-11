---
title: "TPCA / PCN 状态迁移前置控制架构"
summary: "将明确的 Target State Entry（目标状态入口）作为可独立设计、判定、控制和记录的工程对象，并通过 PCN 将状态迁移前判定、控制仲裁、多路径控制和 PCN Trace 组织为一套连续的工程结构。"
description: "介绍 TPCA 状态迁移前置控制架构及其工程节点 PCN。围绕明确的 Target State Entry，将相关状态整理到 C / A / E 状态变量域，并从 S / D / B 判定性质形成 CAE-SDB 判定结果；进一步连接控制仲裁、多路径控制、PCN Trace 和 PCN Network。"
date: 2026-07-01
lastmod: 2026-09-09
author: "全野南政 / Nansei Zenno"
document_type: "公开白皮书"
version: "Public Version 1.5"
citation_title: "TPCA / PCN 状态迁移前置控制架构"
citation_url: "https://zennns.com/zh/whitepaper/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## 概要

TPCA / PCN 的核心命题是：

> **明确的 Target State Entry（目标状态入口），应当作为可以独立设计、判定、控制和记录的工程对象。**

**TPCA（Transition Pre-Control Architecture，状态迁移前置控制架构）** 是状态迁移前置控制的总体架构。

**PCN（Pre-Control Node，前置控制节点）** 设置在明确的 Target State Entry 之前，将该入口对应的判定、控制和履历作为一个工程单元进行组织。

基本工程关系如下：

```text
① Current State
   （当前状态 / 当前阶段 / 当前路径位置）
   ↓
② 明确 Target State
   （目标状态 / 目标执行路径 / 目标物理执行阶段）
   以及 Target State Entry（目标状态入口）
   ↓
③ PCN（Pre-Control Node，前置控制节点）
   └─ 获取相关状态，
      完成 C / A / E 状态映射
   ↓
④ S / D / B 判定
   → CAE-SDB Matrix
   → CAE-SDB Result（CAE-SDB 判定结果） + T
   ↓
⑤ Arbitration（控制仲裁）
   ↓
⑥ Multipath Control（多路径控制）
   ↓
⑦ 形成当前 Target State Entry 的控制结果
   ├─ 允许进入
   ├─ 等待 / 再确认 / 重试
   ├─ 选择其他 Target State
   │  （目标状态 / 目标执行路径 / 目标物理执行阶段）
   └─ 禁止进入等
   ↓
⑧ 执行选定的控制路径
   → 进入 Target State
   → 等待 / 再确认 / 重试
   → 禁止进入等
   → 形成执行结果
   ↓
⑨ PCN Trace（状态迁移判定履历）
   → 关联记录输入、判定、控制和执行结果
```

C / A / E 用于整理相关状态在本次状态迁移中的工程作用，构成三个状态变量域。

S / D / B 用于从结构完整性、动态时序有效性和控制边界三个方面对相关状态进行判定，并与 C / A / E 组合形成 CAE-SDB Matrix。

PCN 形成 CAE-SDB 判定结果后，将重要许可和控制约束一并纳入 Arbitration，处理当前 Target State Entry 的控制优先关系，并据此形成 Multipath Control。

判定、控制和执行结果记录为 PCN Trace。

多个 PCN 还可以按照实际状态迁移关系，以及许可、资源、执行和状态更新等依赖关系连接，形成 PCN Network（PCN 网络）。

---

# 第 1 章 工程问题

复杂制造和自动化系统中，PLC、机器人、视觉系统、安全系统、MES / WCS、HMI 等往往已经拥有各自的状态信息，但系统仍可能无法进入下一状态或下一执行阶段。

常见情况包括：

- 机器人已经 Ready（就绪），但抓取没有开始；
- 任务已经存在，但没有进入执行；
- 上游工序已经完成，下游暂时无法接收；
- 单体设备没有明确故障，但 Waiting（等待）持续存在；
- 多个系统都有状态记录，却难以说明究竟是哪一项状态影响了当前状态迁移。

遇到这类问题时，首先需要明确：

```text
Current State（当前状态）
    ↓
Target State Entry（目标状态入口）
    ↓
Target State（目标状态）
```

然后再把与本次 Target State Entry 直接相关的状态放到同一状态迁移上下文中进行确认。

TPCA / PCN 以 Target State Entry 为中心，把原本分散在不同系统中的状态、判定、控制和履历整理为一个明确的工程对象。

![复杂工程系统中的共通状态迁移问题](/images/tpca/01-common-state-transition-problem.png)

图1：多个现场问题可能集中出现在系统准备进入 Target State 之前的 Target State Entry。

详细问题可参见：

[工程问题](/zh/questions/) 从自动化执行单元、多系统协同和状态迁移设计三个方向，对“为什么系统不能进入下一状态”进行整理。

---

# 第 2 章 TPCA / PCN 的基本架构

## 2.1 TPCA 与 PCN

TPCA 面向 Target State（目标状态、目标执行路径或目标物理执行阶段）进入之前的判定与控制。

典型 Target State 可以包括：

- 机器人抓取、放置、检测等物理执行阶段；
- 压装、搬送交接、分流等工艺阶段；
- MES / WCS 中的任务执行路径；
- AGV / AMR 群控中的协同执行状态；
- 制造 DX 中跨系统的重要状态切换；
- 数字系统中的明确执行路径。

一个 PCN 对应一个明确的 Target State Entry。

PCN 获取与该入口直接相关的状态，完成 CAE-SDB 结构化判定、控制仲裁、多路径控制以及 PCN Trace 记录。

基本层级如下：

```text
TPCA
→ PCN
→ CAE-SDB
→ Arbitration（控制仲裁）
→ Multipath Control（多路径控制）
→ PCN Trace
```

| 要素 | 作用 |
|---|---|
| TPCA | 状态迁移前置控制的总体架构 |
| PCN | 对应一个明确 Target State Entry 的前置控制节点 |
| CAE-SDB | PCN 内部的结构化判定逻辑 |
| Arbitration（控制仲裁） | 处理多个判定结果、重要许可和控制约束之间的优先关系 |
| Multipath Control（多路径控制） | 形成当前 Target State Entry 对应的控制路径 |
| PCN Trace | 记录一次 Target State Entry 的判定、控制和执行履历 |

## 2.2 基本工程链

概要中的 ①～⑨ 可以进一步整理为下表。

| 工程位置 | 工程对象 | 主要处理 | 主要结果 |
|---|---|---|---|
| 1 | **Current State（当前状态 / 当前阶段 / 当前路径位置）** | 确认本次状态迁移的起点 | 明确当前状态 |
| 2 | **Target State / Target State Entry** | 明确准备进入的目标状态及对应入口 | 确定本次判定对象 |
| 3 | **PCN** | 获取相关状态并映射到 C / A / E | 整理状态变量域 |
| 4 | **PCN 内部判定** | 对 C / A / E 状态变量域执行当前入口所需的 S / D / B 判定，并将结果整理到 CAE-SDB Matrix | CAE-SDB Result + T |
| 5 | **PCN 内部控制判断** | 结合判定结果、重要许可和控制约束进行 Arbitration | 明确控制优先关系 |
| 6 | **PCN 控制输出** | 根据仲裁结果形成 Multipath Control | 允许、等待、再确认、其他路径、禁止等 |
| 7 | **Target State Entry 控制结果** | 确定当前入口的后续处理 | 明确下一控制或执行方向 |
| 8 | **选定控制路径** | 执行已经确定的状态、路径或处理 | 形成执行结果 |
| 9 | **PCN Trace** | 将输入状态、判定、控制、执行结果和时间信息 T 关联记录 | 形成状态迁移判定履历 |

![TPCA 的基本处理链](/images/tpca/02-tpca-process-chain.png)

图2：PCN 位于 Target State Entry 之前，将相关状态连接到结构化判定、控制仲裁、多路径控制和 PCN Trace。

因此，现场不仅可以看到 Ready / Not Ready、OK / NG、Waiting / Blocked 等结果，还可以继续确认：

- 结果发生在哪个状态变量域；
- 对应哪一类判定性质；
- 最终选择了哪条控制路径；
- 执行以后实际形成了什么结果。

## 2.3 状态类型与状态实例

TPCA / PCN 区分 State Type（状态类型）与实际运行中形成的 State Instance（状态实例）。

状态类型之间可以存在循环：

```text
A → B → A
```

实际运行履历则表现为：

```text
A₁ → B₁ → A₂
```

`A₁` 和 `A₂` 可以属于同一个状态类型 A，但由于发生时间和运行履历不同，属于两个不同的状态实例。

> **状态类型可以循环，实际运行中的状态实例沿时间方向持续生成。**

Recovery（恢复）、Rollback（回退）、Reset（复位）、Retry（重试）、Re-entry（重新进入）等处理，也按照进入新的状态实例来理解。

详细说明参见：

[TPCA 中状态实例的单向性——状态类型循环与实际运行履历的区别](/zh/notes/tpca-unidirectional-state-transition/)

---

# 第 3 章 PCN：状态迁移前置控制的最小工程节点

## 3.1 PCN 的位置与基本要素

PCN 设置在明确的 Target State Entry 之前：

```text
Current State
    ↓
PCN
［针对 Target State Entry 的前置判定］
    ↓
Target State Entry
    ↓
Target State
```

![PCN 前置控制节点的位置与工作方式](/images/tpca/04-pcn-node-position.png)

图3：PCN 在进入 Target State 之前完成相关状态整理、结构化判定、控制仲裁和控制路径形成。

一个 PCN 至少需要整理以下对象。

| 项目 | 内容 |
|---|---|
| Current State（当前状态 / 当前阶段 / 当前路径位置） | 当前处于什么状态、阶段或路径位置 |
| Target State（目标状态 / 目标执行路径 / 目标物理执行阶段） | 下一步准备进入什么状态或阶段 |
| Target State Entry（目标状态入口） | 本次前置判定对应哪个入口 |
| 相关状态 | 与本次状态迁移直接有关的状态 |
| C / A / E 状态映射 | 各状态在本次迁移中的工程作用 |
| S / D / B 判定 | 对相关状态执行的判定 |
| CAE-SDB Result | 本次形成的结构化判定结果 |
| 时间信息 T | 与状态及判定对应的时间信息 |
| Arbitration | 多个结果和约束之间的控制优先关系 |
| Multipath Control | 经 Arbitration 形成的当前入口控制路径 |
| Target State Entry 控制结果 | 明确本次目标状态入口最终如何处理，例如允许进入、暂不进入或禁止进入 |
| PCN Trace | 输入、判定、控制和执行结果的履历 |

PCN 的输入数量、判定规则和实现规模根据具体系统确定。

其基本责任边界是：

> **把一次 Target State Entry 的输入状态、判定、控制和履历保持在同一工程上下文中。**

详细说明参见：

[为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)

## 3.2 PCN 的配置位置示例

自动化执行单元中，可以在以下入口设置 PCN：

- 等待 → 抓取；
- 放置完成 → 压装；
- 待检测 → 检测执行；
- 搬送等待 → 交接；
- 检测完成 → 正常分流入口，并根据判定结果选择异常分流等其他路径。

MES / WCS 与多设备协同中，可以在以下入口设置 PCN：

- 任务生成完成 → 执行；
- 区域进入；
- 站点接收；
- 共享资源使用；
- 下游交接。

制造 DX 中，可以在以下入口设置 PCN：

- 质量放行后的下一工序进入；
- 保全完成后的自动运行恢复；
- 工单切换后的目标生产状态进入；
- 人工确认后的自动运行恢复。

PCN 的配置位置由 Target State Entry 决定，而不是由设备台数、控制器数量或系统名称决定。

## 3.3 TPCA / PCN 的导入与验证

TPCA / PCN 可以根据项目阶段逐步导入。

### 非介入评价 / PoC

利用历史日志、准实时状态或导出数据，验证按 Target State Entry 进行结构化判定和履历组织是否有效。

### 结构化显示

把判定结果显示到 HMI、MES / WCS 页面或事件报告中，支持现场按 Target State Entry 查看状态。

### 控制建议

根据判定结果与 Arbitration，向工程师或上位系统提供建议控制路径。

### 工程嵌入

在满足安全要求、控制规范和验证要求的前提下，将 PCN 的判定和控制逻辑嵌入 PLC / HMI、WCS、边缘控制器或软件平台。

---

# 第 4 章 CAE-SDB：状态变量域与判定性质

## 4.1 双轴结构

CAE-SDB 使用两个不同维度整理 Target State Entry 相关状态。

```text
C / A / E：状态变量域

S / D / B：判定性质
```

C / A / E 表示相关状态在本次状态迁移中的工程作用。

| 状态变量域 | 定义 | 基本问题 |
|---|---|---|
| C = Condition / 条件状态 | 进入 Target State 前需要成立的前提条件 | 需要的条件是否具备 |
| A = Authority / 许可状态 | 是否允许进入 Target State | 当前是否被允许进入 |
| E = Execution Chain / 执行链状态 | 进入 Target State 后所需要的执行链 | 进入以后所需执行链能否继续 |

关键 A：Authority 可以构成 Target State Entry 的独立必要约束。

关键许可未成立时，不允许进入当前 Target State。

E：Execution Chain 不等于单体设备 Ready。它面向当前 Target State 进入后所需要的执行链，例如下游接收、相关资源、结果上传或回写，以及该 Target State 下已经定义的后续执行关系。

S / D / B 是对相关状态执行判定时采用的三类判定性质。

| 判定性质 | 定义 | 基本问题 |
|---|---|---|
| S = Structure / 结构完整性 | 所需信号、接口、映射、许可来源、路径和执行链边界是否已经定义、连接并可观测 | 判定所需结构是否完整 |
| D = Dynamics / 动态时序有效性 | 当前状态是否仍能作为本次 Target State Entry 的有效判定依据 | 这个状态当前还能否使用 |
| B = Boundary / 控制边界 | 当前有效状态是否处于预先定义的允许范围、阈值或控制边界内 | 当前状态是否处于允许边界内 |

D：Dynamics 典型涉及：

- 超时；
- 未更新；
- 期限失效；
- 延迟；
- 不同步；
- 冲突；
- 许可撤销；
- 状态切换；
- 对象或版本不一致。

B：Boundary 典型涉及：

- 尺寸、公差和偏差；
- 温度、压力、流量；
- 识别置信度；
- 位置、姿态、速度；
- 缓冲区容量；
- 资源使用范围；
- 许可范围和时间窗口。

D 与 B 可以这样区分：

```text
D：
这个状态能否作为当前 Target State Entry
此刻有效的判定依据。

B：
这个已经确认有效的状态，
是否处于预先定义的范围或阈值内。
```

例如，前一个工件的视觉识别结果或已经过期的结果属于 D 的判定对象。

当前工件对应的结果仍然有效，但识别置信度或位置偏差已经超出设定范围，则属于 B 的判定对象。

## 4.2 CAE-SDB 组合

C / A / E 与 S / D / B 组合后，可以形成以下判定坐标。

| 状态变量域 | S：结构完整性 | D：动态时序有效性 | B：控制边界 |
|---|---|---|---|
| C：条件状态 | C-S | C-D | C-B |
| A：许可状态 | A-S | A-D | A-B |
| E：执行链状态 | E-S | E-D | E-B |

![CAE-SDB 双轴判定结构](/images/tpca/03-cae-sdb-matrix.png)

图4：C / A / E 表示状态变量域，S / D / B 表示判定性质，两个维度组合后形成 CAE-SDB 判定结果。

例如：

```text
C-D：
视觉识别结果已经过期

A-D：
许可已经撤销

E-D：
下游状态长时间未更新
```

同一个 D：Dynamics 可以分别作用于不同状态变量域。

这样，即使不同设备和系统使用的信号名、接口和实现方式不同，也可以把判定结果整理为统一的 CAE-SDB 形式。

CAE-SDB Result 只有在对应的 S / D / B 判定已经定义、存在判定依据并实际完成后才形成。需要进行某项判定，不等于相应结果已经触发。

> **一次 Target State Entry 不要求形成全部 9 项 CAE-SDB Result。**

详细说明参见：

[为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)

## 4.3 时间信息 T

状态和判定结果需要关联时间信息 T。

T 主要用于：

- 标识状态和判定所处的时间位置；
- 确认状态之间的先后关系；
- 支持 D：Dynamics 判定；
- 形成 PCN Trace。

根据系统实现，可以使用 Timestamp（时间戳）、更新时间、事件时间、序列时间、批次时间等信息。

---

# 第 5 章 控制仲裁、多路径控制、PCN Trace 与 PCN Network

## 5.1 从判定结果到控制

PCN 内部把 CAE-SDB 判定结果连接到控制：

```text
CAE-SDB Result + T
→ Arbitration（控制仲裁）
→ Multipath Control（多路径控制）
→ Target State Entry 控制结果
→ 选定控制路径的执行
→ Execution Result（执行结果）
→ PCN Trace
```

一次 Target State Entry 中，可能同时形成多个 CAE-SDB Result。

例如：

```text
C-D
A-B
E-D
```

Arbitration 需要结合：

- CAE-SDB Result；
- 关键 Authority；
- 安全约束；
- 预先定义的控制规则；
- 当前入口允许选择的控制路径。

在当前 Target State Entry 所要求的相关状态判定、关键许可和其他上位约束满足时，可以形成允许进入当前 Target State 的控制结果。

如果进入要求未成立，则根据 Arbitration 结果进入对应的后续控制路径。

## 5.2 Multipath Control（多路径控制）

代表性的控制路径包括：

- 允许进入；
- 等待；
- 再确认；
- 重新识别；
- 重新采样；
- 重新定位；
- 重试；
- Return（返回）；
- 异常分流；
- 替代路径；
- 下游协调；
- 资源释放；
- 降级执行；
- 人工确认；
- 禁止进入；
- 安全锁定；
- 异常隔离；
- 增强记录。

相同的 CAE-SDB Result，在不同 Target State Entry、安全约束、系统结构和控制规则下，可能对应不同的合法控制路径。

Multipath Control 的作用，是针对当前 Target State Entry 形成下一步应该执行的工程控制处理。

替代路径、回流路径、回退路径等可以作为候选控制路径；如果它们对应其他 Target State 或 Target Path，则应在相应入口下单独判断，不能因为这些路径可用就直接认定当前 Target State 的 E 已经成立。

## 5.3 PCN Trace

PCN Trace 把一次 Target State Entry 的判定、控制和执行结果作为独立的工程数据对象进行记录。

公开范围内可以关联以下内容：

| 项目 | 内容 |
|---|---|
| Current State | 判定时的当前状态 |
| Target State | 本次准备进入的目标状态 |
| Target State Entry | 本次判定对应的目标状态入口 |
| PCN | 承担本次判定的前置控制节点 |
| 相关状态 | 本次判定实际使用的主要状态 |
| 时间信息 T | 状态和判定的时间位置 |
| C / A / E 状态映射 | 各状态在本次迁移中的工程作用 |
| S / D / B 判定 | 对相关状态执行的判定 |
| CAE-SDB Result | 结构化判定结果 |
| Arbitration Result（控制仲裁结果） | 控制优先关系处理结果 |
| Multipath Control | 经 Arbitration 形成的本次控制路径 |
| Target State Entry 控制结果 | 本次目标状态入口最终允许进入、暂不进入、禁止进入等控制结果 |
| Execution Result | 已选控制路径执行后的实际结果 |
| Trace ID | 识别一次判定履历的标识 |

PCN Trace 长期积累后，可以比较：

- 哪些 Target State Entry 反复出现问题；
- 哪些 CAE-SDB Result 高频出现；
- 哪些 Multipath Control 被反复选择；
- 控制选择与实际执行结果之间存在什么关系；
- 工程修改以后这些分布如何变化。

详细说明参见：

[为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)

## 5.4 PCN Network（PCN 网络）

一个 PCN 对应一个 Target State Entry。

复杂系统中存在连续、并行、分支、循环和相互依赖的多个 Target State Entry。

多个 PCN 可以按照状态推进、许可、资源、执行和状态更新等依赖关系连接，形成 PCN Network。

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

PCN Network 表示：

> **多个 Target State Entry，以及这些入口之间的状态迁移和工程依赖关系。**

将各 PCN 的 PCN Trace 与 Network 中的依赖关系对应起来后，可以进一步分析跨入口重复出现的许可、资源、执行和状态更新问题。

详细说明参见：

[多个 PCN 如何形成状态迁移前置控制网络？](/zh/notes/pcn-network-structure/)

---

# 第 6 章 代表性应用方向

![TPCA / PCN 的应用方向](/images/tpca/05-tpca-application-map.png)

图5：TPCA / PCN 可以应用于自动化执行单元、MES / WCS 与多设备协同、制造 DX，以及具有明确执行入口的数字系统。

## 6.1 自动化执行单元

代表对象包括：

- 机器人抓取；
- 压装；
- 检测；
- 搬送交接；
- 上下料；
- 正常分流 / 异常分流。

例如机器人已经 Ready，但视觉结果失效、安全许可未成立、夹爪状态异常或下游无法接收，都可能影响当前 Target State Entry。

PCN 设置在目标物理执行阶段之前，对相关状态进行 CAE-SDB 判定，经 Arbitration 后形成 Multipath Control。

相关案例：

[自动化执行单元前置判定案例](/zh/cases/automation-execution-unit-pre-control/)

## 6.2 MES / WCS 与多设备协同

代表对象包括：

- AGV / AMR 群控；
- 任务执行；
- 共享资源使用；
- 区域进入；
- 站点接收；
- 下游交接。

单个设备没有明显故障时，任务、许可、资源、执行主体和下游状态之间的组合关系仍可能造成 Waiting、Blocked（阻塞）或 Pending（待处理）持续存在。

PCN 可以把这些分散状态对应到明确的 Target State Entry，并形成协同状态迁移的判定、控制和履历。

相关案例：

[MES / WCS 协同停滞诊断模块案例](/zh/cases/collaborative-stagnation-diagnosis/)

## 6.3 制造 DX

制造 DX 中，可以围绕设备数据、生产数据、质量状态、保全状态和人工确认等信息设计跨系统状态迁移。

例如：

- 质量放行后的下一工序进入；
- 工单切换后的目标生产状态进入；
- 保全完成后的自动运行恢复；
- 人工确认后的自动运行恢复；
- 多系统之间的重要工程状态切换。

PCN 将这些分散在设备、系统和人员环节中的状态迁移条件对应到明确 Target State Entry，并组织为判定、控制和 PCN Trace。

相关案例：

[制造 DX 状态迁移条件设计与履历分析案例](/zh/cases/production-dx-state-transition/)

## 6.4 数字调用扩展

TPCA / PCN 也可以应用于具有明确执行入口的数字系统，例如：

- AI 推理调用；
- Tool Call（工具调用）；
- API 执行；
- 外部服务调用；
- 企业知识库访问；
- 高成本模型调用。

在执行入口前，可以对请求条件、权限、执行链等状态进行判断，并根据结果选择高成本路径、补充确认、降级、等待或阻断等处理。

该方向属于 TPCA / PCN 的扩展应用。

适用范围和边界参见：

[TPCA / PCN 适用场景分析](/zh/notes/tpca-pcn-applicable-scenarios/)

---

# 结语

TPCA / PCN 的核心，是把 Target State Entry 作为独立的工程对象进行处理。

PCN 设置在 Target State Entry 之前，将相关状态映射到 C / A / E 状态变量域，并从 S / D / B 判定性质进行结构化判定，形成 CAE-SDB Result。

随后，PCN 通过 Arbitration 处理多个判定结果、重要许可和控制约束之间的优先关系，形成 Multipath Control，并把判定、控制和执行结果记录到 PCN Trace。

一个 PCN 对应一个明确的 Target State Entry。

多个 PCN 按照实际状态迁移和工程依赖关系连接后，可以形成 PCN Network。

TPCA / PCN 因而提供了一种围绕同一状态迁移入口组织状态条件、许可、执行链、控制边界、多路径控制和履历的工程架构。

---

# 相关内容

从现场问题进入：

- [工程问题](/zh/questions/)

查看术语定义：

- [Concepts｜核心概念](/zh/concepts/)

查看专题说明：

- [技术札记](/zh/notes/)

查看代表性应用：

- [应用案例](/zh/cases/)

了解作者及本站定位：

- [关于本站](/zh/about/)

---

# 版本信息

本文为 **TPCA / PCN 状态迁移前置控制架构** 的公开白皮书。

- Public Version 1.0：2026-07-01 发布。
- Public Version 1.1：2026-08-19 更新。明确 CAE-SDB Result、Arbitration、Multipath Control 和 PCN Trace 的层级关系。
- Public Version 1.2：2026-08-20 更新。统一以 Target State Entry 作为可独立设计、判定、控制和记录的工程对象，并进一步明确 TPCA 与 PCN 的架构关系。
- Public Version 1.3：2026-08-21 更新。补充时间信息 T、状态实例、PCN Trace、PCN Network 和 Multipath Control 相关说明。
- Public Version 1.4：2026-08-25 更新。整理 CAE-SDB 的双轴结构。
- Public Version 1.5：2026-09-09 更新。追加九步工程分析顺序，减少重复说明，并统一 Target State Entry、CAE-SDB、Arbitration、Multipath Control、PCN Trace 和 PCN Network 的公开表达。

作者：全野南政 / Nansei Zenno

建议引用：

```text
全野南政 / Nansei Zenno，《TPCA / PCN 状态迁移前置控制架构》，公开白皮书，Public Version 1.5，2026-09-09，https://zennns.com/zh/whitepaper/
```
