---
title: "自動化実行ユニット前判定事例"
summary: "画像認識を用いたコンベヤロボットユニットを代表例として、1回の状態遷移が実際に進行するエンジニアリング上の順序に沿い、PCN（Pre-Control Node / 前制御ノード）が Current State（現在状態）と Target State Entry（目標状態入口）を起点として、関連状態の取得、C / A / E 状態マッピング、S / D / B 判定、Arbitration（制御優先度調停）、Multipath Control（複数経路制御）、現在の入口に対する制御結果、後続の Target State Entry、経路実行および PCN Trace（PCN 状態遷移判定履歴）の記録までをどのように行うかを説明する。"
description: "TPCA / PCN を自動化実行ユニットへ適用する公開事例。ロボットがピックアップ段階へ移行する事例を用い、Current State、Target State / Target State Entry、PCN、CAE-SDB、Arbitration、Multipath Control、現在の入口に対する制御結果、後続の Target State Entry、Execution Result、PCN Trace の順に、1回の状態遷移前制御の全体を説明する。"
date: 2026-06-30
lastmod: 2026-09-20
author: "全野南政 / Nansei Zenno"
document_type: "公開事例"
case_type: "自動化実行ユニット層"
version: "Public Case Version 1.5"
citation_title: "自動化実行ユニット前判定事例：なぜ Robot Ready だけではピックアップ段階へ入れないのか"
citation_url: "https://zennns.com/jp/cases/automation-execution-unit-pre-control/"
draft: false
weight: 1
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## なぜ Robot Ready だけではピックアップ段階へ入れないのか

> 適用階層：自動化実行ユニット層

> 代表対象：画像認識を用いたコンベヤロボットユニット

**推奨引用形式：**

```text
全野南政 / Nansei Zenno，「自動化実行ユニット前判定事例：なぜ Robot Ready だけではピックアップ段階へ入れないのか」，公開事例，Public Case Version 1.5，2026-09-20，https://zennns.com/jp/cases/automation-execution-unit-pre-control/
```

画像認識を用いたコンベヤロボットユニットでは、Robot Ready が成立し、画像認識システムも認識結果を出力し、安全システムにも明確な異常がないにもかかわらず、ピックアップ動作が開始されないことがある。

Robot Ready は、ロボット本体が定義された運転準備状態にあることを示す。

一方、ピックアップ段階へ入るためには、現在のワーク条件、重要な許可、ピックアップ段階に必要な Execution Chain（実行チェーン）、およびこれらの状態を現在の判定根拠として使用できるかを確認する必要がある。

本事例では、1回の状態遷移が実際に進行するエンジニアリング上の処理順序に沿って、次の9ステップで説明する。

```text
1. Current State（現在状態）

2. Target State（目標状態） / Target State Entry（目標状態入口）

3. PCN（Pre-Control Node / 前制御ノード）：関連状態の取得 + C / A / E 状態マッピング

4. S / D / B 判定 → CAE-SDB Result（CAE-SDB 判定結果）+ T（時間情報）

5. Arbitration（制御優先度調停）

6. Multipath Control（複数経路制御）

7. 現在の入口に対する制御結果

8. 後続の Target State Entry と Execution Result（実行結果）

9. PCN Trace（PCN 状態遷移判定履歴）
```

この9ステップによって、

> **「ピックアップ段階へ入ろうとする 1 回の要求」が、TPCA / PCN でどのように判定され、制御され、後続の状態遷移へ進み、記録されるか**
を確認できる。

基本概念については、以下を参照。

- [Concepts｜基本概念](/jp/concepts/)
- [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)

---

## 事例対象

本事例では、画像認識を用いたコンベヤロボットユニットを代表対象とし、PCN（Pre-Control Node / 前制御ノード）を PLC 内の制御ロジックとして実装する構成を想定する。

ワークが認識・ピックアップ領域へ入ると、画像認識システムは、ワークの存在、位置、姿勢、認識信頼度、結果生成時刻、ワーク追跡情報などを生成する。

ロボットコントローラ、安全システム、メインコンベヤ、正常品置場、上位システムなどからも、今回のピックアップ入口に関係する状態を取得する。

