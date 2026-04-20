# 📅 2026-03-23 - Paper Digest
## Summary
Total Papers: 39 | High Impact: 6

## 📝 Papers List
### 🔥 CanViT: Toward Active-Vision Foundation Models (Score: 8/10)
- **💡 Innovation**: CanViT introduces an asymmetric cross-attention mechanism and a spatiotopic latent canvas to decouple retinotopic feature extraction from scene-wide memory, enabling efficient active vision.
- **⚠️ Limitations**: The current evaluation is restricted to static image datasets like ADE20K and ImageNet, leaving the model's performance in dynamic, closed-loop robotic environments unverified.
- **🔗 Link**: [[CanViT]]
- **👥 Authors**: Yohaï-Eliel Berreby, Sabrina Du, Audrey Durand, B. Suresh Krishna
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #World_Model

---

### 🔥 EgoForge: Goal-Directed Egocentric World Simulator (Score: 8/10)
- **💡 Innovation**: EgoForge introduces VideoDiffusionNFT, a trajectory-level reward-guided refinement mechanism that optimizes diffusion sampling for temporal causality and goal alignment in egocentric video generation.
- **⚠️ Limitations**: The reliance on diffusion-based sampling for video generation may introduce significant latency, potentially hindering real-time closed-loop control in high-frequency robotic manipulation tasks.
- **🔗 Link**: [[EgoForge]]
- **👥 Authors**: Yifan Shen, Jiateng Liu, Xinzhuo Li, Yuanzhe Liu, Bingxuan Li, Houze Yang, Wenqi Jia, Yijiang Li, Tianjiao Yu, James Matthew Rehg, Xu Cao, Ismini Lourentzou
- **🏷️ Tags**: #World_Model #Diffusion_Model #Embodied_AI

---

### ✨ ProactiveBench: Benchmarking Proactiveness in Multimodal Large Language Models (Score: 7/10)
- **💡 Innovation**: The paper introduces a systematic benchmark for evaluating proactive information-seeking behavior in MLLMs and demonstrates that such behavior can be effectively induced via reinforcement learning fine-tuning.
- **⚠️ Limitations**: The benchmark relies on repurposed static datasets rather than interactive, closed-loop environments, which may not fully capture the complexities of real-world embodied decision-making.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19466)
- **👥 Authors**: Thomas De Min, Subhankar Roy, Stéphane Lathuilière, Elisa Ricci, Massimiliano Mancini
- **🏷️ Tags**: #Foundation_Model #LLM #Reinforcement_Learning #Embodied_AI

---

### ✨ A Subgoal-driven Framework for Improving Long-Horizon LLM Agents (Score: 7/10)
- **💡 Innovation**: The framework introduces MiRA, a reinforcement learning training paradigm that utilizes dense, milestone-based reward signals to mitigate the sparse reward problem in long-horizon LLM agent planning.
- **⚠️ Limitations**: The evaluation is restricted to digital web-based environments, leaving the transferability of these subgoal decomposition techniques to physical embodied robotics tasks unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19685)
- **👥 Authors**: Taiyi Wang, Sian Gooding, Florian Hartmann, Oriana Riva, Edward Grefenstette
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ WorldAgents: Can Foundation Image Models be Agents for 3D World Models? (Score: 7/10)
- **💡 Innovation**: The paper introduces a multi-agent architecture that leverages VLM-based directors and verifiers to extract implicit 3D spatial consistency from 2D foundation image models for world synthesis.
- **⚠️ Limitations**: The approach relies on iterative generation and verification cycles, which may introduce significant latency and computational overhead compared to end-to-end generative world models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19708)
- **👥 Authors**: Ziya Erkoç, Angela Dai, Matthias Nießner
- **🏷️ Tags**: #World_Model #Foundation_Model #LLM #Diffusion_Model

---

