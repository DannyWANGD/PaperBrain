# 📅 2026-03-25 - Paper Digest
## Summary
Total Papers: 43 | High Impact: 16

## 📝 Papers List
### 🔥 DreamerAD: Efficient Reinforcement Learning via Latent World Model for Autonomous Driving (Score: 8/10)
- **💡 Innovation**: DreamerAD accelerates latent world model inference by employing recursive multi-resolution step compression to reduce diffusion sampling from 100 steps to a single step.
- **⚠️ Limitations**: The reliance on latent-space autoregressive reward modeling may struggle with long-horizon temporal consistency or rare-event safety scenarios not captured in the training distribution.
- **🔗 Link**: [[DreamerAD]]
- **👥 Authors**: Pengxuan Yang, Yupeng Zheng, Deheng Qian, Zebin Xing, Qichao Zhang, Linbo Wang, Yichen Zhang, Shaoyu Guo, Zhongpu Xia, Qiang Chen, Junyu Han, Lingyun Xu, Yifeng Pan, Dongbin Zhao
- **🏷️ Tags**: #World_Model #Diffusion_Model #Reinforcement_Learning #Embodied_AI

---

### 🔥 TAG: Target-Agnostic Guidance for Stable Object-Centric Inference in Vision-Language-Action Models (Score: 8/10)
- **💡 Innovation**: TAG introduces an inference-time guidance mechanism that computes a residual steering signal by contrasting VLA policy outputs between original and object-erased visual observations.
- **⚠️ Limitations**: The method relies on the existence of a reliable object-erasure mechanism (e.g., in-painting or masking), which may introduce its own artifacts or latency overhead during real-time inference.
- **🔗 Link**: [[TAG]]
- **👥 Authors**: Jiaying Zhou, Zhihao Zhan, Ruifeng Zhai, Qinhan Lyu, Hao Liu, Keze Wang, Liang Lin, Guangrun Wang
- **🏷️ Tags**: #Robot_Manipulation #VLA #Embodied_AI #Foundation_Model

---

### 🔥 WildWorld: A Large-Scale Dataset for Dynamic World Modeling with Actions and Explicit State toward Generative ARPG (Score: 8/10)
- **💡 Innovation**: The paper introduces a large-scale, action-conditioned world modeling dataset derived from AAA game engines that provides explicit state annotations (skeletons, depth, camera poses) to decouple action semantics from pixel-level dynamics.
- **⚠️ Limitations**: The reliance on a specific game engine environment may limit the direct transferability of learned world dynamics to real-world robotic systems with different physical constraints.
- **🔗 Link**: [[WildWorld]]
- **👥 Authors**: Zhen Li, Zian Meng, Shuwei Shi, Wenshuo Peng, Yuwei Wu, Bo Zheng, Chuanhao Li, Kaipeng Zhang
- **🏷️ Tags**: #World_Model #Embodied_AI #Reinforcement_Learning #Foundation_Model

---

### 🔥 SIMART: Decomposing Monolithic Meshes into Sim-ready Articulated Assets via MLLM (Score: 8/10)
- **💡 Innovation**: SIMART introduces a Sparse 3D VQ-VAE to compress 3D token sequences by 70%, enabling unified MLLM-based decomposition and kinematic prediction for articulated assets.
- **⚠️ Limitations**: The method remains constrained by the quality and diversity of the training data in PartNet-Mobility and the inherent difficulty of generalizing kinematic priors to unseen, complex mechanical structures.
- **🔗 Link**: [[SIMART]]
- **👥 Authors**: Chuanrui Zhang, Minghan Qin, Yuang Wang, Baifeng Xie, Hang Li, Ziwei Wang
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #LLM #Robot_Manipulation

---

### 🔥 ThinkJEPA: Empowering Latent World Models with Large Vision-Language Reasoning Model (Score: 8/10)
- **💡 Innovation**: The method introduces a dual-temporal pathway architecture that fuses dense JEPA-style latent dynamics with sparse, long-horizon semantic guidance extracted from a VLM via a hierarchical pyramid representation module.
- **⚠️ Limitations**: The reliance on VLM-based guidance may introduce significant latency, potentially hindering real-time performance in high-frequency robotic control loops.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22281)
- **👥 Authors**: Haichao Zhang, Yijiang Li, Shwai He, Tushar Nagarajan, Mingfei Chen, Jianglin Lu, Ang Li, Yun Fu
- **🏷️ Tags**: #World_Model #Embodied_AI #Robot_Manipulation #Foundation_Model

