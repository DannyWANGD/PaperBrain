# 📅 2026-03-10 - Paper Digest
## Summary
Total Papers: 44 | High Impact: 7

## 📝 Papers List
### 🔥 TiPToP: A Modular Open-Vocabulary Planning System for Robotic Manipulation (Score: 8/10)
- **💡 Innovation**: TiPToP introduces a modular, zero-shot planning framework that leverages vision foundation models to perform complex manipulation tasks without requiring embodiment-specific robot demonstration data.
- **⚠️ Limitations**: The system relies on the performance of underlying TAMP components and vision foundation models, which may struggle with highly dynamic environments or tasks requiring fine-grained tactile feedback compared to end-to-end VLA models.
- **🔗 Link**: [[TiPToP]]
- **👥 Authors**: William Shen, Nishanth Kumar, Sahit Chintalapudi, Jie Wang, Christopher Watson, Edward Hu, Jing Cao, Dinesh Jayaraman, Leslie Pack Kaelbling, Tomás Lozano-Pérez
- **🏷️ Tags**: #Robot_Manipulation #Embodied_AI #Foundation_Model #LLM #Sim2Real

---

### 🔥 HydroShear: Hydroelastic Shear Simulation for Tactile Sim-to-Real Reinforcement Learning (Score: 8/10)
- **💡 Innovation**: HydroShear introduces a non-holonomic hydroelastic contact model that tracks on-surface point displacements to simulate complex stick-slip transitions and path-dependent shear forces for tactile sensors.
- **⚠️ Limitations**: The method relies on watertight geometries and may struggle with highly deformable or non-rigid objects that deviate from the assumed hydroelastic contact model.
- **🔗 Link**: [[HydroShear]]
- **👥 Authors**: An Dang, Jayjun Lee, Mustafa Mukadam, X. Alice Wu, Bernadette Bucher, Manikantan Nambi, Nima Fazeli
- **🏷️ Tags**: #Robot_Manipulation #Sim2Real #Reinforcement_Learning #Embodied_AI

---

### ✨ Emerging Extrinsic Dexterity in Cluttered Scenes via Dynamics-aware Policy Learning (Score: 7/10)
- **💡 Innovation**: The paper introduces a Dynamics-Aware Policy Learning (DAPL) framework that utilizes explicit world modeling to learn contact-induced object dynamics, enabling the emergence of extrinsic dexterity in cluttered environments without manual heuristics.
- **⚠️ Limitations**: The real-world success rate of 50% suggests that the sim-to-real gap remains significant, and the approach may struggle with highly deformable objects or complex, long-horizon manipulation tasks not covered in the grocery deployment.
- **🔗 Link**: [[Emerging Extrinsic Dexterity in Cluttered Scenes via Dynamicsaware Policy Learning]]
- **👥 Authors**: Yixin Zheng, Jiangran Lyu, Yifan Zhang, Jiayi Chen, Mi Yan, Yuntian Deng, Xuesong Shi, Xiaoguang Zhao, Yizhou Wang, Zhizheng Zhang, He Wang
- **🏷️ Tags**: #Robot_Manipulation #World_Model #Reinforcement_Learning #Embodied_AI #Sim2Real

---

### ✨ LoGeR: Long-Context Geometric Reconstruction with Hybrid Memory (Score: 7/10)
- **💡 Innovation**: LoGeR introduces a hybrid memory architecture combining parametric Test-Time Training (TTT) for global coordinate anchoring and non-parametric Sliding Window Attention (SWA) for local precision to enable long-horizon 3D reconstruction.
- **⚠️ Limitations**: The paper focuses on geometric reconstruction rather than semantic understanding or closed-loop control, leaving its direct utility for downstream robot manipulation tasks unverified.
- **🔗 Link**: [[LoGeR]]
- **👥 Authors**: Junyi Zhang, Charles Herrmann, Junhwa Hur, Chen Sun, Ming-Hsuan Yang, Forrester Cole, Trevor Darrell, Deqing Sun
- **🏷️ Tags**: #Foundation_Model #Embodied_AI #World_Model

---

