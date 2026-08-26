---
title: "TPCA / PCN と既存の産業オートメーション手法・制御メカニズムとの関係"
summary: "TPCA / PCN と FMEA、STPA、RCA、Process Mining、状態機械、SFC、Interlock、安全制御、アラーム管理、MES / WCS、AI 分析、形式検証との役割分担と適用範囲を説明する。"
description: "既存の産業オートメーション手法や制御機構がそれぞれの役割を担う中で、TPCA / PCN が明確な Target State Entry を対象として、分散している状態、条件、許可、実行チェーン、判定結果、制御出力を、判定・制御・記録・追跡可能な PCN として整理する位置付けを説明する。"
date: 2026-07-04
lastmod: 2026-08-20
author: "全野南政 / Nansei Zenno"
document_type: "技術ノート"
version: "Public Note Version 1.2"
citation_url: "https://zennns.com/jp/notes/tpca-existing-theories/"
draft: false
weight: 1
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## TPCA / PCN と既存の産業オートメーション手法・制御メカニズムとの関係

基本概念については、以下を参照。

- [中核概念](/jp/concepts/)
- [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)
- [なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)
- [なぜ状態遷移条件を明示する必要があるのか？](/jp/notes/explicit-state-transition-conditions/)
- [TPCA / PCN はどのようなエンジニアリング基盤の上に成り立つのか？ ― 5つの基本的なエンジニアリング共通認識](/jp/notes/engineering-foundations-of-tpca-pcn/)
- [TPCA / PCN は既存技術上の論点をどのように捉えるのか？ ― 3つの代表的なエンジニアリング論点](/jp/notes/engineering-positions-of-tpca-pcn/)

---

## 1. 本稿で扱う範囲

産業オートメーションでは、状態、状態遷移、Ready、Interlock、安全許可、アラーム、タイムアウト、資源制約、異常処理などがすでに広く使用されている。

状態機械や SFC では、状態、ステップ、遷移条件を定義できる。

PLC、ロボットコントローラ、設備プログラムには、Interlock、Handshake、Ready、シーケンス制御などのロジックが実装されている。

安全 PLC、安全リレー、安全回路は、安全機能や危険動作の制限、安全許可を担う。

MES、WCS、群制御システムでは、タスク、資源、経路、ステーション、権限、実行条件などを管理・判定している。

TPCA / PCN は、これらの既存機構を利用しながら、次の工程対象を扱う。

> **明確な Target State Entry に対して、複数の設備、システム、制御機構に分散している状態を、一回の状態遷移前判定、制御、履歴として整理する。**

例えば、ロボットがピックアップ段階へ入る前には、すでに次のような状態が存在する場合がある。

- 画像認識結果
- Robot Ready
- 安全エリア許可
- PLC Interlock
- 上位システム許可
- 下流受入状態
- 戻り経路状態

PCN は、今回の Target State Entry に対して、これらの状態を次の観点から整理する。

- Current State は何か。
- Target State は何か。
- C にマッピングする状態は何か。
- A にマッピングする状態は何か。
- E にマッピングする状態は何か。
- 関連状態に対して、どの S / D / B 判定が必要か。
- 複数の CAE-SDB Result が形成された場合、Arbitration でどのように制御上の優先関係を処理するか。
- 今回の Target State Entry に対して、どの Multipath Control を形成するか。
- 判定、制御、実行結果をどのように PCN Trace として記録するか。

TPCA / PCN では、この一回の Target State Entry に対する状態遷移判定を、独立したエンジニアリング対象として扱う。

---

## 2. FMEA、STPA、RCA、Process Mining との関係

FMEA、STPA、RCA、Process Mining は、複雑なエンジニアリング上の問題を構造化するために用いられる。

それぞれの基本的位置付けについては、ASQ の FMEA 公開資料、MIT の STPA Handbook、ASQ の RCA 公開資料、van der Aalst の Process Mining に関する文献を参照できる。[1][2][3][4]

