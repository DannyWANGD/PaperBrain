# 📅 2026-03-18 - Paper Digest
## Summary
Total Papers: 50 | High Impact: 8

## 📝 Papers List
### 🔥 ProbeFlow: Training-Free Adaptive Flow Matching for Vision-Language-Action Models (Score: 8/10)
- **💡 Innovation**: ProbeFlow introduces a training-free, adaptive inference mechanism for Flow Matching action heads that dynamically schedules ODE integration steps based on real-time trajectory complexity to minimize latency in robotic control.
- **⚠️ Limitations**: The reliance on cosine similarity of velocity vectors as a heuristic for trajectory complexity may struggle in highly stochastic environments or scenarios where the flow field is non-smooth or discontinuous.
- **🔗 Link**: [[ProbeFlow]]
- **👥 Authors**: Zhou Fang, Jiaqi Wang, Yi Zhou, Qiongfeng Shi
- **🏷️ Tags**: #Robot_Manipulation #VLA #Embodied_AI #Sim2Real #Foundation_Model

---

### 🔥 Kinema4D: Kinematic 4D World Modeling for Spatiotemporal Embodied Simulation (Score: 8/10)
- **💡 Innovation**: Kinema4D introduces a hybrid approach that combines explicit URDF-based kinematic control with generative 4D pointmap-conditioned modeling to ensure precise robot-world interaction dynamics.
- **⚠️ Limitations**: The reliance on URDF-based kinematics may limit the model's ability to simulate complex non-rigid object deformations or interactions that deviate significantly from standard kinematic chains.
- **🔗 Link**: [[Kinema4D]]
- **👥 Authors**: Mutian Xu, Tianbao Zhang, Tianqi Liu, Zhaoxi Chen, Xiaoguang Han, Ziwei Liu
- **🏷️ Tags**: #World_Model #Diffusion_Model #Embodied_AI #Robot_Manipulation #Sim2Real

---

### 🔥 From Passive Observer to Active Critic: Reinforcement Learning Elicits Process Reasoning for Robotic Manipulation (Score: 8/10)
- **💡 Innovation**: The paper introduces a novel framework that uses outcome-based reinforcement learning to fine-tune video MLLMs into active 'Critics' capable of explicit chain-of-thought progress estimation for long-horizon manipulation.
- **⚠️ Limitations**: The reliance on outcome-based RL may introduce sample efficiency challenges or reward hacking risks, and the paper does not fully detail the computational overhead of the temporal anchoring mechanism during real-time inference.
- **🔗 Link**: [[PRIMO R1]]
- **👥 Authors**: Yibin Liu, Yaxing Lyu, Daqi Gao, Zhixuan Liang, Weiliang Tang, Shilong Mu, Xiaokang Yang, Yao Mu
- **🏷️ Tags**: #Robot_Manipulation #Reinforcement_Learning #Embodied_AI #LLM #Foundation_Model

---

### ✨ Loc3R-VLM: Language-based Localization and 3D Reasoning with Vision-Language Models (Score: 7/10)
- **💡 Innovation**: The framework introduces a dual-objective spatial supervision mechanism—global layout reconstruction and egocentric situation modeling—to ground 2D Vision-Language Models in 3D space using monocular video and camera pose priors.
- **⚠️ Limitations**: The reliance on pre-trained 3D foundation models for camera pose priors may introduce error propagation, and the paper does not explicitly demonstrate closed-loop control or real-time performance in dynamic robotic manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.18002v1)
- **👥 Authors**: Kevin Qu, Haozhe Qi, Mihai Dusmanu, Mahdi Rad, Rui Wang, Marc Pollefeys
- **🏷️ Tags**: #Foundation_Model #LLM #Embodied_AI

---

### ✨ Specification-Aware Distribution Shaping for Robotics Foundation Models (Score: 7/10)
- **💡 Innovation**: The paper introduces a framework that enforces Signal Temporal Logic (STL) constraints on pretrained robotics foundation models via action distribution optimization without requiring model fine-tuning.
- **⚠️ Limitations**: The reliance on forward dynamics propagation for horizon reasoning may introduce significant computational overhead or inaccuracies if the world model is not perfectly aligned with the environment.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17969v1)
- **👥 Authors**: Sadık Bera Yüksel, Derya Aksaray
- **🏷️ Tags**: #Robot_Manipulation #Foundation_Model #Embodied_AI #World_Model

---

