# 📅 2026-03-06 - Paper Digest
## Summary
Total Papers: 11 | High Impact: 1

## 📝 Papers List
### 🔥 Latent Particle World Models: Self-supervised Object-centric Stochastic Dynamics Modeling (Score: 8/10)
- **💡 Innovation**: The paper introduces a self-supervised, object-centric world model that learns stochastic dynamics through latent particle representations, enabling scene decomposition and action-conditioned prediction without explicit supervision.
- **⚠️ Limitations**: The reliance on latent particle dynamics may struggle with complex, non-rigid object interactions or highly occluded environments compared to more holistic generative approaches.
- **🔗 Link**: [[Latent Particle World Models]]
- **👥 Authors**: Tal Daniel, Carl Qi, Dan Haramati, Amir Zadeh, Chuan Li, Aviv Tamar, Deepak Pathak, David Held
- **🏷️ Tags**: #World_Model #Embodied_AI #Robot_Manipulation

---

### ✨ DreamWorld: Unified World Modeling in Video Generation (Score: 6/10)
- **💡 Innovation**: The paper introduces a Joint World Modeling Paradigm that integrates heterogeneous world knowledge (physical, 3D, temporal) into video generation via Consistent Constraint Annealing and Multi-Source Inner-Guidance.
- **⚠️ Limitations**: The paper lacks explicit evaluation on embodied tasks or closed-loop control, focusing primarily on video generation benchmarks rather than actionable robot manipulation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.00466)
- **👥 Authors**: Boming Tan, Xiangdong Zhang, Ning Liao, Yuqing Zhang, Shaofeng Zhang, Xue Yang, Qi Fan, Yanyong Zhang
- **🏷️ Tags**: #World_Model #Diffusion_Model #Foundation_Model

---

### ✨ Lightweight Visual Reasoning for Socially-Aware Robots (Score: 6/10)
- **💡 Innovation**: The paper introduces a lightweight, gated MLP feedback loop that re-injects LLM-derived text context into the vision encoder to refine scene interpretation for robotics tasks.
- **⚠️ Limitations**: The evaluation is primarily focused on perception and reasoning tasks rather than closed-loop control, and the performance gains on navigation tasks appear inconsistent across different model architectures.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03942)
- **👥 Authors**: Alessio Galatolo, Ronald Cumbal, Alexandros Rouchitsas, Katie Winkle, Didem Gürdür Broo, Ginevra Castellano
- **🏷️ Tags**: #Embodied_AI #LLM #Foundation_Model

---

### ✨ MASQuant: Modality-Aware Smoothing Quantization for Multimodal Large Language Models (Score: 5/10)
- **💡 Innovation**: The paper introduces a modality-aware smoothing technique and cross-modal compensation via SVD whitening to mitigate quantization errors specifically arising from the heterogeneous activation distributions in multimodal large language models.
- **⚠️ Limitations**: The evaluation is restricted to standard MLLM benchmarks (like LLaVA) and does not demonstrate the efficacy of the quantization method on resource-constrained embodied agents or VLA models where latency and precision are critical.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.04800)
- **👥 Authors**: Lulu Hu, Wenhu Xiao, Xin Chen, Xinhua Xu, Bowen Xu, Kun Li, Yongliang Tao
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Towards Multimodal Lifelong Understanding: A Dataset and Agentic Baseline (Score: 5/10)
- **💡 Innovation**: The paper introduces a recursive belief state mechanism for long-term memory management in multimodal agents to mitigate context saturation and localization collapse over extended temporal horizons.
- **⚠️ Limitations**: The work focuses primarily on video understanding and agentic reasoning rather than physical interaction, lacking direct application to robot control or manipulation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.05484)
- **👥 Authors**: Guo Chen, Lidong Lu, Yicheng Liu, Liangrui Dong, Lidong Zou, Jixin Lv, Zhenquan Li, Xinyi Mao, Baoqi Pei, Shihao Wang, Zhiqi Li, Karan Sapra, Fuxiao Liu, Yin-Dong Zheng, Yifei Huang, Limin Wang, Zhiding Yu, Andrew Tao, Guilin Liu, Tong Lu
- **🏷️ Tags**: #LLM #Foundation_Model #Embodied_AI

---

