---
tags:
  - 灵巧手专项
  - safe_dexterous_grasping
  - diffusion
  - contact_mechanics
  - chance_constrained_QP
created: 2026-06-20
related:
  - "[[灵巧手专项/C3-Diffuser算法创新点与可行性验证.md]]"
  - "[[灵巧手专项/ABCD物理约束注入Diffusion数学推导.md]]"
---

# C³-Diffuser：面向接触力学的 Chance-Constrained Safety Projection

## 0. ABCD 分层处理原则

不统一编码四类约束。每类数学结构不同，分层处理：

| 类别 | 处理方式 | 理由 |
|---|---|---|
| **A** 关节限位 | 硬约束（barrier / clip），不进入 QP | 确定性解析不等式，无 uncertainty 来源 |
| **B** 非穿透 + 摩擦锥 | **chance-constrained QP 投影** ← 本文焦点 | diffusion 位姿噪声 → SDF/法向查询不可靠 → 约束违反概率不可忽略 |
| **C** 力封闭 | 辅助惩罚项，加在训练 loss 中 | 已含内层 QP，嵌套 chance constraint 计算爆炸 |
| **D** 任务成功 | 不进入约束，做最终评估指标 | 不可微仿真依赖，作为 safe success rate 的分子 |

**C³-Diffuser 的核心贡献收窄为一句：在 diffusion denoising 中，对 B 类接触力学约束做 uncertainty-calibrated minimum-intervention safety projection。**

---

## 1. B 类 Safety Functions

### 1.1 变量

抓取变量 $z = (T_w, q)$，$T_w \in SE(3)$ 手腕位姿，$q \in \mathbb{R}^{n_q}$ 关节角。条件 $y$：物体点云/SDF $\phi_o(p)$，约定外部 $\phi_o > 0$，表面 $\phi_o = 0$，内部 $\phi_o < 0$。

第 $k$ 个手部采样点 $p_k(z)$，表面法向 $n_k = \nabla \phi_o(p_k) / \|\nabla \phi_o(p_k)\|$。

### 1.2 非穿透

$$h_k^{pen}(z) = \phi_o(p_k(z)) - \epsilon_p$$

要求 $h_k^{pen} \ge 0$。梯度：

$$\nabla_z h_k^{pen} = \underbrace{\left(\frac{\partial p_k}{\partial z}\right)^\top}_{\text{手部雅可比}} \underbrace{\nabla_p \phi_o(p_k)}_{\text{SDF 法向}}$$

### 1.3 摩擦锥

接触力分解：$f_{n,i} = n_i^\top f_i$，$f_{t,i} = (I - n_i n_i^\top) f_i$。Coulomb 条件 $\|f_{t,i}\| \le \mu_i f_{n,i}$。

$$h_i^{fric}(z) = \mu_i f_{n,i} - \|f_{t,i}\|_2 - \epsilon_f$$

要求 $h_i^{fric} \ge 0$。

若 $z$ 不显式包含 $f_i$，则 $f_i$ 由接触模型给出（如 point-contact 法向力正比于穿透深度的 spring-damper，或由力封闭内层 QP 解得）。

---

## 2. 推导一：Chance Constraint → Risk-Tightened Margin

### 2.1 问题

DDPM 第 $t$ 步，从 $z_t$ 预测 clean estimate：

$$\hat{z}_0 = \frac{z_t - \sqrt{1 - \bar{\alpha}_t}\,\epsilon_\theta(z_t, t, y)}{\sqrt{\bar{\alpha}_t}}$$

高噪声时 ($t$ 大)，$\hat{z}_0$ 位姿误差可达厘米级，SDF 查询位置偏移显著，穿透判断不可靠。**直接要求 $h_k^{pen}(\hat{z}_0) \ge 0$ 产生错误梯度。**

### 2.2 后验建模

$$z_0 \mid z_t, y \sim \mathcal{N}(\hat{z}_0, \Sigma_t)$$

