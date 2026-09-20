---
title: "制造 DX 状态迁移条件设计与履历分析案例"

summary: "以部件自动加工完成后进入人工作业单元组装为代表场景，说明 PCN 如何围绕明确的 Target State Entry，组织 MES、自动加工设备、质量系统、部件搬送与供给、作业人员资格、单元设备、治具工具和后续处理中的相关状态，并按照统一九步工程顺序完成 C / A / E 状态映射、S / D / B 判定、Arbitration、Multipath Control、入口控制、控制路径执行或后续 Target State Entry、Execution Result 和 PCN Trace 记录。"

description: "公开说明 TPCA / PCN 在制造 DX 状态迁移条件设计与履历分析中的应用方式。以“自动加工完成 → 人工作业单元组装开始”为代表状态迁移，将分散在 MES、自动加工设备、质量系统、部件供给、作业人员资格、单元设备、治具工具、后续检测和结果回写中的状态，围绕一次明确的 Target State Entry 组织为可判定、可控制、可记录和可复盘的工程结构。"

date: 2026-08-18
lastmod: 2026-09-20

author: "全野南政 / Nansei Zenno"

document_type: "公开案例"

version: "Public Case Version 1.5"

citation_title: "制造 DX 状态迁移条件设计与履历分析案例：自动加工已经完成，为什么仍不能开始人工作业单元组装？"
citation_url: "https://zennns.com/zh/cases/production-dx-state-transition/"

draft: false

ShowReadingTime: false
ShowToc: true
TocOpen: true
---

# 自动加工已经完成，为什么仍不能开始人工作业单元组装？

> 应用层级：制造流程 / 跨系统状态迁移  
> 代表对象：部件自动加工 → 人工作业单元组装

**建议引用：**

```text
全野南政 / Nansei Zenno，《制造 DX 状态迁移条件设计与履历分析案例：自动加工已经完成，为什么仍不能开始人工作业单元组装？》，公开案例，Public Case Version 1.5，2026-09-20，https://zennns.com/zh/cases/production-dx-state-transition/
```

制造现场中，经常存在这样的生产流程：

```text
自动加工设备
    ↓
部件加工完成
    ↓
搬送 / 供给
    ↓
人工作业单元组装
```

自动加工侧可以从 PLC 和设备系统取得加工完成、部件 ID、产品型号、批次、加工条件和设备状态。质量系统可以记录测量结果、质量判定和质量放行。MES 可以保存作业指示、生产对象和工序信息。

进入人工作业单元以后，还会增加新的状态来源，例如作业人员身份、作业资格、组装指示、必要零部件、治具、紧固工具、单元设备、组装后检测、完成品搬出和生产实绩回写。

因此，即使自动加工已经完成，现场仍可能出现：

- 加工完成已经成立，但对象部件与组装作业指示的对应关系尚未确认；
- 质量结果已经合格，但进入下一工序所需的质量放行尚未成立；
- 加工部件已经到达作业单元，但组装所需的其他零部件尚未齐套；
- 作业人员已经登录，但当前人员的产品资格或作业权限已经失效；
- 单元设备处于 Ready，但治具或紧固工具的设定与当前产品不一致；
- MES 已经切换作业指示，但单元侧显示内容或设备设定仍处于上一产品状态；
- 组装本身可以开始，但后续检测、完成品放置、搬出或实绩回写链路当前无法接续。

本案例选择其中一个明确的状态迁移：

```text
自动加工完成
        ↓
人工作业单元组装开始
```

并按照 TPCA / PCN 的统一九步工程分析顺序展开：

```text
1. Current State
2. Target State / Target State Entry
3. PCN：相关状态获取 + C / A / E Mapping
4. S / D / B Evaluation    → CAE-SDB Result + T
5. Arbitration
6. Multipath Control
7. 当前入口控制结果
8. 控制路径执行 / 后续 Target State Entry 与 Execution Result
9. PCN Trace
```

通过这 9 个步骤，可以看到一次从自动加工设备跨越到人工作业单元的制造状态迁移，如何被组织为明确的判定、控制、执行和履历对象。

基础概念可参见：

