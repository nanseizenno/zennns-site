---
title: "なぜ OEE の後に PCN が必要なのか？"
summary: "OEE が運転実績や損失を把握するのに対し、PCN は明確な Target State Entry における判定・制御・履歴を扱う。両者を関連付けることで、損失が発生した時間帯と、その時点の状態遷移判定を確認できる。"
description: "OEE と PCN が扱う対象の違い、および OEE / 生産実績データと PCN Trace を関連付けて改善へつなげる考え方を説明する。"
date: 2026-07-04
lastmod: 2026-09-08
author: "全野南政 / Nansei Zenno"
document_type: "技術ノート"
version: "Public Note Version 1.4"
citation_url: "https://zennns.com/jp/notes/why-oee-pcn/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## なぜ OEE の後に PCN が必要なのか？

OEE、設備稼働データ、アラーム履歴、保全データは、製造現場の運転実績や損失を把握するための重要な情報である。

OEE を用いることで、例えば次の内容を確認できる。

- 設備がどの程度稼働していたか。
- 停止や待機がどの程度継続したか。
- 性能が低下しているか。
- 不良が増加しているか。
- どの時間帯や工程で損失が発生しているか。
- 改善後に運転実績がどのように変化したか。

一方、複雑な自動化システムでは、設備に明確な故障がなくても次の工程や動作へ進まない場合がある。

例えば、

- ロボットは Ready だが、ピックアップ動作が開始されない。
- タスクは存在するが、実行へ進まない。
- 上流工程は完了しているが、下流が受け入れられない。
- MES、WCS、PLC、ロボットに状態記録がある状態で Waiting が継続している。
- 個々の設備に明確なアラームがない状態で、特定の工程へ進めない。

このような場合に必要になるのは、

> **その時間帯に、どの Target State Entry で、どの状態が判定に使用され、どの判定結果と制御結果が形成されていたか。**

という情報である。

PCN は、明確な Target State Entry を対象として、その入口に必要な状態遷移前判定、制御、履歴を構成する。

基本概念については、以下を参照。

- [Concepts｜基本概念](/jp/concepts/)
- [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)
- [なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)
- [なぜ PCN Trace は新しいエンジニアリングデータなのか？](/jp/notes/why-pcn-trace-is-engineering-data/)

---

## 1. OEE と PCN が扱う対象

OEE は、主として設備や生産プロセスの運転実績と損失を把握するために使用される。

代表的な対象には、次のようなものがある。

- 時間稼働率
- 性能稼働率
- 良品率
- 停止ロス
- 性能ロス
- 品質ロス
- サイクルタイム
- 生産数量

OEE を用いることで、

> **どこで、どの程度の損失が発生しているか**

を確認できる。

PCN は、1回の明確な Target State Entry を対象とする。

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

したがって、両者の役割は次のように整理できる。

> **OEE は、運転実績と損失を把握する。**

> **PCN は、Target State Entry における状態遷移前判定と制御を行い、その結果を PCN Trace として記録する。**

---

## 2. なぜ複雑な自動化では Target State Entry の情報が必要なのか

複雑な設備や自動化ラインでは、「運転」と「停止」の間に多数の Target State Entry が存在する。

例えば、

```text
待機 → 自動運転
投入完了 → 加工
加工完了 → 検査
検査完了 → 排出
認識完了 → ピックアップ
配置完了 → 圧入
タスク生成 → タスク実行
AGV 到着 → ステーション受入
```

などである。

各 Target State Entry では、複数の状態が同時に関係する。

例えば、ロボットが Ready であっても、

- ワーク認識結果が期限切れである。
- 安全許可が成立していない。
- 上位システムからの許可待ちである。
- 下流受入状態が成立していない。
- 必要な経路や機構が使用できない。
- 関連状態が更新されていない。
- 判定に必要な信号やマッピングが不足している。

といった理由で、Target State へ進入できない場合がある。

OEE や設備データからは、待機時間や停止時間を把握できる。

PCN Trace を確認することで、その時間帯に、

- どの Target State Entry が判定対象だったか。
- どの関連状態が使用されたか。
- どの CAE-SDB Result が形成されたか。
- どの Multipath Control が選択されたか。
- 実行結果がどうなったか。

を追跡できる。

これにより、運転実績上の損失と、Target State Entry 単位の判定履歴を関連付けて確認できる。

---

## 3. OEE と PCN Trace をどのように関連付けるか

OEE / 生産実績データと PCN Trace は、異なる粒度の情報を扱う。

