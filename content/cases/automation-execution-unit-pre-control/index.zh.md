---
title: "自动化执行单元前置判定案例"

summary: "以视觉识别输送线机器人单元为代表例，围绕“进入抓取阶段”这一目标状态入口，按照统一九步工程顺序展示 PCN 如何完成状态获取、CAE-SDB 判定、控制仲裁、多路径控制、后续状态迁移与状态迁移判定履历记录。"

description: "公开说明 TPCA / PCN 在自动化执行单元中的应用方式。以机器人进入抓取阶段为例，用一个完整运行实例展示当前状态、目标状态入口、C / A / E 状态映射、S / D / B 判定、控制仲裁、多路径控制、执行结果和状态迁移判定履历之间的实际连接关系。"

date: 2026-06-30
lastmod: 2026-09-20

author: "全野南政 / Nansei Zenno"

document_type: "公开案例"
case_type: "自动化执行单元层"

version: "Public Case Version 1.5"

citation_title: "自动化执行单元前置判定案例：为什么机器人已经就绪，仍不足以进入抓取阶段"
citation_url: "https://zennns.com/zh/cases/automation-execution-unit-pre-control/"

draft: false
weight: 1

ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## 为什么机器人已经就绪，仍不足以进入抓取阶段

> 应用层级：自动化执行单元层  
> 代表对象：视觉识别输送线机器人单元

**建议引用：**

```text
全野南政 / Nansei Zenno，《自动化执行单元前置判定案例：为什么机器人已经就绪，仍不足以进入抓取阶段》，公开案例，Public Case Version 1.5，2026-09-20，https://zennns.com/zh/cases/automation-execution-unit-pre-control/
```

视觉识别输送线机器人单元中，现场可能看到这样的状态：

```text
Robot Ready        = TRUE
Vision Result      = OK
Safety Permission  = TRUE
Downstream Ready   = TRUE

Robot Motion       = STOP
```

从单个系统看，各项状态似乎都没有明显异常。

但机器人仍然没有开始抓取。

问题在于，Robot Ready、Vision Result、Safety Permission 和 Downstream Ready 分别来自不同设备或系统。它们是否能够共同支持**当前这一时刻进入抓取阶段**，还需要放到同一个目标状态入口中判断。

本案例以“进入抓取阶段”为 Target State Entry（目标状态入口），沿统一九步工程顺序说明 PCN 如何取得相关状态、形成 CAE-SDB 判定结果，并继续连接控制仲裁、多路径控制、后续状态迁移和状态迁移判定履历。

九步顺序为：

1. 当前状态
2. 目标状态 / 目标状态入口
3. PCN：相关状态获取与 C / A / E 状态映射
4. S / D / B 判定与 CAE-SDB 结果 + T
5. 控制仲裁
6. 多路径控制
7. 当前入口控制结果
8. 后续目标状态入口与执行结果
9. 状态迁移判定履历

基础概念可参见：

