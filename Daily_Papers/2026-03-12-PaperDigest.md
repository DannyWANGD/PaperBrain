# 📅 2026-03-12 - Paper Digest
## Summary
Total Papers: 36 | High Impact: 5

## 📝 Papers List
### 🔥 EmboAlign: Aligning Video Generation with Compositional Constraints for Zero-Shot Manipulation (Score: 8/10)
- **💡 Innovation**: EmboAlign introduces a data-free framework that leverages VLM-based compositional constraints to filter and refine VGM-generated rollouts, bridging the gap between generative video priors and precise robot control.
- **⚠️ Limitations**: The reliance on inference-time optimization and VLM-based constraint extraction may introduce significant latency, potentially hindering real-time performance in dynamic environments.
- **🔗 Link**: [[EmboAlign]]
- **👥 Authors**: Gehao Zhang, Zhenyang Ni, Payal Mohapatra, Han Liu, Ruohan Zhang, Qi Zhu
- **🏷️ Tags**: #Robot_Manipulation #Diffusion_Model #Embodied_AI #Foundation_Model #LLM

---

### ✨ LABSHIELD: A Multimodal Benchmark for Safety-Critical Reasoning and Planning in Scientific Laboratories (Score: 7/10)
- **💡 Innovation**: The paper introduces a specialized, OSHA-grounded benchmark for evaluating the safety-critical reasoning and hazard identification capabilities of multimodal agents in high-stakes laboratory environments.
- **⚠️ Limitations**: The evaluation is primarily focused on reasoning and planning benchmarks rather than closed-loop physical execution or real-world robot deployment, leaving the gap between safety-aware planning and successful manipulation unaddressed.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.11987v1)
- **👥 Authors**: Qianpu Sun, Xiaowei Chi, Yuhan Rui, Ying Li, Kuangzhi Ge, Jiajun Li, Sirui Han, Shanghang Zhang
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #LLM #Robot_Manipulation

---

### ✨ RetroAgent: From Solving to Evolving via Retrospective Dual Intrinsic Feedback (Score: 7/10)
- **💡 Innovation**: RetroAgent introduces a dual intrinsic feedback mechanism that combines numerical subtask tracking with a language-based memory buffer retrieved via a novel SimUtil-UCB strategy to facilitate continuous experiential learning in RL agents.
- **⚠️ Limitations**: The paper focuses on text-based or logic-heavy environments (ALFWorld, WebShop) rather than high-dimensional continuous control tasks typical of physical robot manipulation, leaving the scalability to real-world embodied settings unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08561)
- **👥 Authors**: Xiaoying Zhang, Zichen Liu, Yipeng Zhang, Xia Hu, Wenqi Shao
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model #Embodied_AI

---

### ✨ Lost in Backpropagation: The LM Head is a Gradient Bottleneck (Score: 7/10)
- **💡 Innovation**: The paper identifies that the LM head acts as a 'gradient bottleneck' where the projection from a low-dimensional hidden space to a high-dimensional vocabulary space suppresses the vast majority of gradient information during backpropagation.
- **⚠️ Limitations**: The study focuses primarily on standard language modeling tasks and does not explicitly demonstrate how this gradient bottleneck manifests in the multimodal or action-space heads typically used in VLA or Embodied AI models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10145)
- **👥 Authors**: Nathan Godey, Yoav Artzi
- **🏷️ Tags**: #LLM #Foundation_Model #VLA

---

### ✨ StyleVLA: Driving Style-Aware Vision Language Action Model for Autonomous Driving (Score: 7/10)
- **💡 Innovation**: StyleVLA introduces a physics-informed hybrid loss function that integrates kinematic consistency constraints with continuous regression heads into a VLA framework to enable style-aware, physically plausible trajectory generation.
- **⚠️ Limitations**: The reliance on a relatively small, curated instruction dataset may limit generalization to long-tail edge cases compared to models trained on massive, diverse internet-scale driving data.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09482)
- **👥 Authors**: Yuan Gao, Dengyuan Hua, Mattia Piccinini, Finn Rasmus Schäfer, Korbinian Moller, Lin Li, Johannes Betz
- **🏷️ Tags**: #VLA #Foundation_Model #LLM #Embodied_AI

---