| 手法 | 主な対象 |
|---|---|
| FMEA | 潜在的な故障モード、影響、原因、管理策 |
| STPA / STAMP | 安全制御構造、制御制約、ハザードシナリオ |
| RCA | 発生した問題とその原因関係 |
| Process Mining | イベントログから復元した実際のプロセス、逸脱、待機、ボトルネック |
| TPCA / PCN | 明確な Target State Entry におけるランタイムの状態遷移前判定と制御 |

FMEA では、主として次の問題を扱う。

> 何が故障する可能性があるか。

STPA / STAMP では、主として次の問題を扱う。

> どのような制御関係が危険な状態につながる可能性があるか。

RCA では、主として次の問題を扱う。

> 発生した問題は、なぜ発生したか。

Process Mining では、主として次の問題を扱う。

> 実際のプロセスはどのように流れ、どこで待機、手直し、逸脱が発生しているか。

TPCA / PCN では、実運転中の明確な Target State Entry に対して、次の問題を扱う。

> **現在の状態から Target State へ進むために必要な状態を判定し、その結果に基づいてどの制御経路へ進むか。**

これらの手法は、同じエンジニアリングシステムに対して異なる段階から利用できる。

例えば FMEA では、ある許可信号に関する故障リスクを分析できる。

STPA では、安全許可に関係する制御構造や制約を分析できる。

PCN では、実運転時に取得した許可状態を A に関係する状態として、今回の Target State Entry の判定に使用する。

---

## 3. 状態機械、SFC、Interlock、安全制御、アラーム管理との関係

### 3.1 状態機械、SFC と PCN

状態機械や SFC は、状態、遷移、シーケンスを構成するための基本的な制御手法である。

状態図 / Statecharts の代表的な研究については Harel、SFC を含む PLC プログラミング言語の標準化については IEC 61131-3 および PLCopen の公開資料を参照できる。[5][6]

状態機械や SFC では、例えば次の内容を定義できる。

- 状態
- ステップ
- 動作
- 遷移
- 遷移条件
- 状態間の実行関係

例えば、既存の遷移条件を次のように構成できる。

```text
Vision_OK
AND Robot_Ready
AND Safety_OK
AND Downstream_Ready
```

このロジックは、設備の状態遷移条件としてそのまま使用できる。

PCN では、同じ Target State Entry に関係する状態を、さらに次の処理関係で整理する。

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
→ PCN Trace
```

状態機械や SFC は、状態、遷移、シーケンス制御を担う。

PCN は、その中の明確な Target State Entry を対象として、今回の遷移に関係する複数ソース状態を整理し、判定、Arbitration、Multipath Control、PCN Trace へ展開する。

PCN は、既存の状態機械、SFC、PLC 制御プログラムの内部に組み込む構成や、それらと連携する判定モジュールとして構成できる。

---

### 3.2 Interlock と PCN

Interlock は、複数の状態を組み合わせ、設備動作や工程への進入を制限するために広く使用されている。

既存の Interlock は、その設備やシステムで定義された制御条件として継続して使用できる。

PCN では、Interlock に関係する個々の状態を、今回の Target State Entry における C / A / E の役割と、必要な S / D / B 判定に基づいて整理する。

例えば、Interlock に関係する状態として次のようなものがある。

- Target State へ進むための条件状態
- 重要な許可状態
- 下流受入や後続工程に関係する実行チェーン状態
- 更新時刻や同期状態
- 事前定義された制御境界に関係する状態

これらの状態から CAE-SDB Result を形成し、Arbitration を経て今回の Target State Entry に対応する Multipath Control を形成する。

この構成により、Interlock の状態と、Target State Entry に対する状態遷移判定を同じ工程関係の中で扱うことができる。

---

### 3.3 安全制御と PCN

安全 PLC、安全リレー、安全扉、ライトカーテン、非常停止、安全スキャナなどは、設備や機械の安全機能を構成する。

機械安全に関係する制御システムの設計原則については、ISO 13849-1 を参照できる。[7]

PCN は、安全システムから出力される許可状態を A に関係する状態として取得できる。

例えば、

```text
C：Target State へ進むための条件状態

