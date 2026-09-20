---
title: "応用事例"
draft: false
ShowReadingTime: false
---

本ページでは、TPCA / PCN を異なるエンジニアリング対象に適用した公開事例を紹介する。

## 事例一覧

### [自動化実行ユニット前判定事例](/jp/cases/automation-execution-unit-pre-control/)

画像認識を用いたロボットユニットを例に、ピックアップ段階へ移行する前に関連状態を C / A / E へ整理し、S / D / B 判定、Arbitration（制御優先度調停）、Multipath Control（複数経路制御）、PCN Trace までの流れを示す。

### [MES / WCS 協調停滞診断モジュール事例](/jp/cases/collaborative-stagnation-diagnosis/)

MES / WCS の協調停滞を対象に、CAE-SDB 判定に加えて、群集約指標、協調停滞の識別、停滞構造の分類を扱う。

### [製造 DX 状態遷移条件設計・履歴分析事例](/jp/cases/production-dx-state-transition/)

自動加工工程からセル組立工程への移行を例に、品質、作業者資格、部品供給、セル設備などの状態を Target State Entry（目標状態入口）に対応付け、CAE-SDB Matrix（CAE-SDB マトリクス）を用いた判定と履歴分析を示す。

# 9ステップのエンジニアリング分析手順

各公開事例では、次の9ステップを共通の基本構成として使用する。

| 工程 | 概要 |
|---|---|
| **1. Current State（現在状態）** | 状態遷移の起点を明確にする。 |
| **2. Target State（目標状態） / Target State Entry（目標状態入口）** | 目標状態と目標状態入口を明確にする。 |
| **3. PCN：関連状態取得 + C / A / E 状態マッピング** | 関連状態を Condition（条件状態）、Authority（許可状態）、Execution Chain（実行チェーン状態）へ整理する。 |
| **4. S / D / B 判定 → CAE-SDB Matrix（CAE-SDB マトリクス） → CAE-SDB Result（CAE-SDB 判定結果） + T** | Structure（構造完全性）、Dynamics（動的時系列有効性）、Boundary（制御境界）の判定結果を構造化する。 |
| **5. Arbitration（制御優先度調停）** | 判定結果と重要な制約の優先関係を処理する。 |
| **6. Multipath Control（複数経路制御）** | Target State Entry（目標状態入口）に対する制御出力を形成する。 |
| **7. Target State Entry（目標状態入口）に対する制御結果** | 移行、保留、禁止などの結果を明確にする。 |
| **8. 選択された制御経路の実行 → Execution Result（実行結果）** | 選択された制御を実行し、その結果を確認する。 |
| **9. PCN Trace** | 状態、判定、制御、実行結果を状態遷移判定履歴として記録する。 |

各事例では、この共通構成に対して、対象ごとに必要な状態、判定、分析、制御経路を具体化している。

このページでは、TPCA / PCN 状態遷移前制御体系を異なる対象へ適用した公開事例をまとめている。
