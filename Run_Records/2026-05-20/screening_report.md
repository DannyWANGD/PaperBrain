# 2026-05-20 Screening Results

- Provider: `openrouter`
- Providers seen: `openrouter`
- Run modes: `daily`
- Run state: `state.json`
- Papers tracked: 44

| Score | Stage | Source | Forced | Paper ID | Title | Decision | Red Flags |
|---:|---|---|---|---|---|---|---|
| 7.1 | detailed | daily |  | `arxiv:2605.22882` | GEM-4D: Geometry-Enhanced Video World Models for Robot Manipulation | digest, stage2 | Real-world manipulation evaluation lacks details (single success rate, no error bars, task description missing), Quantitative results for video prediction and geometric consistency not shown in excerpt, making SOTA claims unverifiable |
| 6.8 | detailed | daily |  | `arxiv:2605.18746` | ESI-Bench: Towards Embodied Spatial Intelligence that Closes the Perception-Action Loop | digest, stage2 | Benchmark paper with no new algorithmic contribution; may have limited direct applicability to method development., Simulation-only benchmark, real-world transfer unclear., Insufficient technical details in provided excerpt to fully assess evaluation rigor. |
| 6.1 | detailed | daily |  | `arxiv:2605.15458` | Video Models Can Reason with Verifiable Rewards | stage2 | Evaluation limited to synthetic 2D puzzle tasks, not directly applicable to robot manipulation or embodied AI., Unclear scalability to high-resolution, real-world video reasoning. |
| 6.0 | detailed | daily |  | `arxiv:2605.19436` | CEPO: RLVR Self-Distillation using Contrastive Evidence Policy Optimization | digest, stage2 | Not directly relevant to robot manipulation, VLA, world model, or embodied AI; evaluation limited to math reasoning benchmarks, no robotics tasks. |
| 6.0 | detailed | daily |  | `arxiv:2605.17076` | S-Bus: Automatic Read-Set Reconstruction for Multi-Agent LLM State Coordination | digest | Low relevance to target interests (robot manipulation, VLA, world model, RL, diffusion, embodied AI); primarily a systems paper for LLM agent coordination. |
| 5.8 | detailed | daily |  | `arxiv:2605.20164` | Not Every Rubric Teaches Equally: Policy-Aware Rubric Rewards for RLVR | digest, stage2 | Low relevance to target interests: paper focuses on LLM post-training, not robot manipulation, VLA, world models, or embodied AI., No evaluation on robotic or embodied tasks, limiting applicability claims. |
| 5.6 | detailed | daily |  | `arxiv:2605.09640` | Overcoming Catastrophic Forgetting in Visual Continual Learning with Reinforcement Fine-Tuning | stage2 | Limited direct relevance to robotics/embodied AI: evaluation is on static image classification, not on manipulation, navigation, or embodied tasks., Novelty is incremental: trajectory-level KL regularization is a known idea in continual learning, now adapted to RFT. |
| 5.2 | detailed | daily |  | `arxiv:2605.21800` | stable-worldmodel: A Platform for Reproducible World Modeling Research and Evaluation | stage2 | No quantitative results or empirical validation of platform benefits in the provided excerpt, Potential overclaim of impact without demonstrated performance improvements, Platform paper with limited algorithmic novelty; may not directly advance state-of-the-art in target interests |
| 5.2 | detailed | daily |  | `arxiv:2605.19577` | GoLongRL: Capability-Oriented Long Context Reinforcement Learning with Multitask Alignment | screened | Not relevant to robotics/embodied AI; purely text-based LLM post-training., Potential overclaim of comparable performance to much larger models without rigorous statistical testing. |
| 5.0 | coarse_only | daily |  | `arxiv:2605.21770` | Manifold-Guided Attention Steering | screened |  |
| 5.0 | detailed | daily |  | `arxiv:2605.18703` | EnvFactory: Scaling Tool-Use Agents via Executable Environments Synthesis and Robust RL | stage2 | Mismatch with core robotics interests: focuses on software tool-use agents, not embodied manipulation, VLA, or world models., Limited evaluation scope: only 85 environments and 2,575 trajectories; generalization to diverse real-world tool ecosystems unclear. |
| 5.0 | coarse_only | daily |  | `arxiv:2605.19932` | PEEK: Context Map as an Orientation Cache for Long-Context LLM Agents | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2605.22883` | Energy per Successful Goal: Goal-Level Energy Accounting for Agentic AI Systems | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2605.20035` | Stage-adaptive Token Selection for Efficient Omni-modal LLMs | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2605.20075` | CopT: Contrastive On-Policy Thinking with Continuous Spaces for General and Agentic Reasoning | screened |  |
| 4.6 | coarse_only | daily |  | `arxiv:2605.18101` | SENSE: Satellite-based ENergy Synthesis for Sustainable Environment | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2605.21822` | Implicit Safety Alignment from Crowd Preferences | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2605.21726` | Probabilistic Attribution For Large Language Models | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2605.17734` | Harnessing LLM Agents with Skill Programs | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2605.20087` | ThoughtTrace: Understanding User Thoughts in Real-World LLM Interactions | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2605.08472` | Mid-Training with Self-Generated Data Improves Reinforcement Learning in Language Models | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2605.19147` | Be Kind, Rewrite: Benign Projections via Rewriting Defend Against LLM Data Poisoning Attacks | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2605.21827` | Does Slightly Mean Somewhat? Measuring Vague Intensity Words in LLM Numeric Actions | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2605.21773` | HIDBench: Benchmarking Large Language Models for Host-Based Intrusion Detection | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2605.21768` | Memory-R2: Fair Credit Assignment for Long-Horizon Memory-Augmented LLM Agents | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2605.16003` | Echo-Forcing: A Scene Memory Framework for Interactive Long Video Generation | screened |  |
| 4.2 | coarse_only | daily |  | `arxiv:2605.19769` | OpenComputer: Verifiable Software Worlds for Computer-Use Agents | screened |  |
| 4.1 | coarse_only | daily |  | `arxiv:2605.21740` | SMDD-Bench: Can LLMs Solve Real-World Small Molecule Drug Design Tasks? | screened |  |
| 4.0 | coarse_only | daily |  | `arxiv:2605.21728` | BEiTScore: Reference-free Image Captioning Evaluation with an Efficient Cross-Encoder Model | screened |  |
| 4.0 | coarse_only | daily |  | `arxiv:2605.16403` | When Vision Speaks for Sound | screened |  |
| 4.0 | coarse_only | daily |  | `arxiv:2605.20147` | PixVerve: Advancing Native UHR Image Generation to 100MP with a Large-Scale High-Quality Dataset | screened |  |
| 4.0 | coarse_only | daily |  | `arxiv:2605.19633` | optimize_anything: A Universal API for Optimizing any Text Parameter | screened |  |
| 3.9 | detailed | daily |  | `arxiv:2605.19995` | CogOmniControl: Reasoning-Driven Controllable Video Generation via Creative Intent Cognition | screened | Low relevance to target robotics/AI workflow; application is creative video generation, not embodied AI or manipulation., Insufficient empirical evidence in the provided excerpt; no quantitative comparisons or metrics., Benchmarks built from proprietary anime production data may not be publicly available, limiting reproducibility. |
| 3.9 | coarse_only | daily |  | `arxiv:2605.18226` | Context Memorization for Efficient Long Context Generation | screened |  |
| 3.9 | coarse_only | daily |  | `arxiv:2605.17360` | Omni-DuplexEval: Evaluating Real-time Duplex Omni-modal Interaction | screened |  |
| 3.7 | coarse_only | daily |  | `arxiv:2605.18984` | Artifact-Bench: Evaluating MLLMs on Detecting and Assessing the Artifacts of AI-Generated Videos | screened |  |
| 3.6 | coarse_only | daily |  | `arxiv:2605.14236` | Active Learners as Efficient PRP Rerankers | screened |  |
| 3.2 | coarse_only | daily |  | `arxiv:2605.21834` | On-Policy Consistency Training Improves LLM Safety with Minimal Capability Degradation | screened |  |
| 3.2 | coarse_only | daily |  | `arxiv:2605.21763` | On the Sample Complexity of Discounted Reinforcement Learning with Optimized Certainty Equivalents | screened |  |
| 3.2 | coarse_only | daily |  | `arxiv:2605.21739` | AttuneBench: A Conversation-Based Benchmark for LLM Emotional Intelligence | screened |  |
| 3.0 | coarse_only | daily |  | `arxiv:2605.14842` | Editor's Choice: Evaluating Abstract Intent in Image Editing through Atomic Entity Analysis | screened |  |
| 1.8 | coarse_only | daily |  | `arxiv:2605.21810` | Trace2Skill: Verifier-Guided Skill Evolution for Long-Context EDA Agents | screened |  |
| 1.8 | coarse_only | daily |  | `arxiv:2605.21778` | What Counts as AI Sycophancy? A Taxonomy and Expert Survey of a Fragmented Construct | screened |  |
| 1.6 | coarse_only | daily |  | `arxiv:2605.17829` | Interactive Evaluation Requires a Design Science | screened |  |
