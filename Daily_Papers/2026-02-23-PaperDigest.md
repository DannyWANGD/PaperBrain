# 📅 2026-02-23 - Paper Digest
## Summary
Total Papers: 23 | High Impact: 2

## 📝 Papers List
### ✨ QuantVLA: Scale-Calibrated Post-Training Quantization for Vision-Language-Action Models (Score: 7/10)
- **💡 Innovation**: The key novelty is the first training-free post-training quantization framework for Vision-Language-Action models that successfully quantizes diffusion transformer action heads via three scale-calibrated components, outperforming full-precision baselines while delivering significant memory savings and inference speedup for practical VLA deployment.
- **⚠️ Limitations**: The work only evaluates its performance on the simulated LIBERO benchmark, lacks validation on real-world robot manipulation tasks, does not test compatibility with a wider range of VLA backbones, and does not explore performance of more aggressive low-bit quantization settings like 2-bit or 3-bit.
- **🔗 Link**: [[QuantVLA]]
- **👥 Authors**: Jingxuan Zhang, Yunta Hsieh, Zhongwei Wan, Haokun Lin, Xin Wang, Ziqi Wang, Yingtie Lei, Mi Zhang
- **🏷️ Tags**: #VLA #Post_Training_Quantization #Diffusion_Transformer #Embodied_AI #Foundation_Models

---

### ✨ Generated Reality: Human-centric World Simulation using Interactive Video Generation with Hand and Camera Control (Score: 7/10)
- **💡 Innovation**: The key novelty is a human-centric video world model conditioned on tracked 3D head pose and joint-level hand poses, paired with an optimized diffusion transformer conditioning mechanism that is distilled into a low-latency causal interactive system for generating controllable egocentric virtual environments.
- **⚠️ Limitations**: The work does not evaluate applicability to robotics use cases such as sim2real transfer or robot manipulation, lacks integration with 3D/4D Gaussian Splatting for improved 3D consistency, and does not leverage foundation models like LLMs or VLAs for semantic action control.
- **🔗 Link**: [[Generated_Reality]]
- **👥 Authors**: Linxi Xie, Lisong C. Sun, Ashley Neall, Tong Wu, Shengqu Cai, Gordon Wetzstein
- **🏷️ Tags**: #World_Model #Diffusion_Transformer #Video_Diffusion_Model #Embodied_AI #Interactive_Video_Generation

---

### ✨ Diffusion Modulation via Environment Mechanism Modeling for Planning (Score: 6/10)
- **💡 Innovation**: The key novelty is the proposed DMEMM framework that modulates diffusion model training for offline reinforcement learning planning by incorporating environment transition dynamics and reward function constraints to reduce discrepancies between generated trajectories and real-world environment mechanisms.
- **⚠️ Limitations**: The work lacks validation on embodied AI or real robot manipulation tasks, and does not integrate or evaluate against relevant related advances such as world models, 3D/4D Gaussian splatting, or vision-language-action foundation models that are widely used in modern robotics planning pipelines.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.20422v1)
- **👥 Authors**: Hanping Zhang, Yuhong Guo
- **🏷️ Tags**: #Diffusion_Models #Offline_Reinforcement_Learning #Trajectory_Planning #Environment_Dynamics_Modeling

---

### 📄 Generalizing from References using a Multi-Task Reference and Goal-Driven RL Framework (Score: 4/10)
- **💡 Innovation**: The key novelty is a unified multi-task reinforcement learning framework that co-optimizes a reference-guided imitation task (without feeding references as policy inputs) and a goal-conditioned generalization task to acquire human-like, adaptable humanoid motor skills without requiring adversarial objectives, explicit trajectory tracking or phase variables.
- **⚠️ Limitations**: The work only evaluates on simulated box parkour tasks, lacks real robot or sim2real transfer testing, does not integrate with foundation models, VLAs or modern 3D scene representations that are core to your stated interests, and does not validate performance on robot manipulation or other common embodied AI tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.20375v1)
- **👥 Authors**: Jiashun Wang, M. Eva Mungai, He Li, Jean Pierre Sleiman, Jessica Hodgins, Farbod Farshidian
- **🏷️ Tags**: #Reinforcement_Learning #Multi_Task_RL #Goal_Conditioned_RL #Humanoid_Robot_Control #Motion_Imitation

---

