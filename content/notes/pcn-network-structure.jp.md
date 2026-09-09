---
title: "複数の PCN はどのように状態遷移前制御ネットワークを形成するのか？"
summary: "複数の Target State Entry とそれぞれに対応する PCN が、状態遷移、許可、資源、実行、状態更新などの依存関係によって PCN Network を形成する考え方を説明する。"
description: "PCN Network の定義、PCN 間のエンジニアリング上の依存関係、Runtime、PCN Trace を用いた分析価値、および代表的な適用形態を整理する。"
date: 2026-07-04
lastmod: 2026-09-08
author: "全野南政 / Nansei Zenno"
document_type: "技術ノート"
version: "Public Note Version 1.4"
citation_url: "https://zennns.com/jp/notes/pcn-network-structure/"
draft: false
ShowReadingTime: true
ShowToc: true
TocOpen: true
---

## 複数の PCN はどのように状態遷移前制御ネットワークを形成するのか？

1 つの PCN（Pre-Control Node / 前制御ノード）は、1 つの明確な Target State Entry に対応する。

複雑なエンジニアリングシステムには、連続、並列、分岐、循環、または相互依存する複数の Target State Entry が存在する。

それぞれの Target State Entry に対応する PCN を、実際の状態遷移関係とエンジニアリング上の依存関係に基づいて関連付けることで、PCN Network を構成する。

PCN Network は、

> **複数の Target State Entry と、それぞれに対応する PCN、およびそれらの間に存在する状態遷移・許可・資源・実行・状態更新などの依存関係を表すエンジニアリング上の関係構造**

である。

基本概念については、以下を参照。

- [Concepts｜基本概念](/jp/concepts/)
- [TPCA / PCN 状態遷移前制御アーキテクチャ｜ホワイトペーパー](/jp/whitepaper/)
- [なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)

---

## 1. PCN Network のノードは Target State Entry / PCN である

PCN Network では、独立して設計・判定・制御・記録する価値のある Target State Entry をノード対象とする。

例えば、次のような Target State Entry に PCN を設定できる。

| 状態遷移 | 対応する PCN |
|---|---|
| ロボット待機 → ピックアップ段階 | ピックアップ前 PCN |
| 配置完了 → 圧入段階 | 圧入前 PCN |
| 検査待ち → 検査段階 | 検査前 PCN |
| タスク生成済み → 実行状態 | タスク実行前 PCN |
| AGV 到着 → ステーション受入状態 | ステーション受入前 PCN |
| 保全解除 → 自動運転再開 | 自動運転再開前 PCN |

設備、PLC、ロボットコントローラ、MES、WCS、品質システムなどは、各 PCN に必要な状態を提供する。

PCN の設定単位は、設備台数やコントローラ台数ではなく、Target State Entry の位置によって決まる。

そのため、

- 1 台の複雑設備内に複数の PCN を設定できる。
- 1 本の生産ラインに複数の PCN を設定できる。
- MES / WCS と現場設備をまたぐ Target State Entry に PCN を設定できる。
- 人による確認や品質放行を含む Target State Entry も PCN Network に含めることができる。

PCN Network は、このような複数の Target State Entry / PCN を関係付けることで形成される。

---

## 2. PCN 間を接続するエンジニアリング関係

PCN Network における PCN 間の接続は、実際の状態遷移とエンジニアリング上の依存関係に基づいて設定する。

代表的な関係は次の通りである。

```text
状態進行関係

許可依存関係

資源依存関係

実行依存関係

状態更新依存関係
```

### 2.1 状態進行関係

ある状態遷移が完了し、新しい Current State が形成された後、その状態から後続の Target State Entry へ進む関係である。

例えば、

```text
ピックアップ待ち
→ ピックアップ前 PCN
→ ピックアップ完了

ピックアップ完了
→ 配置前 PCN
→ 配置完了

配置完了
→ 後続段階 PCN
→ 後続実行
```

のように構成できる。

各 PCN は、それぞれ異なる Target State Entry に対応する。

### 2.2 許可依存関係

ある PCN が使用する許可状態が、他の設備、システム、人による処理、または前段の状態遷移結果に依存する関係である。

例えば、

- 品質放行状態
- エリア進入許可
- 上位システムからの実行許可
- 相手機器からの受入許可
- 人による確認状態

などがある。

これらは、該当する PCN における A：Authority に関係する状態として使用できる。

