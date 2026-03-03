# 📅 2026-03-02 - Paper Digest
## Summary
Total Papers: 27 | High Impact: 1

## 📝 Papers List
### ✨ OnlineX: Unified Online 3D Reconstruction and Understanding with Active-to-Stable State Evolution (Score: 7/10)
- **💡 Innovation**: The key novelty is the proposed decoupled active-to-stable state evolution paradigm that splits memory states to mitigate cumulative drift, enabling a feed-forward framework for online joint 3D visual appearance and language field reconstruction directly from streaming image inputs.
- **⚠️ Limitations**: The work only evaluates performance on standard 3D reconstruction datasets, and does not validate its practical utility on real robotic platforms or integration with downstream embodied AI tasks such as robot manipulation or vision-language-action planning.
- **🔗 Link**: [[OnlineX]]
- **👥 Authors**: Chong Xia, Fangfu Liu, Yule Wang, Yize Pang, Yueqi Duan
- **🏷️ Tags**: #3D_Gaussian_Splatting #Embodied_AI #Foundation_Model

---

### ✨ ACDC: Adaptive Curriculum Planning with Dynamic Contrastive Control for Goal-Conditioned Reinforcement Learning in Robotic Manipulation (Score: 6/10)
- **💡 Innovation**: The key novelty is the proposed ACDC paradigm that combines adaptive curriculum planning which dynamically balances diversity-driven exploration and quality-driven exploitation based on agent training progress, with dynamic contrastive control that uses norm-constrained contrastive learning for magnitude-guided experience selection aligned with the current curriculum focus for goal-conditioned robotic manipulation reinforcement learning.
- **⚠️ Limitations**: The paper does not evaluate real-world sim2real transfer performance, test integration with modern foundation model or VLA pipelines, or demonstrate generalization to open-vocabulary, unstructured robotic manipulation tasks outside its closed experimental benchmark set.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.02104v1)
- **👥 Authors**: Xuerui Wang, Guangyu Ren, Tianhong Dai, Bintao Hu, Shuangyao Huang, Wenzhang Zhang, Hengyan Liu
- **🏷️ Tags**: #Reinforcement_Learning #Robot_Manipulation #Embodied_AI

---

### ✨ LiftAvatar: Kinematic-Space Completion for Expression-Controlled 3D Gaussian Avatar Animation (Score: 5/10)
- **💡 Innovation**: The key novelty is a paradigm that lifts sparse monocular kinematic observations (facial expressions, head pose) to richer kinematic representations via a fine-grained expression-controllable video diffusion Transformer, to reduce artifacts and improve animation quality of 3D Gaussian Splatting-based avatars.
- **⚠️ Limitations**: The work is limited exclusively to facial and head avatar animation use cases, with no evaluation or demonstration of applicability to robotics, embodied AI, manipulation, or other core research interests you listed.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.02129v1)
- **👥 Authors**: Hualiang Wei, Shunran Jia, Jialun Liu, Wenhui Li
- **🏷️ Tags**: #Diffusion_Model #3D_Gaussian_Splatting #Foundation_Model

---

### 📄 Tool Verification for Test-Time Reinforcement Learning (Score: 4/10)
- **💡 Innovation**: The key novelty is the proposed T^3RL framework that integrates external tool verification into test-time reinforcement learning reward estimation to mitigate mode collapse caused by spurious high-frequency unverified consensus, producing more reliable pseudo-labels for self-evolving large reasoning models.
- **⚠️ Limitations**: The work only validates the proposed approach on math reasoning tasks, with no exploration of its applicability to robotics, embodied AI, or other domains covered by your research interests, and does not analyze its computational overhead during test-time adaptation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.02203v1)
- **👥 Authors**: Ruotong Liao, Nikolai Röhrich, Xiaohan Wang, Yuhui Zhang, Yasaman Samadzadeh, Volker Tresp, Serena Yeung-Levy
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### 📄 Learning from Synthetic Data Improves Multi-hop Reasoning (Score: 4/10)
- **💡 Innovation**: The key novelty is demonstrating that low-cost, scalable rule-generated synthetic fictional reasoning data can be used for RL fine-tuning of LLMs to improve their multi-hop reasoning performance and generalizable knowledge composition skills.
- **⚠️ Limitations**: The work does not explore if the proposed synthetic data RL fine-tuning approach transfers to cross-modal, embodied or robotics-related reasoning tasks, nor does it validate its performance on non-text reasoning benchmarks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.02091v1)
- **👥 Authors**: Anmol Kabra, Yilun Yin, Albert Gong, Kamilė Stankevičiūtė, Dongyoung Go, Johann Lee, Katie Z. Luo, Carla P. Gomes, Kilian Q. Weinberger
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 dLLM: Simple Diffusion Language Modeling (Score: 4/10)
- **💡 Innovation**: The key novelty is dLLM, an open-source unified framework that standardizes core training, inference, and evaluation components of diffusion language models, supports easy customization for new diffusion LM designs, enables conversion of existing BERT-style encoders or autoregressive LLMs to diffusion language models, and releases accessible small DLM checkpoints to lower research barriers.
- **⚠️ Limitations**: This work only provides engineering-level pipeline standardization for diffusion language models, lacks novel theoretical or architectural breakthroughs for diffusion models or LLMs, and has no coverage of embodied AI, robotics, or 3D vision use cases relevant to the user's core research interests.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.22661)
- **👥 Authors**: Zhanhui Zhou, Lingjie Chen, Hanghang Tong, Dawn Song
- **🏷️ Tags**: #Diffusion_Model #LLM #Foundation_Model

