# 📅 2026-03-17 - Paper Digest
## Summary
Total Papers: 44 | High Impact: 9

## 📝 Papers List
### 🔥 DreamPlan: Efficient Reinforcement Fine-Tuning of Vision-Language Planners via Video World Models (Score: 8/10)
- **💡 Innovation**: DreamPlan enables sample-efficient reinforcement fine-tuning of VLM planners by training an action-conditioned video world model on sub-optimal exploratory data and performing policy optimization entirely within the model's imagination.
- **⚠️ Limitations**: The framework's performance is heavily bottlenecked by the fidelity and long-horizon consistency of the video world model, which may struggle with complex contact dynamics or occlusions inherent in deformable object manipulation.
- **🔗 Link**: [[DreamPlan]]
- **👥 Authors**: Emily Yue-Ting Jia, Weiduo Yuan, Tianheng Shi, Vitor Guizilini, Jiageng Mao, Yue Wang
- **🏷️ Tags**: #Robot_Manipulation #World_Model #Reinforcement_Learning #Embodied_AI #Foundation_Model

---

### 🔥 Towards Generalizable Robotic Manipulation in Dynamic Environments (Score: 8/10)
- **💡 Innovation**: The paper introduces a dynamics-aware VLA architecture (PUMA) that leverages scene-centric historical optical flow and world queries to implicitly forecast object-centric future states for improved performance in dynamic environments.
- **⚠️ Limitations**: The reliance on optical flow as a primary mechanism for temporal reasoning may struggle with occlusions or rapid, non-linear object movements compared to more explicit latent world models.
- **🔗 Link**: [[Towards Generalizable Robotic Manipulation in Dynamic Environments]]
- **👥 Authors**: Heng Fang, Shangru Li, Shuhan Wang, Xuanyang Xi, Dingkang Liang, Xiang Bai
- **🏷️ Tags**: #Robot_Manipulation #VLA #Embodied_AI #Foundation_Model #World_Model

---

### 🔥 OxyGen: Unified KV Cache Management for Vision-Language-Action Models under Multi-Task Parallelism (Score: 8/10)
- **💡 Innovation**: The paper introduces a unified KV cache management paradigm that enables cross-task KV sharing and cross-frame continuous batching to optimize multi-task inference in Mixture-of-Transformers VLAs.
- **⚠️ Limitations**: The evaluation is currently limited to the π0.5 architecture, and it remains to be seen how the unified cache management scales to larger, more diverse MoT models or varying hardware constraints.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14371)
- **👥 Authors**: Xiangyu Li, Huaizhi Tang, Xin Ding, Weijun Wang, Ting Cao, Yunxin Liu
- **🏷️ Tags**: #VLA #Embodied_AI #Robot_Manipulation #Foundation_Model #LLM

---

### ✨ WorldCam: Interactive Autoregressive 3D Gaming Worlds with Camera Pose as a Unifying Geometric Representation (Score: 7/10)
- **💡 Innovation**: The paper introduces a unifying geometric representation by using 6-DoF camera poses in Lie algebra to ground action control and enable spatial indexing for long-horizon consistency in generative world models.
- **⚠️ Limitations**: The approach is primarily validated on gaming environments, leaving the transferability to real-world robotic sensorimotor control and complex physical interaction dynamics unproven.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16871v1)
- **👥 Authors**: Jisu Nam, Yicong Hong, Chun-Hao Paul Huang, Feng Liu, JoungBin Lee, Jiyoung Kim, Siyoon Jin, Yunsung Lee, Jaeyoon Jung, Suhwan Choi, Seungryong Kim, Yang Zhou
- **🏷️ Tags**: #World_Model #Diffusion_Model #Embodied_AI

---

### ✨ CABTO: Context-Aware Behavior Tree Grounding for Robot Manipulation (Score: 7/10)
- **💡 Innovation**: CABTO introduces a framework that automates the grounding of Behavior Trees by using LLMs to heuristically search and synthesize action models and control policies, bridging the gap between high-level planning and low-level execution.
- **⚠️ Limitations**: The reliance on LLM heuristics for policy generation may struggle with complex, long-horizon tasks requiring precise physical constraints or high-frequency reactive control that LLMs are not inherently optimized to verify.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16809v1)
- **👥 Authors**: Yishuai Cai, Xinglin Chen, Yunxin Mao, Kun Hu, Minglong Li, Yaodong Yang, Yuanpei Chen
- **🏷️ Tags**: #Robot_Manipulation #LLM #Embodied_AI #Foundation_Model

