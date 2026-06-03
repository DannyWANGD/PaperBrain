# 📅 2026-05-29 - Paper Digest
## Summary
Total Papers: 3 | High Impact: 3

## 📝 Papers List
### 🔥 DynaFLIP: Rethinking Robotics Perception via Tri-Modal-Dynamics Guided Representation (Score: 8.1/10)
- **💡 Innovation**: Introduces tri-modal (image, language, 3D flow) alignment via simplex volume minimization on a hypersphere to inject dynamics awareness into an image-only encoder.
- **⚠️ Limitations**: Relies on pre-computed 3D flow from external estimators, which may introduce noise and limit scalability to domains without reliable flow.
- **🔗 Link**: [[DynaFLIP DynamicsAware Visual Pretraining]]
- **👥 Authors**: Jusuk Lee, Seungjae Lee, Jonghun Shin, Hoseong Jung, Sungha Kim, Daesol Cho, H. Jin Kim, Jia-Bin Huang, Furong Huang
- **🏷️ Tags**: #domain/robot_manipulation #domain/vla #domain/embodied_ai #method/foundation_model #method/imitation_learning #type/method #impact/solid

---

### ✨ Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments (Score: 7.5/10)
- **💡 Innovation**: Unifies manipulation, navigation, and trajectory prediction into a single VLA model using embodiment-aware prompts and a DiT-based action decoder.
- **⚠️ Limitations**: Navigation performance (69% OSR on R2R) lags behind specialized models, and zero-shot dynamic manipulation success is only 26.6%.
- **🔗 Link**: [[QwenVLA Unified VLA for Manipulation and Navigation]]
- **👥 Authors**: Qiuyue Wang, Mingsheng Li, Jian Guan, Jinhui Ye, Sicheng Xie, Yitao Liu, Junhao Chen, Zhixuan Liang, Jie Zhang, Xintong Hu, Xuhong Huang, Pei Lin, Junyang Lin, Dayiheng Liu, Shuai Bai, Jingren Zhou, Jiazhao Zhang, Haoqi Yuan, Gengze Zhou, Hang Yin, Ye Wang, Yiyang Huang, Zixing Lei, Wujian Peng, Delin Chen, Yingming Zheng, Jingyang Fan, Xianwei Zhuang, Xin Zhou, Haoyang Li, Anzhe Chen, Tong Zhang, Xuejing Liu, Yuchong Sun, Ruizhe Chen, Zhaohai Li, Chenxu Lü, Zhibo Yang, Tao Yu, Xionghui Chen
- **🏷️ Tags**: #domain/vla #domain/robot_manipulation #domain/embodied_ai #method/diffusion_policy #method/foundation_model #task/navigation #type/system #impact/high_value

---

### ✨ YoCausal: How Far is Video Generation from World Model? A Causality Perspective (Score: 7.0/10)
- **💡 Innovation**: Introduces a cognitive-science-inspired benchmark using temporally reversed real-world videos as natural counterfactuals to disentangle arrow-of-time perception from genuine causal reasoning in video diffusion models.
- **⚠️ Limitations**: The benchmark may not fully capture causal reasoning required for interactive embodied tasks, as it relies on passive video observation rather than action-conditioned generation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2605.30346)
- **👥 Authors**: You-Zhe Xie, Yu-Hsuan Li, Jie-Ying Lee, Kaipeng Zhang, Yu-Lun Liu, Zhixiang Wang
- **🏷️ Tags**: #domain/world_model #method/diffusion_policy #method/benchmark #type/benchmark #task/video_prediction #method/foundation_model

---


