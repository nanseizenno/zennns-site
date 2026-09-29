---
title: "TPCA 中状态实例的单向性——状态类型循环与实际运行履历的区别"
summary: "说明状态类型可以表示 A → B → A 这样的循环，而实际运行中的状态实例则按 A₁ → B₁ → A₂ 的方式沿时间方向持续生成。Recovery、Rollback、Reset、Retry、Re-entry 等处理，也统一作为进入新状态实例的状态迁移来理解。"
description: "说明 TPCA 中 State Type（状态类型）与 State Instance（状态实例）的区别，以及将状态实例按时间方向持续生成的模型应用于状态迁移设计的工程意义。"
date: 2026-08-21
lastmod: 2026-09-09
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.1"
citation_url: "https://zennns.com/zh/notes/tpca-unidirectional-state-transition/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## TPCA 中状态实例的单向性

在状态机、SFC（顺序功能图）和工作流履历中，通常会区分状态类型和实际执行过程。本页把这种区分放到 TPCA 的状态迁移设计中说明。

控制程序可以重复使用同一个状态类型。例如：

```text
A → B → A
```

从状态类型关系看，这种表示没有问题。

但在实际运行履历中，前后的两个 A 不是同一个状态实例。更准确地说：

```text
A₁ → B₁ → A₂
```

`A₁` 和 `A₂` 属于同一个 State Type（状态类型）A，但发生时间和此前经历的运行过程不同，因此是两个不同的 State Instance（状态实例）。

本页讨论的重点，是把这种时间方向明确用于状态实例识别和状态迁移履历。

> **状态类型可以循环，实际运行中的状态实例沿时间方向持续生成。**

按照这一原则，Recovery（恢复）、Rollback（回退）、Reset（复位）、Retry（重试）、Re-entry（重新进入）等处理，也可以统一理解为从当前状态实例进入新的状态实例。

---

## 1. 为什么要区分 A → B → A 和 A₁ → B₁ → A₂

假设机器人在 Home 位置等待，将该状态类型定义为 A：

```text
A:
Robot Position = Home
Mode = Auto
Ready = TRUE
```

机器人开始动作后进入 B：

```text
B:
Robot Executing
Ready = FALSE
```

动作结束后，机器人再次回到 Home：

```text
Robot Position = Home
Mode = Auto
Ready = TRUE
```

从状态类型看，仍然可以表示为：

```text
A → B → A
```

但实际运行中，两个 A 之间已经发生了控制指令、执行器动作、工件变化、资源占用与释放、状态更新以及相关事件。

后一个 A 发生在更晚的时间位置，因此实际履历应区分为：

```text
A₁ → B₁ → A₂
```

其中：

```text
Type(A₁) = Type(A₂) = A
```

但：

```text
A₁ ≠ A₂
```

同一个状态类型可以再次出现，但不会重新变成过去那个状态实例。

---

## 2. State Type（状态类型）与 State Instance（状态实例）

State Type 表示系统设计中的状态类别，例如：

```text
WAIT
EXECUTE
FAULT
RECOVERY
AUTO
```

状态类型之间可以存在循环：

```text
WAIT → EXECUTE → WAIT
```

```text
AUTO → FAULT → AUTO
```

State Instance 表示实际运行中某一次具体发生的状态。

可以写成：

```text
Sᵢ = (Xᵢ, Tᵢ)
```

其中，`Xᵢ` 表示该状态实例的工程状态内容，`Tᵢ` 表示该实例所在的时间位置。

对于连续发生的状态实例：

```text
S₀ → S₁ → S₂ → ...
```

时间位置满足：

```text
T₀ < T₁ < T₂ < ...
```

即使后续状态的工程内容与之前完全相同：

```text
X₀ = X₂
```

只要：

```text
T₂ > T₀
```

就有：

```text
S₂ ≠ S₀
```

因此，状态类型可以重复使用，状态实例则随着实际运行持续生成。

---

## 3. Recovery、Rollback、Reset 等处理也是新的状态实例

控制软件中经常使用以下名称：

```text
Recovery
Rollback
Reset
Retry
Re-entry
```

这些名称可以继续作为程序名、处理名或工程术语使用。

从实际运行履历看，它们都不会把系统重新带回过去的 State Instance。

例如：

```text
AUTO₁ → FAULT₁ → RECOVERY₁ → AUTO₂
```

