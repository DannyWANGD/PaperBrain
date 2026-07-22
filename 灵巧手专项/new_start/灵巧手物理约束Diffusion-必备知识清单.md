---
tags:
  - 灵巧手专项
  - dexterous_grasping
  - diffusion
  - physical_constraints
  - research_checklist
created: 2026-07-20
status: active
---

# 灵巧手物理约束 Diffusion：开题必备知识清单

> 目标：建立足以定义问题、判断文献、设计实验并与导师讨论的共同语言，而不是收集现成 idea。  
> 范围：机器人灵巧抓取、接触力学与控制、扩散/score 生成模型、物理约束、安全与实验方法。  
> 使用原则：只有当你能完成每节的“掌握标准”，才勾选该知识点；“看过论文”不等于掌握。

## 使用方法与优先级

- `P0`：开题前必须掌握；否则容易把研究对象、物理概念或贡献说错。
- `P1`：进入方法设计前掌握；决定方案是否可实现、实验是否有说服力。
- `P2`：确定具体路线后按需深入；不应在问题尚未定义时全部铺开。
- 每个模块先完成 `概念 -> 公式 -> 小例子 -> 代码/实验 -> 反例` 五步，再阅读大量前沿论文。

当前进度标记：`[ ] 未掌握`，`[-] 能复述但不能推导/实现`，`[x] 能推导、实现并说明边界`。

## 0. 先锁定“你究竟在研究什么” `[P0]`

灵巧手领域中，下列问题不能混为一谈：

| 问题 | 典型输出 | 物理时间 | 主要验证 |
|---|---|---:|---|
| 静态抓取姿态生成 | 手腕位姿 $T_{WH}$、关节角 $q$ | 无 | 几何、接触、静态平衡、仿真 lift |
| 接触/力联合抓取生成 | $(T_{WH},q,C,f)$ | 无 | 接触可实现、摩擦锥、平衡、力矩可行 |
| 抓取获取轨迹规划 | $	au=(x_{0:H},u_{0:H-1})$ | 有 | 碰撞、动力学、控制可跟踪、最终抓稳 |
| 闭环抓取策略 | $pi(a_t\mid h_t)$ | 有 | 观测误差、反馈频率、扰动恢复、真实执行 |
| 抓取后的在手操作 | 状态-动作-接触模式序列 | 有且接触切换 | 重抓、滚动/滑动、任务完成 |

- [ ] 能用一句话说清自己的任务属于哪一行，以及明确不研究哪几行。
- [ ] 能写出条件观测 $o$：已知 mesh、完整点云、单视角 RGB-D、物体位姿、任务语言、触觉、关节状态分别是否可用。
- [ ] 能写出模型输出 $x$ 的每个分量、维度、坐标系、单位和合法范围。
- [ ] 能区分物理时间 $t$ 与扩散去噪索引 $k$。去噪中间态通常不是机器人实际运动轨迹。
- [ ] 能区分 `grasp synthesis`、`grasp acquisition`、`dexterous manipulation` 与 `visuomotor policy learning`。
- [ ] 能解释为什么人手 MANO 姿态“看起来合理”不等于机器人手 URDF 上可执行。

**本节掌握标准：** 不看资料，写出如下研究接口并解释每个随机变量：

$$
p_\theta(x\mid o,c),\qquad
x\in\mathcal X,\qquad
\mathcal F(o,c,\xi)=\{x:g_i(x,o,c,\xi)\le 0,\ h_j(x,o,c,\xi)=0\},
$$

其中 $c$ 是任务条件，$\xi$ 是摩擦、质量、形状或感知误差等不确定物理参数。

## 1. 一张图掌握物理约束的层次 `[P0]`

| 层次 | 核心问题 | 典型变量/约束 | 不能推出什么 |
|---|---|---|---|
| 几何 | 手和物体摆得下吗 | 关节限位、自碰撞、手物穿透、环境碰撞 | 不能推出接触能承力 |
| 运动学 | 手到得了、动得了吗 | FK/IK、Jacobian、可达性、奇异性、闭链约束 | 不能推出动力学可执行 |
| 接触 | 接触允许传什么力/运动 | 单边接触、摩擦锥、粘着/滑动/分离、互补条件 | 不能推出整个物体平衡 |
| 抓取静力学 | 接触能否抵抗外部 wrench | grasp map、平衡、force closure、内力、关节力矩 | 不能推出真实闭环一定成功 |
| 动力学与控制 | 接近、碰撞、闭合、提起能否稳定执行 | 刚体动力学、冲击、柔顺、阻抗/力控、延迟 | 不能自动覆盖模型误差 |
| 不确定性与安全 | 模型不准时是否仍可靠 | robust/chance/CVaR、校准、扰动集、约束违例率 | 不能凭标称仿真宣称保证 |
| 任务与材料 | 是否完成正确且不损坏对象 | task wrench、可供性、压力/应力、扭矩/功耗 | 不能由通用 force closure 替代 |

- [ ] 对自己的候选课题逐层写出“状态、约束、可观测量、验证器”。
- [ ] 能指出每个约束是必要条件、充分条件、代理指标，还是纯经验相关量。
- [ ] 能给每个“安全”结论标注证据等级：经验统计、概率结论、模型内确定性保证、真实闭环保证。

