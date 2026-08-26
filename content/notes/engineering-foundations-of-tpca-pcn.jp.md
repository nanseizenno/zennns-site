---
title: "TPCA / PCN はどのようなエンジニアリング基盤の上に成り立つのか？ ― 5つの基本的なエンジニアリング共通認識"
summary: "状態遷移、許可制約、実行チェーン、動的時系列有効性、制御境界という5つの基本的なエンジニアリング共通認識から、TPCA / PCN の位置付けを説明する。既存の PLC、状態機械、安全ロジック、スケジューリングシステム、エンジニアリング判断に分散している状態関係を、明確な Target State Entry を中心として整理する。"
description: "TPCA / PCN の基礎となる5つのエンジニアリング共通認識を整理する。さらに、PCN、C / A / E Mapping、S / D / B Evaluation、CAE-SDB Result、Arbitration、Multipath Control、PCN Trace によって、Target State Entry 前の判定を設計・判定・制御・追跡可能なエンジニアリング対象として構成する方法を説明する。"
date: 2026-08-18
lastmod: 2026-08-20
author: "全野南政 / Nansei Zenno"
document_type: "技術ノート"
version: "Public Note Version 1.0"
citation_url: "https://zennns.com/jp/notes/engineering-foundations-of-tpca-pcn/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## TPCA / PCN はどのようなエンジニアリング基盤の上に成り立つのか？

新しいエンジニアリング手法を評価する場合、個々の構成要素が既存技術に含まれているかだけでなく、それらをどの対象に対して、どのような関係で組み合わせているかを確認する必要がある。

状態、状態遷移、Interlock、Ready、安全許可、タイムアウト、縮退実行、代替経路などの機構は、すでに成熟した産業オートメーションシステムで広く使用されている。IEC 61131-3、ISA-88、ISO 13849-1、OPC UA なども、プログラム構成、バッチプロセス制御、安全関連制御、状態情報モデルなどの観点から、それぞれのエンジニアリング基盤を形成している。[1][2][3][4]

複雑な自動化システムでは、これらの機構を備えていても、次のような状態が発生することがある。

- 設備にアラームはないが、次の段階へ進まない。
- ロボットは Ready であるが、動作が開始されない。
- MES にタスクがあり、WCS にも記録があるが、現場では Waiting が継続している。
- 個々の設備は運転可能である一方、後続の実行チェーンが継続できない。
- 直前まで有効であった状態が、短時間後には今回の Target State Entry の判定に使用できなくなる。
- 安全許可、運転条件、下流状態、異常処理経路などが複数のプログラムやシステムに分散し、状態遷移の判定時に複数の情報を照合する必要がある。

TPCA / PCN は、

> **システムが明確な Target State へ入ろうとする際に、分散している状態関係を同じ Target State Entry に対応付けて判定する**

ことを対象とする。

この考え方は、次の5つの基本的なエンジニアリング共通認識に基づいている。

---

## 1. エンジニアリング制御では状態と状態遷移の両方を扱う

一つの信号が TRUE であることは、その信号が表す局所状態を示す。

Target State へ進む判定では、その状態に加えて、Current State、Target State、および今回の Target State Entry に関係する他の状態を確認する。

例えば Robot Ready は、ロボット本体の運転準備状態を示す。

一方、ロボットが次の段階へ進む Target State Entry では、例えば次の状態も判定対象となる。

- Current State
- Target State
- ワーク条件
- 必要な許可
- 下流受入状態
- 今回の判定に使用する状態の動的時系列有効性

自動化制御では、個々の信号値とともに、状態間の遷移関係が重要な設計対象となる。

例えば、

```text
Current State → Target State
```

という関係を明確にした上で、

> **Current State から Target State へ進むために、今回の Target State Entry でどの状態を確認するか。**

を定義する。

SFC、状態機械、産業設備の状態モデルなどでは、状態、ステップ、遷移を用いて制御関係を構成している。[1][2][4]

