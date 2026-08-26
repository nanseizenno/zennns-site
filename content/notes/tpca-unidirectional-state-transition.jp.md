---
title: "TPCA の状態遷移単方向性 ― なぜ実システムでは過去の状態インスタンスへ戻らないのか？"
summary: "実システムにおける時間の単方向性から、エンジニアリング状態内容が再び同一になっても、時間成分が異なる状態インスタンスは過去の状態インスタンスには戻らないことを説明する。これに基づき、TPCA が Current State から新しい Target State への単方向の状態遷移として実運転を扱う理由を示す。"
description: "TPCA の状態遷移単方向性について説明する。実際の運転状態はエンジニアリング状態内容と時間成分によって区別され、後続状態が過去と同じ状態内容を持つ場合でも、新しい状態インスタンスとして扱う。この観点から Rollback、Recovery、復帰、回流、Multipath Control を整理し、PCN、PCN Trace、PCN Network、制御ソフトウェアアーキテクチャとの関係を示す。"
date: 2026-08-21
lastmod: 2026-08-21
author: "全野南政 / Nansei Zenno"
document_type: "技術ノート"
version: "Public Note Version 1.0"
citation_url: "https://zennns.com/jp/notes/tpca-unidirectional-state-transition/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## TPCA の状態遷移単方向性

自動化システムでは、状態機械、SFC、シーケンス制御、設備状態モデルなどを用いて運転状態を表現する。

これらのモデルでは、同じ状態名やステップへ再び遷移する構造を表現できる。

例えば、次のような状態遷移である。

```text
A → B → A
```

制御プログラムや状態図では、このような表現を使用できる。

一方、実システムで実際に発生した状態インスタンスとして見ると、前後の `A` は同じ状態インスタンスではない。

両者は異なる時間位置で発生しているためである。

システムが B を経由した後、設備位置、モード、Ready、変数値などが最初の A と同じ内容になったとしても、その状態はより後の時間位置に存在する。

TPCA では、この関係を次のように扱う。

> **状態内容は再び同一になり得るが、状態インスタンスは過去の状態インスタンスには戻らない。**

これが TPCA の状態遷移単方向性である。

> **実システムの状態遷移は、常に時間方向へ進む。実運転上は、Current State から新しい Target State への状態遷移として扱う。**

---

## 1. 状態インスタンスは状態内容と時間成分によって区別される

制御プログラム上の状態名だけでシステムを表す場合、次のように記述できる。

```text
State = X
```

ここで `X` は、現在のエンジニアリング状態内容を表す。

例えば、次のような内容である。

```text
Robot Position = Home
Mode = Auto
Ready = TRUE
```

実運転中に発生した一つの状態インスタンスを区別する場合は、状態内容に加えて、その状態が発生した時間位置も考慮する。

本稿では、説明上、実際の状態インスタンスを次のように表す。

```text
Sᵢ = (Xᵢ, Tᵢ)
```

ここで、

- `Xᵢ`：その時点のエンジニアリング状態内容
- `Tᵢ`：その状態インスタンスが存在する時間位置

を表す。

実際に連続して発生する状態インスタンスを、

```text
S₀ → S₁ → S₂ → ...
```

とすると、時間位置は次の関係を持つ。

```text
T₀ < T₁ < T₂ < ...
```

したがって、後続する状態のエンジニアリング状態内容が過去の状態と同一であっても、

```text
X₀ = X₂
```

かつ、

```text
T₂ > T₀
```

であれば、

```text
S₂ ≠ S₀
```

となる。

すなわち、

> **エンジニアリング状態内容が同一であっても、異なる時間位置に発生した状態は別の状態インスタンスである。**

---

## 2. 状態タイプ上の A → B → A と実際の状態インスタンスを区別する

設備が初期状態 A にあるとする。

```text
A:
Robot Position = Home
Mode = Auto
Ready = TRUE
```

その後、状態 B へ遷移する。

```text
B:
Robot Executing
Ready = FALSE
```

動作完了後、ロボットが再び Home へ戻り、次の状態内容になったとする。

```text
Robot Position = Home
Mode = Auto
Ready = TRUE
```

状態タイプや状態図では、この状態を再び A と表現できる。

```text
A → B → A
```

TPCA では、実際に発生した状態インスタンスを記述する場合、後続状態を新しい状態インスタンスとして扱う。

例えば、

```text
A → B → C
```

とする。

このとき、

```text
X_C = X_A
```

であっても、

```text
T_C > T_A
```

であるため、

```text
C ≠ A
```

となる。

C は A と同一または類似したエンジニアリング状態内容を持つ新しい状態インスタンスである。

A から C までの間には、実際に次のような事象が発生している。

- 時間の進行
- 制御指令
- アクチュエータ動作
- ワークまたは設備状態の変化
- 資源の占有と解放
- 状態更新
- システムイベント
- 運転履歴