### 📄 Aesthetic Camera Viewpoint Suggestion with 3D Aesthetic Field (Score: 4/10)
- **💡 Innovation**: The key novelty is the introduction of a 3D aesthetic field learned via a feedforward 3D Gaussian Splatting network that distills knowledge from pretrained 2D aesthetic models, paired with an efficient two-stage coarse-to-fine viewpoint search pipeline that eliminates the need for costly reinforcement learning exploration or dense 3D scene captures.
- **⚠️ Limitations**: The work does not explore integration with embodied AI or robotic perception pipelines, lacks support for semantic or user-customized aesthetic preferences that could be enabled via foundation models or LLMs, and is only validated on static scene viewpoint suggestion tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.20363v1)
- **👥 Authors**: Sheyang Tang, Armin Shafiee Sarvestani, Jialu Xu, Xiaoyu Xu, Zhou Wang
- **🏷️ Tags**: #3D_Gaussian_Splatting #Aesthetic_Viewpoint_Suggestion #Knowledge_Distillation #Gradient_Based_View_Optimization

---

### 📄 Large-scale Photorealistic Outdoor 3D Scene Reconstruction from UAV Imagery Using Gaussian Splatting Techniques (Score: 4/10)
- **💡 Innovation**: The key novelty is an end-to-end low-latency pipeline that integrates live UAV RTMP video streaming, synchronized sensor fusion, camera pose estimation, and 3D Gaussian Splatting optimization to enable real-time large-scale outdoor 3D scene reconstruction compatible with AR/VR interactive visualization.
- **⚠️ Limitations**: The work lacks comparison against existing 3D Gaussian Splatting-based reconstruction pipelines, does not explore downstream applications of the reconstructed scenes for robotics or embodied AI tasks, and provides no ablation analysis of individual pipeline components' impact on latency and reconstruction quality.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.20342v1)
- **👥 Authors**: Christos Maikos, Georgios Angelidis, Georgios Th. Papadopoulos
- **🏷️ Tags**: #3D_Gaussian_Splatting #UAV_3D_Reconstruction #Real_Time_Neural_Rendering #Sensor_Fusion #AR_VR_Visualization

---

### 📄 Learning Smooth Time-Varying Linear Policies with an Action Jacobian Penalty (Score: 4/10)
- **💡 Innovation**: The key novelty is the proposed Linear Policy Net (LPN) architecture that reduces the computational overhead of applying an action Jacobian penalty for smooth reinforcement learning policy learning, eliminating the need for task-specific tuning of action smoothness terms while improving training convergence and inference efficiency.
- **⚠️ Limitations**: The work is only evaluated on motion imitation and quadruped robot control tasks, does not integrate with or compare against methods based on foundation models, diffusion models, or modern embodied perception pipelines, and does not analyze generalization to unseen real-world environments beyond the tested quadruped setup.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.18312)
- **👥 Authors**: Zhaoming Xie, Kevin Karol, Jessica Hodgins
- **🏷️ Tags**: #Reinforcement_Learning #Sim2Real #Robot_Manipulation #Policy_Regularization #Linear_Policy_Net

---

### 📄 Cross domain Persistent Monitoring for Hybrid Aerial Underwater Vehicles (Score: 3/10)
- **💡 Innovation**: The key novelty is a unified deep reinforcement learning framework combined with transfer learning that processes aerial lidar and underwater sonar data to enable cross-domain adaptive persistent monitoring for hybrid aerial-underwater vehicles.
- **⚠️ Limitations**: The work lacks real-world hardware validation, does not compare against state-of-the-art cross-domain robot control baselines, and does not explore integration with relevant advanced methods such as foundation models or sim2real transfer to further boost cross-domain performance.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.21259v1)
- **👥 Authors**: Ricardo B. Grando, Victor A. Kich, Alisson H. Kolling, Junior C. D. Jesus, Rodrigo S. Guerra, Paulo L. J. Drews-Jr
- **🏷️ Tags**: #Deep_Reinforcement_Learning #Transfer_Learning #Cross_Domain_Adaptation #Hybrid_Aerial_Underwater_Vehicle #Autonomous_Persistent_Monitoring

---

### 📄 Does Your Reasoning Model Implicitly Know When to Stop Thinking? (Score: 3/10)
- **💡 Innovation**: The key novelty is the empirical discovery that large reasoning models implicitly know the optimal time to terminate reasoning chains, and the proposal of the SAGE sampling paradigm and SAGE-RL integration to improve both reasoning accuracy and efficiency across mathematical reasoning benchmarks.
- **⚠️ Limitations**: The work is only validated on mathematical reasoning tasks, with no exploration of applicability to embodied AI, robotics, or other downstream use cases relevant to your interests, and does not address integration with other foundation model paradigms like VLAs or world models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.08354)
- **👥 Authors**: Zixuan Huang, Xin Xia, Yuxi Ren, Jianbin Zheng, Xuanda Wang, Zhixia Zhang, Hongyan Xie, Songshi Liang, Zehao Chen, Xuefeng Xiao, Fuzhen Zhuang, Jianxin Li, Yikun Ban, Deqing Wang
- **🏷️ Tags**: #Chain_of_Thought #Reinforcement_Learning #Large_Language_Models #Efficient_Reasoning