TPCA では、分析対象を明確な Target State Entry に設定する。

```text
Current State → Target State
```

を明確にすることで、後続の C / A / E Mapping と S / D / B Evaluation の判定対象を定めることができる。

---

## 2. 実行条件と進入許可は異なる状態変数領域として扱う

複雑なエンジニアリングシステムでは、設備や経路が実行可能な状態であっても、Target State への進入には別途許可が必要となる場合がある。

例えば、ロボットが Ready であり、グリッパ状態や経路状態が運転可能であっても、安全許可、エリア許可、上位システム許可などが Target State Entry の必要条件として設定されている場合、それらの許可状態を個別に確認する。

安全関連制御は、独立したエンジニアリング領域として確立されている。ISO 13849-1:2023 は、安全機能を実行する制御システムの安全関連部（SRP/CS）について、設計と統合に関する方法、要求事項、推奨事項、指針を示している。[3]

TPCA では、Target State Entry に関係する状態を C / A / E の状態変数領域に整理する。

### C：Condition

C は、Target State へ入るために必要な事実条件に関係する状態変数領域である。

代表例は次の通りである。

- 対象条件
- 現場条件
- 認識条件
- タスク条件
- パラメータ条件
- 前工程完了状態

### A：Authority

A は、Target State への進入を許可する状態に関係する状態変数領域である。

代表例は次の通りである。

- 安全許可
- エリア許可
- 上位システム許可
- 手動確認
- 権限・認可
- 資源ロック
- 相手機器からの許可

重要な A は、Target State Entry に対する独立した必要制約として設定できる。

例えば、

```text
C：必要な事実条件を満たしている
A：重要な許可が未成立
E：実行チェーンに必要な状態を確認済み
```

という場合、Arbitration では重要な A の制約を含めて今回の Target State Entry に対する制御上の優先関係を処理する。

C と A を分けて扱うことで、事実条件と進入許可をそれぞれの役割に応じて判定できる。

---

## 3. Target State Entry では実行チェーン全体を確認する

複雑な自動化システムでは、単体設備の Ready に加えて、Target State へ入った後の実行チェーンに関係する状態を確認する必要がある。

例えば、

- ロボットが Ready であっても、ピックアップ後の配置先状態を確認する必要がある。
- 圧入設備が Ready であっても、搬送機構の位置や後続工程の状態が関係する場合がある。
- 検査設備が Ready であっても、検査結果の送信や後工程への引渡し状態が関係する場合がある。
- AGV が Ready であっても、Target State Entry に関係するステーション受入状態を確認する必要がある。
- 主設備の状態に加えて、異常処理、回流、結果書戻しなどの経路状態が今回の実行チェーン定義に含まれる場合がある。

ISA-88 では、バッチプロセス制御に関する物理モデル、機能関係、シーケンス制御などの標準化された枠組みが整備されており、関連資料では機械やユニット状態の実装例も示されている。[2]

TPCA では、

> **E = Execution Chain / 実行チェーン状態**

を、Target State へ入った後の実行チェーンに関係する状態変数領域として扱う。

E に関係する代表的な状態には、次のようなものがある。

- 本体設備状態
- エンドエフェクタ状態
- 下流受入状態
- 正常実行経路
- 回流経路
- 異常分流経路
- 代替経路
- 資源解放状態
- 結果送信状態
- 状態書戻し状態
- 相手機器の受入状態

どの経路や状態を E に含めるかは、今回の Target State Entry に対して定義した実行チェーンに基づいて決定する。

Robot Ready などの局所状態は、E に関係する入力状態の一つとして使用できる。

---

## 4. 状態判定には時間情報と動的時系列有効性が必要である

産業システムでは、状態値そのものに加えて、その状態を今回の Target State Entry の判定に使用できるかを確認する必要がある。

例えば、

