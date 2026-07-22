# 📅 2026-05-19 - Paper Digest
## Summary
Total Papers: 5 | High Impact: 2

## 📝 Papers List
### 🔥 StableVLA: Towards Robust Vision-Language-Action Models without Extra Data (Score: 8.1/10)
- **💡 Innovation**: Proposes an Information Bottleneck Adapter that selectively filters visual noise without extra data, improving VLA robustness by 30% on average.
- **⚠️ Limitations**: The adapter's effectiveness may be limited to visual corruptions similar to those tested; generalization to other disturbance types (e.g., adversarial attacks) is not evaluated.
- **🔗 Link**: [[StableVLA]]
- **👥 Authors**: Yiyang Fu, Chubin Zhang, Shukai Gong, Yufan Deng, Kaiwei Sun, Qiyang Min, Qibin Hou, Yansong Tang, Jianan Wang, Daquan Zhou
- **🏛️ Institutions**: Peking University, Tsinghua University, Astribot, Nanjing University, Nankai University
- **🏷️ Tags**: #domain/vla #domain/robot_manipulation #domain/embodied_ai #method/foundation_model #type/method #impact/solid
- **Source Mode**: daily

---
### 🔥 AR-VLA: True Autoregressive Action Expert for Vision-Language-Action Models (Score: 8.0/10)
- **💡 Innovation**: Introduces a standalone autoregressive action expert with persistent memory and a re-anchoring mechanism that mathematically accounts for perception staleness, enabling asynchronous vision-language conditioning and continuous context-aware action generation.
- **⚠️ Limitations**: The re-anchoring mechanism relies on a model of perception staleness, and the approach may require careful tuning of asynchronous update frequencies; generalization to highly dynamic tasks is not yet demonstrated.
- **🔗 Link**: [[ARVLA]]
- **👥 Authors**: Yutong Hu, Jan-Nico Zaech, Nikolay Nikolov, Yuanqi Yao, Sombit Dey, Giuliano Albanese, Renaud Detry, Luc Van Gool, Danda Paudel
- **🏛️ Institutions**: INSAIT, Sofia University “St. Kliment Ohridski”, KU Leuven, Dept. Mechanical Engineering
- **🏷️ Tags**: #domain/vla #domain/robot_manipulation #method/diffusion_policy #method/foundation_model #method/memory #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ FuRA: Full-Rank Parameter-Efficient Fine-Tuning with Spectral Preconditioning (Score: 6.3/10)
- **💡 Innovation**: Introduces full-rank spectral preconditioning via block tensor-train factorization to achieve parameter-efficient fine-tuning that outperforms full fine-tuning.
- **⚠️ Limitations**: Evaluation is limited to language and vision-language benchmarks; no demonstration on robotics-specific tasks or sim-to-real transfer.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2605.22869v1)
- **👥 Authors**: Yequan Zhao, Ruijie Zhang, Liyan Tan, Niall Moran, Tong Qin, Zheng Zhang
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #method/foundation_model #type/method #domain/multimodal_perception #impact/solid
- **Source Mode**: daily

---
### ✨ The Yes-Man Syndrome: Benchmarking Abstention in Embodied Robotic Agents (Score: 5.0/10)
- **💡 Innovation**: 
- **⚠️ Limitations**: 
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2605.20544v1)
- **👥 Authors**: Doguhan Yeke, Elif Su Temirel, Ananth Shreekumar, Brandon Lee, Dongyan Xu, Z Berkay Celik
- **🏛️ Institutions**: Unknown
- **🏷️ Source**: #arXiv
- **Source Mode**: daily

---
### ✨ Incantation: Natural Language as the Action Interface for Multi-Entity Video World Models (Score: 5.0/10)
- **💡 Innovation**: First interactive video world model using per-frame natural language actions for multi-entity control and cross-entity transfer via ODE-initialized Self-Forcing distillation.
- **⚠️ Limitations**: Only demonstrated on video games, not on real-world robotic manipulation or embodied tasks; limited baseline comparison.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2605.18601)
- **👥 Authors**: Shangwen Zhu, Qianyu Peng, Zhao Pu, Zhilei Shu, Xiangrui Ke, Zhaohu Xing, Zizhao Tong, Zeqing Wang, Xinyu Cui, Huangji Wang, Jian Zhao, Yeying Jin, Fan Cheng, Ruili Feng
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/world_model #method/world_model #task/video_prediction #method/foundation_model
- **Source Mode**: daily

---

