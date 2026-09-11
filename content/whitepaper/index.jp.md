---
title: "TPCA / PCN 状態遷移前制御アーキテクチャ"
summary: "明確な Target State Entry を独立して設計・判定・制御・記録可能なエンジニアリング対象として扱い、PCN によって状態遷移前判定、制御優先度調停、複数経路制御、PCN Trace までを一連の構造として構成する。"
description: "TPCA / PCN 状態遷移前制御アーキテクチャの公開ホワイトペーパー。Target State Entry を中心に、C / A / E、S / D / B、CAE-SDB Result、Arbitration、Multipath Control、PCN Trace、PCN Network の全体構造を示す。"
date: 2026-07-01
lastmod: 2026-09-09
author: "全野南政 / Nansei Zenno"
document_type: "公開ホワイトペーパー"
version: "Public Version 1.5"
citation_title: "TPCA / PCN 状態遷移前制御アーキテクチャ"
citation_url: "https://zennns.com/jp/whitepaper/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## 概要

TPCA / PCN の中核命題は、次のとおりである。

> **明確な Target State Entry は、独立して設計・判定・制御・記録可能なエンジニアリング対象として扱う。**

**TPCA（Transition Pre-Control Architecture）** は、状態遷移前制御の全体アーキテクチャである。

**PCN（Pre-Control Node / 前制御ノード）** は、明確な Target State Entry（目標状態入口）の前に配置し、その入口に対する判定、制御、履歴を一つのエンジニアリング単位として扱う。

基本的な工程関係は次の通りである。

```text
① Current State
   （現在状態・現在段階・現在経路位置）
   ↓
② Target State
   （目標状態・目標実行経路・目標物理実行段階）
   と Target State Entry（目標状態入口）を特定
   ↓
③ PCN（Pre-Control Node / 前制御ノード）
   └─ 関連状態を取得し、
      C / A / E 状態マッピング
   ↓
④ S / D / B 判定
   → CAE-SDB Matrix
   → CAE-SDB Result（CAE-SDB 判定結果）+ T（時間情報）
   ↓
⑤ Arbitration（制御優先度調停）
   ↓
⑥ Multipath Control（複数経路制御）
   ↓
⑦ Target State Entry（目標状態入口）に対する制御結果
   ├─ 移行許可
   ├─ 待機・再確認・再試行
   ├─ 別の Target State
   │  （目標状態・目標実行経路・目標物理実行段階）
   └─ 移行禁止 など
   ↓
⑧ 選択された制御経路を実行
   → Target State
      （目標状態・目標実行経路・目標物理実行段階）への移行
   → 待機・再確認・再試行
   → 移行禁止など
   → 実行結果
   ↓
⑨ PCN Trace（状態遷移判定履歴）
   → 入力・判定・制御・実行結果を関連付けて記録
```


C / A / E は、今回の状態遷移に関係する状態の役割を整理する状態変数領域である。

S / D / B は、それらの状態を構造完全性、動的時系列有効性、制御境界の観点から判定する判定性質である。

PCN は CAE-SDB Result（CAE-SDB 判定結果）を形成した後、重要な許可や制御制約を Arbitration（制御優先度調停）へ渡して制御上の優先関係を処理し、その結果に基づいて Multipath Control（複数経路制御）を形成する。

判定、制御、実行結果は PCN Trace として記録する。

複数の PCN を、実際の状態遷移関係、および許可、資源、実行、状態更新などの依存関係に基づいて接続することで PCN Network を構成できる。

---

# 第 1 章 エンジニアリング課題

複雑な製造・自動化システムでは、PLC、ロボット、画像認識、安全システム、MES / WCS、HMI などがそれぞれ状態を持っていても、次の状態や実行段階へ進まないことがある。

例えば、次のような状態である。

- ロボットは Ready だが、ピックアップ動作が開始されない。
- タスクは存在するが、実行へ進まない。
- 上流工程は完了しているが、下流が受け入れられない。
- 個々の設備に明確な故障がない状態で Waiting が継続する。
- 複数システムに状態記録が存在していても、どの状態が今回の状態遷移を止めているか説明しにくい。

![複雑なエンジニアリングシステムにおける共通状態遷移問題](/images/tpca/01-common-state-transition-problem.jp.png)

