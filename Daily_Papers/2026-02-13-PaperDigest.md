# 📅 2026-02-13 - Paper Digest
## Summary
Total Papers: 45 | High Impact: 9

## 📝 Papers List
### 🔥 RISE: Self-Improving Robot Policy with Compositional World Model (Score: 9/10)
- **💡 Innovation**: The key novelty is the RISE framework that integrates a compositional world model with separate multi-view controllable dynamics prediction and progress value estimation modules to enable closed-loop robotic policy self-improvement via imagined rollouts, eliminating the need for costly on-policy real-world RL interaction while significantly boosting VLA performance on contact-rich dynamic manipulation tasks.
- **⚠️ Limitations**: The work does not analyze the compositional world model's out-of-distribution generalization ability, does not compare against alternative world model architectures such as diffusion models, and does not explore sim2real transfer performance for policies trained fully on imagined rollouts.
- **🔗 Link**: [[RISE]]
- **👥 Authors**: Jiazhi Yang, Kunyang Lin, Jinwei Li, Wencong Zhang, Tianwei Lin, Longyan Wu, Zhizhong Su, Hao Zhao, Ya-Qin Zhang, Li Chen, Ping Luo, Xiangyu Yue, Hongyang Li
- **🏷️ Tags**: #World_Model #Embodied_AI #Reinforcement_Learning #Robot_Manipulation #VLA

---

### 🔥 FlowHOI: Flow-based Semantics-Grounded Generation of Hand-Object Interactions for Dexterous Robot Manipulation (Score: 8/10)
- **💡 Innovation**: The key novelty is the two-stage flow-matching FlowHOI framework that explicitly models hand-object interaction structure to generate semantically grounded, temporally coherent HOI sequences for dexterous manipulation, paired with an egocentric video reconstruction pipeline to address high-fidelity HOI training data scarcity.
- **⚠️ Limitations**: The work lacks extensive evaluation of generalization to unseen object categories and long-horizon multi-step contact-rich tasks, and does not provide detailed analysis of real-robot retargeting performance across different dexterous hand morphologies.
- **🔗 Link**: [[FlowHOI]]
- **👥 Authors**: Huajian Zeng, Lingyun Chen, Jiaqi Yang, Yuantai Zhang, Fan Shi, Peidong Liu, Xingxing Zuo
- **🏷️ Tags**: #VLA #Robot_Manipulation #Embodied_AI #3D_Gaussian_Splatting

---

### 🔥 RynnBrain: Open Embodied Foundation Models (Score: 8/10)
- **💡 Innovation**: The key novelty is RynnBrain, an open-source unified spatiotemporal embodied foundation model family with three parameter scales and four task-specific post-trained variants that outperforms existing embodied foundation models by a large margin across 20 embodied and 8 vision understanding benchmarks, enabling physically grounded reasoning/planning and efficient downstream task adaptation.
- **⚠️ Limitations**: The abstract does not disclose critical implementation and validation details including model architecture design, training data curation pipeline, real-world robot deployment performance, and ablation studies verifying the contribution of each proposed core capability to the reported state-of-the-art results.
- **🔗 Link**: [[RynnBrain]]
- **👥 Authors**: Ronghao Dang, Jiayan Guo, Bohan Hou, Sicong Leng, Kehan Li, Xin Li, Jiangpin Liu, Yunxuan Mao, Zhikai Wang, Yuqian Yuan, Minghao Zhu, Xiao Lin, Yang Bai, Qian Jiang, Yaxi Zhao, Minghua Zeng, Junlong Gao, Yuming Jiang, Jun Cen, Siteng Huang, Liuyi Wang, Wenqiao Zhang, Chengju Liu, Jianfei Yang, Shijian Lu, Deli Zhao
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #VLA

---

### 🔥 Steerable Vision-Language-Action Policies for Embodied Reasoning and Hierarchical Control (Score: 8/10)
- **💡 Innovation**: The key novelty is the development of Steerable Vision-Language-Action (VLA) policies trained on synthetic commands spanning multiple abstraction levels (subtasks, motions, grounded pixel coordinates) to address the limited controllability of standard VLAs by high-level VLM reasoning, enabling improved generalization for long-horizon embodied manipulation tasks.
- **⚠️ Limitations**: The paper does not report the data efficiency of training steerable VLAs on multi-abstraction synthetic commands, nor does it explore integration with related popular paradigms such as diffusion models, world models, or reinforcement learning to further expand applicability.
- **🔗 Link**: [[Steerable_VisionLanguageAction_Policies_for_Embodied_Reasoning_and_Hierarchical_Control]]
- **👥 Authors**: William Chen, Jagdeep Singh Bhatia, Catherine Glossop, Nikhil Mathihalli, Ria Doshi, Andy Tang, Danny Driess, Karl Pertsch, Sergey Levine
- **🏷️ Tags**: #VLA #Embodied_AI #Robot_Manipulation #Foundation_Model #LLM

---

