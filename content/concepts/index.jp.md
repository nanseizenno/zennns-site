---
title: "概念・用語"
summary: "TPCA / PCN 状態遷移前制御体系における中核用語を整理する。Current State、Target State、Target State Entry、前制御、TPCA、PCN、関連状態、C / A / E、S / D / B、CAE-SDB Result、時間情報 T、Arbitration、Multipath Control、PCN Trace、PCN Runtime、PCN Network を含む。"
description: "TPCA / PCN 状態遷移前制御体系における中核用語と相互関係を整理する。Target State Entry、PCN、CAE-SDB、制御優先度調停、複数経路制御、PCN Trace、PCN Runtime、PCN Network の公開定義を示す。"
draft: false
date: 2026-07-04
lastmod: 2026-09-09
author: "全野南政 / Nansei Zenno"
ShowReadingTime: false
ShowToc: true
TocOpen: true
---

本ページでは、TPCA / PCN 状態遷移前制御体系で使用する中核用語を整理する。

これらの用語は、公開説明、適用事例、協業時の説明、今後の技術文書における共通用語として使用する。

TPCA / PCN の中核となる考え方は、次の通りである。

> **明確な Target State Entry（目標状態入口）は、独立して設計・判定・制御・記録できるエンジニアリング対象として扱う。**

TPCA / PCN と既存技術との関係については、以下を参照。

[TPCA / PCN と既存の産業オートメーション技術・エンジニアリング手法との関係](/jp/notes/tpca-existing-theories/)

---

## 中核用語クイックリファレンス

| 用語 | 日本語名称 | 基本的な役割 |
|---|---|---|
| TPCA | 状態遷移前制御アーキテクチャ | 明確な Target State Entry を対象として、前置判定、制御、履歴を構成する全体アーキテクチャ |
| PCN | 前制御ノード | 1 つの明確な Target State Entry の前に配置するエンジニアリングノード |
| Current State | 現在状態・現在段階・現在経路位置 | システムが現在位置している状態、工程段階、または経路位置 |
| Target State | 目標状態・目標実行経路・目標物理実行段階 | システムが次に入ろうとしている状態、実行経路、または物理実行段階 |
| Target State Entry | 目標状態入口 | Current State から Target State へ進む際に前置判定の対象となるエンジニアリング上の入口 |
| 関連状態 | Target State Entry に関係する状態 | 今回の状態遷移に必要な、複数の情報源から取得される状態 |
| C | Condition / 条件状態 | Target State へ進むための前提条件に関係する状態変数領域 |
| A | Authority / 許可状態 | Target State への進入許可に関係する状態変数領域 |
| E | Execution Chain / 実行チェーン状態 | Target State へ進入した後に必要となる実行チェーンに関係する状態変数領域 |
| S | Structure / 構造完全性 | 判定に必要な信号、インターフェース、マッピング、許可元、経路、役割、実行チェーン境界が定義・接続され、観測可能かを判定する特性 |
| D | Dynamics / 動的時系列有効性 | 関連状態を今回の Target State Entry に対する現在有効な判定根拠として使用できるかを判定する特性 |
| B | Boundary / 制御境界 | 現在有効な関連状態が、事前定義された許容範囲、しきい値、制御境界内にあるかを判定する特性 |
| CAE-SDB | 構造化判定ロジック | C / A / E の状態変数領域と S / D / B の判定特性を組み合わせる二軸判定構造 |
| CAE-SDB Result | CAE-SDB 判定結果 | 1 回の前置判定によって形成される 1 つまたは複数の構造化判定結果 |
| T | 時間情報 | 状態および判定とともに保持し、前後関係、D 判定、PCN Trace に使用する時間情報 |
| Arbitration | 制御優先度調停 | CAE-SDB 判定結果、重要な許可、制御制約などに基づいて制御上の優先関係を処理する |
| Multipath Control | 複数経路制御 | Arbitration の結果に基づいて、進入許可、待機、再確認、再試行、代替経路、移行禁止など、次に適用する制御処理を形成する |
| PCN Trace | PCN 状態遷移判定履歴 | 1 回の Target State Entry における入力、判定、時間情報、制御結果、実行結果を関連付けて記録する |
| PCN Runtime | PCN ランタイム | 単一 PCN のオンライン状態処理、判定、制御、履歴生成を実行するランタイム基盤 |
| PCN Network | PCN ネットワーク | 複数の PCN と Target State Entry 間の状態遷移および依存関係を接続した前制御構造 |

