# 📅 2026-03-04 - Paper Digest
## Summary
Total Papers: 48 | High Impact: 7

## 📝 Papers List
### 🔥 Beyond Language Modeling: An Exploration of Multimodal Pretraining (Score: 8/10)
- **💡 Innovation**: The paper introduces a unified Transfusion-based architecture that treats vision as a diffusion process and language as next-token prediction, demonstrating that world modeling emerges naturally from scaling these modalities together via Mixture-of-Experts.
- **⚠️ Limitations**: The study focuses on general multimodal pretraining and lacks specific downstream evaluation on complex, long-horizon robotic manipulation tasks or real-world deployment metrics.
- **🔗 Link**: [[Beyond Language Modeling]]
- **👥 Authors**: Shengbang Tong, David Fan, John Nguyen, Ellis Brown, Gaoyue Zhou, Shengyi Qian, Boyang Zheng, Théophane Vallaeys, Junlin Han, Rob Fergus, Naila Murray, Marjan Ghazvininejad, Mike Lewis, Nicolas Ballas, Amir Bar, Michael Rabbat, Jakob Verbeek, Luke Zettlemoyer, Koustuv Sinha, Yann LeCun, Saining Xie
- **🏷️ Tags**: #World_Model #Diffusion_Model #Foundation_Model #LLM #VLA

---

### 🔥 Chain of World: World Model Thinking in Latent Motion (Score: 8/10)
- **💡 Innovation**: CoWVLA introduces a 'Chain of World' paradigm that factorizes video into structure and motion latents to enable continuous temporal reasoning within a VLA framework, bridging the gap between predictive world models and compact latent-action models.
- **⚠️ Limitations**: The reliance on a pretrained video VAE for latent extraction may introduce bottlenecks in reconstruction quality or generalization to novel robotic environments not covered by the VAE's training distribution.
- **🔗 Link**: [[Chain of World]]
- **👥 Authors**: Fuxiang Yang, Donglin Di, Lulu Tang, Xuancheng Zhang, Lei Fan, Hao Li, Chen Wei, Tonghua Su, Baorui Ma
- **🏷️ Tags**: #World_Model #Embodied_AI #Robot_Manipulation #VLA #Foundation_Model

---

### ✨ ManipulationNet: An Infrastructure for Benchmarking Real-World Robot Manipulation with Physical Skill Challenges and Embodied Multimodal Reasoning (Score: 7/10)
- **💡 Innovation**: The paper introduces a standardized, distributed infrastructure for real-world robotic manipulation benchmarking, aiming to solve the reproducibility crisis in physical AI research.
- **⚠️ Limitations**: The infrastructure relies on the adoption of standardized hardware kits, which may create a barrier to entry for labs with heterogeneous or custom robotic setups.
- **🔗 Link**: [[ManipulationNet]]
- **👥 Authors**: Yiting Chen, Kenneth Kimble, Edward H. Adelson, Tamim Asfour, Podshara Chanrungmaneekul, Sachin Chitta, Yash Chitambar, Ziyang Chen, Ken Goldberg, Danica Kragic, Hui Li, Xiang Li, Yunzhu Li, Aaron Prather, Nancy Pollard, Maximo A. Roa-Garzon, Robert Seney, Shuo Sha, Shihefeng Wang, Yu Xiang, Kaifeng Zhang, Yuke Zhu, Kaiyu Hang
- **🏷️ Tags**: #Embodied_AI #Robot_Manipulation #Foundation_Model #VLA

---

### ✨ ArtHOI: Articulated Human-Object Interaction Synthesis by 4D Reconstruction from Video Priors (Score: 7/10)
- **💡 Innovation**: ArtHOI introduces a decoupled 4D reconstruction pipeline that uses monocular video diffusion priors to recover articulated object geometry and human motion without 3D supervision.
- **⚠️ Limitations**: The reliance on monocular video priors and optical flow cues may struggle with complex occlusions or highly dynamic, non-rigid interactions that deviate from the diffusion model's training distribution.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04338v1)
- **👥 Authors**: Zihao Huang, Tianqi Liu, Zhaoxi Chen, Shaocong Xu, Saining Zhang, Lixing Xiao, Zhiguo Cao, Wei Li, Hao Zhao, Ziwei Liu
- **🏷️ Tags**: #Diffusion_Model #Embodied_AI #Robot_Manipulation

---

