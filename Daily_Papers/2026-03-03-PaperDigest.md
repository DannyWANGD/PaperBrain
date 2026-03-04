# 📅 2026-03-03 - Paper Digest
## Summary
Total Papers: 41 | High Impact: 10

## 📝 Papers List
### 🔥 ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation (Score: 8/10)
- **💡 Innovation**: ULTRA introduces a physics-driven neural retargeting algorithm combined with a unified multimodal controller that enables whole-body loco-manipulation by distilling universal tracking policies into a latent motor skill space.
- **⚠️ Limitations**: The reliance on a distillation process from motion-capture-based tracking policies may still inherit the limitations of the source motion data, potentially restricting the emergence of truly novel, non-human-like behaviors.
- **🔗 Link**: [[ULTRA]]
- **👥 Authors**: Xialin He, Sirui Xu, Xinyao Li, Runpei Dong, Liuyu Bian, Yu-Xiong Wang, Liang-Yan Gui
- **🏷️ Tags**: #Embodied_AI #Sim2Real #Reinforcement_Learning #Robot_Manipulation

---

### 🔥 Beyond Language Modeling: An Exploration of Multimodal Pretraining (Score: 8/10)
- **💡 Innovation**: The paper introduces a unified Transfusion-based architecture that treats vision as a generative task via diffusion and language as a next-token prediction task, demonstrating that world modeling emerges naturally from this multimodal pretraining.
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
- **🏷️ Tags**: #World_Model #VLA #Embodied_AI #Robot_Manipulation #Foundation_Model

---

### 🔥 Planning from Observation and Interaction (Score: 8/10)
- **💡 Innovation**: The paper introduces a planning-based Inverse Reinforcement Learning (IRL) framework that enables robots to learn complex manipulation tasks from raw observations without requiring demonstrator actions, pre-training, or hand-designed rewards.
- **⚠️ Limitations**: The reliance on planning-based IRL may struggle with high-dimensional state spaces or long-horizon tasks compared to end-to-end Foundation Models or VLA approaches.
- **🔗 Link**: [[Planning from Observation and Interaction]]
- **👥 Authors**: Tyler Han, Siyang Shen, Rohan Baijal, Harine Ravichandiran, Bat Nemekhbold, Kevin Huang, Sanghun Jung, Byron Boots
- **🏷️ Tags**: #World_Model #Embodied_AI #Reinforcement_Learning #Robot_Manipulation

---

### ✨ Utonia: Toward One Encoder for All Point Clouds (Score: 7/10)
- **💡 Innovation**: Utonia introduces a unified self-supervised point transformer encoder trained across highly heterogeneous 3D domains to learn a consistent representation space that generalizes to downstream embodied and multimodal tasks.
- **⚠️ Limitations**: The paper lacks a detailed analysis of the computational overhead and latency trade-offs when deploying this unified encoder in real-time robotic control loops compared to domain-specific encoders.
- **🔗 Link**: [[Utonia]]
- **👥 Authors**: Yujia Zhang, Xiaoyang Wu, Yunhan Yang, Xianzhe Fan, Han Li, Yuechen Zhang, Zehao Huang, Naiyan Wang, Hengshuang Zhao
- **🏷️ Tags**: #Embodied_AI #Robot_Manipulation #VLA #Foundation_Model

---

### ✨ LoGeR: Long-Context Geometric Reconstruction with Hybrid Memory (Score: 7/10)
- **💡 Innovation**: LoGeR introduces a hybrid memory architecture that combines parametric Test-Time Training (TTT) for global coordinate anchoring with non-parametric Sliding Window Attention (SWA) to enable long-horizon 3D reconstruction without quadratic complexity.
- **⚠️ Limitations**: The paper focuses on geometric reconstruction rather than semantic understanding or closed-loop control, leaving the integration of this long-context spatial memory into downstream embodied decision-making tasks unexplored.
- **🔗 Link**: [[LoGeR]]
- **👥 Authors**: Junyi Zhang, Charles Herrmann, Junhwa Hur, Chen Sun, Ming-Hsuan Yang, Forrester Cole, Trevor Darrell, Deqing Sun
- **🏷️ Tags**: #World_Model #Embodied_AI #Foundation_Model