- [核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

---

## 案例对象

本案例假设自动加工设备已经完成某个部件的加工，部件经过搬送或供给后，准备进入由作业人员负责的人工作业单元进行组装。

代表性系统关系如下：

```text
自动加工设备 / PLC
        ↓
加工完成・部件识别・加工条件
        ↓
质量系统 / MES
        ↓
搬送・部件供给
        ↓
PCN［人工作业单元组装开始前的判定］
        ↓
作业人员 + 单元设备 + 治具 / 工具
        ↓
人工作业单元组装
        ↓
组装后检测 / 搬出 / 实绩回写
```

与本次状态迁移有关的主要系统和对象包括：

- MES；
- 自动加工设备 / PLC；
- 质量系统；
- 部件搬送与供给系统；
- 作业人员认证与资格管理；
- 人工作业单元设备 / HMI；
- 治具与紧固工具；
- 组装后检测；
- 完成品放置与搬出；
- 生产实绩与追溯回写。

这一场景同时包含自动设备、信息系统、人员、物料、工具和后续工序，是制造 DX 中具有代表性的跨系统状态迁移对象。

---

# 1. Current State（当前状态 / 当前阶段）

本案例从自动加工已经完成、对象部件正在等待进入人工作业单元组装的时点开始。

```text
Current State：自动加工完成 / 等待人工作业单元组装
```

此时可能已经成立：

```text
加工完成 = TRUE
部件 ID = 已读取
当前批次 = 已确定
质量测量 = 已完成
部件搬送 = 已完成
```

这些状态构成本次状态迁移的当前运行事实。

Current State 用于明确本次工程分析的起点，并作为后续相关状态获取、C / A / E 映射和 S / D / B 判定的共同上下文。

---

# 2. Target State / Target State Entry（目标状态 / 目标状态入口）

本次准备进入的 Target State 为：

```text
Target State：对象部件的人工作业单元组装中
```

对应的 Target State Entry 为：

```text
Target State Entry：开始对象部件的人工作业单元组装
```

PCN 位于 Current State 与 Target State Entry 之间：

```text
Current State
自动加工完成 / 等待人工作业单元组装
        ↓
PCN［针对“开始人工作业单元组装”的前置判定］
        ↓
Target State Entry
开始对象部件的人工作业单元组装
        ↓
Target State
对象部件的人工作业单元组装中
```

明确这个入口以后，本次判定对象可以收敛为：

> **当前加工完成的部件，能否由当前作业人员，在当前人工作业单元中开始组装，并保证组装后的执行链能够继续接续。**

本案例后续的 C / A / E、S / D / B、Arbitration 和 Multipath Control 均绑定这个明确的 Target State Entry。

关于 PCN 与 Target State Entry 的对应关系，可参见：

[为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)

---

# 3. PCN：相关状态获取与 C / A / E 状态映射

PCN 取得与“开始对象部件的人工作业单元组装”直接相关的多源状态。

代表性输入如下。

| 来源 | 与本次组装开始入口有关的状态 |
|---|---|
| MES | 作业指示、产品型号、批次、组装品种、生产许可、作业顺序 |
| 自动加工设备 / PLC | 加工完成、加工品 ID、加工程序、加工条件、设备状态 |
| 质量系统 | 测量结果、质量判定、质量放行、对应批次 |
| 搬送 / 部件供给系统 | 加工部件到达、必要零部件供给、部件位置、供给完成 |
| 作业人员认证 / 资格管理 | 作业人员 ID、登录状态、作业资格、当前产品作业权限 |
| 人工作业单元设备 / HMI | 单元运行状态、设备 Ready、作业指示显示、产品切换状态 |
| 治具 / 工具 | 治具状态、紧固工具 Ready、设定值、校准状态 |
| 后续处理 | 组装后检测、完成品放置、搬出状态、实绩回写状态 |

这些状态根据其在当前 Target State Entry 中承担的工程作用映射到 C / A / E 状态变量域。

```text
C = Condition（条件状态）
A = Authority（许可状态）
E = Execution Chain（执行链状态）
```

本案例可以整理为：

| 状态变量域 | 当前入口中的代表性状态 |
|---|---|
| C：Condition | 加工完成、部件 ID、批次一致、质量结果、产品型号、组装作业指示、必要零部件 |
| A：Authority | 质量放行、生产许可、作业人员资格、当前产品作业权限、必要人工确认 |
| E：Execution Chain | 单元设备 Ready、治具状态、紧固工具状态、组装后检测、完成品放置、搬出状态、实绩回写状态 |

例如：

```text
加工完成 → C
质量放行 → A
作业人员资格 → A
单元设备 Ready → E
实绩回写状态 → E
```

质量相关状态可以进一步区分：

```text
质量结果
  → 当前部件是否满足质量要求
  → C
```

```text
质量放行
  → 当前部件是否被允许进入组装工序
  → A
```

作业人员相关状态也需要按当前 Target State Entry 中的作用进行整理：

```text
作业人员已登录
  → 当前人员身份和登录状态

当前产品作业资格
  → 当前人员是否被允许执行该组装作业
  → A
```

单元设备 Ready 作为 E 的一个相关状态参与判定。

当前组装开始入口所要求的 Execution Chain 还包括治具、紧固工具、组装后检测、完成品放置、搬出以及实绩回写等后续接续状态。

---

# 4. S / D / B Evaluation 与 CAE-SDB Result

完成 C / A / E 状态映射后，PCN 对当前 Target State Entry 所需要的状态执行 S / D / B 判定。

```text
S = Structure（结构完整性）
D = Dynamics（动态时序有效性）
B = Boundary（控制边界）
```

本案例中的典型判定包括：

| 判定性质 | 典型确认内容 |
|---|---|
| S：Structure | 当前组装入口所需的部件、作业指示、质量、许可、人员资格、单元设备、治具 / 工具、后续处理和实绩回写等状态，其接口、映射、来源及对象关系是否已经定义、接入并可观测 |
| D：Dynamics | 当前状态是否仍可作为本次组装开始入口的有效判定依据，包括批次与质量信息同步、作业指示版本、人员登录与资格有效性、产品切换、单元设备及工具状态刷新、后续处理状态更新 |
| B：Boundary | 当前有效状态的数值或范围是否处于预先定义的质量阈值、部件位置、在制品数量、缓存容量、工具设定、许可适用范围、等待时间等允许边界内 |

C / A / E 状态变量域与 S / D / B 判定性质组合后，可以形成 9 个 CAE-SDB 判定坐标。

|  | S：Structure | D：Dynamics | B：Boundary |
|---|---|---|---|
| C：Condition | C-S | C-D | C-B |
| A：Authority | A-S | A-D | A-B |
| E：Execution Chain | E-S | E-D | E-B |

在本案例中，可以按照当前“开始对象部件的人工作业单元组装”这一 Target State Entry，将代表性的工程问题展开如下。

| 判定坐标 | 本案例中的代表性工程问题 |
|---|---|
| C-S | 部件 ID 与组装作业指示的对应关系未建立；批次与质量结果的映射未定义；必要零部件与当前产品的对应关系未完整建立；相关条件状态无法由当前 PCN 取得 |
| C-D | 当前质量结果对应上一批次；MES 作业指示已经切换但单元侧仍保留上一版本；部件供给状态长时间未刷新；当前部件 ID 与现场实际对象发生切换不同步 |
| C-B | 当前有效的质量测量值超出允许范围；部件位置超出允许作业范围；单元前在制品数量、等待时间或其他条件参数达到预定义边界 |
| A-S | 质量放行、生产许可、作业人员资格、当前产品作业权限或必要人工确认的来源未定义；许可接口或映射关系未建立；关键许可状态无法由当前 PCN 取得 |
| A-D | 当前产品作业资格被撤销；质量放行状态长时间未刷新；生产许可或人工确认发生更新延迟；许可状态与当前产品切换不同步 |
| A-B | 当前产品作业资格超过有效期；当前有效的作业资格适用产品范围不包含当前产品；当前有效生产许可的有效时间窗、适用单元或批次范围不满足本次入口要求；许可使用范围达到预定义边界 |
| E-S | 当前组装执行链所要求的单元设备、治具、紧固工具、组装后检测、完成品放置、搬出或实绩回写接口未完整定义、未接入或对象关系未建立 |
| E-D | 单元设备或工具状态长时间未刷新；产品切换后治具 / 工具状态仍对应上一产品；组装后检测、搬出或实绩回写状态延迟、不同步或无法确认当前有效 |
| E-B | 当前有效的紧固工具设定值超出允许范围；治具位置或设备参数超出允许边界；组装后缓存容量、完成品放置容量或当前执行链等待时间达到预定义边界 |

这 9 个坐标用于组织当前 Target State Entry 中可能出现的状态判定问题。

> **每一次运行不要求形成全部 9 项 CAE-SDB Result。**

只有当前入口已经定义相应判定规则、存在可用判定依据，并且实际完成 Evaluation 后，才形成对应的 CAE-SDB Result。

例如，作业人员已经登录，但当前产品对应的作业资格已经超过有效期：

```text
作业人员登录：有效

当前产品作业资格：已登记

资格有效期：已过期
```

如果当前产品作业资格映射到 A，并完成相应 B 判定，可以形成：

```text
A-B：
当前作业资格已经超过有效期，
不满足本次组装开始入口的许可边界
```

再例如：

```text
质量结果：当前批次有效
质量测量值：超出预定义允许范围
```

完成相应 B 判定后，可以形成：

```text
C-B：
质量测量值超出当前组装开始入口允许的控制边界
```

如果紧固工具当前设定值超出该产品允许范围，则完成相应 B 判定后，可以形成：

```text
E-B：
紧固工具设定值超出当前组装执行链允许的控制边界
```

再例如：

```text
作业人员资格：当前有效
资格适用产品范围：不包含当前产品
```

如果该资格映射到 A，并且相应 B 判定已经定义并实际完成，可以形成：

```text
A-B：
当前有效的作业资格
超出本次组装入口允许的产品适用范围
```

> **需要执行某项 S / D / B 判定，表示该判定属于当前入口的评价规则；CAE-SDB Result 在对应判定实际完成并获得结果后形成。**

时间信息 T 与本次使用的状态及判定结果关联保存。

关于 C / A / E 与 S / D / B 的双轴关系，可参见：

[为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)

---

# 5. Arbitration（控制仲裁）

一次 Target State Entry 中，可能同时形成多个 CAE-SDB Result，也可能同时存在关键许可、安全约束、质量约束和执行链状态。

本案例假设当前状态如下：

```text
加工完成：成立
质量结果：合格
质量放行：成立
必要零部件：齐套
单元设备 Ready：成立
作业人员登录：有效
当前产品作业资格：已过期
```

完成对应判定后形成：

```text
CAE-SDB Result：
  A-B
  当前作业人员资格已经超过有效期
```

当前产品作业资格属于本次人工作业单元组装开始入口的关键 A。

Arbitration 结合：

- CAE-SDB Result；
- 关键许可；
- 安全与质量约束；
- 当前 Target State Entry 的进入要求；
- 当前入口允许选择的合法控制路径；

处理当前入口的控制优先关系。

本例中，C 和 E 相关状态满足进入要求，关键 A 中的作业人员资格当前无效，因此控制仲裁优先处理该 A-B。

```text
控制仲裁结果：
  暂缓当前作业人员开始组装
  优先确认具备有效资格的作业人员
```

关键 A 作为独立必要约束参与当前入口控制。

---

# 6. Multipath Control（多路径控制）

Arbitration 完成后，PCN 输出当前 Target State Entry 对应的 Multipath Control。

本案例中的代表性控制路径可以包括：

```text
允许进入
等待
重新取得作业指示
重新确认质量状态
确认具备有效资格的作业人员
更换作业人员
补充必要零部件
重新确认单元设定
重新确认工具设定
转入其他作业单元
退避至在制品缓存
转入返修工序
隔离
禁止进入
人工确认
增强记录
```

针对本次 A-B，可以形成：

```text
Multipath Control：暂缓当前组装开始 + 确认具备有效资格的作业人员
```

如果转入其他作业单元、返修、隔离等路径对应新的 Target State / Target Path，则在进入相应路径时，由其对应的 Target State Entry 继续执行新的状态迁移前置判定。

---

# 7. 当前入口控制结果

根据第 6 步已经形成的 Multipath Control，确认当前“开始对象部件的人工作业单元组装”这一 Target State Entry 的控制结果。

```text
当前入口控制结果：
暂不开始当前人工作业单元组装

Multipath Control：
确认具备有效资格的作业人员
```

本步骤只确认当前 Target State Entry 如何处理。

具体处理动作完成后的结果，在下一步确认。

---

# 8. 控制路径执行 / 后续 Target State Entry 与 Execution Result（执行结果）

本次 Multipath Control 为：

```text
确认具备有效资格的作业人员
```

在本案例中，该输出属于当前组装入口下的处理动作，不自动构成新的 Target State Entry。

现场可以按以下方式执行：

```text
当前组装开始暂缓
    ↓
重新确认作业人员资格
    ↓
更换为具备有效资格的作业人员
    ↓
重新取得当前资格状态
    ↓
Execution Result
```

例如：

```text
Execution Result：
已完成具备有效资格的作业人员更换，
当前作业资格状态已确认有效
```

处理动作完成后形成新的运行事实。后续再次请求：

```text
Target State Entry：
开始对象部件的人工作业单元组装
```

时，需要基于更新后的 Current State 和相关状态重新进行前置判定。

如果 Multipath Control 指向转入其他作业单元、返修、隔离等新的 Target State / Target Path，则该路径形成新的 Target State Entry，并由对应 PCN 重新进行前置判定。

> **处理动作完成或候选路径被选中，都不等于相应 Target State Entry 已经获得进入许可。**

关于状态类型循环与实际运行状态实例之间的关系，可参见：

[TPCA 中状态实例的单向性——状态类型循环与实际运行履历的区别](/zh/notes/tpca-unidirectional-state-transition/)

---

# 9. PCN Trace（状态迁移判定履历）

PCN Trace 以一次明确的 Target State Entry 为基本记录对象。

本次组装开始入口可以记录：

```text
PCN：
人工作业单元组装开始入口 PCN

Current State：
自动加工完成 / 等待人工作业单元组装

Target State：
对象部件的人工作业单元组装中

Target State Entry：
开始对象部件的人工作业单元组装

主要状态：
  加工完成 = TRUE
  质量结果 = 合格
  质量放行 = 成立
  必要零部件 = 齐套
  单元设备 Ready = TRUE
  作业人员登录 = 有效
  当前产品作业资格 = 已过期

CAE-SDB Result：
A-B

Arbitration Result：
暂缓当前作业人员开始组装

Multipath Control：
确认具备有效资格的作业人员

当前入口控制结果：
暂不开始当前人工作业单元组装

Execution Result：
已完成具备有效资格的作业人员更换，
当前作业资格状态已确认有效

时间信息：
T

Trace ID：
PCN-CELL-XXXX
```

作业人员更换完成后形成新的运行事实。后续再次请求同一 Target State Entry 时，基于更新后的状态重新进行前置判定，并形成新的 Trace；前一次 Trace 不被覆盖。

关于 PCN Trace 作为状态迁移判定履历的工程意义，可参见：

[为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)

---

## 案例总结

本案例以：

```text
自动加工完成
    ↓
人工作业单元组装开始
```

这一跨系统状态迁移为对象，按照统一九步工程顺序展开：

```text
1. Current State
2. Target State / Target State Entry
3. PCN：相关状态获取 + C / A / E Mapping
4. S / D / B Evaluation → CAE-SDB Result + T
5. Arbitration
6. Multipath Control
7. 当前入口控制结果
8. 控制路径执行 / 后续 Target State Entry 与 Execution Result
9. PCN Trace
```

该案例将自动加工侧已经形成的生产事实，与人员资格、质量放行、部件齐套、单元设备、治具工具及后续执行链接续状态，组织到同一次 Target State Entry 中进行判定。

当前入口下的处理动作完成后，需要基于更新后的状态重新判定原 Target State Entry；如果 Multipath Control 指向新的 Target State / Target Path，则由对应入口的 PCN 重新进行前置判定。

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
- Public Case Version 1.4：2026-09-10，按统一九步工程分析顺序重新整理，并采用“自动加工 → 人工作业单元组装”作为代表场景。
- Public Case Version 1.5：2026-09-20，按当前 S / D / B 定义修正作业资格有效期的判定性质。

作者：全野南政 / Nansei Zenno
