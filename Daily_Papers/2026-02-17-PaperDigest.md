# 📅 2026-02-17 - Paper Digest
## Summary
Total Papers: 42 | High Impact: 2

## 📝 Papers List
### ✨ VisPhyWorld: Probing Physical Reasoning via Code-Driven Video Reconstruction (Score: 7/10)
- **💡 Innovation**: The key novelty is the introduction of VisPhyWorld, an execution-based evaluation framework that assesses multimodal large language models' physical reasoning capabilities by requiring them to generate executable simulator code from visual observations, paired with the VisPhyBench benchmark of 209 physical scenes for standardized performance testing.
- **⚠️ Limitations**: The work is limited to evaluating physical reasoning for simulated scene reconstruction only, and does not extend to real-world embodied tasks, robot manipulation, or integrate with other popular world modeling techniques such as 3D Gaussian Splatting or diffusion models.
- **🔗 Link**: [[VisPhyWorld]]
- **👥 Authors**: Jiarong Liang, Max Ku, Ka-Hei Hui, Ping Nie, Wenhu Chen
- **🏷️ Tags**: #World_Model #Foundation_Model #LLM #Embodied_AI

---

### ✨ MoRL: Reinforced Reasoning for Unified Motion Understanding and Generation (Score: 7/10)
- **💡 Innovation**: The key novelty is the proposed MoRL unified multimodal motion model trained with supervised fine-tuning and verifiable reinforcement learning rewards combining semantic alignment, reasoning coherence, physical plausibility and text-motion consistency signals, paired with the Chain-of-Motion test-time stepwise reasoning method and two new large-scale chain-of-thought motion datasets.
- **⚠️ Limitations**: The paper does not evaluate the proposed motion model on real robotic manipulation tasks, nor demonstrate integration with world models, 3D/4D Gaussian splatting, or sim2real transfer pipelines for practical embodied AI deployment.
- **🔗 Link**: [[MoRL]]
- **👥 Authors**: Hongpeng Wang, Zeyu Zhang, Wenhao Li, Hao Tang
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #Embodied_AI #LLM

---

### ✨ Experiential Reinforcement Learning (Score: 6/10)
- **💡 Innovation**: The key novelty is the proposed Experiential Reinforcement Learning (ERL) paradigm that embeds an explicit experience-reflection-consolidation loop into the reinforcement learning process for language models, converting sparse delayed environmental feedback into structured behavioral revisions to improve exploration, stabilize optimization and avoid extra inference cost at deployment.
- **⚠️ Limitations**: The work only evaluates ERL on general sparse-reward control environments and agentic reasoning benchmarks for language models, with no validation on embodied AI, robot manipulation or other robotics and 3D perception related tasks, and no exploration of integration with other listed technologies such as world models, VLAs or Gaussian Splatting.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.13949)
- **👥 Authors**: Taiwei Shi, Sihao Chen, Bowen Jiang, Linxin Song, Longqi Yang, Jieyu Zhao
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ WebWorld: A Large-Scale World Model for Web Agent Training (Score: 6/10)
- **💡 Innovation**: The key novelty is the development of WebWorld, the first large-scale open-web world model trained on over 1 million open-web interactions, paired with the dedicated WebWorld-Bench evaluation suite, that delivers strong web agent performance and cross-domain generalization to code, GUI, and game digital environments.
- **⚠️ Limitations**: This work is restricted to digital domain use cases, provides no exploration of applicability to physical embodied AI or robotics scenarios, and does not evaluate integration with other common focus areas including diffusion models, 3D Gaussian Splatting, reinforcement learning, or vision-language-action models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.14721)
- **👥 Authors**: Zikai Xiao, Jianhong Tu, Chuhang Zou, Yuxin Zuo, Zhi Li, Peng Wang, Bowen Yu, Fei Huang, Junyang Lin, Zuozhu Liu
- **🏷️ Tags**: #World_Model #Foundation_Model #LLM

---

