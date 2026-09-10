---
title: "应用案例"
draft: false
ShowReadingTime: false
---

这里整理 TPCA / PCN 在不同工程对象中的公开说明案例。

### [自动化执行单元前置判定案例](/zh/cases/automation-execution-unit-pre-control/)

以视觉识别输送线机器人单元为代表例，围绕“进入抓取阶段”这一 Target State Entry，说明视觉、机器人、安全、输送带、下游承接和上位系统状态如何进入 C / A / E 映射与 S / D / B 判定，并进一步连接 Arbitration、Multipath Control、当前入口控制结果、执行结果和 PCN Trace。

### [MES / WCS 协同停滞诊断模块案例](/zh/cases/collaborative-stagnation-diagnosis/)

以制造现场协同停滞为对象，说明 MES、WCS、搬送主体、站点、资源、许可和下游状态如何围绕“进入可持续协同执行状态”进行前置判定，并结合群体指标、群体停滞识别和停滞结构分型，经 Arbitration 形成 Multipath Control、当前入口控制结果、执行结果和 PCN Trace。

### [制造 DX 状态迁移条件设计与履历分析案例](/zh/cases/production-dx-state-transition/)

以“自动加工完成 → 人工作业单元组装开始”为代表状态迁移，说明自动加工设备、MES、质量系统、部件搬送与供给、作业人员资格、单元设备、治具工具以及后续检测和结果回写等状态，如何围绕同一个 Target State Entry 进行结构化判定，并形成可判定、可控制、可记录、可复盘的状态迁移工程结构。

## 九步工程分析顺序

以下九个步骤来自 [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)，作为公开案例的统一工程展开顺序。

| 步骤 | 简要说明 |
|---|---|
| **1. Current State** | 明确本次状态迁移从什么状态或阶段开始。 |
| **2. Target State / Target State Entry** | 明确准备进入什么目标状态，以及需要进行前置判定的目标状态入口。 |
| **3. PCN：相关状态获取 + C / A / E Mapping** | 获取与本次状态迁移直接相关的多源状态，并按照 Condition、Authority、Execution Chain 进行状态映射。 |
| **4. S / D / B Evaluation** | 从结构完整性、动态时序有效性和控制边界三个方面进行判定，形成 CAE-SDB Result，并保留时间信息 T。 |
| **5. Arbitration** | 处理多个判定结果、关键许可和控制约束之间的优先关系。 |
| **6. Multipath Control** | 输出经控制仲裁确定的多路径控制。 |
| **7. 当前入口控制结果** | 明确本次 Target State Entry 的控制结果，例如允许进入、暂不进入、禁止进入或转入已确定的后续控制路径。 |
| **8. 选定控制路径与 Execution Result** | 由相应执行主体执行已确定的控制路径，并记录实际 Execution Result（执行结果）。 |
| **9. PCN Trace** | 将本次状态、判定、控制和执行结果关联记录为状态迁移判定履历。 |

不同应用可以在九步主链内部加入本领域需要的分析。例如，制造现场协同停滞案例在第 4 步进一步加入群体指标、群体停滞识别和停滞结构分型，但整体工程顺序保持一致。

---

三个案例使用同一套工程分析顺序，各案例在九步主链内保留与具体工程对象相对应的专业分析内容。

本文属于 TPCA / PCN 状态迁移前置控制体系的公开应用案例索引。
