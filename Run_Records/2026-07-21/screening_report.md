# 2026-07-21 Screening Results

- Provider: `openrouter`
- Providers seen: `openrouter`
- Run modes: `daily`
- Run state: `state.json`
- Papers tracked: 27

| Score | Stage | Source | Forced | Paper ID | Title | Decision | Red Flags |
|---:|---|---|---|---|---|---|---|
| 8.1 | detailed | daily |  | `arxiv:2607.16401` | Apple-π: Benchmarking Thinking with Video Towards Law-Grounded Physical Intelligence | digest, deep, stage2 |  |
| 6.9 | detailed | daily |  | `arxiv:2607.16204` | Masked Diffusion Language Models are Strong and Steerable Text-Based World Models for Agentic RL | digest, stage2 | Evaluation limited to text-based environments; no direct evidence of transfer to physical robot manipulation or VLA tasks., Claim of up to 47% absolute gains lacks detailed statistical significance and may be cherry-picked from best-case scenarios. |
| 6.3 | detailed | daily |  | `arxiv:2607.17977` | RynnBrain 1.1: Towards More Capable and Generalizable Embodied Foundation Model | digest, stage2 | Vague evaluation claims without concrete numbers in the provided excerpt, Incremental upgrade from RynnBrain 1.0 with limited methodological detail, Real-robot comparisons only mentioned against Qwen-based VLAs, missing broader baselines |
| 5.5 | detailed | daily |  | `arxiv:2607.15550` | SeerGuard: A Safety Framework for Mobile GUI Agents via World Model Prediction | stage2 | Missing comparison with existing safety mechanisms (e.g., guardrails, prompt-based safety checks, post-hoc verification) beyond the baseline agents without any safety., Limited to mobile GUI domain, unclear transferability to physical robot manipulation scenarios., No mention of RL, diffusion, or physical embodied evaluation, which are key interests of the target workflow. |
| 5.4 | detailed | daily |  | `arxiv:2607.14183` | Open-AoE: An Open Egocentric Manipulation Dataset and Toolchain for Embodied Learning | stage2 | No downstream task performance reported, No annotation quality metrics or error analysis, Training recipes mentioned but not empirically validated, Lacks concrete evidence of dataset utility for robot learning |
| 5.2 | detailed | daily |  | `arxiv:2607.17423` | TimeLens2: Generalist Video Temporal Grounding with Multimodal LLMs | digest | Low relevance to target robotics/AI interests: the paper addresses video temporal grounding, not robot manipulation, VLA, world models, RL, diffusion models, or embodied AI. |
| 5.1 | detailed | daily |  | `arxiv:2607.16850` | Group Entropy-Controlled Policy Optimization | digest, stage2 | Mismatch with target research interests: no connection to robotics, manipulation, or embodied AI., Limited applicability to continuous control problems; method is LLM-specific RL. |
| 4.8 | coarse_only | daily |  | `arxiv:2607.17097` | HarmoHOI: Harmonizing Appearance and 3D Motion for Multi-view Hand-Object Interaction Synthesis | screened |  |
| 4.8 | coarse_only | daily |  | `arxiv:2607.16074` | JoyNexus: Service-Oriented Multi-Tenant Post-Training for VLA Models | screened |  |
| 4.6 | coarse_only | daily |  | `arxiv:2607.18213` | SWE-Pruner Pro: The Coder LLM Already Knows What to Prune | screened |  |
| 4.5 | detailed | daily |  | `arxiv:2607.16900` | Environment-free Synthetic Data Generation for API-Calling Agents | screened | Low relevance to target research interests: paper focuses on API-calling agents, not on robot manipulation, VLA, or embodied AI. |
| 4.5 | coarse_only | daily |  | `arxiv:2607.13365` | DiffGI: Differentiable Geometry Images for High-Fidelity Thin-Shell 3D Generation | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2607.17247` | Distilled Reinforcement Learning for LLM Post-training | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2607.14186` | NexForge: Scaling Agent Capabilities through Requirement-Driven Task Synthesis for LLMs | screened |  |
| 4.5 | coarse_only | daily |  | `arxiv:2607.15434` | Coercion and Deception in AI-to-AI Management: An Agentic Benchmark of Unprompted Escalation | screened |  |
| 4.4 | detailed | daily |  | `arxiv:2607.18110` | LLM-as-a-Coach: Experiential Learning for Non-Verifiable Tasks | screened | Relevance to robotics/embodied AI is low; purely text-based LLM training., Limited quantitative evidence in provided excerpt. |
| 4.4 | coarse_only | daily |  | `arxiv:2607.17972` | DiFA: Inference-Time Forward-Process Alignment for Diffusion Models | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2607.10387` | GigaChat Audio: Time-aware Large Audio Language Model | screened |  |
| 4.3 | coarse_only | daily |  | `arxiv:2607.10371` | GigaAM Multilingual: Foundation Model for Underrepresented Languages | screened |  |
| 4.1 | coarse_only | daily |  | `arxiv:2607.18227` | FlowMimic: Mask-free Visual Editing and Generation with Pixel-pair Warped Flow Field for Online Video Editing Data Generation and Modality Mimicry | screened |  |
| 4.1 | detailed | daily |  | `arxiv:2607.18171` | FlashRT: Agent Harness for Guiding Agents to Deploy Real-Time Multimodal Applications | screened | Low relevance to target research interests (system deployment, not advancement of robot manipulation, VLA, RL, diffusion models, or embodied AI), Limited evaluation details in excerpt; no comparison with other auto-parallelism frameworks for multimodal applications beyond a single vLLM-Omni case, Claims of scalability on less mature platforms based on a single AMD GPU benchmark without broader validation across diverse hardware-software stacks |
| 3.9 | coarse_only | daily |  | `arxiv:2607.18217` | HOMIE: Human-object Centric Video Personalization via Multimodal Intelligent Enchancement | screened |  |
| 3.8 | coarse_only | daily |  | `arxiv:2607.07820` | DeepSearch-World: Self-Distillation for Deep Search Agents in a Verifiable Environment | screened |  |
| 3.3 | coarse_only | daily |  | `arxiv:2607.16609` | Can Multimodal Large Language Models Understand OCT? | screened |  |
| 3.2 | coarse_only | daily |  | `arxiv:2607.17250` | EvolvingWorld: An Open-Schema Framework for Co-Evolving Role-Play Agents and World Model in Interactive Literary World | screened |  |
| 2.1 | coarse_only | daily |  | `arxiv:2607.06306` | UI2App: Benchmarking Visual Interaction Inference in Executable Web Application Generation | screened |  |
| 1.7 | coarse_only | daily |  | `arxiv:2607.18144` | Do Language Models Dream of Binding Molecules? Benchmarking LLMs under Spatial Constraints | screened |  |