### ✨ Embed-RL: Reinforcement Learning for Reasoning-Driven Multimodal Embeddings (Score: 5/10)
- **💡 Innovation**: The key novelty is the proposed Embedder-Guided Reinforcement Learning (EG-RL) framework that optimizes the reasoning module to produce retrieval-aligned Traceability CoT (T-CoT) with explicit embedder supervision, to boost cross-modal multimodal embedding performance.
- **⚠️ Limitations**: The work is only evaluated on general cross-modal retrieval benchmarks, lacks validation on downstream robotics/embodied AI tasks relevant to your interests, and does not explore integration with perception or action-focused modeling techniques listed in your keywords.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.13823)
- **👥 Authors**: Haonan Jiang, Yuji Wang, Yongjie Zhu, Xin Lu, Wenyu Qin, Meng Wang, Pengfei Wan, Yansong Tang
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### ✨ LaViDa-R1: Advancing Reasoning for Unified Multimodal Diffusion Language Models (Score: 5/10)
- **💡 Innovation**: The key novelty is a unified post-training framework that seamlessly integrates supervised finetuning and multi-task reinforcement learning, paired with novel training techniques including answer-forcing, tree search, and complementary likelihood estimation, to build a high-performance general-purpose reasoning multimodal diffusion language model.
- **⚠️ Limitations**: The work only evaluates on general multimodal tasks such as visual math reasoning and image editing, and does not explore applications to robotics, embodied AI or other domain-specific tasks aligned with your stated research interests, nor does it provide benchmarks on relevant robotics or 3D vision datasets.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.14147)
- **👥 Authors**: Shufan Li, Yuchen Zhu, Jiuxiang Gu, Kangning Liu, Zhe Lin, Yongxin Chen, Molei Tao, Aditya Grover, Jason Kuen
- **🏷️ Tags**: #Diffusion_Model #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Found-RL: foundation model-enhanced reinforcement learning for autonomous driving (Score: 5/10)
- **💡 Innovation**: The key novelty is an asynchronous batch inference framework that decouples heavy vision-language model reasoning from the reinforcement learning simulation loop to resolve latency bottlenecks, paired with novel supervision and reward shaping mechanisms to distill foundation model knowledge into lightweight real-time RL policies for autonomous driving.
- **⚠️ Limitations**: This work is restricted to autonomous driving use cases, does not evaluate on robot manipulation or general embodied AI tasks, does not address sim2real transfer or real-world deployment, and does not leverage other relevant technologies in your interest list such as 3D Gaussian Splatting or world models for improved scene understanding.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10458)
- **👥 Authors**: Yansong Qu, Zihao Sheng, Zilin Huang, Jiancong Chen, Yuhao Luo, Tianyi Wang, Yiheng Feng, Samuel Labi, Sikai Chen
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #Embodied_AI

---

