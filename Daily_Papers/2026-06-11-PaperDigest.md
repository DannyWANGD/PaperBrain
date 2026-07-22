# 📅 2026-06-11 - Paper Digest
## Summary
Total Papers: 5 | High Impact: 3

## 📝 Papers List
### 🔥 Embodied-R1.5: Evolving Physical Intelligence via Embodied Foundation Models (Score: 8.0/10)
- **💡 Innovation**: A unified Embodied Foundation Model with integrated reasoning, planning, and self-correction, trained with multi-task balanced RL and automated data pipelines, achieving strong zero-shot real-robot performance.
- **⚠️ Limitations**: The model's performance on real-world long-horizon tasks may still be limited by the closed-loop framework's reliance on visual grounding accuracy, and the 8B parameter size may constrain complex reasoning.
- **🔗 Link**: [[EmbodiedR15]]
- **👥 Authors**: Yifu Yuan, Yaoting Huang, Xianze Yao, Yutong Li, Shuoheng Zhang, Linqi Han, Pengyi Li, Jiangeng Sun, Wenting Jia, Zhao Zhang, Yuhao Liu, Ruihao Liao, Yucheng Hu, Qiyu Wu, Yuxiao Li, Zibin Dong, Fei Ni, Yan Zheng, Shuyang Gu, Yi Ma, Hongyao Tang, Han Hu, Jianye Hao
- **🏛️ Institutions**: Tianjin University, Tencent Hunyuan
- **🏷️ Tags**: #domain/vla #domain/embodied_ai #method/foundation_model #method/reinforcement_learning #method/planning #task/manipulation #type/system #type/benchmark
- **Source Mode**: daily

---
### 🔥 World Pilot: Steering Vision-Language-Action Models with World-Action Priors (Score: 8.0/10)
- **💡 Innovation**: Introduces dual-pathway injection of world-action model priors (latent scene-evolution and action trajectory) into VLA decision chain for improved OOD manipulation.
- **⚠️ Limitations**: Relies on a pre-trained world-action model; effectiveness may depend on quality of video pretraining and may not generalize to tasks with very different dynamics.
- **🔗 Link**: [[World Pilot]]
- **👥 Authors**: Zefu Lin, Rongxu Cui, Junjia Xu, Xiaojuan Jin, Wenling Li, Lue Fan, Zhaoxiang Zhang
- **🏛️ Institutions**: Institute of Automation, Chinese Academy of Sciences (CASIA), Nanjing University, Beihang University
- **🏷️ Tags**: #domain/vla #domain/world_model #domain/robot_manipulation #method/foundation_model #method/world_model #task/manipulation #type/method #impact/high_value
- **Source Mode**: daily

---
### ✨ DRIFT: A Residual Flow Adapter for Decoding Continuous Outputs in Vision-Language Models (Score: 7.3/10)
- **💡 Innovation**: DRIFT introduces a residual flow matching adapter that refines coarse predictions from a base predictor, simplifying generative modeling by focusing on localized residual distributions.
- **⚠️ Limitations**: The method relies on a base predictor that may fail for highly multimodal outputs, and evaluation on robotic control is limited to a single benchmark without comparison to recent VLA-specific architectures.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.05758)
- **👥 Authors**: Zhuoming Liu, Jinhong Lin, Kwan Man Cheng, Lin Zhang, Shayok Bagchi, Yin Li
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/vla #domain/world_model #method/diffusion_policy #method/foundation_model #task/manipulation #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ World Model Self-Distillation: Training World Models to Solve General Tasks (Score: 6.8/10)
- **💡 Innovation**: Self-distillation from detailed solution-conditioned video diffusion to task-only conditioning, combined with RL using VLM as a reward model, enables world models to solve tasks without curated demonstrations.
- **⚠️ Limitations**: Relies on VLM for task generation and evaluation, which may introduce biases; transfer to real robot tasks is only competitive, not state-of-the-art.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.12072)
- **👥 Authors**: Sebastian Stapf, Pablo Acuaviva Huertos, Aram Davtyan, Paolo Favaro
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/world_model #method/diffusion_policy #method/reinforcement_learning #method/foundation_model #domain/embodied_ai #task/video_prediction #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ Grammar-Constrained Decoding Can Jailbreak LLMs into Generating Malicious Code (Score: 6.0/10)
- **💡 Innovation**: Reveals that grammar-constrained decoding can be exploited to jailbreak LLMs into generating malicious code by preventing natural-language refusals.
- **⚠️ Limitations**: The defense method CodeShield may not generalize to all types of grammar constraints or adversarial attacks beyond code generation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.11817)
- **👥 Authors**: Yitong Zhang, Shiteng Lu, Jia Li
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #method/foundation_model #type/analysis
- **Source Mode**: daily

---

