---
title: "Core Concepts"
summary: "Core terminology of the TPCA / PCN state-transition pre-control framework, including Current State, Target State, Target State Entry, TPCA, PCN, C / A / E, S / D / B, CAE-SDB Result, Arbitration, Multipath Control, PCN Trace, PCN Runtime, and PCN Network."
description: "Defines the core terminology and relationships within TPCA / PCN, including Target State Entry, PCN, C / A / E Mapping, S / D / B Evaluation, CAE-SDB Result, time information T, Arbitration, Multipath Control, PCN Trace, PCN Runtime, and PCN Network."
draft: false
date: 2026-07-04
lastmod: 2026-09-07
author: "Nansei Zenno"
ShowReadingTime: false
ShowToc: true
TocOpen: true
---

This page defines the core terminology used in the TPCA / PCN state-transition pre-control framework.

The terminology is intended for public technical explanations, application cases, engineering discussions, and future technical documentation.

The core proposition of TPCA / PCN is:

> **A clearly defined Target State Entry should be treated as an engineering object that can be independently designed, evaluated, controlled, and recorded.**

---

## Core Terminology

| Term | Meaning | Basic Role |
|---|---|---|
| TPCA | Transition Pre-Control Architecture | Overall pre-control architecture organized around a clearly defined Target State Entry |
| PCN | Pre-Control Node | Engineering node placed before a specific Target State Entry |
| Current State | Current state | The state, stage, or path position currently occupied by the system |
| Target State | Target state | The next state, execution path, or physical execution stage that the system is intended to enter |
| Target State Entry | Target-state entry point | The engineering point at which pre-control is performed before entering the Target State |
| C | Condition | Determines whether the factual prerequisites required for the Target State are satisfied |
| A | Authority | Determines whether the system is permitted to enter the Target State |
| E | Execution Chain | Determines whether the execution chain can continue after entry into the Target State |
| S | Structure | Evaluates whether required signals, interfaces, mappings, authority sources, and execution-chain boundaries are structurally established |
| D | Dynamics | Evaluates whether relevant states remain dynamically valid, synchronized, stable, current, and effective |
| B | Boundary | Evaluates whether relevant states remain within predefined control boundaries |
| CAE-SDB | Structured evaluation logic | Combines C / A / E state roles with S / D / B evaluation properties |
| CAE-SDB Result | Structured evaluation result | One or more structured results produced by a pre-control evaluation |
| T | Time information | Time-related information retained with states and evaluation results |
| Arbitration | Control arbitration | Resolves priorities among evaluation results and predefined control constraints |
| Multipath Control | Multi-path control output | Determines the controlled path following Arbitration |
| PCN Trace | State-transition decision trace | Records the inputs, evaluations, time information, control output, and execution result of a Target State Entry |
| PCN Runtime | PCN runtime | Runtime layer that performs online evaluation, arbitration, control output, and trace generation |
| PCN Network | PCN network | A pre-control structure formed by multiple PCNs connected through state-transition and dependency relationships |

The basic engineering relationship is:

```text
Current State
→ Target State
→ Target State Entry / PCN
→ Multi-source State Signals
→ C / A / E Mapping
→ S / D / B Evaluation
→ CAE-SDB Result + T
→ Arbitration
→ Multipath Control
→ PCN Trace
```

PCN Runtime executes this process in an operating system.

Multiple PCNs can be connected according to their Target State Entries and state-transition relationships to form a PCN Network.

---

## Current State, Target State, and Target State Entry

**Current State** is the state, stage, or path position occupied by the system before a state transition.

**Target State** is the next state, target execution path, or target physical execution stage that the system is intended to enter.

**Target State Entry** is the engineering point immediately before the system moves from the Current State into the Target State, where pre-control evaluation is performed.

TPCA / PCN focuses on the engineering decision made before the system actually enters the Target State.

Typical transitions include:

- Waiting Stage → Pick Stage
- Placement Complete → Pressing Stage
- Inspection Waiting → Inspection Execution
- Task Exists → Task Execution
- AGV Arrival → Station Acceptance
- Current Request → Target Invocation Path

