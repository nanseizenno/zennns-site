---
title: "なぜ OEE の後に PCN が必要なのか？"
summary: "OEE、設備データ、PCN の関係を説明する。OEE は運転実績や損失の把握に用いられ、PCN は明確な Target State Entry を対象として、一回の状態遷移に必要な状態を判定し、Arbitration、Multipath Control、PCN Trace へ展開する。"
description: "OEE、設備運転データ、複雑な自動化システムの状態遷移、多システム連携の観点から、OEE と PCN の役割を整理する。運転実績や損失に関するデータに加えて、明確な Target State Entry を対象とする構造化された状態遷移前判定、Arbitration、Multipath Control、PCN Trace をどのように利用できるかを説明する。"
date: 2026-07-04
lastmod: 2026-08-22
author: "全野南政 / Nansei Zenno"
document_type: "技術ノート"
version: "Public Note Version 1.3"
citation_url: "https://zennns.com/jp/notes/why-oee-pcn/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## なぜ OEE の後に PCN が必要なのか？

基本概念については、以下を参照。

- [中核概念](/jp/concepts/)
- [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)
- [なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)
- [なぜ状態遷移条件を明示する必要があるのか？](/jp/notes/explicit-state-transition-conditions/)
- [なぜ PCN Trace は新しいエンジニアリングデータなのか？](/jp/notes/why-pcn-trace-is-engineering-data/)
- [TPCA の状態遷移単方向性 ― なぜ実システムでは過去の状態インスタンスへ戻らないのか？](/jp/notes/tpca-unidirectional-state-transition/)

OEE、設備稼働データ、アラーム履歴、保全データは、製造現場のデジタル化を支える基本的な情報である。

日本プラントメンテナンス協会（JIPM）は、OEE を生産設備の効率改善に用いる代表的な指標として説明しており、設備効率を把握し、損失を明確にして改善につなげるために利用されている。[1] ISO 22400 シリーズでは、製造オペレーション管理に用いる KPI の概念、定義、構成、利用方法などが体系化されている。[2]

これらの情報から、例えば次の内容を確認できる。

- 設備が運転していたか。
- 停止がどの程度継続したか。
- 性能が低下しているか。
- 不良が増加しているか。
- 生産損失がどこで発生しているか。
- 改善後に運転実績がどのように変化したか。

一方、複雑な自動化システムでは、設備に明確な故障がない状態でも、次の工程や動作へ進まない場合がある。

例えば、

- ロボットは Ready であるが、ピックアップ動作が開始されない。
- タスクは存在するが、実行経路へ進まない。
- 上流工程は完了しているが、下流が受け入れられない。
- MES、WCS、PLC、ロボットに状態記録がある一方で、Waiting が継続している。
- 個々の設備に明確なアラームがない状態で、特定の工程へ進めない。

この場合に確認する対象は、

> **一回の明確な Target State Entry に対して、状態遷移に必要な判定がどのような結果になっているか。**

という問題である。

PCN は、この状態遷移入口を対象とする。

---

## 1. OEE は運転実績を把握し、PCN は Target State Entry を判定する

OEE は、主として生産設備、生産ユニット、生産プロセスの運転実績と損失を把握するために使用される。

代表的な項目には、次のようなものがある。

- 時間稼働率
- 性能稼働率
- 良品率
- 停止ロス
- 性能ロス
- 品質ロス
- サイクルタイムの変化
- 生産数量の変化

JIPM の公開資料でも、OEE は設備総合効率を把握し、各種損失を明確にして改善へ結び付ける指標として説明されている。[1]

OEE を用いることで、例えば次の内容を確認できる。

> 運転効率はどの程度か。

> 損失はどこで発生しているか。

> どの時間帯で性能が低下しているか。

> 改善後に生産実績がどのように変化したか。

PCN が対象とするのは、明確な Target State Entry である。

```text
Current State → PCN → Target State
```

PCN では、今回の Target State Entry に対して、次の内容を確認する。

- Current State は何か。
- Target State は何か。
- Target State へ入るために必要な C の状態は何か。
- Target State への進入に必要な A の状態は何か。
- Target State へ入った後の E に関係する状態は何か。
- 各状態に対して、どの S / D / B 判定が必要か。
- 一つまたは複数の CAE-SDB Result を Arbitration でどのように処理するか。
- 今回の Target State Entry に対して、どの Multipath Control を形成するか。
- 判定と実行の結果をどのように PCN Trace として記録するか。

