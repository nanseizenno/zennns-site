---
title: "なぜ PCN は TPCA の最小エンジニアリングノードなのか？"
summary: "PCN が1つの明確な Target State Entry に対応し、関連状態の取得、CAE-SDB 判定、Arbitration、Multipath Control、PCN Trace を一つの工程単位として構成する理由を説明する。"
description: "TPCA における最小エンジニアリングノードとしての PCN の位置付けと基本構造を説明する。"
date: 2026-07-04
lastmod: 2026-09-08
author: "全野南政 / Nansei Zenno"
document_type: "技術ノート"
version: "Public Note Version 1.3"
citation_url: "https://zennns.com/jp/notes/pcn-minimum-engineering-unit/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## なぜ PCN は TPCA の最小エンジニアリングノードなのか？

TPCA は、状態遷移前制御アーキテクチャである。

PCN（Pre-Control Node / 前制御ノード）は、明確な Target State Entry の前に配置するエンジニアリングノードである。

1つの PCN は、1つの明確な Target State Entry に対応する。

PCN は、その Target State Entry に関係する状態を取得し、構造化判定、制御、履歴を一つのエンジニアリング単位として整理する。

基本関係は次の通りである。

```text
Current State
    ↓
Target State Entry / PCN
    ↓
Target State
```

PCN 内では、今回の Target State Entry に関係する状態を取得し、次の処理へ接続する。

```text
関連状態
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

ここで、

```text
C = Condition         条件状態
A = Authority         許可状態
E = Execution Chain   実行チェーン状態

S = Structure         構造完全性
D = Dynamics          動的時系列有効性
B = Boundary          制御境界
```

である。

PCN は、TPCA の全体アーキテクチャを具体的な Target State Entry へ展開する際の最小エンジニアリングノードとして位置付けられる。

基本概念については、以下を参照。

- [Concepts｜中核概念](/jp/concepts/)
- [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)
- [なぜ状態遷移条件を明示する必要があるのか？](/jp/notes/explicit-state-transition-conditions/)
- [なぜ CAE-SDB なのか ― 状態変数領域と判定特性の二軸構造](/jp/notes/why-cae-sdb/)

---

## 1. PCN は Target State Entry の前に配置する

PCN を設定する際は、まず Current State と Target State を明確にする。

```text
Current State
→ Target State
```

そのうえで、両者の間に Target State Entry を設定し、その入口の前に PCN を配置する。

例えば、ロボットが待機状態からピックアップ段階へ進む場合は、次のように整理できる。

```text
ロボット待機
    ↓
Target State Entry / PCN
    ↓
ピックアップ段階
```

PCN は、ピックアップ段階へ進入するために必要な状態を取得し、進入前に判定と制御を行う。

1つの PCN は、1つの明確な Target State Entry に対応する。

複雑な設備やシステムでは複数の Target State Entry が存在するため、同一設備内や複数システム間に複数の PCN を配置できる。

PCN の配置単位は設備台数やコントローラ台数ではなく、

> **どこに独立した Target State Entry を設定するか**

によって決まる。

---

## 2. 1つの PCN を構成する基本要素

1つの PCN は、少なくとも次の対象を整理する。

| 対象 | エンジニアリング上の役割 |
|---|---|
| Current State | 今回の状態遷移前にシステムが存在する状態、工程段階、実行位置 |
| Target State | システムが次に進入しようとする状態、実行経路、物理実行段階 |
| Target State Entry / PCN | 今回の状態遷移前判定を行う工程位置 |
| 関連状態 | 今回の Target State Entry に関係する状態情報 |
| C / A / E Mapping | 関連状態を Condition、Authority、Execution Chain へ整理する |
| S / D / B Evaluation | 関連状態を Structure、Dynamics、Boundary の観点から判定する |
| CAE-SDB Result | 今回の Target State Entry に対する構造化判定結果 |
| 時間情報 T | 状態および判定とともに保持する時間情報 |
| Arbitration | 複数の判定結果や重要な制約に基づいて制御上の優先関係を処理する |
| Multipath Control | 今回の Target State Entry に対する制御経路を形成する |
| PCN Trace | 今回の Target State Entry における判定・制御・実行結果を記録する |

これらを一つの Target State Entry に対応付けることで、

```text
状態入力
→ 構造化判定
→ 制御
→ 履歴
```

を同じエンジニアリング文脈で扱うことができる。

各 PCN の入力数、判定ルール、制御経路、実装規模は、対象設備やシステムに応じて異なる。

---

## 3. なぜこれが「最小エンジニアリングノード」なのか

TPCA における「最小エンジニアリングノード」は、ソフトウェアサイズや信号数の最小値を意味しない。

1つの現場信号、1つの Ready 状態、1つの許可、1つの Interlock、1つの判定結果、1つの制御出力だけでは、Target State Entry に対する判定と制御の全体関係を表すことはできない。

PCN は、

> **1回の明確な Target State Entry に対する状態入力、構造化判定、制御、履歴を一つの責任単位として保持できる最小のエンジニアリングノード**

である。

基本関係は次のように表せる。

```text
Target State Entry / PCN
    ↓