---

### 📄 SenCache: Accelerating Diffusion Model Inference via Sensitivity-Aware Caching (Score: 4/10)
- **💡 Innovation**: The key novelty is a principled sensitivity-aware dynamic caching framework for diffusion model inference that adaptively selects per-sample denoising timesteps for caching via formalized sensitivity analysis, removing the need for heuristic cache timestep tuning required by prior caching methods.
- **⚠️ Limitations**: The work only validates the proposed method on video generation diffusion models, and does not explore its applicability to diffusion use cases relevant to the user's core interests such as world modeling, 3D content generation, or robot learning pipelines.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.24208)
- **👥 Authors**: Yasaman Haghighi, Alexandre Alahi
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 Reinforcement-aware Knowledge Distillation for LLM Reasoning (Score: 4/10)
- **💡 Innovation**: The key novelty is the proposed RL-aware Distillation (RLAD) framework with the Trust Region Ratio Distillation (TRRD) component that replaces standard teacher-student KL regularization with a PPO/GRPO-style likelihood-ratio objective anchored to a teacher-old-policy mixture, resolving distribution mismatch and objective interference issues when distilling RL-post-trained LLMs into smaller student models.
- **⚠️ Limitations**: The work only evaluates the proposed method on narrow logic reasoning and math benchmarks, with no exploration of its applicability to other LLM use cases such as embodied AI task planning or robot manipulation, and no detailed ablation of performance sensitivity to the teacher-old-policy mixture weight.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.22495)
- **👥 Authors**: Zhaoyang Zhang, Shuli Jiang, Yantao Shen, Yuting Zhang, Dhananjay Ram, Shuo Yang, Zhuowen Tu, Wei Xia, Stefano Soatto
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Pencil Puzzle Bench: A Benchmark for Multi-Step Verifiable Reasoning (Score: 3/10)
- **💡 Innovation**: The key novelty is a large-scale pencil puzzle benchmark featuring 300 puzzles across 20 varieties with deterministic step-level constraint verification, enabling dense per-move reward signals for LLM process supervision and reinforcement learning.
- **⚠️ Limitations**: The benchmark is restricted to text-based LLM reasoning evaluation for constraint satisfaction problems, with no support for or evaluation of robotics, embodied AI, perception, or world modeling tasks, and does not empirically validate the utility of its proposed reward signals for reinforcement learning use cases outside of LLM reasoning.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.02119v1)
- **👥 Authors**: Justin Waugh
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 Recursive Models for Long-Horizon Reasoning (Score: 3/10)
- **💡 Innovation**: The key novelty is proposing recursive self-invoking models that decompose problems into subtasks with exponentially smaller active context requirements than standard autoregressive models, with theoretical proofs of superiority over single-sequence context management approaches and empirical outperformance of frontier LLMs on long-horizon Boolean satisfiability tasks.
- **⚠️ Limitations**: The work is only validated on abstract combinatorial reasoning tasks, with no exploration of applications to embodied AI, robot manipulation, or other robotics-related domains of interest, and no integration with relevant paradigms like VLAs or world models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.02112v1)
- **👥 Authors**: Chenxiao Yang, Nathan Srebro, Zhiyuan Li
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Enhancing Spatial Understanding in Image Generation via Reward Modeling (Score: 3/10)
- **💡 Innovation**: The key novelty is the construction of the 80k+ SpatialReward-Dataset of spatial relationship preference pairs, the development of the SpatialScore reward model that outperforms leading proprietary models on spatial evaluation for text-to-image generation, and the application of this reward model to enable online reinforcement learning fine-tuning for improved spatial generation performance.
- **⚠️ Limitations**: This work is restricted to 2D text-to-image generation use cases, provides no exploration of applications to 3D vision, embodied AI, or robotic spatial reasoning aligned with your core interests, and does not disclose the underlying architecture of the base text-to-image generation model it optimizes.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.24233)
- **👥 Authors**: Zhenyu Tang, Chaoran Feng, Yufan Deng, Jie Wu, Xiaojie Li, Rui Wang, Yunpeng Chen, Daquan Zhou
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model

