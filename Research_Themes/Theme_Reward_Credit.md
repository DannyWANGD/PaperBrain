---
theme_id: Theme_Reward_Credit
theme_title: "奖励建模与信用分配"
parent_keyword: "Reinforcement Learning"
updated_at: "2026-03-27"
---

# 🧭 奖励建模与信用分配（Theme_Reward_Credit）

## 🎯 主题定义
- 归属上位关键词：**Reinforcement Learning**
- 细分关注：reward model, reward shaping, credit assignment, value function, return decomposition, intrinsic reward, vlm reward, preference learning
- 标准标签参考：#Reinforcement_Learning

## 📊 主题仪表盘
- 总论文数：**21**
- 平均分：**7.57**
- 高频标签：#Reinforcement_Learning #Embodied_AI #Robot_Manipulation #World_Model #Foundation_Model #Sim2Real #LLM #VLA #Diffusion_Model #Human_Scene_Reconstruction

## 🆕 最近新增
- [[DreamerAD]] | 2026-03-25 | DreamerAD: Efficient Reinforcement Learning via Latent World Model for Autonomous Driving
- [[WildWorld]] | 2026-03-24 | WildWorld: A Large-Scale Dataset for Dynamic World Modeling with Actions and Explicit State toward Generative ARPG
- [[DreamPlan]] | 2026-03-17 | DreamPlan: Efficient Reinforcement Fine-Tuning of Vision-Language Planners via Video World Models
- [[PRIMO R1]] | 2026-03-16 | From Passive Observer to Active Critic: Reinforcement Learning Elicits Process Reasoning for Robotic Manipulation
- [[Simple Recipe Works]] | 2026-03-12 | Simple Recipe Works: Vision-Language-Action Models are Natural Continual Learners with Reinforcement Learning
- [[Emerging Extrinsic Dexterity in Cluttered Scenes via Dynamicsaware Policy Learning]] | 2026-03-10 | Emerging Extrinsic Dexterity in Cluttered Scenes via Dynamics-aware Policy Learning
- [[MetaWorldX]] | 2026-03-09 | MetaWorld-X: Hierarchical World Modeling via VLM-Orchestrated Experts for Humanoid Loco-Manipulation
- [[ACEBrain0]] | 2026-03-04 | ACE-Brain-0: Spatial Intelligence as a Shared Scaffold for Universal Embodiments

## ⭐ 核心论文 Top
- [[RISE]] | Score: 9/10 | 2026-02-11 | RISE: Self-Improving Robot Policy with Compositional World Model
- [[Simple Recipe Works]] | Score: 9/10 | 2026-03-12 | Simple Recipe Works: Vision-Language-Action Models are Natural Continual Learners with Reinforcement Learning
- [[ACEBrain0]] | Score: 8/10 | 2026-03-04 | ACE-Brain-0: Spatial Intelligence as a Shared Scaffold for Universal Embodiments
- [[DreamerAD]] | Score: 8/10 | 2026-03-25 | DreamerAD: Efficient Reinforcement Learning via Latent World Model for Autonomous Driving
- [[DreamPlan]] | Score: 8/10 | 2026-03-17 | DreamPlan: Efficient Reinforcement Fine-Tuning of Vision-Language Planners via Video World Models
- [[HydroShear]] | Score: 8/10 | 2026-02-28 | HydroShear: Hydroelastic Shear Simulation for Tactile Sim-to-Real Reinforcement Learning
- [[MetaWorldX]] | Score: 8/10 | 2026-03-09 | MetaWorld-X: Hierarchical World Modeling via VLM-Orchestrated Experts for Humanoid Loco-Manipulation
- [[Persistent_Robot_World_Models]] | Score: 8/10 | Unknown | Persistent Robot World Models: Stabilizing Multi-Step Rollouts via Reinforcement Learning
- [[PRIMO R1]] | Score: 8/10 | 2026-03-16 | From Passive Observer to Active Critic: Reinforcement Learning Elicits Process Reasoning for Robotic Manipulation
- [[TICVLA]] | Score: 8/10 | 2026-02-02 | TIC-VLA: A Think-in-Control Vision-Language-Action Model for Robot Navigation in Dynamic Environments
- [[ULTRA]] | Score: 8/10 | 2026-03-03 | ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation
- [[WildWorld]] | Score: 8/10 | 2026-03-24 | WildWorld: A Large-Scale Dataset for Dynamic World Modeling with Actions and Explicit State toward Generative ARPG