A Target State is not limited to the next state in the normal production flow.

Rework, return flow, fallback, exception routing, re-entry, alternative execution paths, and other states that require a new entry decision may also become Target States.

From the runtime perspective of TPCA, these are represented as:

```text
Current State → New Target State
```

Even when a later Target State has the same or similar engineering content as a previous state, it represents a new state instance in actual operation.

The Current State, Target State, and Target State Entry must therefore be clearly defined. Without them, a PCN does not have a definite object for pre-control evaluation.

---

## Pre-Control

Pre-Control refers to the structured evaluation of relevant multi-source states before a system enters a Target State, target execution path, or target physical execution stage.

Based on the complete evaluation result, the system determines whether the transition may proceed and which controlled path should be taken.

Pre-Control can include evaluation of:

- whether required conditions are satisfied;
- whether required authority is established;
- whether the execution chain can continue;
- whether the required engineering structure is complete;
- whether the current states remain dynamically valid;
- whether predefined control boundaries have been reached;
- how multiple evaluation results should be arbitrated;
- which Target State or controlled execution path should follow.

Pre-Control occurs before entry into the Target State.

Its engineering position is therefore different from post-failure diagnosis or simple alarm classification.

---

## TPCA

**Transition Pre-Control Architecture**

TPCA is the overall architecture for pre-control around a clearly defined Target State Entry.

It organizes states that may otherwise be distributed across equipment, control programs, MES / WCS, safety systems, manual confirmation processes, and other engineering interfaces around the same Target State Entry.

The basic engineering chain is:

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

{{< pcn-animation >}}

TPCA does not replace PLCs, state machines, SFCs, interlocks, safety control, MES, or WCS.

When multiple existing mechanisms jointly determine whether a state transition can occur, TPCA organizes their relevant states, pre-control evaluation, control result, and decision trace around one explicit Target State Entry.

TPCA also retains time-related information associated with states and evaluations.

Real system transitions proceed forward in time. Even when a later state has the same engineering content as an earlier state, it represents a new state instance in actual operation.

---

## PCN

**Pre-Control Node**

A PCN is an engineering node placed before one clearly defined Target State Entry.

One PCN corresponds to one explicit Target State Entry and can perform:

- confirmation of the Current State and Target State;
- acquisition and organization of multi-source states;
- C / A / E Mapping;
- S / D / B Evaluation;
- generation of CAE-SDB Result;
- retention of time information T;
- Arbitration;
- Multipath Control output;
- generation of PCN Trace.

The implementation form of a PCN is not fixed.

In an automated execution unit, a PCN may be implemented as a PLC function block, an industrial edge-control module, or a software evaluation node.

In MES / WCS, AGV / AMR fleet control, manufacturing DX, or digital systems, a PCN may be placed before task execution, resource release, station acceptance, state recovery, or entry into a target invocation path.

---

## PCN Runtime

**PCN Runtime** is the runtime layer that performs online state processing, evaluation, control output, and trace generation for a PCN.

For a specific Target State Entry, PCN Runtime can perform:

- state acquisition and organization;
- C / A / E Mapping;
- S / D / B Evaluation;
- generation of CAE-SDB Result;
- retention of time information;
- Arbitration;
- Multipath Control output;
- PCN Trace generation.

PCN Runtime describes a runtime role rather than a fixed implementation platform.

It may be implemented in software, PLCs, industrial edge controllers, MES / WCS plug-ins, or other suitable systems.

Detailed Runtime architecture, configuration structures, Rule Packs, complete Arbitration logic, control priorities, key parameters, interfaces, and deployment implementation are outside the general public scope of this website.

---

## PCN Network

A **PCN Network** is a pre-control structure formed by multiple PCNs connected according to actual state-transition relationships and the necessary authority, resource, and execution dependencies between them.

A single PCN corresponds to one explicit Target State Entry.

Multiple PCNs may be distributed across equipment units, production lines, MES / WCS, AGV / AMR fleet-control layers, manufacturing DX systems, or digital systems.

