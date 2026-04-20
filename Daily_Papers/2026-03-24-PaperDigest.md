# 📅 2026-03-24 - Paper Digest
## Summary
Total Papers: 48 | High Impact: 20

## 📝 Papers List
### 🔥 WildWorld: A Large-Scale Dataset for Dynamic World Modeling with Actions and Explicit State toward Generative ARPG (Score: 8/10)
- **💡 Innovation**: The paper introduces a large-scale, action-conditioned dataset from a AAA game engine that provides explicit state annotations (skeletons, depth, camera poses) to decouple action-driven dynamics from pixel-level changes.
- **⚠️ Limitations**: The dataset is derived from a specific game environment, which may introduce domain-specific biases that limit direct transferability to real-world robotic systems.
- **🔗 Link**: [[WildWorld]]
- **👥 Authors**: Zhen Li, Zian Meng, Shuwei Shi, Wenshuo Peng, Yuwei Wu, Bo Zheng, Chuanhao Li, Kaipeng Zhang
- **🏷️ Tags**: #World_Model #Embodied_AI #Reinforcement_Learning

---

### 🔥 VTAM: Video-Tactile-Action Models for Complex Physical Interaction Beyond VLAs (Score: 8/10)
- **💡 Innovation**: VTAM integrates tactile feedback into a video-action world model via a lightweight modality transfer finetuning and a tactile regularization loss to prevent visual latent dominance.
- **⚠️ Limitations**: The reliance on a pretrained video transformer may inherit visual biases, and the paper does not explicitly detail the scalability of the tactile sensor integration across different hardware platforms.
- **🔗 Link**: [[VTAM]]
- **👥 Authors**: Haoran Yuan, Weigang Yi, Zhenyu Zhang, Wendi Chen, Yuchen Mo, Jiashi Yin, Xinzhuo Li, Xiangyu Zeng, Chuan Wen, Cewu Lu, Katherine Driggs-Campbell, Ismini Lourentzou
- **🏷️ Tags**: #Robot_Manipulation #World_Model #Embodied_AI #Foundation_Model

---

### 🔥 SIMART: Decomposing Monolithic Meshes into Sim-ready Articulated Assets via MLLM (Score: 8/10)
- **💡 Innovation**: SIMART introduces a Sparse 3D VQ-VAE within a unified MLLM architecture to perform joint part-level decomposition and kinematic prediction, significantly reducing token overhead for articulated 3D asset generation.
- **⚠️ Limitations**: The reliance on MLLM-based generation may still struggle with complex topological constraints or high-precision kinematic joints required for specific robotic manipulation tasks.
- **🔗 Link**: [[SIMART]]
- **👥 Authors**: Chuanrui Zhang, Minghan Qin, Yuang Wang, Baifeng Xie, Hang Li, Ziwei Wang
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #LLM

---

### 🔥 ABot-PhysWorld: Interactive World Foundation Model for Robotic Manipulation with Physics Alignment (Score: 8/10)
- **💡 Innovation**: The model utilizes a DPO-based post-training framework with decoupled discriminators to enforce physical constraints on a 14B Diffusion Transformer architecture.
- **⚠️ Limitations**: The reliance on a curated dataset for physics-aware annotation may limit generalization to novel, out-of-distribution physical interactions not captured in the training set.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23376v1)
- **👥 Authors**: Yuzhi Chen, Ronghan Chen, Dongjie Huo, Yandan Yang, Dekang Qi, Haoyun Liu, Tong Lin, Shuang Zeng, Junjin Xiao, Xinyuan Chang, Feng Xiong, Xing Wei, Zhiheng Ma, Mu Xu
- **🏷️ Tags**: #World_Model #Diffusion_Model #Embodied_AI #Robot_Manipulation #Foundation_Model

---

### 🔥 Omni-WorldBench: Towards a Comprehensive Interaction-Centric Evaluation for World Models (Score: 8/10)
- **💡 Innovation**: The paper introduces a 4D interaction-centric evaluation framework that quantifies world model performance by measuring the causal impact of actions on state transitions rather than just visual fidelity.
- **⚠️ Limitations**: The benchmark's reliance on agent-based evaluation may introduce bias depending on the quality and generalization capabilities of the underlying agent used for assessment.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22212)
- **👥 Authors**: Meiqi Wu, Zhixin Cai, Fufangchen Zhao, Xiaokun Feng, Rujing Dang, Bingze Song, Ruitian Tian, Jiashu Zhu, Jiachen Lei, Hao Dou, Jing Tang, Lei Sun, Jiahong Wu, Xiangxiang Chu, Zeming Liu, Kaiqi Huang
- **🏷️ Tags**: #World_Model #Embodied_AI #Robot_Manipulation

