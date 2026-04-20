# 📅 2026-03-20 - Paper Digest
## Summary
Total Papers: 16 | High Impact: 4

## 📝 Papers List
### 🔥 Generation Models Know Space: Unleashing Implicit 3D Priors for Scene Understanding (Score: 8/10)
- **💡 Innovation**: The method extracts spatiotemporal features from intermediate noise levels of a pre-trained video diffusion model to provide dense geometric cues to MLLMs via a token-level adaptive gated fusion mechanism.
- **⚠️ Limitations**: The reliance on pre-trained video diffusion models may introduce significant computational overhead during inference and potential biases inherent in the generative training data.
- **🔗 Link**: [[Generation_Models_Know_Space]]
- **👥 Authors**: Xianjin Wu, Dingkang Liang, Tianrui Feng, Kui Xia, Yumeng Zhang, Xiaofan Li, Xiao Tan, Xiang Bai
- **🏷️ Tags**: #World_Model #Diffusion_Model #Embodied_AI #Foundation_Model #Robot_Manipulation

---

### 🔥 FASTER: Rethinking Real-Time Flow VLAs (Score: 8/10)
- **💡 Innovation**: The paper introduces a Horizon-Aware Schedule for flow-based VLAs that prioritizes near-term action denoising to reduce reaction latency without sacrificing long-horizon trajectory quality.
- **⚠️ Limitations**: The approach relies on the specific structure of flow-based action models and may not generalize to autoregressive or non-flow-based VLA architectures.
- **🔗 Link**: [[FASTER]]
- **👥 Authors**: Yuxiang Lu, Zhe Liu, Xianzhe Fan, Zhenya Yang, Jinghua Hou, Junyi Li, Kaixin Ding, Hengshuang Zhao
- **🏷️ Tags**: #VLA #Diffusion_Model #Robot_Manipulation #Embodied_AI

---

### ✨ MHPO: Modulated Hazard-aware Policy Optimization for Stable Reinforcement Learning (Score: 7/10)
- **💡 Innovation**: MHPO introduces a Log-Fidelity Modulator for differentiable importance ratio clipping and a Decoupled Hazard Penalty based on survival analysis to regulate asymmetric policy updates in GRPO-based training.
- **⚠️ Limitations**: The abstract lacks specific details on how the hazard-aware mechanism scales to high-dimensional continuous action spaces typical in robotics, focusing primarily on text and vision-language reasoning benchmarks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16929)
- **👥 Authors**: Hongjun Wang, Wei Liu, Weibo Gu, Xing Sun, Kai Han
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Loc3R-VLM: Language-based Localization and 3D Reasoning with Vision-Language Models (Score: 7/10)
- **💡 Innovation**: The framework integrates global layout reconstruction and egocentric situation modeling into a 2D VLM to ground language in 3D space using monocular video and camera pose priors.
- **⚠️ Limitations**: The reliance on pre-trained 3D foundation models for camera pose priors may introduce error propagation and limit performance in dynamic or unconstrained environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.18002)
- **👥 Authors**: Kevin Qu, Haozhe Qi, Mihai Dusmanu, Mahdi Rad, Rui Wang, Marc Pollefeys
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #LLM

---

### ✨ Bridging Semantic and Kinematic Conditions with Diffusion-based Discrete Motion Tokenizer (Score: 6/10)
- **💡 Innovation**: The framework introduces a diffusion-based discrete motion tokenizer that decouples semantic planning from fine-grained kinematic reconstruction to improve motion fidelity and controllability.
- **⚠️ Limitations**: The evaluation is restricted to the HumanML3D dataset, leaving the efficacy of the motion tokenizer in complex, real-world robotic manipulation or embodied environments unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19227)
- **👥 Authors**: Chenyang Gu, Mingyuan Zhang, Haozhe Xie, Zhongang Cai, Lei Yang, Ziwei Liu
- **🏷️ Tags**: #Diffusion_Model #Embodied_AI

---