---

### 📄 Learning to Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use (Score: 2/10)
- **💡 Innovation**: The key novelty is Trace-Free+, a curriculum learning framework that progressively transfers supervision from trace-rich to trace-free deployment settings for LLM-agent tool interface optimization without requiring execution traces, paired with a large-scale high-quality curated tool interface dataset that supports generalization to unseen tools.
- **⚠️ Limitations**: The work is only evaluated on text-only tool use benchmarks, does not test applicability to embodied AI, robot manipulation, or vision-language agent tool use cases, and does not explore integration with robotics-related pipelines such as Sim2Real or 3D perception models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.20426v1)
- **👥 Authors**: Ruocheng Guo, Kaiwen Dong, Xiang Gao, Kamalika Das
- **🏷️ Tags**: #LLM_Agents #Curriculum_Learning #Tool_Interface_Optimization #Trace_Free_Learning

---

### 📄 gQIR: Generative Quanta Image Reconstruction (Score: 2/10)
- **💡 Innovation**: The key novelty is adapting pre-trained large text-to-image latent diffusion models with custom mechanisms for Bernoulli photon statistics and burst-level spatio-temporal reasoning to recover high-fidelity, photometrically accurate images from sparse, noisy binary single-photon (SPAD) quanta burst frames.
- **⚠️ Limitations**: The work does not address real-time inference requirements for edge deployment, nor does it explore integration with downstream perception tasks for robotics or embodied AI systems, and may introduce semantic hallucinations for rare content not present in the pre-trained diffusion model's training data.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.20417v1)
- **👥 Authors**: Aryan Garg, Sizhuo Ma, Mohit Gupta
- **🏷️ Tags**: #Latent_Diffusion_Models #Computational_Imaging #Single_Photon_Imaging #Generative_Image_Reconstruction #Foundation_Models

---

### 📄 Examining and Addressing Barriers to Diversity in LLM-Generated Ideas (Score: 2/10)
- **💡 Innovation**: This work identifies two distinct cognitive mechanisms (individual-level generation fixation and collective-level lack of knowledge partitioning) that reduce diversity in LLM-generated ideas, and demonstrates that combining Chain-of-Thought prompting and ordinary persona prompting can boost idea diversity to outperform human ideation.
- **⚠️ Limitations**: The study only evaluates general text ideation tasks, does not assess tradeoffs between improved diversity and idea quality/real-world feasibility, and does not explore applications of the proposed prompting strategies to robotics or embodied AI use cases.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.20408v1)
- **👥 Authors**: Yuting Deng, Melanie Brucks, Olivier Toubia
- **🏷️ Tags**: #LLM #Chain_of_Thought_Prompting #Persona_Prompting #Ideation_Diversity

---

### 📄 Case-Aware LLM-as-a-Judge Evaluation for Enterprise-Scale RAG Systems (Score: 2/10)
- **💡 Innovation**: The key novelty is a case-aware LLM-as-a-Judge evaluation framework with eight operationally grounded metrics and a severity-aware scoring protocol tailored for multi-turn enterprise RAG systems, addressing gaps in existing single-turn benchmark-focused evaluation methods that fail to capture enterprise-specific failure modes.
- **⚠️ Limitations**: The work only validates the framework on enterprise RAG use cases, does not test its generalizability to other conversational LLM application scenarios, and lacks head-to-head comparison against other state-of-the-art multi-turn LLM-as-a-Judge evaluation pipelines.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.20379v1)
- **👥 Authors**: Mukul Chhabra, Luigi Medrano, Arush Verma
- **🏷️ Tags**: #LLM #LLM_as_a_Judge #Retrieval_Augmented_Generation #Multi_Turn_Conversation #RAG_Evaluation

---