![画像認識コンベヤロボットユニットの前制御例](/images/tpca/06-pcn-pick-flow.png)

図：PCN は、ロボットがピックアップ段階へ入る前に、現在の Target State Entry（目標状態入口）に関係する複数の状態を取得し、判定結果に基づいて制御経路を形成する。

---

## 1. Current State（現在状態）

本事例は、「画像認識が完了しているが、ロボットはまだピックアップ動作を開始していない」時点から開始する。

今回の Current State は、次のように定義する。

```text
Current State（現在状態）：認識完了 / ピックアップ待ち
```

この状態では、ワークは今回のピックアップ処理対象として認識され、画像認識結果も生成されているが、ロボットはまだピックアップ段階へ移行していない。

ここでは、今回の実運転における状態遷移の起点を明確にする。

後続の関連状態の取得、C / A / E 状態マッピング、および S / D / B 判定は、すべてこの Current State を今回の実行インスタンスの起点として扱う。

---

## 2. Target State / Target State Entry（目標状態 / 目標状態入口）

今回の Target State（目標状態）は、

```text
Target State（目標状態）：ピックアップ段階
```

である。

対応する Target State Entry（目標状態入口）は、

```text
Target State Entry（目標状態入口）：ピックアップ段階への移行
```

である。

PCN は、Current State と Target State Entry の間に配置する。

```text
Current State［認識完了 / ピックアップ待ち］

    ↓

PCN［「ピックアップ段階への移行」に対する移行前判定］

    ↓

Target State Entry［ピックアップ段階への移行］

    ↓

Target State［ピックアップ段階］
```

![Target State Entry 前における PCN の配置関係](/images/tpca/07-pcn-position-before-target-stage.png)

図：PCN は、ピックアップ動作が実際に開始される前に、「ピックアップ段階への移行」という Target State Entry を判定対象とする。

本事例における C / A / E、S / D / B、Arbitration、Multipath Control は、すべてこの明確な Target State Entry に対応付ける。

PCN と Target State Entry の関係については、以下を参照。

[なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)

---

## 3. PCN：関連状態の取得と C / A / E 状態マッピング

PCN は、「ピックアップ段階への移行」に直接関係する状態を取得する。

代表的な入力を以下に示す。

| 情報源 | 今回のピックアップ入口に関係する状態 |
|---|---|
| 画像認識システム | ワーク存在、位置、姿勢、認識結果、認識信頼度、結果生成時刻、ワーク追跡情報 |
| メインコンベヤ | 運転状態、速度、ワーク位置、ピックアップ領域の状態 |
| ロボットコントローラ | 自動モード、Ready（準備状態）、現在位置、経路状態、グリッパ / 真空状態、アラーム状態 |
| 安全システム | 安全扉、ライトカーテン、非常停止、安全回路、エリア許可 |
| 正常品置場 | 空き状態、受入状態、前ワーク処理状態 |
| 上位システム / HMI | 生産許可、作業指示、必要な手動確認、結果記録または書戻し要求 |

これらの状態を、現在の Target State Entry におけるエンジニアリング上の役割に基づいて、C / A / E の状態変数領域へマッピングする。

```text
C = Condition（条件状態）

A = Authority（許可状態）

E = Execution Chain（実行チェーン状態）
```

本事例では、次のように整理できる。

| 状態変数領域 | 現在の入口における主な対象 |
|---|---|
| C：Condition（条件状態） | ワーク存在、位置、姿勢、画像認識結果、認識信頼度、ワーク追跡 |
| A：Authority（許可状態） | 安全許可、エリア許可、PLC 放行、上位システム許可、必要な手動確認 |
| E：Execution Chain（実行チェーン状態） | ロボット経路、グリッパ / 真空状態、現在のピックアップ段階で必要となる下流受入状態、結果書戻し経路 |

例えば、

```text
ワーク位置 → C

エリア許可 → A

正常品置場の受入状態 → E
```

と整理できる。

Robot Ready は、ロボット側の関連状態の一つとして、現在のピックアップ入口におけるエンジニアリング上の役割に応じて、状態マッピングと判定に使用する。