### 📄 REDSearcher: A Scalable and Cost-Efficient Framework for Long-Horizon Search Agents (Score: 4/10)
- **💡 Innovation**: The key novelty is the co-designed REDSearcher unified framework that integrates dual-constrained complex task synthesis, tool-augmented querying, atomic capability mid-training, and low-cost local simulated reinforcement learning iteration to address the bottleneck of sparse high-quality search trajectories and reward signals for long-horizon search agent optimization.
- **⚠️ Limitations**: This work is restricted to digital text and multimodal search scenarios, with no exploration of physical world embodied or robotic search use cases, and does not integrate relevant robotics/3D perception technologies from your listed interests such as world models, 3D Gaussian Splatting, or vision-language-action models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.14234)
- **👥 Authors**: Zheng Chu, Xiao Wang, Jack Hong, Huiming Fan, Yuqi Huang, Yue Yang, Guohai Xu, Chenxiao Zhao, Cheng Xiang, Shengchao Hu, Dongdong Kuang, Ming Liu, Bing Qin, Xing Yu
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 UniWeTok: An Unified Binary Tokenizer with Codebook Size 2^{128} for Unified Multimodal Large Language Model (Score: 4/10)
- **💡 Innovation**: The key novelty is the proposal of UniWeTok, a unified discrete visual tokenizer with an unprecedented 2^128 size binary codebook, paired with novel Pre-Post Distillation, Generative-Aware Prior, SigLu activation function, and three-stage training pipeline that achieves state-of-the-art image generation and multimodal task performance with drastically lower training compute than prior leading tokenizers.
- **⚠️ Limitations**: The work only evaluates the tokenizer on general 2D image and multimodal understanding/generation tasks, with no exploration of its applicability to embodied AI, robotics manipulation, 3D/4D perception, or other use cases aligned with the stated research interests, and also does not ablate the practical utility of the extremely large 2^128 codebook versus smaller codebook alternatives.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.14178)
- **👥 Authors**: Shaobin Zhuang, Yuang Ai, Jiaming Han, Weijia Mao, Xiaohui Li, Fangyikang Wang, Xiao Wang, Yan Li, Shanchuan Lin, Kun Xu, Zhenheng Yang, Huaibo Huang, Xiangyu Yue, Hao Chen, Yali Wang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Verifier-Constrained Flow Expansion for Discovery Beyond the Data (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposed Flow Expander framework, a scalable verifier-constrained mirror descent scheme that adapts pre-trained flow/diffusion models to expand generation coverage beyond the training data distribution while preserving sample validity, paired with formal theoretical convergence guarantees.
- **⚠️ Limitations**: The work is only evaluated on synthetic low-dimensional settings and molecular design tasks, with no exploration of applicability to robotics, embodied AI, or other core domains of interest to the user, and lacks comparison to existing diffusion model expansion methods for non-molecular use cases.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.15984v1)
- **👥 Authors**: Riccardo De Santi, Kimon Protopapas, Ya-Ping Hsieh, Andreas Krause
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 BitDance: Scaling Autoregressive Generative Models with Binary Tokens (Score: 3/10)
- **💡 Innovation**: The key novelty is a scalable autoregressive image generator that uses high-entropy binary visual tokens instead of standard codebook indices, paired with a binary diffusion head for sampling from the large token space and next-patch diffusion for fast, accurate parallel inference.
- **⚠️ Limitations**: The work is only evaluated on 2D image and text-to-image generation tasks, with no exploration of applications to robotics, embodied AI, 3D content generation or other use cases aligned with your stated research interests, and does not integrate capabilities like LLMs or vision-language-action models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.14041)
- **👥 Authors**: Yuang Ai, Jiaming Han, Shaobin Zhuang, Weijia Mao, Xuefeng Hu, Ziyan Yang, Zhenheng Yang, Huaibo Huang, Xiangyu Yue, Hao Chen
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 Nanbeige4.1-3B: A Small General Model that Reasons, Aligns, and Acts (Score: 3/10)
- **💡 Innovation**: The key novelty is an open-source 3B-parameter small language model that combines point-wise and pair-wise reward modeling for alignment, complexity-aware reinforcement learning rewards for code generation, and turn-level supervision for long-horizon tool interactions, outperforming both similar-scale and much larger competing models across reasoning, code, and agentic tasks.
- **⚠️ Limitations**: The paper does not explore applications of the proposed model to embodied AI, robotics or related domains, and lacks detailed ablation studies to quantify the individual contribution of each proposed training component to performance gains.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.13367)
- **👥 Authors**: Chen Yang, Guangyue Peng, Jiaying Zhu, Ran Le, Ruixiang Feng, Tao Zhang, Xiyun Xu, Yang Song, Yiming Jia, Yuntao Wen, Yunzhi Xu, Zekai Wang, Zhenwei An, Zhicong Sun, Zongchao Chen
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 Data Darwinism Part I: Unlocking the Value of Scientific Data for Pre-training (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposal of the 10-level Data Darwinism taxonomy for conceptualizing data-model co-evolution, alongside the curated 900B-token Darwin-Science corpus and contamination-free daVinci-origin baseline models that validate the performance gains of higher-level data processing for scientific domain foundation model pre-training.
- **⚠️ Limitations**: This work is only validated on scientific text understanding tasks, with no exploration of applications to robotics, computer vision, or embodied AI domains, and does not test if the proposed data processing framework improves performance of non-LLM foundation models such as vision-language-action models or world models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.07824)
- **👥 Authors**: Yiwei Qin, Zhen Huang, Tiantian Mi, Weiye Si, Chenyang Zhou, Qipeng Guo, Siyuan Feng, Pengfei Liu
- **🏷️ Tags**: #Foundation_Model #LLM

---

### 📄 Learning to Configure Agentic AI Systems (Score: 3/10)
- **💡 Innovation**: The key novelty is formulating LLM-based agent configuration as a per-query decision problem and introducing ARC, a lightweight hierarchical reinforcement learning policy that dynamically adjusts agent configurations to improve task accuracy while reducing token and runtime costs.
- **⚠️ Limitations**: The work is only evaluated on reasoning and tool-augmented question answering benchmarks, with no exploration of applicability to embodied AI, robotics or other core domains in your stated research interests, and no validation on complex real-world multi-step agent deployment scenarios.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.11574)
- **👥 Authors**: Aditya Taparia, Som Sagar, Ransalu Senanayake
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 FireRed-Image-Edit-1.0 Techinical Report (Score: 3/10)
- **💡 Innovation**: The key novelty is the development of a state-of-the-art diffusion transformer for instruction-based image editing, supported by a large curated 100M-sample training corpus, custom multi-stage training and optimization strategies for improved alignment and controllability, and the new comprehensive REDEdit-Bench evaluation benchmark.
- **⚠️ Limitations**: This work is restricted to 2D image editing tasks, with no exploration of applications to robotics, embodied AI, 3D content generation, or other use cases aligned with your core research interests, and does not integrate large language models for enhanced instruction understanding.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.13344)
- **👥 Authors**: Super Intelligence Team, Changhao Qiao, Chao Hui, Chen Li, Cunzheng Wang, Dejia Song, Jiale Zhang, Jing Li, Qiang Xiang, Runqi Wang, Shuang Sun, Wei Zhu, Xu Tang, Yao Hu, Yibo Chen, Yuhao Huang, Yuxuan Duan, Zhiyi Chen, Ziyuan Guo
- **🏷️ Tags**: #Diffusion_Model #Reinforcement_Learning #Foundation_Model