### ✨ Memento-Skills: Let Agents Design Agents (Score: 6/10)
- **💡 Innovation**: The system implements a self-improving agent architecture that treats skill libraries as persistent, evolving memory modules updated via a Read-Write Reflective Learning mechanism without modifying LLM weights.
- **⚠️ Limitations**: The approach is primarily validated on text-based reasoning benchmarks rather than physical embodied tasks, limiting its immediate applicability to robot control or manipulation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.18743)
- **👥 Authors**: Huichi Zhou, Siyuan Guo, Anjie Liu, Zhongwei Yu, Ziqin Gong, Bowen Zhao, Zhixun Chen, Menglong Zhang, Yihang Chen, Jinsong Li, Runyu Yang, Qiangbin Liu, Xinlei Yu, Jianmin Zhou, Na Wang, Chunyang Sun, Jun Wang
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ VTC-Bench: Evaluating Agentic Multimodal Models via Compositional Visual Tool Chaining (Score: 6/10)
- **💡 Innovation**: The paper introduces a benchmark framework that evaluates MLLM tool-use proficiency through a hierarchical composition of 32 OpenCV-based visual operations.
- **⚠️ Limitations**: The benchmark focuses on digital visual processing pipelines rather than physical agentic interaction, limiting its direct applicability to embodied robotics or closed-loop control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15030)
- **👥 Authors**: Xuanyu Zhu, Yuhao Dong, Rundong Wang, Yang Shi, Zhipeng Wu, Yinlun Peng, YiFan Zhang, Yihang Lou, Yuanxing Zhang, Ziwei Liu, Yan Bai, Yuan Zhou
- **🏷️ Tags**: #Foundation_Model #LLM #VLA

---