### ✨ Breaking the Capability Ceiling of LLM Post-Training by Reintroducing Markov States (Score: 7/10)
- **💡 Innovation**: The paper introduces a framework that replaces history-dependent LLM post-training with explicit Markov state representations to improve sample efficiency and reasoning discovery.
- **⚠️ Limitations**: The empirical evaluation is currently restricted to logic puzzles, leaving the scalability and effectiveness of Markovian state estimation in high-dimensional embodied or continuous action spaces unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19987)
- **👥 Authors**: Yurun Yuan, Tengyang Xie
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Privacy-Preserving Reinforcement Learning from Human Feedback via Decoupled Reward Modeling (Score: 6/10)
- **💡 Innovation**: The paper introduces a decoupled reward modeling framework that applies differential privacy exclusively to the reward learning phase of RLHF to mitigate privacy leakage while maintaining policy performance.
- **⚠️ Limitations**: The approach is evaluated solely on text-based LLM alignment tasks, leaving its efficacy and privacy-utility trade-offs in high-dimensional embodied or robotic control settings unexplored.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22563v1)
- **👥 Authors**: Young Hyun Cho, Will Wei Sun
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Ego2Web: A Web Agent Benchmark Grounded in Egocentric Videos (Score: 6/10)
- **💡 Innovation**: The paper introduces a cross-modal benchmark that bridges egocentric video perception with web-based agent execution through an automated data-generation pipeline and a specialized LLM-as-a-Judge evaluation framework.
- **⚠️ Limitations**: The benchmark focuses on high-level task planning and perception rather than low-level physical control or closed-loop interaction with the environment.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22529v1)
- **👥 Authors**: Shoubin Yu, Lei Shu, Antoine Yang, Yao Fu, Srinivas Sunkara, Maria Wang, Jindong Chen, Mohit Bansal, Boqing Gong
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #LLM

---

### ✨ Astrolabe: Steering Forward-Process Reinforcement Learning for Distilled Autoregressive Video Models (Score: 6/10)
- **💡 Innovation**: Astrolabe introduces a forward-process RL formulation for distilled autoregressive video models that optimizes inference endpoints via negative-aware fine-tuning without requiring reverse-process unrolling.
- **⚠️ Limitations**: The method is specifically optimized for video generation quality rather than embodied control tasks, and the reliance on reward-based alignment may still struggle with complex long-horizon temporal consistency.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.17051)
- **👥 Authors**: Songchun Zhang, Zeyue Xue, Siming Fu, Jie Huang, Xianghao Kong, Y Ma, Haoyang Huang, Nan Duan, Anyi Rao
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model

---

### ✨ The Y-Combinator for LLMs: Solving Long-Context Rot with λ-Calculus (Score: 6/10)
- **💡 Innovation**: The paper introduces a typed functional runtime based on λ-calculus to constrain recursive LLM reasoning, replacing open-ended code generation with pre-verified combinators.
- **⚠️ Limitations**: The framework is primarily evaluated on abstract long-context reasoning tasks rather than embodied or sequential decision-making environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.20105)
- **👥 Authors**: Amartya Roy, Rasul Tutunov, Xiaotong Ji, Matthieu Zimmer, Haitham Bou-Ammar
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Reasoning as Compression: Unifying Budget Forcing via the Conditional Information Bottleneck (Score: 6/10)
- **💡 Innovation**: The paper formalizes efficient Chain-of-Thought reasoning as a Conditional Information Bottleneck (CIB) problem, optimizing the reasoning trace as a bridge between prompt and response to minimize redundant information.
- **⚠️ Limitations**: The approach relies on a language model prior for surprisal-based cost estimation, which may not generalize well to non-textual modalities or complex embodied reasoning tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08462)
- **👥 Authors**: Fabio Valerio Massoli, Andrey Kuzmin, Arash Behboodi
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ LoopRPT: Reinforcement Pre-Training for Looped Language Models (Score: 6/10)
- **💡 Innovation**: LoopRPT introduces a reinforcement pre-training framework that applies reinforcement signals directly to latent reasoning steps in looped architectures using EMA teacher references and noisy rollouts.
- **⚠️ Limitations**: The approach is currently validated only on language-based reasoning tasks, leaving its efficacy for high-dimensional embodied control or multimodal latent spaces unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19714)
- **👥 Authors**: Guo Tang, Shixin Jiang, Heng Chang, Nuo Chen, Yuhan Li, Huiming Fan, Jia Li, Ming Liu, Bing Qin
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ BEAVER: A Training-Free Hierarchical Prompt Compression Method via Structure-Aware Page Selection (Score: 6/10)
- **💡 Innovation**: BEAVER introduces a training-free hierarchical prompt compression framework that utilizes dual-path pooling and structure-aware page selection to map long-context inputs into dense tensors.
- **⚠️ Limitations**: The method focuses exclusively on text-based long-context retrieval and lacks evaluation on multi-modal or embodied reasoning tasks where semantic density differs significantly from document processing.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19635)
- **👥 Authors**: Zhengpei Hu, Kai Li, Dapeng Fu, Chang Zeng, Yue Li, Yuanhao Tang, Jianqiang Huang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ HiMu: Hierarchical Multimodal Frame Selection for Long Video Question Answering (Score: 6/10)
- **💡 Innovation**: HiMu utilizes a hierarchical logic tree generated by an LLM to decompose complex queries into atomic predicates, which are then evaluated via lightweight multimodal experts and fuzzy-logic temporal composition.
- **⚠️ Limitations**: The framework relies on pre-defined, static multimodal experts and lacks the end-to-end learnable temporal reasoning required for complex embodied decision-making tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.18558)
- **👥 Authors**: Dan Ben-Ami, Gabriele Serussi, Kobi Cohen, Chaim Baskin
- **🏷️ Tags**: #LLM #Foundation_Model #VLA