---

### 📄 Updating Parametric Knowledge with Context Distillation Retains Post-Training Capabilities (Score: 2/10)
- **💡 Innovation**: The key novelty is the Distillation via Split Contexts (DiSC) method, a simple context-distillation based continual knowledge adaptation approach that balances learning new knowledge and preserving prior post-trained LLM capabilities without requiring explicit generation steps during training.
- **⚠️ Limitations**: The work only evaluates on text-only LLM adaptation tasks, with no exploration of applicability to multi-modal foundation models, embodied AI or robotics use cases, and does not test performance scaling with very large model sizes or massive adaptation corpora.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16093v1)
- **👥 Authors**: Shankar Padmanabhan, Mustafa Omer Gul, Tanya Goyal
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Quantifying LLM Attention-Head Stability: Implications for Circuit Universality (Score: 2/10)
- **💡 Innovation**: This work delivers the first systematic empirical quantification of attention head stability across independently initialized training runs of LLMs of varying sizes, identifying novel patterns of stability across layers, model depth, and optimization strategies, plus the higher functional importance of unstable deeper-layer heads.
- **⚠️ Limitations**: The study is limited to decoder-only transformer LLMs, and does not extend its stability analysis to multi-modal foundation models or validate the practical implications of its findings for downstream safety, alignment, or robotics-related applications.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16740v1)
- **👥 Authors**: Karan Bali, Jack Stanley, Praneet Suresh, Danilo Bzdok
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 The Limits of Long-Context Reasoning in Automated Bug Fixing (Score: 2/10)
- **💡 Innovation**: This work systematically evaluates long-context reasoning capabilities of state-of-the-art LLMs for automated bug fixing, revealing that agentic coding performance stems from task decomposition into short-context steps rather than effective long-context reasoning, and quantifying sharp performance degradation in single-shot long-context patch generation even with perfect retrieval of relevant code files.
- **⚠️ Limitations**: The study is limited to the automated bug fixing domain, does not investigate if the observed long-context reasoning gaps generalize to other LLM application areas such as embodied AI or robot task planning, and does not present solutions to address the identified failure modes of long-context LLMs for code tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16069v1)
- **👥 Authors**: Ravi Raju, Mengmeng Ji, Shubhangi Upasani, Bo Li, Urmish Thakker
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Self-Evolving Multi-Agent Network for Industrial IoT Predictive Maintenance (Score: 2/10)
- **💡 Innovation**: The key novelty is SEMAS, a hierarchical multi-agent system distributed across edge, fog, and cloud tiers that integrates PPO-driven policy evolution, LLM-based explainability, and federated knowledge aggregation to deliver low-latency, interpretable, adaptive anomaly detection for industrial IoT predictive maintenance.
- **⚠️ Limitations**: The work does not benchmark against state-of-the-art edge multi-agent or LLM-based anomaly detection baselines, does not validate generalizability to non-industrial IoT use cases, and lacks analysis of system robustness under extreme operational drift or edge node failure scenarios.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16738v1)
- **👥 Authors**: Rebin Saleh, Khanh Pham Dinh, Balázs Villányi, Truong-Son Hy
- **🏷️ Tags**: #Reinforcement_Learning #LLM

---

### 📄 Can Generative Artificial Intelligence Survive Data Contamination? Theoretical Guarantees under Contaminated Recursive Training (Score: 2/10)
- **💡 Innovation**: This work presents the first positive theoretical convergence guarantee for contaminated recursive training of general universal approximator generative models without restrictive distributional assumptions on real data, with extensions to sampling bias settings and supporting empirical results.
- **⚠️ Limitations**: The work does not validate its theoretical findings on large-scale real-world foundation models or LLMs, nor does it examine implications of data contamination for downstream use cases relevant to your core research interests such as robotics or embodied AI.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16065v1)
- **👥 Authors**: Kevin Wang, Hongqian Niu, Didong Li
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 MARLEM: A Multi-Agent Reinforcement Learning Simulation Framework for Implicit Cooperation in Decentralized Local Energy Markets (Score: 2/10)
- **💡 Innovation**: The key novelty is an open-source Gymnasium-compatible multi-agent reinforcement learning simulation framework for decentralized local energy markets that enhances agent observations and rewards with system-level key performance indicators to foster implicit inter-agent cooperation without explicit communication.
- **⚠️ Limitations**: The work only validates the proposed framework in limited simulated case studies, lacks benchmarking against state-of-the-art multi-agent coordination approaches for decentralized energy systems, and provides no evidence of real-world deployability of the learned cooperation strategies.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16063v1)
- **👥 Authors**: Nelson Salazar-Pena, Alejandra Tabares, Andres Gonzalez-Mancera
- **🏷️ Tags**: #Reinforcement_Learning #Multi_Agent_Reinforcement_Learning #Decentralized_Local_Energy_Markets #Gymnasium_Environment