### ✨ LiveWorld: Simulating Out-of-Sight Dynamics in Generative Video World Models (Score: 7/10)
- **💡 Innovation**: LiveWorld introduces a monitor-based mechanism that decouples dynamic entity simulation from the observer's field of view, enabling persistent 4D world evolution through a global state representation.
- **⚠️ Limitations**: The framework relies on explicit entity tracking and simulation, which may struggle with complex, non-rigid, or highly cluttered environments where object segmentation and state synchronization become computationally prohibitive.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07145)
- **👥 Authors**: Zicheng Duan, Jiatong Xia, Zeyu Zhang, Wenbo Zhang, Gengze Zhou, Chenhui Gou, Yefei He, Feng Chen, Xinyu Zhang, Lingqiao Liu
- **🏷️ Tags**: #World_Model #Diffusion_Model #Embodied_AI

---

### ✨ MWM: Mobile World Models for Action-Conditioned Consistent Prediction (Score: 7/10)
- **💡 Innovation**: The paper introduces Action-Conditioned Consistency (ACC) and Inference-Consistent State Distillation (ICSD) to mitigate drift and training-inference mismatch in diffusion-based world models for navigation.
- **⚠️ Limitations**: The evaluation is primarily focused on image-goal navigation, leaving the scalability and generalizability of the world model to more complex, long-horizon manipulation tasks unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07799)
- **👥 Authors**: Han Yan, Zishang Xiang, Zeyu Zhang, Hao Tang
- **🏷️ Tags**: #World_Model #Diffusion_Model #Embodied_AI #Sim2Real

---

### ✨ SeedPolicy: Horizon Scaling via Self-Evolving Diffusion Policy for Robot Manipulation (Score: 7/10)
- **💡 Innovation**: The paper introduces Self-Evolving Gated Attention (SEGA), a recurrent temporal module that compresses long-horizon observations into a fixed-size latent state to mitigate the performance degradation of Diffusion Policies over extended time sequences.
- **⚠️ Limitations**: The evaluation is primarily focused on imitation learning within the RoboTwin 2.0 benchmark, leaving the generalization capabilities to real-world deployment and diverse, unseen environments under-explored.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.05117)
- **👥 Authors**: Youqiang Gui, Yuxuan Zhou, Shen Cheng, Xinyang Yuan, Haoqiang Fan, Peng Cheng, Shuaicheng Liu
- **🏷️ Tags**: #Robot_Manipulation #Diffusion_Model #Embodied_AI #VLA

---

### ✨ When Learning Rates Go Wrong: Early Structural Signals in PPO Actor-Critic (Score: 6/10)
- **💡 Innovation**: The paper introduces the Overfitting-Underfitting Indicator (OUI), a metric based on hidden neuron activation patterns, to predict the success of PPO training runs early in the training process.
- **⚠️ Limitations**: The empirical validation is restricted to discrete-control environments, leaving it unclear if the OUI metric generalizes to the high-dimensional, continuous action spaces typical of complex robot manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09950v1)
- **👥 Authors**: Alberto Fernández-Hernández, Cristian Pérez-Corral, Jose I. Mestre, Manuel F. Dolz, Jose Duato, Enrique S. Quintana-Ortí
- **🏷️ Tags**: #Reinforcement_Learning #Embodied_AI

---

### ✨ MA-EgoQA: Question Answering over Egocentric Videos from Multiple Embodied Agents (Score: 6/10)
- **💡 Innovation**: The paper introduces a novel benchmark, MA-EgoQA, specifically designed to evaluate the ability of models to process and reason over multiple, simultaneous long-horizon egocentric video streams from different embodied agents.
- **⚠️ Limitations**: The proposed baseline, EgoMAS, is relatively simple and does not fully address the computational complexity or real-time constraints required for actual multi-agent robotic deployment.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09827v1)
- **👥 Authors**: Kangsan Kim, Yanlai Yang, Suji Kim, Woongyeong Yeo, Youngwan Lee, Mengye Ren, Sung Ju Hwang
- **🏷️ Tags**: #Embodied_AI #LLM #Foundation_Model