### ✨ Truncated Step-Level Sampling with Process Rewards for Retrieval-Augmented Reasoning (Score: 5/10)
- **💡 Innovation**: The paper introduces truncated step-level sampling to reduce gradient variance in reinforcement learning by sharing prefixes across trajectories, combined with LLM-as-judge process rewards.
- **⚠️ Limitations**: The approach is evaluated exclusively on text-based QA benchmarks, leaving its applicability to high-dimensional, continuous action spaces in embodied robotics unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.23440)
- **👥 Authors**: Chris Samarinas, Haw-Shiuan Chang, Hamed Zamani
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Timer-S1: A Billion-Scale Time Series Foundation Model with Serial Scaling (Score: 4/10)
- **💡 Innovation**: The paper introduces Serial-Token Prediction (STP) and a Mixture-of-Experts architecture to scale time series forecasting to 8.3B parameters while avoiding traditional rolling-style inference.
- **⚠️ Limitations**: The work is strictly focused on time series forecasting and lacks any integration with embodied agents, multi-modal action spaces, or physical environment interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.04791)
- **👥 Authors**: Yong Liu, Xingjian Su, Shiyu Wang, Haoran Zhang, Haixuan Liu, Yuxuan Wang, Zhou Ye, Yang Xiang, Jianmin Wang, Mingsheng Long
- **🏷️ Tags**: #Foundation_Model

---

### 📄 Mozi: Governed Autonomy for Drug Discovery LLM Agents (Score: 3/10)
- **💡 Innovation**: The paper introduces a dual-layer architecture (Control Plane and Workflow Plane) that enforces hierarchical governance and stateful skill graphs to constrain LLM agent behavior in high-stakes drug discovery pipelines.
- **⚠️ Limitations**: The work is entirely focused on digital/computational workflows and lacks any connection to physical embodiment, robotic manipulation, or sensorimotor control, making it irrelevant to the specified robotics-focused research interests.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03655)
- **👥 Authors**: He Cao, Siyu Liu, Fan Zhang, Zijing Liu, Hao Li, Bin Feng, Shengyuan Bai, Leqing Chen, Kai Xie, Yu Li
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 MOOSE-Star: Unlocking Tractable Training for Scientific Discovery by Breaking the Complexity Barrier (Score: 2/10)
- **💡 Innovation**: The paper introduces a hierarchical search and decomposition framework to reduce the computational complexity of generative hypothesis formation in scientific discovery from exponential to logarithmic.
- **⚠️ Limitations**: The work is entirely focused on abstract scientific reasoning and lacks any connection to physical embodiment, sensorimotor control, or the specific challenges of robot manipulation and world modeling.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03756)
- **👥 Authors**: Zonglin Yang, Lidong Bing
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 DARE: Aligning LLM Agents with the R Statistical Ecosystem via Distribution-Aware Retrieval (Score: 2/10)
- **💡 Innovation**: The paper introduces a distribution-aware retrieval mechanism that incorporates statistical data characteristics into function embeddings to improve the selection of R packages for LLM-based data analysis.
- **⚠️ Limitations**: The work is strictly confined to the domain of statistical software engineering and data analysis, offering no methodological contributions or relevance to embodied agents, physical control, or multimodal perception.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.04743)
- **👥 Authors**: Maojun Sun, Yue Wu, Yifei Xie, Ruijian Han, Binyan Jiang, Defeng Sun, Yancheng Yuan, Jian Huang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 KARL: Knowledge Agents via Reinforcement Learning (Score: 2/10)
- **💡 Innovation**: The paper introduces an iterative off-policy reinforcement learning paradigm for training enterprise search agents using synthetic data generated via long-horizon reasoning.
- **⚠️ Limitations**: The work is entirely focused on digital knowledge retrieval and agentic search, lacking any connection to physical embodiment, sensorimotor control, or spatial reasoning.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.05218)
- **👥 Authors**: Jonathan D. Chang, Andrew Drozdov, Shubham Toshniwal, Owen Oertell, Alexander Trott, Jacob Portes, Abhay Gupta, Pallavi Koppol, Ashutosh Baheti, Sean Kulinski, Ivan Zhou, Irene Dea, Krista Opsahl-Ong, Simon Favreau-Lessard, Sean Owen, Jose Javier Gonzalez Ortiz, Arnav Singhvi, Xabi Andrade, Cindy Wang, Kartik Sreenivasan, Sam Havens, Jialu Liu, Peyton DeNiro, Wen Sun, Michael Bendersky, Jonathan Frankle
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---