---

### ✨ Anticipatory Planning for Multimodal AI Agents (Score: 7/10)
- **💡 Innovation**: TraceR1 introduces a two-stage reinforcement learning framework that decouples trajectory-level anticipatory reasoning from step-level execution refinement to improve long-horizon planning coherence.
- **⚠️ Limitations**: The reliance on frozen tool agents for the second stage of fine-tuning may limit the agent's ability to adapt to novel environments where tool dynamics are not pre-defined or static.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16777v1)
- **👥 Authors**: Yongyuan Liang, Shijie Zhou, Yu Gu, Hao Tan, Gang Wu, Franck Dernoncourt, Jihyung Kil, Ryan A. Rossi, Ruiyi Zhang
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model #Embodied_AI

---

### ✨ Grounding World Simulation Models in a Real-World Metropolis (Score: 7/10)
- **💡 Innovation**: The paper introduces a retrieval-augmented world model that grounds video generation in real-world geographic data using a Virtual Lookahead Sink to maintain long-horizon spatial consistency.
- **⚠️ Limitations**: The reliance on pre-captured street-view imagery limits the model's ability to handle dynamic, non-static urban changes or novel, unseen environments not covered by the retrieval database.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15583)
- **👥 Authors**: Junyoung Seo, Hyunwook Choi, Minkyung Kwon, Jinhyeok Choi, Siyoon Jin, Gayoung Lee, Junho Kim, JoungBin Lee, Geonmo Gu, Dongyoon Han, Sangdoo Yun, Seungryong Kim, Jin-Hwa Kim
- **🏷️ Tags**: #World_Model #Sim2Real #Embodied_AI

---

### ✨ HSImul3R: Physics-in-the-Loop Reconstruction of Simulation-Ready Human-Scene Interactions (Score: 7/10)
- **💡 Innovation**: The paper introduces a bi-directional optimization framework that integrates physics simulation feedback into the 3D reconstruction process to ensure human-scene interactions are physically stable for embodied agents.
- **⚠️ Limitations**: The reliance on physics-in-the-loop optimization is computationally expensive and may struggle with complex, non-rigid, or highly dynamic interactions that exceed the stability limits of current simulators.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15612)
- **👥 Authors**: Yukang Cao, Haozhe Xie, Fangzhou Hong, Long Zhuo, Zhaoxi Chen, Liang Pan, Ziwei Liu
- **🏷️ Tags**: #Embodied_AI #Sim2Real #Reinforcement_Learning

---

### ✨ Panoramic Affordance Prediction (Score: 7/10)
- **💡 Innovation**: The paper introduces a novel panoramic affordance prediction framework that uses a training-free, coarse-to-fine recursive visual routing mechanism to handle the geometric distortions and high-resolution demands of 360-degree imagery.
- **⚠️ Limitations**: The current approach is purely perception-focused and lacks integration with closed-loop control or temporal consistency, which are essential for real-world robot manipulation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15558)
- **👥 Authors**: Zixin Zhang, Chenfei Liao, Hongfei Zhang, Harold Haodong Chen, Kanghao Chen, Zichen Wen, Litao Guo, Bin Ren, Xu Zheng, Yinchuan Li, Xuming Hu, Nicu Sebe, Ying-Cong Chen
- **🏷️ Tags**: #Embodied_AI #Robot_Manipulation #Foundation_Model

---

### ✨ M^3: Dense Matching Meets Multi-View Foundation Models for Monocular Gaussian Splatting SLAM (Score: 6/10)
- **💡 Innovation**: The paper introduces a dedicated matching head to multi-view foundation models to refine pixel-level correspondences, enabling higher precision geometric optimization within a 3D Gaussian Splatting SLAM framework.
- **⚠️ Limitations**: The approach relies on monocular video input and may struggle with extreme dynamic occlusions or textureless environments despite the dynamic area suppression mechanism.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16844v1)
- **👥 Authors**: Kerui Ren, Guanghao Li, Changjian Jiang, Yingxiang Xu, Tao Lu, Linning Xu, Junting Dong, Jiangmiao Pang, Mulin Yu, Bo Dai
- **🏷️ Tags**: #3D_Gaussian_Splatting #Foundation_Model