---

### 📄 Ref-Adv: Exploring MLLM Visual Reasoning in Referring Expression Tasks (Score: 3/10)
- **💡 Innovation**: The key novelty is the introduction of Ref-Adv, a challenging Referring Expression Comprehension benchmark that suppresses shortcut learning by using linguistically complex expressions, hard distractors, and annotated reasoning facets to require genuine visual reasoning and grounding from multimodal large language models.
- **⚠️ Limitations**: The work is limited to static 2D image referring expression tasks, and does not explore extensions to dynamic 3D environments, embodied perception scenarios, or robotic use cases that are relevant to broader robotics and embodied AI research.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.23898)
- **👥 Authors**: Qihua Dong, Kuo Yang, Lin Ju, Handong Zhao, Yitian Zhang, Yizhou Wang, Huimin Zeng, Jianglin Lu, Yun Fu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Cognitive Models and AI Algorithms Provide Templates for Designing Language Agents (Score: 3/10)
- **💡 Innovation**: The key novelty is proposing to leverage existing cognitive model and traditional AI algorithm literature as reusable blueprints to design modular, interpretable LLM-based language agent templates that define individual LLM roles and functional composition logic.
- **⚠️ Limitations**: As a position paper, it lacks empirical validation of the effectiveness of the proposed agent template approach on real-world complex tasks, and does not explore integration with robotics, embodied AI or other domains relevant to your stated research interests.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.22523)
- **👥 Authors**: Ryan Liu, Dilip Arumugam, Cedegao E. Zhang, Sean Escola, Xaq Pitkow, Thomas L. Griffiths
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 How Small Can 6G Reason? Scaling Tiny Language Models for AI-Native Networks (Score: 2/10)
- **💡 Innovation**: This work conducts the first systematic empirical scaling study of compact language models for 6G network semantic reasoning, introducing the standardization-aligned 6G-Bench benchmark and Edge Score metric to identify that 1.5B to 3B parameter models achieve the optimal balance of reasoning accuracy and edge deployment efficiency.
- **⚠️ Limitations**: The study only carries out offline benchmarking and inference profiling without validating the evaluated models' performance and efficiency in real-world 6G edge network deployment scenarios, and does not explore custom model architectures optimized specifically for 6G semantic reasoning tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.02156v1)
- **👥 Authors**: Mohamed Amine Ferrag, Abderrahmane Lakas, Merouane Debbah
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Near-Optimal Regret for KL-Regularized Multi-Armed Bandits (Score: 2/10)
- **💡 Innovation**: This work develops a novel peeling argument for sharp analysis of KL-UCB, deriving the first high-probability near-optimal regret upper bound for KL-regularized multi-armed bandits paired with a matching non-constant lower bound from custom hard-instance constructions.
- **⚠️ Limitations**: The work is limited to the simplified multi-armed bandit setting, with no extensions to more complex reinforcement learning paradigms or practical applications aligned with the user's stated interests in robotics, embodied AI, and related applied domains.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.02155v1)
- **👥 Authors**: Kaixuan Ji, Qingyue Zhao, Heyang Zhao, Qiwei Di, Quanquan Gu
- **🏷️ Tags**: #Reinforcement_Learning #Multi_Armed_Bandits #Regret_Analysis #KL_Regularization

---