図1：複雑なエンジニアリングシステムが現在状態から次の状態へ遷移する際には、前提条件、関連システム状態、時系列・境界情報、許可条件を総合して入口前判定を行い、その判定結果に応じて異なる実行チェーンへ進む。

このような問題を確認する際は、まず次の関係を明確にする。

```text
Current State
    ↓
Target State Entry
    ↓
Target State
```

そのうえで、今回の Target State Entry に関係する状態を同じ状態遷移の文脈で確認する。

TPCA / PCN は、この Target State Entry を中心として、分散した状態、判定、制御、履歴を一つのエンジニアリング対象として整理する。

詳細な問題構造については、以下を参照。

[エンジニアリング課題](/jp/questions/) では、TPCA / PCN を理解する入口として、自動化ユニット、複数システム連携、状態遷移設計の3つの問題領域から、「次の状態へ進まない」問題を整理している。

---

# 第 2 章 TPCA / PCN の基本アーキテクチャ

## 2.1 TPCA と PCN

TPCA は、Target State（目標状態・目標実行経路・目標物理実行段階）へ進入する前の判定と制御を対象とする。

TPCA / PCN が対象とする Target State（目標状態・目標実行経路・目標物理実行段階）には、例えば次のものがある。

- ロボットのピック、配置、検査などの物理実行段階
- 圧入、搬送引渡し、分流などの工程段階
- MES / WCS におけるタスク実行経路
- AGV / AMR 群制御における協調実行状態
- 製造DX における複数システム横断の重要な状態切替
- デジタルシステムにおける明確な実行経路

PCN は、1 つの明確な Target State Entry に対応する。

PCN は、その入口に関係する状態を取得し、CAE-SDB による構造化判定、制御優先度調停、複数経路制御、PCN Trace を一つの工程単位として構成する。

基本階層は次の通りである。

```text
TPCA
→ PCN
→ CAE-SDB
→ Arbitration（制御優先度調停）
→ Multipath Control（複数経路制御）
→ PCN Trace
```

各要素の役割は次の通りである。

| 要素 | 役割 |
|---|---|
| TPCA | 状態遷移前制御の全体アーキテクチャ |
| PCN | 1 つの Target State Entry に対応する前制御ノード |
| CAE-SDB | PCN 内部の構造化判定ロジック |
| Arbitration（制御優先度調停） | 複数の判定結果、重要な許可、制御制約の優先関係を処理する |
| Multipath Control（複数経路制御） | 今回の Target State Entry に対する制御経路を形成する |
| PCN Trace | 1 回の Target State Entry に対する判定・制御・実行履歴 |

## 2.2 基本エンジニアリングチェーン

概要で示した ①～⑨ の工程を表にまとめると、次のようになる。

| 工程位置 | エンジニアリング対象 | 主な処理 | 主な結果 |
|---|---|---|---|
| 1 | **Current State（現在状態・現在段階・現在経路位置）** | 今回の状態遷移の起点となる現在状態を確認する | 現在状態を特定 |
| 2 | **Target State（目標状態・目標実行経路・目標物理実行段階） / Target State Entry（目標状態入口）** | 今回移行しようとする Target State と、それに対応する Target State Entry を明確にする | 今回の判定対象を確定 |
| 3 | **PCN / 前制御ノード** | Target State Entry に関係する状態を取得し、C / A / E へ状態マッピングする | 状態変数領域を整理 |
| 4 | **PCN 内部判定** | C / A / E の関連状態に対して S / D / B 判定を行い、結果を CAE-SDB Matrix に整理する | CAE-SDB Result（CAE-SDB 判定結果）+ T（時間情報） |
| 5 | **PCN 内部制御判断** | CAE-SDB Result、重要な許可、制御制約などを Arbitration（制御優先度調停）で処理する | 制御上の優先関係を明確化 |
| 6 | **PCN 制御出力** | Arbitration の結果に基づいて Multipath Control（複数経路制御）を形成する | 移行許可、待機、再確認、代替経路、移行禁止など |
| 7 | **Target State Entry に対する制御結果** | 今回の Target State Entry に対して、移行、保留、禁止、別経路などの処理結果を明確にする | 次の制御・実行方向を明確化 |
| 8 | **選択された制御経路** | 選択された制御経路を実行する | Execution Result（実行結果）を形成 |
| 9 | **PCN Trace** | 入力状態、判定結果、制御結果、実行結果、時間情報 T を一つの履歴として関連付ける | PCN 状態遷移判定履歴を記録 |

