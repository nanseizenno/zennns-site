---
title: "TPCA / PCN と既存の産業オートメーション技術・エンジニアリング手法との関係"
summary: "TPCA / PCN と FMEA、STPA、RCA、Process Mining、状態機械、SFC、Interlock、安全制御、MES / WCS、AI 分析などとの役割分担を、Target State Entry を中心として整理する。"
description: "既存の産業オートメーション手法や制御機構がそれぞれの役割を担う中で、TPCA / PCN が Target State Entry に対する判定・制御・記録をどのように構成するかを説明する。"
date: 2026-07-04
lastmod: 2026-09-08
author: "全野南政 / Nansei Zenno"
document_type: "技術ノート"
version: "Public Note Version 1.3"
citation_url: "https://zennns.com/jp/notes/tpca-existing-theories/"
draft: false
weight: 1
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## TPCA / PCN と既存の産業オートメーション技術・エンジニアリング手法との関係

産業オートメーションには、状態機械、SFC、Interlock、安全制御、アラーム管理、MES / WCS、FMEA、STPA、RCA、Process Mining など、多数の成熟した手法や制御機構が存在する。

それぞれは、状態管理、安全、設備制御、タスク管理、故障分析、履歴分析など、異なる役割を担っている。

TPCA / PCN は、これらの既存技術が提供する状態や判定結果を利用しながら、明確な Target State Entry に対する状態遷移前判定、制御、履歴を一つの工程単位として整理する。

基本関係は次の通りである。

```text
Current State
    ↓
Target State Entry / PCN
    ↓
Target State
```

PCN では、今回の Target State Entry に関係する状態を取得し、次の関係へ接続する。