### ✨ What Does Flow Matching Bring To TD Learning? (Score: 7/10)
- **💡 Innovation**: The paper identifies that flow-matching critics improve TD learning not through distributional modeling, but by providing test-time error recovery via integration and enhanced feature plasticity through dense velocity supervision.
- **⚠️ Limitations**: The empirical validation is primarily focused on high-UTD online RL benchmarks, leaving the scalability and performance of flow-matching critics in complex, high-dimensional robotic manipulation tasks or offline RL settings less explored.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04333v1)
- **👥 Authors**: Bhavya Agrawalla, Michal Nauman, Aviral Kumar
- **🏷️ Tags**: #Reinforcement_Learning #Diffusion_Model

---

### ✨ Utonia: Toward One Encoder for All Point Clouds (Score: 7/10)
- **💡 Innovation**: Utonia introduces a unified self-supervised point transformer encoder trained across highly heterogeneous 3D domains to create a general-purpose representation space for sparse 3D data.
- **⚠️ Limitations**: The paper lacks a detailed analysis of the computational overhead and latency implications of using a unified transformer encoder in real-time robotic control loops compared to domain-specific encoders.
- **🔗 Link**: [[Utonia]]
- **👥 Authors**: Yujia Zhang, Xiaoyang Wu, Yunhan Yang, Xianzhe Fan, Han Li, Yuechen Zhang, Zehao Huang, Naiyan Wang, Hengshuang Zhao
- **🏷️ Tags**: #Embodied_AI #Robot_Manipulation #Foundation_Model #VLA

---

### ✨ Next Embedding Prediction Makes World Models Stronger (Score: 7/10)
- **💡 Innovation**: The paper introduces a decoder-free world model that replaces traditional image reconstruction losses with direct temporal predictive alignment of latent embeddings using a transformer architecture.
- **⚠️ Limitations**: The evaluation is primarily restricted to simulated environments (DeepMind Control Suite and DMLab), leaving the efficacy of the representation learning in real-world, high-variance robotic settings unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.02765)
- **👥 Authors**: George Bredis, Nikita Balagansky, Daniil Gavrilov, Ruslan Rakhimov
- **🏷️ Tags**: #World_Model #Reinforcement_Learning #Embodied_AI

---

### ✨ Helios: Real Real-Time Long Video Generation Model (Score: 6/10)
- **💡 Innovation**: Helios introduces a 14B autoregressive diffusion model that achieves real-time long-video generation by simulating drifting during training and implementing infrastructure-level memory optimizations without relying on standard acceleration heuristics.
- **⚠️ Limitations**: The paper focuses primarily on video generation quality and efficiency rather than demonstrating downstream utility in embodied control, planning, or physical interaction tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04379v1)
- **👥 Authors**: Shenghai Yuan, Yuanyang Yin, Zongjian Li, Xinwei Huang, Xiao Yang, Li Yuan
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #World_Model

---

### ✨ Robustness of Agentic AI Systems via Adversarially-Aligned Jacobian Regularization (Score: 6/10)
- **💡 Innovation**: The paper introduces Adversarially-Aligned Jacobian Regularization (AAJR), which constrains policy sensitivity specifically along adversarial ascent directions rather than applying global Jacobian bounds, thereby reducing the 'Price of Robustness'.
- **⚠️ Limitations**: The paper focuses on theoretical stability and minimax training for agentic systems, but lacks empirical validation in high-dimensional embodied or robotic control tasks where such regularization might interact unpredictably with complex observation spaces.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04378v1)
- **👥 Authors**: Furkan Mumcu, Yasin Yilmaz
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Tendon Force Modeling for Sim2Real Transfer of Reinforcement Learning Policies for Tendon-Driven Robots (Score: 6/10)
- **💡 Innovation**: The paper introduces a transformer-based, robot-agnostic tendon force estimation model that bridges the sim-to-real gap by incorporating contextual history into a GPU-accelerated rigid body simulation.
- **⚠️ Limitations**: The approach is limited to tendon-driven systems and does not address the broader challenges of high-dimensional state spaces or vision-based control typical of modern foundation model-based robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04351v1)
- **👥 Authors**: Valentin Yuryev, Josie Hughes
- **🏷️ Tags**: #Sim2Real #Reinforcement_Learning #Robot_Manipulation #Embodied_AI

---

