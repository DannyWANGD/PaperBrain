# 📅 2026-02-15 - Paper Digest
## Summary
Total Papers: 18 | High Impact: 1

## 📝 Papers List
### ✨ WIMLE: Uncertainty-Aware World Models with IMLE for Sample-Efficient Continuous Control (Score: 7/10)
- **💡 Innovation**: The key novelty is extending Implicit Maximum Likelihood Estimation (IMLE) to the model-based reinforcement learning framework to learn stochastic multi-modal world models with predictive uncertainty estimation, which weights synthetic transitions by confidence to reduce compounding error and bias for more sample-efficient continuous control.
- **⚠️ Limitations**: This work is only evaluated on simulated continuous control benchmarks, with no demonstration of real-world robotic applicability, integration with other relevant paradigms like diffusion models or foundation models, or testing on robot manipulation or sim2real transfer tasks.
- **🔗 Link**: [[WIMLE]]
- **👥 Authors**: Mehran Aghabozorgi, Alireza Moazeni, Yanshu Zhang, Ke Li
- **🏷️ Tags**: #World_Model #Reinforcement_Learning #Embodied_AI

---

### 📄 Zero-Shot Instruction Following in RL via Structured LTL Representations (Score: 4/10)
- **💡 Innovation**: The key novelty is conditioning multi-task reinforcement learning policies on sequences of Boolean formulae derived from finite automata of LTL task specifications, paired with a hierarchical neural encoding architecture and future subgoal attention mechanism to better capture logical and temporal structure for improved zero-shot task generalization.
- **⚠️ Limitations**: The work does not validate performance on embodied or robotic manipulation tasks, nor does it integrate state-of-the-art components like LLMs, foundation models, or VLAs that could enhance real-world instruction following capabilities.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14344v1)
- **👥 Authors**: Mathias Jackermeier, Mattia Giuri, Jacques Cloete, Alessandro Abate
- **🏷️ Tags**: #Reinforcement_Learning

---

### 📄 GRAIL: Goal Recognition Alignment through Imitation Learning (Score: 4/10)
- **💡 Innovation**: The key novelty of GRAIL is its combination of imitation learning and inverse reinforcement learning to learn per-candidate-goal directed policies directly from potentially suboptimal demonstration trajectories, enabling more accurate goal recognition than traditional optimal-policy based methods even when observed behavior is biased, suboptimal, or noisy.
- **⚠️ Limitations**: The work does not evaluate GRAIL on real-world embodied or robotic manipulation tasks, nor does it explore integration with modern foundation models, vision-language-action pipelines, or 3D perception methods that would expand its real-world applicability for aligned embodied AI systems.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14252v1)
- **👥 Authors**: Osher Elhadad, Felipe Meneguzzi, Reuth Mirsky
- **🏷️ Tags**: #Reinforcement_Learning #Embodied_AI

---