TPCA / PCN の基本的な工程関係は、次のように表せる。

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
   → CAE-SDB 判定結果 + T
   ↓
⑤ 制御優先度調停（Arbitration）
   ↓
⑥ 複数経路制御（Multipath Control）
   ↓
⑦ Target State Entry に対する制御を適用
   ├─ 進入許可
   ├─ 待機・再確認・再試行
   ├─ 別の Target State
   └─ 進入禁止 など
   ↓
⑧ 選択された制御経路を実行
   → 実行結果
   ↓
⑨ PCN Trace（状態遷移判定履歴）
   → 入力・判定・制御・実行結果を関連付けて記録
```

PCN Runtime は、単一 PCN のオンライン処理を実行するランタイム基盤である。

複数の PCN を、Target State Entry 間の実際の状態遷移関係、および許可、資源、実行、状態更新などの依存関係に基づいて接続すると、PCN Network を形成できる。

---

## Current State、Target State、Target State Entry

**Current State（現在状態・現在段階・現在経路位置）** は、状態遷移前にシステムが現在位置している状態、工程段階、または経路位置を示す。

**Target State（目標状態・目標実行経路・目標物理実行段階）** は、システムが次に入ろうとしている状態、実行経路、または物理実行段階を示す。

**Target State Entry（目標状態入口）** は、システムが Current State から Target State へ進もうとする際に、前置判定の対象となるエンジニアリング上の入口である。

例えば、次のような状態遷移が該当する。

- 待機段階 → ピックアップ段階
- 配置完了 → 圧入段階
- 検査待ち → 検査実行段階
- タスク存在 → タスク実行
- AGV 到着 → ステーション受入
- 現在リクエスト → 目標呼出経路

Target State には、正常な次工程だけでなく、あらためて移行判定が必要となる手直し、リターン、退避、異常分岐、再投入、代替経路なども含めることができる。

実運転では、同じ状態タイプへ再進入する場合も新しい状態インスタンスとして扱う。

```text
State Type:
A → B → A

State Instance:
A₁ → B₁ → A₂
```

Current State、Target State、Target State Entry を明確にすることが、PCN を設定する基本となる。

---

## 前制御

前制御とは、Target State Entry の前で、今回の状態遷移に関係する状態を構造化して判定し、その判定結果を制御優先度調停と複数経路制御へ接続する考え方である。

前制御では、主に次の事項を扱う。

- Target State へ進むための条件
- Target State への進入許可
- 進入後の実行チェーン
- 判定に必要な構造完全性
- 状態の動的時系列有効性
- 事前定義された制御境界
- 複数判定結果の制御上の優先関係
- 今回の Target State Entry に対して適用する制御処理
- 判定、制御、実行結果の履歴

---

## TPCA

英語：Transition Pre-Control Architecture

日本語：状態遷移前制御アーキテクチャ。

TPCA は、明確な Target State Entry を中心として構築する状態遷移前制御の全体アーキテクチャである。

装置、制御プログラム、MES / WCS、安全システム、人による確認、その他のエンジニアリングインターフェースに分散している関連状態を、Target State Entry 単位の判定、制御、記録へ整理する。

基本階層は次の通りである。

```text
TPCA
→ PCN
→ CAE-SDB
→ 制御優先度調停
→ 複数経路制御
→ PCN Trace
```

{{< pcn-animation >}}

TPCA は、PLC、ステートマシン、SFC、Interlock、安全制御、MES / WCS などと役割分担し、Target State Entry 単位の前置判定、制御、履歴を構成する。

---

## PCN

英語：Pre-Control Node

日本語：前制御ノード。

PCN は、1 つの明確な Target State Entry の前に配置するエンジニアリングノードである。

1 つの PCN は 1 つの Target State Entry に対応し、主に次の処理を構成する。

- Current State と Target State の確認
- 関連状態の取得と整理
- C / A / E 状態マッピング
- S / D / B 判定
- CAE-SDB Result の生成
- 時間情報 T の保持
- Arbitration
- Multipath Control
- PCN Trace の生成

PCN の実装形式は対象システムに応じて決定する。

例えば、PLC ファンクションブロック、産業用エッジコントローラ、ソフトウェア判定モジュール、MES / WCS 上の判定モジュールなどとして実装できる。

---

## PCN Runtime

英語：PCN Runtime

日本語：PCN ランタイム。

PCN Runtime は、単一 PCN のオンライン状態処理、判定、制御、履歴生成を実行するランタイム基盤である。

主な処理は次の通りである。

```text
関連状態取得
→ C / A / E 状態マッピング
→ S / D / B 判定
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

