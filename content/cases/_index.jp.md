---
title: "応用事例"
draft: false
ShowReadingTime: false
---

本ページでは、TPCA / PCN を異なるエンジニアリング対象へ適用した公開事例を整理する。

## 事例一覧

### [自動化実行ユニット前判定事例](/jp/cases/automation-execution-unit-pre-control/)

画像認識を用いたロボットユニットを例に、ピックアップ段階への移行前に、関連状態を C / A / E へ整理し、S / D / B 判定、Arbitration、Multipath Control、PCN Trace までを示す。

### [MES / WCS 協調停滞診断モジュール事例](/jp/cases/collaborative-stagnation-diagnosis/)

MES / WCS の協調停滞を対象に、CAE-SDB 判定に加えて、群集約指標、協調停滞の識別、停滞構造の分類を扱う。

### [製造DX 状態遷移条件設計・履歴分析事例](/jp/cases/production-dx-state-transition/)

自動加工工程からセル組立工程への移行を例に、品質、作業者資格、部品供給、セル設備などの状態を Target State Entry に対応付け、CAE-SDB Matrix を用いた判定と履歴分析を示す。

# 9ステップのエンジニアリング分析手順

各公開事例では、次の 9 ステップを共通骨格として使用する。

| 工程 | 概要 |
|---|---|
| **1. Current State（現在状態）** | 状態遷移の起点を明確にする。 |
| **2. Target State / Target State Entry** | 目標状態と目標状態入口を明確にする。 |
| **3. PCN：関連状態取得 + C / A / E 状態マッピング** | 関連状態を Condition、Authority、Execution Chain へ整理する。 |
| **4. S / D / B 判定 → CAE-SDB Matrix → CAE-SDB Result + T** | Structure、Dynamics、Boundary の判定結果を構造化する。 |
| **5. Arbitration（制御優先度調停）** | 判定結果と重要な制約の優先関係を処理する。 |
| **6. Multipath Control（複数経路制御）** | Target State Entry に対する制御出力を形成する。 |
| **7. Target State Entry に対する制御結果** | 移行、保留、禁止などの結果を明確にする。 |
| **8. 選択された制御経路の実行 → Execution Result** | 選択された制御を実行し、その結果を確認する。 |
| **9. PCN Trace** | 状態、判定、制御、実行結果を状態遷移判定履歴として記録する。 |

各事例では、この共通骨格に対して、対象に必要な状態、判定、分析、制御経路を具体化している。

本ページは、TPCA / PCN 状態遷移前制御体系における公開応用事例の索引である。