![TPCA の基本処理チェーン](/images/tpca/02-tpca-process-chain.png)

図2：PCN は Target State Entry の前に配置され、関連状態を整理して構造化判定、制御優先度調停、複数経路制御を行い、その結果を PCN Trace として記録する。

この構造により、単純な Ready / Not Ready、OK / NG、Waiting / Blocked などの結果に加えて、

- どの状態変数領域に関係する結果か。
- どの判定性質に関係する結果か。
- どの制御経路が選択されたか。
- 実行後にどのような結果となったか。

を同じ Target State Entry の文脈で確認できる。

## 2.3 状態タイプと状態インスタンス

TPCA / PCN では、状態タイプと実運転で発生する状態インスタンスを区別して扱う。

状態タイプでは、

```text
A → B → A
```

のような循環を表現できる。

実運転では、

```text
A₁ → B₁ → A₂
```

となり、A₁ と A₂ は同じ状態タイプに属していても異なる状態インスタンスである。

> **状態タイプは循環できるが、実運転の状態インスタンスは時間方向へ継続して生成される。**

Recovery、Rollback、Reset、Retry、Re-entry などによる再進入も、新しい状態インスタンスへの遷移として扱う。

詳細については、以下を参照。

[TPCA における状態インスタンスの単方向性 ― 状態タイプの循環と実運転履歴の違い](/jp/notes/tpca-unidirectional-state-transition/)

---

# 第 3 章 PCN：状態遷移前制御の最小エンジニアリングノード

## 3.1 PCN の位置と基本要素

PCN は、明確な Target State Entry の前に配置する。

```text
Current State
    ↓
PCN
［Target State Entry に対する前置判定］
    ↓
Target State Entry
    ↓
Target State
```

![PCN 前制御ノードの位置と動作](/images/tpca/04-pcn-node-position.png)

図3：PCN は Target State Entry の前に配置され、Target State へ移行する前に、関連状態の整理、構造化判定、制御優先度調停、制御経路形成を行う。

1 つの PCN では、少なくとも次の対象を整理する。

| 項目 | 内容 |
|---|---|
| Current State（現在状態・現在段階・現在経路位置） | 現在どの状態・工程段階・経路位置にいるか |
| Target State（目標状態・目標実行経路・目標物理実行段階） | 次にどの状態・実行経路・物理実行段階へ進むか |
| Target State Entry（目標状態入口） | 今回どの入口を判定対象とするか |
| 関連状態 | 今回の状態遷移に直接関係する状態 |
| C / A / E 状態マッピング | 関連状態が今回の状態遷移で担う役割 |
| S / D / B 判定 | 各状態に対して実行する判定性質 |
| CAE-SDB Result（CAE-SDB 判定結果） | 今回形成された構造化判定結果 |
| 時間情報 T | 状態および判定に対応する時間情報 |
| Arbitration（制御優先度調停） | 複数の判定結果、重要な許可、制御制約の優先関係 |
| Multipath Control（複数経路制御） | Arbitration の結果に基づいて形成する制御経路 |
| Target State Entry に対する制御結果 | 今回の目標状態入口に対する移行、保留、禁止などの処理結果 |
| PCN Trace | 入力、判定、制御、実行結果の履歴 |

PCN の実装規模、入力数、判定ルール数は対象システムに応じて設定する。

基本単位は、

> **1 つの Target State Entry に対する入力状態、判定、制御、履歴を一つのエンジニアリング文脈として保持すること**

である。

詳細については、以下を参照。

[なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)

## 3.2 PCN の配置例

自動化実行ユニットでは、例えば次の入口に PCN を配置できる。

- 待機 → ピックアップ
- 配置完了 → 圧入
- 検査待ち → 検査実行
- 搬送待機 → 引渡し
- 検査完了 → 正常分流への移行（判定結果に応じて異常分流などの別経路を選択）

MES / WCS・複数設備協調では、例えば次の入口がある。

