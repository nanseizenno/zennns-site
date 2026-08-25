---
title: "TPCA / PCN 状態遷移前制御アーキテクチャ"
summary: "明確な Target State Entry を、独立して設計・判定・制御・記録可能なエンジニアリング対象として扱い、PCN によって前判定、Arbitration、Multipath Control、状態遷移判定履歴を構成する。"
description: "TPCA 状態遷移前制御アーキテクチャと、そのエンジニアリングノードである PCN について説明する。明確な Target State Entry を中心として複数ソース状態信号を整理し、C / A / E 遷移機能役割マッピングと S / D / B 状態判定を行って CAE-SDB Result を形成する。さらに、Arbitration を経て Multipath Control を出力し、PCN Trace に状態遷移判定履歴を記録する一連の構造を示す。"
date: 2026-07-01
lastmod: 2026-08-25
author: "全野南政 / Nansei Zenno"
document_type: "公開ホワイトペーパー"
version: "Public Version 1.4"
citation_title: "TPCA / PCN 状態遷移前制御アーキテクチャ"
citation_url: "https://zennns.com/jp/whitepaper/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## 一文での定義

TPCA / PCN の中核命題は、次のとおりである。

> **明確な Target State Entry は、独立して設計・判定・制御・記録可能なエンジニアリング対象として扱う。**

**TPCA（Transition Pre-Control Architecture）** は、状態遷移前制御の全体アーキテクチャである。

**PCN（Pre-Control Node）** は、具体的な Target State Entry の前に配置する前制御ノードであり、このエンジニアリング対象を実システム上で扱うためのエンジニアリングノードである。

PCN は、明確な Target State Entry を中心として複数ソース状態信号を整理し、C / A / E 遷移機能役割マッピングと S / D / B 状態判定を行って CAE-SDB Result を形成する。その後、Arbitration を経て Multipath Control を出力し、PCN Trace に本判定および実行の履歴を記録する。

複数の PCN を、実際の状態遷移関係および必要な許可、リソース、実行依存関係に基づいて接続することで、PCN Network を形成できる。

TPCA / PCN が主に扱う問題は、次のとおりである。

- なぜ現在、Target State へ進めないのか。
- 問題が Condition、Authority、Execution Chain のどこにあるのか。
- 関連状態の構造が完全か、現在も有効か、事前定義された境界内にあるか。
- 複数の判定結果が同時に存在する場合、どのように最終的な制御結論を形成するのか。
- 次にどの制御経路へ進むべきか。
- 本判定、制御、実行結果をどのように記録し、追跡可能にするのか。

---

## エグゼクティブサマリー

製造現場では、すでに Ready、Interlock、Handshake、アラーム、状態コード、MES 記録、WCS ログなどが使用されている。

これらの仕組みは設備運転を支え、多くの状態を記録できる。

一方、複雑なシステムでは、次のエンジニアリング問題が繰り返し発生する。

> **システムが明確な Target State へ進もうとするとき、関連状態は各システムに存在していても、本 Target State Entry でなぜ進入、待機、阻止、分流となるのかが、統一されたエンジニアリング対象として整理されていない。**

具体的な問題については、[エンジニアリング問題](/jp/questions/) で整理している。

本稿では、これらの問題に共通する構造を次のように整理する。

> **明確な Target State Entry は、独立して設計・判定・制御・記録可能なエンジニアリング対象として扱う。**

![複雑なエンジニアリングシステムにおける共通状態遷移問題](/images/tpca/01-common-state-transition-problem.png)

図1：複数の現場問題は、システムが Target State へ進む前に集中して発生することが多い。

TPCA は、状態遷移前制御の全体アーキテクチャを定義する。

PCN は、明確な Target State Entry の前に配置し、複数ソース状態信号を取得して C / A / E 遷移機能役割マッピング、S / D / B 状態判定、CAE-SDB Result の形成を行う。その後、Arbitration を経て対応する Multipath Control を出力し、PCN Trace を記録する。

基本的な判定・制御チェーンは、次のとおりである。

