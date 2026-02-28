# 📅 2026-02-18 - Paper Digest
## Summary
Total Papers: 35 | High Impact: 5

## 📝 Papers List
### 🔥 Geometry-Aware Rotary Position Embedding for Consistent Video World Model (Score: 8/10)
- **💡 Innovation**: The key novelty is the proposal of ViewRope, a geometry-aware rotary position embedding that encodes camera-ray directions instead of screen-space pixel positions in video transformer self-attention, paired with a geometry-aware frame-sparse attention mechanism and the ViewBench diagnostic suite to reduce geometric drift and boost efficiency of video world models.
- **⚠️ Limitations**: The work does not evaluate the integration of the proposed consistent video world model with downstream embodied AI, reinforcement learning, or robot manipulation pipelines, nor does it test performance on real-world dynamic or unconstrained scene data.
- **🔗 Link**: [[GeometryAware_Rotary_Position_Embedding_for_Consistent_Video_World_Model]]
- **👥 Authors**: Chendong Xiang, Jiajun Liu, Jintao Zhang, Xiao Yang, Zhengwei Fang, Shizun Wang, Zijun Wang, Yingtian Zou, Hang Su, Jun Zhu
- **🏷️ Tags**: #World_Model #Embodied_AI

---

### ✨ MALLVI: A Multi-Agent Framework for Integrated Generalized Robotics Manipulation (Score: 7/10)
- **💡 Innovation**: The key novelty is a closed-loop multi-agent large language and vision framework for robotic manipulation that decomposes the task pipeline into specialized modular agents and supports targeted error recovery by only reactivating relevant agents instead of full replanning, boosting zero-shot task success rates.
- **⚠️ Limitations**: The work lacks ablation studies quantifying the contribution of each individual agent module, does not evaluate performance on long-horizon complex manipulation tasks, and does not integrate advanced 3D scene representations or dynamic world modeling for more robust perception in highly unstructured environments.
- **🔗 Link**: [[MALLVI]]
- **👥 Authors**: Iman Ahmadi, Mehrshad Taji, Arad Mahdinezhad Kashani, AmirHossein Jadidi, Saina Kashani, Babak Khalaj
- **🏷️ Tags**: #LLM #Robot_Manipulation #Embodied_AI #Foundation_Model #VLA

---

### ✨ SimToolReal: An Object-Centric Policy for Zero-Shot Dexterous Tool Manipulation (Score: 7/10)
- **💡 Innovation**: The key novelty is a sim-to-real reinforcement learning framework trained on procedurally generated diverse tool-like primitive objects with a universal pose manipulation objective, enabling zero-shot dexterous tool manipulation across unseen real-world tasks, object instances, and tool categories without any task or object-specific fine-tuning.
- **⚠️ Limitations**: The work does not incorporate advanced perception or foundation model-based approaches including VLAs, LLMs, or 3D Gaussian Splatting that are part of the user's stated interests, and also does not evaluate generalization to complex multi-step tool use tasks requiring dynamic force regulation.
- **🔗 Link**: [[SimToolReal]]
- **👥 Authors**: Kushal Kedia, Tyler Ga Wei Lum, Jeannette Bohg, C. Karen Liu
- **🏷️ Tags**: #Sim2Real #Reinforcement_Learning #Robot_Manipulation #Embodied_AI

---

### ✨ Causal-JEPA: Learning World Models through Object-Level Latent Interventions (Score: 7/10)
- **💡 Innovation**: The key novelty is extending masked joint embedding prediction from image patches to object-centric representations, using object-level masking to induce causal latent interventions that improve counterfactual reasoning and planning efficiency for world models.
- **⚠️ Limitations**: The work does not evaluate performance on real-world embodied tasks like robot manipulation, does not explore integration with foundation models or VLAs, and lacks validation of sim2real transfer capability for the proposed world model.
- **🔗 Link**: [[CausalJEPA]]
- **👥 Authors**: Heejeong Nam, Quentin Le Lidec, Lucas Maes, Yann LeCun, Randall Balestriero
- **🏷️ Tags**: #World_Model #Embodied_AI #Reinforcement_Learning

---

