---
title: "なぜ PCN Trace は新しいエンジニアリングデータなのか？"
summary: "PCN Trace と従来の設備データ、生産データ、アラーム履歴との違いを説明する。PCN Trace は、明確な Target State Entry を中心として、関連する入力状態、CAE-SDB Result、Arbitration、Multipath Control、実行結果、時間情報 T を一つの状態遷移判定履歴として関連付ける。"
description: "明確な Target State Entry を起点として、PCN が Current State、Target State、複数ソース状態、C / A / E 状態マッピング、S / D / B 判定、CAE-SDB Result、Arbitration、Multipath Control、実行結果、時間情報 T を PCN Trace として関連付ける方法を説明する。また、PLC / HMI 診断、MES / WCS 協調分析、状態遷移改善、生産 DX における活用方法を示す。"
date: 2026-07-14
lastmod: 2026-08-26
author: "全野南政 / Nansei Zenno"
document_type: "技術ノート"
version: "Public Note Version 1.4"
citation_url: "https://zennns.com/jp/notes/why-pcn-trace-is-engineering-data/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## なぜ PCN Trace は新しいエンジニアリングデータなのか？

基本概念については、以下を参照。

* [Concepts｜中核概念](/jp/concepts/)
* [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)
* [なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)
* [なぜ状態遷移条件を明示する必要があるのか？](/jp/notes/explicit-state-transition-conditions/)
* [なぜ OEE の後に PCN が必要なのか？](/jp/notes/why-oee-pcn/)
* [TPCA の状態遷移単方向性 ― なぜ実システムでは過去の状態インスタンスへ戻らないのか？](/jp/notes/tpca-unidirectional-state-transition/)

製造現場では、すでに大量のデータが蓄積されている。

PLC は状態やアラームを記録し、MES は生産履歴を保持する。WCS はタスクやスケジューリングの記録を持ち、設備プラットフォームでは温度、電流、位置、サイクルタイム、運転時間などを収集している。

これらのデータは、主として設備、タスク、作業指示、アラーム、イベントなどを単位として整理される。

PCN Trace は、これらに加えて、

> **一回の明確な Target State Entry に対する状態遷移判定**

を記録対象とする。

対象となるのは、例えば次のような判定である。

> **今回の Target State Entry に対して、どの状態を判定に使用し、どの CAE-SDB Result が形成され、Arbitration の結果としてどの Multipath Control が選択され、最終的にどの状態が実際に形成されたか。**

PCN Trace では、PLC、MES、WCS、ロボット、画像認識システムなどから得られる既存の状態情報を、今回の Target State Entry に対応する一つの判定履歴として関連付ける。

一回の状態遷移前判定について、PCN は Current State、Target State、関連する入力状態、C / A / E 状態マッピング、S / D / B 判定、CAE-SDB Result、Arbitration、Multipath Control、実行結果、時間情報 T を関連付ける。

この一連の状態遷移判定履歴を **PCN Trace** と呼ぶ。

PCN Trace により、

```text
判定に使用した状態
→ 構造化判定結果
→ Arbitration
→ Multipath Control
→ 実行結果
```

を同じ Target State Entry に対応する履歴として追跡できる。

---

## 1. PCN Trace と従来のエンジニアリングデータ

製造現場で一般的に扱われるデータには、次のようなものがある。

### 設備状態データ

* 運転
* 停止
* Ready
* 位置
* 回転速度
* 温度
* 電流
* 圧力
* エネルギー使用量

### 生産データ

* 生産数量
* 良品率
* サイクルタイム
* OEE
* 不良数量
* 停止時間
* ロスタイム

### イベント・アラーム履歴

* アラーム発生
* アラームリセット
* 設備起動
* 設備停止
* 工程開始
* 工程終了
* タスク完了
* タスク失敗

### MES / WCS 運転記録

* タスク生成
* タスク割当
* Waiting
* Blocked
* Pending
* 資源占有
* 経路状態
* ステーション状態

これらのデータから、各設備、タスク、工程がある時点でどのような状態であったかを確認できる。

例えば、現場に次の記録が残っている場合を考える。

```text
Robot Ready = TRUE
安全回路 = TRUE
画像認識結果 = OK
下流 Ready = FALSE
ロボット未動作
```

この記録から、各システムの状態を確認できる。

さらに、「なぜその時点でピックアップ段階へ入らなかったのか」を確認する場合には、今回の Target State Entry に対応する判定関係が必要になる。

確認対象には、例えば次の内容が含まれる。

* 当時の Target State
* C にマッピングされた入力状態
* A にマッピングされた入力状態
* E にマッピングされた入力状態
* 各状態に対する S / D / B 判定
* 同時に形成された CAE-SDB Result
* Arbitration の結果
* 選択された Multipath Control
* 実行後に確認された状態