現在の Target State に直接関係する C / A / E 状態に加えて、PCN は Return（リターン）や異常分岐など、候補となる制御経路の利用可能状態を取得し、後続の Arbitration および Multipath Control に使用することもできる。

これらの候補経路が別の Target State / Target Path に対応する場合、その利用可能性は後続の制御選択に関する情報として扱い、現在の「ピックアップ段階」に対する Execution Chain とは分けて扱う。

候補経路が利用可能であることは、現在の「ピックアップ段階への移行」という Target State Entry に対する E が成立していることを意味せず、その候補経路自体がすでに移行許可を得ていることも意味しない。

---

## 4. S / D / B 判定と CAE-SDB Result（CAE-SDB 判定結果）

C / A / E 状態マッピングの後、PCN は、現在の Target State Entry に必要な関連状態に対して S / D / B 判定を行う。

```text
S = Structure（構造完全性）

D = Dynamics（動的時系列有効性）

B = Boundary（制御境界）
```

本事例における代表的な判定内容を以下に示す。

| 判定特性 | 代表的な確認内容 |
|---|---|
| S：Structure（構造完全性） | 関連状態に必要な信号、インターフェース、マッピング、許可元、実行チェーンのインターフェースおよび対象間関係が定義・接続され、観測可能であるか |
| D：Dynamics（動的時系列有効性） | 現在の状態を今回のピックアップ入口に対する有効な判定根拠として引き続き使用できるか。更新、同期、許可撤回、遅延、状態切替などを確認する |
| B：Boundary（制御境界） | 現在有効な状態の値または範囲が、事前に定義された許容しきい値、偏差、容量、時間窓、その他の制御境界内にあるか |

C / A / E の状態変数領域と S / D / B の判定特性を組み合わせることで、9つの CAE-SDB 判定座標を構成できる。

|  | S：Structure | D：Dynamics | B：Boundary |
|---|---|---|---|
| C：Condition | C-S | C-D | C-B |
| A：Authority | A-S | A-D | A-B |
| E：Execution Chain | E-S | E-D | E-B |

本事例では、現在の「ピックアップ段階への移行」という Target State Entry に対して、代表的なエンジニアリング上の問題を次のように整理できる。

| 判定座標 | 本事例における代表的なエンジニアリング上の問題 |
|---|---|
| C-S | 画像認識インターフェースが未接続である。認識結果の項目または対象との対応関係が未定義である。ロボット座標系と画像座標系のマッピングが未設定である。ワークと認識結果の追跡関係が確立されていない |
| C-D | 画像認識結果が長時間更新されていない。認識結果が現在の有効時間を超過している。ワーク追跡とコンベヤ上の位置が同期していない。認識結果が別のワークに切り替わっている |
| C-B | 現在有効な認識信頼度が許容しきい値を下回っている。ワーク位置がピックアップ可能範囲外にある。姿勢偏差が事前に定義した許容範囲を超えている |
| A-S | 安全許可、エリア許可、PLC 放行、上位システム許可の許可元が未定義である。許可インターフェースまたはマッピングが未設定である。必要な許可状態を現在の PCN から取得できない |
| A-D | 許可状態が長時間更新されていない。ピックアップ入口の判定中に許可が撤回された。許可情報に遅延がある。安全状態またはエリア状態が切替中である |
| A-B | 現在有効な許可がその適用可能範囲を超えている。許可の有効時間窓が現在の入口条件を満たしていない。エリアまたは資源許可が事前に定義した使用境界を超えている |
| E-S | 現在のピックアップ段階に必要なロボット経路、グリッパ / 真空状態のインターフェース、正常品置場の受入インターフェース、または結果書戻し経路が完全に定義・接続されていない |
| E-D | 現在のピックアップ段階に必要なロボット経路状態が更新されていない。グリッパ / 真空状態と現在ワークの対応が同期していない。正常品置場の受入状態に遅延または失効がある。結果書戻し状態を現在有効と確認できない |
| E-B | 現在有効なグリッパ / 真空状態が許容範囲外にある。正常品置場の容量が事前に定義した境界に達している。現在のピックアップ実行チェーンに関係する位置、容量または時間パラメータが許容範囲を超えている |

