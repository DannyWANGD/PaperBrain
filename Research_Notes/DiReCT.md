---
tags:
- paper
- domain/reinforcement_learning
- domain/world_model
- impact/high_value
- method/diffusion_policy
- method/foundation_model
- method/reinforcement_learning
- review/auto_tagged
- status/unread
- task/navigation
- task/scene_understanding
- task/video_prediction
- type/system
aliases:
- 'DiReCT: Disentangled Regularization of Contrastive Trajectories for Physics-Refined
  Video Generation'
url: http://arxiv.org/abs/2603.25931v1
pdf_url: https://arxiv.org/pdf/2603.25931v1
local_pdf: '[[DiReCT Disentangled Regularization of Contrastive Trajectories for PhysicsRefined
  Video Generation.pdf]]'
github: None
project_page: None
publication_date: Unknown
score: '8.0'
domains:
- reinforcement_learning
methods:
- diffusion_policy
- foundation_model
- reinforcement_learning
tasks:
- navigation
- scene_understanding
- video_prediction
paper_type: system
impact_band: high_value
reading_status: unread
year: null
priority_score: 95
review_status: auto_tagged
next_action: inspect_protocol
arxiv_id: '2603.25931'
paper_id: arxiv:2603.25931
---

# DiReCT: Disentangled Regularization of Contrastive Trajectories for Physics-Refined Video Generation

## 📌 Abstract
Flow-matching video generators produce temporally coherent, high-fidelity outputs yet routinely violate elementary physics because their reconstruction objectives penalize per-frame deviations without distinguishing physically consistent dynamics from impossible ones. Contrastive flow matching offers a principled remedy by pushing apart velocity-field trajectories of differing conditions, but we identify a fundamental obstacle in the text-conditioned video setting: semantic-physics entanglement. Because natural-language prompts couple scene content with physical behavior, naive negative sampling draws conditions whose velocity fields largely overlap with the positive sample's, causing the contrastive gradient to directly oppose the flow-matching objective. We formalize this gradient conflict, deriving a precise alignment condition that reveals when contrastive learning helps versus harms training. Guided by this analysis, we introduce DiReCT (Disentangled Regularization of Contrastive Trajectories), a lightweight post-training framework that decomposes the contrastive signal into two complementary scales: a macro-contrastive term that draws partition-exclusive negatives from semantically distant regions for interference-free global trajectory separation, and a micro-contrastive term that constructs hard negatives sharing full scene semantics with the positive sample but differing along a single, LLM-perturbed axis of physical behavior; spanning kinematics, forces, materials, interactions, and magnitudes. A velocity-space distributional regularizer helps to prevent catastrophic forgetting of pretrained visual quality. When applied to Wan 2.1-1.3B, our method improves the physical commonsense score on VideoPhy by 16.7% and 11.3% compared to the baseline and SFT, respectively, without increasing training time.

## 🖼️ Architecture
![[DiReCT Disentangled Regularization of Contrastive Trajectories for PhysicsRefined Video Generation_arch.png]]

## 🧠 AI Analysis
Analysis Failed: All models unavailable.

## 📂 Resources
- **Local PDF**: [[DiReCT Disentangled Regularization of Contrastive Trajectories for PhysicsRefined Video Generation.pdf]]
- [Online PDF](https://arxiv.org/pdf/2603.25931v1)
- [ArXiv Link](http://arxiv.org/abs/2603.25931v1)
