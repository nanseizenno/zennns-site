---
title: "TPCA における状態インスタンスの単方向性 ― 状態タイプの循環と実運転履歴の違い"
summary: "状態タイプでは A → B → A のような循環を表現できる一方、実運転では A₁ → B₁ → A₂ のように新しい状態インスタンスが時間方向へ継続して生成されることを説明する。Recovery、Rollback、Reset、Retry、Re-entry も新しい状態インスタンスへの遷移として整理し、この考え方を TPCA の状態遷移設計に採用する理由を示す。"
description: "TPCA における State Type と State Instance の違い、および単方向の状態インスタンスモデルを制御ソフトウェアへ適用する考え方を整理する。"
date: 2026-08-21
lastmod: 2026-09-08
author: "全野南政 / Nansei Zenno"
document_type: "技術ノート"
version: "Public Note Version 1.1"
citation_url: "https://zennns.com/jp/notes/tpca-unidirectional-state-transition/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## TPCA における状態インスタンスの単方向性

自動化システムでは、状態機械、SFC、シーケンス制御、設備状態モデルなどを用いて運転状態を表現する。

これらのモデルでは、同じ状態タイプへ再び遷移する構造を表現できる。

例えば、

```text
A → B → A
```

という状態遷移である。

一方、実運転で発生した状態を時間位置とともに見ると、最初の A と後の A は同じ発生状態ではない。

実際には、

```text
A₁ → B₁ → A₂
```

と考えることができる。

`A₁` と `A₂` は同じ状態タイプ A に属していても、発生した時間位置とそこへ至る履歴が異なるため、別の状態インスタンスである。

本稿の論点は、時間が進行するという事実そのものではない。その時間方向を State Instance の識別と状態遷移設計に明示的に反映することにある。

本稿では、この関係を次のように整理する。

> **状態タイプは循環できるが、実運転の状態インスタンスは時間方向へ継続して生成される。**

この考え方を用いると、Recovery、Rollback、Reset、Retry、Re-entry なども、現在の State Instance から次の State Instance への遷移として共通の状態モデルで扱うことができる。

---

## 1. なぜ A → B → A と A₁ → B₁ → A₂ を区別するのか

例えば、ロボットが Home 位置で待機している状態を A とする。

```text
A:
Robot Position = Home
Mode = Auto
Ready = TRUE
```

その後、ロボットが動作を開始して状態 B へ進む。

```text
B:
Robot Executing
Ready = FALSE
```

動作完了後、ロボットが再び Home へ戻り、

```text
Robot Position = Home
Mode = Auto
Ready = TRUE
```

となった場合、状態タイプとしては再び A と表現できる。

```text
A → B → A
```

一方、実運転では、最初の A と後の A の間に実際の処理が発生している。

例えば、

- 時間の進行
- 制御指令
- アクチュエータ動作
- ワーク状態の変化
- 資源の占有と解放
- 状態更新
- アラームやイベント
- 運転履歴

などである。

そのため、実運転履歴としては、

```text
A₁ → B₁ → A₂
```

と区別する。

ここで、

```text
Type(A₁) = Type(A₂) = A
```

であっても、

```text
A₁ ≠ A₂
```

である。

> **同じ状態タイプへ再進入しても、それは過去の状態インスタンスそのものではない。**

---

## 2. State Type と State Instance

本稿では、状態を二つのレベルに分けて考える。

### State Type

State Type は、システム設計上の状態の種類を表す。

例えば、

```text
WAIT
EXECUTE
FAULT
RECOVERY
AUTO
```

などである。

状態タイプ間の関係には循環を含めることができる。

```text
WAIT → EXECUTE → WAIT
```

```text
AUTO → FAULT → AUTO
```

### State Instance

State Instance は、実運転中に実際に発生した一つの状態を表す。

説明上、状態インスタンスを次のように表す。

```text
Sᵢ = (Xᵢ, Tᵢ)
```

ここで、

- `Xᵢ`：その時点のエンジニアリング状態内容
- `Tᵢ`：その状態が存在する時間位置

を表す。

実運転中に連続して発生する状態インスタンスを、

```text
S₀ → S₁ → S₂ → ...
```

とすると、時間位置は、

```text
T₀ < T₁ < T₂ < ...
```

となる。

後続する状態の内容が過去と同一で、

```text
X₀ = X₂
```

であっても、

```text
T₂ > T₀
```

であるため、

```text
S₂ ≠ S₀
```

となる。

したがって、

> **State Type は繰り返し現れることができるが、State Instance は実運転の時間方向に沿って新しく生成される。**

---

## 3. Recovery / Rollback / Reset も新しい State Instance への遷移である

制御ソフトウェアでは、異常復旧、状態再設定、再試行、状態再進入などを表す処理として、例えば次のような名称が使用される。

```text
Recovery
Rollback
Reset
Retry
Re-entry
```

これらの処理も、実運転上は過去の State Instance そのものへ戻るわけではない。

例えば、

```text
AUTO₁
→ FAULT₁
→ RECOVERY₁
→ AUTO₂
```

という状態遷移を考える。

`AUTO₂` が `AUTO₁` と同じ State Type であっても、

```text
Type(AUTO₁) = Type(AUTO₂)
```

実運転上は、

```text
AUTO₁ ≠ AUTO₂
```

である。

`AUTO₂` は、異常発生と Recovery を経た後に形成された新しい State Instance である。

同様に、

