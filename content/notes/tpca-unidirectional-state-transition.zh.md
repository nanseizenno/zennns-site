---
title: "TPCA 的状态迁移单向性——为什么真实工程系统不存在状态回退？"
summary: "从真实工程系统的时间单向性出发，说明状态内容可以再次相同，但状态实例因时间分量不同而不可能回到过去；并据此解释 TPCA 为什么只采用从 Current State 到新 Target State 的单向状态迁移。"
description: "提出 TPCA 的状态迁移单向性观点：实际运行状态由工程状态内容与时间分量共同确定，后续状态即使与历史状态具有相同内容，也属于新的状态实例。由此重新解释 Rollback、Recovery、复归、回流和多路径控制，并说明单向状态模型对 PCN、PCN Trace、PCN Network 和控制软件架构的意义。"
date: 2026-08-21
lastmod: 2026-08-21
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.0"
citation_url: "https://zennns.com/zh/notes/tpca-unidirectional-state-transition/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## TPCA 的状态迁移单向性

自动化系统通常使用状态机、SFC、顺序控制和设备状态模型描述系统运行过程。

在这些模型中，同一个状态名称或步骤可以被重复进入。

例如：

```text
A
→ B
→ A
```

从控制程序或状态图角度看，这种表达是成立的。

但如果观察真实工程系统实际发生的状态演化，前后的两个 `A` 并不是同一个状态实例。

原因很简单：

> **时间已经不同。**

系统经历过 B 以后，即使设备位置、模式、Ready、变量值等再次恢复到与原来 A 相同的内容，新的状态仍然发生在更晚的时间。

因此，TPCA 对实际运行状态采用一个基本观点：

> **状态内容可以再次相同，状态实例不能回到过去。**

由此得到 TPCA 的状态迁移单向性：

> **真实工程系统中的状态迁移始终沿时间方向发生。系统没有状态回退，只有从当前状态继续进入新的目标状态。**

---

## 1. 状态不仅包含内容，还包含时间分量

如果只按照控制程序中的状态名称理解系统，可以写成：

```text
State = X
```

其中 `X` 表示当前工程状态内容。

例如：

```text
Robot Position = Home
Mode = Auto
Ready = TRUE
```

但对于实际运行中的一次具体状态，仅有这些内容还不足以唯一确定状态实例。

TPCA 可以将实际状态表示为：

```text
Sᵢ = (Xᵢ, Tᵢ)
```

其中：

- `Xᵢ`：该时刻的工程状态内容；
- `Tᵢ`：该状态实例所处的时间位置。

对于连续发生的实际状态：

```text
S₀
→ S₁
→ S₂
→ ...
```

其时间关系始终满足：

```text
T₀ < T₁ < T₂ < ...
```

因此，即使后续某个状态的工程内容与历史状态完全相同：

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

也就是说：

> **工程状态内容可以重复，实际状态实例不会重复。**

---

## 2. A → B → A 在真实运行中只能是 A → B → C

假设设备初始处于状态 A：

```text
A:
Robot Position = Home
Mode = Auto
Ready = TRUE
```

随后进入状态 B：

```text
B:
Robot Executing
Ready = FALSE
```

完成相关动作以后，机器人重新回到 Home，系统再次显示：

```text
Robot Position = Home
Mode = Auto
Ready = TRUE
```

传统状态图可以再次把这一状态标记为 A：

```text
A
→ B
→ A
```

TPCA 在描述**实际状态实例**时，不采用这种表示。

真实运行过程应表示为：

```text
A
→ B
→ C
```

其中：

```text
X_C = X_A
```

但：

```text
T_C > T_A
```

因此：

```text
C ≠ A
```

C 是新的状态。

它只是与 A 具有相同或相似的工程状态内容。

从 A 到 C 之间，系统已经实际发生过：

- 时间推进；
- 控制指令；
- 执行器动作；
- 工件或设备变化；
- 资源占用与释放；
- 状态刷新；
- 系统事件；
- 运行履历。

这些已经发生的过程不会因为 C 与 A 的状态内容相同而消失。