---

### 🔥 VP-VLA: Visual Prompting as an Interface for Vision-Language-Action Models (Score: 8/10)
- **💡 Innovation**: VP-VLA introduces a dual-system architecture that decouples high-level reasoning from low-level control by injecting structured visual prompts (crosshairs and bounding boxes) directly into the observation space to guide the controller.
- **⚠️ Limitations**: The reliance on a System 2 planner to generate spatial anchors may introduce latency bottlenecks and potential failure modes if the grounding module misidentifies target coordinates.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22003)
- **👥 Authors**: Zixuan Wang, Yuxin Chen, Yuqi Liu, Jinhui Ye, Pengguang Chen, Changsheng Lu, Shu Liu, Jiaya Jia
- **🏷️ Tags**: #VLA #Robot_Manipulation #Embodied_AI #Foundation_Model

---

### 🔥 CanViT: Toward Active-Vision Foundation Models (Score: 8/10)
- **💡 Innovation**: CanViT introduces an asymmetric cross-attention mechanism that decouples a retinotopic backbone from a spatiotopic latent canvas, enabling efficient active-vision inference through dense latent distillation.
- **⚠️ Limitations**: The current evaluation is limited to static image datasets (ADE20K, ImageNet) rather than dynamic, closed-loop robotic environments, leaving the policy-agnostic claim untested in embodied settings.
- **🔗 Link**: [[CanViT]]
- **👥 Authors**: Yohaï-Eliel Berreby, Sabrina Du, Audrey Durand, B. Suresh Krishna
- **🏷️ Tags**: #Foundation_Model #Embodied_AI #World_Model

---

### 🔥 VTAM: Video-Tactile-Action Models for Complex Physical Interaction Beyond VLAs (Score: 8/10)
- **💡 Innovation**: VTAM introduces a multimodal world modeling framework that integrates tactile streams into a pretrained video transformer using a tactile regularization loss to prevent visual latent dominance during action prediction.
- **⚠️ Limitations**: The reliance on a lightweight modality transfer finetuning may still struggle with long-term tactile-visual drift or scenarios where tactile sensors lack sufficient spatial resolution.
- **🔗 Link**: [[VTAM]]
- **👥 Authors**: Haoran Yuan, Weigang Yi, Zhenyu Zhang, Wendi Chen, Yuchen Mo, Jiashi Yin, Xinzhuo Li, Xiangyu Zeng, Chuan Wen, Cewu Lu, Katherine Driggs-Campbell, Ismini Lourentzou
- **🏷️ Tags**: #Robot_Manipulation #VLA #World_Model #Embodied_AI

---

### 🔥 ABot-PhysWorld: Interactive World Foundation Model for Robotic Manipulation with Physics Alignment (Score: 8/10)
- **💡 Innovation**: The paper introduces a DPO-based post-training framework with decoupled discriminators to enforce physical constraints in a 14B Diffusion Transformer world model.
- **⚠️ Limitations**: The reliance on a curated dataset of three million clips may limit generalization to out-of-distribution physical dynamics not captured in the training distribution.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.23376)
- **👥 Authors**: Yuzhi Chen, Ronghan Chen, Dongjie Huo, Yandan Yang, Dekang Qi, Haoyun Liu, Tong Lin, Shuang Zeng, Junjin Xiao, Xinyuan Chang, Feng Xiong, Xing Wei, Zhiheng Ma, Mu Xu
- **🏷️ Tags**: #World_Model #Diffusion_Model #Embodied_AI #Robot_Manipulation #Foundation_Model

---

### ✨ Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving (Score: 7/10)
- **💡 Innovation**: Latent-WAM introduces a Spatial-Aware Compressive World Encoder that distills foundation model geometric priors into compact scene tokens for autoregressive trajectory planning.
- **⚠️ Limitations**: The reliance on specific simulation benchmarks (NAVSIM/HUGSIM) may limit the generalizability of the latent dynamics to complex, unstructured real-world driving environments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24581v1)
- **👥 Authors**: Linbo Wang, Yupeng Zheng, Qiang Chen, Shiwei Li, Yichen Zhang, Zebin Xing, Qichao Zhang, Xiang Li, Deheng Qian, Pengxuan Yang, Yihang Dong, Ce Hao, Xiaoqing Ye, Junyu han, Yifeng Pan, Dongbin Zhao
- **🏷️ Tags**: #World_Model #Embodied_AI #Foundation_Model

