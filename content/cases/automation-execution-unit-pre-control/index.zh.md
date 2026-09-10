---
title: "自动化执行单元前置判定案例"

summary: "以视觉识别输送线机器人单元为代表例，按照一次状态迁移实际发生的工程顺序，说明 PCN 如何从 Current State 和 Target State Entry 出发，完成相关状态获取、C / A / E 状态映射、S / D / B 判定、控制仲裁、多路径控制、入口控制结果、路径执行和 PCN Trace 记录。"

description: "公开说明 TPCA / PCN 在自动化执行单元中的应用方式。以机器人进入抓取阶段为例，按照 Current State、Target State / Target State Entry、PCN、CAE-SDB、Arbitration、Multipath Control、入口控制结果、Execution Result 和 PCN Trace 的顺序展开一次完整的状态迁移前置控制过程。"

date: 2026-06-30
lastmod: 2026-09-10

author: "全野南政 / Nansei Zenno"

document_type: "公开案例"
case_type: "自动化执行单元层"

version: "Public Case Version 1.4"

citation_title: "自动化执行单元前置判定案例：为什么 Robot Ready 还不足以进入抓取阶段"
citation_url: "https://zennns.com/zh/cases/automation-execution-unit-pre-control/"

draft: false
weight: 1

ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## 为什么 Robot Ready 还不足以进入抓取阶段

> 应用层级：自动化执行单元层  
> 代表对象：视觉识别输送线机器人单元

**建议引用：**

```text
全野南政 / Nansei Zenno，《自动化执行单元前置判定案例：为什么 Robot Ready 还不足以进入抓取阶段》，公开案例，Public Case Version 1.4，2026-09-10，https://zennns.com/zh/cases/automation-execution-unit-pre-control/
```

视觉识别输送线机器人单元中，可能出现这样的现场状态：

机器人已经 Ready（就绪），视觉系统也已经输出识别结果，安全系统没有明显异常，但抓取动作仍然没有开始。

Robot Ready 表示机器人本体处于所定义的运行准备状态。

进入抓取阶段还涉及当前工件条件、关键许可、抓取阶段所需执行链，以及这些状态在当前时间位置是否仍可作为有效判定依据。

本案例按照一次实际状态迁移的工程处理顺序展开：

```text
1. Current State
2. Target State / Target State Entry
3. PCN：相关状态获取 + C / A / E Mapping
4. S / D / B Evaluation → CAE-SDB Result + T
5. Arbitration
6. Multipath Control
7. 当前入口控制结果
8. 选定控制路径与 Execution Result
9. PCN Trace
```

通过这 9 个步骤，可以直接看到：

> **一次“准备进入抓取阶段”的请求，在 TPCA / PCN 中如何完成判定、控制、执行和记录。**

基础概念可参见：

