---
tags:
  - 灵巧手专项
  - diffusion
  - dexterous_grasp
  - physical_constraints
  - literature
created: 2026-06-19
source_pdf: "[[灵巧手专项/物理约束分类.pdf]]"
---

# 灵巧手物理约束注入 Diffusion：近五年顶会/顶刊论文清单

> 检索时间：2026-06-19。  
> 筛选范围：近五年内的 CVPR / ECCV / ICRA / CoRL / NeurIPS / ICLR / RA-L / RSS / IJRR 等顶会顶刊或强相关高水平机器人会议论文。  
> 主题范围：优先选择“灵巧手 / dexterous grasp / dexterous manipulation + diffusion / score / flow / Schrödinger bridge + 物理约束 / 接触 / 碰撞 / 力封闭 / safety guidance”的论文。少数论文本身不是 diffusion，但提供了力封闭、接触、穿透等可微物理约束形式，因此作为“可借鉴的约束模块”列入。

## 0. 快速结论

如果你的目标是把 `[[灵巧手专项/物理约束分类.pdf]]` 里的 A/B/C/D 物理指标系统注入 Diffusion，最值得优先读的是下面四类工作：

1. **直接把物理约束写进 diffusion 训练和采样**：DexGrasp Anything。
2. **用 evaluator / discriminator / classifier guidance 引导 diffusion**：DexDiffuser、UGG。
3. **把接触、碰撞、力封闭设计成中间表征或优化能量**：CADGrasp、Contact Map Transfer、DexGraspNet、GraspQP、ContactOpt。
4. **通用约束 diffusion 理论**：SafeDiffuser、Constrained Diffusers。

最接近你现在问题的主线是：

```text
物理约束指标 E_phys(x)
→ 作为训练 loss / posterior sampling guidance / classifier guidance
→ 在 denoising 过程中加入 -∇E_phys(x)
→ 生成后再用物理优化器或仿真验证兜底
```

---

## 1. 核心论文表