PCN Trace は、これらを判定時点で同じ Target State Entry に関連付ける。

データの整理単位は、次のように区別できる。

```text
従来の設備・生産データ：
設備、イベント、タスク、作業指示などを単位として記録

PCN Trace：
一回の Target State Entry に対する状態遷移判定を単位として記録
```

---

## 2. PCN Trace に記録する情報

PCN は、明確な Target State Entry に対応する。

```text
Current State
→ Target State Entry / PCN
→ Target State
```

Target State へ入る前に、PCN は今回の状態遷移に関係する複数ソース状態を整理し、必要な判定を行う。

```text
Current State
→ Target State
→ Target State Entry / PCN
→ 複数ソース状態
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ 実行結果
→ PCN Trace
```

各要素の位置付けは次の通りである。

* C / A / E は、今回の Target State Entry に関係する状態の機能役割を表す状態変数領域である。
* S / D / B は、それらの状態に対して適用する判定性質である。
* CAE-SDB Result は、C / A / E と S / D / B の判定によって形成される構造化判定結果である。
* 時間情報 T は、状態および判定とともに保持し、状態の前後関係、D 判定、PCN Trace に使用する。
* Arbitration は、CAE-SDB Result、重要な許可、制御制約、優先関係などを処理する。
* Multipath Control は、Arbitration の結果に基づくエンジニアリング制御出力である。
* 実行結果は、Multipath Control の実行後に確認された状態を記録する。

一つの PCN Trace には、例えば次の情報を関連付けることができる。

| 項目                   | 記録内容                      |
| -------------------- | ------------------------- |
| PCN                  | 対象となった Target State Entry |
| Current State        | 判定時点の現在状態                 |
| Target State         | 今回進入しようとしている目標状態          |
| 主要な入力状態              | 今回の判定に使用した状態              |
| 時間情報 T               | 状態、判定、制御、実行の時間位置          |
| C / A / E Mapping    | 各入力状態の今回の状態遷移における役割       |
| S / D / B Evaluation | 各状態に対する判定結果               |
| CAE-SDB Result       | 今回形成された構造化判定結果            |
| Arbitration Result   | 制御上の優先関係を処理した結果           |
| Multipath Control    | 今回選択された制御出力               |
| 実行結果                 | 制御実行後に確認された状態             |
| Trace ID             | 上記情報を一回の状態遷移判定として関連付ける識別子 |

例えば、次のような PCN Trace を形成できる。

```text
PCN：ピックアップ入口

Current State：ピックアップ待ち

Target State：ピックアップ段階

時間情報：T₂

CAE-SDB Result：C-D

判定内容：画像認識結果が有効時間を超過

Arbitration Result：回流経路を選択

Multipath Control：回流

実行結果：ワークが戻り経路へ進入

Trace ID：PCN-XXXX-XXXX
```

この Trace では、次の関係が一回の Target State Entry に対応する履歴として保持される。

```text
判定に使用した状態
→ CAE-SDB Result
→ Arbitration Result
→ Multipath Control
→ 実行結果
```

本文では、PCN Trace の基本的な構成と役割を公開範囲とする。

内部リクエスト識別子、PCN Runtime のライフサイクル、詳細なフィールド構成、バージョン関係、保存方式、索引方式、再生機構などは、PCN Runtime および Trace Schema の実装範囲に含まれる。

---

## 3. 同じ状態内容が再び現れた場合の Trace

同じ状態内容は、システムの運転中に複数回現れることがある。

例えば、次の状態を考える。

```text
Robot Position = Home
Mode = Auto
Ready = TRUE
```

この状態は、タスク開始前だけでなく、運転完了後、異常処理後、手直し後、回流後、再投入後などにも現れる場合がある。

状態内容が同じであっても、それぞれは異なる時間位置と状態遷移履歴を持つ。

```text
状態内容が同一
↓
異なる状態インスタンスとして記録
```

PCN Trace は、実際に発生したそれぞれの状態遷移判定を個別に記録する。

例えば、

```text
T₁：
Home / Auto / Ready
→ PCN-A
→ 実行段階へ進入

T₃：
Home / Auto / Ready
→ PCN-A
→ 再度、実行段階へ進入
```

T₁ と T₃ では状態内容が同じであっても、異なる状態インスタンスとして扱う。

手直し、回流、復旧、補償、再投入などの経路についても、後続の状態遷移によって新しい状態インスタンスが形成される。

PCN Trace は、このように時間方向へ継続して形成される状態インスタンスと、それぞれの Target State Entry に対する判定履歴を関連付ける。