### 2.3 資源依存関係

複数の PCN が同じ共有資源に依存する関係である。

例えば、

- 共有経路
- バッファ
- 自動扉
- エレベータ
- 治具
- ステーション
- 共有アクチュエータ

などがある。

共有資源の状態は、複数の Target State Entry に同時に影響する場合がある。

### 2.4 実行依存関係

Target State へ進入した後の実行が、他の設備、経路、下流システムなどの状態に依存する関係である。

例えば、

- 下流設備の受入状態
- 代替経路の利用状態
- 異常処理経路の利用状態
- 結果送信経路の状態
- 後続工程の承接状態

などがある。

これらは、該当する PCN における E：Execution Chain に関係する状態として使用できる。

### 2.5 状態更新依存関係

ある PCN に関係する実行結果や状態変化が、後続 PCN の入力状態へ影響する関係である。

例えば、

```text
工程完了
→ MES / PLC / WCS の状態更新
→ 後続 PCN が更新後の状態を取得
→ 次の Target State Entry を判定
```

という関係である。

PLC、MES、WCS、品質システムなどへの状態書戻しは、この状態更新依存の一例である。

---

## 3. PCN Network が取り得る構造

PCN Network は、対象システムの実際の状態遷移と依存関係に応じて複数の構造を取ることができる。

代表的には、

- 連続
- 並列
- 分岐
- 循環
- 相互依存
- システム横断

などである。

### 連続

```text
PCN-A
→ State Transition
→ PCN-B
→ State Transition
→ PCN-C
```

### 並列

```text
          → PCN-B
PCN-A
          → PCN-C
```

### 分岐

```text
PCN-A
   ├→ PCN-B
   └→ PCN-C
```

### 循環

状態タイプの関係として、例えば、

```text
A → B → C → A
```

のような循環を含むことができる。

実運転では、同じ State Type へ再進入した場合も、新しい State Instance が時間方向へ継続して生成される。

```text
A₁ → B₁ → C₁ → A₂
```

この状態インスタンスの扱いについては、以下を参照。

- [TPCA における状態インスタンスの単方向性 ― 状態タイプの循環と実運転履歴の違い](/jp/notes/tpca-unidirectional-state-transition/)

### システム横断

PCN Network は、PLC、ロボット、MES、WCS、品質システムなど、複数のシステムをまたぐ Target State Entry 間の関係も表現できる。

重要なのは、PCN の実装位置そのものより、どの Target State Entry が存在し、それらの間にどのようなエンジニアリング関係があるかを明確にすることである。

---

## 4. PCN Network と Runtime

各 PCN は、それぞれの Target State Entry において、オンラインで関連状態を取得し、判定と制御を行う。

PCN Runtime は、単一 PCN のオンライン運転を支える実行基盤として位置付ける。

PCN Network は、複数の Target State Entry / PCN 間に存在する状態遷移と依存関係を表す関係層である。

そのため、複数の PCN は異なる実装位置に配置できる。

例えば、

- PLC / HMI
- 産業用コントローラ
- エッジコントローラ
- WCS
- MES
- ソフトウェアサービス

などである。

各 PCN の Runtime は対象システムに応じて構成し、Network 上では PCN 間の状態進行、許可、資源、実行、状態更新などの関係を扱う。

Runtime の内部ライフサイクル、PCN 間プロトコル、同期機構、詳細なインターフェース、完全な Arbitration ルールなどは、本公開ノートの対象外とする。

---

## 5. PCN Network と PCN Trace

単一 PCN は、1 回の Target State Entry に対する PCN Trace を形成する。

PCN Trace には、その Target State Entry における状態、判定、制御、実行結果などを記録する。

複数の PCN Trace を PCN Network 上の関係と対応付けることで、単一の Target State Entry だけでは見えにくいシステムレベルの関係を分析できる。

例えば、

```text
PCN-A
許可更新の遅延
    ↓
PCN-B
Wait 長期化
```

のように、前段の状態変化や許可依存が後続 PCN の待機へ影響している関係を確認できる。

また、

```text
PCN-C
共有資源を占有
    ↓
PCN-D / PCN-E
Target State Entry で待機
```

のように、共有資源を介した複数 PCN 間の影響も分析対象にできる。

PCN Network と PCN Trace を組み合わせることで、例えば次の内容を確認できる。

