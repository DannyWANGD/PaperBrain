# 📅 2026-06-08 - Paper Digest
## Summary
Total Papers: 5 | High Impact: 1

## 📝 Papers List
### ✨ TBD-VLA: Temporal Block Diffusion Vision Language Action Model (Score: 7.2/10)
- **💡 Innovation**: Introduces temporal block diffusion for discrete VLA, unifying autoregressive block-level generation with parallel masked diffusion within blocks to model temporal dependencies and enable asynchronous execution.
- **⚠️ Limitations**: The excerpt lacks experimental details and quantitative comparisons, making it difficult to assess the actual performance gains and generalizability.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.07895)
- **👥 Authors**: Sung-Wook Lee, Xuhui Kang, Yen-Ling Kuo
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/vla #domain/robot_manipulation #domain/embodied_ai #method/diffusion_policy #method/foundation_model #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ Stream3D-VLM: Online 3D Spatial Understanding with Incremental Geometry Priors (Score: 6.8/10)
- **💡 Innovation**: First online 3D vision-language model that incrementally integrates geometry priors from streaming video for real-time spatial understanding.
- **⚠️ Limitations**: Relies on an external geometry prior model (StreamVGGT) and may not generalize to scenes with poor depth estimation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.06891)
- **👥 Authors**: Hanxun Yu, Xuan Qu, Lei Ke, Boqiang Zhang, Yuxin Wang, Jianke Zhu, Dong Yu
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/embodied_ai #domain/3d_perception #domain/multimodal_perception #method/foundation_model #task/scene_understanding #type/method #type/benchmark #type/dataset
- **Source Mode**: daily

---
### ✨ SpatialWorld: Benchmarking Interactive Spatial Reasoning of Multimodal Agents in Real-World Tasks (Score: 6.7/10)
- **💡 Innovation**: A unified, simulator-agnostic benchmark for interactive spatial reasoning that requires MLLMs to actively explore under partial observability using a native text-based action interface.
- **⚠️ Limitations**: The benchmark focuses on high-level spatial reasoning and does not evaluate low-level manipulation or continuous control, limiting direct applicability to robot manipulation and VLA.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2606.09669v1)
- **👥 Authors**: Hongcheng Gao, Hailong Qu, Jingyi Tang, Jiahao Wang, Zihao Huang, Hengkang Qiao, Shihong Huang, Junming Yang, Yi Li, Hongyixuan Yuan, Wenjie Li, Bohan Zeng, Wenbo Li, Bo Wang, Jianhui Liu, Olive Huang, Haoyang Huang, Wentao Zhang, Guoqing Huang, Nan Duan, Yinpeng Dong
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #method/benchmark #domain/embodied_ai #method/foundation_model #task/planning_reasoning #type/benchmark
- **Source Mode**: daily

---
### ✨ AnchorWorld: Embodied Egocentric World Simulation with View-based Evolution Customization (Score: 6.2/10)
- **💡 Innovation**: Introduces anchor views with textual evolution prompts for customizable egocentric world simulation, and uses exogenous viewpoints to supervise full-body spatial grounding.
- **⚠️ Limitations**: The method's reliance on 3D human motion and anchor views may limit applicability to scenarios without such data; evaluation details are sparse in the excerpt.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.07326)
- **👥 Authors**: Yu Li, Menghan Xia, Gongye Liu, Xintao Wang, Conglang Zhang, Lei Ke, Yuxuan Lin, Ruihang Chu, Pengfei Wan, Kun Gai, Yujiu Yang
- **🏛️ Institutions**: Fudan University, KAUST, SJTU, East China Normal University
- **🏷️ Tags**: #domain/world_model #domain/embodied_ai #method/world_model #task/video_prediction #type/method
- **Source Mode**: daily

---
### ✨ Physics in 2-Steps: Locking Motion Priors Before Visual Refinement Erases Them (Score: 6.2/10)
- **💡 Innovation**: Proposes PhaseLock, a training-free method that locks motion priors from 2-step diffusion inference to prevent phase erosion and improve physical consistency in video generation.
- **⚠️ Limitations**: The method is evaluated only on image-to-video generation and may not generalize to other diffusion-based tasks like action prediction or world model training.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.06361)
- **👥 Authors**: Woojung Han, Seil Kang, Youngjun Jun, Min-Hung Chen, Fu-En Yang, Seong Jae Hwang
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #method/diffusion_policy #task/video_prediction #type/analysis #domain/world_model #impact/solid
- **Source Mode**: daily

---

