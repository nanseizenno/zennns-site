---
title: "なぜ PCN は TPCA の最小エンジニアリングノードなのか？"
summary: "PCN が TPCA の最小エンジニアリングノードを構成する理由と、1 つの明確な Target State Entry に対して、複数系統の状態、構造化判定、Arbitration、Multipath Control、PCN Trace までの一連のエンジニアリング関係をどのように形成するかを説明する。"
description: "TPCA 状態遷移前制御体系における PCN のエンジニアリング上の位置付けを説明する。PCN が明確な Target State Entry を中心として、Current State、Target State、複数系統の状態、C / A / E Mapping、S / D / B Evaluation、CAE-SDB Result、時間情報 T、Arbitration、Multipath Control、PCN Trace をどのように整理するかを示す。"
date: 2026-07-04
lastmod: 2026-08-20
author: "全野南政 / Nansei Zenno"
document_type: "技術ノート"
version: "Public Note Version 1.2"
citation_url: "https://zennns.com/jp/notes/pcn-minimum-engineering-unit/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

TPCA は、状態遷移前制御アーキテクチャである。

PCN（Pre-Control Node / 前制御ノード）は、明確な Target State Entry の前に配置するエンジニアリングノードである。

CAE-SDB は、PCN 内部で使用する構造化判定ロジックである。

1 つの PCN は、1 回の明確な Target State Entry に関係する入力状態、判定、Arbitration、Multipath Control、PCN Trace を同じエンジニアリング対象として整理する。

基本的な構成は次の通りである。

```text
Current State
→ Target State
→ PCN
    ├─ 複数系統の状態
    ├─ C / A / E Mapping
    ├─ S / D / B Evaluation
    ├─ CAE-SDB Result + T
    ├─ Arbitration
    ├─ Multipath Control
    └─ PCN Trace
```

PCN は、TPCA の全体アーキテクチャを具体的な Target State Entry に適用する際の最小エンジニアリングノードである。

基本概念については、以下を参照。

- [Concepts｜中核概念](/jp/concepts/)
- [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)
- [なぜ状態遷移条件を明示する必要があるのか？](/jp/notes/explicit-state-transition-conditions/)

---

## 1. PCN は明確な Target State Entry の前に配置する

TPCA は、Target State、目標実行経路、または目標物理実行段階へ入る前の判定と制御を対象とする。

PCN を設定する際は、まず次の関係を明確にする。

```text
Current State → Target State
```

その上で、PCN を Target State Entry の前に配置する。

例えば、

```text
ロボット待機
→ PCN
→ ピックアップ段階
```

という構成では、PCN はロボットがピックアップ段階へ入る前に、今回の Target State Entry に関係する状態を取得し、判定と制御を行う。

また、

```text
検査完了
→ PCN
→ 正常分流 / 異常分流 / その他の処理経路
```

という構成では、PCN は候補となる Target State または目標実行経路へ進む前に、必要な状態を判定する。

1 つの PCN は、1 つの明確な Target State Entry に対応する。

複雑な設備には複数の Target State Entry が存在するため、1 台の設備内に複数の PCN を配置できる。

設備間、コントローラ間、上位システム間、または手動確認を含む状態遷移についても、明確な Target State Entry を設定できる場合は、その入口に対応する PCN を構成できる。

---

## 2. 1 つの PCN を構成する基本要素

1 つの PCN は、少なくとも次の対象を整理する。

| 対象 | エンジニアリング上の役割 |
|---|---|
| Current State | システムが現在位置している状態、工程段階、または実行位置 |
| Target State | システムが次に入ろうとしている状態、目標実行経路、または目標物理実行段階 |
| PCN の配置位置 | 今回の Target State Entry をどこに設定するか |
| 複数系統の状態 | 今回の状態遷移に関係する入力状態 |
| C / A / E Mapping | 関連状態を Condition、Authority、Execution Chain の状態変数領域へマッピングする |
| S / D / B Evaluation | Structure、Dynamics、Boundary の判定性質から関連状態を評価する |
| CAE-SDB Result | 1 回の前判定によって形成される 1 つまたは複数の構造化判定結果 |
| 時間情報 T | 状態および判定とともに保持し、状態の前後関係、D の判定、PCN Trace に使用する |
| Arbitration | CAE-SDB Result と事前定義された制御制約に基づき、制御上の優先関係を処理する |
| Multipath Control | Arbitration の結果に基づいて、次の Target State または目標実行経路を決定する |
| PCN Trace | 今回の Target State Entry における入力、判定、時間情報、制御出力、実行結果を記録する |