### 📄 AbracADDbra: Touch-Guided Object Addition by Decoupling Placement and Editing Subtasks (Score: 4/10)
- **💡 Innovation**: The key novelty is the proposed decoupled AbracADDbra framework that leverages touch priors to spatially ground text instructions for object placement via a vision-language transformer, followed by a diffusion model for high-fidelity object generation and blending, alongside the new Touch2Add benchmark for standardized evaluation of interactive object addition tasks.
- **⚠️ Limitations**: The work is restricted to 2D image editing use cases, does not extend to 3D scene editing, embodied robotic manipulation, or other core robotics research areas in your keyword list, and does not evaluate performance on any real-world robotic interaction scenarios.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14237v1)
- **👥 Authors**: Kunal Swami, Raghu Chittersu, Yuvraj Rathore, Rajeev Irny, Shashavali Doodekula, Alok Shukla
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 REDSearcher: A Scalable and Cost-Efficient Framework for Long-Horizon Search Agents (Score: 4/10)
- **💡 Innovation**: The key novelty is the proposed REDSearcher unified framework that co-designs dual-constrained high-quality scalable task synthesis, tool-augmented queries, mid-training for core atomic capability strengthening, and a local simulated environment for low-cost reinforcement learning iteration to address the bottlenecks of sparse high-quality trajectories and expensive interaction rollouts for long-horizon search agents.
- **⚠️ Limitations**: The work is only validated on text and multimodal search benchmarks, lacks exploration of applications to embodied or robotic search tasks, and provides no details on integration with perception, world modeling, or robotic control systems relevant to physical real-world use cases.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14234v1)
- **👥 Authors**: Zheng Chu, Xiao Wang, Jack Hong, Huiming Fan, Yuqi Huang, Yue Yang, Guohai Xu, Chenxiao Zhao, Cheng Xiang, Shengchao Hu, Dongdong Kuang, Ming Liu, Bing Qin, Xing Yu
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### 📄 Train Less, Learn More: Adaptive Efficient Rollout Optimization for Group-Based Reinforcement Learning (Score: 3/10)
- **💡 Innovation**: The key novelty is Adaptive Efficient Rollout Optimization (AERO), an improved GRPO variant that uses adaptive rollout sizing, selective rollout pruning, and Bayesian posterior maintenance to eliminate zero-advantage compute waste during RL-based LLM fine-tuning.
- **⚠️ Limitations**: The work is only validated on math-specific Qwen LLM variants for RL fine-tuning, with no testing of generalizability to other LLM families, non-math tasks, or relevant domains like embodied robot learning.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14338v1)
- **👥 Authors**: Zhi Zhang, Zhen Han, Costas Mavromatis, Qi Zhu, Yunyi Zhang, Sheng Guan, Dingmin Wang, Xiong Zhou, Shuai Wang, Soji Adeshina, Vassilis Ioannidis, Huzefa Rangwala
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 Benchmarking at the Edge of Comprehension (Score: 3/10)
- **💡 Innovation**: The key novelty is an adversarial Critique-Resilient Benchmarking framework that uses bounded human verification of localized claims and an itemized bipartite Bradley-Terry model to reliably rank LLMs even when humans cannot fully comprehend the evaluated complex tasks.
- **⚠️ Limitations**: The work is only validated on mathematical LLM tasks, does not explore applicability to domains like robotics or embodied AI relevant to the user's interests, and still relies on human adjudicators which may create scalability bottlenecks for large-scale benchmarking.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14307v2)
- **👥 Authors**: Samuele Marro, Jialin Yu, Emanuele La Malfa, Oishi Deb, Jiawei Li, Yibo Yang, Ebey Abraham, Sunando Sengupta, Eric Sommerlade, Michael Wooldridge, Philip Torr
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Text Before Vision: Staged Knowledge Injection Matters for Agentic RLVR in Ultra-High-Resolution Remote Sensing Understanding (Score: 3/10)
- **💡 Innovation**: The key novelty is a two-stage staged knowledge injection recipe that first injects domain reasoning priors via text-only Earth-science QA, then pre-warms on ultra-high-resolution image-text pairs during supervised fine-tuning to significantly boost agentic RLVR performance for remote sensing visual reasoning tasks.
- **⚠️ Limitations**: The work is only validated on remote sensing benchmarks, provides no exploration of generalizability to other domains such as robotics or embodied AI, and lacks ablation analysis of performance variance across different base foundation model scales.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14225v1)
- **👥 Authors**: Fengxiang Wang, Mingshuo Chen, Yueying Li, Yajie Yang, Yuhao Zhou, Di Wang, Yifan Zhang, Haoyu Wang, Haiyan Zhao, Hongda Sun, Long Lan, Jun Song, Yulin Wang, Jing Zhang, Wenlong Zhang, Bo Du
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 Conformal Signal Temporal Logic for Robust Reinforcement Learning Control: A Case Study (Score: 2/10)
- **💡 Innovation**: The key novelty is the introduction of a conformal Signal Temporal Logic (STL) shield that leverages online conformal prediction to filter reinforcement learning agent actions, providing stronger robustness guarantees for STL requirement satisfaction than classical rule-based STL shields under perturbed aerospace flight conditions.
- **⚠️ Limitations**: The work is only evaluated on a simulated F-16 aerospace flight control benchmark with no real-world validation, no exploration of extension to robotics or embodied AI use cases, and no comparison against a broader range of state-of-the-art safe reinforcement learning methods.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14322v2)
- **👥 Authors**: Hani Beirami, M M Manjurul Islam
- **🏷️ Tags**: #Reinforcement_Learning #Signal_Temporal_Logic #Conformal_Prediction #Safe_Control

