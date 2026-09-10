---

title: "制造 DX 状态迁移条件设计与履历分析案例"

summary: "以跨 MES、质量、设备、人员、保全与下游系统的制造状态迁移为对象，按照一次状态迁移实际发生的工程顺序，说明 PCN 如何从 Current State 和 Target State Entry 出发，完成相关状态获取、C / A / E 状态映射、S / D / B 判定、控制仲裁、多路径控制、入口控制结果、路径执行和 PCN Trace 记录。"

description: "公开说明 TPCA / PCN 在制造 DX 状态迁移条件设计与履历分析中的应用。以“前工序完成后进入下一生产工序”为代表状态迁移，按照 Current State、Target State / Target State Entry、PCN、CAE-SDB、Arbitration、Multipath Control、入口控制结果、Execution Result 和 PCN Trace 的顺序展开一次完整的跨系统状态迁移前置控制过程。"

date: 2026-08-18

lastmod: 2026-09-10

author: "全野南政 / Nansei Zenno"

document_type: "公开案例"

version: "Public Case Version 1.4"

citation_title: "制造 DX 状态迁移条件设计与履历分析案例：为什么制造 DX 已有数据，状态迁移仍然依赖经验？"

citation_url: "https://zennns.com/zh/cases/production-dx-state-transition/"

draft: false

ShowReadingTime: false

ShowToc: true

TocOpen: true

---

# 为什么制造 DX 已有数据，状态迁移仍然依赖经验？

> 应用层级：制造流程 / 跨系统状态迁移

> 代表对象：工序切换、质量判定、生产放行、返工、回流、废品处理、保全解除、人工确认、下游承接

**建议引用：**

```text
全野南政 / Nansei Zenno，《制造 DX 状态迁移条件设计与履历分析案例：为什么制造 DX 已有数据，状态迁移仍然依赖经验？》，公开案例，Public Case Version 1.4，2026-09-10，https://zennns.com/zh/cases/production-dx-state-transition/
```

制造 DX 项目通常已经能够获取大量生产与运行数据。

MES 可以记录工单、批次、计划和生产实绩；质量系统可以记录检测结果、质量判定和放行状态；PLC 与设备控制系统可以提供自动模式、设备就绪、报警、互锁和动作状态；人员系统可以管理身份与权限；保全系统可以记录维修、点检和复归；下游设备、搬送系统和缓存区也可以提供接收、占用和运行状态。

但现场仍可能出现：

- 前工序已经完成，但下一工序迟迟没有开始；
- MES 显示工单有效，设备也已就绪，但当前产品或批次仍不能进入下一阶段；
- 质量结果已经产生，却不能确认当前批次是否已经正式放行；
- 工单已经切换，但 PLC 配方、物料、质量结果和追溯信息没有完全同步；
- 保全作业已经结束，但设备是否允许重新投入生产仍需要确认；
- 下游显示可接收，但当前状态是否仍能作为本次状态迁移的有效依据需要进一步确认。

本案例选择其中一个代表性状态迁移：

```text
前工序完成 → 下一生产工序
```

按照统一的九步工程分析顺序展开：

```text
1. Current State
2. Target State / Target State Entry
3. PCN：相关状态获取 + C / A / E Mapping
4. S / D / B Evaluation  → CAE-SDB Result + T
5. Arbitration
6. Multipath Control
7. 当前入口控制结果
8. 选定控制路径与 Execution Result
9. PCN Trace
```

通过这 9 个步骤，可以直接看到：

> **一次“准备进入下一生产工序”的跨系统状态迁移，在 TPCA / PCN 中如何完成判定、控制、执行和记录。**

基础概念可参见：