取 $\Sigma_t = \kappa_t^2 I$，$\kappa_t = c\sqrt{1 - \bar{\alpha}_t}$。物理直觉：噪声水平正比于 clean estimate 的不确定性。

### 2.3 机会约束

$$\mathbb{P}\left(h_i(z_0) \ge 0 \mid z_t, y\right) \ge 1 - \delta_i$$

一阶 Taylor：$h_i(z_0) \approx h_i(\hat{z}_0) + \nabla h_i(\hat{z}_0)^\top(z_0 - \hat{z}_0)$。

因 $z_0 - \hat{z}_0 \sim \mathcal{N}(0, \Sigma_t)$：

$$h_i(z_0) \sim \mathcal{N}\left(h_i(\hat{z}_0),\; \nabla h_i^\top \Sigma_t \nabla h_i\right)$$

机会约束等价于：

$$h_i(\hat{z}_0) - \Phi^{-1}(1 - \delta_i) \cdot \|\Sigma_t^{1/2} \nabla h_i(\hat{z}_0)\|_2 \ge 0$$

令 $\beta_\delta = \Phi^{-1}(1 - \delta)$，定义：

$$\boxed{\bar{h}_i(\hat{z}_0, t) = h_i(\hat{z}_0) - \beta_{\delta_i} \left\| \Sigma_t^{1/2} \nabla h_i(\hat{z}_0) \right\|_2}$$

### 2.4 物理含义

$\|\Sigma_t^{1/2} \nabla h_i\|$ 是 $h_i$ 在 posterior 不确定性下的标准差。

- $t$ 大 → $\Sigma_t$ 大 → 减项大 → $\bar{h}_i$ 更保守 → 高噪声时远离边界
- $t$ 小 → $\Sigma_t \to 0$ → $\bar{h}_i \to h_i$ → 低噪声时收紧至确定性约束

**$\beta_\delta$ 替代了手工调参的 $\lambda_B$，且有概率含义：$\delta = 0.05$ 表示允许 5% 的约束违反概率。**

### 2.5 非穿透的具体形式

代入 $\Sigma_t = \kappa_t^2 I$：

$$\bar{h}_k^{pen} = \phi_o(p_k(\hat{z}_0)) - \epsilon_p - \beta_\delta \cdot \kappa_t \cdot \left\| \nabla_z \phi_o(p_k(\hat{z}_0)) \right\|_2$$

$\nabla_z \phi_o = J_k^\top \nabla_p \phi_o$ 是 SDF 值对抓取变量的敏感度。敏感度越大（手离表面近且法向对齐良好），不确定性惩罚越大。

---

## 3. 推导二：最小干预 QP 投影

### 3.1 为什么不用梯度

$$s_{guided} = s_\theta - \lambda_B \nabla_z E_B$$

问题：(a) $\lambda_B$ 恒定，不随 $t$ 变化；(b) 即使 $\hat{z}_0$ 已安全，梯度仍拉动。

### 3.2 QP 形式

$$\boxed{u^\star = \arg\min_{u, \xi} \frac{1}{2}\|u\|^2 + \frac{\rho}{2}\sum_i \xi_i^2}$$

$$\text{s.t.} \quad \bar{h}_i(\hat{z}_0^\theta, t) + \nabla \bar{h}_i^\top u \ge -\xi_i, \quad \xi_i \ge 0$$

- $u \in \mathbb{R}^{\dim(z)}$：对 clean estimate 的修正
- $\xi_i$：slack，保证 QP 可行
- $\rho$：slack 代价，$\rho \to \infty$ 趋近硬约束

**关键性质：若 $\forall i, \bar{h}_i \ge 0$，则 $u^\star = 0$。仅在违反或接近违反时干预。**

### 3.3 修正映射

$$\hat{z}_0^+ = \hat{z}_0^\theta + u^\star$$

