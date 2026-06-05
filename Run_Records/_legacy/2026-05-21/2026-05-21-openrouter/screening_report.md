# 2026-05-21 Screening Results

- Provider: `openrouter`
- Run state: `state.json`
- Papers tracked: 44

| Score | Stage | Paper ID | Title | Decision | Red Flags |
|---:|---|---|---|---|---|
| 7.0 | detailed | `arxiv:2605.21468` | You Only Need Minimal RLVR Training: Extrapolating LLMs via Rank-1 Trajectories | digest | Limited relevance to target robotics interests; evaluated only on math reasoning tasks, not on embodied AI or manipulation. |
| 6.0 | detailed | `arxiv:2605.23054` | Model Collapse as Cultural Evolution | digest | No direct connection to robotics, manipulation, VLA, world models, RL, diffusion models, or embodied AI; purely a linguistic study on LLM self-training degradation., Findings may not transfer to embodied or action-oriented domains without additional validation. |
| 6.0 | detailed | `arxiv:2605.20834` | Conditional Equivalence of DPO and RLHF: Implicit Assumption, Failure Modes, and Provable Alignment | digest, stage2 | Mismatch with target research interests: paper focuses on LLM alignment, not robot manipulation, VLA, world models, or embodied AI. |
| 6.0 | detailed | `arxiv:2605.18565` | MINTEval: Evaluating Memory under Multi-Target Interference in Long-Horizon Agent Systems | digest | Low relevance to core robotics interests (robot manipulation, VLA, world models, RL, diffusion models); benchmark focuses on text-based memory for language agents, not embodied or physical tasks. |
| 5.9 | detailed | `arxiv:2605.23089` | Dreaming Smoothly and Sample Efficiently with Gradient Penalized Latent Dynamics | digest, stage2 | Evaluation limited to DeepMind Control proprioceptive locomotion; no manipulation or real-world embodied tasks., Milder gains on pixel-based observations suggest limited applicability to visual domains., No comparison to other smoothness regularization methods. |
| 5.5 | detailed | `arxiv:2605.15113` | Learning from Language Feedback via Variational Policy Distillation | screened | Evaluation is limited to scientific reasoning and code generation tasks, with no demonstration on robot manipulation, embodied AI, or world model domains., The method does not address any robotics-specific challenges, reducing its priority for a robotics/AI research workflow. |
| 5.4 | detailed | `arxiv:2605.19660` | OScaR: The Occam's Razor for Extreme KV Cache Quantization in LLMs and Beyond | screened | Low relevance to robotics/embodied AI interests; paper focuses on LLM inference optimization, not on manipulation, VLA, world models, RL, or diffusion. |
| 5.1 | detailed | `arxiv:2605.24043` | LLM-AutoSciLab: Closed-Loop Scientific Discovery via Active Experimentation with LLMs | screened | Mismatch with target research interests: paper focuses on scientific discovery in chemistry/biology, not robotics, manipulation, VLA, world models, RL, diffusion models, or embodied AI. |
| 4.8 | coarse_only | `arxiv:2605.23102` | LLM Sparsity Prior for Robust Feature Selection | screened |  |
| 4.8 | coarse_only | `arxiv:2605.23065` | Dithering Defense: Adversarial Robustness of Vision Foundation Models via Multi-Level Floyd-Steinberg Dithering | screened |  |
| 4.8 | coarse_only | `arxiv:2605.20630` | Evaluating Temporal Semantic Caching and Workflow Optimization in Agentic Plan-Execute Pipelines | screened |  |
| 4.8 | coarse_only | `arxiv:2602.07892` | Safety Alignment as Continual Learning: Mitigating the Alignment Tax via Orthogonal Gradient Projection | screened |  |
| 4.7 | coarse_only | `arxiv:2605.23025` | World Machine: Towards Generative World Modeling for Time-Series | screened |  |
| 4.7 | coarse_only | `arxiv:2605.20873` | PlanningBench: Generating Scalable and Verifiable Planning Data for Evaluating and Training Large Language Models | screened |  |
| 4.5 | coarse_only | `arxiv:2605.20682` | IndusAgent: Reinforcing Open-Vocabulary Industrial Anomaly Detection with Agentic Tools | screened |  |
| 4.5 | coarse_only | `arxiv:2605.20119` | Toto 2.0: Time Series Forecasting Enters the Scaling Era | screened |  |
| 4.5 | coarse_only | `arxiv:2605.19597` | LLMEval-Logic: A Solver-Verified Chinese Benchmark for Logical Reasoning of LLMs with Adversarial Hardening | screened |  |
| 4.5 | coarse_only | `arxiv:2605.16787` | The Unlearnability Phenomenon in RLVR for Language Models | screened |  |
| 4.5 | coarse_only | `arxiv:2605.17110` | Capturing LLM Capabilities via Evidence-Calibrated Query Clustering | screened |  |
| 4.4 | coarse_only | `arxiv:2605.24050` | More Skills, Worse Agents? Skill Shadowing Degrades Performance When Expanding Skill Libraries | screened |  |
| 4.4 | detailed | `arxiv:2605.19330` | MOCHA: Multi-Objective Chebyshev Annealing for Agent Skill Optimization | screened | Not relevant to robotics/embodied AI; tasks are text-based agent skills, not manipulation or physical interaction. |
| 4.4 | coarse_only | `arxiv:2605.17916` | PanoWorld: A Generative Spatial World Model for Consistent Whole-House Panorama Synthesis | screened |  |
| 4.3 | coarse_only | `arxiv:2605.23039` | Do Language Models Know What Not to Say? Causal Evidence for Statistical Preemption in LLMs | screened |  |
| 4.2 | coarse_only | `arxiv:2605.23078` | GEMQ: Global Expert-Level Mixed-Precision Quantization for MoE LLMs | screened |  |
| 4.1 | coarse_only | `arxiv:2605.20258` | It Takes Two: Complementary Self-Distillation for Contextual Integrity in LLMs | screened |  |
| 4.1 | coarse_only | `arxiv:2605.17991` | Stable Audio 3 | screened |  |
| 4.1 | coarse_only | `arxiv:2605.20179` | TIDE: Efficient and Lossless MoE Diffusion LLM Inference with I/O-aware Expert Offload | screened |  |
| 4.0 | coarse_only | `arxiv:2605.20315` | Mix-Quant: Quantized Prefilling, Precise Decoding for Agentic LLMs | screened |  |
| 4.0 | detailed | `arxiv:2605.21463` | Mem-π: Adaptive Memory through Learning When and What to Generate | stage2 | Inconsistent improvement claims between abstract (30%) and excerpt (20%), Text-based embodied interaction is not real robot manipulation, Limited relevance to target robotics interests (no physical robot, VLA, or world model) |
| 3.8 | coarse_only | `arxiv:2605.23057` | ModeSwitch-LLM: A Lightweight Phase-Aware Controller for Cross-Mode LLM Inference on a Single GPU | screened |  |
| 3.8 | coarse_only | `arxiv:2605.23052` | DreamerNLplus: Interpretable Modeling of Mental Health Dynamics from Social Media Timelines using Hybrid Rule-Based and RAG Methods | screened |  |
| 3.8 | coarse_only | `arxiv:2605.23040` | Steered Generation via Gradient-Based Optimization on Sparse Query Features | screened |  |
| 3.8 | coarse_only | `arxiv:2605.23035` | Sparse Autoencoders Map Brain-LLM Alignment onto Cortical Semantic Topography | screened |  |
| 3.6 | coarse_only | `arxiv:2605.28863` | Self-Play Reinforcement Learning under Imperfect Information in Big 2 | screened |  |
| 3.6 | coarse_only | `arxiv:2605.24048` | Mixture of Complementary Agents for Robust LLM Ensemble | screened |  |
| 3.6 | coarse_only | `arxiv:2605.23028` | RADAR: Relative Angular Divergence Across Representations | screened |  |
| 3.4 | coarse_only | `arxiv:2605.23032` | Brain-LLM Alignment Tracks Training Data, Not Typology | screened |  |
| 3.4 | coarse_only | `arxiv:2605.18233` | Enhancing Train-Free Infinite-Frame Generation for Consistent Long Videos | screened |  |
| 3.2 | coarse_only | `arxiv:2605.23007` | MadEvolve: Evolutionary Optimization of Trading Systems with Large Language Models | screened |  |
| 3.1 | detailed | `arxiv:2605.19008` | Learn-by-Wire Training Control Governance: Bounded Autonomous Training Under Stress for Stability and Efficiency | screened | Mismatch with target robotics/AI interests: paper focuses on LLM training stability, not on robot manipulation, VLA, world models, RL, diffusion models, or embodied AI., Evaluation limited to language modeling perplexity on a single dataset; no demonstration on robotics or embodied tasks., Method details are sparse in the excerpt, making it difficult to assess the control mechanism fully., Comparison only against gradient clipping; lacks comparison to other training stabilization techniques (e.g., loss spike recovery, adaptive clipping). |
| 2.9 | coarse_only | `arxiv:2605.23091` | Security of LLM-generated Code: A Comparative Analysis | screened |  |
| 2.9 | coarse_only | `arxiv:2605.23027` | PIMbot: A Self-Adaptive Attack Framework for Adversarial Manipulation of Multi-Robot Reinforcement Learning | screened |  |
| 1.9 | coarse_only | `arxiv:2605.20266` | A Survey of Large Audio Language Models: Generalization, Trustworthiness, and Outlook | screened |  |
| 1.4 | coarse_only | `arxiv:2604.27263` | Decoupling the Benefits of Subword Tokenization for Language Model Training via Byte-level Simulation | screened |  |