## 2. 数学与机器人学工具箱 `[P0]`

### 2.1 线性代数、几何与 Lie 群

- [ ] 向量/矩阵微分、Jacobian、Hessian、SVD、零空间、条件数、特征值。
- [ ] 凸集、凸包、锥、对偶锥；知道摩擦锥为什么自然落在锥优化中。
- [ ] $SO(3)$ 与 $SE(3)$、指数/对数映射、twist、wrench、adjoint 变换。
- [ ] 旋转矩阵、四元数、轴角、6D rotation representation 的优缺点与归一化问题。
- [ ] 能检查一个 loss/距离是否随世界坐标系刚体变换保持不变或协变。

### 2.2 概率、统计与随机过程

- [ ] 条件概率、Bayes、边缘化、KL、交叉熵、最大似然、Monte Carlo。
- [ ] score $\nabla_x\log p(x)$、Langevin dynamics、Itô SDE、Fokker-Planck 的直观含义。
- [ ] aleatoric、epistemic 与 simulator/model bias 的区别。
- [ ] 置信区间、bootstrap、校准误差、可靠性图、分位数与尾部风险。
- [ ] 能解释“模型输出多样”与“对不确定物理参数稳健”是两件不同的事。

### 2.3 优化与约束

- [ ] 无约束/等式/不等式优化，Lagrangian、KKT、互补松弛、Slater 条件。
- [ ] QP、SOCP、非线性规划、投影、barrier、penalty、primal-dual、augmented Lagrangian。
- [ ] 隐式函数定理与通过优化层反向传播；知道 active set 改变时梯度可能不光滑。
- [ ] chance constraint、robust optimization、distributionally robust optimization、CVaR 的对象和假设。
- [ ] 能用一个二维例子画出：数据高密度区、可行集、投影结果以及约束边界。

### 2.4 动力系统与控制

- [ ] 刚体/多体动力学、Euler-Lagrange、状态空间、离散化与数值积分。
- [ ] 可控性、稳定性、Lyapunov 函数的基本概念。
- [ ] 位置、速度、力矩、力、阻抗/导纳、混合位置-力控制的区别。
- [ ] MPC/receding horizon：预测、只执行前缀、重新观测和再规划。
- [ ] 能解释一个“物理可行目标姿态”为何仍可能因控制带宽、饱和与冲击而失败。

## 3. 灵巧手本体、运动学与可执行性 `[P0]`

- [ ] 区分手的关节自由度、独立执行器数、欠驱动、腱驱动、耦合与 synergy。
- [ ] 理解 URDF/MJCF 中 link、joint、collision mesh、inertial、transmission/actuator 的含义。
- [ ] 写出多指 FK：$p_i=f_i(q)$；写出速度关系 $\dot p_i=J_i(q)\dot q$。
- [ ] 理解手腕 6-DoF 与指关节构成的完整构型空间，明确是否还包含机械臂。
- [ ] 掌握 joint limit、自碰撞、环境碰撞、可达性、奇异位形与 manipulability。
- [ ] 理解 hand Jacobian 将接触力映射到关节力矩：$\tau=J_h(q)^\top f$。
- [ ] 知道位置控制手与力矩控制手对“可执行抓取”的定义不同。
- [ ] 了解至少两种真实手型或仿真手型的差异，例如 Shadow Hand、Allegro、LEAP Hand，而不是把一种手的结论默认迁移到全部手型。

**本节掌握标准：** 给定一个手的 URDF/MJCF，能程序化读取关节范围、计算指尖 FK/Jacobian、做自碰撞查询，并说明控制接口和真实传感器可获得什么。

## 4. 物体、场景几何与感知 `[P0/P1]`

- [ ] 区分 mesh、point cloud、voxel、occupancy、SDF/TSDF、NeRF/3D Gaussian 对接触查询的适用性。
- [ ] 掌握点到面距离、signed distance、表面法向、最近点、连续/离散碰撞检测。
- [ ] 理解非 watertight mesh、薄物体、凹物体、尺度和单位错误为何会破坏 SDF/穿透指标。
- [ ] 区分 object-centric、hand-centric、world frame，保证训练、物理求解和执行坐标一致。
- [ ] 理解完整 CAD 与单视角部分点云之间的任务难度差异；遮挡区域不是已知自由空间。
- [ ] 掌握 6D object pose、尺度、质量、质心、惯量、摩擦、柔性/脆弱性中哪些被观测，哪些只是仿真假设。
- [ ] 了解视觉、proprioception、触觉、关节力矩/电流、力-力矩传感器的噪声、延迟和标定。
- [ ] 能给感知误差建立可实验扫描的扰动模型，而不是只加未定义的 Gaussian noise。

## 5. 接触力学：抓取研究的核心语法 `[P0]`

### 5.1 接触模型