---

### 🔥 RoboAlign: Learning Test-Time Reasoning for Language-Action Alignment in Vision-Language-Action Models (Score: 8/10)
- **💡 Innovation**: RoboAlign introduces a test-time reasoning framework that uses reinforcement learning to align language-based reasoning with low-level action tokens in diffusion-based VLA models.
- **⚠️ Limitations**: The reliance on a diffusion-based action head may introduce significant inference latency, and the paper does not detail the computational overhead of the RL-based alignment process.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.21341)
- **👥 Authors**: Dongyoung Kim, Sumin Park, Woomin Song, Seungku Kim, Taeyoung Kim, Huiwon Jang, Jinwoo Shin, Jaehyung Kim, Younggyo Seo
- **🏷️ Tags**: #VLA #Reinforcement_Learning #Diffusion_Model #Robot_Manipulation #Embodied_AI

---

### 🔥 WorldCache: Content-Aware Caching for Accelerated Video World Models (Score: 8/10)
- **💡 Innovation**: WorldCache introduces a perception-constrained caching framework that utilizes motion-adaptive thresholds and saliency-weighted drift estimation to enable training-free, artifact-aware feature reuse in Diffusion Transformers.
- **⚠️ Limitations**: The method is evaluated primarily on video generation benchmarks rather than closed-loop embodied control tasks, leaving its performance in high-frequency robotic decision-making cycles unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22286)
- **👥 Authors**: Umair Nawaz, Ahmed Heakl, Ufaq Khan, Abdelrahman Shaker, Salman Khan, Fahad Shahbaz Khan
- **🏷️ Tags**: #World_Model #Diffusion_Model #Foundation_Model

---

### 🔥 Understanding Behavior Cloning with Action Quantization (Score: 8/10)
- **💡 Innovation**: The paper provides a formal theoretical framework for action quantization in autoregressive behavior cloning, establishing optimal sample complexity bounds and polynomial horizon error propagation.
- **⚠️ Limitations**: The analysis relies on specific assumptions regarding dynamics stability and probabilistic policy smoothness, which may not hold in complex, non-linear robotic manipulation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.20538)
- **👥 Authors**: Haoqun Cao, Tengyang Xie
- **🏷️ Tags**: #VLA #Embodied_AI #Robot_Manipulation #Foundation_Model

---

### ✨ OccAny: Generalized Unconstrained Urban 3D Occupancy (Score: 7/10)
- **💡 Innovation**: OccAny introduces a generalized 3D occupancy framework that utilizes segmentation-forced feature learning and test-time novel-view rendering to achieve metric geometry completion in uncalibrated, out-of-domain urban scenes.
- **⚠️ Limitations**: The reliance on segmentation-based forcing and novel-view rendering may introduce significant computational overhead during inference, potentially hindering real-time performance in dynamic robotic applications.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23502v1)
- **👥 Authors**: Anh-Quan Cao, Tuan-Hung Vu
- **🏷️ Tags**: #Embodied_AI #Foundation_Model

---

### ✨ VISion On Request: Enhanced VLLM efficiency with sparse, dynamically selected, vision-language interactions (Score: 7/10)
- **💡 Innovation**: VISOR introduces a dynamic computation mechanism that sparsifies cross-attention interactions between text and high-resolution visual tokens rather than compressing the visual input itself.
- **⚠️ Limitations**: The method relies on a lightweight policy mechanism for dynamic allocation, which may introduce overhead or latency jitter in real-time embodied control loops.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23495v1)
- **👥 Authors**: Adrian Bulat, Alberto Baldrati, Ioannis Maniadis Metaxas, Yassine Ouali, Georgios Tzimiropoulos
- **🏷️ Tags**: #VLA #Foundation_Model #LLM

---