### ✨ Learning Native Continuation for Action Chunking Flow Policies (Score: 7/10)
- **💡 Innovation**: The key novelty is Legato, a training-time continuation method for action-chunked flow-based VLA policies that uses schedule-shaped denoising initialization from a mixture of known actions and noise, reshapes learned flow dynamics for train-inference consistency, and applies randomized schedule conditioning to eliminate chunk boundary discontinuities and enable controllable trajectory smoothness.
- **⚠️ Limitations**: The work does not evaluate generalizability to long-horizon manipulation tasks, compare against non-flow-based action chunking baselines, or test integration with widely used large pre-trained generalist VLA models like OpenVLA or RT-2.
- **🔗 Link**: [[Learning_Native_Continuation_for_Action_Chunking_Flow_Policies]]
- **👥 Authors**: Yufeng Liu, Hang Yu, Juntu Zhao, Bocheng Li, Di Zhang, Mingzhu Li, Wenxuan Wu, Yingdong Hu, Junyuan Xie, Junliang Guo, Dequan Wang, Yang Gao
- **🏷️ Tags**: #VLA #Embodied_AI #Robot_Manipulation #Foundation_Model

---

### 📄 Mind the GAP: Text Safety Does Not Transfer to Tool-Call Safety in LLM Agents (Score: 4/10)
- **💡 Innovation**: The key novelty is the introduction of the GAP benchmark, a systematic evaluation framework that quantifies divergence between text-level safety and tool-call-level safety in LLM agents, alongside empirical proof that text-only alignment does not transfer to safe tool call behavior across multiple frontier models and test conditions.
- **⚠️ Limitations**: The study only evaluates digital tool use cases in non-physical regulated domains, does not test tool-call safety for embodied or robotic systems, and does not propose generalizable, actionable mitigation strategies for the identified tool-call safety gaps.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16943v1)
- **👥 Authors**: Arnold Cartagena, Ariane Teixeira
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Discovering Multiagent Learning Algorithms with Large Language Models (Score: 4/10)
- **💡 Innovation**: The key novelty is the development of AlphaEvolve, an LLM-powered evolutionary coding agent that automatically explores the large multi-agent reinforcement learning algorithm design space to discover novel, state-of-the-art variants of both iterative regret minimization and population-based training game-theoretic learning paradigms.
- **⚠️ Limitations**: The work is only validated on imperfect-information multi-agent game benchmarks, with no exploration of generalizability to other reinforcement learning application domains (such as robot manipulation or embodied AI) and no analysis of the interpretability of the automatically discovered algorithmic mechanisms.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16928v2)
- **👥 Authors**: Zun Li, John Schultz, Daniel Hennes, Marc Lanctot
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 StereoAdapter-2: Globally Structure-Consistent Underwater Stereo Depth Estimation (Score: 4/10)
- **💡 Innovation**: The key novelty is replacing conventional ConvGRU updaters with a novel ConvSS2D operator based on selective state space models for efficient long-range spatial disparity propagation in a single update step, paired with a new large-scale synthetic underwater stereo dataset UW-StereoDepth-80K built via a two-stage pipeline combining semantic-aware style transfer and geometry-consistent novel view synthesis.
- **⚠️ Limitations**: The work only evaluates standalone stereo depth estimation performance without exploring integration with downstream embodied AI tasks such as underwater navigation or manipulation, and does not leverage other relevant advanced techniques from your interest areas like diffusion models or Gaussian splatting to further improve performance.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16915v1)
- **👥 Authors**: Zeyu Ren, Xiang Li, Yiran Wang, Zeyu Zhang, Hao Tang
- **🏷️ Tags**: #Embodied_AI #Foundation_Model #Sim2Real

---