- [ ] 区分 point contact without friction、point contact with friction、soft-finger contact。
- [ ] 单边接触：间隙 $\phi(q)\ge 0$、法向力 $f_n\ge 0$。
- [ ] 互补关系：$\phi(q)f_n=0$，并解释分离和接触两个模式。
- [ ] Coulomb 摩擦：$\|f_t\|_2\le\mu f_n$；理解圆锥与多面锥近似的精度/速度取舍。
- [ ] 区分静摩擦、动摩擦、扭转摩擦、滚动摩擦；知道真实材料中的摩擦并非常数。
- [ ] 区分 sticking、sliding、rolling、separating 及其速度/力条件。
- [ ] 理解刚性接触、compliant contact、冲量接触模型的适用条件。

### 5.2 接触数值问题

- [ ] 理解碰撞检测给出的 contact point/normal 对 mesh 分辨率和 solver 参数敏感。
- [ ] 了解 LCP/NCP、QP/SOCP、penalty/soft contact 等求解方式的基本差异。
- [ ] 知道接触 active set 与 stick-slip 切换会造成目标/梯度不连续。
- [ ] 不把某个 simulator 的接触力直接当成真实真值；能列出 timestep、solver、摩擦锥、stiffness/damping 等敏感参数。

**本节掌握标准：** 对单个指尖压在平面上的例子，分别写出分离、粘着、滑动的约束，并说明法向力和切向力由什么决定。

## 6. 抓取静力学、质量与“稳定”的边界 `[P0]`

### 6.1 两个最重要的映射

接触力经 grasp map 变成物体 wrench：

$$
w=Gf,\qquad
G_i=\begin{bmatrix}I\\[p_i-c]_{\times}\end{bmatrix}
$$

接触力经 hand Jacobian 变成关节力矩：

$$
\tau=J_h(q)^\top f.
$$

- [ ] 能解释 $G$ 处理“力对物体做了什么”，$J_h^\top$ 处理“手需要付出多少关节力矩”。
- [ ] 能写出特定外部 wrench 下的静态平衡：$Gf+w_{ext}=0$。
- [ ] 能把摩擦锥、法向力上下界、关节力矩上下界一起放进一个可行性问题。
- [ ] 理解 internal force 位于 $G$ 的零空间：它不改变物体净 wrench，但会改变夹持与损伤风险。
- [ ] 能解释 $\operatorname{rank}(G)=6$ 通常只是必要检查；若允许的接触力受单边性和摩擦锥限制，满秩本身不是 force closure 的充分条件。

### 6.2 必须严格区分的概念

- [ ] `equilibrium`：对某个给定 $w_{ext}$ 存在平衡接触力。
- [ ] `force closure`：在给定接触/摩擦模型与力界假设下，可抵抗一类（理想定义中任意方向）外部 wrench。
- [ ] `form closure`：主要由几何/单边约束消除物体自由运动，不等于带摩擦的 force closure。
- [ ] `caging`：物体被拓扑限制在有界区域，不一定持续接触，也不等于 immobilization。
- [ ] `grasp quality`：$\epsilon/Q_1$、最小奇异值、wrench-space volume、扰动裕度等是不同代理，排序可能不一致。
- [ ] `stable grasp`：必须说明是静态可行、扰动后仿真不掉落、动态/Lyapunov 稳定，还是经验成功率。

### 6.3 重要反例

- [ ] 能解释 force closure 为何不保证：无穿透、关节可达、力矩可行、接近轨迹存在、控制器能建立接触、未知摩擦下不滑、物体不损伤。
- [ ] 能解释只减小 hand-object distance 为何可能产生“贴得很近但没有有效对向接触”的姿态。
- [ ] 能解释只优化单一质量指标为何容易牺牲多样性或收敛到 power grasp。

**本节掌握标准：** 手算或用小型 QP 判断一个平面二指抓取在给定 $\mu$、外力和力界下是否平衡，再改变 $\mu$ 和外力画出可行域变化。

## 7. 从静态抓取到真实执行 `[P1]`

- [ ] 区分 pregrasp、approach、first contact、closure、lift、hold、task execution 各阶段。
- [ ] 写出含接触力的多体动力学框架：

$$
M(q)\ddot q+C(q,\dot q)+g(q)=\tau+J_c(q)^\top f_c.
$$

- [ ] 理解碰撞冲击、接触建立顺序、闭合速度、过冲和结构柔顺性。
- [ ] 掌握 impedance/compliance 对感知误差和提前接触的作用。
- [ ] 理解 position target、velocity、torque、fingertip wrench 作为 action space 的差异。
- [ ] 理解 controller trackability：生成轨迹的速度、加速度、jerk、扭矩和带宽约束。
- [ ] 了解触觉用于 contact localization、法向/剪切力估计、slip detection 与闭环调节的基本链路。
- [ ] 能列出开环静态 grasp 在真实执行中的失败树，而不是只记录 success/fail。

## 8. 不确定性、鲁棒性与安全 `[P1]`