---

### ✨ Teaching an Agent to Sketch One Part at a Time (Score: 6/10)
- **💡 Innovation**: The method introduces a multi-turn process-reward reinforcement learning framework to generate vector sketches sequentially by decomposing them into semantic parts.
- **⚠️ Limitations**: The approach is limited to 2D vector sketch generation and lacks direct application to 3D physical robot manipulation or embodied control tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19500)
- **👥 Authors**: Xiaodan Du, Ruize Xu, David Yunis, Yael Vinker, Greg Shakhnarovich
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Cooperation and Exploitation in LLM Policy Synthesis for Sequential Social Dilemmas (Score: 6/10)
- **💡 Innovation**: The paper introduces an iterative LLM-based policy synthesis framework that utilizes dense social-metric feedback to guide the generation of programmatic agent policies in multi-agent sequential social dilemmas.
- **⚠️ Limitations**: The approach is restricted to abstract grid-world environments and lacks validation in physical or high-fidelity embodied robotics settings.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19453)
- **👥 Authors**: Víctor Gallego
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ CurveStream: Boosting Streaming Video Understanding in MLLMs via Curvature-Aware Hierarchical Visual Memory Management (Score: 6/10)
- **💡 Innovation**: The method introduces a training-free memory management framework that uses geometric curvature of feature trajectories to dynamically prioritize semantically significant frames in streaming video.
- **⚠️ Limitations**: The approach is evaluated primarily on video understanding benchmarks rather than closed-loop embodied control tasks, leaving its efficacy in real-time robotic decision-making unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19571)
- **👥 Authors**: Chao Wang, Xudong Tan, Jianjian Cao, Kangcong Li, Tao Chen
- **🏷️ Tags**: #Foundation_Model #LLM #Embodied_AI

---

### ✨ TAPESTRY: From Geometry to Appearance via Consistent Turntable Videos (Score: 6/10)
- **💡 Innovation**: TAPESTRY utilizes geometry-conditioned video diffusion to generate consistent 360-degree turntable videos from untextured meshes, which are then back-projected to synthesize high-fidelity UV textures.
- **⚠️ Limitations**: The framework relies on a multi-stage pipeline for 3D-aware inpainting to handle occlusions, which may introduce artifacts or temporal inconsistencies during the secondary generation phase.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.17735)
- **👥 Authors**: Yan Zeng, Haoran Jiang, Kaixin Yao, Qixuan Zhang, Longwen Zhang, Lan Xu, Jingyi Yu
- **🏷️ Tags**: #Diffusion_Model #3D_Gaussian_Splatting

---

