---
title: "なぜ Ready だけでは不十分なのか？"
summary: "設備 Ready、Robot Ready、Downstream Ready などは局所的な運転可能状態を示すものであり、それだけではシステムが Target State へ入れることを意味しない理由を説明する。"
description: "自動化実行ユニットが次の状態へ入る前のエンジニアリング課題を対象として、Ready が局所状態の一つであること、および一回の状態遷移では Current State、Target State、必要な Condition、Authority、Execution Chain と関連状態の有効性を組み合わせて判定する必要があることを説明する。"
date: 2026-07-04
lastmod: 2026-08-20
author: "全野南政 / Nansei Zenno"
document_type: "エンジニアリング課題"
question_type: "ユニット・現場実行問題"
version: "Public Question Version 1.2"
citation_title: "なぜ Ready だけでは不十分なのか？"
citation_url: "https://zennns.com/jp/questions/why-ready-is-not-enough/"
draft: false
ShowReadingTime: false
ShowToc: true
TocOpen: true
---

自動化ラインがピックアップ動作の直前で停止している。

ロボットは Ready を表示し、PLC にも明確な異常はないが、ピックアップ動作が開始されない。

確認を進めると、例えば次のような状態が見つかる場合がある。

- ワーク条件がまだ成立していない。
- 必要な許可が成立していない。
- 下流が現在受入できない。
- 関連状態は正常値を示しているが、長時間更新されていない。

このような場合、現場では次の疑問が生じる。

> **設備は Ready なのに、なぜ次の段階へ進まないのか？**

Ready 自体が誤っているとは限らない。

> **Ready は、設備、機構、モジュールなどの局所的な運転可能状態を示す。今回の Target State Entry に必要な状態遷移判定全体を示すものではない。**

---

## 1. Ready は主として局所的な運転可能状態を示す

自動化システムにおいて、Ready は重要な運転状態である。

Ready は、システムや設備の設計によって、例えば次のような状態を表す。

- 設備が自動モードにある。
- サーボが運転可能な状態にある。
- 主要なアラームが発生していない。
- プログラムが実行可能な状態にある。
- 機構が待機位置にある。
- 相手機器から Ready が返されている。
- 通信対象がオンラインである。

これらは、

> **対象となる設備、機構、モジュールが現在どのような運転状態にあるか。**

を確認するための情報である。

一方、実際の状態遷移では、複数の状態が同じ Target State Entry に関係する場合がある。

例えば Robot Ready が成立していても、今回の Target State Entry に対しては、次の状態を別途確認する必要がある場合がある。

- ワーク条件が成立しているか。
- 必要な許可が成立しているか。
- 対象エリアへの進入が許可されているか。
- Target State へ入った後の実行チェーンが継続できるか。
- 今回の判定に使用する関連状態が現在も有効か。

したがって、Ready は Target State Entry に関係する入力状態の一つとして扱う。

---

## 2. Ready は Target State と組み合わせて解釈する

同じ Ready 信号でも、Target State が異なれば、今回の状態遷移における役割や関連状態は変わる場合がある。

例えば、

```text
Robot Ready = TRUE
```

であっても、システムが次に入ろうとしている状態が「ピックアップ段階」である場合と、「原点復帰」「異常時退避」などの段階である場合では、Target State Entry に必要な判定内容は同一とは限らない。

そのため、最初に確認する対象は Ready の値だけではない。

```text
Current State
→ Target State
```

を明確にし、

> **今回、どの Target State Entry に対して判定を行うのか。**

を定める必要がある。

Target State が変われば、今回の状態遷移に関係する Condition、Authority、Execution Chain の状態も変わる場合がある。

Ready 信号は制御や表示を簡潔にする上で有用であるが、複数設備や複数システムが関係する状態遷移では、Target State Entry に必要なすべての状態関係を単一の Ready だけで表すことはできない。

---

## 3. Target State Entry では複数の状態変数領域を確認する

一回の Target State Entry では、設備自身の Ready に加えて、今回の状態遷移に関係する複数の状態を確認する。

TPCA / PCN では、これらの状態を C / A / E の状態変数領域に整理する。

### C：Condition

C は、Target State へ入るために必要な事実条件に関係する状態変数領域である。

例えば、

- ワークが存在するか。
- 対象が正しいか。
- 必要なデータを取得しているか。
- 前段階が完了しているか。

などが該当する。

### A：Authority

A は、Target State への進入を許可する状態に関係する状態変数領域である。

例えば、