- [ ] 列出不确定量：物体位姿/形状/法向、摩擦、质量/质心、手标定、控制延迟、触觉偏置。
- [ ] 区分 nominal constraint、worst-case robust constraint、chance constraint、CVaR/尾部风险。
- [ ] 知道概率约束依赖 $p(\xi\mid o)$ 的质量；未校准后验不能产生可信概率保证。
- [ ] 理解 domain randomization 是训练/评估手段，不自动等于 distributional robustness。
- [ ] 区分 constraint satisfaction、collision avoidance、grasp stability 与 object safety/damage。
- [ ] 对每项“安全保证”写清：假设、适用状态、离散误差、solver 误差、感知误差和闭环条件。
- [ ] 能设计 controlled stress test：单独扫描摩擦、位姿、质量、法向噪声、延迟，而非只报平均随机化成功率。

## 9. 扩散与 score-based 生成模型 `[P0]`

### 9.1 DDPM 基础

- [ ] 前向加噪与闭式采样：

$$
q(x_k\mid x_0)=\mathcal N\!\left(\sqrt{\bar\alpha_k}x_0,(1-\bar\alpha_k)I\right),
\quad
x_k=\sqrt{\bar\alpha_k}x_0+\sqrt{1-\bar\alpha_k}\epsilon.
$$

- [ ] 理解 $\epsilon$-prediction、$x_0$-prediction、$v$-prediction、score prediction 的转换。
- [ ] 理解 reverse kernel、noise schedule、DDPM 与 DDIM、随机与确定采样。
- [ ] 能从 denoising score matching 解释为何网络在学习扰动分布的 score。
- [ ] 理解 MSE 最优的 clean estimate 是后验均值 $\hat x_0(x_k)=\mathbb E[x_0\mid x_k]$，并非“本次采样最终一定到达的 clean sample”。
- [ ] 能解释对非线性接触/碰撞函数，通常 $F(\mathbb E[x_0\mid x_k])\ne\mathbb E[F(x_0)\mid x_k]$；两个有效抓取模式的均值也可能无效。
- [ ] 理解连续时间 forward SDE、reverse-time SDE 与 probability-flow ODE 的关系。
- [ ] 知道采样步数、数值误差、训练/采样 schedule 不匹配的影响。

### 9.2 条件生成与 guidance

- [ ] 条件模型 $p_\theta(x\mid o,c)$ 中，哪些条件在训练时可用、测试时可得。
- [ ] 区分 classifier guidance、classifier-free guidance 与任意能量梯度 guidance。
- [ ] 对能量重加权目标：

$$
\tilde p(x\mid o)\propto p_\theta(x\mid o)\exp[-\lambda E_{phys}(x,o)],
$$

能推得形式上的 score：

$$
\nabla_x\log\tilde p=\nabla_x\log p_\theta-\lambda\nabla_xE_{phys}.
$$

- [ ] 能说明该 clean-distribution 等式本身不保证离散 sampler 最终满足硬约束，也不保证 $E_{phys}$ 是校准似然。
- [ ] 理解真正的 noisy marginal 修正涉及后验期望

$$
\nabla_{x_k}\log \mathbb E\!\left[\exp(-\lambda E_{phys}(x_0))\mid x_k\right],
$$

而常用的 $-\lambda\nabla_{x_k}E_{phys}(\hat x_0(x_k))$ 是 plug-in 近似；二者一般不相等。
- [ ] 理解在 noisy $x_k$ 上直接算接触力学常无物理意义；需要明确约束作用于 $x_k$、预测的 $\hat x_0$，还是整条物理轨迹。
- [ ] 若约束作用于 $\hat x_0(x_k)$，能正确处理链式梯度而不是把 $\hat x_0$ 当常量。

### 9.3 机器人输出空间的特殊问题

- [ ] 明确扩散对象是静态姿态、接触图、力、状态轨迹还是 action chunk。
- [ ] 了解对 $SO(3)/SE(3)$、关节周期变量直接加欧氏 Gaussian noise 的问题。
- [ ] 了解 equality-constrained/lower-dimensional manifold 在连续空间中可能是零测集。
- [ ] 了解接触模式是离散变量、姿态/力是连续变量时产生的 hybrid distribution。
- [ ] 理解数据多模态来自抓取类型、接触组合、对称性和任务策略，不只是随机噪声。
- [ ] 能回答：如果任务只需要一个最优解，为什么不用优化器/回归器而必须用 diffusion？

**本节掌握标准：** 在二维 toy data 上训练一个条件 DDPM，并分别实现无 guidance、软能量 guidance、投影；比较可行率、分布偏差、多样性与计算量。

## 10. 物理约束可以进入生成系统的哪些位置 `[P0/P1]`

这是中性方法分类，不是研究路线推荐：

| 位置 | 做法 | 优点 | 主要风险/必须验证 |
|---|---|---|---|
| 数据层 | 物理优化/仿真筛选数据 | backbone 简单 | 数据偏差、覆盖不足、验证器泄漏 |
| 表示层 | 接触图、SDF、wrench、相对坐标、对称性 | 降低学习难度 | 中间表征是否足够、恢复是否可行 |
| 训练层 | physics loss、辅助头、联合预测 | 可内化先验 | 权重冲突、代理偏差、约束仍非硬满足 |
| 采样层 | classifier/energy guidance | 可插拔、可控 | 梯度尺度、局部极值、分布扭曲 |
| 约束采样层 | projection、primal-dual、AL、barrier | 更直接处理可行集 | 非凸/不光滑、计算与近似保证 |
| 后处理 | QP/NLP/refinement/filter/ranking | 易落地、验证清楚 | 生成器未学物理、失败/耗时可能很高 |
| 闭环执行层 | 触觉/状态反馈后重规划或控制修正 | 应对现实误差 | 实时性、稳定性、训练-执行接口 |