---

### ✨ ConfCtrl: Enabling Precise Camera Control in Video Diffusion via Confidence-Aware Interpolation (Score: 6/10)
- **💡 Innovation**: The paper introduces a confidence-aware interpolation framework that integrates a Kalman-inspired predict-update mechanism into the diffusion process to balance noisy geometric projections with learned residual corrections.
- **⚠️ Limitations**: The method relies on initial point cloud projections which may struggle with highly dynamic scenes or complex non-Lambertian surfaces, and it lacks explicit integration into an embodied control loop.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09819v1)
- **👥 Authors**: Liudi Yang, George Eskandar, Fengyi Shen, Mohammad Altillawi, Yang Bai, Chi Zhang, Ziyuan Liu, Abhinav Valada
- **🏷️ Tags**: #Diffusion_Model #World_Model #Embodied_AI

---

### ✨ Agentic Critical Training (Score: 6/10)
- **💡 Innovation**: The paper introduces a reinforcement learning paradigm that trains LLM agents to autonomously evaluate and reason about action quality through comparative judgment rather than imitating pre-written reflection text.
- **⚠️ Limitations**: The evaluation is restricted to general agentic benchmarks (e.g., web/tool use) and lacks empirical validation in physical embodied environments or robot manipulation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08706)
- **👥 Authors**: Weize Liu, Minghui Liu, Sy-Tuyen Ho, Souradip Chakraborty, Xiyao Wang, Furong Huang
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Skip to the Good Part: Representation Structure & Inference-Time Layer Skipping in Diffusion vs. Autoregressive LLMs (Score: 6/10)
- **💡 Innovation**: The paper identifies that diffusion-based language models exhibit higher representational redundancy than autoregressive models, enabling effective task-agnostic inference-time layer skipping.
- **⚠️ Limitations**: The study focuses exclusively on text-based reasoning and code generation benchmarks, leaving the applicability of these representational findings to multimodal or embodied VLA architectures unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07475)
- **👥 Authors**: Raghavv Goel, Risheek Garrepalli, Sudhanshu Agrawal, Chris Lott, Mingu Lee, Fatih Porikli
- **🏷️ Tags**: #LLM #Diffusion_Model #Foundation_Model

---

### ✨ How Far Can Unsupervised RLVR Scale LLM Training? (Score: 5/10)
- **💡 Innovation**: The paper provides a unified theoretical framework for Unsupervised Reinforcement Learning with Verifiable Rewards (URLVR), identifying that intrinsic reward methods are fundamentally limited by the alignment between a model's initial confidence and its correctness.
- **⚠️ Limitations**: The study focuses exclusively on text-based LLM training dynamics, leaving the applicability of these scaling limits to multimodal or embodied agents (VLA/Robotics) as an open, unverified question.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08660)
- **👥 Authors**: Bingxiang He, Yuxin Zuo, Zeyuan Liu, Shangziqi Zhao, Zixuan Fu, Junlin Yang, Cheng Qian, Kaiyan Zhang, Yuchen Fan, Ganqu Cui, Xiusi Chen, Youbang Sun, Xingtai Lv, Xuekai Zhu, Li Sheng, Ran Li, Huan-ang Gao, Yuchen Zhang, Bowen Zhou, Zhiyuan Liu, Ning Ding
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ HiAR: Efficient Autoregressive Long Video Generation via Hierarchical Denoising (Score: 5/10)
- **💡 Innovation**: HiAR introduces a hierarchical denoising framework that performs causal generation across all video blocks simultaneously at each denoising step, ensuring context and target frames share the same noise level to mitigate error accumulation.
- **⚠️ Limitations**: The paper focuses on general video generation rather than embodied control, meaning the temporal consistency improvements may not directly translate to the high-precision requirements of robot manipulation or closed-loop policy execution.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08703)
- **👥 Authors**: Kai Zou, Dian Zheng, Hongbo Liu, Tiankai Hang, Bin Liu, Nenghai Yu
- **🏷️ Tags**: #Diffusion_Model #World_Model

---

