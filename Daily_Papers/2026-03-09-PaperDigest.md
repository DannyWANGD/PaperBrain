# 📅 2026-03-09 - Paper Digest
## Summary
Total Papers: 34 | High Impact: 11

## 📝 Papers List
### 🔥 MetaWorld-X: Hierarchical World Modeling via VLM-Orchestrated Experts for Humanoid Loco-Manipulation (Score: 8/10)
- **💡 Innovation**: The paper introduces a hierarchical framework that uses a VLM-supervised Intelligent Routing Mechanism to dynamically compose specialized, human-prior-constrained expert policies for complex humanoid loco-manipulation.
- **⚠️ Limitations**: The reliance on a VLM for real-time routing may introduce significant latency bottlenecks, and the paper lacks explicit discussion on the computational overhead of maintaining multiple specialized expert policies in a single deployment.
- **🔗 Link**: [[MetaWorldX]]
- **👥 Authors**: Yutong Shen, Hangxu Liu, Penghui Liu, Jiashuo Luo, Yongkang Zhang, Rex Morvley, Chen Jiang, Jianwei Zhang, Lei Zhang
- **🏷️ Tags**: #Embodied_AI #Reinforcement_Learning #Robot_Manipulation #World_Model #LLM

---

### 🔥 Planning in 8 Tokens: A Compact Discrete Tokenizer for Latent World Model (Score: 8/10)
- **💡 Innovation**: The paper introduces a highly efficient discrete tokenizer that compresses visual observations into a minimal 8-token latent space, enabling real-time decision-time planning within a world model framework.
- **⚠️ Limitations**: The extreme compression to 8 tokens may lead to the loss of fine-grained spatial details or small object features necessary for complex, high-precision manipulation tasks.
- **🔗 Link**: [[Planning in 8 Tokens]]
- **👥 Authors**: Dongwon Kim, Gawon Seo, Jinsung Lee, Minsu Cho, Suha Kwak
- **🏷️ Tags**: #World_Model #Embodied_AI #Robot_Manipulation

---

### 🔥 RoboMME: Benchmarking and Understanding Memory for Robotic Generalist Policies (Score: 8/10)
- **💡 Innovation**: The paper introduces a systematic taxonomy and large-scale benchmark specifically designed to evaluate and compare memory mechanisms in VLA models for long-horizon, history-dependent robotic manipulation.
- **⚠️ Limitations**: The study focuses on variants of a single backbone (π0.5), which may limit the generalizability of the findings to other architectures like transformer-based diffusion policies or non-VLA approaches.
- **🔗 Link**: [[RoboMME]]
- **👥 Authors**: Yinpei Dai, Hongze Fu, Jayjun Lee, Yuejiang Liu, Haoran Zhang, Jianing Yang, Chelsea Finn, Nima Fazeli, Joyce Chai
- **🏷️ Tags**: #Robot_Manipulation #VLA #Embodied_AI #Foundation_Model

---

### 🔥 π-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs (Score: 8/10)
- **💡 Innovation**: The paper introduces a critic-and-likelihood-free framework for flow-based VLAs that enables online reinforcement learning via single-pass step-wise guidance, bypassing the computational intractability of multi-step sampling.
- **⚠️ Limitations**: The reliance on flow-based models may limit applicability to other popular VLA architectures (like autoregressive models), and the paper lacks explicit real-world hardware deployment results to validate the 'scalable for real-world' claim.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.02083)
- **👥 Authors**: Siting Wang, Xiaofeng Wang, Zheng Zhu, Minnan Pei, Xinyu Cui, Cheng Deng, Jian Zhao, Guan Huang, Haifeng Zhang, Jun Wang
- **🏷️ Tags**: #Robot_Manipulation #VLA #Reinforcement_Learning #Embodied_AI

---

### ✨ Embedding Classical Balance Control Principles in Reinforcement Learning for Humanoid Recovery (Score: 7/10)
- **💡 Innovation**: The paper introduces a hybrid approach that embeds classical control-theoretic balance metrics (capture point, centroidal momentum) into the reward function and critic architecture of a reinforcement learning framework to stabilize humanoid recovery.
- **⚠️ Limitations**: The reliance on privileged information (full state) during training and the lack of explicit generalization testing against highly dynamic, non-flat terrain or external object interactions limit the scope of the recovery behaviors.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08619v1)
- **👥 Authors**: Nehar Poddar, Stephen McCrory, Luigi Penco, Geoffrey Clark, Hakki Erhan Svil, Robert Griffin
- **🏷️ Tags**: #Reinforcement_Learning #Embodied_AI #Sim2Real