### ✨ FocusGraph: Graph-Structured Frame Selection for Embodied Long Video Question Answering (Score: 6/10)
- **💡 Innovation**: The paper introduces a graph-structured frame selection framework that replaces raw visual input with compact textual scene-captions for query-relevant clip retrieval, combined with a training-free patch-wise sparse-flow retention method.
- **⚠️ Limitations**: The reliance on pre-generated scene captions introduces a potential bottleneck where errors in the captioning stage propagate to the selection process, and the method is not evaluated on closed-loop robotic control tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04349v1)
- **👥 Authors**: Tatiana Zemskova, Solomon Andryushenko, Ilya Obrubov, Viktoriia Khoruzhaia, Ekaterina Eroshenko, Ekaterina Derevyanka, Dmitry Yudin
- **🏷️ Tags**: #Embodied_AI #LLM #Foundation_Model

---

### ✨ IPD: Boosting Sequential Policy with Imaginary Planning Distillation in Offline Reinforcement Learning (Score: 6/10)
- **💡 Innovation**: IPD introduces a framework that augments offline datasets by using a world model and MPC to replace suboptimal trajectories with imagined optimal rollouts, which are then distilled into a Transformer-based sequential policy.
- **⚠️ Limitations**: The reliance on a world model for trajectory generation introduces potential compounding errors and model bias, and the method is only evaluated on standard D4RL benchmarks rather than complex, high-dimensional robotic manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04289v1)
- **👥 Authors**: Yihao Qin, Yuanfei Wang, Hang Zhou, Peiran Liu, Hao Dong, Yiding Ji
- **🏷️ Tags**: #World_Model #Reinforcement_Learning #Robot_Manipulation

---