---

### ✨ UI-Voyager: A Self-Evolving GUI Agent Learning via Failed Experience (Score: 7/10)
- **💡 Innovation**: UI-Voyager introduces a two-stage self-evolving framework that combines Rejection Fine-Tuning for autonomous data co-evolution and Group Relative Self-Distillation to derive dense step-level supervision from successful trajectories.
- **⚠️ Limitations**: The approach is specifically constrained to mobile GUI automation tasks and may not generalize to physical robot manipulation or continuous control environments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24533v1)
- **👥 Authors**: Zichuan Lin, Feiyu Liu, Yijun Yang, Jiafei Lyu, Yiming Gao, Yicheng Liu, Zhicong Lu, Yangbin Yu, Mingyu Yang, Junyou Li, Deheng Ye, Jie Jiang
- **🏷️ Tags**: #LLM #Foundation_Model #Embodied_AI

---

### ✨ Toward Physically Consistent Driving Video World Models under Challenging Trajectories (Score: 7/10)
- **💡 Innovation**: PhyGenesis introduces a two-stage framework that decouples trajectory conditioning via a physical condition generator before feeding it into a physics-enhanced video diffusion model to ensure temporal and spatial consistency.
- **⚠️ Limitations**: The reliance on CARLA-generated synthetic data for physical grounding may introduce domain gaps when generalizing to complex, long-tail real-world edge cases not captured in the simulator.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24506v1)
- **👥 Authors**: Jiawei Zhou, Zhenxin Zhu, Lingyi Du, Linye Lyu, Lijun Zhou, Zhanqian Wu, Hongcheng Luo, Zhuotao Tian, Bing Wang, Guang Chen, Hangjun Ye, Haiyang Sun, Yu Li
- **🏷️ Tags**: #World_Model #Diffusion_Model #Sim2Real #Embodied_AI

---

### ✨ CUA-Suite: Massive Human-annotated Video Demonstrations for Computer-Use Agents (Score: 7/10)
- **💡 Innovation**: The paper introduces a large-scale, high-frequency (30 fps) continuous video dataset for computer-use agents that captures temporal dynamics and kinematic cursor traces, moving beyond sparse screenshot-based interaction data.
- **⚠️ Limitations**: The dataset is restricted to desktop environments, which may not generalize to physical robot manipulation or complex 3D spatial reasoning tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24440v1)
- **👥 Authors**: Xiangru Jian, Shravan Nayak, Kevin Qinghong Lin, Aarash Feizi, Kaixin Li, Patrice Bechard, Spandana Gella, Sai Rajeswar
- **🏷️ Tags**: #VLA #Foundation_Model #LLM #Embodied_AI

---

### ✨ Attend Before Attention: Efficient and Scalable Video Understanding via Autoregressive Gazing (Score: 7/10)
- **💡 Innovation**: AutoGaze employs an autoregressive reinforcement learning-based selection mechanism to dynamically prune redundant visual patches, enabling efficient processing of high-resolution, long-form video inputs.
- **⚠️ Limitations**: The method relies on a reconstruction-based objective which may discard task-relevant but visually subtle information critical for precise robotic manipulation or state estimation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12254)
- **👥 Authors**: Baifeng Shi, Stephanie Fu, Long Lian, Hanrong Ye, David Eigen, Aaron Reite, Boyi Li, Jan Kautz, Song Han, David M. Chan, Pavlo Molchanov, Trevor Darrell, Hongxu Yin
- **🏷️ Tags**: #Foundation_Model #LLM #Embodied_AI

---