---

### ✨ ACE-Brain-0: Spatial Intelligence as a Shared Scaffold for Universal Embodiments (Score: 7/10)
- **💡 Innovation**: The paper introduces the Scaffold-Specialize-Reconcile (SSR) paradigm, which uses spatial intelligence as a domain-agnostic foundation to unify heterogeneous embodiments through data-free model merging.
- **⚠️ Limitations**: The reliance on data-free model merging may struggle to capture complex, non-linear interactions between specialized domains compared to joint end-to-end training.
- **🔗 Link**: [[ACEBrain0]]
- **👥 Authors**: Ziyang Gong, Zehang Luo, Anke Tang, Zhe Liu, Shi Fu, Zhi Hou, Ganlin Yang, Weiyun Wang, Xiaofeng Wang, Jianbo Liu, Gen Luo, Haolan Kang, Shuang Luo, Yue Zhou, Yong Luo, Li Shen, Xiaosong Jia, Yao Mu, Xue Yang, Chunxiao Liu, Junchi Yan, Hengshuang Zhao, Dacheng Tao, Xiaogang Wang
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #LLM #Robot_Manipulation #Reinforcement_Learning

---

### ✨ WorldStereo: Bridging Camera-Guided Video Generation and Scene Reconstruction via 3D Geometric Memories (Score: 7/10)
- **💡 Innovation**: The paper introduces a dual-memory architecture (global-geometric and spatial-stereo) that enforces 3D structural consistency in video diffusion models by constraining attention receptive fields with 3D point cloud priors.
- **⚠️ Limitations**: The reliance on distilled VDM backbones and point cloud updates may struggle with highly dynamic, non-rigid scene elements or long-horizon temporal consistency compared to end-to-end learned world models.
- **🔗 Link**: [[WorldStereo]]
- **👥 Authors**: Yisu Zhang, Chenjie Cao, Tengfei Wang, Xuhui Zuo, Junta Wu, Jianke Zhu, Chunchao Guo
- **🏷️ Tags**: #World_Model #Diffusion_Model #Foundation_Model

---

### ✨ Tool-R0: Self-Evolving LLM Agents for Tool-Learning from Zero Data (Score: 7/10)
- **💡 Innovation**: The paper introduces a self-evolving framework that uses a Generator-Solver co-evolutionary loop to train tool-calling agents via self-play RL without requiring any pre-existing task datasets.
- **⚠️ Limitations**: The reliance on a 'real-world tool call' environment for self-play may be computationally expensive or unsafe to scale without a robust, high-fidelity simulation sandbox.
- **🔗 Link**: [[ToolR0]]
- **👥 Authors**: Emre Can Acikgoz, Cheng Qian, Jonas Hübotter, Heng Ji, Dilek Hakkani-Tür, Gokhan Tur
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ ArtLLM: Generating Articulated Assets via 3D LLM (Score: 7/10)
- **💡 Innovation**: ArtLLM introduces a 3D multimodal LLM that autoregressively predicts kinematic structures and part layouts directly from point clouds to condition 3D generative models for articulated asset synthesis.
- **⚠️ Limitations**: The reliance on a pre-curated dataset for training may limit the model's ability to generalize to highly novel or complex non-standard articulation mechanisms not represented in the training distribution.
- **🔗 Link**: [[ArtLLM]]
- **👥 Authors**: Penghao Wang, Siyuan Xie, Hongyu Yan, Xianghui Yang, Jingwei Huang, Chunchao Guo, Jiayuan Gu
- **🏷️ Tags**: #LLM #Foundation_Model #Embodied_AI #Sim2Real #Diffusion_Model

---