---

### ✨ Diff-Muscle: Efficient Learning for Musculoskeletal Robotic Table Tennis (Score: 7/10)
- **💡 Innovation**: The paper introduces a hierarchical framework that uses differential flatness to map high-dimensional, redundant musculoskeletal muscle-activation spaces into a lower-dimensional joint space for efficient reinforcement learning.
- **⚠️ Limitations**: The reliance on differential flatness may limit the framework's applicability to systems where the dynamics are not easily analytically invertible or where non-holonomic constraints are dominant.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08617v1)
- **👥 Authors**: Wentao Zhao, Jun Guo, Kangyao Huang, Xin Liu, Huaping Liu
- **🏷️ Tags**: #Embodied_AI #Reinforcement_Learning #Robot_Manipulation

---

### ✨ RetroAgent: From Solving to Evolving via Retrospective Dual Intrinsic Feedback (Score: 7/10)
- **💡 Innovation**: RetroAgent introduces a dual intrinsic feedback mechanism that combines numerical subtask tracking with a language-based memory buffer retrieved via a novel SimUtil-UCB strategy to facilitate continuous experiential learning in RL agents.
- **⚠️ Limitations**: The paper focuses on text-based or logic-heavy environments (ALFWorld, WebShop, Sokoban) rather than high-dimensional continuous control or physical robot manipulation, leaving the scalability to real-world embodied tasks unproven.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08561v1)
- **👥 Authors**: Xiaoying Zhang, Zichen Liu, Yipeng Zhang, Xia Hu, Wenqi Shao
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model #Embodied_AI

---

### ✨ Physical Simulator In-the-Loop Video Generation (Score: 7/10)
- **💡 Innovation**: The paper introduces a framework that enforces physical consistency in diffusion-based video generation by using a physical simulator to guide trajectory generation and employing test-time optimization for texture consistency.
- **⚠️ Limitations**: The reliance on 4D scene reconstruction and mesh initialization may limit the framework's scalability to complex, non-rigid, or highly cluttered environments compared to end-to-end generative approaches.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.06408)
- **👥 Authors**: Lin Geng Foo, Mark He Huang, Alexandros Lattas, Stylianos Moschoglou, Thabo Beeler, Christian Theobalt
- **🏷️ Tags**: #Diffusion_Model #World_Model #Embodied_AI

---

### ✨ WorldCache: Accelerating World Models for Free via Heterogeneous Token Caching (Score: 7/10)
- **💡 Innovation**: WorldCache introduces a curvature-guided caching mechanism that dynamically predicts token predictability and selectively recomputes only 'chaotic' tokens in diffusion-based world models to accelerate inference.
- **⚠️ Limitations**: The paper focuses primarily on inference speedup for world models and lacks a detailed evaluation of how these caching approximations impact long-horizon closed-loop policy performance in complex, high-degree-of-freedom robotic manipulation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.06331)
- **👥 Authors**: Weilun Feng, Guoxin Fan, Haotong Qin, Chuanguang Yang, Mingqiang Wu, Yuqi Li, Xiangqi Li, Zhulin An, Libo Huang, Dingrui Wang, Longlong Liao, Michele Magno, Yongjun Xu
- **🏷️ Tags**: #World_Model #Diffusion_Model #Embodied_AI

---

### ✨ Stabilizing Reinforcement Learning for Diffusion Language Models (Score: 7/10)
- **💡 Innovation**: The paper introduces StableDRL, a reformulation of GRPO that addresses reward collapse in diffusion-based language models by employing unconditional clipping and self-normalization to mitigate gradient instability caused by noisy likelihood estimates.
- **⚠️ Limitations**: The evaluation is primarily focused on language generation tasks, leaving the efficacy and stability of the proposed method in high-dimensional, continuous-action embodied control settings (e.g., robot manipulation) unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.06743)
- **👥 Authors**: Jianyuan Zhong, Kaibo Wang, Ding Ding, Zijin Feng, Haoli Bai, Yang Xiang, Jiacheng Sun, Qiang Xu
- **🏷️ Tags**: #Reinforcement_Learning #Diffusion_Model #LLM

