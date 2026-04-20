# 📅 2026-03-16 - Paper Digest
## Summary
Total Papers: 38 | High Impact: 7

## 📝 Papers List
### 🔥 Towards Generalizable Robotic Manipulation in Dynamic Environments (Score: 8/10)
- **💡 Innovation**: The paper introduces a dynamics-aware VLA architecture (PUMA) that integrates historical optical flow and world queries to enable implicit future state forecasting for dynamic manipulation.
- **⚠️ Limitations**: The reliance on optical flow may struggle with occlusions or rapid, non-linear object movements, and the paper does not explicitly detail the computational overhead of the historical query mechanism during real-time inference.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15620v1)
- **👥 Authors**: Heng Fang, Shangru Li, Shuhan Wang, Xuanyang Xi, Dingkang Liang, Xiang Bai
- **🏷️ Tags**: #Robot_Manipulation #VLA #Embodied_AI #Foundation_Model #World_Model

---

### 🔥 From Passive Observer to Active Critic: Reinforcement Learning Elicits Process Reasoning for Robotic Manipulation (Score: 8/10)
- **💡 Innovation**: The paper introduces a novel framework that uses outcome-based reinforcement learning to fine-tune video MLLMs to act as active 'Critics' capable of explicit chain-of-thought progress estimation for long-horizon manipulation.
- **⚠️ Limitations**: The reliance on outcome-based RL may introduce sample efficiency challenges or reward hacking risks, and the paper does not fully detail the computational overhead of the temporal anchoring mechanism during real-time inference.
- **🔗 Link**: [[PRIMO R1]]
- **👥 Authors**: Yibin Liu, Yaxing Lyu, Daqi Gao, Zhixuan Liang, Weiliang Tang, Shilong Mu, Xiaokang Yang, Yao Mu
- **🏷️ Tags**: #Robot_Manipulation #Reinforcement_Learning #Embodied_AI #LLM #Foundation_Model

---

### ✨ Look Before Acting: Enhancing Vision Foundation Representations for Vision-Language-Action Models (Score: 7/10)
- **💡 Innovation**: The paper introduces a Vision-Language Mixture-of-Transformers (VL-MoT) architecture that injects multi-level visual features into deeper VLA layers and employs Action-Guided Visual Pruning (AGVP) to focus on task-relevant visual tokens.
- **⚠️ Limitations**: The study focuses primarily on architectural modifications for visual grounding without addressing long-horizon planning or the potential catastrophic forgetting that may occur when fine-tuning deep VLA backbones with multi-level feature injection.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15618v1)
- **👥 Authors**: Yulin Luo, Hao Chen, Zhuangzhe Wu, Bowen Sui, Jiaming Liu, Chenyang Gu, Zhuoyang Liu, Qiuxuan Feng, Jiale Yu, Shuo Gu, Peng Jia, Pheng-Ann Heng, Shanghang Zhang
- **🏷️ Tags**: #Robot_Manipulation #VLA #Embodied_AI #Foundation_Model #LLM

---

### ✨ HSImul3R: Physics-in-the-Loop Reconstruction of Simulation-Ready Human-Scene Interactions (Score: 7/10)
- **💡 Innovation**: The paper introduces a bi-directional optimization framework that integrates physics simulation feedback into the 3D reconstruction process to ensure human-scene interactions are physically stable for downstream embodied agents.
- **⚠️ Limitations**: The reliance on physics-in-the-loop optimization is computationally expensive and may struggle with complex, non-rigid, or highly dynamic interactions that are difficult to simulate accurately in real-time.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15612v1)
- **👥 Authors**: Yukang Cao, Haozhe Xie, Fangzhou Hong, Long Zhuo, Zhaoxi Chen, Liang Pan, Ziwei Liu
- **🏷️ Tags**: #Embodied_AI #Sim2Real #Reinforcement_Learning

---

