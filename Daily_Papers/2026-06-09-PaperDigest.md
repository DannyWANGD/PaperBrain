# 📅 2026-06-09 - Paper Digest
## Summary
Total Papers: 5 | High Impact: 5

## 📝 Papers List
### 🔥 Dynamic Execution Horizon Prediction for Chunk-based Robot Policies (Score: 8.2/10)
- **💡 Innovation**: A lightweight execution-horizon prediction branch trained with online RL on a frozen chunk-based policy to dynamically adjust the number of executed actions per chunk.
- **⚠️ Limitations**: The method relies on online RL, which may require environment interaction and may not be directly applicable to offline settings; the horizon predictor is task-specific and may not generalize across tasks without retraining.
- **🔗 Link**: [[DEHP]]
- **👥 Authors**: Yuchi Zhao, Miroslav Bogdanovic, Arjun Sohal, Liyu Tao, Kourosh Darvish, Alán Aspuru-Guzik, Florian Shkurti, Animesh Garg
- **🏛️ Institutions**: University of Toronto, Georgia Institute of Technology
- **🏷️ Tags**: #domain/robot_manipulation #domain/vla #method/reinforcement_learning #method/diffusion_policy #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ Light-WAM: Efficient World Action Models with State-Fusion Action Decoding (Score: 7.5/10)
- **💡 Innovation**: Introduces a lightweight World Action Model with frozen video backbone, latent-space video supervision, and a multi-layer feature fusion action decoder for efficient robot manipulation.
- **⚠️ Limitations**: Relies on a pretrained video diffusion model and may not generalize to tasks requiring long-horizon video prediction or complex dynamics.
- **🔗 Link**: [[LightWAM]]
- **👥 Authors**: Ziang Li, Dongzhou Cheng, Yibin Wang, Shiyue Wang, Xiaoyang Xu, Lingxuan Weng, Juan Wang, Jiaqi Wang
- **🏛️ Institutions**: Wuhan University, Shanghai Innovation Institute, Southeast University, Fudan University, East China Normal University
- **🏷️ Tags**: #domain/world_model #domain/robot_manipulation #domain/vla #method/world_model #method/foundation_model #method/imitation_learning #task/video_prediction #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ AHA-WAM:Asynchronous Horizon-Adaptive World-Action Modeling with Observation-Guided Context Routing (Score: 7.3/10)
- **💡 Innovation**: Asynchronous horizon-adaptive world-action modeling decouples slow world planning from fast action execution via a dual DiT with observation-guided context routing, enabling efficient closed-loop control.
- **⚠️ Limitations**: The world planner's low-frequency updates may miss rapid scene changes, and the method's reliance on a video DiT may limit applicability to domains without suitable video data.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.09811)
- **👥 Authors**: Jisong Cai, Long Ling, Shiwei Chu, Zhongshan Liu, Jiayue Kang, Zhixuan Liang, Wenjie Xu, Yinan Mao, Weinan Zhang, Xiaokang Yang, Ru Ying, Ran Zheng, Yao Mu
- **🏛️ Institutions**: Qwen Team
- **🏷️ Tags**: #domain/world_model #domain/robot_manipulation #domain/embodied_ai #method/diffusion_policy #method/world_model #method/memory #method/planning #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ PLUME: Probabilistic Latent Unified World Modeling and Parameter Estimation for Multi-Finger Manipulation (Score: 7.2/10)
- **💡 Innovation**: Jointly learns a probabilistic latent representation of physical parameters and rewards via flow matching to condition a world model for online parameter inference and planning in dexterous manipulation.
- **⚠️ Limitations**: Hardware evaluation is restricted to one task, and the method requires simulation data with ground-truth parameter labels for training.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2606.11396v1)
- **👥 Authors**: Abhinav Kumar, Soshi Iba, Rana Soltani Zarrin, Dmitry Berenson
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/robot_manipulation #domain/world_model #method/diffusion_policy #method/world_model #method/planning #task/dexterous_contact #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ VoLo: A Physical Orchestrator for Open-Vocabulary Long-Horizon Manipulation (Score: 7.1/10)
- **💡 Innovation**: A VLM orchestrator that treats a VLA as an interruptible tool for mid-rollout recovery in long-horizon manipulation.
- **⚠️ Limitations**: The system relies on pre-defined tools and may not generalize to novel manipulation skills beyond the toolset.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.07723)
- **👥 Authors**: Siyi Chen, Hugo Hadfield, Alex Zook, Mikaela Angelina Uy, Chan Hee Song, Erwin Coumans, Xuning Yang, Faisal Ladhak, Qing Qu, Stan Birchfield, Jonathan Tremblay, Valts Blukis
- **🏛️ Institutions**: NVIDIA
- **🏷️ Tags**: #domain/vla #domain/robot_manipulation #domain/embodied_ai #method/foundation_model #method/planning #method/benchmark #type/system #impact/solid
- **Source Mode**: daily

---