### ✨ SpecEyes: Accelerating Agentic Multimodal LLMs via Speculative Perception and Planning (Score: 7/10)
- **💡 Innovation**: SpecEyes implements a speculative execution framework for agentic MLLMs by using a lightweight model to predict tool-use trajectories and a cognitive gating mechanism for self-verification.
- **⚠️ Limitations**: The reliance on a lightweight speculative model may introduce failure modes in complex, long-horizon tasks where the small model lacks the reasoning depth to accurately predict tool-chain outcomes.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23483v1)
- **👥 Authors**: Haoyu Huang, Jinfa Huang, Zhongwei Wan, Xiawu Zheng, Rongrong Ji, Jiebo Luo
- **🏷️ Tags**: #Foundation_Model #LLM #Embodied_AI

---

### ✨ Off-Policy Value-Based Reinforcement Learning for Large Language Models (Score: 7/10)
- **💡 Innovation**: ReVal introduces a value-based, off-policy reinforcement learning framework for LLMs that utilizes Bellman updates and replay buffers to enable sample-efficient training compared to standard on-policy methods like GRPO.
- **⚠️ Limitations**: The approach is currently validated primarily on mathematical reasoning benchmarks, leaving its scalability and stability in more complex, multi-modal, or embodied decision-making environments unproven.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23355v1)
- **👥 Authors**: Peng-Yuan Wang, Ziniu Li, Tian Xu, Bohan Yang, Tian-Shuo Liu, ChenYang Wang, Xiong-Hui Chen, Yi-Chen Li, Tianyun Yang, Congliang Chen, Yang Yu
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Repurposing Geometric Foundation Models for Multi-view Diffusion (Score: 7/10)
- **💡 Innovation**: The paper introduces Geometric Latent Diffusion (GLD), which utilizes the geometrically consistent feature space of pre-trained geometric foundation models as a latent representation for multi-view diffusion, bypassing the need for view-independent VAEs.
- **⚠️ Limitations**: The approach relies on the quality of the underlying geometric foundation model and lacks explicit evaluation on downstream embodied tasks or real-world robotic sensor data.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22275)
- **👥 Authors**: Wooseok Jang, Seonghu Jeon, Jisang Han, Jinhyeok Choi, Minkyung Kwon, Seungryong Kim, Saining Xie, Sainan Liu
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #World_Model

---

### ✨ Group3D: MLLM-Driven Semantic Grouping for Open-Vocabulary 3D Object Detection (Score: 7/10)
- **💡 Innovation**: Group3D introduces a semantically gated merging mechanism that incorporates MLLM-derived scene-adaptive vocabulary to constrain 3D instance construction, preventing geometry-only over-merging.
- **⚠️ Limitations**: The reliance on MLLM-driven semantic grouping may introduce significant latency, potentially hindering real-time performance in dynamic robotic environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.21944)
- **👥 Authors**: Youbin Kim, Jinho Park, Hogun Park, Eunbyung Park
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #LLM

---

### ✨ On the Direction of RLVR Updates for LLM Reasoning: Identification and Exploitation (Score: 7/10)
- **💡 Innovation**: The paper introduces a directional analysis of RLVR updates using token-level log probability differences to identify and amplify reasoning-critical policy shifts.
- **⚠️ Limitations**: The proposed methods are evaluated primarily on text-based reasoning benchmarks, leaving the transferability of these directional update insights to multimodal or embodied policy optimization unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22117)
- **👥 Authors**: Kexin Huang, Haoming Meng, Junkang Wu, Jinda Lu, Chiyu Ma, Ziqian Chen, Xue Wang, Bolin Ding, Jiancan Wu, Xiang Wang, Xiangnan He, Guoyin Wang, Jingren Zhou
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ PivotRL: High Accuracy Agentic Post-Training at Low Compute Cost (Score: 7/10)
- **💡 Innovation**: PivotRL optimizes agentic post-training by filtering for high-variance 'pivot' states in local on-policy rollouts and utilizing functional-equivalence rewards to improve generalization without full E2E RL compute overhead.
- **⚠️ Limitations**: The reliance on existing SFT trajectories may limit the framework's ability to discover novel exploration strategies outside the initial demonstration distribution.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.21383)
- **👥 Authors**: Junkeun Yi, Damon Mosk-Aoyama, Baihe Huang, Ritu Gala, Charles Wang, Sugam Dipak Devare, Khushi Bhardwaj, Abhibha Gupta, Oleksii Kuchaiev, Jiantao Jiao, Jian Zhang, Venkat Srinivasan
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Perceptio: Perception Enhanced Vision Language Models via Spatial Token Generation (Score: 7/10)
- **💡 Innovation**: Perceptio integrates explicit semantic segmentation and VQ-VAE-based depth tokens into the autoregressive LLM sequence to force spatial reasoning before textual output.
- **⚠️ Limitations**: The approach relies on heavy teacher-distillation and multi-task co-training, which may introduce significant computational overhead and latency during inference.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.18795)
- **👥 Authors**: Yuchen Li, Amanmeet Garg, Shalini Chaudhuri, Rui Zhao, Garin Kessler
- **🏷️ Tags**: #Foundation_Model #LLM #Embodied_AI

