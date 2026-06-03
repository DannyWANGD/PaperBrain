# 2026-06-02 Screening Results

- Provider: `openrouter`
- Run state: `2026-06-02-openrouter-run-state.json`
- Papers tracked: 48

| Score | Stage | Paper ID | Title | Decision | Red Flags |
|---:|---|---|---|---|---|
| 7.9 | detailed | `arxiv:2606.01247` | Where to Look: Can Foundation Models Reach a Target Viewpoint Through Active Exploration? | digest, deep, stage2 |  |
| 7.5 | detailed | `arxiv:2606.02551` | AFUN: Towards an Affordance Foundation Model for Functionality Understanding | digest, deep, stage2 | The term 'foundation model' may be overstated without evidence of scaling laws or broad generalization beyond the training distribution., Real-robot evaluation is qualitative and lacks quantitative metrics or comparisons. |
| 7.2 | detailed | `arxiv:2606.03949` | Preference-Calibrated Human-in-the-Loop Reinforcement Learning for Robotic Manipulation | digest, stage2 | Limited baseline comparison with recent preference-based RL methods, Evaluation on a single robot platform may limit generalizability |
| 7.2 | detailed | `arxiv:2606.03943` | PointAction: 3D Points as Universal Action Representations for Robot Control | digest, stage2 | Vague baseline comparison; no specific metrics or baselines mentioned in abstract/excerpt., Limited details on real-world evaluation tasks and success criteria. |
| 6.9 | detailed | `arxiv:2605.30931` | MineExplorer: Evaluating Open-World Exploration of MLLM Agents in Minecraft | stage2 | Domain specificity: despite filtering, Minecraft mechanics may still influence agent behavior; generalizability to physical robot tasks is unverified. |
| 6.9 | detailed | `arxiv:2606.02277` | RoboSemanticBench: Diagnosing Semantic Grounding in Action Prediction for VLA Models | stage2 | Task diversity is limited to a single tabletop grasping scenario, potentially overfitting the diagnosis to this setup., Poor semantic performance may partially stem from out-of-distribution instruction styles rather than intrinsic grounding failure, not fully disentangled. |
| 6.4 | coarse_only | `arxiv:2606.03937` | Entropy Is Not Enough: Unlocking Effective Reinforcement Learning for Visual Reasoning via Vision-Anchored Token Selection | stage2 |  |
| 6.4 | coarse_only | `arxiv:2605.30723` | Skill is Not One-Size-Fits-All: Model-Aware Skill Alignment for LLM Agents | stage2 |  |
| 6.3 | detailed | `arxiv:2606.02031` | OpenWebRL: Demystifying Online Multi-turn Reinforcement Learning for Visual Web Agents | stage2 | Target domain is web agents, not physical robot manipulation or embodied AI, limiting direct applicability to core robotics interests., Live-web evaluation introduces temporal variance that may complicate strict reproducibility. |
| 6.2 | detailed | `arxiv:2606.02388` | Policy and World Modeling Co-Training for Language Agents | stage2 | Focused on text-based agent environments; direct applicability to vision-based embodied tasks (VLA, robot manipulation) is limited. |
| 6.1 | detailed | `arxiv:2605.24202` | When Does Multi-Agent RL Improve LLM Workflows? Workflow, Scale, and Policy-Sharing Tradeoffs | stage2 | Domain mismatch with core embodied/robotics interests; study is limited to text-based math/code tasks without physical actions or robot embodiment. |
| 6.1 | detailed | `arxiv:2606.00828` | RoboStressBench: Benchmarking VLM Robustness to Physical Visual Stress in Embodied Scenes | stage2 | Limited results detail in provided excerpt reduces confidence in empirical support, Extent of real-world data coverage and synthetic stress fidelity unclear, No direct connection to action prediction (VLA) or robot manipulation benchmarks |
| 5.0 | coarse_only | `arxiv:2606.03971` | Video-Mirai: Autoregressive Video Diffusion Models Need Foresight | screened |  |
| 5.0 | coarse_only | `arxiv:2606.03968` | QUBRIC: Co-Designing Queries and Rubrics for RL Beyond Verifiable Rewards | screened |  |
| 5.0 | coarse_only | `arxiv:2605.24956` | NITP: Next Implicit Token Prediction for LLM Pre-training | screened |  |
| 5.0 | coarse_only | `arxiv:2605.30501` | Linear Ensembles Wash Away Watermarks: On the Fragility of Distributional Perturbations in LLMs | screened |  |
| 5.0 | detailed | `arxiv:2605.29860` | ESPO: Early-Stopping Proximal Policy Optimization | stage2 | Only compared against vanilla PPO, missing baselines like GRPO or DAPO that also address credit assignment in LLM RL., Evaluation limited to a single model (7B) and solely on math reasoning tasks; no other domains or scalability tests., Incremental performance gains (≤1% absolute) on AIME, AMC, MATH-500 with no significance testing., No code or detailed hyperparameters provided, limiting reproducibility. |
| 5.0 | coarse_only | `arxiv:2606.01682` | Off-the-Shelf LLMs as Process Scorers: Training-Free Alternative to PRMs for Mathematical Reasoning | screened |  |
| 5.0 | coarse_only | `arxiv:2605.26248` | Unified Neural Scaling Laws | screened |  |
| 4.8 | coarse_only | `arxiv:2605.31597` | SOCO: Benchmarking Semantic Object Correspondence in Vision Foundation Models | screened |  |
| 4.7 | coarse_only | `arxiv:2605.29707` | Domino: Decoupling Causal Modeling from Autoregressive Drafting in Speculative Decoding | screened |  |
| 4.5 | coarse_only | `arxiv:2606.03980` | Skill-RM: Unifying Heterogeneous Evaluation Criteria via Agent Skill | screened |  |
| 4.5 | coarse_only | `arxiv:2606.03969` | Quantifying Faithful Confidence Expression in Large Reasoning Models | screened |  |
| 4.5 | coarse_only | `arxiv:2605.28556` | A Matter of TASTE: Improving Coverage and Difficulty of Agent Benchmarks | screened |  |
| 4.5 | coarse_only | `arxiv:2605.25381` | Not only where, But when: Temporal Scheduling for RLVR | screened |  |
| 4.5 | coarse_only | `arxiv:2606.00240` | MindZero: Learning Online Mental Reasoning With Zero Annotations | screened |  |
| 4.4 | coarse_only | `arxiv:2606.03910` | NetKV: Network-Aware Decode Instance Selection for Disaggregated LLM Inference | screened |  |
| 4.3 | coarse_only | `arxiv:2606.03962` | Using Reward Uncertainty to Induce Diverse Behaviour in Reinforcement Learning | screened |  |
| 4.3 | coarse_only | `arxiv:2606.03920` | Benchmarking Visual State Tracking in Multimodal Video Understanding | screened |  |
| 4.3 | coarse_only | `arxiv:2605.25659` | StreamChar: Long-Horizon Streaming Character Audio-Video Generation with Decoupled Orchestration | screened |  |
| 4.3 | coarse_only | `arxiv:2605.24614` | Measuring the Depth of LLM Unlearning via Activation Patching | screened |  |
| 4.2 | coarse_only | `arxiv:2606.03965` | Agentic Chain-of-Thought Steering for Efficient and Controllable LLM Reasoning | screened |  |
| 4.2 | coarse_only | `arxiv:2606.01311` | SkillAdaptor: Self-Adapting Skills for LLM Agents from Trajectories | screened |  |
| 4.1 | coarse_only | `arxiv:2606.03957` | Efficient ASR Training with Conversations that Never Happened | screened |  |
| 4.0 | coarse_only | `arxiv:2606.03926` | DiffUNet^2: Bidirectional Prediction, Probabilistic Generation and Collaborative Visual Discovery for Scientific Data | screened |  |
| 4.0 | coarse_only | `arxiv:2606.01528` | Joint Agent Memory and Exploration Learning via Novelty Signals | screened |  |
| 3.9 | detailed | `arxiv:2606.03963` | Self-Refining Agentic Reinforcement Learning for Vision-Conditioned UAV Navigation | stage2 | No comparison with human-designed or LLM-based reward generation baselines, Limited evaluation details provided in abstract/excerpt, Only tested on UAV navigation tasks, not manipulation |
| 3.9 | coarse_only | `arxiv:2606.00090` | Silent Failures in Physical AI: A Literature Review of Runtime Action Authorization for Autonomous Systems | screened |  |
| 3.8 | coarse_only | `arxiv:2606.02373` | Harness-1: Reinforcement Learning for Search Agents with State-Externalizing Harnesses | screened |  |
| 3.8 | coarse_only | `arxiv:2605.30852` | Speculative Pipeline Decoding: Higher-Accruacy and Zero-Bubble Speculation via Pipeline Parallelism | screened |  |
| 3.6 | coarse_only | `arxiv:2606.02482` | X-Stream: Exploring MLLMs as Multiplexers for Multi-Stream Understanding | screened |  |
| 3.5 | coarse_only | `arxiv:2606.02404` | K-BrowseComp: A Web Browsing Agent Benchmark Grounded in Korean Contexts | screened |  |
| 3.4 | coarse_only | `arxiv:2606.03986` | NewtPhys: Do Foundation Models Understand Newtonian Physics? | screened |  |
| 3.4 | coarse_only | `arxiv:2606.03967` | AlignAtt4LLM: Fast AlignAtt for Decoder-Only LLMs at IWSLT 2026 Simultaneous Speech Translation Task | screened |  |
| 3.2 | coarse_only | `arxiv:2606.03979` | Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories | screened |  |
| 3.2 | coarse_only | `arxiv:2606.02437` | On the Scaling of PEFT: Towards Million Personal Models of Trillion Parameters | screened |  |
| 3.2 | coarse_only | `arxiv:2606.02470` | MCP-Persona: Benchmarking LLM Agents on Real-World Personal Applications via Environment Simulation | screened |  |
| 3.0 | coarse_only | `arxiv:2605.21102` | ACL-Verbatim: hallucination-free question answering for research | screened |  |