由 $\hat{z}_0 = (z_t - \sqrt{1 - \bar{\alpha}_t}\,\epsilon_\theta) / \sqrt{\bar{\alpha}_t}$，代入得：

$$\boxed{\epsilon_\theta^+ = \epsilon_\theta - \frac{\sqrt{\bar{\alpha}_t}}{\sqrt{1 - \bar{\alpha}_t}} u^\star}$$

随后用 $\epsilon_\theta^+$ 做 DDPM/DDIM 更新。

---

## 4. 推导三：安全感知训练

### 4.1 训练损失

$$\boxed{\mathcal{L} = \underbrace{\mathbb{E}\left[\|\epsilon - \epsilon_\theta\|^2\right]}_{\mathcal{L}_{DDPM}} + \lambda \cdot \underbrace{\mathbb{E}\left[\sum_{i \in \mathcal{B}} \max(0, -\bar{h}_i)^2\right]}_{\mathcal{L}_{safe}}}$$

仅对 B 类 safety function 施加 $\mathcal{L}_{safe}$。A 类在采样后 clip，C 类可选加入 $\lambda_C E_{fc}$。

### 4.2 效果

训练反传梯度 $\partial \mathcal{L}_{safe}/\partial \theta$ 迫使 denoiser 学会生成 $\hat{z}_0$ 时自动远离穿透和摩擦锥违反。收敛后推理时大部分步 $\bar{h}_i \ge 0$，QP 跳过。

---

## 5. 一步算法的完整形式

```
输入：z_t, t, y, ε_θ, φ_o, {δ_i}, ρ
输出：z_{t-1}

1. ε̂ = ε_θ(z_t, t, y)
2. ẑ₀ = (z_t - √(1-ᾱ_t)·ε̂) / √(ᾱ_t)
3. 对每个手部采样点 k：
     h̄_k = φ_o(p_k(ẑ₀)) - ε_p - β_δ·κ_t·‖J_kᵀ∇φ_o‖
4. 对每个接触 i：
     h̄_i = μ·f_{n,i} - ‖f_{t,i}‖ - ε_f - β_δ·κ_t·‖∇h_i^{fric}‖
5. 若 ∃ h̄ < 0：
     解 QP → u*
     ε̂⁺ = ε̂ - (√(ᾱ_t)/√(1-ᾱ_t))·u*
   否则 ε̂⁺ = ε̂
6. z_{t-1} = DDPM_step(z_t, ε̂⁺, t)
```

---

## 6. A/C/D 的协同处理

不进入 QP，但保留在系统里：

| 类别 | 位置 | 具体做法 |
|---|---|---|
| **A** 关节限位 | step 2 之后 | $\hat{q} \leftarrow \operatorname{clip}(\hat{q}, q_{\min} + \epsilon_q, q_{\max} - \epsilon_q)$ |
| **C** 力封闭 | 训练 loss | $\mathcal{L} += \lambda_C \cdot E_{fc}(\hat{z}_0)$，推理阶段仅报告不约束 |
| **D** 任务成功 | 评估 | Safe Success Rate $= \mathbf{1}[Success \land \min_i h_i^{B} \ge 0]$ |

---

## 7. 最小可行实验

1. **backbone**：现成灵巧手抓取 diffusion（如 DexGrasp Anything 开源权重）
2. **约束**：仅 B 类非穿透（top-16 手部采样点），暂不加摩擦锥
3. **对比**：
   - Baseline：无约束采样
   - Energy guidance：$-\lambda_B \nabla E_{pen}$
   - C³ (deterministic)：$\bar{h} = h$（$\beta = 0$，去掉 chance tightening）
   - **C³ (full)**：$\beta_{\delta} > 0$
4. **指标**：Safe Success Rate、mean penetration depth、grasp diversity、QP skip rate

**最关键的一条曲线：** $\|u^\star\|$ 随 denoising step 的变化。安全感知训练后，该曲线应从"全程非零"收敛到"后期归零"。