- [核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

---

## 案例对象

本案例以视觉识别输送线机器人单元为代表对象，并假设 PCN 由 PLC 内的控制逻辑实现。

单元主要包含：

- 输送带；
- 工件检测；
- 视觉识别系统；
- 机器人；
- 夹爪 / 真空末端执行机构；
- 安全系统；
- 正常投放位；
- 回流路径；
- 上位系统。

其中，与“进入抓取阶段”直接有关的状态分别来自视觉、机器人、安全、输送、下游和上位系统。

![视觉识别输送线机器人单元前置控制示意图](/images/tpca/06-pcn-pick-flow.png)

图：PCN 在机器人进入抓取阶段前取得与当前目标状态入口有关的多源状态，并根据判定结果形成控制路径。

以下时间和值用于说明公开案例中的一次示例运行关系，不代表特定真实项目参数。

---

# 1. 当前状态 / 当前阶段

当前工件已经完成视觉识别，但机器人尚未执行抓取。

当前状态为：

```text
识别完成 / 等待抓取
```

示例运行状态：

```text
Workpiece Present  = TRUE
Vision Result      = OK
Robot Ready        = TRUE
Robot Motion       = STOP
```

工件已经进入本次抓取流程，视觉系统也已经产生本周期识别结果。

此时系统正在等待是否允许从“识别完成 / 等待抓取”进入“抓取阶段”。

这构成本次状态迁移的起点。

---

# 2. 目标状态 / 目标状态入口

本次目标状态为：

```text
抓取阶段
```

对应的目标状态入口为：

```text
进入抓取阶段
```

PCN 设置在当前状态与这一目标状态入口之间。

机器人真正开始动作之前，PCN 需要完成本次入口所需的状态获取、映射、判定与控制。

![PCN 在目标阶段入口前的位置关系图](/images/tpca/07-pcn-position-before-target-stage.png)

图：PCN 在抓取动作真正开始之前，对“进入抓取阶段”这一目标状态入口进行前置判定。

---

# 3. PCN：相关状态获取与 C / A / E 状态映射

PCN 只取得与当前“进入抓取阶段”直接相关的状态，并根据这些状态在本次状态迁移中的工程作用进行 C / A / E Mapping。

| 代表状态 | 状态映射 |
|---|---|
| 工件存在、位置、姿态、视觉识别结果 | C：条件状态 |
| 安全许可、区域许可、上位系统许可 | A：许可状态 |
| 机器人就绪、机器人路径、夹爪 / 真空状态、正常投放位接收状态 | E：执行链状态 |

本次示例重点使用：

- 视觉结果：C；
- 安全许可：A；
- 机器人就绪：E 的相关输入；
- 正常投放位接收状态：E。

这里，`Robot Ready = TRUE` 只是当前抓取执行链中的一个相关状态。

它不能单独说明：

```text
进入抓取阶段 = 允许
```

还需要确认视觉结果是否属于当前对象、是否仍在有效时间内，必要许可是否成立，以及抓取以后执行链是否能够继续。

回流、异常分流等路径的可用状态用于后续控制路径选择，不作为当前抓取入口 E 的直接替代。

---

# 4. S / D / B 判定与 CAE-SDB 结果

在本次示例运行中，PCN 在抓取入口取得如下状态：

```text
Current Time                 = 10:32:21.850

Robot Ready                  = TRUE
Safety Permission            = TRUE
Downstream Receive Ready     = TRUE

Vision Result                = OK
Vision Result Timestamp      = 10:32:14.200
Vision Valid Window          = 5.0 s
```

视觉结果距离当前判定时刻已经过去：

```text
10:32:21.850
-
10:32:14.200
=
7.650 s
```

而本次示例设定的视觉结果有效窗口为：

```text
5.0 s
```

因此，虽然：

```text
Vision Result = OK
```

但这一结果已经不能继续作为当前抓取入口的有效判定依据。

视觉结果在当前入口中映射为 C。

问题发生在该状态的动态时序有效性，因此形成：

```text
CAE-SDB Result：

C-D

视觉结果已经超过有效时间，
不能继续作为本次抓取入口的有效判定依据
```

这一区分很重要。

现场看到的原始状态仍然可以是：

```text
Vision Result = OK
```

但 PCN 当前需要判断的是：

```text
这个 OK 现在是否仍然有效？
```

两者不是同一个工程问题。

本次状态值、更新时间、判定时刻和形成的 C-D 结果与时间信息 T 关联保存。

本案例只展开与当前问题直接有关的判定关系，不逐项展开全部 CAE-SDB 坐标。

完整 C / A / E 与 S / D / B 双轴关系可参见：

[为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)

---

# 5. 控制仲裁

当前抓取入口已经形成以下主要判定信息：

```text
CAE-SDB Result：
C-D

关键安全许可：
成立

Robot Ready：
成立

正常投放位接收状态：
满足当前入口要求

回流路径：
可用
```

此时不能因为 Robot Ready、安全许可和下游状态正常，就忽略已经失效的视觉条件继续执行抓取。

当前抓取动作的位置和姿态依据已经失去有效性。

控制仲裁最终形成：

```text
当前抓取入口：
不允许进入

后续控制方向：
优先转入回流路径
```

这里的控制仲裁处理的是多个状态和判定结果共同存在时，本次入口最终应形成什么控制结果。

---

# 6. 多路径控制

根据控制仲裁结果，本次选定：

```text
Multipath Control：

回流
```

此时“回流”表示当前抓取入口已经确定下一候选控制路径。

它还不表示工件已经获得“进入回流路径”的许可。

---

# 7. 当前入口控制结果

对于当前 Target State Entry：

```text
进入抓取阶段
```

形成的入口控制结果为：

```text
不进入
```

因此，本周期机器人不会使用已经失效的视觉结果执行抓取。

系统同时确定新的候选目标状态：

```text
Target State：
回流状态

Target State Entry：
进入回流路径
```

到这里，当前“抓取入口 PCN”的责任已经完成。

---

# 8. 后续目标状态入口与执行结果

系统准备进入回流路径后，工程对象发生了变化。

新的状态迁移为：

```text
Current State：
识别完成 / 等待抓取

Target State：
回流状态

Target State Entry：
进入回流路径
```

“进入回流路径”属于新的 Target State Entry。

因此，需要由对应 PCN 根据回流入口自己的相关状态和进入条件重新执行前置判定。

例如，回流入口实际可能需要确认：

```text
Return Conveyor Ready
Return Path Available
Area Permission
Workpiece Position
Downstream Return Capacity
```

这些状态并不因为抓取入口已经选择“回流”就自动成立。

如果新的回流入口判定允许进入，系统才真正执行回流，并形成：

```text
Execution Result：

工件已进入回流路径
```

本案例到这里停止，不继续展开回流入口的完整状态配置、CAE-SDB 判定和控制规则。

---

# 9. 状态迁移判定履历

本次抓取入口可以形成如下 PCN Trace：

```text
Trace ID：
PCN-PICK-XXXX

PCN：
抓取入口 PCN

Current State：
识别完成 / 等待抓取

Target State：
抓取阶段

Target State Entry：
进入抓取阶段

Judgment Time：
10:32:21.850

Related States：
  Robot Ready = TRUE
  Safety Permission = TRUE
  Downstream Receive Ready = TRUE
  Vision Result = OK
  Vision Result Timestamp = 10:32:14.200

CAE-SDB Result：
C-D

Judgment：
视觉结果超过 5.0 s 有效窗口

Arbitration Result：
当前抓取入口不允许进入

Multipath Control：
回流

Current Entry Result：
当前抓取入口不进入

Next Target State：
回流状态

Next Target State Entry：
进入回流路径

Time Information：
T
```

这条履历保留的不是单纯一个：

```text
Robot Not Moving
```

而是一次完整状态迁移中的状态、判定和控制关系。

系统随后进入“回流路径”判定时，由回流入口对应的 PCN 形成新的状态迁移判定履历。

关于 PCN Trace 的详细说明可参见：

[为什么状态迁移判定履历是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)

---

## 案例总结

本次示例开始时，现场看到：

```text
Robot Ready        = TRUE
Vision Result      = OK
Safety Permission  = TRUE
Downstream Ready   = TRUE
```

如果只查看当前状态值，很容易留下一个问题：

> **机器人已经准备好，为什么仍然不抓取？**

将这些状态对应到“进入抓取阶段”这一 Target State Entry 后，可以进一步看到：

```text
Vision Result          = OK
Vision Result Age      = 7.650 s
Valid Window           = 5.0 s

CAE-SDB Result         = C-D
```

问题由“机器人没有动作”进一步定位为：

> **当前抓取入口所依赖的视觉结果已经失去动态时序有效性。**

### 本案例带来的工程信息差异

| 原有现场能够确认 | 通过本案例进一步明确 |
|---|---|
| 机器人已经就绪 | Robot Ready 是当前抓取执行链中的相关状态之一，不能单独代表入口成立 |
| 视觉系统已经输出 OK | 当前结果虽然为 OK，但已经超过本次入口允许的有效时间 |
| 安全许可成立 | 关键 A 已成立，但不能替代 C 和 E 的判定 |
| 正常投放位可以接收 | 当前执行链相关状态满足本次入口要求 |
| 抓取动作没有开始 | 当前入口形成 `C-D` |
| 现场需要人工继续判断为什么不能抓 | 问题已经定位到视觉结果的动态时序有效性 |
| 下一步由工程师临时判断 | 当前控制仲裁选择回流作为后续候选路径 |
| 回流路径可以使用 | 仍需在新的“进入回流路径”入口重新判定 |
| 不同系统分别保存自己的日志 | 当前状态、时间、判定、控制和后续目标状态入口被关联到同一 PCN Trace |

从这条履历可以直接还原本周期的工程关系：

```text
Robot Ready
Safety Permission
Downstream Ready
        ↓
均满足

Vision Result = OK
        ↓
已过期
        ↓
C-D
        ↓
抓取入口不进入
        ↓
选择回流
        ↓
进入新的回流入口判定
```

这个案例最终得到的不是更多设备状态，而是一条能够解释**本周期为什么没有抓取、依据是什么、下一步转向哪里**的状态迁移判定关系。

---

## 进一步阅读

- [为什么是 CAE-SDB？——状态变量域与判定性质的双轴结构](/zh/notes/why-cae-sdb/)
- [为什么“就绪”还不够？](/zh/questions/why-ready-is-not-enough/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)
- [为什么状态迁移判定履历是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)

---

## 版本说明

本文为 TPCA / PCN 状态迁移前置控制架构在自动化执行单元中的公开案例。

- Public Case Version 1.0：2026-06-30
- Public Case Version 1.1：2026-08-20，统一 PCN、CAE-SDB 结果、控制仲裁、多路径控制与状态迁移判定履历的层级表达。
- Public Case Version 1.2：2026-08-21，补充时间信息 T 与状态实例相关说明。
- Public Case Version 1.3：2026-08-25，明确 C / A / E 与 S / D / B 的双轴关系。
- Public Case Version 1.4：2026-09-10，按统一九步案例工程分析顺序重构正文。
- Public Case Version 1.5：2026-09-20，补充被选定路径对应的新目标状态入口、对应 PCN 重新判定及不同入口状态迁移判定履历的衔接关系。

作者：全野南政 / Nansei Zenno