---

### ✨ Physics Informed Viscous Value Representations (Score: 7/10)
- **💡 Innovation**: The paper introduces a physics-informed regularization for offline goal-conditioned RL by leveraging the viscosity solution of the HJB equation and the Feynman-Kac theorem to enable tractable Monte Carlo estimation of value functions.
- **⚠️ Limitations**: The evaluation focuses primarily on navigation and simulated manipulation, leaving the scalability and robustness of the approach in high-dimensional, real-world unstructured environments under-explored.
- **🔗 Link**: [[Physics Informed Viscous Value Representations]]
- **👥 Authors**: Hrishikesh Viswanath, Juanwu Lu, S. Talha Bukhari, Damon Conover, Ziran Wang, Aniket Bera
- **🏷️ Tags**: #Reinforcement_Learning #Robot_Manipulation #Embodied_AI

---

### ✨ Agentic Critical Training (Score: 6/10)
- **💡 Innovation**: The paper introduces a reinforcement learning paradigm that trains LLM agents to autonomously evaluate and reason about action quality through comparative judgment rather than imitating pre-written reflection text.
- **⚠️ Limitations**: The evaluation is restricted to general agentic benchmarks (e.g., web/tool use) and lacks empirical validation in physical embodied environments or robot manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08706v1)
- **👥 Authors**: Weize Liu, Minghui Liu, Sy-Tuyen Ho, Souradip Chakraborty, Xiyao Wang, Furong Huang
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Boosting MLLM Spatial Reasoning with Geometrically Referenced 3D Scene Representations (Score: 6/10)
- **💡 Innovation**: The paper introduces a zero-shot framework that encodes 3D geometric attributes as textual references indexed by unique object IDs, allowing MLLMs to perform 3D spatial reasoning without additional training.
- **⚠️ Limitations**: The approach relies on the accuracy of external 3D reconstruction or object detection pipelines to generate the geometric annotations, which may introduce error propagation in complex or cluttered real-world scenes.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08592v1)
- **👥 Authors**: Jiangye Yuan, Gowri Kumar, Baoyuan Wang
- **🏷️ Tags**: #LLM #Foundation_Model #Embodied_AI

---

### ✨ Towards Batch-to-Streaming Deep Reinforcement Learning for Continuous Control (Score: 6/10)
- **💡 Innovation**: The paper introduces Streaming Soft Actor-Critic (S2AC) and Streaming Deterministic Actor-Critic (SDAC), which bridge the gap between batch-based RL and online streaming updates to facilitate efficient on-device finetuning.
- **⚠️ Limitations**: The evaluation is limited to standard benchmarks, lacking a demonstration of the proposed algorithms on high-dimensional, real-world robotic manipulation tasks where streaming constraints are most critical.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08588v1)
- **👥 Authors**: Riccardo De Monte, Matteo Cederle, Gian Antonio Susto
- **🏷️ Tags**: #Reinforcement_Learning #Sim2Real #Embodied_AI

---

### ✨ Penguin-VL: Exploring the Efficiency Limits of VLM with LLM-based Vision Encoders (Score: 6/10)
- **💡 Innovation**: The paper introduces a vision encoder initialized from a text-only LLM rather than contrastive pretraining (CLIP/SigLIP) to preserve fine-grained visual cues for more efficient multimodal reasoning.
- **⚠️ Limitations**: The evaluation focuses primarily on static image and video benchmarks, lacking direct validation in closed-loop robotic control or embodied action-prediction tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.06569)
- **👥 Authors**: Boqiang Zhang, Lei Ke, Ruihan Yang, Qi Gao, Tianyuan Qu, Rossell Chen, Dong Yu, Leoweiliang
- **🏷️ Tags**: #Foundation_Model #LLM #VLA

---