- 安全許可
- エリア許可
- 上位システム許可
- 資源に関する許可
- 相手機器からの許可

などが該当する。

重要な A は、Target State Entry に対する独立した必要制約として扱う。

### E：Execution Chain

E は、Target State へ入った後の実行チェーンに関係する状態変数領域である。

例えば、

- 目標位置が受入可能か。
- 後続設備が実行を継続できるか。
- 今回の実行チェーンとして定義された正常経路、代替経路、回流経路などの状態はどうか。
- 実行結果を後続システムへ送信または書き戻せるか。

などが該当する。

したがって、Ready は今回の Target State Entry に関係する状態の一つであり、PCN は Ready を含む複数ソース状態を Target State Entry に対応付けて整理する。

---

## 4. 状態値が正常でも、今回の判定に使用できるとは限らない

複雑な自動化システムでは、状態値そのものに明確な異常がなくても、その状態を今回の Target State Entry の判定に使用できない場合がある。

例えば、

- 検査結果が長時間更新されていない。
- 下流 Ready が、下流状態の変化後も以前の値を保持している。
- 許可が、動作開始前に取り消されている。
- 上流と下流で状態更新時刻が大きく異なっている。
- システムが状態切替中である。

このような場合、

```text
Ready = TRUE
```

という状態値だけでは、今回の Target State Entry に対する判定根拠として十分かどうかを確定できない。

Target State Entry では、関連状態が今回の判定時点でも有効であるかを確認する必要がある。

TPCA / PCN では、関連状態に対して必要な S / D / B Evaluation を行い、その判定結果を CAE-SDB Result として整理する。

特に、状態のタイムアウト、未更新、取消、非同期、競合、切替中などの時間的・運転時の有効性は、D：Dynamics / 動的時系列有効性の判定対象となる。

---

## 5. Ready を Target State Entry の状態遷移判定に組み込む

Ready、Interlock、Handshake、Alarm は、いずれも自動化システムで使用される重要な状態・制御情報である。

複数の設備やシステムが一回の状態遷移に関係する場合、PCN はこれらの情報を、今回の Target State Entry に関係する複数ソース状態として扱う。

基本的な処理関係は次の通りである。

```text
Current State
→ Target State
→ PCN
→ 複数ソース状態
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

この構成により、例えば次の事項を同じ Target State Entry の中で確認できる。

- Current State は何か。
- Target State は何か。
- Ready を含め、どの状態が今回の状態遷移に関係するか。
- 各状態は C / A / E のどの状態変数領域に属するか。
- どの S / D / B Evaluation が必要か。
- どの CAE-SDB Result が形成されたか。
- Arbitration の結果、今回の Target State Entry に対してどの Multipath Control を形成するか。
- 判定と制御結果を PCN Trace にどのように記録するか。

詳細な用語と構造については、以下を参照。

[Concepts｜中核概念](/jp/concepts/)

自動化実行ユニットでの適用例については、以下を参照。

[自動化実行ユニット前判定事例](/jp/cases/automation-execution-unit-pre-control/)

---

## エンジニアリング上の結論

Ready は、設備、機構、モジュールなどの局所的な運転可能状態を確認するための重要な情報である。

一方、複雑な自動化システムでは、Target State Entry に対してさらに次の状態を確認する必要がある。

- C：Condition に関係する状態
- A：Authority に関係する状態
- E：Execution Chain に関係する状態
- それらの状態に必要な S / D / B Evaluation

したがって、PCN では Ready を単独の状態遷移結論として扱うのではなく、今回の Target State Entry に関係する複数ソース状態の一つとして使用する。

TPCA / PCN が対象とするのは、

> **Current State から Target State へ入る前に、今回の Target State Entry に必要な状態関係をどのように判定し、Arbitration を経て Multipath Control へ接続するか。**

というエンジニアリング課題である。

---

## さらに読む

- [なぜ Waiting は原因を追跡しにくいのか？](/jp/questions/why-waiting-is-hard-to-trace/)
- [自動化実行ユニット前判定事例](/jp/cases/automation-execution-unit-pre-control/)
- [Concepts｜中核概念](/jp/concepts/)
- [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)

---

## 文書情報

題目："なぜ Ready だけでは不十分なのか？"  
文書種別：エンジニアリング課題  
問題種別：ユニット・現場実行問題  
バージョン：Public Question Version 1.2  
初回公開日：2026-07-04  
最終更新日：2026-08-20  
著者：全野南政 / Nansei Zenno  
現在の URL：https://zennns.com/jp/questions/why-ready-is-not-enough/