### ✨ TDM-R1: Reinforcing Few-Step Diffusion Models with Non-Differentiable Reward (Score: 5/10)
- **💡 Innovation**: TDM-R1 introduces a decoupled reinforcement learning paradigm for few-step diffusion models that utilizes surrogate reward learning to enable optimization with non-differentiable reward signals.
- **⚠️ Limitations**: The paper focuses exclusively on text-to-image generation tasks and lacks evaluation on embodied control or robot manipulation benchmarks, limiting its immediate applicability to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07700)
- **👥 Authors**: Yihong Luo, Tianyang Hu, Weijian Luo, Jing Tang
- **🏷️ Tags**: #Diffusion_Model #Reinforcement_Learning #Foundation_Model

---

### ✨ Concept-Guided Fine-Tuning: Steering ViTs away from Spurious Correlations to Improve Robustness (Score: 5/10)
- **💡 Innovation**: The paper introduces a label-free fine-tuning framework that aligns ViT relevance maps with fine-grained semantic concept masks generated automatically by LLMs and VLMs to mitigate spurious correlations.
- **⚠️ Limitations**: The method is evaluated on static image classification benchmarks rather than dynamic embodied tasks, leaving its efficacy in complex, closed-loop robotic manipulation scenarios unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08309)
- **👥 Authors**: Yehonatan Elisha, Oren Barkan, Noam Koenigstein
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ CaTok: Taming Mean Flows for One-Dimensional Causal Image Tokenization (Score: 5/10)
- **💡 Innovation**: CaTok introduces a 1D causal image tokenizer that utilizes a MeanFlow decoder to enforce strict causality in visual tokenization, enabling autoregressive generation without heuristic 2D ordering.
- **⚠️ Limitations**: The paper focuses exclusively on static image reconstruction and generation, lacking any evaluation or discussion on temporal consistency or applicability to embodied action sequences.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.06449)
- **👥 Authors**: Yitong Chen, Zuxuan Wu, Xipeng Qiu, Yu-Gang Jiang
- **🏷️ Tags**: #Foundation_Model #Diffusion_Model #LLM

---

### ✨ HY-WU (Part I): An Extensible Functional Neural Memory Framework and An Instantiation in Text-Guided Image Editing (Score: 5/10)
- **💡 Innovation**: The paper introduces a functional neural memory framework that synthesizes instance-specific weight updates on-the-fly, replacing static weight overwriting with dynamic operator generation.
- **⚠️ Limitations**: The current instantiation is limited to text-guided image editing, leaving the efficacy and scalability of this approach for high-dimensional, real-time embodied control tasks unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07236)
- **👥 Authors**: Tencent HY Team
- **🏷️ Tags**: #Foundation_Model

---

### ✨ Sparse-BitNet: 1.58-bit LLMs are Naturally Friendly to Semi-Structured Sparsity (Score: 5/10)
- **💡 Innovation**: The paper introduces a unified framework, Sparse-BitNet, that demonstrates 1.58-bit LLMs are inherently more robust to N:M semi-structured sparsity than full-precision models.
- **⚠️ Limitations**: The study focuses exclusively on language modeling tasks, leaving the efficacy and transferability of these compressed architectures to compute-constrained embodied agents or VLA models unexplored.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.05168)
- **👥 Authors**: Di Zhang, Xun Wu, Shaohan Huang, Yudong Wang, Hanyong Shao, Yingbo Hao, Zewen Chi, Li Dong, Ting Song, Yan Xia, Zhifang Sui, Furu Wei
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Generalizable Knowledge Distillation from Vision Foundation Models for Semantic Segmentation (Score: 5/10)
- **💡 Innovation**: The paper introduces a two-stage knowledge distillation framework that decouples representation learning from task adaptation using a query-based soft distillation mechanism to preserve the generalization capabilities of vision foundation models.
- **⚠️ Limitations**: The research focuses exclusively on semantic segmentation in static computer vision contexts, lacking evaluation on dynamic embodied tasks or temporal consistency required for robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.02554)
- **👥 Authors**: Chonghua Lv, Dong Zhao, Shuang Wang, Dou Quan, Ning Huyan, Nicu Sebe, Zhun Zhong
- **🏷️ Tags**: #Foundation_Model