### ✨ BandPO: Bridging Trust Regions and Ratio Clipping via Probability-Aware Bounds for LLM Reinforcement Learning (Score: 6/10)
- **💡 Innovation**: The paper introduces BandPO, a novel policy optimization framework that replaces fixed PPO clipping with dynamic, probability-aware bounds derived from f-divergence projections to prevent entropy collapse in LLM fine-tuning.
- **⚠️ Limitations**: The evaluation is restricted to LLM alignment tasks, leaving the effectiveness of this optimization technique in high-dimensional, continuous action spaces typical of Embodied AI and robot manipulation unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.04918)
- **👥 Authors**: Yuan Li, Bo Wang, Yufei Gao, Yuqian Yao, Xinyuan Wang, Zhangyue Yin, Xipeng Qiu
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ HiAR: Efficient Autoregressive Long Video Generation via Hierarchical Denoising (Score: 5/10)
- **💡 Innovation**: HiAR introduces a hierarchical denoising framework that performs causal generation across all video blocks simultaneously at each denoising step, ensuring context and target frames share the same noise level to mitigate error accumulation.
- **⚠️ Limitations**: The paper focuses exclusively on open-loop video generation benchmarks (VBench) and lacks evaluation on closed-loop embodied tasks or control-based downstream applications.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08703v1)
- **👥 Authors**: Kai Zou, Dian Zheng, Hongbo Liu, Tiankai Hang, Bin Liu, Nenghai Yu
- **🏷️ Tags**: #Diffusion_Model #World_Model

---

### ✨ How Far Can Unsupervised RLVR Scale LLM Training? (Score: 5/10)
- **💡 Innovation**: The paper provides a unified theoretical framework for Unsupervised Reinforcement Learning with Verifiable Rewards (URLVR), identifying that intrinsic reward methods are fundamentally limited by the alignment between a model's initial confidence and its correctness.
- **⚠️ Limitations**: The study focuses exclusively on text-based LLM training dynamics, leaving the applicability of these scaling limits and the 'Model Collapse Step' metric to embodied agents or VLA models unverified.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08660v1)
- **👥 Authors**: Bingxiang He, Yuxin Zuo, Zeyuan Liu, Shangziqi Zhao, Zixuan Fu, Junlin Yang, Cheng Qian, Kaiyan Zhang, Yuchen Fan, Ganqu Cui, Xiusi Chen, Youbang Sun, Xingtai Lv, Xuekai Zhu, Li Sheng, Ran Li, Huan-ang Gao, Yuchen Zhang, Bowen Zhou, Zhiyuan Liu, Ning Ding
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ UNBOX: Unveiling Black-box visual models with Natural-language (Score: 5/10)
- **💡 Innovation**: UNBOX introduces a black-box interpretability framework that uses LLMs and diffusion models to perform semantic activation maximization without requiring gradient or internal model access.
- **⚠️ Limitations**: The method relies on the semantic alignment between the diffusion model's generation space and the target model's decision boundaries, which may fail for highly specialized or non-semantic visual domains.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08639v1)
- **👥 Authors**: Simone Carnemolla, Chiara Russo, Simone Palazzo, Quentin Bouniot, Daniela Giordano, Zeynep Akata, Matteo Pennisi, Concetto Spampinato
- **🏷️ Tags**: #LLM #Diffusion_Model #Foundation_Model

---

### ✨ FOMO-3D: Using Vision Foundation Models for Long-Tailed 3D Object Detection (Score: 5/10)
- **💡 Innovation**: The paper introduces a two-stage 3D detection framework that integrates semantic and depth priors from pre-trained vision foundation models (OWLv2 and Metric3Dv2) to improve long-tailed object detection in autonomous driving.
- **⚠️ Limitations**: The approach relies on heavy multi-modal fusion and external foundation models, which may introduce significant latency and computational overhead that could hinder real-time deployment in safety-critical robotics applications.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08611v1)
- **👥 Authors**: Anqi Joyce Yang, James Tu, Nikita Dvornik, Enxu Li, Raquel Urtasun
- **🏷️ Tags**: #Foundation_Model #Embodied_AI

---