- タスク生成済み → 実行
- エリア進入前
- ステーション受入前
- 共有資源使用前
- 下流引渡し前

製造DX では、例えば次の入口がある。

- 品質放行後の次工程への移行
- 保全完了後の自動運転再開
- 作業指示切替後の目標生産状態への移行
- 手動確認後の自動運転再開

PCN の配置位置は Target State Entry を基準として決定する。

## 3.3 TPCA / PCN の導入・検証

TPCA / PCN の導入・検証は、プロジェクト段階に応じて段階的に進めることができる。

### 非介入評価 / PoC

履歴ログ、準リアルタイム状態、エクスポートデータなどを使用し、Target State Entry 単位の構造化判定と履歴形成が有効かを確認する。

### 構造化表示

判定結果を HMI、MES / WCS 画面、イベントレポートなどへ表示し、現場で Target State Entry 単位の状態確認を行う。

### 制御提案

判定結果と制御優先度調停に基づき、エンジニアまたは上位システムへ推奨制御経路を提示する。

### エンジニアリング組込み

安全要求、制御仕様、検証要求を満たすことを前提として、PCN の判定および制御ロジックを PLC / HMI、WCS、エッジコントローラ、ソフトウェアプラットフォームへ組み込む。

---

# 第 4 章 CAE-SDB：状態変数領域と判定性質

## 4.1 二軸構造

CAE-SDB は、Target State Entry に関係する状態を二つの軸で整理する。

```text
C / A / E：状態変数領域

S / D / B：判定性質
```

C / A / E は、状態が今回の状態遷移で担う役割を表す。

| 状態変数領域 | 定義 | 基本的な問い |
|---|---|---|
| C = Condition / 条件状態 | Target State へ進むための前提条件 | 必要な条件はそろっているか |
| A = Authority / 許可状態 | Target State への移行を許可する状態 | 現在、この状態へ進むことが許可されているか |
| E = Execution Chain / 実行チェーン状態 | Target State へ移行した後に必要な実行チェーン | 進入後も必要な実行チェーンを継続できるか |

重要な A：Authority は、Target State Entry に対する独立した必要制約となる場合がある。

重要な許可が成立していない場合、その Target State Entry からの移行は許可しない。

E：Execution Chain は、単体設備の Ready に加えて、下流受入、代替経路、異常経路、資源、結果書戻しなど、移行後の継続に必要な実行チェーンを対象とする。

S / D / B は、各状態に対する判定性質である。

| 判定性質 | 定義 | 基本的な問い |
|---|---|---|
| S = Structure / 構造完全性 | 必要な信号、インターフェース、マッピング、許可元、経路、実行チェーン境界が定義・接続・観測可能か | 判定に必要な構造が整っているか |
| D = Dynamics / 動的時系列有効性 | 状態が今回の Target State Entry に対する現在有効な判定根拠として使用できるか | この状態を現在の判定根拠として使用できるか |
| B = Boundary / 制御境界 | 現在有効な状態が事前定義された許容範囲、しきい値、制御境界内にあるか | 現在の状態は制御境界内にあるか |

D：Dynamics では、例えば次の状態を扱う。

- タイムアウト
- 未更新
- 期限切れ
- 遅延
- 非同期
- 競合
- 許可取消
- 状態切替
- 対象・バージョン不一致

B：Boundary では、例えば次の対象を扱う。

- 寸法、公差、偏差
- 温度、圧力、流量
- 認識信頼度
- 位置、姿勢、速度
- バッファ容量
- 資源利用範囲
- 許可範囲、時間ウィンドウ

D と B は、次のように整理できる。

```text
D：
その状態を、今回の Target State Entry に対する
現在有効な判定根拠として使用できるか。

B：
その現在有効な状態が、
事前に定義された範囲やしきい値の内側にあるか。
```

例えば、前のワークに対する画像認識結果や期限切れの結果は D の判定対象となる。

現在のワークに対応する有効な認識結果であっても、認識信頼度や位置偏差が設定範囲を外れている場合は B の判定対象となる。

## 4.2 CAE-SDB の組合せ

C / A / E と S / D / B を組み合わせることで、CAE-SDB Matrix の各セルを構成できる。

