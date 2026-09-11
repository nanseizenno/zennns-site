---

title: "MES / WCS 协同停滞诊断模块案例"

summary: "以制造现场协同停滞为对象，按照统一九步工程分析顺序，说明 PCN 如何从 Current State 和 Target State Entry 出发，汇总 MES、WCS、搬送主体、站点、资源、许可和下游状态，完成 C / A / E 状态映射、S / D / B 判定，并结合群控协同层的群体指标、停滞识别与停滞结构分型形成控制与履历。"

description: "公开说明 TPCA / PCN 在 MES / WCS 协同停滞诊断中的应用方式。围绕制造现场进入可持续协同执行状态这一 Target State，按照 Current State、Target State / Target State Entry、PCN、CAE-SDB、群控协同分析、Arbitration、Multipath Control、入口控制结果、Execution Result 和 PCN Trace 的顺序展开完整案例。"

date: 2026-06-30

lastmod: 2026-09-10

author: "全野南政 / Nansei Zenno"

document_type: "公开案例"

case_type: "群控协同层 / MES-WCS 协同停滞诊断"

version: "Public Case Version 1.5"

citation_title: "MES / WCS 协同停滞诊断模块案例：为什么 MES 记录了状态，仍解释不了制造现场为什么停"

citation_url: "https://zennns.com/zh/cases/collaborative-stagnation-diagnosis/"

draft: false

weight: 2

ShowReadingTime: true

ShowToc: true

TocOpen: true

---

## 为什么 MES 记录了状态，仍解释不了制造现场为什么停

> 应用层级：群控协同层 / MES-WCS 协同停滞诊断

> 代表对象：制造现场协同停滞诊断模块

**建议引用：**

```text
全野南政 / Nansei Zenno，《MES / WCS 协同停滞诊断模块案例：为什么 MES 记录了状态，仍解释不了制造现场为什么停》，公开案例，Public Case Version 1.5，2026-09-10，https://zennns.com/zh/cases/collaborative-stagnation-diagnosis/
```

MES 可以记录任务、设备、工位、物料、报警、产量和生产实绩。

WCS 可以记录搬送任务、车辆状态、路径状态、资源占用和调度结果。设备系统可以记录运行、等待、报警和互锁状态，HMI 也可以显示 Ready、Waiting、Blocked、Pending 等运行状态。

在多设备、多任务和多系统协同场景中，仍可能出现以下情况：

- 任务已经生成，但执行持续无法推进；
- 车辆在线，工位存在需求，但补料没有形成连续执行；
- 单体设备没有明显故障，系统整体吞吐却持续下降；
- MES、WCS、PLC、车辆和工位均有状态记录，但协同受阻位置难以快速确认；
- 订单变化、资源竞争、许可等待、下游阻塞、人工确认和能源补给等因素同时影响群体执行。

本案例关注的工程问题是：

> **当前系统为什么无法进入可持续协同执行状态？**

本案例按照统一的九步工程分析顺序展开：

```text
1. Current State

2. Target State / Target State Entry

3. PCN：相关状态获取 + C / A / E Mapping

4. 前置判定与群控协同分析
   ├─ S / D / B Evaluation
   │  → CAE-SDB Result + T
   └─ 群体指标
      → 群体停滞识别
      → 停滞结构分型

5. Arbitration

6. Multipath Control

7. 当前入口控制结果

8. 选定控制路径与 Execution Result

9. PCN Trace
```

通过这 9 个步骤，可以看到：

> **一次“从当前协同状态进入可持续协同执行状态”的请求，如何完成状态整理、前置判定、群体停滞识别、停滞结构分型、控制、执行和记录。**

基础概念可参见：