A：重要な安全許可状態

E：Target State へ進んだ後の実行チェーン状態
```

として整理する。

重要な安全許可は、Target State Entry に対する独立した必要制約として扱う。

安全システムは安全機能と安全許可を担い、PCN はその許可状態を今回の Target State Entry に関係する A として他の状態とともに判定する。

---

### 3.4 アラーム管理、故障診断と PCN

アラーム管理には、アラーム定義、優先度、応答、履歴、ライフサイクルなどを扱う既存の体系がある。

IEC 62682 および ISA-18.2 は、プロセス産業におけるアラーム管理の代表的な標準体系である。公開資料については ISA の ISA-18.2 関連資料を参照できる。[8]

アラーム管理では、例えば次の内容を扱う。

- アラーム定義
- アラーム優先度
- アラーム応答
- アラーム履歴
- アラームライフサイクル

故障診断では、例えば次の内容を扱う。

- 故障モード
- 故障原因
- 故障伝播
- 故障位置

PCN では、これらのアラーム、故障、異常に関係する状態を、今回の Target State Entry における C / A / E と S / D / B の判定対象として扱うことができる。

例えば同じ通信異常であっても、Target State Entry によって関係する状態変数領域が異なる場合がある。

ある Target State Entry では、画像認識結果の有効性に関係する C の状態となる。

別の Target State Entry では、上位システム許可に関係する A の状態となる。

さらに別の Target State Entry では、結果書戻し経路に関係する E の状態となる。

アラーム管理は異常情報を管理し、故障診断は故障状態や原因を分析する。

PCN は、それらの状態を今回の Target State Entry に関連付け、CAE-SDB Result、Arbitration、Multipath Control へ展開する。

---

## 4. MES / WCS、AI 分析、形式検証との関係

### 4.1 MES / WCS と PCN

MES、WCS、群制御システムには、タスク、資源、実行、情報交換に関する多数の機能が実装されている。

製造オペレーションと企業システム・制御システム間の情報モデルや統合境界については、ISA-95 / IEC 62264 シリーズを参照できる。[9]

MES、WCS、群制御システムでは、例えば次の情報や機能を扱う。

- タスク条件
- 資源制約
- 経路状態
- ステーション状態
- 車両状態
- 資源ロック
- 権限・許可
- スケジューリングルール
- 実行可能性の判定

PCN は、重要なタスク、協調状態、実行経路が次の Target State へ進む Target State Entry に対して、複数システムに分散した関連状態を一つの状態遷移判定として整理する。

例えば、次の状態が取得されている場合を考える。

```text
MES：タスク生成済み
WCS：タスク記録あり
設備：オンライン
車両：オンライン
主要アラームなし
```

今回の Target State Entry では、さらに次の状態を確認できる。

- タスク状態が今回の判定に使用できるか。
- スケジューリングや資源に関する許可状態はどうなっているか。
- 資源ロック状態はどうなっているか。
- 経路状態は今回の実行に使用できるか。
- 下流ステーションは受入可能か。
- 関連状態の更新時刻や同期状態は適切か。
- Target State へ進んだ後の実行チェーンを継続できるか。

MES / WCS は、タスク、資源、スケジューリングなどの機能を継続して担う。

PCN は、その中の重要な Target State Entry に対して、構造化された状態遷移前判定、Arbitration、Multipath Control、PCN Trace を構成できる。

---

### 4.2 AI とデータ分析

AI やデータ分析は、例えば次の用途に利用できる。

- 履歴比較
- パターン分析
- トレンド分析
- クラスタリング
- 改善候補の抽出
- レポート作成

PCN Runtime では、明確な工程状態、許可、ルール、制御境界に基づいて、Target State Entry に対する判定と制御を行う。

PCN Trace が蓄積された後は、AI を用いて例えば次の分析を支援できる。

- 同じ Target State Entry で繰り返し発生する状態の抽出
- 高頻度で形成される CAE-SDB Result の比較
- 頻繁に選択される Multipath Control の分析
- エンジニアリング変更前後における判定結果や実行結果の比較

この構成では、PCN Runtime が状態遷移前判定と Multipath Control を担い、AI は PCN Trace を用いた比較分析や改善検討を支援する。

---

### 4.3 形式検証とランタイム検証

形式検証、モデル検査、ランタイム検証では、状態、状態遷移、制約、性質、実行イベントなどを扱う。

モデル検査およびランタイム検証は、TPCA / PCN と隣接する技術領域である。

形式的手法では、一般に次のような問題を扱う。

> システムまたはモデルが、事前に定義した性質を満たしているか。

PCN では、実運転中の明確な Target State Entry に対して、

> **今回の状態遷移に必要な状態をどのように判定し、その結果としてどの Multipath Control を形成するか。**

を扱う。

形式検証やランタイム検証によって得られた結果を、システム構成に応じて PCN の入力状態として利用することもできる。

---

## 5. TPCA / PCN が追加する工程構造

TPCA / PCN で扱う個々の要素は、既存の産業オートメーションでも広く使用されている。

例えば、

- Condition
- Authority
- Ready
- 状態遷移
- Interlock
- アラーム
- タイムアウト
- 待機
- 再試行
- 回流
- 縮退実行

などである。

TPCA / PCN では、これらの状態や制御要素を、明確な Target State Entry を中心として一つの工程構造に整理する。

基本的な処理関係は次の通りである。

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
→ PCN Trace
```