### 🔥 GigaBrain-0.5M*: a VLA That Learns From World Model-Based Reinforcement Learning (Score: 8/10)
- **💡 Innovation**: The key novelty is the proposal of GigaBrain-0.5M*, a VLA built on a large pre-trained robotic manipulation foundation model, that leverages the proposed RAMP framework to integrate world model-based reinforcement learning, enabling improved cross-task adaptation and robust long-horizon robot manipulation performance.
- **⚠️ Limitations**: This work lacks detailed ablation studies to isolate the performance contribution of each core component, only compares against the single RECAP baseline rather than a wider set of state-of-the-art VLAs, and provides no quantitative metrics for real-world deployment performance relying only on video validation.
- **🔗 Link**: [[GigaBrain05M]]
- **👥 Authors**: GigaBrain Team, Boyuan Wang, Chaojun Ni, Guan Huang, Guosheng Zhao, Hao Li, Jie Li, Jindi Lv, Jingyu Liu, Lv Feng, Mingming Yu, Peng Li, Qiuping Deng, Tianze Liu, Xinyu Zhou, Xinze Chen, Xiaofeng Wang, Yang Wang, Yifan Li, Yifei Nie, Yilong Li, Yukun Zhou, Yun Ye, Zhichao Liu, Zheng Zhu
- **🏷️ Tags**: #VLA #World_Model #Reinforcement_Learning #Robot_Manipulation #Foundation_Model

---

### 🔥 Sparse Video Generation Propels Real-World Beyond-the-View Vision-Language Navigation (Score: 8/10)
- **💡 Innovation**: The key novelty is the first application of long-horizon supervision-aligned video generation models to Beyond-the-View Navigation, paired with the proposed SparseVideoNav framework that reduces inference latency by 27x to enable sub-second 20-second horizon sparse trajectory generation for real-world deployment.
- **⚠️ Limitations**: The work lacks ablation studies to validate the contribution of individual components of SparseVideoNav, does not test performance on dynamic environments with moving obstacles, and does not report comparisons to non-LLM navigation baselines.
- **🔗 Link**: [[Sparse_Video_Generation_Propels_RealWorld_BeyondtheView_VisionLanguage_Navigation]]
- **👥 Authors**: Hai Zhang, Siqi Liang, Li Chen, Yuxian Li, Yukuan Xu, Yichao Zhong, Fu Zhang, Hongyang Li
- **🏷️ Tags**: #Embodied_AI #LLM #World_Model #Foundation_Model

---

### 🔥 ABot-N0: Technical Report on the VLA Foundation Model for Versatile Embodied Navigation (Score: 8/10)
- **💡 Innovation**: The key novelty is the ABot-N0 unified VLA foundation model with a hierarchical Brain-Action architecture pairing an LLM-based cognitive brain for semantic reasoning and a flow matching action expert for continuous trajectory generation, supported by a large-scale data engine curating 21.9M total samples across 7,802 3D scenes, that unifies 5 core embodied navigation tasks, achieves SOTA on 7 benchmarks, and enables robust long-horizon real-world navigation via an integrated agentic system with hierarchical topological memory.
- **⚠️ Limitations**: The work does not provide quantitative evaluations of sim2real transfer performance, does not compare its flow matching action generation approach to diffusion model baselines, does not explore integration with world models for improved unseen scene adaptation, and does not discuss extensibility to robot manipulation tasks.
- **🔗 Link**: [[ABotN0]]
- **👥 Authors**: Zedong Chu, Shichao Xie, Xiaolong Wu, Yanfen Shen, Minghua Luo, Zhengbo Wang, Fei Liu, Xiaoxu Leng, Junjun Hu, Mingyang Yin, Jia Lu, Yingnan Guo, Kai Yang, Jiawei Han, Xu Chen, Yanqing Zhu, Yuxiang Zhao, Xin Liu, Yirong Yang, Ye He, Jiahang Wang, Yang Cai, Tianlin Zhang, Li Gao, Liu Liu, Mingchao Sun, Fan Jiang, Chiyu Wang, Zhicheng Liu, Hongyu Pan, Honglin Han, Zhining Gu, Kuan Yang, Jianfang Zhang, Di Jing, Zihao Guan, Wei Guo, Guoqing Liu, Di Yang, Xiangpo Yang, Menglin Yang, Hongguang Xing, Weiguo Li, Mu Xu
- **🏷️ Tags**: #VLA #Embodied_AI #Foundation_Model #LLM

---

### ✨ AsyncVLA: An Asynchronous VLA for Fast and Robust Navigation on the Edge (Score: 7/10)
- **💡 Innovation**: The key novelty is the AsyncVLA asynchronous control framework that decouples high-level semantic reasoning from remote large foundation models and high-frequency reactive execution on edge devices, supported by an end-to-end finetuning protocol and trajectory re-weighting strategy to handle asynchronous streams and up to 6 seconds of communication delay.
- **⚠️ Limitations**: The work is only evaluated on vision-based navigation tasks, does not test generalization to other common robotic tasks such as manipulation, and does not explore integration with predictive components like world models to further improve performance in highly dynamic environments.
- **🔗 Link**: [[AsyncVLA]]
- **👥 Authors**: Noriaki Hirose, Catherine Glossop, Dhruv Shah, Sergey Levine
- **🏷️ Tags**: #VLA #Foundation_Model #Embodied_AI #LLM

---

### ✨ Dreaming in Code for Curriculum Learning in Open-Ended Worlds (Score: 7/10)
- **💡 Innovation**: The key novelty is the proposed Dreaming in Code (DiCode) framework that leverages foundation models to synthesize executable code-level environment variations to automatically build scaffolding curricula that enable reinforcement learning agents to make sustained progression in complex open-ended worlds with large combinatorial challenge spaces.
- **⚠️ Limitations**: The work is only validated on the 2D Craftax game benchmark, with no demonstration of applicability to embodied robotics domains, and does not include comparisons to state-of-the-art curriculum learning methods designed for embodied AI or robot learning tasks.
- **🔗 Link**: [[Dreaming_in_Code_for_Curriculum_Learning_in_OpenEnded_Worlds]]
- **👥 Authors**: Konstantinos Mitsides, Maxence Faldor, Antoine Cully
- **🏷️ Tags**: #Foundation_Model #Reinforcement_Learning #LLM

