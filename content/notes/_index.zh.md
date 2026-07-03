---
title: 技术札记
draft: false
---

技术札记整理面向制造现场、自动化系统和数字调用治理的技术札记。

星级表示推荐阅读优先级：
-⭐⭐⭐ 为重点阅读
-⭐⭐ 为建议阅读
-⭐ 为补充阅读

## 技术札记清单



### ⭐⭐⭐ 理论边界

[TPCA / CAE-SDB 与既有工业自动化理论的关系](/zh/notes/tpca-existing-theories/)

-用于理解 TPCA / CAE-SDB 与状态机、安全互锁、报警诊断、AI 诊断、MES / WCS 调度和形式化验证之间的边界关系。

### ⭐⭐⭐ PCN 前置控制节点

[为什么 PCN 是 TPCA 的最小工程单元？](/zh/notes/pcn-minimum-engineering-unit/)

-用于理解 TPCA 如何通过 PCN 落到具体状态入口、输入、判定、输出和记录。

### ⭐⭐⭐ PCN 网络结构

[多个 PCN 如何形成状态迁移前置控制网络？](/zh/notes/pcn-network-structure/)

-用于理解多个 PCN 如何按目标状态入口连接成状态迁移前置控制网络，并形成“这里需要增加一个 PCN 点”的工程讨论语言。



## 相关栏目阅读

- [TPCA / CAE-SDB 白皮书](/zh/whitepaper/)  
  系统理解 TPCA / CAE-SDB 的整体方法论主线。

- [Concepts｜核心概念](/zh/concepts/)  
  查看 TPCA、PCN、CAE-SDB、C/A/E、S/D/B 等核心术语定义。

- [Engineering Questions｜工程问题](/zh/questions/)  
  从制造现场常见问题进入，例如 Ready、Waiting、MES / WCS 停滞、任务存在但不能执行等问题。