`AUTO₁` 和 `AUTO₂` 属于同一个状态类型 AUTO，但经过故障和恢复以后，`AUTO₂` 已经是新的状态实例。

同样：

```text
READY₁ → EXECUTE₁ → RESETTING₁ → READY₂
```

这里的 `READY₂` 也不是过去的 `READY₁`。

因此，Recovery、Rollback、Reset、Retry、Re-entry 在履历上都可以按“当前状态实例进入新的状态实例”处理。

这种表示不改变现场原有术语，只统一实际运行履历中的状态实例关系。

---

## 4. 对控制软件状态设计的作用

把状态类型循环和状态实例履历分开以后，正常处理和异常处理可以使用同一种状态迁移表达。

正常执行、故障恢复、Reset、Retry 或 Re-entry，都可以作为从当前状态实例进入新状态实例的过程记录，而不需要把 Recovery 或 Retry 理解为沿时间方向返回过去状态。

同一个状态类型多次出现时，也可以在运行履历中明确区分。

例如：

```text
WAIT₁ → EXECUTE₁ → WAIT₂
```

比单纯记录：

```text
WAIT → EXECUTE → WAIT
```

更容易确认问题发生在哪一次 WAIT，以及进入该状态之前经历了什么处理。

按照状态实例记录实际运行过程，可以把正常运行、异常处理、恢复和重试放到同一条时间序列中，便于状态组织、运行履历追踪、调试分析和日志比较。

这种设计对软件复杂度、维护性和开发效率能够带来多大改善，仍需要结合具体实现验证。

---

## 5. TPCA 中如何使用这一原则

TPCA / PCN 按实际运行中的状态实例记录状态迁移。

Target State 即使与过去出现过的 State Type 相同，实际进入后仍然形成新的 State Instance。

例如：

```text
AUTO₁ → FAULT₁ → RECOVERY₁ → AUTO₂
```

其中：

```text
Type(AUTO₁) = Type(AUTO₂)
```

但：

```text
AUTO₁ ≠ AUTO₂
```

TPCA 将这一原则同时用于正常处理、异常处理、恢复、重试和重新进入。

可以用两组关系概括：

```text
State Type（状态类型）:
A → B → A
```

```text
State Instance（状态实例）:
A₁ → B₁ → A₂
```

PCN Network（PCN 网络）可以包含状态类型上的循环；PCN Trace（状态迁移判定履历）记录实际运行中持续向前生成的状态实例和判定结果。

---

## 工程结论

状态类型和状态实例需要分开理解。

State Type（状态类型）可以形成循环：

```text
A → B → A
```

实际运行中的 State Instance（状态实例）则沿时间方向持续生成：

```text
A₁ → B₁ → A₂
```

Recovery、Rollback、Reset、Retry、Re-entry 等处理即使重新进入过去出现过的状态类型，也形成新的状态实例。

因此，TPCA / PCN 采用以下状态迁移原则：

> **状态类型可以循环，状态实例沿时间方向持续生成。**

这一原则为正常处理、异常处理、恢复和重试提供统一的状态实例记录方式，也为 PCN Trace 和 PCN Network 的运行履历提供一致的状态基础。

---

## 参考文献与外部资料

以下资料用于说明工业自动化中状态、步骤、迁移以及重复进入既有状态类型等已有工程表达。

1. **PLCopen — IEC 61131-3**  
   IEC 61131-3 中的 Sequential Function Chart（SFC，顺序功能图）使用步骤、迁移和动作表示 PLC 程序中的顺序结构。  
   https://www.plcopen.org/standards/logic/iec-61131-3/

2. **PLCopen — SFC FAQ / Structuring with SFC**  
   PLCopen 的公开资料说明，SFC 可以通过分支结构再次进入已有步骤。  
   https://www.plcopen.org/standards/logic/iec-61131-3/faqs/

3. **OMAC — PackML**  
   PackML 提供标准化的机器 / 单元状态和行为模型，用于不同设备之间统一表达运行状态。  
   https://www.omac.org/packml

---

## 文档信息

题目：TPCA 中状态实例的单向性——状态类型循环与实际运行履历的区别  
文档类型：技术札记  
版本：Public Note Version 1.1  
首次发布日期：2026-08-21  
最后更新：2026-09-09  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/tpca-unidirectional-state-transition/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
