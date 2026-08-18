from pathlib import Path
import zipfile

# 1) 修正 V3.3 正式 Hugo 文件中的资源引用
v33 = Path("/mnt/data/pcn_home_animation_v3_3")
html_path = v33 / "pcn-animation-v3-3.html"
html = html_path.read_text(encoding="utf-8")
html = html.replace("layouts/shortcodes/pcn-animation-v3-2.html", "layouts/shortcodes/pcn-animation-v3-3.html")
html = html.replace('css/pcn-animation-v3-2.css', 'css/pcn-animation-v3-3.css')
html = html.replace('js/pcn-animation-v3-2.js', 'js/pcn-animation-v3-3.js')
html_path.write_text(html, encoding="utf-8")

zip_path = Path("/mnt/data/pcn_home_animation_v3_3_fixed.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(v33 / "pcn-animation-v3-3.html", "layouts/shortcodes/pcn-animation-v3-3.html")
    z.write(v33 / "pcn-animation-v3-3.css", "static/css/pcn-animation-v3-3.css")
    z.write(v33 / "pcn-animation-v3-3.js", "static/js/pcn-animation-v3-3.js")
    z.write(v33 / "README.md", "README.md")

# 2) 生成更新后的 Concepts 完整 Markdown
content = r'''---
title: "概念术语"
summary: "整理 TPCA / PCN 状态迁移前置控制体系中的基础术语，包括当前状态、目标状态、前置控制、PCN、PCN 网络、多源状态信号、C / A / E、S / D / B、CAE-SDB 判定结果、控制仲裁、多路径控制和 PCN Trace。"
description: "用于统一 TPCA / PCN 状态迁移前置控制体系中的核心术语，说明 PCN 前置控制节点、C / A / E 状态映射、S / D / B 判定、CAE-SDB 判定结果、控制仲裁、多路径控制和 PCN Trace 之间的关系。"
draft: false
date: 2026-07-04
lastmod: 2026-08-19
author: "全野南政 / Nansei Zenno"
ShowReadingTime: false
ShowToc: true
TocOpen: true
---

本页整理 TPCA / PCN 状态迁移前置控制体系中的基础术语。  
术语以工程使用为主，用于统一公开说明、案例资料、合作沟通和后续技术文档中的表达。

[TPCA / CAE-SDB 与既有工业自动化理论的关系](/zh/notes/tpca-existing-theories/)

> 用于理解 TPCA / CAE-SDB 与状态机、安全互锁、报警诊断、AI 诊断、MES / WCS 调度和形式化验证之间的边界关系。

---

## 当前状态 / 目标状态

当前状态，是系统在执行前所处的状态、阶段或路径位置。

目标状态，是系统准备进入的下一状态、目标执行路径或目标物理执行阶段。

TPCA 关注的问题，发生在当前状态进入目标状态之前。

例如：

- 等待阶段 → 抓取阶段；
- 放置完成 → 压装阶段；
- 待检测 → 检测执行阶段；
- 任务存在 → 任务派发路径；
- AGV 到站 → 站点承接；
- 当前请求 → 目标调用路径。

如果没有明确当前状态和目标状态，就无法判断这个状态迁移入口需要哪些条件、许可和执行链。

---

## 前置控制

前置控制，是指系统进入目标状态、目标执行路径或目标物理执行阶段之前，对相关多源状态进行结构化判定，并根据完整判定结果控制是否进入以及进入哪条执行路径。

它关注的是进入目标状态之前的问题，而不是动作失败后的事后诊断，也不是单纯报警分类。

前置控制需要回答：

- 条件是否成立；
- 许可是否成立；
- 执行链是否能够接续；
- 所需结构是否完整；
- 当前状态是否具有动态时序有效性；
- 是否进入预先定义的控制边界；
- 多个判定结果同时存在时，哪个结果具有更高控制优先级；
- 最终应输出哪一类控制路径。

---

## TPCA

英文：Transition Pre-Control Architecture

状态迁移前置控制架构。

TPCA 用于目标状态、目标执行路径或目标物理执行阶段进入前的结构化判定与多路径控制。

其基本工程链条为：

> Current State  
> → Target State  
> → PCN  
> → C / A / E Mapping  
> → S / D / B Evaluation  
> → CAE-SDB Result  
> → Arbitration  
> → Multipath Control  
> → PCN Trace

{{< pcn-animation >}}

TPCA 的重点不是增加一个新的报警层，而是把目标状态进入前原本分散的判断整理为明确的工程结构。

---

## PCN

英文：Pre-Control Node

前置控制节点。

PCN 部署在目标状态进入前，是 TPCA 的最小工程实现单元。

PCN 用于完成：

- 当前状态与目标状态确认；
- 多源状态获取与整理；
- C / A / E 状态映射；
- S / D / B 判定；
- CAE-SDB 判定结果生成；
- 控制优先级仲裁；
- 多路径控制输出；
- 状态记录与追溯。

一个 PCN 对应一个明确的状态迁移入口。

在自动化执行单元中，PCN 可以实现为 PLC 功能块、边缘控制器模块或软件判定节点，并可通过 HMI 等界面显示其判定与控制结果。

在 MES / WCS、AGV / AMR 群控、生产 DX 或数字调用治理场景中，PCN 可以部署在任务派发前、资源放行前、站点承接前、协同执行恢复前或目标调用路径进入前。

---

## PCN 网络

PCN 网络，是多个 PCN 按状态迁移关系连接形成的前置控制结构。

单个 PCN 对应一个目标状态入口。

多个 PCN 可以分布在设备单元、产线、MES / WCS、AGV / AMR 群控层、生产 DX 系统或数字调用系统中。

PCN 网络关注的是状态迁移入口之间的关系，而不是设备连接关系本身。

它可以用于识别：

- 哪些位置需要设置 PCN；
- 哪些状态迁移入口经常不能成立；
- 哪些关键许可需要独立约束；
- 哪些执行链经常不能接续；
- 哪些状态迁移条件需要显式化；
- 哪些 PCN 判定履历可以用于复盘和改善。

---

## 多源状态信号

多源状态信号，是与目标状态进入相关的输入信息。

信号来源可以包括 PLC、机器人控制器、视觉系统、安全系统、HMI / SCADA、MES、WCS、AGV / AMR 调度系统、现场传感器、上位系统、人工确认以及数字系统接口等。

PCN 不单纯按照信号来源划分问题，而是根据这些信号在特定状态迁移入口中承担的工程作用进行 C / A / E 映射。

同一个信号，在不同目标状态入口前可能承担不同作用。

因此，多源状态信号必须结合 Current State 和 Target State 理解。

---

## CAE-SDB

CAE-SDB 是 PCN 内部的结构化判定逻辑。

其基本结构为：

> {C, A, E} × {S, D, B}

其中：

C / A / E 表示状态变量域。

S / D / B 表示对这些状态变量进行判断时使用的判定性质。

C / A / E 与 S / D / B 组合后，形成 9 个判定坐标：

|  | S | D | B |
|---|---|---|---|
| C | C-S | C-D | C-B |
| A | A-S | A-D | A-B |
| E | E-S | E-D | E-B |

一次前置判定可以形成一个或多个有效判定坐标。

这些坐标共同构成：

> CAE-SDB Result

当多个判定结果同时存在时，还需要经过控制优先级仲裁：

> CAE-SDB Result  
> → Arbitration  
> → Multipath Control

因此，CAE-SDB 的价值不在于形成静态的 3 × 3 分类表，而在于把目标状态进入前的 false、NG、not ready、waiting、pending、blocked 等压缩状态，展开为可判定、可仲裁、可控制、可记录的工程结构。

---

## C

英文：Condition

条件状态。

C 表示进入目标状态前，现场条件、对象条件、识别条件、数据条件、任务条件、参数条件等是否成立。

例如：

- 工件存在；
- 位置合格；
- 识别结果有效；
- 任务存在；
- 参数完整；
- 前序阶段完成。

---

## A

英文：Authority

许可状态。

A 表示系统是否允许进入目标状态。

典型内容包括：

- 安全许可；
- 上位许可；
- 区域许可；
- 人工确认；
- 权限；
- 授权；
- 资源锁；
- 对方设备许可。

关键 A 可以构成独立必要约束。

安全许可、授权、资源锁、区域许可等关键许可不成立时，即使 C 条件和 E 执行链满足，也不得允许进入目标状态。

A 不应被简单当作普通 Condition 项处理。

---

## E

英文：Execution Chain

执行链状态。

E 表示进入目标状态后，执行链是否能够继续接续。

E 不等同于单体设备 Ready。

执行链可以包括：

- 本体设备；
- 末端执行机构；
- 下游承接；
- 正常执行路径；
- 替代路径；
- 回退路径；
- 异常排出路径；
- 结果上传或回写链路；
- 对方设备接收状态。

例如机器人 Ready 只是局部状态。

抓取以后下游是否能够承接、异常品是否能够排出、结果是否能够回写，同样属于 E 的判断范围。

---

## S

英文：Structure

结构完整性。

S 是对 C / A / E 状态变量进行判定时使用的一类分析性质。

S 用于判断目标状态进入前所需的信号、接口、映射关系、许可来源、路径、角色和执行链边界是否已经定义、接入并可观测。

典型问题包括：

- 所需信号未定义；
- 接口未接入；
- 映射关系未建立；
- 许可来源不明确；
- 执行链边界缺失。

---

## D

英文：Dynamics

动态时序有效性。

D 是对 C / A / E 状态变量进行判定时使用的一类分析性质。

D 用于判断运行中的相关状态是否有效、同步、稳定和可信。

典型问题包括：

- 信号超时；
- 未刷新；
- 抖动；
- 冲突；
- 延迟；
- 不同步；
- 低置信度；
- 许可撤销；
- 状态处于切换中。

---

## B

英文：Boundary

控制边界。

B 是对 C / A / E 状态变量进行判定时使用的一类分析性质。

B 用于判断某个 C、A 或 E 状态是否已经进入预先定义的控制边界，以及相关边界条件是否已经触发。

用于形成边界判定的工程参数可以包括：

- 容许范围；
- 时间窗口；
- 重试上限；
- 置信度范围；
- 位置偏差范围；
- 其他与目标状态进入相关的边界条件。

B 本身不是最终控制路径。

最终控制输出需要结合完整的 CAE-SDB Result，并经过 Arbitration 后生成。

---

## CAE-SDB 判定结果

英文：CAE-SDB Result

CAE-SDB 判定结果，是 PCN 对目标状态进入前的 C / A / E 状态变量，从 S / D / B 判定性质进行分析后形成的结构化结果。

例如：

> C-D

表示 C 条件域中存在动态时序有效性问题。

> E-S

表示 E 执行链域中存在结构完整性问题。

一次状态迁移前置判定可以同时形成一个或多个坐标结果。

例如：

> C-D + E-D

表示条件域和执行链域中同时存在动态时序有效性问题。

这些结果用于说明：

> 问题发生在哪个状态变量域，以及属于什么判定性质。

CAE-SDB Result 不是最终控制指令。

---

## 控制优先级仲裁

英文：Arbitration

当一个状态迁移入口同时形成多个 CAE-SDB 判定结果时，需要根据预先定义的控制约束和优先关系确定最终控制方向。

例如：

某个条件状态存在动态异常的同时，也可能存在关键许可未成立。

这时不能简单根据某一个判定坐标直接生成最终动作。

Arbitration 的作用是：

> 在完整 CAE-SDB Result 基础上处理一个或多个判定结果之间的控制优先关系，并确定应触发的执行链或控制路径。

最终结果再进入 Multipath Control。

---

## 多路径控制

英文：Multipath Control

多路径控制，是根据完整 CAE-SDB Result 经过 Arbitration 后生成的最终工程控制输出。

典型控制路径可以包括：

- 允许进入；
- 等待；
- 重识别；
- 重采样；
- 重定位；
- 回流；
- 异常分流；
- 下游协调；
- 资源释放；
- 降级执行；
- 备用路径；
- 禁止进入；
- 安全锁定；
- 人工确认；
- 异常隔离；
- 增强记录。

多路径控制的作用，是把目标状态进入前一个或多个判定结果最终转化为可执行、可显示和可记录的工程控制路径。

其中，正常执行链成立时，系统可以进入目标状态；其他判定结果则可以触发等待、重试、回流、人工确认、禁止进入或其他预先定义的执行路径。

---

## PCN Trace / 状态记录与追溯

PCN Trace 是对一次状态迁移前置判定过程及其控制结果进行结构化记录。

记录内容可以包括：

- Current State；
- Target State；
- 参与本次判定的多源状态；
- C / A / E 映射结果；
- S / D / B 判定结果；
- CAE-SDB Result；
- Arbitration 结果；
- Multipath Control 输出；
- 时间信息；
- 追溯标识。

PCN Trace 用于现场复盘、问题追溯、设计审核、项目交接和后续改善。

在产品化场景中，也可以作为 MES / WCS、HMI、SCADA 或后续数据分析模块的结构化数据来源。

---

相关索引：  
[TPCA / CAE-SDB 术语索引](/zh/terms/)

延伸阅读：

- [TPCA / PCN 建立在什么工程基础上？——五个基础工程共识](/zh/notes/engineering-foundations-of-tpca-pcn/)
- [TPCA / PCN 面对已有技术分歧，它站在哪里？——三个典型工程争议](/zh/notes/engineering-positions-of-tpca-pcn/)
- [你真的理解 TPCA / PCN 了吗？——十个工程问题](/zh/notes/tpca-pcn-understanding-test/)

---

本文属于 TPCA / PCN 状态迁移前置控制体系的公开说明内容。  
TPCA、CAE-SDB 与 PCN 为本站作者围绕复杂工程系统目标状态进入前判定问题所整理的术语体系。
'''

out = Path("/mnt/data/concepts-index.zh.md")
out.write_text(content, encoding="utf-8")

print("已生成 Concepts 完整版：", out)
print("已修正 V3.3 Hugo 包：", zip_path)
