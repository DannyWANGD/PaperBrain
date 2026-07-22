# 2026-06-10 Screening Results

- Provider: `openrouter`
- Providers seen: `openrouter`
- Run modes: `daily`
- Run state: `state.json`
- Papers tracked: 48

| Score | Stage | Source | Forced | Paper ID | Title | Decision | Red Flags |
|---:|---|---|---|---|---|---|---|
| 7.5 | detailed | daily |  | `arxiv:2606.12403` | World Pilot: Steering Vision-Language-Action Models with World-Action Priors | digest, deep, stage2 | Limited evaluation details in excerpt; potential overclaim on world model transfer without action post-training. |
| 7.4 | detailed | daily |  | `arxiv:2606.11187` | Next Forcing: Causal World Modeling with Multi-Chunk Prediction | digest, stage2 | Limited comparison with world model baselines beyond LingBot-VA; evaluation on manipulation tasks restricted to RoboTwin, which may not fully represent broader embodied AI scenarios., Inference acceleration claim (2x) may rely on auxiliary modules that could compromise prediction quality, though not thoroughly ablated. |
| 7.3 | detailed | daily |  | `arxiv:2606.12366` | APT: Action Expert Pretraining Improves Instruction Generalization of Vision-Language-Action Policies | digest, stage2 | Limited empirical evidence in provided excerpt; full evaluation details and quantitative results not shown. |
| 7.2 | detailed | daily |  | `arxiv:2606.11087` | Test-Time Gradient Guidance of Flow Policies in Reinforcement Learning | digest, stage2 | No real-world robot experiments, only offline RL benchmarks, Relies on pre-trained critic which may be inaccurate |
| 7.0 | detailed | daily |  | `arxiv:2606.12402` | DIRECT: When and Where Should You Allocate Test-Time Compute in Embodied Planners? | digest, stage2 | Limited evaluation details in abstract; potential lack of comparison to other adaptive compute methods. |
| 6.8 | detailed | daily |  | `arxiv:2606.12372` | UniIntervene: Agentic Intervention for Efficient Real-World Reinforcement Learning | stage2 | Limited comparison to methods using world models or foundation models for autonomous intervention, No ablation studies mentioned in excerpt, Reproducibility unclear without code or detailed algorithm description |
| 6.7 | detailed | daily |  | `arxiv:2606.12299` | Learning What to Say to Your VLA: Mostly Harmless Vision Language Action Model Steering | stage2 | Limited baseline comparisons beyond base VLA; no explicit comparison to other prompt optimization or steering methods., Harmlessness guarantees via conformal prediction may not generalize beyond the calibration distribution., No code release mentioned, limiting reproducibility. |
| 6.5 | detailed | daily |  | `arxiv:2606.11129` | WorldOlympiad: Can Your World Model Survive a Triathlon? | stage2 | Limited empirical evidence in provided excerpt; no quantitative results shown., Reliance on MLLM-as-judge for physical track may introduce uncalibrated biases., Potential overlap with existing benchmarks (e.g., Physion, VBench) not fully differentiated in excerpt. |
| 6.4 | detailed | daily |  | `arxiv:2606.12352` | CHORUS: Decentralized Multi-Embodiment Collaboration with One VLA Policy | stage2 | Unclear if centralized baselines are strong; potential overclaiming without detailed comparison., Scalability claims limited to small teams (3 robots); larger team performance not shown., Limited reproducibility details: VLA backbone, training data, and hyperparameters not specified in excerpt. |
| 6.2 | detailed | daily |  | `arxiv:2606.12396` | VLGA: Vision-Language-Geometry-Action Models for Autonomous Driving | stage2 | Application is autonomous driving, not robot manipulation; relevance to manipulation is indirect., No code or model release mentioned, limiting reproducibility. |
| 5.8 | coarse_only | daily |  | `arxiv:2606.09032` | Bridging the Agent-World Gap: Text World Models for LLM-based Agents | stage2 |  |
| 5.6 | detailed | daily |  | `arxiv:2606.11025` | Flow-DPPO: Divergence Proximal Policy Optimization for Flow Matching Models | stage2 | Evaluation limited to image/video generation, not applied to robot manipulation or embodied AI tasks., Direct relevance to target interests (Robot Manipulation, VLA, World Model, Embodied AI) is low; method may transfer but not demonstrated. |
| 5.5 | detailed | daily |  | `arxiv:2606.12384` | APPO: Agentic Procedural Policy Optimization | stage2 | The paper focuses on LLM agents for text-based tool-use tasks, not on robot manipulation or embodied AI, limiting its direct applicability to the target robotics interests. |
| 5.0 | coarse_only | daily |  | `arxiv:2606.12370` | Breaking Entropy Bounds: Accelerating RL Training via MTP with Rejection Sampling | screened |  |
| 5.0 | coarse_only | daily |  | `arxiv:2606.12316` | Slots, Transitions, Loops: Learning Composable World Models for ARC | screened |  |
| 5.0 | coarse_only | daily |  | `arxiv:2606.10917` | Role-Agent: Bootstrapping LLM Agents via Dual-Role Evolution | screened |  |
| 5.0 | coarse_only | daily |  | `arxiv:2606.10968` | Beyond Uniform Token-Level Trust Region in LLM Reinforcement Learning | screened |  |
| 5.0 | coarse_only | daily |  | `arxiv:2606.11180` | Lip Forcing: Few-Step Autoregressive Diffusion for Real-time Lip Synchronization | screened |  |
| 5.0 | coarse_only | daily |  | `arxiv:2606.10572` | One Token per Multimodal Evidence: Latent Memory for Resource-Constrained QA | screened |  |
| 5.0 | coarse_only | daily |  | `arxiv:2606.10646` | How Does Reasoning Flow? Tracing Attention-Induced Information Flow for Targeted RL in LLMs | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2606.12412` | Reroute, Don't Remove: Recoverable Visual Token Routing for Vision-Language Models | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2606.05922` | Retrospective Harness Optimization: Improving LLM Agents via Self-Preference over Trajectory Rollouts | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2606.12387` | TAHOE: Text-to-SQL with Automated Hint Optimization from Experience | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2606.12346` | Atlas H&E-TME: Scalable AI-Based Tissue Profiling at Expert Pathologist-Level Accuracy | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2606.11188` | ARM: An AutoRegressive Large Multimodal Model with Unified Discrete Representations | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2606.12071` | On the Limits of LLM-as-Judge for Scientific Novelty Assessment | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2606.08044` | When Behavioral Safety Evaluation Fails: A Representation-Level Perspective | screened |  |
| 4.4 | coarse_only | daily |  | `arxiv:2606.09056` | MilliVid: Hierarchical Latents for Long-Range Consistency in Video Generation | screened |  |
| 4.4 | coarse_only | daily |  | `arxiv:2606.09131` | Late-Layer Fusion is Enough: Dual-Path Vision Token Routing for Multimodal Large Language Models under Visual Saturation | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2606.12407` | How Seemingly Inconsequential Design Choices Dictate Performance of LLMs in Pathology | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2606.12332` | Measuring Semantic Progress in Multi-turn Dialogue via Information Gain | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2606.11052` | Attention Amnesia in Hybrid LLMs: When CoT Fine-Tuning Breaks Long-Range Recall, and How to Fix It | screened |  |
| 4.2 | coarse_only | daily |  | `arxiv:2606.12386` | ATLAS: Active Theory Learning for Automated Science | screened |  |
| 4.2 | coarse_only | daily |  | `arxiv:2606.12342` | ALIGNBEAM : Inference-Time Alignment Transfer via Cross-Vocabulary Logit Mixing | screened |  |
| 4.1 | coarse_only | daily |  | `arxiv:2606.12364` | On Subquadratic Architectures: From Applications to Principles | screened |  |
| 4.1 | coarse_only | daily |  | `arxiv:2606.12300` | Natural-Language Temporal Grounding in Hour-Long Videos is a Search Problem: A Benchmark and Empirical Decomposition | screened |  |
| 4.1 | coarse_only | daily |  | `arxiv:2606.09697` | PsychoSafe: Eliciting Psychologically-Informed Refusals in Large Language Models | screened |  |
| 4.1 | coarse_only | daily |  | `arxiv:2606.10061` | BenSyc: Benchmarking Conversational Sycophancy and Human Alignment in LLMs for Bengali Contexts | screened |  |
| 3.9 | coarse_only | daily |  | `arxiv:2606.09967` | ABot-Earth 0.5: Generative 3D Earth Model | screened |  |
| 3.9 | coarse_only | daily |  | `arxiv:2606.11182` | EEVEE: Towards Test-time Prompt Learning in the Real World for Self-Improving Agents | screened |  |
| 3.6 | coarse_only | daily |  | `arxiv:2606.09821` | Rethinking the Divergence Regularization in LLM RL | screened |  |
| 3.2 | coarse_only | daily |  | `arxiv:2606.12392` | System Report for CCL25-Eval Task 5: New Dataset and LoRA-Fine-Tuned Qwen2.5 | screened |  |
| 3.2 | coarse_only | daily |  | `arxiv:2606.12318` | Harness In-Context Operator Learning with Chain of Operators | screened |  |
| 3.2 | coarse_only | daily |  | `arxiv:2606.09730` | SearchSwarm: Towards Delegation Intelligence in Agentic LLMs for Long-Horizon Deep Research | screened |  |
| 3.2 | coarse_only | daily |  | `arxiv:2606.10650` | Dynamic Linear Attention | screened |  |
| 3.1 | coarse_only | daily |  | `arxiv:2606.12294` | Bridging the Modality Gap in Forensic Image Retrieval | screened |  |
| 2.2 | coarse_only | daily |  | `arxiv:2606.06098` | IR3DE: A Linear Router for Large Language Models | screened |  |
| 1.9 | coarse_only | daily |  | `arxiv:2606.12350` | Nonslop: A Gamified Experiment in Human-AI Collaborative Writing | screened |  |