### ✨ nabla-Reasoner: LLM Reasoning via Test-Time Gradient Descent in Latent Space (Score: 5/10)
- **💡 Innovation**: The paper introduces Differentiable Textual Optimization (DTO), which replaces discrete search algorithms with first-order gradient-based optimization in the latent space of LLMs during inference.
- **⚠️ Limitations**: The approach is currently validated only on mathematical reasoning benchmarks and lacks evaluation in embodied or multi-modal settings, where gradient-based optimization might face challenges with non-differentiable environment feedback.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.04948)
- **👥 Authors**: Peihao Wang, Ruisi Cai, Zhen Wang, Hongyuan Mei, Qiang Liu, Pan Li, Zhangyang Wang
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ IF-RewardBench: Benchmarking Judge Models for Instruction-Following Evaluation (Score: 5/10)
- **💡 Innovation**: The paper introduces a listwise evaluation paradigm using preference graphs to better assess judge model performance in instruction-following compared to traditional pairwise comparisons.
- **⚠️ Limitations**: The benchmark is strictly focused on text-based instruction-following and lacks evaluation metrics for multimodal or embodied constraints relevant to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.04738)
- **👥 Authors**: Bosi Wen, Yilin Niu, Cunxiang Wang, Xiaoying Ling, Ying Zhang, Pei Ke, Hongning Wang, Minlie Huang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Making Reconstruction FID Predictive of Diffusion Generation FID (Score: 5/10)
- **💡 Innovation**: The paper introduces 'interpolated FID' (iFID), a metric that bridges the gap between reconstruction quality and generative performance by interpolating latent representations to better predict diffusion model generation quality.
- **⚠️ Limitations**: The work focuses exclusively on image generation benchmarks and lacks validation in embodied settings or complex action-conditioned diffusion models common in robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.05630)
- **👥 Authors**: Tongda Xu, Mingwei He, Shady Abu-Hussein, Jose Miguel Hernandez-Lobato, Haotian Zhang, Kai Zhao, Chao Zhou, Ya-Qin Zhang, Yan Wang
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 Scale Space Diffusion (Score: 4/10)
- **💡 Innovation**: The paper introduces a diffusion framework that replaces standard Gaussian noise with scale-space downsampling, allowing the model to perform denoising at lower resolutions to improve computational efficiency.
- **⚠️ Limitations**: The evaluation is restricted to static image generation tasks (CelebA, ImageNet) without demonstrating applicability to high-dimensional embodied control or temporal consistency required for robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08709v1)
- **👥 Authors**: Soumik Mukhopadhyay, Prateksha Udhayanan, Abhinav Shrivastava
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 PostTrainBench: Can LLM Agents Automate LLM Post-Training? (Score: 4/10)
- **💡 Innovation**: The paper introduces a benchmark to evaluate the capability of autonomous LLM agents to perform the end-to-end post-training pipeline, including data curation and experiment management.
- **⚠️ Limitations**: The study focuses exclusively on text-based model optimization and lacks any connection to embodied agents, physical environment interaction, or multi-modal training pipelines.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08640v1)
- **👥 Authors**: Ben Rank, Hardik Bhatnagar, Ameya Prabhu, Shira Eisenberg, Karina Nguyen, Matthias Bethge, Maksym Andriushchenko
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Impact of Connectivity on Laplacian Representations in Reinforcement Learning (Score: 4/10)
- **💡 Innovation**: The paper provides a theoretical grounding for Laplacian-based state representation learning by bounding approximation error as a function of the algebraic connectivity of the state-graph.
- **⚠️ Limitations**: The work is limited to theoretical analysis and simple gridworld simulations, lacking empirical validation in high-dimensional, continuous, or real-world robotic environments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08558v1)
- **👥 Authors**: Tommaso Giorgi, Pierriccardo Olivieri, Keyue Jiang, Laura Toni, Matteo Papini
- **🏷️ Tags**: #Reinforcement_Learning

---