### ✨ Spilled Energy in Large Language Models (Score: 6/10)
- **💡 Innovation**: The paper introduces a training-free hallucination detection method by reinterpreting LLM softmax outputs as an Energy-Based Model to track 'energy spills' across decoding steps.
- **⚠️ Limitations**: The method relies on logit-level analysis which may be less effective for black-box models where logit access is restricted or for models with heavy post-processing/sampling strategies.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.18671)
- **👥 Authors**: Adrian Robert Minut, Hazem Dewidar, Iacopo Masi
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Learning When to Act or Refuse: Guarding Agentic Reasoning Models for Safe Multi-Step Tool Use (Score: 6/10)
- **💡 Innovation**: MOSAIC introduces a post-training framework that formalizes safety as an explicit 'plan, check, act/refuse' reasoning loop, optimized via preference-based reinforcement learning to handle multi-step tool-use risks.
- **⚠️ Limitations**: The evaluation is primarily focused on digital tool-use and text-based agentic tasks, leaving the efficacy of this safety framework in physical, high-stakes embodied robotics environments unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03205)
- **👥 Authors**: Aradhye Agarwal, Gurdit Siyan, Yash Pandya, Joykirat Singh, Akshay Nambi, Ahmed Awadallah
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Dual-Modality Multi-Stage Adversarial Safety Training: Robustifying Multimodal Web Agents Against Cross-Modal Attacks (Score: 5/10)
- **💡 Innovation**: The paper introduces a dual-modality adversarial training framework (DMAST) that treats web agent security as a two-player zero-sum Markov game, utilizing GRPO-based self-play to harden agents against cross-modal DOM-based attacks.
- **⚠️ Limitations**: The research is confined to web-based agents (MiniWob++) and lacks direct application or validation in physical robotic systems, limiting its immediate relevance to embodied manipulation or real-world sensor-fusion safety.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04364v1)
- **👥 Authors**: Haoyu Liu, Dingcheng Li, Lukas Rutishauser, Zeyu Zheng
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### ✨ Dissecting Quantization Error: A Concentration-Alignment Perspective (Score: 5/10)
- **💡 Innovation**: The paper introduces a theoretical framework decomposing quantization error into weight-activation concentration and alignment, proposing a block-wise linear transform (CAT) to optimize both simultaneously.
- **⚠️ Limitations**: The evaluation is restricted to LLMs, leaving the efficacy of this quantization technique on resource-constrained Embodied AI or VLA models—where latency and precision are critical—untested.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04359v1)
- **👥 Authors**: Marco Federici, Boris van Breugel, Paul Whatmough, Markus Nagel
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ Underrepresented in Foundation Model Pretraining Data? A One-Shot Probe (Score: 5/10)
- **💡 Innovation**: The paper introduces a data-efficient probing method that uses LLM-generated counterfactual descriptions to predict the zero-shot accuracy of Vision-Language Foundation Models on underrepresented domains using only one labeled image per class.
- **⚠️ Limitations**: The approach relies heavily on the quality and diversity of the LLM's counterfactual generation, which may fail to capture complex visual nuances or domain-specific features that are not well-represented in the LLM's training data.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04346v1)
- **👥 Authors**: Chris Vorster, Mayug Maniparambil, Noel E. O'Connor, Noel Murphy, Derek Molloy
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ Pointer-CAD: Unifying B-Rep and Command Sequences via Pointer-based Edges & Faces Selection (Score: 5/10)
- **💡 Innovation**: The paper introduces a pointer-based mechanism that allows LLMs to explicitly select geometric entities (edges/faces) within a B-Rep model, bridging the gap between sequential command generation and precise CAD editing.
- **⚠️ Limitations**: The approach remains constrained to synthetic CAD generation and lacks integration with physical robotic systems or real-world sensor-to-CAD feedback loops.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04337v1)
- **👥 Authors**: Dacheng Qi, Chenyu Wang, Jingwei Xu, Tianzhe Chu, Zibo Zhao, Wen Liu, Wenrui Ding, Yi Ma, Shenghua Gao
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Beyond Length Scaling: Synergizing Breadth and Depth for Generative Reward Models (Score: 5/10)
- **💡 Innovation**: The paper introduces a modular synthesis pipeline that decomposes Chain-of-Thought reasoning into Breadth-CoT and Depth-CoT to optimize Generative Reward Models for specific task types.
- **⚠️ Limitations**: The work is strictly focused on text-based reasoning and reward modeling, lacking any integration with embodied agents, visual-action spaces, or physical environment feedback.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01571)
- **👥 Authors**: Qiyuan Zhang, Yufei Wang, Tianhe Wu, Can Xu, Qingfeng Sun, Kai Zheng, Xue Liu, Chen Ma
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Surgical Post-Training: Cutting Errors, Keeping Knowledge (Score: 5/10)
- **💡 Innovation**: The paper introduces a surgical post-training paradigm that uses an Oracle-based data rectification pipeline and a binary cross-entropy reward objective to improve reasoning while mitigating catastrophic forgetting.
- **⚠️ Limitations**: The methodology is evaluated exclusively on mathematical reasoning tasks, leaving its generalizability to embodied domains or multimodal reasoning (like VLA) unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01683)
- **👥 Authors**: Wenye Lin, Kai Han
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ InfoPO: Information-Driven Policy Optimization for User-Centric Agents (Score: 5/10)
- **💡 Innovation**: The paper introduces an information-gain reward mechanism that credits specific interaction turns by measuring the divergence in action distributions against a masked-feedback counterfactual.
- **⚠️ Limitations**: The approach is primarily evaluated on text-based agent tasks and lacks empirical validation in physical robotic environments or high-dimensional sensorimotor control settings.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.00656)
- **👥 Authors**: Fanqi Kong, Jiayi Zhang, Mingyi Deng, Chenglin Wu, Yuyu Luo, Bang Liu
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ CFG-Ctrl: Control-Based Classifier-Free Diffusion Guidance (Score: 5/10)
- **💡 Innovation**: The paper reinterprets Classifier-Free Guidance (CFG) as a control problem and introduces Sliding Mode Control (SMC-CFG) to replace linear proportional control, ensuring finite-time convergence and stability in the generative flow.
- **⚠️ Limitations**: The work is currently focused on static image generation and lacks empirical validation in dynamic, embodied, or closed-loop control settings relevant to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03281)
- **👥 Authors**: Hanyang Wang, Yiyang Liu, Jiawei Chi, Fangfu Liu, Ran Xue, Yueqi Duan
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ LFPO: Likelihood-Free Policy Optimization for Masked Diffusion Models (Score: 5/10)
- **💡 Innovation**: LFPO introduces a likelihood-free policy optimization framework for masked diffusion models by reformulating alignment as geometric velocity rectification in discrete token space.
- **⚠️ Limitations**: The paper focuses exclusively on text-based reasoning and code generation, leaving the efficacy of this optimization method for continuous action spaces in embodied robotics unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01563)
- **👥 Authors**: Chenxing Wei, Jiazhen Kang, Hong Wang, Jianqing Zhang, Hao Jiang, Xiaolong Xu, Ningyuan Sun, Ying He, F. Richard Yu, Yao Shu, Bo Jiang
- **🏷️ Tags**: #Diffusion_Model #Reinforcement_Learning #Foundation_Model #LLM

---