---

### ✨ SlowBA: An efficiency backdoor attack towards VLM-based GUI agents (Score: 5/10)
- **💡 Innovation**: The paper introduces a novel backdoor attack strategy (SlowBA) that specifically targets the response latency of VLM-based GUI agents by inducing long reasoning chains via reinforcement learning.
- **⚠️ Limitations**: The attack is highly specific to GUI-based agents and does not address physical embodied systems or real-time robot control loops where latency impacts safety.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08316)
- **👥 Authors**: Junxian Li, Tu Lan, Haozhen Tan, Yan Meng, Haojin Zhu
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Variational Flow Maps: Make Some Noise for One-Step Conditional Generation (Score: 5/10)
- **💡 Innovation**: The paper introduces a variational framework that enables conditional generation in one-step flow maps by learning a noise adapter to map observations to an optimal initial noise distribution.
- **⚠️ Limitations**: The approach is primarily evaluated on static image generation tasks (ImageNet) rather than temporal or embodied control tasks, leaving its efficacy in high-dimensional, dynamic robotic state spaces unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07276)
- **👥 Authors**: Abbas Mammadov, So Takao, Bohan Chen, Ricardo Baptista, Morteza Mardani, Yee Whye Teh, Julius Berner
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 Think Before You Lie: How Reasoning Improves Honesty (Score: 4/10)
- **💡 Innovation**: The paper identifies that deceptive model outputs occupy metastable regions in the representational space, which are destabilized by the process of generating reasoning tokens.
- **⚠️ Limitations**: The study focuses exclusively on text-based moral trade-offs and lacks any connection to physical grounding, embodied decision-making, or multi-modal action spaces.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09957v1)
- **👥 Authors**: Ann Yuan, Asma Ghandeharioun, Carter Blum, Alicia Machado, Jessica Hoffmann, Daphne Ippolito, Martin Wattenberg, Lucas Dixon, Katja Filippova
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Towards a Neural Debugger for Python (Score: 4/10)
- **💡 Innovation**: The paper introduces a 'neural debugger' framework that enables LLMs to perform interactive, state-conditioned execution prediction (stepping, breakpoints) rather than just linear trace generation.
- **⚠️ Limitations**: The work is strictly confined to symbolic code execution and lacks integration with physical environments or multi-modal sensory feedback, limiting its direct applicability to embodied robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09951v1)
- **👥 Authors**: Maximilian Beck, Jonas Gehring, Jannik Kossen, Gabriel Synnaeve
- **🏷️ Tags**: #LLM #Foundation_Model #World_Model

---

### 📄 Generative Drifting is Secretly Score Matching: a Spectral and Variational Perspective (Score: 4/10)
- **💡 Innovation**: The paper provides a theoretical grounding for 'Generative Drifting' by proving it is equivalent to score matching under a Gaussian kernel and analyzing its convergence through the lens of McKean-Vlasov dynamics and Fourier analysis.
- **⚠️ Limitations**: The work is purely theoretical and focused on generative modeling foundations, offering no direct application or empirical evaluation in embodied AI, robotics, or control tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09936v1)
- **👥 Authors**: Erkan Turan, Maks Ovsjanikov
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 MSSR: Memory-Aware Adaptive Replay for Continual LLM Fine-Tuning (Score: 4/10)
- **💡 Innovation**: The paper introduces an adaptive experience replay framework that uses memory strength estimation and dynamic scheduling to mitigate catastrophic forgetting in sequential LLM fine-tuning.
- **⚠️ Limitations**: The work is strictly focused on text-based LLM benchmarks and lacks evaluation on embodied tasks or multi-modal settings relevant to robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09892v1)
- **👥 Authors**: Yiyang Lu, Yu He, Jianlong Chen, Hongyuan Zha
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 InternVL-U: Democratizing Unified Multimodal Models for Understanding, Reasoning, Generation and Editing (Score: 4/10)
- **💡 Innovation**: The paper introduces a lightweight 4B-parameter unified multimodal model that integrates understanding and generation by decoupling visual representations and employing a reasoning-centric data synthesis pipeline.
- **⚠️ Limitations**: The work focuses exclusively on image generation and multimodal understanding, lacking any integration with action spaces or embodied control, making it currently irrelevant for robotics applications.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09877v1)
- **👥 Authors**: Changyao Tian, Danni Yang, Guanzhou Chen, Erfei Cui, Zhaokai Wang, Yuchen Duan, Penghao Yin, Sitao Chen, Ganlin Yang, Mingxin Liu, Zirun Zhu, Ziqian Fan, Leyao Gu, Haomin Wang, Qi Wei, Jinhui Yin, Xue Yang, Zhihang Zhong, Qi Qin, Yi Xin, Bin Fu, Yihao Liu, Jiaye Ge, Qipeng Guo, Gen Luo, Hongsheng Li, Yu Qiao, Kai Chen, Hongjie Zhang
- **🏷️ Tags**: #Foundation_Model #LLM #Diffusion_Model

