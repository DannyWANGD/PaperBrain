# 📅 2026-06-17 - Paper Digest
## Summary
Total Papers: 5 | High Impact: 3

## 📝 Papers List
### 🔥 Does VLA Even Know the Basics? Measuring Commonsense and World Knowledge Retention in Vision-Language-Action Models (Score: 8.0/10)
- **💡 Innovation**: Proposes Act2Answer, an action-grounded protocol that evaluates VLA knowledge retention by requiring agents to answer benchmark questions through physical object-placement actions, decoupling knowledge from control.
- **⚠️ Limitations**: The protocol is limited to short-horizon tabletop actions and may not fully assess knowledge integration in long-horizon or dexterous tasks.
- **🔗 Link**: [[Act2Answer]]
- **👥 Authors**: Nikita Kachaev, Andrey Moskalenko, Matvey Skripkin, Nikita Kurlaev, Daria Pugacheva, Albina Burlova, Mikhail Kolosov, Denis Shepelev, Andrey Kuznetsov, Elena Tutubalina, Aleksandr I. Panov, Alexey K. Kovalev, Vlad Shakhuro
- **🏛️ Institutions**: CogAI Lab, FusionBrain Lab
- **🏷️ Tags**: #domain/vla #domain/robot_manipulation #domain/embodied_ai #method/benchmark #type/analysis #method/foundation_model
- **Source Mode**: daily

---
### ✨ OneCanvas: 3D Scene Understanding via Panoramic Reprojection (Score: 7.6/10)
- **💡 Innovation**: A panoramic canvas that reprojects multi-view patch features into a continuous angular coordinate system with 3D position embeddings, enabling a frozen VLM to reason spatially without specialized geometry encoders.
- **⚠️ Limitations**: Overlapping patches from different views are placed independently without aggregation, potentially causing feature conflicts; equirectangular distortion may degrade fine-grained spatial reasoning.
- **🔗 Link**: [[OneCanvas]]
- **👥 Authors**: Bartłomiej Baranowski, Dave Zhenyu Chen, Matthias Nießner
- **🏛️ Institutions**: Technical University of Munich, Huawei
- **🏷️ Tags**: #domain/embodied_ai #domain/3d_perception #task/scene_understanding #method/foundation_model #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ ACE-Ego-0: Unifying Egocentric Human and Robotic Data for VLA Pretraining (Score: 7.5/10)
- **💡 Innovation**: A unified action representation that aligns egocentric human and multi‑embodiment robot data via camera‑space actions, morphology conditioning, and time‑aligned chunking, combined with a reliability‑aware training objective.
- **⚠️ Limitations**: The pseudo‑action labeling pipeline may introduce systematic domain biases, and real‑world performance is demonstrated qualitatively without extensive quantitative metrics across diverse tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.17200)
- **👥 Authors**: Hao Li, Ganlong Zhao, Yufei Liu, Haotian Hou, Guoquan Ye, Tongyan Fang, Chunxiao Liu, Siyuan Huang, Jianbo Liu, Xiaogang Wang, Hongsheng Li
- **🏛️ Institutions**: CUHK, PolyU, Peking University, ACE Robotics
- **🏷️ Tags**: #domain/vla #domain/robot_manipulation #domain/embodied_ai #method/foundation_model #method/imitation_learning #type/method
- **Source Mode**: daily

---
### ✨ UBP2: Uncertainty-Balanced Preference Planning for Efficient Preference-based Reinforcement Learning (Score: 6.2/10)
- **💡 Innovation**: A model-based planning objective that unifies epistemic uncertainty from reward, dynamics, and value ensembles to guide exploration in preference-based RL.
- **⚠️ Limitations**: Scalability to more complex embodied tasks with visual observations and real-world robot manipulation remains unvalidated.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2606.19328v1)
- **👥 Authors**: Mohamed Nabail, Leo Cheng, Jingmin Wang, Nicholas Rhinehart
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/world_model #domain/robot_manipulation #domain/reinforcement_learning #method/planning #method/reinforcement_learning #method/world_model #task/manipulation #type/method #impact/solid #status/unread #review/needs_review
- **Source Mode**: daily

---
### ✨ MotionVLA: Vision-Language-Action Model for Humanoid Motion (Score: 6.1/10)
- **💡 Innovation**: Proposes dual-stream frequency tokenization (DSFT) to separate low-frequency pose and high-frequency physical dynamics, improving autoregressive humanoid motion generation.
- **⚠️ Limitations**: Evaluated solely on motion generation benchmarks, lacking validation in real-world robotics tasks or manipulation settings.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.15142)
- **👥 Authors**: Nonghai Zhang, Siyu Zhai, Yanjun Li, Zeyu Zhang, Zhihan Yin, Yandong Guo, Boxin Shi, Hao Tang
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/embodied_ai #method/foundation_model #type/method
- **Source Mode**: daily

---