```text
READY₁
→ EXECUTE₁
→ RESETTING₁
→ READY₂
```

の場合も、`READY₂` は `READY₁` と同じ State Type に属する新しい State Instance である。

Retry や Re-entry についても同じである。

この整理により、Recovery、Rollback、Reset、Retry、Re-entry を、

```text
Current State
→ New State
```

という同じ方向の状態遷移として扱うことができる。

---

## 4. 制御ソフトウェア設計上の利点

State Type の循環と State Instance の時間方向を分けて扱うと、制御ソフトウェアの状態モデルを一貫した形で整理しやすくなる。

### 4.1 正常処理と異常処理を同じ遷移形式で扱える

正常処理だけでなく、異常処理、Recovery、Rollback、Reset、Retry、Re-entry も、

```text
Current State
→ New State
```

という同じ状態遷移形式で表現できる。

Recovery や Retry を、過去の State Instance へ逆向きに戻る遷移として表現する必要がない。

### 4.2 実運転履歴を区別して残せる

同じ State Type へ再進入した場合も、新しい State Instance として扱うことで、

```text
AUTO₁
AUTO₂
AUTO₃
```

のように、それぞれの発生を区別できる。

これにより、同じ状態名が繰り返し現れるシステムでも、実際の運転順序を追跡しやすくなる。

### 4.3 デバッグ時に状態の前後関係を追いやすい

例えば、

```text
WAIT → EXECUTE → WAIT
```

だけでは、どの WAIT で問題が発生したのか区別しにくい。

状態インスタンスとして、

```text
WAIT₁ → EXECUTE₁ → WAIT₂
```

と記録すれば、状態の前後関係や直前の実行履歴を確認しやすくなる。

### 4.4 実運転の状態インスタンス列と実行履歴を一つの時間方向で記述できる

正常処理、異常処理、Recovery、Retry などを、過去の State Instance へ逆向きに戻る遷移として扱わず、すべて後続する State Instance への遷移として記述することで、実運転の状態インスタンス列と実行履歴を一つの時間方向で整理できる。

この整理は、次のような項目に利用できる可能性がある。

- 状態構成の整理
- 遷移経路の記述
- 運転履歴の追跡
- デバッグ分析
- 状態ログの比較
- 制御モジュールの再利用

実際のソフトウェア複雑度、保守性、開発効率に対する効果は、具体的な実装による検証が必要である。

---

## 5. TPCA での採用

TPCA / PCN では、実運転上の状態遷移を、

```text
Current State
→ Target State
```

という関係で扱う。

ここで Target State が過去に存在した State Type と同じであっても、実際に進入した後の状態は新しい State Instance として扱う。

例えば、

```text
AUTO₁
→ FAULT₁
→ RECOVERY₁
→ AUTO₂
```

では、

```text
Type(AUTO₁) = Type(AUTO₂)
```

であっても、

```text
AUTO₁ ≠ AUTO₂
```

である。

TPCA では、この考え方を正常処理、異常処理、復旧処理、再試行、状態再進入などに共通して適用する。

TPCA における状態インスタンスの単方向性は、

> **実運転で発生した State Instance を、時間方向へ継続する一連の状態として扱う。**

という設計原則である。

この関係は、次のように表現できる。

```text
State Type:
A → B → A

State Instance:
A₁ → B₁ → A₂
```

TPCA / PCN は、この区別を状態遷移表現の基本原則として採用する。

---

## エンジニアリング上の結論

本稿の要点は、次の3点である。

1. State Type には循環を含めることができる。

```text
A → B → A
```

2. 実運転で発生する State Instance は時間方向へ継続する。

```text
A₁ → B₁ → A₂
```

3. Recovery、Rollback、Reset、Retry、Re-entry も、新しい State Instance への遷移として扱う。

この整理により、正常処理、異常処理、復旧処理、再試行、状態再進入を共通した状態遷移形式で表現できる。

> **状態タイプは循環できるが、状態インスタンスは時間方向へ継続する。**

TPCA / PCN では、この考え方を実運転上の状態遷移設計に採用する。

---

## 参考文献と外部資料

以下の資料は、産業オートメーションにおいて状態、ステップ、遷移、同一状態タイプへの再進入などの表現が使用されていることを確認するための参考資料である。

1. **PLCopen — IEC 61131-3**  
   IEC 61131-3 の Sequential Function Chart（SFC）は、ステップ、遷移、アクションを用いて PLC プログラムのシーケンス構造を表現する。  
   https://www.plcopen.org/standards/logic/iec-61131-3/

2. **PLCopen — SFC FAQ / Structuring with SFC**  
   PLCopen の公開資料では、SFC において既存ステップへ戻る分岐構造を表現できることが説明されている。  
   https://www.plcopen.org/standards/logic/iec-61131-3/faqs/

3. **OMAC — PackML**  
   PackML は、機械・ユニットにおける標準化された状態と動作モデルを提供し、設備間で共通した運転状態表現に使用される。  
   https://www.omac.org/packml

---

## 文書情報

題目：TPCA における状態インスタンスの単方向性 ― 状態タイプの循環と実運転履歴の違い  
文書種別：技術ノート  
バージョン：Public Note Version 1.1  
初回公開日：2026-08-21  
最終更新日：2026-09-08  
著者：全野南政 / Nansei Zenno  
現在の URL：https://zennns.com/jp/notes/tpca-unidirectional-state-transition/

---

本稿は、TPCA / PCN 状態遷移前制御体系の公開説明資料である。