### ✨ Adaptive Layerwise Perturbation: Unifying Off-Policy Corrections for LLM RL (Score: 6/10)
- **💡 Innovation**: The method introduces Adaptive Layerwise Perturbation (ALP) to stabilize LLM reinforcement learning by injecting learnable noise into hidden states to mitigate heavy-tailed importance ratios.
- **⚠️ Limitations**: The approach is evaluated primarily on text-based reasoning tasks, leaving its efficacy in high-dimensional, continuous-action embodied control settings unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19470)
- **👥 Authors**: Chenlu Ye, Xuanchang Zhang, Yifan Hao, Zhou Yu, Ziji Zhang, Abhinav Gullapalli, Hao Chen, Jing Huang, Tong Zhang
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Q-Tacit: Image Quality Assessment via Latent Visual Reasoning (Score: 5/10)
- **💡 Innovation**: The paper introduces a latent-space reasoning paradigm for image quality assessment that bypasses the bottleneck of textual tokenization by injecting structural visual quality priors directly into the latent representation.
- **⚠️ Limitations**: The approach is strictly focused on image quality assessment and lacks a clear mechanism for generalization to dynamic, multi-modal embodied tasks or action-conditioned reasoning.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22641v1)
- **👥 Authors**: Yuxuan Jiang, Yixuan Li, Hanwei Zhu, Siyue Teng, Fan Zhang, David Bull
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ Bridging the Know-Act Gap via Task-Level Autoregressive Reasoning (Score: 5/10)
- **💡 Innovation**: The paper introduces a task-level autoregressive framework that decouples discriminative validation from generative reasoning through self-distillation to mitigate hallucination in LLMs.
- **⚠️ Limitations**: The approach is evaluated on a scientific QA benchmark rather than embodied tasks, leaving its efficacy in high-stakes robotic decision-making or action-sequence planning unproven.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22619v1)
- **👥 Authors**: Jihyun Janice Ahn, Ryo Kamoi, Berk Atil, Renze Lou, WonWoo Kang, Heehyun Park, Sarkar Snigdha Sarathi Das, Zhuoyang Zou, Xiaoxin Lu, Yusen Zhang, Asfahan Shah, Ridwanul Hasan Tanvir, Lingxiao Zhao, Hongxi Huang, Vignesh Venkatesh, Dianjun Lin, Hamid Shah, Wentao Wang, Zhanpeng Song, Joshua Reed Bassin, Dax Patel, Ishan Appareddy Agrahar, Sahil Pardasani, Xin Dong, Fatemeh Rahbari, Benjamin David Rishel, Soochan Andrew Lee, Yuv Boghani, Ali B. AlNaseeb, Pranav Suby, Seokhyeon Bae, Shreya Buddharaju, Damien Kula, Soumyadeep Das, Hanyang Frank Liu, Faye Mo, Wenpeng Yin
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Understanding LLM Performance Degradation in Multi-Instance Processing: The Roles of Instance Count and Context Length (Score: 5/10)
- **💡 Innovation**: The paper identifies that LLM performance degradation in multi-instance processing is driven more significantly by the number of discrete instances than by total context length.
- **⚠️ Limitations**: The study focuses on general text-based sentiment and aggregation tasks rather than the high-frequency, multimodal, or temporal constraints typical of embodied robotics workflows.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22608v1)
- **👥 Authors**: Jingxuan Chen, Mohammad Taher Pilehvar, Jose Camacho-Collados
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ A Foundation Model for Instruction-Conditioned In-Context Time Series Tasks (Score: 5/10)
- **💡 Innovation**: The model employs a hierarchical Transformer architecture with cross-example attention to enable instruction-conditioned in-context learning for multi-task time series forecasting.
- **⚠️ Limitations**: The approach is restricted to 1D time series data and lacks integration with multi-modal sensory inputs required for embodied robotic control.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22586v1)
- **👥 Authors**: Anish Saha, Konstantin Shmakov
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ STRIATUM-CTF: A Protocol-Driven Agentic Framework for General-Purpose CTF Solving (Score: 5/10)
- **💡 Innovation**: The framework introduces a standardized Model Context Protocol (MCP) to abstract tool interfaces for stateful, multi-step reasoning in cybersecurity agentic workflows.
- **⚠️ Limitations**: The approach is strictly limited to cyber-reasoning and lacks integration with physical sensors, motor control, or spatial reasoning required for embodied robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22577v1)
- **👥 Authors**: James Hugglestone, Samuel Jacob Chacko, Dawson Stoller, Ryan Schmidt, Xiuwen Liu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ GraphRAG for Engineering Diagrams: ChatP&ID Enables LLM Interaction with P&IDs (Score: 5/10)
- **💡 Innovation**: The paper introduces a GraphRAG-based agentic framework that converts DEXPI-standard P&IDs into structured knowledge graphs to facilitate grounded LLM reasoning over engineering diagrams.
- **⚠️ Limitations**: The approach relies on pre-existing structured data (DEXPI) and does not address the challenge of parsing unstructured or legacy raster-based engineering diagrams.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22528v1)
- **👥 Authors**: Achmad Anggawirya Alimin, Artur M. Schweidtmann
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ LLMON: An LLM-native Markup Language to Leverage Structure and Semantics at the LLM Interface (Score: 5/10)
- **💡 Innovation**: LLMON introduces a structured markup language designed to explicitly delineate instructions from data within LLM prompts to improve semantic parsing and security.
- **⚠️ Limitations**: The abstract lacks specific performance metrics or architectural details on how this markup is integrated into the model's internal attention mechanisms or training objectives.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22519v1)
- **👥 Authors**: Michael Hind, Basel Shbita, Bo Wu, Farhan Ahmed, Chad DeLuca, Nathan Fulton, David Cox, Dan Gutfreund
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Beyond Single Tokens: Distilling Discrete Diffusion Models via Discrete MMD (Score: 5/10)
- **💡 Innovation**: The method introduces Discrete Moment Matching Distillation (D-MMD) to enable efficient multi-step distillation for discrete diffusion models by minimizing the Maximum Mean Discrepancy between teacher and student distributions.
- **⚠️ Limitations**: The abstract lacks specific evidence regarding the computational overhead of the MMD objective or its scalability to high-dimensional latent spaces common in embodied tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.20155)
- **👥 Authors**: Emiel Hoogeboom, David Ruhe, Jonathan Heek, Thomas Mensink, Tim Salimans
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ Language on Demand, Knowledge at Core: Composing LLMs with Encoder-Decoder Translation Models for Extensible Multilinguality (Score: 5/10)
- **💡 Innovation**: The paper introduces a compositional architecture that bridges English-centric LLMs with multilingual encoder-decoder translation models using lightweight cross-model mapping layers and an optimal transport-based alignment objective.
- **⚠️ Limitations**: The approach relies on external translation models, which may introduce latency and error propagation issues that are not evaluated in the context of real-time embodied systems.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.17512)
- **👥 Authors**: Mengyu Bu, Yang Feng
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 AwesomeLit: Towards Hypothesis Generation with Agent-Supported Literature Research (Score: 4/10)
- **💡 Innovation**: The system integrates a human-in-the-loop agentic workflow with a dynamic query exploration tree and semantic similarity visualization to assist in academic hypothesis generation.
- **⚠️ Limitations**: The paper focuses on general literature research methodology rather than providing technical contributions to embodied intelligence, robot control, or specific AI model architectures.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22648v1)
- **👥 Authors**: Zefei Xie, Yuhan Guo, Kai Xu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 PIVM: Diffusion-Based Prior-Integrated Variation Modeling for Anatomically Precise Abdominal CT Synthesis (Score: 4/10)
- **💡 Innovation**: The framework introduces a diffusion-based approach that predicts voxel-wise intensity variations relative to organ-specific priors to synthesize anatomically accurate CT images.
- **⚠️ Limitations**: The method is strictly constrained to medical image synthesis and lacks integration with embodied perception or action-oriented spatial reasoning.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22626v1)
- **👥 Authors**: Dinglun He, Baoming Zhang, Xu Wang, Yao Hao, Deshan Yang, Ye Duan
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 Dress-ED: Instruction-Guided Editing for Virtual Try-On and Try-Off (Score: 4/10)
- **💡 Innovation**: The paper introduces a large-scale, multimodal dataset for instruction-guided garment editing by integrating MLLM-based understanding with diffusion-based synthesis.
- **⚠️ Limitations**: The work is strictly focused on 2D image-to-image synthesis and lacks any grounding in 3D geometry, physical interaction, or embodied control tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22607v1)
- **👥 Authors**: Fulvio Sanguigni, Davide Lobba, Bin Ren, Marcella Cornia, Nicu Sebe, Rita Cucchiara
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #LLM