これらの要素によって、1 回の Target State Entry に対する状態入力から判定、制御、履歴までの関係を一つのエンジニアリング単位として扱うことができる。

各 PCN の入力数、判定ルール、制御経路、実装規模は、対象設備やシステムによって異なる。

共通するのは、

> **1 つの明確な Target State Entry を中心として、状態入力、構造化判定、Arbitration、Multipath Control、PCN Trace を一連の関係として構成すること**

である。

---

## 3. 「最小エンジニアリングノード」の意味

ここでいう「最小」は、信号数、ソフトウェアサイズ、PLC ファンクションブロックの大きさ、判定ルール数などの実装規模を指すものではない。

TPCA における最小単位は、

> **1 回の明確な Target State Entry に対する状態遷移前判定、制御出力、状態遷移判定履歴を一つの関係として保持できるエンジニアリング組織単位**

を意味する。

PCN をさらに構成要素へ分解すると、例えば次のような対象になる。

- 1 つの現場信号
- 1 つの Ready 状態
- 1 つの許可状態
- 1 つの Interlock
- 1 つの S / D / B Evaluation
- 1 つの CAE-SDB Result
- 1 つの制御出力

これらは PCN を構成する要素である。

PCN は、それらを今回の Target State Entry に対応付け、次の関係としてまとめる。

```text
Target State Entry
→ 複数系統の状態
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

この単位まで構成することで、Target State Entry に対する判定根拠、構造化判定結果、制御結果、履歴を同じエンジニアリング文脈で扱うことができる。

そのため、PCN は TPCA を具体的なシステムへ展開する際の最小エンジニアリングノードとなる。

---

## 4. PCN は分散した現場状態を Target State Entry に対応付ける

複雑なシステムでは、1 回の Target State Entry に必要な状態が複数の設備やシステムに分散している。

例えば、ロボットがピックアップ段階へ入る場合、関連状態は次のような情報源から取得されることがある。

- 画像認識システム
- ロボットコントローラ
- PLC
- 安全システム
- メインコンベヤ
- 正常配置先
- 回流経路
- 異常分流経路
- 上位システム

PCN は、これらの状態を取得元ではなく、今回の Target State Entry における役割に基づいて C / A / E へマッピングする。

### C：Condition

C は、Target State へ入るために必要な事実条件に関係する状態変数領域である。

例えば、

- ワーク存在状態
- 画像認識結果
- ワーク位置
- ワーク姿勢

などが該当する。

### A：Authority

A は、Target State への進入を許可する状態に関係する状態変数領域である。

例えば、

- 安全許可
- エリア許可
- 上位システム許可
- 今回の動作に必要な許可
- 手動確認

などが該当する。

重要な A は、Target State Entry に対する独立した必要制約として扱う。

### E：Execution Chain

E は、Target State へ入った後の実行チェーンに関係する状態変数領域である。

例えば、

- ロボット経路状態
- グリッパ状態
- 正常配置先の受入状態
- 下流受入状態
- 結果書戻し状態
- 今回の実行チェーンとして定義された関連経路の状態

などが該当する。

C / A / E Mapping の後、PCN は関連状態に対して必要な S / D / B Evaluation を行う。

```text
C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
```

1 回の Target State Entry で複数の CAE-SDB Result が形成される場合は、Arbitration で制御上の優先関係を処理する。

その結果に基づいて Multipath Control を形成する。

代表的な制御経路には、例えば次のものがある。

- 進入許可
- 待機
- 再認識
- 再位置決め
- 回流
- 異常分流
- 手動確認
- 進入禁止
- 安全関連の制御経路

関連事例：

[自動化実行ユニット前判定事例](/jp/cases/automation-execution-unit-pre-control/)

---

## 5. PCN は異なるエンジニアリング階層に配置できる

PCN の実装形式は、Target State Entry が存在するシステム階層に応じて決定する。

### 自動化実行ユニット

PCN は、例えば次の Target State Entry に配置できる。

- ロボットがピックアップ段階へ入る前
- 圧入段階へ入る前
- 検査実行段階へ入る前
- 搬送引渡しへ入る前
- 正常分流または異常分流へ入る前

実装には、例えば次の構成を使用できる。

- PLC ファンクションブロック
- 産業用コントローラ
- エッジコントローラ
- ソフトウェア判定モジュール
- HMI と連携する制御モジュール

### MES / WCS・群制御協調

PCN は、例えば次の Target State Entry に配置できる。

- タスク実行へ入る前
- 資源使用へ入る前
- ステーション受入へ入る前
- エリア進入へ入る前
- 協調実行状態へ移行する前

### 生産 DX

PCN は、例えば次の Target State Entry に配置できる。

- 品質放行後の次工程進入前
- 作業指示切替後の目標生産状態への進入前
- 保全完了後の再投入前
- 手動確認後の自動運転再開前
- 下流生産状態への進入前

各適用先では、入力状態、判定ルール、Multipath Control の候補、PCN Runtime の実装方法が異なる。

一方、基本的なエンジニアリング関係は共通である。

```text
Current State
→ Target State
→ PCN
→ 複数系統の状態
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