### ✨ Token Reduction via Local and Global Contexts Optimization for Efficient Video Large Language Models (Score: 5/10)
- **💡 Innovation**: The paper introduces a training-free token reduction method for Video LLMs that uses Optimal Transport to aggregate information from pruned tokens into local and global anchors.
- **⚠️ Limitations**: The evaluation is focused on general video understanding benchmarks rather than embodied or robotic control tasks, leaving its efficacy in high-frequency, real-time robot manipulation scenarios unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01400)
- **👥 Authors**: Jinlong Li, Liyuan Jiang, Haonan Zhang, Nicu Sebe
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 TaxonRL: Reinforcement Learning with Intermediate Rewards for Interpretable Fine-Grained Visual Reasoning (Score: 4/10)
- **💡 Innovation**: The paper introduces a hierarchical reinforcement learning framework that enforces taxonomic reasoning (family-genus-species) to improve fine-grained visual classification accuracy and interpretability.
- **⚠️ Limitations**: The approach is strictly focused on visual classification tasks and lacks integration with embodied agents or physical interaction, making it less relevant to robotics and world modeling.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04380v1)
- **👥 Authors**: Maximilian von Klinski, Maximilian Schall
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model

---

### 📄 Efficient Refusal Ablation in LLM through Optimal Transport (Score: 4/10)
- **💡 Innovation**: The paper introduces a framework using Gaussian optimal transport to align harmful activation distributions with harmless ones, moving beyond simple orthogonal projection-based refusal removal.
- **⚠️ Limitations**: The research focuses exclusively on text-based safety alignment and does not address how these distributional interventions translate to multimodal or embodied agents where safety constraints are grounded in physical actions.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04355v1)
- **👥 Authors**: Geraldin Nanfack, Eugene Belilovsky, Elvis Dohmatob
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Out-of-distribution transfer of PDE foundation models to material dynamics under extreme loading (Score: 4/10)
- **💡 Innovation**: The paper benchmarks the out-of-distribution transfer capabilities of existing PDE foundation models on non-smooth, extreme-loading material dynamics tasks like shock-driven interfaces and dynamic fracture.
- **⚠️ Limitations**: The study is limited to terminal-state prediction rather than full trajectory modeling, and it does not propose a new architecture, serving primarily as an empirical evaluation of existing models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04354v1)
- **👥 Authors**: Mahindra Rautela, Alexander Most, Siddharth Mansingh, Aleksandra Pachalieva, Bradley Love, Daniel O Malley, Alexander Scheinker, Kyle Hickmann, Diane Oyen, Nathan Debardeleben, Earl Lawrence, Ayan Biswas
- **🏷️ Tags**: #Foundation_Model #World_Model

---

