---
title: "自動化実行ユニット前判定事例"

summary: "画像認識を用いたコンベヤロボットユニットを代表例として、1 回の状態遷移前制御の処理順序に沿い、PCN（Pre-Control Node / 前制御ノード）が Current State（現在状態）と Target State Entry（目標状態入口）を起点として、関連状態の取得、C / A / E 状態マッピング、S / D / B 判定、Arbitration（制御優先度調停）、Multipath Control（複数経路制御）、Target State Entry に対する制御結果、制御経路の実行、PCN Trace（PCN 状態遷移判定履歴）の記録までをどのように行うかを説明する。"

description: "TPCA / PCN を自動化実行ユニットへ適用する公開事例。ロボットのピックアップ段階への移行を例に、CAE-SDB 判定から複数経路制御、実行結果、状態遷移判定履歴までを示す。"

date: 2026-06-30
lastmod: 2026-09-10

author: "全野南政 / Nansei Zenno"

document_type: "公開事例"
case_type: "自動化実行ユニット層"

version: "Public Case Version 1.4"

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
全野南政 / Nansei Zenno，「自動化実行ユニット前判定事例：なぜ Robot Ready だけではピックアップ段階へ入れないのか」，TPCA / PCN 公開事例，Public Case Version 1.4，2026-09-10，https://zennns.com/jp/cases/automation-execution-unit-pre-control/
```

画像認識を用いたコンベヤロボットユニットでは、Robot Ready が成立し、画像認識結果も生成され、安全システムにも明確な異常がないにもかかわらず、ピックアップ動作が開始されないことがある。

Robot Ready は、ロボット本体が所定の運転準備状態にあることを示す。

一方、ピックアップ段階へ入るためには、現在のワーク条件、重要な許可、ピックアップ段階に必要な Execution Chain（実行チェーン）、および各状態を今回の判定根拠として現在も使用できるかを確認する必要がある。

本事例では、1 回の状態遷移前制御の処理順序に沿って、次の 9 ステップで説明する。

```text
1. Current State（現在状態）
2. Target State（目標状態）   / Target State Entry（目標状態入口）
3. PCN（Pre-Control Node / 前制御ノード）：関連状態の取得 + C / A / E 状態マッピング
4. S / D / B 判定 → CAE-SDB Result（CAE-SDB 判定結果）+ T（時間情報）
5. Arbitration（制御優先度調停）
6. Multipath Control（複数経路制御）
7. Target State Entry に対する制御結果
8. 選択された制御経路 → Execution Result（実行結果）
9. PCN Trace（PCN 状態遷移判定履歴）
```

この 9 ステップによって、

> **「ピックアップ段階へ入ろうとする 1 回の要求」が、TPCA / PCN でどのように判定・制御・実行・記録されるか**

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

図：PCN は、ロボットがピックアップ段階へ入る前に、今回の Target State Entry（目標状態入口）に関係する複数の状態を取得し、構造化判定と Arbitration を経て制御経路を形成する。

---

# 1. Current State（現在状態）

本事例は、「画像認識が完了しているが、ロボットはまだピックアップ動作を開始していない」時点から開始する。

今回の Current State は、次のように定義する。

```text
Current State（現在状態）：認識完了 / ピックアップ待ち
```

この状態では、ワークは今回のピックアップ処理対象として認識され、画像認識結果も生成されているが、ロボットはまだピックアップ段階へ移行していない。

ここでは、1 回の状態遷移の起点となる Current State を明確にする。

後続の関連状態の取得、C / A / E 状態マッピング、S / D / B 判定、Arbitration（制御優先度調停）、Multipath Control（複数経路制御）は、この Current State を起点とする 1 回の状態遷移前制御として扱う。

---

# 2. Target State / Target State Entry（目標状態・目標状態入口）

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

PCN は、Current State から Target State へ入る際の Target State Entry の前に配置する。

```text
Current State（現在状態）
認識完了 / ピックアップ待ち
    ↓
PCN（Pre-Control Node / 前制御ノード）
［「ピックアップ段階への移行」に対する前置判定］
    ↓
Target State Entry（目標状態入口）
ピックアップ段階への移行
    ↓