- [核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

---

## 案例对象

本案例以视觉识别输送线机器人单元为代表对象，并假设 PCN 由 PLC 内的控制逻辑实现。

工件进入识别和抓取区域后，视觉系统生成工件存在、位置、姿态、识别置信度、结果时间和工件跟踪信息。

机器人控制器、安全系统、主输送带、正常投放位和上位系统分别提供与抓取入口有关的状态。

![视觉识别输送线机器人单元前置控制示意图](/images/tpca/06-pcn-pick-flow.png)

图：PCN 在机器人进入抓取阶段前取得与当前 Target State Entry 有关的多源状态，并根据判定结果形成控制路径。

---

# 1. Current State（当前状态 / 当前阶段）

本案例从“识别已经完成，但机器人尚未开始抓取”的时点开始。

当前状态定义为：

```text
Current State： 识别完成 / 等待抓取
```

这一状态表示工件已经进入本次抓取流程，视觉识别结果已经生成，机器人尚未进入抓取执行。

这里先明确本次实际运行的状态迁移起点。

后续的状态获取、C / A / E 状态映射以及 S / D / B 判定，均以这个 Current State 为本次运行实例的起点。

---

# 2. Target State / Target State Entry（目标状态 / 目标状态入口）

本次准备进入的 Target State 为：

```text
Target State： 抓取阶段
```

对应的 Target State Entry 为：

```text
Target State Entry： 进入抓取阶段
```

PCN 位于 Current State 与 Target State Entry 之间：

```text
Current State［识别完成 / 等待抓取］
    ↓
PCN［针对“进入抓取阶段”的前置判定］
    ↓
Target State［Entry 进入抓取阶段］
    ↓
Target State［抓取阶段］
```

![PCN 在目标阶段入口前的位置关系图](/images/tpca/07-pcn-position-before-target-stage.png)

图：PCN 在抓取动作真正开始之前，对“进入抓取阶段”这一 Target State Entry 进行前置判定。

本案例后续的 C / A / E、S / D / B、Arbitration 和 Multipath Control，均绑定这个明确的 Target State Entry。

关于 PCN 与 Target State Entry 的对应关系，可参见：

[为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)

---

# 3. PCN：相关状态获取与 C / A / E 状态映射

PCN 取得与“进入抓取阶段”直接相关的状态。

代表性输入如下。

| 来源 | 与本次抓取入口有关的状态 |
|---|---|
| 视觉系统 | 工件存在、位置、姿态、识别结果、识别置信度、结果时间、工件跟踪 |
| 主输送带 | 运行状态、速度、工件位置、抓取区域状态 |
| 机器人控制器 | 自动模式、Ready、当前位置、路径状态、夹爪 / 真空状态、报警状态 |
| 安全系统 | 安全门、光栅、急停、安全回路、区域许可 |
| 正常投放位 | 空位、接收状态、前一工件处理状态 |
| 上位系统 / HMI | 生产许可、工单状态、必要人工确认、结果记录或回写要求 |

这些状态根据其在当前 Target State Entry 中承担的工程作用映射到 C / A / E 状态变量域。

```text
C = Condition（条件状态）
A = Authority（许可状态）
E = Execution Chain（执行链状态）
```

本案例可以整理为：

| 状态变量域 | 当前入口中的主要对象 |
|---|---|
| C：Condition | 工件存在、位置、姿态、视觉识别结果、识别置信度、工件跟踪 |
| A：Authority | 安全许可、区域许可、PLC 放行、上位系统许可、必要人工确认 |
| E：Execution Chain | 机器人路径、夹爪 / 真空状态、当前抓取阶段所要求的下游接收状态、结果回写链路 |

例如：

```text
工件位置 → C
区域许可 → A
正常投放位接收状态 → E
```

Robot Ready 作为机器人侧的相关状态之一，根据当前抓取入口中的工程作用参与状态映射和判定。

除当前 Target State 直接相关的 C / A / E 状态外，PCN 还可以取得回流、异常分流等候选控制路径的可用状态，供后续 Arbitration 和 Multipath Control 使用。

如果这些候选路径对应其他 Target State / Target Path，则其可用性属于后续控制选择信息，并与当前“抓取阶段”的 Execution Chain 分开处理。

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
| S：Structure | 视觉接口、坐标映射、安全许可来源、下游接收接口、结果回写接口是否已经定义、接入并可观测 |
| D：Dynamics | 视觉结果是否仍有效，工件跟踪是否同步，许可是否被撤销，机器人或下游状态是否延迟或未更新 |
| B：Boundary | 识别置信度、工件位置、姿态、抓取区域、下游容量等是否处于预先定义的允许边界内 |

例如：

```text
视觉接口已经建立
坐标映射已经建立
视觉结果超过有效时间
```

此时可以确认结构已经建立，但当前视觉结果无法继续作为本次抓取入口的有效判定依据。

如果相应 D 判定已经定义并实际完成，可以形成：

```text
C-D：
视觉结果在动态时序有效性方面
不满足当前入口要求
```

又例如：

```text
视觉结果仍然有效
工件位置已经超出允许抓取范围
```

如果相应 B 判定已经定义并实际完成，可以形成：

```text
C-B：
工件位置超出当前抓取入口的
预定义控制边界
```

> **需要执行某项 S / D / B 判定，表示该判定属于当前入口的评价规则；CAE-SDB Result 在对应判定实际完成并获得结果后形成。**

时间信息 T 与本次使用的状态及判定结果关联保存。

关于 C / A / E 与 S / D / B 的双轴关系，可参见：

[为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)

---

# 5. Arbitration（控制仲裁）

一次 Target State Entry 中，可能同时形成多个 CAE-SDB Result，也可能同时存在关键许可、安全约束和执行链状态等入口控制条件。

例如，本次 Arbitration 的输入可以包括：

```text
CAE-SDB Result：
C-D
视觉结果失效
```

```text
关键许可：
关键安全许可成立
```

```text
执行链状态：
当前抓取阶段所需执行链
满足当前入口要求
```

另一种情况下，也可能同时形成：

```text
CAE-SDB Result：
C-D
A-D
E-B
```

Arbitration（控制仲裁）结合：

- CAE-SDB Result；
- 关键许可；
- 安全约束；
- 当前 Target State Entry 的控制规则；
- 当前入口允许选择的合法控制路径；

处理当前入口的控制优先关系。

其中，关键 A 可以构成独立必要约束。

关键安全许可未成立时，当前抓取入口不得形成允许进入抓取阶段的控制结果。

Arbitration 处理的是：

> **当前多个判定结果和控制约束同时存在时，控制上应当优先处理什么。**

---

# 6. Multipath Control（多路径控制）

Arbitration 完成后，PCN 形成当前 Target State Entry 对应的 Multipath Control。

本案例可以配置的代表性控制路径包括：

```text
Allow（允许进入）
Wait（等待）
Re-identify（重新识别）
Re-sample（重新采样）
Re-position（重新定位）
Retry（重试）
Return（回流）
异常分流
下游协调
Manual Confirm（人工确认）
Prohibit（禁止进入）
Safety Lock（安全锁定）
增强记录
```

CAE-SDB Result 经 Arbitration 与当前 Target State Entry 的合法控制路径建立控制关系。

例如，同样是：

```text
C-D
```

在不同 Target State Entry、不同控制规则和不同候选路径条件下，可以形成不同的 Multipath Control。

Return、异常分流或其他替代路径如果对应新的 Target State / Target Path，则作为当前入口的候选控制输出处理。

后续进入这些新的 Target State / Target Path 时，在其对应入口下继续进行新的状态迁移判定。

---

# 7. 当前入口控制结果

Multipath Control 形成后，需要明确当前“进入抓取阶段”这一 Target State Entry 的最终控制结果。

例如，本次状态为：

```text
Robot Ready：
成立

关键安全许可：
成立

视觉结果：
已经超过有效时间

回流路径：
可用
```

对视觉结果完成 D 判定后形成：

```text
CAE-SDB Result：
C-D

视觉结果不能继续作为
当前抓取入口的有效判定依据
```

经过 Arbitration 后，本次入口的控制结果可以整理为：

```text
当前入口控制结果：
当前抓取入口不进入

后续控制方向：
Return（回流）
```

这一步明确当前 Target State Entry 最终如何处理，以及后续进入哪一个已经选定的控制方向。

实际控制路径是否执行成功，在下一步确认。

---

# 8. 选定控制路径与 Execution Result（执行结果）

本次选定的控制路径为：

```text
选定控制路径：
Return（回流）
```

系统开始执行该控制路径：

```text
当前抓取入口不进入
    ↓
工件执行回流
    ↓
工件进入回流路径
    ↓
形成新的运行状态
```

实际执行完成后形成：

```text
Execution Result：
工件已进入回流路径
```

后续如果需要重新识别，则“进入重新识别流程”构成新的 Target State / Target Path，并在相应 Target State Entry 下继续进行新的状态迁移判定。

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
选定控制路径
↓
Execution Result
```

第 7 步确定当前入口的控制结果与后续方向。

第 8 步确认已经选定的控制路径实际执行成了什么结果。

关于状态类型循环与实际运行状态实例之间的关系，可参见：

[TPCA 中状态实例的单向性——状态类型循环与实际运行履历的区别](/zh/notes/tpca-unidirectional-state-transition/)

---

# 9. PCN Trace（状态迁移判定履历）

本次状态迁移完成控制处理后，PCN 将输入、判定、控制和执行结果关联记录为 PCN Trace。

例如：

```text
PCN：抓取入口 PCN

Current State：识别完成 / 等待抓取

Target State：抓取阶段

Target State Entry：进入抓取阶段

主要输入：
  Robot Ready = TRUE
  Safety Permission = TRUE
  Vision Result = Expired


CAE-SDB Result：C-D

关键许可：关键安全许可成立

控制仲裁结果：当前抓取入口不允许进入，选择 Return 作为后续控制方向

Multipath Control：Return（回流）

当前入口控制结果：当前抓取入口不进入

选定控制路径：Return（回流）

Execution Result：工件已进入回流路径

时间信息：T

Trace ID：PCN-PICK-XXXX
```

PCN Trace 以一次 Target State Entry 为单位，关联记录本次使用的状态、结构化判定、控制仲裁、控制路径和实际执行结果。

长期积累后，这些 Trace 可以用于：

- HMI 或上位系统的结构化显示；
- 现场问题复盘；
- 高频判定结果统计；
- 高频控制路径统计；
- 控制路径与 Execution Result 的关系比较；
- 工程修改前后比较；
- 同类自动化执行单元复用；
- 工程交接。

关于 PCN Trace 作为状态迁移判定履历的工程意义，可参见：

[为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)

---

## 案例总结

Robot Ready 表示机器人本体的局部准备状态。

本案例进一步围绕明确的 Target State Entry，把进入抓取阶段所涉及的相关状态、结构化判定、控制仲裁、控制路径和执行结果按照统一工程顺序展开：

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

自动化执行单元进入目标物理执行阶段之前，可以按照这一顺序组织一次完整的状态迁移前置控制。

不同设备和不同应用对象可以采用相同的工程分析骨架，具体变化主要体现在：

```text
相关状态，判定规则，关键许可，合法控制路径，执行结果
```

这也构成 TPCA / PCN 应用案例、PoC 和工程展开时的基本分析顺序。

---

## 进一步阅读

- [为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)
- [为什么 Ready 不够？](/zh/questions/why-ready-is-not-enough/)
- [为什么状态迁移条件需要显式化？](/zh/notes/explicit-state-transition-conditions/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)
- [为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

---

## 版本说明

本文为 TPCA / PCN 状态迁移前置控制架构在自动化执行单元中的公开案例。

- Public Case Version 1.0：2026-06-30
- Public Case Version 1.1：2026-08-20，统一 PCN、CAE-SDB Result、Arbitration、Multipath Control 与 PCN Trace 的层级表达。
- Public Case Version 1.2：2026-08-21，补充时间信息 T 与状态实例相关说明。
- Public Case Version 1.3：2026-08-25，明确 C / A / E 与 S / D / B 的双轴关系。
- Public Case Version 1.4：2026-09-10，按统一九步案例工程分析顺序重构正文，并统一当前 Target State 的状态映射、候选控制路径、入口控制结果、实际执行结果及案例辅助标签的表达方式。

作者：全野南政 / Nansei Zenno