---

### 📄 SCENEBench: An Audio Understanding Benchmark Grounded in Assistive and Industrial Use Cases (Score: 4/10)
- **💡 Innovation**: The paper introduces a specialized benchmark suite (SCENEBench) designed to evaluate Large Audio Language Models on non-speech audio comprehension tasks relevant to assistive and industrial environments.
- **⚠️ Limitations**: The benchmark relies heavily on synthetic audio construction, which may not fully capture the complex acoustic nuances and sensor noise profiles encountered in real-world robotic deployments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09853v1)
- **👥 Authors**: Laya Iyer, Angelina Wang, Sanmi Koyejo
- **🏷️ Tags**: #Foundation_Model #LLM

---

### 📄 PIRA-Bench: A Transition from Reactive GUI Agents to GUI-based Proactive Intent Recommendation Agents (Score: 4/10)
- **💡 Innovation**: The paper introduces a benchmark and a memory-aware framework (PIRF) to shift GUI agents from reactive instruction-following to proactive intent recommendation based on continuous, noisy visual streams.
- **⚠️ Limitations**: The work focuses exclusively on digital GUI environments rather than physical embodied agents, limiting its direct applicability to robotics or real-world manipulation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08013)
- **👥 Authors**: Yuxiang Chai, Shunye Tang, Han Xiao, Rui Liu, Hongsheng Li
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 AutoResearch-RL: Perpetual Self-Evaluating Reinforcement Learning Agents for Autonomous Neural Architecture Discovery (Score: 4/10)
- **💡 Innovation**: The paper introduces a framework for autonomous neural architecture search by treating code modification as an RL action space, allowing an agent to iteratively optimize a training script without human intervention.
- **⚠️ Limitations**: The approach is limited to hyperparameter and architecture tuning for language models and lacks any connection to physical embodiment, sensorimotor control, or the specific challenges of robotic manipulation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07300)
- **👥 Authors**: Nilesh Jain, Rohit Yadav, Sagar Kotian, Claude AI
- **🏷️ Tags**: #Reinforcement_Learning #LLM

---