C の状態内容が A と同一であっても、これらの実行履歴は消失しない。

したがって、

> **状態タイプは再び現れることができるが、実際の状態インスタンスは時間方向へ継続して生成される。**

![TPCA の状態遷移単方向性：状態タイプは循環できるが、状態インスタンスは時間方向へ継続する](/images/tpca/11-tpca-unidirectional-state-transition.zh.png)

図：従来の状態モデルでは `A → B → A` のように、同じ状態タイプへ再び遷移する構造を表現できる。TPCA では実際に発生した状態インスタンスを時間位置とともに扱うため、後続状態が過去と同じエンジニアリング状態内容を持つ場合でも、新しい状態インスタンスとして区別する。

---

## 3. Rollback、Recovery、復帰、回流も新しい Target State への遷移として扱う

状態インスタンスを時間位置とともに扱うと、実システムでは過去の状態インスタンスそのものへ戻ることはない。

現場で使用される次のような名称は、プログラム名、制御経路名、運用上の用語としてそのまま使用できる。

```text
Rollback
Recovery
Return
Reset
Restore
復帰
回流
再投入
```

TPCA の状態遷移の観点では、これらも Current State から新しい Target State への遷移として扱う。

例えば、

```text
A：正常運転
→ B：実行異常
→ C：安全停止
→ D：復帰準備
→ E：正常運転状態への再進入
```

という実行履歴を考える。

E のエンジニアリング状態内容が A と同一であっても、

```text
X_E = X_A
```

かつ、

```text
T_E > T_A
```

であるため、

```text
E ≠ A
```

となる。

実際の状態インスタンス列は、

```text
A → B → C → D → E
```

として時間方向へ継続する。

したがって、TPCA では Rollback を過去の状態インスタンスへ戻る処理としてではなく、

```text
Current State → New Target State
```

として扱う。

Recovery、復帰、回流、再投入についても同様である。

---

## 4. 異常発生後は、新しい Current State から次の Target State を決定する

運転中に異常が発生した場合、一般的な工程表現では次のように記述することがある。

```text
Normal → Fault → Recovery → Normal
```

TPCA では、Recovery を時間方向が逆になる遷移として扱わない。

異常が発生した時点で、実システムには新しい状態インスタンスが形成される。

例えば、ロボットのピックアップ中に真空保持が失われた場合を考える。

異常発生前は、

```text
S₁：ピックアップ実行中
```

であったとする。

異常発生後には、例えば次のような新しい状態インスタンスが形成される。

```text
S₂：
ピックアップ実行中断
+ ワーク保持状態を確認できない
+ 設備状態および安全状態が更新済み
```

この時点では、

```text
Current State = S₂
```

となる。

次に、現在の実状態に対して新しい Target State を設定する。

```text
Target State = ?
```

候補となる Target State または目標実行経路には、例えば次のものがある。

- 安全保持
- 異常排出
- ワーク解放
- 退避位置
- 手動確認
- 再認識
- その他の事前定義されたエンジニアリング状態

その後、今回の Target State Entry に対して PCN の前置判定を行う。

```text
Current State
→ Target State Entry / PCN
→ Selected Target State
```

異常が発生した場合も、状態遷移の時間方向は変わらない。

新しい Current State が形成され、その状態から次の Target State を決定する。

正常運転、異常処理、復帰、再投入は、いずれも同じ状態遷移関係で扱う。

---

## 5. Multipath Control は次の Target State または目標実行経路を決定する

状態遷移単方向性の観点から見ると、Multipath Control は、現在の Target State Entry に対して次に進む Target State または目標実行経路を決定する制御出力として整理できる。

代表的な Multipath Control には、次のようなものがある。

- Allow
- Wait
- Recheck
- Re-identify
- Return
- Degrade
- Manual Confirm
- Prohibit
- Safety Lock
- その他の事前定義された制御経路

これらは、それぞれ異なるエンジニアリング上の用途を持つ。

例えば Current State が、

```text
Current State:
ピックアップ失敗後、ワーク保持状態を確定できない状態
```

であるとする。

候補となる Target State または目標実行経路を次のように設定できる。

```text
T₁ = 安全保持
T₂ = 異常排出
T₃ = 再認識
T₄ = 手動確認
T₅ = 回流状態
```

今回の Target State Entry に対する処理は、次の関係で行う。

```text
CAE-SDB Result + T
→ Arbitration
→ Multipath Control
```

Arbitration の結果として T₃ が選択された場合、

```text
Selected Target State = T₃
```

となり、その後の状態遷移は、

```text
Current State → T₃
```

として扱う。

回流が選択された場合も、

```text
Current State → T₅
```

である。

したがって、TPCA の状態遷移単方向性では、

> **Multipath Control は、現在の Target State Entry に対して、次の Target State または目標実行経路を決定する。**