```text
Current State
→ Target State
→ PCN
→ 複数ソース状態信号
→ C / A / E 遷移機能役割マッピング
→ S / D / B 状態判定
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

時間情報 T は、本状態および判定とともに保持し、状態の前後関係、D：Dynamics の判定、PCN Trace の形成に使用する。

TPCA では、実システム上の状態遷移は常に時間方向へ進むものとして扱う。後続で過去と同じ状態内容が再び現れた場合でも、時間位置が異なるため、新しい状態インスタンスである。

この考え方については、後述する状態遷移単方向性で補足する。

---

# 第 1 章 エンジニアリング問題

製造現場では、通常、複数の制御機構および記録機構がすでに使用されている。

PLC には、シーケンス制御、Interlock、状態ビットがある。

ロボットには、Ready、自動モード、アラーム、動作完了フィードバックがある。

画像認識システムには、OK / NG、信頼度、位置、姿勢などの状態がある。

安全システムには、安全扉、ライトカーテン、非常停止、安全回路などがある。

MES / WCS には、タスク、作業指示、配車、実行状態、ログなどがある。

HMI / SCADA には、アラーム画面、設備状態、トレンド記録などがある。

これらの仕組みは基本運転を支えるが、システムが次の状態へ進めない場合、関連結果が次のような単純な表現に集約されることがある。

```text
OK / NG
Ready / Not Ready
True / False
許可 / 不許可
アラーム / 正常
Waiting / Pending / Blocked
```

これらの結果だけでは、次の内容を直接説明できない場合がある。

- 問題が対象条件、許可状態、Execution Chain のどこにあるのか。
- 現在状態が構造欠落、動的失効、事前定義された境界外のどれに該当するのか。
- Ready が単体設備の準備完了だけを示しているのか。
- タスクが実際に Target State または目標実行経路へ進む条件を満たしているのか。
- アラームが原因側の問題なのか、後続で発生した結果なのか。
- 次に待機、再認識、回流、調整、縮退、進入禁止、人による確認のどれを選択すべきか。

[エンジニアリング問題](/jp/questions/) では、代表的な現場問題を整理している。

## 1.1 ユニット・現場実行に関する問題

- [なぜ Ready だけでは不十分なのか？](/jp/questions/why-ready-is-not-enough/)
- [なぜ Waiting は原因を追いにくいのか？](/jp/questions/why-waiting-is-hard-to-trace/)

## 1.2 複数システム連携に関する問題

- [なぜ MES / WCS は状態を記録できても、停滞の理由を説明できないのか？](/jp/questions/why-mes-records-but-cannot-explain/)
- [なぜタスクが存在していても、実行できるとは限らないのか？](/jp/questions/why-task-exists-but-cannot-execute/)

## 1.3 状態遷移設計に関する問題

- [なぜ状態遷移設計は長年、個人の経験に依存してきたのか？](/jp/questions/why-state-transition-depends-on-experience/)
- [なぜ状態が記録されていても、明確な状態遷移判定にならないのか？](/jp/questions/why-status-records-cannot-form-coordination-judgment/)

多くの状態遷移判定は、エンジニアの経験、ラダー、調整記録、HMI 画面、設備インターフェース、現場運用ルールなどに分散している。

TPCA / PCN は、明確に管理すべき Target State Entry を、独立して設計・判定・制御・記録・再利用可能なエンジニアリング対象として扱う。

---


# 第 2 章 TPCA / PCN の基本アーキテクチャ

## 2.1 TPCA の位置付け

TPCA（Transition Pre-Control Architecture）は、状態遷移前制御アーキテクチャである。

TPCA は、システムが Target State、目標実行経路、または目標物理実行段階へ進む前の前判定と Multipath Control を対象とし、明確な Target State Entry を前制御の基本的なエンジニアリング対象として扱う。

Target State には、例えば次のものがある。

- 自動化実行ユニットの次の物理実行段階
- ロボットユニットのピック、配置、回流、異常分流段階
- 圧入、検査、搬送引渡しなどの工程段階
- AGV / AMR 群制御システムにおける継続可能な協調実行状態
- MES / WCS における目標実行経路
- 生産 DX における人員、設備、システム、プロセス間の重要な状態切替
- デジタル呼出しシステムにおける目標実行経路

TPCA が確認する主な事項は、次のとおりである。

- Target State へ進むための Condition が成立しているか。
- 必要な Authority が成立しているか。
- Target State へ進んだ後、Execution Chain を継続できるか。
- 現在の判定構造が完全であるか。
- 現在状態が現在も有効であるか。
- 現在状態が事前定義された境界に対してどの位置にあるか。
- 複数の判定結果から、どのように最終的な制御経路を形成するか。
- 本状態遷移をどのように追跡可能な履歴として残すか。

複数の既存機構が一つの Target State への進入を共同で決定する場合、TPCA / PCN は、同一の Target State Entry を中心として前判定、制御、履歴を構成する。

## 2.2 PCN と CAE-SDB の階層関係

PCN（Pre-Control Node）は、前制御ノードである。

PCN は、TPCA の最小エンジニアリングノードである。

PCN は、明確な Target State Entry の前に配置し、本 Target State への進入に関係する入力、判定、Arbitration、制御、履歴を一つの単位として扱う。

CAE-SDB は、PCN 内部の構造化判定ロジックである。

C / A / E は、関連状態が本 Target State Entry において担う遷移機能役割を示す。

- C = Condition（条件状態）
- A = Authority（許可状態）
- E = Execution Chain（実行チェーン状態）

S / D / B は、これらの関連状態を判定するときに使用する判定性質を示す。

- S = Structure（構造完全性）
- D = Dynamics（動的時系列有効性）
- B = Boundary（境界判定）

基礎構造は、次のように整理できる。

```text
CAE — Transition Role Axis

C：必要な条件はそろっているか？
A：進入が許可されているか？
E：進入後も実行を継続できるか？

SDB — State Validation Axis