### 📄 Scale Space Diffusion (Score: 4/10)
- **💡 Innovation**: The paper introduces a diffusion framework that replaces standard Gaussian noise with downsampling-based degradation, allowing the model to operate on lower-resolution representations during early denoising stages to improve computational efficiency.
- **⚠️ Limitations**: The evaluation is restricted to static image generation (CelebA/ImageNet) without demonstrating applicability to high-frequency temporal dynamics or embodied control tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08709)
- **👥 Authors**: Soumik Mukhopadhyay, Prateksha Udhayanan, Abhinav Shrivastava
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 Scaling Data Difficulty: Improving Coding Models via Reinforcement Learning on Fresh and Challenging Problems (Score: 4/10)
- **💡 Innovation**: The paper introduces an automated, multi-dimensional difficulty-filtering framework that uses LLMs to curate high-quality, challenging competitive programming datasets for improved model training.
- **⚠️ Limitations**: The methodology is strictly confined to the domain of code generation and lacks any empirical validation or discussion regarding its applicability to embodied agents or multimodal action-space learning.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07779)
- **👥 Authors**: Zongqian Li, Tengchao Lv, Shaohan Huang, Yixuan Su, Qinzheng Sun, Qiufeng Yin, Ying Xin, Scarlett Li, Lei Cui, Nigel Collier, Furu Wei
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 MedSteer: Counterfactual Endoscopic Synthesis via Training-Free Activation Steering (Score: 4/10)
- **💡 Innovation**: The paper introduces a training-free activation-steering framework that isolates pathology-specific vectors in diffusion transformer cross-attention layers to enable precise counterfactual image synthesis without structural drift.
- **⚠️ Limitations**: The method is strictly limited to medical image synthesis and lacks application to temporal consistency or dynamic environments required for embodied robotics tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07066)
- **👥 Authors**: Trong-Thang Pham, Loc Nguyen, Anh Nguyen, Hien Nguyen, Ngan Le
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 PathMem: Toward Cognition-Aligned Memory Transformation for Pathology MLLMs (Score: 3/10)
- **💡 Innovation**: The paper introduces a Memory Transformer architecture that dynamically retrieves and grounds structured pathology knowledge into a working memory for multimodal diagnostic reasoning.
- **⚠️ Limitations**: The work is strictly confined to the medical domain (computational pathology) and lacks any connection to physical agency, spatial reasoning, or embodied interaction.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09943v1)
- **👥 Authors**: Jinyue Li, Yuci Liang, Qiankun Li, Xinheng Lyu, Jiayu Qian, Huabao Chen, Kun Wang, Zhigang Zeng, Anil Anthony Bharath, Yang Liu
- **🏷️ Tags**: #Foundation_Model #LLM

---

### 📄 Influencing LLM Multi-Agent Dialogue via Policy-Parameterized Prompts (Score: 3/10)
- **💡 Innovation**: The paper introduces a framework that treats prompts as parameterized actions to influence multi-agent LLM dialogue dynamics without requiring additional model training.
- **⚠️ Limitations**: The work focuses exclusively on linguistic social simulation and lacks any connection to physical embodiment, sensorimotor control, or the specific challenges of robotic interaction.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09890v1)
- **👥 Authors**: Hongbo Bo, Jingyu Hu, Weiru Liu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Lost in Stories: Consistency Bugs in Long Story Generation by LLMs (Score: 3/10)
- **💡 Innovation**: The paper introduces a systematic benchmark (ConStory-Bench) and an automated detection pipeline (ConStory-Checker) to quantify and categorize narrative consistency errors in long-form LLM generation.
- **⚠️ Limitations**: The research is strictly confined to textual narrative consistency and lacks any connection to embodied reasoning, physical world grounding, or multi-modal state tracking relevant to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.05890)
- **👥 Authors**: Junjie Li, Xinrui Guo, Yuhao Wu, Roy Ka-Wei Lee, Hongzhi Li, Yutao Xie
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Breaking Training Bottlenecks: Effective and Stable Reinforcement Learning for Coding Models (Score: 3/10)
- **💡 Innovation**: The paper introduces MicroCoder-GRPO, an optimization framework for code generation models that utilizes conditional truncation masking and diversity-determined temperature selection to stabilize reinforcement learning training.
- **⚠️ Limitations**: The research is strictly focused on code generation and lacks any application, evaluation, or theoretical connection to embodied agents, physical environments, or multimodal action spaces.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07777)
- **👥 Authors**: Zongqian Li, Shaohan Huang, Zewen Chi, Yixuan Su, Lexin Zhou, Li Dong, Nigel Collier, Furu Wei
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Making LLMs Optimize Multi-Scenario CUDA Kernels Like Experts (Score: 3/10)
- **💡 Innovation**: The paper introduces a multi-agent, hardware-aware framework (CUDAMaster) and a comprehensive benchmark (MSKernelBench) for automating the optimization of diverse GPU kernels beyond standard machine learning operators.
- **⚠️ Limitations**: The work is strictly focused on high-performance computing and GPU kernel optimization, offering no direct contribution to embodied intelligence, robot control, or physical world interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07169)
- **👥 Authors**: Yuxuan Han, Meng-Hao Guo, Zhengning Liu, Wenguang Chen, Shi-Min Hu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Understanding the Use of a Large Language Model-Powered Guide to Make Virtual Reality Accessible for Blind and Low Vision People (Score: 2/10)
- **💡 Innovation**: The paper explores the social dynamics and human-computer interaction aspects of using an LLM-based virtual guide for accessibility in social VR environments.
- **⚠️ Limitations**: The study focuses on human-computer interaction and social psychology rather than technical advancements in robotics, embodied control, or perception.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09964v1)
- **👥 Authors**: Jazmin Collins, Sharon Y Lin, Tianqi Liu, Andrea Stevenson Won, Shiri Azenkot
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 SignalMC-MED: A Multimodal Benchmark for Evaluating Biosignal Foundation Models on Single-Lead ECG and PPG (Score: 2/10)
- **💡 Innovation**: The paper introduces a standardized benchmark (SignalMC-MED) for evaluating biosignal foundation models on synchronized, long-duration ECG and PPG data.
- **⚠️ Limitations**: The work is entirely focused on clinical biosignal analysis and lacks any connection to embodied agents, robot control, or physical interaction tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.09940v1)
- **👥 Authors**: Fredrik K. Gustafsson, Xiao Gu, Mattia Carletti, Patitapaban Palo, David W. Eyre, David A. Clifton
- **🏷️ Tags**: #Foundation_Model