### ✨ Cross-Domain Policy Optimization via Bellman Consistency and Hybrid Critics (Score: 6/10)
- **💡 Innovation**: The paper introduces 'cross-domain Bellman consistency' as a metric to quantify transferability and a 'hybrid critic' (QAvatar) to adaptively weight source-domain knowledge during target-domain reinforcement learning.
- **⚠️ Limitations**: The approach relies on the assumption of structural similarity between domains, and the paper lacks evaluation on high-dimensional, vision-based foundation model backbones common in modern Embodied AI.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12087v1)
- **👥 Authors**: Ming-Hong Chen, Kuan-Chen Pan, You-De Huang, Xi Liu, Ping-Chun Hsieh
- **🏷️ Tags**: #Reinforcement_Learning #Robot_Manipulation #Embodied_AI

---

### ✨ Can RL Improve Generalization of LLM Agents? An Empirical Study (Score: 6/10)
- **💡 Innovation**: The paper provides a systematic empirical evaluation of how Reinforcement Fine-Tuning (RFT) affects the generalization capabilities of LLM agents across task difficulty, environment shifts, and sequential learning scenarios.
- **⚠️ Limitations**: The study focuses primarily on text-based or high-level decision-making environments, leaving a gap in how these findings translate to low-level continuous control in physical robot manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12011v1)
- **👥 Authors**: Zhiheng Xi, Xin Guo, Jiaqi Liu, Jiazheng Zhang, Yutao Fan, Zhihao Zhang, Shichun Liu, Mingxu Chai, Xiaowei Shi, Yitao Zhai, Xunliang Cai, Tao Gui, Qi Zhang, Xuanjing Huang
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Embodied_AI #Foundation_Model

---

### ✨ MA-EgoQA: Question Answering over Egocentric Videos from Multiple Embodied Agents (Score: 6/10)
- **💡 Innovation**: The paper introduces a novel benchmark, MA-EgoQA, specifically designed to evaluate the ability of models to process and reason over multiple, simultaneous long-horizon egocentric video streams from different embodied agents.
- **⚠️ Limitations**: The proposed baseline, EgoMAS, is relatively simple and the study lacks a closed-loop control evaluation, focusing primarily on passive video understanding rather than active agent coordination.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09827)
- **👥 Authors**: Kangsan Kim, Yanlai Yang, Suji Kim, Woongyeong Yeo, Youngwan Lee, Mengye Ren, Sung Ju Hwang
- **🏷️ Tags**: #Embodied_AI #LLM #Foundation_Model

---

### ✨ Bootstrapping Exploration with Group-Level Natural Language Feedback in Reinforcement Learning (Score: 6/10)
- **💡 Innovation**: GOLF introduces a framework that leverages group-level natural language feedback—combining external critiques and intra-group failure patterns—to guide RL exploration through actionable refinements.
- **⚠️ Limitations**: The reliance on high-quality language feedback may be difficult to scale to complex, non-verifiable robotic tasks where generating precise, actionable natural language critiques is non-trivial.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.04597)
- **👥 Authors**: Lei Huang, Xiang Cheng, Chenxiao Zhao, Guobin Shen, Junjie Yang, Xiaocheng Feng, Yuxuan Gu, Xing Yu, Bing Qin
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Embodied_AI

---

### ✨ Hindsight Credit Assignment for Long-Horizon LLM Agents (Score: 6/10)
- **💡 Innovation**: The paper introduces HCAPO, a framework that utilizes the LLM itself as a post-hoc critic to perform hindsight credit assignment, refining step-level Q-values for long-horizon decision-making.
- **⚠️ Limitations**: The approach relies on the LLM's self-reasoning capabilities for credit assignment, which may introduce significant computational overhead and potential hallucination-based bias in complex, non-textual environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08754)
- **👥 Authors**: Hui-Ze Tan, Xiao-Wen Yang, Hao Chen, Jie-Jing Shao, Yi Wen, Yuteng Shen, Weihong Luo, Xiku Du, Lan-Zhe Guo, Yu-Feng Li
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Taming the Adversary: Stable Minimax Deep Deterministic Policy Gradient via Fractional Objectives (Score: 5/10)
- **💡 Innovation**: The paper introduces a fractional objective function within a minimax DDPG framework to stabilize the training of robust policies by balancing task performance against adversarial disturbance magnitude.
- **⚠️ Limitations**: The evaluation is restricted to standard MuJoCo control benchmarks, lacking validation on complex, high-dimensional robot manipulation tasks or real-world hardware deployment.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12110v1)
- **👥 Authors**: Taeho Lee, Donghwan Lee
- **🏷️ Tags**: #Reinforcement_Learning #Embodied_AI