正常経路、回流経路、縮退経路、手動確認経路、安全関連経路などは、候補となる Target State または目標実行経路の用途が異なる。

---

## 6. PCN は状態インスタンスが変化する前の Target State Entry を判定する

TPCA / PCN の中核となる考え方は、次の通りである。

> **明確な Target State Entry は、それ自体を独立して設計・判定・制御・記録できるエンジニアリング対象として扱うべきである。**

状態遷移単方向性は、Target State Entry を明確にする必要性を、実際の状態インスタンスと時間位置の関係から説明する。

一度、状態遷移が実際に発生すると、

```text
Sᵢ → Sᵢ₊₁
```

システムは新しい時間位置へ進む。

```text
Tᵢ₊₁ > Tᵢ
```

後続の状態遷移によって過去と同じエンジニアリング状態内容が再び形成された場合も、それは別の状態インスタンスである。

したがって PCN は、今回の Target State Entry において、Target State へ実際に入る前に必要な判定と制御を行う。

```text
Current State
    ↓
Target State Entry / PCN
    ↓
Target State
```

PCN は、今回の Target State Entry に関係する状態を取得し、C / A / E Mapping、S / D / B Evaluation、CAE-SDB Result と時間情報 T の形成、Arbitration、Multipath Control を行う。

この意味で Pre-Control は、

> **新しい状態インスタンスへ進む前に、今回の Target State Entry に必要な判定と制御を実行する**

という位置付けを持つ。

---

## 7. PCN Trace は時間方向へ生成される状態遷移判定履歴を記録する

システムが現在の状態内容だけを記録している場合を考える。

```text
Robot Position = Home
Mode = Auto
Ready = TRUE
```

この情報だけでは、その状態が、

```text
A：タスク開始前
```

の状態インスタンスであるのか、

```text
C：
実行
→ 異常発生
→ 後続処理
→ Home / Auto / Ready を再び形成
```

した後の状態インスタンスであるのかを区別できない。

A と C のエンジニアリング状態内容が同一であっても、

```text
X_A = X_C
```

時間位置が異なる場合、

```text
T_A ≠ T_C
```

であるため、A と C は異なる状態インスタンスである。

PCN Trace は、時間方向へ発生した状態遷移と、それぞれの Target State Entry における判定履歴を記録する。

例えば、

```text
S₀ → S₁ → S₂ → S₃ → ...
```

という状態インスタンス列とともに、各 Target State Entry について次の情報を関連付ける。

- Current State
- Target State
- 判定に使用した状態
- CAE-SDB Result
- 時間情報 T
- Arbitration Result
- Multipath Control
- Execution Result
- Trace ID

この関係により、

> **Current State は、システムが現在どの状態インスタンスにあるかを示す。**

> **PCN Trace は、各 Target State Entry における判定と制御の履歴を、実際の時間位置に沿って記録する。**

同じ状態内容は後続運転で再び現れる場合がある。

その場合も、新しい状態インスタンスとして新しい PCN Trace の文脈に記録される。

---

## 8. PCN Network の状態タイプ関係には循環を含められるが、実運転の状態インスタンス列は時間方向へ進む

ここでは、状態タイプ関係と実際の状態インスタンスを区別する必要がある。

### 状態タイプ関係

システム設計上は、次のような状態タイプ間の遷移関係を定義できる。

```text
AUTO → FAULT → AUTO
```

または、

```text
WAIT → EXECUTE → WAIT
```

これは、

> どの状態タイプから、どの状態タイプへ遷移できるか。

を表す。

したがって、状態タイプ関係には循環を含めることができる。

### 実際の状態インスタンス

実運転中には、状態インスタンスが次のように生成される。

```text
S₀ → S₁ → S₂ → S₃ → ...
```

各状態インスタンスの時間位置は、

```text
T₀ < T₁ < T₂ < T₃ < ...
```

となる。

例えば、

```text
A：AUTO，T₁
→ B：FAULT，T₂
→ C：AUTO，T₃
```

の場合、

```text
Type(C) = Type(A)
```

であっても、

```text
C ≠ A
```

である。

したがって、

> **PCN Network の状態タイプ関係には循環を含めることができるが、実運転における状態インスタンスは時間方向へ継続して生成される。**

PCN Network は、複数の Target State Entry とそれらの実際の状態遷移関係、必要な依存関係を表す。

PCN Trace は、実際に発生した Target State Entry の判定履歴を時間方向に記録する。

---

## 9. 状態遷移単方向性を制御ソフトウェアの状態モデルに適用する

自動化ソフトウェアでは、例えば次のような処理名が使用される。

```text
Normal Logic
Fault Logic
Rollback Logic
Recovery Logic
Reset Logic
Return Logic
```

これらの処理は、それぞれの工程目的に応じて実装できる。