- [Concepts｜核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

---

## 案例对象

本案例对象为：

> **MES / WCS 协同停滞诊断模块。**

该模块位于制造现场协同层，可连接 MES、WCS、搬送系统、设备单元、站点、缓存、路径资源、许可系统和现场执行对象。

AGV / AMR 群控搬送可以作为代表场景，模块还可以用于无人叉车和自动搬运系统、多设备协同生产、线边补料与缓存调度、工位等待与站点承接、路径资源竞争、区域许可和资源锁协调，以及能源补给集中导致的群体执行能力下降等场景。

本案例在 TPCA / PCN 母框架下保留群控协同层独立的群体指标、群体停滞识别和停滞结构分型，并将其与 CAE-SDB 判定结果共同连接到后续控制仲裁。

![MES / WCS 协同停滞诊断模块示意图](/images/tpca/08-mes-wcs-collaborative-stagnation-module.png)

图：MES / WCS 协同停滞诊断模块位于制造现场协同层，汇总 MES、WCS、AGV / AMR、缓存区、加工设备、路径资源、自动门、电梯、充电区、安全许可系统和监控系统等多源状态。

---

# 1. Current State（当前协同状态）

本案例从制造现场已经存在任务和执行主体，但协同执行持续受阻的状态开始。

Current State 可以整理为：

```text
Current State：

任务存在 + 执行主体在线 + 部分任务持续未执行 + Waiting / Blocked / Pending 持续存在 + 协同执行受阻
```

现场还可能同时看到：

```text
工位有需求
车辆仍可移动
部分路径仍可用
单体设备无重大报警
局部任务仍在执行
```

这些现象只能说明当前协同执行存在受阻状态，还不能在这一步直接认定已经形成群体协同停滞。

本次分析首先明确当前协同状态，以及哪些任务、主体、资源、许可和站点属于同一次协同执行上下文。

后续的状态获取、C / A / E 状态映射、S / D / B 判定、群体指标计算和停滞识别，均以这个 Current State 为本次分析起点。

---

# 2. Target State / Target State Entry（目标状态 / 目标状态入口）

本次准备进入的 Target State 为：

```text
Target State： 可持续协同执行状态
```

对应的 Target State Entry 为：

```text
Target State Entry： 进入可持续协同执行状态
```

该 Target State 表示任务、执行主体、路径、资源、许可、站点、下游和结果回写形成能够持续接续的协同执行关系。

PCN 位于当前协同状态与 Target State Entry 之间：

```text
Current State［协同执行受阻］
    ↓
PCN［针对“进入可持续协同执行状态”的前置判定］
    ↓
Target State Entry［进入可持续协同执行状态］
    ↓
Target State［可持续协同执行状态］
```

本案例后续的 C / A / E、S / D / B、群体停滞识别、停滞结构分型、Arbitration 和 Multipath Control，均绑定这个明确的 Target State Entry。

关于 PCN 与 Target State Entry 的对应关系，可参见：

[为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)

---

# 3. PCN：相关状态获取与 C / A / E 状态映射

协同停滞涉及多个任务、主体、资源和执行对象。

PCN 取得与“进入可持续协同执行状态”直接相关的多源状态。

| 信号来源 | 与本次协同入口有关的状态 |
|---|---|
| MES | 工单、任务、优先级、物料需求、工位需求、计划变更、人工确认、异常记录 |
| WCS / 调度系统 | 任务队列、任务分配结果、任务状态、派单结果、资源锁、路径分配、站点占用、缓存状态 |
| AGV / AMR / 无人叉车 | 在线状态、自动模式、位置、空载 / 负载、电量、任务执行、等待、移动、报警状态 |
| 设备 / 工位 | 可接收状态、运行状态、等待状态、缺料状态、完成状态、报警状态 |
| 路径与设施资源 | 窄通道、交叉口、自动门、电梯、区域通行权、缓存区、装卸点占用状态 |
| 安全与许可系统 | 区域许可、安全许可、上位放行、人工放行、锁定状态 |
| 下游与回写链路 | 下游承接状态、结果回写状态、异常处理状态 |

这些状态根据其在当前 Target State Entry 中承担的工程作用映射到 C / A / E 状态变量域。

```text
C = Condition（条件状态）
A = Authority（许可状态）
E = Execution Chain（执行链状态）
```

本案例可以整理为：

| 状态变量域 | 当前入口中的主要对象 |
|---|---|
| C：Condition | 任务状态、物料需求、工位需求、目标站点信息、订单与工艺条件 |
| A：Authority | 调度许可、资源锁、区域许可、安全许可、人工确认、上位放行 |
| E：Execution Chain | 执行主体状态、路径通行状态、站点承接状态、缓存状态、下游接续状态、结果回写状态 |

例如：

```text
任务状态 → C
区域许可 → A
站点承接状态 → E
```

同一个主体在线、同一个任务存在或某个设备 Ready，都只构成本次 Target State Entry 的相关状态之一。

当前协同执行是否能够持续，还需要结合其他 Condition、Authority 和 Execution Chain 状态进行判定。

能源补给状态、群体未执行比例等群体层信息在本案例中进入群控协同分析过程。只有在具体 PCN 已明确定义其 C / A / E 角色并配置相应 S / D / B 规则时，才形成对应的 CAE-SDB Result。

---

# 4. 前置判定与群控协同分析

完成相关状态获取和 C / A / E 状态映射后，本案例在同一个 Target State Entry 下进行两类处理：

```text
A. S / D / B Evaluation
   → CAE-SDB Result + T

B. 群控协同分析
   → 群体指标
   → 群体停滞识别
   → 停滞结构分型
```

CAE-SDB Result 与群体停滞识别、停滞结构分型分别形成，并共同作为后续 Arbitration 的输入。

---

## 4.1 S / D / B Evaluation

PCN 对当前 Target State Entry 所需要的相关状态执行 S / D / B 判定。

```text
S = Structure（结构完整性）
D = Dynamics（动态时序有效性）
B = Boundary（控制边界）
```

本案例中的典型判定包括：

| 判定性质 | 典型确认内容 |
|---|---|
| S：Structure | 相关任务、主体、资源、许可、站点、下游和回写状态所需的接口、映射、来源及对象关系是否已经定义、接入并可观测 |
| D：Dynamics | 当前状态是否仍可作为本次协同入口的有效判定依据，包括工单与任务同步、主体位置刷新、许可撤销、资源锁更新、站点状态刷新、路径状态同步和执行反馈时序 |
| B：Boundary | 当前有效状态的数值或范围是否处于预先定义的等待时间、资源占用时间、站点容量、许可时间窗、资源使用范围、重试次数等允许边界内 |

C / A / E 状态变量域与 S / D / B 判定性质组合后，可以形成 9 个 CAE-SDB 判定坐标。

```text
                 S                   D                   B
        ┌────────────────┬────────────────┬────────────────┐
C       │      C-S       │      C-D       │      C-B       │
        ├────────────────┼────────────────┼────────────────┤
A       │      A-S       │      A-D       │      A-B       │
        ├────────────────┼────────────────┼────────────────┤
E       │      E-S       │      E-D       │      E-B       │
        └────────────────┴────────────────┴────────────────┘
```

在本案例中，可以按照当前“进入可持续协同执行状态”这一 Target State Entry，将代表性的工程问题展开如下。

| 判定坐标 | 本案例中的代表性工程问题 |
|---|---|
| C-S | MES 与 WCS 的任务映射未建立；任务与对象、工位、目标站点或工艺条件之间的关系未完整定义；当前入口所需任务字段或对象关系无法取得 |
| C-D | 工单变更未同步到当前任务；任务状态长时间未刷新；工位需求或目标站点信息已经过期；当前任务与实际执行对象发生切换不同步 |
| C-B | 当前有效任务的等待时间超出允许范围；任务优先级、需求时间窗或计划偏差超出当前入口预定义边界 |
| A-S | 调度许可、资源锁、区域许可、安全许可、人工确认或上位放行的来源未定义；许可接口或映射关系未建立；关键许可状态无法由当前 PCN 取得 |
| A-D | 许可状态长时间未刷新；许可在当前入口判定期间被撤销；资源锁状态不同步；区域许可或人工确认发生更新延迟或失效 |
| A-B | 当前有效许可超出允许适用范围；许可有效时间窗不满足当前入口要求；资源锁占用时间或许可使用范围达到预定义边界 |
| E-S | 当前协同执行所要求的执行主体状态、路径资源关系、站点承接接口、缓存接口、下游接续或结果回写链路未完整定义或未接入 |
| E-D | 执行主体位置或任务执行状态未刷新；路径资源状态不同步；站点承接状态延迟或失效；下游状态未刷新；执行反馈或结果回写超时 |
| E-B | 当前有效的路径容量、站点容量、缓存容量、下游承接能力、执行等待时间或其他当前执行链参数超出预定义允许范围 |

这 9 个坐标用于组织当前 Target State Entry 中可能出现的状态判定问题。

> **每一次运行不要求形成全部 9 项 CAE-SDB Result。**

只有当前入口已经定义相应判定规则、存在可用判定依据，并且实际完成 Evaluation 后，才形成对应的 CAE-SDB Result。

例如：

```text
资源锁接口已经建立
但资源锁状态长时间未刷新
```

如果该资源锁状态在当前入口映射到 A，并且相应 D 判定已经定义并实际完成，可以形成：

```text
A-D：
资源锁状态无法继续作为
当前协同入口的有效许可依据
```

又例如：

```text
下游站点状态仍显示 Available
但该状态长时间未刷新
```

如果该状态映射到当前入口的 E，并且相应 D 判定已经定义并实际完成，可以形成：

```text
E-D：
下游承接状态无法继续作为
当前协同入口的有效执行链依据
```

再例如：

```text
站点承接状态当前有效
但站点容量已经达到
当前入口预定义的允许上限
```

如果该状态映射到当前入口的 E，并且相应 B 判定已经定义并实际完成，可以形成：

```text
E-B：
当前有效的站点承接能力
达到本次协同入口的预定义控制边界
```

> **需要执行某项 S / D / B 判定，表示该判定属于当前入口的评价规则；CAE-SDB Result 在对应判定实际完成并获得结果后形成。**

时间信息 T 与本次使用的状态及判定结果关联保存。

关于 C / A / E 与 S / D / B 的双轴关系，可参见：

[为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)

---

## 4.2 群体指标

单体状态之外，群控协同分析还需要观察群体层面的运行特征。

代表性群体指标包括：

```text
群体未执行比例
群体辅助执行比例
群体能源补给比例
群体许可未成立比例
```

还可以结合路径资源占用、站点承接和关键任务持续未执行等群体状态进行判断。

这些群体指标用于描述当前多主体系统的整体执行状态，并作为群控协同分析结果独立保留。

例如：

```text
群体未执行比例超过停滞识别条件
```

首先表示群体指标已经达到相应的停滞识别条件。

只有当该指标已经在当前 PCN 中被明确映射到某一 C / A / E 状态变量域，并完成相应 S / D / B 判定时，才形成 C-B、A-B 或 E-B 等对应的 CAE-SDB Result。

---

## 4.3 群体停滞识别

在群体指标形成后，进一步判断当前协同受阻是否已经达到群体停滞识别条件。

示意关系如下：

```text
存在有效任务 + 多个自动运行主体持续未进入有效执行 + 群体未执行状态持续达到判定条件

    ↓

群体停滞识别
```

如果判定条件满足，则形成：

```text
群体停滞识别：成立
```

如果不满足，则保持当前运行事实，不提前赋予“群体停滞”结论。

---

## 4.4 停滞结构分型

群体停滞识别成立后，再结合群体指标、任务、许可、资源和执行状态进行停滞结构分型。

本文所称“停滞结构分型”属于群控协同层的群体停滞分析，与 S：Structure（结构完整性）分属不同处理层。

代表性分型包括：

### 分配约束型

典型表现包括存在有效任务，但多个主体长期未进入执行，任务分配、许可或资源释放没有形成有效执行关系。

### 资源竞争型

典型表现包括主体仍在移动、绕行、等待或争用共享资源，路径、交叉口、自动门、电梯、站点或其他共享资源形成竞争，群体辅助执行较多而有效任务推进不足。

### 能源偏在型

典型表现包括较多主体集中进入充电或其他能源补给状态，可用于实际任务执行的主体比例下降，能源补给分布对整体协同执行形成明显影响。

### 未确定型

当现有状态、群体指标和其他证据不足以形成可靠分型时，保留为未确定型，并进入增强记录或人工复核。

![协同停滞识别与多路径控制流程图](/images/tpca/09-collaborative-stagnation-control-flow.png)

图：模块在完成相关状态获取和 C / A / E 状态映射后，一方面形成 CAE-SDB 判定结果，另一方面形成群体指标、停滞识别和停滞结构分型；两类结果共同进入后续控制仲裁。

---

# 5. Arbitration（控制仲裁）

一次 Target State Entry 中，可能同时存在：

```text
CAE-SDB Result
群体停滞识别结果
停滞结构分型结果
关键许可
安全约束
其他控制约束
```

例如，本次 Arbitration 的输入为：

```text
CAE-SDB Result：
A-D
资源锁状态不同步
```

同时：

```text
群体指标：群体未执行比例超过停滞识别条件

群体停滞识别：成立

停滞结构分型：资源竞争型

关键许可：安全许可成立
```

Arbitration（控制仲裁）结合：

- CAE-SDB Result；
- 群体停滞识别结果；
- 停滞结构分型结果；
- 关键许可；
- 安全约束；
- 当前 Target State Entry 的控制规则；
- 当前入口允许选择的合法控制路径；

处理当前入口的控制优先关系。

关键 A 可以构成独立必要约束。

例如，当关键安全许可未成立时，当前入口不得形成允许进入目标协同执行状态的控制结果。

Arbitration 处理的是：

> **当前多个判定结果、群体停滞状态和控制约束同时存在时，控制上应当优先处理什么。**

---

# 6. Multipath Control（多路径控制）

Arbitration 完成后，PCN 输出当前 Target State Entry 对应的 Multipath Control。

MES / WCS 协同停滞诊断模块可以输出的代表性控制路径包括：

```text
正常继续执行
等待
任务重新分配
资源释放
路径或通行权协调
限流
缓存分流
下游协调
能源补给策略调整
降级执行
人工确认
禁止进入
异常隔离
增强记录
```

例如，本次已经确认：

```text
群体停滞识别：成立

停滞结构分型：资源竞争型

CAE-SDB Result：A-D
资源锁状态不同步
```

根据当前控制规则，Arbitration 可以确定：

```text
Multipath Control： 资源释放 + 路径协调 + 任务重新分配
```

在本公开案例中，MES / WCS 协同停滞诊断模块首先输出结构化控制结果、控制建议或协调请求。实际项目中是否由模块直接下发控制指令，取决于既有 MES / WCS、调度系统、现场控制系统的接口和控制权限。

如果某一控制路径对应新的 Target State / Target Path，则在进入相应路径时继续进行新的状态迁移判定。

---

# 7. 当前入口控制结果

本次代表状态设定为：

```text
任务：存在
执行主体：在线
资源锁状态：不同步
安全许可：成立
群体未执行比例：达到停滞识别条件
群体停滞识别：成立
停滞结构分型：资源竞争型
```

当前已形成：

```text
CAE-SDB Result：
A-D
```

Arbitration 已经确定本次 Multipath Control 为：

```text
资源释放 + 路径协调 + 任务重新分配
```

因此，当前“进入可持续协同执行状态”这一 Target State Entry 的控制结果为：

```text
当前入口控制结果： 暂不进入可持续协同执行状态
```

路径选择已在 Arbitration 阶段完成；本步骤确认当前 Target State Entry 的控制结果。

实际控制路径是否执行成功，在下一步确认。

---

# 8. 选定控制路径与 Execution Result（执行结果）

本次已经确定的 Multipath Control 为：

```text
资源释放 + 路径协调 + 任务重新分配
```

在采用控制建议或协调请求输出方式的部署中，既有 WCS、调度系统或现场控制系统接收这些结果，并按照其原有控制权限执行相应处理。

示意执行过程如下：

```text
当前协同入口暂不进入
    ↓
既有控制系统处理异常占用或失效资源锁
    ↓
重新协调路径与通行权
    ↓
重新分配受影响任务
    ↓
形成新的协同运行状态
```

假设执行完成后：

```text
资源锁：恢复一致
关键路径：恢复可用
受影响任务：重新分配完成
群体未执行比例：回到停滞识别条件以下
```

则形成：

```text
Execution Result：
相关资源与路径关系已恢复，
受影响任务重新进入可执行状态
```

后续如果再次请求进入“可持续协同执行状态”，则基于新的 Current State / State Instance，在对应 Target State Entry 下继续进行新的状态迁移判定。

因此，一次完整处理需要区分：

```text
CAE-SDB Result + 群体停滞识别 + 停滞结构分型
        ↓
控制仲裁结果
        ↓
Multipath Control
        ↓

当前入口控制结果
        ↓
控制路径执行
        ↓
Execution Result
```

其中：

```text
Arbitration = 决定控制优先关系

Multipath Control = 输出已经确定的控制路径

当前入口控制结果 = 说明当前 Target State Entry 是否进入或暂不进入

控制路径执行 = 由具有相应控制权限的系统执行已经确定的处理

Execution Result = 说明已确定的控制路径实际执行后形成了什么结果
```

关于状态类型循环与实际运行状态实例之间的关系，可参见：

[TPCA 中状态实例的单向性——状态类型循环与实际运行履历的区别](/zh/notes/tpca-unidirectional-state-transition/)

---

# 9. PCN Trace（状态迁移判定履历）

本次状态迁移完成控制处理后，PCN 将输入、判定、群体停滞识别、停滞结构分型、控制和执行结果关联记录为 PCN Trace。

例如：

```text
PCN：协同执行入口 PCN

Current State：协同执行受阻 / 多主体 Waiting 持续

Target State：可持续协同执行状态

Target State Entry：进入可持续协同执行状态

主要输入：
  Task = Available
  Agents = Online
  Resource Lock = Unsynchronized
  Safety Permission = TRUE

CAE-SDB Result：A-D  资源锁状态不同步

群体指标：群体未执行比例达到停滞识别条件

群体停滞识别：成立

停滞结构分型：资源竞争型

关键许可：安全许可成立

控制仲裁结果：优先执行资源释放、路径协调和任务重新分配

Multipath Control：资源释放 + 路径协调 + 任务重新分配

当前入口控制结果：暂不进入可持续协同执行状态

Execution Result：相关资源与路径关系已恢复，受影响任务重新进入可执行状态

时间信息：T

Trace ID：PCN-COLLAB-XXXX
```

PCN Trace 以一次 Target State Entry 为单位，关联记录本次使用的状态、CAE-SDB 判定结果、群控协同分析结果、控制仲裁、控制路径和实际执行结果。

长期积累后，这些 Trace 可以用于：

- 高频协同受阻入口识别；
- 群体停滞识别结果统计；
- 停滞结构分型比较；
- 任务分配与资源锁问题复盘；
- 路径与站点协同问题分析；
- 能源补给分布分析；
- 高频 CAE-SDB Result 统计；
- 高频 Multipath Control 统计；
- 控制路径与 Execution Result 的关系比较；
- MES / WCS 诊断页面；
- 工程修改前后比较。

进一步还可以比较：

```text
哪些 Target State Entry 经常无法成立
哪些群体停滞类型高频出现
哪些 CAE-SDB Result 经常与特定停滞类型同时出现
哪些 Multipath Control 被反复选择
控制选择与 Execution Result 之间存在什么关系
```

关于 PCN Trace 作为状态迁移判定履历的工程意义，可参见：

[为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)

---

## 案例总结

MES、WCS、设备和搬送系统已经拥有大量任务、主体、路径、资源、站点和运行状态数据。

本案例围绕明确的 Target State Entry，将这些分散状态按照统一工程顺序重新组织：

```text
1. Current State
2. Target State / Target State Entry
3. PCN：相关状态获取 + C / A / E Mapping
4. 前置判定与群控协同分析
   ├─ S / D / B Evaluation
   │  → CAE-SDB Result + T
   └─ 群体指标
      → 群体停滞识别
      → 停滞结构分型
5. Arbitration
6. Multipath Control
7. 当前入口控制结果
8. 选定控制路径   → Execution Result
9. PCN Trace
```

这样可以把“任务存在、设备在线，但为什么现场仍持续受阻”进一步展开为：

```text
当前协同状态是什么
准备进入什么目标协同状态
哪些任务、主体、资源、许可和下游状态与本次入口有关
这些状态分别进入 C / A / E 的什么状态变量域
需要执行哪些 S / D / B 判定
形成了哪些 CAE-SDB Result
群体指标是否达到停滞识别条件
群体停滞是否成立
停滞属于哪一种结构类型
上述结果如何进入 Arbitration
最终形成什么 Multipath Control
当前入口最终如何处理
选定路径实际执行成什么结果
这些信息如何形成 PCN Trace
```

其中，第 4 步包含两条相互区分的分析线。

CAE-SDB 通过：

```text
C / A / E
×
S / D / B
```

形成 9 个用于组织当前入口状态判定问题的坐标，并根据当前入口实际存在的判定规则形成相应 CAE-SDB Result。

群控协同分析则保留群控层自身的分析结构：

```text
群体指标
→ 群体停滞识别
→ 停滞结构分型
```

因此，两类分析分别承担不同的工程作用：

```text
CAE-SDB
  → 对当前 Target State Entry 的相关状态进行结构化判定

群控协同分析
  → 描述和识别多主体系统的群体协同受阻结构
```

两类结果在 Arbitration 层汇合，再连接到 Multipath Control、当前入口控制结果、实际执行和 PCN Trace。

这种组织方式保留了群控协同层的技术特征，同时与 TPCA / PCN 的统一九步工程分析顺序保持一致。

---


## 进一步阅读

- [为什么 MES / WCS 能记录，却不能解释停滞？](/zh/questions/why-mes-records-but-cannot-explain/)
- [为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)
- [为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)
- [多个 PCN 如何形成状态迁移前置控制网络？](/zh/notes/pcn-network-structure/)
- [为什么 OEE 之后还需要 PCN？](/zh/notes/why-oee-pcn/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

---

## 版本说明

本文为 TPCA / PCN 在 MES / WCS 协同停滞诊断中的公开案例。

- Public Case Version 1.0：2026-06-30 发布。
- Public Case Version 1.2：2026-08-20，统一 PCN、CAE-SDB Result、控制仲裁、多路径控制和 PCN Trace 的表达。
- Public Case Version 1.3：2026-08-21，补充时间信息 T 与状态实例相关说明。
- Public Case Version 1.4：2026-08-25，按 CAE-SDB 双轴结构统一案例表达，并统一停滞识别、结构分型与 CAE-SDB Result 的处理顺序。
- Public Case Version 1.5：2026-09-10，按统一九步工程分析顺序重新整理；明确 Current State 与群体停滞识别的先后关系，并收紧诊断模块与既有控制系统之间的执行边界。

作者：全野南政 / Nansei Zenno
