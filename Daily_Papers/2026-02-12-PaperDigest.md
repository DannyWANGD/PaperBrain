# 📅 2026-02-12 - Paper Digest
## Summary
Total Papers: 55 | High Impact: 5

## 📝 Papers List
### 🔥 TIC-VLA: A Think-in-Control Vision-Language-Action Model for Robot Navigation in Dynamic Environments (Score: 8/10)
- **💡 Innovation**: The paper introduces a latency-aware VLA framework that explicitly models the asynchronous nature of semantic reasoning and real-time control by conditioning action generation on delayed vision-language states and latency metadata.
- **⚠️ Limitations**: The reliance on explicit latency metadata during inference may require precise system profiling, and the approach is primarily validated in navigation tasks rather than high-precision manipulation scenarios.
- **🔗 Link**: [[TICVLA]]
- **👥 Authors**: Zhiyu Huang, Yun Zhang, Johnson Liu, Rui Song, Chen Tang, Jiaqi Ma
- **🏷️ Tags**: #VLA #Embodied_AI #Reinforcement_Learning #Sim2Real #Foundation_Model

---

### ✨ Visual Foresight for Robotic Stow: A Diffusion-Based World Model from Sparse Snapshots (Score: 7/10)
- **💡 Innovation**: The paper introduces a stow-intent-conditioned world model that utilizes a latent diffusion transformer to predict post-stow bin configurations represented as item-aligned instance masks.
- **⚠️ Limitations**: The reliance on instance masks as a state representation may limit the model's ability to capture complex physical interactions or fine-grained geometric details compared to raw visual or point-cloud representations.
- **🔗 Link**: [[FOREST]]
- **👥 Authors**: Lijun Zhang, Nikhil Chacko, Petter Nilsson, Ruinian Xu, Shantanu Thakar, Bai Lou, Harpreet Sawhney, Zhebin Zhang, Mudit Agrawal, Bhavana Chandrashekhar, Aaron Parness
- **🏷️ Tags**: #World_Model #Diffusion_Model #Embodied_AI #Robot_Manipulation

---

### ✨ Soft Contamination Means Benchmarks Test Shallow Generalization (Score: 7/10)
- **💡 Innovation**: The paper introduces a semantic-based decontamination framework using embedding-space similarity to detect 'soft contamination' in training corpora, revealing that benchmark performance is significantly inflated by semantically equivalent test data.
- **⚠️ Limitations**: The study focuses primarily on text-based benchmarks and LLMs, leaving it unclear how these findings translate to the high-dimensional, multi-modal data distributions typical of VLA and Embodied AI benchmarks.
- **🔗 Link**: [[Soft_Contamination]]
- **👥 Authors**: Ari Spiesberger, Juan J. Vazquez, Nicky Pochinkov, Tomáš Gavenčiak, Peli Grietzer, Gavin Leech, Nandi Schoots
- **🏷️ Tags**: #LLM #Foundation_Model #VLA #Embodied_AI

---