整理すると、両者は次の異なる対象を扱う。

> **OEE は、運転実績と損失を把握する。**

> **PCN は、一回の明確な Target State Entry に必要な状態を判定し、その結果を制御へつなげる。**

---

## 2. 複雑な自動化システムでは状態遷移入口が多数存在する

複雑な設備や自動化ラインでは、「運転」と「停止」の間にも多数の工程状態が存在する。

一台の設備内でも、例えば次のような状態遷移がある。

```text
待機 → 自動運転
原点復帰完了 → 自動運転
投入完了 → 加工
加工完了 → 検査
検査完了 → 排出
異常停止 → 復旧後状態
段取り替え完了 → 量産運転
```

複数設備が連携するシステムでは、さらに次のような状態遷移が存在する。

```text
認識完了 → ピックアップ
配置完了 → 圧入
検査完了 → 分流
包装完了 → パレタイズ
パレタイズ完了 → 入庫引渡し
タスク生成 → タスク割当
AGV 到着 → ステーション引渡し
手動確認完了 → 自動運転再開
```

これらは、それぞれ明確な Target State Entry として設定できる。

「復帰」「再開」「再投入」などの名称は、現場で使用される工程状態や制御経路の名称としてそのまま使用できる。

実際の運転履歴では、同じ状態内容が再び現れた場合も、その時点で新しい状態インスタンスが形成される。

状態遷移は、実運転上の時間位置に沿って次のように継続する。

```text
Current State → New Target State
```

例えば、ロボットが Ready であっても、今回の Target State Entry に関係する状態として次のような状況が考えられる。

- ワーク認識結果が有効時間を超えている。
- 安全エリア許可が成立していない。
- 上位システムからの許可待ちである。
- 下流の配置位置が受入待ちである。
- 戻り経路が使用できない。
- 関連状態が切替中である。
- 判定に必要な信号やマッピング関係が定義されていない。

これらの状態は、Current State から Target State へ進む際の C / A / E および S / D / B の判定対象となる。

設備の運転実績からは停止時間や待機時間を把握できる。

PCN Trace を組み合わせることで、その時間帯にどの Target State Entry が判定対象となり、どの状態が遷移に影響していたかを確認できる。

---

## 3. PCN は一回の状態遷移を判定可能な構造として整理する

PCN は Target State Entry の前に配置する。

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

C / A / E は、今回の Target State Entry に関係する状態の機能役割を表す状態変数領域である。

- C：Condition
- A：Authority
- E：Execution Chain

S / D / B は、これらの状態に対する判定性質である。

- S：Structure
- D：Dynamics
- B：Boundary

S / D / B の判定結果を C / A / E の状態変数領域と組み合わせ、CAE-SDB Result を形成する。

一回の Target State Entry について複数の CAE-SDB Result が形成された場合は、Arbitration で制御上の優先関係を処理する。

その結果に基づいて Multipath Control を形成し、今回の判定と実行結果を PCN Trace として記録する。

PCN は、このように一回の Target State Entry に関係する、

> **入力状態、状態マッピング、判定、Arbitration、Multipath Control、PCN Trace**

を一つの工程関係として整理する。

---

## 4. OEE と PCN は異なる工程事実を記録する

両者の対象は次のように整理できる。

| 項目 | OEE / 設備・生産データ | PCN |
|---|---|---|
| 主な対象 | 運転実績、生産結果、損失 | 一回の明確な Target State Entry |
| 主な確認内容 | 稼働状況、性能、品質、損失 | 今回の Target State Entry に関する状態、判定、制御結果 |
| 主なデータ | 稼働、性能、品質、停止、サイクルタイム、生産数量 | Current State、Target State、時間情報 T、CAE-SDB Result、Arbitration Result、Multipath Control、PCN Trace |
| 時間の扱い | 一定期間の運転実績を集計・比較 | 一回の Target State Entry に対応する状態と判定の時間位置を記録 |
| 主な用途 | 損失の把握、実績比較、改善効果の確認 | 状態遷移判定、制御経路選択、履歴追跡 |
| 主な改善対象 | 設備、工程、生産プロセス、運転損失 | 状態遷移条件、許可、実行チェーン、制御境界、制御経路 |

例えば、OEE やその他の生産データから、

> ある設備で、一つのシフト中に長時間の待機が発生していた。

ことが確認されたとする。

対応する PCN Trace には、例えば次の内容が記録される。