---

### 📄 Harnessing Implicit Cooperation: A Multi-Agent Reinforcement Learning Approach Towards Decentralized Local Energy Markets (Score: 2/10)
- **💡 Innovation**: The key novelty is an implicit cooperation framework that uses stigmergic system-level performance signals instead of explicit peer-to-peer communication to enable decentralized multi-agent coordination in local energy markets, alongside empirical identification of APPO-DTDE as the optimal training-algorithm configuration for this use case.
- **⚠️ Limitations**: This work lacks validation on real-world energy grid deployments, does not test scalability to topologies larger than the IEEE 34-node test case, and does not compare against non-MARL state-of-the-art decentralized energy market coordination approaches.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16062v1)
- **👥 Authors**: Nelson Salazar-Pena, Alejandra Tabares, Andres Gonzalez-Mancera
- **🏷️ Tags**: #Reinforcement_Learning #Multi_Agent_Reinforcement_Learning #Decentralized_POMDP #Local_Energy_Markets #Stigmergic_Signaling

---

### 📄 Partial Identification under Missing Data Using Weak Shadow Variables from Pretrained Models (Score: 2/10)
- **💡 Innovation**: The key novelty is a partial identification framework for missing not at random data that leverages predictions from pretrained models as weak shadow variables to tighten identification bounds without requiring the strict completeness conditions of classical shadow variable methods, paired with a finite-sample set-expansion estimator with valid coverage guarantees.
- **⚠️ Limitations**: The work only evaluates the framework on simulations and semi-synthetic customer service dialogue data, does not test generalizability to other domains, and lacks extensive validation of the weak shadow variable conditional independence assumption across diverse pretrained model types.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16061v1)
- **👥 Authors**: Hongyu Chen, David Simchi-Levi, Ruoxuan Xiong
- **🏷️ Tags**: #LLM #Foundation_Model #Partial_Identification #Missing_Data_Analysis #Weak_Shadow_Variables

---