---

### ✨ Think Longer to Explore Deeper: Learn to Explore In-Context via Length-Incentivized Reinforcement Learning (Score: 6/10)
- **💡 Innovation**: The key novelty is proposing Length-Incentivized Exploration, a reinforcement learning method combining length-based reward and redundancy penalty to mitigate the newly identified shallow exploration trap and improve in-context exploration performance of large language models.
- **⚠️ Limitations**: The work only evaluates the proposed method on general LLM text reasoning benchmarks, with no validation of its applicability to embodied AI, robot manipulation, VLA, or other robotics-related use cases, and does not test its performance on multimodal foundation models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.11748)
- **👥 Authors**: Futing Wang, Jianhao Yan, Yun Luo, Ganqu Cui, Zhi Wang, Xiaoye Qu, Yue Zhang, Yu Cheng, Tao Lin
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Gaia2: Benchmarking LLM Agents on Dynamic and Asynchronous Environments (Score: 6/10)
- **💡 Innovation**: The key novelty is the introduction of Gaia2, the first benchmark for evaluating LLM agents in realistic asynchronous dynamic environments with fine-grained action-level verifiers that enable direct use for reinforcement learning from verifiable rewards.
- **⚠️ Limitations**: The paper does not support or evaluate integration with world models, diffusion models, vision-language-action models, or robot manipulation tasks, and lacks deep root cause analysis of model failures on time-sensitive dynamic scenarios.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.11964)
- **👥 Authors**: Romain Froger, Pierre Andrews, Matteo Bettini, Amar Budhiraja, Ricardo Silveira Cabral, Virginie Do, Emilien Garreau, Jean-Baptiste Gaya, Hugo Laurençon, Maxime Lecanu, Kunal Malkan, Dheeraj Mekala, Pierre Ménard, Gerard Moreno-Torres Bertran, Ulyana Piterbarg, Mikhail Plekhanov, Mathieu Rita, Andrey Rusakov, Vladislav Vorotilov, Mengjue Wang, Ian Yu, Amine Benhalloum, Grégoire Mialon, Thomas Scialom
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning #Sim2Real #Embodied_AI

---

### 📄 SpargeAttention2: Trainable Sparse Attention via Hybrid Top-k+Top-p Masking and Distillation Fine-Tuning (Score: 4/10)
- **💡 Innovation**: The key novelty is the proposed SpargeAttention2, a trainable sparse attention method that combines a hybrid Top-k+Top-p masking rule, efficient trainable sparse attention implementation, and a distillation-inspired fine-tuning objective to achieve high attention sparsity and significant speedup without degrading video diffusion generation quality.
- **⚠️ Limitations**: This work is only evaluated on video diffusion generation tasks, with no exploration of the applicability of the proposed sparse attention method to other relevant domains in your research interests such as embodied AI, robot manipulation, or vision-language-action models, nor validation on large language models or general foundation models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13515v1)
- **👥 Authors**: Jintao Zhang, Kai Jiang, Chendong Xiang, Weiqi Feng, Yuezhou Hu, Haocheng Xi, Jianfei Chen, Jun Zhu
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 Unveiling Implicit Advantage Symmetry: Why GRPO Struggles with Exploration and Difficulty Adaptation (Score: 4/10)
- **💡 Innovation**: The key novelty is identifying that implicit advantage symmetry in Group Relative Advantage Estimation (GRAE) causes GRPO's poor exploration and difficulty adaptation, and proposing Asymmetric GRAE (A-GRAE) that dynamically modulates exploration incentives and sample difficulty focus to improve performance across LLM and MLLM benchmarks.
- **⚠️ Limitations**: The work only evaluates A-GRAE on LLM/MLLM reasoning tasks, with no validation of its performance on robotics, embodied AI, or other RL application domains relevant to your stated interests, and provides no analysis of its compatibility with robotics-aligned foundation models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.05548)
- **👥 Authors**: Zhiqi Yu, Zhangquan Chen, Mengting Liu, Heye Zhang, Liangqiong Qu
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 MetaphorStar: Image Metaphor Understanding and Reasoning with End-to-End Visual Reinforcement Learning (Score: 4/10)
- **💡 Innovation**: The key novelty is the proposal of MetaphorStar, the first end-to-end visual reinforcement learning framework for image metaphor implication tasks, paired with a custom fine-grained dataset, dedicated RL training method, and standardized benchmark that achieves SOTA performance over 20+ mainstream MLLMs on related tasks.
- **⚠️ Limitations**: The work is restricted to visual metaphor reasoning tasks, does not explore applicability to your core robotics/embodied AI related research interests, and lacks deep ablation of how the proposed RL method outperforms standard MLLM fine-tuning for visual reasoning tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10575)
- **👥 Authors**: Chenhao Zhang, Yazhe Niu, Hongsheng Li
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 Budget-Constrained Agentic Large Language Models: Intention-Based Planning for Costly Tool Use (Score: 4/10)
- **💡 Innovation**: The key novelty is the proposed INTENT inference-time planning framework that leverages an intention-aware hierarchical world model to anticipate future tool usage and associated risk-calibrated costs, enabling budget-constrained LLM-based tool-augmented agents to maintain hard budget feasibility while achieving higher task success rates than existing baselines.
- **⚠️ Limitations**: The work is only evaluated on the text-based StableToolBench benchmark for tool use, with no exploration of applicability to embodied or robotics tasks, no validation with real-world physical tool execution, and no analysis of how the framework would perform when integrated with vision or robotic actuation modules.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.11541)
- **👥 Authors**: Hanbing Liu, Chunhao Tian, Nan An, Ziyuan Wang, Pinyan Lu, Changyuan Yu, Qi Qi
- **🏷️ Tags**: #LLM #Foundation_Model #World_Model

