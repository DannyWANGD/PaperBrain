---
tags:
  - dexterous_hand
  - safe_grasping
  - diffusion
  - chance_constrained_sampling
  - projection_guidance
  - force_closure
created: 2026-06-23
updated: 2026-06-23
status: top-conference-theory-draft
---

# C3-Diffuser：面向灵巧手安全抓取的 Chance-Constrained Contact-Closure 扩散投影算法

### 顶会投稿导向的完整理论体系、方法定义与可实现方案

> **全称**：C3-Diffuser, **C**hance-**C**onstrained **C**ontact-Closure Diffuser  
> **核心命题**：将灵巧手抓取生成中的物理安全问题建模为 diffusion clean posterior 上的 chance-constrained minimum-intervention projection，在每个去噪步对 clean estimate 进行带概率语义的局部安全修正，而不是使用手工权重的 energy guidance。  
> **投稿定位**：适合 CoRL / RSS / ICRA / CVPR robotics track。若投 ICLR，需要把机器人力学实现细节压缩，把重点放在 constrained generative sampling 与 differentiable optimization layer。  

本文档的目标不是把 C3-Diffuser 包装成一个超出实际能力的“全局安全生成定理”，而是形成一套顶会可防守的理论与方法系统：它要合理，因为每个约束都对应明确物理对象；要有效，因为采样时确实能减少穿透、关节越界和不稳定抓取；要创新，因为它把扩散模型的 clean posterior、不确定性收缩和最小干预 QP 统一起来；要可实现，因为每一步都可以用现有 SDF、手部运动学、摩擦锥近似、QP 求解器和可微优化层落地。

本文主张的创新点应收敛为四条。

1. **Clean-posterior safety projection**：物理约束作用在 \(\hat z_0^\theta\) 及其局部后验不确定性上，而不是直接作用在高噪声 \(z_t\) 上。
2. **Chance-constrained margin**：用 \(\delta\)-risk margin 把 denoising step 的不确定性转化为安全余量，替代没有概率语义的 guidance weight。
3. **Minimum-intervention QP**：用局部线性化安全约束定义最小修正 \(u^\star\)，使投影只在必要时发生，并且具有 KL / \(W_2\) 最小偏移解释。
4. **Contact-closure physical layer**：把非穿透、接触候选、摩擦锥和力封闭代理组织成可微的接触闭合约束链，使生成模型不仅“像数据”，还更接近准静态可抓取。

需要特别强调：C3-Diffuser 不应声称给出无条件全局安全保证。可防守的理论边界是：在校准的局部高斯 clean posterior、一阶安全线性化、QP 可行或 soft-feasible、以及物理代理与仿真稳定性经验证相关的条件下，C3 给出每一步的最小信息偏移安全修正，并提供保守的概率安全下界。

---

## 目录