- [ ] 对一种方法同时写出其 `target distribution`、约束作用变量、梯度/求解器、输出分布变化和验证器。
- [ ] 区分 soft preference $E(x)$ 与 hard feasible set $x\in\mathcal F$。
- [ ] 区分在每个去噪步“数值上减少 violation”与“最终样本满足约束”的结论。
- [ ] 检查 equality、inequality、离散模式、黑盒 simulator constraint 是否被同一种工具粗暴处理。
- [ ] 分析多个约束的单位、梯度范数、冲突、优先级和 Pareto trade-off。
- [ ] 检查物理修正是否造成 mode collapse，尤其是否把 precision/pinch 全部推成 power grasp。
- [ ] 检查精确物理 oracle 的调用次数、梯度稳定性、batch/GPU 可并行性和 wall-clock。

## 11. 学习范式与强基线 `[P1]`

- [ ] 优化式 grasp synthesis：直接优化接触、姿态和力；理解它何时比生成模型更合理。
- [ ] 判别/回归、CVAE、GAN、normalizing flow、autoregressive/masked model、diffusion/flow matching 的基本取舍。
- [ ] imitation learning、offline RL、online RL、model-based planning 的数据与闭环假设。
- [ ] static grasp generator、trajectory diffuser 与 Diffusion Policy 的训练样本/部署接口差异。
- [ ] 对任何 diffusion 方案至少设置一个非 diffusion 强基线，防止把收益错误归因于“扩散”。
- [ ] 知道公正比较应统一数据、输入、输出、物理 refinement 预算和候选样本数。

## 12. 数据、仿真、真实系统与复现 `[P1]`

### 12.1 数据问题

- [ ] 区分优化合成、仿真 rollout、遥操作/人类示范、真实机器人试验数据。
- [ ] 检查 object split 是 unseen instance 还是 unseen category，避免同 mesh/近重复 mesh 泄漏。
- [ ] 检查 grasp label 来自解析指标、仿真 lift、扰动测试还是真实成功。
- [ ] 检查数据是否只覆盖完整 mesh、固定手型、固定摩擦和固定重力。
- [ ] 掌握 DexGraspNet 的数据生成和验证逻辑，而不只是样本数量。

| 资源 | 主要覆盖 | 使用时必须记住的边界 |
|---|---|---|
| DexGraspNet 1.0 | 单物体、完整几何、ShadowHand、大规模静态抓姿 | 不含 approach/close 轨迹，仿真稳定不等于真实可执行 |
| DexGrasp Anything dataset | 更多对象上的大规模静态抓姿 | 仍需核对手型、物理生成器和统一评测设置 |
| DexGraspNet 2.0 | 单视角、clutter scene、大规模候选抓姿 | 与 1.0 的完整单物体任务不能直接横比 |
| RealDex | 真实遥操作、多视角/多模态手物交互 | 人手式数据/重定向不自动满足目标机器人力学 |
| GraspQP dataset | 多手型、多 grasp type、强调严格 force closure 与多样性 | 其解析模型和扰动协议仍需与自己的执行环境独立验证 |

### 12.2 仿真器不是“物理真值”

- [ ] 至少熟悉 MuJoCo 或 Isaac Lab/PhysX 中手模型、接触、摩擦、solver、timestep、actuator 与 sensor 配置。
- [ ] 记录 mesh 预处理、碰撞体简化、mass/inertia、friction、contact stiffness/damping、solver iterations。
- [ ] 做 timestep/solver/contact 参数敏感性分析，并保存可复现实验配置。
- [ ] 了解仿真接触模型与解析 force-closure 模型不一致时，指标为何会冲突。

### 12.3 真实实验

- [ ] 标定相机-机器人、指尖/触觉、关节零位、力矩/电流映射和控制延迟。
- [ ] 预先定义 success、failure taxonomy、重置方法、每对象试验次数与停止规则。
- [ ] 同时报告看得见的失败，而不是只展示挑选视频。
- [ ] 将仿真随机化范围与真实测得范围对应起来。

### 12.4 与本课题直接相关的 Sim2Real / 真机迁移底座（核查于 2026-07-20）

先区分三个容易混淆的标签：

- **真机部署**：模型能在真实机器人上运行，但训练数据可能来自真实示范。
- **Sim2Real**：训练主要或完全在仿真中完成，再迁移到真实机器人；需要说明是否使用真实微调。
- **安全部署**：除了平均成功率，还要说明约束、监测、恢复和失效边界；有真机视频不等于有安全保证。