この 9 つの判定座標は、現在の Target State Entry において発生し得る判定上の問題を整理するために使用する。

> **1回の実運転で、9つすべての CAE-SDB Result を形成する必要はない。**
現在の入口に対して対応する判定ルールが定義され、利用可能な判定根拠が存在し、実際に Evaluation が完了した場合にのみ、対応する CAE-SDB Result を形成する。

例えば、

```text
画像認識インターフェース：接続済み

座標マッピング：設定済み

画像認識結果：有効時間超過
```

の場合、必要な構造は成立しているが、画像認識結果は今回のピックアップ入口に対する有効な判定根拠として継続使用できない。

対応する D 判定が定義され、実際に実行された場合、

```text
C-D：

画像認識結果は、動的時系列有効性の観点から

現在の入口に対する要件を満たしていない
```

という CAE-SDB Result を形成できる。

また、

```text
画像認識結果：現在有効

ワーク位置：ピックアップ可能範囲外
```

の場合、対応する B 判定が定義され、実際に実行された場合、

```text
C-B：

ワーク位置が、現在のピックアップ入口に対する

事前定義済みの制御境界を超えている
```

という CAE-SDB Result を形成できる。

さらに、

```text
安全許可インターフェース：接続済み

許可状態：現在有効

許可対象エリア：現在のピックアップ領域を含まない
```

の場合、対応する B 判定が定義され、実際に実行された場合、

```text
A-B：

現在有効なエリア許可が、

今回のピックアップ入口に対する許容適用範囲外にある
```

という CAE-SDB Result を形成できる。

> **特定の S / D / B 判定を実行する必要があることは、その判定が現在の入口に対する評価ルールに含まれることを意味する。CAE-SDB Result は、対応する判定が実際に完了し、その結果が得られた場合に形成される。**
時間情報 T は、今回使用した状態および判定結果に関連付けて保持する。

C / A / E と S / D / B の二軸構造については、以下を参照。

[なぜ CAE-SDB なのか ― 状態変数領域と判定特性の二軸構造](/jp/notes/why-cae-sdb/)

---

## 5. Arbitration（制御優先度調停）

1回の Target State Entry に対する前制御では、複数の CAE-SDB Result が同時に形成される場合があり、重要な許可、安全上の制約、Execution Chain の状態など、入口制御に関係する条件も同時に存在することがある。

例えば、今回の Arbitration への入力は次のように整理できる。

```text
CAE-SDB Result：

C-D

画像認識結果が無効
```

```text
重要な許可：

重要な安全許可は成立
```

```text
Execution Chain 状態：

現在のピックアップ段階に必要な実行チェーンは

現在の入口に対する要件を満たしている
```

別の運転時には、例えば、

```text
CAE-SDB Result：

C-D

A-D

E-B
```

のように複数の結果が同時に形成される場合もある。

Arbitration（制御優先度調停）は、次の情報を組み合わせて、現在の入口に対する制御上の優先関係を整理する。

- CAE-SDB Result
- 重要な許可
- 安全上の制約
- 現在の Target State Entry に対する制御ルール
- 現在の入口で選択可能な制御経路

重要な A は、独立した必要制約を構成できる。

重要な安全許可が成立していない場合、現在のピックアップ入口に対してピックアップ段階への移行許可を形成してはならない。

Arbitration が扱うのは、

> **複数の判定結果と制御制約が同時に存在する場合に、制御上何を優先して処理するか**
である。

---

## 6. Multipath Control（複数経路制御）

Arbitration の後、PCN は現在の Target State Entry に対応する Multipath Control（複数経路制御）を形成する。

本事例で設定可能な代表的な制御経路は次のとおりである。

```text
Allow（移行許可）

Wait（待機）

Re-identify（再認識）

Re-sample（再サンプリング）

Re-position（再位置決め）

Retry（再試行）

Return（リターン）

Abnormal Diversion（異常分岐）

Downstream Coordination（下流調整）

Manual Confirm（手動確認）

Prohibit（移行禁止）

Safety Lock（安全ロック）

Enhanced Recording（強化記録）
```