### ✨ Self-Refining Vision Language Model for Robotic Failure Detection and Reasoning (Score: 7/10)
- **💡 Innovation**: The paper introduces a self-refining multi-task framework that leverages heterogeneous supervision—combining sparse binary failure labels with rich reasoning annotations—to enable iterative failure detection and natural language explanation.
- **⚠️ Limitations**: The reliance on self-certainty metrics for inference-time selection may be prone to overconfidence or calibration issues in novel, out-of-distribution failure scenarios.
- **🔗 Link**: [Web Link](https://arxiv.org/abs/2602.12405)
- **👥 Authors**: Carl Qi, Xiaojie Wang, Silong Yong, Stephen Sheng, Huitan Mao, Sriram Srinivasan, Manikantan Nambi, Amy Zhang, Yesh Dattatreya
- **🏷️ Tags**: #Embodied_AI #Robot_Manipulation #Foundation_Model #LLM

---

### ✨ Weight Decay Improves Language Model Plasticity (Score: 7/10)
- **💡 Innovation**: The paper identifies that higher weight decay during pretraining significantly enhances model plasticity, enabling better downstream fine-tuning performance despite potentially higher initial validation loss.
- **⚠️ Limitations**: The study focuses exclusively on text-based LLMs, leaving it unclear whether these findings regarding weight decay and plasticity translate to multimodal models or VLA architectures used in robotics.
- **🔗 Link**: [Web Link](https://arxiv.org/abs/2305.07125)
- **👥 Authors**: Tessa Han, Sebastian Bordt, Hanlin Zhang, Sham Kakade
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Continuous Diffusion Models Can Obey Formal Syntax (Score: 6/10)
- **💡 Innovation**: The paper introduces a training-free guidance method that uses analytic gradients from regular expression-based syntactic constraints to steer the denoising process of continuous diffusion language models.
- **⚠️ Limitations**: The approach is currently limited to formal syntactic constraints (regular expressions) and may struggle with more complex, semantic-heavy constraints or long-horizon reasoning tasks required in embodied settings.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12468v1)
- **👥 Authors**: Jinwoo Kim, Taylor Berg-Kirkpatrick, Loris D'Antoni
- **🏷️ Tags**: #Diffusion_Model #LLM #Foundation_Model

---

### ✨ Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward (Score: 6/10)
- **💡 Innovation**: The paper formalizes a modular 'skill abstraction layer' for LLM agents, introducing a standardized framework (SKILL$.$md) and a governance model for secure, composable agentic capabilities.
- **⚠️ Limitations**: The survey focuses heavily on software-based agentic workflows and digital environments, lacking deep integration or empirical evidence regarding physical embodiment and real-world robotic control.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12430v3)
- **👥 Authors**: Renjun Xu, Yang Yan
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Stabilizing Native Low-Rank LLM Pretraining (Score: 6/10)
- **💡 Innovation**: The paper introduces Spectron, a spectral renormalization and orthogonalization technique that stabilizes the training of LLMs from scratch using exclusively low-rank factorized weights.
- **⚠️ Limitations**: The study focuses exclusively on language modeling tasks, leaving the efficacy and stability of this low-rank training approach for multimodal or VLA architectures in embodied settings unverified.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12429v1)
- **👥 Authors**: Paul Janson, Edouard Oyallon, Eugene Belilovsky
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ What does RL improve for Visual Reasoning? A Frankenstein-Style Analysis (Score: 6/10)
- **💡 Innovation**: The paper introduces a 'Frankenstein-style' analysis framework—combining causal probing, parameter comparison, and model merging—to isolate and characterize the specific internal computational shifts induced by RL in vision-language models.
- **⚠️ Limitations**: The analysis is restricted to visual reasoning tasks and does not explicitly address whether these findings generalize to high-dimensional action spaces or embodied control loops in robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12395v1)
- **👥 Authors**: Xirui Li, Ming Li, Tianyi Zhou
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### ✨ ASA: Training-Free Representation Engineering for Tool-Calling Agents (Score: 6/10)
- **💡 Innovation**: The paper introduces a training-free, inference-time activation steering mechanism that bridges the representation-behavior gap in LLM tool-calling by using probe-guided steering vectors to modulate mid-layer activations.
- **⚠️ Limitations**: The evaluation is limited to a specific benchmark (MTU-Bench) and a small model (Qwen2.5-1.5B), leaving questions about the scalability of the steering vectors to larger, more complex instruction-tuned models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.04935)
- **👥 Authors**: Youjin Wang, Run Zhou, Rong Fu, Shuaishuai Cao, Hongwei Zeng, Jiaxuan Lu, Sicheng Fan, Jiaqiao Zhao, Liangming Pan
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Free(): Learning to Forget in Malloc-Only Reasoning Models (Score: 6/10)
- **💡 Innovation**: The paper introduces a plug-and-play LoRA adapter (Free-Module) that enables LLMs to dynamically prune redundant reasoning tokens during test-time compute, addressing the 'malloc-only' accumulation problem.
- **⚠️ Limitations**: The paper lacks evaluation on embodied or multi-modal reasoning tasks, leaving it unclear if the 'forgetting' mechanism preserves critical spatial or temporal context required for robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.08030)
- **👥 Authors**: Yilun Zheng, Dongyang Ma, Tian Liang, Jiahao Xu, Xinting Huang, Lihui Chen, Haitao Mi, Yan Wang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ UMEM: Unified Memory Extraction and Management Framework for Generalizable Memory (Score: 6/10)
- **💡 Innovation**: The paper introduces a unified framework that jointly optimizes memory extraction and management using a neighborhood-level marginal utility reward via GRPO to improve memory generalizability.
- **⚠️ Limitations**: The framework is primarily evaluated on interactive text-based or high-level reasoning benchmarks, lacking evidence of its effectiveness in low-level physical robot control or complex embodied environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10652)
- **👥 Authors**: Yongshi Ye, Hui Jiang, Feihu Jiang, Tian Lan, Yichao Du, Biao Fu, Xiaodong Shi, Qianghuai Jia, Longyue Wang, Weihua Luo
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Safe Reinforcement Learning via Recovery-based Shielding with Gaussian Process Dynamics Models (Score: 5/10)
- **💡 Innovation**: The paper introduces a recovery-based shielding framework that utilizes Gaussian Process uncertainty quantification to trigger safe backup policies in unknown, non-linear continuous dynamical systems.
- **⚠️ Limitations**: The reliance on Gaussian Processes for dynamics modeling may struggle with high-dimensional state spaces or complex, non-smooth environments typical of modern robot manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12444v2)
- **👥 Authors**: Alexander W. Goodall, Francesco Belardinelli
- **🏷️ Tags**: #Reinforcement_Learning #Embodied_AI

---