S：必要な構造は確立されているか？
D：現在状態は有効か？
B：現在状態は規定境界内にあるか？
```

CAE は、関連状態が 1 回の Target State Entry で担う遷移機能役割を示す。

SDB は、関連状態の構造完全性、動的時系列有効性、および事前定義された境界との位置関係をそれぞれ判定する。

詳細については、以下を参照。

[なぜ CAE-SDB なのか？― 状態遷移における機能役割と状態検証の二軸構造](/jp/notes/why-cae-sdb/)

階層関係は、次のとおりである。

```text
TPCA
→ PCN
→ CAE-SDB
→ Arbitration
→ Multipath Control
→ PCN Trace
```

TPCA は、全体アーキテクチャを定義する。

PCN は、具体的な Target State Entry に対する前制御を担う。

CAE-SDB は、構造化判定を行う。

Arbitration は、複数の判定結果と制御制約の優先関係を処理する。

Multipath Control は、最終的なエンジニアリング制御出力を形成する。

PCN Trace は、本状態遷移の判定および実行履歴を記録する。

## 2.3 基本エンジニアリングチェーン

TPCA / PCN の基本エンジニアリングチェーンは、次のとおりである。

```text
Current State / 現在段階
→ Target State / 目標段階
→ PCN
→ 複数ソース状態信号
→ C / A / E 遷移機能役割マッピング
→ S / D / B 状態判定
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
→ 振り返り、改善、再配置
```

![TPCA の基本処理チェーン](/images/tpca/02-tpca-process-chain.png)

図2：TPCA は、Current State、Target State、複数ソース状態から開始し、PCN 内で構造化判定、Arbitration、Multipath Control、PCN Trace の記録を行う。

このチェーンでは、False、NG、Not Ready、Pending などを判定の終点としない。

さらに、次の内容を判定する。

- 問題がどの変数領域に属するか。
- どの判定性質に該当するか。
- 複数の結果から、どのように最終的な制御結論を形成するか。
- 最終的にどの制御経路へ進むか。
- 本状態遷移をどのように追跡可能な履歴として残すか。

## 2.4 状態遷移単方向性

TPCA は、実システムで実際に発生する状態遷移を対象とする。

実システムでは、状態遷移は常に時間方向へ進む。

例えば、

```text
A → B → C
```

と遷移した後、C のエンジニアリング上の状態内容が A と同一であっても、システムが過去の A に戻ったことにはならない。

両者が発生した時間位置が異なるためである。

したがって、

> **状態内容は再び同一になり得るが、状態インスタンスは異なる。**

このため、現場で使用される次の用語は、制御経路またはエンジニアリング動作の名称としてそのまま使用できる。

- 回流
- 戻り
- Return
- Rollback
- Recovery
- 復帰
- 再投入

一方、TPCA の状態遷移視点では、これらはいずれも次のように扱う。

```text
Current State → New Target State
```

新しい Target State が過去の状態と同一または類似したエンジニアリング内容を持っていても、実際には新しい状態インスタンスである。

この原則は、次のように整理できる。

> **状態タイプは循環できるが、状態インスタンスは時間方向にのみ進む。**

状態遷移単方向性は、PCN、CAE-SDB、Arbitration、Multipath Control の基本構造を変更するものではない。

この原則が示すのは、

> **TPCA における実際の制御は、すべて Current State から新しい Target State への遷移として扱う。**

という点である。

詳細については、以下を参照。

[TPCA の状態遷移単方向性 ― なぜ実際のエンジニアリングシステムに状態の巻き戻しは存在しないのか？](/jp/notes/tpca-unidirectional-state-transition/)

---


# 第 3 章 PCN：状態遷移前制御の最小エンジニアリングノード

## 3.1 PCN の定義

PCN は、明確な Target State Entry の前に配置する前制御ノードである。

1 つの PCN は、1 つの明確な Target State Entry に対応する。

主な役割は、次のとおりである。

- Current State と Target State を取得する。
- 本状態遷移に関係する複数ソース状態信号を取得する。
- 必要な時間情報、対象情報、バージョン情報を取得する。
- 状態を必要に応じて標準化・整理する。
- C / A / E 遷移機能役割マッピングを行う。
- S / D / B 状態判定を行う。
- 1 つまたは複数の CAE-SDB Result を形成する。
- 複数の判定結果に対して Arbitration を行う。
- 最終的な Multipath Control を出力する。
- PCN Trace を記録する。

PCN は、TPCA の全体アーキテクチャを、設定、配置、表示、記録、振り返りが可能なエンジニアリングノードとして実システムへ展開する。

関連資料：

[なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)

## 3.2 PCN の配置位置

PCN は、Current State と Target State の間に配置する。

```text
Current State → PCN → Target State
```

![PCN 前制御ノードの位置と動作](/images/tpca/04-pcn-node-position.png)

図3：PCN は Current State と Target State の間に位置し、Target State へ進む前に、状態整理、構造化判定、Arbitration、制御経路出力を行う。

自動化実行ユニットでは、例えば次の Target State Entry の前に PCN を配置できる。

- 待機段階 → ピック段階
- 配置完了 → 圧入段階
- 検査待ち → 検査実行
- 搬送待機 → 引渡し段階
- 正常経路、回流経路、異常分流経路への切替

MES / WCS 協調システムでは、例えば次の Target State Entry の前に PCN を配置できる。

- タスクが実行経路へ入る前
- エリア進入許可前
- ステーション受入前
- 実行主体が有効実行状態へ入る前
- 群制御システムが継続可能な協調実行状態へ移行する前

生産 DX では、人員、設備、システム、プロセス間の重要な状態切替入口に PCN を配置できる。

PCN の配置位置は、設備名称やシステム種別ではなく、Target State Entry によって決定する。

## 3.3 PCN の基本分析テンプレート

1 つの PCN をエンジニアリング対象として記述する場合、少なくとも次の項目を明確にする。

| 分析項目 | 内容 |
|---|---|
| Current State / 現在段階 | システムが現在どの状態にあるか |
| Target State / 目標段階 | システムが次にどの状態へ進もうとしているか |
| PCN 配置位置 | どの Target State Entry の前に PCN を配置するか |
| トリガ条件 | どの時点で本前判定を開始するか |
| 複数ソース状態信号 | 本状態遷移の判定に使用する状態 |
| 時間 / バージョン / 対象情報 | 状態が本対象、本時系列、本バージョンに対応しているか |
| C：Condition | どの状態を進入条件の判定に使用するか |
| A：Authority | どの状態を進入許可の判定に使用するか |
| E：Execution Chain | どの状態を、進入後に Execution Chain を継続できるかの判定に使用するか |
| S：Structure | 必要な信号、インターフェース、マッピング、許可元、Execution Chain 境界が完全であるか |
| D：Dynamics | 現在状態が有効、同期済み、未タイムアウトであり、判定根拠として使用可能か |
| B：Boundary | 現在有効な状態が、事前定義された許容範囲、制限値、または境界内にあるか |
| CAE-SDB Result | 本判定で形成された構造化判定結果 |
| 時間情報 T | 本状態および判定の時間位置 |
| Arbitration | 複数の判定結果から、どのように最終制御結論を形成するか |
| Multipath Control | 最終的にどの制御経路へ進むか |
| PCN Trace | 本入力、判定、制御、実行結果の記録 |

設備、信号、インターフェースは現場ごとに異なるが、PCN の基本エンジニアリング構造は共通である。

PCN は、現場のすべてのデータを取得する必要はない。

PCN に取り込む状態は、本 Target State Entry に直接関係し、C / A / E 遷移機能役割マッピング、S / D / B 状態判定、または最終制御経路の決定に使用するものとする。

適用対象およびエンジニアリング上の境界については、以下を参照。

[TPCA / PCN 適用シナリオ分析](/jp/notes/tpca-pcn-applicable-scenarios/)

## 3.4 PCN ノードの例

ロボットが待機段階からピック段階へ進む場合を例とする。

Current State：ロボットは待機状態にあり、メインコンベヤがワークを搬送し、画像認識システムが認識を完了している。

Target State：ロボットがピック段階へ進む。

PCN 配置位置：ピック動作を開始する直前。

関連状態は、画像認識システム、ロボットコントローラ、安全システム、搬送システム、下流投入先、戻り経路、異常分流経路、上位システムなどから取得する。

C：Condition に関係する状態には、例えば次のものがある。

- ワークが存在しているか。
- 位置が適合しているか。
- 姿勢が適合しているか。
- 画像認識結果が現在も有効であるか。

A：Authority に関係する状態には、例えば次のものがある。

- 安全許可
- エリア許可
- 上位生産許可
- 本動作の許可
- 必要な人による確認

E：Execution Chain に関係する状態には、例えば次のものがある。

- ロボット経路が到達可能であるか。
- グリッパが使用可能であるか。
- 正常投入先が受入可能であるか。
- 戻り経路が使用可能であるか。
- 異常分流経路が使用可能であるか。
- 退避経路が存在するか。
- 結果を書き戻せるか。

その後、関連状態に対して S / D / B 状態判定を行い、CAE-SDB Result を形成する。さらに Arbitration を経て、最終的な Multipath Control を出力する。

## 3.5 複数の PCN による PCN Network

1 つの PCN は、1 つの明確な Target State Entry に対応する。

複雑なエンジニアリングシステムには、連続、並行、または相互依存する複数の Target State Entry が存在する。

複数の PCN を、実際の状態遷移関係および許可、リソース、実行依存関係に基づいて接続することで、PCN Network を形成できる。

例えば、自動化実行ユニットでは、次の状態遷移が存在する。

```text
待機 → ピック
ピック完了 → 搬送
搬送完了 → 投入
投入完了 → 後続処理
```

各重要な Target State Entry に、独立した PCN を設定できる。

MES / WCS 協調システムでも、タスク実行、エリア進入、ステーション受入、リソース解放、下流接続、結果書戻しなどの Target State Entry に複数の PCN を配置できる。

PCN Network は、Target State Entry と、それらのエンジニアリング上の関係を表す。

状態タイプの関係として循環構造を持つ場合があるが、実運用上の状態遷移は時間方向へ継続して生成される。

したがって、

> **PCN Network は状態タイプとして循環関係を持つことができるが、実際の状態インスタンスに真の状態巻き戻しは存在しない。**

PCN Network により、例えば次の内容を確認できる。

- どの Target State Entry で問題が頻発しているか。
- どの Authority が継続的な阻止要因となっているか。
- どの Execution Chain が繰り返し継続不能となっているか。
- どの制御経路が高頻度で選択されているか。
- どのノード間で許可、リソース、実行依存関係の問題が繰り返されているか。
- エンジニアリング変更後に状態遷移の傾向がどのように変化したか。

関連資料：

[複数の PCN はどのように状態遷移前制御ネットワークを形成するのか？](/jp/notes/pcn-network-structure/)

## 3.6 PCN の配置方式

PCN の導入にあたり、既存制御システムを一度に再構築する必要はない。

実際の導入は、プロジェクト段階に応じて段階的に進めることができる。

### 非介入診断

履歴ログ、準リアルタイム状態、エクスポートデータなどを取得し、構造化判定と履歴を形成して、分析上の有効性を確認する。

### 構造化表示

PCN の判定結果を HMI、MES / WCS 画面、イベントレポート、振り返り記録などに表示する。

### 制御提案

判定結果と Arbitration に基づき、エンジニアまたは上位システムへ推奨制御経路を提示する。

### エンジニアリング組込み

安全要求、制御仕様、検証要求を満たすことを前提として、PCN の一部の前判定および制御ロジックを PLC / HMI、WCS、エッジコントローラ、ソフトウェアプラットフォームへ組み込む。

各配置方式は、プロジェクトの異なる段階に対応できる。

---


# 第 4 章 C / A / E 遷移機能役割マッピングと S / D / B 状態判定

各定義に入る前に、CAE-SDB を二つの異なる分析軸として整理する。

```text
CAE — Transition Role Axis