### 📄 DMCD: Semantic-Statistical Framework for Causal Discovery (Score: 2/10)
- **💡 Innovation**: The key novelty is a two-phase causal discovery framework that first leverages LLMs to generate a semantically informed sparse draft directed acyclic graph from variable metadata, then refines the draft via conditional independence testing to produce accurate causal structures.
- **⚠️ Limitations**: The paper does not evaluate performance on low-metadata or unstructured variable datasets, nor does it explore applications of the proposed causal discovery method to robotics, embodied AI or other domains aligned with your stated research interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.20333v1)
- **👥 Authors**: Samarth KaPatel, Sofia Nikiforova, Giacinto Paolo Saggese, Paul Smith
- **🏷️ Tags**: #Causal_Discovery #Large_Language_Models #Semantic_Priors #Statistical_Causal_Validation

---

### 📄 No One Size Fits All: QueryBandits for Hallucination Mitigation (Score: 2/10)
- **💡 Innovation**: The key novelty is QueryBandits, a model-agnostic online contextual bandit framework that adaptively selects optimal query rewrite strategies to mitigate LLM hallucinations, supporting closed-source models without requiring retraining or gradient-based adaptation.
- **⚠️ Limitations**: The work is only evaluated on standard QA scenarios, with no exploration of its applicability to embodied AI, robot manipulation, or other relevant domains in your research interests, nor does it test integration with vision-language-action models or other robotics-focused foundation models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.20332v1)
- **👥 Authors**: Nicole Cho, William Watson, Alec Koppel, Sumitra Ganesh, Manuela Veloso
- **🏷️ Tags**: #LLM #Hallucination_Mitigation #Contextual_Bandits #Query_Rewriting

---

### 📄 In-context Pre-trained Time-Series Foundation Models adapt to Unseen Tasks (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed In-Context Time-series Pre-training (ICTP) framework that restructures pre-training data to endow time-series foundation models with in-context learning capabilities, enabling zero-shot adaptation to unseen time-series tasks without requiring fine-tuning.
- **⚠️ Limitations**: The work only evaluates performance on general time-series tasks, lacks analysis of the inference computational overhead of its in-context learning mechanism, and does not explore applicability to domain-specific time series such as robot perception or control data relevant to your research interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.20307v1)
- **👥 Authors**: Shangqing Xu, Harshavardhan Kamarthi, Haoxin Liu, B. Aditya Prakash
- **🏷️ Tags**: #Time_Series_Foundation_Models #In_Context_Learning #Zero_Shot_Task_Adaptation #Foundation_Models

---

### 📄 VESPO: Variational Sequence-Level Soft Policy Optimization for Stable Off-Policy LLM Training (Score: 2/10)
- **💡 Innovation**: The key novelty is a theoretically grounded variational sequence-level soft policy optimization framework that derives a closed-form reshaping kernel for sequence-level importance weights to reduce variance and enable stable off-policy LLM training even under high staleness ratios without length normalization.
- **⚠️ Limitations**: This work is only evaluated on mathematical reasoning LLM benchmarks, does not explore applicability to robotics, embodied AI, or other domains matching your research interests, and lacks comparisons to the full range of state-of-the-art off-policy LLM alignment methods.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.10693)
- **👥 Authors**: Guobin Shen, Chenxiao Zhao, Xiang Cheng, Lei Huang, Xing Yu
- **🏷️ Tags**: #Reinforcement_Learning #Large_Language_Models #Off_Policy_Training #Sequence_Level_Policy_Optimization #LLM_Training

---

### 📄 DeepVision-103K: A Visually Diverse, Broad-Coverage, and Verifiable Mathematical Dataset for Multimodal Reasoning (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposal of DeepVision-103K, a large-scale, visually diverse K12 mathematical multimodal dataset specifically designed for Reinforcement Learning with Verifiable Rewards (RLVR) training to boost the visual perception and reasoning capabilities of large multimodal models.
- **⚠️ Limitations**: The work only validates the dataset's effectiveness on multimodal mathematical and general reasoning tasks, does not explore its potential applications in robotics, embodied AI or other related domains, and lacks ablation studies to disentangle the contribution of different dataset characteristics to observed model performance gains.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.16742)
- **👥 Authors**: Haoxiang Sun, Lizhen Xu, Bing Zhao, Wotao Yin, Wei Wang, Boyu Yang, Rui Wang, Hu Wei
- **🏷️ Tags**: #Reinforcement_Learning #Large_Multimodal_Models #Multimodal_Reasoning #RLVR #Mathematical_Dataset

---