Target State（目標状態）
ピックアップ段階
```

![Target State Entry 前における PCN の配置関係](/images/tpca/07-pcn-position-before-target-stage.png)

図：PCN はピックアップ動作が実際に開始される前に、「ピックアップ段階への移行」という Target State Entry を判定対象とする。

本事例における C / A / E、S / D / B、Arbitration、Multipath Control は、すべてこの Target State Entry に対応付ける。

PCN と Target State Entry の関係については、以下を参照。

[なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)

---

# 3. PCN：関連状態の取得と C / A / E 状態マッピング

PCN は、「ピックアップ段階への移行」に直接関係する状態を取得する。

代表的な入力を次に示す。

| 情報源 | 今回のピックアップ入口に関係する状態 |
|---|---|
| 画像認識システム | ワーク存在、位置、姿勢、認識結果、認識信頼度、結果生成時刻、ワーク追跡情報 |
| メインコンベヤ | 運転状態、速度、ワーク位置、ピックアップ領域の状態 |
| ロボットコントローラ | 自動モード、Ready（準備状態）、現在位置、経路状態、グリッパ / 真空状態、アラーム状態 |
| 安全システム | 安全扉、ライトカーテン、非常停止、安全回路、エリア許可 |
| 正常品置場 | 空き状態、受入状態、前ワーク処理状態 |
| 上位システム / HMI | 生産許可、作業指示、必要な手動確認、結果記録または書戻し要求 |

これらの関連状態を、今回の Target State Entry における役割に基づいて C / A / E の状態変数領域へマッピングする。

```text
C = Condition（条件状態）
A = Authority（許可状態）
E = Execution Chain（実行チェーン状態）
```

本事例では、次のように整理できる。

| 状態変数領域 | 今回の Target State Entry における代表的な状態 |
|---|---|
| C：Condition（条件状態） | ワーク存在、位置、姿勢、画像認識結果、認識信頼度、ワーク追跡 |
| A：Authority（許可状態） | 安全許可、エリア許可、PLC 放行、上位システム許可、必要な手動確認 |
| E：Execution Chain（実行チェーン状態） | Robot Ready（ロボット準備状態）、ロボット経路、グリッパ / 真空状態、ピックアップ後に必要な正常品置場の受入状態、結果書戻し経路 |

例えば、

```text
ワーク位置 → C：Condition（条件状態）
エリア許可 → A：Authority（許可状態）
Robot Ready → E：Execution Chain（実行チェーン状態）
正常品置場の受入状態 → E：Execution Chain（実行チェーン状態）
```

と整理できる。

Robot Ready は、今回の Target State Entry における E：Execution Chain の入力の一つである。

E には、Robot Ready に加え、ロボット経路、グリッパ / 真空状態、正常品置場の受入状態、結果書戻し経路など、Target State へ入った後の実行チェーンに関係する状態を含む。

また、PCN は、現在の Target State とは別に、Return（リターン）や異常分岐など、後続の候補制御経路が利用可能かを確認するための状態も取得できる。

現在の Target State へ入った後に必要となる実行チェーンは、E として判定する。Return、異常分岐、その他の代替経路が別の Target State に対応する場合は、それらの経路状態を後続候補の実行可能性として取得し、Arbitration（制御優先度調停）および Multipath Control（複数経路制御）における制御経路の選択にも使用する。

---

# 4. S / D / B 判定 → CAE-SDB Result（CAE-SDB 判定結果）+ T（時間情報）

C / A / E 状態マッピングの後、PCN は、今回の Target State Entry に必要な関連状態に対して S / D / B 判定を行う。

```text
S = Structure（構造完全性）
D = Dynamics（動的時系列有効性）
B = Boundary（制御境界）
```

本事例における代表的な確認内容は次のとおりである。

| 判定特性 | 代表的な確認内容 |
|---|---|
| S：Structure（構造完全性） | 画像認識インターフェース、座標マッピング、安全許可元、下流受入インターフェース、結果書戻しインターフェースなどが定義・接続され、観測可能であるか |
| D：Dynamics（動的時系列有効性） | 画像認識結果を現在も判定根拠として使用できるか、ワーク追跡が同期しているか、許可が撤回されていないか、ロボットや下流状態に遅延・未更新がないか |
| B：Boundary（制御境界） | 認識信頼度、ワーク位置、姿勢、ピックアップ領域、下流容量などが、事前に定義された許容範囲、しきい値、または制御境界内にあるか |

例えば、

```text
画像認識インターフェース：接続済み
座標マッピング：設定済み
画像認識結果：有効時間超過
```

の場合、必要な構造は成立しているが、画像認識結果は今回の判定根拠として使用できない。

対応する D 判定により、この状態が確認された場合、

```text
C-D：
画像認識結果を、今回の Target State Entry に対する有効な判定根拠として現在は使用できない
```

という CAE-SDB Result（CAE-SDB 判定結果）を形成できる。

また、

```text
画像認識結果：現在有効
ワーク位置：ピックアップ可能範囲外
```

の場合、対応する B 判定により、この状態が確認された場合、

```text
C-B：