C：必要な条件はそろっているか？
A：進入が許可されているか？
E：進入後も実行を継続できるか？
```

CAE は、関連状態が 1 回の Target State Entry において担う遷移機能役割を示す。

ここでいう「進入前―入口―進入後」は、C / A / E が対応するエンジニアリング上の機能位置を示すものであり、E を Target State へ進入した後に判定するという意味ではない。C、A、E は、いずれも Target State Entry の前に PCN で前判定する。

```text
SDB — State Validation Axis

S：必要な構造は確立されているか？
D：現在状態は有効か？
B：現在状態は規定境界内にあるか？
```

SDB は状態の役割を再分類するものではない。

SDB は、関連状態について、構造完全性、動的時系列有効性、および現在有効な状態と事前定義された境界との位置関係をそれぞれ判定する。

したがって、

```text
本 Target State Entry に関係する状態を識別
→ C / A / E 遷移機能役割マッピング
→ S / D / B 状態判定
→ CAE-SDB Result
→ Arbitration
→ Multipath Control
```

という関係になる。

CAE-SDB は、「状態が状態遷移でどの役割を担うか」と「その状態をどの性質から判定するか」を二つの分析次元に分ける。

詳細については、以下を参照。

[なぜ CAE-SDB なのか？― 状態遷移における機能役割と状態検証の二軸構造](/jp/notes/why-cae-sdb/)

## 4.1 C = Condition（条件状態）

C：Condition は、Target State へ進む前に、本 Target State Entry に関係する事実条件が成立しているかを扱う。

自動化実行ユニットでは、例えば次の状態が含まれる。

- ワーク存在状態
- 位置・姿勢状態
- 画像認識結果
- 認識信頼度
- 前工程動作状態
- 工程パラメータ状態

MES / WCS 協調システムでは、例えば次の状態が含まれる。

- タスク存在状態
- タスク目標情報
- 材料要求状態
- Target Station 情報
- バッファ状態
- オーダー、工程、現場条件の状態

## 4.2 A = Authority（許可状態）

A：Authority は、システムが Target State への進入を許可されているかを扱う。

例えば、次の状態が含まれる。

- 安全許可
- エリア許可
- 上位システム許可
- 人による確認
- リソースロック
- タスク割当許可
- 相手機器の受入許可
- 権限または認可状態
- スケジューリングシステムからの許可
- 品質または工程上の許可

重要な A：Authority は、独立した必要条件となり得る。

重要な Authority が成立していない場合、C：Condition と E：Execution Chain が成立していても、Target State へ進入してはならない。

## 4.3 E = Execution Chain（実行チェーン状態）

E：Execution Chain は、Target State へ進んだ後、Execution Chain 全体を継続できるかを扱う。

E：Execution Chain の対象範囲は、単体設備の Ready と同一ではない。

自動化実行ユニットでは、例えば次の状態が含まれる。

- ロボット経路が到達可能であるか。
- グリッパ、真空、治具が使用可能であるか。
- 下流投入先が受入可能であるか。
- 戻り経路が使用可能であるか。
- 異常分流経路が使用可能であるか。
- 退避経路が存在するか。
- 結果アップロードまたは書戻しを継続できるか。

AGV / AMR 群制御システムでは、例えば次の状態が含まれる。

- 実行主体がタスクを実行可能であるか。
- 経路が通行可能であるか。
- ステーションが受入可能であるか。
- 共有リソースが使用可能であるか。
- エネルギー補給状態が実行能力へ影響していないか。
- 下流が後続処理を継続できるか。
- 結果状態を書き戻せるか。

「戻り」「回流」「Rollback」などの用語は、E：Execution Chain における後続実行経路の用途を示す。

これらの経路へ実際に進む場合、TPCA では新しい Target State または目標実行経路への状態遷移として扱う。

E：Execution Chain が扱うのは、

> **Target State へ進んだ後、後続の Execution Chain を継続できるか。**

という点である。

## 4.4 S = Structure（構造完全性）

S：Structure は、Target State Entry の判定に必要な構造が定義・接続され、観測可能であるかを判定する。

代表的な対象は、次のとおりである。

- 必要な信号
- インターフェース
- マッピング関係
- 許可元
- 経路
- 役割
- Execution Chain の境界

例えば、次のような状態が S：Structure の問題となる。

- 画像認識結果は存在するが、時間情報が取り込まれていない。
- 下流状態は存在するが、Target State Entry の判定に使用されていない。
- リソースロックは存在するが、取得元や解放状態を観測できない。
- 異常分流経路は存在するが、Execution Chain として定義されていない。

## 4.5 D = Dynamics（動的時系列有効性）

D：Dynamics は、関連状態が本 Target State Entry に対して現在も有効で、同期され、判定根拠として使用可能であるかを判定する。

代表的な問題は、次のとおりである。

- タイムアウト
- 未更新
- チャタリング
- 競合
- 遅延
- 非同期
- 低信頼度
- Authority の取消
- 状態切替
- 対象またはバージョン不一致

例えば、次のような状態がある。

- 画像認識結果は一度成立していたが、現在は有効時間を超えている。
- 下流 Ready が長時間更新されていない。
- 上位 Authority が複数周期にわたり成立と取消を繰り返している。
- WCS ではタスク配車済みであるが、実行主体は実行状態へ移行していない。

D：Dynamics では、Timestamp、更新時刻、シーケンス、バージョン、対象関連情報などを使用し、C：Condition、A：Authority、E：Execution Chain に関係する状態が、本 Target State Entry の有効な判定根拠として現在も使用可能かを判断できる。

## 4.6 B = Boundary（境界判定）

B：Boundary は、C / A / E に関係する状態の現在有効な値が、事前に定義された許容範囲、制限値、または境界に対してどの位置にあるかを判定する。

境界判定の対象には、例えば次のものがある。

- 寸法、公差、偏差範囲
- 温度、圧力、流量などの工程範囲
- 認識信頼度範囲
- 位置、姿勢、距離、速度範囲
- バッファ容量、負荷率、リソース占有範囲
- 許可レベル、許可エリア、許可状態集合
- その他、Target State Entry に関係する事前定義されたしきい値または境界

例えば、

```text
許容寸法：19.90 mm ～ 20.10 mm
現在有効値：20.06 mm
→ 規定境界内