### ✨ Efficient RLVR Training via Weighted Mutual Information Data Selection (Score: 6/10)
- **💡 Innovation**: The paper introduces a data selection framework for RLVR that replaces heuristic difficulty-based sampling with a weighted mutual information objective derived from Bayesian latent success rates to account for both difficulty and epistemic uncertainty.
- **⚠️ Limitations**: The evaluation is focused primarily on reasoning and mathematical benchmarks rather than embodied or robotic control tasks, leaving the efficacy of this selection strategy in high-dimensional continuous action spaces unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01907)
- **👥 Authors**: Xinyu Zhou, Boyu Zhu, Haotian Zhang, Huiming Wang, Zhijiang Guo
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Agentic Code Reasoning (Score: 6/10)
- **💡 Innovation**: The paper introduces 'semi-formal reasoning,' a structured prompting framework that forces LLMs to generate explicit premises and execution traces as a verifiable certificate for code analysis without execution.
- **⚠️ Limitations**: The approach relies on the LLM's inherent reasoning capabilities and may struggle with highly complex, non-linear, or state-dependent codebases where static analysis is fundamentally limited compared to dynamic execution.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01896)
- **👥 Authors**: Shubham Ugare, Satish Chandra
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Reasoning Core: A Scalable Procedural Data Generation Suite for Symbolic Pre-training and Post-Training (Score: 6/10)
- **💡 Innovation**: The paper introduces a scalable, procedural generation framework that provides verifiable symbolic reasoning data and solver-derived traces to enhance the reasoning capabilities of foundation models.
- **⚠️ Limitations**: The work focuses primarily on abstract symbolic reasoning and lacks a direct bridge to the physical grounding or multi-modal sensory inputs required for embodied robotics applications.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.02208)
- **👥 Authors**: Valentin Lacombe, Valentin Quesnel, Damien Sileo
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ MIBURI: Towards Expressive Interactive Gesture Synthesis (Score: 5/10)
- **💡 Innovation**: The paper introduces a two-dimensional causal framework that autoregressively generates hierarchical, body-part aware motion tokens synchronized with real-time speech-text embeddings from an LLM.
- **⚠️ Limitations**: The framework lacks physical grounding or interaction with the environment, focusing solely on expressive synthesis rather than the functional robot manipulation or embodied control tasks relevant to robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.03282v1)
- **👥 Authors**: M. Hamza Mughal, Rishabh Dabral, Vera Demberg, Christian Theobalt
- **🏷️ Tags**: #LLM #Embodied_AI #Foundation_Model

---

### ✨ CFG-Ctrl: Control-Based Classifier-Free Diffusion Guidance (Score: 5/10)
- **💡 Innovation**: The paper reinterprets Classifier-Free Guidance (CFG) as a control problem and introduces Sliding Mode Control (SMC-CFG) to replace linear proportional control, ensuring finite-time convergence and stability in generative flows.
- **⚠️ Limitations**: The work is strictly focused on image generation benchmarks and lacks evaluation on embodied tasks or sequential decision-making processes where such control-theoretic improvements might be most impactful.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.03281v1)
- **👥 Authors**: Hanyang Wang, Yiyang Liu, Jiawei Chi, Fangfu Liu, Ran Xue, Yueqi Duan
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ DuoMo: Dual Motion Diffusion for World-Space Human Reconstruction (Score: 5/10)
- **💡 Innovation**: The paper introduces a dual-stage diffusion framework that factorizes human motion reconstruction into camera-space estimation and world-space refinement to ensure global consistency.
- **⚠️ Limitations**: The method focuses exclusively on human motion reconstruction rather than agent-environment interaction, limiting its direct applicability to embodied robot control or manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.03265v1)
- **👥 Authors**: Yufu Wang, Evonne Ng, Soyong Shin, Rawal Khirodkar, Yuan Dong, Zhaoen Su, Jinhyung Park, Kris Kitani, Alexander Richard, Fabian Prada, Michael Zollhofer
- **🏷️ Tags**: #Diffusion_Model

---