---

### ✨ On Information Self-Locking in Reinforcement Learning for Active Reasoning of LLM agents (Score: 5/10)
- **💡 Innovation**: The paper identifies 'information self-locking' as a failure mode in RL-trained LLM agents and proposes a directional critique mechanism to decouple action selection from belief tracking during training.
- **⚠️ Limitations**: The study focuses exclusively on text-based reasoning tasks, leaving the applicability of this 'self-locking' phenomenon and the proposed solution to embodied, multi-modal, or physical robot environments unverified.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12109v1)
- **👥 Authors**: Deyu Zou, Yongqiang Chen, Fan Feng, Mufei Li, Pan Li, Yu Gong, James Cheng
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ EvoTok: A Unified Image Tokenizer via Residual Latent Evolution for Visual Understanding and Generation (Score: 5/10)
- **💡 Innovation**: EvoTok introduces a residual evolution process within a shared latent space, using cascaded residual vector quantization to unify fine-grained pixel reconstruction and high-level semantic abstraction.
- **⚠️ Limitations**: The paper lacks evaluation in embodied or temporal contexts, leaving it unclear how this tokenizer performs for video-based world modeling or action-conditioned generation required for robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12108v1)
- **👥 Authors**: Yan Li, Ning Liao, Xiangyu Zhao, Shaofeng Zhang, Xiaoxing Wang, Yifan Yang, Junchi Yan, Xue Yang
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ Sim-to-reality adaptation for Deep Reinforcement Learning applied to an underwater docking application (Score: 5/10)
- **💡 Innovation**: The paper presents a systematic pipeline for deploying PPO-based DRL for underwater docking by integrating high-fidelity digital twin dynamics and domain randomization within a multiprocessing simulation framework.
- **⚠️ Limitations**: The approach relies on traditional DRL and simulation-based training without leveraging modern foundation models, world models, or vision-language-action (VLA) architectures, making it an incremental application of established techniques.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12020v1)
- **👥 Authors**: Alaaeddine Chaarani, Narcis Palomeras, Pere Ridao
- **🏷️ Tags**: #Sim2Real #Reinforcement_Learning #Embodied_AI

---

### ✨ Learning Visuomotor Policy for Multi-Robot Laser Tag Game (Score: 5/10)
- **💡 Innovation**: The paper introduces a multi-agent distillation framework that transfers teacher-policy knowledge into an end-to-end visuomotor student policy using permutation-invariant feature extraction for dynamic laser tag scenarios.
- **⚠️ Limitations**: The approach lacks the generalization capabilities associated with modern foundation models and relies on a specific, constrained game environment rather than open-world robotic tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.11980v1)
- **👥 Authors**: Kai Li, Shiyu Zhao
- **🏷️ Tags**: #Embodied_AI #Reinforcement_Learning #Sim2Real

---