- 画像認識システムが OK を出力した後、ワーク位置が変化している。
- 下流設備が Ready を出力した後、設備状態が切り替わっている。
- 資源ロックが解放された後、他の主体によって再取得されている。
- 上位許可が成立した後、許可が取り消されている。

このような場合、状態値、更新時刻、状態変化、関連状態との同期関係を組み合わせて判定する。

確認対象には、例えば次のようなものがある。

- 状態の生成時刻
- 更新状態
- タイムアウト
- チャタリング
- 関連状態間の同期
- 状態競合
- 状態切替
- 認識信頼度

TPCA では、この判定性質を、

> **D = Dynamics / 動的時系列有効性**

として扱う。

また、状態の利用可否を判定する前提として、判定に必要な構造が定義され、接続され、観測可能であることを確認する。

この判定性質を、

> **S = Structure / 構造完全性**

として扱う。

例えば、同じ状態に対して次の2つの観点を設定できる。

```text
S：
必要な信号、インターフェース、マッピング関係が定義・接続されているか

D：
取得した状態が現在も有効で、今回の Target State Entry に使用できるか
```

OPC UA の状態機械情報モデルでは、CurrentState、Transition、LastTransition、Transition の時間情報などが明示的に表現されている。[4]

TPCA / PCN では、状態および判定とともに時間情報 T を保持し、状態の前後関係、D の判定、PCN Trace に使用する。

---

## 5. エンジニアリングシステムでは制御境界を事前に定義する

産業システムの状態は、単純な二値だけで表現できない場合がある。

例えば、

- 画像認識信頼度が許容範囲の境界付近にある。
- 位置偏差が補正可能範囲の境界付近にある。
- 下流受入待ちが継続し、事前に設定された待機時間に近づいている。
- 許可状態が切替中であり、確認時間の境界に近づいている。

このような状態を扱うため、エンジニアリングシステムでは、値、時間、回数、容量などに対して制御境界を設定することがある。

代表的な対象は次の通りである。

- 許容範囲
- 再サンプリング条件
- 再確認条件
- 再試行回数
- 縮退実行の候補範囲
- 進入禁止に関係する境界
- 手動確認に関係する境界
- 上位制約へ移行する条件

TPCA では、この判定性質を、

> **B = Boundary / 制御境界**

として扱う。

B は、C / A / E に関係する状態と、事前に定義された制御境界との関係を判定する。

例えば、

- 画像認識信頼度と事前定義された境界との関係を C-B として表す。
- 許可状態に関係する確認条件と制御境界との関係を A-B として表す。
- 下流待機時間と実行チェーン側の制御境界との関係を E-B として表す。

これらの CAE-SDB Result は、他の判定結果および制御制約とともに Arbitration で処理される。

Arbitration の結果に基づいて、待機、再サンプリング、回流、手動確認、縮退実行、進入禁止などの Multipath Control を形成する。

---

## 6. TPCA / PCN はこれらのエンジニアリング基盤をどのように構成するか

前述した5つの事項は、既存の産業オートメーションでも広く使用されている。

- 状態機械や SFC は状態と遷移を扱う。
- PLC や設備プログラムでは Interlock を使用する。
- 安全関連制御では、安全機能と許可状態を扱う。
- 産業システムでは、更新、同期、タイムアウトなどの時間的な状態管理を行う。
- 制御システムでは、値、時間、回数、容量などに対する各種制御境界を使用する。

TPCA / PCN は、これらを明確な Target State Entry を中心として、一回の状態遷移前判定と制御の関係に整理する。

Target State Entry には PCN（Pre-Control Node / 前制御ノード）を配置する。

基本的な処理関係は次の通りである。

