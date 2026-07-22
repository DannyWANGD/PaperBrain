# 2026-06-09 Screening Results

- Provider: `openrouter`
- Providers seen: `openrouter`
- Run modes: `daily`
- Run state: `state.json`
- Papers tracked: 52

| Score | Stage | Source | Forced | Paper ID | Title | Decision | Red Flags |
|---:|---|---|---|---|---|---|---|
| 8.2 | detailed | daily |  | `arxiv:2606.11408` | Dynamic Execution Horizon Prediction for Chunk-based Robot Policies | digest, deep, stage2 |  |
| 7.5 | detailed | daily |  | `arxiv:2606.08242` | Light-WAM: Efficient World Action Models with State-Fusion Action Decoding | digest, deep, stage2 |  |
| 7.3 | detailed | daily |  | `arxiv:2606.09811` | AHA-WAM:Asynchronous Horizon-Adaptive World-Action Modeling with Observation-Guided Context Routing | digest, stage2 | Limited real-world evaluation (4 tasks) may not fully demonstrate generalization., No ablation studies visible in excerpt to isolate contributions of asynchronous design, memory, and routing. |
| 7.2 | detailed | daily |  | `arxiv:2606.11396` | PLUME: Probabilistic Latent Unified World Modeling and Parameter Estimation for Multi-Finger Manipulation | digest, stage2 | Hardware validation limited to a single screwdriver turning task, limiting evidence of broad sim-to-real generalization., Reliance on simulation data with known parameter values for training may restrict applicability to scenarios where such data is unavailable. |
| 7.1 | detailed | daily |  | `arxiv:2606.07723` | VoLo: A Physical Orchestrator for Open-Vocabulary Long-Horizon Manipulation | digest, stage2 | Limited real-robot validation details in excerpt, Benchmark availability unclear |
| 6.5 | detailed | daily |  | `arxiv:2606.09828` | Latent Spatial Memory for Video World Models | stage2 | Evaluation limited to static scene datasets (RealEstate10K, WorldScore), unclear applicability to dynamic manipulation tasks., Reliance on depth estimation may introduce errors in complex or occluded scenes. |
| 6.3 | detailed | daily |  | `arxiv:2606.11431` | Mirror Descent Beyond Euclidean Stability: An Exponential Separation in Initialization Sensitivity | stage2 | No empirical validation on RL or LLM tasks, Limited direct relevance to robot manipulation, VLA, world model, diffusion model, embodied AI |
| 6.3 | detailed | daily |  | `arxiv:2606.07217` | Robotic Policy Adaptation via Weight-Space Meta-Learning | stage2 | Real-robot evaluation lacks quantitative metrics and only reports consistent improvement without numbers., Relative improvements (up to ~14x) may be inflated by very low baseline success rates; absolute performance is unclear., Requires a demonstration video for each new task, which may limit zero-shot deployment practicality. |
| 5.6 | detailed | daily |  | `arxiv:2605.25077` | WorldCraft: From Camera Navigation to Object Manipulation in Interactive Video World Models | stage2 | Limited quantitative evaluation details in the provided excerpt; no concrete metrics or comparisons with adapted baselines., Relevance to physical robot manipulation and VLA is indirect; the work focuses on video generation rather than real-world robotic control. |
| 5.6 | detailed | daily |  | `arxiv:2606.07436` | Skill-3D: Evolving Scene-Aware Skills for Agentic 3D Spatial Reasoning | stage2 | Limited direct relevance to robot manipulation or VLA; focuses on 3D question answering rather than physical action or control., Evaluation confined to static benchmarks without real-world robotic deployment or manipulation tasks. |
| 5.0 | coarse_only | daily |  | `arxiv:2606.11440` | INFRAMIND: Infrastructure-Aware Multi-Agent Orchestration | screened |  |
| 5.0 | coarse_only | daily |  | `arxiv:2606.11417` | Signed Compression Progress on a Sealed Audit is Goodhart-Resistant | screened |  |
| 5.0 | coarse_only | daily |  | `arxiv:2606.11375` | When Probing Accuracy Saturates, Fragility Resolves: A Complementary Metric for LLM Pre-Training Analysis | screened |  |
| 5.0 | coarse_only | daily |  | `arxiv:2606.09380` | Reasoning Arena: Trace Tournaments When Verifiable Rewards Fall Short | screened |  |
| 5.0 | coarse_only | daily |  | `arxiv:2606.05633` | Answer Presence Drives RAG Rewriting Gains | screened |  |
| 5.0 | detailed | daily |  | `arxiv:2606.08548` | OASIS: From Simulation Data Collection to Real-World Humanoid Loco-Manipulation | stage2 | Claim that simulation data outperforms real-robot teleoperation data lacks detailed comparison and may be task-specific, Hierarchical policy architecture and training details not provided in excerpt, Limited baseline comparisons beyond real-robot data |
| 5.0 | coarse_only | daily |  | `arxiv:2606.08960` | Hardening Agent Benchmarks with Adversarial Hacker-Fixer Loops | screened |  |
| 4.8 | detailed | daily |  | `arxiv:2606.09803` | Echo-Memory: A Controlled Study of Memory in Action World Models | stage2 | Evaluation limited to video generation metrics, no downstream task performance, Camera-action focus may not directly transfer to robot manipulation, No quantitative results in provided excerpt |
| 4.8 | coarse_only | daily |  | `arxiv:2606.07074` | SlimSearcher: Training Efficiency-Aware Web Agents via Adaptive Reward Gating | screened |  |
| 4.6 | coarse_only | daily |  | `arxiv:2606.05122` | Self-Evaluation Is Already There: Eliciting Latent Judge Calibration in Base LLMs with Minimal Data | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2606.11409` | Risk Under Pressure: Compute-Aware Evaluation of Adversarial Robustness in Language Models | screened |  |
| 4.4 | coarse_only | daily |  | `arxiv:2606.06087` | LatentSkill: From In-Context Textual Skills to In-Weight Latent Skills for LLM Agents | screened |  |
| 4.4 | coarse_only | daily |  | `arxiv:2606.08348` | Bayesian-Agent: Posterior-Guided Skill Evolution for LLM Agent Harnesses | screened |  |
| 4.4 | coarse_only | daily |  | `arxiv:2606.00440` | SDR: Set-Distance Rewards for Radiology Report Generation | screened |  |
| 4.4 | coarse_only | daily |  | `arxiv:2605.30837` | Send a SCOUT First: Pre-hoc Reasoning for Adaptive Detector Allocation in Prompt-Injection Defense | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2606.11502` | When Roleplaying, Do Models Believe What They Say? | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2606.11477` | Towards Fully Automated Exam Grading: Fairness-Aware Recognition of Handwritten Answers with Foundation Models | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2606.11473` | CRUMB: Efficient Prior Fitted Network Inference via Distributionally Matched Context Batching | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2606.09079` | FlashMemory-DeepSeek-V4: Lightning Index Ultra-Long Context via Lookahead Sparse Attention | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2606.09826` | OmniGameArena: A Unified UE5 Benchmark for VLM Game Agents with Improvement Dynamics | screened |  |
| 4.2 | coarse_only | daily |  | `arxiv:2606.11521` | Counterexample Guided Learning in the Large using Reasoning Agents | screened |  |
| 4.1 | coarse_only | daily |  | `arxiv:2606.07082` | On the Geometry of On-Policy Distillation | screened |  |
| 4.1 | coarse_only | daily |  | `arxiv:2606.08432` | Trajectory-Refined Distillation | screened |  |
| 4.0 | coarse_only | daily |  | `arxiv:2605.27130` | DEI: Diversity in Evolutionary Inference for Quality-Diversity Search | screened |  |
| 4.0 | coarse_only | daily |  | `arxiv:2606.07547` | Liberating LLM Capabilities in Full-Duplex Speech Models | screened |  |
| 4.0 | coarse_only | daily |  | `arxiv:2606.06523` | Lean4Agent: Formal Modeling and Verification for Agent Workflow and Trajectory | screened |  |
| 3.8 | coarse_only | daily |  | `arxiv:2606.11500` | FlexiBrain: Resolution-Agnostic Voxel-Level Encoding for Native fMRI | screened |  |
| 3.8 | coarse_only | daily |  | `arxiv:2606.11425` | JailbreakOPT: Tool-Assisted Iterative Jailbreak Prompt Optimization | screened |  |
| 3.8 | coarse_only | daily |  | `arxiv:2606.11416` | MPC-Patch-Bench: Security-Aware LLM Code Patch for Multi-Party Computation | screened |  |
| 3.8 | coarse_only | daily |  | `arxiv:2606.11385` | DeceptionX: Explainable Deception Detection with Multimodal Large Language Models | screened |  |
| 3.8 | coarse_only | daily |  | `arxiv:2606.11379` | Automated Mediator for Human Negotiation: Pre-Mediation via a Structured LLM Pipeline | screened |  |
| 3.8 | coarse_only | daily |  | `arxiv:2606.11371` | The Dynamics of Human and AI-Generated Language: How Semantics Fluctuates across Different Timescales | screened |  |
| 3.8 | coarse_only | daily |  | `arxiv:2509.10078` | Human Psychometric Questionnaires Mischaracterize LLM Behavior | screened |  |
| 3.8 | coarse_only | daily |  | `arxiv:2606.03980` | Skill-RM: Unifying Heterogeneous Evaluation Criteria via Agent Skill | screened |  |
| 3.8 | coarse_only | daily |  | `arxiv:2606.08362` | EmpiriGraph-Psy: A Dataset and LLM Pipeline for Extracting Empirical Relation Graphs from Psychology Abstracts | screened |  |
| 3.5 | coarse_only | daily |  | `arxiv:2606.11459` | APEX: Automated Prompt Engineering eXpert with Dynamic Data Selection | screened |  |
| 3.5 | detailed | daily |  | `arxiv:2606.09669` | SpatialWorld: Benchmarking Interactive Spatial Reasoning of Multimodal Agents in Real-World Tasks | stage2 | Uses non-existent model names (GPT-5, Qwen-3.5) which raises concerns about the validity of the evaluation. |
| 3.5 | coarse_only | daily |  | `arxiv:2606.09585` | Optical Reasoning: Rethinking Images as an Expressive Reasoning Medium Beyond Text | screened |  |
| 3.4 | coarse_only | daily |  | `arxiv:2606.08572` | OmniCap-IF: Benchmarking and Improving Instruction Following Abilities for Omni-Video Captioning | screened |  |
| 2.2 | coarse_only | daily |  | `arxiv:2606.11437` | The Power of Test-Time Training for Approximate Sampling | screened |  |
| 1.9 | coarse_only | daily |  | `arxiv:2606.08415` | CoVEBench: Can Video Editing Models Handle Complex Instructions? | screened |  |
| 1.0 | coarse_only | daily |  | `arxiv:2606.11456` | AI Coding Agents in Social Science: Methodologically Diverse, Empirically Consistent, Interpretively Vulnerable | screened |  |