一回の Target State Entry に関係する状態は、例えば次のシステムに分散している場合がある。

```text
PLC
ロボット
画像認識システム
安全システム
MES
WCS
下流設備
資源ロック
手動確認
```

PCN は、これらの状態を同じ Target State Entry に対応付ける。

その上で、

- C / A / E の状態変数領域へマッピングする。
- 必要な S / D / B 判定を行う。
- CAE-SDB Result と時間情報 T を形成する。
- Arbitration で制御上の優先関係を処理する。
- Multipath Control を形成する。
- 判定、制御、実行結果を PCN Trace として記録する。

これにより、一回の Target State Entry を、

> **独立して設計、判定、制御、記録、追跡できるエンジニアリング対象**

として扱うことができる。

---

## 6. 既存の自動化システムとの役割分担

TPCA / PCN と既存の自動化システムとの主な役割分担を次に示す。

| 既存の対象 | 主な役割 | PCN との関係 |
|---|---|---|
| PLC / 状態機械 / SFC | シーケンス制御、状態管理、動作実行 | 状態と遷移ロジックを構成し、PCN と連携して Target State Entry の判定結果を利用する |
| Interlock / Handshake | 動作条件、設備間の条件調整 | Target State Entry に関係する入力状態や既存の制御制約として利用する |
| 安全システム | 安全機能、安全許可、危険動作の制限 | Target State Entry に必要な重要な A の状態を提供する |
| アラーム管理 / 故障診断 | 異常管理、故障分析、原因分析 | アラームや診断結果を PCN の判定に関係する状態として利用できる |
| MES / WCS | タスク、資源、スケジューリング、生産協調 | 上位状態を提供し、必要に応じて PCN の判定・制御・履歴情報を利用する |
| AI / データ分析 | 履歴分析、パターン抽出、改善支援 | PCN Trace を用いて比較分析や改善検討を支援する |
| TPCA / PCN | Target State Entry に対する構造化判定、Arbitration、Multipath Control、PCN Trace | 複数ソース状態を同じ Target State Entry に対応付け、状態遷移前判定と制御を構成する |

この役割分担により、既存の設備制御、安全制御、タスク管理、スケジューリング、診断機能を維持しながら、複数の工程レベルに分散している状態を一回の Target State Entry に関連付けることができる。

---

## まとめ

産業オートメーションには、状態機械、SFC、Interlock、安全制御、アラーム管理、故障診断、MES / WCS、各種分析手法など、多数の成熟した工程技術が存在する。

TPCA / PCN は、これらの既存機構が提供する状態や判定結果を、明確な Target State Entry を中心として次の処理関係に整理する。