### 📄 CLAA: Cross-Layer Attention Aggregation for Accelerating LLM Prefill (Score: 2/10)
- **💡 Innovation**: The key novelty is the introduction of an Answer-Informed Oracle to define ground-truth token importance for LLM prefill stages, paired with the Cross-Layer Attention Aggregation (CLAA) method that aggregates token importance scores across layers to close the gap to the oracle upper bound and reduce Time-to-First-Token by up to 39% over full KV cache baselines.
- **⚠️ Limitations**: The work only evaluates CLAA on a limited set of small-to-medium LLM architectures and context window lengths, and does not explore its applicability to LLM use cases in robotics, embodied AI or other domains aligned with your core research interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16054v1)
- **👥 Authors**: Bradley McDanel, Steven Li, Harshit Khaitan
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Multi-Objective Alignment of Language Models for Personalized Psychotherapy (Score: 2/10)
- **💡 Innovation**: The key novelty is the development of a multi-objective direct preference optimization (MODPO) framework for LLM alignment tailored to psychotherapy use cases, trained on real patient preference data across six therapeutic criteria to achieve a better balance of empathy, clinical safety and other therapeutic priorities than existing single-objective alignment approaches.
- **⚠️ Limitations**: The work does not evaluate the long-term real-world therapeutic efficacy of the aligned model, nor does it validate performance across diverse patient demographics, mental health condition types or severity levels.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16053v1)
- **👥 Authors**: Mehrab Beikzadeh, Yasaman Asadollah Salmanpour, Ashima Suvarna, Sriram Sankararaman, Matteo Malgaroli, Majid Sarrafzadeh, Saadia Gabriel
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 MoE-Spec: Expert Budgeting for Efficient Speculative Decoding (Score: 2/10)
- **💡 Innovation**: The key novelty is MoE-Spec, a training-free verification-time expert budgeting method that enforces fixed per-layer expert capacity limits to reduce memory pressure and improve throughput of speculative decoding for MoE LLMs while maintaining comparable output quality.
- **⚠️ Limitations**: The work is only evaluated on standard text-only LLM benchmarks, with no exploration of its applicability to other foundation model architectures or downstream use cases relevant to robotics and embodied AI.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16052v1)
- **👥 Authors**: Bradley McDanel, Steven Li, Sruthikesh Surineni, Harshit Khaitan
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Evidence-Grounded Subspecialty Reasoning: Evaluating a Curated Clinical Intelligence Layer on the 2025 Endocrinology Board-Style Examination (Score: 2/10)
- **💡 Innovation**: The key novelty is the January Mirror evidence-grounded clinical reasoning system, which integrates a curated endocrinology and cardiometabolic evidence corpus with a structured reasoning architecture to outperform frontier web-enabled LLMs and a human reference cohort on 2025 endocrinology board-style examinations while providing fully traceable, 100% manually verified accurate citations under closed-evidence constraints.
- **⚠️ Limitations**: The paper only evaluates performance on a static endocrinology board-style question set, and does not test real-world clinical deployment efficacy, generalizability to other medical subspecialties, or performance relative to board-certified endocrinology subspecialists rather than the reported general human reference cohort.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16050v1)
- **👥 Authors**: Amir Hosseinian, MohammadReza Zare Shahneh, Umer Mansoor, Gilbert Szeto, Kirill Karlin, Nima Aghaeepour
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 How Uncertain Is the Grade? A Benchmark of Uncertainty Metrics for LLM-Based Automatic Assessment (Score: 2/10)
- **💡 Innovation**: The key novelty is the first systematic benchmark of a broad range of uncertainty quantification methods for LLM-based automatic educational assessment, with comprehensive characterization of uncertainty patterns across different datasets, LLM families, and generation control settings.
- **⚠️ Limitations**: This work is restricted to the educational automatic assessment use case, does not explore the applicability of its findings to other LLM downstream tasks, and offers no insights relevant to robotics or embodied AI research areas aligned with your interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16039v1)
- **👥 Authors**: Hang Li, Kaiqi Yang, Xianxuan Long, Fedor Filippov, Yucheng Chu, Yasemin Copur-Gencturk, Peng He, Cory Miller, Namsoo Shin, Joseph Krajcik, Hui Liu, Jiliang Tang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Heuristic Search as Language-Guided Program Optimization (Score: 2/10)
- **💡 Innovation**: The key novelty is a modular three-stage framework for LLM-driven automated heuristic design that explicitly decomposes the discovery process into forward evaluation, backward analytical feedback, and program refinement steps, enabling modular component upgrades and outperforming existing baselines across four combinatorial optimization domains.
- **⚠️ Limitations**: The work is only validated on combinatorial optimization tasks, with no exploration of applicability to robotics or embodied AI domains, and does not investigate integration with other relevant foundation model types like vision-language-action models or diffusion models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16038v1)
- **👥 Authors**: Mingxin Yu, Ruixiao Yang, Chuchu Fan
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 MedProbCLIP: Probabilistic Adaptation of Vision-Language Foundation Model for Reliable Radiograph-Report Retrieval (Score: 2/10)
- **💡 Innovation**: The key novelty is MedProbCLIP, a probabilistic vision-language learning framework that leverages Gaussian embeddings, a probabilistic contrastive objective, and a variational information bottleneck to achieve calibrated, reliable bidirectional chest X-ray and radiology report retrieval.
- **⚠️ Limitations**: The work is only evaluated on the MIMIC-CXR chest X-ray dataset, with no validation of generalizability to other medical imaging modalities, real clinical deployment settings, or non-medical domains.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16019v1)
- **👥 Authors**: Ahmad Elallaf, Yu Zhang, Yuktha Priya Masupalli, Jeong Yang, Young Lee, Zechun Cao, Gongbo Liang
- **🏷️ Tags**: #Foundation_Model

---