### ✨ In-Context Reinforcement Learning for Tool Use in Large Language Models (Score: 5/10)
- **💡 Innovation**: The paper introduces In-Context Reinforcement Learning (ICRL), which replaces supervised fine-tuning with a curriculum of few-shot in-context examples during RL rollouts to teach tool-use.
- **⚠️ Limitations**: The approach is evaluated primarily on text-based reasoning and tool-use benchmarks rather than physical robotic manipulation tasks, limiting its immediate applicability to embodied agents.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08068)
- **👥 Authors**: Yaoqi Ye, Yiran Zhao, Keyu Duan, Zeyu Zheng, Kenji Kawaguchi, Cihang Xie, Michael Qizhe Shieh
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Can Large Language Models Keep Up? Benchmarking Online Adaptation to Continual Knowledge Streams (Score: 5/10)
- **💡 Innovation**: The paper introduces OAKS, a benchmark specifically designed to evaluate the ability of LLMs to track and adapt to dynamically evolving facts within streaming knowledge contexts.
- **⚠️ Limitations**: The study focuses exclusively on textual knowledge streams and does not address how these adaptation failures manifest in embodied or multi-modal robotic control tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07392)
- **👥 Authors**: Jiyeon Kim, Hyunji Lee, Dylan Zhou, Sue Hyun Park, Seunghyun Yoon, Trung Bui, Franck Dernoncourt, Sungmin Cha, Minjoon Seo
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ CodePercept: Code-Grounded Visual STEM Perception for MLLMs (Score: 5/10)
- **💡 Innovation**: The paper introduces a 'code-as-perception' paradigm that uses executable code as a structured intermediate representation to improve MLLM visual reasoning in STEM domains.
- **⚠️ Limitations**: The approach is primarily focused on static STEM visual reasoning and lacks direct application or evaluation in dynamic, closed-loop embodied robotic tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10757)
- **👥 Authors**: Tongkun Guan, Zhibo Yang, Jianqiang Wan, Mingkun Yang, Zhengtao Guo, Zijian Hu, Ruilin Luo, Ruize Chen, Songtao Jiang, Peng Wang, Wei Shen, Junyang Lin, Xiaokang Yang
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ V_{0.5}: Generalist Value Model as a Prior for Sparse RL Rollouts (Score: 5/10)
- **💡 Innovation**: The paper introduces a dynamic baseline estimation method that adaptively fuses a pre-trained value model prior with empirical rollout means using real-time statistical hypothesis testing to minimize variance in RLVR.
- **⚠️ Limitations**: The evaluation is restricted to mathematical reasoning benchmarks, leaving the efficacy of this adaptive baseline in high-dimensional, continuous control tasks like robot manipulation unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10848)
- **👥 Authors**: Yi-Kai Zhang, Yueqing Sun, Hongyan Hao, Qi Gu, Xunliang Cai, De-Chuan Zhan, Han-Jia Ye
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Causal Concept Graphs in LLM Latent Space for Stepwise Reasoning (Score: 5/10)
- **💡 Innovation**: The paper introduces Causal Concept Graphs (CCG) to map causal dependencies between interpretable latent features in LLMs using sparse autoencoders and differentiable structure learning.
- **⚠️ Limitations**: The evaluation is restricted to static reasoning benchmarks (ARC, LogiQA) and does not demonstrate how these causal graphs translate to dynamic, embodied, or multi-modal decision-making tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10377)
- **👥 Authors**: Md Muntaqim Meherab, Noor Islam S. Mohammad, Faiza Feroz
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Code-Space Response Oracles: Generating Interpretable Multi-Agent Policies with Large Language Models (Score: 5/10)
- **💡 Innovation**: The paper introduces Code-Space Response Oracles (CSRO), which replaces traditional black-box reinforcement learning oracles in multi-agent systems with LLMs that generate interpretable, human-readable code policies.
- **⚠️ Limitations**: The approach is primarily evaluated in abstract game-theoretic or strategic domains rather than high-dimensional, continuous control tasks typical of physical robotics, raising questions about scalability to real-world embodied environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10098)
- **👥 Authors**: Daniel Hennes, Zun Li, John Schultz, Marc Lanctot
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Resource-Efficient Iterative LLM-Based NAS with Feedback Memory (Score: 4/10)
- **💡 Innovation**: The paper introduces a resource-efficient NAS framework that utilizes a sliding-window feedback memory and dual-LLM specialization to iteratively optimize CNN architectures on consumer-grade hardware.
- **⚠️ Limitations**: The scope is restricted to static image classification tasks, lacking any application to embodied agents, control policies, or the complex action spaces typical of robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12091v1)
- **👥 Authors**: Xiaojie Gu, Dmitry Ignatov, Radu Timofte
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Coarse-Guided Visual Generation via Weighted h-Transform Sampling (Score: 4/10)
- **💡 Innovation**: The paper introduces a training-free guided generation method using h-transform drift functions and a noise-level-aware schedule to steer diffusion models without requiring explicit forward transformation operators.
- **⚠️ Limitations**: The work focuses on general image/video synthesis and lacks evaluation or discussion regarding its applicability to embodied control, robot state estimation, or real-time robotic constraints.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12057v1)
- **👥 Authors**: Yanghao Wang, Ziqi Jiang, Zhen Wang, Long Chen
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 ReMix: Reinforcement routing for mixtures of LoRAs in LLM finetuning (Score: 4/10)
- **💡 Innovation**: The paper introduces a reinforcement learning-based routing mechanism (ReMix) for Mixture-of-LoRAs that replaces learnable routing weights with non-learnable weights to prevent expert collapse and improve parameter efficiency.
- **⚠️ Limitations**: The method is evaluated exclusively on NLP tasks (LLM finetuning) and lacks any demonstration of its utility in embodied settings or vision-language-action models where routing efficiency is also critical.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10160)
- **👥 Authors**: Ruizhong Qiu, Hanqing Zeng, Yinglong Xia, Yiwen Meng, Ren Chen, Jiarui Feng, Dongqi Fu, Qifan Wang, Jiayi Liu, Jun Xiao, Xiangjun Fan, Benyu Zhang, Hong Li, Zhining Liu, Hyunsik Yoo, Zhichen Zeng, Tianxin Wei, Hanghang Tong
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 CLIPO: Contrastive Learning in Policy Optimization Generalizes RLVR (Score: 4/10)
- **💡 Innovation**: The paper introduces a contrastive learning objective into the RLVR framework to regularize LLM reasoning paths by enforcing structural invariance across successful trajectories.
- **⚠️ Limitations**: The work is strictly focused on textual reasoning and lacks any application or evaluation in embodied settings, making its direct utility for robotics or VLA research minimal.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10101)
- **👥 Authors**: Sijia Cui, Pengyu Cheng, Jiajun Song, Yongbo Gai, Guojun Zhang, Zhechao Yu, Jianhe Lin, Xiaoxi Jiang, Guanjun Jiang
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Meissa: Multi-modal Medical Agentic Intelligence (Score: 4/10)
- **💡 Innovation**: The paper introduces a lightweight, offline medical agent that uses stratified supervision and unified trajectory modeling to distill complex agentic behaviors from frontier models into a 4B-parameter model.
- **⚠️ Limitations**: The work focuses exclusively on clinical reasoning and diagnostic tool use rather than physical interaction, making it largely irrelevant to the specific challenges of robot manipulation or embodied control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09018)
- **👥 Authors**: Yixiong Chen, Xinyi Bai, Yue Pan, Zongwei Zhou, Alan Yuille
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 A Robust and Efficient Multi-Agent Reinforcement Learning Framework for Traffic Signal Control (Score: 3/10)
- **💡 Innovation**: The paper introduces a MARL framework for traffic signal control that combines turning ratio randomization, exponential phase duration adjustments, and neighbor-based observations to improve generalization.
- **⚠️ Limitations**: The work is strictly confined to traffic signal control in a simulator and lacks any connection to embodied robotics, vision-language models, or foundation model architectures.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12096v1)
- **👥 Authors**: Sheng-You Huang, Hsiao-Chuan Chang, Yen-Chi Chen, Ting-Han Wei, I-Hau Yeh, Sheng-Yao Kuan, Chien-Yao Wang, Hsuan-Han Lee, I-Chen Wu
- **🏷️ Tags**: #Reinforcement_Learning #Sim2Real