| 序号  | 论文                                                                                                 | 年份/venue             | 与你问题的关系                                                                                       | 链接                                                                                                                                                                                                                                                                     |
| --- | -------------------------------------------------------------------------------------------------- | -------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | DexGrasp Anything: Towards Universal Robotic Dexterous Grasping with Physics Awareness             | CVPR 2025 Highlight  | 最直接：物理约束同时进入 diffusion 训练和 sampling                                                           | [arXiv](https://arxiv.org/abs/2503.08257), [CVF](https://openaccess.thecvf.com/content/CVPR2025/html/Zhong_DexGrasp_Anything_Towards_Universal_Robotic_Dexterous_Grasping_with_Physics_Awareness_CVPR_2025_paper.html), [Project](https://dexgraspanything.github.io/) |
| 2   | DexDiffuser: Generating Dexterous Grasps with Diffusion Models                                     | IEEE RA-L 2024       | 用 grasp evaluator 做 classifier-guided diffusion 和后验 refinement                                | [arXiv](https://arxiv.org/abs/2402.02989), [Project](https://yulihn.github.io/DexDiffuser_page/)                                                                                                                                                                       |
| 3   | UGG: Unified Generative Grasping                                                                   | ECCV 2024 Oral       | diffusion + contact anchors + physics discriminator + optimization                            | [arXiv](https://arxiv.org/abs/2311.16917), [Project](https://jiaxin-lu.github.io/ugg/), [ECCV](https://dl.acm.org/doi/10.1007/978-3-031-72855-6_24)                                                                                                                    |
| 4   | GAGrasp: Geometric Algebra Diffusion for Dexterous Grasping                                        | ICRA 2025            | SE(3) 等变约束 + differentiable physics-informed refinement                                       | [arXiv](https://arxiv.org/abs/2503.04123), [Project](https://gagrasp.github.io/)                                                                                                                                                                                       |
| 5   | CADGrasp: Learning Contact and Collision Aware General Dexterous Grasping in Cluttered Scenes      | NeurIPS 2025         | contact/collision-aware 表征 + occupancy diffusion + force closure score filtering              | [arXiv](https://arxiv.org/abs/2601.15039), [NeurIPS PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/2aff7a9ba2c654ad96e24f994c3f11bc-Paper-Conference.pdf), [Code](https://github.com/matthewmzy/CADGrasp)                                             |
| 6   | Contact Map Transfer with Conditional Diffusion Model for Generalizable Dexterous Grasp Generation | NeurIPS 2025         | 把 grasp 生成转成 contact map / part map / direction map 的条件扩散                                     | [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2025/hash/728a3f18902026dc60b7f7a84c7d2ce4-Abstract-Conference.html), [arXiv](https://arxiv.org/abs/2511.01276), [OpenReview](https://openreview.net/forum?id=ou9HeYvNhB)                                   |
| 7   | Grasp2Grasp: Vision-Based Dexterous Grasp Translation via Schrödinger Bridges                      | NeurIPS 2025         | score/flow matching + physics-informed costs：contact, wrench, manipulability                  | [arXiv](https://arxiv.org/abs/2506.02489), [Project](https://grasp2grasp.github.io/), [Code](https://github.com/n3il666/grasp2grasp)                                                                                                                                   |
| 8   | SceneDiffuser: Diffusion-based Generation, Optimization, and Planning in 3D Scenes                 | CVPR 2023            | 通用 3D scene diffusion，包含 dexterous grasp generation，强调 physics-based / goal-oriented guidance | [Project](https://scenediffuser.github.io/), [Paper](https://pku.ai/publication/scenediffusion2023cvpr/)                                                                                                                                                               |
| 9   | SafeDiffuser: Safe Planning with Diffusion Probabilistic Models                                    | ICLR 2025            | 用 control barrier functions 给 diffusion planning 安全约束保证                                       | [OpenReview](https://openreview.net/forum?id=ig2wk7kK9J), [arXiv](https://arxiv.org/abs/2306.00148), [Code](https://github.com/Weixy21/SafeDiffuser)                                                                                                                   |
| 10  | Constrained Diffusers for Safe Planning and Control                                                | NeurIPS 2025         | projected / primal-dual / augmented Lagrangian constrained Langevin sampling                  | [OpenReview](https://openreview.net/forum?id=tahkGZjjWA), [arXiv](https://arxiv.org/abs/2506.12544), [NeurIPS PDF](https://papers.nips.cc/paper_files/paper/2025/file/31fb284a0aaaad837d2930a610cd5e50-Paper-Conference.pdf)                                           |
| 11  | DexGraspNet: A Large-Scale Robotic Dexterous Grasp Dataset for General Objects Based on Simulation | ICRA 2023            | 不是 diffusion，但提供大规模灵巧手稳定抓取数据和可微力封闭 estimator                                                  | [Project](https://pku-epic.github.io/DexGraspNet/), [arXiv](https://arxiv.org/abs/2210.02697)                                                                                                                                                                          |
| 12  | GraspQP: Differentiable Optimization of Force Closure for Diverse and Robust Dexterous Grasping    | CoRL 2025            | 不是 diffusion，但提供严谨可微 QP 力封闭能量，可直接作为 C 类 guidance                                              | [arXiv](https://arxiv.org/abs/2508.15002), [Project](https://graspqp.github.io/), [Code](https://github.com/leggedrobotics/graspqp)                                                                                                                                    |
| 13  | ContactOpt: Optimizing Contact to Improve Grasps                                                   | CVPR 2021            | 不是 diffusion，但提供可微接触优化思想，可借鉴到 B/D 类约束                                                         | [CVF PDF](https://openaccess.thecvf.com/content/CVPR2021/papers/Grady_ContactOpt_Optimizing_Contact_To_Improve_Grasps_CVPR_2021_paper.pdf), [arXiv](https://arxiv.org/abs/2104.07267), [Code](https://github.com/facebookresearch/contactopt)                          |
| 14  | Diffusion Policy: Visuomotor Policy Learning via Action Diffusion                                  | RSS 2023 / IJRR 2024 | 动作 diffusion policy 基础；A 类动作平滑、能量、饱和率可注入此框架                                                   | [RSS](https://roboticsconference.org/2023/program/papers/026/), [arXiv](https://arxiv.org/abs/2303.04137), [Code](https://github.com/real-stanford/diffusion_policy)                                                                                                   |

---

## 2. 每篇论文的思路和可借鉴点

### 2.1 DexGrasp Anything, CVPR 2025 Highlight

**核心思路。** 这篇是目前最直接对应你问题的论文。论文明确说它把物理约束同时注入 diffusion 的训练阶段和采样阶段。它设计了三类物理约束：Surface Pulling Force, External-penetration Repulsion Force, Self-Penetration Repulsion Force。第一类让手的内表面靠近物体表面，第二类减少手和物体之间不合理穿透，第三类避免手自身结构发生自碰撞。论文还使用 clean sample estimation，把 noisy hand pose 映射成估计的干净手姿态后，在该估计上计算物理能量并反传。

**可借鉴点。**

1. 你的 B 类接触指标、D.3 穿透深度、A.4 关节限位可以类似地写成几何能量。
2. 不必只依赖 classifier；可直接定义可微物理能量 $E_{phys}(\hat x_0)$，在采样时加 $-\nabla E_{phys}$。
3. 训练和采样可以都注入：训练阶段让模型学习物理先验，采样阶段进一步用物理梯度修正。

**最值得复用的数学范式。**

$$
\tilde p(x|o)\propto p_\theta(x|o)\exp[-\lambda E_{phys}(x,o)]
$$

对应 guided score：

$$
\nabla_x\log \tilde p(x|o)
=
\nabla_x\log p_\theta(x|o)-\lambda\nabla_xE_{phys}(x,o).
$$

---

### 2.2 DexDiffuser, RA-L 2024

**核心思路。** DexDiffuser 包含两个模块：DexSampler 是条件 diffusion grasp sampler，DexEvaluator 判断一个抓取是否成功。推理时有两种 refinement：Evaluator-Guided Diffusion 和 Evaluator-based Sampling Refinement。Evaluator-Guided Diffusion 本质是 classifier-guided diffusion：在每一步反向扩散中，用 evaluator 对 grasp success 的梯度修正采样方向。

**可借鉴点。**

1. 你可以把 `[[灵巧手专项/物理约束分类.pdf]]` 中的指标组合成多头物理 evaluator：contact_good, lift_good, joint_safe, smooth, force_closure_good。
2. 对无法精确微分的物理指标，例如仿真成功率、扰动恢复成功率，可以离线生成标签，训练 evaluator 后做 classifier guidance。
3. 如果只用真实物理能量太贵，可以先走 evaluator guidance 路线。

**数学范式。**

若 evaluator 输出 $p_\psi(y=1|x,o)$，则条件采样可写成：

$$
\nabla_x\log p(x|o,y=1)
=
\nabla_x\log p(x|o)
+
\nabla_x\log p_\psi(y=1|x,o).
$$

---

### 2.3 UGG, ECCV 2024 Oral

**核心思路。** UGG 是 diffusion-based dexterous grasp generation。它引入 contact anchors 作为接触建模表征，并加入 physics discriminator 来筛选或推动更高成功率的抓取。其整体流程是：扩散模型生成多样 grasp，物理 discriminator 判断成功可能性，再利用 contact anchor 和点云进行优化。

**可借鉴点。**

1. 你的 B 类接触力学指标可以不直接预测完整手姿态，而先预测接触相关中间表征，例如 contact map / contact anchor。
2. 对灵巧手而言，接触位置比完整动作更低维、更稳定，适合作为 diffusion 的中间变量。
3. discriminator 不必是“糊弄式网络”，它可以被设计为物理指标的代理：输入 contact anchors、penetration、wrench features，输出成功概率。

---

### 2.4 GAGrasp, ICRA 2025

**核心思路。** GAGrasp 用 geometric algebra 表示来编码 SE(3) 等变性，并加入 differentiable physics-informed refinement layer。它的重点不是像 DexGrasp Anything 那样直接列出物理能量，而是把几何对称性本身作为硬结构约束，并在生成后用可微物理 refinement 修正。

**可借鉴点。**

1. 灵巧手抓取对物体坐标系旋转/平移应当具有 SE(3) 协变性；这本身就是一种物理几何约束。
2. 你的 diffusion 不一定只加 penalty，也可以把某些物理对称性直接编码进表示。
3. 对 A/D 类轨迹约束而言，可以考虑让约束在坐标变换下保持不变，例如相对物体坐标系下定义接触、提升、姿态误差。

---

### 2.5 CADGrasp, NeurIPS 2025

**核心思路。** CADGrasp 解决 cluttered scenes 中的通用灵巧手抓取。它提出 sparse IBS 作为 contact- and collision-aware intermediate representation，用 occupancy diffusion 预测这个表征，并用 force closure score filtering 和能量优化得到最终抓取。

**可借鉴点。**

1. 复杂物理约束不一定直接施加到动作序列上，可以先转成“物理友好的中间表征”。
2. contact-aware 和 collision-aware 可以被表征层编码，减少直接在高维动作空间做难优化。
3. C 类力封闭可以作为筛选/ranking，也可以作为采样后优化目标。

---

### 2.6 Contact Map Transfer with Conditional Diffusion, NeurIPS 2025

**核心思路。** 这篇把 dexterous grasp generation 改写成接触图迁移问题：从模板物体到新物体，条件 diffusion 生成 contact map、part map、direction map，并保持三者一致性。最后用 reliable contact points 做 grasp recovery。

**可借鉴点。**

1. 你的 B/C 类指标可以先在 object-centric map 上定义，而不是在 hand pose 上定义。
2. 对任务约束而言，part map / direction map 可表达“应该抓哪里”和“应该从哪个方向施力”。
3. 对于 D 类任务成功，例如“抓杯柄喝水”，接触图比动作序列更接近物理目标。

---

### 2.7 Grasp2Grasp, NeurIPS 2025

**核心思路。** Grasp2Grasp 用 Schrödinger Bridge / score matching / flow matching 做不同手型之间的 grasp translation，并设计物理启发的 cost：base pose alignment、contact maps、wrench space、manipulability。它不是传统 DDPM，但属于 score/flow generative modeling，和 diffusion guidance 思想非常接近。

**可借鉴点。**

1. 物理约束可以设计成“两个 grasp 的功能等价性 cost”，不仅是单个 grasp 的可行性。
2. contact map、wrench space、manipulability 三个 cost 很适合你的 B/C 类约束。
3. 如果将来你要从人手/Allegro/ShadowHand 之间迁移策略，这篇的物理 cost 设计很有价值。

---

### 2.8 SceneDiffuser, CVPR 2023

**核心思路。** SceneDiffuser 是 3D 场景条件 diffusion，覆盖 human pose、human motion、dexterous grasp generation、robot arm planning 等任务。它强调 scene-aware、physics-based、goal-oriented 的生成与优化。

**可借鉴点。**

1. 你可以把灵巧手约束拆成 scene constraints、physics constraints、goal constraints。
2. 对 D 类任务成功指标，例如目标位姿、提升高度、避障，可以写成 goal-oriented guidance。
3. 它提供了“生成 + 优化 + 规划”统一视角，不必把 diffusion 只看成一次性采样器。

---

### 2.9 SafeDiffuser, ICLR 2025

**核心思路。** SafeDiffuser 用 Control Barrier Function（CBF）给 diffusion planning 加安全保证，把 safety specification 嵌入反向扩散过程，提出 finite-time diffusion invariance。

**可借鉴点。**

1. A.4 关节限位、D.3 不穿透、动作饱和率等可以定义成安全集：

$$
\mathcal{S}=\{x:h(x)\ge 0\}.
$$

2. 采样过程中要求 denoising update 不离开安全集或逐步回到安全集。
3. 适合处理“绝对不能违反”的硬约束，比如关节限位、碰撞安全。

---

### 2.10 Constrained Diffusers, NeurIPS 2025

**核心思路。** 这篇提出不重训模型的 constrained Langevin sampling，把约束通过 projected method、primal-dual method、augmented Lagrangian 加入 reverse diffusion。它是非常适合你写理论章节的通用数学框架。

**可借鉴点。**

1. 对 ABCD 约束都可以写成：

$$
g_i(x)\le 0,\quad h_j(x)=0.
$$

2. 采样时用增广拉格朗日：

$$
\mathcal{L}_\rho(x,\lambda)
=
E(x)+\sum_i\lambda_i[g_i(x)]_+
+\frac{\rho}{2}\sum_i[g_i(x)]_+^2.
$$

3. 这比单纯 classifier guidance 更接近“数学约束优化”，适合你想要的严格推导路线。

---

### 2.11 DexGraspNet, ICRA 2023

**核心思路。** DexGraspNet 不是 diffusion，但它生成了大规模 ShadowHand 稳定抓取数据，并使用 deeply accelerated differentiable force closure estimator，所有抓取还经过 Isaac Gym 验证。

**可借鉴点。**

1. C 类力封闭指标的源头之一。
2. 可以借鉴其 differentiable force closure estimator 作为 diffusion guidance 的物理能量。
3. 你的 C.8 DFC energy 可以直接沿用这类思路。

---

### 2.12 GraspQP, CoRL 2025

**核心思路。** GraspQP 将 force closure 写成凸 QP，并通过 KKT 隐式微分得到可微能量。它的目标是生成多样且物理可行的灵巧手抓取。

**可借鉴点。**

1. 这是 C 类“力封闭”最值得借鉴的数学工具。
2. 与其用不可微凸包/Ferrari-Canny 指标，不如用 QP residual 作为连续可微 guidance。
3. 对 diffusion sampling，可令：

$$
E_{fc}(x)=\min_{\alpha\in\mathcal{K}}\|G(x)\alpha\|_2^2,
$$

再用 $-\nabla_xE_{fc}$ 引导生成。

---

### 2.13 ContactOpt, CVPR 2021

**核心思路。** ContactOpt 用可微接触模型优化手姿态，使预测的人手/物体接触更合理。它重点不是机器人 diffusion，而是“期望接触 → 可微优化 → 改善抓取”。

**可借鉴点。**

1. B 类接触点、接触面积、手物穿透可以写成几何可微 loss。
2. 可以借鉴“先预测 desired contact，再优化姿态满足 contact”的两阶段结构。
3. 对你的 D.3 穿透与 B 类接触持续性，可以用 SDF/mesh distance 构造可微能量。

---

### 2.14 Diffusion Policy, RSS 2023 / IJRR 2024

**核心思路。** Diffusion Policy 把机器人动作序列建模为条件 denoising diffusion，并采用 receding horizon control。它是动作 diffusion policy 的基础框架。

**可借鉴点。**

1. 你的 A 类指标正好作用在动作 chunk 上：平滑性、能量、饱和率、块间一致性。
2. 对动作 diffusion，最直接的物理约束注入就是在 action sequence 上加：

$$
E_A(a_{0:H-1})
=
\lambda_s\|D^2a\|^2+\lambda_e\sum_t\|a_t\|^2+\lambda_{sat}\sum_{t,j}[|a_{t,j}|-a_{\max}]_+^2.
$$

3. 这比先生成 grasp pose 再优化更接近你的“Diffusion Policy 引导”问题。

---

## 3. 按 ABCD 类别的论文映射

| 约束类别 | 最相关论文 | 可借鉴方法 |
|---|---|---|
| A 动作层指标 | Diffusion Policy, SafeDiffuser, Constrained Diffusers, Sentinel | action energy、smoothness、saturation、CBF、安全集、consistency |
| B 接触力学 | DexGrasp Anything, ContactOpt, UGG, Contact Map Transfer, CADGrasp | 接触点/接触图、surface pulling、penetration repulsion、contact anchors |
| C 抓取质量/力封闭 | DexGraspNet, GraspQP, Grasp2Grasp, CADGrasp | GWS、force closure QP、wrench-space cost、force-closure filtering |
| D 物体层/任务成功 | DexDiffuser, SceneDiffuser, SafeDiffuser, Constrained Diffusers | success evaluator、goal guidance、lift/pose constraints、CBF/AL constraints |

---

## 4. 对你最值得做的三条路线

### 路线 1：Energy-based Physics Guidance

适合你已经能写出显式物理公式的指标，例如动作平滑、关节限位、穿透、摩擦锥、力封闭 QP。

$$
x_{t-1}
\leftarrow
\text{Denoise}(x_t)
-\eta_t\nabla_{x_t}E_{phys}(\hat x_0(x_t)).
$$

代表论文：DexGrasp Anything, GraspQP, ContactOpt, Constrained Diffusers。

### 路线 2：Physics Classifier / Evaluator Guidance

适合不可微或仿真才知道的指标，例如 lift success、扰动鲁棒性、闭环成功率。

$$
\nabla_x\log p(x|success)
=
\nabla_x\log p(x)+\nabla_x\log p_\psi(success|x).
$$

代表论文：DexDiffuser, UGG。

### 路线 3：Physical Intermediate Representation

不直接生成高维动作，而先生成接触图、contact anchor、IBS、wrench features。

代表论文：UGG, CADGrasp, Contact Map Transfer, Grasp2Grasp。

这条路线适合 B/C 类约束，因为接触和力封闭天然是中间物理结构。

---

## 5. 推荐阅读顺序

如果你的目标是快速建立“物理约束注入 diffusion”的研究主线，我建议按以下顺序读：

1. **DexGrasp Anything**：直接回答“物理约束如何进入 diffusion”。
2. **DexDiffuser**：理解 evaluator-guided diffusion。
3. **Constrained Diffusers**：理解更严格的 constrained sampling 数学框架。
4. **GraspQP**：理解 C 类力封闭如何写成可微能量。
5. **ContactOpt / CADGrasp**：理解接触和碰撞如何作为几何约束。
6. **Diffusion Policy**：如果你的最终对象是动作序列，而不是静态 grasp pose，则补读。