TPCA の状態遷移単方向性では、これらを時間方向の異なる状態モデルとして扱うのではなく、Current State から次の Target State への遷移として整理する。

基本的な関係は次のように表せる。

```text
Current State
→ Candidate Target States
→ PCN
→ Arbitration
→ Selected Target State
→ State Transition
```

これにより、正常実行、異常処理、復帰、回流、縮退、再投入を、次の共通した状態遷移関係で記述できる。

> **現在の実状態から、次の Target State を選択する。**

この整理方法には、制御ソフトウェアの状態モデルを統一する上での検討価値がある。

例えば、次のような整理が可能になる。

- Rollback を時間方向が逆の状態遷移として扱わない。
- Recovery に別の時間方向を定義しない。
- 異常発生後も Current State → Target State の関係で扱う。
- Multipath Control を次の Target State または目標実行経路の選択として整理する。
- PCN Trace と実際の状態インスタンス列を同じ時間方向で記録する。

この単方向の状態モデルを適用することで、複雑な制御ソフトウェアにおける次の項目を、同じ状態遷移関係で整理できる可能性がある。

- 状態構成
- 経路設計
- Arbitration
- 履歴記録
- デバッグ分析
- モジュール再利用

実際のソフトウェア複雑度に対する効果は、具体的な実装による検証が必要である。

TPCA のアーキテクチャ上の状態遷移は、次の関係で統一して扱う。

> **Current State → Target State**

---

## エンジニアリング上の結論

TPCA の状態遷移単方向性は、次の3点に整理できる。

### 1. 状態インスタンスは時間成分を持つ

実際の状態インスタンスを、説明上、次のように表す。

```text
Sᵢ = (Xᵢ, Tᵢ)
```

2 つの状態が同じエンジニアリング状態内容を持っていても、

```text
Xᵢ = Xⱼ
```

時間位置が異なれば、

```text
Tᵢ ≠ Tⱼ
```

別の状態インスタンスとして扱う。

---

### 2. 実際の状態インスタンスは時間方向へ継続して生成される

実際に発生する連続した状態遷移では、

```text
Sᵢ → Sᵢ₊₁
```

時間位置は、

```text
Tᵢ₊₁ > Tᵢ
```

となる。

したがって、実運転の状態インスタンス列は時間方向へ継続する。

---

### 3. 復帰、回流、Rollback、Recovery も新しい Target State への遷移である

現場で使用される、

```text
Rollback
Recovery
Return
Reset
復帰
回流
再投入
```

などの名称は、そのまま工程名称や制御経路名として使用できる。

TPCA の実運転上の状態遷移では、これらも次のように扱う。

```text
Current State → New Target State
```

新しい Target State が過去と同じエンジニアリング状態内容を持つ場合も、時間位置が異なるため新しい状態インスタンスである。

この関係は、次のように表現できる。

> **状態タイプは循環できるが、状態インスタンスは時間方向へ継続する。**

TPCA は、この状態遷移単方向性に基づいて、正常実行、異常処理、復帰、回流、縮退、再投入を同じ Current State → Target State の関係で扱い、PCN、Multipath Control、PCN Trace、PCN Network の状態遷移基盤を統一する。

---

## 参考文献と外部資料

以下の資料は、産業オートメーションで状態、ステップ、遷移、同一状態タイプへの再進入などの表現が広く使用されていることを示すための参考資料である。

これらの資料は、本稿における技術比較の背景を示すものであり、TPCA の状態遷移単方向性の理論的出典を示すものではない。

1. **PLCopen — IEC 61131-3**  
   IEC 61131-3 の Sequential Function Chart（SFC）は、ステップ、遷移、アクションを用いて PLC プログラムのシーケンス構造を表現する。  
   https://www.plcopen.org/standards/logic/iec-61131-3/

2. **PLCopen — SFC FAQ / Structuring with SFC**  
   PLCopen の公開資料では、SFC において既存ステップへ戻る分岐構造を表現できることが説明されている。本稿では、この状態タイプ上の再進入と、実際の状態インスタンスを区別して扱う。  
   https://www.plcopen.org/standards/logic/iec-61131-3/faqs/

3. **OMAC — PackML**  
   PackML は、機械・ユニットにおける標準化された状態と動作モデルを提供し、設備間で共通した運転状態表現に使用される。  
   https://www.omac.org/packml

---

## 文書情報

題目："TPCA の状態遷移単方向性 ― なぜ実システムでは過去の状態インスタンスへ戻らないのか？"  
文書種別：技術ノート  
バージョン：Public Note Version 1.0  
初回公開日：2026-08-21  
最終更新日：2026-08-21  
著者：全野南政 / Nansei Zenno  
現在の URL：https://zennns.com/jp/notes/tpca-unidirectional-state-transition/

---

本稿は、TPCA / PCN 状態遷移前制御体系の公開説明資料である。