因此：

> **状态类型可以再次出现，状态实例只能继续向前生成。**

![TPCA 的状态迁移单向性：状态类型可以循环，状态实例只能向前](/images/tpca/11-tpca-unidirectional-state-transition.zh.png)

图：传统状态模型可以用 `A → B → A` 表示状态类型的再次进入；在 TPCA 的实际状态实例视角下，后续状态即使与历史状态具有相同的工程状态内容，只要时间分量不同，就属于新的状态实例。状态类型可以再次出现，实际状态实例始终沿时间方向继续生成。


---

## 3. TPCA 不需要“回撤”这一基本控制概念

一旦接受状态实例具有时间分量，就会得到一个直接结论：

> **真实工程系统不存在返回历史状态实例的控制。**

工程中常见的：

```text
Rollback
Recovery
Return
Reset
Restore
复归
回流
重新投入
```

仍然可以作为程序名称、控制路径名称或现场操作术语使用。

但从 TPCA 的状态迁移视角看，它们都不是反向迁移。

例如：

```text
A：正常运行
→
B：执行异常
→
C：安全停止
→
D：复归准备
→
E：重新进入正常运行
```

即使：

```text
X_E = X_A
```

仍然有：

```text
T_E > T_A
```

因此：

```text
E ≠ A
```

整个实际过程始终是：

```text
A
→ B
→ C
→ D
→ E
```

没有任何一步真正沿时间方向返回 A。

所以在 TPCA 中：

> **Rollback 不是回到历史状态，而是进入一个新的 Target State；这个 Target State 的工程状态内容可以与某个历史状态相同。**

Recovery、复归、回流和重新投入也是同样的关系。

从架构层看，它们都可以统一为：

```text
Current State
→ Target State
```

---

## 4. 异常不会产生“反向过程”，而是形成新的 Current State

运行过程中发生异常时，传统工程语言经常表示为：

```text
Normal
→ Fault
→ Recovery
→ Normal
```

TPCA 不需要把 Recovery 建立为与正常状态迁移相反的另一套时间过程。

异常发生以后，首先发生的是：

> **真实系统状态已经改变。**

例如机器人抓取过程中真空丢失：

```text
S₁：
抓取执行中
```

异常发生后形成新的现实状态：

```text
S₂：
抓取执行已中断
+
工件保持状态不可确认
+
当前设备与安全状态已更新
```

此时：

```text
Current State = S₂
```

系统接下来需要重新确定：

```text
Target State = ?
```

候选目标状态可能是：

- 安全保持；
- 异常排出；
- 工件释放；
- 退避位置；
- 人工确认；
- 重新识别；
- 其他预先定义的工程状态。

随后仍然按照同一条状态迁移关系处理：

```text
Current State
→ Target State Entry
→ PCN
→ Selected Target State
```

因此：

> **异常并没有改变状态迁移的方向。**

它只是形成新的 Current State，并使系统需要重新确定下一 Target State。

正常运行、异常处置、复归和重新投入，在 TPCA 中遵循同一种状态迁移结构。

---

## 5. Multipath Control 本质上是下一 Target State 的选择

从状态迁移单向性的角度看，Multipath Control 也可以获得更统一的解释。

通常，多路径控制可以表现为：

- Allow；
- Wait；
- Recheck；
- Re-identify；
- Return；
- Degrade；
- Manual Confirm；
- Prohibit；
- Safety Lock；
- 其他控制路径。

这些名称表示不同的工程处理语义。

但从状态迁移本质看，它们最终都在回答：

> **当前状态下一步应该进入哪个 Target State？**

例如当前状态为：

```text
Current State:
抓取失败后的对象保持不确定状态
```

可以存在多个候选目标状态：

```text
T₁ = 安全保持
T₂ = 异常排出
T₃ = 重新识别
T₄ = 人工确认
T₅ = 回流状态
```

经过：

```text
CAE-SDB Result
→ Arbitration
→ Multipath Control
```

最终确定：

```text
Selected Target State = T₃
```