### ✨ Step 3.5 Flash: Open Frontier-Level Intelligence with 11B Active Parameters (Score: 5/10)
- **💡 Innovation**: The paper introduces a sparse Mixture-of-Experts architecture optimized with Multi-Token Prediction and interleaved attention to achieve frontier-level agentic reasoning with high computational efficiency.
- **⚠️ Limitations**: The paper lacks specific evidence or experiments regarding embodied control, sensorimotor integration, or real-world robotic deployment, despite the claims of industrial applicability.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10604)
- **👥 Authors**: Ailin Huang, Ang Li, Aobo Kong, Bin Wang, Binxing Jiao, Bo Dong, Bojun Wang, Boyu Chen, Brian Li, Buyun Ma, Chang Su, Changxin Miao, Changyi Wan, Chao Lou, Chen Hu, Chen Xu, Chenfeng Yu, Chengting Feng, Chengyuan Yao, Chunrui Han, Dan Ma, Dapeng Shi, Daxin Jiang, Dehua Ma, Deshan Sun, Di Qi, Enle Liu, Fajie Zhang, Fanqi Wan, Guanzhe Huang, Gulin Yan, Guoliang Cao, Guopeng Li, Han Cheng, Hangyu Guo, Hanshan Zhang, Hao Nie, Haonan Jia, Haoran Lv, Hebin Zhou, Hekun Lv, Heng Wang, Heung-Yeung Shum, Hongbo Huang, Hongbo Peng, Hongyu Zhou, Hongyuan Wang, Houyong Chen, Huangxi Zhu, Huimin Wu, Huiyong Guo, Jia Wang, Jian Zhou, Jianjian Sun, Jiaoren Wu, Jiaran Zhang, Jiashu Lv, Jiashuo Liu, Jiayi Fu, Jiayu Liu, Jie Cheng, Jie Luo, Jie Yang, Jie Zhou, Jieyi Hou, Jing Bai, Jingcheng Hu, Jingjing Xie, Jingwei Wu, Jingyang Zhang, Jishi Zhou, Junfeng Liu, Junzhe Lin, Ka Man Lo, Kai Liang, Kaibo Liu, Kaijun Tan, Kaiwen Yan, Kaixiang Li, Kang An, Kangheng Lin, Lei Yang, Liang Lv, Liang Zhao, Liangyu Chen, Lieyu Shi, Liguo Tan, Lin Lin, Lina Chen, Luck Ma, Mengqiang Ren, Michael Li, Ming Li, Mingliang Li, Mingming Zhang, Mingrui Chen, Mitt Huang, Na Wang, Peng Liu, Qi Han, Qian Zhao, Qinglin He, Qinxin Du, Qiuping Wu, Quan Sun, Rongqiu Yang, Ruihang Miao, Ruixin Han, Ruosi Wan, Ruyan Guo, Shan Wang, Shaoliang Pang, Shaowen Yang, Shengjie Fan, Shijie Shang, Shiliang Yang, Shiwei Li, Shuangshuang Tian, Siqi Liu, Siye Wu, Siyu Chen, Song Yuan, Tiancheng Cao, Tianchi Yue, Tianhao Cheng, Tianning Li, Tingdan Luo, Wang You, Wei Ji, Wei Yuan, Wei Zhang, Weibo Wu, Weihao Xie, Wen Sun, Wenjin Deng, Wenzhen Zheng, Wuxun Xie, Xiangfeng Wang, Xiangwen Kong, Xiangyu Liu, Xiangyu Zhang, Xiaobo Yang, Xiaojia Liu, Xiaolan Yuan, Xiaoran Jiao, Xiaoxiao Ren, Xiaoyun Zhang, Xin Li, Xin Liu, Xin Wu, Xing Chen, Xingping Yang, Xinran Wang, Xu Zhao, Xuan He, Xuanti Feng, Xuedan Cai, Xuqiang Zhou, Yanbo Yu, Yang Li, Yang Xu, Yanlin Lai, Yanming Xu, Yaoyu Wang, Yeqing Shen, Yibo Zhu, Yichen Lv, Yicheng Cao, Yifeng Gong, Yijing Yang, Yikun Yang, Yin Zhao, Yingxiu Zhao, Yinmin Zhang, Yitong Zhang, Yixuan Zhang, Yiyang Chen, Yongchi Zhao, Yongshen Long, Yongyao Wang, Yousong Guan, Yu Zhou, Yuang Peng, Yuanhao Ding, Yuantao Fan, Yuanzhen Yang, Yuchu Luo, Yudi Zhao, Yue Peng, Yueqiang Lin, Yufan Lu, Yuling Zhao, Yunzhou Ju, Yurong Zhang, Yusheng Li, Yuxiang Yang, Yuyang Chen, Yuzhu Cai, Zejia Weng, Zetao Hong, Zexi Li, Zhe Xie, Zheng Ge, Zheng Gong, Zheng Zeng, Zhenyi Lu, Zhewei Huang, Zhichao Chang, Zhiguo Huang, Zhiheng Hu, Zidong Yang, Zili Wang, Ziqi Ren, Zixin Zhang, Zixuan Wang
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ VidVec: Unlocking Video MLLM Embeddings for Video-Text Retrieval (Score: 5/10)
- **💡 Innovation**: The paper introduces a training-free method for video-text retrieval by leveraging intermediate layer embeddings from pre-trained MLLMs combined with a lightweight text-based alignment strategy.
- **⚠️ Limitations**: The approach is strictly focused on video-text retrieval benchmarks and lacks evaluation on downstream embodied tasks or temporal reasoning required for robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.08099)
- **👥 Authors**: Issar Tzachor, Dvir Samuel, Rami Ben-Ari
- **🏷️ Tags**: #Foundation_Model #LLM

---

