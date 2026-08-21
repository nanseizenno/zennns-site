---
title: 技术札记
draft: false
---

技术札记用于补充 TPCA / PCN 公开体系中的专题说明。

本页按三个方向整理：

1. **TPCA / PCN 与既有理论、方法和工程机制的关系**
2. **PCN 本身的工程结构与扩展**
3. **理解测试**

如需先建立整体认识，建议先阅读 [Concepts｜核心概念](/zh/concepts/) 和 [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)。

---

## 一、TPCA / PCN 与既有理论、方法和工程机制的关系

这一组主要用于回答：

> TPCA / PCN 与现有工业自动化方法是什么关系？

> 它建立在什么工程基础上？

> 哪些问题属于既有机制，哪些问题属于状态迁移前置控制？

### [TPCA / PCN 与既有工业自动化方法和控制机制的关系](/zh/notes/tpca-existing-theories/)

说明 TPCA / PCN 与 FMEA、STPA、RCA、Process Mining、状态机、SFC、Interlock、安全控制、报警管理、MES / WCS、AI 分析及形式化验证之间的边界关系。

### [从迁移后恢复到迁移前判定](/zh/notes/pre-transition-judgment-vs-post-transition-recovery/)

从状态机、SFC 和现场异常恢复逻辑出发，区分必要的运行中恢复与可以在迁移前识别的问题，说明为什么部分控制问题应前移到目标状态入口进行判定。

### [TPCA / PCN 建立在什么工程基础上？——五个基础工程共识](/zh/notes/engineering-foundations-of-tpca-pcn/)

从状态迁移、许可约束、执行链接续、动态时序有效性和控制边界五个基础工程共识出发，说明 TPCA / PCN 建立在什么已有工程事实之上。

### [TPCA / PCN 面对已有技术分歧，它站在哪里？——三个典型工程争议](/zh/notes/engineering-positions-of-tpca-pcn/)

围绕确定性控制与 AI、集中控制与分布式自治、保守阻断与受控继续三个典型工程争议，说明 TPCA / PCN 在节点部署、控制仲裁和运行边界上的基本技术立场。

### [为什么 OEE 之后还需要 PCN？](/zh/notes/why-oee-pcn/)

说明 OEE、设备数据与 PCN 的互补关系。OEE 主要观察运行绩效和损失，PCN 则处理一次明确的状态迁移为什么能够成立，或者为什么没有成立。

---

## 二、PCN 本身的工程结构与扩展

这一组主要用于回答：

> PCN 到底是什么？

> 为什么要把状态迁移入口独立出来？

> 一个 PCN 如何判定、控制、记录并进一步形成网络？

### [为什么状态迁移条件必须显式化？](/zh/notes/explicit-state-transition-conditions/)

说明为什么应把隐含在程序、接口、许可、设备联动和工程师经验中的状态迁移条件，转化为可设计、可检查、可记录和可改善的工程对象。

### [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)

说明一个 PCN 如何围绕明确的状态迁移入口，组织当前状态、目标状态、多源状态信号、C/A/E 状态映射、S/D/B 判定、CAE-SDB 判定结果、控制仲裁、多路径控制和 PCN Trace。

### [为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)

说明 PCN Trace 与设备数据、生产数据和报警履历的区别，以及为什么“一次完整的状态迁移判定”可以成为独立记录、比较和复盘的工程数据对象。

### [TPCA / PCN 适用场景分析](/zh/notes/tpca-pcn-applicable-scenarios/)

说明什么样的对象适合设置 PCN，什么样的问题不应纳入 PCN，并整理自动化执行单元、MES / WCS、群控协同、生产 DX 和人工确认等场景中的应用边界。

### [多个 PCN 如何形成状态迁移前置控制网络？](/zh/notes/pcn-network-structure/)

说明多个 PCN 如何按照实际状态迁移关系连接，并从单个目标状态入口进一步形成 PCN 网络。

---

## 三、理解测试

这一组不再增加新的概念，用于检查是否真正理解 TPCA / PCN 的工程逻辑。

### [你真的理解 TPCA / PCN 了吗？——十个工程问题](/zh/notes/tpca-pcn-understanding-test/)

通过十个具体工程问题，检查是否能够正确理解状态迁移入口、PCN、C/A/E、S/D/B、CAE-SDB 判定结果、多路径控制和 PCN Trace 之间的关系。

---

## 相关栏目

### [Concepts｜核心概念](/zh/concepts/)

查看 TPCA、PCN、CAE-SDB、C/A/E、S/D/B、控制仲裁、多路径控制、PCN Trace 和 PCN Network 等核心术语定义。

### [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

系统了解 TPCA / PCN 的总体工程主线、核心结构和典型应用方向。

### [Engineering Questions｜工程问题](/zh/questions/)

从 Ready、Waiting、任务执行、多系统协同和状态迁移设计等制造现场问题进入 TPCA / PCN。

### [应用案例](/zh/cases/)

查看自动化执行单元、协同停滞诊断和生产 DX 等公开应用案例。

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开技术札记索引。

技术札记用于补充白皮书和核心概念页，不替代 TPCA / PCN 的总体定义。