### ✨ ProRL Agent: Rollout-as-a-Service for RL Training of Multi-Turn LLM Agents (Score: 6/10)
- **💡 Innovation**: The paper introduces a decoupled, API-based infrastructure for managing multi-turn LLM agent rollouts, abstracting environment interaction from the core RL training loop.
- **⚠️ Limitations**: The framework focuses exclusively on software-based agentic tasks rather than physical embodied environments, limiting its direct applicability to robotics hardware.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.18815)
- **👥 Authors**: Hao Zhang, Mingjie Liu, Shaokun Zhang, Songyang Han, Jian Hu, Zhenghui Jin, Yuchi Zhang, Shizhe Diao, Ximing Lu, Binfeng Xu, Zhiding Yu, Jan Kautz, Yi Dong
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Nemotron-Cascade 2: Post-Training LLMs with Cascade RL and Multi-Domain On-Policy Distillation (Score: 5/10)
- **💡 Innovation**: The paper introduces a multi-domain on-policy distillation technique integrated into a Cascade RL framework to improve reasoning density in compact Mixture-of-Experts models.
- **⚠️ Limitations**: The methodology is strictly evaluated on static reasoning and coding benchmarks, lacking any empirical evidence or application in embodied or robotic control tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19220)
- **👥 Authors**: Zhuolin Yang, Zihan Liu, Yang Chen, Wenliang Dai, Boxin Wang, Sheng-Chieh Lin, Chankyu Lee, Yangyi Chen, Dongfu Jiang, Jiafan He, Renjie Pi, Grace Lam, Nayeon Lee, Alexander Bukharin, Mohammad Shoeybi, Bryan Catanzaro, Wei Ping
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ LVOmniBench: Pioneering Long Audio-Video Understanding Evaluation for Omnimodal LLMs (Score: 5/10)
- **💡 Innovation**: The paper introduces a benchmark specifically designed to evaluate long-form audio-visual comprehension in multimodal models using 275 videos ranging from 10 to 90 minutes.
- **⚠️ Limitations**: The benchmark focuses on passive video understanding rather than active agent interaction or decision-making, limiting its direct utility for embodied control tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19217)
- **👥 Authors**: Keda Tao, Yuhua Zheng, Jia Xu, Wenjie Du, Kele Shao, Hesong Wang, Xueyi Chen, Xin Jin, Junhan Zhu, Bohan Yu, Weiqiang Wang, Jian Liu, Can Qin, Yulun Zhang, Ming-Hsuan Yang, Huan Wang
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ ReactMotion: Generating Reactive Listener Motions from Speaker Utterance (Score: 5/10)
- **💡 Innovation**: The paper introduces a preference-oriented generative framework that models the one-to-many mapping of human listener reactions using a multi-candidate dataset and preference-based training objectives.
- **⚠️ Limitations**: The approach is focused on human-human nonverbal communication synthesis rather than physical robot control or embodied interaction, limiting its direct utility for robotic manipulation or navigation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15083)
- **👥 Authors**: Cheng Luo, Bizhu Wu, Bing Li, Jianfeng Ren, Ruibin Bai, Rong Qu, Linlin Shen, Bernard Ghanem
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ Cognitive Mismatch in Multimodal Large Language Models for Discrete Symbol Understanding (Score: 5/10)
- **💡 Innovation**: The paper introduces a multi-domain benchmark specifically designed to quantify the discrepancy between MLLM visual symbol recognition and their high-level reasoning capabilities.
- **⚠️ Limitations**: The study focuses on static symbolic interpretation rather than the dynamic, spatial, or temporal grounding required for embodied robotics tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.18472)
- **👥 Authors**: Yinghui Li, Jiayi Kuang, Peng Xing, Daixian Liu, Junnan Dong, Shu-Yu Guo, Yangning Li, Qingyu Zhou, Wenhao Jiang, Hai-Tao Zheng, Ying Shen, Liang Lin, Philip S. Yu
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ Reasoning over mathematical objects: on-policy reward modeling and test time aggregation (Score: 5/10)
- **💡 Innovation**: The paper introduces an on-policy reward modeling and test-time aggregation framework specifically designed to improve the derivation of structured mathematical objects rather than simple numerical outputs.
- **⚠️ Limitations**: The methodology is strictly confined to symbolic mathematical reasoning and lacks any grounding in physical environments or multimodal sensorimotor data.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.18886)
- **👥 Authors**: Pranjal Aggarwal, Marjan Ghazvininejad, Seungone Kim, Ilia Kulikov, Jack Lanchantin, Xian Li, Tianjian Li, Bo Liu, Graham Neubig, Anaelia Ovalle, Swarnadeep Saha, Sainbayar Sukhbaatar, Sean Welleck, Jason Weston, Chenxi Whitehouse, Adina Williams, Jing Xu, Ping Yu, Weizhe Yuan, Jingyu Zhang, Wenting Zhao
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 F2LLM-v2: Inclusive, Performant, and Efficient Embeddings for a Multilingual World (Score: 4/10)
- **💡 Innovation**: The paper introduces a multi-stage training pipeline combining matryoshka learning, model pruning, and knowledge distillation to optimize multilingual embedding models across a wide range of parameter scales.
- **⚠️ Limitations**: The work focuses exclusively on text-based semantic retrieval and lacks integration with visual or embodied modalities required for robotics applications.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19223)
- **👥 Authors**: Ziyin Zhang, Zihan Liao, Hang Yu, Peng Di, Rui Wang
- **🏷️ Tags**: #Foundation_Model #LLM

---

### 📄 What Really Controls Temporal Reasoning in Large Language Models: Tokenisation or Representation of Time? (Score: 4/10)
- **💡 Innovation**: The paper introduces a multilingual temporal reasoning benchmark and a Date Fragmentation Ratio (mDFR) metric to quantify how tokenization artifacts impact temporal reasoning performance across diverse calendar systems.
- **⚠️ Limitations**: The study is strictly confined to linguistic and symbolic temporal reasoning within text-only LLMs, lacking any connection to physical world dynamics or embodied temporal grounding.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19017)
- **👥 Authors**: Gagan Bhatia, Ahmad Muhammad Isa, Maxime Peyrard, Wei Zhao
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Mending the Holes: Mitigating Reward Hacking in Reinforcement Learning for Multilingual Translation (Score: 3/10)
- **💡 Innovation**: The paper introduces WALAR, a reinforcement learning framework that utilizes word and language alignment to mitigate reward hacking in quality estimation models during multilingual translation training.
- **⚠️ Limitations**: The methodology is strictly confined to natural language translation tasks and lacks any connection to embodied agents, physical interaction, or multimodal action spaces.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.13045)
- **👥 Authors**: Yifeng Liu, Siqi Ouyang, Yatish Hosmane Revanasiddappa, Lei Li
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---