---

### ✨ Demystifying Reinforcement Learning for Long-Horizon Tool-Using Agents: A Comprehensive Recipe (Score: 7/10)
- **💡 Innovation**: The paper provides a systematic empirical decomposition of the RL design space for long-horizon agentic planning, identifying scale-dependent optimal configurations for reward shaping and data composition.
- **⚠️ Limitations**: The findings are derived exclusively from the TravelPlanner benchmark, which focuses on symbolic tool orchestration rather than the continuous control or physical interaction dynamics typical of embodied robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.21972)
- **👥 Authors**: Xixi Wu, Qianguo Sun, Ruiyang Zhang, Chao Song, Junlong Wu, Yiyan Qi, Hong Cheng
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Safe Flow Q-Learning: Offline Safe Reinforcement Learning with Reachability-Based Flow Policies (Score: 7/10)
- **💡 Innovation**: SafeFQL integrates Hamilton-Jacobi reachability-based safety value functions with flow-based policy distillation to enable real-time, constraint-satisfying action selection without iterative sampling.
- **⚠️ Limitations**: The reliance on offline datasets for safety boundary estimation may lead to poor generalization in out-of-distribution scenarios despite the conformal prediction calibration.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15136)
- **👥 Authors**: Mumuksh Tayal, Manan Tayal, Ravi Prakash
- **🏷️ Tags**: #Reinforcement_Learning #Embodied_AI #Sim2Real

---

### ✨ FluidWorld: Reaction-Diffusion Dynamics as a Predictive Substrate for World Models (Score: 7/10)
- **💡 Innovation**: FluidWorld replaces standard Transformer-based latent predictors with reaction-diffusion partial differential equations to achieve O(N) spatial complexity and improved multi-step temporal coherence.
- **⚠️ Limitations**: The evaluation is currently limited to unconditional video prediction on a small-scale dataset (UCF-101), leaving the scalability to complex, high-dimensional embodied environments unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.21315)
- **👥 Authors**: Fabien Polly
- **🏷️ Tags**: #World_Model #Diffusion_Model #Embodied_AI

---

### ✨ UniGRPO: Unified Policy Optimization for Reasoning-Driven Visual Generation (Score: 6/10)
- **💡 Innovation**: UniGRPO introduces a unified reinforcement learning framework that applies GRPO to both text reasoning and flow-matching-based image synthesis by replacing classifier-free guidance with linear rollouts and utilizing velocity-field MSE penalties.
- **⚠️ Limitations**: The framework is currently validated only on single-round reasoning-driven image generation, lacking empirical evidence for its scalability to complex, multi-turn interleaved generation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23500v1)
- **👥 Authors**: Jie Liu, Zilyu Ye, Linxiao Yuan, Shenhan Zhu, Yu Gao, Jie Wu, Kunchang Li, Xionghui Wang, Xiaonan Nie, Weilin Huang, Wanli Ouyang
- **🏷️ Tags**: #Reinforcement_Learning #Diffusion_Model #Foundation_Model #LLM

---

### ✨ DA-Flow: Degradation-Aware Optical Flow Estimation with Diffusion Models (Score: 6/10)
- **💡 Innovation**: The method leverages intermediate representations from image restoration diffusion models, augmented with spatio-temporal attention, to improve optical flow estimation under severe real-world degradations.
- **⚠️ Limitations**: The reliance on iterative refinement and diffusion-based feature extraction likely imposes significant computational overhead, potentially hindering real-time performance in robotics applications.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23499v1)
- **👥 Authors**: Jaewon Min, Jaeeun Lee, Yeji Choi, Paul Hyunbin Cho, Jin Hyeon Kim, Tae-Young Lee, Jongsik Ahn, Hwayeong Lee, Seonghyun Park, Seungryong Kim
- **🏷️ Tags**: #Diffusion_Model #Sim2Real

---