---

### 📄 Preventing Rank Collapse in Federated Low-Rank Adaptation with Client Heterogeneity (Score: 3/10)
- **💡 Innovation**: The key novelty is identifying the previously overlooked rank collapse phenomenon in heterogeneous federated low-rank adaptation, theoretically revealing its root cause of mismatched rank-agnostic aggregation weights and rank-dependent client contributions, and proposing the rank-partitioned raFLoRA aggregation method to mitigate the issue while preserving communication efficiency.
- **⚠️ Limitations**: The paper only evaluates raFLoRA on generic classification and reasoning tasks, with no exploration of its performance on robotics, embodied AI or other downstream use cases relevant to your research interests, and no analysis of its compatibility with task-specific foundation models like VLAs or domain-specific LLMs.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13486v1)
- **👥 Authors**: Fei Wu, Jia Hu, Geyong Min, Shiqiang Wang
- **🏷️ Tags**: #Foundation_Model #Federated_Learning #LoRA #Rank_Collapse #Parameter_Efficient_Fine_Tuning

---

### 📄 On-Policy Supervised Fine-Tuning for Efficient Reasoning (Score: 3/10)
- **💡 Innovation**: The key novelty is simplifying prior complex RL-based training paradigms for large reasoning models by removing KL regularization and group-wise normalization, replacing multi-reward objectives with a simple truncation-based length penalty to reduce the training problem to supervised fine-tuning on filtered self-generated on-policy data that achieves state-of-the-art accuracy-efficiency Pareto frontier performance.
- **⚠️ Limitations**: The work only evaluates on text reasoning benchmarks, does not test applicability to robotics or embodied AI pipelines, and lacks analysis of how its method performs when scaled to extremely large foundation model sizes.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13407v1)
- **👥 Authors**: Anhao Zhao, Ziyang Chen, Junlong Tong, Yingqi Fan, Fanghua Ye, Shuhao Li, Yunpu Ma, Wenjie Li, Xiaoyu Shen
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### 📄 Composition-RL: Compose Your Verifiable Prompts for Reinforcement Learning of Large Language Models (Score: 3/10)
- **💡 Innovation**: The key novelty is Composition-RL, a simple approach that automatically composes multiple easy pass-rate-1 verifiable prompts into new valid compositional prompts for LLM RL training, paired with a curriculum variant that gradually increases compositional depth to further boost performance and enable more effective cross-domain RL.
- **⚠️ Limitations**: This work is only validated on general LLM reasoning tasks, with no exploration of applicability to robotics or embodied AI scenarios, and does not analyze the upper limit of compositional depth before generated prompts lose coherence or verifiability.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12036)
- **👥 Authors**: Xin Xu, Clive Bai, Kai Yang, Tianhao Chen, Yangkun Chen, Weijie Liu, Hao Chen, Yang Wang, Saiyong Yang, Can Yang
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 DeepGen 1.0: A Lightweight Unified Multimodal Model for Advancing Image Generation and Editing (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposed Stacked Channel Bridging deep alignment framework for fusing hierarchical VLM features with learnable think tokens, paired with a three-stage progressive data-centric training strategy including RL with MR-GRPO, to enable a lightweight 5B unified multimodal model to outperform much larger state-of-the-art image generation and editing models.
- **⚠️ Limitations**: This work is limited exclusively to 2D image generation and editing tasks, provides no exploration of its methods' applicability to robotics or embodied AI use cases, and does not assess whether its lightweight design could support low-latency deployment on resource-constrained robotic edge platforms.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12205)
- **👥 Authors**: Dianyi Wang, Ruihang Li, Feng Han, Chaofan Ma, Wei Song, Siyuan Wang, Yibin Wang, Yi Xin, Hongjian Liu, Zhixiong Zhang, Shengyuan Ding, Tianhang Wang, Zhenglin Cheng, Tao Lin, Cheng Jin, Kaicheng Yu, Jingjing Chen, Wenjie Wang, Zhongyu Wei, Jiaqi Wang
- **🏷️ Tags**: #Diffusion_Model #Reinforcement_Learning #Foundation_Model

---

### 📄 Learning beyond Teacher: Generalized On-Policy Distillation with Reward Extrapolation (Score: 3/10)
- **💡 Innovation**: This work theoretically frames on-policy distillation as a special case of dense KL-constrained reinforcement learning, and proposes the Generalized On-Policy Distillation framework with a flexible reference model and adjustable reward scaling factor that enables student models to outperform teachers in knowledge merging and strong-to-weak distillation settings.
- **⚠️ Limitations**: The proposed framework is only validated on math reasoning and code generation tasks with no evaluation on robotics or embodied AI use cases, and its reward correction variant requires access to the teacher's pre-RL base model which introduces extra computational overhead and is not always available.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12125)
- **👥 Authors**: Wenkai Yang, Weijie Liu, Ruobing Xie, Kai Yang, Saiyong Yang, Yankai Lin
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 dVoting: Fast Voting for dLLMs (Score: 3/10)
- **💡 Innovation**: The key novelty is dVoting, a training-free fast voting technique for diffusion large language models that iteratively identifies uncertain tokens via cross-sample consistency analysis and regenerates only those tokens to boost reasoning performance with acceptable extra computational overhead.
- **⚠️ Limitations**: The work only evaluates dVoting on standard natural language reasoning benchmarks, with no exploration of applications to robotics or embodied AI domains, nor does it analyze its performance and efficiency tradeoffs on extremely long sequence generation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12153)
- **👥 Authors**: Sicheng Feng, Zigeng Chen, Xinyin Ma, Gongfan Fang, Xinchao Wang
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #LLM

