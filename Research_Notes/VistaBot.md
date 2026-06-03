---
tags:
- paper
- domain/3d_perception
- domain/embodied_ai
- domain/multimodal_perception
- domain/reinforcement_learning
- domain/robot_manipulation
- domain/world_model
- impact/high_value
- method/benchmark
- method/diffusion_policy
- method/planning
- method/reinforcement_learning
- method/simulation
- review/auto_tagged
- status/unread
- task/manipulation
- task/navigation
- task/planning_reasoning
- task/scene_understanding
- type/benchmark
aliases:
- 'VistaBot: View-Robust Robot Manipulation via Spatiotemporal-Aware View Synthesis'
- VistaBot
- Spatiotemporal View Synthesis
- View-Robust Manipulation
- Calibration-Free Manipulation
- Video Diffusion Robotics
- Geometric Video Diffusion
- Closed-Loop View Synthesis
arxiv_id: '2604.21914'
url: http://arxiv.org/abs/2604.21914v1
pdf_url: https://arxiv.org/pdf/2604.21914v1
local_pdf: '[[VistaBot ViewRobust Robot Manipulation via SpatiotemporalAware View
  Synthesis.pdf]]'
github: None
project_page: None
publication_date: Unknown
score: '8.0'
domains:
- 3d_perception
- embodied_ai
- multimodal_perception
- reinforcement_learning
- robot_manipulation
methods:
- benchmark
- planning
- reinforcement_learning
- simulation
tasks:
- manipulation
- navigation
- planning_reasoning
- scene_understanding
paper_type: benchmark
impact_band: high_value
reading_status: unread
year: null
priority_score: 103
review_status: auto_tagged
next_action: inspect_protocol
paper_id: arxiv:2604.21914
---

# VistaBot: View-Robust Robot Manipulation via Spatiotemporal-Aware View Synthesis

## 📌 Abstract
Recently, end-to-end robotic manipulation models have gained significant attention for their generalizability and scalability. However, they often suffer from limited robustness to camera viewpoint changes when training with a fixed camera. In this paper, we propose VistaBot, a novel framework that integrates feed-forward geometric models with video diffusion models to achieve view-robust closed-loop manipulation without requiring camera calibration at test time. Our approach consists of three key components: 4D geometry estimation, view synthesis latent extraction, and latent action learning. VistaBot is integrated into both action-chunking (ACT) and diffusion-based ($π_0$) policies and evaluated across simulation and real-world tasks. We further introduce the View Generalization Score (VGS) as a new metric for comprehensive evaluation of cross-view generalization. Results show that VistaBot improves VGS by 2.79$\times$ and 2.63$\times$ over ACT and $π_0$, respectively, while also achieving high-quality novel view synthesis. Our contributions include a geometry-aware synthesis model, a latent action planner, a new benchmark metric, and extensive validation across diverse environments. The code and models will be made publicly available.

## 🖼️ Architecture
![[VistaBot ViewRobust Robot Manipulation via SpatiotemporalAware View Synthesis_arch.png]]

## 🧠 AI Analysis
Analysis Failed: All models unavailable.

## 📂 Resources
- **Local PDF**: [[VistaBot ViewRobust Robot Manipulation via SpatiotemporalAware View Synthesis.pdf]]
- [Online PDF](https://arxiv.org/pdf/2604.21914v1)
- [ArXiv Link](http://arxiv.org/abs/2604.21914v1)