### ✨ Grounding World Simulation Models in a Real-World Metropolis (Score: 7/10)
- **💡 Innovation**: The paper introduces a retrieval-augmented world model that grounds video generation in real-world urban geometry using cross-temporal pairing and a Virtual Lookahead Sink to maintain long-horizon spatial consistency.
- **⚠️ Limitations**: The reliance on pre-captured street-view imagery limits the model's ability to handle dynamic, non-static urban changes or novel, unseen environments not covered by the retrieval database.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15583v1)
- **👥 Authors**: Junyoung Seo, Hyunwook Choi, Minkyung Kwon, Jinhyeok Choi, Siyoon Jin, Gayoung Lee, Junho Kim, JoungBin Lee, Geonmo Gu, Dongyoon Han, Sangdoo Yun, Seungryong Kim, Jin-Hwa Kim
- **🏷️ Tags**: #World_Model #Sim2Real #Embodied_AI #Foundation_Model

---

### ✨ Panoramic Affordance Prediction (Score: 7/10)
- **💡 Innovation**: The paper introduces a novel panoramic affordance prediction framework that uses a training-free, coarse-to-fine recursive visual routing mechanism to handle the geometric distortions and high-resolution demands of 360-degree imagery.
- **⚠️ Limitations**: The current approach is purely perception-focused and lacks integration with closed-loop control or temporal consistency, which are essential for real-world robot manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15558v1)
- **👥 Authors**: Zixin Zhang, Chenfei Liao, Hongfei Zhang, Harold Haodong Chen, Kanghao Chen, Zichen Wen, Litao Guo, Bin Ren, Xu Zheng, Yinchuan Li, Xuming Hu, Nicu Sebe, Ying-Cong Chen
- **🏷️ Tags**: #Embodied_AI #Robot_Manipulation #Foundation_Model

---

### ✨ Steve-Evolving: Open-World Embodied Self-Evolution via Fine-Grained Diagnosis and Dual-Track Knowledge Distillation (Score: 7/10)
- **💡 Innovation**: The paper introduces a non-parametric self-evolution framework that uses fine-grained execution diagnosis and dual-track knowledge distillation to iteratively refine agent behavior without requiring model parameter updates.
- **⚠️ Limitations**: The reliance on Minecraft as the primary testbed limits the demonstrated generalizability to real-world robotic hardware, where state estimation and diagnosis are significantly noisier and more complex.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.13131)
- **👥 Authors**: Zhengwei Xie, Zhisheng Chen, Ziyan Weng, Tingyu Wu, Chenglong Li, Vireo Zhang, Kun Wang
- **🏷️ Tags**: #Embodied_AI #LLM #Foundation_Model

---

### ✨ Kimodo: Scaling Controllable Human Motion Generation (Score: 6/10)
- **💡 Innovation**: Kimodo introduces a two-stage denoiser architecture that decouples root and body motion prediction to enable high-fidelity, constraint-controllable human motion generation at a significantly larger scale than previous mocap-trained models.
- **⚠️ Limitations**: The paper focuses exclusively on kinematic motion generation without addressing physical dynamics, contact physics, or the integration of these motions into closed-loop robot control policies.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15546v1)
- **👥 Authors**: Davis Rempe, Mathis Petrovich, Ye Yuan, Haotian Zhang, Xue Bin Peng, Yifeng Jiang, Tingwu Wang, Umar Iqbal, David Minor, Michael de Ruyter, Jiefeng Li, Chen Tessler, Edy Lim, Eugene Jeong, Sam Wu, Ehsan Hassani, Michael Huang, Jin-Bey Yu, Chaeyeon Chung, Lina Song, Olivier Dionne, Jan Kautz, Simon Yuen, Sanja Fidler
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #Embodied_AI

---