### ✨ AgentRVOS: Reasoning over Object Tracks for Zero-Shot Referring Video Object Segmentation (Score: 6/10)
- **💡 Innovation**: The method introduces an agentic pipeline that reverses the traditional RVOS workflow by performing object-level spatio-temporal tracking via SAM3 before applying MLLM-based semantic reasoning.
- **⚠️ Limitations**: The approach relies on the pre-existence of high-quality mask tracks from SAM3, which may fail in highly cluttered or occluded dynamic environments where object identity is ambiguous.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23489v1)
- **👥 Authors**: Woojeong Jin, Jaeho Lee, Heeseong Shin, Seungho Jang, Junhwan Heo, Seungryong Kim
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ RealMaster: Lifting Rendered Scenes into Photorealistic Video (Score: 6/10)
- **💡 Innovation**: RealMaster utilizes an anchor-based propagation strategy to generate paired synthetic-to-photorealistic training data, which is then distilled into an IC-LoRA for consistent video-to-video translation.
- **⚠️ Limitations**: The method relies on pre-existing 3D engine control and geometric cues, potentially struggling with complex dynamic occlusions or non-rigid deformations not captured by the initial rendering.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23462v1)
- **👥 Authors**: Dana Cohen-Bar, Ido Sobol, Raphael Bensadoun, Shelly Sheynin, Oran Gafni, Or Patashnik, Daniel Cohen-Or, Amit Zohar
- **🏷️ Tags**: #Diffusion_Model #Sim2Real

---

### ✨ DetPO: In-Context Learning with Multi-Modal LLMs for Few-Shot Object Detection (Score: 6/10)
- **💡 Innovation**: DetPO introduces a gradient-free, test-time prompt optimization framework that iteratively refines text-only prompts to maximize few-shot object detection accuracy in black-box MLLMs.
- **⚠️ Limitations**: The approach relies on iterative API calls for optimization, which may introduce significant latency and cost overhead during inference compared to fine-tuned or zero-shot methods.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23455v1)
- **👥 Authors**: Gautam Rajendrakumar Gare, Neehar Peri, Matvei Popov, Shruti Jain, John Galeotti, Deva Ramanan
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ 3DCity-LLM: Empowering Multi-modality Large Language Models for 3D City-scale Perception and Understanding (Score: 6/10)
- **💡 Innovation**: The framework introduces a coarse-to-fine feature encoding strategy that parallelizes target object, inter-object relationship, and global scene representations for city-scale 3D understanding.
- **⚠️ Limitations**: The approach focuses primarily on static perception and scene understanding rather than dynamic agent interaction or closed-loop control required for embodied robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23447v1)
- **👥 Authors**: Yiping Chen, Jinpeng Li, Wenyu Ke, Yang Luo, Jie Ouyang, Zhongjie He, Li Liu, Hongchao Fan, Hao Wu
- **🏷️ Tags**: #Foundation_Model #LLM #Embodied_AI

---

### ✨ SortedRL: Accelerating RL Training for LLMs through Online Length-Aware Scheduling (Score: 6/10)
- **💡 Innovation**: SortedRL introduces an online length-aware scheduling strategy that reorders rollout samples to minimize synchronization overhead and enable near on-policy micro-curriculum construction during LLM reinforcement learning.
- **⚠️ Limitations**: The method is specifically optimized for text-based autoregressive generation and does not address the distinct latency or stochasticity challenges inherent in embodied robotics environments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23414v1)
- **👥 Authors**: Yiqi Zhang, Huiqiang Jiang, Xufang Luo, Zhihe Yang, Chengruidong Zhang, Yifei Shen, Dongsheng Li, Yuqing Yang, Lili Qiu, Yang You
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Unleashing Spatial Reasoning in Multimodal Large Language Models via Textual Representation Guided Reasoning (Score: 6/10)
- **💡 Innovation**: The paper introduces TRACE, a prompting framework that forces MLLMs to generate structured text-based spatial abstractions of egocentric video to improve 3D reasoning capabilities.
- **⚠️ Limitations**: The approach relies on textual intermediate reasoning traces rather than grounding spatial information directly into the model's latent space or visual features, potentially limiting its utility for real-time control.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23404v1)
- **👥 Authors**: Jiacheng Hua, Yishu Yin, Yuhang Wu, Tai Wang, Yifei Huang, Miao Liu
- **🏷️ Tags**: #Foundation_Model #LLM #Embodied_AI

---