### 📄 LLM-WikiRace Benchmark: How Far Can LLMs Plan over Real-World Knowledge Graphs? (Score: 4/10)
- **💡 Innovation**: The key novelty is the proposal of the LLM-Wikirace benchmark, which evaluates large language models' planning, long-horizon reasoning, and world knowledge capabilities via the task of navigating Wikipedia hyperlinks from a specified source page to a target page.
- **⚠️ Limitations**: The work only evaluates LLM performance on Wikipedia hyperlink navigation, does not provide solutions to the identified planning and replanning deficiencies of frontier LLMs, and does not extend its findings to downstream use cases such as embodied AI or robot task planning.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16902v3)
- **👥 Authors**: Juliusz Ziomek, William Bankes, Lorenz Wolf, Shyam Sundhar Ramesh, Xiaohang Tang, Ilija Bogunovic
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 STAPO: Stabilizing Reinforcement Learning for LLMs by Silencing Rare Spurious Tokens (Score: 4/10)
- **💡 Innovation**: The key novelty is identifying that approximately 0.01% of rare spurious tokens drive late-stage training instability and performance collapse in RL fine-tuning of LLMs, and proposing the STAPO algorithm that selectively masks gradient updates for these tokens to stabilize training and improve reasoning performance.
- **⚠️ Limitations**: The work is only evaluated on text-based mathematical reasoning benchmarks for standard LLMs, with no exploration of applicability to multi-modal models, robotics/embodied AI tasks, or other LLM downstream use cases outside reasoning.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.15620)
- **👥 Authors**: Shiqi Liu, Zeyu He, Guojian Zhan, Letian Tao, Zhilong Zheng, Jiang Wu, Yinuo Wang, Yang Guan, Kehua Sheng, Bo Zhang, Keqiang Li, Jingliang Duan, Shengbo Eben Li
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 Automating Agent Hijacking via Structural Template Injection (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposed Phantom automated agent hijacking framework that targets LLM agent architectural mechanisms via optimized structured template injection, combined with a template autoencoder and Bayesian optimization to improve attack success rate and transferability to black-box commercial models.
- **⚠️ Limitations**: The paper does not provide comprehensive defensive mechanisms against the proposed structured template injection attacks, nor does it evaluate the attack's efficacy on LLM agents integrated with robotics or embodied AI systems.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16958v1)
- **👥 Authors**: Xinhao Deng, Jiaqing Wu, Miao Chen, Yue Xiao, Ke Xu, Qi Li
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 LLM4Cov: Execution-Aware Agentic Learning for High-coverage Testbench Generation (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposal of LLM4Cov, an offline agent learning framework for high-coverage hardware verification, paired with execution-validated data curation, policy-aware agentic data synthesis, and worst-state-prioritized sampling to enable scalable LLM agent learning without expensive online reinforcement learning feedback.
- **⚠️ Limitations**: The work is only validated on hardware verification tasks, with no exploration of its applicability to robotics or embodied AI use cases, and lacks comparison against state-of-the-art general offline reinforcement learning methods for agent learning.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16953v2)
- **👥 Authors**: Hejia Zhang, Zhongming Yu, Chia-Tung Ho, Haoxing Ren, Brucek Khailany, Jishen Zhao
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 SourceBench: Can AI Answers Reference Quality Web Sources? (Score: 3/10)
- **💡 Innovation**: The key novelty is the introduction of SourceBench, a benchmark with an eight-metric evaluation framework and human-calibrated LLM evaluator to assess the quality of web sources cited by LLMs and AI search tools across multiple query intents, instead of only evaluating answer correctness as in prior work.
- **⚠️ Limitations**: The benchmark only covers 100 general-domain queries across 5 intent categories, does not address source citation evaluation for specialized domains like robotics or embodied AI, and does not propose methods to improve the source citation quality of LLMs.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16942v1)
- **👥 Authors**: Hexi Jin, Stephen Liu, Yuheng Li, Simran Malik, Yiying Zhang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 AgentLAB: Benchmarking LLM Agents against Long-Horizon Attacks (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposal of AgentLAB, the first dedicated benchmark for measuring LLM agent vulnerabilities to adaptive long-horizon multi-turn attacks, covering 5 distinct attack types, 28 realistic environments, and 644 security test cases.
- **⚠️ Limitations**: The benchmark currently only supports general LLM agent security evaluation, with no integration of embodied AI, robotic manipulation or other robotics-related agent scenarios, and does not assess cross-domain applicability to robotics use cases.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16901v1)
- **👥 Authors**: Tanqiu Jiang, Yuhui Wang, Jiacheng Liang, Ting Wang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 OpenSage: Self-programming Agent Generation Engine (Score: 3/10)
- **💡 Innovation**: OpenSage is the first agent development kit that enables LLMs to automatically generate agents with self-created topology and toolsets, paired with a hierarchical graph-based memory system, eliminating the need for manual human design of core agent components.
- **⚠️ Limitations**: The work only evaluates OpenSage on generic agent and software engineering benchmarks, with no demonstrated applicability to robotics, embodied AI, 3D vision, reinforcement learning, or other domains listed in the stated research interests, and does not integrate with relevant state-of-the-art paradigms like world models or diffusion models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16891v1)
- **👥 Authors**: Hongwei Li, Zhun Wang, Qinrun Dai, Yuzhou Nie, Jinjun Peng, Ruitong Liu, Jingyang Zhang, Kaijie Zhu, Jingxuan He, Lun Wang, Yangruibo Ding, Yueqi Chen, Wenbo Guo, Dawn Song
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Training Large Reasoning Models Efficiently via Progressive Thought Encoding (Score: 3/10)
- **💡 Innovation**: The key novelty is Progressive Thought Encoding, a parameter-efficient fine-tuning method that progressively encodes intermediate reasoning steps of large reasoning models into fixed-size vectors to reduce memory overhead of reinforcement learning training and inference while preserving long-context reasoning performance under fixed cache budgets.
- **⚠️ Limitations**: The work is only validated on mathematical reasoning benchmarks for general large language models, with no exploration of its utility for robotics, embodied AI, or other domains aligned with your core research interests, and no comparison to non-parameter-efficient full fine-tuning baselines.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16839v1)
- **👥 Authors**: Zeliang Zhang, Xiaodong Liu, Hao Cheng, Hao Sun, Chenliang Xu, Jianfeng Gao
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 GLM-5: from Vibe Coding to Agentic Engineering (Score: 3/10)
- **💡 Innovation**: GLM-5 adopts DSA to reduce training and inference costs while maintaining long-context fidelity, implements an asynchronous reinforcement learning infrastructure that decouples generation from training to improve post-training efficiency, and proposes novel asynchronous agent RL algorithms to enable better learning from long-horizon complex interactions, achieving SOTA performance on coding and end-to-end software engineering tasks.
- **⚠️ Limitations**: The paper does not address any research topics related to embodied AI, robot manipulation, 3D/4D Gaussian Splatting, diffusion models, world models or sim2real that align with the stated research interests, and lacks detailed ablation analysis of its proposed asynchronous RL algorithm components.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.15763)
- **👥 Authors**: GLM-5 Team, Aohan Zeng, Xin Lv, Zhenyu Hou, Zhengxiao Du, Qinkai Zheng, Bin Chen, Da Yin, Chendi Ge, Chengxing Xie, Cunxiang Wang, Gengzheng Pan, Hao Zeng, Haoke Zhang, Haoran Wang, Huilong Chen, Jiajie Zhang, Jian Jiao, Jiaqi Guo, Jingsen Wang, Jingzhao Du, Jinzhu Wu, Kedong Wang, Lei Li, Lin Fan, Lucen Zhong, Mingdao Liu, Mingming Zhao, Pengfan Du, Qian Dong, Rui Lu, Shuang-Li, Shulin Cao, Song Liu, Ting Jiang, Xiaodong Chen, Xiaohan Zhang, Xuancheng Huang, Xuezhen Dong, Yabo Xu, Yao Wei, Yifan An, Yilin Niu, Yitong Zhu, Yuanhao Wen, Yukuo Cen, Yushi Bai, Zhongpei Qiao, Zihan Wang, Zikang Wang, Zilin Zhu, Ziqiang Liu, Zixuan Li, Bojie Wang, Bosi Wen, Can Huang, Changpeng Cai, Chao Yu, Chen Li, Chen Li, Chenghua Huang, Chengwei Hu, Chenhui Zhang, Chenzheng Zhu, Congfeng Yin, Daoyan Lin, Dayong Yang, Di Wang, Ding Ai, Erle Zhu, Fangzhou Yi, Feiyu Chen, Guohong Wen, Hailong Sun, Haisha Zhao, Haiyi Hu, Hanchen Zhang, Hanrui Liu, Hanyu Zhang, Hao Peng, Hao Tai, Haobo Zhang, He Liu, Hongwei Wang, Hongxi Yan, Hongyu Ge, Huan Liu, Huan Liu, Huanpeng Chu, Jia'ni Zhao, Jiachen Wang, Jiajing Zhao, Jiamin Ren, Jiapeng Wang, Jiaxin Zhang, Jiayi Gui, Jiayue Zhao, Jijie Li, Jing An, Jing Li, Jingwei Yuan, Jinhua Du, Jinxin Liu, Junkai Zhi, Junwen Duan, Kaiyue Zhou, Kangjian Wei, Ke Wang, Keyun Luo, Laiqiang Zhang, Leigang Sha, Liang Xu, Lindong Wu, Lintao Ding, Lu Chen, Minghao Li, Nianyi Lin, Pan Ta, Qiang Zou, Rongjun Song, Ruiqi Yang, Shangqing Tu, Shangtong Yang, Shaoxiang Wu, Shengyan Zhang, Shijie Li, Shuang Li, Shuyi Fan, Wei Qin, Wei Tian, Weining Zhang, Wenbo Yu, Wenjie Liang, Xiang Kuang, Xiangmeng Cheng, Xiangyang Li, Xiaoquan Yan, Xiaowei Hu, Xiaoying Ling, Xing Fan, Xingye Xia, Xinyuan Zhang, Xinze Zhang, Xirui Pan, Xunkai Zhang, Yandong Wu, Yanfu Li, Yidong Wang, Yifan Zhu, Yijun Tan, Yilin Zhou, Yiming Pan, Ying Zhang, Yinpei Su, Yipeng Geng, Yipeng Geng, Yong Yan, Yonglin Tan, Yuean Bi, Yuhan Shen, Yuhao Yang, Yujiang Li, Yunan Liu, Yunqing Wang, Yuntao Li, Yurong Wu, Yutao Zhang, Yuxi Duan, Yuxuan Zhang, Zezhen Liu, Zhengtao Jiang, Zhenhe Yan, Zheyu Zhang, Zhixiang Wei, Zhuo Chen, Zhuoer Feng, Zijun Yao, Ziwei Chai, Ziyuan Wang, Zuzhou Zhang, Bin Xu, Minlie Huang, Hongning Wang, Juanzi Li, Yuxiao Dong, Jie Tang
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 On Surprising Effectiveness of Masking Updates in Adaptive Optimizers (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposal of Momentum-aligned gradient masking (Magma), a simple drop-in adaptive optimizer that uses random parameter update masking modulated by momentum-gradient alignment to deliver consistent performance gains over state-of-the-art optimizers for LLM pre-training with negligible computational overhead.
- **⚠️ Limitations**: The work only validates Magma on LLM pre-training tasks up to 1B parameters, with no evaluation of its effectiveness on other model types, downstream applications, or any of the robotics and embodied AI use cases aligned with your research interests.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.15322)
- **👥 Authors**: Taejong Joo, Wenhan Xia, Cheolmin Kim, Ming Zhang, Eugene Ie
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 TAROT: Test-driven and Capability-adaptive Curriculum Reinforcement Fine-tuning for Code Generation with Large Language Models (Score: 3/10)
- **💡 Innovation**: The key novelty is TAROT, a test-driven and capability-adaptive curriculum reinforcement fine-tuning framework that uses a four-tier difficulty test suite to decouple curriculum progression from raw reward scores, enabling stable optimization and improved robustness of LLM-generated code.
- **⚠️ Limitations**: The work is only validated on code generation tasks, with no exploration of applicability to robotics, embodied AI, or other domains in the user's stated interests, and it does not verify if the curriculum policy generalizes to non-code LLM fine-tuning scenarios.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.15449)
- **👥 Authors**: Chansung Park, Juyong Jiang, Fan Wang, Sayak Paul, Jiasi Shen, Jing Tang, Jianguo Li
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Panini: Continual Learning in Token Space via Structured Memory (Score: 3/10)
- **💡 Innovation**: The key novelty is a non-parametric continual learning framework for fixed base LLMs that stores new knowledge as entity- and event-aware Generative Semantic Workspace networks of QA pairs instead of raw document chunks, improving QA performance while drastically reducing inference-time context token usage and hallucinations.
- **⚠️ Limitations**: The work is only validated on text-only QA benchmarks, with no testing of applicability to multi-modal data, robotics use cases, or scaling to extremely large knowledge corpora and extended continual learning time horizons.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.15156)
- **👥 Authors**: Shreyas Rajesh, Pavan Holur, Mehmet Yigit Turali, Chenda Duan, Vwani Roychowdhury
- **🏷️ Tags**: #LLM #Foundation_Model #Continual_Learning #Retrieval_Augmented_Generation