### ✨ Specificity-aware reinforcement learning for fine-grained open-world classification (Score: 5/10)
- **💡 Innovation**: The paper introduces a reinforcement learning framework (SpeciaRL) that uses a dynamic, verifier-based reward signal to steer Large Multimodal Models toward more specific, fine-grained classifications without sacrificing accuracy.
- **⚠️ Limitations**: The approach is limited to static image classification tasks and does not address the temporal or physical reasoning requirements necessary for embodied agents or robot manipulation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.03197v1)
- **👥 Authors**: Samuele Angheben, Davide Berasi, Alessandro Conti, Elisa Ricci, Yiming Wang
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ MoD-DPO: Towards Mitigating Cross-modal Hallucinations in Omni LLMs using Modality Decoupled Preference Optimization (Score: 5/10)
- **💡 Innovation**: The paper introduces Modality-Decoupled Direct Preference Optimization (MoD-DPO), which uses modality-aware regularization and language-prior debiasing to reduce cross-modal hallucinations in omni-modal LLMs.
- **⚠️ Limitations**: The research focuses exclusively on audiovisual understanding benchmarks rather than embodied or action-oriented tasks, limiting its direct applicability to robotics or VLA-based control.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.03192v1)
- **👥 Authors**: Ashutosh Chaubey, Jiacheng Pang, Mohammad Soleymani
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ A Covering Framework for Offline POMDPs Learning using Belief Space Metric (Score: 5/10)
- **💡 Innovation**: The paper introduces a covering analysis framework for offline POMDPs that replaces raw history coverage requirements with Lipschitz continuity constraints in the belief space.
- **⚠️ Limitations**: The theoretical framework relies on the assumption of Lipschitz continuity in belief space, which may be difficult to verify or satisfy in high-dimensional, complex robotic environments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.03191v1)
- **👥 Authors**: Youheng Zhu, Yiping Lu
- **🏷️ Tags**: #Reinforcement_Learning

---

### ✨ MMR-Life: Piecing Together Real-life Scenes for Multimodal Multi-image Reasoning (Score: 5/10)
- **💡 Innovation**: The paper introduces a comprehensive benchmark, MMR-Life, specifically designed to evaluate multimodal multi-image reasoning across seven distinct logical reasoning types in real-world contexts.
- **⚠️ Limitations**: The work is purely evaluative and lacks a proposed architectural improvement or a novel training methodology for the models being tested.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.02024)
- **👥 Authors**: Jiachun Li, Shaoping Huang, Zhuoran Jin, Chenlong Zhang, Pengfei Cao, Yubo Chen, Kang Liu, Jun Zhao
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ CHIMERA: Compact Synthetic Data for Generalizable LLM Reasoning (Score: 5/10)
- **💡 Innovation**: The paper introduces a compact, high-quality synthetic dataset (CHIMERA) constructed via a hierarchical taxonomy and automated cross-validation to improve reasoning in smaller LLMs.
- **⚠️ Limitations**: The work focuses exclusively on textual reasoning benchmarks and lacks application or evaluation in embodied settings, such as robot planning or multi-modal reasoning.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.00889)
- **👥 Authors**: Xinyu Zhu, Yihao Feng, Yanchao Sun, Xianzhi Du, Pingzhi Li, Olli Saarikivi, Yun Zhu, Yu Meng
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ CoVe: Training Interactive Tool-Use Agents via Constraint-Guided Verification (Score: 5/10)
- **💡 Innovation**: The paper introduces a constraint-guided data synthesis framework that uses explicit task constraints to simultaneously generate complex training trajectories and provide deterministic verification for reward signal derivation.
- **⚠️ Limitations**: The approach is primarily focused on digital tool-use (API/agentic tasks) rather than physical embodiment, limiting its direct applicability to real-world robotic manipulation or sensorimotor control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01940)
- **👥 Authors**: Jinpeng Chen, Cheng Gong, Hanbo Li, Ziru Liu, Zichen Tian, Xinyu Fu, Shi Wu, Chenyang Zhang, Wu Zhang, Suiyun Zhang, Dandan Tu, Rui Liu
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Spectral Condition for μP under Width-Depth Scaling (Score: 5/10)
- **💡 Innovation**: The paper introduces a unified spectral condition for maximal update parameterization (μP) that generalizes weight and update scaling rules to joint width-depth scaling regimes.
- **⚠️ Limitations**: The evaluation is restricted to GPT-2 style language models, leaving the effectiveness of this scaling theory for vision-heavy architectures or multimodal foundation models (like VLAs) unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.00541)
- **👥 Authors**: Chenyu Zheng, Rongzhen Wang, Xinyu Zhang, Chongxuan Li
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ Learn Hard Problems During RL with Reference Guided Fine-tuning (Score: 5/10)
- **💡 Innovation**: The paper introduces Reference-Guided Fine-Tuning (ReGFT), which bridges the gap between human-written reference solutions and model-generated reasoning traces by using partial references to guide the model's own generation process.
- **⚠️ Limitations**: The method is highly specific to mathematical reasoning tasks and does not address the broader challenges of reward sparsity in non-textual domains like robotics or physical interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01223)
- **👥 Authors**: Yangzhen Wu, Shanda Li, Zixin Wen, Xin Zhou, Ameet Talwalkar, Yiming Yang, Wenhao Huang, Tianle Cai
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Tool Verification for Test-Time Reinforcement Learning (Score: 5/10)
- **💡 Innovation**: The paper introduces a verification-aware voting mechanism that uses external tool execution to filter and weight pseudo-labels during test-time reinforcement learning, mitigating mode collapse caused by unverified consensus.
- **⚠️ Limitations**: The approach is strictly limited to domains where problems can be programmatically verified (e.g., math/code), making it difficult to generalize to open-ended embodied tasks where ground-truth verification is often unavailable.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.02203)
- **👥 Authors**: Ruotong Liao, Nikolai Röhrich, Xiaohan Wang, Yuhui Zhang, Yasaman Samadzadeh, Volker Tresp, Serena Yeung-Levy
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Recursive Think-Answer Process for LLMs and VLMs (Score: 5/10)
- **💡 Innovation**: The paper introduces a recursive inference framework (R-TAP) that utilizes a confidence generator and dual-reward mechanism to iteratively refine reasoning outputs in LLMs and VLMs.
- **⚠️ Limitations**: The approach relies on additional inference-time compute cycles, which may introduce significant latency overhead that is not fully evaluated in real-time or resource-constrained environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.02099)
- **👥 Authors**: Byung-Kwan Lee, Youngchae Chee, Yong Man Ro
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ RAISE: Requirement-Adaptive Evolutionary Refinement for Training-Free Text-to-Image Alignment (Score: 5/10)
- **💡 Innovation**: RAISE introduces a requirement-driven evolutionary framework that dynamically allocates computational resources for T2I generation by verifying images against a structured checklist of prompt requirements.
- **⚠️ Limitations**: The method is strictly focused on static image generation and lacks integration with temporal consistency or physical grounding, making it currently inapplicable to embodied robotics or dynamic world modeling.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.00483)
- **👥 Authors**: Liyao Jiang, Ruichen Chen, Chao Gao, Di Niu
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #LLM