### ✨ VideoDetective: Clue Hunting via both Extrinsic Query and Intrinsic Relevance for Long Video Understanding (Score: 6/10)
- **💡 Innovation**: The framework utilizes a Hypothesis-Verification-Refinement loop combined with a visual-temporal affinity graph to propagate query relevance across long-form video segments.
- **⚠️ Limitations**: The method relies on pre-segmented video inputs and graph-based propagation, which may introduce latency and computational overhead unsuitable for real-time embodied control loops.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22285)
- **👥 Authors**: Ruoliu Yang, Chu Wu, Caifeng Shan, Ran He, Chaoyou Fu
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ SpatialBoost: Enhancing Visual Representation through Language-Guided Reasoning (Score: 6/10)
- **💡 Innovation**: The framework utilizes a multi-turn Chain-of-Thought reasoning process to distill dense 3D spatial relationships into linguistic descriptions for injecting spatial awareness into vision encoders.
- **⚠️ Limitations**: The approach relies on linguistic proxies for 3D spatial reasoning rather than direct 3D geometric supervision, which may limit its utility in high-precision robotic manipulation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22057)
- **👥 Authors**: Byungwoo Jeon, Dongyoung Kim, Huiwon Jang, Insoo Kim, Jinwoo Shin
- **🏷️ Tags**: #Foundation_Model #LLM #Embodied_AI

---

### ✨ Manifold-Aware Exploration for Reinforcement Learning in Video Generation (Score: 6/10)
- **💡 Innovation**: SAGE-GRPO introduces a manifold-aware SDE with logarithmic curvature correction and dual trust-region constraints to stabilize reinforcement learning alignment for video generation models.
- **⚠️ Limitations**: The method is evaluated exclusively on video generation quality metrics rather than downstream embodied tasks or control-based reward functions.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.21872)
- **👥 Authors**: Mingzhe Zheng, Weijie Kong, Yue Wu, Dengyang Jiang, Yue Ma, Xuanhua He, Bin Lin, Kaixiong Gong, Zhao Zhong, Liefeng Bo, Qifeng Chen, Harry Yang
- **🏷️ Tags**: #Reinforcement_Learning #Diffusion_Model #Foundation_Model

---

### ✨ Insight-V++: Towards Advanced Long-Chain Visual Reasoning with Multimodal Large Language Models (Score: 6/10)
- **💡 Innovation**: The paper introduces a multi-agent framework utilizing ST-GRPO and J-GRPO algorithms to iteratively refine long-chain visual reasoning through a self-improving feedback loop between a reasoning agent and a summary agent.
- **⚠️ Limitations**: The approach is primarily evaluated on static image and video reasoning benchmarks rather than closed-loop embodied control or physical interaction tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.18118)
- **👥 Authors**: Yuhao Dong, Zuyan Liu, Shulin Tian, Yongming Rao, Ziwei Liu
- **🏷️ Tags**: #Foundation_Model #LLM #Reinforcement_Learning

---

### ✨ Generalized Discrete Diffusion from Snapshots (Score: 6/10)
- **💡 Innovation**: The framework introduces a unified discrete diffusion approach using uniformization to enable arbitrary noising processes and a snapshot-based ELBO for efficient training.
- **⚠️ Limitations**: The abstract lacks specific evidence or benchmarks related to embodied tasks, focusing primarily on general discrete generation rather than robotics-specific state-action modeling.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.21342)
- **👥 Authors**: Oussama Zekri, Théo Uscidda, Nicolas Boullé, Anna Korba
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ ToolRosetta: Bridging Open-Source Repositories and Large Language Model Agents through Automated Tool Standardization (Score: 6/10)
- **💡 Innovation**: ToolRosetta automates the conversion of heterogeneous open-source codebases into standardized Model Context Protocol (MCP) services to facilitate autonomous toolchain planning for LLM agents.
- **⚠️ Limitations**: The framework lacks specific evaluation on embodied robotics tasks, focusing primarily on general scientific domains and code execution rather than physical interaction or sensorimotor control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09290)
- **👥 Authors**: Shimin Di, Xujie Yuan, Hanghui Guo, Chaoqian Ouyang, Zhangze Chen, Ling Yue, Libin Zheng, Jia Zhu, Shaowu Pan, Jian Yin, Min-Ling Zhang, Yong Rui
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Foveated Diffusion: Efficient Spatially Adaptive Image and Video Generation (Score: 5/10)
- **💡 Innovation**: The paper introduces a spatially adaptive token allocation mechanism that uses foveated masking to reduce computational complexity in diffusion models by assigning higher token density to gaze-centric regions.
- **⚠️ Limitations**: The approach relies on the availability of accurate gaze tracking data, which is often noisy or unavailable in standard autonomous robotic manipulation or embodied navigation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23491v1)
- **👥 Authors**: Brian Chao, Lior Yariv, Howard Xiao, Gordon Wetzstein
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ End-to-End Efficient RL for Linear Bellman Complete MDPs with Deterministic Transitions (Score: 5/10)
- **💡 Innovation**: The paper introduces a computationally efficient algorithm for linear Bellman complete MDPs by leveraging deterministic transition dynamics to bypass the need for strong oracle assumptions.
- **⚠️ Limitations**: The approach is restricted to deterministic transitions and linear function approximation, which limits its applicability to complex, stochastic real-world robotic environments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23461v1)
- **👥 Authors**: Zakaria Mhammedi, Alexander Rakhlin, Nneka Okolo
- **🏷️ Tags**: #Reinforcement_Learning