### ✨ WorldCam: Interactive Autoregressive 3D Gaming Worlds with Camera Pose as a Unifying Geometric Representation (Score: 7/10)
- **💡 Innovation**: The paper introduces a unifying geometric representation by using 6-DoF camera poses in Lie algebra to ground action control and enable long-term 3D spatial consistency in autoregressive video generation.
- **⚠️ Limitations**: The approach focuses primarily on camera-centric navigation in gaming environments, which may not directly translate to the complex physical dynamics and contact-rich interactions required for general-purpose robot manipulation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16871)
- **👥 Authors**: Jisu Nam, Yicong Hong, Chun-Hao Paul Huang, Feng Liu, JoungBin Lee, Jiyoung Kim, Siyoon Jin, Yunsung Lee, Jaeyoon Jung, Suhwan Choi, Seungryong Kim, Yang Zhou
- **🏷️ Tags**: #World_Model #Diffusion_Model #Embodied_AI

---

### ✨ Anticipatory Planning for Multimodal AI Agents (Score: 7/10)
- **💡 Innovation**: TraceR1 introduces a two-stage reinforcement learning framework that decouples trajectory-level anticipatory reasoning from step-level execution refinement to improve long-horizon planning coherence.
- **⚠️ Limitations**: The reliance on frozen tool agents for the second stage of fine-tuning may limit the agent's ability to adapt to novel environments where tool dynamics are not pre-defined or static.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16777)
- **👥 Authors**: Yongyuan Liang, Shijie Zhou, Yu Gu, Hao Tan, Gang Wu, Franck Dernoncourt, Jihyung Kil, Ryan A. Rossi, Ruiyi Zhang
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model #Embodied_AI

---

### ✨ Chain-of-Trajectories: Unlocking the Intrinsic Generative Optimality of Diffusion Models via Graph-Theoretic Planning (Score: 7/10)
- **💡 Innovation**: The paper introduces a train-free framework that treats diffusion denoising as a graph-theoretic planning problem by using 'Diffusion DNA' to dynamically allocate computational resources across the sampling trajectory.
- **⚠️ Limitations**: The reliance on a heuristic proxy (Diffusion DNA) for high-dimensional state complexity may not generalize across diverse, non-stationary robotic manipulation tasks where the 'difficulty' of a trajectory is highly context-dependent.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14704)
- **👥 Authors**: Ping Chen, Xiang Liu, Xingpeng Zhang, Fei Shen, Xun Gong, Zhaoxiang Liu, Zezhou Chen, Huan Hu, Kai Wang, Shiguo Lian
- **🏷️ Tags**: #Diffusion_Model #Embodied_AI #Robot_Manipulation

---

### ✨ Unified Spatio-Temporal Token Scoring for Efficient Video VLMs (Score: 6/10)
- **💡 Innovation**: The paper introduces a unified, architecture-wide token pruning module (STTS) that simultaneously prunes vision tokens in both the ViT and LLM layers using a joint spatio-temporal scoring mechanism without requiring text-conditioned selection.
- **⚠️ Limitations**: The evaluation is restricted to video QA tasks, leaving the efficacy and potential performance degradation of this pruning strategy in high-precision, closed-loop embodied control or VLA tasks unverified.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.18004v1)
- **👥 Authors**: Jianrui Zhang, Yue Yang, Rohun Tripathi, Winson Han, Ranjay Krishna, Christopher Clark, Yong Jae Lee, Sangho Lee
- **🏷️ Tags**: #VLA #Foundation_Model #LLM

---

### ✨ Universal Skeleton Understanding via Differentiable Rendering and MLLMs (Score: 6/10)
- **💡 Innovation**: The paper introduces a differentiable, format-agnostic renderer (DrAction) that translates arbitrary skeletal kinematics into visual tokens, enabling MLLMs to process non-visual motion data without lossy compression.
- **⚠️ Limitations**: The reliance on a rendering-based bridge may introduce artifacts or lose high-frequency temporal dynamics that are critical for complex, fine-grained robotic manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.18003v1)
- **👥 Authors**: Ziyi Wang, Peiming Li, Xinshun Wang, Yang Tang, Kai-Kuang Ma, Mengyuan Liu
- **🏷️ Tags**: #LLM #Foundation_Model #Embodied_AI

---

### ✨ Feeling the Space: Egomotion-Aware Video Representation for Efficient and Accurate 3D Scene Understanding (Score: 6/10)
- **💡 Innovation**: The paper introduces an egomotion-aware framework that integrates IMU data into MLLMs via a cascaded keyframe filtering module and asymmetric cross-modal fusion to resolve 3D spatial ambiguities without explicit 3D reconstruction.
- **⚠️ Limitations**: The reliance on IMU data limits the model's applicability to platforms equipped with specific inertial sensors, and the paper does not explicitly demonstrate closed-loop robot control or manipulation capabilities.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17980v1)
- **👥 Authors**: Shuyao Shi, Kang G. Shin
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #LLM