---

### ✨ Stochastic Resetting Accelerates Policy Convergence in Reinforcement Learning (Score: 6/10)
- **💡 Innovation**: The paper introduces stochastic resetting as a formal mechanism to accelerate reinforcement learning convergence by truncating uninformative trajectories and enhancing value propagation, bridging statistical mechanics with RL optimization.
- **⚠️ Limitations**: The evaluation is limited to tabular grid worlds and basic continuous control tasks, lacking demonstration on high-dimensional, complex robotic manipulation or real-world embodied settings.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16842v1)
- **👥 Authors**: Jello Zhou, Vudtiwat Ngampruetikorn, David J. Schwab
- **🏷️ Tags**: #Reinforcement_Learning #Embodied_AI

---

### ✨ Surg$Σ$: A Spectrum of Large-Scale Multimodal Data and Foundation Models for Surgical Intelligence (Score: 6/10)
- **💡 Innovation**: The paper introduces a large-scale, unified multimodal dataset (SurgΣ-DB) and a hierarchical reasoning framework designed to improve cross-task generalization in surgical AI.
- **⚠️ Limitations**: The work focuses primarily on perception, reasoning, and planning, lacking a direct integration with closed-loop robotic control or physical interaction benchmarks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16822v1)
- **👥 Authors**: Zhitao Zeng, Mengya Xu, Jian Jiang, Pengfei Guo, Yunqiu Xu, Zhu Zhuo, Chang Han Low, Yufan He, Dong Yang, Chenxi Lin, Yiming Gu, Jiaxin Guo, Yutong Ban, Daguang Xu, Qi Dou, Yueming Jin
- **🏷️ Tags**: #Foundation_Model #LLM #Embodied_AI

---

### ✨ Attention Residuals (Score: 6/10)
- **💡 Innovation**: The paper introduces Attention Residuals (AttnRes), a mechanism that replaces fixed-weight residual connections with input-dependent softmax attention over preceding layer outputs to mitigate hidden-state dilution.
- **⚠️ Limitations**: The evaluation is restricted to language modeling tasks, leaving the efficacy of this architectural change in multimodal or embodied settings (like VLA models) unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15031)
- **👥 Authors**: Kimi Team, Guangyu Chen, Yu Zhang, Jianlin Su, Weixin Xu, Siyuan Pan, Yaoyu Wang, Yucheng Wang, Guanduo Chen, Bohong Yin, Yutian Chen, Junjie Yan, Ming Wei, Y. Zhang, Fanqing Meng, Chao Hong, Xiaotong Xie, Shaowei Liu, Enzhe Lu, Yunpeng Tai, Yanru Chen, Xin Men, Haiqing Guo, Y. Charles, Haoyu Lu, Lin Sui, Jinguo Zhu, Zaida Zhou, Weiran He, Weixiao Huang, Xinran Xu, Yuzhi Wang, Guokun Lai, Yulun Du, Yuxin Wu, Zhilin Yang, Xinyu Zhou
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Safe and Scalable Web Agent Learning via Recreated Websites (Score: 6/10)
- **💡 Innovation**: The paper introduces a framework that leverages LLMs to automatically clone real-world websites into executable, verifiable synthetic environments, enabling safe and scalable training for web agents.
- **⚠️ Limitations**: The approach relies on the fidelity of the LLM-generated clones, which may fail to capture complex dynamic behaviors or state-dependent interactions present in the original, highly interactive websites.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10505)
- **👥 Authors**: Hyungjoo Chae, Jungsoo Park, Alan Ritter
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning #Sim2Real

---