---

### ✨ Bilevel Autoresearch: Meta-Autoresearching Itself (Score: 5/10)
- **💡 Innovation**: The paper introduces a bilevel optimization framework where an outer LLM loop autonomously generates and injects Python-based search mechanisms into an inner autoresearch loop to improve task-specific performance.
- **⚠️ Limitations**: The methodology is evaluated exclusively on a synthetic GPT pretraining benchmark, lacking evidence of generalizability to complex, non-differentiable, or physical robotics research tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23420v1)
- **👥 Authors**: Yaonan Qu, Meng Lu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ GeoSANE: Learning Geospatial Representations from Models, Not Data (Score: 5/10)
- **💡 Innovation**: GeoSANE introduces a weight-generation framework that synthesizes a unified neural representation by aggregating weights from diverse pre-trained geospatial foundation models rather than relying on raw data.
- **⚠️ Limitations**: The approach is strictly confined to remote sensing classification, segmentation, and detection tasks, lacking direct applicability to embodied control or temporal action-based robotics workflows.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23408v1)
- **👥 Authors**: Joelle Hanna, Damian Falk, Stella X. Yu, Damian Borth
- **🏷️ Tags**: #Foundation_Model

---

### ✨ LongCat-Flash-Prover: Advancing Native Formal Reasoning via Agentic Tool-Integrated Reinforcement Learning (Score: 5/10)
- **💡 Innovation**: The paper introduces a Hierarchical Importance Sampling Policy Optimization (HisPO) algorithm that utilizes gradient masking to stabilize reinforcement learning for long-horizon formal reasoning tasks in MoE models.
- **⚠️ Limitations**: The methodology is strictly confined to formal mathematical reasoning in Lean4 and lacks any grounding in physical environments or multi-modal perception required for embodied tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.21065)
- **👥 Authors**: Jianing Wang, Jianfei Zhang, Qi Guo, Linsen Guo, Rumei Li, Chao Zhang, Chong Peng, Cunguang Wang, Dengchang Zhao, Jiarong Shi, Jingang Wang, Liulin Feng, Mengxia Shen, Qi Li, Shengnan An, Shun Wang, Wei Shi, Xiangyu Xi, Xiaoyu Li, Xuezhi Cao, Yi Lu, Yunke Zhao, Zhengyu Chen, Zhimin Lin, Wei Wang, Peng Pei, Xunliang Cai
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Not All Layers Are Created Equal: Adaptive LoRA Ranks for Personalized Image Generation (Score: 5/10)
- **💡 Innovation**: The method introduces an adaptive rank selection mechanism for LoRA by imposing an importance ordering on rank positions, allowing individual layers to dynamically determine their optimal capacity during fine-tuning.
- **⚠️ Limitations**: The approach is evaluated exclusively on static image generation tasks, leaving its efficacy and computational overhead in high-dimensional, temporal, or embodied control settings unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.21884)
- **👥 Authors**: Donald Shenaj, Federico Errica, Antonio Carta
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ AdditiveLLM2: A Multi-modal Large Language Model for Additive Manufacturing (Score: 5/10)
- **💡 Innovation**: The paper introduces a domain-specific multi-modal LLM for additive manufacturing by fine-tuning Gemma 3 on a curated 50-million-token dataset of technical literature.
- **⚠️ Limitations**: The approach lacks integration with physical control loops or embodied feedback, limiting its utility to knowledge retrieval and visual analysis rather than active robotic control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22017)
- **👥 Authors**: Peter Pak, Amir Barati Farimani
- **🏷️ Tags**: #Foundation_Model #LLM