PCN Runtime の具体的なライフサイクル、Rule Pack、完全な Arbitration、主要パラメータ、インターフェース構成などは内部実装範囲とする。

---

## PCN Network

英語：PCN Network

日本語：PCN ネットワーク。

PCN Network は、複数の PCN と Target State Entry を、実際の状態遷移関係、および許可、資源、実行、状態更新などの依存関係に基づいて接続した前制御構造である。

例えば、

```text
State A
→ PCN-1
→ State B
→ PCN-2
→ State C
```

のような関係を構成できる。

PCN Network では、例えば次の関係を扱う。

- 状態進行
- 許可依存
- 資源依存
- 実行チェーンの接続
- 状態更新・書戻し
- PCN Trace 間の履歴関係

装置ユニット、生産ライン、MES / WCS、AGV / AMR 群制御、製造 DX、デジタルシステムなど、異なるシステム階層へ PCN を配置できる。

状態タイプの関係には循環を含めることができる。

実運転で生成される状態インスタンスは、時間方向へ継続して生成される。

---

## 関連状態

関連状態とは、1 回の Target State Entry における前置判定に使用する状態を指す。

状態の取得元には、例えば次のものがある。

- PLC
- ロボットコントローラ
- 画像認識システム
- 安全システム
- HMI / SCADA
- MES
- WCS
- AGV / AMR スケジューリングシステム
- 現場センサ
- 上位システム
- 人による確認
- デジタルシステムインターフェース

PCN は、関連状態を今回の Target State Entry における役割に基づいて C / A / E へマッピングする。

同じ状態でも、Target State Entry が変われば異なる役割を持つ場合がある。

状態には必要に応じて、次のような付随情報を関連付けることができる。

- タイムスタンプ
- 更新時刻
- 状態バージョン
- シーケンス情報
- ロット番号
- オブジェクト ID
- イベント ID
- その他、今回の状態遷移に関係するトレース情報

---

## CAE-SDB

CAE-SDB は、PCN 内部で使用する構造化判定ロジックである。

基本構造は次の通りである。

```text
{C, A, E} × {S, D, B}
```

- C / A / E：状態変数領域
- S / D / B：判定特性

両者を組み合わせることで、次の判定座標を構成する。

|   | S | D | B |
|---|---|---|---|
| C | C-S | C-D | C-B |
| A | A-S | A-D | A-B |
| E | E-S | E-D | E-B |

1 回の前置判定では、1 つまたは複数の CAE-SDB Result が形成される場合がある。

各状態および判定結果には、必要な時間情報 T を関連付ける。

```text
CAE-SDB Result + T
→ Arbitration
→ Multipath Control
```

CAE-SDB は、Target State Entry に関係する状態を「状態変数領域 × 判定特性」の共通形式で表現し、後続の制御と履歴へ接続する。

---

## C：Condition

日本語：条件状態。

C は、Target State へ進むための前提条件に関係する状態変数領域である。

代表例を示す。

- ワークが存在している
- 対象、位置、姿勢が要求条件を満たしている
- 認識結果が取得されている
- タスクが存在している
- 必要なパラメータが揃っている
- 前工程が完了している
- 必要なデータが存在している

C が扱う基本的な問いは、

> **この Target State へ進むための前提条件が揃っているか。**

である。

---

## A：Authority

日本語：許可状態。

A は、Target State への進入を許可する状態に関係する状態変数領域である。