### ✨ Ego2Web: A Web Agent Benchmark Grounded in Egocentric Videos (Score: 7/10)
- **💡 Innovation**: The paper introduces a cross-modal benchmark that bridges egocentric video perception with web-based agent execution, requiring agents to ground digital tasks in physical visual context.
- **⚠️ Limitations**: The evaluation relies heavily on an LLM-as-a-Judge framework, which may inherit biases and struggle with the nuances of physical-to-digital task grounding.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22529)
- **👥 Authors**: Shoubin Yu, Lei Shu, Antoine Yang, Yao Fu, Srinivas Sunkara, Maria Wang, Jindong Chen, Mohit Bansal, Boqing Gong
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #LLM

---

### ✨ Sparse but Critical: A Token-Level Analysis of Distributional Shifts in RLVR Fine-Tuning of LLMs (Score: 7/10)
- **💡 Innovation**: The paper introduces a cross-sampling intervention framework to isolate the minimal set of token-level distributional shifts responsible for performance gains in RLVR-tuned LLMs.
- **⚠️ Limitations**: The analysis is restricted to text-based reasoning tasks and does not address the high-dimensional, continuous action spaces characteristic of embodied robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22446)
- **👥 Authors**: Haoming Meng, Kexin Huang, Shaohang Wei, Chiyu Ma, Shuo Yang, Xue Wang, Guoyin Wang, Bolin Ding, Jingren Zhou
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Polynomial Speedup in Diffusion Models with the Multilevel Euler-Maruyama Method (Score: 6/10)
- **💡 Innovation**: The paper introduces a Multilevel Euler-Maruyama (ML-EM) framework that achieves polynomial speedup in SDE solving by leveraging a hierarchy of drift approximators with varying computational costs.
- **⚠️ Limitations**: The method relies on the existence of a hierarchy of models with increasing accuracy and cost, which may be difficult to curate or train effectively for complex, high-dimensional embodied control policies.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24594v1)
- **👥 Authors**: Arthur Jacot
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ SEGAR: Selective Enhancement for Generative Augmented Reality (Score: 6/10)
- **💡 Innovation**: SEGAR introduces a two-stage pipeline that decouples generative world model prediction from a selective correction mechanism to ensure safety-critical alignment in augmented future frames.
- **⚠️ Limitations**: The approach relies on well-defined semantic region structures, which may not generalize to the unstructured environments typical of complex robot manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24541v1)
- **👥 Authors**: Fanjun Bu, Chenyang Yuan, Hiroshi Yasuda
- **🏷️ Tags**: #World_Model #Diffusion_Model

---

### ✨ CliPPER: Contextual Video-Language Pretraining on Long-form Intraoperative Surgical Procedures for Event Recognition (Score: 6/10)
- **💡 Innovation**: CliPPER introduces a multi-objective pretraining framework for surgical videos using Contextual Video-Text Contrastive Learning, Clip Order Prediction, and Cycle-Consistency Alignment to improve temporal representation.
- **⚠️ Limitations**: The framework is specialized for surgical event recognition and lacks an action-conditioned policy or embodied feedback loop necessary for direct robotic manipulation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24539v1)
- **👥 Authors**: Florian Stilz, Vinkle Srivastav, Nassir Navab, Nicolas Padoy
- **🏷️ Tags**: #Foundation_Model #Embodied_AI

---

### ✨ AVO: Agentic Variation Operators for Autonomous Evolutionary Search (Score: 6/10)
- **💡 Innovation**: AVO replaces fixed evolutionary mutation and crossover operators with a self-directed agentic loop that utilizes execution feedback and domain knowledge to iteratively refine code implementations.
- **⚠️ Limitations**: The approach is computationally expensive, requiring 7 days of continuous autonomous evolution on high-end B200 GPUs to achieve performance gains.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24517v1)
- **👥 Authors**: Terry Chen, Zhifan Ye, Bing Xu, Zihao Ye, Timmy Liu, Ali Hassani, Tianqi Chen, Andrew Kerr, Haicheng Wu, Yang Xu, Yu-Jung Chen, Hanfeng Chen, Aditya Kane, Ronny Krashinsky, Ming-Yu Liu, Vinod Grover, Luis Ceze, Roger Bringmann, John Tran, Wei Liu, Fung Xie, Michael Lightstone, Humphrey Shi
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Claudini: Autoresearch Discovers State-of-the-Art Adversarial Attack Algorithms for LLMs (Score: 6/10)
- **💡 Innovation**: The paper introduces an autoresearch pipeline that iteratively optimizes adversarial attack algorithms for LLMs by leveraging dense quantitative feedback from white-box red-teaming objectives.
- **⚠️ Limitations**: The scope is strictly limited to LLM security and does not address the challenges of physical grounding, sensorimotor control, or embodied decision-making.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24511v1)
- **👥 Authors**: Alexander Panfilov, Peter Romov, Igor Shilov, Yves-Alexandre de Montjoye, Jonas Geiping, Maksym Andriushchenko
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Video-Only ToM: Enhancing Theory of Mind in Multimodal Large Language Models (Score: 6/10)
- **💡 Innovation**: The paper introduces VisionToM, a framework that computes intervention vectors to align visual representations with semantic targets, effectively steering MLLM attention layers to mitigate reliance on linguistic priors during Theory of Mind tasks.
- **⚠️ Limitations**: The approach is validated primarily on multiple-choice QA benchmarks rather than closed-loop embodied control tasks, limiting its immediate applicability to robot manipulation or navigation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24484v1)
- **👥 Authors**: Siqi Liu, Xinyang Li, Bochao Zou, Junbao Zhuo, Huimin Ma, Jiansheng Chen
- **🏷️ Tags**: #Foundation_Model #LLM #Embodied_AI