---

## 4. PCN Trace を用いたエンジニアリング改善

製造現場で状態遷移の原因を確認する場合、複数システムの記録を時系列に沿って照合することがある。

代表的な確認手順は次のようになる。

```text
現象を確認
→ アラームを確認
→ PLC 状態を確認
→ ロボット / 画像認識 / MES / WCS の状態を確認
→ 時刻を照合
→ 当時の状態関係を整理
→ Target State Entry が進まなかった要因を確認
→ 改善対象を特定
```

PCN Trace では、Target State Entry に対する主要な判定情報が生成時点で関連付けられている。

Trace を継続して蓄積すると、例えば次の観点から状態遷移上の問題を集計できる。

| PCN Trace で繰り返し確認される状態             | 確認対象となるエンジニアリング項目                        |
| ---------------------------------- | ---------------------------------------- |
| C-S が集中                            | 条件状態に必要な信号、インターフェース、マッピング、対象定義           |
| C-D が継続                            | データ更新、同期、時間有効性、認識信頼度                     |
| C-B が高頻度                           | 条件値、信頼度、位置偏差、時間などの制御境界                   |
| A-S が集中                            | 許可元、権限インターフェース、資源許可の構造                   |
| A-D が継続                            | 許可更新、同期、取消、状態切替                          |
| A-B が高頻度                           | 許可範囲、時間ウィンドウ、関連する制御境界                    |
| E-S が集中                            | 下流、代替経路、回流経路、異常経路、結果書戻しなどの実行チェーン構造       |
| E-D が継続                            | 実行チェーン、下流受入、資源状態、システム間時系列                |
| E-B が高頻度                           | 容量、待機時間、資源利用範囲などの実行チェーンに関係する制御境界         |
| 特定の Multipath Control が高頻度         | 対応する Target State Entry の制御ルール、優先関係、候補経路 |
| 特定の Multipath Control と実行結果の組合せが継続 | 制御経路と実際の実行結果との関係                         |

これにより、改善対象を次の単位で整理できる。

```text
Target State Entry
→ 状態変数領域
→ 判定性質
→ CAE-SDB Result
→ Arbitration Result
→ Multipath Control
→ 実行結果
```

改善後は、同じ種類の PCN Trace を継続して比較できる。

例えば、ある PCN で次の CAE-SDB Result が継続して発生している場合を考える。

```text
C-D：画像認識結果の有効性または同期に関する問題
```

画像認識結果の更新方法、同期方法、有効性判定ルールなどを変更した後、次の項目を比較できる。

* C-D の発生頻度
* CAE-SDB Result の分布
* Arbitration Result
* 再認識、回流などの Multipath Control の発生頻度
* B 判定の発生状況
* 実行結果

この改善サイクルは、次のように表せる。

```text
PCN 運用
    ↓
PCN Trace
    ↓
集計・比較
    ↓
状態遷移上の改善対象を抽出
    ↓
エンジニアリング改善
    ↓
ルール / 設定 / システム設計を更新
    ↓
再運用
    ↓
新しい PCN Trace
    ↓
改善前後を比較
```

PCN Trace は、状態遷移設計と制御ルールを継続して確認するためのデータとして利用できる。

---

## 5. PLC / HMI、MES / WCS、生産 DX における PCN Trace

### PLC / HMI

PLC / HMI では、一般に次のような状態を表示・記録する。

* 信号状態
* Ready
* Interlock
* Alarm
* シーケンス状態
* 設備状態

PCN Trace を組み合わせることで、さらに次の情報を一つの Target State Entry に対応付けて表示できる。

* Current State
* Target State
* Target State Entry
* 時間情報 T
* CAE-SDB Result
* Arbitration Result
* Multipath Control
* 実行結果
* Trace ID

例えば HMI 上の表示を、

```text
CONDITION NOT READY
```

から、Target State Entry に対応する情報へ展開できる。

```text
Target State：ピックアップ段階

CAE-SDB Result：C-D

判定内容：画像認識結果が有効時間を超過

Arbitration Result：回流経路を選択

Multipath Control：回流
```

これにより、対象となった Target State、判定結果、制御経路を同じ画面または履歴情報から確認できる。

### MES / WCS

MES / WCS では、タスク、車両、ステーション、経路、資源、Waiting、Blocked、Pending など、多数の状態を扱っている。

PCN Trace は、これらの状態を具体的な Target State Entry に対応する状態遷移判定として関連付ける。

例えば次の情報を一回の判定履歴として整理できる。

```text
PCN
Target State Entry
Target State
時間情報 T
C / A / E Mapping
S / D / B Evaluation
CAE-SDB Result
Arbitration Result
Multipath Control
実行結果
```