---

### 📄 Prescriptive Scaling Reveals the Evolution of Language Model Capabilities (Score: 3/10)
- **💡 Innovation**: The key novelty is a smoothed quantile regression framework with monotone saturating sigmoid parameterization to estimate prescriptive, temporally stable scaling laws for foundation model performance across tasks, alongside the release of the Proteus 2k evaluation dataset and an efficient algorithm that recovers near-full performance frontiers using only 20% of the typical evaluation budget.
- **⚠️ Limitations**: The work only evaluates general foundation model and LLM performance on standard academic benchmarks, does not explore the applicability of its proposed scaling law framework to domain-specific models for robotics or embodied AI, and does not fully account for emerging post-training techniques that could shift performance boundaries.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.15327)
- **👥 Authors**: Hanlin Zhang, Jikai Jin, Vasilis Syrgkanis, Sham Kakade
- **🏷️ Tags**: #Foundation_Model #LLM

---

### 📄 BrainRVQ: A High-Fidelity EEG Foundation Model via Dual-Domain Residual Quantization and Hierarchical Autoregression (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed BrainRVQ general-purpose EEG foundation model that uses a Dual-Domain Residual Vector Quantization tokenizer to disentangle temporal waveforms and spectral patterns of EEG signals, paired with a hierarchical autoregressive pre-training objective with importance-guided curriculum masking to learn robust, generalizable neural representations.
- **⚠️ Limitations**: The work is limited exclusively to clinical EEG representation learning and does not explore cross-modal integration with other foundation models, or potential applications to embodied AI, robot control, or other domains aligned with common robotics and applied AI research interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16951v1)
- **👥 Authors**: Mingzhe Cui, Tao Chen, Yang Jiao, Yiqin Wang, Lei Xie, Yi Pan, Luca Mainardi
- **🏷️ Tags**: #Foundation_Model #EEG_Representation_Learning #Residual_Vector_Quantization #Autoregressive_Pre_Training #Neural_Signal_Modeling

