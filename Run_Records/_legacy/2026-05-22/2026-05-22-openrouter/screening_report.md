# 2026-05-22 Screening Results

- Provider: `openrouter`
- Run state: `state.json`
- Papers tracked: 52

| Score | Stage | Paper ID | Title | Decision | Red Flags |
|---:|---|---|---|---|---|
| 7.5 | detailed | `arxiv:2605.24203` | Afford-VLA: Action-Aligned Visual Planning via Internalized Affordance | digest, deep, stage2 | Limited evaluation details in provided excerpt; SOTA claims not substantiated with numbers in the excerpt. |
| 6.8 | detailed | `arxiv:2605.22536` | SpaceDG: Benchmarking Spatial Intelligence under Visual Degradation | digest | Limited relevance to robot manipulation and VLA; benchmark focuses on static spatial reasoning without action or dynamics. |
| 6.7 | detailed | `arxiv:2605.21572` | PhysX-Omni: Unified Simulation-Ready Physical 3D Generation for Rigid, Deformable, and Articulated Objects | digest, stage2 | Limited direct relevance to core VLA/RL methods; primarily a 3D generation and dataset work., Unclear if generated assets are truly simulation-ready without extensive physics validation in downstream simulators. |
| 6.5 | detailed | `arxiv:2605.22718` | WorldKV: Efficient World Memory with World Retrieval and Compression | digest, stage2 | Evaluation limited to synthetic game environments; no direct robot manipulation or real-world embodied tasks., Retrieval mechanism may rely on accurate camera/action correspondence, which could be brittle in noisy real-world settings. |
| 5.7 | detailed | `arxiv:2605.21467` | DelTA: Discriminative Token Credit Assignment for Reinforcement Learning from Verifiable Rewards | screened | The paper focuses on LLM reasoning for math/code tasks, with no evaluation on robot manipulation, VLA, world models, or embodied AI, limiting direct applicability to the target interests., The method's effectiveness in multimodal or embodied settings remains untested. |
| 5.7 | detailed | `arxiv:2605.22138` | Efficient Agentic Reasoning Through Self-Regulated Simulative Planning | digest, stage2 | Evaluation limited to language tasks; no embodied or physical world modeling., Potential overclaim about general agentic reasoning without evidence in robotics or embodied settings., Not directly applicable to robot manipulation or VLA. |
| 5.5 | detailed | `arxiv:2605.18607` | Forecasting Downstream Performance of LLMs With Proxy Metrics | screened | Low relevance to target interests (robot manipulation, VLA, world model, RL, diffusion, embodied AI); paper focuses solely on text-based LLM evaluation without any application to robotics or embodied settings. |
| 5.4 | detailed | `arxiv:2605.10158` | Unsupervised Process Reward Models | screened | Limited relevance to robotics/embodied AI; application domain is math reasoning, not physical interaction., Insufficient details on RL setup for policy optimization in the provided excerpt., Potential missing comparison to recent unsupervised PRM baselines like implicit PRM. |
| 5.1 | detailed | `arxiv:2605.17602` | AutoRubric-T2I: Robust Rule-Based Reward Model for Text-to-Image Alignment | screened | Low relevance to target domains (robot manipulation, embodied AI, VLA, world model) |
| 5.0 | coarse_only | `arxiv:2605.22109` | Perception or Prejudice: Can MLLMs Go Beyond First Impressions of Personality? | screened |  |
| 5.0 | coarse_only | `arxiv:2605.13734` | KVServe: Service-Aware KV Cache Compression for Communication-Efficient Disaggregated LLM Serving | screened |  |
| 5.0 | coarse_only | `arxiv:2605.22074` | From Reasoning Chains to Verifiable Subproblems: Curriculum Reinforcement Learning Enables Credit Assignment for LLM Reasoning | screened |  |
| 4.9 | coarse_only | `arxiv:2605.24248` | Attested Tool-Server Admission: A Security Extension to the Model Context Protocol | screened |  |
| 4.8 | coarse_only | `arxiv:2605.22012` | LatentOmni: Rethinking Omni-Modal Understanding via Unified Audio-Visual Latent Reasoning | screened |  |
| 4.8 | coarse_only | `arxiv:2605.21072` | Q-ARVD: Quantizing Autoregressive Video Diffusion Models | screened |  |
| 4.7 | coarse_only | `arxiv:2605.22791` | Gated DeltaNet-2: Decoupling Erase and Write in Linear Attention | screened |  |
| 4.7 | coarse_only | `arxiv:2605.22717` | Live Music Diffusion Models: Efficient Fine-Tuning and Post-Training of Interactive Diffusion Music Generators | screened |  |
| 4.6 | coarse_only | `arxiv:2605.21850` | ACC: Compiling Agent Trajectories for Long-Context Training | screened |  |
| 4.6 | detailed | `arxiv:2605.22177` | Maestro: Reinforcement Learning to Orchestrate Hierarchical Model-Skill Ensembles | screened | Comparison against monolithic models (GPT-5, Gemini-2.5-Pro) without clarifying if baselines had access to the same skill/tool registry, making the ensemble advantage potentially unfair., Evaluation entirely on multimodal benchmarks (math, charts, perception) with no connection to robot manipulation, VLA, or embodied AI tasks., Limited technical detail in the provided excerpt to fully assess the RL training setup and reward design. |
| 4.6 | detailed | `arxiv:2605.22715` | AnyMo: Geometry-Aware Setup-Agnostic Modeling of Human Motion in the Wild | screened | Mismatch with target research interests: paper focuses on wearable IMU-based human motion sensing and language alignment, not robot manipulation, VLA, world models, or reinforcement learning., Limited applicability to embodied AI as defined by robot learning; the work does not address action generation or robot control. |
| 4.5 | coarse_only | `arxiv:2605.24292` | TUBE: Tangent Upper Bound on Evidence for Discrete Diffusion Language Models | screened |  |
| 4.5 | coarse_only | `arxiv:2605.24217` | Identifying and Mitigating Systemic Measurement Bias in Production LLM Inference Benchmarks | screened |  |
| 4.5 | detailed | `arxiv:2605.22642` | Spreadsheet-RL: Advancing Large Language Model Agents on Realistic Spreadsheet Tasks via Reinforcement Learning | screened | Off-topic for target interests (robotics/embodied AI), Low absolute performance on benchmarks, Limited generalization beyond spreadsheet domain |
| 4.5 | coarse_only | `arxiv:2605.22144` | One Sentence, One Drama: Personalized Short-Form Drama Generation via Multi-Agent Systems | screened |  |
| 4.5 | coarse_only | `arxiv:2605.13163` | LoREnc: Low-Rank Encryption for Securing Foundation Models and LoRA Adapters | screened |  |
| 4.4 | coarse_only | `arxiv:2605.24202` | When Does Multi-Agent RL Improve LLM Workflows? Workflow, Scale, and Policy-Sharing Tradeoffs | screened |  |
| 4.4 | coarse_only | `arxiv:2605.24192` | Filtered Posterior Mean Collections: A Unified Framework for Analytical Models of Diffusion Generalization | screened |  |
| 4.4 | coarse_only | `arxiv:2605.22344` | Bernini: Latent Semantic Planning for Video Diffusion | screened |  |
| 4.4 | coarse_only | `arxiv:2605.22538` | Segment Anything with Motion, Geometry, and Semantic Adaptation for Complex Nonlinear Visual Object Tracking | screened |  |
| 4.3 | coarse_only | `arxiv:2605.24300` | Enhancing Reliability in LLM-Based Secure Code Generation | screened |  |
| 4.3 | detailed | `arxiv:2605.24216` | Agent-ToM: Learning to Monitor Autonomous LLM Agents via Theory-of-Mind Reasoning | screened | Low relevance to target research interests (robot manipulation, VLA, world model, RL, diffusion, embodied AI); paper focuses on LLM agent security monitoring. |
| 4.2 | coarse_only | `arxiv:2605.15669` | Rule2DRC: Benchmarking LLM Agents for DRC Script Synthesis with Execution-Guided Test Generation | screened |  |
| 4.1 | coarse_only | `arxiv:2605.24298` | An Empirical Evaluation of LLM-Generated Code Security Across Prompting Methods | screened |  |
| 4.1 | coarse_only | `arxiv:2605.26144` | VISTA: An End-to-End Benchmark for Visual Spec-to-Web-App Coding Agents | screened |  |
| 4.1 | coarse_only | `arxiv:2605.24180` | Human-AI Collaboration in Science at Scale: A Global Large-scale Randomized Field Experiment | screened |  |
| 4.1 | coarse_only | `arxiv:2605.16928` | Full Attention Strikes Back: Transferring Full Attention into Sparse within Hundred Training Steps | screened |  |
| 4.1 | coarse_only | `arxiv:2605.20910` | FlowLong: Inference-time Long Video Generation via Manifold-constrained Tweedie Matching | screened |  |
| 4.1 | coarse_only | `arxiv:2605.22641` | More Context, Larger Models, or Moral Knowledge? A Systematic Study of Schwartz Value Detection in Political Texts | screened |  |
| 4.0 | coarse_only | `arxiv:2605.24266` | An Interactive Paradigm for Deep Research | screened |  |
| 4.0 | coarse_only | `arxiv:2605.24219` | Beyond Final Answers: Auditing Trajectory-Level Hallucinations in Multi-Agent Industrial Workflows | screened |  |
| 4.0 | coarse_only | `arxiv:2605.21363` | "I didn't Make the Micro Decisions": Measuring, Inducing, and Exposing Goal-Level AI Contributions in Collaboration | screened |  |
| 3.9 | coarse_only | `arxiv:2605.22777` | DecQ: Detail-Condensing Queries for Enhanced Reconstruction and Generation in Representation Autoencoders | screened |  |
| 3.7 | coarse_only | `arxiv:2605.22355` | TransitLM: A Large-Scale Dataset and Benchmark for Map-Free Transit Route Generation | screened |  |
| 3.5 | coarse_only | `arxiv:2605.24211` | Teaching Through Analogies: A Modular Pipeline for Educational Analogy Generation | screened |  |
| 3.4 | coarse_only | `arxiv:2605.20244` | Lean Refactor: Multi-Objective Controllable Proof Optimization via Agentic Strategy Search | screened |  |
| 3.2 | coarse_only | `arxiv:2605.24299` | LLMs Show No Signs Of Individuated Metacognition | screened |  |
| 3.2 | coarse_only | `arxiv:2605.24247` | Improving Labeling Consistency with Detailed Constitutional Definitions and AI-Driven Evaluation | screened |  |
| 2.5 | coarse_only | `arxiv:2605.24296` | When Does Synthetic Patent Data Help? Volume-Fidelity Trade-offs in Low-Resource Multi-Label Classification | screened |  |
| 2.3 | coarse_only | `arxiv:2605.24238` | Toward Enactive Artificial Intelligence | screened |  |
| 1.5 | coarse_only | `arxiv:2605.26146` | Augment Engineering: A Methodology for Multi-Tool AI Orchestration Across Professional Domains | screened |  |
| 1.0 | coarse_only | `arxiv:2605.24294` | Concept Drift Adaptation Using Self-Supervised and Reinforcement Learning In Android Malware Detection | screened |  |
| 1.0 | coarse_only | `arxiv:2605.20176` | ClinSeekAgent: Automating Multimodal Evidence Seeking for Agentic Clinical Reasoning | screened |  |