現在有効値：20.18 mm
→ 規定境界外
```

となる。

B：Boundary の具体的なしきい値または境界は、Target State、設備特性、工程条件、安全要求、エンジニアリング設計に基づいて設定する。

## 4.7 時間情報 T

PCN が使用する状態は、固定された静的情報ではない。

Target State へ進むまでの間、複数ソース状態は継続して更新される。

例えば、次のように変化する。

| 時点 | C：Condition | A：Authority | E：Execution Chain | 説明 |
|---|---|---|---|---|
| T0 | C(T0) | A(T0) | E(T0) | 現在サンプリング |
| T1 | C(T1) | A(T1) | E(T1) | 状態更新 |
| T2 | C(T2) | A(T2) | E(T2) | 安定、取消、競合、失効などへ変化する可能性がある |
| Tn | C(Tn) | A(Tn) | E(Tn) | Target State へ進む直前の現在の判定根拠 |

現場では、例えば次のような変化が発生する。

- 画像認識結果は T0 では有効であったが、その後失効する。
- 安全 Authority は T0 では成立していたが、T1 で取り消される。
- 下流 Ready は T0 では成立していたが、その後長時間更新されない。
- タスクは存在しているが、リソースロックが解放されていない。
- 実行主体は自動モードであるが、有効実行能力が継続して低下している。

このため、各 CAE-SDB 判定には、対応する時間情報 T を保持する。

時間情報 T は、次の用途に使用する。

- 本状態および判定の時間位置を示す。
- 状態間の前後関係を判定する。
- D：Dynamics の動的時系列有効性判定を支援する。
- PCN Trace を形成する。

システムに応じて、時間情報 T には次の情報を使用できる。

- Timestamp
- 更新時刻
- イベント時刻
- シーケンス時刻
- バッチ時刻
- その他、状態の前後関係を特定できる時間情報

## 4.8 CAE-SDB の組合せ関係

C / A / E は、関連状態が本状態遷移で担う機能役割を示す。

S / D / B は、これらの関連状態を判定するときに使用する判定性質を示す。

両者を組み合わせて、CAE-SDB 判定構造を形成する。

| 判定性質 / 遷移機能役割 | C：Condition | A：Authority | E：Execution Chain |
|---|---|---|---|
| S：Structure | Condition に必要な信号、インターフェース、マッピングが完全であるか | Authority の取得元、インターフェース、関係が完全であるか | 下流、退避、異常経路、書戻し経路が完全であるか |
| D：Dynamics | Condition がタイムアウト、チャタリング、競合、未更新となっていないか | Authority が遅延、取消、競合、非同期となっていないか | Execution Chain が閉塞、フィードバックタイムアウト、未更新、切替中となっていないか |
| B：Boundary | Condition の現在有効値が事前定義された境界内にあるか | Authority の現在状態が事前定義された境界内にあるか | Execution Chain の現在状態が事前定義された境界内にあるか |

![CAE-SDB 二軸判定構造](/images/tpca/03-cae-sdb-matrix.png)

図4：C / A / E は遷移機能役割、S / D / B は状態判定性質を示し、二つの分析軸を組み合わせて CAE-SDB Result を形成する。

同一の状態遷移に対して、複数の CAE-SDB Result が同時に形成される場合がある。

これらの結果に対して Arbitration を行った後、最終的な Multipath Control を形成する。

---


# 第 5 章 CAE-SDB Result、Arbitration、Multipath Control

## 5.1 判定結果から制御経路まで

PCN 内部の制御チェーンは、次のとおりである。

```text
CAE-SDB Result + T → Arbitration → Multipath Control → 実行結果 → PCN Trace
```

CAE-SDB Result は、

> **関連状態が本状態遷移でどの機能役割を担い、それぞれの Structure、Dynamics、Boundary の判定結果がどうなっているか。**

を示す。

Arbitration は、

> **複数の判定結果、重要な Authority、制御制約が同時に存在する場合に、どの制御結論を採用するか。**

を処理する。

Multipath Control は、Arbitration の結果を実際のエンジニアリング制御経路へ変換する。

代表的な制御経路には、次のものがある。

- 進入許可
- 待機
- 再認識
- 再サンプリング
- 再位置決め
- 回流
- Return
- 退避経路
- 異常分流
- 下流調整
- リソース解放
- タスク再割当
- 縮退実行
- 代替経路
- 進入禁止
- 安全ロック
- 人による確認
- 異常隔離
- 強化記録

Multipath Control は、現在の判定結果に基づいて、システムが次に進む Target State または Target Path を決定する。

## 5.2 CAE-SDB Result

代表的な CAE-SDB Result を以下に示す。

| 判定結果 | 内容 |
|---|---|
| C-S | Condition に Structure の問題がある |
| C-D | Condition に Dynamics の問題がある |
| C-B | Condition の現在状態と事前定義された Boundary との位置関係 |
| A-S | Authority に Structure の問題がある |
| A-D | Authority に Dynamics の問題がある |
| A-B | Authority の現在状態と事前定義された Boundary との位置関係 |
| E-S | Execution Chain に Structure の問題がある |
| E-D | Execution Chain に Dynamics の問題がある |
| E-B | Execution Chain の現在状態と事前定義された Boundary との位置関係 |

同一の Target State Entry に対する判定で、複数の CAE-SDB Result が同時に存在する場合がある。

## 5.3 Arbitration の基本原則

重要な A：Authority は、独立した必要条件となり得る。

重要な Authority が成立していない場合、Target State への進入を許可しない。

重要な Structure が欠落している場合、または Dynamics が失効している場合、関連状態を現在の進入許可の根拠として使用してはならない。

複数の CAE-SDB Result が同時に存在する場合、Arbitration を経て最終的な Multipath Control を形成する。

必要な Condition、重要な Authority、Execution Chain が成立し、かつそれらより高い優先度を持つ制限制約が存在しない場合に、Target State への進入を許可する。

それ以外の場合は、完全な判定結果に基づいて、対応する Target State または Target Path へ進む。

## 5.4 PCN Trace

PCN は、判定および制御を行うと同時に、PCN Trace を形成できる。

公開レベルでは、PCN Trace を次の項目で構成される状態遷移判定履歴として整理する。

| 記録項目 | 内容 |
|---|---|
| Current State / 現在段階 | システムが当時どの状態にあったか |
| Target State / 目標段階 | システムがどの状態へ進もうとしていたか |
| 主要入力状態 | 本状態遷移に直接関係する状態 |
| 時間情報 T | 本状態および判定の時間位置 |
| バージョン / 対象情報 | 状態バージョンおよび対象との関連 |
| C / A / E 遷移機能役割マッピング | 関連状態が本状態遷移で担う機能役割 |
| S / D / B 状態判定 | 判定性質 |
| CAE-SDB Result | 構造化判定結果 |
| Arbitration Result | 最終制御結論の形成結果 |
| Multipath Control | 最終制御経路 |
| 実行結果 | 制御後に実際に発生した結果 |
| Trace ID | 同一の状態遷移判定履歴を関連付ける識別子 |

PCN Trace の価値は、ログ項目を増やすことではない。

1 回の状態遷移判定を、一つのエンジニアリングデータ対象として記録することにある。

PCN Trace により、例えば次の違いを区別できる。

- 状態内容は同じでも、発生時間が異なる状態インスタンス
- 同じ Ready 状態でも、異なる状態遷移履歴を持つ状態インスタンス
- 同一の状態タイプに対して、異なる経路から形成された状態インスタンス

関連資料：

[なぜ PCN Trace は新しいエンジニアリングデータなのか？](/jp/notes/why-pcn-trace-is-engineering-data/)

## 5.5 振り返りと改善

PCN Trace を用いることで、例えば次の内容を確認できる。

- どの Target State Entry で問題が頻発しているか。
- どの Condition が継続的に失効しているか。
- どの Authority が高頻度で進入を阻止しているか。
- どの Execution Chain が繰り返し継続不能となっているか。
- どの Dynamics の問題が継続して発生しているか。
- どの状態が事前定義された Boundary に高頻度で近づき、到達し、または超過しているか。
- どの制御経路が高頻度で選択されているか。
- 同一の状態タイプが繰り返し現れていても、実際の状態インスタンスがどのような異なる遷移履歴を持っているか。
- エンジニアリング変更後に、状態遷移の傾向がどのように変化したか。

したがって、TPCA / PCN は現在の状態遷移制御だけでなく、後続の設計改善、設備再利用、エンジニア教育、プロジェクト引継ぎ、生産 DX のための構造化履歴としても使用できる。

AI は、PCN Trace に基づく履歴比較、パターン分析、改善候補の整理、レポート生成を補助できる。

---


# 第 6 章 代表的な適用方向

![TPCA / PCN の適用方向](/images/tpca/05-tpca-application-map.png)

図5：TPCA / PCN は、自動化実行ユニット、群制御協調、生産 DX、デジタル呼出しガバナンスなど、異なるエンジニアリング対象へ展開できる。

## 6.1 自動化実行ユニット

代表的な対象には、次のものがある。

- ロボットピック
- 圧入
- 検査
- 搬送引渡し
- 画像認識コンベヤ
- 搬入・搬出ユニット
- PLC / HMI 自動化ユニット

代表的な問題には、次のものがある。

- Robot Ready であるが、ピックできない。
- 画像認識結果は一度 OK であったが、現在は失効している。
- 必要な安全 Authority が成立していない。
- 圧入ヘッドは Ready であるが、搬送機構が退避していない。
- 検査設備は Ready であるが、結果書戻し経路が利用できない。
- 下流は Ready を表示しているが、実際には受入不能である。
- 回流経路または異常経路は存在するが、Target State Entry の判定に含まれていない。

PCN は、目標物理実行段階へ進む前に配置し、複数ソース状態に対して C / A / E 遷移機能役割マッピングと S / D / B 状態判定を行って CAE-SDB Result を形成する。その後、Arbitration を経て Multipath Control を出力する。

安全停止、退避、回流、再認識、再投入などの経路へ進む場合も、それぞれ新しい Target State Entry を中心として整理できる。

関連事例：

[自動化実行ユニット前判定事例](/jp/cases/automation-execution-unit-pre-control/)

## 6.2 MES / WCS 協調停滞

AGV / AMR、複数設備、WCS、MES、バッファ、ステーション、共有リソース、下流工程が相互に関係するシステムでは、単体設備が正常であっても、システム全体として継続的に実行できるとは限らない。

代表的な問題には、次のものがある。

- タスクは存在するが、実行主体が有効実行状態へ移行しない。
- 複数の実行主体が長時間 Waiting、Blocked、Idle、Pending にある。
- 複数の実行主体が共有リソース待ちに集中する。
- リソースロックが解放されていない。
- エリア Authority が成立していない。
- 下流ステーションが受入不能である。
- エネルギー補給が集中し、実行可能主体の比率が低下する。
- MES / WCS に記録はあるが、現場では依然として複数システムのログ確認が必要である。

群制御協調層の PCN は、複数ソース状態を取得し、C / A / E 遷移機能役割マッピング、S / D / B 状態判定を行う。さらに、群全体の指標を用いて停滞識別と構造分析を行う。

代表的な診断結果または制御出力には、次のものがある。

- 割当制約
- リソース競合
- エネルギー偏在
- 未確定状態
- 待機
- タスク再割当
- リソース解放
- 経路または通行権の調整
- 流量制限
- 下流調整
- 人による確認
- 強化記録

関連事例：

[MES / WCS 協調停滞診断モジュール事例](/jp/cases/collaborative-stagnation-diagnosis/)

## 6.3 生産 DX

生産 DX は、データ収集、可視化、レポート、ダッシュボードの構築から開始する場合が多い。

TPCA / PCN は、その上でさらに、

> **取得したデータを、明確な Target State Entry のエンジニアリング判定にどのように使用するか。**

を対象とする。

例えば、次のような状態遷移がある。

- 人による確認完了後に自動運転へ移行してよいか。
- 作業指示切替後に目標生産状態へ進んでよいか。
- 保全解除後に再投入してよいか。
- 品質承認後に次の処理経路へ進んでよいか。
- 複数システムの状態が、継続可能な Execution Chain を形成しているか。

「復帰」「再投入」などのエンジニアリング上の用語は、そのまま維持する。

TPCA の状態遷移視点では、これらは Current State から新しい Target State への状態遷移を表す。

PCN は、従来、設備、システム、人員、プロセスに分散していた状態遷移条件を明示化し、判定、制御、履歴として整理できる。

関連事例：

[生産 DX 状態遷移条件設計・履歴分析事例](/jp/cases/production-dx-state-transition/)

## 6.4 デジタル呼出しガバナンスへの拡張

TPCA / PCN は、デジタル呼出しガバナンスにも拡張できる。

例えば、次のような対象がある。

- AI 推論呼出し
- ツール呼出し
- 企業知識ベースへのアクセス
- API 呼出し
- 外部サービス呼出し
- AI エージェントの呼出しチェーン
- 高コストモデルの呼出し

リクエストが生成された後も、さらに次の内容を判定する必要がある。

- リクエスト条件が成立しているか。
- 権限、予算、テナント認可、ツール呼出し Authority などが成立しているか。
- モデル、ツールチェーン、インターフェースサービス、キューリソースが実行可能であるか。
- 最終的に高コスト経路、追加確認経路、縮退経路、待機経路、阻止経路のどれへ進むか。

この領域は、TPCA / PCN の拡張適用である。

製造システムにおける主要な適用対象は、自動化実行ユニット前制御、MES / WCS 協調停滞、生産 DX における複数システム横断の状態遷移である。

関連資料：

[TPCA / PCN 適用シナリオ分析](/jp/notes/tpca-pcn-applicable-scenarios/)

---


# 結語

複雑な製造システムにおける問題は、設備、信号、ログの数が増えることだけによって発生するものではない。

システムが複雑になるほど、管理すべき Target State Entry も増加する。

TPCA は、状態遷移前制御の全体アーキテクチャを定義する。

PCN は、明確な Target State Entry の前に配置し、本状態遷移に関係する複数ソース状態を C / A / E の遷移機能役割に基づいて整理し、S / D / B 状態判定を行って CAE-SDB Result を形成する。その後、Arbitration を経て最終的な Multipath Control を出力し、PCN Trace に本状態遷移の履歴を記録する。

現在の体系における中核関係は、次のように整理できる。

```text
TPCA = 状態遷移前制御アーキテクチャ

