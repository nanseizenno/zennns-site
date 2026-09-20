---
title: "技术札记"
draft: false
ShowReadingTime: false
---

技术札记用于补充 TPCA / PCN 公开体系中的专题说明。

---

## 一、基础原则与技术定位

> 说明 TPCA / PCN 的基础工程认识、适用边界及与既有技术的关系。

### [为什么智能算法与物理执行控制之间，需要状态迁移前置控制？](/zh/notes/why-production-lines-still-need-deterministic-control/)

- 说明智能算法与明确状态迁移控制之间的工程分工，以及目标状态入口和 TPCA / PCN 的位置。

### [TPCA 中状态实例的单向性——状态类型循环与实际运行履历的区别](/zh/notes/tpca-unidirectional-state-transition/)

- 说明状态类型可以循环，而实际运行中的状态实例沿时间方向持续生成。

### [TPCA / PCN 适用场景分析](/zh/notes/tpca-pcn-applicable-scenarios/)

- 从目标状态入口、状态可观测性、控制连接和状态迁移判定履历四个方面说明适用条件和工程边界。

### [TPCA / PCN 与既有工业自动化技术和工程方法的关系](/zh/notes/tpca-existing-theories/)

- 说明 TPCA / PCN 与既有自动化技术、工程方法及数据分析方法之间的工程分工。

### [为什么 OEE 之后还需要 PCN？](/zh/notes/why-oee-pcn/)

- 说明 OEE / 生产实绩数据与状态迁移判定履历在观察运行结果和记录状态迁移过程上的不同作用。

---

## 二、状态迁移、CAE-SDB 与 PCN 结构

> 说明目标状态入口如何形成状态映射、判定、控制和履历，并进一步连接多个 PCN。

### [为什么是 CAE-SDB？——目标状态入口前的双轴结构化分析方法](/zh/notes/why-cae-sdb/)

- 说明 C / A / E 与 S / D / B 的双轴结构，以及 CAE-SDB 判定结果如何形成。

### [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)

- 说明 PCN 如何围绕一个明确目标状态入口组织状态、判定、控制、执行和履历。

### [多个 PCN 如何形成状态迁移前置控制网络？](/zh/notes/pcn-network-structure/)

- 说明多个 PCN 如何通过状态、许可、资源和执行依赖形成系统级关系网络。

### [为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)

- 说明状态迁移判定履历与一般运行日志、报警履历和生产数据之间的区别。

---

## 三、工程数据、案例证据与方法评价

> 说明状态迁移数据如何形成，以及工程方法的结构价值如何评价。

### [状态迁移如何形成可分析的工程数据？——从目标状态入口、CAE-SDB 到 PCN Trace](/zh/notes/how-state-transition-becomes-engineering-data/)

- 说明一次真实状态迁移如何形成具有明确判定语义、可比较和可追溯的工程数据。

### [工程方法评价中的结构有效性与案例证据](/zh/notes/engineering-method-structural-validity/)

- 说明结构有效性、案例证据和方法使用前后信息结构差异之间的关系及其评价边界。

---

## 四、工程理解检查

> 用于检查 TPCA / PCN 核心概念是否理解一致。

### [TPCA / PCN 工程理解检查——十个问题](/zh/notes/tpca-pcn-understanding-test/)

- 通过十个工程问题检查目标状态入口、PCN、CAE-SDB、控制、履历和适用边界是否理解一致。

---

## 相关栏目

### [核心概念](/zh/concepts/)

- 查看 TPCA / PCN 主要概念和固定定义。

### [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

- 系统了解 TPCA / PCN 的总体工程结构。

### [工程问题](/zh/questions/)

- 从典型工程问题进入 TPCA / PCN。

### [应用案例与工程价值](/zh/cases/)

- 查看三个公开案例及方法使用前后的工程信息对照。

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开技术札记索引。

技术札记用于补充白皮书和核心概念页，不替代 TPCA / PCN 的总体定义。