---

### ✨ Unified Policy Value Decomposition for Rapid Adaptation (Score: 6/10)
- **💡 Innovation**: The paper introduces a bilinear actor-critic decomposition that uses shared, low-dimensional goal embeddings to modulate state-dependent basis functions, enabling zero-shot policy adaptation.
- **⚠️ Limitations**: The evaluation is restricted to a low-dimensional locomotion task in MuJoCo, leaving the scalability and effectiveness of this decomposition in high-dimensional, vision-based robotic manipulation tasks unproven.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17947v1)
- **👥 Authors**: Cristiano Capone, Luca Falorsi, Andrea Ciardiello, Luca Manneschi
- **🏷️ Tags**: #Reinforcement_Learning #Embodied_AI

---

### ✨ AgentProcessBench: Diagnosing Step-Level Process Quality in Tool-Using Agents (Score: 6/10)
- **💡 Innovation**: The paper introduces a systematic, human-annotated benchmark for step-level process verification in tool-using agents, addressing the critical issue of irreversible failure propagation in long-horizon tasks.
- **⚠️ Limitations**: The benchmark is primarily focused on software-based tool use rather than physical robot manipulation, limiting its direct applicability to embodied agents operating in continuous, high-dimensional physical environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14465)
- **👥 Authors**: Shengda Fan, Xuyan Ye, Yupeng Huo, Zhi-Yuan Chen, Yiju Guo, Shenzhi Yang, Wenkai Yang, Shuqi Ye, Jingwen Chen, Haotian Chen, Xin Cong, Yankai Lin
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ M^3: Dense Matching Meets Multi-View Foundation Models for Monocular Gaussian Splatting SLAM (Score: 6/10)
- **💡 Innovation**: The paper introduces a dedicated matching head to multi-view foundation models to refine pixel-level correspondences, enabling higher precision geometric optimization within a 3D Gaussian Splatting SLAM framework.
- **⚠️ Limitations**: The approach focuses primarily on static scene reconstruction and pose estimation, lacking explicit integration with embodied control loops or dynamic interaction capabilities required for robotic manipulation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16844)
- **👥 Authors**: Kerui Ren, Guanghao Li, Changjian Jiang, Yingxiang Xu, Tao Lu, Linning Xu, Junting Dong, Jiangmiao Pang, Mulin Yu, Bo Dai
- **🏷️ Tags**: #3D_Gaussian_Splatting #Foundation_Model

---

### ✨ FlashSampling: Fast and Memory-Efficient Exact Sampling (Score: 6/10)
- **💡 Innovation**: FlashSampling introduces a fused, tiled kernel that performs exact categorical sampling directly within the LM-head matrix multiplication, eliminating the need to materialize large logit tensors in HBM.
- **⚠️ Limitations**: The performance gains are primarily focused on the decoding phase of large-vocabulary LLMs and may offer diminishing returns for smaller models or architectures where the LM-head is not the primary bottleneck.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15854)
- **👥 Authors**: Tomas Ruiz, Zhen Qin, Yifan Zhang, Xuyang Shen, Yiran Zhong, Mengdi Wang
- **🏷️ Tags**: #LLM #Foundation_Model #VLA

---

### ✨ OneWorld: Taming Scene Generation with 3D Unified Representation Autoencoder (Score: 6/10)
- **💡 Innovation**: The paper introduces a 3D Unified Representation Autoencoder (3D-URAE) that performs diffusion directly in a 3D latent space, enforced by cross-view correspondence and manifold-drift forcing to ensure geometric and appearance consistency.
- **⚠️ Limitations**: The paper focuses primarily on static scene generation and lacks evaluation on dynamic, interactive, or embodied tasks, which are essential for downstream robotics applications.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16099)
- **👥 Authors**: Sensen Gao, Zhaoqing Wang, Qihang Cao, Dongdong Yu, Changhu Wang, Tongliang Liu, Mingming Gong, Jiawang Bian
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #Embodied_AI

---