### ✨ When to Memorize and When to Stop: Gated Recurrent Memory for Long-Context Reasoning (Score: 5/10)
- **💡 Innovation**: The paper introduces a gated recurrent memory mechanism for LLMs that uses RL-trained update and exit gates to selectively process long-context information and terminate computation early.
- **⚠️ Limitations**: The approach relies on task-specific reward signals for the gates, which may limit generalization to open-ended reasoning tasks where ground-truth labels for 'correct' memory updates are unavailable.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10560)
- **👥 Authors**: Leheng Sheng, Yongtao Zhang, Wenchang Ma, Yaorui Shi, Ting Huang, Xiang Wang, An Zhang, Ke Shen, Tat-Seng Chua
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Internalizing Meta-Experience into Memory for Guided Reinforcement Learning in Large Language Models (Score: 5/10)
- **💡 Innovation**: The paper introduces Meta-Experience Learning (MEL), which distills contrastive analysis of successful and failed reasoning trajectories into parametric memory to improve credit assignment in RLVR.
- **⚠️ Limitations**: The approach is evaluated exclusively on reasoning benchmarks (e.g., GSM8K, MATH) rather than embodied tasks, leaving its applicability to high-dimensional robotic control or VLA-based decision-making unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10224)
- **👥 Authors**: Shiting Huang, Zecheng Li, Yu Zeng, Qingnan Ren, Zhen Fang, Qisheng Su, Kou Shi, Lin Chen, Zehui Chen, Feng Zhao
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ DataChef: Cooking Up Optimal Data Recipes for LLM Adaptation via Reinforcement Learning (Score: 5/10)
- **💡 Innovation**: The paper introduces an automated, reinforcement learning-based framework to optimize data processing pipelines (data recipes) for LLM adaptation, replacing manual curation with a proxy-reward-driven search.
- **⚠️ Limitations**: The reliance on a proxy reward model for downstream performance prediction may introduce bias or instability, and the approach is currently limited to text-based LLM adaptation rather than multimodal or embodied agents.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.11089)
- **👥 Authors**: Yicheng Chen, Zerun Ma, Xinchen Xie, Yining Li, Kai Chen
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ The Pensieve Paradigm: Stateful Language Models Mastering Their Own Context (Score: 5/10)
- **💡 Innovation**: The paper introduces StateLM, a framework that enables LLMs to actively manage their own context window through an internal reasoning loop and a suite of memory-manipulation tools.
- **⚠️ Limitations**: The paper focuses exclusively on text-based long-context and research tasks, lacking any evaluation or discussion regarding its applicability to embodied agents or multimodal action sequences.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12108)
- **👥 Authors**: Xiaoyuan Liu, Tian Liang, Dongyang Ma, Deyu Zhou, Haitao Mi, Pinjia He, Yan Wang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ ECHO-2: A Large-Scale Distributed Rollout Framework for Cost-Efficient Reinforcement Learning (Score: 5/10)
- **💡 Innovation**: ECHO-2 introduces a distributed RL framework that optimizes post-training by modeling policy staleness and using peer-assisted pipelined broadcasting to overlap rollout generation with centralized training.
- **⚠️ Limitations**: The paper focuses exclusively on LLM post-training (text-based RL) rather than embodied agents, making its direct application to robotics or VLA training speculative.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.02192)
- **👥 Authors**: Jie Xiao, Meng Chen, Qingnan Ren, Jingwei Song, Jiaqi Huang, Yangshen Deng, Chris Tong, Wanyi Chen, Suli Wang, Ziqian Bi, Shuo Lu, Yiqun Duan, Xu Wang, Rymon Yu, Ween Yang, Lynn Ai, Eric Yang, Bill Shi, Song Jingwei
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Reasoning Cache: Continual Improvement Over Long Horizons via Short-Horizon RL (Score: 5/10)
- **💡 Innovation**: The paper introduces Reasoning Cache (RC), an iterative decoding algorithm that leverages the asymmetry between response generation and summarization to enable test-time extrapolation of reasoning horizons.
- **⚠️ Limitations**: The work focuses exclusively on symbolic/textual reasoning tasks and lacks an evaluation of how this iterative improvement mechanism translates to high-dimensional, continuous control spaces or embodied environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.03773)
- **👥 Authors**: Ian Wu, Yuxiao Qu, Amrith Setlur, Aviral Kumar
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ EcoGym: Evaluating LLMs for Long-Horizon Plan-and-Execute in Interactive Economies (Score: 5/10)
- **💡 Innovation**: The paper introduces a benchmark for evaluating long-horizon, strategic decision-making in persistent, stochastic economic environments rather than traditional episodic tasks.
- **⚠️ Limitations**: The benchmark focuses on abstract economic simulation rather than physical embodiment, limiting its direct applicability to real-world robotic control or sensorimotor tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.09514)
- **👥 Authors**: Xavier Hu, Jinxiang Xia, Shengze Xu, Kangqi Song, Yishuo Yuan, Guibin Zhang, JinCheng Ren, Boyu Feng, Li Lu, Tieyong Zeng, Jiaheng Liu, Minghao Liu, He Zhu, Yuchen Eleanor Jiang, Wei Wang, Wangchunshu Zhou
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Stroke3D: Lifting 2D strokes into rigged 3D model via latent diffusion models (Score: 5/10)
- **💡 Innovation**: The paper introduces a two-stage generative pipeline that uses a Skeletal Graph VAE and DiT to lift 2D user-drawn strokes into fully rigged, animatable 3D meshes.
- **⚠️ Limitations**: The framework lacks integration with embodied simulation environments or physics-based constraints, limiting its direct utility for robotics or real-world motion planning.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.09713)
- **👥 Authors**: Ruisi Zhao, Haoren Zheng, Zongxin Yang, Hehe Fan, Yi Yang
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ Latent Thoughts Tuning: Bridging Context and Reasoning with Fused Information in Latent Tokens (Score: 5/10)
- **💡 Innovation**: The paper introduces a Context-Prediction-Fusion mechanism that integrates predictive semantic guidance from the vocabulary space into latent hidden states to stabilize continuous reasoning.
- **⚠️ Limitations**: The paper focuses exclusively on linguistic reasoning tasks and lacks evaluation on embodied or multimodal control benchmarks, making its direct utility for robotics unclear.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10229)
- **👥 Authors**: Weihao Liu, Dehai Min, Lu Cheng
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Beyond Correctness: Learning Robust Reasoning via Transfer (Score: 5/10)
- **💡 Innovation**: The paper introduces Reinforcement Learning with Transferable Reward (RLTR), which optimizes LLM reasoning by rewarding models for generating prefixes that enable other models to successfully complete a task.
- **⚠️ Limitations**: The approach is evaluated exclusively on mathematical reasoning benchmarks (MATH500) and lacks application to embodied or multimodal tasks, limiting its direct relevance to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.08489)
- **👥 Authors**: Hyunseok Lee, Soheil Abbasloo, Jihoon Tack, Jinwoo Shin
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ ArcFlow: Unleashing 2-Step Text-to-Image Generation via High-Precision Non-Linear Flow Distillation (Score: 5/10)
- **💡 Innovation**: The paper introduces a non-linear flow distillation method that parameterizes velocity fields as a mixture of continuous momentum processes to enable high-precision, few-step image generation.
- **⚠️ Limitations**: The work focuses exclusively on static image generation and lacks any application or evaluation within embodied, temporal, or robotic control contexts.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.09014)
- **👥 Authors**: Zihan Yang, Shuyuan Tu, Licheng Zhang, Qi Dai, Yu-Gang Jiang, Zuxuan Wu
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ Large Language Lobotomy: Jailbreaking Mixture-of-Experts via Expert Silencing (Score: 5/10)
- **💡 Innovation**: The paper introduces a training-free jailbreak method that identifies and silences specific 'safety-critical' experts within Mixture-of-Experts (MoE) architectures to bypass alignment guardrails.
- **⚠️ Limitations**: The research focuses exclusively on text-based safety alignment in LLMs and does not address how these vulnerabilities manifest in multimodal or embodied agents where safety-critical behaviors are more complex.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.08741)
- **👥 Authors**: Jona te Lintelo, Lichao Wu, Stjepan Picek
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ From Features to Actions: Explainability in Traditional and Agentic AI Systems (Score: 5/10)
- **💡 Innovation**: The paper empirically demonstrates that traditional attribution-based XAI methods fail to diagnose execution-level failures in agentic trajectories, advocating instead for trace-grounded rubric evaluation.
- **⚠️ Limitations**: The study is restricted to text-based agentic benchmarks (TAU-bench and AssistantBench) and does not address the complexities of physical embodiment or multi-modal sensorimotor feedback loops.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.06841)
- **👥 Authors**: Sindhuja Chaduvula, Jessee Ho, Kina Kim, Aravind Narayanan, Mahshid Alinoori, Muskan Garg, Dhanesh Ramachandram, Shaina Raza
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 RankLLM: Weighted Ranking of LLMs by Quantifying Question Difficulty (Score: 4/10)
- **💡 Innovation**: The paper introduces a bidirectional score propagation framework that simultaneously quantifies LLM competency and question difficulty to improve benchmark granularity.
- **⚠️ Limitations**: The framework is strictly limited to text-based LLM evaluation and lacks applicability to multimodal or embodied agents where ground truth is often ambiguous or non-binary.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12424v1)
- **👥 Authors**: Ziqian Zhang, Xingjian Hu, Yue Huang, Kai Zhang, Ruoxi Chen, Yixin Liu, Qingsong Wen, Kaidi Xu, Xiangliang Zhang, Neil Zhenqiang Gong, Lichao Sun
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Intent-Driven Smart Manufacturing Integrating Knowledge Graphs and Large Language Models (Score: 4/10)
- **💡 Innovation**: The paper introduces a framework that bridges natural language intent with structured manufacturing ontologies by fine-tuning an LLM to generate JSON requirements mapped to an ISA-95 compliant Knowledge Graph.
- **⚠️ Limitations**: The work focuses on high-level task planning and semantic mapping rather than physical execution, lacking integration with embodied control, sensorimotor feedback, or real-world robotic manipulation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12419v1)
- **👥 Authors**: Takoua Jradi, John Violos, Dimitrios Spatharakis, Lydia Mavraidi, Ioannis Dimolitsas, Aris Leivadeas, Symeon Papavassiliou
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Sparse Autoencoders are Capable LLM Jailbreak Mitigators (Score: 4/10)
- **💡 Innovation**: The paper introduces Context-Conditioned Delta Steering (CC-Delta), which leverages sparse features from pre-trained Sparse Autoencoders (SAEs) to perform targeted inference-time steering for mitigating jailbreak attacks in LLMs.
- **⚠️ Limitations**: The method relies on the availability of paired harmful/jailbreak prompts for feature selection, which may not be feasible in real-world, zero-shot deployment scenarios.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12418v1)
- **👥 Authors**: Yannick Assogba, Jacopo Cortellazzi, Javier Abad, Pau Rodriguez, Xavier Suau, Arno Blaas
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 AstRL: Analog and Mixed-Signal Circuit Synthesis with Deep Reinforcement Learning (Score: 4/10)
- **💡 Innovation**: The paper introduces a graph-based deep reinforcement learning framework for automated analog circuit synthesis that operates at the transistor level using behavioral cloning and discriminator-based rewards.
- **⚠️ Limitations**: The work is strictly confined to simulation-based circuit design and lacks any connection to physical hardware deployment, embodied agents, or the multimodal foundation models relevant to your research interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12402v1)
- **👥 Authors**: Felicia B. Guo, Ken T. Ho, Andrei Vladimirescu, Borivoje Nikolic
- **🏷️ Tags**: #Reinforcement_Learning

