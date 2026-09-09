---
title: "为什么 OEE 之后还需要 PCN？"
summary: "OEE 用于观察运行实绩和损失，PCN 则面向明确的 Target State Entry（目标状态入口），处理状态迁移前判定、控制和履历。将两者关联后，可以把损失发生的时间区间与当时的状态迁移判定对应起来。"
description: "说明 OEE 与 PCN 所处理对象的区别，以及如何将 OEE / 生产实绩数据与 PCN Trace（状态迁移判定履历）关联，用于进一步分析状态迁移条件和控制路径。"
date: 2026-07-04
lastmod: 2026-09-09
author: "全野南政 / Nansei Zenno"
document_type: "技术札记"
version: "Public Note Version 1.4"
citation_url: "https://zennns.com/zh/notes/why-oee-pcn/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## 为什么 OEE 之后还需要 PCN？

OEE、设备运行数据、报警履历和保全数据，是制造现场观察运行实绩和损失的重要基础。

通过 OEE，可以确认设备实际运行了多长时间，停止或等待持续了多久，性能和质量是否发生变化，以及损失主要集中在哪些时间段或工序。改善实施以后，也可以继续用同一套指标比较运行结果。

但复杂自动化系统中还经常出现另一类问题：设备没有明确故障，却迟迟不能进入下一阶段。

例如，机器人已经 Ready（就绪），但抓取没有开始；任务已经生成，但没有进入执行；上游已经完成，下游暂时无法接收；MES、WCS、PLC 和机器人都有状态记录，但现场仍持续 Waiting（等待）。

这类问题仅看损失时间还不够。现场还需要知道：

> **在这个时间段内，系统卡在哪一个 Target State Entry（目标状态入口），当时用了哪些状态进行判定，形成了什么判定结果，又选择了什么控制路径。**

PCN 面向的正是这个工程位置。

基础概念可参见：

- [Concepts｜核心概念](/zh/concepts/)
- [TPCA / PCN 状态迁移前置控制架构｜白皮书](/zh/whitepaper/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)
- [为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)

---

## 1. OEE 和 PCN 处理的对象不同

OEE 主要用于观察设备或生产过程的运行实绩和损失，例如时间开动率、性能效率、良品率、停机损失、性能损失、质量损失、节拍和产量。

它更适合回答：

> **哪里发生了损失，损失有多大。**

PCN 处理的是一次明确的状态迁移入口。

```text
Current State（当前状态）
    ↓
Target State Entry（目标状态入口） / PCN
    ↓
Target State（目标状态）
```

在这个入口前，PCN 获取与本次状态迁移直接相关的状态，并形成：

```text
相关状态
→ C / A / E Mapping（状态映射）
→ S / D / B Evaluation（判定）
→ CAE-SDB Result（CAE-SDB 判定结果） + T
→ Arbitration（控制仲裁）
→ Multipath Control（多路径控制）
→ PCN Trace（状态迁移判定履历）
```

因此，两者的职责并不重复。

> **OEE 用于观察运行实绩和损失。**

> **PCN 用于处理 Target State Entry 上的状态迁移前判定和控制，并把结果记录到 PCN Trace。**

---

## 2. 复杂自动化为什么还需要 Target State Entry 的信息

复杂设备和自动化产线中，“运行”和“停止”之间往往存在很多状态迁移入口。

例如：

```text
待机 → 自动运行
上料完成 → 加工
加工完成 → 检测
检测完成 → 排出
识别完成 → 抓取
放置完成 → 压装
任务生成 → 任务执行
AGV 到站 → 站点接收
```

每一个入口都可能同时依赖多个状态。

以机器人抓取为例，Robot Ready（机器人就绪）已经成立，并不代表抓取入口一定可以放行。视觉结果可能已经过期，安全许可可能尚未成立，上位系统仍在等待放行，下游接收状态可能未成立，或者相关状态长时间没有刷新。

OEE 和设备运行数据可以告诉我们这段时间发生了等待或停止。PCN Trace 则可以进一步确认，当时判定的是哪个 Target State Entry、使用了哪些相关状态、形成了什么 CAE-SDB 判定结果、最终选择了哪条 Multipath Control，以及执行结果如何。

这样，生产实绩上的损失就可以和具体的状态迁移判定对应起来。

---

## 3. OEE / 生产实绩如何与 PCN Trace 对应

OEE / 生产实绩数据和 PCN Trace 处理的是不同粒度的信息。

| 项目 | OEE / 设备与生产数据 | PCN / PCN Trace |
|---|---|---|
| 主要对象 | 运行实绩、生产结果、损失 | 一次明确的 Target State Entry |
| 主要确认内容 | 稼动、性能、质量、停止、等待 | 状态、判定结果、控制结果、执行结果 |
| 时间处理 | 对一定时间区间进行汇总和比较 | 记录每次 Target State Entry 的具体时间位置 |
| 主要用途 | 识别损失、比较实绩、确认改善效果 | 确认状态迁移判定、控制履历和问题位置 |
| 主要改善对象 | 设备、工序、生产过程 | 状态迁移条件、许可、Execution Chain（执行链）、控制路径 |