A PCN Network describes engineering relationships between Target State Entries.

It is not defined simply by the physical connections between devices.

For example:

```text
State A
→ PCN-1
→ State B
→ PCN-2
→ State C
```

When a system enters rework, return flow, exception routing, re-entry, or another execution path, a new Target State Entry and the corresponding PCN may also be formed.

State-type relationships within a PCN Network may form cycles, while actual state instances continue to be generated forward in time.

Such cycles describe relationships among state types or transition paths, not a reversal of runtime history. Each actual state instance occurs at a new point in time and remains uniquely traceable.

A PCN Network can be used to observe relationships involving:

- state progression;
- authority dependencies;
- resource dependencies;
- execution-chain continuity;
- state write-back;
- decision traces.

---

## Multi-source State Signals

Multi-source state signals are input information directly relevant to the current Target State Entry.

Signal sources may include:

- PLCs;
- robot controllers;
- vision systems;
- safety systems;
- HMI / SCADA;
- MES;
- WCS;
- AGV / AMR fleet-control systems;
- field sensors;
- supervisory systems;
- manual confirmation;
- digital-system interfaces.

A PCN maps relevant states into C / A / E according to the engineering role that each state plays in the current Target State Entry.

The mapping is not determined simply by the source system.

The same signal may play different roles at different Target State Entries.

Multi-source state information must therefore be interpreted together with the Current State, Target State, and Target State Entry.

Depending on the system, state information may also include:

- timestamps;
- update times;
- state versions;
- sequence information;
- lot numbers;
- object IDs;
- event IDs;
- other traceability information related to the current transition.

---

## CAE-SDB

CAE-SDB is the structured evaluation logic used within a PCN.

Its basic structure is:

```text
{C, A, E} × {S, D, B}
```

where:

- C / A / E represent state-variable roles;
- S / D / B represent evaluation properties applied to those states.

Together they define a 3 × 3 available evaluation space:

|   | S | D | B |
|---|---|---|---|
| C | C-S | C-D | C-B |
| A | A-S | A-D | A-B |
| E | E-S | E-D | E-B |

A specific pre-control evaluation may produce one or more CAE-SDB Results, together with the relevant time information T.

A CAE-SDB Result is produced only when the corresponding evaluation has actually been executed and has produced a result.

When multiple results exist at the same Target State Entry, the relationship is:

```text
CAE-SDB Result + T
→ Arbitration
→ Multipath Control
```

CAE-SDB expands compressed operational states such as:

```text
false
NG
not ready
waiting
pending
blocked
```

into structured engineering results that identify both:

- the state-variable role involved; and
- the type of evaluation that produced the result.

---

## C: Condition

**Condition**

C represents whether the factual conditions required before entering the Target State are satisfied.

Typical examples include:

- whether a workpiece exists;
- whether position requirements are satisfied;
- whether recognition results are valid;
- whether a task exists;
- whether required parameters are complete;
- whether the preceding stage is complete;
- whether product or lot information is correct;
- whether the object can be correctly associated with the corresponding result.

C focuses on the factual prerequisites required for the Target State Entry.

---

## A: Authority

**Authority**

A represents whether the system is permitted to enter the Target State.

Typical examples include:

- safety permission;
- supervisory-system permission;
- area permission;
- manual confirmation;
- access rights or authorization;
- resource locks;
- permission from another device or system.

A critical Authority state can constitute an independent necessary constraint.

If a critical permission such as safety authorization, access authorization, resource ownership, or area permission is not established, the system must not enter the Target State even when C and E are otherwise satisfied.

A therefore answers:

> **Is the system allowed to enter this Target State?**

---

## E: Execution Chain

**Execution Chain**

E represents whether the execution chain associated with the current Target State can continue after the system enters that state.

E is not equivalent to the Ready state of an individual device.

Depending on the current Target State Entry, the execution chain may include:

- the primary equipment;
- the end effector;
- the required motion or execution path;
- downstream acceptance;
- counterpart-device acceptance;
- result transmission;
- result write-back;
- other links required for the current Target State to continue successfully.

