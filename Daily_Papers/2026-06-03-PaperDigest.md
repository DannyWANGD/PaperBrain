# 📅 2026-06-03 - Paper Digest
## Summary
Total Papers: 5 | High Impact: 1

## 📝 Papers List
### ✨ Generalization of World Models under Environmental Variability for Vision-based Quadrotor Navigation (Score: 7.3/10)
- **💡 Innovation**: Systematic cross-environment validation reveals that world model robustness during SSL pretraining predicts sim-to-real transfer, and identifies discrete latent size and training-sequence length as key factors.
- **⚠️ Limitations**: Study limited to a single world model architecture (DreamerV3) and a specific quadrotor navigation task, with environmental variability confined to simulated randomness.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2606.05015v1)
- **👥 Authors**: Luca Zanatta, Grzegorz Malczyk, Kostas Alexis
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/world_model #domain/reinforcement_learning #domain/embodied_ai #domain/sim2real #task/navigation #type/analysis #impact/solid

---
### ✨ X4Val: Learning Neural Surrogates for Variance-Reduced Policy Evaluation (Score: 6.7/10)
- **💡 Innovation**: X4Val introduces a shared embedding space and transferable metric predictor to enable control-variate variance reduction with non-paired multi-domain data.
- **⚠️ Limitations**: The approach assumes that auxiliary domains share sufficient structure with the real domain to learn a useful predictor, which may not hold for highly disparate domains.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2606.05159v1)
- **👥 Authors**: Rachel Luo, Michael Watson, Apoorva Sharma, Heng Yang, Han Qi, Edward Schmerling, Sushant Veer, Boris Ivanovic, Marco Pavone
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/robot_manipulation #domain/embodied_ai #type/method #type/analysis #method/simulation

---
### ✨ GRAIL: Generating Humanoid Loco-Manipulation from 3D Assets and Video Priors (Score: 6.4/10)
- **💡 Innovation**: A fully digital pipeline that generates humanoid loco-manipulation data by composing 3D assets with video foundation model priors, enabling sim-to-real policy training without physical data collection.
- **⚠️ Limitations**: The pipeline requires known 3D scene configurations and robot-proportioned characters, which may not generalize to unstructured environments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2606.05160v1)
- **👥 Authors**: Tianyi Xie, Haotian Zhang, Jinhyung Park, Zi Wang, Bowen Wen, Jiefeng Li, Xueting Li, Qingwei Ben, Haoyang Weng, Yufei Ye, David Minor, Tingwu Wang, Chenfanfu Jiang, Sanja Fidler, Jan Kautz, Linxi Fan, Yuke Zhu, Zhengyi Luo, Umar Iqbal, Ye Yuan
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/embodied_ai #domain/robot_manipulation #method/simulation #method/foundation_model #task/loco_manipulation #type/system

---
### ✨ STRIDE: Training Data Attribution via Sparse Recovery from Subset Perturbations (Score: 5.4/10)
- **💡 Innovation**: Proposes a training data attribution method that uses activation-space steering operators and sparse recovery instead of gradient-based approximations.
- **⚠️ Limitations**: The method is evaluated only on LLM pre-training attribution, not on robotics or embodied AI tasks, limiting its direct applicability to the target workflow.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2606.05165v1)
- **👥 Authors**: Rishit Dagli, Abir Harrasse, Luke Zhang, Florent Draye, Amirali Abdullah, Bernhard Schölkopf, Zhijing Jin
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #method/foundation_model #type/method #type/analysis

---
### ✨ Reinforcement Learning from Rich Feedback with Distributional DAgger (Score: 5.2/10)
- **💡 Innovation**: Proposes a distributional DAgger variant with forward cross-entropy that guarantees monotonic policy improvement for RL with rich feedback, unlike prior self-distillation objectives.
- **⚠️ Limitations**: Requires a blackbox expert that can provide token-level distributions on states visited by the current policy, which may be unavailable or expensive in real-world robot learning.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2606.05152v1)
- **👥 Authors**: Rishabh Agrawal, Jacob Fein-Ashley, Paria Rashidinejad
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #method/reinforcement_learning #method/imitation_learning #method/foundation_model #type/method

---