```text
Current State
→ Target State
→ Target State Entry / PCN
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

既存の各システムは、それぞれの状態取得、設備制御、安全制御、タスク管理、スケジューリング、診断、実行などを担う。

PCN は、その中の明確な Target State Entry に関係する状態をまとめ、C / A / E の状態変数領域と S / D / B の判定性質によって CAE-SDB Result を形成する。

その結果と時間情報 T を Arbitration で処理し、今回の Target State Entry に対する Multipath Control を形成する。

さらに、判定に使用した状態、CAE-SDB Result、Arbitration Result、Multipath Control、実行結果を PCN Trace として記録する。

この構成により、一回の状態遷移入口を、設計、判定、制御、記録、追跡の共通単位として扱うことができる。

---

## 参考文献と外部資料

本節の参考文献は、本文で比較した既存の産業オートメーション手法、標準、理論の基本的位置付けを確認するための資料である。

一部の IEC / ISO 規格本文は有償またはアクセス条件があるため、ここでは公開されている公式機関ページ、学術出版ページ、安定した書誌情報を中心に掲載する。正式な規格番号は、追加調査のため各項目に記載する。

1. **ASQ — What is FMEA? Failure Mode & Effects Analysis**  
   FMEA の基本対象、用途、分析方法に関する公開資料。正式規格については IEC 60812:2018 も参照できる。  
   https://asq.org/quality-resources/fmea

2. **MIT Partnership for Systems Approaches to Safety and Security — Books and Handbooks**  
   *STPA Handbook* および STPA / CAST 関連資料への公開入口。  
   https://psas.scripts.mit.edu/home/books-and-handbooks/

3. **ASQ — What is Root Cause Analysis (RCA)?**  
   RCA の基本的位置付けを確認するための公開資料。  
   https://asq.org/quality-resources/root-cause-analysis

4. **Wil van der Aalst — *Process Mining: Data Science in Action*, 2nd ed., Springer, 2016**  
   Process Mining に関する代表的な体系書。  
   DOI: 10.1007/978-3-662-49851-4  
   https://link.springer.com/book/10.1007/978-3-662-49851-4

5. **David Harel — “Statecharts: A Visual Formalism for Complex Systems,” 1987**  
   Statecharts に関する代表的な論文。  
   DOI: 10.1016/0167-6423(87)90035-9  
   https://doi.org/10.1016/0167-6423(87)90035-9

6. **PLCopen — IEC 61131-3**  
   IEC 61131-3 の PLC プログラミング言語体系、および SFC の位置付けに関する公開資料。正式規格については IEC 61131-3 を参照。  
   https://www.plcopen.org/standards/logic/iec-61131-3/

7. **ISO 13849-1:2023 — Safety of machinery — Safety-related parts of control systems**  
   機械安全に関係する制御システムの設計原則を示す ISO 公式ページ。  
   https://www.iso.org/standard/73481.html

8. **ISA — ISA-18.2, Management of Alarm Systems for the Process Industries**  
   ISA-18.2 および IEC 62682 との関係を含むアラーム管理に関する公開資料。  
   https://www.isa.org/intech/2020/september-october/isa-18-2-management-of-alarm-systems-for-the-proce

9. **ISA — ISA-95 Series of Standards: Enterprise-Control System Integration**  
   ISA-95 / IEC 62264 の階層、対象、企業システムと製造制御システム間の情報統合に関する ISA 公式ページ。  
   https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard

10. **Martin Leucker, Christian Schallhart — “A brief account of runtime verification,” 2009**  
    ランタイム検証に関する代表的なレビュー論文。  
    DOI: 10.1016/j.jlap.2008.08.004  
    https://doi.org/10.1016/j.jlap.2008.08.004

## 文書情報

題目："TPCA / PCN と既存の産業オートメーション手法・制御機構の関係"  
文書種別：技術ノート  
バージョン：Public Note Version 1.2  
初回公開日：2026-07-04  
最終更新日：2026-08-20  
著者：全野南政 / Nansei Zenno  
現在の URL：https://zennns.com/jp/notes/tpca-existing-theories/
