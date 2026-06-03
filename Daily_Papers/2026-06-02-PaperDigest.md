# 📅 2026-06-02 - Paper Digest
## Summary
Total Papers: 4 | High Impact: 4

## 📝 Papers List
### ✨ Where to Look: Can Foundation Models Reach a Target Viewpoint Through Active Exploration? (Score: 7.9/10)
- **💡 Innovation**: Introduces Target Viewpoint Reproduction (TVR), an active 3D exploration task that requires closing the perception‑action loop to match a target viewpoint, revealing fundamental bottlenecks in foundation models' spatial reasoning.
- **⚠️ Limitations**: Post‑training is demonstrated on a single open‑source 9B model in indoor simulation, leaving generalization across diverse embodiments and real‑world settings unverified.
- **🔗 Link**: [[Target Viewpoint Reproduction TVR Benchmark]]
- **👥 Authors**: Liyang Li, Muzhi Zhu, Zhiyue Zhao, Hengyu Zhao, Ke Liu, Linhao Zhong, Hao Chen, Chunhua Shen
- **🏷️ Tags**: #domain/embodied_ai #domain/vla #method/foundation_model #method/benchmark #method/reinforcement_learning

---

### ✨ AFUN: Towards an Affordance Foundation Model for Functionality Understanding (Score: 7.5/10)
- **💡 Innovation**: Unifies heterogeneous data sources into a shared affordance schema to train a model that jointly predicts task-conditional interaction masks and 3D motion curves from a single RGB-D image and language instruction.
- **⚠️ Limitations**: The model predicts post-contact motion but does not handle pre-contact planning or dynamic task constraints, and real-robot deployment is only demonstrated qualitatively.
- **🔗 Link**: [[AFUN Affordance Foundation Model]]
- **👥 Authors**: Zhaoning Wang, Yi Zhong, Jiawei Fu, Henrik I. Christensen, Jun Gao
- **🏷️ Tags**: #domain/robot_manipulation #domain/embodied_ai #method/foundation_model #task/manipulation #task/planning_reasoning #type/method #type/dataset #impact/high_value

---

### ✨ Preference-Calibrated Human-in-the-Loop Reinforcement Learning for Robotic Manipulation (Score: 7.2/10)
- **💡 Innovation**: Proposes a progress model to identify suboptimal segments and uses counterfactual advantage from human-policy action pairs to calibrate credit assignment in HIL-RL.
- **⚠️ Limitations**: The progress model relies on human demonstrations for training, which may require additional data collection; the method's scalability to more complex tasks is not demonstrated.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2606.03949v1)
- **👥 Authors**: Zeyi Liu, Guangyao Liu, Yinuo Qu, Yuquan Xue, Bofang Jia, Chunhua Yang, Weihua Gui, Keke Huang, Ziwei Wang
- **🏷️ Tags**: #domain/robot_manipulation #domain/reinforcement_learning #method/reinforcement_learning #type/method #impact/solid

---

### ✨ PointAction: 3D Points as Universal Action Representations for Robot Control (Score: 7.2/10)
- **💡 Innovation**: Introduces dynamic 3D pointmaps as an embodiment-agnostic intermediate representation to bridge video prediction and robot action decoding, reducing ambiguity in action grounding.
- **⚠️ Limitations**: Relies on a pre-trained video generation model and requires pointmap supervision, which may limit applicability to domains without 3D data.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2606.03943v1)
- **👥 Authors**: Mutian Tong, Han Jiang, Qiao Feng, Lingjie Liu, Jiatao Gu
- **🏷️ Tags**: #domain/robot_manipulation #domain/vla #domain/world_model #domain/3d_perception #method/diffusion_policy #method/foundation_model #task/manipulation #task/video_prediction #type/method

---