### ✨ Efficient Reasoning on the Edge (Score: 5/10)
- **💡 Innovation**: The paper introduces a budget-forcing reinforcement learning approach to prune redundant reasoning traces in small LLMs, combined with dynamic adapter-switching for resource-constrained edge inference.
- **⚠️ Limitations**: The work focuses exclusively on textual reasoning tasks and lacks evaluation on embodied or multimodal benchmarks, which are critical for robotics applications.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16867v1)
- **👥 Authors**: Yelysei Bondarenko, Thomas Hehn, Rob Hesselink, Romain Lepert, Fabio Valerio Massoli, Evgeny Mironov, Leyla Mirvakhabova, Tribhuvanesh Orekondy, Spyridon Stasis, Andrey Kuzmin, Anna Kuzina, Markus Nagel, Ankita Nayak, Corrado Rainone, Ork de Rooij, Paul N Whatmough, Arash Behboodi, Babak Ehteshami Bejnordi
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Mixture-of-Depths Attention (Score: 5/10)
- **💡 Innovation**: The paper introduces Mixture-of-Depths Attention (MoDA), which allows attention heads to attend to both current-layer KV pairs and depth-wise KV pairs from preceding layers to mitigate signal degradation in deep models.
- **⚠️ Limitations**: The evaluation is restricted to language modeling benchmarks, leaving the efficacy of this architecture for high-dimensional, multi-modal embodied tasks or VLA models unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15619)
- **👥 Authors**: Lianghui Zhu, Yuxin Fang, Bencheng Liao, Shijie Wang, Tianheng Cheng, Zilong Huang, Chen Chen, Lai Wei, Yutao Zeng, Ya Wang, Yi Lin, Yu Li, Xinggang Wang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Effective Distillation to Hybrid xLSTM Architectures (Score: 5/10)
- **💡 Innovation**: The paper introduces a distillation pipeline that merges linearized experts into a hybrid xLSTM architecture to achieve near-lossless performance recovery from transformer-based teacher models.
- **⚠️ Limitations**: The study focuses exclusively on text-based LLM benchmarks, lacking evaluation on multimodal or embodied tasks that would demonstrate utility for robotics or VLA applications.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15590)
- **👥 Authors**: Lukas Hauzenberger, Niklas Schmidinger, Thomas Schmied, Anamaria-Roberta Hartl, David Stap, Pieter-Jan Hoedt, Maximilian Beck, Sebastian Böck, Günter Klambauer, Sepp Hochreiter
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ ViFeEdit: A Video-Free Tuner of Your Video Diffusion Transformer (Score: 5/10)
- **💡 Innovation**: The paper introduces an architectural reparameterization that decouples spatial attention from 3D attention in video diffusion transformers, allowing for video-level temporal consistency using only 2D image training data.
- **⚠️ Limitations**: The method lacks explicit grounding in physical dynamics or embodied interaction, making its utility for robotics-specific tasks like world modeling or action planning unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15478)
- **👥 Authors**: Ruonan Yu, Zhenxiong Tan, Zigeng Chen, Songhua Liu, Xinchao Wang
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ POLCA: Stochastic Generative Optimization with LLM (Score: 5/10)
- **💡 Innovation**: POLCA introduces a stochastic generative optimization framework that utilizes an LLM as an optimizer, employing a priority queue and epsilon-net mechanism to manage exploration-exploitation and solution diversity in noisy optimization landscapes.
- **⚠️ Limitations**: The paper focuses on software-centric benchmarks (code, agents, prompts) and lacks evaluation on physical robotic systems or high-dimensional continuous control tasks typical of Embodied AI.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14769)
- **👥 Authors**: Xuanfei Ren, Allen Nie, Tengyang Xie, Ching-An Cheng
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ MMOU: A Massive Multi-Task Omni Understanding and Reasoning Benchmark for Long and Complex Real-World Videos (Score: 5/10)
- **💡 Innovation**: The paper introduces a large-scale, manually annotated benchmark (MMOU) specifically designed to evaluate long-form, omni-modal (audio-visual-textual) reasoning in MLLMs.
- **⚠️ Limitations**: The benchmark focuses on passive video understanding and reasoning rather than active interaction, limiting its direct applicability to embodied agents or closed-loop robot control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14145)
- **👥 Authors**: Arushi Goel, Sreyan Ghosh, Vatsal Agarwal, Nishit Anand, Kaousheik Jayakumar, Lasha Koroshinadze, Yao Xu, Katie Lyons, James Case, Karan Sapra, Kevin J. Shih, Siddharth Gururani, Abhinav Shrivastava, Ramani Duraiswami, Dinesh Manocha, Andrew Tao, Bryan Catanzaro, Mohammad Shoeybi, Wei Ping
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ The PokeAgent Challenge: Competitive and Long-Context Learning at Scale (Score: 5/10)
- **💡 Innovation**: The paper introduces a large-scale, multi-modal benchmark for long-horizon planning and game-theoretic reasoning using the Pokemon environment to stress-test LLM and RL agents.
- **⚠️ Limitations**: The benchmark is purely digital and lacks physical grounding, making it less relevant for direct applications in robot manipulation or real-world embodied control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15563)
- **👥 Authors**: Seth Karten, Jake Grigsby, Tersoo Upaa, Junik Bae, Seonghun Hong, Hyunyoung Jeong, Jaeyoon Jung, Kun Kerdthaisong, Gyungbo Kim, Hyeokgi Kim, Yujin Kim, Eunju Kwon, Dongyu Liu, Patrick Mariglia, Sangyeon Park, Benedikt Schink, Xianwei Shi, Anthony Sistilli, Joseph Twin, Arian Urdu, Matin Urdu, Qiao Wang, Ling Wu, Wenli Zhang, Kunsheng Zhou, Stephanie Milani, Kiran Vodrahalli, Amy Zhang, Fei Fang, Yuke Zhu, Chi Jin
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ VisionCoach: Reinforcing Grounded Video Reasoning via Visual-Perception Prompting (Score: 5/10)
- **💡 Innovation**: The paper introduces a training-time visual prompting framework that uses RL and self-distillation to teach models to ground spatio-temporal reasoning without requiring inference-time prompts or external tools.
- **⚠️ Limitations**: The approach is primarily evaluated on video reasoning and understanding benchmarks rather than closed-loop robotic control or physical interaction tasks, limiting its immediate applicability to embodied agents.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14659)
- **👥 Authors**: Daeun Lee, Shoubin Yu, Yue Zhang, Mohit Bansal
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### 📄 What DINO saw: ALiBi positional encoding reduces positional bias in Vision Transformers (Score: 4/10)
- **💡 Innovation**: The paper introduces the use of ALiBi relative positional encoding to mitigate inherent positional biases in Vision Transformers (specifically DINOv2) to improve performance on tasks requiring spatial invariance.
- **⚠️ Limitations**: The study focuses on material science microscopy rather than embodied tasks, leaving the impact on spatial reasoning in robotics or VLA models largely speculative.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16840v1)
- **👥 Authors**: Moritz Pawlowsky, Antonis Vamvakeros, Alexander Weiss, Anja Bielefeld, Samuel J. Cooper, Ronan Docherty
- **🏷️ Tags**: #Foundation_Model