| 状態変数領域 | S：構造完全性 | D：動的時系列有効性 | B：制御境界 |
|---|---|---|---|
| C：条件状態 | C-S | C-D | C-B |
| A：許可状態 | A-S | A-D | A-B |
| E：実行チェーン状態 | E-S | E-D | E-B |

![CAE-SDB 二軸判定構造](/images/tpca/03-cae-sdb-matrix.png)

図4：C / A / E は状態変数領域、S / D / B は判定性質を示し、二つの軸を組み合わせて CAE-SDB 判定結果を形成する。

例えば、

```text
C-D：
画像認識結果が期限切れ

A-D：
許可が取り消されている

E-D：
下流状態が長時間更新されていない
```

のように、同じ D：Dynamics を異なる状態変数領域へ適用できる。

この構造により、設備やシステムごとに信号名称や実装方法が異なっても、判定結果を共通形式で整理できる。

CAE-SDB Result は、対応する S / D / B 判定が定義され、判定に必要な根拠が取得され、実際に判定を行った場合に形成する。

> **1 回の Target State Entry で、9 つすべての CAE-SDB Result を形成する必要はない。**

詳細については、以下を参照。

[なぜ CAE-SDB なのか ― 状態変数領域と判定性質の二軸構造](/jp/notes/why-cae-sdb/)

## 4.3 時間情報 T

状態および判定結果には時間情報 T を関連付ける。

時間情報 T は、次の用途に使用する。

- 状態および判定の時間位置を示す。
- 状態間の前後関係を確認する。
- D：Dynamics の判定を支援する。
- PCN Trace を形成する。

システムに応じて、Timestamp、更新時刻、イベント時刻、シーケンス時刻、バッチ時刻などを利用できる。

---

# 第 5 章 Arbitration、Multipath Control、PCN Trace、PCN Network

## 5.1 判定結果から制御へ

PCN 内部では、CAE-SDB 判定結果を制御へ接続する。

```text
CAE-SDB Result + T
→ Arbitration（制御優先度調停）
→ Multipath Control（複数経路制御）
→ Target State Entry に対する制御結果
→ 選択された制御経路の実行
→ Execution Result（実行結果）
→ PCN Trace
```

1 回の Target State Entry では、複数の CAE-SDB Result が同時に形成される場合がある。

例えば、

```text
C-D
A-B
E-D
```

が同時に存在する場合である。

Arbitration（制御優先度調停）では、

- CAE-SDB Result（CAE-SDB 判定結果）
- 重要な Authority
- 安全上の制約
- 事前定義された制御ルール
- 選択可能な制御経路

を用いて、今回の Target State Entry に対する制御上の優先関係を処理する。

今回の Target State Entry に必要な関連状態の判定結果、重要な許可、および上位の制限制約が移行条件を満たしている場合は、Target State への移行を許可する。

移行条件を満たしていない場合は、Arbitration の結果に基づいて対応する制御経路を形成する。

## 5.2 Multipath Control（複数経路制御）

代表的な制御経路には、次のものがある。

- 移行許可
- 待機
- 再確認
- 再認識
- 再サンプリング
- 再位置決め
- 再試行
- リターン
- 異常分岐
- 代替経路
- 下流調整
- 資源解放
- 縮退実行
- 手動確認
- 移行禁止
- 安全ロック
- 異常隔離
- 詳細記録

同じ CAE-SDB Result であっても、Target State Entry、安全上の制約、設備構成、制御ルールによって選択される制御経路は異なる。

Multipath Control は、今回の Target State Entry に対して、移行許可、待機、再確認、再試行、代替経路、移行禁止など、次に適用する制御処理を形成するエンジニアリング制御出力である。

代替経路やリターン経路などが別の Target State に対応する場合は、今回の Target State Entry に対する候補制御経路として扱う。実際に別の Target State へ移行する場合は、その Target State に対応する Target State Entry で改めて判定する。

## 5.3 PCN Trace

PCN Trace は、1 回の Target State Entry に対する判定・制御・実行結果を、一つの独立したエンジニアリングデータ対象として記録する。

公開範囲では、例えば次の情報を関連付ける。