```text
Current State
→ Target State
→ PCN
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

各要素の役割は次の通りである。

**PCN** は、

> どの Target State Entry を今回の判定対象とするか。

を明確にする。

**C / A / E** は、

> 今回の Target State Entry に関係する状態が、Condition、Authority、Execution Chain のどの機能役割を持つか。

を整理する。

**S / D / B** は、

> 関連状態に対して、Structure、Dynamics、Boundary のどの判定性質を適用するか。

を定める。

**CAE-SDB Result** は、

> C / A / E と S / D / B の判定によって形成された構造化判定結果

を表す。

**時間情報 T** は、

> 状態および判定とともに保持し、状態の前後関係、動的時系列有効性、PCN Trace に使用する。

**Arbitration** は、

> CAE-SDB Result と事前定義された制御制約に基づき、制御上の優先関係を処理する。

**Multipath Control** は、

> Arbitration の結果に基づいて、今回の Target State Entry に対する次の Target State または目標実行経路を形成する。

**PCN Trace** は、

> 今回の Target State Entry における入力状態、判定、時間情報 T、Arbitration Result、Multipath Control、実行結果を状態遷移判定履歴として記録する。

この関係により、一回の Target State Entry を次の工程単位として扱うことができる。

```text
Target State Entry
→ 状態整理
→ 構造化判定
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

---

## まとめ

TPCA / PCN は、成熟した産業オートメーション技術を基盤として、明確な Target State Entry に対する状態遷移前判定を構成する。

その基礎となる5つの共通認識は、次の通りである。

1. エンジニアリング制御では、個々の状態とともに状態遷移を扱う。
2. Condition と Authority は異なる状態変数領域として整理する。
3. Target State Entry では、局所的な Ready に加えて Execution Chain に関係する状態を確認する。
4. 状態判定では、Structure と Dynamics、および時間情報 T を使用して現在の判定根拠を確認する。
5. Boundary により、関連状態と事前定義された制御境界との関係を判定する。

TPCA / PCN は、これらを一つの Target State Entry に対応する次の処理関係として整理する。

```text
PCN
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

これにより、Target State Entry を設計、判定、制御、記録、追跡できるエンジニアリング対象として扱うことができる。

---

## 参考文献と外部資料

以下の資料は、本文で扱った状態遷移、バッチプロセス制御、安全関連制御、状態情報モデルなどの既存のエンジニアリング基盤を示すための参考資料である。

1. **PLCopen — IEC 61131-3**  
   PLCopen による IEC 61131-3 PLC プログラミング言語体系の公開説明。Sequential Function Chart（SFC）では、ステップ、遷移、アクションを用いてシーケンス制御を構成する。  
   https://www.plcopen.org/standards/logic/iec-61131-3/

2. **ISA — ISA-88 Series of Standards: Batch Process Control**  
   ISA-88 は、バッチプロセス制御に関する用語、データ構造、物理モデル、機能関係などの標準化された枠組みを提供する。関連技術資料には、機械およびユニット状態に関する実装例も含まれる。  
   https://www.isa.org/standards-and-publications/isa-standards/isa-88-standards

3. **ISO 13849-1:2023 — Safety of machinery — Safety-related parts of control systems — Part 1: General principles for design**  
   安全機能を実行する制御システムの安全関連部（SRP/CS）の設計および統合に関する方法、要求事項、推奨事項、指針を示す。  
   https://www.iso.org/standard/73481.html

4. **OPC Foundation — OPC Unified Architecture, Part 16: State Machines**  
   OPC UA Part 16 は、状態機械、CurrentState、状態遷移、および関連する状態変数を規定する。TransitionVariableType には遷移時刻に関係する情報も含まれる。  
   https://reference.opcfoundation.org/specs/OPC-10000-16

---

## 文書情報

題目：TPCA / PCN はどのようなエンジニアリング基盤の上に成り立つのか？ ― 5つの基本的なエンジニアリング共通認識  
文書種別：技術ノート  
バージョン：Public Note Version 1.0  
公開日：2026-08-18  
著者：全野南政 / Nansei Zenno  
現在の URL：https://zennns.com/jp/notes/engineering-foundations-of-tpca-pcn/

---

本稿は、TPCA / PCN 状態遷移前制御体系の公開説明資料である。