```text
関連状態
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

本稿では、既存技術そのものを網羅的に説明するのではなく、

> **既存の手法や制御機構がそれぞれの役割を担う中で、TPCA / PCN がどの工程位置を担当するか**

を整理する。

基本概念については、以下を参照。

- [Concepts｜中核概念](/jp/concepts/)
- [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)
- [なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)

---

## 1. 分析・診断手法との関係

FMEA、STPA、RCA、Process Mining は、複雑なエンジニアリング上の問題を異なる観点から分析するために利用される。

| 手法 | 主な対象 |
|---|---|
| FMEA | 潜在的な故障モード、影響、原因、管理策 |
| STPA / STAMP | 安全制御構造、制御制約、ハザードシナリオ |
| RCA | 発生した問題とその原因関係 |
| Process Mining | イベントログから確認される実際のプロセス、逸脱、待機、ボトルネック |
| TPCA / PCN | 明確な Target State Entry における状態遷移前判定、制御、履歴 |

例えば、ある許可状態に問題がある場合、

- FMEA では、その許可に関係する故障モードや影響を分析できる。
- STPA では、その許可に関係する制御構造や安全制約を分析できる。
- RCA では、実際に発生した問題の原因関係を分析できる。
- Process Mining では、その問題が工程全体の待機や逸脱としてどのように現れているかを分析できる。
- PCN では、実運転中に取得した許可状態を、今回の Target State Entry に関係する A：Authority の状態として判定に使用する。

このように、分析・診断手法と PCN は同じシステムに対して異なる工程位置から利用できる。

STPA / STAMP の代表的な公開資料については MIT の STPA Handbook、Process Mining については van der Aalst の体系書を参照できる。[1][2]

---

## 2. 状態機械、SFC、Interlock、安全制御との関係

### 2.1 状態機械、SFC

状態機械や SFC は、状態、ステップ、遷移、シーケンスを構成するための基本的な制御手法である。

例えば、設備の遷移条件を次のように構成できる。

```text
Vision_OK
AND Robot_Ready
AND Safety_OK
AND Downstream_Ready
```

このような既存の状態遷移条件は、そのまま設備制御に使用できる。

PCN は、その中の明確な Target State Entry に対して、今回の遷移に関係する状態を対応付け、CAE-SDB Result、Arbitration、Multipath Control、PCN Trace へ接続する。

状態機械や SFC は状態遷移とシーケンスを構成し、PCN は Target State Entry 単位の判定・制御・履歴を構成する。

SFC を含む PLC プログラミング言語体系については、IEC 61131-3 および PLCopen の公開資料を参照できる。[3]

### 2.2 Interlock / Handshake

Interlock や Handshake は、設備動作や設備間連携に必要な条件を構成するために広く使用されている。

PCN では、既存の Interlock や Handshake に関係する状態を、今回の Target State Entry における関連状態として利用できる。

例えば、

- Target State へ進むための条件
- 重要な許可
- 下流受入状態
- 相手機器の状態
- 更新時刻や同期状態

などを、C / A / E の役割と必要な S / D / B 判定に対応付ける。

Interlock や Handshake は既存の設備制御条件を担い、PCN はそれらを Target State Entry 単位の判定関係へ整理する。

### 2.3 安全制御

安全 PLC、安全リレー、安全扉、ライトカーテン、非常停止、安全スキャナなどは、設備や機械の安全機能を構成する。

PCN は、安全システムから出力される許可状態を A：Authority に関係する状態として取得できる。

重要な安全許可は、Target State Entry に対する独立した必要制約として扱う。

安全システムは安全機能と安全許可を担い、PCN はその許可状態を今回の Target State Entry に関係する状態として他の関連状態とともに判定する。

機械安全に関係する制御システムの設計原則については ISO 13849-1 を参照できる。[4]

### 2.4 アラーム管理・故障診断

アラーム管理や故障診断は、異常情報、故障状態、原因、応答、履歴などを扱う。

PCN は、それらのアラームや診断結果を、今回の Target State Entry に関係する状態として利用できる。

同じ通信異常であっても、Target State Entry によって工程上の意味は異なる。

例えば、

- 画像認識結果の有効性に影響する場合
- 上位システム許可に影響する場合
- 後続の結果送信や書戻しに影響する場合

などである。

PCN は、異常情報を Target State Entry に対応付け、その状態遷移における役割と判定特性を整理する。

---

## 3. MES / WCS・AI との関係

### 3.1 MES / WCS

MES、WCS、群制御システムは、タスク、資源、経路、ステーション、スケジューリング、権限、実行状態などを管理する。

例えば、

```text
MES：タスク生成済み
WCS：タスク記録あり
設備：オンライン
車両：オンライン
```

という状態が存在していても、今回の Target State Entry ではさらに、

- タスク状態を今回の判定に使用できるか。
- 必要な許可が成立しているか。
- 資源ロック状態はどうなっているか。
- 経路状態は今回の実行に使用できるか。
- 下流ステーションは受入可能か。
- 関連状態は現在有効か。
- Target State へ進入した後の Execution Chain を継続できるか。

などを確認する必要がある場合がある。

MES / WCS は、タスク、資源、スケジューリング、生産協調などの機能を担う。

PCN は、その中の重要な Target State Entry に対して、複数システムに分散した関連状態を一つの状態遷移前判定として整理する。

製造オペレーションと企業システム・制御システム間の統合境界については、ISA-95 / IEC 62264 シリーズを参照できる。[5]

### 3.2 AI / データ分析

AI やデータ分析は、PCN Trace を用いた後続分析に利用できる。

代表的な用途には、次のようなものがある。

- 履歴比較
- パターン抽出
- 反復問題の検出
- 改善候補の整理
- エンジニアリング変更前後の比較
- レポート作成支援

PCN は Target State Entry に対する判定と制御を行い、AI は PCN Trace を用いた比較・分析・改善検討を支援する。

この役割分担により、オンラインの状態遷移前判定と、蓄積履歴を利用した改善分析を異なる工程位置で扱うことができる。

---

## 4. TPCA / PCN の工程上の位置付け

TPCA / PCN で扱う個々の状態や制御要素は、既存の産業オートメーションでも広く使用されている。

例えば、

- Condition
- Authority
- Ready
- 状態遷移
- Interlock
- 安全許可
- アラーム
- タイムアウト
- 待機
- 再試行
- 縮退実行

などである。

TPCA / PCN は、これらの状態や制御要素を、明確な Target State Entry を中心として一つの工程構造に対応付ける。

```text
Current State
    ↓