例如，生产实绩数据显示某台设备出现了较长时间等待。对应时间段内的 PCN Trace 记录为：

```text
PCN：PCN-07

Current State（当前状态）：检测完成
Target State（目标状态）：工件排出

CAE-SDB Result（判定结果）：E-D
判定内容：下游状态长时间未更新

Multipath Control（多路径控制）：Wait（等待）
Execution Result（执行结果）：下游状态更新后进入排出阶段
```

这时可以把两部分信息对应起来：

```text
OEE / 生产实绩
→ 发现等待损失
```

```text
PCN Trace
→ 确认当时的 Target State Entry
→ 确认 E-D 判定结果
→ 确认 Wait（等待）控制路径
```

实际分析时，可以先通过 OEE 或其他生产实绩数据确定损失区间，再查看该时间段内对应的 PCN Trace，确认状态迁移条件和控制路径。

```text
OEE / 生产实绩数据
        ↓
确定损失发生区间
        ↓
确认该时间段的 Target State Entry
        ↓
PCN Trace
        ↓
CAE-SDB Result / Multipath Control
        ↓
检查状态迁移条件和控制路径
```

---

## 4. 两类数据结合后，改善对象会更具体

OEE 能够指出损失集中在哪个设备、工序或时间段。PCN Trace 则可以继续观察这个时间段内是否反复出现相同的状态迁移判定。

例如，某一个 Target State Entry 长期出现 E-D，某项许可相关的等待反复发生，或者同一个 PCN 长期选择 Wait（等待）。这些信息可以把改善范围从“等待时间较长”进一步缩小到状态更新、许可条件、执行链、控制边界或控制路径等具体工程对象。

改善以后，还可以继续比较对应时间区间的 OEE 和 PCN Trace。例如等待时间是否缩短，某个 CAE-SDB Result 的出现频率是否下降，或者控制路径调整以后实际执行结果是否发生变化。

因此，两者可以形成比较直接的补充关系：

> **OEE 指出损失发生在哪里、持续多久。**

> **PCN Trace 说明这个时间段内，Target State Entry 上实际发生了什么判定和控制。**

这使改善工作可以从生产绩效继续下钻到状态迁移条件和控制关系。

---

## 总结

OEE 和 PCN 面向制造系统中的不同工程对象。

> **OEE 用于观察运行实绩和损失。**

> **PCN 用于处理明确 Target State Entry 上的状态迁移前判定和控制，并把结果记录到 PCN Trace。**

将两者关联以后，可以同时看到：

```text
OEE / 生产实绩 → 哪个时间段、哪个工序发生了损失
```

以及：

```text
PCN Trace
→ 当时处于哪个 Target State Entry
→ 使用了哪些状态
→ 形成了什么判定结果
→ 选择了什么控制路径
→ 最终执行结果如何
```

这样，生产实绩上的损失可以继续对应到状态迁移条件、许可、Execution Chain（执行链）和控制路径等具体改善对象。

---

## 相关技术札记

- [为什么 PCN Trace 是一种新的工程数据？](/zh/notes/why-pcn-trace-is-engineering-data/)
- [为什么 PCN 是 TPCA 的最小工程节点？](/zh/notes/pcn-minimum-engineering-unit/)
- [多个 PCN 如何形成状态迁移前置控制网络？](/zh/notes/pcn-network-structure/)
- [TPCA / PCN 适用场景分析](/zh/notes/tpca-pcn-applicable-scenarios/)

---

## 参考文献与外部资料

以下资料用于确认 OEE 及制造运营 KPI 的既有工程定位。

1. **Japan Institute of Plant Maintenance（JIPM）— TPM / Overall Equipment Efficiency（OEE）**  
   JIPM 将 OEE 作为衡量设备综合效率、识别相关损失并用于改善的代表性指标。  
   https://jipmglobal.com/tpm/about_us_en

2. **ISO 22400-1:2014 — Automation systems and integration — Key performance indicators (KPIs) for manufacturing operations management — Part 1: Overview, concepts and terminology**  
   该标准对制造运营管理中 KPI 的基本概念和术语进行了整理。  
   https://www.iso.org/standard/56847.html

---

## 文档信息

题目：为什么 OEE 之后还需要 PCN？  
文档类型：技术札记  
版本：Public Note Version 1.4  
首次发布日期：2026-07-04  
最后更新：2026-09-09  
作者：全野南政 / Nansei Zenno  
当前 URL：https://zennns.com/zh/notes/why-oee-pcn/

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。