---

### 📄 NLE: Non-autoregressive LLM-based ASR by Transcript Editing (Score: 2/10)
- **💡 Innovation**: The paper introduces a non-autoregressive approach to speech recognition by framing the task as conditional transcript editing using a bidirectional LLM.
- **⚠️ Limitations**: The work is entirely focused on speech processing and lacks any connection to embodied agents, multimodal action spaces, or physical world interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08397)
- **👥 Authors**: Avihu Dekel, Samuel Thomas, Takashi Fukada, George Saon
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Unlocking Data Value in Finance: A Study on Distillation and Difficulty-Aware Training (Score: 2/10)
- **💡 Innovation**: The paper introduces a data-centric framework for financial LLMs by utilizing multi-stage distillation and difficulty-aware sampling to optimize Chain-of-Thought supervision.
- **⚠️ Limitations**: The research is entirely focused on financial text processing and lacks any connection to physical agents, sensorimotor control, or embodied environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07223)
- **👥 Authors**: Chuxue Cao, Honglin Lin, Zhanping Zhong, Xin Gao, Mengzhang Cai, Conghui He, Sirui Han, Lijun Wu
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 OfficeQA Pro: An Enterprise Benchmark for End-to-End Grounded Reasoning (Score: 2/10)
- **💡 Innovation**: The paper introduces a specialized benchmark for long-context, multi-document analytical reasoning over historical financial corpora to test the limits of enterprise-grade LLM retrieval and parsing.
- **⚠️ Limitations**: The work is entirely focused on text-based document reasoning and lacks any connection to physical agents, sensorimotor control, or embodied environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08655)
- **👥 Authors**: Krista Opsahl-Ong, Arnav Singhvi, Jasmine Collins, Ivan Zhou, Cindy Wang, Ashutosh Baheti, Owen Oertell, Jacob Portes, Sam Havens, Erich Elsen, Michael Bendersky, Matei Zaharia, Xing Chen
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Retrieval-Augmented Generation for Predicting Cellular Responses to Gene Perturbation (Score: 2/10)
- **💡 Innovation**: The paper introduces a differentiable, cell-type-aware retrieval-augmented generation (RAG) framework specifically designed for predicting cellular responses to gene perturbations.
- **⚠️ Limitations**: The methodology is entirely focused on computational biology and genomics, lacking any intersection with physical agents, sensorimotor control, or embodied environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07233)
- **👥 Authors**: Andrea Giuseppe Di Francesco, Andrea Rubbi, Pietro Liò
- **🏷️ Tags**: #Foundation_Model #LLM

---