---

### ✨ Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs? (Score: 6/10)
- **💡 Innovation**: The paper identifies that self-distillation degrades reasoning by suppressing epistemic verbalization, which is essential for handling out-of-distribution tasks.
- **⚠️ Limitations**: The study is restricted to text-based mathematical reasoning tasks and does not explore how these findings translate to multimodal or embodied decision-making contexts.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24472v1)
- **👥 Authors**: Jeonghye Kim, Xufang Luo, Minbeom Kim, Sangmook Lee, Dohyung Kim, Jiwon Jeon, Dongsheng Li, Yuqing Yang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ SpecEyes: Accelerating Agentic Multimodal LLMs via Speculative Perception and Planning (Score: 6/10)
- **💡 Innovation**: SpecEyes implements a speculative execution framework for agentic MLLMs by using a lightweight model to predict tool-calling trajectories, gated by an answer-separability confidence metric.
- **⚠️ Limitations**: The approach relies on the assumption that agentic tool-use patterns are predictable by smaller models, which may fail in high-entropy, real-time robotic control scenarios.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.23483)
- **👥 Authors**: Haoyu Huang, Jinfa Huang, Zhongwei Wan, Xiawu Zheng, Rongrong Ji, Jiebo Luo
- **🏷️ Tags**: #LLM #Foundation_Model #Embodied_AI

---

### ✨ From Static Templates to Dynamic Runtime Graphs: A Survey of Workflow Optimization for LLM Agents (Score: 6/10)
- **💡 Innovation**: The paper introduces a unified taxonomy for agentic computation graphs (ACGs) that categorizes LLM-based workflows by the timing of structural determination and the nature of optimization signals.
- **⚠️ Limitations**: The survey focuses primarily on high-level software agent workflows and lacks specific analysis of how these graph-based optimizations translate to the latency and safety constraints of embodied robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22386)
- **👥 Authors**: Ling Yue, Kushal Raj Bhandari, Ching-Yun Ko, Dhaval Patel, Shuxin Lin, Nianjun Zhou, Jianxi Gao, Pin-Yu Chen, Shaowu Pan
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ DA-Flow: Degradation-Aware Optical Flow Estimation with Diffusion Models (Score: 6/10)
- **💡 Innovation**: DA-Flow leverages the internal feature representations of pre-trained image restoration diffusion models, augmented with spatio-temporal attention, to provide robust optical flow estimation under severe image degradation.
- **⚠️ Limitations**: The method relies on computationally expensive diffusion-based feature extraction, which may hinder real-time performance requirements in closed-loop robotic systems.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.23499)
- **👥 Authors**: Jaewon Min, Jaeeun Lee, Yeji Choi, Paul Hyunbin Cho, Jin Hyeon Kim, Tae-Young Lee, Jongsik Ahn, Hwayeong Lee, Seonghyun Park, Seungryong Kim
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ UniGRPO: Unified Policy Optimization for Reasoning-Driven Visual Generation (Score: 6/10)
- **💡 Innovation**: UniGRPO introduces a unified reinforcement learning framework that integrates standard GRPO for reasoning with FlowGRPO for visual synthesis by replacing latent KL penalties with velocity-field MSE penalties.
- **⚠️ Limitations**: The framework is currently validated only on static image generation tasks, lacking the temporal dynamics and physical constraints required for embodied robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.23500)
- **👥 Authors**: Jie Liu, Zilyu Ye, Linxiao Yuan, Shenhan Zhu, Yu Gao, Jie Wu, Kunchang Li, Xionghui Wang, Xiaonan Nie, Weilin Huang, Wanli Ouyang
- **🏷️ Tags**: #Reinforcement_Learning #Diffusion_Model #LLM #Foundation_Model