- どの Target State Entry で問題が頻発しているか。
- どの PCN 間で許可依存による待機が繰り返されているか。
- どの共有資源が複数 PCN の進入に影響しているか。
- どの Execution Chain に関係する問題が後続 PCN へ波及しているか。
- どの状態更新関係で遅延や不整合が繰り返されているか。
- エンジニアリング変更後に、関連する複数 PCN の判定結果や実行結果がどのように変化したか。

このように、PCN Network は PCN Trace に PCN 間の関係情報を与え、状態遷移入口単位の履歴分析をシステムレベルへ拡張するための構造として利用できる。

PCN Trace については、以下を参照。

- [なぜ PCN Trace は新しいエンジニアリングデータなのか？](/jp/notes/why-pcn-trace-is-engineering-data/)

---

## 6. 3つの代表的な PCN Network 形態

### 6.1 自動化実行ユニット

1つの自動化実行ユニット内でも、複数の主要な Target State Entry を設定できる。

例えば、

```text
待機
→ ピックアップ前 PCN
→ ピックアップ

ピックアップ完了
→ 配置前 PCN
→ 配置

配置完了
→ 後続段階 PCN
→ 後続実行
```

という構成である。

この場合、PCN 間では主に状態進行、許可、実行チェーンなどの関係を扱う。

### 6.2 MES / WCS・複数設備協調

MES / WCS と複数設備が連携する場合、Target State Entry はシステム間にまたがって存在する。

例えば、

```text
タスク生成
→ タスク実行前 PCN
→ 実行

ステーション到着
→ ステーション受入前 PCN
→ 引渡し

実行完了
→ 状態更新
→ 後続 PCN
```

という構成である。

この場合、タスク、資源、経路、ステーション、許可、Execution Chain、状態更新などの依存関係を PCN Network 上で整理できる。

### 6.3 製造 DX・システム間状態遷移

設備、人、MES、品質システム、保全システムなどをまたぐ状態遷移にも PCN Network を適用できる。

例えば、

```text
品質確認
→ 次工程前 PCN
→ 工程進入

保全解除
→ 自動運転再開前 PCN
→ 運転再開

作業指示切替
→ 目標生産状態前 PCN
→ 新しい生産状態
```

という構成である。

このようなシステム横断の状態遷移でも、各 Target State Entry と依存関係を PCN Network として整理できる。

---

## まとめ

1つの PCN は、1つの明確な Target State Entry に対応する。

複数の PCN を、実際の状態遷移関係とエンジニアリング上の依存関係に基づいて関連付けることで PCN Network を形成する。

PCN Network が扱う代表的な関係は、

```text
状態進行
許可依存
資源依存
実行依存
状態更新依存
```

である。

Network は、連続、並列、分岐、循環、システム横断など、対象システムに応じた構造を取ることができる。

各 PCN Runtime は、それぞれの Target State Entry におけるオンライン判定と制御を支え、PCN Network は複数 PCN 間の関係構造を表す。

さらに、各 PCN の PCN Trace を Network 上の関係と対応付けることで、単一入口の履歴から、複数 Target State Entry 間の依存関係、問題連鎖、共有資源影響、状態更新影響などの分析へ展開できる。

したがって、PCN Network は、

> **複数の Target State Entry を個別の PCN として明確化し、それらの状態遷移と依存関係をシステムレベルで設計・確認・分析するための関係構造**

として位置付けられる。

---

## 関連技術ノート

- [なぜ PCN は TPCA の最小エンジニアリングノードなのか？](/jp/notes/pcn-minimum-engineering-unit/)
- [TPCA における状態インスタンスの単方向性 ― 状態タイプの循環と実運転履歴の違い](/jp/notes/tpca-unidirectional-state-transition/)
- [なぜ PCN Trace は新しいエンジニアリングデータなのか？](/jp/notes/why-pcn-trace-is-engineering-data/)
- [TPCA / PCN の適用場面分析](/jp/notes/tpca-pcn-applicable-scenarios/)

---

## 文書情報

題目：複数の PCN はどのように状態遷移前制御ネットワークを形成するのか？  
文書種別：技術ノート  
バージョン：Public Note Version 1.4  
初回公開日：2026-07-04  
最終更新日：2026-09-08  
著者：全野南政 / Nansei Zenno  
現在の URL：https://zennns.com/jp/notes/pcn-network-structure/

---

本稿は、TPCA / PCN 状態遷移前制御体系の公開説明資料である。