- [核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

---

## 案例对象

本案例以跨 MES、质量、PLC / 设备、人员、保全、物料追溯与下游系统的制造状态迁移为对象。

代表性生产流程如下：

```text
前工序完成
    ↓
生产放行判定
    ↓
下一生产工序
```

在同一个制造系统中，还可能存在其他后续目标状态或目标执行路径，例如：

```text
检测完成 → 返工工序
检测完成 → 回流工序
检测完成 → 废品处理工序
检测完成 → 隔离工序
保全完成 → 自动生产重新投入
```

这些路径分别对应各自的 Target State / Target State Entry。

本案例的九步展开只绑定：

```text
Target State： 下一生产工序
```

返工、回流、废品处理、隔离等路径在需要时作为其他候选控制方向或新的 Target State / Target Path 单独处理。

PCN 的具体实现可以由 MES、制造执行中间层、工业边缘系统、PLC / HMI 协同模块或其他软件组件承担。本案例不限定具体部署平台。

{{< production-dx-animation >}}

---

# 1. Current State（当前状态 / 当前阶段）

本案例从前工序已经完成，但当前对象尚未进入下一生产工序的时点开始。

当前状态定义为：

```text
Current State： 前工序完成 / 等待下一工序放行
```

此时，当前产品或批次已经完成上一阶段处理，下一步是否进入目标生产工序仍需要确认。

相关系统中可能已经存在：

```text
MES 工单 = 有效
质量结果 = 合格
设备 = Ready
操作人员 = 已确认
下游 = 可接收
```

这些状态分别来自不同系统。

这里先明确本次实际运行的状态迁移起点。后续的相关状态获取、C / A / E 状态映射以及 S / D / B 判定，均以这个 Current State 为本次运行实例的起点。

---

# 2. Target State / Target State Entry（目标状态 / 目标状态入口）

本次准备进入的 Target State 为：

```text
Target State： 下一生产工序
```

对应的 Target State Entry 为：

```text
Target State Entry： 进入下一生产工序
```

PCN 位于 Current State 与 Target State Entry 之间：

```text
Current State［前工序完成 / 等待下一工序放行］
    ↓
PCN［针对“进入下一生产工序”的前置判定］
    ↓
Target State Entry ［进入下一生产工序］
    ↓
Target State［下一生产工序］
```

本案例后续的 C / A / E、S / D / B、Arbitration 和 Multipath Control，均绑定这个明确的 Target State Entry。

例如，质量 NG 对“进入下一正常生产工序”可能表示相关条件不成立；如果后续 Target State 改为“进入返工工序”，同一个质量 NG 又可能成为该状态迁移所需的条件之一。

因此，相关状态需要绑定当前 Current State、Target State 与 Target State Entry 进行解释。

关于 PCN 与 Target State Entry 的对应关系，可参见：

[为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)

---

# 3. PCN：相关状态获取与 C / A / E 状态映射

PCN 取得与“进入下一生产工序”直接相关的多源状态。

代表性输入如下。

| 来源 | 与本次入口有关的状态 |
|---|---|
| MES | 工单状态、批次号、产品型号、生产许可、配方编号 |
| 质量系统 | 检测完成、质量结果、质量放行 |
| PLC / 设备 | 自动模式、设备 Ready、当前工艺阶段、配方加载、动作完成、设备报警 |
| 保全系统 | 点检完成、维修完成、保全解除、重新投入许可 |
| 人员 / 权限系统 | 操作人员身份、资格、权限、人工确认 |
| 物料 / 追溯系统 | 物料身份、批次关联、追溯标识、前序结果关联 |
| 下游 / 搬送系统 | 下游可接收、缓存容量、搬送可用、交接许可 |
| 数据接口 | 状态更新时间、状态版本、序列信息、回写完成、接口可用、同步完成 |

这些状态根据其在当前 Target State Entry 中承担的工程作用映射到 C / A / E 状态变量域。

```text
C = Condition（条件状态）
A = Authority（许可状态）
E = Execution Chain（执行链状态）
```

本案例可以整理为：

| 状态变量域 | 当前入口中的主要对象 |
|---|---|
| C：Condition | 工单状态、批次状态、前序完成状态、质量结果、物料状态、配方状态、追溯关系 |
| A：Authority | 质量放行、生产许可、保全解除、人员权限、必要人工确认 |
| E：Execution Chain | 设备执行状态、下游承接状态、搬送状态、缓存状态、结果上传与追溯回写状态 |

例如：

```text
质量结果 → C
质量放行 → A
下游接收状态 → E
```

`设备 Ready` 作为设备侧相关状态之一，根据当前 Target State Entry 中承担的工程作用参与状态映射和判定。

除当前“下一生产工序”直接相关的 C / A / E 状态外，PCN 还可以取得与返工、回流、废品处理、隔离等候选控制路径选择有关的状态，供后续 Arbitration 使用。

如果这些路径对应其他 Target State / Target Path，其可用性不作为当前“下一生产工序” Execution Chain 成立的依据。

---

# 4. S / D / B Evaluation 与 CAE-SDB Result

完成 C / A / E 状态映射后，PCN 对当前 Target State Entry 所需要的相关状态执行 S / D / B 判定。

```text
S = Structure（结构完整性）
D = Dynamics（动态时序有效性）
B = Boundary（控制边界）
```

本案例中的典型判定包括：

| 判定性质 | 典型确认内容 |
|---|---|
| S：Structure | 批次与质量结果映射、质量放行来源、保全解除来源、人员权限来源、下游承接接口、结果回写接口是否已经定义、接入并可观测 |
| D：Dynamics | 工单与配方是否同步，质量结果是否属于当前批次，许可是否被撤销，下游状态是否延迟或未更新，状态版本与序列关系是否一致 |
| B：Boundary | 等待时间、确认有效期、缓存容量、资源使用范围、同步时间、重试次数等是否处于预先定义的允许边界内 |

例如：

```text
MES 已经切换到新工单
PLC 仍处于上一配方
```

如果相应 D 判定已经定义并实际完成，可以形成：

```text
C-D：
工单与当前配方在动态时序有效性方面不满足本次入口要求
```

又例如：

```text
质量结果 = 合格
质量结果对应批次 = 上一批次
```

如果该质量结果被映射为当前入口的 C 状态，并且相应 D 判定已经定义并实际完成，可以形成与 C-D 对应的判定结果。

再例如：

```text
下游接收状态仍显示 Available
但该状态长时间未刷新
```

如果相应 D 判定已经定义并实际完成，可以形成：

```text
E-D：
下游接收状态无法继续作为当前入口的有效执行链依据
```

对于 Boundary，可以出现：

```text
下游缓存容量达到预定义上限
```

如果相应 B 判定已经定义并实际完成，可以形成：

```text
E-B：
当前下游容量超出本次入口允许的控制边界
```

> **需要执行某项 S / D / B 判定，表示该判定属于当前入口的评价规则；CAE-SDB Result 在对应判定实际完成并获得结果后形成。**

时间信息 T 与本次使用的状态及判定结果关联保存。

关于 C / A / E 与 S / D / B 的双轴关系，可参见：

[为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)

---

# 5. Arbitration（控制仲裁）

一次 Target State Entry 中，可能同时形成多个 CAE-SDB Result，也可能同时存在关键许可、安全或质量约束，以及与当前入口有关的执行链状态。

例如，本次 Arbitration 的输入可以包括：

```text
CAE-SDB Result：
A-D：质量放行状态不同步
E-D：下游接收状态未及时刷新
```

同时：

```text
其他关键许可：
生产许可 = 成立

质量放行：
存在 A-D 判定结果

E 相关状态：
设备本体可执行
```

这里的生产许可与质量放行是两个不同的 Authority 状态，不能合并理解为一个“许可”。

Arbitration（控制仲裁）结合：

- CAE-SDB Result；
- 关键许可；
- 安全与质量约束；
- 当前 Target State Entry 的控制规则；
- 当前入口允许选择的合法控制路径；

处理当前入口的控制优先关系。

其中，关键 A 可以构成独立必要约束。

例如，质量结果已经合格，但正式质量放行尚未满足当前入口要求时，当前入口不能形成“允许进入下一生产工序”的控制结果。

Arbitration 处理的是：

> **当前多个判定结果和控制约束同时存在时，控制上应当优先处理什么。**

---

# 6. Multipath Control（多路径控制）

Arbitration 完成后，PCN 输出当前 Target State Entry 对应的 Multipath Control。

制造 DX 场景中的代表性控制路径可以包括：

```text
允许进入
等待
重新读取
重新核对
重新确认
状态重新同步
下游协调
资源释放
人工确认
禁止进入
隔离
增强记录
返工
回流
废品处理
```

CAE-SDB Result 经 Arbitration 与当前 Target State Entry 的合法控制路径建立控制关系。

例如，本次入口同时存在：

```text
A-D + E-D
```

根据当前控制规则，Arbitration 可以确定：

```text
Multipath Control： 状态重新同步 + 重新确认
```

如果返工、回流、废品处理、隔离等路径对应新的 Target State / Target Path，则作为当前入口的候选控制输出处理。

进入这些新的 Target State / Target Path 时，在其对应 Target State Entry 下继续进行新的状态迁移判定。

---

# 7. 当前入口控制结果

本次代表状态设定为：

```text
MES 工单：有效
质量结果：合格
质量放行：状态不同步
设备 Ready：成立
下游接收状态：未及时刷新
```

经过相关 D 判定后形成：

```text
CAE-SDB Result： A-D + E-D
```

Arbitration 已经确定本次 Multipath Control 为：

```text
状态重新同步 + 重新确认
```

因此，当前“进入下一生产工序”这一 Target State Entry 的控制结果为：

```text
当前入口控制结果： 暂不进入下一生产工序
```

这一步只说明当前 Target State Entry 最终如何处理，不再重新选择控制路径。

实际控制路径是否执行成功，在下一步确认。

---

# 8. 选定控制路径与 Execution Result（执行结果）

本次已经确定的 Multipath Control 为：

```text
状态重新同步 + 重新确认
```

系统执行相应处理：

```text
当前入口暂不进入
    ↓
重新同步质量放行状态
    ↓
重新读取下游接收状态
    ↓
重新确认当前批次、工单和目标工序关系
    ↓
形成新的运行状态
```

假设执行完成后：

```text
质量放行：当前批次有效
下游接收状态：当前有效
```

则形成：

```text
Execution Result： 相关状态已重新同步并完成确认
```

后续如果再次请求进入“下一生产工序”，则基于新的 Current State / State Instance，在对应 Target State Entry 下继续进行新的状态迁移判定。

同样，如果后续改为进入返工、回流、废品处理或隔离工序，则分别形成新的 Target State / Target Path 及其对应入口。

因此，一次完整处理需要区分：

```text
CAE-SDB Result
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

控制路径执行 = 执行已经确定的控制路径

Execution Result = 说明已确定的控制路径实际执行后形成了什么结果
```

关于状态类型循环与实际运行状态实例之间的关系，可参见：

[TPCA 中状态实例的单向性——状态类型循环与实际运行履历的区别](/zh/notes/tpca-unidirectional-state-transition/)

---

# 9. PCN Trace（状态迁移判定履历）

本次状态迁移完成控制处理后，PCN 将输入、判定、控制和执行结果关联记录为 PCN Trace。

例如：

```text
PCN：下一生产工序入口 PCN

Current State：前工序完成 / 等待下一工序放行

Target State：下一生产工序

Target State Entry：进入下一生产工序

主要输入：
  Work Order = Valid
  Quality Result = Pass
  Quality Release = Unsynchronized
  Equipment Ready = TRUE
  Downstream State = Stale
  CAE-SDB Result：A-D + E-D

关键许可：
  生产许可 = 成立
  质量放行 = 存在 A-D 判定结果

控制仲裁结果： 优先执行状态重新同步与重新确认

Multipath Control： 状态重新同步 + 重新确认

当前入口控制结果： 暂不进入下一生产工序

Execution Result： 相关状态已重新同步并完成确认

时间信息： T

Trace ID： PCN-PROD-XXXX
```

PCN Trace 以一次 Target State Entry 为单位，关联记录本次使用的状态、结构化判定、控制仲裁、控制路径和实际执行结果。

长期积累后，这些 Trace 可以用于：

- HMI、MES 或上位系统的结构化显示；
- 制造状态迁移问题复盘；
- 高频 C / A / E 问题统计；
- 高频 S / D / B 判定结果统计；
- 高频控制路径统计；
- 工单、质量、设备、下游状态同步问题分析；
- 返工、回流、废品处理和隔离路径使用情况比较；
- 工程修改前后比较；
- 同类制造流程复用与工程交接。

进一步还可以比较：

```text
哪些 Target State Entry 经常不能成立
哪些 CAE-SDB Result 高频出现
哪些 Multipath Control 被反复选择
控制选择与 Execution Result 之间存在什么关系
```

这些结构化履历可以继续作为后续统计分析、工程复盘和 AI 辅助分析的数据来源。

关于 PCN Trace 作为状态迁移判定履历的工程意义，可参见：

[为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)

---

## 案例总结

制造 DX 中已经存在大量 MES、质量、PLC、保全、人员、物料追溯和下游状态数据。

本案例围绕一个明确的 Target State Entry，把这些分散状态按照统一工程顺序重新组织：

```text
1. Current State
2. Target State / Target State Entry
3. PCN：相关状态获取 + C / A / E Mapping
4. S / D / B Evaluation  → CAE-SDB Result + T
5. Arbitration
6. Multipath Control
7. 当前入口控制结果
8. 选定控制路径  → Execution Result
9. PCN Trace
```

这样可以把“前工序已经完成，但为什么还不能进入下一生产工序”进一步展开为：

```text
当前从哪里出发
准备进入哪个目标状态
哪些跨系统状态与本次入口有关
这些状态分别属于 C / A / E 的什么作用
需要执行哪些 S / D / B 判定
形成了哪些 CAE-SDB Result
多个结果和关键许可如何进入 Arbitration
最终形成什么 Multipath Control
当前入口最终如何处理
选定路径实际执行成什么结果
这些信息如何形成 PCN Trace
```

同样的工程分析骨架也可以用于：

- 质量放行；
- 工单 / 配方切换；
- 保全解除后的生产重新投入；
- 返工；
- 回流；
- 废品处理；
- 隔离；
- 人工确认后的自动运行恢复；
- 其他具有明确 Target State Entry 的跨系统制造状态迁移。

具体变化主要体现在相关状态、判定规则、关键许可、合法控制路径和 Execution Result。

这也构成 TPCA / PCN 在制造 DX 案例、PoC 和工程展开时的基本分析顺序。

---


## 进一步阅读

- [为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)
- [为什么状态迁移条件需要显式化？](/zh/notes/explicit-state-transition-conditions/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)
- [为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)
- [TPCA 中状态实例的单向性——状态类型循环与实际运行履历的区别](/zh/notes/tpca-unidirectional-state-transition/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

---

## 版本说明

本文为 TPCA / PCN 状态迁移前置控制架构在制造 DX 状态迁移条件设计与履历分析中的公开案例。

- Public Case Version 1.0：2026-08-18 发布。
- Public Case Version 1.1：2026-08-20，统一 PCN、CAE-SDB Result、控制仲裁、多路径控制和 PCN Trace 的表达。
- Public Case Version 1.2：2026-08-21，补充时间信息 T 与状态实例相关说明。
- Public Case Version 1.3：2026-08-25，明确 C / A / E 与 S / D / B 的双轴关系。
- Public Case Version 1.4：2026-09-10，按九步工程分析顺序重新整理。

作者：全野南政 / Nansei Zenno