ワーク位置が、今回の Target State Entry に対して事前に定義された制御境界外にある
```

という CAE-SDB Result を形成できる。

> **S / D / B は C / A / E の状態変数を分析するための判定特性であり、対応する判定結果が得られた場合に CAE-SDB Result を形成する。**

時間情報 T は、本判定に使用した状態および判定結果に関連付けて保持する。

C / A / E と S / D / B の二軸構造については、以下を参照。

[なぜ CAE-SDB なのか ― 状態変数領域と判定特性の二軸構造](/jp/notes/why-cae-sdb/)

---

# 5. Arbitration（制御優先度調停）

1 回の Target State Entry に対する前置判定では、複数の CAE-SDB Result が同時に形成される場合がある。

また、重要な許可、安全上の制約、今回の Target State Entry に適用する制御制約も同時に存在する。

例えば、本判定における Arbitration の入力は次のように整理できる。

```text
CAE-SDB Result（CAE-SDB 判定結果）：
C-D
画像認識結果が現在無効
```

```text
重要な A：Authority（許可状態）：
重要な安全許可は成立
```

別の運転時には、例えば、

```text
CAE-SDB Result（CAE-SDB 判定結果）：
C-D
A-D
E-B
```

のように複数の結果が同時に形成される場合もある。

Arbitration（制御優先度調停）は、次の情報に基づいて、今回の Target State Entry に対する制御上の優先関係を処理する。

- CAE-SDB Result（CAE-SDB 判定結果）
- 重要な A：Authority（許可状態）
- 安全上の制約
- 今回の Target State Entry に適用する制御制約
- 事前に定義され、現在選択可能な制御経路

重要な A は、Target State Entry に対する独立した必要制約である。

重要な安全許可が成立していない場合は、C と E がともに成立していても、現在のピックアップ入口に対する移行許可を形成しない。

Arbitration が扱うのは、

> **複数の判定結果と制御制約が同時に存在する場合に、今回の Target State Entry で何を優先して処理するか**

である。

---

# 6. Multipath Control（複数経路制御）

Arbitration の結果に基づき、PCN は今回の Target State Entry に対する Multipath Control（複数経路制御）を形成する。

本事例における代表的な制御経路は次のとおりである。

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

CAE-SDB Result は Arbitration を経て、今回の Target State Entry に対して選択可能な制御経路と対応付けられる。

例えば、同じ `C-D` であっても、対象となる Target State Entry、設備構成、制御ルール、候補経路の利用可能状態によって、形成される Multipath Control は異なる場合がある。

Return、異常分岐、その他の代替経路が別の Target State に対応する場合は、今回の Target State Entry に対する候補制御出力として選択する。

別の Target State へ実際に入る際は、対応する新しい Target State Entry に対して、次の状態遷移判定を行う。

---

# 7. Target State Entry（目標状態入口）に対する制御結果

Multipath Control の結果を今回の Target State Entry に反映し、その入口に対する制御結果を明確にする。

例えば、今回の状態が次のとおりであるとする。

```text
Robot Ready：成立
重要な安全許可：成立
画像認識結果：有効時間を超過
Return Path（リターン経路）：利用可能
```

画像認識結果に対する D 判定から、

```text
CAE-SDB Result（CAE-SDB 判定結果）：
C-D
画像認識結果を、現在のピックアップ入口に対する有効な判定根拠として現在は使用できない
```

という結果が形成されたとする。

Arbitration と Multipath Control の結果を今回の Target State Entry に反映すると、例えば次のように整理できる。

```text
Target State Entry に対する制御結果：現在のピックアップ入口からピックアップ段階へ移行しない
後続の制御経路：Return（リターン）
```

このステップでは、新たな制御判断を追加するのではなく、

> **Arbitration と Multipath Control によって形成された結果を、現在の Target State Entry に対する具体的な制御結果として反映する。**

実際に選択された制御経路の実行結果は、次の工程で確認する。

---

# 8. 選択された制御経路 → Execution Result（実行結果）

今回選択された制御経路を、

```text
選択された制御経路：Return（リターン）
```

とする。

システムは、この制御結果に基づいて Return（リターン）処理を実行する。

```text
現在のピックアップ入口からピックアップ段階へ移行しない
    ↓
ワークをリターン経路へ送る
    ↓
ワークがリターン経路へ進入
    ↓
新しい状態インスタンスを形成
```

実際の処理結果は、例えば次のようになる。

```text
Execution Result（実行結果）：ワークがリターン経路へ進入した
```

後続で再認識が必要な場合は、「再認識工程への移行」を新しい Target State として扱い、その Target State Entry に対して新しい状態遷移判定を行う。

1 回の処理は、次のように区別して記述できる。

```text
CAE-SDB Result（CAE-SDB 判定結果）
↓
Arbitration Result（制御優先度調停結果）
↓
Multipath Control（複数経路制御）
↓
Target State Entry に対する制御結果
↓
選択された制御経路
↓
Execution Result（実行結果）
```

第 7 ステップでは、Arbitration と Multipath Control の結果を現在の Target State Entry に反映し、その入口に対する制御結果と後続の制御経路を明確にする。

第 8 ステップでは、選択された制御経路を実行し、実際に形成された Execution Result を確認する。

状態タイプの循環と実運転の状態インスタンスの関係については、以下を参照。

[TPCA における状態インスタンスの単方向性 ― 状態タイプの循環と実運転履歴の違い](/jp/notes/tpca-unidirectional-state-transition/)

---

# 9. PCN Trace（PCN 状態遷移判定履歴）

1 回の状態遷移前制御が完了した後、PCN は今回の入力、判定、制御、実行結果を PCN Trace として関連付けて記録する。

例えば、今回の Trace は次のように整理できる。

```text
PCN：
ピックアップ入口 PCN