### ✨ Video Streaming Thinking: VideoLLMs Can Watch and Think Simultaneously (Score: 6/10)
- **💡 Innovation**: The paper introduces a 'thinking while watching' paradigm that amortizes LLM reasoning latency over video playback to enable real-time streaming comprehension without sacrificing logical depth.
- **⚠️ Limitations**: The work focuses on video understanding benchmarks rather than closed-loop control, leaving the efficacy of this streaming reasoning architecture for real-time robot manipulation tasks unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12262)
- **👥 Authors**: Yiran Guan, Liang Yin, Dingkang Liang, Jianzhong Ju, Zhenbo Luo, Jian Luan, Yuliang Liu, Xiang Bai
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Think While Watching: Online Streaming Segment-Level Memory for Multi-Turn Video Reasoning in Multimodal Large Language Models (Score: 6/10)
- **💡 Innovation**: The paper introduces a memory-anchored streaming framework that enables concurrent perception and generation by utilizing segment-level memory and a streaming causal mask to mitigate memory decay in long-range video reasoning.
- **⚠️ Limitations**: The framework is evaluated primarily on video understanding benchmarks rather than closed-loop embodied control tasks, leaving its efficacy in real-time robot manipulation or high-frequency action inference unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.11896)
- **👥 Authors**: Lu Wang, Zhuoran Jin, Yupu Hao, Yubo Chen, Kang Liu, Yulong Ao, Jun Zhao
- **🏷️ Tags**: #LLM #Foundation_Model #Embodied_AI

---

### ✨ Do You See What I Am Pointing At? Gesture-Based Egocentric Video Question Answering (Score: 6/10)
- **💡 Innovation**: The paper introduces Hand Intent Tokens (HINT), a method that explicitly encodes 3D hand keypoints as tokens to improve the grounding of deictic gestures in egocentric video-language models.
- **⚠️ Limitations**: The reliance on an off-the-shelf 3D hand reconstruction model introduces a potential point of failure and latency, and the study lacks evaluation on closed-loop robotic control tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12533)
- **👥 Authors**: Yura Choi, Roy Miles, Rolandos Alexandros Potamias, Ismail Elezi, Jiankang Deng, Stefanos Zafeiriou
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #LLM

---

### ✨ Mixture-of-Depths Attention (Score: 5/10)
- **💡 Innovation**: The paper introduces Mixture-of-Depths Attention (MoDA), which allows attention heads to attend to both current-layer KV pairs and depth-wise KV pairs from preceding layers to mitigate signal degradation in deep models.
- **⚠️ Limitations**: The evaluation is restricted to language modeling benchmarks, leaving the efficacy of this architecture for high-dimensional, multi-modal embodied tasks or VLA models unverified.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15619v1)
- **👥 Authors**: Lianghui Zhu, Yuxin Fang, Bencheng Liao, Shijie Wang, Tianheng Cheng, Zilong Huang, Chen Chen, Lai Wei, Yutao Zeng, Ya Wang, Yi Lin, Yu Li, Xinggang Wang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Effective Distillation to Hybrid xLSTM Architectures (Score: 5/10)
- **💡 Innovation**: The paper introduces a distillation pipeline that merges linearized experts into a hybrid xLSTM architecture to achieve performance parity with quadratic attention-based LLMs.
- **⚠️ Limitations**: The research focuses exclusively on text-based language modeling tasks, lacking any evaluation or discussion regarding the applicability of these distilled architectures to embodied or multimodal robotic control.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15590v1)
- **👥 Authors**: Lukas Hauzenberger, Niklas Schmidinger, Thomas Schmied, Anamaria-Roberta Hartl, David Stap, Pieter-Jan Hoedt, Maximilian Beck, Sebastian Böck, Günter Klambauer, Sepp Hochreiter
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Mamba-3: Improved Sequence Modeling using State Space Principles (Score: 5/10)
- **💡 Innovation**: The paper introduces a MIMO formulation and complex-valued state updates within a state space model (SSM) framework to improve state tracking and inference efficiency.
- **⚠️ Limitations**: The paper focuses exclusively on language modeling and state-tracking benchmarks, lacking any evaluation on embodied tasks, multimodal inputs, or control-based environments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15569v1)
- **👥 Authors**: Aakash Lahoti, Kevin Y. Li, Berlin Chen, Caitlin Wang, Aviv Bick, J. Zico Kolter, Tri Dao, Albert Gu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ The PokeAgent Challenge: Competitive and Long-Context Learning at Scale (Score: 5/10)
- **💡 Innovation**: The paper introduces a large-scale, multi-modal benchmark for long-horizon planning and game-theoretic reasoning using the Pokemon environment to stress-test LLM and RL agents.
- **⚠️ Limitations**: The benchmark is purely digital and lacks physical grounding, making it less relevant for real-world robotics or embodied manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15563v1)
- **👥 Authors**: Seth Karten, Jake Grigsby, Tersoo Upaa, Junik Bae, Seonghun Hong, Hyunyoung Jeong, Jaeyoon Jung, Kun Kerdthaisong, Gyungbo Kim, Hyeokgi Kim, Yujin Kim, Eunju Kwon, Dongyu Liu, Patrick Mariglia, Sangyeon Park, Benedikt Schink, Xianwei Shi, Anthony Sistilli, Joseph Twin, Arian Urdu, Matin Urdu, Qiao Wang, Ling Wu, Wenli Zhang, Kunsheng Zhou, Stephanie Milani, Kiran Vodrahalli, Amy Zhang, Fei Fang, Yuke Zhu, Chi Jin
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Cheers: Decoupling Patch Details from Semantic Representations Enables Unified Multimodal Comprehension and Generation (Score: 5/10)
- **💡 Innovation**: The paper introduces a decoupled architecture that separates semantic tokens from patch-level detail residuals, allowing a single model to handle both multimodal understanding and high-fidelity image generation efficiently.
- **⚠️ Limitations**: The work focuses exclusively on static image generation and understanding, lacking the temporal consistency or action-space grounding required for embodied robotics or world modeling applications.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12793)
- **👥 Authors**: Yichen Zhang, Da Peng, Zonghao Guo, Zijian Zhang, Xuesong Yang, Tong Sun, Shichu Sun, Yidan Zhang, Yanghao Li, Haiyan Zhao, Wang Xu, Qi Shi, Yangang Sun, Chi Chen, Shuo Wang, Yukun Yan, Xu Han, Qiang Ma, Wei Ke, Liang Wang, Zhiyuan Liu, Maosong Sun
- **🏷️ Tags**: #Foundation_Model #LLM #Diffusion_Model