### 📄 ReLoop: Structured Modeling and Behavioral Verification for Reliable LLM-Based Optimization (Score: 2/10)
- **💡 Innovation**: The key novelty is ReLoop, a framework combining structured four-stage LLM code generation reasoning chains and ground-truth-free behavioral verification via solver-based parameter perturbation to reduce silent semantic failures in LLM-generated optimization code, alongside the new RetailOpt-190 benchmark for compositional retail optimization tasks.
- **⚠️ Limitations**: The work is restricted to optimization code generation use cases, does not demonstrate applicability to robotics or embodied AI domains, and only validates performance on retail-focused optimization problems rather than broader cross-domain optimization benchmarks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.15983v1)
- **👥 Authors**: Junbo Jacob Lian, Yujun Sun, Huiling Chen, Chaoyu Zhang, Chung-Piaw Teo
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 Query as Anchor: Scenario-Adaptive User Representation via Large Language Model (Score: 2/10)
- **💡 Innovation**: The key novelty is the Query-as-Anchor framework that shifts user representation learning from static task-agnostic encoding to dynamic query-aware synthesis, supported by the industrial multi-modal UserU pre-training dataset, a dual-tower LLM Q-Anchor Embedding architecture with joint contrastive-autoregressive optimization, and cluster-based soft prompt tuning for scenario-specific alignment.
- **⚠️ Limitations**: This work is limited exclusively to industrial user representation use cases with no exploration of applicability to robotics or embodied AI domains aligned with your research interests, and lacks detailed ablation studies on the impact of LLM backbone scale and pre-training dataset size on end performance.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.14492)
- **👥 Authors**: Jiahao Yuan, Yike Xu, Jinyong Wen, Baokun Wang, Ziyi Gao, Xiaotong Lin, Yun Liu, Xing Fu, Yu Cheng, Yongchao Liu, Weiqiang Wang, Zhongle Xie
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 InnoEval: On Research Idea Evaluation as a Knowledge-Grounded, Multi-Perspective Reasoning Problem (Score: 2/10)
- **💡 Innovation**: The key novelty is framing scientific research idea evaluation as a knowledge-grounded multi-perspective reasoning problem, and proposing the InnoEval framework that combines heterogeneous deep knowledge search and a multi-background expert reviewer board to produce evaluation outputs highly aligned with human expert consensus.
- **⚠️ Limitations**: The paper only evaluates InnoEval on generic peer-reviewed submission datasets, and does not test its performance on niche domain-specific research idea evaluation such as for robotics or 3D vision tasks, nor does it address robustness to evaluation of highly novel unproven ideas with limited existing supporting literature.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.14367)
- **👥 Authors**: Shuofei Qiao, Yunxiang Wei, Xuehai Wang, Bin Wu, Boyang Xue, Ningyu Zhang, Hossein A. Rahmani, Yanshan Wang, Qiang Zhang, Keyan Ding, Jeff Z. Pan, Huajun Chen, Emine Yilmaz
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 BrowseComp-V^3: A Visual, Vertical, and Verifiable Benchmark for Multimodal Browsing Agents (Score: 2/10)
- **💡 Innovation**: The key novelty is the introduction of BrowseComp-V^3, a 300-question challenging multimodal web browsing benchmark emphasizing cross-modal multi-hop reasoning with publicly verifiable evidence and fine-grained subgoal-driven process evaluation, alongside the unified OmniSeeker multimodal browsing agent framework.
- **⚠️ Limitations**: This work is limited to the web browsing agent domain, has no applicability to robotics, 3D perception, or embodied AI tasks aligned with the specified research interests, and does not explore integration with relevant techniques such as diffusion models, Gaussian splatting, or reinforcement learning.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12876)
- **👥 Authors**: Huanyao Zhang, Jiepeng Zhou, Bo Li, Bowen Zhou, Yanzhe Dan, Haishan Lu, Zhiyong Cao, Jiaoyang Chen, Yuqian Han, Zinan Sheng, Zhengwei Tao, Hao Liang, Jialong Wu, Yang Shi, Yuanpeng He, Jiaye Lin, Qintong Zhang, Guochen Yan, Runhao Zhao, Zhengpin Li, Xiaohan Yu, Lang Mei, Chong Chen, Wentao Zhang, Bin Cui
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 CellMaster: Collaborative Cell Type Annotation in Single-Cell Analysis (Score: 2/10)
- **💡 Innovation**: The key novelty is CellMaster, a zero-shot cell-type annotation AI agent that leverages LLM-encoded biological knowledge to generate interpretable annotations without requiring pre-training or fixed marker databases, with optional human-in-the-loop refinement that further improves annotation accuracy especially for rare and novel cell states.
- **⚠️ Limitations**: This work is restricted to the computational biology domain of single-cell RNA-seq analysis, has no relevance to your core robotics and AI research areas, and its performance is limited by the accuracy of biological knowledge encoded in the underlying large language model.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.13346)
- **👥 Authors**: Zhen Wang, Yiming Gao, Jieyuan Liu, Enze Ma, Jefferson Chen, Mark Antkowiak, Mengzhou Hu, JungHo Kong, Dexter Pratt, Zhiting Hu, Wei Wang, Trey Ideker, Eric P. Xing
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 EditCtrl: Disentangled Local and Global Control for Real-Time Generative Video Editing (Score: 2/10)
- **💡 Innovation**: The key novelty is EditCtrl, an efficient video inpainting control framework that uses a masked-token-only local video context module paired with a lightweight temporal global context embedder, delivering 10x higher compute efficiency and better editing quality than prior full-attention state-of-the-art generative editing methods.
- **⚠️ Limitations**: This work is limited to standard 2D generative video editing tasks, with no exploration of applications to robotics, embodied AI, 3D/4D scene modeling, or world modeling use cases, and does not confirm compatibility with diffusion models or large language models for more flexible control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.15031)
- **👥 Authors**: Yehonathan Litman, Shikun Liu, Dario Seyb, Nicholas Milef, Yang Zhou, Carl Marshall, Shubham Tulsiani, Caleb Leak
- **🏷️ Tags**: #Foundation_Model

---