Target State Entry / PCN
    ↓
Target State

PCN 内部：
関連状態
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

既存の各システムと PCN の主な役割分担を次に示す。

| 既存の対象 | 主な役割 | PCN との関係 |
|---|---|---|
| PLC / 状態機械 / SFC | 状態管理、シーケンス制御、動作実行 | Target State Entry に必要な状態や遷移ロジックを提供し、PCN の判定結果を利用できる |
| Interlock / Handshake | 動作条件、設備間条件 | Target State Entry に関係する状態や既存制約として利用する |
| 安全システム | 安全機能、安全許可、危険動作の制限 | 重要な A に関係する状態を提供する |
| アラーム管理 / 故障診断 | 異常管理、故障状態・原因の分析 | アラームや診断結果を関連状態として利用できる |
| MES / WCS | タスク、資源、スケジューリング、生産協調 | 上位状態や許可、資源情報を提供し、必要に応じて PCN の判定・履歴情報を利用する |
| AI / データ分析 | 履歴分析、パターン抽出、改善支援 | PCN Trace を用いた分析や改善検討を支援する |
| TPCA / PCN | Target State Entry に対する構造化判定、Arbitration、Multipath Control、PCN Trace | 複数の関連状態を Target State Entry に対応付け、状態遷移前判定・制御・履歴を一つの工程単位として構成する |

この関係により、既存の設備制御、安全制御、タスク管理、スケジューリング、診断、分析はそれぞれの役割を継続しながら、Target State Entry に関係する状態を共通の工程位置へ接続できる。

---

## まとめ

産業オートメーションには、状態機械、SFC、Interlock、安全制御、アラーム管理、故障診断、MES / WCS、FMEA、STPA、RCA、Process Mining など、多数の成熟した技術が存在する。

TPCA / PCN は、それらが提供する状態、許可、診断結果、タスク情報、資源情報などを、明確な Target State Entry に対応付ける。

そのうえで、

```text
関連状態
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

という一連の工程関係を構成する。

この構造によって、一回の Target State Entry を、

> **設計、判定、制御、記録、追跡の共通単位**

として扱うことができる。

既存技術は、それぞれの設備制御、安全、タスク管理、診断、分析などを担い、PCN はそれらの状態や結果を Target State Entry 単位の状態遷移前判定へ接続する。

---

## 参考文献と外部資料

本稿では、比較対象となる既存技術の代表的な背景資料として、以下を参照する。

1. **MIT Partnership for Systems Approaches to Safety and Security — Books and Handbooks**  
   *STPA Handbook* および STPA / CAST 関連資料への公開入口。  
   https://psas.scripts.mit.edu/home/books-and-handbooks/

2. **Wil van der Aalst — *Process Mining: Data Science in Action*, 2nd ed., Springer, 2016**  
   Process Mining に関する代表的な体系書。  
   DOI: 10.1007/978-3-662-49851-4  
   https://link.springer.com/book/10.1007/978-3-662-49851-4

3. **PLCopen — IEC 61131-3**  
   IEC 61131-3 の PLC プログラミング言語体系、および SFC の位置付けに関する公開資料。  
   https://www.plcopen.org/standards/logic/iec-61131-3/

4. **ISO 13849-1:2023 — Safety of machinery — Safety-related parts of control systems**  
   機械安全に関係する制御システムの設計原則を示す ISO 公式ページ。  
   https://www.iso.org/standard/73481.html

5. **ISA — ISA-95 Series of Standards: Enterprise-Control System Integration**  
   ISA-95 / IEC 62264 の階層、対象、企業システムと製造制御システム間の情報統合に関する ISA 公式ページ。  
   https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard

---

## 文書情報

題目：TPCA / PCN と既存の産業オートメーション技術・エンジニアリング手法との関係  
文書種別：技術ノート  
バージョン：Public Note Version 1.3  
初回公開日：2026-07-04  
最終更新日：2026-09-08  
著者：全野南政 / Nansei Zenno  
現在の URL：https://zennns.com/jp/notes/tpca-existing-theories/

---

本稿は、TPCA / PCN 状態遷移前制御体系の公開説明資料である。