然后发生新的状态迁移：

```text
Current State
→ T₃
```

如果选择回流，同样只是：

```text
Current State
→ T₅
```

并不存在一个特殊的“反方向”。

因此，从 TPCA 的单向状态模型看：

> **Multipath Control 的本质，是根据当前判定结果确定下一目标状态。**

所谓正常路径、回流路径、降级路径、人工确认路径或安全路径，只是候选 Target State 的工程用途不同。

---

## 6. PCN 的作用因此更加明确

TPCA 的核心命题是：

> **一次明确的目标状态入口，应当成为可以被独立设计、判定、控制和记录的工程对象。**

状态迁移单向性进一步说明了为什么这个入口重要。

因为一旦状态迁移实际发生：

```text
Sᵢ
→ Sᵢ₊₁
```

系统就已经进入新的时间位置：

```text
Tᵢ₊₁ > Tᵢ
```

这次状态迁移不能被真正撤销。

即使后续通过新的状态迁移重新形成相同的工程状态内容，也已经是另一个状态实例。

因此，PCN 部署在：

```text
Current State
    ↓
Target State Entry
    ↓
   PCN
    ↓
Target State
```

其工程意义不是简单“提前检查一个条件”。

而是：

> **在真实状态实例发生变化之前，完成本次目标状态入口所需要的判定和控制选择。**

这就是 Pre-Control 的基础意义。

---

## 7. PCN Trace 记录的是单向生成的状态历史

如果系统只记录当前状态内容：

```text
Robot Position = Home
Mode = Auto
Ready = TRUE
```

就无法判断这个状态是：

```text
A：
任务尚未开始
```

还是：

```text
C：
已经执行
→ 发生异常
→ 完成后续状态迁移
→ 再次形成 Home / Auto / Ready
```

A 与 C 的工程状态内容可以完全相同：

```text
X_A = X_C
```

但：

```text
T_A ≠ T_C
```

因此它们是两个不同的状态实例。

PCN Trace 进一步记录：

```text
S₀
→ S₁
→ S₂
→ S₃
→ ...
```

以及每一次状态迁移中的：

- Current State；
- Target State；
- 参与判定的状态；
- CAE-SDB Result；
- Arbitration Result；
- Multipath Control；
- Execution Result；
- Timestamp；
- Trace ID。

因此：

> **Current State 描述系统现在是什么。**

> **PCN Trace 描述系统如何沿时间方向成为现在。**

状态内容可以再次出现。

状态迁移历史不会回到过去。

---

## 8. PCN Network 可以有拓扑循环，但运行轨迹只有单向序列

这里需要区分两类对象。

### 状态类型关系

在系统设计阶段，可以存在：

```text
AUTO
→ FAULT
→ AUTO
```

或者：

```text
WAIT
→ EXECUTE
→ WAIT
```

这些关系描述的是：

> 哪些状态类型之间允许发生迁移。

因此，状态类型关系可以存在循环。

---

### 实际运行状态实例

真实运行时则只能形成：

```text
S₀
→ S₁
→ S₂
→ S₃
→ ...
```

并满足：

```text
T₀ < T₁ < T₂ < T₃ < ...
```

例如：

```text
A：AUTO，T₁
→
B：FAULT，T₂
→
C：AUTO，T₃
```

虽然：

```text
Type(C) = Type(A)
```

但：

```text
C ≠ A
```

因此：

> **PCN Network 的状态类型拓扑可以出现循环，实际运行中的状态实例序列始终沿时间单向生成。**

PCN Network 描述可发生的目标状态入口及其工程关系。

PCN Trace 记录实际发生的单向状态迁移序列。

二者不能混为一谈。

---

## 9. 单向状态模型对控制软件架构的意义

传统自动化软件中，经常分别设计：

```text
Normal Logic
Fault Logic
Rollback Logic
Recovery Logic
Reset Logic
Return Logic
```

这些逻辑在具体工程中有其作用。

但从 TPCA 的状态迁移单向性看，它们不需要对应不同方向的状态模型。