---

### 📄 Synthetic Interaction Data for Scalable Personalization in Large Language Models (Score: 4/10)
- **💡 Innovation**: The paper introduces PersonaGym, a framework that uses agentic LLMs to simulate dynamic, multi-turn user preference interactions to generate synthetic training data for prompt optimization.
- **⚠️ Limitations**: The work is strictly confined to text-based LLM personalization and lacks any connection to physical embodiment, multi-modal sensorimotor control, or real-world robotic deployment.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12394v1)
- **👥 Authors**: Yuchen Ma, Yue Huang, Wenjie Wang, Xiaonan Luo, Xiangliang Zhang, Stefan Feuerriegel
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 Provably Convergent Actor-Critic in Risk-averse MARL (Score: 4/10)
- **💡 Innovation**: The paper introduces a two-timescale Actor-Critic algorithm that achieves global convergence for Risk-averse Quantal Response Equilibria (RQE) in general-sum Markov games.
- **⚠️ Limitations**: The work is purely theoretical and focused on multi-agent game theory, lacking any connection to embodied agents, vision-language models, or physical robot manipulation tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12386v1)
- **👥 Authors**: Yizhou Zhang, Eric Mazumdar
- **🏷️ Tags**: #Reinforcement_Learning

---

### 📄 G-LNS: Generative Large Neighborhood Search for LLM-Based Automatic Heuristic Design (Score: 4/10)
- **💡 Innovation**: The paper introduces a generative evolutionary framework that utilizes LLMs to co-evolve coupled destroy and repair operators for Large Neighborhood Search in combinatorial optimization.
- **⚠️ Limitations**: The approach is strictly confined to combinatorial optimization problems (TSP/CVRP) and lacks any connection to physical embodiment, sensorimotor control, or real-world robotic deployment.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.08253)
- **👥 Authors**: Baoyun Zhao, He Wang, Liang Zeng
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Online Causal Kalman Filtering for Stable and Effective Policy Optimization (Score: 4/10)
- **💡 Innovation**: The paper introduces a Kalman filter-based approach to smooth token-level importance sampling ratios in reinforcement learning for LLMs, mitigating variance and instability during policy optimization.
- **⚠️ Limitations**: The method is strictly evaluated on text-based math reasoning tasks and lacks any demonstration of applicability to embodied agents or continuous control settings.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10609)
- **👥 Authors**: Shuo He, Lang Feng, Xin Cheng, Lei Feng, Bo An
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 Ex-Omni: Enabling 3D Facial Animation Generation for Omni-modal Large Language Models (Score: 4/10)
- **💡 Innovation**: The paper introduces a Token-as-Query Gated Fusion (TQGF) mechanism to bridge the gap between discrete LLM semantic reasoning and continuous, fine-grained 3D facial motion dynamics.
- **⚠️ Limitations**: The work focuses exclusively on digital avatar animation rather than physical embodiment or interaction, limiting its direct applicability to robotics or embodied agents.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.07106)
- **👥 Authors**: Haoyu Zhang, Zhipeng Li, Yiwen Guo, Tianshu Yu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 AgenticPay: A Multi-Agent LLM Negotiation System for Buyer-Seller Transactions (Score: 4/10)
- **💡 Innovation**: The paper introduces a structured benchmark and simulation framework specifically designed to evaluate multi-agent linguistic negotiation and economic interaction among LLM-based agents.
- **⚠️ Limitations**: The work focuses exclusively on abstract economic negotiation and lacks integration with physical environments or embodied constraints, making it less relevant to robotics and sensorimotor control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.06008)
- **👥 Authors**: Xianyang Liu, Shangding Gu, Dawn Song
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 GoodVibe: Security-by-Vibe for LLM-Based Code Generation (Score: 4/10)
- **💡 Innovation**: The paper introduces a neuron-level fine-tuning framework that identifies and updates only security-critical subspaces within an LLM to improve code safety with minimal parameter overhead.
- **⚠️ Limitations**: The approach is strictly focused on software code generation and lacks any connection to embodied agents, physical world interaction, or multi-modal reasoning required for robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10778)
- **👥 Authors**: Maximilian Thang, Lichao Wu, Sasha Behrouzi, Mohamadreza Rostami, Jona te Lintelo, Stjepan Picek, Ahmad-Reza Sadeghi
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Designing RNAs with Language Models (Score: 3/10)
- **💡 Innovation**: The paper reframes RNA secondary structure design as a conditional sequence generation task using an autoregressive language model optimized via reinforcement learning.
- **⚠️ Limitations**: The work is entirely focused on computational biology and lacks any connection to physical agents, sensorimotor control, or spatial reasoning required for embodied robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12470v1)
- **👥 Authors**: Milan Gautam, Ning Dai, Tianshuo Zhou, Bowen Xie, David Mathews, Liang Huang
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Reproducing DragDiffusion: Interactive Point-Based Editing with Diffusion Models (Score: 3/10)
- **💡 Innovation**: The paper provides a rigorous reproducibility study of the DragDiffusion framework, validating its core claims while identifying hyperparameter sensitivities and the inefficiency of multi-timestep optimization.
- **⚠️ Limitations**: The work is strictly a reproducibility study of an image editing technique and lacks any direct application, integration, or contribution to embodied AI, robotics, or world modeling.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12393v1)
- **👥 Authors**: Ali Subhan, Ashir Raza
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 Vibe Coding on Trial: Operating Characteristics of Unanimous LLM Juries (Score: 3/10)
- **💡 Innovation**: The paper introduces a 'unanimous jury' framework using multiple LLMs to verify code generation accuracy, prioritizing safety by requiring consensus for acceptance.
- **⚠️ Limitations**: The study is restricted to text-to-SQL tasks and does not address the high computational overhead or latency costs associated with running multiple LLM inference passes for real-time verification.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.18492v1)
- **👥 Authors**: Muhammad Aziz Ullah, Abdul Serwadda
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 How Do Decoder-Only LLMs Perceive Users? Rethinking Attention Masking for User Representation Learning (Score: 3/10)
- **💡 Innovation**: The paper introduces Gradient-Guided Soft Masking, a training technique that uses a gradient-based pre-warmup to transition decoder-only LLMs from causal to bidirectional attention for user representation learning.
- **⚠️ Limitations**: The research is strictly focused on user behavior modeling in industrial recommendation systems and lacks any connection to physical agents, spatial reasoning, or embodied decision-making.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10622)
- **👥 Authors**: Jiahao Yuan, Yike Xu, Jinyong Wen, Baokun Wang, Yang Chen, Xiaotong Lin, Wuliang Huang, Ziyi Gao, Xing Fu, Yu Cheng, Weiqiang Wang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 FeatureBench: Benchmarking Agentic Coding for Complex Feature Development (Score: 3/10)
- **💡 Innovation**: The paper introduces an automated, test-driven framework for generating feature-level coding tasks from software repositories to evaluate agentic performance beyond simple bug fixes.
- **⚠️ Limitations**: The work is strictly focused on software engineering and code generation, offering no direct contribution to physical world modeling, robot control, or embodied interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10975)
- **👥 Authors**: Qixing Zhou, Jiacheng Zhang, Haiyang Wang, Rui Hao, Jiahe Wang, Minghao Han, Yuxue Yang, Shuzhe Wu, Feiyang Pan, Lue Fan, Dandan Tu, Zhaoxiang Zhang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 LiveMedBench: A Contamination-Free Medical Benchmark for LLMs with Automated Rubric Evaluation (Score: 3/10)
- **💡 Innovation**: The paper introduces a dynamic, contamination-free medical benchmark that utilizes a multi-agent framework to curate real-world clinical cases and employs a granular, rubric-based evaluation system to replace subjective LLM-as-a-Judge metrics.
- **⚠️ Limitations**: The work is strictly confined to clinical text reasoning and lacks any connection to physical world interaction, sensorimotor control, or embodied decision-making processes.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10367)
- **👥 Authors**: Zhiling Yan, Dingjie Song, Zhe Fang, Yisheng Ji, Xiang Li, Quanzheng Li, Lichao Sun
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Benchmarking Large Language Models for Knowledge Graph Validation (Score: 3/10)
- **💡 Innovation**: The paper introduces FactCheck, a benchmark specifically designed to evaluate the efficacy of LLMs in validating factual accuracy within structured Knowledge Graphs.
- **⚠️ Limitations**: The research focuses exclusively on symbolic knowledge verification and lacks any connection to physical grounding, sensorimotor tasks, or embodied reasoning.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10748)
- **👥 Authors**: Farzad Shami, Stefano Marchesin, Gianmaria Silvello
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents (Score: 3/10)
- **💡 Innovation**: The paper provides an empirical analysis demonstrating that agent-generated tests in software engineering tasks often serve as observational feedback rather than functional validation, offering little marginal utility for task resolution.
- **⚠️ Limitations**: The study is strictly confined to software engineering benchmarks (SWE-bench) and does not explore how these findings might generalize to embodied agents or physical world interaction where validation is inherently more complex.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.07900)
- **👥 Authors**: Zhi Chen, Zhensu Sun, Yuling Shi, Chao Peng, Xiaodong Gu, David Lo, Lingxiao Jiang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Spend Search Where It Pays: Value-Guided Structured Sampling and Optimization for Generative Recommendation (Score: 3/10)
- **💡 Innovation**: The paper introduces a value-guided tree search decoding strategy (VED) and a sibling-relative advantage estimation method (Sibling-GRPO) to mitigate probability-reward mismatch in autoregressive recommendation models.
- **⚠️ Limitations**: The work is strictly focused on generative recommendation systems and lacks any connection to physical environment interaction, world modeling, or embodied control tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10699)
- **👥 Authors**: Jie Jiang, Yangru Huang, Zeyu Wang, Changping Wang, Yuling Xiong, Jun Zhang, Huan Yu
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 Graph-Enhanced Deep Reinforcement Learning for Multi-Objective Unrelated Parallel Machine Scheduling (Score: 3/10)
- **💡 Innovation**: The paper applies a Graph Neural Network to encode state representations for the Unrelated Parallel Machine Scheduling Problem, which is then solved using a PPO-based reinforcement learning agent.
- **⚠️ Limitations**: The work focuses on combinatorial optimization in manufacturing scheduling rather than physical robot control, lacking any connection to embodied agents, vision-language models, or real-world robotic deployment.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.08052)
- **👥 Authors**: Bulent Soykan, Sean Mondesire, Ghaith Rabadi, Grace Bochenek
- **🏷️ Tags**: #Reinforcement_Learning