---

### ✨ RealMaster: Lifting Rendered Scenes into Photorealistic Video (Score: 6/10)
- **💡 Innovation**: RealMaster utilizes an anchor-based propagation strategy combined with IC-LoRA to distill 3D-consistent geometric cues into a video diffusion model for photorealistic rendering.
- **⚠️ Limitations**: The method relies on pre-rendered 3D engine outputs as a structural prior, which may struggle with complex, non-rigid, or unmodeled real-world dynamics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.23462)
- **👥 Authors**: Dana Cohen-Bar, Ido Sobol, Raphael Bensadoun, Shelly Sheynin, Oran Gafni, Or Patashnik, Daniel Cohen-Or, Amit Zohar
- **🏷️ Tags**: #Sim2Real #Diffusion_Model

---

### ✨ Rethinking Token-Level Policy Optimization for Multimodal Chain-of-Thought (Score: 6/10)
- **💡 Innovation**: The method introduces Perception-Exploration Policy Optimization (PEPO), which uses hidden state similarity to derive a perception prior for token-level advantage weighting in RLVR.
- **⚠️ Limitations**: The approach is evaluated on static multimodal reasoning benchmarks and lacks demonstration of transferability to embodied action spaces or continuous control tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22847)
- **👥 Authors**: Yunheng Li, Hangyi Kuang, Hengrui Zhang, Jiangxia Cao, Zhaojie Liu, Qibin Hou, Ming-Ming Cheng
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### ✨ 2Xplat: Two Experts Are Better Than One Generalist (Score: 6/10)
- **💡 Innovation**: The framework decouples pose estimation and 3D Gaussian generation into a two-expert architecture, replacing monolithic models to reduce feature entanglement.
- **⚠️ Limitations**: The approach relies on feed-forward inference which may struggle with complex, occluded, or dynamic scenes compared to optimization-based methods.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.21064)
- **👥 Authors**: Hwasik Jeong, Seungryong Lee, Gyeongjin Kang, Seungkwon Yang, Xiangyu Sun, Seungtae Nam, Eunbyung Park
- **🏷️ Tags**: #3D_Gaussian_Splatting #Foundation_Model

---

### ✨ Fair splits flip the leaderboard: CHANRG reveals limited generalization in RNA secondary-structure prediction (Score: 6/10)
- **💡 Innovation**: The paper introduces a hierarchical, structure-aware deduplication and genome-aware splitting framework to rigorously evaluate the out-of-distribution generalization of RNA structure predictors.
- **⚠️ Limitations**: The methodology is domain-specific to RNA bioinformatics and does not provide transferable insights for visual-motor control or physical world modeling.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.22330)
- **👥 Authors**: Zhiyuan Chen, Zhenfeng Deng, Pan Deng, Yue Liao, Xiu Su, Peng Ye, Xihui Liu
- **🏷️ Tags**: #Foundation_Model

---

