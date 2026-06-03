# 📅 2026-06-01 - Paper Digest
## Summary
Total Papers: 3 | High Impact: 3

## 📝 Papers List
### 🔥 VisualThink-VLA: Visual Intermediate Reasoning for Effective and Low-Latency Vision-Language-Action Policies (Score: 8.6/10)
- **💡 Innovation**: Introduces a compact visual-evidence interface with selective routing to replace textual chain-of-thought in VLA policies, achieving low-latency and accurate action prediction.
- **⚠️ Limitations**: The approach relies on a pre-constructed visual evidence dataset and may not generalize to tasks requiring abstract reasoning beyond visual cues.
- **🔗 Link**: [[VisualThinkVLA]]
- **👥 Authors**: Mingjian Gao, Wenqiao Zhang, Yuqian Yuan, Yang Dai, Binhe Yu, Zheqi Lv, Haoyu Zheng, Jiaqi Zhu, Zhiqi Ge, Zixuan Wan, Siliang Tang, Yueting Zhuang
- **Institutions**: Zhejiang University, Cornell University, National University of Singapore, Xi’an University of Electronic Science and Technology
- **🏷️ Tags**: #domain/vla #domain/robot_manipulation #domain/embodied_ai #method/foundation_model #task/manipulation #task/planning_reasoning #type/method #impact/high_value

---
### 🔥 Hide-and-Seek in Trajectories: Discovering Failure Signals for VLA Runtime Monitoring (Score: 8.1/10)
- **💡 Innovation**: Hide-and-Seek introduces inter- and intra-trajectory contrastive objectives to localize failure-indicative actions from trajectory-level labels without step-level annotation.
- **⚠️ Limitations**: The method assumes failure signals are temporally localized and may not capture distributed or gradual failures.
- **🔗 Link**: [[HideandSeek Failure Detection for VLA]]
- **👥 Authors**: Seongheon Park, Wendi Li, Changdae Oh, Samuel Yeh, Zsolt Kira, Michael Hagenow, Sharon Li
- **Institutions**: University of Wisconsin–Madison, Georgia Institute of Technology
- **🏷️ Tags**: #domain/vla #domain/robot_manipulation #domain/embodied_ai #method/foundation_model #type/method #impact/solid

---
### ✨ GDSD: Reinforcement Learning as Guided Denoiser Self-Distillation for Diffusion Language Models (Score: 7.4/10)
- **💡 Innovation**: Proposes to reduce RL for diffusion language models to likelihood-free self-distillation from an advantage-guided teacher, bypassing training-inference mismatch biases inherent in ELBO-based methods.
- **⚠️ Limitations**: The method is evaluated only on language tasks (planning, math, coding) and not on embodied or robotic domains, leaving its applicability to diffusion policies in robotics unexplored.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2605.29398)
- **👥 Authors**: Xiaohang Tang, Keyue Jiang, Che Liu, Qifang Zhao, Xiaoxiao Xu, Sangwoong Yoon, Ilija Bogunovic
- **Institutions**: Unknown
- **🏷️ Tags**: #method/reinforcement_learning #method/diffusion_policy #method/foundation_model #type/method #impact/solid

---