| 項目 | 内容 |
|---|---|
| Current State（現在状態） | 判定時点の現在状態 |
| Target State（目標状態・目標実行経路・目標物理実行段階） | 今回移行しようとした Target State |
| Target State Entry（目標状態入口） | 今回判定対象となった目標状態入口 |
| PCN（Pre-Control Node / 前制御ノード） | 今回の判定を担当した前制御ノード |
| 関連状態 | 今回の判定に使用した主要状態 |
| 時間情報 T | 状態および判定の時間位置 |
| C / A / E 状態マッピング | 状態遷移における役割 |
| S / D / B 判定 | 各状態に対する判定 |
| CAE-SDB Result（CAE-SDB 判定結果） | 構造化判定結果 |
| Arbitration Result（制御優先度調停結果） | 制御上の優先関係を処理した結果 |
| Multipath Control（複数経路制御） | Arbitration の結果に基づいて形成された制御経路 |
| Target State Entry に対する制御結果 | 今回の目標状態入口に対する移行、保留、禁止などの処理結果 |
| Execution Result（実行結果） | 選択された制御経路を実行した結果 |
| Trace ID | 1 回の判定履歴を識別する情報 |

PCN Trace を継続して蓄積することで、

- どの Target State Entry で問題が頻発しているか。
- どの CAE-SDB 判定結果が反復しているか。
- どの複数経路制御が高頻度で選択されているか。
- 制御選択と実行結果にどのような関係があるか。
- エンジニアリング変更後に傾向がどう変化したか。

を比較できる。

詳細については、以下を参照。

[なぜ PCN Trace は新しいエンジニアリングデータなのか？](/jp/notes/why-pcn-trace-is-engineering-data/)

## 5.4 PCN Network

1 つの PCN は、1 つの Target State Entry に対応する。

複雑なシステムでは、連続、並列、分岐、相互依存する複数の Target State Entry が存在する。

複数の PCN を、状態進行、許可、資源、実行、状態更新などの依存関係に基づいて接続することで、PCN Network を構成できる。

例えば、

```text
待機
→ ピックアップ前 PCN
→ ピックアップ

ピックアップ完了
→ 配置前 PCN
→ 配置

配置完了
→ 後続段階 PCN
→ 後続実行
```

のように、複数の Target State Entry を接続できる。

PCN Network は、

> **複数の Target State Entry と、それらの間に存在する状態遷移およびエンジニアリング上の依存関係**

を表す。

各 PCN の PCN Trace を対応付けることで、複数の Target State Entry 間で反復する許可、資源、実行、状態更新などの問題をシステムレベルで分析できる。

詳細については、以下を参照。

[複数の PCN はどのように状態遷移前制御ネットワークを形成するのか？](/jp/notes/pcn-network-structure/)

---

# 第 6 章 代表的な適用方向

![TPCA / PCN の適用方向](/images/tpca/05-tpca-application-map.png)

図5：TPCA / PCN は、自動化実行ユニット、MES / WCS・複数設備協調、製造DX、デジタル呼出しなど、異なる Target State Entry へ展開できる。

## 6.1 自動化実行ユニット

代表的な対象には、次のものがある。

- ロボットピックアップ
- 圧入
- 検査
- 搬送引渡し
- 搬入・搬出
- 正常分流 / 異常分流

例えば、ロボットが Ready であっても、画像認識結果の失効、安全許可、グリッパ状態、下流受入、異常経路などが今回の Target State Entry に影響する。

PCN は目標物理実行段階へ移行する前に配置し、関連状態に対して CAE-SDB 判定を行い、Arbitration（制御優先度調停）を経て Multipath Control（複数経路制御）へ接続する。

関連事例：

[自動化実行ユニット前判定事例](/jp/cases/automation-execution-unit-pre-control/)

## 6.2 MES / WCS・複数設備協調

代表的な対象には、次のものがある。

- AGV / AMR 群制御
- タスク実行
- 共有資源使用
- エリア進入
- ステーション受入
- 下流引渡し

個別の設備に明確な故障がない状態でも、タスク、許可、資源、実行主体、下流状態などの組合せによって Waiting、Blocked、Pending が継続する場合がある。

PCN は、複数システムに分散した状態を Target State Entry に対応付け、協調停滞の判定、制御、履歴を構成する。

関連事例：