---

### 📄 Failure of contextual invariance in gender inference with large language models (Score: 4/10)
- **💡 Innovation**: The paper introduces a Contextuality-by-Default analysis to quantify the violation of contextual invariance in LLMs during gender inference tasks.
- **⚠️ Limitations**: The study focuses exclusively on linguistic gender inference rather than embodied reasoning or action-conditioned decision-making.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23485v1)
- **👥 Authors**: Sagar Kumar, Ariel Flint, Luca Maria Aiello, Andrea Baronchelli
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Evaluating LLM-Based Test Generation Under Software Evolution (Score: 4/10)
- **💡 Innovation**: The study quantifies the semantic fragility of LLM-generated unit tests by evaluating performance degradation across 22,374 program variants under semantic-altering and semantic-preserving changes.
- **⚠️ Limitations**: The research focuses exclusively on software engineering unit testing rather than the reasoning or planning capabilities required for embodied robotics or VLA tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23443v1)
- **👥 Authors**: Sabaat Haroon, Mohammad Taha Khan, Muhammad Ali Gulzar
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Graph Energy Matching: Transport-Aligned Energy-Based Modeling for Graph Generation (Score: 4/10)
- **💡 Innovation**: The paper introduces Graph Energy Matching (GEM), which utilizes a JKO-scheme-inspired transport map to align energy-based potential functions with discrete graph generation processes.
- **⚠️ Limitations**: The methodology is strictly evaluated on molecular graph benchmarks and lacks demonstration of applicability to embodied state representations or physical dynamics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23398v1)
- **👥 Authors**: Michal Balcerak, Suprosana Shit, Chinmay Prabhakar, Sebastian Kaltenbach, Michael S. Albergo, Yilun Du, Bjoern Menze
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 BubbleRAG: Evidence-Driven Retrieval-Augmented Generation for Black-Box Knowledge Graphs (Score: 4/10)
- **💡 Innovation**: The paper formalizes black-box knowledge graph retrieval as an Optimal Informative Subgraph Retrieval problem and introduces a training-free heuristic pipeline for evidence graph discovery.
- **⚠️ Limitations**: The approach is strictly limited to text-based knowledge graph reasoning and lacks any grounding in physical environments or multi-modal action spaces.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.20309)
- **👥 Authors**: Duyi Pan, Tianao Lou, Xin Li, Haoze Song, Yiwen Wu, Mengyi Deng, Mingyu Yang, Wei Wang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 ReqFusion: A Multi-Provider Framework for Automated PEGS Analysis Across Software Domains (Score: 3/10)
- **💡 Innovation**: The framework introduces a multi-provider LLM orchestration pipeline that enforces the PEGS (Project, Environment, Goal, System) structured prompting schema to improve requirement extraction accuracy.
- **⚠️ Limitations**: The methodology is strictly limited to software engineering requirement analysis and lacks any integration with embodied agents, physical sensors, or action-space reasoning.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23482v1)
- **👥 Authors**: Muhammad Khalid, Manuel Oriol, Yilmaz Uygun
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 FG-Portrait: 3D Flow Guided Editable Portrait Animation (Score: 3/10)
- **💡 Innovation**: The method integrates geometry-driven 3D flow priors into a diffusion-based animation framework by using depth-guided sampling to map target pixels back to source locations.
- **⚠️ Limitations**: The approach relies on parametric 3D head models, which restricts its applicability to human faces and limits its utility for general-purpose embodied robotics tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.23381v1)
- **👥 Authors**: Yating Xu, Yunqi Miao, Evangelos Ververas, Jiankang Deng, Jifei Song
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 Progressive Training for Explainable Citation-Grounded Dialogue: Reducing Hallucination to Zero in English-Hindi LLMs (Score: 3/10)
- **💡 Innovation**: The paper introduces a four-stage progressive training pipeline that integrates citation-grounded SFT and GRPO alignment to eliminate hallucinations in bilingual English-Hindi dialogue systems.
- **⚠️ Limitations**: The methodology is strictly confined to text-based dialogue generation and lacks any integration with visual, spatial, or physical action modalities required for embodied robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.18911)
- **👥 Authors**: Vedant Pandya
- **🏷️ Tags**: #LLM #Foundation_Model

---