| 項目 | OEE / 設備・生産データ | PCN / PCN Trace |
|---|---|---|
| 主な対象 | 運転実績、生産結果、損失 | 1回の明確な Target State Entry |
| 主な確認内容 | 稼働、性能、品質、停止、待機 | 状態、判定結果、制御結果、実行結果 |
| 時間の扱い | 一定期間の実績を集計・比較 | Target State Entry ごとの時間位置を記録 |
| 主な用途 | 損失の把握、実績比較、改善効果確認 | 状態遷移判定、制御履歴、原因候補の確認 |
| 主な改善対象 | 設備、工程、生産プロセス | 状態遷移条件、許可、Execution Chain、制御経路 |

例えば、OEE やその他の生産実績データから、

> ある設備で長時間の待機が発生していた。

ことが確認されたとする。

対応する PCN Trace に、次のような記録がある場合を考える。

```text
PCN：PCN-07
Current State：検査完了
Target State：ワーク排出
CAE-SDB Result：E-D
判定内容：下流状態が未更新
Multipath Control：Wait
実行結果：下流状態更新後に進入
```

この場合、

```text
OEE / 生産実績
→ 待機による損失を確認
```

と、

```text
PCN Trace
→ 下流状態の未更新に関係する E-D が発生
→ Wait が選択
```

を同じ時間帯の情報として関連付けることができる。

分析の流れは、次のように整理できる。

```text
OEE / 生産実績データ
        ↓
損失発生区間を確認
        ↓
該当時間帯の Target State Entry を確認
        ↓
PCN Trace
        ↓
CAE-SDB Result / Multipath Control
        ↓
状態遷移条件や制御経路を確認
```

---

## 4. OEE と PCN を組み合わせることで何を改善できるか

OEE と PCN Trace を関連付けることで、損失の発生位置だけでなく、その時間帯に繰り返し発生している状態遷移判定を確認できる。

例えば、

- 特定の Target State Entry で E-D が繰り返し発生している。
- 特定の A に関係する待機が長期化している。
- 同じ PCN で Wait が高頻度に選択されている。
- 下流受入状態の未更新が複数回発生している。
- エンジニアリング変更後に特定の CAE-SDB Result が減少した。
- 制御経路変更後に待機時間が短縮した。

といった関係を確認できる。

この場合、改善対象は単に「設備停止時間」だけではなく、

- 状態更新方法
- 許可条件
- Execution Chain
- 状態遷移条件
- 制御境界
- Multipath Control
- システム間の状態連携

などへ具体化できる。

したがって、

> **OEE が損失の大きさや発生区間を示し、PCN Trace がその時間帯の Target State Entry における判定・制御履歴を示す。**

という補完関係を構成できる。

OEE や生産実績データで改善対象となる時間帯や工程を把握し、その区間に対応する PCN Trace を確認することで、状態遷移条件や制御経路まで掘り下げた改善につなげることができる。

---

## まとめ

OEE と PCN は、製造システムの異なる対象を扱う。

> **OEE は、運転実績と損失を把握する。**

> **PCN は、明確な Target State Entry に対する状態遷移前判定と制御を行い、その結果を PCN Trace として記録する。**

両者を関連付けることで、

```text
OEE / 生産実績
→ どこで損失が発生したか
```

と、

```text
PCN Trace
→ その時間帯に
   どの Target State Entry で
   どのような判定と制御が行われていたか
```

を同じ改善文脈で確認できる。

その結果、運転実績上の損失から、状態遷移条件、許可、Execution Chain、制御経路などの具体的なエンジニアリング改善対象へ展開できる。

---

## 関連技術ノート

- [なぜ PCN Trace は新しいエンジニアリングデータなのか？](/jp/notes/why-pcn-trace-is-engineering-data/)
- [なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)
- [複数の PCN はどのように状態遷移前制御ネットワークを形成するのか？](/jp/notes/pcn-network-structure/)
- [TPCA / PCN の適用シナリオ分析](/jp/notes/tpca-pcn-applicable-scenarios/)

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

題目：なぜ OEE の後に PCN が必要なのか？  
文書種別：技術ノート  
バージョン：Public Note Version 1.4  
初回公開日：2026-07-04  
最終更新日：2026-09-08  
著者：全野南政 / Nansei Zenno  
現在の URL：https://zennns.com/jp/notes/why-oee-pcn/

---

本稿は、TPCA / PCN 状態遷移前制御体系の公開説明資料である。
