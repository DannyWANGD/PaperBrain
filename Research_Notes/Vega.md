---
tags:
- paper
- domain/embodied_ai
- domain/multimodal_perception
- domain/reinforcement_learning
- domain/vla
- domain/world_model
- impact/high_value
- method/benchmark
- method/diffusion_policy
- method/foundation_model
- method/planning
- method/reinforcement_learning
- review/auto_tagged
- status/unread
- task/navigation
- task/planning_reasoning
- task/scene_understanding
- type/benchmark
aliases:
- 'Vega: Learning to Drive with Natural Language Instructions'
url: http://arxiv.org/abs/2603.25741v1
pdf_url: https://arxiv.org/pdf/2603.25741v1
local_pdf: '[[Vega Learning to Drive with Natural Language Instructions.pdf]]'
github: None
project_page: None
publication_date: Unknown
score: '8.0'
domains:
- embodied_ai
- multimodal_perception
- reinforcement_learning
- vla
- world_model
methods:
- benchmark
- planning
- reinforcement_learning
tasks:
- navigation
- planning_reasoning
- scene_understanding
paper_type: benchmark
impact_band: high_value
reading_status: unread
year: null
priority_score: 107
review_status: auto_tagged
next_action: inspect_protocol
arxiv_id: '2603.25741'
paper_id: arxiv:2603.25741
---

# Vega: Learning to Drive with Natural Language Instructions

## 📌 Abstract
Vision-language-action models have reshaped autonomous driving to incorporate languages into the decision-making process. However, most existing pipelines only utilize the language modality for scene descriptions or reasoning and lack the flexibility to follow diverse user instructions for personalized driving. To address this, we first construct a large-scale driving dataset (InstructScene) containing around 100,000 scenes annotated with diverse driving instructions with the corresponding trajectories. We then propose a unified Vision-Language-World-Action model, Vega, for instruction-based generation and planning. We employ the autoregressive paradigm to process visual inputs (vision) and language instructions (language) and the diffusion paradigm to generate future predictions (world modeling) and trajectories (action). We perform joint attention to enable interactions between the modalities and use individual projection layers for different modalities for more capabilities. Extensive experiments demonstrate that our method not only achieves superior planning performance but also exhibits strong instruction-following abilities, paving the way for more intelligent and personalized driving systems.

## 🖼️ Architecture
![[Vega Learning to Drive with Natural Language Instructions_arch.png]]

## 🧠 AI Analysis
Analysis Failed: All models unavailable.

## 📂 Resources
- **Local PDF**: [[Vega Learning to Drive with Natural Language Instructions.pdf]]
- [Online PDF](https://arxiv.org/pdf/2603.25741v1)
- [ArXiv Link](http://arxiv.org/abs/2603.25741v1)


## Related Work Updates
- [ ] **2026-06-03**: New paper [[HideandSeek Failure Detection for VLA]] discusses *vega: learning to drive with natural language instructions*. Innovation: "Hide-and-Seek introduces inter- and intra-trajectory contrastive objectives to localize failure-indicative actions from trajectory-level labels without step-level annotation."