### 📄 LLMs as Strategic Actors: Behavioral Alignment, Risk Calibration, and Argumentation Framing in Geopolitical Simulations (Score: 2/10)
- **💡 Innovation**: The key novelty is the systematic comparative evaluation of six state-of-the-art LLMs against human decision-making performance across four real-world geopolitical crisis scenarios, assessing metrics of action alignment, risk calibration, and argumentation framing grounded in international relations theory.
- **⚠️ Limitations**: The study is restricted to predefined action selection in closed geopolitical simulation environments, does not explore generalizability to other decision domains including robotic or embodied AI use cases, and lacks validation of the real-world decision impact of the modeled LLM behaviors.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.02128v1)
- **👥 Authors**: Veronika Solopova, Viktoria Skorik, Maksym Tereshchenko, Alina Haidun, Ostap Vykhopen
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 OmniRet: Efficient and High-Fidelity Omni Modality Retrieval (Score: 2/10)
- **💡 Innovation**: The key novelty is the development of OmniRet, the first retrieval model capable of handling composed queries across text, vision, and audio modalities, which introduces an attention-based resampling mechanism for computational efficiency and Attention Sliced Wasserstein Pooling to preserve fine-grained representation details, alongside a new Audio-Centric Multimodal Benchmark for more comprehensive omni-modal embedding evaluation.
- **⚠️ Limitations**: The work only supports three modalities (text, vision, audio) without extending to other relevant modalities such as 3D data or robotic action signals, and fails to demonstrate any applicability to the user's core interest areas including embodied AI, robot manipulation, or 3D perception, while also not validating performance on extremely large-scale retrieval deployments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.02098v1)
- **👥 Authors**: Chuong Huynh, Manh Luong, Abhinav Shrivastava
- **🏷️ Tags**: #LLM #Foundation_Model #Multimodal_Retrieval #Attention_Mechanism #Audio_Visual_Retrieval

---