これにより、MES / WCS の協調停滞分析では、タスクや設備状態に加えて、Target State Entry 単位の判定結果を分析対象として利用できる。

### 生産 DX

生産 DX では、設備データ、生産データ、イベントデータなどを利用して、次のような分析を行う。

```text
設備 / 生産データ
→ 可視化
→ 分析
→ 改善
```

PCN Trace を用いる場合は、状態遷移判定に対して次のデータチェーンを形成できる。

```text
状態遷移前判定
→ PCN Trace
→ 状態遷移パターン分析
→ エンジニアリング改善
→ 再運用
→ Trace 比較
```

両者の主な整理対象を次に示す。

| 項目       | 設備 / 生産データ                 | PCN Trace                                                                    |
| -------- | -------------------------- | ---------------------------------------------------------------------------- |
| 主な記録対象   | 設備、工程、タスク、生産結果             | 一回の Target State Entry に対する状態遷移判定                                            |
| 主な確認内容   | 設備や生産プロセスで発生した状態・結果        | 判定に使用した状態、判定結果、制御経路、実行結果                                                     |
| データの整理単位 | 設備、時間、タスク、作業指示、イベント        | PCN、Target State Entry、Current State、Target State、時間情報 T                     |
| 主な分析項目   | 稼働、性能、品質、異常、生産数量           | C / A / E、S / D / B、CAE-SDB Result、Arbitration Result、Multipath Control、実行結果 |
| 主な改善対象   | 設備、工程、保全、生産プロセス            | 状態遷移条件、許可、実行チェーン、制御境界、制御経路                                                   |
| 改善確認     | OEE、サイクルタイム、生産数量、アラーム、品質など | 改善後の PCN Trace における判定、制御、実行結果の変化                                             |

PCN Trace によって、状態遷移判定を継続的に集計、比較、分析できる。

---

## 6. まとめ

製造現場では、設備データ、生産データ、タスクデータ、アラームデータ、イベントデータなどが継続的に記録されている。

PCN Trace は、これらの状態情報を一回の Target State Entry に対する状態遷移判定履歴として関連付ける。

基本的な記録関係は次の通りである。

```text
Current State
→ Target State
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ 実行結果
→ PCN Trace
```

各要素の役割は次の通りである。

* C / A / E は、今回の状態遷移に関係する状態の機能役割を表す。
* S / D / B は、各状態に対して適用する判定性質を表す。
* CAE-SDB Result は、一回の状態遷移前判定で形成された構造化判定結果である。
* 時間情報 T は、状態および判定とともに保持し、状態の前後関係、動的時系列有効性、PCN Trace に使用する。
* Arbitration は、判定結果と制御制約に基づいて制御上の優先関係を処理する。
* Multipath Control は、現在の Target State Entry に対するエンジニアリング制御出力である。
* 実行結果は、Multipath Control の実行後に確認された状態を記録する。
* PCN Trace は、これらを一回の状態遷移判定履歴として関連付ける。

本稿でいう「新しいエンジニアリングデータ」とは、

> **一回の Target State Entry に対する状態遷移判定そのものを、継続して記録、比較、集計、分析できるデータ対象として扱うこと**

を指す。

設備・生産データからは、設備や生産プロセスで発生した状態や結果を確認できる。

PCN Trace からは、

> **どの Target State Entry に対して、どの状態を判定に使用し、どの CAE-SDB Result と Arbitration Result が形成され、どの Multipath Control が選択され、最終的にどの実行結果となったか**

を確認できる。

この構造により、判定に使用した状態、構造化判定結果、制御選択、実行結果を、同じ状態遷移の文脈で継続して追跡できる。

---

## さらに読む

* [Concepts｜中核概念](/jp/concepts/)
* [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)
* [なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)
* [なぜ OEE の後に PCN が必要なのか？](/jp/notes/why-oee-pcn/)
* [複数の PCN はどのように状態遷移前制御ネットワークを形成するのか？](/jp/notes/pcn-network-structure/)
* [TPCA の状態遷移単方向性 ― なぜ実システムでは過去の状態インスタンスへ戻らないのか？](/jp/notes/tpca-unidirectional-state-transition/)

---

## 文書情報

題目："なぜ PCN Trace は新しいエンジニアリングデータなのか？"
文書種別：技術ノート
バージョン：Public Note Version 1.4
初回公開日：2026-07-14
最終更新日：2026-08-26
著者：全野南政 / Nansei Zenno
現在の URL：https://zennns.com/jp/notes/why-pcn-trace-is-engineering-data/

---

本稿は、TPCA / PCN 状態遷移前制御体系の公開説明資料である。