---

### 📄 Frequentist Consistency of Prior-Data Fitted Networks for Causal Inference (Score: 3/10)
- **💡 Innovation**: The paper introduces a one-step posterior correction (OSPC) using martingale posteriors to align Prior-Data Fitted Networks (PFNs) with frequentist consistency in causal inference.
- **⚠️ Limitations**: The work is purely theoretical and methodological regarding causal inference, lacking any application to embodied agents, robot manipulation, or real-world sensorimotor control tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12037v1)
- **👥 Authors**: Valentyn Melnychuk, Vahid Balazadeh, Stefan Feuerriegel, Rahul G. Krishnan
- **🏷️ Tags**: #Foundation_Model

---

### 📄 Cascade: Composing Software-Hardware Attack Gadgets for Adversarial Threat Amplification in Compound AI Systems (Score: 3/10)
- **💡 Innovation**: The paper introduces a framework for composing traditional software/hardware vulnerabilities (e.g., Rowhammer) with algorithmic LLM attacks to amplify security threats in compound AI systems.
- **⚠️ Limitations**: The work focuses exclusively on cybersecurity and system-level vulnerabilities, offering no contributions to robotics, embodied control, or the specific technical domains requested.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12023v1)
- **👥 Authors**: Sarbartha Banerjee, Prateek Sahu, Anjo Vahldiek-Oberwagner, Jose Sanchez Vicarte, Mohit Tiwari
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 LLM2Vec-Gen: Generative Embeddings from Large Language Models (Score: 3/10)
- **💡 Innovation**: The paper introduces a self-supervised method to generate embeddings by training special tokens to represent an LLM's potential response rather than encoding the input directly.
- **⚠️ Limitations**: The work is strictly focused on text-based semantic retrieval and lacks any integration with multimodal, spatial, or action-oriented data required for embodied tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10913)
- **👥 Authors**: Parishad BehnamGhader, Vaibhav Adlakha, Fabian David Schmidt, Nicolas Chapados, Marius Mosbach, Siva Reddy
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 RbtAct: Rebuttal as Supervision for Actionable Review Feedback Generation (Score: 3/10)
- **💡 Innovation**: The paper introduces a method to improve the actionability of AI-generated peer reviews by using author rebuttals as implicit supervision to fine-tune LLMs.
- **⚠️ Limitations**: The work is entirely focused on academic NLP and peer-review processes, offering no direct contribution to embodied intelligence, robot control, or physical world modeling.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09723)
- **👥 Authors**: Sihong Wu, Yiling Ma, Yilun Zhao, Tiansheng Hu, Owen Jiang, Manasi Patwardhan, Arman Cohan
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Human-Centred LLM Privacy Audits: Findings and Frictions (Score: 2/10)
- **💡 Innovation**: The paper introduces a browser-based self-audit tool (LMP2) to empirically measure and quantify the associations LLMs form regarding specific individuals.
- **⚠️ Limitations**: The research focuses exclusively on text-based privacy and social auditing, lacking any connection to physical embodiment, sensorimotor control, or the safety challenges inherent in robotic systems.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12094v1)
- **👥 Authors**: Dimitri Staufer, Kirsten Morehouse, David Hartmann, Bettina Berendt
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 AGMARL-DKS: An Adaptive Graph-Enhanced Multi-Agent Reinforcement Learning for Dynamic Kubernetes Scheduling (Score: 2/10)
- **💡 Innovation**: The paper introduces a multi-agent reinforcement learning framework for Kubernetes scheduling that utilizes Graph Neural Networks for global context awareness and a lexicographical ordering policy for multi-objective optimization.
- **⚠️ Limitations**: The work is entirely focused on cloud-native resource scheduling and lacks any connection to physical embodiment, robotics, or vision-language-action models, making it irrelevant to the specified research interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12031v1)
- **👥 Authors**: Hamed Hamzeh
- **🏷️ Tags**: #Reinforcement_Learning

