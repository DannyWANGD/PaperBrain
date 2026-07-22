---
tags:
- paper
- domain/reinforcement_learning
- domain/world_model
- impact/high_value
- method/benchmark
- method/diffusion_policy
- method/reinforcement_learning
- review/auto_tagged
- status/unread
- task/navigation
- type/benchmark
aliases:
- 'Persistent Robot World Models: Stabilizing Multi-Step Rollouts via Reinforcement
  Learning'
url: http://arxiv.org/abs/2603.25685v1
pdf_url: https://arxiv.org/pdf/2603.25685v1
local_pdf: '[[Persistent Robot World Models Stabilizing MultiStep Rollouts via Reinforcement
  Learning.pdf]]'
github: None
project_page: None
publication_date: Unknown
score: '8.0'
domains:
- reinforcement_learning
- world_model
methods:
- benchmark
- reinforcement_learning
tasks:
- navigation
paper_type: benchmark
impact_band: high_value
reading_status: unread
year: null
priority_score: 95
review_status: auto_tagged
next_action: inspect_protocol
arxiv_id: '2603.25685'
paper_id: arxiv:2603.25685
---

# Persistent Robot World Models: Stabilizing Multi-Step Rollouts via Reinforcement Learning

## 📌 Abstract
Action-conditioned robot world models generate future video frames of the manipulated scene given a robot action sequence, offering a promising alternative for simulating tasks that are difficult to model with traditional physics engines. However, these models are optimized for short-term prediction and break down when deployed autoregressively: each predicted clip feeds back as context for the next, causing errors to compound and visual quality to rapidly degrade. We address this through the following contributions. First, we introduce a reinforcement learning (RL) post-training scheme that trains the world model on its own autoregressive rollouts rather than on ground-truth histories. We achieve this by adapting a recent contrastive RL objective for diffusion models to our setting and show that its convergence guarantees carry over exactly. Second, we design a training protocol that generates and compares multiple candidate variable-length futures from the same rollout state, reinforcing higher-fidelity predictions over lower-fidelity ones. Third, we develop efficient, multi-view visual fidelity rewards that combine complementary perceptual metrics across camera views and are aggregated at the clip level for dense, low-variance training signal. Fourth, we show that our approach establishes a new state-of-the-art for rollout fidelity on the DROID dataset, outperforming the strongest baseline on all metrics (e.g., LPIPS reduced by 14% on external cameras, SSIM improved by 9.1% on the wrist camera), winning 98% of paired comparisons, and achieving an 80% preference rate in a blind human study.

## 🖼️ Architecture
![[Persistent Robot World Models Stabilizing MultiStep Rollouts via Reinforcement Learning_arch.png]]

## 🧠 AI Analysis
Analysis Failed: All models unavailable.

## 📂 Resources
- **Local PDF**: [[Persistent Robot World Models Stabilizing MultiStep Rollouts via Reinforcement Learning.pdf]]
- [Online PDF](https://arxiv.org/pdf/2603.25685v1)
- [ArXiv Link](http://arxiv.org/abs/2603.25685v1)


## Related Work Updates
- [ ] **2026-06-02**: New paper [[AFUN Affordance Foundation Model]] discusses *persistent_robot_world_models*. Innovation: "Unified affordance foundation model predicting task-conditional functional masks and 3D post-contact motion curves from RGB-D and language, trained on a large-scale heterogeneous dataset."
- [ ] **2026-06-03**: New paper [[QwenVLA Unified VLA for Manipulation and Navigation]] discusses *persistent_robot_world_models*. Innovation: "Unifies manipulation, navigation, and trajectory prediction into a single VLA model using embodiment-aware prompts and a DiT-based action decoder."
- [ ] **2026-06-03**: New paper [[HideandSeek Failure Detection for VLA]] discusses *persistent_robot_world_models*. Innovation: "Hide-and-Seek introduces inter- and intra-trajectory contrastive objectives to localize failure-indicative actions from trajectory-level labels without step-level annotation."
- [ ] **2026-06-04**: New paper [[AffordVLA]] discusses *persistent robot world models*. Innovation: "Internalizing task-conditioned affordance as learnable tokens that decode masks and directly condition action generation in a tightly coupled VLA framework."
- [ ] **2026-06-06**: New paper [[WLA]] discusses *persistent robot world models*. Innovation: "Proposes a unified autoregressive model that predicts both high-level textual subtasks and low-level physical dynamics to guide action synthesis, enabling optional world prediction for test-time scaling."
- [ ] **2026-06-09**: New paper [[ARVLA]] discusses *persistent robot world models*. Innovation: "Introduces a standalone autoregressive action expert with persistent memory and a re-anchoring mechanism that mathematically accounts for perception staleness, enabling asynchronous vision-language conditioning and continuous context-aware action generation."
- [ ] **2026-06-11**: New paper [[LightWAM]] discusses *persistent robot world models*. Innovation: "Introduces a lightweight World Action Model with frozen video backbone, latent-space video supervision, and a multi-layer feature fusion action decoder for efficient robot manipulation."
- [ ] **2026-06-11**: New paper [[World Pilot]] discusses *persistent robot world models*. Innovation: "Introduces dual-pathway injection of world-action model priors into VLA: latent steering for scene evolution and action steering for trajectory prior."
- [ ] **2026-06-12**: New paper [[EmbodiedR15]] discusses *persistent robot world models*. Innovation: "A unified Embodied Foundation Model with integrated reasoning, planning, and self-correction, trained with multi-task balanced RL and automated data pipelines, achieving strong zero-shot real-robot performance."
- [ ] **2026-07-22**: New paper [[Appleπ]] discusses *persistent robot world models*. Innovation: "Introduces the first benchmark that evaluates video models as world models through a three-stage law-grounded reasoning protocol (Perception, Formulation, Deduction) with hybrid physics-law and MLLM metrics."