### 📄 Adam Converges Without Any Modification On Update Rules (Score: 2/10)
- **💡 Innovation**: This work identifies a novel phase transition of Adam's convergence/divergence behavior on the 2D (β₁, β₂) hyperparameter plane, proves Adam converges without modifying its update rules when using proper problem-dependent hyperparameters, and provides actionable hyperparameter tuning guidance for LLM training.
- **⚠️ Limitations**: The work lacks extensive original empirical validation of its proposed hyperparameter tuning strategy across diverse model architectures and task types, only relying on existing reported results for empirical support.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.02092v1)
- **👥 Authors**: Yushun Zhang, Bingran Li, Congliang Chen, Zhi-Quan Luo, Ruoyu Sun
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation (Score: 2/10)
- **💡 Innovation**: The key novelty is the development of CUDA Agent, a large-scale agentic reinforcement learning system that combines a scalable data synthesis pipeline, a skill-augmented CUDA development environment with automated verification and profiling for reliable reward signals, and stable RL training techniques to achieve state-of-the-art CUDA kernel generation performance that outperforms both leading compiler systems and top proprietary LLMs on the KernelBench benchmark.
- **⚠️ Limitations**: The work only evaluates performance on the fixed KernelBench benchmark without testing generalization to custom real-world CUDA kernel use cases, and does not explore any applications of the proposed system to robotics, embodied AI or other domains aligned with your stated research interests.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.24286)
- **👥 Authors**: Weinan Dai, Hanlin Wu, Qiying Yu, Huan-ang Gao, Jiahao Li, Chengquan Jiang, Weiqiang Lou, Yufan Song, Hongli Yu, Jiaze Chen, Wei-Ying Ma, Ya-Qin Zhang, Jingjing Liu, Mingxuan Wang, Xin Liu, Hao Zhou
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 Recovered in Translation: Efficient Pipeline for Automated Translation of Benchmarks and Datasets (Score: 2/10)
- **💡 Innovation**: The key novelty is a fully automated scalable benchmark translation framework that combines Universal Self-Improvement test-time compute scaling and the proposed T-RANK multi-round ranking method to reduce semantic drift and preserve original task structure and linguistic nuances during translation.
- **⚠️ Limitations**: The work only evaluates its framework on 8 Eastern and Southern European languages, lacks validation of consistent task difficulty parity across translated benchmarks for different LLM families, and does not address translation of robotics or embodied AI related datasets relevant to the user's interests.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.22207)
- **👥 Authors**: Hanna Yukhymenko, Anton Alexandrov, Martin Vechev
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 LK Losses: Direct Acceptance Rate Optimization for Speculative Decoding (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposal of LK losses that directly optimize the acceptance rate of lightweight draft models for LLM speculative decoding, replacing the standard proxy KL divergence objective to achieve higher inference speedup.
- **⚠️ Limitations**: The work only evaluates on text-domain LLM inference tasks, does not explore applicability to other foundation model types relevant to robotics and embodied AI, and does not fully analyze potential tradeoffs between acceptance rate improvements and downstream task output quality.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.23881)
- **👥 Authors**: Alexander Samarin, Sergei Krutikov, Anton Shevtsov, Sergei Skvortsov, Filipp Fisin, Alexander Golubev
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 CiteAudit: You Cited It, But Did You Read It? A Benchmark for Verifying Scientific References in the LLM Era (Score: 2/10)
- **💡 Innovation**: This work presents the first comprehensive benchmark and multi-agent verification pipeline for detecting hallucinated scientific citations in LLM-generated writing, along with a large-scale human-validated cross-domain dataset and unified metrics for evaluating citation faithfulness and evidence alignment.
- **⚠️ Limitations**: The framework is not evaluated for generalizability to non-English scientific publications or highly specialized technical domains with unique citation conventions, and does not support verification of non-textual cited claims such as experimental result figures or mathematical proofs.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.23452)
- **👥 Authors**: Zhengqing Yuan, Kaiwen Shi, Zheyuan Zhang, Lichao Sun, Nitesh V. Chawla, Yanfang Ye
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 LongVideo-R1: Smart Navigation for Low-cost Long Video Understanding (Score: 2/10)
- **💡 Innovation**: The key novelty is LongVideo-R1, an active reasoning-enabled multimodal large language model agent that iteratively navigates hierarchical video summaries to avoid redundant processing of full long videos, trained via a two-stage supervised fine-tuning and reinforcement learning pipeline on custom curated chain-of-thought trajectories.
- **⚠️ Limitations**: The work is limited to long video question answering tasks with no exploration of applicability to robotics or 3D perception use cases aligned with your research interests, and its training data curation relies on the non-public GPT-5 model reducing reproducibility.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.20913)
- **👥 Authors**: Jihao Qiu, Lingxi Xie, Xinyue Huo, Qi Tian, Qixiang Ye
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Shared Nature, Unique Nurture: PRISM for Pluralistic Reasoning via In-context Structure Modeling (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposal of the PRISM model-agnostic system that augments LLMs with dynamic on-the-fly epistemic graphs under the Epistemic Evolution paradigm to improve distributional diversity and pluralistic reasoning performance on creativity and long-tail rare disease diagnosis tasks.
- **⚠️ Limitations**: The work does not explore applications of the proposed pluralistic reasoning framework to robotics, embodied AI or other domains outside natural language reasoning and medical diagnosis, nor does it validate compatibility with other foundation model variants like vision-language-action models or world models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.21317)
- **👥 Authors**: Guancheng Tu, Shiyang Zhang, Tianyu Zhang, Yi Zhang, Diji Yang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 How to Take a Memorable Picture? Empowering Users with Actionable Feedback (Score: 2/10)
- **💡 Innovation**: This work introduces the novel Memorability Feedback (MemFeed) task for generating actionable natural language guidance to improve image memorability, proposes the training-free MemCoach approach leveraging MLLM teacher-student activation steering, and releases the MemBench benchmark for standardized evaluation of this new task.
- **⚠️ Limitations**: The work does not validate the real-world effectiveness of its generated suggestions for actual user photography outcomes, and does not explore integration with autonomous robotic or embodied systems that could act on the memorability feedback.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.21877)
- **👥 Authors**: Francesco Laiti, Davide Talon, Jacopo Staiano, Elisa Ricci
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 CL4SE: A Context Learning Benchmark For Software Engineering Tasks (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposal of CL4SE, the first standardized evaluation framework for software engineering context learning, with a fine-grained taxonomy of four SE-specific context types mapped to core SE tasks and a large high-quality dataset of over 13,000 samples.
- **⚠️ Limitations**: The work is limited exclusively to software engineering use cases, does not explore the generalizability of its context learning taxonomy to other LLM application domains like robotics or embodied AI, and only evaluates a small set of 5 mainstream LLMs.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.23047)
- **👥 Authors**: Haichuan Hu, Ye Shang, Guoqing Xie, Congqing He, Quanjun Zhang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators (Score: 2/10)
- **💡 Innovation**: The key novelty is the design of STATIC, which flattens prefix trees (Tries) into a static Compressed Sparse Row matrix to convert irregular tree traversal steps into fully vectorized sparse matrix operations, delivering massive speedups for constrained LLM decoding on TPUs/GPUs for generative retrieval.
- **⚠️ Limitations**: The work is only validated on recommendation system generative retrieval use cases, with no exploration of its performance or applicability to other LLM use cases such as embodied AI planning or open-domain conversational AI, and no evaluation on smaller open-source LLM architectures.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.22647)
- **👥 Authors**: Zhengyang Su, Isay Katsman, Yueqi Wang, Ruining He, Lukasz Heldt, Raghunandan Keshavan, Shao-Chuan Wang, Xinyang Yi, Mingyan Gao, Onkar Dalal, Lichan Hong, Ed Chi, Ningren Han
- **🏷️ Tags**: #LLM #Foundation_Model

---