---

### 📄 Learning to Present: Inverse Specification Rewards for Agentic Slide Generation (Score: 4/10)
- **💡 Innovation**: The paper introduces an 'inverse specification reward' mechanism where an LLM acts as a discriminator to recover the original prompt from generated artifacts, providing a self-supervised signal for reinforcement learning.
- **⚠️ Limitations**: The work is strictly confined to digital content generation (HTML slides) and lacks any physical grounding, sensory-motor feedback, or spatial reasoning components relevant to embodied robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16839v1)
- **👥 Authors**: Karthik Ragunath Ananda Kumar, Subrahmanyam Arunachalam
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 V-Co: A Closer Look at Visual Representation Alignment via Co-Denoising (Score: 4/10)
- **💡 Innovation**: The paper introduces a systematic, unified framework for visual co-denoising that isolates four essential design ingredients—dual-stream architecture, CFG structure, perceptual-drifting hybrid loss, and RMS-based calibration—to improve pixel-space diffusion.
- **⚠️ Limitations**: The research is focused exclusively on generative image synthesis on ImageNet and lacks any evaluation or discussion regarding its applicability to embodied tasks, robot manipulation, or temporal consistency required for world models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16792v1)
- **👥 Authors**: Han Lin, Xichen Pan, Zun Wang, Yue Zhang, Chu Wang, Jaemin Cho, Mohit Bansal
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 IOSVLM: A 3D Vision-Language Model for Unified Dental Diagnosis from Intraoral Scans (Score: 4/10)
- **💡 Innovation**: The paper introduces a 3D VLM architecture that processes raw point cloud data from intraoral scans using a geometry-to-chromatic proxy to align 3D geometric features with an LLM for dental diagnosis.
- **⚠️ Limitations**: The work is highly domain-specific to dental diagnostics and lacks any connection to embodied control, robot manipulation, or dynamic environment interaction, making it tangential to general robotics research.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16781v1)
- **👥 Authors**: Huimin Xiong, Zijie Meng, Tianxiang Hu, Chenyi Zhou, Yang Feng, Zuozhu Liu
- **🏷️ Tags**: #Foundation_Model #LLM