PCN の共通性は、特定のハードウェアやソフトウェア形式ではなく、明確な Target State Entry に対して同じ階層関係で状態遷移前判定、制御、履歴を構成する点にある。

---

## 6. PCN Trace は 1 回の Target State Entry に対する状態遷移判定履歴である

PCN は、今回の Target State Entry に対する判定、Arbitration、Multipath Control、実行結果を PCN Trace として記録する。

1 つの PCN Trace には、例えば次の情報を関連付ける。

- PCN
- Current State
- Target State
- 主要な入力状態
- 時間情報 T
- 状態に関係するバージョン、シーケンス、対象情報
- C / A / E Mapping
- S / D / B Evaluation
- CAE-SDB Result
- Arbitration Result
- Multipath Control
- 実行結果
- Trace ID

PCN Trace により、個別の信号やアラームだけではなく、1 回の Target State Entry に対する状態遷移判定全体を履歴として追跡できる。

PCN Trace を継続して蓄積すると、例えば次の内容を確認できる。

- どの Target State Entry で特定の CAE-SDB Result が頻発しているか。
- C / A / E のどの状態変数領域で反復的な問題が発生しているか。
- S / D / B のどの判定性質に関係する結果が多いか。
- どの Multipath Control が高頻度で選択されているか。
- エンジニアリング変更後に CAE-SDB Result、Arbitration Result、実行結果がどのように変化したか。

このように、PCN Trace は PCN が一回の Target State Entry に対して形成する状態遷移判定履歴として、現場確認、設計レビュー、改善比較に使用できる。

---

## 7. 単一 PCN から PCN Network へ展開する

1 つの PCN は、1 つの明確な Target State Entry に対応する。

複雑なシステムでは、連続、並列、または依存関係を持つ複数の Target State Entry が存在する。

例えば、

```text
PCN-01
待機 → ピックアップ

        ↓

PCN-02
ピックアップ完了 → 搬送

        ↓

PCN-03
搬送完了 → 配置

        ↓

PCN-04
配置完了 → 後続処理
```

という関係を構成できる。

複数の PCN を、実際の状態遷移関係、および必要な許可、資源、実行チェーンの依存関係に基づいて接続すると、PCN Network を形成できる。

単一 PCN は、個別の Target State Entry に対する判定と制御を担当する。

PCN Network は、複数の Target State Entry 間に存在する状態進行、許可依存、資源依存、実行チェーン接続、履歴関係などを扱う。

したがって、PCN Network が表す対象は、

> **複数の Target State Entry 間に存在するエンジニアリング上の関係**

である。

関連説明：

[複数の PCN はどのように状態遷移前制御ネットワークを形成するのか？](/jp/notes/pcn-network-structure/)

---

## まとめ

TPCA は、状態遷移前制御アーキテクチャである。

PCN は、明確な Target State Entry の前に配置する前制御ノードである。

CAE-SDB は、PCN 内部で使用する構造化判定ロジックである。

1 つの PCN は、1 回の明確な Target State Entry に対して、次の関係を構成する。

```text
Current State
→ Target State
→ PCN
    ├─ 複数系統の状態
    ├─ C / A / E Mapping
    ├─ S / D / B Evaluation
    ├─ CAE-SDB Result + T
    ├─ Arbitration
    ├─ Multipath Control
    └─ PCN Trace
```

この単位によって、Target State Entry に関係する状態入力、構造化判定、時間情報、制御上の優先関係、制御出力、状態遷移判定履歴を同じエンジニアリング文脈で扱うことができる。

そのため、PCN は TPCA の全体アーキテクチャを具体的なシステムへ展開する際の最小エンジニアリングノードとなる。

単一 PCN を起点として、複数の Target State Entry と PCN を実際の状態遷移関係に沿って接続することで、PCN Network へ展開できる。

---

## 文書情報

題目："なぜ PCN は TPCA の最小エンジニアリングノードなのか？"  
文書種別：技術ノート  
バージョン：Public Note Version 1.2  
初回公開日：2026-07-04  
最終更新日：2026-08-20  
著者：全野南政 / Nansei Zenno  
現在の URL：https://zennns.com/jp/notes/pcn-minimum-engineering-unit/
