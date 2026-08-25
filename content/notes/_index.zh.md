---
title: 技术札记
draft: false
---

技术札记用于补充 TPCA / PCN 公开体系中的专题说明。

本页按四个方向整理：

1. **TPCA 的基础原则与技术定位**
2. **CAE-SDB 与 PCN 的工程结构和系统扩展**
3. **工程价值与适用边界**
4. **理解测试**

如需先建立整体认识，建议先阅读：

- [Concepts｜核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

---

## 一、TPCA 的基础原则与技术定位

这一组主要回答：

> TPCA 建立在什么工程认识之上？

> 它如何理解真实系统中的状态迁移？

> 它与既有工业自动化方法是什么关系？

### [TPCA 的状态迁移单向性——为什么真实工程系统不存在状态回退？](/zh/notes/tpca-unidirectional-state-transition/)

从真实工程系统的时间单向性出发，说明状态内容可以再次相同，但状态实例因时间分量不同而不可能回到过去；并据此重新解释 Rollback、Recovery、复归、回流和多路径控制。

### [TPCA / PCN 建立在什么工程基础上？——五个基础工程共识](/zh/notes/engineering-foundations-of-tpca-pcn/)

从状态迁移、许可约束、执行链接续、动态时序有效性和控制边界五个基础工程共识出发，说明 TPCA / PCN 建立在什么已有工程事实之上。

### [TPCA / PCN 与既有工业自动化方法和控制机制的关系](/zh/notes/tpca-existing-theories/)

说明 TPCA / PCN 与状态机、SFC、Interlock、安全控制、报警管理、FMEA、STPA、RCA、Process Mining、MES / WCS、AI 分析及形式化验证之间的边界关系。

### [TPCA / PCN 面对已有技术分歧，它站在哪里？——三个典型工程争议](/zh/notes/engineering-positions-of-tpca-pcn/)

围绕确定性控制与 AI、集中控制与分布式自治、保守阻断与受控继续三个典型工程争议，说明 TPCA / PCN 在运行时控制、节点部署和控制仲裁方面的基本技术立场。

---

## 二、CAE-SDB 与 PCN 的工程结构和系统扩展

这一组主要回答：

> 为什么一次目标状态入口需要被独立组织和判定？

> CAE-SDB 为什么由两个不同维度的分析轴构成？

> PCN 如何完成判定、控制和记录？

> 多个 PCN 如何进一步形成系统级结构？

### [为什么是 CAE-SDB？——状态迁移功能角色与状态验证的双轴结构](/zh/notes/why-cae-sdb/)

从 Target State Entry 出发，说明 CAE 与 SDB 并不是两套状态分类。CAE 用于识别相关状态在一次状态迁移中的功能角色：C 回答具不具备，A 回答允不允许，E 回答接不接得住；SDB 则分别判断相关状态的结构完整性、动态时序有效性以及相对于预定义边界的位置关系，并形成 CAE-SDB Result。

### [为什么状态迁移条件必须显式化？](/zh/notes/explicit-state-transition-conditions/)

说明为什么应将分散在程序、接口、许可、设备联动和工程师经验中的状态迁移判断，围绕明确的目标状态入口转化为可设计、可检查、可记录和可改善的工程结构。

### [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)

说明一个 PCN 如何围绕明确的目标状态入口，组织当前状态、目标状态、多源状态信号、C / A / E 状态映射、S / D / B 判定、CAE-SDB Result、控制仲裁、多路径控制和 PCN Trace。

### [多个 PCN 如何形成状态迁移前置控制网络？](/zh/notes/pcn-network-structure/)

说明多个 PCN 如何按照实际状态迁移关系以及许可、资源和执行依赖关系连接，并从单个目标状态入口进一步形成 PCN Network。

### [为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)

说明 PCN Trace 与设备数据、生产数据和报警履历之间的区别，以及为什么一次完整的目标状态进入判定可以成为独立记录、比较和复盘的工程数据对象。

---

## 三、工程价值与适用边界

这一组主要回答：

> TPCA / PCN 适合解决什么问题？

> 它与已有运行指标和工程数据是什么关系？

> 哪些对象值得设置 PCN，哪些问题不适合纳入？

### [TPCA / PCN 适用场景分析](/zh/notes/tpca-pcn-applicable-scenarios/)

说明什么样的目标状态入口适合设置 PCN，什么样的问题不应纳入 PCN，并整理自动化执行单元、MES / WCS、群控协同、生产 DX 和人工确认等场景中的应用边界。

### [为什么 OEE 之后还需要 PCN？](/zh/notes/why-oee-pcn/)

说明 OEE、设备数据与 PCN 的互补关系。OEE 主要用于观察运行绩效和损失，PCN 则围绕一次明确的目标状态入口，记录为什么可以进入、等待、阻断或分流。

---

## 四、理解测试

这一组不再增加新的概念，用于检查是否真正理解 TPCA / PCN 的工程逻辑。

### [你真的理解 TPCA / PCN 了吗？——十个工程问题](/zh/notes/tpca-pcn-understanding-test/)

通过十个具体工程问题，检查是否能够正确理解目标状态入口、PCN、C / A / E、S / D / B、CAE-SDB Result、控制仲裁、多路径控制、PCN Trace 和 PCN Network 之间的关系。

---

## 相关栏目

### [Concepts｜核心概念](/zh/concepts/)

查看 TPCA、PCN、Current State、Target State、C / A / E、S / D / B、CAE-SDB Result、控制仲裁、多路径控制、PCN Trace 和 PCN Network 等核心术语定义。

### [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

系统了解 TPCA / PCN 的总体工程主线、核心结构和典型应用方向。

### [Engineering Questions｜工程问题](/zh/questions/)

从 Ready、Waiting、任务执行、多系统协同和状态迁移设计等制造现场问题进入 TPCA / PCN。

### [应用案例](/zh/cases/)

查看自动化执行单元、MES / WCS 协同停滞和生产 DX 跨系统状态迁移等公开应用案例。

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开技术札记索引。

技术札记用于补充白皮书和核心概念页，不替代 TPCA / PCN 的总体定义。