- [1 问题定义：灵巧手抓取生成与 clean-space 约束](#1-问题定义灵巧手抓取生成与-clean-space-约束)
- [2 接触力学建模：从接触点到 wrench space](#2-接触力学建模从接触点到-wrench-space)
- [3 C3 的必要性：energy guidance 的结构性缺陷](#3-c3-的必要性energy-guidance-的结构性缺陷)
- [4 Safety functions：把物理约束写成可投影边界](#4-safety-functions把物理约束写成可投影边界)
- [5 Chance constraint：从 clean posterior 到风险收缩余量](#5-chance-constraint从-clean-posterior-到风险收缩余量)
- [6 C3-QP：最小干预安全投影](#6-c3-qp最小干预安全投影)
- [7 理论命题 I：局部高斯下的最小信息偏移](#7-理论命题-i局部高斯下的最小信息偏移)
- [8 理论命题 II：有限约束集合的保守安全下界](#8-理论命题-ii有限约束集合的保守安全下界)
- [9 力封闭代理：从 GraspQP 思路到 C3 的可实现版本](#9-力封闭代理从-graspqp-思路到-c3-的可实现版本)
- [10 训练与采样算法：让投影从补救变成校正](#10-训练与采样算法让投影从补救变成校正)
- [11 可实现性设计：数值、复杂度与工程边界](#11-可实现性设计数值复杂度与工程边界)
- [12 顶会实验设计：每个主张如何被验证](#12-顶会实验设计每个主张如何被验证)
- [13 论文写作边界：哪些话能说，哪些话不能说](#13-论文写作边界哪些话能说哪些话不能说)
- [附录 A：核心公式速查](#附录-a核心公式速查)
- [附录 B：QP 敏感度与反传说明](#附录-bqp-敏感度与反传说明)

---

# 第一部分：方法定义

---

## 1 问题定义：灵巧手抓取生成与 clean-space 约束

### 1.1 生成变量

灵巧手静态抓取样本记为：

$$
x=(T_w,q)\in SE(3)\times\mathbb R^{n_q},
\tag{1.1}
$$

其中 \(T_w\) 是手腕相对物体坐标系的 6D 位姿，\(q\) 是手部关节角。扩散模型通常要求欧氏向量空间，因此实际实现中选取局部坐标：

$$
z=\operatorname{chart}(T_w,q)\in\mathbb R^d,\qquad d=6+n_q.
\tag{1.2}
$$

下文统一使用 \(z\) 表示局部参数化后的抓取变量。这个约定必须写清楚，因为后续的高斯后验、线性化安全函数和 QP 修正都发生在 \(\mathbb R^d\) 中，而不是直接在全局 \(SE(3)\) 流形上。实现时，位姿部分可以使用 axis-angle、Lie algebra \(\mathfrak{se}(3)\)、6D rotation representation 或局部增量坐标；论文中只需要求该 chart 在局部邻域内光滑且可逆。

条件输入记为 \(y\)，可以包含物体点云、mesh、SDF、类别、尺度和期望抓取类型。C3 不绑定某个条件编码器，它是一个作用在扩散采样过程外侧的 safety correction layer。

### 1.2 DDPM clean estimate

标准前向扩散为：

$$
z_t=\sqrt{\bar\alpha_t}z_0+\sqrt{1-\bar\alpha_t}\epsilon,\qquad
\epsilon\sim\mathcal N(0,I).
\tag{1.3}
$$

噪声预测模型通过：

$$
\mathcal L_{DDPM}
=
\mathbb E\left[
\|\epsilon-\epsilon_\theta(z_t,t,y)\|_2^2
\right]
\tag{1.4}
$$

训练。由 (1.3) 得到当前 denoising step 的 clean estimate：

$$
\hat z_0^\theta
=
\frac{
z_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta(z_t,t,y)
}{
\sqrt{\bar\alpha_t}
}.
\tag{1.5}
$$

若使用 score 参数化 \(s_\theta(z_t,t,y)\approx\nabla_{z_t}\log p_t(z_t|y)\)，则有 Tweedie 形式：

$$
\hat z_0^\theta
=
\frac{
z_t+(1-\bar\alpha_t)s_\theta(z_t,t,y)
}{
\sqrt{\bar\alpha_t}
}.
\tag{1.6}
$$

C3 的基本判断是：物理约束应作用在 \(\hat z_0^\theta\) 上，而不是 \(z_t\) 上。原因很直接：穿透深度、接触法向、摩擦锥、关节限位、wrench matrix 和力封闭都只对干净抓取姿态有几何意义。高噪声变量 \(z_t\) 只是采样过程的中间状态，不能直接解释为真实手姿态。

### 1.3 C3 的采样目标

给定当前 \(z_t\)，未约束扩散模型隐式给出 clean posterior：

$$
p_\theta(z_0|z_t,y).
\tag{1.7}
$$

普通采样只要求 \(z_0\) 来自模型分布；C3 进一步要求其以高概率满足安全约束：

$$
\mathbb P\left(z_0\in\mathcal S_{safe}(y)\mid z_t,y\right)\ge 1-\delta.
\tag{1.8}
$$

由于真实 posterior 不可精确求解，C3 使用局部高斯近似：

$$
z_0|z_t,y
\approx
\mathcal N(\hat z_0^\theta,\Sigma_t).
\tag{1.9}
$$

然后在 \(\hat z_0^\theta\) 处构造 chance-tightened safety constraints，并求解最小修正：

$$
\hat z_0^+
=
\hat z_0^\theta+u^\star.
\tag{1.10}
$$

直观地说，C3 每一步都在问：当前 clean posterior 的均值是否足够远离物理风险边界？如果不够，应该用多小的改动把它推回一个概率安全的局部区域？

### 1.4 Clean-space 修正如何映射回扩散更新

若在 clean estimate 上得到修正 \(u^\star\)，则 score 参数化下：

$$
\Delta s
=
\frac{\sqrt{\bar\alpha_t}}{1-\bar\alpha_t}u^\star.
\tag{1.11}
$$

epsilon 参数化下：

$$
\epsilon_\theta^+
=
\epsilon_\theta
-
\frac{\sqrt{\bar\alpha_t}}{\sqrt{1-\bar\alpha_t}}u^\star.
\tag{1.12}
$$

实际实现必须只选择一种修正路径。多数 DDPM / DDIM 代码使用 \(\epsilon_\theta\) 参数化，因此推荐用 (1.12)，再把 \(\epsilon_\theta^+\) 代入原始 sampler。需要注意后期 \(\bar\alpha_t\to1\) 时 (1.12) 的系数变大，必须加入 \(\|u^\star\|\) 或 \(\|\Delta\epsilon\|\) 的裁剪。

---

## 2 接触力学建模：从接触点到 wrench space

### 2.1 接触候选与 SDF

设物体 SDF 为 \(\phi_o(p)\)，约定：

$$
\phi_o(p)>0 \text{ 表示物体外部},\quad
\phi_o(p)=0 \text{ 表示表面},\quad
\phi_o(p)<0 \text{ 表示内部}.
\tag{2.1}
$$

手部表面采样点记为 \(p_k(z)\)。由运动学链式法则：

$$
\nabla_z\phi_o(p_k(z))
=
\left(\frac{\partial p_k}{\partial z}\right)^\top
\nabla_p\phi_o(p_k).
\tag{2.2}
$$

非穿透只能说明手没有插入物体，不等于形成有效接触。因此 C3 应区分两类几何条件：

1. **Non-penetration**：所有高风险手部点满足 \(\phi_o(p_k)\ge0\) 或带余量版本。
2. **Contact existence**：若某些指尖/指腹被选为接触候选，则它们应靠近物体表面，例如 \(|\phi_o(p_i)|\le \epsilon_c\) 或用软接触权重 \(a_i(z)\) 建模。

如果没有明确接触候选，force closure 的 \(W(z)\) 没有物理意义。论文中必须避免在“手离物体很远”的样本上讨论力封闭。

### 2.2 摩擦锥与 primitive wrench

采用 hard-finger 点接触模型。第 \(i\) 个接触点有接触位置 \(p_i\)、物体表面法向 \(n_i\)、接触力 \(f_i\)。Coulomb 摩擦条件为：

$$
\|f_{t,i}\|_2\le \mu_i f_{n,i},\qquad f_{n,i}=n_i^\top f_i\ge0.
\tag{2.3}
$$

为了得到可计算的有限维问题，用 \(L\) 条边的多面体内近似摩擦锥：

$$
f_i=\sum_{\ell=1}^{L}d_{i\ell}\alpha_{i\ell},\qquad
\alpha_{i\ell}\ge0.
\tag{2.4}
$$

每个边方向 \(d_{i\ell}\) 产生一个 6D primitive wrench：

$$
w_{i\ell}
=
\begin{bmatrix}
d_{i\ell}\\
r_i\times d_{i\ell}
\end{bmatrix},
\qquad
r_i=p_i-c_o,
\tag{2.5}
$$

其中 \(c_o\) 为物体质心。将所有 primitive wrench 按列堆叠：

$$
W(z)
=
[w_{11},\dots,w_{1L},\dots,w_{M1},\dots,w_{ML}]
\in\mathbb R^{6\times K},
\quad K=ML.
\tag{2.6}
$$

这里 \(W(z)\) 是抓取 wrench matrix。它依赖手姿态、接触点、物体法向、摩擦系数和质心位置。

### 2.3 严格力封闭条件

力封闭的几何含义是：接触 wrench 的非负组合能够抵抗任意外部 6D wrench。令 \(w_j\) 表示 \(W\) 的第 \(j\) 列，则严格 force closure 可写为：

$$
\operatorname{pos}\{w_1,\dots,w_K\}=\mathbb R^6.
\tag{2.7}
$$

一个常用代数判据是：

$$
\operatorname{rank}(W)=6
\quad\text{and}\quad
\exists \alpha\succ0,\; W\alpha=0.
\tag{2.8}
$$

两个条件缺一不可。若只有 \(W\alpha=0\)，可能只是低维子空间内的自平衡，无法抵抗任意 6D 扰动；若只有 \(\operatorname{rank}(W)=6\)，仍不能保证原点被正系数包围，因为接触力只能推不能拉，不能使用任意负系数。

这也决定了 C3 中力封闭模块的写法：它应被表述为 **force-closure proxy** 或 **contact-closure surrogate**，而不是完整替代严格力封闭判定。顶会审稿人会非常敏感于“rank proxy 是否等价于 force closure”这类问题，因此需要主动写清代理与严格条件的差别。

---

## 3 C3 的必要性：energy guidance 的结构性缺陷

传统物理引导常写作：

$$
\tilde p(z|y)
\propto
p_\theta(z|y)\exp[-E_{phys}(z,y)],
\qquad
E_{phys}=\sum_k\lambda_kE_k.
\tag{3.1}
$$

反向采样时对应加入：

$$
s_{guided}
=
s_\theta-\nabla_z E_{phys}.
\tag{3.2}
$$

这一范式简单，但在灵巧手安全抓取中存在三个结构性问题。

第一，**高噪声阶段的物理梯度不可靠**。即使使用 \($\hat z_0^\theta$\) 计算物理能量，该 clean estimate 在大 \(t\) 时仍有较大后验不确定性。直接沿 \($\nabla E(\hat z_0)$\) 做强更新，可能把一个不确定姿态的错误几何解释当成真值。

第二，**权重 \(\lambda_k\) 没有概率语义**。非穿透、摩擦锥、关节限位、force closure 残差尺度完全不同，一个固定 \($\lambda_k$\) 既不能解释为违反概率，也不能随 denoising uncertainty 自动调整。

第三，**梯度步不等于最小安全修正**。Penalty 梯度告诉我们某个能量下降方向，但没有告诉我们满足线性化约束所需的最小位移。步长过小修不回来，步长过大会破坏样本分布和多样性。

C3 的核心替代是：

$$
u^\star
=
\arg\min_u
\text{intervention}(u)
\quad
\text{s.t. local chance-tightened safety constraints}.
\tag{3.3}
$$

也就是说，C3 不是“多加一个 loss”，而是把物理引导从能量下降改成带概率语义的局部投影。

---

## 4 Safety functions：把物理约束写成可投影边界

### 4.1 定义

对第 \(i\) 个物理约束定义 safety function：

$$
h_i(z,y)>0 \text{ 安全},\qquad
h_i(z,y)=0 \text{ 边界},\qquad
h_i(z,y)<0 \text{ 违反}.
\tag{4.1}
$$

Safety function 和普通 penalty 的区别在于：它的零水平集就是安全边界，因此可以被线性化为 QP 约束；而 penalty 的数值大小通常只表达“越小越好”，不一定能定义清晰的可行集。

### 4.2 A 类：关节限位

对每个关节 \(j\)，定义：

$$
h_j^{lower}(q)=q_j-q_j^{min}-\epsilon_q,\qquad
h_j^{upper}(q)=q_j^{max}-q_j-\epsilon_q.
\tag{4.2}
$$

这类约束是确定性线性边界，梯度精确：

$$
\nabla_q h_j^{lower}=e_j,\qquad
\nabla_q h_j^{upper}=-e_j.
\tag{4.3}
$$

实现中，关节限位可以直接进入 C3-QP，也可以在 clean estimate 上做 conservative clipping。若投顶会，建议主方法中把它放入 QP，因为这能保持方法形式统一；clip 可作为高效实现近似。

### 4.3 B1 类：非穿透

对手部表面点 \(p_k(z)\)：

$$
h_k^{pen}(z,y)
=
\phi_o(p_k(z))-\epsilon_p.
\tag{4.4}
$$

梯度为：

$$
\nabla_z h_k^{pen}
=
\left(\frac{\partial p_k}{\partial z}\right)^\top
\nabla_p\phi_o(p_k).
\tag{4.5}
$$

非穿透是 C3 最适合展示 chance constraint 的约束，因为 \(\hat z_0\) 的位姿不确定性会直接变成 SDF 查询不确定性。实验中应至少报告 mean penetration depth、max penetration depth 和 penetration rate。

### 4.4 B2 类：接触存在与接近表面

仅有非穿透会允许手远离物体。为了形成抓取，需要接触候选接近表面。可以定义：

$$
h_i^{near}(z,y)
=
\epsilon_c^2-\phi_o(p_i(z))^2,
\tag{4.6}
$$

或者采用只惩罚过远的形式：

$$
h_i^{near}(z,y)
=
\epsilon_c-\left|\phi_o(p_i(z))\right|_\nu,
\tag{4.7}
$$

其中 \(|a|_\nu=\sqrt{a^2+\nu^2}\) 是平滑绝对值。接近表面约束不应对所有手部采样点施加，否则会把整只手吸到物体表面；它只应作用于预定义指尖/指腹候选，或由接触网络预测的 top-\(M\) 接触点。

### 4.5 B3 类：摩擦锥

如果模型显式生成或估计接触力 \(f_i\)，可写：

$$
h_i^{fric}(z,y)
=
\mu_i f_{n,i}
-
\sqrt{\|f_{t,i}\|_2^2+\nu^2}
-
\epsilon_f.
\tag{4.8}
$$

如果接触力并不在生成变量中，而是由 force-closure 内层 QP 的摩擦锥 primitive coefficients 表示，则摩擦约束已隐式包含在 \($d_{i\ell}$\) 的构造中。此时不应重复加入 (4.8)，否则可能在数学上重复计约束。论文中可以把摩擦锥处理分成两种设置：

1. **Explicit-force setting**：\(z\) 包含 \($f_i$\)，使用 (4.8)。
2. **Primitive-wrench setting**：\(z\) 不包含 \($f_i$\)，摩擦由 \(W(z)\) 的列构造保证。

### 4.6 C 类：contact closure / force closure proxy

严格 force closure 难以直接作为可微硬约束嵌入每个 denoising step，因此 C3 使用两个互补代理：

$$
E_{bal}(z)
=
\min_{\alpha\in\Delta_K}
\|W(z)\alpha\|_2^2,
\qquad
\Delta_K=\{\alpha\succeq0,\;\mathbf1^\top\alpha=1\}.
\tag{4.9}
$$

它衡量原点到 wrench convex hull 的距离。定义 balance safety：

$$
h^{bal}(z)=\tau_{bal}-E_{bal}(z).
\tag{4.10}
$$

再定义 rank / volume proxy：

$$
h^{rank}(z)=\sigma_6(W(z))-\tau_{rank},
\tag{4.11}
$$

或更平滑的：

$$
h^{vol}(z)=\log\det(W(z)W(z)^\top+\epsilon I)-\tau_{vol}.
\tag{4.12}
$$

\($h^{bal}$\) 约束自平衡能力，\($h^{rank}$\) 或 \($h^{vol}$\) 约束 6D wrench 覆盖能力。二者结合比单独使用任一项更接近严格 force closure 的两个要素。

### 4.7 层次安全集

最终安全集写为：

$$
\mathcal S_{safe}
=
\mathcal S_{exec}
\cap
\mathcal S_{geom}
\cap
\mathcal S_{contact}
\cap
\mathcal S_{closure}.
\tag{4.13}
$$

其中：

$$
\mathcal S_{exec}=\{z:h_j^{lower}\ge0,\;h_j^{upper}\ge0,\forall j\},
\tag{4.14}
$$

$$
\mathcal S_{geom}=\{z:h_k^{pen}\ge0,\forall k\},
\tag{4.15}
$$

$$
\mathcal S_{contact}=\{z:h_i^{near}\ge0,\forall i\in\mathcal C(z)\},
\tag{4.16}
$$

$$
\mathcal S_{closure}=\{z:h^{bal}\ge0,\;h^{rank}\ge0\}.
\tag{4.17}
$$

任务成功、lift success、drop rate 和抗扰动表现不直接放入安全集，而作为最终评估指标。原因是它们通常依赖不可微仿真和控制器，不适合作为每步 QP 的硬约束。

---

# 第二部分：chance constraint 与 QP 理论

---

## 5 Chance constraint：从 clean posterior 到风险收缩余量

### 5.1 局部高斯后验假设

在第 \(t\) 个 denoising step，C3 使用：

$$
z_0|z_t,y
\approx
\mathcal N(\hat z_0^\theta,\Sigma_t).
\tag{5.1}
$$

原型实现可采用各向同性协方差：

$$
\Sigma_t=\kappa_t^2 I,
\qquad
\kappa_t=c\sqrt{\frac{1-\bar\alpha_t}{\bar\alpha_t}}.
\tag{5.2}
$$

其中 \(c\) 由验证集 clean-estimation error 标定：

$$
c^2
\approx
\operatorname{median}_t
\frac{\mathbb E[\|z_0-\hat z_0^\theta\|_2^2]/d}
{(1-\bar\alpha_t)/\bar\alpha_t}.
\tag{5.3}
$$

更精细版本可以用 ensemble、MC dropout 或模型输出方差估计对角协方差。论文初版建议使用 (5.2) 作为主方法，因为它简单、可复现、消融清楚。

这里的关键写法是：\(\Sigma_t\) 是 **calibrated local uncertainty model**，不是对真实 diffusion posterior 的严格解析解。

### 5.2 单个约束的机会约束

对安全函数一阶线性化：

$$
h_i(z_0)
\approx
h_i(\hat z_0)
+
\nabla h_i(\hat z_0)^\top(z_0-\hat z_0).
\tag{5.4}
$$

由高斯仿射不变性：

$$
h_i(z_0)|z_t,y
\approx
\mathcal N
\left(
h_i(\hat z_0),
\nabla h_i^\top\Sigma_t\nabla h_i
\right).
\tag{5.5}
$$

要求：

$$
\mathbb P(h_i(z_0)\ge0|z_t,y)\ge1-\delta_i.
\tag{5.6}
$$

对一维高斯变量 \(X\sim\mathcal N(\mu,\sigma^2)\)，
\(\mathbb P(X\ge0)\ge1-\delta\) 等价于：

$$
\mu-\Phi^{-1}(1-\delta)\sigma\ge0.
\tag{5.7}
$$

因此得到 risk-tightened margin：

$$
\bar h_i(\hat z_0,t,y)
=
h_i(\hat z_0,y)
-
\beta_{\delta_i}
\|\Sigma_t^{1/2}\nabla h_i(\hat z_0,y)\|_2
-
\rho_i(t),
\tag{5.8}
$$

其中：

$$
\beta_{\delta_i}=\Phi^{-1}(1-\delta_i).
\tag{5.9}
$$

C3 实际要求：

$$
\bar h_i(\hat z_0,t,y)\ge0.
\tag{5.10}
$$

### 5.3 线性化误差 reserve

若 \(h_i\) 在局部邻域二阶可微，且：

$$
\|\nabla^2 h_i(z)\|_2\le L_i,
\tag{5.11}
$$

则 Taylor 余项 \(R_i\) 满足：

$$
|R_i|
\le
\frac{L_i}{2}\|z_0-\hat z_0\|_2^2.
\tag{5.12}
$$

在 \(z_0-\hat z_0\sim\mathcal N(0,\Sigma_t)\) 下：

$$
\mathbb E|R_i|
\le
\frac{L_i}{2}\operatorname{tr}(\Sigma_t).
\tag{5.13}
$$

若希望得到概率形式，可由 Markov inequality：

$$
\mathbb P(|R_i|>\rho_i)
\le
\frac{L_i\operatorname{tr}(\Sigma_t)}{2\rho_i}.
\tag{5.14}
$$

这说明 \(\rho_i(t)\) 不是随意加的保守项，而是为一阶线性化误差预留的 reserve。实际实现中，可以设：

$$
\rho_i(t)=c_\rho L_i\operatorname{tr}(\Sigma_t),
\tag{5.15}
$$

或把 \(\rho_i\) 作为验证集标定超参数。论文中不要把 (5.13) 直接写成概率保证；真正的概率扣除来自 (5.14)。

### 5.4 多约束风险预算

对 \(m\) 个约束，若总风险预算为 \(\delta_{total}\)，最简单做法是：

$$
\delta_i=\frac{\delta_{total}}{m}.
\tag{5.16}
$$

由 union bound：

$$
\mathbb P\left(\bigwedge_{i=1}^{m}h_i(z_0)\ge0\right)
\ge
1-\sum_{i=1}^{m}\delta_i
\tag{5.17}
$$

在线性化误差也计入时，变成：

$$
\mathbb P\left(\bigwedge_{i=1}^{m}h_i(z_0)\ge0\right)
\ge
1-\sum_{i=1}^{m}(\delta_i+\eta_i),
\tag{5.18}
$$

其中 \(\eta_i\) 来自 (5.14)。这个 bound 保守但可防守，因为它不依赖各约束独立性。

---

## 6 C3-QP：最小干预安全投影

### 6.1 线性化安全约束

给定 \(\hat z_0\)，对每个 risk-tightened safety function 线性化：

$$
\bar h_i(\hat z_0)
+
\nabla \bar h_i(\hat z_0)^\top u
\ge0.
\tag{6.1}
$$

这里 \(u\in\mathbb R^d\) 是对 clean estimate 的修正。注意 \(\nabla\bar h_i\) 包含两部分：

$$
\nabla\bar h_i
=
\nabla h_i
-
\beta_{\delta_i}\nabla_z
\|\Sigma_t^{1/2}\nabla h_i\|_2
-
\nabla\rho_i.
\tag{6.2}
$$

工程上也可以 stop-gradient 掉第二项，只用 \(\nabla h_i\) 作为约束法向。这会牺牲一部分理论一致性，但显著提高数值稳定性。若采用该近似，论文应明确写为 first-order practical approximation。

### 6.2 理想无 slack QP

理想情况下，求：

$$
u^\star
=
\arg\min_u
\frac12\|u\|_{W_t}^2
\quad
\text{s.t.}\quad
\bar h_i+\nabla\bar h_i^\top u\ge0,\;\forall i.
\tag{6.3}
$$

\(W_t\succ0\) 是修正度量。常用选择：

$$
W_t=I
\tag{6.4}
$$

表示欧氏最小修正；或者：

$$
W_t=\Sigma_t^{-1}
\tag{6.5}
$$

表示 posterior precision 度量下的最小修正。后者的含义是：沿不确定性更大的方向移动代价更低，沿模型确定的方向移动代价更高。

### 6.3 实用 soft-constrained QP

真实系统中，局部线性化约束可能互相冲突，或者某些接触代理不可满足。因此实际 QP 使用 slack：

$$
(u^\star,\xi^\star)
=
\arg\min_{u,\xi}
\frac12\|u\|_{W_t}^2
+
\lambda_\xi\mathbf1^\top\xi
+
\frac{\lambda_2}{2}\|\xi\|_2^2
\tag{6.6}
$$

subject to：

$$
\bar h_i+\nabla\bar h_i^\top u+\xi_i\ge0,\quad
\xi_i\ge0,\quad
\|u\|_\infty\le u_{\max}.
\tag{6.7}
$$

\(\ell_1\) slack 让少数不可满足约束承担违反，\(\ell_2\) slack 保持数值平滑。论文主定理只适用于无 slack 可行版本；工程系统使用 (6.6)-(6.7)。这一区分必须写清楚。

### 6.4 KKT 解释：为什么它是“最小干预”

设 \(W_t=I\)，忽略 box constraint 和 slack，Lagrangian 为：

$$
\mathcal L(u,\lambda)
=
\frac12\|u\|^2
-
\sum_i\lambda_i(\bar h_i+\nabla\bar h_i^\top u),
\qquad
\lambda_i\ge0.
\tag{6.8}
$$

Stationarity 给出：

$$
u^\star
=
\sum_i\lambda_i^\star\nabla\bar h_i.
\tag{6.9}
$$

Complementary slackness 给出：

$$
\lambda_i^\star(\bar h_i+\nabla\bar h_i^\top u^\star)=0.
\tag{6.10}
$$

因此 \(u^\star\) 只由活跃或被违反的约束决定。已经有足够安全余量的约束对 \(u^\star\) 没有贡献。这正是 C3 相比 energy guidance 的核心差异：不是所有物理项都持续拉动样本，而是只有必要边界参与修正。

---

## 7 理论命题 I：局部高斯下的最小信息偏移

### 7.1 设定

令未修正 clean posterior 为：

$$
P_0=\mathcal N(\hat z_0,\Sigma_t).
\tag{7.1}
$$

修正 \(u\) 后：

$$
P_u=\mathcal N(\hat z_0+u,\Sigma_t).
\tag{7.2}
$$

即 C3 只移动 posterior 均值，不改变协方差。令无 slack 线性化可行集为：

$$
\mathcal U_t
=
\{u:\bar h_i+\nabla\bar h_i^\top u\ge0,\;\forall i\}.
\tag{7.3}
$$

### 7.2 命题

**命题 I（理想 C3 投影的最小信息偏移）**。在同协方差局部高斯、线性化安全约束、无 slack 且 \(\mathcal U_t\neq\emptyset\) 的条件下：

1. 若 \(W_t=\Sigma_t^{-1}\)，则 (6.3) 的解满足：

$$
u^\star
=
\arg\min_{u\in\mathcal U_t}
D_{KL}(P_0\|P_u).
\tag{7.4}
$$

2. 若 \(W_t=I\)，则 (6.3) 的解满足：

$$
u^\star
=
\arg\min_{u\in\mathcal U_t}
W_2^2(P_0,P_u).
\tag{7.5}
$$

3. 若 \(\Sigma_t=\kappa_t^2I\)，则 \(W_t=I\) 与 \(W_t=\Sigma_t^{-1}\) 的最优解一致。

### 7.3 证明

同协方差高斯分布的 KL 为：

$$
D_{KL}(P_0\|P_u)
=
\frac12u^\top\Sigma_t^{-1}u.
\tag{7.6}
$$

因此在 \(W_t=\Sigma_t^{-1}\) 时，QP 目标与 KL 偏移完全一致。

同协方差高斯的二阶 Wasserstein 距离为：

$$
W_2^2(P_0,P_u)=\|u\|_2^2.
\tag{7.7}
$$

因此在 \(W_t=I\) 时，QP 目标与 \(W_2^2\) 只差常数因子。若 \(\Sigma_t=\kappa_t^2I\)，则：

$$
u^\top\Sigma_t^{-1}u
=
\kappa_t^{-2}\|u\|_2^2,
\tag{7.8}
$$

正标量缩放不改变最优解。证毕。

### 7.4 解释

这个命题不是为了炫耀数学，而是给方法一个清楚、可防守的理论定位：在局部近似成立时，C3 是满足安全线性化约束所需的最小 posterior 改动。它不像 energy guidance 那样依赖人工步长，也不会在已经安全时继续移动样本。

---

## 8 理论命题 II：有限约束集合的保守安全下界

### 8.1 单约束下界

若 \(u^\star\) 使修正后均值满足：

$$
\bar h_i(\hat z_0+u^\star,t,y)\ge0,
\tag{8.1}
$$

并且一阶线性化误差 \(R_i\) 满足：

$$
\mathbb P(|R_i|>\rho_i)\le\eta_i,
\tag{8.2}
$$

则：

$$
\mathbb P(h_i(z_0)\ge0|z_t,y)\ge1-\delta_i-\eta_i.
\tag{8.3}
$$

证明思路是把失败事件分成两部分：线性高斯项违反和 Taylor 余项超过 reserve。前者由 \(\delta_i\) 控制，后者由 \(\eta_i\) 控制，再用 union bound 即可。

### 8.2 联合安全下界

对有限约束集合 \(\mathcal I\)，不要求约束独立，有：

$$
\mathbb P\left(\bigwedge_{i\in\mathcal I}h_i(z_0)\ge0\mid z_t,y\right)
\ge
1-\sum_{i\in\mathcal I}(\delta_i+\eta_i).
\tag{8.4}
$$

这就是 C3 能在论文中合理主张的概率安全保证。它是局部的、保守的、依赖假设的，但比“penalty 变小所以更安全”更有理论含义。

### 8.3 不建议主张全局收敛定理

不建议声称 C3 采样过程全局收敛到严格截断分布：

$$
p_\theta(z|y,z\in\mathcal S_{safe}).
\tag{8.5}
$$

原因有三点：

1. \(\mathcal S_{safe}\) 非凸，force closure 代理高度非线性。
2. C3 使用局部线性化切平面，不是真实集合投影。
3. 实际 QP 带 slack 和裁剪，可能允许软违反。

更合适的论文表述是：

> C3 does not claim global convergence to the exact truncated data distribution. Instead, it provides a local minimum-information correction under calibrated clean-posterior uncertainty and linearized safety constraints. This local property explains why safety improves while diversity is better preserved, and the global effect is evaluated empirically.

---

# 第三部分：力封闭与可微接触闭合

---

## 9 力封闭代理：从 GraspQP 思路到 C3 的可实现版本

### 9.1 为什么力封闭不能只写成一个简单 residual

严格 force closure 依赖 positive span：

$$
\operatorname{pos}\{w_j\}_{j=1}^{K}=\mathbb R^6.
\tag{9.1}
$$

若直接写：

$$
E_{fc}=\left\|\sum_j\alpha_jw_j\right\|^2,\qquad \alpha_j>0,
\tag{9.2}
$$

会出现系数趋近 0 的退化：让所有 \(\alpha_j\) 很小即可使 residual 很小，但这并不代表真实接触力能够平衡外部扰动。GraspQP 的关键启发是使用带下界和上界的接触力系数，例如：

$$
E_{gqp}(z)
=
\min_{1\le\gamma_j\le u}
\|W(z)\gamma\|_2^2.
\tag{9.3}
$$

下界避免零力退化，上界表达真实接触力或执行器能力限制。若最优值接近 0，说明当前接触几何允许一组有界非负接触力形成自平衡。

### 9.2 C3 中推荐的三层 force-closure proxy

为了兼顾物理性和可实现性，C3 的 force closure 模块建议分三层。

**Layer 1：接触存在 gating。** 只有当候选接触点足够接近表面时，才计算 \(W(z)\)。可以用接触权重：

$$
a_i(z)=\exp\left(-\frac{\phi_o(p_i(z))^2}{2\sigma_c^2}\right),
\tag{9.4}
$$

并对 wrench 列加权：

$$
\tilde w_{i\ell}=a_i(z)w_{i\ell}.
\tag{9.5}
$$

这样远离表面的“虚假接触”不会贡献稳定性。

**Layer 2：bounded balance QP。**

$$
E_{bal}^{box}(z)
=
\min_{\gamma}
\frac12\|W(z)\gamma\|_2^2
\quad
\text{s.t.}\quad
1\le\gamma_j\le u.
\tag{9.6}
$$

这比 simplex residual 更接近 GraspQP 的物理解释。若计算成本过高，可在训练中使用它，在每步采样中使用蒸馏出的轻量 proxy。

**Layer 3：rank / volume coverage。**

$$
E_{vol}(z)
=
-\log\det(W(z)W(z)^\top+\epsilon I).
\tag{9.7}
$$

或：

$$
E_{rank}(z)=\max(0,\tau_{rank}-\sigma_6(W(z)))^2.
\tag{9.8}
$$

bounded balance 只能说明可自平衡，rank / volume 负责鼓励完整 6D 覆盖。两者组合才更接近 force closure 的两个必要结构。

### 9.3 作为 C3 safety function 的写法

定义：

$$
h^{gqp}(z)=\tau_{gqp}-E_{bal}^{box}(z),
\tag{9.9}
$$

$$
h^{vol}(z)=\log\det(W(z)W(z)^\top+\epsilon I)-\tau_{vol}.
\tag{9.10}
$$

然后将它们加入 C3-QP：

$$
\bar h^{gqp}
=
h^{gqp}
-
\beta_{\delta_c}\|\Sigma_t^{1/2}\nabla h^{gqp}\|_2
-
\rho_c,
\tag{9.11}
$$

$$
\bar h^{vol}
=
h^{vol}
-
\beta_{\delta_v}\|\Sigma_t^{1/2}\nabla h^{vol}\|_2
-
\rho_v.
\tag{9.12}
$$

原型阶段可以只在后期 denoising steps 启用 C 类约束，因为早期 \(\hat z_0\) 的接触几何不稳定，force closure 的梯度容易误导采样。

### 9.4 可微 QP 的反传含义

内层 QP 的最优值：

$$
E(W)
=
\min_{\gamma\in[1,u]^K}
\frac12\|W\gamma\|_2^2
\tag{9.13}
$$

是 \(W\) 的函数，而 \(W\) 又是 \(z\) 的函数：

$$
z\to W(z)\to \gamma^\star(W)\to E(W(z)).
\tag{9.14}
$$

若最优解唯一且 active set 局部稳定，envelope theorem 给出：

$$
dE
=
(W\gamma^\star)^\top dW\,\gamma^\star.
\tag{9.15}
$$

因此：

$$
\nabla_W E
=
(W\gamma^\star)\gamma^{\star\top}.
\tag{9.16}
$$

再由链式法则把 \(\nabla_WE\) 反传到接触点、法向、手腕位姿和关节角。若需要最优解 \(\gamma^\star\) 本身对 \(W\) 的敏感度，则应使用 KKT 隐式微分或 cvxpylayers / qpth 等可微 QP 工具。论文中可以强调：C3 不把 force closure 当作后处理筛选器，而是把它变成能向手姿态提供梯度的准静态接触力学层。

### 9.5 计算成本的现实方案

每个 denoising step 对每个样本求一次 force-closure QP 可能过重。可实现策略如下：

1. 只在后 \(T_c\) 个 denoising steps 启用 C 类约束。
2. 只对 top-\(M\) 接触候选构造 \(W\)，例如每指 1-2 个候选。
3. 主采样使用 \(E_{vol}\) 和轻量 \(E_{bal}\)，最终 refinement 使用 GraspQP-style QP。
4. 训练一个小网络蒸馏 \(E_{gqp}\) 或 \(\nabla_zE_{gqp}\)，把昂贵 QP 从每步采样移到离线标签生成。

这组策略使方法可落地，也能形成很好的消融实验。

---

# 第四部分：训练、实现与实验

---

## 10 训练与采样算法：让投影从补救变成校正

### 10.1 推理时 C3 sampler

每个 denoising step 执行：

1. 输入 \(z_t,t,y\)，计算 \(\epsilon_\theta(z_t,t,y)\)。
2. 由 (1.5) 得到 \(\hat z_0^\theta\)。
3. 计算候选 safety functions \(h_i(\hat z_0^\theta,y)\) 和梯度。
4. 用 \(\Sigma_t\)、\(\delta_i\)、\(\rho_i\) 得到 \(\bar h_i\)。
5. 若所有 \(\bar h_i\ge0\)，设置 \(u^\star=0\)。
6. 否则求解 C3-QP 得到 \(u^\star\)。
7. 用 (1.12) 得到 \(\epsilon_\theta^+\)。
8. 执行标准 DDPM / DDIM 更新得到 \(z_{t-1}\)。

伪代码：

```text
for t = T, ..., 1:
    eps = eps_theta(z_t, t, y)
    z0_hat = (z_t - sqrt(1-alpha_bar_t) * eps) / sqrt(alpha_bar_t)

    H = collect_active_safety_functions(z0_hat, y)
    margins = chance_tighten(H, Sigma_t, delta, rho)

    if all margins >= 0:
        u = 0
    else:
        u = solve_C3_QP(margins, gradients, W_t, slack, u_max)

    eps_plus = eps - sqrt(alpha_bar_t) / sqrt(1-alpha_bar_t) * clip(u)
    z_{t-1} = sampler_step(z_t, eps_plus, t)
```

### 10.2 安全感知训练

如果模型本身长期输出不安全 \(\hat z_0^\theta\)，推理时 QP 会频繁介入，最终破坏分布。因此训练阶段加入：

$$
\mathcal L_{C3}
=
\mathcal L_{DDPM}
+
\lambda_{safe}
\mathbb E\left[
w(t)\sum_i
\max(0,-\bar h_i(\hat z_0^\theta,t,y))^2
\right]
+
\lambda_{fc}\mathbb E[w_c(t)E_{closure}(\hat z_0^\theta)].
\tag{10.1}
$$

其中 \(w(t)\) 是时间门控。为了避免高噪声阶段错误物理梯度，推荐：

$$
w(t)
=
\operatorname{sigmoid}(a(\operatorname{SNR}(t)-\tau_{SNR})).
\tag{10.2}
$$

C 类 force closure 使用更保守门控：

$$
w_c(t)
=
\mathbf1[\bar\alpha_t\ge\tau_c].
\tag{10.3}
$$

训练的目标不是让 QP 消失，而是让模型内生地产生更接近安全集的 clean estimate，使推理时 C3 投影变成小幅校正，而不是大幅抢救。

### 10.3 训练监控指标

必须记录：

$$
\text{QPTriggerRate}
=
\frac{1}{BT}\sum_{b,t}\mathbf1[\exists i,\bar h_i^{(b,t)}<0],
\tag{10.4}
$$

$$
\text{MeanCorrection}
=
\frac{1}{BT}\sum_{b,t}\|u_{b,t}^\star\|_2,
\tag{10.5}
$$

以及：

- validation penetration rate；
- validation joint-limit violation；
- closure proxy value；
- \(\|\nabla\mathcal L_{safe}\|/\|\nabla\mathcal L_{DDPM}\|\)；
- diversity / coverage；
- final safe success rate。

若安全训练有效，预期现象是：QP trigger rate 和 \(\mathbb E\|u^\star\|\) 下降，而 final safe success rate 上升或至少不下降。

---

## 11 可实现性设计：数值、复杂度与工程边界

### 11.1 QP 规模

Shadow Hand 级别通常 \(d\approx 30\)。每步 QP 不应塞入所有手部网格点，而应保留 active constraints：

- 每个关节只保留接近上下界的约束；
- 非穿透只保留 penetration 最危险的 top-\(K_p\) 点；
- 接触存在只保留 top-\(M\) 指尖/指腹候选；
- force closure 只在后期 step 或 refinement 阶段启用；
- 摩擦锥约束只在显式接触力设置中启用。

这样变量是 \(u\in\mathbb R^d\) 加少量 slack，约束数量通常几十个以内。OSQP、Clarabel、qpOASES、qpth 或 cvxpylayers 都可用于原型。

### 11.2 数值保护

epsilon 修正：

$$
\Delta\epsilon
=
-
\frac{\sqrt{\bar\alpha_t}}{\sqrt{1-\bar\alpha_t}}u^\star.
\tag{11.1}
$$

后期系数可能很大。建议：

$$
\|u^\star\|_\infty\le u_{max}(t),
\tag{11.2}
$$

$$
\|\Delta\epsilon\|_\infty\le c_\epsilon,
\tag{11.3}
$$

并对 \(u^\star\) 使用 trust region：

$$
u_{max}(t)=u_0\sqrt{1-\bar\alpha_t}+\epsilon_u.
\tag{11.4}
$$

这样高噪声阶段允许较大探索，低噪声阶段避免微小 clean 修正被放大成巨大 epsilon 改动。

### 11.3 SDF 与法向鲁棒性

SDF 梯度在 mesh 边界、薄结构、扫描噪声处可能不稳定。实现中应：

1. 使用平滑 SDF 或神经 SDF 的正则化梯度。
2. 对 \(\|\nabla_p\phi_o\|\) 做归一化和裁剪。
3. 在法向不可靠区域降低约束权重或增大 reserve。
4. 报告复杂物体、薄物体和凹形物体上的失败案例。

### 11.4 阈值标定

\(\epsilon_p,\epsilon_c,\tau_{bal},\tau_{rank},\tau_{vol}\) 不应手工拍脑袋。推荐流程：

1. 从 DexGraspNet 或自建仿真中收集成功抓取、失败抓取。
2. 计算每个样本的 penetration、contact distance、closure proxy、disturbance success。
3. 在验证集上选择阈值，使 proxy 与仿真稳定性相关性最高。
4. 报告阈值敏感性曲线。

这能把“理论 proxy”与“真实仿真稳定性”连接起来，是顶会审稿中非常关键的防守点。

---

## 12 顶会实验设计：每个主张如何被验证

### 12.1 核心假设

| 编号 | 主张 | 必须支持它的证据 |
|---|---|---|
| H1 | C3 比 tuned energy guidance 更安全 | penetration rate、joint violation、safe success rate |
| H2 | C3 比 deterministic projection 更稳健 | 不同噪声阶段 violation rate、\(\delta\) 消融 |
| H3 | Minimum-intervention 保持多样性 | coverage、MMD、joint entropy、unique successful grasps |
| H4 | 安全感知训练减少推理干预 | QP trigger rate、\(\mathbb E\|u^\star\|\)、采样耗时 |
| H5 | contact-closure proxy 提升稳定抓取 | disturbance rejection、drop rate、closure metric 与仿真相关性 |

### 12.2 对比组

1. **Base diffusion**：无物理修正。
2. **Energy guidance**：调优 \(\lambda\) 的传统 penalty 梯度。
3. **Deterministic projection**：C3-QP 但 \(\beta_\delta=0\)。
4. **C3 without training**：只在推理时投影。
5. **C3 without closure**：只用关节限位、非穿透、接触接近。
6. **C3 full**：chance projection + safety-aware training + closure proxy。
7. **Final refinement baseline**：只在采样结束后用优化器修正，用于证明逐步 C3 不是简单后处理。

### 12.3 数据与任务

建议设置：

- 多类别物体，含凸体、凹体、薄物体、工具类物体；
- 至少两类灵巧手或两种自由度配置；
- power grasp 与 precision grasp 分开统计；
- 训练集物体和未见物体分开报告；
- 对每个物体生成固定数量候选，例如 50 或 100。

### 12.4 指标

必须报告：

- raw success rate；
- safe success rate；
- mean / max penetration depth；
- joint-limit violation rate；
- contact distance；
- force-closure proxy；
- disturbance robustness；
- diversity / coverage；
- QP trigger rate；
- average QP time；
- average \(\|u^\star\|\)；
- final refinement time。

### 12.5 消融

关键消融：

1. \(\delta\) 或 \(\beta_\delta\)：展示风险预算与安全/多样性 trade-off。
2. \(\Sigma_t\) 标定：固定 \(\kappa\) vs schedule \(\kappa_t\) vs learned/ensemble uncertainty。
3. slack 权重：过软会违反安全，过硬会降低可行率。
4. force closure proxy：rank-only、balance-only、balance+rank、GraspQP-style bounded QP。
5. 启用 step：全程启用 vs 后期启用。
6. active constraint 数量：top-\(K\) 对速度和安全的影响。

### 12.6 失败案例

论文必须主动展示：

- 高噪声 clean estimate 错误导致的误投影；
- SDF 法向错误导致的穿透修正失败；
- 接触候选错误导致 force closure proxy 无意义；
- closure proxy 通过但仿真仍掉落；
- QP slack 大量激活导致软约束失效；
- 多样性下降到单一抓取模式。

这些失败案例不会削弱论文，反而能说明作者理解方法边界。

---

## 13 论文写作边界：哪些话能说，哪些话不能说

### 13.1 可以强主张的内容

可以主张：

1. C3 将物理安全约束从 hand-tuned energy guidance 改写为 clean posterior 上的 chance-constrained local projection。
2. 在局部高斯和线性化约束下，C3-QP 是满足安全约束的最小 KL / \(W_2\) 均值偏移。
3. Risk-tightened margin 给 \(\delta\) 明确概率语义，比固定 guidance weight 更可解释。
4. Force-closure proxy 结合 bounded balance 与 rank / volume，比单一 residual 更贴近 positive span 的物理结构。
5. 安全感知训练可降低推理时 QP 介入频率，使方法更高效。

### 13.2 不应过强主张的内容

不应主张：

1. C3 保证所有生成抓取严格安全。
2. C3 采样严格收敛到安全截断数据分布。
3. \(E_{bal}=0\) 等价于 force closure。
4. rank proxy 等价于 force closure。
5. 仿真成功等价于真实机器人成功。
6. 使用 chance constraint 后不再需要阈值标定。

更准确的措辞是：

> C3 provides calibrated local safety corrections rather than global safety certificates.

### 13.3 论文最核心的一句话

建议摘要中的核心句子写成：

> We propose C3-Diffuser, a chance-constrained diffusion sampler that performs minimum-information safety projection in the clean-sample posterior space, enabling uncertainty-aware non-penetration, contact consistency, and differentiable contact-closure constraints for dexterous grasp generation.

这句话同时包含：diffusion sampler、chance constraint、minimum-information projection、clean posterior、接触闭合物理约束，能让审稿人快速识别创新点。

---

# 附录 A：核心公式速查

| 含义 | 公式 |
|---|---|
| Clean estimate | \(\hat z_0=(z_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta)/\sqrt{\bar\alpha_t}\) |
| Local posterior | \(z_0|z_t,y\approx\mathcal N(\hat z_0,\Sigma_t)\) |
| Risk margin | \(\bar h_i=h_i-\beta_{\delta_i}\|\Sigma_t^{1/2}\nabla h_i\|-\rho_i\) |
| Ideal C3-QP | \(\min_u \frac12\|u\|_{W_t}^2\;\text{s.t.}\;\bar h_i+\nabla\bar h_i^\top u\ge0\) |
| Practical C3-QP | \(\min_{u,\xi}\frac12\|u\|_{W_t}^2+\lambda_\xi\mathbf1^\top\xi+\frac{\lambda_2}{2}\|\xi\|^2\) |
| Score correction | \(\Delta s=\frac{\sqrt{\bar\alpha_t}}{1-\bar\alpha_t}u^\star\) |
| Epsilon correction | \(\epsilon_\theta^+=\epsilon_\theta-\frac{\sqrt{\bar\alpha_t}}{\sqrt{1-\bar\alpha_t}}u^\star\) |
| Strict force closure | \(\operatorname{rank}(W)=6,\;\exists\alpha\succ0,\;W\alpha=0\) |
| Bounded balance | \(E_{gqp}=\min_{1\le\gamma_j\le u}\|W\gamma\|^2\) |
| Volume proxy | \(h^{vol}=\log\det(WW^\top+\epsilon I)-\tau_{vol}\) |
| Safety bound | \(P(\wedge_i h_i\ge0)\ge1-\sum_i(\delta_i+\eta_i)\) |

---

# 附录 B：QP 敏感度与反传说明

考虑一般二次规划：

$$
E(W)
=
\min_{\gamma}
\frac12\gamma^\top H(W)\gamma
\quad
\text{s.t.}\quad
l\le\gamma\le u,
\qquad
H(W)=W^\top W.
\tag{B.1}
$$

若最优解唯一且 active set 局部稳定，value function 的一阶微分可由 envelope theorem 得到：

$$
dE
=
\frac12\gamma^{\star\top}dH\,\gamma^\star.
\tag{B.2}
$$

由于：

$$
dH=dW^\top W+W^\top dW,
\tag{B.3}
$$

有：

$$
dE
=
(W\gamma^\star)^\top dW\,\gamma^\star.
\tag{B.4}
$$

因此：

$$
\nabla_W E
=
(W\gamma^\star)\gamma^{\star\top}.
\tag{B.5}
$$

这说明 force-closure QP 的最优值可以把残余 wrench \(W\gamma^\star\) 反传给每个 primitive wrench 列。再通过：

$$
\frac{\partial E}{\partial z}
=
\left\langle
\nabla_W E,
\frac{\partial W}{\partial z}
\right\rangle
\tag{B.6}
$$

即可得到对手腕位姿、关节角、接触点和法向的梯度。若目标还依赖 \(\gamma^\star\) 本身，或存在一般线性约束、活动集切换，则使用 KKT 隐式微分：

$$
F(\gamma^\star,\lambda^\star;W)=0,
\qquad
\frac{\partial(\gamma^\star,\lambda^\star)}{\partial W}
=
-
\left(\frac{\partial F}{\partial(\gamma,\lambda)}\right)^{-1}
\frac{\partial F}{\partial W}.
\tag{B.7}
$$

工程上推荐使用成熟可微 QP 层，避免手写 active-set 逻辑。论文中只需说明在局部正则条件下可微，并把不可微切换点视为分段光滑优化中的常见现象。

---

> **当前版本结论**：C3-Diffuser 最有投稿价值的核心不是“给 diffusion 加物理 loss”，而是把灵巧手抓取的物理安全约束组织成 clean posterior 上的 chance-constrained minimum-intervention projection。理论上主打局部高斯、线性化安全边界和最小信息偏移；方法上用 QP 做可解释修正；工程上通过 active constraints、后期启用 C 类约束和安全感知训练保证可落地；实验上必须证明安全提升不是以严重牺牲多样性为代价。