---

### 📄 DeepContext: Stateful Real-Time Detection of Multi-Turn Adversarial Intent Drift in LLMs (Score: 2/10)
- **💡 Innovation**: The key novelty is DeepContext, a stateful RNN-based monitoring framework that tracks temporal user intent trajectories across multi-turn LLM conversations to detect incremental adversarial jailbreak attempts that stateless safety guardrails miss.
- **⚠️ Limitations**: The work only evaluates on standard multi-turn LLM jailbreak benchmarks, does not test generalization to use cases like LLM integration with VLA or embodied AI systems, and lacks analysis of robustness against adaptive adversarial attacks designed to bypass stateful monitors.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16935v1)
- **👥 Authors**: Justin Albrethsen, Yash Datta, Kunal Kumar, Sharath Rajasekar
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 RankEvolve: Automating the Discovery of Retrieval Algorithms via LLM-Driven Evolution (Score: 2/10)
- **💡 Innovation**: The key novelty is RankEvolve, an LLM-guided evolutionary program search framework that automatically discovers novel, high-performing lexical retrieval algorithms starting from BM25 and query likelihood seed programs, removing the reliance on human intuition for ranking algorithm design.
- **⚠️ Limitations**: This work is only evaluated on information retrieval benchmarks, does not explore applicability to robotics or embodied AI use cases, and does not analyze the computational cost of the LLM-driven evolutionary search process at scale.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16932v1)
- **👥 Authors**: Jinming Nian, Fangchen Li, Dae Hoon Park, Yi Fang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Say It My Way: Exploring Control in Conversational Visual Question Answering with Blind Users (Score: 2/10)
- **💡 Innovation**: The key novelty is empirically studying prompting and customization techniques adopted by 11 blind users interacting with conversational VQA systems, releasing a new public interaction dataset, and providing design insights for more accessible assistive VQA tools.
- **⚠️ Limitations**: The work only identifies user-side prompt engineering workarounds for flaws in current VQA systems instead of proposing concrete system-level or architectural improvements to resolve core issues like poor spatial distance estimation, lack of verbosity controls, and missing camera guidance for blind users.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16930v1)
- **👥 Authors**: Farnaz Zamiri Zeraati, Yang Trista Cao, Yuehan Qiao, Hal Daumé, Hernisa Kacorri
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Xray-Visual Models: Scaling Vision models on Industry Scale Data (Score: 2/10)
- **💡 Innovation**: The key novelty is a unified multimodal vision model architecture trained on 15 billion curated image-text pairs and 10 billion video-hashtag pairs, using a three-stage training pipeline combining self-supervised MAE, semi-supervised hashtag classification, and CLIP-style contrastive learning, with LLM integration as text encoders to boost cross-modal retrieval performance and generalization.
- **⚠️ Limitations**: The work does not explore applications of the proposed model to robotics, embodied AI, 3D perception, or any other task areas relevant to your core research interests, and lacks evaluation on non-social-media domain benchmarks related to real-world robotic deployment.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16918v1)
- **👥 Authors**: Shlok Mishra, Tsung-Yu Lin, Linda Wang, Hongli Xu, Yimin Liu, Michael Hsu, Chaitanya Ahuja, Hao Yuan, Jianpeng Cheng, Hong-You Chen, Haoyuan Xu, Chao Li, Abhijeet Awasthi, Jihye Moon, Don Husa, Michael Ge, Sumedha Singla, Arkabandhu Chowdhury, Phong Dingh, Satya Narayan Shukla, Yonghuan Yang, David Jacobs, Qi Guo, Jun Xiao, Xiangjun Fan, Aashu Singh
- **🏷️ Tags**: #Foundation_Model #LLM #Contrastive_Learning #Vision_Transformer #Multimodal_Vision

