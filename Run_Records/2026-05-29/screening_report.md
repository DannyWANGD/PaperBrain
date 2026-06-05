# 2026-05-29 Screening Results

- Provider: `openrouter`
- Providers seen: `openrouter`
- Run modes: `daily`
- Run state: `state.json`
- Papers tracked: 47

| Score | Stage | Source | Forced | Paper ID | Title | Decision | Red Flags |
|---:|---|---|---|---|---|---|---|
| 8.1 | detailed | daily |  | `arxiv:2605.30350` | DynaFLIP: Rethinking Robotics Perception via Tri-Modal-Dynamics Guided Representation | digest, deep, stage2 |  |
| 7.5 | detailed | daily |  | `arxiv:2605.30280` | Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments | digest, deep, stage2 | Abstract lacks explicit baseline comparisons; potential overclaim of unification without clear cross-task transfer evidence., Reproducibility limited by missing full training recipe and data composition details in the excerpt. |
| 7.0 | detailed | daily |  | `arxiv:2605.30346` | YoCausal: How Far is Video Generation from World Model? A Causality Perspective | digest | Limited direct applicability to robot manipulation or VLA tasks; benchmark focuses on passive video generation rather than interactive embodied settings. |
| 6.9 | detailed | daily |  | `arxiv:2605.30347` | NeuROK: Generative 4D Neural Object Kinematics | stage2 | Relevance to direct robot manipulation is indirect; the method generates object dynamics but does not address action-conditioned control or integration with robot simulators., Evaluation details (metrics, baselines, quantitative comparisons) are not provided in the excerpt, limiting assessment of empirical strength. |
| 6.6 | detailed | daily |  | `arxiv:2606.00350` | Drift Q-Learning | stage2 | Limited baseline comparison: only compared to diffusion/flow methods, not to broader offline RL SOTA like CQL, IQL., Degraded data protocol not detailed in excerpt; claims of robustness need more evidence. |
| 6.3 | detailed | daily |  | `arxiv:2606.00382` | CRMA: A Spectrally-Bounded Backbone for Modular Continual Fine-Tuning of LLMs | stage2 | Modest empirical gains; per-task performance varies; abstract oversells consistency of positive backward transfer. |
| 5.6 | detailed | daily |  | `arxiv:2605.30263` | minWM: A Full-Stack Open-Source Framework for Real-Time Interactive Video World Models | stage2 | Pre-print, not peer-reviewed, Limited quantitative evaluation in abstract, Primarily a system contribution, not a novel algorithm |
| 5.2 | detailed | daily |  | `arxiv:2605.30052` | REPOT: Recoverable Program-of-Thought via Checkpoint Repair | stage2 | Limited relevance to robot manipulation and embodied AI; tasks are abstract planning puzzles, not physical actions., Method is a straightforward combination of existing PoT and verification, with modest novelty. |
| 5.0 | coarse_only | daily |  | `arxiv:2605.29271` | CoHyDE: Iterative Co-Training of LLM Rewriter & Dense Encoder for Tool Retrieval | screened |  |
| 5.0 | coarse_only | daily |  | `arxiv:2605.24786` | CONF-KV: Confidence-Aware KV Cache Eviction with Mixed-Precision Storage for Long-Horizon LLM | screened |  |
| 4.9 | coarse_only | daily |  | `arxiv:2605.29157` | Parallax: Parameterized Local Linear Attention for Language Modeling | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2606.00427` | Topology-Aware State Abstraction with Tangle Cores for Markov Decision Processes | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2606.00402` | A Distribution-Free Framework for Rewrite-Based Human-text Detection via Knockoff Filtering | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2605.30010` | EarlyTom: Early Token Compression Completes Fast Video Understanding | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2605.29888` | LaRA: Layer-wise Representation Analysis for Detecting Data Contamination in RL Post-Training | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2605.30076` | UniSteer: Text-Guided Flow Matching in Activation Space for Versatile LLM Steering | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2605.30093` | Geometry Matters: 3D Foundation Priors for Learning Semantic Correspondence | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2605.30349` | AdaState: Self-Evolving Anchors for Streaming Video Generation | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2605.27355` | Alignment Tampering: How Reinforcement Learning from Human Feedback Is Exploited to Optimize Misaligned Biases | screened |  |
| 4.6 | coarse_only | daily |  | `arxiv:2606.00377` | Score-Control for Hallucination Reduction in Diffusion Models | screened |  |
| 4.6 | detailed | daily |  | `arxiv:2606.00374` | Constrained Whole-Body Tracking for Humanoid Robots | stage2 | No quantitative evaluation metrics provided, No comparison to baseline safety methods, Simulation-only experiments without hardware validation, Limited details on experimental setup and training |
| 4.6 | coarse_only | daily |  | `arxiv:2606.00357` | From "Weak" Signals to Strong Models: Preference Delta Aggregation with LoRA Merging | screened |  |
| 4.6 | detailed | daily |  | `arxiv:2605.28424` | Skill0.5: Joint Skill Internalization and Utilization for Out-of-Distribution Generalization in Agentic Reinforcement Learning | stage2 | Mismatch with target interests: text-based agent tasks (ALFWorld, WebShop), not robot manipulation or VLA., Limited empirical evidence in provided excerpt; no quantitative results shown. |
| 4.5 | coarse_only | daily |  | `arxiv:2606.00392` | Detector-Evasive LLM Paraphrasing via Constrained Policy Optimization | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2606.00369` | Quantifying the Salience of Geo-Cultural Values for Pluralistic Safety Alignment | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2605.25378` | CollectionLoRA: Collecting 50 Effects in 1 LoRA via Multi-Teacher On-Policy Distillation | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2605.30332` | Colored Noise Diffusion Sampling | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2605.30219` | When Should Models Change Their Minds? Contextual Belief Management in Large Language Models | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2605.27995` | AsyncTool: Evaluating the Asynchronous Function Calling Capability under Multi-Task Scenarios | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2605.30189` | Token-Level Generalization in LoRA Adapter Backdoors: Attack Characterization and Behavioral Detection | screened |  |
| 4.2 | coarse_only | daily |  | `arxiv:2606.00367` | Reinforcement Learning with Pairwise Preferences in Long-Term Decision Problems | screened |  |
| 4.2 | coarse_only | daily |  | `arxiv:2605.29156` | RUBRIC-ARROW: Alternating Pointwise Rubric Reward Modeling for LLM Post-training in Non-verifiable Domains | screened |  |
| 4.2 | coarse_only | daily |  | `arxiv:2605.29648` | Verifiable Rewards Beyond Math and Code: Lightweight Corpus-Grounded Process Supervision for Factual Question Answering | screened |  |
| 4.1 | coarse_only | daily |  | `arxiv:2605.30248` | GenClaw: Code-Driven Agentic Image Generation | screened |  |
| 4.1 | coarse_only | daily |  | `arxiv:2605.26730` | PRISM: A Multi-Dimensional Benchmark for Evaluating LLM Peer Reviewers | screened |  |
| 4.0 | coarse_only | daily |  | `arxiv:2606.00395` | PR2: Predictive Routing Replay for MoE-Based LLM Reinforcement Learning | screened |  |
| 4.0 | detailed | daily |  | `arxiv:2606.00366` | GLENS: Global Search via Learning from Solver Iterates with Diffusion Models | stage2 | Low relevance to target interests (optimization method, not embodied AI/RL), Limited evaluation details in excerpt, Simple robotics example may not generalize to complex manipulation tasks |
| 4.0 | coarse_only | daily |  | `arxiv:2605.21781` | Reflective Prompt Tuning through Language Model Function-Calling | screened |  |
| 3.7 | coarse_only | daily |  | `arxiv:2605.26029` | CausaLab: A Scalable Environment for Interactive Causal Discovery Toward AI Scientists | screened |  |
| 3.5 | coarse_only | daily |  | `arxiv:2605.30102` | When Cloud Agents Meet Device Agents: Lessons from Hybrid Multi-Agent Systems | screened |  |
| 3.4 | coarse_only | daily |  | `arxiv:2605.29861` | Towards Verifiable Multimodal Deep Research: A Multi-Agent Harness for Interleaved Report Generation | screened |  |
| 3.4 | detailed | daily |  | `arxiv:2605.30268` | PhyGenHOI: Physically-Aware 4D Generation of Dynamic Human-Object Interactions | screened | Low relevance to target robotics/AI interests (graphics-focused 4D generation, not robot manipulation or embodied AI), Insufficient evaluation details in excerpt; no quantitative results or baselines provided, Method description lacks implementation specifics for reproducibility |
| 3.4 | coarse_only | daily |  | `arxiv:2601.07525` | Thinking Before Constraining: A Unified Decoding Framework for Large Language Models | screened |  |
| 3.2 | coarse_only | daily |  | `arxiv:2605.30260` | How LoRA Remembers? A Parametric Memory Law for LLM Finetuning | screened |  |
| 2.9 | coarse_only | daily |  | `arxiv:2605.29257` | ChildVox: A Speech, Audio, and Large Audio-Language Model Benchmark in Understanding and Characterizing Sound across Childhood | screened |  |
| 2.4 | coarse_only | daily |  | `arxiv:2606.00417` | AgentxGCore: Agentic AI for Next-Generation Mobile Core Network | screened |  |
| 1.3 | coarse_only | daily |  | `arxiv:2606.00370` | Agentic Authoring of Interactive Multiview Visualizations in Genomics | screened |  |