---

### 📄 PISCO: Precise Video Instance Insertion with Sparse Control (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposed PISCO video diffusion model that supports precise video instance insertion with arbitrary sparse keyframe control, paired with three targeted technical components (Variable-Information Guidance, Distribution-Preserving Temporal Masking, geometry-aware conditioning) to resolve distribution shift and stabilize temporal generation, plus a dedicated PISCO-Bench benchmark for standardized evaluation of this task.
- **⚠️ Limitations**: The work is only validated on general video editing and filmmaking use cases, with no exploration of applications to embodied AI, robotics or world modeling, and no integration with LLMs or VLAs for more intuitive natural language control of the instance insertion task.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.08277)
- **👥 Authors**: Xiangbo Gao, Renjie Li, Xinghao Chen, Yuheng Wu, Suofei Feng, Qing Yin, Zhengzhong Tu
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 MemFly: On-the-Fly Memory Optimization via Information Bottleneck (Score: 3/10)
- **💡 Innovation**: The key novelty is MemFly, an information bottleneck-grounded on-the-fly memory evolution framework for LLMs that uses a gradient-free optimizer to balance compression efficiency and retrieval precision, paired with a hybrid semantic-symbolic-topological retrieval mechanism for complex multi-hop queries.
- **⚠️ Limitations**: The work only validates MemFly on generic LLM agent tasks, with no exploration of its applicability for embodied AI, robotics, or cross-modal agent scenarios, and no comparison with memory optimization methods tailored for robotics or reinforcement learning pipelines.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.07885)
- **👥 Authors**: Zhenyuan Zhang, Xianzhang Jia, Zhiqin Yang, Zhenbo Song, Wei Xue, Sirui Han, Yike Guo
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 P-GenRM: Personalized Generative Reward Model with Test-time User-based Scaling (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposed P-GenRM personalized generative reward model, which transforms preference signals into structured evaluation chains, clusters users into User Prototypes, and introduces a dual-granularity test-time user-based scaling mechanism to reduce preference inference noise and improve generalization to unseen users.
- **⚠️ Limitations**: The work only validates the proposed method on text-based personalized reward model benchmarks, does not explore its applicability to domains like embodied AI or robotics, and fails to analyze the computational overhead of the test-time scaling mechanism for real-world large-scale deployment.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12116)
- **👥 Authors**: Pinyi Zhang, Ting-En Lin, Yuchuan Wu, Jingyang Chen, Zongqi Wang, Hua Yang, Ze Xu, Fei Huang, Kai Zhang, Yongbin Li
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Detecting RLVR Training Data via Structural Convergence of Reasoning (Score: 3/10)
- **💡 Innovation**: The key novelty is the design of the Min-kNN Distance, a reference-free black-box detector that identifies membership of prompts in RLVR training datasets by measuring the reduced generation diversity for seen prompts, outperforming existing membership inference baselines.
- **⚠️ Limitations**: The work only evaluates the proposed detector on text-only reasoning RLVR models, and does not explore its applicability to RL-trained models for embodied AI, robot manipulation or vision-language-action use cases, nor analyzes robustness to changes in RLVR reward function or sampling hyperparameters.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.11792)
- **👥 Authors**: Hongbo Zhang, Yue Yang, Jianhao Yan, Guangsheng Bao, Yue Zhang, Yue Zhang
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 Arming Data Agents with Tribal Knowledge (Score: 2/10)
- **💡 Innovation**: The key novelty is Tk-Boost, a bolt-on framework for NL2SQL agents that identifies agent misconceptions via test query performance analysis, generates targeted corrective tribal knowledge indexed by query applicability conditions, and injects this knowledge during inference to improve SQL generation accuracy.
- **⚠️ Limitations**: The work is only evaluated on static public NL2SQL benchmarks, and does not test performance on dynamic real-world databases, explore generalization to other LLM agent task domains, or measure inference time overhead introduced by the framework.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13521v2)
- **👥 Authors**: Shubham Agarwal, Asim Biswal, Sepanta Zeighami, Alvin Cheung, Joseph Gonzalez, Aditya G. Parameswaran
- **🏷️ Tags**: #LLM #Foundation_Model #NL2SQL

---