---

### 📄 From Scale to Speed: Adaptive Test-Time Scaling for Image Editing (Score: 4/10)
- **💡 Innovation**: The paper introduces an adaptive test-time scaling framework (ADE-CoT) for image editing that dynamically allocates sampling budgets and employs edit-specific verification to improve efficiency.
- **⚠️ Limitations**: The work is strictly focused on 2D image editing and lacks any connection to spatial reasoning, temporal consistency, or physical grounding required for embodied robotics applications.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.00141)
- **👥 Authors**: Xiangyan Qu, Zhenlong Yuan, Jing Tang, Rui Chen, Datao Tang, Meng Yu, Lei Sun, Yancheng Bai, Xiangxiang Chu, Gaopeng Gou, Gang Xiong, Yujun Cai
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #LLM

---

### 📄 SWE-rebench V2: Language-Agnostic SWE Task Collection at Scale (Score: 4/10)
- **💡 Innovation**: The paper introduces a language-agnostic automated pipeline that leverages LLM-based agents to synthesize installation and testing procedures for software engineering tasks at scale.
- **⚠️ Limitations**: The work focuses exclusively on software engineering agents and lacks any connection to physical embodiment, sensorimotor control, or real-world robotic interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.23866)
- **👥 Authors**: Ibragim Badertdinov, Maksim Nekrashevich, Anton Shevtsov, Alexander Golubev
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 RubricBench: Aligning Model-Generated Rubrics with Human Standards (Score: 4/10)
- **💡 Innovation**: The paper introduces a benchmark specifically designed to evaluate the reliability of rubric-based LLM evaluation by comparing model-generated rubrics against expert-annotated ground truths.
- **⚠️ Limitations**: The work focuses exclusively on text-based LLM alignment and lacks any connection to embodied agents, multi-modal action spaces, or physical environment feedback.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01562)
- **👥 Authors**: Qiyuan Zhang, Junyi Zhou, Yufei Wang, Fuyuan Lyu, Yidong Ming, Can Xu, Qingfeng Sun, Kai Zheng, Peng Kang, Xue Liu, Chen Ma
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 LLaDA-o: An Effective and Length-Adaptive Omni Diffusion Model (Score: 4/10)
- **💡 Innovation**: The paper introduces a Mixture of Diffusion (MoD) framework that decouples discrete masked diffusion for text and continuous diffusion for visual generation within a shared attention backbone, combined with a length-adaptive decoding strategy.
- **⚠️ Limitations**: The paper focuses exclusively on multimodal understanding and generation benchmarks (text-to-image/text-to-text) without demonstrating any application to embodied agents, robot control, or action prediction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01068)
- **👥 Authors**: Zebin You, Xiaolu Zhang, Jun Zhou, Chongxuan Li, Ji-Rong Wen
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #LLM

