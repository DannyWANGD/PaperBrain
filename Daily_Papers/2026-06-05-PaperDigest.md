# 📅 2026-06-05 - Paper Digest
## Summary
Total Papers: 5 | High Impact: 5

## 📝 Papers List
### 🔥 Trust Region Q Adjoint Matching (Score: 8.1/10)
- **💡 Innovation**: Introduces adaptive trust-region control into stochastic optimal control dynamics for flow policy fine-tuning, with a closed-form path-space KL divergence as a function of the trust-region parameter.
- **⚠️ Limitations**: Evaluation limited to OGBench and Robomimic; trust-region parameter tuning via dual descent may require careful hyperparameter selection.
- **🔗 Link**: [[TRQAM]]
- **👥 Authors**: Yonghoon Dong, Kyungmin Lee, Changyeon Kim, Jaehyuk Kim, Jinwoo Shin
- **🏛️ Institutions**: KAIST AI, Seoul National University, RLWRLD
- **🏷️ Tags**: #domain/robot_manipulation #domain/reinforcement_learning #method/diffusion_policy #method/reinforcement_learning #type/method #impact/high_value #domain/embodied_ai
- **Source Mode**: daily

---
### ✨ World-Language-Action Model for Unified World Modeling, Language Reasoning, and Action Synthesis (Score: 7.5/10)
- **💡 Innovation**: Proposes a unified autoregressive model that predicts both high-level textual subtasks and low-level physical dynamics to guide action synthesis, enabling optional world prediction for test-time scaling.
- **⚠️ Limitations**: The model's ability to learn from cross-embodiment videos without action annotations is only claimed but not empirically validated in the provided excerpt.
- **🔗 Link**: [[WLA]]
- **👥 Authors**: Yi Yang, Zhihong Liu, Siqi Kou, Yiyang Chen, Yanzhe Hu, Jianbo Zhou, Boyuan Zhao, Zhijie Wei, Xiao Xia, Xueqi Li, Pengfei Liu, Zhijie Deng
- **🏛️ Institutions**: SJTU, SII, HUST, SCUT, ECUST, SHU, NJUPT
- **🏷️ Tags**: #domain/vla #domain/world_model #domain/robot_manipulation #domain/embodied_ai #method/foundation_model #type/method
- **Source Mode**: daily

---
### ✨ RobotValues: Evaluating Household Robots When Human Values Conflict (Score: 7.5/10)
- **💡 Innovation**: Introduces a benchmark for evaluating household robot planners on value-conflict scenarios using LLM-generated images and stakeholder-grounded values.
- **⚠️ Limitations**: The benchmark focuses on high-level action selection rather than low-level manipulation skills, and the synthetic images may not fully capture real-world visual complexity.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.03312)
- **👥 Authors**: Jongwook Han, Hyeongjin Kim, Yohan Jo
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/embodied_ai #domain/vla #method/benchmark #method/foundation_model #type/benchmark #type/dataset #task/planning_reasoning
- **Source Mode**: daily

---
### ✨ Dream.exe: Can Video Generation Models Dream Executable Robot Manipulation? (Score: 7.4/10)
- **💡 Innovation**: Introduces a video-to-execution pipeline that grounds video generation models' physical understanding through robot task success in simulation.
- **⚠️ Limitations**: The evaluation is limited to simulation and does not test real-world transfer, and the video-to-trajectory extraction may introduce errors.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.04811)
- **👥 Authors**: Rui Zhao, Kaiming Yang, Jifeng Zhu, Siyang Chen, Ziqi Wang, Weijia Wu, Kevin Qinghong Lin, Heng Wang, Mike Zheng Shou
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/robot_manipulation #domain/world_model #method/benchmark #task/video_prediction #type/benchmark #type/analysis #method/simulation
- **Source Mode**: daily

---
### ✨ AffordanceVLA: A Vision-Language-Action Model Empowering Action Generation through Affordance-Aware Understanding (Score: 7.3/10)
- **💡 Innovation**: Introduces structured affordance forecasting (Which2Act, Where2Act, How2Act) as intermediate representations within a Mixture-of-Transformer VLA to bridge perception-action gap.
- **⚠️ Limitations**: Relies on automated affordance label generation which may introduce noise; real-world evaluation scope unclear from excerpt.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.06155)
- **👥 Authors**: Qize Yu, Jiadi You, Yuran Wang, Jiaqi Liang, Bowen Ping, Yang Tian, Yue Chen, Minghong Cai, Zeying Gong, Ruihai Wu, Yinchuan Li, Junwei Liang, Yingcong Chen
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/vla #domain/robot_manipulation #domain/embodied_ai #method/foundation_model #task/manipulation #task/planning_reasoning #type/method
- **Source Mode**: daily

---