### 📄 SPILLage: Agentic Oversharing on the Web (Score: 2/10)
- **💡 Innovation**: The key novelty is formalizing the concept of Natural Agentic Oversharing for LLM-powered web agents, introducing the SPILLage taxonomy that classifies oversharing across content/behavior channels and explicit/implicit directness, and empirically demonstrating that behavioral oversharing is 5 times more prevalent than content oversharing even under common prompt mitigation strategies.
- **⚠️ Limitations**: The work only evaluates oversharing on live e-commerce websites across a small set of agent frameworks and backbone LLMs, does not test generalizability to other web task domains, and only explores one effective mitigation approach for the identified privacy risks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13516v1)
- **👥 Authors**: Jaechul Roh, Eugene Bagdasarian, Hamed Haddadi, Ali Shahin Shamsabadi
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Benchmarking Video Foundation Models for Remote Parkinson's Disease Screening (Score: 2/10)
- **💡 Innovation**: This work conducts a large-scale systematic benchmark of seven state-of-the-art video foundation models on a novel Parkinson's disease screening dataset covering 1,888 participants and 32,847 videos across 16 standardized clinical tasks, identifying model-specific performance strengths for different clinical assessment scenarios.
- **⚠️ Limitations**: The work only evaluates frozen video foundation model embeddings with linear classification heads, has low Parkinson's disease detection sensitivity (43.2 - 57.3%), does not explore fine-tuning or multi-modal fusion to improve performance, and has no relevance to robotics or general AI use cases outside remote neurological monitoring.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13507v2)
- **👥 Authors**: Md Saiful Islam, Ekram Hossain, Abdelrahman Abdelkader, Tariq Adnan, Fazla Rabbi Mashrur, Sooyong Park, Praveen Kumar, Qasim Sudais, Natalia Chunga, Nami Shah, Jan Freyberg, Christopher Kanan, Ruth Schneider, Ehsan Hoque
- **🏷️ Tags**: #Foundation_Model

---

### 📄 From Perceptions To Evidence: Detecting AI-Generated Content In Turkish News Media With A Fine-Tuned Bert Classifier (Score: 2/10)
- **💡 Innovation**: This work presents the first empirical, data-driven measurement of LLM usage in Turkish news media by fine-tuning a Turkish-specific BERT classifier for AI-rewritten content detection, filling the gap of prior lack of quantitative research on this topic for the Turkish language.
- **⚠️ Limitations**: The study only evaluates detection of AI-rewritten rather than fully original AI-generated news, and does not validate model generalizability to smaller Turkish news outlets or content generated by newer, more advanced LLMs released after its dataset collection period.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13504v1)
- **👥 Authors**: Ozancan Ozdemir
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 GLIMPSE : Real-Time Text Recognition and Contextual Understanding for VQA in Wearables (Score: 2/10)
- **💡 Innovation**: The key novelty is exploiting the asymmetric resolution requirements of OCR (high resolution) and scene understanding (low resolution) to build a hybrid architecture that runs selective high-resolution on-device OCR alongside low-resolution video streaming for visual context, reducing power consumption by more than half while maintaining strong Text VQA accuracy on resource-constrained wearables.
- **⚠️ Limitations**: The work only evaluates on static offline Text VQA benchmarks, does not test performance on dynamic real-world wearable scenarios with fast motion or rapidly changing text, and has no connection to robotics or embodied AI use cases.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13479v1)
- **👥 Authors**: Akhil Ramachandran, Ankit Arun, Ashish Shenoy, Abhay Harpale, Srihari Jayakumar, Debojeet Chatterjee, Mohsen Moslehpour, Pierce Chuang, Yichao Lu, Vikas Bhardwaj, Peyman Heidari
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 OMNI-LEAK: Orchestrator Multi-Agent Network Induced Data Leakage (Score: 2/10)
- **💡 Innovation**: The key novelty is the identification and demonstration of the OMNI-LEAK attack vector, which exploits vulnerabilities in orchestrator-pattern multi-agent LLM systems to leak sensitive data through a single indirect prompt injection even when data access controls are active.
- **⚠️ Limitations**: The work only evaluates the proposed attack on a narrow set of orchestrator multi-agent setups and does not propose or test any actionable mitigation strategies for the identified vulnerability.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13477v2)
- **👥 Authors**: Akshat Naik, Jay Culligan, Yarin Gal, Philip Torr, Rahaf Aljundi, Alasdair Paren, Adel Bibi
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 NeuroWeaver: An Autonomous Evolutionary Agent for Exploring the Programmatic Space of EEG Analysis Pipelines (Score: 2/10)
- **💡 Innovation**: The key novelty is NeuroWeaver, a unified autonomous evolutionary agent that reformulates EEG analysis pipeline engineering as a discrete constrained optimization problem with domain-informed subspace initialization and multi-objective evolutionary optimization to produce lightweight, neuroscientifically plausible pipelines that outperform task-specific state-of-the-art methods and match large foundation model performance with far fewer parameters.
- **⚠️ Limitations**: This work lacks validation of real clinical deployment feasibility, does not test generalizability to other neuroimaging modalities beyond EEG, and does not compare against foundation models explicitly fine-tuned for EEG analysis tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13473v1)
- **👥 Authors**: Guoan Wang, Shihao Yang, Jun-En Ding, Hao Zhu, Feng Liu
- **🏷️ Tags**: #Foundation_Model #Evolutionary_Optimization #EEG_Analysis #Automated_Machine_Learning #Constrained_Optimization

---