---

### ✨ Visual-ERM: Reward Modeling for Visual Equivalence (Score: 5/10)
- **💡 Innovation**: The paper introduces a multimodal generative reward model (Visual-ERM) that provides fine-grained, task-agnostic feedback for vision-to-code tasks by evaluating discrepancies in the rendered visual space.
- **⚠️ Limitations**: The approach is currently restricted to structured visual data (charts, tables, SVGs) and lacks evidence of generalization to the dynamic, unstructured environments typical of embodied robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.13224)
- **👥 Authors**: Ziyu Liu, Shengyuan Ding, Xinyu Fang, Xuanlang Dai, Penghui Yang, Jianze Liang, Jiaqi Wang, Kai Chen, Dahua Lin, Yuhang Zang
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### ✨ MM-CondChain: A Programmatically Verified Benchmark for Visually Grounded Deep Compositional Reasoning (Score: 5/10)
- **💡 Innovation**: The paper introduces an agentic synthesis pipeline that uses a Verifiable Programmatic Intermediate Representation (VPIR) to automatically generate and verify multi-layer compositional reasoning chains for multimodal evaluation.
- **⚠️ Limitations**: The benchmark focuses on static visual reasoning (GUIs, charts, images) rather than dynamic, closed-loop embodied interaction, limiting its direct applicability to physical robot control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12266)
- **👥 Authors**: Haozhan Shen, Shilin Yan, Hongwei Xue, Shuaiqi Lu, Xiaojun Tang, Guannan Zhang, Tiancheng Zhao, Jianwei Yin
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ V-Bridge: Bridging Video Generative Priors to Versatile Few-shot Image Restoration (Score: 5/10)
- **💡 Innovation**: The paper proposes reinterpreting image restoration as a progressive generative process, leveraging the latent priors of pre-trained video generative models to perform multi-task restoration with minimal fine-tuning data.
- **⚠️ Limitations**: The work focuses exclusively on static image restoration tasks and lacks any demonstration of temporal consistency or applicability to embodied control or robotic perception pipelines.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.13089)
- **👥 Authors**: Shenghe Zheng, Junpeng Jiang, Wenbo Li
- **🏷️ Tags**: #Foundation_Model #Diffusion_Model

---