---

### 📄 AI Mental Models: Learned Intuition and Deliberation in a Bounded Neural Architecture (Score: 4/10)
- **💡 Innovation**: The paper introduces a dual-path neural architecture that explicitly separates intuitive associative prediction from deliberative reasoning pathways to improve performance on syllogistic logic tasks.
- **⚠️ Limitations**: The study is restricted to a static, symbolic reasoning benchmark and lacks any connection to sensory-motor grounding, temporal dynamics, or embodied interaction.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22561v1)
- **👥 Authors**: Laurence Anthony
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Do Large Language Models Reduce Research Novelty? Evidence from Information Systems Journals (Score: 4/10)
- **💡 Innovation**: The study quantifies the impact of LLM adoption on academic novelty by measuring the cosine distance of paper embeddings from prior literature using SPECTER2.
- **⚠️ Limitations**: The analysis is restricted to Information Systems journals and relies on semantic embedding distance as a proxy for intellectual novelty, which may not capture qualitative breakthroughs.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22510v1)
- **👥 Authors**: Ali Safari
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 LumosX: Relate Any Identities with Their Attributes for Personalized Video Generation (Score: 4/10)
- **💡 Innovation**: The framework introduces Relational Self-Attention and Cross-Attention mechanisms to enforce explicit subject-attribute dependencies within diffusion-based video generation.
- **⚠️ Limitations**: The method is strictly focused on generative video aesthetics and lacks any grounding in physical dynamics, temporal consistency for control tasks, or embodied interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.20192)
- **👥 Authors**: Jiazheng Xing, Fei Du, Hangjie Yuan, Pengwei Liu, Hongbin Xu, Hai Ci, Ruigang Niu, Weihua Chen, Fan Wang, Yong Liu
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #LLM