### 📄 Sink-Aware Pruning for Diffusion Language Models (Score: 2/10)
- **💡 Innovation**: The key novelty is discovering that attention sinks are transient and less structurally essential in diffusion language models (DLMs) compared to autoregressive LLMs, and proposing a retraining-free sink-aware pruning method that removes unstable sinks to achieve a better quality-efficiency tradeoff than prior DLM pruning baselines.
- **⚠️ Limitations**: The paper only evaluates the proposed method on diffusion language models, with no exploration of its applicability to other diffusion variants (e.g., vision, 3D diffusion) or robotics/embodied AI foundation model pipelines, nor validation on long-context generation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.17664)
- **👥 Authors**: Aidar Myrzakhan, Tianyi Li, Bowei Guo, Shengkun Tang, Zhiqiang Shen
- **🏷️ Tags**: #Diffusion_Language_Models #LLM_Pruning #Attention_Sink #Inference_Efficiency

---

### 📄 Rubrics as an Attack Surface: Stealthy Preference Drift in LLM Judges (Score: 2/10)
- **💡 Innovation**: The key novelty is the identification and empirical demonstration of Rubric-Induced Preference Drift (RIPD), a previously unrecognized vulnerability where seemingly benign, benchmark-compliant rubric edits can cause systematic, exploitable preference shifts in LLM judges that propagate to downstream aligned model policies.
- **⚠️ Limitations**: The work does not propose concrete mitigation strategies for RIPD, nor does it evaluate the presence of this vulnerability in LLM use cases outside of LLM alignment judge pipelines such as embodied AI task planning or vision-language action model evaluation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.13576)
- **👥 Authors**: Ruomeng Ding, Yifei Pang, He Sun, Yizhong Wang, Zhiwei Steven Wu, Zhun Deng
- **🏷️ Tags**: #LLM #LLM_Alignment #LLM_Judge #Preference_Attack #Alignment_Risk

---

### 📄 ReIn: Conversational Error Recovery with Reasoning Inception (Score: 2/10)
- **💡 Innovation**: The key novelty is Reasoning Inception (ReIn), a test-time intervention method that injects external error detection results and generated recovery plans into LLM-based conversational agents' internal reasoning flow to improve error resilience without modifying model parameters or system prompts.
- **⚠️ Limitations**: The work only evaluates performance on predefined text-only conversational error scenarios, lacks validation on cross-modal, embodied or robotics use cases, and does not address recovery from unforeseen, non-predefined error types.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.17022)
- **👥 Authors**: Takyoung Kim, Jinseok Nam, Chandrayee Basu, Xing Fan, Chengyuan Ma, Heng Ji, Gokhan Tur, Dilek Hakkani-Tür
- **🏷️ Tags**: #LLM #Test_Time_Intervention #Conversational_Agent #Error_Recovery

---

### 📄 Whom to Query for What: Adaptive Group Elicitation via Multi-Turn LLM Interactions (Score: 2/10)
- **💡 Innovation**: The key novelty is a theoretically grounded closed-loop adaptive group elicitation framework that jointly optimizes question selection via LLM-based expected information gain scoring and respondent selection via heterogeneous graph neural network response imputation under explicit query and participation budgets.
- **⚠️ Limitations**: The work is only validated on static real-world opinion survey datasets, with no exploration of applicability to dynamic domains, non-opinion elicitation tasks, or robotics/embodied AI use cases, and does not test performance robustness across different LLM backbones for the information gain scoring module.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.14279)
- **👥 Authors**: Ruomeng Ding, Tianwei Gao, Thomas P. Zollo, Eitan Bachmat, Richard Zemel, Zhun Deng
- **🏷️ Tags**: #LLM #Heterogeneous_Graph_Neural_Networks #Expected_Information_Gain #Adaptive_Group_Elicitation

---

### 📄 CrossLLM-Mamba: Multimodal State Space Fusion of LLMs for RNA Interaction Prediction (Score: 1/10)
- **💡 Innovation**: The key novelty is the CrossLLM-Mamba framework that reformulates multi-modal biological interaction prediction as a state-space alignment problem, leveraging bidirectional Mamba encoders to enable dynamic cross-modality embedding crosstalk with linear computational complexity, outperforming existing static fusion approaches for BioLLM embeddings.
- **⚠️ Limitations**: This work does not explore the generalizability of its proposed state-space fusion paradigm to non-biological multi-modal LLM tasks, and lacks detailed ablation studies to disentangle the separate performance contributions of Gaussian noise injection and Focal Loss.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.22236v1)
- **👥 Authors**: Rabeya Tus Sadia, Qiang Ye, Qiang Cheng
- **🏷️ Tags**: #Bio_LLM #State_Space_Model #Multimodal_LLM_Fusion #RNA_Interaction_Prediction #Focal_Loss

---