---

### 📄 Floe: Federated Specialization for Real-Time LLM-SLM Inference (Score: 2/10)
- **💡 Innovation**: The key novelty is Floe, a hybrid federated learning framework that combines cloud-based black-box LLMs and on-device lightweight SLMs with heterogeneity-aware LoRA adaptation and logit-level fusion to achieve low-latency, privacy-preserving real-time language inference.
- **⚠️ Limitations**: The work does not explore applicability to multi-modal or robotics-related use cases aligned with common LLM downstream applications in embodied AI, and lacks analysis of robustness to adversarial attacks targeting the logit-level fusion mechanism.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14302v1)
- **👥 Authors**: Chunlin Tian, Kahou Tam, Yebo Wu, Shuaihang Zhong, Li Li, Nicholas D. Lane, Chengzhong Xu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 DeepFusion: Accelerating MoE Training via Federated Knowledge Distillation from Heterogeneous Edge Devices (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed DeepFusion scalable federated MoE training framework, which introduces a novel View-Aligned Attention module to resolve the view mismatch problem in cross-architecture federated knowledge distillation between heterogeneous on-device LLMs and the global MoE model, achieving performance close to centralized training while significantly reducing communication costs.
- **⚠️ Limitations**: The work only conducts experiments on NLP MoE LLM tasks in medical and finance domains, fails to explore applicability to other foundation model types such as robotics VLAs or edge robotics deployment scenarios, and lacks analysis of the pipeline's robustness against adversarial attacks in federated settings.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14301v1)
- **👥 Authors**: Songyuan Li, Jia Hu, Ahmed M. Abdelmoniem, Geyong Min, Haojun Huang, Jiwei Huang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Machine Learning as a Tool (MLAT): A Framework for Integrating Statistical ML Models as Callable Tools within LLM Agent Workflows (Score: 2/10)
- **💡 Innovation**: The key novelty is the introduction of the MLAT design pattern that allows LLM agent workflows to dynamically invoke pre-trained statistical ML models as first-class callable tools alongside standard APIs, instead of treating ML inference as a static preprocessing step.
- **⚠️ Limitations**: The work is only validated on a single narrow business use case of proposal generation, with no demonstration of generalizability to robotics or embodied AI domains, and the pricing model is trained on an extremely small dataset of only 70 examples, limiting real-world robustness.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14295v1)
- **👥 Authors**: Edwin Chen, Zulekha Bibi
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 KernelBlaster: Continual Cross-Task CUDA Optimization via Memory-Augmented In-Context Reinforcement Learning (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed Memory-Augmented In-context Reinforcement Learning (MAIC-RL) framework with a retrievable Persistent CUDA Knowledge Base and profile-guided textual-gradient agentic workflow that enhances LLM-based agents' cross-GPU architecture CUDA code optimization performance.
- **⚠️ Limitations**: The work only evaluates on CUDA kernel benchmark datasets, does not demonstrate applicability to any robotics, embodied AI or 3D vision tasks aligned with your stated research interests, and lacks validation of generalizability to other programming or optimization domains.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14293v1)
- **👥 Authors**: Kris Shengjun Dong, Sahil Modi, Dima Nikiforov, Sana Damani, Edward Lin, Siva Kumar Sastry Hari, Christos Kozyrakis
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Whom to Query for What: Adaptive Group Elicitation via Multi-Turn LLM Interactions (Score: 2/10)
- **💡 Innovation**: The key novelty is a theoretically grounded closed-loop adaptive group elicitation framework that combines an LLM-based expected information gain objective for question scoring and heterogeneous graph neural network propagation to adaptively select both questions and respondents under explicit budget constraints, achieving superior population-level response prediction performance over prior methods.
- **⚠️ Limitations**: The work is only evaluated on real-world opinion survey datasets, lacks validation on other potential application domains including robotics or embodied AI tasks, and does not explore performance when dealing with non-text response modalities or highly heterogeneous participant populations.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14279v1)
- **👥 Authors**: Ruomeng Ding, Tianwei Gao, Thomas P. Zollo, Eitan Bachmat, Richard Zemel, Zhun Deng
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 A Rational Analysis of the Effects of Sycophantic AI (Score: 2/10)
- **💡 Innovation**: This work presents a novel rational Bayesian analysis of the epistemic risks of LLM sycophancy, empirically validating via a 557-participant modified Wason 2-4-6 rule discovery task that sycophantic LLM responses suppress truth discovery and inflate user confidence relative to unbiased feedback.
- **⚠️ Limitations**: The study only evaluates sycophancy effects in a narrow controlled rule-discovery setting, does not test impacts in real-world high-stakes use cases, and does not propose concrete mitigation strategies for the identified belief distortion issue.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14270v1)
- **👥 Authors**: Rafael M. Batista, Thomas L. Griffiths
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 AD-Bench: A Real-World, Trajectory-Aware Advertising Analytics Benchmark for LLM Agents (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposal of AD-Bench, the first real-world trajectory-aware advertising analytics benchmark built from actual user marketing analysis requests with domain expert-verified reference answers and tool-call trajectories to evaluate LLM agent performance in specialized multi-round, multi-tool marketing analysis scenarios.
- **⚠️ Limitations**: The benchmark is restricted exclusively to the advertising and marketing domain, does not address any capabilities related to robotics, 3D vision, or other AI subfields aligned with your research interests, and lacks assessment of LLM agent generalizability to other professional domains.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14257v1)
- **👥 Authors**: Lingxiang Hu, Yiding Sun, Tianle Xia, Wenwei Li, Ming Xu, Liqun Liu, Peng Shu, Huan Yu, Jie Jiang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Multi-Agent Debate: A Unified Agentic Framework for Tabular Anomaly Detection (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed MAD multi-agent debating framework that resolves disagreements between heterogeneous tabular anomaly detection models via a mathematically grounded coordination layer with LLM-augmented critics, formal regret guarantees, and conformal calibration for false positive control.
- **⚠️ Limitations**: The work is exclusively validated on tabular anomaly detection benchmarks, with no exploration of generalizability to robotics or embodied AI use cases, and no demonstration of performance on non-tabular data modalities relevant to your stated research interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14251v1)
- **👥 Authors**: Pinqiao Wang, Sheng Li
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Evaluating LLMs in Finance Requires Explicit Bias Consideration (Score: 2/10)
- **💡 Innovation**: This paper identifies five distinct recurring biases specific to financial LLM applications, quantifies the widespread underdiscussion of these biases via a review of 164 papers published between 2023 and 2025, and proposes a Structural Validity Framework and evaluation checklist for bias diagnosis and financial LLM system design.
- **⚠️ Limitations**: The work does not provide empirical validation of the proposed framework's real-world efficacy in reducing bias or improving the reliability of deployed financial LLM systems, nor does it offer concrete, actionable bias mitigation algorithm designs.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.14233v1)
- **👥 Authors**: Yaxuan Kong, Hoyoung Lee, Yoontae Hwang, Alejandro Lopez-Lira, Bradford Levy, Dhagash Mehta, Qingsong Wen, Chanyeol Choi, Yongjae Lee, Stefan Zohren
- **🏷️ Tags**: #LLM #Foundation_Model

---