関連状態
    ↓
CAE-SDB
    ↓
Arbitration
    ↓
Multipath Control
    ↓
PCN Trace
```

この単位より大きくすると、複数の Target State Entry が一つの判定責任に混在しやすくなる。

一方、この単位より細かく分解すると、個別信号や個別判定だけが残り、Target State Entry に対する一連の工程関係が失われる。

そのため、PCN は TPCA を具体的なシステムへ展開する際の最小エンジニアリングノードとなる。

---

## 4. PCN は分散した状態を1つの Target State Entry に集約する

複雑な自動化システムでは、1回の Target State Entry に必要な状態が複数の設備やシステムに分散している。

例えば、ロボットがピックアップ段階へ進む場合、関連状態は次のような情報源から取得されることがある。

- 画像認識システム
- ロボットコントローラ
- PLC
- 安全システム
- 搬送設備
- 下流設備
- 上位システム

これらの状態は、それぞれ異なる装置やインターフェースに存在していても、今回の Target State Entry に対する判定という共通の目的を持つ。

PCN は、分散している関連状態を1つの Target State Entry に対応付ける。

```text
画像認識
ロボット
PLC
安全システム
搬送設備
下流設備
上位システム
      ↓
Target State Entry / PCN
      ↓
C / A / E Mapping
      ↓
S / D / B Evaluation
      ↓
CAE-SDB Result
```

この構造によって、

> **状態がどこに存在しているか**

と、

> **今回の状態遷移で何のために使用するか**

を分けて整理できる。

PCN の役割は、分散したすべての情報を一か所へ集中的に管理することではない。

今回の Target State Entry に必要な状態を明確に対応付け、判定と制御の責任範囲を形成することにある。

関連事例：

- [自動化実行ユニット前判定事例](/jp/cases/automation-execution-unit-pre-control/)

---

## 5. PCN は異なるシステム階層へ配置できる

PCN は特定の PLC、設備、MES / WCS に固定された実装単位ではない。

Target State Entry が存在するシステム階層に応じて配置できる。

### 自動化実行ユニット

例えば、

- ロボットがピックアップ段階へ進入する前
- 圧入段階へ進入する前
- 検査実行段階へ進入する前
- 搬送引渡しへ進入する前

などに配置できる。

実装形式には、PLC ファンクションブロック、産業用コントローラ、エッジコントローラ、ソフトウェア判定モジュールなどを使用できる。

### MES / WCS・群制御協調

例えば、

- タスク実行へ進入する前
- 資源使用へ進入する前
- ステーション受入へ進入する前
- エリア進入へ進む前
- 協調実行状態へ移行する前

などに配置できる。

### 生産 DX

例えば、

- 品質放行後の次工程進入前
- 作業指示切替後の目標生産状態への進入前
- 保全完了後の自動運転再開前
- 下流生産状態への進入前

などに配置できる。

適用階層が異なっても、PCN の基本関係は共通する。

```text
Current State
    ↓
Target State Entry / PCN
    ↓
Target State
```

そして PCN 内では、

```text
関連状態
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result
→ Arbitration
→ Multipath Control
→ PCN Trace
```

という一連の工程関係を構成する。

PCN の実装形式は、対象システムに応じて選択する。

---

## 関連技術ノート

PCN から派生する履歴構造と複数ノード構造については、以下の専用技術ノートで説明する。

### [なぜ PCN Trace は新しいエンジニアリングデータなのか？](/jp/notes/why-pcn-trace-is-engineering-data/)

PCN Trace が1回の Target State Entry における判定、制御、実行結果をどのように記録し、比較・振り返り可能なエンジニアリングデータを形成するかを説明する。

### [複数の PCN はどのように状態遷移前制御ネットワークを形成するのか？](/jp/notes/pcn-network-structure/)

複数の PCN が、実際の状態遷移関係、および許可・資源・実行依存関係に基づいてどのように接続され、PCN Network を形成するかを説明する。

---

## まとめ

PCN（Pre-Control Node / 前制御ノード）は、1つの明確な Target State Entry に対応する。

PCN は、その入口に関係する状態を取得し、

```text
関連状態
→ CAE-SDB
→ Arbitration
→ Multipath Control
→ PCN Trace
```

という一連の工程関係を構成する。

PCN の「最小」は、信号数やソフトウェアサイズの最小値を意味するものではない。

> **1回の Target State Entry に対する状態入力、判定、制御、履歴を一つの責任単位として保持できる最小のエンジニアリングノード**

という意味である。

この単位を基準とすることで、TPCA の全体アーキテクチャを、具体的な設備、制御システム、MES / WCS、生産 DX などの Target State Entry へ展開できる。

---

## 文書情報

題目：なぜ PCN は TPCA の最小エンジニアリングノードなのか？  
文書種別：技術ノート  
バージョン：Public Note Version 1.3  
初回公開日：2026-07-04  
最終更新日：2026-09-08  
著者：全野南政 / Nansei Zenno  
現在の URL：https://zennns.com/jp/notes/pcn-minimum-engineering-unit/

---

本稿は、TPCA / PCN 状態遷移前制御体系の公開説明資料である。