## ✅ 核心贡献与共识
- **[[RISE]]**（Score 9/10）：RISE is the first closed-loop self-improving robot RL framework that replaces physical interaction with a compositional controllable multi-view world model, enabling scalable on-policy policy optimization entirely in imaginary space to eliminate physical trial-and-error cost while outperforming SOTA...
- **[[Simple Recipe Works]]**（Score 9/10）：The paper demonstrates empirically and analytically that the synergy between a large pretrained VLA backbone, LoRA-based parameter-efficient adaptation, and on-policy reinforcement learning (GRPO) collectively suppresses catastrophic forgetting to near-zero levels, rendering simple Sequential Fine-T...
- **[[ACEBrain0]]**（Score 8/10）：This work introduces ACE-Brain-0, a generalist multimodal large language model for universal embodied intelligence that leverages spatial intelligence as a domain-agnostic shared scaffold, paired with the novel Scaffold-Specialize-Reconcile (SSR) training paradigm with data-free expert merging, to u...
- **[[DreamerAD]]**（Score 8/10）：DreamerAD提出了一个将强化学习完整嵌入视频扩散模型隐空间的框架，通过快捷强制蒸馏将世界模型采样从100步压缩至1步，并配合隐空间自回归稠密奖励建模与高斯词汇约束探索，实现了高效、物理合理的自动驾驶策略优化。
- **[[DreamPlan]]**（Score 8/10）：DreamPlan introduces an efficient offline RL fine-tuning framework that adapts VLM planners to complex real-world deformable object dynamics entirely within the imagination of an action-conditioned video diffusion world model, using Best-of-K sampling combined with ORPO-based preference optimization...

## ⚠️ 局限性与关键分歧
- **[[RISE]]**：**Latency and Scalability Bottlenecks**: The video diffusion dynamics model has ~2s generation latency for an H-step horizon, limiting throughput for large-scale parallel imaginary rollout.
- **[[Simple Recipe Works]]**：**Sparse reward dependence:** The stability-inducing property of on-policy RL is partly attributed to the sparse, binary reward signal limiting gradient scope.
- **[[ACEBrain0]]**：**Inference Latency**: The large LLM backbone delivers higher inference latency relative to task-specific embodied models, making it unsuitable for low-latency edge deployment use cases (e.g., high-speed UAV navigation requiring sub-10ms inference).
- **[[DreamerAD]]**：**评估泛化性受限**：DreamerAD仅在NavSim v2单一闭环基准上验证，该基准的驾驶场景分布、评估协议与真实世界存在领域差距。词汇库 $\Gamma$（$K=256$）和过滤阈值（$x_{thresh}=10\text{m}, y_{thresh}=5\text{m}$）均基于NavSim数据分布的人工设定，在复杂城市场景（如密集行人、非结构化道路）或极端气候条件下的适用性未经验证，且词汇库的静态性质使其难以覆盖长尾、紧急避险轨迹。
- **[[DreamPlan]]**：**Task scope and generalization**: All three evaluation tasks are pick-and-place variants executed by a fixed bimanual robot with a top-down camera.

## 🔀 跨论文引用网络
- [[Chain of World]] ← 被 [[Simple Recipe Works]], [[DreamPlan]], [[MetaWorldX]] 等 5 篇引用
- [[Xiaomi-Robotics-0]] ← 被 [[Simple Recipe Works]], [[TICVLA]], [[Memex]] 等 3 篇引用
- [[World_Action_Models_are_Zero_shot_Policies]] ← 被 [[Simple Recipe Works]], [[DreamerAD]], [[DreamPlan]] 等 3 篇引用
- [[RISE]] ← 被 [[HydroShear]], [[MetaWorldX]], [[Emerging Extrinsic Dexterity in Cluttered Scenes via Dynamicsaware Policy Learning]] 等 3 篇引用
- [[TICVLA]] ← 被 [[PRIMO R1]], [[Memex]] 等 2 篇引用
- [[DreamPlan]] ← 被 [[DreamerAD]] 等 1 篇引用
- [[Planning in 8 Tokens]] ← 被 [[DreamerAD]] 等 1 篇引用
- [[EmboAlign]] ← 被 [[DreamPlan]] 等 1 篇引用

## 🏛️ 领域里程碑工作（AI Enriched）
- 暂无

## 🚀 前沿信号雷达（AI Enriched）
- 暂无

## 🧬 体系化关联补充（AI Enriched）
- 暂无

## ❓ 开放性问题（AI Enriched）
- 暂无

## 🗺️ 主题关系可视化（AI Enriched）
_暂无_

## 🗓️ 本周推进建议（AI Enriched）
- [ ] 暂无

## 🔗 关联主题
- [[Theme_RL_Algorithms|强化学习算法]]
- [[Theme_VLA_Policy|VLA 策略学习与控制]]
