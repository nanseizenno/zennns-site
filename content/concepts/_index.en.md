---
title: "Concepts"
draft: false
---
This page defines the basic terms used in the TPCA / CAE-SDB framework.  
The definitions are written for engineering use and are intended to keep public materials, case descriptions, cooperation documents, and technical notes consistent.

---

## TPCA

Full name: Transition Pre-Control Architecture

TPCA is an engineering architecture for structured judgment and multi-path control before a system enters a target state, target execution path, or target physical execution phase.

The main role of TPCA is to check condition, authority, and execution chain before state transition, and to output the corresponding control path based on the judgment result.

---

## PCN

Full name: Pre-Control Node

A PCN is an engineering node placed before entry into a target state.

It performs state acquisition, signal organization, C / A / E mapping, S / D / B judgment, control output, and state logging.  
In an automated execution unit, a PCN may be implemented as a PLC function block, an HMI diagnostic module, an edge controller module, or a software judgment node.

---

## CAE-SDB

Full name: CAE-SDB Matrix

CAE-SDB is a pre-control judgment matrix formed by combining the C / A / E state-variable domains with the S / D / B judgment properties.

It is used to identify the source of a pre-transition issue, the nature of the issue, and the next control path.  
Its output includes control results such as allow entry, wait, re-identify, return flow, degrade execution, block entry, safety lock, and manual confirmation.

---

## C

Full name: Condition

C represents the condition state.

It indicates whether the site conditions, object conditions, recognition conditions, data conditions, task conditions, or other prerequisites required for entering the target state are satisfied.  
Examples include object presence, valid position, valid recognition result, existing task, complete parameters, and completion of the previous phase.

---

## A

Full name: Authority

A represents the authority or permission state.

It indicates whether the system is allowed to enter the target state.  
Typical items include safety permission, upper-system permission, area permission, manual confirmation, access rights, authorization, resource lock, and receiving permission from another device.

A critical authority item may act as an independent necessary constraint.  
When safety permission, authorization, resource lock, or area permission is not satisfied, entry into the target state must not be allowed even if the condition state and execution chain state are satisfied.

---

## E

Full name: Execution Chain

E represents the execution chain state.

It indicates whether the execution chain can continue after the system enters the target state.  
E is not equivalent to the ready state of a single device.

The execution chain may include the main device, end effector, downstream receiver, alternative path, return path, abnormal discharge path, result upload path, or write-back path.  
For example, robot ready is only a local state. Whether the downstream process can receive the object, whether an abnormal object can be discharged, and whether the result can be written back are also part of E.

---

## S

Full name: Structure

S represents structural completeness.

It checks whether the signals, interfaces, mapping relationships, authority sources, paths, and execution-chain boundaries required before entering the target state are defined, connected, and observable.  
Typical issues include undefined signals, disconnected interfaces, unclear authority sources, and missing execution-chain boundaries.

---

## D

Full name: Dynamics

D represents dynamic and timing validity.

It checks whether operating signals are valid, synchronized, stable, and reliable.  
Typical issues include timeout, stale signal, chattering, conflict, delay, asynchrony, low confidence, revoked permission, and state transition in progress.

---

## B

Full name: Boundary

B represents the control boundary.

It determines the processing path to be used when the system is in an incomplete or boundary state.  
Typical actions include wait, retry, re-identify, return flow, degrade, block entry, safety lock, manual confirmation, and abnormal isolation.

The purpose of B is to define the next control boundary instead of compressing a boundary state into a simple NG or alarm.

---

## Multi-path Control

Multi-path control refers to the control paths generated from the CAE-SDB judgment result.

Typical control outputs include allow entry, wait, re-identify, resample, reposition, return flow, abnormal diversion, downstream coordination, resource release, degrade execution, backup path, block entry, safety lock, manual confirmation, abnormal isolation, and state logging.

Multi-path control converts different pre-transition failure factors into engineering actions that can be executed, displayed, and recorded.

---

## State Logging and Traceability

State logging and traceability refer to the recording of current state, target state, multi-source state signals, C / A / E mapping results, S / D / B judgment results, control outputs, and time information.

These records support on-site review, issue tracing, design audit, project handover, and continuous improvement.  
In a productized system, they can also serve as structured data sources for MES / WCS, HMI, SCADA, and AI analysis modules.