### ✨ EvoScientist: Towards Multi-Agent Evolving AI Scientists for End-to-End Scientific Discovery (Score: 5/10)
- **💡 Innovation**: The paper introduces a multi-agent framework that utilizes persistent memory modules to enable self-evolution and iterative refinement of research strategies in AI-driven scientific discovery.
- **⚠️ Limitations**: The framework is primarily focused on software-based scientific discovery (code/ideation) and lacks integration with physical experimentation or embodied systems, limiting its direct applicability to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08127)
- **👥 Authors**: Yougang Lyu, Xi Zhang, Xinhao Yi, Yuyue Zhao, Shuyu Guo, Wenxiang Hu, Jan Piotrowski, Jakub Kaliski, Jacopo Urbani, Zaiqiao Meng, Lun Zhou, Xiaohui Yan
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Spend Less, Reason Better: Budget-Aware Value Tree Search for LLM Agents (Score: 5/10)
- **💡 Innovation**: The paper introduces a budget-conditioned node selection mechanism that dynamically adjusts exploration versus exploitation in LLM reasoning trees based on remaining token budgets.
- **⚠️ Limitations**: The framework is evaluated exclusively on text-based multi-hop QA benchmarks, leaving its efficacy in high-stakes, continuous-state embodied environments or long-horizon robotic task planning unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12634)
- **👥 Authors**: Yushu Li, Wenlong Deng, Jiajin Li, Xiaoxiao Li
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Tri-Prompting: Video Diffusion with Unified Control over Scene, Subject, and Motion (Score: 4/10)
- **💡 Innovation**: The paper introduces a unified framework that integrates scene composition, multi-view subject consistency, and motion control into a single video diffusion architecture using a dual-condition motion module.
- **⚠️ Limitations**: The work focuses on video generation for content creation rather than physical interaction or closed-loop control, making it less applicable to real-world robotic manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15614v1)
- **👥 Authors**: Zhenghong Zhou, Xiaohang Zhan, Zhiqin Chen, Soo Ye Kim, Nanxuan Zhao, Haitian Zheng, Qing Liu, He Zhang, Zhe Lin, Yuqian Zhou, Jiebo Luo
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 OpenSeeker: Democratizing Frontier Search Agents by Fully Open-Sourcing Training Data (Score: 4/10)
- **💡 Innovation**: The paper introduces a scalable, fact-grounded data synthesis pipeline that reverse-engineers web graphs to generate high-quality, multi-hop reasoning trajectories for training search agents.
- **⚠️ Limitations**: The work is strictly focused on web-based information retrieval and lacks any connection to physical embodiment, sensorimotor control, or spatial reasoning required for robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15594v1)
- **👥 Authors**: Yuwen Du, Rui Ye, Shuo Tang, Xinyu Zhu, Yijun Lu, Yuzhu Cai, Siheng Chen
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Learning Latent Proxies for Controllable Single-Image Relighting (Score: 4/10)
- **💡 Innovation**: The paper introduces a latent proxy encoder and a DPO-based objective to inject physical priors into a diffusion-based relighting pipeline, bypassing the need for full intrinsic decomposition.
- **⚠️ Limitations**: The method is focused on static image relighting and lacks integration with dynamic scene understanding or embodied interaction, which are critical for robotics applications.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15555v1)
- **👥 Authors**: Haoze Zheng, Zihao Wang, Xianfeng Wu, Yajing Bai, Yexin Liu, Yun Li, Xiaogang Xu, Harry Yang
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 Understanding Reasoning in LLMs through Strategic Information Allocation under Uncertainty (Score: 4/10)
- **💡 Innovation**: The paper introduces an information-theoretic framework that models LLM reasoning as a process of epistemic verbalization, framing the externalization of uncertainty as a mechanism for information acquisition.
- **⚠️ Limitations**: The work is purely theoretical and linguistic in nature, lacking any connection to embodied agents, sensorimotor control, or the physical constraints inherent in robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15500v1)
- **👥 Authors**: Jeonghye Kim, Xufang Luo, Minbeom Kim, Sangmook Lee, Dongsheng Li, Yuqing Yang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 OmniForcing: Unleashing Real-time Joint Audio-Visual Generation (Score: 4/10)
- **💡 Innovation**: The paper introduces a distillation framework that converts bidirectional audio-visual diffusion models into streaming autoregressive generators using asymmetric causal alignment and audio sink tokens.
- **⚠️ Limitations**: The work focuses exclusively on audio-visual generation and lacks any integration with embodied control, action prediction, or physical environment interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.11647)
- **👥 Authors**: Yaofeng Su, Yuming Li, Zeyue Xue, Jie Huang, Siming Fu, Haoran Li, Ying Li, Zezhong Qian, Haoyang Huang, Nan Duan
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 HybridStitch: Pixel and Timestep Level Model Stitching for Diffusion Acceleration (Score: 4/10)
- **💡 Innovation**: The paper introduces a hybrid inference paradigm that dynamically partitions image generation tasks between large and small diffusion models at both the pixel and timestep levels based on regional complexity.
- **⚠️ Limitations**: The method is strictly focused on T2I generation and lacks any application or evaluation within embodied contexts, such as diffusion-based policy inference or world modeling for robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07815)
- **👥 Authors**: Desen Sun, Jason Hon, Jintao Zhang, Sihang Liu
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 LookaheadKV: Fast and Accurate KV Cache Eviction by Glimpsing into the Future without Generation (Score: 4/10)
- **💡 Innovation**: LookaheadKV replaces computationally expensive draft generation for KV cache eviction with lightweight, parameter-efficient modules trained to predict token importance scores directly.
- **⚠️ Limitations**: The paper focuses exclusively on text-based long-context LLM inference and does not address the specific memory or latency constraints of real-time embodied agents or VLA models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10899)
- **👥 Authors**: Jinwoo Ahn, Ingyu Seong, Akhil Kedia, Junhan Kim, Hyemi Jang, Kangwook Lee, Yongkweon Jeon
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Mechanistic Origin of Moral Indifference in Language Models (Score: 3/10)
- **💡 Innovation**: The paper introduces a mechanistic approach to identifying and correcting 'moral indifference' in LLMs by using Sparse Autoencoders to reconstruct the topological relationships of moral features in latent space.
- **⚠️ Limitations**: The research is strictly confined to textual moral reasoning and lacks any connection to embodied agents, physical grounding, or the multi-modal constraints required for robotic decision-making.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15615v1)
- **👥 Authors**: Lingyu Li, Yan Teng, Yingchun Wang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 SmartSearch: How Ranking Beats Structure for Conversational Memory Retrieval (Score: 3/10)
- **💡 Innovation**: The paper proposes a deterministic, CPU-efficient retrieval pipeline that replaces complex LLM-based structuring with a rank-fusion approach to optimize conversational memory.
- **⚠️ Limitations**: The work is strictly focused on text-based conversational memory retrieval and lacks any connection to embodied perception, multimodal grounding, or physical action spaces.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15599v1)
- **👥 Authors**: Jesper Derehag, Carlos Calva, Timmy Ghiurau
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Unbiased and Biased Variance-Reduced Forward-Reflected-Backward Splitting Methods for Stochastic Composite Inclusions (Score: 3/10)
- **💡 Innovation**: The paper introduces a unified framework for incorporating both unbiased and biased variance-reduced estimators into the forward-reflected-backward splitting (FRBS) method for solving stochastic composite inclusions.
- **⚠️ Limitations**: The work is purely theoretical and optimization-focused, lacking direct application or empirical validation in the context of modern embodied AI, VLA, or high-dimensional robot learning tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15576v1)
- **👥 Authors**: Quoc Tran-Dinh, Nghia Nguyen-Trung
- **🏷️ Tags**: #Reinforcement_Learning