---

### 📄 OpenSeeker: Democratizing Frontier Search Agents by Fully Open-Sourcing Training Data (Score: 4/10)
- **💡 Innovation**: The paper introduces a scalable, fact-grounded data synthesis pipeline that reverse-engineers web graphs to generate high-quality, multi-hop reasoning trajectories for training search agents.
- **⚠️ Limitations**: The work is strictly focused on web-based information retrieval and lacks any connection to physical embodiment, sensorimotor control, or spatial reasoning required for robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15594)
- **👥 Authors**: Yuwen Du, Rui Ye, Shuo Tang, Xinyu Zhu, Yijun Lu, Yuzhu Cai, Siheng Chen
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 WebVR: Benchmarking Multimodal LLMs for WebPage Recreation from Videos via Human-Aligned Visual Rubrics (Score: 4/10)
- **💡 Innovation**: The paper introduces a benchmark for video-conditioned webpage generation, shifting the paradigm from static screenshot or text-prompt inputs to dynamic video demonstrations.
- **⚠️ Limitations**: The work focuses exclusively on web-based UI generation rather than physical world interaction, offering limited direct utility for embodied agents or robot manipulation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.13391)
- **👥 Authors**: Yuhong Dai, Yanlin Lai, Mitt Huang, Hangyu Guo, Dingming Li, Hongbo Peng, Haodong Li, Yingxiu Zhao, Haoran Lyu, Zheng Ge, Xiangyu Zhang, Daxin Jiang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Understanding Reasoning in LLMs through Strategic Information Allocation under Uncertainty (Score: 4/10)
- **💡 Innovation**: The paper introduces an information-theoretic framework that models LLM reasoning as a process of epistemic verbalization, framing the externalization of uncertainty as a mechanism for achieving information sufficiency.
- **⚠️ Limitations**: The study focuses exclusively on linguistic reasoning tasks and lacks empirical validation in embodied settings, making its direct applicability to robot control or VLA architectures speculative.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15500)
- **👥 Authors**: Jeonghye Kim, Xufang Luo, Minbeom Kim, Sangmook Lee, Dongsheng Li, Yuqing Yang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Code-A1: Adversarial Evolving of Code LLM and Test LLM via Reinforcement Learning (Score: 4/10)
- **💡 Innovation**: The paper introduces an adversarial co-evolution framework that separates code generation and test generation into two distinct LLMs to prevent self-collusion during reinforcement learning.
- **⚠️ Limitations**: The approach is strictly limited to software code generation and lacks any grounding in physical environments, sensorimotor control, or multi-modal interaction required for embodied agents.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15611)
- **👥 Authors**: Aozhe Wang, Yuchen Yan, Nan Zhou, Zhengxi Lu, Weiming Lu, Jun Xiao, Yueting Zhuang, Yongliang Shen
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Supervised Fine-Tuning versus Reinforcement Learning: A Study of Post-Training Methods for Large Language Models (Score: 4/10)
- **💡 Innovation**: The paper provides a unified theoretical and empirical framework that bridges the gap between SFT and RL for post-training, characterizing the shift toward hybrid paradigms.
- **⚠️ Limitations**: The study is strictly focused on text-based LLMs and lacks any discussion or application regarding embodied agents, VLA models, or physical world interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.13985)
- **👥 Authors**: Haitao Jiang, Wenbo Zhang, Jiarui Yao, Hengrui Cai, Sheng Wang, Rui Song
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Learning Latent Proxies for Controllable Single-Image Relighting (Score: 4/10)
- **💡 Innovation**: The paper introduces a latent proxy encoder and a DPO-based objective to inject physical priors into a diffusion-based relighting pipeline, bypassing the need for full intrinsic decomposition.
- **⚠️ Limitations**: The method is focused on static image relighting and lacks integration with dynamic scene understanding or embodied interaction, which are critical for robotics applications.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15555)
- **👥 Authors**: Haoze Zheng, Zihao Wang, Xianfeng Wu, Yajing Bai, Yexin Liu, Yun Li, Xiaogang Xu, Harry Yang
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 RS-WorldModel: a Unified Model for Remote Sensing Understanding and Future Sense Forecasting (Score: 4/10)
- **💡 Innovation**: The paper introduces a unified framework for remote sensing that integrates spatiotemporal change understanding and future scene forecasting through a three-stage training pipeline involving geo-aware pre-training and verifiable reinforcement optimization.
- **⚠️ Limitations**: The work is strictly domain-specific to remote sensing and lacks any connection to embodied agents, physical interaction, or action-space control, making it largely irrelevant to robotics manipulation or VLA research.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14941)
- **👥 Authors**: Linrui Xu, Zhongan Wang, Fei Shen, Gang Xu, Huiping Zhuang, Ming Li, Haifeng Li
- **🏷️ Tags**: #World_Model #Reinforcement_Learning #Foundation_Model #Diffusion_Model #LLM