PCN = 前制御ノード

CAE-SDB = PCN 内部の構造化判定ロジック

T = 状態および CAE-SDB Result とともに保持する時間情報

Arbitration = 複数の判定結果と制御制約から制御結論を形成する処理

Multipath Control = 次の Target State / 目標実行経路に対するエンジニアリング制御出力

PCN Trace = 状態遷移判定履歴
```

> **明確な Target State Entry は、独立して設計・判定・制御・記録可能なエンジニアリング対象として扱う。**

このエンジニアリング対象を中心として、TPCA / PCN は従来分散していた状態を、判定・制御・追跡可能な前制御構造として整理する。

TPCA は、状態および判定に対応する時間情報も保持する。

このため、後続で過去と同一の状態内容が再び現れた場合でも、新しい状態インスタンスとして扱う。

通常実行、回流、戻り、復帰、縮退、異常処理、再投入などのプロセスも、次のように表すことができる。

```text
Current State → New Target State
```

1 つの PCN は、独立して設計、配置、振り返りができる。

複数の PCN を、実際の状態遷移関係および許可、リソース、実行依存関係に基づいて接続することで、PCN Network を形成できる。

---

# 関連技術ノート

技術ノートは、本ホワイトペーパーの個別テーマを補足するものであり、TPCA / PCN の全体定義を置き換えるものではない。

## 1. TPCA の基本原則と技術的位置付け

TPCA がどのようなエンジニアリング上の認識を基盤とし、実際の状態遷移をどのように捉え、既存の産業オートメーション手法とどのような境界を持つかを整理する。

- [TPCA の状態遷移単方向性 ― なぜ実際のエンジニアリングシステムに状態の巻き戻しは存在しないのか？](/jp/notes/tpca-unidirectional-state-transition/)  
  状態と時間の関係から、状態内容は再び同一になり得る一方、実際の状態遷移は常に時間方向へ進むことを説明する。

- [TPCA / PCN はどのようなエンジニアリング基盤の上に成り立つか ― 5 つの基本的な工学的共通認識](/jp/notes/engineering-foundations-of-tpca-pcn/)  
  状態遷移、許可制約、Execution Chain、動的時系列有効性、Boundary という観点から、TPCA / PCN のエンジニアリング基盤を整理する。

- [TPCA / PCN と既存の産業オートメーション方法・制御メカニズムとの関係](/jp/notes/tpca-existing-theories/)  
  FMEA、STPA、RCA、Process Mining、ステートマシン、SFC、Interlock、安全制御、アラーム管理、MES / WCS、AI 分析、形式検証との境界を比較する。

- [TPCA / PCN は既存技術との論点に対してどの位置を取るか ― 3 つの代表的なエンジニアリング論点](/jp/notes/engineering-positions-of-tpca-pcn/)  
  決定論的制御と AI、集中制御と分散自律、保守的な阻止と制御された継続などに対する TPCA / PCN の基本的な技術的位置付けを示す。

## 2. CAE-SDB と PCN のエンジニアリング構造・システム拡張

CAE-SDB の二軸構造、Target State Entry を独立して設計する必要性、PCN が判定・制御・記録可能なエンジニアリング構造を形成する方法を整理する。

- [なぜ CAE-SDB なのか？― 状態遷移における機能役割と状態検証の二軸構造](/jp/notes/why-cae-sdb/)  
  Target State Entry を起点として、CAE の Transition Role Axis と SDB の State Validation Axis、および両者が CAE-SDB Result を形成する関係を説明する。

- [なぜ状態遷移条件を明示化する必要があるのか？](/jp/notes/explicit-state-transition-conditions/)  
  プログラム、インターフェース、許可、設備連携、エンジニアの経験に内在している状態遷移判定を明示化する必要性を説明する。

- [なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)  
  1 つの PCN が明確な Target State Entry を中心として、状態遷移前制御の一連の構造を形成することを説明する。

- [複数の PCN はどのように状態遷移前制御ネットワークを形成するのか？](/jp/notes/pcn-network-structure/)  
  複数の PCN が、実際の状態遷移関係および許可、リソース、実行依存関係に基づいて PCN Network を形成することを説明する。

- [なぜ PCN Trace は新しいエンジニアリングデータなのか？](/jp/notes/why-pcn-trace-is-engineering-data/)  
  1 回の状態遷移判定を、独立して記録・比較・振り返り可能なエンジニアリングデータ対象として扱える理由を説明する。

## 3. エンジニアリング上の価値と適用範囲

- [TPCA / PCN 適用シナリオ分析](/jp/notes/tpca-pcn-applicable-scenarios/)  
  どのような Target State Entry に PCN を配置することが適切か、TPCA / PCN のエンジニアリング上の適用範囲を整理する。

- [なぜ OEE の後にも PCN が必要なのか？](/jp/notes/why-oee-pcn/)  
  OEE、設備データ、PCN の、運転パフォーマンス観測と状態遷移判定における補完関係を説明する。

## 4. 理解確認

TPCA / PCN のエンジニアリングロジックを正しく理解しているかを確認するための内容であり、新しい概念は追加しない。

- [TPCA / PCN を本当に理解しているか ― 10 のエンジニアリング問題](/jp/notes/tpca-pcn-understanding-test/)  
  具体的なエンジニアリング問題を通じて、Target State Entry、PCN、C / A / E、S / D / B、Arbitration、Multipath Control、PCN Trace の関係を確認する。

---

# 次に読む

現場問題から確認する場合：

[エンジニアリング問題](/jp/questions/)

用語定義を確認する場合：

[中核概念](/jp/concepts/)

適用事例を確認する場合：

[適用事例](/jp/cases/)

TPCA の基本原則、PCN のエンジニアリング構造、適用範囲、理解確認を続けて読む場合：

[技術ノート](/jp/notes/)

著者および本サイトの位置付けを確認する場合：

[本サイトについて](/jp/about/)

---

# バージョン情報

本稿は、**TPCA / PCN 状態遷移前制御アーキテクチャ**の公開ホワイトペーパーである。

Public Version 1.0：2026-07-01 公開。

Public Version 1.1：2026-08-19 更新。CAE-SDB Result、Arbitration、Multipath Control、PCN Trace の階層関係を明確化。

Public Version 1.2：2026-08-20 更新。明確な Target State Entry を、独立して設計・判定・制御・記録可能なエンジニアリング対象として統一し、TPCA と PCN の全体アーキテクチャおよびエンジニアリングノードの関係を明確化。

Public Version 1.3：2026-08-21 更新。Execution Chain、回流、戻り、復帰などの現場エンジニアリング表現を維持したうえで、状態遷移単方向性と時間情報 T を追加し、PCN Trace、PCN Network、Multipath Control に関する説明を更新。

Public Version 1.4：2026-08-25 更新。CAE-SDB の二軸基礎構造を明確化。CAE を Transition Role Axis、SDB を State Validation Axis として整理し、CAE-SDB に関する技術ノートへのリンクを追加。

著者：全野南政 / Nansei Zenno

推奨引用形式：

```text
全野南政 / Nansei Zenno，《TPCA / PCN 状態遷移前制御アーキテクチャ》，公開ホワイトペーパー，Public Version 1.4，2026-08-25，https://zennns.com/zh/whitepaper/
```