For example, a robot may report:

```text
Robot Ready = TRUE
```

but this alone does not demonstrate that the complete execution chain for the current Target State is available.

E must always be evaluated in relation to the current Target State Entry.

Alternative, fallback, return-flow, or exception-routing paths may become separate candidate Target States or execution paths.

The availability of such an alternative path does not, by itself, establish E for the current Target State and does not justify an Allow decision for the current Target State Entry.

E therefore answers:

> **Can the execution chain continue after entering this Target State?**

---

## S: Structure

**Structure**

S is an evaluation property applied to C / A / E states.

S determines whether the engineering structure required for the Target State Entry has been defined, connected, and made observable.

Typical structural issues include:

- required signals are undefined;
- required interfaces are not connected;
- mapping relationships have not been established;
- the source of Authority is unclear;
- execution-chain boundaries are undefined;
- required states cannot be observed;
- relationships between objects and states have not been established.

S therefore evaluates whether the engineering structure required for the transition decision is complete.

---

## D: Dynamics

**Dynamics**

D is an evaluation property applied to C / A / E states.

D determines whether relevant runtime states remain valid, synchronized, stable, current, and reliable.

Typical dynamic issues include:

- timeout;
- no refresh;
- stale state;
- oscillation;
- conflict;
- delay;
- lack of synchronization;
- version mismatch;
- abnormal sequence relationship;
- low confidence;
- permission revocation;
- a state currently undergoing transition.

A state value being logically true does not necessarily mean that it remains valid for the current Target State Entry.

For example:

```text
Downstream Acceptable = TRUE
```

If the state has not been refreshed for an extended period, or was generated before a later downstream state change, the current value alone cannot establish that the execution chain remains valid.

D can therefore use information such as:

- timestamps;
- update times;
- sequence information;
- versions;
- object associations.

D answers:

> **Can this state still be used as valid evidence for the current Target State Entry?**

---

## B: Boundary

**Boundary**

B is an evaluation property applied to C / A / E states.

B determines whether a relevant state remains within a predefined control boundary.

Engineering parameters used for Boundary evaluation may include:

- allowable ranges;
- time windows;
- retry limits;
- confidence ranges;
- position-deviation limits;
- manual-confirmation validity periods;
- buffer capacity;
- degraded-operation boundaries;
- prohibition thresholds;
- other engineering limits associated with the Target State Entry.

B itself does not determine the final control action.

The Boundary result is passed to Arbitration together with other CAE-SDB Results.

---

## CAE-SDB Result

A **CAE-SDB Result** is a structured result produced after applying S / D / B evaluation to C / A / E states.

For example:

```text
C-D
```

indicates a Dynamics-related problem within the Condition domain.

```text
E-S
```

indicates a Structure-related problem within the Execution Chain domain.

A single Target State Entry may produce multiple results, for example:

```text
C-D + E-D
```

which indicates dynamic-validity problems in both the Condition and Execution Chain domains.

A CAE-SDB Result is created only when the corresponding S / D / B evaluation has actually been executed and produced a result.

Relevant time information T is retained together with the result.

CAE-SDB Result identifies:

- which C / A / E state role is involved; and
- which S / D / B evaluation property produced the result.

The result is then passed to Arbitration.

---

## Time Information T

T represents time-related information retained together with the state and CAE-SDB Result.

Depending on the system, T may include:

- Timestamp;
- update time;
- event time;
- sequence time;
- lot-related time;
- other information that establishes temporal relationships between states.

T is used to:

- identify the temporal position of the current state and evaluation;
- determine ordering relationships among states;
- support Dynamics evaluation;
- form the PCN Trace.

From the runtime perspective of TPCA, even when a later state has the same engineering content as a previous state, it represents a new state instance when it occurs at a different point in time.

---

## Arbitration

**Arbitration** processes the priority relationships among one or more CAE-SDB Results, critical Authority states, and predefined control constraints.

When multiple evaluation results exist at the same Target State Entry, the final control direction cannot be determined by a single CAE-SDB coordinate alone.

The engineering position of Arbitration is:

```text
CAE-SDB Result + T
→ Arbitration
→ Multipath Control
```

Relevant time information T is retained as part of the Arbitration context, allowing control rules to distinguish states with different timing, duration, freshness, or boundary conditions.

This website publicly explains the engineering role and position of Arbitration.

Detailed control priorities, short-circuit mechanisms, rule configuration, and complete arbitration implementation are outside the general public scope.

---

## Multipath Control

**Multipath Control** is the final engineering control output produced after the complete CAE-SDB Result has been processed through Arbitration.

Representative controlled paths may include:

- Allow;
- Wait;
- Re-identify;
- Re-sample;
- Reposition;
- Return flow;
- Fallback;
- Exception routing;
- Downstream coordination;
- Resource release;
- Degraded execution;
- Alternative path;
- Prohibit;
- Safety lock;
- Manual confirmation;
- Exception isolation;
- Enhanced recording.

Different control paths correspond to different subsequent engineering actions.

From the TPCA state-transition perspective, Multipath Control determines what controlled state or execution path should follow the current evaluation.

The basic relationship is:

```text
CAE-SDB Result + T
→ Arbitration
→ Multipath Control
```

Authority (A) is an input state used in the pre-control evaluation, whereas Allow is a final control output produced only after Arbitration. Therefore, A being satisfied does not by itself result in an Allow decision.

All Allow, Prohibit, and other Multipath Control outputs are bound to the current explicit Target State Entry.

An alternative, fallback, or return-flow path may be selected as a Multipath Control candidate.

However, the availability of such an alternative path does not mean that E for the current Target State has been established, and it does not justify an Allow decision for the current Target State Entry.

---

## PCN Trace

**PCN Trace** is the structured record of a state-transition pre-control evaluation and its resulting control outcome.

Its record unit corresponds to one Target State Entry.

Representative contents may include:

- Current State;
- Target State;
- multi-source states used in the evaluation;
- time information T;
- versions, sequences, or object information associated with the states;
- C / A / E Mapping;
- S / D / B Evaluation;
- CAE-SDB Result;
- Arbitration Result;
- Multipath Control;
- execution result;
- Trace ID.

PCN Trace can support:

- shop-floor review;
- problem tracing;
- state-transition design review;
- project handover;
- long-term comparison;
- engineering improvement.

Its basic record relationship is:

```text
Which Target State was being entered?
→ Which states were used as evidence?
→ Which structured results were produced?
→ How were those results arbitrated?
→ Which control path was selected?
→ Which state or path was actually reached?
```

Time information allows PCN Trace to distinguish state instances that have the same engineering content but occur at different points in time.

The detailed PCN Trace data structure is outside the general public scope of this website.

---

## Relationship Between the Core Concepts

The relationship between the main TPCA / PCN concepts can be represented as:

```text
TPCA
│
├─ PCN
│   │
│   ├─ PCN Runtime
│   │   │
│   │   ├─ C / A / E Mapping
│   │   ├─ S / D / B Evaluation
│   │   ├─ CAE-SDB Result + T
│   │   ├─ Arbitration
│   │   ├─ Multipath Control
│   │   └─ PCN Trace
│   │
│   └─ corresponds to one explicit Target State Entry
│
└─ Multiple PCNs
    ↓
   PCN Network
```

In summary:

- **TPCA**: the overall architecture;
- **PCN**: the engineering node associated with a specific Target State Entry;
- **PCN Runtime**: the runtime layer that performs online pre-control evaluation and control;
- **C / A / E**: state-variable roles;
- **S / D / B**: evaluation properties;
- **CAE-SDB Result**: structured evaluation result;
- **T**: time information retained with states and results;
- **Arbitration**: control arbitration;
- **Multipath Control**: controlled output path;
- **PCN Trace**: the trace of one Target State Entry evaluation;
- **PCN Network**: a state-transition pre-control network formed by multiple PCNs.

---

## Further Reading

Additional English application cases and technical notes will be added progressively.

---

This page is part of the public technical documentation of the TPCA / PCN state-transition pre-control framework.