---

### 📄 StealthRL: Reinforcement Learning Paraphrase Attacks for Multi-Detector Evasion of AI-Text Detectors (Score: 3/10)
- **💡 Innovation**: The paper introduces a reinforcement learning framework (StealthRL) that utilizes GRPO and LoRA adapters to optimize adversarial paraphrasing for evading multiple AI-text detectors simultaneously.
- **⚠️ Limitations**: The research focuses exclusively on text-based adversarial robustness and lacks any connection to embodied agents, physical dynamics, or multimodal sensor integration relevant to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.08934)
- **👥 Authors**: Suraj Ranganath, Atharv Ramesh
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 Detecting Brick Kiln Infrastructure at Scale: Graph, Foundation, and Remote Sensing Models for Satellite Imagery Data (Score: 2/10)
- **💡 Innovation**: The paper introduces ClimateGraph, a region-adaptive graph-based model designed to leverage spatial and directional kiln layouts for large-scale satellite imagery monitoring.
- **⚠️ Limitations**: The research focuses exclusively on remote sensing and geospatial analysis, lacking any connection to embodied agents, robot control, or the specified robotics-centric research interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13350v1)
- **👥 Authors**: Usman Nazir, Xidong Chen, Hafiz Muhammad Abubakar, Hadia Abu Bakar, Raahim Arbaz, Fezan Rasool, Bin Chen, Sara Khalid
- **🏷️ Tags**: #Foundation_Model

