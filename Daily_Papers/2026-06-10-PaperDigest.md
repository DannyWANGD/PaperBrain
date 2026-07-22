# 📅 2026-06-10 - Paper Digest
## Summary
Total Papers: 5 | High Impact: 5

## 📝 Papers List
### ✨ World Pilot: Steering Vision-Language-Action Models with World-Action Priors (Score: 7.5/10)
- **💡 Innovation**: Introduces dual-pathway injection of world-action model priors into VLA: latent steering for scene evolution and action steering for trajectory prior.
- **⚠️ Limitations**: Relies on a pre-trained world-action model; real-robot evaluation limited to four tasks; generalization to tasks where world model fails is unclear.
- **🔗 Link**: [[World Pilot]]
- **👥 Authors**: Zefu Lin, Rongxu Cui, Junjia Xu, Xiaojuan Jin, Wenling Li, Lue Fan, Zhaoxiang Zhang
- **🏛️ Institutions**: Institute of Automation, Chinese Academy of Sciences (CASIA), Nanjing University, Beihang University
- **🏷️ Tags**: #domain/vla #domain/world_model #domain/robot_manipulation #domain/embodied_ai #method/foundation_model #method/world_model #task/manipulation #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ Next Forcing: Causal World Modeling with Multi-Chunk Prediction (Score: 7.4/10)
- **💡 Innovation**: Introduces multi-chunk prediction with causal chain auxiliary modules to provide dense temporal supervision for world action models, improving convergence and accuracy.
- **⚠️ Limitations**: Evaluation on manipulation tasks is limited to RoboTwin; broader real-world robot tasks and comparison with diverse world model architectures are not explored.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.11187)
- **👥 Authors**: Gangwei Xu, Qihang Zhang, Jiaming Zhou, Xing Zhu, Yujun Shen, Xin Yang, Yinghao Xu
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/world_model #domain/robot_manipulation #method/diffusion_policy #method/world_model #task/video_prediction #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ APT: Action Expert Pretraining Improves Instruction Generalization of Vision-Language-Action Policies (Score: 7.3/10)
- **💡 Innovation**: Bayesian factorization of VLA policy into a language-agnostic vision-action prior and a language-conditioned likelihood, with action expert pretraining to mitigate visual shortcuts.
- **⚠️ Limitations**: Relies on a frozen VLM and may not fully exploit joint vision-language fine-tuning; generalization to entirely new tasks not tested.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2606.12366v1)
- **👥 Authors**: Kechun Xu, Zhenjie Zhu, Anzhe Chen, Rong Xiong, Yue Wang
- **🏛️ Institutions**: Qwen Team
- **🏷️ Tags**: #domain/vla #domain/robot_manipulation #method/foundation_model #method/imitation_learning #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ Test-Time Gradient Guidance of Flow Policies in Reinforcement Learning (Score: 7.2/10)
- **💡 Innovation**: Introduces a test-time gradient guidance for flow policies that uses the critic gradient on the final action, avoiding backpropagation through time and noisy action gradients.
- **⚠️ Limitations**: The method assumes a well-trained critic and has only been evaluated in simulation, leaving real-world applicability uncertain.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2606.11087)
- **👥 Authors**: Zhiyuan Zhou, Andy Peng, Charles Xu, Qiyang Li, Tobias Springenberg, Kevin Frans, Sergey Levine
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/reinforcement_learning #domain/robot_manipulation #method/diffusion_policy #method/reinforcement_learning #method/imitation_learning #type/method #impact/solid
- **Source Mode**: daily

---
### ✨ DIRECT: When and Where Should You Allocate Test-Time Compute in Embodied Planners? (Score: 7.0/10)
- **💡 Innovation**: Introduces a multimodal context-conditioned router that dynamically selects among chain-of-thought depth, model size, and memory history to optimize embodied planning success-cost tradeoffs.
- **⚠️ Limitations**: Router generalization to unseen tasks and planner configurations is not demonstrated; reliance on pre-defined scaling axes may limit adaptability.
- **🔗 Link**: [[DIRECT]]
- **👥 Authors**: Jadelynn Dao, Milan Ganai, Yasmina Abukhadra, Ajay Sridhar, Mozhgan Nasr Azadani, Katie Luo, Clark Barrett, Jiajun Wu, Chelsea Finn, Marco Pavone
- **🏛️ Institutions**: Unknown
- **🏷️ Tags**: #domain/embodied_ai #domain/robot_manipulation #domain/vla #method/foundation_model #method/planning #method/memory #task/planning_reasoning #type/method #type/analysis #impact/solid
- **Source Mode**: daily

---