### ✨ VISion On Request: Enhanced VLLM efficiency with sparse, dynamically selected, vision-language interactions (Score: 6/10)
- **💡 Innovation**: VISOR replaces visual token compression with a dynamic, policy-driven sparsification of cross-attention and self-attention layers to maintain high-resolution visual fidelity at reduced inference costs.
- **⚠️ Limitations**: The method relies on a policy mechanism for dynamic computation allocation, which may introduce non-deterministic latency jitter unsuitable for real-time robot control loops.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.23495)
- **👥 Authors**: Adrian Bulat, Alberto Baldrati, Ioannis Maniadis Metaxas, Yassine Ouali, Georgios Tzimiropoulos
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ Reasoning or Rhetoric? An Empirical Analysis of Moral Reasoning Explanations in Large Language Models (Score: 6/10)
- **💡 Innovation**: The study introduces a systematic empirical framework to evaluate moral reasoning consistency in LLMs by mapping outputs to Kohlberg’s developmental stages and identifying 'moral decoupling' between justification and action.
- **⚠️ Limitations**: The analysis is restricted to textual moral dilemmas and does not address how these reasoning failures manifest in embodied agents or multi-modal action spaces.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.21854)
- **👥 Authors**: Aryan Kasat, Smriti Singh, Aman Chadha, Vinija Jain
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ VFIG: Vectorizing Complex Figures in SVG with Vision-Language Models (Score: 5/10)
- **💡 Innovation**: The method employs a coarse-to-fine training curriculum that transitions from supervised fine-tuning of atomic primitives to reinforcement learning for global topological consistency in vector graphics.
- **⚠️ Limitations**: The approach is strictly limited to 2D vector graphic reconstruction and lacks the spatial-temporal grounding or physical dynamics modeling required for embodied robotics applications.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24575v1)
- **👥 Authors**: Qijia He, Xunmei Liu, Hammaad Memon, Ziang Li, Zixian Ma, Jaemin Cho, Jason Ren, Daniel S Weld, Ranjay Krishna
- **🏷️ Tags**: #Foundation_Model #LLM #Reinforcement_Learning

---

### ✨ Completeness of Unbounded Best-First Minimax and Descent Minimax (Score: 5/10)
- **💡 Innovation**: The paper provides a formal proof of completeness for generalized versions of Unbounded Best-First Minimax and Descent Minimax algorithms when augmented with completion techniques.
- **⚠️ Limitations**: The scope is restricted to theoretical game-tree search in perfect information games, which does not directly translate to the high-dimensional, continuous state-action spaces typical of modern embodied AI.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24572v1)
- **👥 Authors**: Quentin Cohen-Solal
- **🏷️ Tags**: #Reinforcement_Learning

---

### ✨ Anti-I2V: Safeguarding your photos from malicious image-to-video generation (Score: 5/10)
- **💡 Innovation**: Anti-I2V introduces a dual-domain adversarial perturbation strategy operating in L*a*b* and frequency spaces to disrupt temporal coherence in Diffusion Transformer-based video generation.
- **⚠️ Limitations**: The method is specifically designed for image-to-video generation security and lacks applicability to embodied control policies or robotic perception tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24570v1)
- **👥 Authors**: Duc Vu, Anh Nguyen, Chi Tran, Anh Tran
- **🏷️ Tags**: #Diffusion_Model

---

