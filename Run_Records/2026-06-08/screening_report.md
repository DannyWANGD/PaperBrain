# 2026-06-08 Screening Results

- Provider: `openrouter`
- Providers seen: `openrouter`
- Run modes: `daily`
- Run state: `state.json`
- Papers tracked: 47

| Score | Stage | Source | Forced | Paper ID | Title | Decision | Red Flags |
|---:|---|---|---|---|---|---|---|
| 7.2 | detailed | daily |  | `arxiv:2606.07895` | TBD-VLA: Temporal Block Diffusion Vision Language Action Model | digest, stage2 | Missing quantitative results in excerpt; claims of SOTA unsupported by provided evidence., No baselines or metrics listed in the provided material. |
| 6.8 | detailed | daily |  | `arxiv:2606.06891` | Stream3D-VLM: Online 3D Spatial Understanding with Incremental Geometry Priors | digest | Potential overclaim on real-time capability without explicit latency benchmarks in the provided excerpt. |
| 6.7 | detailed | daily |  | `arxiv:2606.09669` | SpatialWorld: Benchmarking Interactive Spatial Reasoning of Multimodal Agents in Real-World Tasks | digest, stage2 | Limited relevance to robot manipulation and VLA due to text-based high-level actions; benchmark does not include low-level control or continuous action spaces., As an evaluation benchmark, it does not directly contribute new methods for manipulation, world models, or reinforcement learning. |
| 6.2 | detailed | daily |  | `arxiv:2606.07326` | AnchorWorld: Embodied Egocentric World Simulation with View-based Evolution Customization | digest, stage2 | Limited quantitative evidence in provided excerpt; relevance to manipulation/VLA is indirect. |
| 6.2 | detailed | daily |  | `arxiv:2606.06361` | Physics in 2-Steps: Locking Motion Priors Before Visual Refinement Erases Them | digest | Limited direct applicability to robot manipulation or VLA tasks; focuses on video generation physical consistency., Evaluation on physical consistency may not translate to improved downstream task performance in embodied AI. |
| 5.9 | detailed | daily |  | `arxiv:2606.09646` | Do Video Foundation Models Understand Intuitive Physics? A Layerwise Probing Analysis | screened | Limited direct applicability to robot manipulation or VLA; primarily a video understanding analysis. |
| 5.8 | detailed | daily |  | `arxiv:2606.09630` | ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies | stage2 | Limited baseline comparison (only fine-tuned VLA mentioned, no explicit recovery or RL baselines), Evaluation details sparse (number of tasks, trials, variance not reported in excerpt), Zero-shot sim-to-real claim lacks domain randomization or transfer method details, Reproducibility hindered by missing reward library and compilation specifics |
| 5.6 | detailed | daily |  | `arxiv:2606.09572` | CT-VAM: A Cerebello-Thalamic-Inspired Vision-Action Model for Efficient Visuomotor Control | stage2 | No quantitative results provided in excerpt; claims of competitiveness with larger VLA models unverified., Cloud-edge paradigm not demonstrated as high-level decision module is absent. |
| 5.1 | detailed | daily |  | `arxiv:2606.05152` | Reinforcement Learning from Rich Feedback with Distributional DAgger | screened | Relevance mismatch: paper focuses on LLM reasoning tasks, not robot manipulation, VLA, world model, or embodied AI as required by target interests. |
| 4.8 | coarse_only | daily |  | `arxiv:2606.09640` | Physics-Aware Sparse Learning and Selective Online Adaptation for Euler-Lagrange Robot Dynamics | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2606.05806` | When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents | screened |  |
| 4.7 | coarse_only | daily |  | `arxiv:2606.07591` | ResearchClawBench: A Benchmark for End-to-End Autonomous Scientific Research | screened |  |
| 4.6 | coarse_only | daily |  | `arxiv:2606.06622` | UnpredictaBench: A Benchmark for Evaluating Distributional Randomness in LLMs | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2606.09664` | In-Context Learning for Latent Space Bayesian Optimization | screened |  |
| 4.5 | detailed | daily |  | `arxiv:2606.09605` | Next-Token Prediction Learns Generalisable Representations of Sleep Physiology | screened | Domain mismatch: paper focuses on sleep physiology and healthcare, not robotics or embodied AI. |
| 4.5 | coarse_only | daily |  | `arxiv:2606.07412` | Socratic-SWE: Self-Evolving Coding Agents via Trace-Derived Agent Skills | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2606.06538` | WorldBench: A Challenging and Visually Diverse Multimodal Reasoning Benchmark | screened |  |
| 4.4 | coarse_only | daily |  | `arxiv:2606.09549` | SecureClaw: Clawing Back Control of LLM Agents | screened |  |
| 4.4 | coarse_only | daily |  | `arxiv:2605.26046` | When Gradients Collide: Failure Modes of Multi-Objective Prompt Optimization for LLM Judges | screened |  |
| 4.4 | coarse_only | daily |  | `arxiv:2603.16142` | Parametric Social Identity Injection and Diversification in Public Opinion Simulation | screened |  |
| 4.3 | detailed | daily |  | `arxiv:2606.06556` | Robots Need More than VLA and World Models | screened | No empirical validation, Lacks concrete technical contribution, Position paper without systematic survey methodology |
| 4.3 | detailed | daily |  | `arxiv:2606.06741` | OpenSkill: Open-World Self-Evolution for LLM Agents | screened | Low relevance to robotics/embodied AI interests; paper focuses on LLM agents without physical embodiment., Insufficient evaluation details in excerpt to assess methodological rigor and benchmark specifics. |
| 4.3 | coarse_only | daily |  | `arxiv:2603.20990` | ECI_{sem}: Semantic Residual Effective Contrastive Information for Evaluating Hard Negatives | screened |  |
| 4.2 | coarse_only | daily |  | `arxiv:2606.04525` | GENEB: Why Genomic Models Are Hard to Compare | screened |  |
| 4.2 | coarse_only | daily |  | `arxiv:2606.05972` | LLM Explainability with Counterfactual Chains and Causal Graphs | screened |  |
| 4.1 | coarse_only | daily |  | `arxiv:2606.07502` | Your UnEmbedding Matrix is Secretly a Feature Lens for Text Embeddings | screened |  |
| 4.0 | coarse_only | daily |  | `arxiv:2606.09585` | Optical Reasoning: Rethinking Images as an Expressive Reasoning Medium Beyond Text | screened |  |
| 4.0 | coarse_only | daily |  | `arxiv:2606.09559` | Safe-RULE: Safe Reinforcement UnLEarning | screened |  |
| 4.0 | coarse_only | daily |  | `arxiv:2605.29430` | Towards Human-Like Interactive Speech Recognition With Agentic Correction and Semantic Evaluation | screened |  |
| 3.9 | coarse_only | daily |  | `arxiv:2606.09658` | Muon Learns More Robust and Transferable Features than Adam | screened |  |
| 3.9 | coarse_only | daily |  | `arxiv:2606.09644` | Where Does the Answer Come From? Benchmarking View-Level Visual Evidence Identification in Multi-View MLLMs for Autonomous Driving | screened |  |
| 3.9 | coarse_only | daily |  | `arxiv:2606.09610` | Shape Formation for the Cooperative Transportation of Arbitrary Objects Using Multi-Agent Reinforcement Learning | screened |  |
| 3.9 | coarse_only | daily |  | `arxiv:2606.09563` | PRISM: Recovering Instruction Sets from Language Model Activations | screened |  |
| 3.9 | coarse_only | daily |  | `arxiv:2606.09551` | FuseFSS: Efficient Secure LLM Inference with Function Secret Sharing | screened |  |
| 3.8 | coarse_only | daily |  | `arxiv:2606.05563` | SoCRATES: Towards Reliable Automated Evaluation of Proactive LLM Mediation across Domains and Socio-cognitive Variations | screened |  |
| 3.8 | coarse_only | daily |  | `arxiv:2606.06843` | Empirical Study on the Characteristics and Evolution of AI-usage in GitHub Repositories: Evidence from Code Comments | screened |  |
| 3.6 | coarse_only | daily |  | `arxiv:2606.01779` | HarnessForge: Joint Harness and Policy Evolution for Adaptive Agent Systems | screened |  |
| 3.5 | coarse_only | daily |  | `arxiv:2606.06880` | Towards Retrieving Interaction Spaces for Agentic Search | screened |  |
| 3.4 | coarse_only | daily |  | `arxiv:2606.09674` | (Auto)formalization is supposed to be easy: Trellis process semantics for spelling out rigorous proofs | screened |  |
| 3.2 | coarse_only | daily |  | `arxiv:2606.09578` | TABVERSE: Benchmarking Cross-Format Table Understanding in LLMs and VLMs | screened |  |
| 3.2 | coarse_only | daily |  | `arxiv:2606.09577` | Code Is More Than Text: Uncertainty Estimation for Code Generation | screened |  |
| 2.5 | coarse_only | daily |  | `arxiv:2606.09643` | FMplex: Model Virtualization for Serving Extensible Foundation Models | screened |  |
| 2.1 | coarse_only | daily |  | `arxiv:2606.04291` | A Cookbook of 3D Vision: Data, Learning Paradigms, and Application | screened |  |
| 1.8 | coarse_only | daily |  | `arxiv:2606.09613` | AGENTSERVESIM: A Hardware-aware Simulator for Multi-Turn LLM Agent Serving | screened |  |
| 1.8 | coarse_only | daily |  | `arxiv:2606.07433` | Watch, Remember, Reason: Human-View Video Understanding with MLLMs | screened |  |
| 1.3 | coarse_only | daily |  | `arxiv:2606.09556` | AI Scientists Are Only as Good as Their Evidence: A Stratified Ablation of Proprietary Data and Reasoning Skills in Drug-Asset Valuation | screened |  |
| 1.0 | coarse_only | daily |  | `arxiv:2606.09558` | Integrating gene regulatory priors into Transformer attention with scTransformer for interpretable scRNA-seq analysis | screened |  |
