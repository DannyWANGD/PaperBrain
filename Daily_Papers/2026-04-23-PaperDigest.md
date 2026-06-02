# 📅 2026-04-23 - Paper Digest
## Summary
Total Papers: 9 | High Impact: 9

## 📝 Papers List
### 🔥 Long-Horizon Manipulation via Trace-Conditioned VLA Planning (Score: 8/10)
- **💡 Innovation**: Introduces a modular framework for long-horizon manipulation by decoupling task management from execution using a progress-aware visual trace and lightweight language memory.
- **⚠️ Limitations**: The approach relies heavily on the accuracy of the visual trace prediction, which may fail in highly dynamic or occluded environments.
- **🔗 Link**: [[LongHorizon_Manipulation_via_TraceConditioned_VLA_Planning]]
- **👥 Authors**: Isabella Liu, An-Chieh Cheng, Rui Yan, Geng Chen, Ri-Zhao Qiu, Xueyan Zou, Sha Yi, Hongxu Yin, Xiaolong Wang, Sifei Liu
- **🏷️ Tags**: #Robot_Manipulation #VLA #Embodied_AI #World_Model

---

### 🔥 VistaBot: View-Robust Robot Manipulation via Spatiotemporal-Aware View Synthesis (Score: 8/10)
- **💡 Innovation**: Integrates feed-forward geometric models with video diffusion models for view-robust closed-loop manipulation without requiring camera calibration at test time.
- **⚠️ Limitations**: Potential inefficiency in inference due to the integration of multiple complex models (geometry estimation and video diffusion).
- **🔗 Link**: [[VistaBot]]
- **👥 Authors**: Songen Gu, Yuhang Zheng, Weize Li, Yupeng Zheng, Yating Feng, Xiang Li, Yilun Chen, Pengfei Li, Wenchao Ding
- **🏷️ Tags**: #Robot_Manipulation #Diffusion_Model #Embodied_AI #World_Model

---

### 🔥 LLaDA2.0-Uni: Unifying Multimodal Understanding and Generation with Diffusion Large Language Model (Score: 8/10)
- **💡 Innovation**: LLaDA2.0-Uni introduces a unified discrete diffusion large language model (dLLM) that natively integrates multimodal understanding and generation through a MoE-based backbone and diffusion decoder.
- **⚠️ Limitations**: The model's performance in real-time robotic manipulation tasks is not demonstrated, limiting its applicability in embodied AI scenarios.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.20796)
- **👥 Authors**: Inclusion AI, Tiwei Bie, Haoxing Chen, Tieyuan Chen, Zhenglin Cheng, Long Cui, Kai Gan, Zhicheng Huang, Zhenzhong Lan, Haoquan Li, Jianguo Li, Tao Lin, Qi Qin, Hongjun Wang, Xiaomei Wang, Haoyuan Wu, Yi Xin, Junbo Zhao
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #LLM #VLA #World_Model

---

### 🔥 Cortex 2.0: Grounding World Models in Real-World Industrial Deployment (Score: 8/10)
- **💡 Innovation**: Cortex 2.0 integrates a visual-latent world model with a multi-criteria scoring function (PRO) for k-step lookahead planning in industrial robotic manipulation.
- **⚠️ Limitations**: The paper does not explicitly address the computational overhead of generating and scoring multiple future trajectories in real-time industrial settings.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.20246)
- **👥 Authors**: Adriana Aida, Walida Amer, Katarina Bankovic, Dhruv Behl, Fabian Busch, Annie Bhalla, Minh Duong, Florian Gienger, Rohan Godse, Denis Grachev, Ralf Gulde, Elisa Hagensieker, Junpeng Hu, Shivam Joshi, Tobias Knoblauch, Likith Kumar, Damien LaRocque, Keerthana Lokesh, Omar Moured, Khiem Nguyen, Christian Preyss, Ranjith Sriganesan, Vikram Singh, Carsten Sponner, Anh Tong, Dominik Tuscher, Marc Tuscher, Pavan Upputuri
- **🏷️ Tags**: #World_Model #Robot_Manipulation #VLA #Embodied_AI #Reinforcement_Learning

---

### 🔥 COMPASS: COntinual Multilingual PEFT with Adaptive Semantic Sampling (Score: 8/10)
- **💡 Innovation**: COMPASS introduces a distribution-aware sampling strategy using multilingual embeddings and clustering to maximize positive cross-lingual transfer while minimizing interference.
- **⚠️ Limitations**: The method relies heavily on the availability of high-quality multilingual embeddings and may struggle with extremely low-resource languages.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.20720)
- **👥 Authors**: Noah Flynn
- **🏷️ Tags**: #LLM #Foundation_Model #Multilingual_AI

---

### ✨ Transient Turn Injection: Exposing Stateless Multi-Turn Vulnerabilities in Large Language Models (Score: 7/10)
- **💡 Innovation**: Introduces Transient Turn Injection (TTI), a novel multi-turn attack technique exploiting stateless moderation in LLMs by distributing adversarial intent across isolated interactions.
- **⚠️ Limitations**: The paper does not fully detail the mitigation strategies' effectiveness or scalability across diverse real-world deployments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.21860v1)
- **👥 Authors**: Naheed Rayhan, Sohely Jahan
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Near-Future Policy Optimization (Score: 7/10)
- **💡 Innovation**: Proposes Near-Future Policy Optimization (NPO), a mixed-policy scheme that uses a policy's own near-future checkpoints as a source of auxiliary trajectories to balance quality and variance cost.
- **⚠️ Limitations**: Relies on manual interventions for early-stage bootstrapping and late-stage plateau breakthrough, which may limit scalability.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.20733)
- **👥 Authors**: Chuanyu Qin, Chenxu Yang, Qingyi Si, Naibin Gu, Dingyu Yao, Zheng Lin, Peng Fu, Nan Duan, Jiaqi Wang
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### ✨ DR-Venus: Towards Frontier Edge-Scale Deep Research Agents with Only 10K Open Data (Score: 7/10)
- **💡 Innovation**: Combines agentic SFT with turn-level RL rewards based on information gain and format-aware regularization to enhance small model performance in long-horizon tasks.
- **⚠️ Limitations**: Limited to 10K open-data, which may restrict generalization to more diverse or complex tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.19859)
- **👥 Authors**: Venus Team, Sunhao Dai, Yong Deng, Jinzhen Lin, Yusheng Song, Guoqing Wang, Xiaofeng Wu, Yuqi Zhou, Shuo Yang, Zhenzhe Ying, Zhanwei Zhang, Changhua Meng, Weiqiang Wang
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### ✨ Benign Fine-Tuning Breaks Safety Alignment in Audio LLMs (Score: 7/10)
- **💡 Innovation**: Decomposes embedding proximity into semantic, acoustic, and mixed axes to study safety degradation in Audio LLMs, revealing architecture-conditioned vulnerabilities.
- **⚠️ Limitations**: Focuses solely on audio LLMs, leaving open whether findings generalize to other modalities or more diverse architectures.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.16659)
- **👥 Authors**: Jaechul Roh, Amir Houmansadr
- **🏷️ Tags**: #LLM #Foundation_Model #Embodied_AI

---