所有控制都可以统一为：

```text
Current State
→ Candidate Target States
→ PCN
→ Arbitration
→ Selected Target State
→ State Transition
```

这样，正常执行、异常处置、复归、回流、降级和重新投入可以使用同一个状态迁移语义：

> **从当前真实状态出发，选择下一目标状态。**

这种统一具有一个值得进一步验证的软件工程意义：

> **它有望减少控制软件中的特殊状态语义，使不同控制场景使用同一种状态迁移模型。**

这里减少的首先不是代码行数，而是控制概念的种类。

例如：

- 不再需要把 Rollback 理解为反向状态迁移；
- 不需要为 Recovery 建立另一种时间方向；
- 异常以后仍然使用 Current State → Target State；
- Multipath Control 统一为下一目标状态选择；
- PCN Trace 与实际状态迁移序列天然一致。

因此，TPCA 的单向状态模型有望使复杂控制软件更容易进行：

- 状态组织；
- 路径设计；
- 控制仲裁；
- 履历记录；
- 调试分析；
- 模块复用。

其实际软件复杂度改善程度，需要结合具体实现进一步验证。

但在架构语义上，TPCA 只保留一个方向：

> **Current State → Target State。**

---

## 工程结论

TPCA 的状态迁移单向性可以归结为三个基本命题。

### 1. 状态具有时间分量

实际状态可以表示为：

```text
Sᵢ = (Xᵢ, Tᵢ)
```

即使两个状态具有相同工程内容：

```text
Xᵢ = Xⱼ
```

只要：

```text
Tᵢ ≠ Tⱼ
```

它们就是不同的状态实例。

---

### 2. 状态实例只能沿时间方向继续生成

对于实际发生的连续状态迁移：

```text
Sᵢ
→ Sᵢ₊₁
```

始终满足：

```text
Tᵢ₊₁ > Tᵢ
```

因此，真实运行过程只有向前迁移。

---

### 3. TPCA 不需要状态回撤

所谓：

```text
Rollback
Recovery
Return
Reset
复归
回流
重新投入
```

本质上都只是：

```text
Current State
→ New Target State
```

新的 Target State 可以与历史状态具有相同的工程状态内容，但由于时间分量不同，它仍然是新的状态实例。

因此：

> **系统没有回退，只有继续迁移。**

也可以进一步表述为：

> **状态类型可以循环，状态实例只能向前。**

这使 TPCA 可以用统一的状态迁移模型解释正常执行、异常处置、复归、回流、降级和重新投入，并为 PCN、Multipath Control、PCN Trace 和 PCN Network 提供统一的状态基础。

---

## 参考文献与外部依据

以下资料用于说明传统工业自动化中已经广泛使用状态、步骤、迁移和可重复进入状态等工程表达。

这些资料用于建立本文的技术对照背景，不构成 TPCA 状态迁移单向性的理论来源。

1. **PLCopen — IEC 61131-3**  
   IEC 61131-3 中的 Sequential Function Chart（SFC）用于通过步骤、迁移和动作组织 PLC 程序中的顺序结构。  
   https://www.plcopen.org/standards/logic/iec-61131-3/

2. **PLCopen — SFC FAQ / Structuring with SFC**  
   PLCopen 的公开资料说明，SFC 可以通过显式分支跳回先前步骤，包括从序列末端返回初始步骤。这说明工程状态图和顺序控制结构可以重复进入既有步骤，而本文进一步区分状态类型复用与实际状态实例。  
   https://www.plcopen.org/standards/logic/iec-61131-3/faqs/

3. **OMAC — PackML**  
   PackML 提供标准化机器 / 单元状态和行为模型，用于形成跨设备一致的运行状态表达。  
   https://www.omac.org/packml

---

## 文档信息

题目："TPCA 的状态迁移单向性——为什么真实工程系统不存在状态回退？"  
文档类型：技术札记  
版本：Public Note Version 1.0  
首次发布日期：2026-08-21  
最后更新：2026-08-21  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/tpca-unidirectional-state-transition/
