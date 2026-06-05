# 📅 2026-05-21 - Paper Digest
## Summary
Total Papers: 5 | High Impact: 1

## 📝 Papers List
### ✨ You Only Need Minimal RLVR Training: Extrapolating LLMs via Rank-1 Trajectories (Score: 7.0/10)
- **💡 Innovation**: Proposes RELEX, a method that extrapolates future RLVR checkpoints from a short observation window using rank-1 subspace estimation and linear regression, reducing required training steps by up to 85%.
- **⚠️ Limitations**: The method is only validated on math reasoning tasks for LLMs, and its applicability to other domains or embodied AI tasks remains unexplored.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2605.21468)
- **👥 Authors**: Zhepei Wei, Xinyu Zhu, Wei-Lin Chen, Chengsong Huang, Jiaxin Huang, Yu Meng
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/reinforcement_learning #method/reinforcement_learning #method/foundation_model #type/analysis #type/method #impact/solid

---
### ✨ Conditional Equivalence of DPO and RLHF: Implicit Assumption, Failure Modes, and Provable Alignment (Score: 6.0/10)
- **💡 Innovation**: Proves conditional equivalence of DPO and RLHF and introduces Constrained Preference Optimization for provable alignment.
- **⚠️ Limitations**: Limited to LLM alignment, not directly applicable to robot manipulation or embodied AI.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2605.20834)
- **👥 Authors**: Zhiqin Yang, Yonggang Zhang, Wei Xue, Dong Fang, Bo Han, Yike Guo
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/reinforcement_learning #method/reinforcement_learning #method/foundation_model #type/analysis

---
### ✨ Model Collapse as Cultural Evolution (Score: 6.0/10)
- **💡 Innovation**: First systematic test of discriminative predictions from cultural evolution theory at full LLM scale, revealing a non-monotonic compositionality trajectory and compression-communication tradeoff in model collapse.
- **⚠️ Limitations**: Experiments are limited to text-only LLMs and natural language; applicability to multimodal or embodied foundation models remains untested.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2605.23054v1)
- **👥 Authors**: Dongxin Guo, Jikun Wu, Siu Ming Yiu
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #method/foundation_model #type/analysis #review/needs_review

---
### ✨ MINTEval: Evaluating Memory under Multi-Target Interference in Long-Horizon Agent Systems (Score: 6.0/10)
- **💡 Innovation**: Introduces a benchmark for evaluating memory under multi-target interference in long-horizon agents, with diverse domains and question types probing recall and aggregation under conflicting updates.
- **⚠️ Limitations**: The benchmark is limited to text-based domains and does not assess memory in embodied or robotic settings where physical state tracking and sensorimotor interference are critical.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2605.18565)
- **👥 Authors**: Hyunji Lee, Justin Chih-Yao Chen, Joykirat Singh, Zaid Khan, Elias Stengel-Eskin, Mohit Bansal
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #method/benchmark #type/benchmark #type/dataset #method/memory #method/foundation_model

---
### ✨ Dreaming Smoothly and Sample Efficiently with Gradient Penalized Latent Dynamics (Score: 5.9/10)
- **💡 Innovation**: Proposes a gradient-penalized latent dynamics regularizer for DreamerV3 that encourages local smoothness via a row-wise Jacobian penalty, motivated by a discrete-to-continuous smoothing argument.
- **⚠️ Limitations**: Evaluation is limited to proprioceptive locomotion tasks, with milder gains on pixel-based observations, and no direct application to manipulation or real-world embodied tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2605.23089v1)
- **👥 Authors**: Romil V. Sonigra, P. R. Kumar
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/world_model #domain/reinforcement_learning #method/world_model #method/reinforcement_learning #task/loco_manipulation #type/method #impact/solid

---