### ✨ AgentFactory: A Self-Evolving Framework Through Executable Subagent Accumulation and Reuse (Score: 5/10)
- **💡 Innovation**: The paper introduces a self-evolution paradigm that archives successful task solutions as reusable, executable Python subagent code rather than relying on textual prompts or reflections.
- **⚠️ Limitations**: The framework lacks integration with physical sensor feedback loops or low-level control primitives, limiting its direct applicability to complex, real-world robotic manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.18000v1)
- **👥 Authors**: Zhang Zhang, Shuqi Lu, Hongjin Qian, Di He, Zheng Liu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ SegFly: A 2D-3D-2D Paradigm for Aerial RGB-Thermal Semantic Segmentation at Scale (Score: 5/10)
- **💡 Innovation**: The paper introduces a geometry-driven 2D-3D-2D paradigm that automates large-scale RGB-T semantic segmentation and cross-modal alignment by propagating labels through a sparse 3D point cloud.
- **⚠️ Limitations**: The reliance on high-overlap multi-view imagery and geo-referenced data may limit applicability in dynamic environments or scenarios where camera motion is insufficient for accurate 3D reconstruction.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17920v1)
- **👥 Authors**: Markus Gross, Sai Bharadhwaj Matha, Rui Song, Viswanathan Muthuveerappan, Conrad Christoph, Julius Huber, Daniel Cremers
- **🏷️ Tags**: #Foundation_Model

---

### ✨ Only relative ranks matter in weight-clustered large language models (Score: 5/10)
- **💡 Innovation**: The paper demonstrates that LLM performance is primarily governed by the relative rank order of weight values rather than their precise magnitudes, enabling effective compression via weight clustering.
- **⚠️ Limitations**: The study focuses exclusively on text-based LLMs, leaving it unclear whether these rank-preservation properties hold for high-dimensional, continuous-action policy heads in VLA or robotic control models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17917v1)
- **👥 Authors**: Borja Aizpurua, Sukhbinder Singh, Román Orús
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ RAMP: Reinforcement Adaptive Mixed Precision Quantization for Efficient On Device LLM Inference (Score: 5/10)
- **💡 Innovation**: RAMP utilizes a Soft Actor-Critic (SAC) reinforcement learning framework to dynamically determine per-layer bit-width assignments for LLM quantization, combined with a Scale Folding technique to stabilize sub-4-bit performance.
- **⚠️ Limitations**: The paper focuses exclusively on LLM inference efficiency and does not address the specific latency or memory constraints inherent to real-time Embodied AI or VLA models, which often require different quantization trade-offs.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17891v1)
- **👥 Authors**: Arpit Singh Gautam, Saurabh Jha
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Efficient Reasoning on the Edge (Score: 5/10)
- **💡 Innovation**: The paper introduces a budget-forcing reinforcement learning approach to prune redundant reasoning traces in small LLMs, combined with dynamic adapter-switching for resource-constrained edge inference.
- **⚠️ Limitations**: The work focuses exclusively on textual reasoning tasks and lacks evaluation on embodied agents or multimodal action-prediction tasks, which are critical for robotics applications.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16867)
- **👥 Authors**: Yelysei Bondarenko, Thomas Hehn, Rob Hesselink, Romain Lepert, Fabio Valerio Massoli, Evgeny Mironov, Leyla Mirvakhabova, Tribhuvanesh Orekondy, Spyridon Stasis, Andrey Kuzmin, Anna Kuzina, Markus Nagel, Ankita Nayak, Corrado Rainone, Ork de Rooij, Paul N Whatmough, Arash Behboodi, Babak Ehteshami Bejnordi
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ V-Co: A Closer Look at Visual Representation Alignment via Co-Denoising (Score: 5/10)
- **💡 Innovation**: The paper introduces a systematic, unified framework for visual co-denoising that isolates four essential design ingredients—dual-stream architecture, CFG structure, perceptual-drifting hybrid loss, and RMS-based calibration—to improve pixel-space diffusion training.
- **⚠️ Limitations**: The study is restricted to static image generation on ImageNet and lacks evaluation on downstream embodied tasks or temporal consistency, which are critical for robotics and world modeling applications.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16792)
- **👥 Authors**: Han Lin, Xichen Pan, Zun Wang, Yue Zhang, Chu Wang, Jaemin Cho, Mohit Bansal
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ SuperLocalMemory V3: Information-Geometric Foundations for Zero-LLM Enterprise Agent Memory (Score: 5/10)
- **💡 Innovation**: The paper introduces a formal mathematical framework for agent memory using information geometry (Fisher information), stochastic dynamics (Langevin dynamics), and sheaf theory to replace heuristic-based retrieval and decay mechanisms.
- **⚠️ Limitations**: The paper lacks empirical validation in embodied or robotic contexts, focusing exclusively on conversational dialogue benchmarks (LoCoMo) rather than the physical interaction or state-tracking tasks relevant to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14588)
- **👥 Authors**: Varun Pratap Bhardwaj
- **🏷️ Tags**: #Foundation_Model #LLM

---