### ✨ Scaling Recurrence-aware Foundation Models for Clinical Records via Next-Visit Prediction (Score: 5/10)
- **💡 Innovation**: The paper introduces a recurrence-aware generative pretraining strategy that explicitly regularizes repeated event tokens to prevent performance inflation in sequential clinical forecasting.
- **⚠️ Limitations**: The methodology is strictly confined to structured EHR sequences and lacks the spatial, temporal, or multimodal grounding required for embodied robotics applications.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24562v1)
- **👥 Authors**: Haresh Rengaraj Rajamohan, Xiang Gao, Weicheng Zhu, Shih-Lun Huang, Long Chen, Gabe Schulman, Huizhen Jin, Shengduo Li, Yixuan Wang, Huidi Yang, Kyunghyun Cho, Cem M. Deniz, Narges Razavian
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ TuneShift-KD: Knowledge Distillation and Transfer for Fine-tuned Models (Score: 5/10)
- **💡 Innovation**: The method identifies specialized knowledge by calculating perplexity divergence between a base model and a fine-tuned model to automatically synthesize a distillation dataset.
- **⚠️ Limitations**: The approach relies on the assumption that specialized knowledge is uniquely identifiable through perplexity gaps, which may fail for complex reasoning tasks or non-textual modalities.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24518v1)
- **👥 Authors**: Yushi Guan, Jeanine Ohene-Agyei, Daniel Kwan, Jean Sebastien Dandurand, Yifei Zhang, Nandita Vijaykumar
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ Composer 2 Technical Report (Score: 5/10)
- **💡 Innovation**: The paper introduces a two-phase training pipeline combining continued pretraining with large-scale reinforcement learning specifically optimized for long-horizon software engineering tasks within a production-grade harness.
- **⚠️ Limitations**: The methodology is highly specialized for code generation and lacks any grounding in visual-motor control, spatial reasoning, or physical world interaction.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24477v1)
- **👥 Authors**: Cursor Reseach, :, Aaron Chan, Ahmed Shalaby, Alexander Wettig, Aman Sanger, Andrew Zhai, Anurag Ajay, Ashvin Nair, Charlie Snell, Chen Lu, Chen Shen, Emily Jia, Federico Cassano, Hanpeng Liu, Haoyu Chen, Henry Wildermuth, Jacob Jackson, Janet Li, Jediah Katz, Jiajun Yao, Joey Hejna, Josh Warner, Julius Vering, Kevin Frans, Lee Danilek, Less Wright, Lujing Cen, Luke Melas-Kyriazi, Michael Truell, Michiel de Jong, Naman Jain, Nate Schmidt, Nathan Wang, Niklas Muennighoff, Oleg Rybkin, Paul Loh, Phillip Kravtsov, Rishabh Yadav, Sahil Shah, Sam Kottler, Alexander M Rush, Shengtong Zhang, Shomil Jain, Sriram Sankar, Stefan Heule, Stuart H. Sul, Sualeh Asif, Victor Rong, Wanqi Zhu, William Lin, Yuchen Wu, Yuri Volkov, Yury Zemlyanskiy, Zack Holbrook, Zhiyuan Zhang
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Design, Modelling and Characterisation of a Miniature Fibre-Reinforced Soft Bending Actuator for Endoluminal Interventions (Score: 5/10)
- **💡 Innovation**: The paper introduces a multi-stage, multi-stiffness silicone casting process combined with embedded Kevlar fibre reinforcement to achieve high-curvature bending in a centimetre-scale soft actuator.
- **⚠️ Limitations**: The study lacks integration with closed-loop control or learning-based frameworks, focusing exclusively on open-loop mechanical characterization and FEM validation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24461v1)
- **👥 Authors**: Xiangyi Tan, Aoife McDonald-Bowyer, Danail Stoyanov, Agostino Stilli
- **🏷️ Tags**: #Embodied_AI

---

### ✨ Unleashing Vision-Language Semantics for Deepfake Video Detection (Score: 5/10)
- **💡 Innovation**: The method introduces a ForgePerceiver to extract forgery-specific cues while preserving pre-trained Vision-Language Alignment, combined with identity-aware text prompting for cross-modal semantic verification.
- **⚠️ Limitations**: The approach is strictly limited to the domain of digital media forensics and lacks any grounding in physical interaction, action space, or embodied decision-making.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24454v1)
- **👥 Authors**: Jiawen Zhu, Yunqi Miao, Xueyi Zhang, Jiankang Deng, Guansong Pang
- **🏷️ Tags**: #Foundation_Model

---

### ✨ Can AI Agents Answer Your Data Questions? A Benchmark for Data Agents (Score: 5/10)
- **💡 Innovation**: The paper introduces a multi-step, cross-database benchmark (DAB) that evaluates the end-to-end pipeline of data integration, transformation, and analysis for LLM-based agents.
- **⚠️ Limitations**: The benchmark is strictly limited to text-based database querying and lacks any grounding in physical environments, sensorimotor control, or multimodal action spaces.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.20576)
- **👥 Authors**: Ruiying Ma, Shreya Shankar, Ruiqi Chen, Yiming Lin, Sepanta Zeighami, Rajoshi Ghosh, Abhinav Gupta, Anushrut Gupta, Tanmai Gopal, Aditya G. Parameswaran
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Evaluating Chunking Strategies For Retrieval-Augmented Generation in Oil and Gas Enterprise Documents (Score: 4/10)
- **💡 Innovation**: The paper empirically compares four document chunking strategies specifically for complex, structure-heavy industrial documentation in the oil and gas sector.
- **⚠️ Limitations**: The study is restricted to text-based RAG pipelines and fails to address the spatial or visual reasoning required for interpreting technical diagrams like P&IDs.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.24556v1)
- **👥 Authors**: Samuel Taiwo, Mohd Amaluddin Yusoff
- **🏷️ Tags**: #LLM #Foundation_Model

---