### 📄 Exposing the Systematic Vulnerability of Open-Weight Models to Prefill Attacks (Score: 2/10)
- **💡 Innovation**: This work presents the largest systematic empirical study of prefill attacks on open-weight LLMs to date, evaluating over 20 existing and novel attack strategies across multiple model families and revealing a previously underexplored widespread vulnerability in all major contemporary open-weight models.
- **⚠️ Limitations**: The study does not develop or evaluate targeted defenses against prefill attacks, nor does it assess if these vulnerabilities extend to non-language foundation models such as vision-language-action models used in robotics and embodied AI.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.14689)
- **👥 Authors**: Lukas Struppek, Adam Gleave, Kellin Pelrine
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Can I Have Your Order? Monte-Carlo Tree Search for Slot Filling Ordering in Diffusion Language Models (Score: 2/10)
- **💡 Innovation**: The key novelty is the McDiffuSE framework that formulates slot selection for plan-and-infill decoding in masked diffusion models as a decision-making problem optimized via Monte Carlo Tree Search to systematically explore generation orders and improve output quality on reasoning tasks.
- **⚠️ Limitations**: The work is only evaluated on mathematical reasoning and code generation benchmarks, does not explore applicability to diffusion model use cases in robotics or embodied AI, and lacks analysis of generalization across different scales of masked diffusion models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12586)
- **👥 Authors**: Joshua Ong Jun Leang, Yu Zhao, Mihaela Cătălina Stoian, Wenda Li, Shay B. Cohen, Eleonora Giunchiglia
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #LLM

---

### 📄 Blind to the Human Touch: Overlap Bias in LLM-Based Summary Evaluation (Score: 2/10)
- **💡 Innovation**: This work provides a granular analysis of LLM judge bias as a function of overlap with human-written summaries, revealing that most tested small to medium LLMs increasingly prefer LLM-generated summaries over human ones as content similarity measured by ROUGE and BLEU decreases.
- **⚠️ Limitations**: The study only evaluates LLMs up to 12B parameters on English text summarization tasks, and does not explore whether the observed overlap bias extends to larger LLMs, other language tasks, or use cases relevant to robotics and embodied AI research.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.07673)
- **👥 Authors**: Jiangnan Fang, Cheng-Tse Liu, Hanieh Deilamsalehy, Nesreen K. Ahmed, Puneet Mathur, Nedim Lipka, Franck Dernoncourt, Ryan A. Rossi
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 A Critical Look at Targeted Instruction Selection: Disentangling What Matters (and What Doesn't) (Score: 2/10)
- **💡 Innovation**: This work provides the first systematic controlled analysis of data representation and selection algorithm components for targeted LLM instruction selection, unifying existing selection algorithms as forms of approximate distance minimization between selected subsets and query sets with supporting new generalization bounds.
- **⚠️ Limitations**: The study only evaluates its findings on generic LLM instruction tuning tasks, and does not explore the applicability of its data selection framework to specialized use cases such as robotics VLA fine-tuning or embodied AI, nor does it test performance on the largest state-of-the-art LLM parameter scales.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.14696)
- **👥 Authors**: Nihal V. Nayak, Paula Rodriguez-Diaz, Neha Hulkund, Sara Beery, David Alvarez-Melis
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 SPILLage: Agentic Oversharing on the Web (Score: 2/10)
- **💡 Innovation**: This work formalizes the Natural Agentic Oversharing phenomenon for LLM-powered web agents, proposes the SPILLage two-dimensional taxonomy covering channel and directness to categorize oversharing types, and empirically verifies that behavioral oversharing is 5 times more prevalent than content oversharing in web agent tasks.
- **⚠️ Limitations**: The study only conducts experiments on e-commerce web scenarios, does not explore more effective oversharing mitigation approaches beyond pre-execution irrelevant information removal, and lacks evaluation on other web agent application domains such as office automation and social media interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.13516)
- **👥 Authors**: Jaechul Roh, Eugene Bagdasarian, Hamed Haddadi, Ali Shahin Shamsabadi
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 A Few-Shot LLM Framework for Extreme Day Classification in Electricity Markets (Score: 1/10)
- **💡 Innovation**: The key novelty is a data-efficient few-shot LLM framework that converts electricity market system state statistical features into natural language prompts to classify extreme price spike days, outperforming traditional supervised models such as SVM and XGBoost under limited historical data conditions.
- **⚠️ Limitations**: The work is only validated on historical data from the Texas electricity market, lacks cross-regional market generalization testing, and does not compare against state-of-the-art time series forecasting or classification models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16735v1)
- **👥 Authors**: Saud Alghumayjan, Ming Yi, Bolun Xu
- **🏷️ Tags**: #LLM #Foundation_Model

---