---

### 📄 s2n-bignum-bench: A practical benchmark for evaluating low-level code reasoning of LLMs (Score: 4/10)
- **💡 Innovation**: The paper introduces a benchmark for evaluating LLM-based formal proof synthesis specifically targeting industrial-grade cryptographic assembly routines in the HOL Light environment.
- **⚠️ Limitations**: The benchmark is strictly focused on formal verification of low-level code and lacks any connection to physical robot control, perception, or embodied decision-making.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14628)
- **👥 Authors**: Balaji Rao, John Harrison, Soonho Kong, Juneyoung Lee, Carlo Lipizzi
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Sketch2CT: Multimodal Diffusion for Structure-Aware 3D Medical Volume Generation (Score: 3/10)
- **💡 Innovation**: The paper introduces a two-stage generative pipeline that uses a capsule-attention backbone to condition 3D medical volume synthesis on 2D sketches and textual descriptions.
- **⚠️ Limitations**: The method is strictly confined to medical imaging synthesis and lacks any integration with embodied agents, action spaces, or physical environment interaction.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.22509v1)
- **👥 Authors**: Delin An, Chaoli Wang
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 AgentDS Technical Report: Benchmarking the Future of Human-AI Collaboration in Domain-Specific Data Science (Score: 3/10)
- **💡 Innovation**: The paper introduces a benchmark suite for evaluating human-AI collaborative performance in domain-specific data science workflows across six distinct industries.
- **⚠️ Limitations**: The study focuses exclusively on software-based data science tasks and lacks any connection to physical embodiment, robotics, or sensorimotor control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.19005)
- **👥 Authors**: An Luo, Jin Du, Xun Xian, Robert Specht, Fangqiao Tian, Ganghua Wang, Xuan Bi, Charles Fleming, Ashish Kundu, Jayanth Srinivasa, Mingyi Hong, Rui Zhang, Tianxi Li, Galin Jones, Jie Ding
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Probing Cultural Signals in Large Language Models through Author Profiling (Score: 3/10)
- **💡 Innovation**: The paper introduces Modality Accuracy Divergence (MAD) and Recall Divergence (RD) metrics to quantify cultural bias in LLM-based author profiling tasks.
- **⚠️ Limitations**: The study focuses exclusively on text-based cultural profiling from song lyrics, offering no direct application or implications for embodied agents or physical robot control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16749)
- **👥 Authors**: Valentin Lafargue, Ariel Guerra-Adames, Emmanuelle Claeys, Elouan Vuichard, Jean-Michel Loubes
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 ReLMXEL: Adaptive RL-Based Memory Controller with Explainable Energy and Latency Optimization (Score: 3/10)
- **💡 Innovation**: The paper proposes a multi-agent reinforcement learning framework that utilizes reward decomposition to optimize memory controller parameters for energy and latency.
- **⚠️ Limitations**: The research focuses exclusively on computer architecture and memory systems, lacking any application to physical robot hardware, vision-language models, or embodied agents.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.17309)
- **👥 Authors**: Panuganti Chirag Sai, Gandholi Sarat, R. Raghunatha Sarma, Venkata Kalyan Tavva, Naveen M
- **🏷️ Tags**: #Reinforcement_Learning

---


