---
tags:
  - paper
  - Embodied_AI
  - Sim2Real
  - Foundation_Model
  - 3D_Gaussian_Splatting
aliases:
  - "SIMART: Decomposing Monolithic Meshes into Sim-ready Articulated Assets via MLLM"
url: http://arxiv.org/abs/2603.23386v1
pdf_url: https://arxiv.org/pdf/2603.23386v1
local_pdf: "[[SIMART Decomposing Monolithic Meshes into Simready Articulated Assets via MLLM.pdf]]"
github: "None"
project_page: "None"
publication_date: "Unknown"
score: 8
---

# SIMART: Decomposing Monolithic Meshes into Sim-ready Articulated Assets via MLLM

## 📌 Abstract
High-quality articulated 3D assets are indispensable for embodied AI and physical simulation, yet 3D generation still focuses on static meshes, leaving a gap in "sim-ready" interactive objects. Most recent articulated object creation methods rely on multi-stage pipelines that accumulate errors across decoupled modules. Alternatively, unified MLLMs offer a single-stage path to joint static asset understanding and sim-ready asset generation. However dense voxel-based 3D tokenization yields long 3D token sequences and high memory overhead, limiting scalability to complex articulated objects. To address this, we propose SIMART, a unified MLLM framework that jointly performs part-level decomposition and kinematic prediction. By introducing a Sparse 3D VQ-VAE, SIMART reduces token counts by 70% vs. dense voxel tokens, enabling high-fidelity multi-part assemblies. SIMART achieves state-of-the-art performance on PartNet-Mobility and in-the-wild AIGC datasets, and enables physics-based robotic simulation.

## 🖼️ Architecture
![[SIMART Decomposing Monolithic Meshes into Simready Articulated Assets via MLLM_arch.png]]

## 🧠 AI Analysis
Analysis Failed: Could not process images with any model. Error code: 403 - {'error': {'message': 'This model is not available in your region.', 'code': 403}}

## 📂 Resources
- **Local PDF**: [[SIMART Decomposing Monolithic Meshes into Simready Articulated Assets via MLLM.pdf]]
- [Online PDF](https://arxiv.org/pdf/2603.23386v1)
- [ArXiv Link](http://arxiv.org/abs/2603.23386v1)
