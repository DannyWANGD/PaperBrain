---
tags:
  - 灵巧手专项
  - safe_dexterous_grasping
  - diffusion
  - constrained_sampling
  - CVPR
created: 2026-06-23
---

# C³-Diffuser：面向灵巧手安全抓取的 Chance-Constrained Contact-Closure 投影算法

> **全称**：C³-Diffuser — **C**hance-**C**onstrained **C**ontact-Closure Diffuser
> **一句话**：将灵巧手安全抓取建模为 diffusion posterior 下的 chance-constrained safety satisfaction 问题，通过 clean-sample 空间的最小干预 QP 投影，替代传统 energy guidance 的盲目梯度下降。

---

## 目录

1. [符号约定与先决知识](#1-符号约定与先决知识)
2. [问题形式化](#2-问题形式化)
3. [从 ABCD Energy 到 Safety Functions](#3-从-abcd-energy-到-safety-functions)
4. [Chance Constraint 理论推导](#4-chance-constraint-理论推导)
5. [最小干预 QP 投影](#5-最小干预-qp-投影)
6. [安全感知训练](#6-安全感知训练)
7. [力封闭可微形式的深化](#7-力封闭可微形式的深化)
8. [算法伪代码与实现细节](#8-算法伪代码与实现细节)
9. [理论保证](#9-理论保证)
10. [相关文献分层综述](#10-相关文献分层综述)
11. [实验设计与待验证命题](#11-实验设计与待验证命题)
12. [风险与缓解](#12-风险与缓解)

---

## 1. 符号约定与先决知识

### 1.1 生成变量

灵巧手抓取的生成变量定义在 joint space + task space：

$$
z = (T_w, q) \in SE(3) \times \mathbb{R}^{n_q}
$$

| 符号 | 含义 | 典型维度 |
|------|------|---------|
| $T_w \in SE(3)$ | 手腕位姿（相对物体坐标系） | 6 DoF |
| $q \in \mathbb{R}^{n_q}$ | 灵巧手关节角向量 | 16–24 |
| $y$ | 条件输入（物体点云 / mesh / SDF / 类别标签） | — |

### 1.2 DDPM / DDIM 基础

前向过程（加噪）：

$$
q(z_t | z_{t-1}) = \mathcal{N}\left(z_t; \sqrt{1-\beta_t} z_{t-1}, \beta_t I\right)
$$

记 $\alpha_t = 1-\beta_t$，$\bar\alpha_t = \prod_{s=1}^t \alpha_s$，则有闭式：

$$
z_t = \sqrt{\bar\alpha_t} z_0 + \sqrt{1-\bar\alpha_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I) \tag{1.1}
$$

噪声预测网络 $\epsilon_\theta(z_t, t, y)$ 通过去噪得分匹配训练：

$$
\mathcal{L}_{DDPM} = \mathbb{E}_{z_0, t, \epsilon}\left[\|\epsilon - \epsilon_\theta(z_t, t, y)\|^2\right] \tag{1.2}
$$

Clean sample estimate（Tweedie's formula 的直接推论）:

$$
\boxed{\hat z_0^\theta = \frac{z_t - \sqrt{1-\bar\alpha_t} \epsilon_\theta(z_t, t, y)}{\sqrt{\bar\alpha_t}}} \tag{1.3}
$$

等价地，使用 score function $s_\theta(z_t, t, y) \approx \nabla_{z_t} \log p_t(z_t|y)$：

$$
\hat z_0^\theta = \frac{z_t + (1-\bar\alpha_t) s_\theta(z_t, t, y)}{\sqrt{\bar\alpha_t}} \tag{1.4}
$$

### 1.3 抓取力学基础

**接触模型**：第 $i$ 个接触点位于 $p_i \in \mathbb{R}^3$，接触法向为 $n_i$，接触力 $f_i \in \mathbb{R}^3$。

**Coulomb 摩擦锥**（多面体近似）：

$$
\mathcal{F}_i = \left\{ f_i = \sum_{\ell=1}^{L} d_{i\ell} \alpha_{i\ell} \;\middle|\; \alpha_{i\ell} \ge 0 \right\}
$$

其中 $\{d_{i\ell}\}_{\ell=1}^L$ 是线性化摩擦锥的第 $\ell$ 条边方向，满足 $n_i^\top d_{i\ell} \ge \frac{1}{\sqrt{1+\mu_i^2}} \|d_{i\ell}\|$。

**Grasp Wrench Matrix**：

$$
G(z) = \begin{bmatrix} w_{11} & w_{12} & \cdots & w_{1L} & \cdots & w_{ML} \end{bmatrix} \in \mathbb{R}^{6 \times ML} \tag{1.5}
$$

每个 primitive wrench：

$$
w_{i\ell} = \begin{bmatrix} d_{i\ell} \\ r_i \times d_{i\ell} \end{bmatrix} \in \mathbb{R}^6 \tag{1.6}
$$

其中 $r_i = p_i - c_o$ 是接触点相对物体质心 $c_o$ 的位置。

**力封闭条件**：抓取是力封闭的当且仅当 $G(z)$ 的列向量正张成 $\mathbb{R}^6$，即：

$$
\exists \alpha \succ 0 \quad \text{s.t.} \quad G(z)\alpha = 0 \tag{1.7}
$$

---

## 2. 问题形式化

### 2.1 原始框架的局限性

给定条件 $y$，一位扩散模型已能生成似真抓取：

$$
p_\theta(z|y) \quad \text{—— 覆盖 } \mathcal{D}_{train} \text{ 的分布}
$$

标准物理引导范式为：

$$
\tilde p(z|y) \propto p_\theta(z|y) \exp\left[-\sum_k \lambda_k E_k(z, y)\right] \tag{2.1}
$$

对应 guided score：

$$
s_{guided}(z_t, t, y) = s_\theta(z_t, t, y) - \nabla_{z_t} \left[\sum_k \lambda_k E_k(\hat z_0, y)\right] \tag{2.2}
$$

这一范式的三类结构性弱点：

1. **异方差梯度不可靠**：当 $t$ 大时，$\hat z_0$ 的 MSE $\propto \frac{1-\bar\alpha_t}{\bar\alpha_t}$，$\nabla E_k(\hat z_0)$ 近似于在高噪声样本上做随机扰动；
2. **无条件拉动**：即使 $\hat z_0$ 已安全（所有约束满足），$-\lambda_k \nabla E_k \neq 0$ 仍持续修正，破坏生成多样性；
3. **权重无理论校准**：$\lambda_k$ 手工设定，不随 $t$ 自适应，无概率含义。

### 2.2 C³ 的形式化目标

定义**安全抓取集** $\mathcal{S}_{safe}$。C³-Diffuser 求解：

$$
z_{t-1} \sim p_\theta(z_{t-1}|z_t, y) \quad \text{s.t.} \quad \mathbb{P}\left(z_0 \in \mathcal{S}_{safe} \mid z_t, y\right) \ge 1-\delta \tag{2.3}
$$

即：在 denoising 的每一步，我们要求从当前 $z_t$ 恢复的 **真实** $z_0$ 以高概率 $1-\delta$ 落在安全集中——而非仅要求点估计 $\hat z_0$ 安全。

---

## 3. 从 ABCD Energy 到 Safety Functions

### 3.1 Safety Function 的定义

对每类物理约束，定义 **safety function** $h_i: \mathcal{Z} \times \mathcal{Y} \to \mathbb{R}$，满足：

$$
h_i(z, y) \begin{cases}
> 0 & \text{安全，有余量} \\
= 0 & \text{在安全边界上（零水平集）} \\
< 0 & \text{违反安全约束}
\end{cases} \tag{3.1}
$$

与 penalty $E_i$ 的本质区别：

| 属性 | Penalty $E_i$ | Safety Function $h_i$ |
|------|---------------|------------------------|
| 零值含义 | 无约束含义（绝对值任意） | 安全边界（零水平集 $h_i=0$） |
| 梯度语义 | 下降方向（能量越低越好） | 进入安全集的方向（$h_i \ge 0$ 即止） |
| 几何结构 | 无天然水平集 | 定义安全流行 $\partial \mathcal{S}$ |
| QP 适配 | 需转换为约束 | 直接作为不等式约束 |

### 3.2 四类 Safety Functions 的完整构造

#### A 类：关节限位（执行安全集 $\mathcal{S}_{exec}$）

对每个关节 $j \in \{1, \dots, n_q\}$：

$$
\boxed{h_j^{lower}(q) = q_j - q_j^{\min} - \epsilon_q \ge 0} \tag{3.2}
$$

$$
\boxed{h_j^{upper}(q) = q_j^{\max} - q_j - \epsilon_q \ge 0} \tag{3.3}
$$

$\epsilon_q > 0$ 为安全余量，要求关节远离硬限位。梯度为解析常数：

$$
\nabla_q h_j^{lower} = e_j, \quad \nabla_q h_j^{upper} = -e_j \tag{3.4}
$$

其中 $e_j$ 是第 $j$ 个标准基向量。**此类约束不需要 chance-tightening**，因其不依赖 $\hat z_0$ 的几何估计。

#### B₁ 类：非穿透（接触安全集 $\mathcal{S}_{contact}$）

设物体 Signed Distance Function 为 $\phi_o(p)$（正 = 外，0 = 表面，负 = 内）。第 $k$ 个手部表面采样点 $p_k(z)$ 的穿透安全函数：

$$
\boxed{h_k^{pen}(z, y) = \phi_o\big(p_k(z)\big) - \epsilon_p \ge 0} \tag{3.5}
$$

梯度（链式法则经手部运动学雅可比）：

$$
\nabla_z h_k^{pen} = \left(\frac{\partial p_k}{\partial z}\right)^\top \nabla_p \phi_o(p_k) \tag{3.6}
$$

其中 $\frac{\partial p_k}{\partial z} = \begin{bmatrix} \frac{\partial p_k}{\partial T_w} & J_{hand}^{(k)}(q) \end{bmatrix}$，$J_{hand}^{(k)}$ 为第 $k$ 个采样点的位置雅可比。

#### B₂ 类：摩擦锥

对第 $i$ 个接触，分解力为法向 $f_{n,i} = n_i^\top f_i$ 和切向 $f_{t,i} = (I - n_i n_i^\top)f_i$：

$$
\boxed{h_i^{fric}(z, y) = \mu_i f_{n,i} - \|f_{t,i}\|_2 - \epsilon_f \ge 0} \tag{3.7}
$$

若静态抓取生成不显式输出 $f_i$，接触力由内层 force-closure QP 求解得到（见 §7）。

#### C 类：力封闭（力封闭安全集 $\mathcal{S}_{closure}$）

基于 grasp wrench matrix $G(z)$，定义可微分 force-closure residual：

$$
E_{fc}(z) = \min_{\alpha \succeq 0, \mathbf{1}^\top\alpha = 1} \|G(z)\alpha\|_2^2 \tag{3.8}
$$

若 $E_{fc}(z) = 0$，则存在非负系数使合力-力矩平衡——力封闭成立。安全函数：

$$
\boxed{h^{fc}(z, y) = \tau_{fc} - E_{fc}(z) \ge 0} \tag{3.9}
$$

阈值 $\tau_{fc}$ 由成功抓取数据集的经验分位数标定（见 §7.3）。

### 3.3 层次安全集的组织

$$
\boxed{\mathcal{S}_{safe} = \mathcal{S}_{exec} \cap \mathcal{S}_{contact} \cap \mathcal{S}_{closure}} \tag{3.10}
$$

其中：

$$
\mathcal{S}_{exec} = \left\{ z \mid h_j^{lower}(q) \ge 0,\; h_j^{upper}(q) \ge 0,\; \forall j \right\}
$$

$$
\mathcal{S}_{contact} = \left\{ z \mid h_k^{pen}(z) \ge 0,\; h_i^{fric}(z) \ge 0,\; \forall k, i \right\}
$$

$$
\mathcal{S}_{closure} = \left\{ z \mid h^{fc}(z) \ge 0 \right\}
$$

**D 类（任务成功：lift success, drop rate 等）不放入安全集，作为外部评估指标。** 安全抓取 $\neq$ 成功抓取——安全是成功的必要条件但非充分条件。

---

## 4. Chance Constraint 理论推导

### 4.1 后验不确定性建模

核心洞察：$\hat z_0^\theta$ 是 $z_0$ 的 MMSE 估计，而非确定性真值。其估计误差可表述为条件分布：

$$
\boxed{z_0 \mid z_t, y \sim \mathcal{N}\left(\hat z_0^\theta, \Sigma_t\right)} \tag{4.1}
$$

高斯假设的合理性：
- 对于充分训练的 score 网络，Tweedie's formula 的估计误差渐近正态（Laplace 近似）；
- $\Sigma_t$ 可通过扩散噪声水平自然校准：
  - 当 $t \to T$：$z_t$ 几乎纯噪声，$\hat z_0^\theta$ 方差大
  - 当 $t \to 0$：$\hat z_0^\theta$ 接近真实 $z_0$，方差小

**协方差校准方案**：

**方案 A（理论界——推荐原型使用）**：

由 DDPM 的 MSE 上界：

$$
\mathbb{E}\left[\|z_0 - \hat z_0^\theta\|^2\right] \le \frac{1-\bar\alpha_t}{\bar\alpha_t} \cdot \mathbb{E}\left[\|\epsilon - \epsilon_\theta\|^2\right]
$$

取各向同性近似：

$$
\boxed{\Sigma_t = \kappa_t^2 I, \quad \kappa_t = c \cdot \sqrt{\frac{1-\bar\alpha_t}{\bar\alpha_t}}} \tag{4.2}
$$

其中 $c$ 由模型在验证集上的 MSE 校准。

**方案 B（更精细——后续版本）**：

使用 $K$ 个 MC-dropout 前向传播估计经验协方差：

$$
\Sigma_t = \frac{1}{K-1} \sum_{k=1}^K \left(\hat z_0^{(k)} - \bar{\hat z_0}\right)\left(\hat z_0^{(k)} - \bar{\hat z_0}\right)^\top \tag{4.3}
$$

### 4.2 机会约束的线性化近似

对每个 safety function $h_i$，在 $\hat z_0^\theta$ 处一阶 Taylor 展开：

$$
h_i(z_0, y) \approx h_i(\hat z_0^\theta, y) + \nabla_z h_i(\hat z_0^\theta, y)^\top (z_0 - \hat z_0^\theta) \tag{4.4}
$$

记 $\Delta = z_0 - \hat z_0^\theta \sim \mathcal{N}(0, \Sigma_t)$。由高斯仿射变换不变性：

$$
\boxed{h_i(z_0, y) \mid z_t, y \;\sim\; \mathcal{N}\Big(h_i(\hat z_0^\theta),\; \nabla h_i^\top \Sigma_t \nabla h_i\Big)} \tag{4.5}
$$

均值：$h_i(\hat z_0^\theta)$，方差：$\sigma_{h_i}^2 = \nabla h_i^\top \Sigma_t \nabla h_i = \|\Sigma_t^{1/2} \nabla h_i\|_2^2$

### 4.3 机会约束转化为确定性不等式

要求：

$$
\mathbb{P}\big(h_i(z_0, y) \ge 0 \mid z_t, y\big) \ge 1 - \delta_i \tag{4.6}
$$

对一维高斯随机变量 $X \sim \mathcal{N}(\mu, \sigma^2)$，$\mathbb{P}(X \ge 0) \ge 1-\delta$ 等价于：

$$
\mu - \Phi^{-1}(1-\delta) \cdot \sigma \ge 0
$$

其中 $\Phi$ 为标准正态 CDF。记 $\beta_{\delta} = \Phi^{-1}(1-\delta)$，代入 (4.5) 得：

$$
\boxed{\bar h_i(\hat z_0^\theta, t, y) := h_i(\hat z_0^\theta, y) - \beta_{\delta_i} \left\|\Sigma_t^{1/2} \nabla_z h_i(\hat z_0^\theta, y)\right\|_2 \ge 0} \tag{4.7}
$$

### 4.4 Risk-Tightened Margin 的物理含义

$\bar h_i$ 包含两项：

| 项 | 含义 |
|----|------|
| $h_i(\hat z_0^\theta)$ | 确定性安全余量（点估计的安全程度） |
| $\beta_{\delta_i} \|\Sigma_t^{1/2} \nabla h_i\|$ | **不确定性惩罚**——安全函数在 $\hat z_0$ 不确定性方向上的标准差，按置信水平缩放 |

**自适应行为**：

$$
\begin{aligned}
t \to T \text{ (高噪声)} &\Rightarrow \Sigma_t \text{ 大} \Rightarrow \bar h_i \ll h_i \Rightarrow \text{更保守的安全要求} \\
t \to 0 \text{ (低噪声)} &\Rightarrow \Sigma_t \to 0 \Rightarrow \bar h_i \to h_i \Rightarrow \text{退化回确定性约束}
\end{aligned}
$$

这比手工设置 $\lambda(t)$ 的 annealing schedule 有严格概率基础：**$\beta_{\delta_i} = \Phi^{-1}(1-\delta_i)$ 取代了所有手工权重。**

### 4.5 线性化误差分析

定义二阶余项：

$$
r_i(z_0) = h_i(z_0) - \left[h_i(\hat z_0) + \nabla h_i(\hat z_0)^\top(z_0 - \hat z_0)\right]
$$

由 Taylor 余项定理：

$$
|r_i| \le \frac{1}{2} \sup_{\xi \in [\hat z_0, z_0]} \left\| \nabla^2 h_i(\xi) \right\|_2 \cdot \|z_0 - \hat z_0\|^2
$$

当 $\|z_0 - \hat z_0\|$ 小（diffusion 后期），$r_i = O(\|z_0-\hat z_0\|^2)$ 可忽略。**实践建议：仅在 $t \le t_{safe}$（如 $\bar\alpha_t \ge 0.3$）时启用完整 chance constraint，高噪声阶段仅用软惩罚。**

---

## 5. 最小干预 QP 投影

### 5.1 几何动机

Energy guidance 的修正方向由 $-\nabla E$ 完全确定——它总是指向能量下降最快的方向，而不问当前点是否已经在约束内。

设原始 clean estimate $\hat z_0^\theta$ 已满足所有 safety constraints。energy guidance 仍然施加非零修正，因为 $E_i \neq 0 \nRightarrow \nabla E_i = 0$（例如 $E_i = \max(0, -h_i)^2$ 在 $h_i > 0$ 时为零但其梯度为 0）。此问题可通过精心设计的 penalty 缓解但无法根除。

C³ 的替代思路：**仅在违反（或即将违反）安全约束时，以最小的欧几里得扰动修正 clean estimate。**

### 5.2 QP 形式化

设 $\hat z_0^\theta$ 为原始 clean estimate。在 $\hat z_0^\theta$ 处定义 risk-tightened safety set 的线性化切锥：

$$
\mathcal{T}_{\hat z_0^\theta} \bar{\mathcal{C}}_t = \left\{ z \mid \bar h_i(\hat z_0^\theta, t) + \nabla \bar h_i(\hat z_0^\theta, t)^\top (z - \hat z_0^\theta) \ge 0,\; \forall i \right\} \tag{5.1}
$$

求最小修正 $u = z - \hat z_0^\theta$：

$$
\boxed{
\begin{aligned}
u^\star = \arg\min_{u, \xi} \quad & \frac{1}{2} \|u\|_{W_t}^2 + \frac{\rho}{2} \sum_i \xi_i^2 \\
\text{s.t.} \quad & \bar h_i(\hat z_0^\theta, t) + \nabla \bar h_i(\hat z_0^\theta, t)^\top u \ge -\xi_i, \quad \forall i \\
& \xi_i \ge 0, \quad \forall i
\end{aligned}}
\tag{5.2}
$$

**各项含义**：

| 量 | 含义 |
|----|------|
| $u$ | clean estimate 的最小修正（主变量） |
| $\xi_i$ | slack 变量，软化第 $i$ 个约束（避免冲突时 QP 不可行） |
| $W_t \succ 0$ | 修正代价度量（初版可取 $I$；精细版可用 $\Sigma_t^{-1}$ 使修正沿不确定方向更容易） |
| $\rho > 0$ | slack 惩罚权重（大 → 接近硬约束；小 → 允许更多软化） |

### 5.3 QP 的对偶结构与稀疏性

构造 Lagrangian：

$$
L(u, \xi, \mu, \nu) = \frac{1}{2}\|u\|_{W_t}^2 + \frac{\rho}{2}\sum_i \xi_i^2 - \sum_i \mu_i\left[\bar h_i + \nabla \bar h_i^\top u + \xi_i\right] - \sum_i \nu_i \xi_i
$$

KKT 条件（假定 $W_t = I$ 简化表示）：

**Stationarity（对 $u$）**：

$$
u^\star - \sum_i \mu_i \nabla \bar h_i = 0 \quad \Longrightarrow \quad \boxed{u^\star = \sum_{i \in \mathcal{A}} \mu_i \nabla \bar h_i} \tag{5.3}
$$

**Stationarity（对 $\xi_i$）**：

$$
\rho \xi_i - \mu_i - \nu_i = 0 \quad \Longrightarrow \quad \mu_i = \rho \xi_i - \nu_i \tag{5.4}
$$

**Complementary slackness**：

$$
\mu_i\left[\bar h_i + \nabla \bar h_i^\top u + \xi_i\right] = 0, \quad \nu_i \xi_i = 0 \tag{5.5}
$$

**对偶解释**：由 (5.3)，最优修正 $u^\star$ 是**活跃约束梯度**的加权和，权重由对偶变量 $\mu_i$ 决定。只有被违反或紧的约束才具有 $\mu_i > 0$，已安全约束的 $\mu_i = 0$。这正是"最小干预"的数学本质——energy guidance 的 $-\lambda \sum \nabla E_i$ 对所有约束一视同仁。

### 5.4 Clean-Space 到 Diffusion-Space 的精确映射

**Case 1 — Score 参数化**：

由 (1.4)，$\hat z_0 = \frac{z_t + (1-\bar\alpha_t)s_\theta}{\sqrt{\bar\alpha_t}}$。希望 $\hat z_0^+ = \hat z_0 + u^\star$：

$$
\frac{z_t + (1-\bar\alpha_t)(s_\theta + \Delta s)}{\sqrt{\bar\alpha_t}} = \hat z_0 + u^\star
$$

$$
\Rightarrow \boxed{\Delta s = \frac{\sqrt{\bar\alpha_t}}{1-\bar\alpha_t} u^\star} \tag{5.6}
$$

最终 guided score：

$$
s_{C^3}(z_t, t, y) = s_\theta(z_t, t, y) + \frac{\sqrt{\bar\alpha_t}}{1-\bar\alpha_t} u^\star \tag{5.7}
$$

**Case 2 — $\epsilon$ 参数化（DDPM 中常用）**：

由 (1.3)，$\hat z_0 = \frac{z_t - \sqrt{1-\bar\alpha_t} \epsilon_\theta}{\sqrt{\bar\alpha_t}}$。希望 $\hat z_0^+ = \hat z_0 + u^\star$：

$$
\frac{z_t - \sqrt{1-\bar\alpha_t} (\epsilon_\theta + \Delta \epsilon)}{\sqrt{\bar\alpha_t}} = \hat z_0 + u^\star
$$

$$
\Rightarrow \boxed{\Delta \epsilon = -\frac{\sqrt{\bar\alpha_t}}{\sqrt{1-\bar\alpha_t}} u^\star} \tag{5.8}
$$

最终 corrected noise prediction：

$$
\boxed{\epsilon_\theta^+ = \epsilon_\theta - \frac{\sqrt{\bar\alpha_t}}{\sqrt{1-\bar\alpha_t}} u^\star} \tag{5.9}
$$

**量级分析**：当 $t \to 0$，$\frac{\sqrt{\bar\alpha_t}}{\sqrt{1-\bar\alpha_t}} \to \infty$，即使很小的 $u^\star$ 也会产生大的 $\Delta \epsilon$。这对应着 diffusion 后期修正的高精度需求。当 $t \to T$，该比值趋于 0，对应早期低精度阶段的弱修正。此比例因子**自然衔接了 diffusion 的 noise schedule 与 safety correction 的强度**，无需手工设计 weighting schedule。

---

## 6. 安全感知训练

### 6.1 问题：仅推理时投影的局限性

若 diffusion 模型从未见过安全约束信号，其生成的 $\hat z_0^\theta$ 可能系统性地远离 $\mathcal{S}_{safe}$，导致：
- 每步都需求解 QP（计算开销）；
- $u^\star$ 幅值大，破坏生成分布（即便最优 $u^\star$ 是局部最小的，全局看来样本已偏离数据流形）。

### 6.2 训练损失

$$
\boxed{\mathcal{L} = \mathcal{L}_{DDPM} + \lambda_{safe} \cdot \mathcal{L}_{safe}} \tag{6.1}
$$

其中：

$$
\mathcal{L}_{safe} = \mathbb{E}_{z_0, t, \epsilon}\left[ \sum_i \max\left(0, -\bar h_i(\hat z_0^\theta, t)\right)^2 \right] \tag{6.2}
$$

训练时，$\bar h_i$ 使用训练特化的协方差：

$$
\Sigma_t^{train} = \eta \cdot \frac{1-\bar\alpha_t}{\bar\alpha_t} \cdot I
$$

$\eta$ 通常取小于推理时 $c$ 的值（如 $\eta = 0.1c$），因训练时 $z_t$ 由真实 $z_0$ 构造，$\hat z_0^\theta$ 的 uncertainty 小于推理时从头生成。

### 6.3 梯度流分析

$\mathcal{L}_{safe}$ 通过 $\hat z_0^\theta$ 反传至去噪参数 $\theta$：

$$
\frac{\partial \mathcal{L}_{safe}}{\partial \theta} = \frac{\partial \mathcal{L}_{safe}}{\partial \hat z_0^\theta} \cdot \frac{\partial \hat z_0^\theta}{\partial \epsilon_\theta} \cdot \frac{\partial \epsilon_\theta}{\partial \theta} \tag{6.3}
$$

关键缩放因子：

$$
\frac{\partial \hat z_0^\theta}{\partial \epsilon_\theta} = -\frac{\sqrt{1-\bar\alpha_t}}{\sqrt{\bar\alpha_t}} \tag{6.4}
$$

当 $t$ 大（早期 diffusion 步），$\sqrt{\bar\alpha_t}$ 小，梯度被放大——恰好早期步骤最需要安全信号引导。此自然对齐是使用 $\mathcal{L}_{safe}$ 而非后处理约束的另一优势。

### 6.4 训练与推理的协同

训练后，模型参数 $\theta$ 已使 $\hat z_0^\theta$ 在分布上倾向安全区域。推理时：
- 大部分步骤 $\bar h_i \ge 0$ 已自然满足 → $u^\star = 0$，QP 跳过
- 仅在残余违反时 QP 介入 → $u^\star$ 幅值显著小于未训练情况
- 安全性从"外挂修正"转变为"生成分布的内在属性"

---

## 7. 力封闭可微形式的深化

### 7.1 基本 QP 形式

重新审视 (3.8) 的力封闭残差问题：

$$
E_{fc}(z) = \min_{\alpha} \|G(z)\alpha\|_2^2 \quad \text{s.t.} \quad \alpha \succeq 0,\; \mathbf{1}^\top\alpha = 1 \tag{7.1}
$$

这是一个带有单纯形约束的标准 QP。其解 $\alpha^\star(z)$ 关于 $z$ 的可微性：

**敏感度定理**：若 (7.1) 的最优活动集在 $z$ 的邻域内不变，则 $\alpha^\star(z)$ 在 $z$ 处可微，且：

$$
\frac{\partial E_{fc}}{\partial z} = 2 G(z)\alpha^\star \cdot \frac{\partial (G\alpha^\star)}{\partial z} \tag{7.2}
$$

在实践中，活动集切换可通过 entropy-regularized 平滑规避。

### 7.2 平滑替代（推荐原型使用）

添加 entropic barrier 使问题处处可微：

$$
E_{fc}^{smooth}(z) = \min_{\alpha \succeq 0, \mathbf{1}^\top\alpha = 1} \left\{ \|G(z)\alpha\|_2^2 + \eta \sum_\ell \alpha_\ell \log \alpha_\ell \right\} \tag{7.3}
$$

当 $\eta \to 0$ 时恢复原问题。$\nabla_z E_{fc}^{smooth}$ 通过隐函数定理计算，无需跟踪活动集。

### 7.3 阈值 $\tau_{fc}$ 的统计标定

$\tau_{fc}$ 不应手工选择。建议流程：

1. 收集成功抓取数据集 $\mathcal{D}_{succ}$（仿真或真实数据）
2. 对每个 $z \in \mathcal{D}_{succ}$ 计算 $E_{fc}(z)$
3. 取 90% 分位数：

$$
\tau_{fc} = \text{Quantile}_{0.9}\left(\{E_{fc}(z) \mid z \in \mathcal{D}_{succ}\}\right) \tag{7.4}
$$

这保证 90% 的成功抓取的 $E_{fc}$ 值通过 $h^{fc} \ge 0$，有明确的统计含义。

### 7.4 SVD 代理（用于最小可行原型）

在最简原型中可绕过内层 QP，直接使用 grasp wrench matrix 的最小奇异值：

$$
E_{fc}^{SVD}(z) = \sigma_{\min}\left(G(z)\right) \tag{7.5}
$$

若 $\sigma_{\min} > 0$ 则 $G(z)$ 满秩——力封闭的必要条件。梯度由奇异值微分的标准公式给出：

$$
\frac{\partial \sigma_{\min}}{\partial G_{ij}} = u_{\min}^{(i)} v_{\min}^{(j)} \tag{7.6}
$$

其中 $u_{\min}, v_{\min}$ 为 $\sigma_{\min}$ 的左右奇异向量。通过链式法则传递至 $z$。

**SVD vs QP 的权衡**：
- SVD：计算简单，梯度干净，但只是力封闭的必要条件（满秩 $\neq$ 力封闭）
- QP：更精确（充要条件的凸近似），但需要内层优化 + 隐函数微分

建议第一版用 SVD 验证整体框架，第二版替换为 QP。

---

## 8. 算法伪代码与实现细节

### 8.1 训练

```
Algorithm 1: C³-Diffuser Training

Input: dataset D = {(z₀, y)}, denoiser ε_θ, safety functions {h_i},
       risk level δ, noise schedule {ᾱ_t}, λ_safe
Output: trained ε_θ

for each iteration:
    1. (z₀, y) ~ D
    2. t ~ Uniform({1, ..., T})
    3. ε ~ N(0, I)
    4. z_t = √ᾱ_t · z₀ + √(1-ᾱ_t) · ε
    5. ε̂ = ε_θ(z_t, t, y)
    6. ẑ₀ = (z_t - √(1-ᾱ_t) · ε̂) / √ᾱ_t

    7. // 计算 risk-tightened margins
       for each safety function h_i:
           if h_i is deterministic (A类, C类):
               h̄_i = h_i(ẑ₀, y)
           else:  // B类 (penetration, friction)
               ∇h_i = compute_gradient(h_i, ẑ₀, y)
               κ_t = c · √((1-ᾱ_t) / ᾱ_t)
               h̄_i = h_i(ẑ₀, y) - β_δ · κ_t · ‖∇h_i‖₂

    8. L_safe = Σ_i [max(0, -h̄_i)]²
    9. L = ‖ε - ε̂‖² + λ_safe · L_safe
   10. θ ← θ - η · ∇_θ L
```

### 8.2 推理（DDPM Sampling + C³ Projection）

```
Algorithm 2: C³-Diffuser Sampling

Input: condition y, trained ε_θ, safety functions {h_i},
       noise schedules, risk levels δ_i, QP params (W_t, ρ)
Output: safe grasp z₀

1. z_T ~ N(0, I)
2. for t = T, ..., 1:
       // Step 1: nominal denoising
       ε̂ = ε_θ(z_t, t, y)
       ẑ₀ = (z_t - √(1-ᾱ_t) · ε̂) / √ᾱ_t

       // Step 2: compute risk-tightened margins
       for each h_i:
           compute h̄_i as in Algorithm 1

       // Step 3: early exit check
       if all h̄_i ≥ 0:
           u* = 0
       else:
           // Step 4: solve QP (see §8.3)
           u* = solve_QP({h̄_i}, {∇h̄_i}, W_t, ρ)

       // Step 5: correct epsilon
       ε̂⁺ = ε̂ - (√ᾱ_t / √(1-ᾱ_t)) · u*

       // Step 6: DDPM/DDIM step
       z_{t-1} = DDPM_step(z_t, ε̂⁺, t)

3. return z₀
```

### 8.3 QP 求解器选择与加速

**问题规模**（典型）：

| 项 | 数量 |
|----|------|
| 变量 $u$ | $\dim(z) \approx 30$ |
| Slack $\xi$ | $\le 30$（仅 active constraints） |
| 总变量 | $\le 60$ |

**求解方案**：

1. **原型**：使用 `cvxpy` + `OSQP` 求解（纯 Python，易调试）
2. **加速**：OSQP 对此类小规模 QP 可达 < 1ms/step
3. **进一步优化**：使用 active-set warm-start——将上一步的最优活动集作为当前步的初始猜测
4. **选择性启用**：仅在 $t \le t_{safe}$（如 $t \le 0.6T$）时启用 QP

**Active Constraints 筛选**：

- 关节限位：仅保留 $|h_j| \le \epsilon_{active}$（接近边界的关节）
- 非穿透：仅保留 top-K（如 $K=5$）最危险的穿透点（$h_k^{pen}$ 最小）
- 摩擦锥：仅保留有接触的约束
- 力封闭：始终保留 1 条

---

## 9. 理论保证

### 9.1 一阶安全保证

**命题**：修正后 clean estimate $\hat z_0^+ = \hat z_0^\theta + u^\star$ 满足：

$$
\bar h_i(\hat z_0^+) \ge -\xi_i + O(\|u^\star\|^2), \quad \forall i
$$

**证明**：对 $\bar h_i$ 在 $\hat z_0^\theta$ 处一阶展开：

$$
\bar h_i(\hat z_0^+) = \bar h_i + \nabla \bar h_i^\top u^\star + O(\|u^\star\|^2)
$$

由 QP 约束，$\bar h_i + \nabla \bar h_i^\top u^\star \ge -\xi_i$，代入即得。$\square$

若 slack $\xi_i = 0$ 且 $\|u^\star\|^2$ 可忽略（diffusion 后期），则 $\bar h_i(\hat z_0^+) \gtrsim 0$——修正后的一阶安全性成立。

### 9.2 概率安全保证（弱）

**命题**（Chance Satisfaction，线性化近似下）：若修正后 $\bar h_i(\hat z_0^+) \ge 0$，则在 §4 的线性化高斯后验假设下：

$$
\mathbb{P}\big(h_i(z_0, y) \ge 0 \mid z_t, y\big) \gtrsim 1 - \delta_i
$$

**证明**：由 (4.5)–(4.7) 的等价推导，$\bar h_i \ge 0 \iff \mu_{h_i} - \beta_{\delta_i}\sigma_{h_i} \ge 0 \iff \mathbb{P}(h_i(z_0) \ge 0) \ge 1-\delta_i$（在线性化近似下）。$\square$

**保证的边界**：
- 这是一个 **弱** 保证：依赖线性化 + 高斯假设
- 但它 **强于 energy guidance**（后者根本不给概率保证）
- 在 diffusion 后期（$\|u^\star\|$ 小，$\Sigma_t$ 小），两近似均渐近精确

### 9.3 不干预性质

**命题**：若 $\hat z_0^\theta \in \bar{\mathcal{C}}_t$（所有 $\bar h_i \ge 0$），则 $u^\star = 0$。

**证明**：$u = 0, \xi = \max(0, -\bar h_i) = 0$ 是 QP (5.2) 的可行解且目标值为 $0$。因目标函数非负，这是全局最优。$\square$

此性质保证 diffusion 的生成多样性在安全区域完全保留——关键的"不干预"保证。

---

## 10. 相关文献分层综述

### 第一层：灵巧手抓取 Diffusion（直接 baseline）

| 工作 | 会议 | 核心贡献 | C³ 的区别 |
|------|------|---------|----------|
| **DexGrasp Anything** | CVPR 2025 | Physics-aware diffusion；train + sample 阶段加入物理约束 | 我们用 **chance-constrained safety projection**，而非通用物理能量；最小干预 vs 全时梯度 |
| **DexDiffuser** | RA-L 2024 | Evaluator-guided diffusion + sampling refinement | 我们使用**显式 safety functions**，而非黑盒 evaluator；QP 投影有几何解释 |
| **DGTR** | arXiv 2025 | Transformer-based dexterous grasp diffusion | 正交（网络架构 vs 安全约束框架）；可组合 |
| **GraspDiff** | ECCV 2024 | Contact-centric grasp diffusion | 我们额外注入 **力封闭 chance constraint** |

### 第二层：Safety-Critical Diffusion（方法学 baseline）

| 工作 | 会议 | 核心贡献 | C³ 的区别 |
|------|------|---------|----------|
| **SafeDiffuser** | ICLR 2025 | CBF 嵌入 diffusion denoising procedure | 我们面向灵巧手构建 **contact-closure safety set**；使用 clean-sample uncertainty tightening；CBF 是确定性约束 |
| **Constrained Diffusers** | NeurIPS 2025 | Constrained Langevin sampling（projected / primal-dual / AL） | 我们不是通用约束采样；针对灵巧手的 **chance-constrained tangent projection**；最小干预设计 |
| **DSG** | NeurIPS 2024 | 使用辅助优化（safety guidance） | 我们使用 QP 而非辅助优化 |

### 第三层：可微力封闭与接触优化（工具方法）

| 工作 | 会议 | 核心贡献 | C³ 的区别 |
|------|------|---------|----------|
| **GraspQP** | CoRL 2025 | 可微 force-closure QP；多样且物理可行的抓取生成 | 我们将 force-closure QP 嵌入 diffusion **denoising 安全函数** |
| **ContactOpt** | CoRL 2024 | 可微接触优化 | 我们嵌入 diffusion sampling，非后处理优化 |
| **DFC** | RSS 2023 | 可微力封闭分类器 | 可用作 $E_{fc}$ 的替代方案 |

### 第四层：Chance-Constrained Optimization（理论基础）

| 工作 | 领域 | 核心贡献 | 与 C³ 的关系 |
|------|------|---------|------------|
| **CC-RRT** | IJRR 2011 | 运动规划中的机会约束 | 精神祖先——将机会约束引入扩散是新的组合 |
| **Risk-Aware RL** | NeurIPS 系列 | CVaR/风险感知策略优化 | 我们的风险度量更简单（单约束概率边界）但更可计算 |
| **Conformal Prediction** | JMLR 系列 | 分布自由的不确定性量化 | 可用于替代高斯假设，生成严格的概率保证 |

### Novelty Claim 定位

> Existing physics-guided grasp diffusion methods mainly use deterministic physical losses or learned evaluators. C³-Diffuser formulates dexterous grasp safety as **uncertainty-calibrated chance constraints** over clean-sample estimates and enforces them via **minimum-intervention tangent-cone projection** during denoising. It constructs a **hierarchical contact-closure safety set** — covering joint limits, non-penetration, friction cones, and force closure — that is specific to dexterous grasping and goes beyond generic safety constraints.

关键差异维度：

```
1. 确定性约束 → 机会约束（含不确定性校准）
2. 梯度下降修正 → 最小干预 QP 投影
3. 通用安全约束 → 灵巧手 contact-closure 安全集
4. 推理时外挂 → 训练+推理联合优化
```

---

## 11. 实验设计与待验证命题

### 11.1 核心待验证命题

**H₁（安全-成功率提升）**：C³-Diffuser 的 Safe Success Rate 显著高于 energy guidance baseline。

> 度量：SSR = $\frac{\#\{\text{safe AND successful grasps}\}}{\#\{\text{generated grasps}\}}$

**H₂（多样性保护）**：C³-Diffuser 的生成多样性不低于无约束 diffusion（因最小干预性质），而 energy guidance 显著降低多样性。

> 度量：Coverage (C), MMD, 或 grasp pose 的 pairwise distance 分布

**H₃（Uncertainty Calibration 有效）**：risk-tightened margin 优于确定性约束（ablation: 去掉 $\beta_{\delta}\|\Sigma^{1/2}\nabla h\|$ 项）。

> 关键对比：高噪声阶段的 safety violation rate

**H₄（训练协同有效）**：加入 $\mathcal{L}_{safe}$ 训练后，QP 求解频率和 $\|u^\star\|$ 幅值显著下降。

> 度量：QP trigger rate、$\mathbb{E}[\|u^\star\|]$、$\mathbb{E}[\|u^\star\|]$ 在训练过程中的收敛曲线

**H₅（力封闭是关键）**：包含 C 类 force-closure constraint 的 C³ 在物理扰动测试下鲁棒性优于仅含 A+B 的版本。

> 度量：disturbance rejection rate

### 11.2 实验环境与设置

| 组件 | 推荐方案 |
|------|---------|
| 仿真器 | Isaac Gym / SAPIEN |
| 灵巧手 | Shadow Hand / Allegro Hand |
| 物体集 | YCB / ContactDB / DexGrasp Anything 测试集 |
| 条件 $y$ | 物体点云 (1024 点) + 局部 SDF 体素 |
| 生成表示 | $z = (T_w, q)$ — 手腕 6D 位姿 + 关节角 |
| 去噪网络 | 基于 Transformer / PointNet++ 的 $\epsilon_\theta(z_t, t, y)$ |
| QP 求解器 | OSQP (cvxpy 原型 → C++ 加速) |
| 指标 | SSR, success rate, mean penetration, joint violation, fc residual, diversity, QP time |

### 11.3 Ablation 矩阵

| # | 配置 | 验证命题 |
|---|------|---------|
| 1 | Base Diffusion (无任何安全约束) | baseline |
| 2 | + Energy Guidance ($\sum \lambda_i E_i$) | 对比 H₁, H₂ |
| 3 | + Deterministic QP Projection (无 $\beta\delta$ 项) | 验证 H₃ |
| 4 | + C³ w/o Force Closure (仅 A+B) | 验证 H₅ |
| 5 | + C³ w/o Training ($\mathcal{L}_{DDPM}$ only) | 验证 H₄ |
| 6 | **Full C³-Diffuser** | 完整方法 |

### 11.4 关键对比实验

**对比 1：Energy Guidance vs QP Projection**

- 固定相同的 safety functions
- Energy guidance 调 $\lambda_i$ 到最优
- QP projection 使用相同 $\beta_{\delta}$ 和 $\Sigma_t$
- 比较：SSR、diversity、penetration depth、joint violation

**对比 2：Deterministic vs Chance-Tightened**

- 两组 QP 投影：一组用 $\bar h_i$（含风险紧缩），一组用 $h_i$ 直接
- 在高噪声阶段分组报告 safety violation rate
- 预期：Chance-tightened 在高噪声阶段 violation 更低

**对比 3：with vs without Force Closure**

- A+B 约束 vs A+B+C 约束
- 施加随机干扰力（方向随机，幅值从 0 递增）
- 记录 first-drop force 作为鲁棒性指标

**对比 4：with vs without 安全感知训练**

- 未训练 vs 训练后推理
- 报告：QP trigger rate、mean $\|u^\star\|$、生成质量（FID-style metric）
- 预期：训练后 QP trigger rate 从 ~80% 降至 ~20%

### 11.5 灵敏性分析

| 参数 | 范围 | 预期影响 |
|------|------|---------|
| $\delta$ (风险水平) | 0.01–0.3 | $\delta \uparrow \Rightarrow$ 约束放松 $\Rightarrow$ SSR 可能下降但 diversity 上升 |
| $\rho$ (slack 惩罚) | 1–1000 | $\rho \uparrow \Rightarrow$ 接近硬约束 $\Rightarrow$ QP 可能无可行解 |
| $K$ (穿透 top-K) | 3–20 | $K \uparrow \Rightarrow$ 穿透防护更全但 QP 更慢 |
| $\lambda_{safe}$ (训练权重) | 0.01–1.0 | $\lambda_{safe} \uparrow \Rightarrow$ 安全更强但可能降低生成质量 |
| $t_{safe}$ (QP 启用阈值) | 0.3T–0.8T | $t_{safe} \uparrow \Rightarrow$ 更早期启用 QP $\Rightarrow$ 更多安全修正但更多计算 |

---

## 12. 风险与缓解

| 风险 | 可能性 | 严重性 | 缓解策略 |
|------|--------|--------|---------|
| QP 投影与 energy guidance 的实验差异不显著 | 中 | 致命 | 先在简单任务（关节限位+非穿透，无摩擦锥/力封闭）验证，确保 QP 投影本身的优势成立 |
| 高斯后验假设被审稿人质疑 | 高 | 中 | 明确标注为线性化近似，实验上比较 with/without uncertainty tightening |
| 力封闭内层 QP 实现过于复杂 | 高 | 中 | 第一版用 SVD proxy，完整 QP 放第二版或 appendix |
| 高噪声阶段 chance constraint 过于保守 | 中 | 中 | 引入 early-stage 软惩罚 + late-stage chance constraint 的混合策略 |
| 安全约束过强导致 success rate 下降 | 中 | 中 | 引入 slack、报告 safety-success trade-off 曲线（Pareto front） |
| 推理时间过长（每步 QP） | 低 | 低 | OSQP 对 ~60 维变量 < 1ms；选择性启用；warm-start |

---

## 附录 A：核心公式速查

| 公式 | 编号 |
|------|------|
| Clean estimate | $\hat z_0^\theta = \frac{z_t - \sqrt{1-\bar\alpha_t}\epsilon_\theta}{\sqrt{\bar\alpha_t}}$ | (1.3) |
| Safety function 定义 | $h_i(z,y) \ge 0$ 安全, $<0$ 违反 | (3.1) |
| Risk-tightened margin | $\bar h_i = h_i - \beta_{\delta_i}\|\Sigma_t^{1/2}\nabla h_i\|_2$ | (4.7) |
| 机会约束 | $\mathbb{P}(h_i(z_0) \ge 0 \mid z_t) \ge 1-\delta_i$ | (4.6) |
| QP 投影 | $u^\star = \arg\min_{u,\xi} \frac{1}{2}\|u\|^2 + \frac{\rho}{2}\sum\xi_i^2 \text{ s.t. } \bar h_i + \nabla\bar h_i^\top u \ge -\xi_i$ | (5.2) |
| Epsilon 修正 | $\epsilon_\theta^+ = \epsilon_\theta - \frac{\sqrt{\bar\alpha_t}}{\sqrt{1-\bar\alpha_t}}u^\star$ | (5.9) |
| 训练损失 | $\mathcal{L} = \mathcal{L}_{DDPM} + \lambda_{safe}\sum_i \max(0,-\bar h_i)^2$ | (6.1–6.2) |
| 层次安全集 | $\mathcal{S}_{safe} = \mathcal{S}_{exec} \cap \mathcal{S}_{contact} \cap \mathcal{S}_{closure}$ | (3.10) |