### 📄 HiMAP-Travel: Hierarchical Multi-Agent Planning for Long-Horizon Constrained Travel (Score: 4/10)
- **💡 Innovation**: The paper introduces a hierarchical multi-agent framework that utilizes a transactional monitor and a bargaining protocol to enforce global constraints in long-horizon planning tasks.
- **⚠️ Limitations**: The work is strictly focused on symbolic/text-based travel planning and lacks any grounding in physical environments, sensorimotor control, or embodied interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.04750)
- **👥 Authors**: The Viet Bui, Wenjun Li, Yong Liu
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 Mario: Multimodal Graph Reasoning with Large Language Models (Score: 4/10)
- **💡 Innovation**: The paper introduces a graph-conditioned VLM framework that uses cross-modal contrastive learning and a learnable modality router to perform reasoning over heterogeneous multimodal graphs.
- **⚠️ Limitations**: The work focuses on abstract graph reasoning tasks (node classification/link prediction) rather than embodied control, spatial grounding, or temporal dynamics required for robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.05181)
- **👥 Authors**: Yuanfu Sun, Kang Li, Pengkang Guo, Jiajin Liu, Qiaoyu Tan
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey (Score: 4/10)
- **💡 Innovation**: The paper provides a systematic taxonomy and conceptual framework for dynamic routing and cascading across multiple independently trained LLMs to optimize inference efficiency.
- **⚠️ Limitations**: The survey focuses exclusively on text-based LLM routing and lacks discussion on the specific challenges of routing in multimodal or embodied contexts, such as VLA inference or real-time robotic control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.04445)
- **👥 Authors**: Yasmin Moslem, John D. Kelleher
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Layer by layer, module by module: Choose both for optimal OOD probing of ViT (Score: 4/10)
- **💡 Innovation**: The paper identifies that probing specific internal components of Vision Transformers (feedforward networks vs. attention modules) yields superior performance under varying degrees of distribution shift compared to standard block-output probing.
- **⚠️ Limitations**: The study is restricted to static image classification benchmarks and lacks evaluation on embodied tasks or dynamic visual-motor control scenarios relevant to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.05280)
- **👥 Authors**: Ambroise Odonnat, Vasilii Feofanov, Laetitia Chapel, Romain Tavenard, Ievgen Redko
- **🏷️ Tags**: #Foundation_Model

---

### 📄 Impermanent: A Live Benchmark for Temporal Generalization in Time Series Forecasting (Score: 3/10)
- **💡 Innovation**: The paper introduces a live, non-stationary benchmark for time-series forecasting that mitigates data contamination by evaluating models on continuously updated, real-world GitHub activity streams.
- **⚠️ Limitations**: The benchmark is entirely focused on time-series forecasting of software repository metadata, which lacks direct applicability to the physical dynamics, multi-modal sensor fusion, or decision-making challenges inherent in embodied robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08707v1)
- **👥 Authors**: Azul Garza, Renée Rosillo, Rodrigo Mendoza-Smith, David Salinas, Andrew Robert Williams, Arjun Ashok, Mononito Goswami, José Martín Juárez
- **🏷️ Tags**: #Foundation_Model

---

### 📄 Censored LLMs as a Natural Testbed for Secret Knowledge Elicitation (Score: 3/10)
- **💡 Innovation**: The paper proposes using politically censored LLMs as a naturalistic testbed for evaluating honesty elicitation and lie detection techniques, rather than relying on synthetic datasets.
- **⚠️ Limitations**: The research is entirely focused on text-based safety and alignment, offering no direct contributions to embodied intelligence, sensorimotor control, or world modeling.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.05494)
- **👥 Authors**: Helena Casademunt, Bartosz Cywiński, Khoi Tran, Arya Jakkli, Samuel Marks, Neel Nanda
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 OfficeQA Pro: An Enterprise Benchmark for End-to-End Grounded Reasoning (Score: 2/10)
- **💡 Innovation**: The paper introduces a specialized benchmark for long-context, multi-document analytical reasoning over historical financial corpora to test the limits of enterprise-grade LLM retrieval and parsing.
- **⚠️ Limitations**: The work is entirely focused on textual and tabular data processing, offering no contribution to physical interaction, spatial reasoning, or embodied control tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08655v1)
- **👥 Authors**: Krista Opsahl-Ong, Arnav Singhvi, Jasmine Collins, Ivan Zhou, Cindy Wang, Ashutosh Baheti, Owen Oertell, Jacob Portes, Sam Havens, Erich Elsen, Michael Bendersky, Matei Zaharia, Xing Chen
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Evaluating Financial Intelligence in Large Language Models: Benchmarking SuperInvesting AI with LLM Engines (Score: 1/10)
- **💡 Innovation**: The paper introduces a domain-specific benchmark (AFIB) to evaluate the financial reasoning and analytical capabilities of various large language models.
- **⚠️ Limitations**: The research is entirely focused on financial NLP and lacks any connection to physical agents, robotics, or embodied perception.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.08704v1)
- **👥 Authors**: Akshay Gulati, Kanha Singhania, Tushar Banga, Parth Arora, Anshul Verma, Vaibhav Kumar Singh, Agyapal Digra, Jayant Singh Bisht, Danish Sharma, Varun Singla, Shubh Garg
- **🏷️ Tags**: #LLM #Foundation_Model

---