```text
PCN：PCN-07

Current State：検査完了

Target State：ワーク排出

時間情報：T₂

CAE-SDB Result：E-D

判定内容：下流状態が未更新

Arbitration Result：待機経路を選択

Multipath Control：待機

実行結果：下流状態更新後、新しい Target State Entry に対する判定へ移行
```

この場合、

```text
待機による生産損失
```

と、

```text
Target State Entry で形成された判定結果
```

を関連付けて確認できる。

OEE と PCN Trace を組み合わせることで、運転実績上の損失と、それに対応する状態遷移判定履歴を同じ時間帯で確認できる。

---

## 5. 単体の複雑設備にも PCN を設定できる

PCN の適用対象は、多設備システムや MES / WCS に限られない。

自動化設備内部に明確な Target State Entry が存在する場合、その入口を PCN の対象として設定できる。

例えば、

```text
待機 → 自動運転
```

という状態遷移を考える。

自動運転へ進む前には、例えば次の状態を使用する。

- 原点復帰が完了しているか。
- ワークが所定位置にあるか。
- 治具が所定状態であるか。
- 必要な安全許可が成立しているか。
- 工程パラメータが今回の運転に使用できる状態か。
- 下流が受入可能か。
- 異常処理または復旧処理が完了しているか。
- 結果書戻し経路が利用可能か。

これらの状態は、例えば次のシステムに分散している。

- PLC
- 安全 PLC
- ロボットコントローラ
- 画像認識システム
- HMI
- 上位システム
- Interlock
- シーケンス制御ロジック

PCN では、

```text
待機 → 自動運転
```

を一回の明確な Target State Entry として設定し、その入口に必要な状態を C / A / E へマッピングして S / D / B 判定を行う。

HMI では、例えば次の情報を Target State Entry に関連付けて表示できる。

- Current State
- Target State
- 時間情報 T
- CAE-SDB Result
- Arbitration Result
- Multipath Control
- Trace ID

復旧や再投入の場合も、その時点の Current State から新しい Target State への状態遷移として扱う。

Target State の状態内容が過去の状態と同一であっても、その時点で新しい状態インスタンスが形成される。

この履歴を PCN Trace として保持することで、設備の調整、保全、問題分析、同種設備への展開などに利用できる。

---

## 6. 多システム連携では Target State Entry に関係する状態が分散する

MES、WCS、PLC、ロボット、AGV、画像認識、安全システム、手動確認などが一つの生産プロセスに関係する場合、状態遷移に必要な状態は複数のシステムに分散する。

例えば、次のような一連の処理がある。

```text
MES：タスク生成
→ WCS：タスク割当
→ 搬送主体：実行開始
→ 経路資源：通行
→ AGV：到着
→ ステーション：引渡し
→ 下流：受入
→ 結果書戻し
```

各 Target State Entry では、それぞれに関係する状態を取得する。

例えば、

- MES にタスクが存在する。
- WCS にタスク状態が存在する。
- AGV がオンラインである。
- PLC が正常運転状態である。
- ステーションが Ready である。

という状態が同時に存在している場合でも、今回の Target State Entry に関係する C / A / E を個別に設定し、必要な S / D / B 判定を行う。

PCN は、このように分散した状態を一回の Target State Entry に対応付ける。

複数の PCN を状態遷移関係、許可、資源、実行チェーンなどの依存関係に基づいて接続すると、PCN Network を形成できる。

関連説明については、以下を参照。

[複数の PCN はどのように状態遷移前制御ネットワークを形成するのか？](/jp/notes/pcn-network-structure/)

---

## 7. OEE と PCN は異なる改善対象を扱う

OEE では、例えば次の内容を確認できる。

- どの生産区間で効率が低下したか。
- 損失がどの程度継続したか。
- 時間稼働率、性能稼働率、良品率がどのように変化したか。
- 改善前後で運転実績がどのように変化したか。

PCN Trace では、例えば次の内容を確認できる。

- どの Target State Entry で判定が行われたか。
- C / A / E のどの状態変数領域に関係する結果が形成されたか。
- S / D / B のどの判定性質によって CAE-SDB Result が形成されたか。
- Arbitration でどの制御上の優先関係が処理されたか。
- どの Multipath Control が選択されたか。
- 同じ PCN で同種の CAE-SDB Result が繰り返し発生しているか。

両者を関連付ける場合、例えば次のような分析関係を構成できる。