### 📄 AHOY! Animatable Humans under Occlusion from YouTube Videos with Gaussian Splatting and Video Diffusion Priors (Score: 4/10)
- **💡 Innovation**: The paper introduces a hallucination-as-supervision pipeline using identity-finetuned diffusion models to reconstruct occluded body regions in 3D Gaussian avatars from monocular in-the-wild video.
- **⚠️ Limitations**: The method relies on generative priors which may introduce artifacts or identity drift in unobserved regions, and it lacks integration with physical interaction or robotic control frameworks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17975v1)
- **👥 Authors**: Aymen Mir, Riza Alp Guler, Xiangjun Tang, Peter Wonka, Gerard Pons-Moll
- **🏷️ Tags**: #3D_Gaussian_Splatting #Diffusion_Model

---

### 📄 Operator-Theoretic Foundations and Policy Gradient Methods for General MDPs with Unbounded Costs (Score: 4/10)
- **💡 Innovation**: The paper provides a rigorous operator-theoretic framework to generalize policy gradient methods and PPO-type algorithms to MDPs with general state/action spaces and unbounded costs.
- **⚠️ Limitations**: The work is highly theoretical and lacks empirical validation in complex embodied or robotic environments, making its practical utility for current VLA or robot manipulation research unclear.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17875v1)
- **👥 Authors**: Abhishek Gupta, Aditya Mahajan
- **🏷️ Tags**: #Reinforcement_Learning

---

### 📄 Procedural Generation of Algorithm Discovery Tasks in Machine Learning (Score: 4/10)
- **💡 Innovation**: The paper introduces a procedural generation framework (DiscoGen) to create a diverse, scalable suite of machine learning algorithm discovery tasks, moving away from static, saturated benchmarks.
- **⚠️ Limitations**: The work focuses exclusively on algorithmic optimization (e.g., loss functions, optimizers) rather than physical agent control, making it largely tangential to embodied robotics or VLA-based manipulation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17863v1)
- **👥 Authors**: Alexander D. Goldie, Zilin Wang, Adrian Hayler, Deepak Nathani, Edan Toledo, Ken Thampiratwong, Aleksandra Kalisz, Michael Beukman, Alistair Letcher, Shashank Reddy, Clarisse Wibault, Theo Wolf, Charles O'Neill, Uljad Berdica, Nicholas Roberts, Saeed Rahmani, Hannah Erlebach, Roberta Raileanu, Shimon Whiteson, Jakob N. Foerster
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### 📄 One-Eval: An Agentic System for Automated and Traceable LLM Evaluation (Score: 4/10)
- **💡 Innovation**: The paper introduces an agentic framework that automates the end-to-end evaluation pipeline for LLMs by translating natural language requests into executable, traceable workflows.
- **⚠️ Limitations**: The system is focused on general-purpose LLM evaluation and lacks specific integration or benchmarks for embodied tasks, robot manipulation, or multimodal action-space evaluation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09821)
- **👥 Authors**: Chengyu Shen, Yanheng Hou, Minghui Pan, Runming He, Zhen Hao Wong, Meiyi Qiang, Zhou Liu, Hao Liang, Peichao Lai, Zeang Sheng, Wentao Zhang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Reliable Reasoning in SVG-LLMs via Multi-Task Multi-Reward Reinforcement Learning (Score: 4/10)
- **💡 Innovation**: The paper introduces a chain-of-thought mechanism combined with multi-reward reinforcement learning (GRPO) to improve the structural coherence and efficiency of SVG code generation.
- **⚠️ Limitations**: The work is strictly focused on 2D vector graphics generation and lacks any connection to physical embodiment, robot control, or spatial reasoning required for robotics tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16189)
- **👥 Authors**: Haomin Wang, Qi Wei, Qianli Ma, Shengyuan Ding, Jinhui Yin, Kai Chen, Hongjie Zhang
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 ViT-AdaLA: Adapting Vision Transformers with Linear Attention (Score: 4/10)
- **💡 Innovation**: The paper introduces a three-stage adaptation framework (attention alignment, feature alignment, and supervised fine-tuning) to distill knowledge from softmax-based Vision Transformers into linear attention architectures.
- **⚠️ Limitations**: The work focuses exclusively on static vision tasks (classification/segmentation) and lacks evaluation on temporal or embodied benchmarks, which are critical for high-resolution robotics applications.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16063)
- **👥 Authors**: Yifan Li, Seunghyun Yoon, Viet Dac Lai, Franck Dernoncourt, Jason Kuen, Yu Kong, Trung Bui
- **🏷️ Tags**: #Foundation_Model

---

