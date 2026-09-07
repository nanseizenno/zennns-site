---
title: "TPCA / PCN"
description: "Transition Pre-Control Architecture and Pre-Control Node"
translationKey: "home"
---

# TPCA / PCN

## Transition Pre-Control Architecture

**Nansei Zenno**

TPCA / PCN is an engineering framework for controlling state transitions before a system enters a defined target state, execution path, or physical execution stage.

Its core engineering object is a clearly defined **Target State Entry**.

A **PCN (Pre-Control Node)** is placed before that entry to organize relevant system states, evaluate whether the transition can proceed, determine the appropriate controlled path for the resulting outcome, and record the judgment history.

**Within a PCN, relevant states are mapped by their role in the target-state transition into Condition, Authority, and Execution Chain, and are evaluated for structural integrity, dynamic validity, and control boundaries. This makes previously distributed transition checks explicit, structured, and traceable.**

TPCA / PCN can be applied to areas such as:

- industrial automation and execution units;
- multi-agent and collaborative control systems;
- MES / WCS and manufacturing DX;
- digital and AI invocation control.

The framework does not replace PLCs, state machines, safety control, interlocks, MES, WCS, or existing execution systems.

Instead, it focuses on how multiple existing states and control conditions can be organized around one explicit Target State Entry before the transition occurs.

The core concepts and terminology are introduced here:

[Core Concepts](/en/concepts/)

Additional English materials, including application cases and technical notes, will be added progressively.

## Public Use and Intellectual Property

Public materials on this website may be referenced for technical discussion, evaluation, and engineering study.

Publication of these materials does not constitute a patent license, technology transfer, or authorization to use non-public implementation details.

For intellectual property information and usage boundaries, see:

[About](/en/about/)