---

### 📄 The Value Sensitivity Gap: How Clinical Large Language Models Respond to Patient Preference Statements in Shared Decision-Making (Score: 2/10)
- **💡 Innovation**: The paper introduces a quantitative framework to measure 'value sensitivity' in LLMs by evaluating how clinical decision support models align their recommendations with explicit patient preference statements.
- **⚠️ Limitations**: The study focuses exclusively on clinical decision-making and text-based preference alignment, offering no insights into embodied agents, physical world modeling, or action-space decision-making.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.00076v1)
- **👥 Authors**: Sanjay Basu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 CacheMind: From Miss Rates to Why -- Natural-Language, Trace-Grounded Reasoning for Cache Replacement (Score: 2/10)
- **💡 Innovation**: The paper introduces a RAG-based framework specifically tailored for microarchitectural cache trace analysis, enabling natural language querying of low-level CPU performance data.
- **⚠️ Limitations**: The work is strictly confined to CPU microarchitecture and cache replacement policies, offering no direct application or methodology transfer to embodied agents, robot control, or physical world modeling.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.12422v1)
- **👥 Authors**: Kaushal Mhapsekar, Azam Ghanbari, Bita Aslrousta, Samira Mirbagher-Ajorpaz
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 QP-OneModel: A Unified Generative LLM for Multi-Task Query Understanding in Xiaohongshu Search (Score: 2/10)
- **💡 Innovation**: The paper proposes a unified generative framework for query processing in social media search by reformulating heterogeneous sub-tasks into a single sequence generation paradigm optimized via multi-reward Reinforcement Learning.
- **⚠️ Limitations**: The work is entirely focused on natural language processing for search engine optimization and lacks any connection to physical agents, spatial reasoning, or embodied perception.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.09901)
- **👥 Authors**: Jianzhao Huang, Xiaorui Huang, Fei Zhao, Yunpeng Liu, Hui Zhang, Fangcheng Shi, Congfeng Li, Zechen Sun, Yi Wu, Yao Hu, Yunhan Bai, Shaosheng Cao
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Bielik Guard: Efficient Polish Language Safety Classifiers for LLM Content Moderation (Score: 2/10)
- **💡 Innovation**: The paper introduces a specialized, compact safety classification model fine-tuned specifically for the Polish language to improve moderation efficiency.
- **⚠️ Limitations**: The work is strictly focused on NLP-based content moderation and lacks any connection to embodied agents, multimodal perception, or robotic control tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.07954)
- **👥 Authors**: Krzysztof Wróbel, Jan Maria Kowalski, Jerzy Surma, Igor Ciuciura, Maciej Szymański
- **🏷️ Tags**: #LLM #Foundation_Model

---

