---
tags:
- paper
- domain/embodied_ai
- domain/multimodal_perception
- domain/robot_manipulation
- domain/vla
- impact/solid
- method/foundation_model
- method/planning
- review/auto_tagged
- status/unread
- task/loco_manipulation
- task/manipulation
- task/navigation
- task/planning_reasoning
- task/scene_understanding
- type/system
aliases:
- 'ROSClaw: An OpenClaw ROS 2 Framework for Agentic Robot Control and Interaction'
url: http://arxiv.org/abs/2603.26997v1
pdf_url: https://arxiv.org/pdf/2603.26997v1
local_pdf: '[[ROSClaw An OpenClaw ROS 2 Framework for Agentic Robot Control and Interaction.pdf]]'
github: None
project_page: None
publication_date: Unknown
score: '7.0'
domains:
- embodied_ai
- multimodal_perception
- robot_manipulation
- vla
methods:
- foundation_model
- planning
tasks:
- loco_manipulation
- manipulation
- navigation
- planning_reasoning
- scene_understanding
paper_type: system
impact_band: solid
reading_status: unread
year: null
priority_score: 78
review_status: auto_tagged
next_action: inspect_protocol
arxiv_id: '2603.26997'
paper_id: arxiv:2603.26997
---

# ROSClaw: An OpenClaw ROS 2 Framework for Agentic Robot Control and Interaction

## 📌 Abstract
Foundation models can endow robots with open-ended reasoning, language understanding, and adaptive planning, yet connecting a model to a physical robot today requires bespoke integration that couples perception, actuation, and safety to a single model and platform. We present ROSClaw, a model-agnostic executive layer that integrates the OpenClaw agent runtime with ROS 2, enabling any foundation model to perceive, reason about, and act on any ROS-enabled robot through (i) dynamic capability discovery with standardized affordance injection, (ii) multimodal observation normalization, (iii) pre-execution action validation within a configurable safety envelope, and (iv) structured audit logging. Swapping model backends or robot platforms is a configuration change; tool schemas, safety enforcement, and provenance logging remain invariant. We deploy ROSClaw on three platforms (wheeled, quadruped, humanoid) with four foundation-model backends. Under this controlled substrate, models exhibit up to 4.8 x differences in out-of-policy action proposal rates (3.4 x among frontier models alone) and produce qualitatively distinct physical behaviors from identical commands. A cross-framework parity protocol against ROSA confirms that executive-layer design, not just prompt wording, significantly affects both task completion and safety behavior, establishing ROSClaw as both practical agentic-robot infrastructure and a reproducible measurement instrument for embodied AI.

## 🖼️ Architecture
![[ROSClaw An OpenClaw ROS 2 Framework for Agentic Robot Control and Interaction_arch.png]]

## 🧠 AI Analysis
Analysis Failed: All models unavailable.

## 📂 Resources
- **Local PDF**: [[ROSClaw An OpenClaw ROS 2 Framework for Agentic Robot Control and Interaction.pdf]]
- [Online PDF](https://arxiv.org/pdf/2603.26997v1)
- [ArXiv Link](http://arxiv.org/abs/2603.26997v1)