CAE-SDB Result は、Arbitration を経て、現在の Target State Entry に対して選択可能な制御経路と対応付けられる。

例えば、同じ `C-D` であっても、対象となる Target State Entry、制御ルール、候補経路の条件によって、形成される Multipath Control が異なる場合がある。

このうち、

```text
Allow
```

は、現在判定中の Target State Entry への移行を許可することを意味する。

一方、

```text
Return

Abnormal Diversion

Alternative Path

Fallback Path
```

などの制御出力が現在の Target State 以外の別の Target State / Target Path に対応する場合、それらは対応する候補状態遷移入口へ進むことを選択する制御出力である。

これらの候補経路が選択されたことは、その経路自体がすでに移行要件を満たしていることを意味しない。

システムが新しい Target State / Target Path へ進もうとする場合は、その Target State Entry に対応する PCN によって、新たな前制御判定を行う必要がある。

---

## 7. 現在の入口に対する制御結果

Multipath Control が形成された後、現在の「ピックアップ段階への移行」という Target State Entry に対する最終的な制御結果を明確にする。

例えば、今回の状態が次のとおりであるとする。

```text
Robot Ready：成立

重要な安全許可：

成立

画像認識結果：

有効時間を超過

Return Path：

利用可能
```

画像認識結果に対する D 判定が完了し、次の結果が形成されたとする。

```text
CAE-SDB Result：

C-D

画像認識結果を、

現在のピックアップ入口に対する有効な判定根拠として

継続使用できない
```

Arbitration の後、現在の入口に対する制御結果は、例えば次のように整理できる。

```text
現在の入口に対する制御結果：

現在のピックアップ入口からは移行しない

Multipath Control：

Return（リターン）

後続候補 Target State：

リターン状態

後続候補 Target State Entry：

リターン経路への移行
```

ここでは、次の二つを区別する必要がある。

```text
現在のピックアップ入口からは移行しない
```

とは、今回の「ピックアップ段階への移行」という Target State Entry が許可されていないことを意味する。

一方、

```text
Return（リターン）
```

とは、Arbitration によって後続候補の制御経路が選択されたことを意味する。

Return が選択されたことは、リターン経路への移行がすでに許可されたことを意味しない。

システムがリターン状態へ進む場合は、「リターン経路への移行」という新しい Target State Entry に対して、次の前制御判定を行う必要がある。

---

## 8. 後続の Target State Entry と Execution Result（実行結果）

今回の Multipath Control では、

```text
Return（リターン）
```

が選択されている。

対応する新しい状態遷移目標は、次のようになる。

```text
Target State：

リターン状態

Target State Entry：

リターン経路への移行
```

この時点で、システムは新しい前制御判定コンテキストに移る。

```text
Current State［認識完了 / ピックアップ待ち］

    ↓

リターン入口に対応する PCN

    ↓

Target State Entry［リターン経路への移行］

    ↓

Target State［リターン状態］
```

リターン入口に対応する PCN は、その Target State Entry 自身の移行要件に基づいて関連状態を改めて取得し、次の処理を行う。

```text
C / A / E 状態マッピング

↓

S / D / B 判定

↓

CAE-SDB Result

↓

Arbitration

↓

Multipath Control
```

本公開事例では、「リターン経路への移行」に対応する PCN の具体的な状態設定および CAE-SDB 判定ルールは展開しない。

その Target State Entry に対する前制御判定で移行許可が形成された場合にのみ、システムはリターン経路を実行する。

全体の関係は次のようになる。

```text
現在のピックアップ入口からは移行しない

    ↓

Multipath Control：Return

    ↓

Target State：リターン状態

    ↓

Target State Entry：リターン経路への移行

    ↓

対応する PCN が新たに前制御判定を実行

    ↓

移行許可が形成された場合

    ↓

リターンを実行

    ↓

ワークが実際にリターン経路へ進入

    ↓

Execution Result：ワークがリターン経路へ進入した
```

したがって、1回の制御処理では次の関係を区別する必要がある。