### 📄 World Properties without World Models: Recovering Spatial and Temporal Structure from Co-occurrence Statistics in Static Word Embeddings (Score: 4/10)
- **💡 Innovation**: The paper demonstrates that spatial and temporal structures, often attributed to complex internal world models in LLMs, are actually recoverable from simple static co-occurrence statistics in word embeddings.
- **⚠️ Limitations**: The study focuses exclusively on static linguistic correlations and does not address the dynamic, multi-modal, or causal reasoning capabilities required for embodied agents to interact with a physical environment.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04317v1)
- **👥 Authors**: Elan Barenholtz
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 CubeComposer: Spatio-Temporal Autoregressive 4K 360° Video Generation from Perspective Video (Score: 4/10)
- **💡 Innovation**: The paper introduces a spatio-temporal autoregressive diffusion framework that decomposes 360° video into cubemap faces to enable native 4K resolution generation while maintaining temporal and spatial coherence.
- **⚠️ Limitations**: The approach is primarily focused on video synthesis for VR/immersive media and lacks explicit integration with embodied agents, physical dynamics, or interactive control loops required for robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04291v1)
- **👥 Authors**: Lingen Li, Guangzhi Wang, Xiaoyu Li, Zhaoyang Zhang, Qi Dou, Jinwei Gu, Tianfan Xue, Ying Shan
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 Qwen3-Coder-Next Technical Report (Score: 4/10)
- **💡 Innovation**: The paper introduces a sparse-activation architecture (3B active out of 80B) optimized for agentic coding tasks through large-scale synthesis of verifiable environment feedback.
- **⚠️ Limitations**: The work is strictly focused on software-based coding agents and lacks any integration with physical sensors, actuators, or embodied environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.00729)
- **👥 Authors**: Ruisheng Cao, Mouxiang Chen, Jiawei Chen, Zeyu Cui, Yunlong Feng, Binyuan Hui, Yuheng Jing, Kaixin Li, Mingze Li, Junyang Lin, Zeyao Ma, Kashun Shum, Xuwu Wang, Jinxi Wei, Jiaxi Yang, Jiajun Zhang, Lei Zhang, Zongmeng Zhang, Wenting Zhao, Fan Zhou
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 How Controllable Are Large Language Models? A Unified Evaluation across Behavioral Granularities (Score: 4/10)
- **💡 Innovation**: The paper introduces SteerEval, a hierarchical benchmark that decomposes LLM controllability into three distinct granularities (intent, style, and instantiation) to measure performance degradation across levels.
- **⚠️ Limitations**: The work is strictly limited to textual output and does not address the challenges of controllability in multimodal or embodied action spaces, which are critical for robotics applications.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.02578)
- **👥 Authors**: Ziwen Xu, Kewei Xu, Haoming Xu, Haiwen Hong, Longtao Huang, Hui Xue, Ningyu Zhang, Yongliang Shen, Guozhou Zheng, Huajun Chen, Shumin Deng
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Code2Math: Can Your Code Agent Effectively Evolve Math Problems Through Exploration? (Score: 4/10)
- **💡 Innovation**: The paper introduces a multi-agent framework that leverages code execution as a sandbox to autonomously evolve and validate the difficulty of mathematical problems.
- **⚠️ Limitations**: The work is strictly confined to symbolic mathematical reasoning and lacks any connection to physical environments, sensorimotor control, or embodied agents.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03202)
- **👥 Authors**: Dadi Guo, Yuejin Xie, Qingyu Liu, Jiayu Liu, Zhiyuan Fan, Qihan Ren, Shuai Shao, Tianyi Zhou, Dongrui Liu, Yi R. Fung
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Humans and LLMs Diverge on Probabilistic Inferences (Score: 4/10)
- **💡 Innovation**: The paper introduces ProbCOPA, a novel dataset designed to benchmark how LLMs handle open-ended, non-deterministic probabilistic inferences compared to human judgment.
- **⚠️ Limitations**: The study focuses exclusively on linguistic reasoning tasks and lacks any connection to physical grounding, sensorimotor data, or embodied decision-making contexts.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.23546)
- **👥 Authors**: Gaurav Kamath, Sreenath Madathil, Sebastian Schuster, Marie-Catherine de Marneffe, Siva Reddy
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 AgentConductor: Topology Evolution for Multi-Agent Competition-Level Code Generation (Score: 4/10)
- **💡 Innovation**: The paper introduces a reinforcement learning-optimized orchestrator that dynamically adjusts multi-agent interaction topologies (DAGs) based on task difficulty and execution feedback to optimize communication density.
- **⚠️ Limitations**: The work is strictly confined to the domain of code generation and lacks any connection to physical agents, embodied perception, or real-world environment interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.17100)
- **👥 Authors**: Siyu Wang, Ruotian Lu, Zhihao Yang, Yuchao Wang, Yanzhou Zhang, Lei Xu, Qimin Xu, Guojun Yin, Cailian Chen, Xinping Guan
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Words & Weights: Streamlining Multi-Turn Interactions via Co-Adaptation (Score: 4/10)
- **💡 Innovation**: The paper introduces a co-adaptation framework (ROSA2) that treats test-time adaptation as a joint optimization problem over both textual prompts and model weights to resolve ambiguity and capability gaps simultaneously.
- **⚠️ Limitations**: The work focuses exclusively on reasoning tasks (MATH benchmark) and lacks evaluation in embodied environments or physical control tasks, making its direct applicability to robotics uncertain.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01375)
- **👥 Authors**: Chenxing Wei, Hong Wang, Ying He, Zhongxiang Dai, Bo Jiang, F. Richard Yu, Yao Shu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Multi-Domain Riemannian Graph Gluing for Building Graph Foundation Models (Score: 4/10)
- **💡 Innovation**: The paper introduces a theoretical framework for multi-domain graph pre-training by modeling graph datasets as local pieces of a Riemannian manifold and 'gluing' them together using adaptive orthogonal frames.
- **⚠️ Limitations**: The work focuses exclusively on abstract graph-structured data and lacks any empirical validation or connection to embodied agents, physical dynamics, or vision-language-action tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.00618)
- **👥 Authors**: Li Sun, Zhenhao Huang, Silei Chen, Lanxu Yang, Junda Ye, Sen Su, Philip S. Yu
- **🏷️ Tags**: #Foundation_Model

---

