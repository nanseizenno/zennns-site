---
title: 技术札记
draft: false
---

技术札记用于补充 TPCA / PCN 公开体系中的专题说明，内容分为基础原则与技术定位、CAE-SDB / PCN 与系统结构、工程理解检查三个方向。

---

## 一、基础原则与技术定位

>这一组用于说明 TPCA / PCN 的基础工程认识、状态迁移原则、适用边界，以及与既有工业自动化技术和制造现场数据之间的关系。

### [为什么智能算法与物理执行控制之间，需要状态迁移前置控制？](/zh/notes/why-production-lines-still-need-deterministic-control/)

- 从智能算法的识别、预测与优化能力出发，说明为什么具体物理状态迁移入口最终仍需要形成明确的进入、保持或禁止结果，并进一步讨论状态表示、Target State Entry（目标状态入口）以及 TPCA / PCN 在其中的工程位置。

### [TPCA 中状态实例的单向性——状态类型循环与实际运行履历的区别](/zh/notes/tpca-unidirectional-state-transition/)

- 区分 State Type（状态类型）与 State Instance（状态实例）。状态类型可以形成循环，实际运行中的状态实例则沿时间方向持续生成；Recovery、Rollback、Reset、Retry、Re-entry 等处理也按进入新状态实例理解。

### [TPCA / PCN 适用场景分析](/zh/notes/tpca-pcn-applicable-scenarios/)

- 从 Target State Entry 是否明确、相关状态是否可观测、判定结果是否能够连接实际控制，以及是否能够形成 PCN Trace 四个方面，说明 TPCA / PCN 的适用条件和工程边界。

### [TPCA / PCN 与既有工业自动化技术和工程方法的关系](/zh/notes/tpca-existing-theories/)

- 说明 TPCA、PCN 与状态机、SFC、Interlock、安全控制、报警管理、FMEA、STPA、RCA、Process Mining、MES / WCS 和 AI 分析之间的工程位置与分工关系。

### [为什么 OEE 之后还需要 PCN？](/zh/notes/why-oee-pcn/)

- 说明 OEE / 生产实绩数据与 PCN Trace 的工程分工。OEE 用于观察运行实绩和损失，PCN Trace 用于记录具体 Target State Entry 上发生的判定、控制选择和执行结果，为进一步分析对应的状态迁移过程提供依据。

---

## 二、CAE-SDB、PCN 与系统结构

>这一组说明一次 Target State Entry（目标状态入口）如何形成状态映射、判定、控制和履历，以及多个 PCN 如何进一步形成系统级关系结构。

### [为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)

- 说明 C / A / E 状态变量域与 S / D / B 判定性质为什么需要分成两条轴，以及 C-S、A-D、E-B 等 CAE-SDB 判定结果如何形成并进入后续控制处理。

### [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)

- 说明一个 PCN 如何对应一个明确的 Target State Entry，并把相关状态、CAE-SDB 判定、Arbitration（控制仲裁）、Multipath Control（多路径控制）、执行结果和 PCN Trace（状态迁移判定履历）组织为一个工程责任单元。

### [多个 PCN 如何形成状态迁移前置控制网络？](/zh/notes/pcn-network-structure/)

- 说明多个 Target State Entry / PCN 如何通过状态推进、许可、资源、执行和状态更新等依赖关系形成 PCN Network（PCN 网络）。

### [为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)

- 说明 PCN Trace 与设备数据、生产数据和报警履历的区别，以及为什么一次 Target State Entry 的判定、控制选择和执行结果可以围绕同一次状态迁移持续记录、比较和分析。

---

## 三、工程理解检查

### [TPCA / PCN 工程理解检查——十个问题](/zh/notes/tpca-pcn-understanding-test/)

- 通过十个工程问题检查 Target State Entry、PCN 位置、关键 A、Execution Chain（执行链）、CAE-SDB 判定纪律、Target State 绑定、控制仲裁、PCN Trace、PCN Network 和适用边界是否理解一致。

---

## 相关栏目

### [Concepts｜核心概念](/zh/concepts/)

- 查看 TPCA、PCN、Current State（当前状态）、Target State（目标状态）、Target State Entry（目标状态入口）、C / A / E、S / D / B、CAE-SDB Result、Arbitration、Multipath Control、PCN Trace 和 PCN Network 等核心定义。

### [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

- 系统了解 TPCA / PCN 的总体工程主线、核心结构、控制关系和应用方向。

### [Engineering Questions｜工程问题](/zh/questions/)

- 从自动化执行单元、多系统协同和状态迁移设计中常见的工程问题进入 TPCA / PCN。

### [应用案例](/zh/cases/)

- 查看自动化执行单元、MES / WCS 协同停滞和生产 DX 等公开应用案例。

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开技术札记索引。

技术札记用于补充白皮书和核心概念页，不替代 TPCA / PCN 的总体定义。