代表例を示す。

- 安全許可
- 上位システムからの許可
- エリア許可
- 人による確認
- 権限・認可
- 資源ロック
- 相手機器の許可

重要な A は、Target State Entry に対する独立した必要制約となる。

重要な許可が成立していない場合、その Target State Entry への進入は許可しない。

A が扱う基本的な問いは、

> **現在、この Target State へ進むことが許可されているか。**

である。

---

## E：Execution Chain

日本語：実行チェーン状態。

E は、Target State へ進入した後、その段階を継続・完了するために必要となる実行チェーンに関係する状態変数領域である。

実行チェーンには、例えば次の要素が含まれる。

- 本体装置
- エンドエフェクタ
- 下流受入
- 正常実行経路
- 代替経路
- リターン経路
- 異常排出経路
- 結果アップロード・書戻し経路
- 相手機器の受入状態

Robot Ready などの局所的な運転準備状態も E の入力となり得る。

E が扱う基本的な問いは、

> **Target State へ進入した後、必要な実行チェーンが継続できるか。**

である。

---

## S：Structure

日本語：構造完全性。

S は、C / A / E の関連状態に対して適用する判定特性である。

S は、今回の状態遷移判定に必要なエンジニアリング構造が定義・接続され、観測可能かを判定する。

代表的な確認対象を示す。

- 必要信号の定義
- インターフェース接続
- 状態と対象のマッピング
- 許可元
- 実行チェーンの関係と境界
- 必要状態の可観測性

S が確認する基本的な問いは、

> **今回の判定に必要な構造が定義され、接続され、観測可能か。**

である。

---

## D：Dynamics

日本語：動的時系列有効性。

D は、C / A / E の関連状態に対して適用する判定特性である。

D は、その状態を今回の Target State Entry に対する現在有効な判定根拠として使用できるかを判定する。

代表的な確認対象を示す。

- タイムアウト
- 未更新
- 期限切れ
- チャタリング
- 競合
- 遅延
- 非同期
- バージョン不一致
- シーケンス関係
- 許可取消
- 状態切替中

例えば、

```text
VisionOK = TRUE
```

であっても、その値が前のワークに対する結果であれば、現在の Target State Entry の判定には使用できない。

D が確認する基本的な問いは、

> **この状態を、今回の Target State Entry に対する有効な判定根拠として現在も使用できるか。**

である。

---

## B：Boundary

日本語：制御境界。

B は、C / A / E の関連状態に対して適用する判定特性である。

B は、現在有効な関連状態が、事前に定義された許容範囲、しきい値、または制御境界内にあるかを判定する。

代表的な境界条件を示す。

```text
Min / Max
Threshold
Tolerance
Range
Time Window
Quota
Capacity
Rate Limit
Retry Limit
```

具体例には、寸法、公差、認識信頼度、位置偏差、容量、資源利用範囲、時間ウィンドウなどがある。

B が確認する基本的な問いは、

> **現在の状態が、今回の Target State Entry に対して事前に定義された制御境界内にあるか。**

である。

---

## CAE-SDB Result

日本語：CAE-SDB 判定結果。

CAE-SDB Result は、C / A / E の状態変数領域に対して S / D / B の判定を行った結果として形成される構造化判定結果である。

例えば、

```text
C-D
```

は、条件状態について動的時系列有効性に関する結果が確認されたことを示す。

```text
E-S
```

は、実行チェーン状態について構造完全性に関する結果が確認されたことを示す。

1 回の状態遷移前置判定で、複数の CAE-SDB Result が同時に形成される場合もある。

```text
C-D + E-D
```

この場合、条件状態と実行チェーン状態の両方について、動的時系列有効性に関する結果が確認されたことを示す。

CAE-SDB Result は、

> **どの状態変数領域で、どの判定特性に関する結果が確認されたか**

を共通形式で表す。

各判定結果には、必要な時間情報 T を関連付ける。

---

## 時間情報 T

T は、状態および CAE-SDB Result とともに保持する時間情報である。

システムに応じて、例えば次の情報を利用できる。

- Timestamp
- 更新時刻
- イベント時刻
- シーケンス時刻
- ロット時刻
- その他、状態の前後関係を特定できる時間情報