### 📄 A Dual-Helix Governance Approach Towards Reliable Agentic AI for WebGIS Development (Score: 3/10)
- **💡 Innovation**: The paper introduces a 'dual-helix' governance framework that uses a knowledge graph substrate to externalize domain facts and enforce execution protocols for LLM-based software engineering agents.
- **⚠️ Limitations**: The research is strictly focused on software engineering and code refactoring within a WebGIS context, lacking any connection to physical embodiment, sensorimotor control, or the robotics-specific challenges of world modeling and manipulation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04390v1)
- **👥 Authors**: Boyuan, Guan, Wencong Cui, Levente Juhasz
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Dual Diffusion Models for Multi-modal Guided 3D Avatar Generation (Score: 3/10)
- **💡 Innovation**: The paper introduces a dual-diffusion framework that maps multi-modal prompts directly to 3D avatar representations, bypassing iterative optimization like SDS.
- **⚠️ Limitations**: The work focuses exclusively on static 3D avatar generation and lacks integration with embodied agents, dynamic motion, or physical interaction capabilities.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04307v1)
- **👥 Authors**: Hong Li, Yutang Feng, Minqi Meng, Yichen Yang, Xuhui Liu, Baochang Zhang
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 LUMINA: Foundation Models for Topology Transferable ACOPF (Score: 3/10)
- **💡 Innovation**: The paper introduces design principles for foundation models specifically tailored to satisfy hard physical constraints in AC optimal power flow (ACOPF) optimization problems.
- **⚠️ Limitations**: The work is focused on power grid optimization and lacks any connection to embodied agents, physical robot interaction, or the sensory-motor loops required for robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04300v1)
- **👥 Authors**: Yijiang Li, Zeeshan Memon, Hongwei Jin, Stefano Fenu, Keunju Song, Sunash B Sharma, Parfait Gasana, Hongseok Kim, Liang Zhao, Kibaek Kim
- **🏷️ Tags**: #Foundation_Model

---

### 📄 ParEVO: Synthesizing Code for Irregular Data: High-Performance Parallelism through Agentic Evolution (Score: 3/10)
- **💡 Innovation**: The paper introduces an evolutionary agentic framework that combines a specialized instruction-tuning dataset with iterative compiler-feedback loops to synthesize high-performance parallel code for irregular data structures.
- **⚠️ Limitations**: The work is strictly focused on high-performance computing and software engineering for parallel algorithms, lacking any connection to physical robot control, sensorimotor learning, or embodied decision-making.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.02510)
- **👥 Authors**: Liu Yang, Zeyu Nie, Andrew Liu, Felix Zou, Deniz Altinbüken, Amir Yazdanbakhsh, Quanquan C. Liu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 APRES: An Agentic Paper Revision and Evaluation System (Score: 3/10)
- **💡 Innovation**: The paper introduces an automated framework that uses LLMs to refine scientific manuscripts based on a learned rubric optimized for predicting future citation counts.
- **⚠️ Limitations**: The methodology focuses exclusively on textual refinement and citation metrics, lacking any connection to the technical domains of robotics, embodied agents, or physical world modeling.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03142)
- **👥 Authors**: Bingchen Zhao, Jenny Zhang, Chenxi Whitehouse, Minqi Jiang, Michael Shvartsman, Abhishek Charnalia, Despoina Magka, Tatiana Shavrina, Derek Dunfield, Oisin Mac Aodha, Yoram Bachrach
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Towards Simulating Social Media Users with LLMs: Evaluating the Operational Validity of Conditioned Comment Prediction (Score: 3/10)
- **💡 Innovation**: The paper introduces Conditioned Comment Prediction (CCP) as a framework to evaluate the operational validity of LLMs in simulating human social media behavior through behavioral traces.
- **⚠️ Limitations**: The study focuses exclusively on text-based social simulation and lacks any connection to physical embodiment, sensorimotor grounding, or real-world robotic interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.22752)
- **👥 Authors**: Nils Schwager, Simon Münker, Alistair Plum, Achim Rettinger
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Low-Resource Guidance for Controllable Latent Audio Diffusion (Score: 2/10)
- **💡 Innovation**: The paper introduces Latent-Control Heads (LatCHs) to perform guidance directly in the latent space of audio diffusion models, bypassing the computationally expensive decoder backpropagation step.
- **⚠️ Limitations**: The work is exclusively focused on audio generation and lacks any application, evaluation, or relevance to embodied agents, robot manipulation, or multimodal action-conditioned generation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04366v1)
- **👥 Authors**: Zachary Novack, Zack Zukowski, CJ Carr, Julian Parker, Zach Evans, Josiah Taylor, Taylor Berg-Kirkpatrick, Julian McAuley, Jordi Pons
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 A Constrained RL Approach for Cost-Efficient Delivery of Latency-Sensitive Applications (Score: 2/10)
- **💡 Innovation**: The paper applies constrained deep reinforcement learning (CDRL) to optimize resource allocation in network packet delivery under strict per-packet delay constraints.
- **⚠️ Limitations**: The work is entirely focused on network routing and scheduling, lacking any connection to physical embodiment, vision-language models, or robotic control tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04353v1)
- **👥 Authors**: Ozan Aygün, Vincenzo Norman Vitale, Antonia M. Tulino, Hao Feng, Elza Erkip, Jaime Llorca
- **🏷️ Tags**: #Reinforcement_Learning