---

### 📄 An Intent of Collaboration: On Agencies between Designers and Emerging (Intelligent) Technologies (Score: 2/10)
- **💡 Innovation**: The paper explores the human-centric power dynamics and creative agency loss experienced by designers when collaborating with LLMs in digital craftsmanship.
- **⚠️ Limitations**: The study is purely qualitative and sociological, lacking any technical implementation, empirical robotics data, or computational framework relevant to embodied AI or robot manipulation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.12018v1)
- **👥 Authors**: Pei-Ying Lin, Julie Heij, Iris Borst, Britt Joosten, Kristina Andersen, Wijnand IJsselsteijn
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 BTZSC: A Benchmark for Zero-Shot Text Classification Across Cross-Encoders, Embedding Models, Rerankers and LLMs (Score: 2/10)
- **💡 Innovation**: The paper introduces a comprehensive benchmark (BTZSC) to systematically evaluate and compare zero-shot text classification performance across four distinct model architectures: NLI cross-encoders, embedding models, rerankers, and LLMs.
- **⚠️ Limitations**: The work is strictly confined to natural language processing tasks and lacks any connection to embodied agents, multimodal perception, or action-space reasoning relevant to robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.11991v1)
- **👥 Authors**: Ilias Aarab
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 COMIC: Agentic Sketch Comedy Generation (Score: 2/10)
- **💡 Innovation**: The paper introduces a multi-agent framework that utilizes LLM-based critics aligned with human humor preferences to automate the creative pipeline of sketch comedy generation.
- **⚠️ Limitations**: The work focuses entirely on generative media and lacks any connection to physical embodiment, sensorimotor control, or real-world interaction, making it irrelevant to robotics research.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.11048)
- **👥 Authors**: Susung Hong, Brian Curless, Ira Kemelmacher-Shlizerman, Steve Seitz
- **🏷️ Tags**: #LLM #Foundation_Model #Diffusion_Model

---