T は主に次の目的で使用する。

- 状態および判定が発生した時間位置を特定する
- 複数状態間の前後関係を確認する
- D：Dynamics の判定を支援する
- PCN Trace を形成する

---

## Arbitration

英語：Arbitration

日本語：制御優先度調停。

Arbitration は、1 つまたは複数の CAE-SDB Result、重要な許可、制御制約などに基づき、今回の Target State Entry に対する制御上の優先関係を処理する。

基本的な位置は次の通りである。

```text
CAE-SDB Result + T
→ Arbitration
→ Multipath Control
```

本サイトでは、Arbitration のエンジニアリング上の位置と基本的な役割を公開する。

具体的な制御優先度、完全な調停ロジック、主要パラメータなどは内部実装範囲とする。

---

## Multipath Control

英語：Multipath Control

日本語：複数経路制御。

Multipath Control は、Arbitration の結果に基づき、今回の Target State Entry に対して次に適用する制御処理を形成するエンジニアリング制御出力である。

代表的な制御処理を示す。

- 移行許可
- 待機
- 再確認
- 再認識
- 再サンプリング
- 再位置決め
- 再試行
- リターン
- 異常分岐
- 下流調整
- 資源解放
- 縮退実行
- 代替経路
- 移行禁止
- 安全ロック
- 手動確認
- 異常隔離
- 詳細記録

基本関係は次の通りである。

```text
CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ 選択された制御経路
→ 実行結果
```

---

## PCN Trace

日本語：PCN 状態遷移判定履歴。

PCN Trace は、1 回の Target State Entry における入力状態、判定、制御、実行結果を関連付けて記録する状態遷移判定履歴である。

代表的な記録内容を示す。

- Current State
- Target State
- Target State Entry
- PCN
- 関連状態
- 時間情報 T
- C / A / E 状態マッピング
- S / D / B 判定
- CAE-SDB Result
- Arbitration Result
- Multipath Control
- 実行結果
- Trace ID

PCN Trace により、

```text
どの Target State へ進もうとしていたか
→ どの状態を判定に使用したか
→ どの CAE-SDB Result が形成されたか
→ どの制御処理が選択されたか
→ どのような実行結果となったか
```

を一つの状態遷移判定履歴として追跡できる。

PCN Trace は、現場振り返り、問題追跡、状態遷移設計レビュー、長期履歴比較、エンジニアリング改善などに利用できる。

具体的な Trace Schema、保存方式、索引方式、再生機構などは内部実装範囲とする。

---

## 中核用語の関係

TPCA / PCN の中核用語の関係は、次のように整理できる。

```text
TPCA
│
├─ PCN
│   │
│   ├─ 1 つの Target State Entry に対応
│   │
│   └─ PCN Runtime
│       ├─ 関連状態取得
│       ├─ C / A / E 状態マッピング
│       ├─ S / D / B 判定
│       ├─ CAE-SDB Result + T
│       ├─ Arbitration
│       ├─ Multipath Control
│       └─ PCN Trace
│
└─ 複数の PCN
    ↓
    PCN Network
```

各用語の位置付けは次の通りである。

- **TPCA**：全体アーキテクチャ
- **PCN**：1 つの Target State Entry に対応する前制御ノード
- **PCN Runtime**：単一 PCN のオンライン処理を実行するランタイム基盤
- **関連状態**：今回の Target State Entry に関係する入力状態
- **C / A / E**：状態変数領域
- **S / D / B**：判定特性
- **CAE-SDB Result**：構造化判定結果
- **T**：状態および判定とともに保持する時間情報
- **Arbitration**：制御優先度調停
- **Multipath Control**：今回の Target State Entry に対して適用する複数経路制御
- **PCN Trace**：1 回の状態遷移判定履歴
- **PCN Network**：複数の PCN と Target State Entry 間の状態遷移・依存関係を扱う前制御構造

---

## 関連資料

- [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)
- [技術ノート](/jp/notes/)
- [エンジニアリング課題](/jp/questions/)
- [適用事例](/jp/cases/)

---

本ページは、TPCA / PCN 状態遷移前制御体系の公開用語定義資料である。