```text
元の Target State Entry に対する CAE-SDB Result

↓

元の入口に対する Arbitration

↓

元の入口に対する Multipath Control

↓

元の入口に対する制御結果

↓

選択された経路に対応する新しい Target State Entry

↓

対応する PCN による新たな前制御判定

↓

経路実行

↓

Execution Result
```

その後、再認識が必要な場合は、「再認識工程への移行」が再び新しい Target State / Target State Entry となり、同じエンジニアリング上の順序に従って新たな状態遷移前制御を行う。

状態タイプの循環と実運転の状態インスタンスの関係については、以下を参照。

[TPCA における状態インスタンスの単方向性 ― 状態タイプの循環と実運転履歴の違い](/jp/notes/tpca-unidirectional-state-transition/)

---

## 9. PCN Trace（PCN 状態遷移判定履歴）

PCN Trace は、1 回の明確な Target State Entry を基本的な記録単位とする。

したがって、本事例における「ピックアップ段階への移行」と、後続の「リターン経路への移行」は、二つの異なる Target State Entry であり、それぞれ異なる PCN 判定コンテキストに対応する。

まず、今回のピックアップ入口では、次のような Trace を形成できる。

```text
PCN：

ピックアップ入口 PCN

Current State：

認識完了 / ピックアップ待ち

Target State：

ピックアップ段階

Target State Entry：

ピックアップ段階への移行

主要入力：

  Robot Ready = TRUE

  Safety Permission = TRUE

  Vision Result = Expired

CAE-SDB Result：

C-D

重要な許可：

重要な安全許可は成立

Arbitration Result：

現在のピックアップ入口への移行を許可せず、

Return を後続の制御経路として選択

Multipath Control：

Return（リターン）

現在の入口に対する制御結果：

現在のピックアップ入口からは移行しない

Selected Next Target State：

リターン状態

Selected Next Target State Entry：

リターン経路への移行

時間情報：

T

Trace ID：

PCN-PICK-XXXX
```

この Trace が記録するのは、

> **なぜ今回のピックアップ入口へ移行しなかったのか、また、なぜ次の移行先としてリターン入口が選択されたのか**
である。

その後、システムがリターン経路へ進もうとする場合は、対応する PCN が新しい前制御判定を行い、新しい Trace を形成する。

その構造は、例えば次のように表せる。

```text
PCN：

リターン入口 PCN

Current State：

認識完了 / ピックアップ待ち

Target State：

リターン状態

Target State Entry：

リターン経路への移行

関連状態：

リターン入口の実際の設定に基づいて取得

CAE-SDB Result：

リターン入口の実際の判定ルールに基づいて形成

Arbitration Result：

リターン入口の実際の判定結果に基づいて形成

Multipath Control：

移行要件を満たす場合は Allow

Execution Result：

ワークがリターン経路へ進入した

Previous Trace：

PCN-PICK-XXXX

Trace ID：

PCN-RETURN-XXXX
```

本事例では、リターン入口 PCN の具体的な状態設定、判定ルールおよび制御パラメータは公開しない。

ここで保持すべき中心的な関係は次のとおりである。

```text
ピックアップ入口 Trace
    ↓
Selected Next Target State Entry
    ↓
リターン入口 PCN
    ↓
リターン入口 Trace
    ↓
Execution Result
```

つまり、前の PCN の Multipath Control は、次の候補となる状態遷移入口を選択できるが、その入口自体に対する前制御判定を代替することはできない。

PCN Trace は、このようにして次の関係を連続的に記録できる。

```text
Target State Entry
↓
関連状態
↓
CAE-SDB Result
↓
Arbitration
↓
Multipath Control
↓
次の Target State Entry
↓
Execution Result
```

長期的に蓄積された PCN Trace は、例えば次の用途に利用できる。

- HMI または上位システムでの構造化表示
- 現場問題の振り返り
- 頻発する判定結果の集計
- 頻発する制御経路の集計
- 異なる Target State Entry 間の遷移関係分析
- 制御経路と Execution Result の関係比較
- エンジニアリング変更前後の比較
- 同種自動化実行ユニットへの再利用
- プロジェクト引継ぎ