[MES / WCS 協調停滞診断モジュール事例](/jp/cases/collaborative-stagnation-diagnosis/)

## 6.3 製造DX

製造DX では、設備データ、生産データ、品質状態、保全状態、手動確認などを利用して、複数システム横断の状態遷移を設計できる。

代表例には、次のものがある。

- 品質放行後の次工程への移行
- 作業指示切替後の目標生産状態への移行
- 保全完了後の自動運転再開
- 手動確認後の自動運転再開
- 複数システムにまたがる工程状態切替

PCN は、これらの Target State Entry に分散している状態遷移条件を明示し、判定、制御、PCN Trace として整理する。

関連事例：

[製造DX 状態遷移条件設計・履歴分析事例](/jp/cases/production-dx-state-transition/)

## 6.4 デジタル呼出しへの拡張

TPCA / PCN は、明確な実行入口を持つデジタルシステムにも適用できる。

代表例には、次のものがある。

- AI 推論呼出し
- ツール呼出し
- API 実行
- 外部サービス呼出し
- 企業知識ベースへのアクセス
- 高コストモデルの呼出し

この場合も、実行入口の前で条件、権限、実行チェーンを確認し、判定結果に応じて高コスト経路、追加確認、縮退、待機、阻止などの経路を選択できる。

この領域は TPCA / PCN の拡張適用である。

適用範囲と境界については、以下を参照。

[TPCA / PCN の適用シナリオ分析](/jp/notes/tpca-pcn-applicable-scenarios/)

---

# 結語

TPCA / PCN の中核は、Target State Entry（目標状態入口）を独立したエンジニアリング対象として扱うことにある。

PCN は Target State Entry の前に配置され、関連状態を C / A / E の状態変数領域へ整理し、S / D / B の判定性質から CAE-SDB Result を形成する。続いて Arbitration で制御上の優先関係を処理し、Multipath Control を形成して、その判定・制御・実行結果を PCN Trace へ記録する。

この構造により、分散した状態情報を Target State Entry 単位の判定へ集約し、その結果を制御と履歴へ接続できる。

1 つの PCN は、1 つの明確な Target State Entry に対応する。

複数の PCN を実際の状態遷移および依存関係に沿って接続することで、PCN Network へ展開できる。

TPCA / PCN は、状態遷移条件、許可、実行チェーン、制御境界、複数経路制御、履歴を同じ状態遷移の文脈で扱うためのエンジニアリングアーキテクチャとして構成する。

---

# 関連コンテンツ

現場問題から確認する場合：

- [エンジニアリング課題](/jp/questions/)

用語定義を確認する場合：

- [Concepts｜基本概念](/jp/concepts/)

個別の技術論点を確認する場合：

- [技術ノート](/jp/notes/)

代表的な適用例を確認する場合：

- [適用事例](/jp/cases/)

著者および本サイトの位置付けを確認する場合：

- [本サイトについて](/jp/about/)

---

# バージョン情報

本稿は、**TPCA / PCN 状態遷移前制御アーキテクチャ**の公開ホワイトペーパーである。

- Public Version 1.0：2026-07-01 公開。

- Public Version 1.1：2026-08-19 更新。CAE-SDB 判定結果、Arbitration、Multipath Control、PCN Trace の階層関係を明確化。

- Public Version 1.2：2026-08-20 更新。Target State Entry を独立したエンジニアリング対象として統一し、TPCA と PCN の関係を明確化。

- Public Version 1.3：2026-08-21 更新。時間情報 T、状態インスタンス、PCN Trace、PCN Network、Multipath Control に関する説明を更新。

- Public Version 1.4：2026-08-25 更新。CAE-SDB の二軸構造説明を整理。

- Public Version 1.5：2026-09-09 更新。9 ステップのエンジニアリング分析順序を追加し、Target State Entry、CAE-SDB、Arbitration、Multipath Control、PCN Trace、PCN Network の公開表現を統一。

著者：全野南政 / Nansei Zenno

推奨引用形式：

```text
全野南政 / Nansei Zenno，《TPCA / PCN 状態遷移前制御アーキテクチャ》，公開ホワイトペーパー，Public Version 1.5，2026-09-09，https://zennns.com/jp/whitepaper/
```