---

### 📄 AdaptOrch: Task-Adaptive Multi-Agent Orchestration in the Era of LLM Performance Convergence (Score: 2/10)
- **💡 Innovation**: The key novelty is the formal AdaptOrch framework that dynamically selects optimal multi-agent orchestration topologies based on task dependency graphs, paired with a provable performance convergence scaling law, linear-time topology routing algorithm, and adaptive output synthesis protocol with termination guarantees.
- **⚠️ Limitations**: The work is only validated on NLP tasks including coding, reasoning, and retrieval-augmented generation, with no exploration of applicability to robotics, embodied AI, or other non-NLP domains, and no assessment of performance when integrating non-LLM foundation models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16873v1)
- **👥 Authors**: Geunbin Yu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 DODO: Discrete OCR Diffusion Models (Score: 2/10)
- **💡 Innovation**: The key novelty is DODO, the first vision-language model leveraging block discrete diffusion to enable efficient parallel decoding for OCR while mitigating the synchronization errors that plague global diffusion models for exact-match deterministic tasks.
- **⚠️ Limitations**: The work is only evaluated on OCR tasks, lacks exploration of generalizability to other deterministic sequential generation tasks, and does not include ablation studies on the impact of block size on inference speed and accuracy tradeoffs for varying document lengths.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16872v1)
- **👥 Authors**: Sean Man, Roy Ganz, Roi Ronen, Shahar Tsiper, Shai Mazor, Niv Nayman
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 Position: Why a Dynamical Systems Perspective is Needed to Advance Time Series Modeling (Score: 2/10)
- **💡 Innovation**: The key novelty is the position that integrating dynamical systems theory and dynamical systems reconstruction approaches can advance time series modeling by enabling more accurate long-term forecasting, better generalization to unseen system regimes, and significantly lower computational and memory footprints compared to existing approaches.
- **⚠️ Limitations**: As a purely position-focused work, it provides no empirical validation of its proposed claims, no head-to-head performance benchmarks against state-of-the-art time series models, and no concrete implementation guidance for translating dynamical systems insights into practical time series modeling pipelines.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16864v1)
- **👥 Authors**: Daniel Durstewitz, Christoph Jürgen Hemmer, Florian Hess, Charlotte Ricarda Doll, Lukas Eisenmann
- **🏷️ Tags**: #Foundation_Model