PCN Trace の役割については、以下を参照。

[なぜ PCN Trace は新しいエンジニアリングデータなのか？](/jp/notes/why-pcn-trace-is-engineering-data/)

---

## 事例まとめ

Robot Ready（ロボット準備状態）は、ロボット本体の局所的な運転準備状態を表す。

本事例では、明確な Target State Entry を中心として、ピックアップ段階への移行に関係する状態、構造化判定、Arbitration（制御優先度調停）、制御経路、後続の状態遷移入口、および実行結果を、共通のエンジニアリング上の順序に沿って整理した。

```text
1. Current State（現在状態）

2. Target State（目標状態） / Target State Entry（目標状態入口）

3. PCN（Pre-Control Node / 前制御ノード）：関連状態の取得 + C / A / E 状態マッピング

4. S / D / B 判定 → CAE-SDB Result（CAE-SDB 判定結果）+ T（時間情報）

5. Arbitration（制御優先度調停）

6. Multipath Control（複数経路制御）

7. 現在の入口に対する制御結果

8. 後続の Target State Entry → 対応する PCN 判定 → Execution Result（実行結果）

9. PCN Trace（PCN 状態遷移判定履歴）
```

このうち、第4ステップでは、

```text
C / A / E

×

S / D / B
```

によって、現在の入口における判定上の問題を整理する 9つの CAE-SDB 座標を構成し、現在の入口に対して実際に定義されている判定ルールに基づいて、対応する Result を形成する。

現在の Target State Entry へ移行できる場合、Multipath Control は Allow を形成し、現在の Target State へ進むことができる。

一方、現在の Target State Entry へ移行できず、Arbitration が Return、異常分岐、Fallback、その他の代替経路を選択した場合、その経路は新しい Target State / Target State Entry に対応する。

システムは、その新しい Target State Entry に対して、対応する PCN による新たな前制御判定を行う必要がある。

したがって、

> **候補となる代替経路が利用可能であることは、現在の Target State に対する E が成立していることを意味しない。Multipath Control で代替経路が選択されたことも、その経路への移行がすでに許可されたことを意味しない。**
自動化実行ユニットが目標物理実行段階へ入る前の状態遷移前制御は、この順序に沿って 1 回の完全な処理として整理できる。

異なる設備や適用対象であっても、基本的なエンジニアリング上の分析骨格は共通化できる。

対象ごとに主に変化するのは、

```text
関連状態

判定ルール

重要な許可

選択可能な制御経路

後続の Target State Entry

Execution Result
```

である。

この9ステップは、TPCA / PCN の適用事例、PoC、エンジニアリング展開における基本的な分析順序として使用できる。

---

## さらに読む

- [なぜ CAE-SDB なのか ― 状態変数領域と判定特性の二軸構造](/jp/notes/why-cae-sdb/)
- [なぜ Ready だけでは不十分なのか？](/jp/questions/why-ready-is-not-enough/)
- [なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)
- [なぜ PCN Trace は新しいエンジニアリングデータなのか？](/jp/notes/why-pcn-trace-is-engineering-data/)
- [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)

---

## バージョン履歴

本稿は、TPCA / PCN 状態遷移前制御アーキテクチャを自動化実行ユニットへ適用した公開事例である。

- Public Case Version 1.0：2026-06-30
- Public Case Version 1.1：2026-08-20 PCN、CAE-SDB Result、Arbitration、Multipath Control、PCN Trace の階層表現を統一
- Public Case Version 1.2：2026-08-21 時間情報 T と状態インスタンスに関する説明を追加
- Public Case Version 1.3：2026-08-25 C / A / E と S / D / B の二軸関係を明確化
- Public Case Version 1.4：2026-09-10 統一した 9 ステップの事例分析順序へ本文を再構成し、現在の Target State に対する状態マッピング、候補制御経路、入口制御結果、実行結果、および事例内の補助ラベルの表現を統一
- Public Case Version 1.5：2026-09-20 異なる入口間の PCN Trace の接続関係を追記

著者：全野南政 / Nansei Zenno