---

### 📄 When Does RL Help Medical VLMs? Disentangling Vision, SFT, and RL Gains (Score: 4/10)
- **💡 Innovation**: The paper provides a systematic, controlled study disentangling the performance gains of RL versus SFT in medical VLMs, identifying that RL primarily sharpens existing output distributions rather than expanding reasoning capabilities.
- **⚠️ Limitations**: The study is restricted to the medical VQA domain and MedMNIST, making the findings potentially less generalizable to the high-dimensional, continuous action spaces typical of Embodied AI and robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01301)
- **👥 Authors**: Ahmadreza Jeddi, Kimia Shaban, Negin Baghbanzadeh, Natasha Sharan, Abhishek Moturu, Elham Dolatabadi, Babak Taati
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### 📄 LaSER: Internalizing Explicit Reasoning into Latent Space for Dense Retrieval (Score: 4/10)
- **💡 Innovation**: LaSER introduces a self-distillation framework that aligns latent states of a dense retriever with explicit Chain-of-Thought reasoning paths to enable 'silent' reasoning without autoregressive generation.
- **⚠️ Limitations**: The paper focuses exclusively on information retrieval tasks and lacks any application or evaluation within embodied, physical, or multi-modal robotic environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01425)
- **👥 Authors**: Jiajie Jin, Yanzhao Zhang, Mingxin Li, Dingkun Long, Pengjun Xie, Yutao Zhu, Zhicheng Dou
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 FireRed-OCR Technical Report (Score: 4/10)
- **💡 Innovation**: The paper introduces a specialized training pipeline for VLMs that combines geometric feature clustering for data synthesis with format-constrained Group Relative Policy Optimization (GRPO) to ensure structural integrity in document parsing.
- **⚠️ Limitations**: The work is strictly focused on document OCR and structural parsing, offering no direct contributions to embodied perception, spatial reasoning, or action-space modeling relevant to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01840)
- **👥 Authors**: Hao Wu, Haoran Lou, Xinyue Li, Zuodong Zhong, Zhaojun Sun, Phellon Chen, Xuanhe Zhou, Kai Zuo, Yibo Chen, Xu Tang, Yao Hu, Boxiang Zhou, Jian Wu, Yongji Wu, Wenxin Yu, Yingmiao Liu, Yuhao Huang, Manjie Xu, Gang Liu, Yidong Ma, Zhichao Sun, Changhao Qiao
- **🏷️ Tags**: #Foundation_Model #LLM #Reinforcement_Learning

---