```text
OEE / 生産実績データ
        ↓
損失発生区間を確認
        ↓
該当時間帯の Target State Entry を抽出
        ↓
PCN Trace
        ↓
CAE-SDB Result
        ↓
Arbitration Result / Multipath Control
        ↓
状態遷移条件・制御経路を確認
```

OEE では期間単位の運転実績を比較できる。

PCN Trace では、その期間内に実際に発生した個別の Target State Entry と状態インスタンスを区別して記録できる。

同じ状態タイプや同じ状態内容が複数回現れた場合も、それぞれ異なる時間情報 T と PCN Trace を持つ。

この構造により、運転実績と個別の状態遷移判定履歴を関連付けて改善対象を確認できる。

---

## 8. PCN により状態遷移判定をデータとして扱える

PCN を用いることで、プログラム、インターフェース、許可、設備間連携、運転手順などに分散している状態遷移判定を、明確な Target State Entry に対応する形で記録できる。

一つの Target State Entry について、例えば次の情報を関連付ける。

```text
Current State
Target State
主要な入力状態
時間情報 T
C / A / E Mapping
S / D / B Evaluation
CAE-SDB Result
Arbitration Result
Multipath Control
実行結果
PCN Trace
```

これにより、一回の状態遷移判定は次の観点から扱える。

- 定義
- 判定
- 記録
- 比較
- 追跡
- 振り返り

実際の導入では、状態遷移上の影響や現場での分析必要性に応じて、PCN を設定する Target State Entry を選定できる。

代表的な対象には、次のようなものがある。

- 重要設備間の連携入口
- Waiting が頻発する入口
- 上下流の受渡し入口
- 資源ロックに関係する入口
- 重要な許可を必要とする入口
- 自動 / 手動の切替入口
- 異常処理、復旧、再投入に関係する入口
- 現場で複数システムの状態確認が必要となる入口

---

## まとめ

OEE と PCN は、製造システムの異なる工程対象を扱う。

> **OEE は、運転実績と損失を把握する。**

> **PCN は、明確な Target State Entry に対する状態遷移判定を行い、その結果を Multipath Control と PCN Trace へつなげる。**

生産実績が低下した場合、OEE やその他の生産データから損失の発生区間を確認できる。

さらに、その区間で発生した PCN Trace を確認することで、

- どの Target State Entry が判定対象となったか。
- どの C / A / E 状態を使用したか。
- どの S / D / B 判定を行ったか。
- どの CAE-SDB Result が形成されたか。
- Arbitration でどの制御上の優先関係が処理されたか。
- どの Multipath Control が選択されたか。
- その後、どのような実行結果となったか。

を確認できる。

PCN の基本的な処理関係は次の通りである。

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

PCN Trace には、実際の状態遷移に対応する時間情報 T も保持される。

そのため、後続の運転で過去と同じ状態内容が再び現れた場合も、新しい状態インスタンスとして区別し、それぞれの Target State Entry に対する判定履歴を記録できる。

OEE と PCN を組み合わせることで、

> **運転実績上、どこで損失が発生しているか。**

という情報と、

> **その時間帯に、どの Target State Entry でどのような状態遷移判定が行われていたか。**

という情報を関連付けることができる。

---

## 参考文献と外部資料

以下の資料は、OEE および製造オペレーション KPI の既存の工程上の位置付けを確認するための参考資料である。

1. **Japan Institute of Plant Maintenance（JIPM）— TPM / Overall Equipment Efficiency（OEE）**  
   JIPM は OEE を、設備総合効率を把握し、設備に関係する損失を明確にして改善に活用する代表的な指標として説明している。  
   https://jipmglobal.com/tpm/about_us_en

2. **ISO 22400-1:2014 — Automation systems and integration — Key performance indicators (KPIs) for manufacturing operations management — Part 1: Overview, concepts and terminology**  
   製造オペレーション管理で用いる KPI の概要、概念、用語を整理した規格である。  
   https://www.iso.org/standard/56847.html

---

## 文書情報

題目："なぜ OEE の後に PCN が必要なのか？"  
文書種別：技術ノート  
バージョン：Public Note Version 1.3  
初回公開日：2026-07-04  
最終更新日：2026-08-22  
著者：全野南政 / Nansei Zenno  
現在の URL：https://zennns.com/jp/notes/why-oee-pcn/

---

本稿は、TPCA / PCN 状態遷移前制御体系の公開説明資料である。