### 📄 I Know What I Don't Know: Latent Posterior Factor Models for Multi-Evidence Probabilistic Reasoning (Score: 4/10)
- **💡 Innovation**: The paper introduces Latent Posterior Factors (LPF), a framework that integrates VAE latent posteriors into Sum-Product Networks to enable tractable, calibrated probabilistic reasoning over unstructured data.
- **⚠️ Limitations**: The work focuses on abstract decision-making and evidence aggregation tasks, lacking any direct application or evaluation in embodied, physical, or robotic environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15670)
- **👥 Authors**: Aliyu Agboola Alege
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 MDM-Prime-v2: Binary Encoding and Index Shuffling Enable Compute-optimal Scaling of Diffusion Language Models (Score: 4/10)
- **💡 Innovation**: The paper introduces Binary Encoding and Index Shuffling to the MDM-Prime framework to improve sub-token granularity and likelihood estimation in masked diffusion language models.
- **⚠️ Limitations**: The work focuses exclusively on text-based language modeling and lacks any evaluation or discussion regarding embodied agents, robot manipulation, or multi-modal action prediction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16077)
- **👥 Authors**: Chen-Hao Chao, Wei-Fang Sun, Junwei Qua, Chun-Yi Lee, Rahul G. Krishnan
- **🏷️ Tags**: #Diffusion_Model #LLM #Foundation_Model

---

### 📄 Interpretable Traffic Responsibility from Dashcam Video via Legal Multi Agent Reasoning (Score: 3/10)
- **💡 Innovation**: The paper introduces a multi-agent framework that bridges video-based traffic accident perception with legal reasoning by aligning dashcam footage with specific Chinese traffic statutes.
- **⚠️ Limitations**: The work focuses on high-level legal reasoning and semantic understanding rather than the low-level control, physical interaction, or embodied decision-making relevant to robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17930v1)
- **👥 Authors**: Jingchun Yang, Jinchang Zhang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Mitigating LLM Hallucinations through Domain-Grounded Tiered Retrieval (Score: 3/10)
- **💡 Innovation**: The paper introduces a four-phase, self-regulating LangGraph pipeline that integrates intrinsic verification, adaptive search routing, and corrective document grading to mitigate LLM hallucinations.
- **⚠️ Limitations**: The research is strictly focused on textual factual accuracy and lacks any integration with physical grounding, multi-modal perception, or action-space reasoning required for embodied systems.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17872v1)
- **👥 Authors**: Md. Asraful Haque, Aasar Mehdi, Maaz Mahboob, Tamkeen Fatima
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 TRUST-SQL: Tool-Integrated Multi-Turn Reinforcement Learning for Text-to-SQL over Unknown Schemas (Score: 3/10)
- **💡 Innovation**: The paper introduces a Dual-Track GRPO strategy with token-level masked advantages to improve credit assignment in multi-turn, tool-integrated SQL generation tasks.
- **⚠️ Limitations**: The work is strictly focused on database query generation and lacks any connection to physical agents, sensorimotor control, or embodied environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16448)
- **👥 Authors**: Ai Jian, Xiaoyun Zhang, Wanrou Du, Jingqing Ruan, Jiangbo Pei, Weipeng Zhang, Ke Zeng, Xunliang Cai
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 MEMO: Memory-Augmented Model Context Optimization for Robust Multi-Turn Multi-Agent LLM Games (Score: 3/10)
- **💡 Innovation**: The paper introduces a memory-augmented self-play framework that optimizes inference-time context for LLMs in multi-agent games using TrueSkill-based uncertainty selection and prioritized replay.
- **⚠️ Limitations**: The work is strictly confined to text-based games and lacks any grounding in physical environments, sensorimotor control, or embodied decision-making.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09022)
- **👥 Authors**: Yunfei Xie, Kevin Wang, Bobby Cheng, Jianzhu Yao, Zhizhou Sha, Alexander Duffy, Yihan Xi, Hongyuan Mei, Cheston Tan, Chen Wei, Pramod Viswanath, Zhangyang Wang
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World Software Engineering? (Score: 3/10)
- **💡 Innovation**: The paper introduces a systematic, requirement-driven benchmark to quantify the marginal utility of procedural 'agent skills' in software engineering tasks through deterministic execution-based verification.
- **⚠️ Limitations**: The work is entirely focused on software engineering agents and lacks any connection to physical embodiment, sensorimotor control, or the specific challenges of real-world robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15401)
- **👥 Authors**: Tingxu Han, Yi Zhang, Wei Song, Chunrong Fang, Zhenyu Chen, Youcheng Sun, Lijie Hu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Sparking Scientific Creativity via LLM-Driven Interdisciplinary Inspiration (Score: 3/10)
- **💡 Innovation**: The paper introduces a framework that uses LLMs to systematically bridge interdisciplinary research by decomposing domain-specific challenges into abstract conceptual problems to retrieve analogous solutions from disparate fields.
- **⚠️ Limitations**: The framework is purely conceptual and linguistic, lacking any grounding in physical environments, sensorimotor data, or the specific constraints required for embodied robotics or control tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12226)
- **👥 Authors**: Priyanka Kargupta, Shuhaib Mehri, Dilek Hakkani-Tur, Jiawei Han
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 ECG-Reasoning-Benchmark: A Benchmark for Evaluating Clinical Reasoning Capabilities in ECG Interpretation (Score: 3/10)
- **💡 Innovation**: The paper introduces a specialized multi-turn evaluation framework to audit the logical reasoning chains of MLLMs in the specific domain of clinical ECG interpretation.
- **⚠️ Limitations**: The research is strictly focused on medical diagnostics and lacks any connection to physical agency, spatial reasoning, or sensorimotor control relevant to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14326)
- **👥 Authors**: Jungwoo Oh, Hyunseung Chung, Junhee Lee, Min-Gyu Kim, Hangyul Yoon, Ki Seong Lee, Youngchae Lee, Muhan Yeo, Edward Choi
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 ARISE: Agent Reasoning with Intrinsic Skill Evolution in Hierarchical Reinforcement Learning (Score: 3/10)
- **💡 Innovation**: The paper introduces a hierarchical reinforcement learning framework that uses a 'Skills Manager' to distill successful mathematical reasoning traces into a reusable library for future problem-solving.
- **⚠️ Limitations**: The work is strictly focused on mathematical reasoning and symbolic problem-solving, lacking any grounding in physical environments, sensorimotor control, or embodied interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16060)
- **👥 Authors**: Yu Li, Rui Miao, Zhengling Qi, Tian Lan
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 LaDe: Unified Multi-Layered Graphic Media Generation and Decomposition (Score: 2/10)
- **💡 Innovation**: The paper introduces a latent diffusion framework that utilizes an LLM-based prompt expander and a 4D RoPE positional encoding mechanism to generate and decompose layered graphic media.
- **⚠️ Limitations**: The work is entirely focused on 2D graphic design generation and lacks any connection to spatial reasoning, physical interaction, or embodied control tasks relevant to robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17965v1)
- **👥 Authors**: Vlad-Constantin Lungu-Stan, Ionut Mironica, Mariana-Iuliana Georgescu
- **🏷️ Tags**: #Diffusion_Model #LLM #Foundation_Model