| 项目 | 任务与迁移证据 | 代码成熟度 | 对本课题可迁移的部分 | 不能直接继承的能力 |
|---|---|---|---|---|
| [DP3 / 3D Diffusion Policy](https://github.com/YanjieZe/3D-Diffusion-Policy)（RSS 2024） | 点云与本体状态到 action chunk；提供 Franka + Allegro + RealSense L515 的真实数据格式和部署说明 | 高：训练、仿真任务、真实数据和适配接口较完整 | 最适合作为轨迹级 Diffusion 主干 | 原始真机灵巧手实验使用真实示范，不是现成的零样本 Sim2Real；没有接触安全保证 |
| [ClutterDexGrasp](https://clutterdexgrasp.github.io/)（CoRL 2025 Oral） | 仿真 RL teacher 经安全课程训练，再蒸馏为部分点云条件 DP3 student，零样本迁移到真实杂乱场景 | 低：截至核查日期，公开仓库主要只有 README 与媒体文件，安装和使用部分为空 | 最接近本课题的系统级参考；必须正面对比其“安全数据/教师 -> Diffusion -> Sim2Real”范式 | 不能作为当前可直接复现的代码底座；其安全主要来自 teacher curriculum 和数据分布，不是 student 去噪中的显式约束 |
| [DexGraspNet 2.0](https://pku-epic.github.io/DexGraspNet2.0/)（CoRL 2024） | 局部几何条件的静态 grasp diffusion；报告零样本 Sim2Real 与真实杂乱抓取 | 中至高：项目、数据与代码公开 | 适合静态抓姿生成分支和视觉 Sim2Real 基线 | 不生成完整 approach-close-lift 轨迹，也不是闭环接触安全方法 |
| [Blind Dexterous Grasping via Real2Sim2Real Tactile Policy Learning](https://arxiv.org/abs/2606.11767)（2026 预印本） | 真实接触事件校准仿真，RL experts 生成轨迹，再蒸馏为触觉条件 Diffusion Policy；LEAP 真机总体成功率 27% | 低：未核实到完整公开代码 | 与“触觉 + Diffusion + Sim2Real”最接近，适合作为必须覆盖的最新 prior art 和失败证据 | 当前性能和复现条件不足，且没有显式安全约束 |
| [PP-Tac](https://peilin-666.github.io/projects/PP-Tac/)（RSS 2025） | 合成抓取轨迹训练触觉 Diffusion Policy，再迁移到真实手臂-灵巧手；纸状物任务报告 87.5% | 中：传感器 CAD、BOM、标定与源码公开，但需自行核对完整策略训练/部署链路 | 适合研究触觉条件、滑移反馈与高频真实执行 | 任务限定在薄、平、可变形物体，不能直接外推到通用刚体抓取 |
| [SafeDiffuser](https://github.com/Weixy21/SafeDiffuser)（ICLR 2025） | 用 CBF 约束 diffusion planning；包含 Maze、MuJoCo locomotion 和 PyBullet KUKA | 中：算法代码公开，但环境依赖较旧 | 适合作为“约束进入去噪过程”的算法基线 | 没有灵巧手、多接触不确定性或 Sim2Real 证据，不能直接作为真机系统 |
| [BODex / DexGraspBench](https://pku-epic.github.io/BODex/) 与 [GraspQP](https://graspqp.github.io/) | QP/force-closure 抓取合成、仿真扰动与数据评测；BODex 报告 Shadow Hand 真机 lift | 高至中：代码和数据公开 | 适合修复/筛选专家数据、构造终端静力学约束和独立 evaluator | 它们不是轨迹 Diffusion，也不保证真实动态闭环中不滑落 |
| [CoorGrasp](https://ada-grasp-ctrl.github.io/) 与 [TacDexGrasp](https://arxiv.org/abs/2603.07040) | 真实多指触觉反馈下的协调接触控制、MPC/SOCP 力分配与防滑 | 中至低：CoorGrasp 有公开仿真代码；TacDexGrasp 尚未核实到完整代码 | 适合作为 Diffusion 下方的真实执行/安全层，而非替代 Diffusion | 依赖专用触觉、准静态/接触等假设；经验成功不等于端到端形式保证 |
| [TacSL](https://iakinola23.github.io/tacsl/) | GPU 触觉仿真和零样本触觉 Sim2Real 基础设施 | 中 | 若选择触觉路线，可用于建立仿真触觉、标定和随机化管线 | 不是多指抓取 Diffusion，也不提供摩擦锥或抓取安全保证 |

当前最值得采用的不是单个项目，而是明确分层的迁移栈：

```text
DP3：可运行的轨迹 Diffusion 主干
  + BODex/GraspQP：专家数据审计、终端接触与静力学可行性
  + 显式约束去噪：本课题需要研究的核心算法层
  + CoorGrasp/TacDexGrasp 式控制器：真实执行时独立的触觉/QP/MPC 安全层
  + 系统辨识与 domain randomization：Sim2Real 证据链
```

ClutterDexGrasp 是最重要的系统级先验：仅做“安全 curriculum 产生专家数据，再蒸馏 DP3 并迁移真机”已经不新。真正需要回答的是：显式物理约束为何必须进入 Diffusion 去噪，面对摩擦、质量、接触位置、传感误差和执行延迟的不确定性时，比安全数据筛选、采样后 QP 修复和低层安全控制器多解决了什么。

- [ ] 选底座前记录真实手型、机械臂、相机、触觉、控制频率和仿真器，并逐项核对接口，而非只比较论文成功率。
- [ ] 将“部署可用性”和“论文新颖性”分别评分；最接近的论文通常是必须击败的 prior art，不一定是最好改代码的仓库。
- [ ] 真机实验保留独立 runtime safety layer；不能让未经校准的 Diffusion sampler 成为唯一安全机制。
- [ ] 若运行时安全层修复了大部分失败，必须做消融，避免把控制器收益错误归因于约束去噪。

## 13. 评价协议：让实验真正击中论文主张 `[P0/P1]`

### 13.1 五组互补指标

- [ ] 几何/运动学：penetration depth/volume、self-collision、joint-limit、可达率。
- [ ] 接触/静力学：接触覆盖、摩擦锥违例、平衡残差、force-closure/Q1、力矩可行率。
- [ ] 仿真/真实执行：lift/hold/task success、slip、object displacement、峰值力/扭矩、扰动恢复。
- [ ] 生成质量：有效样本率、成功样本 diversity/coverage、抓取类型与接触模式覆盖。
- [ ] 系统代价：采样延迟、denoising steps、物理 oracle/QP 次数、显存、闭环频率。

### 13.2 泛化与压力测试轴

- [ ] unseen object instance/category、尺度、初始位姿、遮挡、clutter。
- [ ] 未知摩擦、质量/质心、表面法向、形状/位姿误差、控制延迟。
- [ ] hand embodiment、控制模式、任务 wrench、材料柔顺/脆弱性。
- [ ] 平均表现之外报告最差分位数、CVaR 或 violation calibration。

### 13.3 论文证据链

- [ ] 每项实验只支撑一个明确 claim；每个主要 claim 都有对应实验或定理。
- [ ] ablation 拆“机制”而不只是拆网络模块。
- [ ] 与 baseline 对齐输入、候选数、refinement 时间和物理信息。
- [ ] 同时报告 single-sample 与 best-of-$N$；“生成很多再选最好”不能和单次输出直接比较。
- [ ] 报告多随机种子、置信区间和统计单位（sample/object/episode）。
- [ ] 同时给出 success-safety-diversity-compute 的 Pareto 曲线，而非只挑一个阈值。
- [ ] 预注册或至少在实验前写出关键失败条件，防止事后挑指标。

## 14. 必读资料：按“基础 -> 桥接 -> 前沿”阅读 `[P0/P1]`

### 14.1 机器人与接触基础

1. Lynch & Park, [Modern Robotics, Chapter 12: Grasping and Manipulation](https://modernrobotics.northwestern.edu/chapters/chapter12/)：先建立 contact kinematics、contact forces、form/force closure 的统一语言。
2. Murray, Li & Sastry, [A Mathematical Introduction to Robotic Manipulation](https://www.cds.caltech.edu/~murray/mlswiki/)：重点看刚体运动、Jacobian、多指手静力学、force closure、手动力学与控制。
3. MIT Underactuated Robotics, [The Dynamics of Contact](https://underactuated.mit.edu/contact.html)：补互补约束、摩擦与接触动力学。
4. MuJoCo, [Computation](https://mujoco.readthedocs.io/en/stable/computation/)：理解仿真器实际怎样处理 contact/constraint，而非把仿真当黑盒。

按需精读：Bicchi, [On the Closure Properties of Robotic Grasping](https://doi.org/10.1177/027836499501400402)；Roa & Suárez, [Grasp Quality Measures: Review and Performance](https://link.springer.com/article/10.1007/s10514-014-9402-3)；Hogan, [Impedance Control](https://doi.org/10.1115/1.3140702)。

### 14.2 扩散理论基础

5. Ho et al., [Denoising Diffusion Probabilistic Models](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html), NeurIPS 2020。
6. Song et al., [Score-Based Generative Modeling through Stochastic Differential Equations](https://openreview.net/forum?id=PxTIG12RRHS), ICLR 2021。
7. Song et al., [Denoising Diffusion Implicit Models](https://openreview.net/forum?id=St1giarCHLP), ICLR 2021。

### 14.3 机器人扩散桥接

8. Chi et al., [Diffusion Policy](https://diffusion-policy.cs.columbia.edu/), RSS 2023 / IJRR：动作序列扩散、视觉条件与 receding-horizon policy。
9. Huang et al., [SceneDiffuser](https://openaccess.thecvf.com/content/CVPR2023/html/Huang_Diffusion-Based_Generation_Optimization_and_Planning_in_3D_Scenes_CVPR_2023_paper.html), CVPR 2023：区分生成、物理优化与规划。
10. Xiao et al., [SafeDiffuser](https://openreview.net/forum?id=ig2wk7kK9J), ICLR 2025；Zhang et al., [Constrained Diffusers](https://proceedings.neurips.cc/paper_files/paper/2025/hash/31fb284a0aaaad837d2930a610cd5e50-Abstract-Conference.html), NeurIPS 2025：理解“安全/约束扩散”的假设与保证边界。

### 14.4 灵巧抓取代表工作

11. Wang et al., [DexGraspNet](https://pku-epic.github.io/DexGraspNet/), ICRA 2023：大规模仿真抓取数据与可微抓取能量。
12. Lu et al., [UGG](https://eccv.ecva.net/virtual/2024/poster/1261), ECCV 2024：联合对象、手与接触的扩散式生成。
13. Weng et al., [DexDiffuser](https://yulihn.github.io/DexDiffuser_page/), RA-L 2024：生成器、evaluator guidance 与 refinement。
14. Zhong et al., [DexGrasp Anything](https://openaccess.thecvf.com/content/CVPR2025/html/Zhong_DexGrasp_Anything_Towards_Universal_Robotic_Dexterous_Grasping_with_Physics_Awareness_CVPR_2025_paper.html), CVPR 2025：训练与采样中的几何物理约束，是必须正面对比的直接基线。
15. Chen et al., [SpringGrasp](https://www.roboticsproceedings.org/rss20/p042.html), RSS 2024：形状不确定性、compliant grasp 与真实执行。
16. Zurbrügg et al., [GraspQP](https://proceedings.mlr.press/v305/zurbrugg25a.html), CoRL 2025：通过 QP 构造严格可微的 force-closure 能量与多样抓取。
17. Liang et al., [DexHandDiff](https://openaccess.thecvf.com/content/CVPR2025/html/Liang_DexHandDiff_Interaction-aware_Diffusion_Planning_for_Adaptive_Dexterous_Manipulation_CVPR_2025_paper.html), CVPR 2025：提醒我们状态轨迹中的“物理交互”与静态抓取约束不同。

阅读每篇论文时必须填写：`任务与输出变量 / 物理假设 / 约束作用位置 / baseline / 证据 / 未覆盖失败 / 能否迁移到我的设置`。

## 15. 最小学习闭环 `[P0]`

不要先尝试完整灵巧手系统。按下列门槛推进：

### Gate A：二维接触与抓取

- [ ] 二维二指/三指物体，手算 grasp map、摩擦锥和平衡。
- [ ] 用 QP 求给定外力下的接触力，扫描 $\mu$ 与接触位置。
- [ ] 给出至少一个“force closure 指标好但执行失败”的反例。

### Gate B：toy constrained diffusion

- [ ] 在二维多峰数据上训练 DDPM。
- [ ] 加入软能量、投影和后处理三种约束方式。
- [ ] 画出有效率、分布偏差、模式覆盖和运行时间，而非只看散点图。

### Gate C：单手型静态 baseline

- [ ] 固定一个手型、一个数据集和一种观测设置，复现无物理增强的 grasp generator。
- [ ] 实现几何检查、静力学检查和仿真 lift 三套彼此独立的 evaluator。
- [ ] 建立按失败类型可视化和回放的评测脚本。

### Gate D：再定义研究问题

- [ ] 找出 baseline 在一个受控物理变量上的稳定失败，而非从方法名倒推问题。
- [ ] 证明该失败不能仅靠更强后处理、更多数据或普通优化轻易解决。
- [ ] 写出一个可证伪假设：在条件 $X$ 下，机制 $M$ 应降低指标 $Y$，同时保持 $Z$，代价不超过 $C$。

## 16. 与导师或合作者沟通时必须能回答的问题 `[P0]`

- [ ] 你的模型生成的是姿态、接触、力、轨迹还是策略？
- [ ] 为什么这个问题需要分布生成，而不是求一个最优解？
- [ ] 所谓“物理约束”具体是哪条方程/可行集？依赖哪些假设？
- [ ] 约束施加在 noisy sample、clean estimate、最终样本还是实际执行轨迹？
- [ ] 物理模型是解析、可微优化、仿真器还是 learned surrogate？误差如何验证？
- [ ] force closure、仿真成功和真实成功之间的证据链是什么？
- [ ] 与 DexGrasp Anything、DexDiffuser、UGG、GraspQP、Safe/Constrained Diffusers 的实质差异是什么？
- [ ] 最强的非 diffusion baseline 是什么？
- [ ] 方法改善安全性时，是否牺牲了多样性、任务性能或实时性？
- [ ] 论文主张是灵巧抓取特有机制，还是通用约束采样方法？为何适合 CVPR/ICLR？

## 17. 后续共同讨论新 idea 的工作表

每次只决定一层，不从算法名称开场：

1. **任务边界**：观测、输出、手型、静态/动态、开环/闭环。
2. **真实失败**：选择一个可重复制造的 baseline failure。
3. **物理对象**：写出方程、约束、未知参数和可观测量。
4. **生成必要性**：指出多模态、分布覆盖或快速条件重采样的必要性。
5. **最小机制**：只引入足以处理该失败的一项机制。
6. **可证伪假设**：提前写出会支持和推翻假设的结果。
7. **最小实验**：先用 toy + 单手型 + 受控扫描验证因果链。
8. **新颖性核查**：最后再与最近工作逐项对齐，不凭关键词宣称首次。

下一轮讨论只需先填写：

```text
我最想研究的任务：
模型在测试时能看到：
模型应该输出：
我能使用的手型/仿真器/真实硬件：
我目前最在意的一种失败：
```

在这五项确定之前，不选具体的物理约束注入算法。