---

### 📄 Five Fatal Assumptions: Why T-Shirt Sizing Systematically Fails for AI Projects (Score: 2/10)
- **💡 Innovation**: The key novelty is identifying five foundational assumptions that make traditional T-shirt sizing agile estimation systematically fail for LLM and multi-agent AI projects, and proposing the iterative Checkpoint Sizing framework with explicit decision gates for regular scope and feasibility reassessment as a more suitable alternative.
- **⚠️ Limitations**: The work lacks rigorous empirical validation of the proposed Checkpoint Sizing approach across diverse AI project contexts, and does not assess its applicability to technical robotics, embodied AI, or generative AI research projects outside general LLM and software AI use cases.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17734v1)
- **👥 Authors**: Raja Soundaramourty, Ozkan Kilic, Ramu Chenchaiah
- **🏷️ Tags**: #LLM

---

### 📄 NeST: Neuron Selective Tuning for LLM Safety (Score: 2/10)
- **💡 Innovation**: The key novelty is NeST, a lightweight structure-aware LLM safety alignment framework that selectively adapts only small clustered subsets of safety-relevant neurons, achieving far stronger safety performance with drastically fewer trainable parameters than existing full fine-tuning, LoRA, and circuit breaker baselines.
- **⚠️ Limitations**: The work only evaluates on text-only LLM safety benchmarks, does not assess impacts on general LLM task performance post-alignment, and does not explore applicability to other foundation model types or robotics/embodied AI use cases.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.16835v1)
- **👥 Authors**: Sasha Behrouzi, Lichao Wu, Mohamadreza Rostami, Ahmad-Reza Sadeghi
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks (Score: 2/10)
- **💡 Innovation**: The key novelty is the introduction of SkillsBench, a standardized benchmark spanning 86 tasks across 11 domains paired with curated skills and deterministic verifiers to systematically measure the impact of different skill sources on LLM agent task performance.
- **⚠️ Limitations**: The benchmark is limited to non-embodied LLM agent tasks and does not evaluate skill transfer for embodied AI, robotic manipulation, or other robotics/3D vision use cases relevant to many applied AI research areas.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12670)
- **👥 Authors**: Xiangyi Li, Wenbo Chen, Yimin Liu, Shenghan Zheng, Xiaokun Chen, Yifeng He, Yubo Li, Bingran You, Haotian Shen, Jiankai Sun, Shuyi Wang, Qunhong Zeng, Di Wang, Xuandong Zhao, Yuanli Wang, Roey Ben Chaim, Zonglin Di, Yipeng Gao, Junwei He, Yizhuo He, Liqiang Jing, Luyang Kong, Xin Lan, Jiachen Li, Songlin Li, Yijiang Li, Yueqian Lin, Xinyi Liu, Xuanqing Liu, Haoran Lyu, Ze Ma, Bowei Wang, Runhui Wang, Tianyu Wang, Wengao Ye, Yue Zhang, Hanwen Xing, Yiqi Xue, Steven Dillmann, Han-chung Lee
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 ClinAlign: Scaling Healthcare Alignment from Clinician Preference (Score: 2/10)
- **💡 Innovation**: The key novelty is a two-stage clinical LLM alignment framework that leverages a 7,034-sample physician-verified preference dataset (HealthRubrics) to distill 119 reusable clinically grounded principles for both offline LLM alignment and inference-time guided self-revision, delivering strong benchmark performance with low inference compute overhead.
- **⚠️ Limitations**: The work is constrained to English clinical NLP use cases, does not demonstrate generalizability to non-medical LLM alignment tasks, and lacks validation of real-world clinical deployment efficacy with actual patient and clinician end users.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.09653)
- **👥 Authors**: Shiwei Lyu, Xidong Wang, Lei Liu, Hao Zhu, Chaohe Zhang, Jian Wang, Jinjie Gu, Benyou Wang, Yue Shen
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Detecting Overflow in Compressed Token Representations for Retrieval-Augmented Generation (Score: 2/10)
- **💡 Innovation**: This work defines the token overflow regime for soft-compressed large language model context representations and proposes a query-aware lightweight probing classifier that achieves 0.72 average AUC-ROC for overflow detection, outperforming prior query-agnostic saturation statistic methods.
- **⚠️ Limitations**: The method is only evaluated on the xRAG soft compression framework and three standard QA datasets, with no testing of generalizability to other LLM compression architectures, broader long-context tasks, or implementation of end-to-end overflow mitigation strategies beyond pre-LLM gating.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12235)
- **👥 Authors**: Julia Belikova, Danila Rozhevskii, Dennis Svirin, Konstantin Polev, Alexander Panchenko
- **🏷️ Tags**: #LLM #Foundation_Model #Retrieval_Augmented_Generation #Token_Compression

---

### 📄 How Much Reasoning Do Retrieval-Augmented Models Add beyond LLMs? A Benchmarking Framework for Multi-Hop Inference over Hybrid Knowledge (Score: 2/10)
- **💡 Innovation**: The key novelty is the introduction of HybridRAG-Bench, a contamination-aware, customizable benchmark framework that generates multi-hop reasoning question-answer pairs over hybrid unstructured text and structured knowledge graph data from recent scientific literature to fairly evaluate retrieval-augmented LLM systems without confounding from parametric knowledge recall.
- **⚠️ Limitations**: The benchmark is limited to text and knowledge graph reasoning across only three non-robotics domains, and does not support evaluation of multimodal, embodied, or robotics-specific reasoning scenarios relevant to your core research interests.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10210)
- **👥 Authors**: Junhong Lin, Bing Zhang, Song Wang, Ziyan Liu, Dan Gutfreund, Julian Shun, Yada Zhu
- **🏷️ Tags**: #LLM #Foundation_Model

---