---

### 📄 Balancing Fidelity, Utility, and Privacy in Synthetic Cardiac MRI Generation: A Comparative Study (Score: 2/10)
- **💡 Innovation**: The study provides a systematic comparative benchmark of generative architectures (DDPM, LDM, FM) specifically for synthetic cardiac MRI data augmentation under privacy constraints.
- **⚠️ Limitations**: The paper focuses exclusively on medical imaging and lacks any connection to embodied agents, robot control, or physical world interaction, making it largely irrelevant to the specified research interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04340v1)
- **👥 Authors**: Madhura Edirisooriya, Dasuni Kawya, Ishan Kumarasinghe, Isuri Devindi, Mary M. Maleckar, Roshan Ragel, Isuru Nawinne, Vajira Thambawita
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 SpotIt+: Verification-based Text-to-SQL Evaluation with Database Constraints (Score: 2/10)
- **💡 Innovation**: The paper introduces a constraint-mining pipeline that combines rule-based specification mining with LLM-based validation to generate realistic database counterexamples for SQL verification.
- **⚠️ Limitations**: The work is strictly focused on database query verification and lacks any connection to physical agents, sensorimotor control, or embodied decision-making processes.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.04334v1)
- **👥 Authors**: Rocky Klopfenstein, Yang He, Andrew Tremante, Yuepeng Wang, Nina Narodytska, Haoze Wu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 QEDBENCH: Quantifying the Alignment Gap in Automated Evaluation of University-Level Mathematical Proofs (Score: 2/10)
- **💡 Innovation**: The paper introduces a dual-rubric alignment benchmark (QEDBench) to quantify the 'alignment gap' and score inflation in LLM-based evaluation of university-level mathematical proofs.
- **⚠️ Limitations**: The paper is entirely focused on symbolic reasoning and mathematical evaluation, offering no contribution to embodied perception, motor control, or physical world modeling.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.20629)
- **👥 Authors**: Santiago Gonzalez, Alireza Amiri Bavandpour, Peter Ye, Edward Zhang, Ruslans Aleksejevs, Todor Antić, Polina Baron, Sujeet Bhalerao, Shubhrajit Bhattacharya, Zachary Burton, John Byrne, Hyungjun Choi, Nujhat Ahmed Disha, Koppany István Encz, Yuchen Fang, Robert Joseph George, Ebrahim Ghorbani, Alan Goldfarb, Jing Guo, Meghal Gupta, Stefano Huber, Annika Kanckos, Minjung Kang, Hyun Jong Kim, Dino Lorenzini, Levi Lorenzo, Tianyi Mao, Giovanni Marzenta, Ariane M. Masuda, Lukas Mauth, Ana Mickovic, Andres Miniguano-Trujillo, Antoine Moulin, Wenqi Ni, Tomos Parry, Kevin Ren, Hossein Roodbarani, Mathieu Rundström, Manjil Saikia, Detchat Samart, Rebecca Steiner, Connor Stewart, Dhara Thakkar, Jeffrey Tse, Vasiliki Velona, Yunhai Xiang, Sibel Yalçın, Jun Yan, Ji Zeng, Arman Cohan, Quanquan C. Liu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 GroupGPT: A Token-efficient and Privacy-preserving Agentic Framework for Multi-User Chat Assistant (Score: 2/10)
- **💡 Innovation**: The paper introduces a collaborative small-large model architecture to decouple intervention timing from response generation in multi-user chat environments to optimize token efficiency.
- **⚠️ Limitations**: The work is entirely focused on conversational agent orchestration and lacks any connection to physical embodiment, sensorimotor control, or robotic task execution.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01059)
- **👥 Authors**: Zhuokang Shen, Yifan Wang, Hanyu Chen, Wenxuan Huang, Shaohui Lin
- **🏷️ Tags**: #LLM #Foundation_Model

---