### 📄 How Multimodal Large Language Models Support Access to Visual Information: A Diary Study With Blind and Low Vision People (Score: 2/10)
- **💡 Innovation**: This work conducts a two-week diary study with 20 blind and low vision participants to evaluate real-world usage, user satisfaction and gaps of MLLM-enabled visual interpretation applications, and proposes the novel "visual assistant" skill and corresponding design guidelines to better support BLV users' visual information access.
- **⚠️ Limitations**: The study only evaluates a single MLLM-enabled visual interpretation tool, lacks comparative analysis against traditional non-MLLM visual accessibility tools, and does not provide concrete technical implementations for the proposed "visual assistant" skill.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13469v2)
- **👥 Authors**: Ricardo E. Gonzalez Penuela, Crescentia Jung, Sharon Y Lin, Ruiying Hu, Shiri Azenkot
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 LLM-Powered Automatic Translation and Urgency in Crisis Scenarios (Score: 2/10)
- **💡 Innovation**: This work introduces a novel 32-language urgency-annotated crisis dataset, and empirically demonstrates that both dedicated translation models and LLMs exhibit substantial performance degradation, instability, and urgency distortion when applied to crisis domain translation, with LLM urgency classification performance varying heavily based on input and prompt language.
- **⚠️ Limitations**: The work only identifies risks and performance gaps of existing systems for crisis domain translation, but does not propose any targeted mitigation strategies, fine-tuning approaches, or crisis-aware model architectures to address the identified issues.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13452v1)
- **👥 Authors**: Belu Ticona, Antonis Anastasopoulos
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Backdooring Bias in Large Language Models (Score: 2/10)
- **💡 Innovation**: The key novelty is conducting over 1000 controlled evaluations to analyze both syntactically and semantically triggered backdoor attacks for bias induction in LLMs under a white-box threat model where the model builder acts as the adversary, as well as quantifying the performance and tradeoffs of two representative backdoor defense paradigms.
- **⚠️ Limitations**: The study does not test the generalizability of its findings across diverse LLM architectures and parameter scales, nor does it explore novel mitigation strategies that avoid the observed tradeoffs between defense efficacy, model utility, and computational overhead.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13427v1)
- **👥 Authors**: Anudeep Das, Prach Chantasantitam, Gurjot Singh, Lipeng He, Mariia Ponomarenko, Florian Kerschbaum
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Protect$^*$: Steerable Retrosynthesis through Neuro-Symbolic State Encoding (Score: 2/10)
- **💡 Innovation**: The key novelty is the Protect* neuro-symbolic framework that combines rule-based chemical symbolic reasoning with LLM generative capabilities to enable steerable retrosynthesis by guarding chemically sensitive molecular sites and injecting hard symbolic constraints during neural inference.
- **⚠️ Limitations**: The work only provides qualitative case study validation on chemical retrosynthesis tasks, lacks quantitative performance comparisons against state-of-the-art retrosynthesis methods, and has no demonstrated generalizability to domains outside chemistry.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13419v1)
- **👥 Authors**: Shreyas Vinaya Sathyanarayana, Shah Rahil Kirankumar, Sharanabasava D. Hiremath, Bharath Ramsundar
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Semantic Chunking and the Entropy of Natural Language (Score: 2/10)
- **💡 Innovation**: This work introduces a novel first-principles statistical model based on hierarchical self-similar semantic chunking of text that accurately explains the observed ~1 bit per character entropy rate of printed English and predicts that language entropy systematically scales with corpus semantic complexity.
- **⚠️ Limitations**: The work is limited to theoretical and experimental analysis of natural language entropy and semantic structure, with no exploration of applications to robotics, embodied AI, or other domains relevant to the user's stated interests, and does not validate the model's utility for practical downstream use cases beyond entropy prediction.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13194v2)
- **👥 Authors**: Weishun Zhong, Doron Sivan, Tankut Can, Mikhail Katkov, Misha Tsodyks
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 The Devil Behind Moltbook: Anthropic Safety is Always Vanishing in Self-Evolving AI Societies (Score: 2/10)
- **💡 Innovation**: The key novelty is formalizing the self-evolution trilemma for multi-agent AI societies via an information-theoretic framework, theoretically and empirically demonstrating that isolated continuously self-evolving LLM-based systems cannot sustain consistent anthropic safety alignment.
- **⚠️ Limitations**: The work only provides high-level proposed solution directions rather than concrete, fully validated safety-preserving mechanisms, and does not extend its analysis to embodied AI or robotics-related use cases relevant to your research interests.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.09877)
- **👥 Authors**: Chenxu Wang, Chaozhuo Li, Songyang Liu, Zejian Chen, Jinyu Hou, Ji Qi, Rui Li, Litian Zhang, Qiwei Ye, Zheng Liu, Xu Chen, Xi Zhang, Philip S. Yu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 MOSS-Audio-Tokenizer: Scaling Audio Tokenizers for Future Audio Foundation Models (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed fully end-to-end, purely Transformer-based Causal Audio Tokenizer (CAT) architecture, and the 1.6B parameter MOSS-Audio-Tokenizer pre-trained on 3 million hours of diverse audio data that outperforms prior state-of-the-art audio codecs across speech, sound, and music domains, enabling leading autoregressive TTS and competitive ASR performance without auxiliary encoders.
- **⚠️ Limitations**: The paper only evaluates the proposed tokenizer on audio-specific tasks, does not explore its integration with multi-modal foundation models or downstream use cases like embodied AI/robotics, and provides no analysis of cross-modal performance when paired with LLMs for non-audio tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10934)
- **👥 Authors**: Yitian Gong, Kuangwei Chen, Zhaoye Fei, Xiaogui Yang, Ke Chen, Yang Wang, Kexin Huang, Mingshu Chen, Ruixiao Li, Qingyuan Cheng, Shimin Li, Xipeng Qiu
- **🏷️ Tags**: #Foundation_Model #LLM

---