---

### 📄 Tri-Prompting: Video Diffusion with Unified Control over Scene, Subject, and Motion (Score: 4/10)
- **💡 Innovation**: The paper introduces a unified framework that integrates scene composition, multi-view subject consistency, and motion control into a single video diffusion architecture using a dual-condition motion module.
- **⚠️ Limitations**: The work focuses on video generation for content creation rather than physical interaction or closed-loop control, making it less applicable to real-world robotic manipulation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15614)
- **👥 Authors**: Zhenghong Zhou, Xiaohang Zhan, Zhiqin Chen, Soo Ye Kim, Nanxuan Zhao, Haitian Zheng, Qing Liu, He Zhang, Zhe Lin, Yuqian Zhou, Jiebo Luo
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 When Does Sparsity Mitigate the Curse of Depth in LLMs (Score: 4/10)
- **💡 Innovation**: The paper identifies that sparsity (both implicit and explicit) acts as a variance regulator that mitigates the 'curse of depth' in LLMs, thereby improving layer utilization in deep architectures.
- **⚠️ Limitations**: The study is strictly confined to text-based LLMs and does not explore whether these findings on depth scaling and variance propagation translate to multimodal or embodied architectures.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15389)
- **👥 Authors**: Dilxat Muhtar, Xinyuan Song, Sebastian Pokutta, Max Zimmer, Nico Pelleriti, Thomas Hofmann, Shiwei Liu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Deep Reinforcement Learning-driven Edge Offloading for Latency-constrained XR pipelines (Score: 3/10)
- **💡 Innovation**: The paper introduces a battery-aware execution management framework for XR systems that uses deep reinforcement learning to optimize the trade-off between motion-to-photon latency and device energy consumption.
- **⚠️ Limitations**: The work focuses exclusively on XR systems and network offloading, lacking any connection to physical robot control, vision-language-action models, or embodied intelligence.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16823v1)
- **👥 Authors**: Sourya Saha, Saptarshi Debroy
- **🏷️ Tags**: #Reinforcement_Learning

---