### 📄 AI-for-Science Low-code Platform with Bayesian Adversarial Multi-Agent Framework (Score: 3/10)
- **💡 Innovation**: The paper introduces a Bayesian adversarial multi-agent framework that co-optimizes test cases and code generation to improve reliability in scientific software development.
- **⚠️ Limitations**: The framework is focused on software engineering for scientific computing rather than physical embodiment, sensorimotor control, or real-world interaction, making it largely irrelevant to the specified robotics and embodied AI research interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.03233v1)
- **👥 Authors**: Zihang Zeng, Jiaquan Zhang, Pengze Li, Yuan Qi, Xi Chen
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Understanding and Mitigating Dataset Corruption in LLM Steering (Score: 3/10)
- **💡 Innovation**: The paper introduces the application of robust mean estimation techniques to mitigate the impact of adversarial or noisy data corruption in contrastive steering vectors for LLMs.
- **⚠️ Limitations**: The study is strictly confined to text-based LLM activation steering and lacks any connection to embodied agents, multi-modal action spaces, or the specific challenges of high-dimensional sensorimotor data.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.03206v1)
- **👥 Authors**: Cullen Anderson, Narmeen Oozeer, Foad Namjoo, Remy Ogasawara, Amirali Abdullah, Jeff M. Phillips
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Saarthi for AGI: Towards Domain-Specific General Intelligence for Formal Verification (Score: 3/10)
- **💡 Innovation**: The paper introduces a domain-specific agentic framework for formal verification by combining structured rulebooks with GraphRAG to improve SystemVerilog Assertion generation.
- **⚠️ Limitations**: The work is strictly focused on software/hardware verification and lacks any connection to physical embodiment, world modeling, or robotic control tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.03175v1)
- **👥 Authors**: Aman Kumar, Deepak Narayan Gadde, Luu Danh Minh, Vaisakh Naduvodi Viswambharan, Keerthan Kopparam Radhakrishna, Sivaram Pothireddypalli
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 CharacterFlywheel: Scaling Iterative Improvement of Engaging and Steerable LLMs in Production (Score: 3/10)
- **💡 Innovation**: The paper introduces a systematic, iterative 'flywheel' framework for continuous production-scale fine-tuning and RL optimization of LLMs specifically tailored for social engagement metrics.
- **⚠️ Limitations**: The work is strictly focused on text-based social chat applications and lacks any connection to physical agency, multi-modal perception, or embodied environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01973)
- **👥 Authors**: Yixin Nie, Lin Guan, Zhongyao Ma, Anchit Gupta, Yipin Zhou, Xiao Li, Zhengping Zhou, Raymond Zeng, Gelin Zhou, Shigan Chu, Ajay Thampi, Wancen Mu, Nathan Shuster, Ketong Wang, Lin Chen, Jason Brewer, Derek Hao Hu, Alexander McCauley, Jason Weston, Sem Park, Na Zhang, Kevin Tang
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 Cryo-Bench: Benchmarking Foundation Models for Cryosphere Applications (Score: 3/10)
- **💡 Innovation**: The paper introduces a specialized benchmark dataset (Cryo-Bench) to evaluate the performance of existing Geo-Foundation Models on specific cryospheric remote sensing tasks.
- **⚠️ Limitations**: The work is strictly focused on Earth observation and remote sensing, lacking any connection to embodied agents, physical interaction, or the robotics-centric domains specified in the interest profile.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01576)
- **👥 Authors**: Saurabh Kaushik, Lalit Maurya, Beth Tellman
- **🏷️ Tags**: #Foundation_Model

---

### 📄 OpenAutoNLU: Open Source AutoML Library for NLU (Score: 1/10)
- **💡 Innovation**: The paper introduces an automated machine learning library specifically optimized for text classification and named entity recognition tasks.
- **⚠️ Limitations**: The work is entirely focused on traditional NLP tasks and lacks any connection to robotics, embodied agents, or physical world interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01824)
- **👥 Authors**: Grigory Arshinov, Aleksandr Boriskin, Sergey Senichev, Ayaz Zaripov, Daria Galimzianova, Daniil Karpov, Leonid Sanochkin
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Legal RAG Bench: an end-to-end benchmark for legal RAG (Score: 1/10)
- **💡 Innovation**: The paper introduces a domain-specific benchmark and a hierarchical error decomposition framework specifically designed to isolate retrieval versus reasoning performance in legal RAG systems.
- **⚠️ Limitations**: The paper is entirely focused on legal document retrieval and natural language processing, offering no contribution to robotics, embodied perception, or physical world modeling.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.01710)
- **👥 Authors**: Abdur-Rahman Butler, Umar Butler
- **🏷️ Tags**: #LLM #Foundation_Model

---