---

### 📄 Are Dilemmas and Conflicts in LLM Alignment Solvable? A View from Priority Graph (Score: 3/10)
- **💡 Innovation**: The paper introduces a priority graph framework to model LLM preference conflicts and identifies 'priority hacking' as a vulnerability in alignment.
- **⚠️ Limitations**: The work is purely theoretical and lacks empirical validation in embodied settings, making it less relevant to the specific challenges of robot manipulation or VLA-based control.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15527v1)
- **👥 Authors**: Zhenheng Tang, Xiang Liu, Qian Wang, Eunsol Choi, Bo Li, Xiaowen Chu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 GlyphPrinter: Region-Grouped Direct Preference Optimization for Glyph-Accurate Visual Text Rendering (Score: 2/10)
- **💡 Innovation**: The paper introduces Region-Grouped Direct Preference Optimization (R-GDPO), which applies preference-based fine-tuning at a localized, region-specific level to improve text rendering accuracy.
- **⚠️ Limitations**: The work is strictly focused on generative computer vision for text rendering and lacks any connection to embodied agents, physical interaction, or spatial reasoning required for robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15616v1)
- **👥 Authors**: Xincheng Shuai, Ziye Li, Henghui Ding, Dacheng Tao
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 Can LLMs Model Incorrect Student Reasoning? A Case Study on Distractor Generation (Score: 2/10)
- **💡 Innovation**: The paper introduces a taxonomy to evaluate how LLMs simulate student misconceptions during the generation of multiple-choice distractors, comparing model reasoning against learning science best practices.
- **⚠️ Limitations**: The research is entirely focused on educational assessment and lacks any connection to physical agency, spatial reasoning, or embodied decision-making processes.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15547v1)
- **👥 Authors**: Yanick Zengaffinen, Andreas Opedal, Donya Rooein, Kv Aditya Srivatsa, Shashank Sonkar, Mrinmaya Sachan
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 InterveneBench: Benchmarking LLMs for Intervention Reasoning and Causal Study Design in Real Social Systems (Score: 2/10)
- **💡 Innovation**: The paper introduces a benchmark and a multi-agent framework (STRIDES) specifically designed for causal inference and intervention reasoning within social science policy studies.
- **⚠️ Limitations**: The work is entirely focused on social science and policy reasoning, lacking any connection to physical agents, sensorimotor control, or embodied environments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15542v1)
- **👥 Authors**: Shaojie Shi, Zhengyu Shi, Lingran Zheng, Xinyu Su, Anna Xie, Bohao Lv, Rui Xu, Zijian Chen, Zhichao Chen, Guolei Liu, Naifu Zhang, Mingjian Dong, Zhuo Quan, Bohao Chen, Teqi Hao, Yuan Qi, Yinghui Xu, Libo Wu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Not All Invariants Are Equal: Curating Training Data to Accelerate Program Verification with SLMs (Score: 2/10)
- **💡 Innovation**: The paper introduces a data curation pipeline (Wonda) that uses AST-based normalization and LLM-driven rewriting to improve the quality of training data for inductive loop invariant synthesis.
- **⚠️ Limitations**: The work is entirely focused on formal program verification and lacks any connection to embodied agents, physical dynamics, or multimodal sensorimotor control.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15510v1)
- **👥 Authors**: Ido Pinto, Yizhak Yisrael Elboher, Haoze Wu, Nina Narodytska, Guy Katz
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Can Fairness Be Prompted? Prompt-Based Debiasing Strategies in High-Stakes Recommendations (Score: 2/10)
- **💡 Innovation**: The paper introduces lightweight, prompt-based debiasing strategies to mitigate group fairness issues in LLM-based recommendation systems without requiring model weight access.
- **⚠️ Limitations**: The study is entirely focused on recommendation systems and lacks any connection to embodied agents, physical interaction, or multimodal action-space reasoning.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12935)
- **👥 Authors**: Mihaela Rotar, Theresia Veronika Rampisela, Maria Maistro
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 SlovKE: A Large-Scale Dataset and LLM Evaluation for Slovak Keyphrase Extraction (Score: 1/10)
- **💡 Innovation**: The paper introduces a large-scale dataset and benchmarking framework for keyphrase extraction specifically tailored to the morphological complexities of the Slovak language.
- **⚠️ Limitations**: The research is entirely focused on Natural Language Processing (NLP) for low-resource languages and lacks any connection to robotics, embodied perception, or physical action spaces.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.15523v1)
- **👥 Authors**: David Števaňák, Marek Šuppa
- **🏷️ Tags**: #LLM #Foundation_Model

---