Current State：認識完了 / ピックアップ待ち

Target State：ピックアップ段階

Target State Entry：ピックアップ段階への移行

関連状態：
  Robot Ready = TRUE
  Safety Permission = TRUE
  Vision Result = Expired
  Return Path = Available

C / A / E 状態マッピング：
  Vision Result（画像認識結果） → C：Condition（条件状態）
  Safety Permission（安全許可） → A：Authority（許可状態）
  Robot Ready（ロボット準備状態） → E：Execution Chain（実行チェーン状態）

S / D / B 判定：
  Vision Result（画像認識結果）
    → D：Dynamics（動的時系列有効性）
    → 現在無効

CAE-SDB Result：C-D

重要な A：Authority：重要な安全許可は成立

Arbitration Result：
  C-D を優先して処理し、現在のピックアップ入口に対する移行許可を形成しない

Multipath Control：Return
  Target State Entry に対する制御結果：現在のピックアップ入口からピックアップ段階へ移行しない

選択された制御経路：Return
  Execution Result（実行結果）：ワークがリターン経路へ進入した

時間情報：T

Trace ID（履歴識別子）：PCN-PICK-XXXX
```

PCN Trace は、1 回の Target State Entry に対する前置判定を単位として、今回使用した状態、C / A / E 状態マッピング、S / D / B 判定、CAE-SDB Result、Arbitration、Multipath Control、Target State Entry に対する制御結果、選択された制御経路、Execution Result を関連付けて記録する。

長期的に蓄積された PCN Trace は、例えば次の用途に利用できる。

- HMI または上位システムでの構造化表示
- 現場問題の振り返り
- 頻発する CAE-SDB Result の集計
- 頻発する制御経路の集計
- Multipath Control と Execution Result の関係比較
- エンジニアリング変更前後の比較
- 同種自動化実行ユニットへの再利用
- プロジェクト引継ぎ
- エンジニア教育

PCN Trace の役割については、以下を参照。

[なぜ PCN Trace は新しいエンジニアリングデータなのか？](/jp/notes/why-pcn-trace-is-engineering-data/)

---

## 事例まとめ

Robot Ready（ロボット準備状態）は、ロボット本体の局所的な運転準備状態を表す。

本事例では、「ピックアップ段階への移行」という明確な Target State Entry を中心として、関連状態、構造化判定、Arbitration（制御優先度調停）、Multipath Control（複数経路制御）、Target State Entry に対する制御結果、選択された制御経路、Execution Result（実行結果）を、1 回の状態遷移前制御の処理順序に沿って整理した。

```text
1. Current State（現在状態）
2. Target State（目標状態） / Target State Entry（目標状態入口）
3. PCN（Pre-Control Node / 前制御ノード）：関連状態の取得 + C / A / E 状態マッピング
4. S / D / B 判定 → CAE-SDB Result（CAE-SDB 判定結果）+ T（時間情報）
5. Arbitration（制御優先度調停）
6. Multipath Control（複数経路制御）
7. Target State Entry に対する制御結果
8. 選択された制御経路 → Execution Result（実行結果）
9. PCN Trace（PCN 状態遷移判定履歴）
```

自動化実行ユニットが目標物理実行段階へ入る前の判定は、この 9 ステップに沿って 1 回の状態遷移前制御として整理できる。

異なる設備や適用対象でも、基本的な分析順序は共通化できる。

具体的に変化するのは主として、

```text
関連状態
判定ルール
重要な許可
選択可能な制御経路
実行結果
```

である。

この 9 ステップは、TPCA / PCN の適用事例、PoC、工程設計を展開する際の基本的な分析順序として使用できる。

---

## さらに読む

- [なぜ CAE-SDB なのか ― 状態変数領域と判定特性の二軸構造](/jp/notes/why-cae-sdb/)
- [なぜ Ready だけでは不十分なのか？](/jp/questions/why-ready-is-not-enough/)
- [なぜ状態遷移条件を明示する必要があるのか？](/jp/notes/explicit-state-transition-conditions/)
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
- Public Case Version 1.4：2026-09-10 統一した 9 ステップの事例分析順序へ本文を再構成

著者：全野南政 / Nansei Zenno