---

### 📄 IndicSafe: A Benchmark for Evaluating Multilingual LLM Safety in South Asia (Score: 2/10)
- **💡 Innovation**: The paper introduces a systematic safety benchmark for LLMs specifically tailored to 12 underrepresented Indic languages and culturally specific harm categories.
- **⚠️ Limitations**: The work focuses exclusively on text-based safety alignment and lacks any connection to embodied agents, multimodal perception, or physical world interaction.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17915v1)
- **👥 Authors**: Priyaranjan Pattnayak, Sanchari Chowdhuri
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Differential Privacy in Generative AI Agents: Analysis and Optimal Tradeoffs (Score: 2/10)
- **💡 Innovation**: The paper introduces a probabilistic framework to quantify privacy leakage in LLM-based agents by applying differential privacy to token generation mechanisms.
- **⚠️ Limitations**: The work is strictly focused on text-based LLM privacy and lacks any connection to embodied agents, physical state spaces, or multimodal action generation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17902v1)
- **👥 Authors**: Ya-Ting Yang, Quanyan Zhu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 scicode-lint: Detecting Methodology Bugs in Scientific Python Code with LLM-Generated Patterns (Score: 2/10)
- **💡 Innovation**: The paper introduces a two-tier architecture that uses frontier LLMs to automatically generate and update static analysis patterns for scientific Python code, decoupling pattern design from runtime execution.
- **⚠️ Limitations**: The methodology is strictly focused on software engineering and static code analysis, offering no contribution to embodied intelligence, physical interaction, or decision-making in robotic systems.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17893v1)
- **👥 Authors**: Sergey V. Samsonau
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Revisiting foundation models for cell instance segmentation (Score: 2/10)
- **💡 Innovation**: The paper introduces an automatic prompt generation (APG) strategy to enhance the performance of SAM-based foundation models specifically for cell instance segmentation in microscopy.
- **⚠️ Limitations**: The work is strictly focused on biological image analysis and lacks any connection to embodied agents, physical interaction, or the robotics-specific paradigms requested.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17845v1)
- **👥 Authors**: Anwai Archit, Constantin Pape
- **🏷️ Tags**: #Foundation_Model