### 📄 DeepSight: An All-in-One LM Safety Toolkit (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposal of the first open-source integrated large model safety toolkit that unifies safety evaluation and diagnosis workflows, bridging black-box external risk identification to white-box internal root cause analysis to reduce general capability degradation during safety alignment.
- **⚠️ Limitations**: The work lacks quantitative experimental validation of the toolkit's performance against existing separate safety evaluation and diagnosis tools, and does not demonstrate its effectiveness across diverse real-world LLM and MLLM deployment scenarios.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12092)
- **👥 Authors**: Bo Zhang, Jiaxuan Guo, Lijun Li, Dongrui Liu, Sujin Chen, Guanxu Chen, Zhijie Zheng, Qihao Lin, Lewen Yan, Chen Qian, Yijin Zhou, Yuyao Wu, Shaoxiong Guo, Tianyi Du, Jingyi Yang, Xuhao Hu, Ziqi Miao, Xiaoya Lu, Jing Shao, Xia Hu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 T3D: Few-Step Diffusion Language Models via Trajectory Self-Distillation with Direct Discriminative Optimization (Score: 2/10)
- **💡 Innovation**: The key novelty is a trajectory self-distillation framework integrated with a reverse-KL based Direct Discriminative Optimization objective to improve few-step decoding quality of diffusion large language models by distilling the model's own generative trajectories.
- **⚠️ Limitations**: The proposed approach still underperforms full-step diffusion LLM decoding on generation quality, is only evaluated on standard text generation benchmarks, and has not been explored for use cases relevant to robotics or embodied AI.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12262)
- **👥 Authors**: Tunyu Zhang, Xinxi Zhang, Ligong Han, Haizhou Shi, Xiaoxiao He, Zhuowei Li, Hao Wang, Kai Xu, Akash Srivastava, Hao Wang, Vladimir Pavlovic, Dimitris N. Metaxas
- **🏷️ Tags**: #Diffusion_Model #LLM #Foundation_Model

---

### 📄 MiniCPM-SALA: Hybridizing Sparse and Linear Attention for Efficient Long-Context Modeling (Score: 2/10)
- **💡 Innovation**: The key novelty is the 9B-parameter MiniCPM-SALA hybrid attention architecture that integrates sparse attention and linear attention in a 1:3 ratio with hybrid positional encoding, paired with a low-cost continual training framework that reduces training cost by ~75% compared to training from scratch while maintaining strong long-context performance and efficiency.
- **⚠️ Limitations**: The paper only evaluates the model on general language tasks, does not explore applications to downstream robotics or embodied AI domains relevant to your interests, and lacks comparison against other state-of-the-art long-context small LLM baselines beyond full-attention models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.11761)
- **👥 Authors**: MiniCPM Team, Wenhao An, Yingfa Chen, Yewei Fang, Jiayi Li, Xin Li, Yaohui Li, Yishan Li, Yuxuan Li, Biyuan Lin, Chuan Liu, Hezi Liu, Siyuan Liu, Hongya Lyu, Yinxu Pan, Shixin Ren, Xingyu Shen, Zhou Su, Haojun Sun, Yangang Sun, Zhen Leng Thai, Xin Tian, Rui Wang, Xiaorong Wang, Yudong Wang, Bo Wu, Xiaoyue Xu, Dong Xu, Shuaikang Xue, Jiawei Yang, Bowen Zhang, Jinqian Zhang, Letian Zhang, Shengnan Zhang, Xinyu Zhang, Xinyuan Zhang, Zhu Zhang, Hengyu Zhao, Jiacheng Zhao, Jie Zhou, Zihan Zhou, Shuo Wang, Chaojun Xiao, Xu Han, Zhiyuan Liu, Maosong Sun
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Pretraining A Large Language Model using Distributed GPUs: A Memory-Efficient Decentralized Paradigm (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed SParse Expert Synchronization (SPES) framework that trains only a subset of Mixture-of-Experts LLM experts per node to reduce memory footprint, paired with an expert-merging warm-up strategy to accelerate convergence for decentralized LLM pretraining.
- **⚠️ Limitations**: The work only evaluates performance on general LLM benchmarks, does not explore applications of the trained models to downstream robotics or embodied AI tasks, and lacks testing on lower-spec consumer GPU setups to expand accessibility.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.11543)
- **👥 Authors**: Jinrui Zhang, Chaodong Xiao, Aoqi Wu, Xindong Zhang, Lei Zhang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Sci-CoE: Co-evolving Scientific Reasoning LLMs via Geometric Consensus with Sparse Supervision (Score: 2/10)
- **💡 Innovation**: The key novelty is the two-stage Sci-CoE co-evolution framework that first uses sparse annotated data to build verifier correctness judgment anchors, then leverages a geometric reward mechanism accounting for consensus, reliability and diversity to drive unsupervised self-iteration of LLMs acting as both solver and verifier on unlabeled scientific data.
- **⚠️ Limitations**: The work only validates performance on text-only scientific reasoning benchmarks, does not explore applicability to multimodal, robotics or embodied AI use cases, and provides no analysis of how the co-evolution approach could integrate with other foundation model paradigms like VLAs or world models for downstream robotic tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12164)
- **👥 Authors**: Xiaohan He, Shiyang Feng, Songtao Huang, Lei Bai, Bin Wang, Bo Zhang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Multimodal Fact-Level Attribution for Verifiable Reasoning (Score: 2/10)
- **💡 Innovation**: The key novelty is the introduction of the MuRGAt benchmark for evaluating fact-level multimodal attribution in complex multi-step reasoning scenarios spanning multiple modalities including video and audio, paired with an automatic evaluation framework that strongly correlates with human judgments.
- **⚠️ Limitations**: The work does not explore applications of the proposed attribution benchmark or evaluation method to downstream robotics, embodied AI, or interactive real-world tasks, nor does it propose solutions to the observed trade-off between reasoning depth and attribution accuracy.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.11509)
- **👥 Authors**: David Wan, Han Wang, Ziyang Wang, Elias Stengel-Eskin, Hyunji Lee, Mohit Bansal
- **🏷️ Tags**: #Foundation_Model #LLM

---