### 📄 Is Conformal Factuality for RAG-based LLMs Robust? Novel Metrics and Systematic Insights (Score: 3/10)
- **💡 Innovation**: The paper provides a systematic empirical evaluation of conformal factuality filtering in RAG pipelines, identifying critical trade-offs between statistical reliability, output informativeness, and robustness to distribution shifts.
- **⚠️ Limitations**: The study is strictly confined to text-based RAG pipelines and does not address the application of conformal prediction or factuality verification in embodied or multimodal action-space contexts.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16817v1)
- **👥 Authors**: Yi Chen, Daiwei Chen, Sukrut Madhav Chikodikar, Caitlyn Heqi Yin, Ramya Korlakai Vinayak
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 SOMP: Scalable Gradient Inversion for Large Language Models via Subspace-Guided Orthogonal Matching Pursuit (Score: 3/10)
- **💡 Innovation**: The paper introduces a sparse signal recovery approach using subspace-guided orthogonal matching pursuit to reconstruct private text from aggregated LLM gradients.
- **⚠️ Limitations**: The work focuses exclusively on privacy and security in NLP, offering no direct contribution to embodied control, sensorimotor learning, or robot manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16761v1)
- **👥 Authors**: Yibo Li, Qiongxiu Li
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 AI Can Learn Scientific Taste (Score: 3/10)
- **💡 Innovation**: The paper introduces Reinforcement Learning from Community Feedback (RLCF) to align LLMs with scientific impact metrics by training a reward model on citation-based preference pairs.
- **⚠️ Limitations**: The work focuses exclusively on text-based scientific ideation and lacks any connection to physical experimentation, embodied agents, or the multi-modal grounding required for robotics research.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14473)
- **👥 Authors**: Jingqi Tong, Mingzhe Li, Hangcheng Li, Yongzhuo Yang, Yurong Mou, Weijie Ma, Zhiheng Xi, Hongji Chen, Xiaoran Liu, Qinyuan Cheng, Ming Zhang, Qiguang Chen, Weifeng Ge, Qipeng Guo, Tianlei Ying, Tianxiang Sun, Yining Zheng, Xinchi Chen, Jun Zhao, Ning Ding, Xuanjing Huang, Yugang Jiang, Xipeng Qiu
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Motivation in Large Language Models (Score: 3/10)
- **💡 Innovation**: The paper investigates whether LLMs exhibit behavioral patterns analogous to human psychological constructs of motivation through self-reporting and task performance modulation.
- **⚠️ Limitations**: The study relies on anthropomorphic interpretation of model outputs rather than grounding these 'motivational' states in physical agency, objective utility functions, or embodied task success.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14347)
- **👥 Authors**: Omer Nahum, Asael Sklar, Ariel Goldstein, Roi Reichart
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Prompt Programming for Cultural Bias and Alignment of Large Language Models (Score: 2/10)
- **💡 Innovation**: The paper applies DSPy-based prompt optimization to systematically tune LLM outputs toward specific cultural value profiles using survey-grounded distance metrics.
- **⚠️ Limitations**: The research is entirely focused on text-based linguistic alignment and lacks any connection to embodied agents, physical interaction, or multimodal reasoning.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16827v1)
- **👥 Authors**: Maksim Eren, Eric Michalak, Brian Cook, Johnny Seales
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Finding Common Ground in a Sea of Alternatives (Score: 2/10)
- **💡 Innovation**: The paper introduces a formal social choice framework using the proportional veto core to select optimal statements from an infinite generative space.
- **⚠️ Limitations**: The work is purely theoretical and social-science oriented, lacking any connection to physical embodiment, sensorimotor control, or robotic decision-making.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.16751v1)
- **👥 Authors**: Jay Chooi, Paul Gölz, Ariel D. Procaccia, Benjamin Schiffer, Shirley Zhang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 GlyphPrinter: Region-Grouped Direct Preference Optimization for Glyph-Accurate Visual Text Rendering (Score: 2/10)
- **💡 Innovation**: The paper introduces Region-Grouped Direct Preference Optimization (R-GDPO), which applies preference-based learning at a localized, region-specific level to improve text rendering accuracy.
- **⚠️ Limitations**: The work is entirely focused on generative computer vision for text rendering and lacks any connection to physical agents, sensorimotor control, or embodied environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.15616)
- **👥 Authors**: Xincheng Shuai, Ziye Li, Henghui Ding, Dacheng Tao
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 Mind the Shift: Decoding Monetary Policy Stance from FOMC Statements with Large Language Models (Score: 2/10)
- **💡 Innovation**: The paper introduces Delta-Consistent Scoring (DCS), a self-supervised framework that leverages temporal inter-meeting shifts in FOMC statements to derive continuous stance scores from frozen LLM representations without manual labels.
- **⚠️ Limitations**: The methodology is highly domain-specific to financial text analysis and lacks any application to physical agents, sensorimotor control, or embodied decision-making.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.14313)
- **👥 Authors**: Yixuan Tang, Yi Yang
- **🏷️ Tags**: #LLM #Foundation_Model

---