---

### 📄 FinToolBench: Evaluating LLM Agents for Real-World Financial Tool Use (Score: 2/10)
- **💡 Innovation**: The paper introduces a domain-specific benchmark for evaluating LLM-based agentic tool use within the financial sector, focusing on regulatory compliance and real-world API execution.
- **⚠️ Limitations**: The work is entirely focused on digital financial agents and lacks any connection to physical embodiment, sensorimotor control, or the spatial reasoning required for robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08262)
- **👥 Authors**: Jiaxuan Lu, Kong Wang, Yemin Wang, Qingmei Tang, Hongwei Zeng, Xiang Chen, Jiahao Pi, Shujian Deng, Lingzhi Chen, Yi Fu, Kehua Yang, Xiao Sun
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Semi-Autonomous Formalization of the Vlasov-Maxwell-Landau Equilibrium (Score: 2/10)
- **💡 Innovation**: The paper demonstrates a fully automated, agentic workflow for formalizing complex mathematical proofs in Lean 4 using LLM-based reasoning and coding agents.
- **⚠️ Limitations**: The work is entirely focused on formal mathematics and automated theorem proving, offering no contribution to physical robot control, perception, or embodied decision-making.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15929)
- **👥 Authors**: Vasily Ilin
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Omnilingual MT: Machine Translation for 1,600 Languages (Score: 2/10)
- **💡 Innovation**: The paper introduces a specialized training strategy for LLMs to achieve high-fidelity machine translation across 1,600 languages, significantly outperforming larger general-purpose baselines.
- **⚠️ Limitations**: The work is entirely focused on natural language processing and lacks any connection to visual perception, motor control, or embodied interaction, making it irrelevant to robotics research.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.16309)
- **👥 Authors**: Omnilingual MT Team, Belen Alastruey, Niyati Bafna, Andrea Caciolai, Kevin Heffernan, Artyom Kozhevnikov, Christophe Ropers, Eduardo Sánchez, Charles-Eric Saint-James, Ioannis Tsiamas, Chierh Cheng, Joe Chuang, Paul-Ambroise Duquenne, Mark Duppenthaler, Nate Ekberg, Cynthia Gao, Pere Lluís Huguet Cabot, João Maria Janeiro, Jean Maillard, Gabriel Mejia Gonzalez, Holger Schwenk, Edan Toledo, Arina Turkatenko, Albert Ventayol-Boada, Rashel Moritz, Alexandre Mourachko, Surya Parimi, Mary Williamson, Shireen Yates, David Dale, Marta R. Costa-jussà
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 VAREX: A Benchmark for Multi-Modal Structured Extraction from Documents (Score: 2/10)
- **💡 Innovation**: The paper introduces a benchmark for structured data extraction from government forms using a 'Reverse Annotation' pipeline to generate synthetic ground truth across four distinct input modalities.
- **⚠️ Limitations**: The research focuses exclusively on document processing and structured data extraction, offering no direct application or methodology relevant to embodied agents, robot manipulation, or physical world modeling.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15118)
- **👥 Authors**: Udi Barzelay, Ophir Azulai, Inbar Shapira, Idan Friedman, Foad Abo Dahood, Madison Lee, Abraham Daniels
- **🏷️ Tags**: #Foundation_Model #LLM

---

### 📄 Test-Time Strategies for More Efficient and Accurate Agentic RAG (Score: 2/10)
- **💡 Innovation**: The paper introduces test-time contextualization and de-duplication modules to optimize the iterative retrieval process in agentic RAG systems.
- **⚠️ Limitations**: The work is entirely focused on text-based information retrieval and reasoning, lacking any connection to embodied agents, physical world interaction, or multimodal perception.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12396)
- **👥 Authors**: Brian Zhang, Deepti Guntur, Zhiyang Zuo, Abhinav Sharma, Shreyas Chaudhari, Wenlong Zhao, Franck Dernoncourt, Puneet Mathur, Ryan Rossi, Nedim Lipka
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 AI-Assisted Goal Setting Improves Goal Progress Through Social Accountability (Score: 1/10)
- **💡 Innovation**: The study investigates the psychological impact of LLM-based coaching on human goal attainment, specifically identifying 'perceived social accountability' as a key mediator.
- **⚠️ Limitations**: The paper is entirely focused on human-computer interaction in a psychological context and contains no technical contributions related to robotics, physical embodiment, or control systems.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.17887v1)
- **👥 Authors**: Michel Schimpf, Julian Voigt, Thomas Bohné
- **🏷️ Tags**: #LLM #Foundation_Model

---


