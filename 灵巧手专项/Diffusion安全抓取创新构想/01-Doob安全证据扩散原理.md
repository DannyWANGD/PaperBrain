---
title: "Doob安全证据扩散：把灵巧手安全抓取写成终点事件条件化"
created: 2026-06-23
status: idea-principle-v1
tags:
  - dexterous_grasping
  - diffusion
  - doob_h_transform
  - safe_generation
  - physical_evidence
---

# Doob安全证据扩散：把灵巧手安全抓取写成终点事件条件化

> 本文只整理第一条理论思路：**不要把物理约束先验地写成 penalty，也不要把生成结果投影到约束集，而是把安全抓取看成 diffusion 终点事件 \(S\)，再用 Doob \(h\)-transform 把这个事件沿 denoising 时间向前传播。**
>
> 这条路线的核心创新不在灵巧手力学公式本身，而在 diffusion 的使用方式：物理安全不再是外接 loss，而是反向扩散路径测度的条件证据。

---

## 1. 一句话主张

给定物体观测 \(y\)，普通 diffusion 生成抓取：

$$
z_0\sim p_\theta(z_0|y),
$$

其中 \(z_0\) 可以是静态抓取姿态、手腕位姿和关节角：

$$
z_0=(T_w,q),
$$

也可以是未来动作片段。安全抓取真正需要的不是 \(p_\theta(z_0|y)\)，而是：

$$
p_\theta(z_0|y,S),
$$

其中

$$
S=\{\text{最终样本是安全、可执行、稳定的抓取}\}.
$$

本文的核心命题是：

$$
\boxed{
\nabla_{z_t}\log p_t(z_t|y,S)
=
\nabla_{z_t}\log p_t(z_t|y)
+
\nabla_{z_t}\log h_t(z_t,y)
}
$$

其中

$$
\boxed{
h_t(z_t,y)=\mathbb P_\theta(S|z_t,y)
}
$$

表示从当前 diffusion 中间状态 \(z_t\) 继续反向采样，最终落入安全抓取事件 \(S\) 的概率。

这就是 Doob 安全证据扩散的全部出发点。安全引导不是：

$$
-\lambda\nabla E_{phys}(z),
$$

而是：

$$
\nabla\log \mathbb P(S|z_t,y).
$$

这一区别非常关键。前者是手工能量下降方向，后者是安全条件分布的精确 score 修正项，如果 \(h_t\) 估计准确，则它直接对应 \(p(z_0|y,S)\) 的采样。

---

## 2. 为什么不要从物理 penalty 开始

传统物理 guidance 常写为：

$$
\tilde p(z_0|y)
\propto
p_\theta(z_0|y)\exp[-\lambda E_{phys}(z_0,y)].
$$

这种写法有直观优点，但它在顶会层面的理论新意有限，原因不是它无效，而是它把问题提前固定成了“找一个能量函数”。这会带来三个结构性限制。

第一，物理项的尺度是人为的。穿透深度、接触距离、扰动稳定性、关节边界这些量没有天然统一单位，因此 \(\lambda\) 很难有清晰概率意义。

第二，物理梯度通常是局部的。一个样本当前穿透小，不代表继续生成后安全；一个 noisy state 的 clean estimate 近似安全，也不代表 posterior 中大多数可能终点安全。

第三，某些重要物理判断本来就不是光滑可微的。例如简单扰动下是否掉落、是否完成 lift、是否在多个随机扰动中保持稳定。这些更自然地是事件 \(S\)，不是解析能量。

Doob 安全证据扩散换一个建模顺序：

1. 先定义最终什么叫安全，即事件 \(S\)。
2. 再学习任意 diffusion 时间 \(t\) 下的安全生存概率 \(h_t(z_t,y)\)。
3. 最后用 \(\nabla\log h_t\) 修改反向扩散 score。

这让物理约束从“样本上的 penalty”变成“路径上的 evidence”。

---

## 3. 基础 diffusion 记号

采用标准 DDPM 前向过程：

$$
q(z_t|z_0)
=
\mathcal N
\left(
\sqrt{\bar\alpha_t}z_0,
(1-\bar\alpha_t)I
\right),
$$

等价地：

$$
z_t
=
\sqrt{\bar\alpha_t}z_0
+
\sqrt{1-\bar\alpha_t}\epsilon,
\qquad
\epsilon\sim\mathcal N(0,I).
$$

噪声预测模型为：

$$
\epsilon_\theta(z_t,t,y).
$$

对应 score 近似为：

$$
s_\theta(z_t,t,y)
\approx
\nabla_{z_t}\log p_t(z_t|y)
=
-\frac{\epsilon_\theta(z_t,t,y)}{\sqrt{1-\bar\alpha_t}}.
$$

普通采样只沿 \(s_\theta\) 去 denoise。它生成的是数据分布意义下合理的抓取，但不保证条件事件 \(S\)。

---

## 4. 把安全抓取定义为终点事件

这里不要把 ABCD 约束全部塞进来。第一版最小理论 baseline 只需要定义一个有辨识度、能证明效果的安全事件：

$$
S
=
S_{\text{geom}}
\cap
S_{\text{contact}}
\cap
S_{\text{survive}}.
$$

可以取：

$$
S_{\text{geom}}
=
\{\text{关节不过界，手物穿透深度低于阈值}\},
$$

$$
S_{\text{contact}}
=
\{\text{至少若干关键指尖或指腹接近物体表面，且接触分布不过度塌缩}\},
$$

$$
S_{\text{survive}}
=
\{\text{轻量 lift 或扰动测试中物体不掉落}\}.
$$

注意这里的 \(S\) 不要求可微。它可以来自解析检测、近似仿真、扰动测试、人工规则、已训练 evaluator，甚至多个来源的组合标签。Doob 方案只需要最终事件标签或软概率：

$$
r(z_0,y)\in[0,1],
$$

其中硬事件时：

$$
r(z_0,y)=\mathbf 1_S(z_0,y).
$$

如果使用软标签，可以理解为：

$$
r(z_0,y)=\mathbb P(S|z_0,y).
$$

这一步打开了比 penalty guidance 更大的空间：不可微物理判断也能进入 diffusion，只要它能被当作终点 evidence。

---

## 5. 从终点事件到任意 diffusion 时刻

关键定义：

$$
h_t(z_t,y)
=
\mathbb P_\theta(S|z_t,y).
$$

如果 \(S\) 是硬事件：

$$
h_t(z_t,y)
=
\mathbb E_{p_\theta(z_0|z_t,y)}
\left[
\mathbf 1_S(z_0,y)
\right].
$$

如果 \(S\) 是软事件：

$$
h_t(z_t,y)
=
\mathbb E_{p_\theta(z_0|z_t,y)}
\left[
r(z_0,y)
\right].
$$

这就是“安全证据传播”。当前 \(z_t\) 本身可能是高噪声的，没有直接物理意义；但是它包含关于最终 \(z_0\) 的 posterior 信息。\(h_t\) 不是问“当前 noisy 姿态是否物理合理”，而是问：

> 如果从当前 \(z_t\) 继续按模型反向生成，最终变成安全抓取的概率有多大？

这和直接在 \(\hat z_0\) 上算物理能量完全不同。后者只看一个 clean estimate，前者看的是当前状态诱导出的整个未来终点分布。

---

## 6. 条件 score 的推导

由 Bayes 公式：

$$
p_t(z_t|y,S)
=
\frac{
p_t(z_t|y)\mathbb P(S|z_t,y)
}{
\mathbb P(S|y)
}.
$$

代入 \(h_t\)：

$$
p_t(z_t|y,S)
=
\frac{
p_t(z_t|y)h_t(z_t,y)
}{
\mathbb P(S|y)
}.
$$

对 \(z_t\) 取对数梯度：

$$
\nabla_{z_t}\log p_t(z_t|y,S)
=
\nabla_{z_t}\log p_t(z_t|y)
+
\nabla_{z_t}\log h_t(z_t,y).
$$

因此安全条件 score 为：

$$
\boxed{
s_{\text{safe}}(z_t,t,y)
=
s_\theta(z_t,t,y)
+
\nabla_{z_t}\log h_t(z_t,y)
}
$$

这条公式是整篇工作的理论核心。它说明只要能估计 \(h_t\)，就不需要手写物理能量梯度，也不需要投影优化器。安全约束自然进入反向扩散 score。

如果实际的 \(h_\phi\) 不是完美估计，可以引入温度：

$$
s_{\text{safe}}
=
s_\theta
+
\omega_t\nabla_{z_t}\log h_\phi(z_t,t,y).
$$

但需要在论文中强调：\(\omega_t\) 是近似补偿或风险偏好，而不是物理 penalty 的任意权重。理想情况下 \(\omega_t=1\)。

---

## 7. 离散 DDPM 中如何进入噪声预测

若模型使用 epsilon prediction：

$$
s_\theta
=
-\frac{\epsilon_\theta}{\sqrt{1-\bar\alpha_t}}.
$$

安全 score：

$$
s_{\text{safe}}
=
-\frac{\epsilon_\theta}{\sqrt{1-\bar\alpha_t}}
+
\omega_t\nabla_{z_t}\log h_\phi(z_t,t,y).
$$

把它重新写成 epsilon：

$$
\epsilon_{\text{safe}}
=
-\sqrt{1-\bar\alpha_t}s_{\text{safe}}.
$$

于是：

$$
\boxed{
\epsilon_{\text{safe}}
=
\epsilon_\theta
-
\omega_t\sqrt{1-\bar\alpha_t}
\nabla_{z_t}\log h_\phi(z_t,t,y)
}
$$

这就是最小实现所需的采样改动。

伪代码：

```text
for t = T, ..., 1:
    eps = eps_theta(z_t, t, y)
    log_h = log(h_phi(z_t, t, y) + eps_num)
    g = grad_z_t(log_h)
    eps_safe = eps - omega_t * sqrt(1 - alpha_bar_t) * g
    z_{t-1} = DDPM_or_DDIM_step(z_t, eps_safe, t)
```

注意：这里的 \(h_\phi\) 输入是 \(z_t,t,y\)，而不是只输入最终 clean sample。这样它才是真正的 diffusion-time safety evidence，而不是普通终点分类器。

---

## 8. 如何训练 \(h_\phi\)

最直接的训练数据构造：

1. 从抓取样本或 diffusion 生成样本中得到 \(z_0\)。
2. 用轻量物理检查或仿真得到事件标签：

$$
r=\mathbf 1_S(z_0,y)
\quad
\text{或}
\quad
r\in[0,1].
$$

3. 随机采样 diffusion 时间 \(t\) 和噪声：

$$
z_t
=
\sqrt{\bar\alpha_t}z_0
+
\sqrt{1-\bar\alpha_t}\epsilon.
$$

4. 训练：

$$
\mathcal L_h
=
\mathbb E_{z_0,t,\epsilon}
\left[
\operatorname{BCE}
\left(
h_\phi(z_t,t,y),
r(z_0,y)
\right)
\right].
$$

在统计意义下，BCE 的最优解满足：

$$
h_\phi^\star(z_t,t,y)
=
\mathbb E[r(z_0,y)|z_t,t,y].
$$

也就是：

$$
h_\phi^\star(z_t,t,y)
=
\mathbb P(S|z_t,y).
$$

这正是 Doob 引导所需要的 \(h_t\)。

### 8.1 这不是普通 grasp evaluator

普通 evaluator 学的是：

$$
p_\psi(S|z_0,y).
$$

Doob 安全证据模型学的是：

$$
p_\phi(S|z_t,t,y).
$$

二者的区别很大。后者必须理解不同噪声水平下的未来可恢复性。

在高噪声阶段，一个 \(z_t\) 可能对应很多可能终点，\(h_t\) 应该更平滑。到了低噪声阶段，posterior 收缩，\(h_t\) 才应变得尖锐。这种时间依赖性是 diffusion 特有的，也是本文理论创新的主要来源。

---

## 9. 可加入的 Doob 一致性正则

为了让 \(h_\phi\) 更像真正的 space-time harmonic function，可以加入一个 diffusion-time consistency 约束。

真实的 \(h_t\) 满足：

$$
h_t(z_t,y)
=
\mathbb E
\left[
h_{t-\Delta}(z_{t-\Delta},y)
\mid
z_t,y
\right],
$$

其中 \(z_{t-\Delta}\) 由当前反向模型从 \(z_t\) 走一步得到。可以构造正则：

$$
\mathcal L_{\text{Doob}}
=
\mathbb E
\left[
\left(
h_\phi(z_t,t,y)
-
\operatorname{stopgrad}
\left[
\frac{1}{K}
\sum_{k=1}^{K}
h_\phi(z_{t-\Delta}^{(k)},t-\Delta,y)
\right]
\right)^2
\right].
$$

最终：

$$
\mathcal L
=
\mathcal L_h
+
\lambda_{\text{Doob}}\mathcal L_{\text{Doob}}.
$$

这不是必须的工程模块，但它是一个很好的论文创新点。它把 \(h_\phi\) 从“time-conditioned classifier”提升为“反向扩散路径上的安全证据函数”。

---

## 10. 和 classifier guidance 的关系

经典 classifier guidance 写成：

$$
\nabla_x\log p(x|c)
=
\nabla_x\log p(x)
+
\nabla_x\log p(c|x).
$$

表面上 Doob 安全证据扩散很像 classifier guidance，但差异在于：

| 项目 | 普通 classifier guidance | Doob 安全证据扩散 |
|---|---|---|
| 条件 | 类别标签 \(c\) | 物理安全终点事件 \(S\) |
| 分类器输入 | noisy image / sample | noisy grasp state \(z_t\)、时间 \(t\)、物体 \(y\) |
| 标签来源 | 数据集类别 | 物理检查、仿真、扰动测试、规则或 evaluator |
| 理论解释 | 条件类别采样 | 终点事件条件化与 Doob transform |
| 关键目标 | 语义一致 | 安全生存概率最大 |

因此这不是简单地“给抓取训练一个 classifier”。更准确的表述是：

> 学习扩散路径上每个中间状态通向安全终点的 survival probability，并用其对数梯度扭转反向过程。

---

## 11. 为什么它适合灵巧手安全抓取

灵巧手抓取的物理判断很适合写成终点事件，而不是全部写成解析能量。

### 11.1 安全是多因素合取事件

抓取是否安全通常不是单个连续指标，而是多个条件同时成立：

$$
S=S_1\cap S_2\cap\cdots\cap S_m.
$$

如果每一项都写成 penalty，需要大量权重。Doob 方式只需要最终事件或软成功概率：

$$
r(z_0,y)=\prod_i r_i(z_0,y)
\quad
\text{或}
\quad
r(z_0,y)=\min_i r_i(z_0,y).
$$

训练后 \(h_\phi\) 自动学习这些条件在不同 denoising 时刻的综合影响。

### 11.2 不可微评估可以进入生成

例如：

- lift 之后是否掉落；
- 加随机小扰动后是否仍保持；
- 接触点是否形成合理分布；
- 仿真中是否出现明显滑移；
- 是否通过一个离散规则检查。

这些都很难变成稳定的解析梯度，但可以变成标签 \(r\)。Doob 方式用标签训练 \(h_\phi\)，再用 \(h_\phi\) 的可微近似梯度引导 diffusion。

### 11.3 高噪声阶段不强行解释物理

在 \(t\) 很大时，\(z_t\) 不是一个真实手姿态。直接计算穿透、接触、稳定性没有严格物理意义。

Doob 方式不会问 \(z_t\) 本身是否物理安全，而是问：

$$
\mathbb P(S|z_t,y)
$$

也就是“从这里继续生成，未来安全的概率”。这避免了高噪声阶段物理梯度误导采样的问题。

---

## 12. 最小 baseline 设计

为了清晰验证算法效果，不需要复杂工程系统。第一版只做静态抓取生成。

### 12.1 生成变量

$$
z_0=(\xi_w,q)\in\mathbb R^{6+n_q},
$$

其中 \(\xi_w\) 是手腕相对物体的局部位姿参数，\(q\) 是关节角。

### 12.2 条件输入

$$
y=\text{object point cloud / SDF / mesh encoding}.
$$

### 12.3 安全事件

最小事件定义：

$$
S
=
S_{\text{penetration}}
\cap
S_{\text{joint}}
\cap
S_{\text{contact}}
\cap
S_{\text{lift}}.
$$

其中：

- \(S_{\text{penetration}}\)：手物最大穿透深度小于阈值；
- \(S_{\text{joint}}\)：关节在可执行范围内；
- \(S_{\text{contact}}\)：关键指尖或指腹接近表面；
- \(S_{\text{lift}}\)：轻量 lift 或扰动 evaluator 判定稳定。

不需要在第一版中引入力闭合 QP，也不需要把所有物理约束都解析展开。

### 12.4 模型

- base model：条件 DDPM 或 DDIM grasp generator；
- safety evidence model：\(h_\phi(z_t,t,y)\)；
- inference：使用

$$
\epsilon_{\text{safe}}
=
\epsilon_\theta
-
\omega_t\sqrt{1-\bar\alpha_t}
\nabla_{z_t}\log h_\phi(z_t,t,y).
$$

---

## 13. 关键对照实验

必须避免只和无约束 diffusion 比。建议对照：

1. **Base Diffusion**：无安全引导。
2. **Post Ranking**：生成多个样本后用 \(r(z_0,y)\) 排序。
3. **Terminal Evaluator Guidance**：只训练 \(p(S|\hat z_0,y)\)，不输入 \(z_t,t\)。
4. **Energy Guidance**：简单穿透和接触 penalty 的梯度引导。
5. **Doob Safety Evidence**：本文方法 \(h_\phi(z_t,t,y)\)。
6. **Doob + Consistency**：加入 \(\mathcal L_{\text{Doob}}\)。

关键假设是：

- Doob 方法比 Post Ranking 更高效，因为它在生成过程中改变路径，而不是事后筛选；
- Doob 方法比 Terminal Evaluator Guidance 更稳定，因为它学习每个噪声阶段的未来安全概率；
- Doob 方法比 Energy Guidance 更容易融合不可微物理事件；
- Consistency 正则能改善 \(h_\phi\) 校准和高噪声阶段引导稳定性。

---

## 14. 评价指标

建议报告：

- safe success rate；
- penetration rate / max penetration depth；
- joint violation rate；
- contact validity；
- lift / perturbation survival rate；
- diversity / coverage；
- rejection efficiency，即达到同等安全率所需采样数；
- \(h_\phi\) calibration：Brier score、ECE、reliability diagram；
- denoising-time analysis：不同 \(t\) 下 \(\|\nabla\log h_\phi\|\)、\(h_\phi\) 分布和最终安全率的相关性。

其中 calibration 很重要。因为本文声称 \(h_t\) 是概率证据，就必须证明它不是普通打分器。

---

## 15. 理论命题草案

### 命题 1：安全条件 score 分解

若 \(h_t(z_t,y)=\mathbb P(S|z_t,y)\)，则：

$$
\nabla_{z_t}\log p_t(z_t|y,S)
=
\nabla_{z_t}\log p_t(z_t|y)
+
\nabla_{z_t}\log h_t(z_t,y).
$$

证明只需要 Bayes 公式。这个命题给出算法合法性。

### 命题 2：Doob 扭转是最小相对熵的条件路径重加权

令 \(P_\theta\) 为原始反向扩散路径测度，终点事件为 \(S\)。条件路径测度：

$$
P_\theta^S(\cdot)
=
P_\theta(\cdot|S)
$$

可写成：

$$
\frac{dP_\theta^S}{dP_\theta}
=
\frac{\mathbf 1_S(Z_0)}{P_\theta(S)}.
$$

它是原始路径测度在事件 \(S\) 上的条件化。若使用软证据 \(r(Z_0,y)\)，则：

$$
\frac{dP_\theta^r}{dP_\theta}
=
\frac{r(Z_0,y)}{\mathbb E_{P_\theta}[r(Z_0,y)]}.
$$

这可以解释为对原始 diffusion 路径的最小信息重加权，而不是任意外部优化。

### 命题 3：时间依赖证据优于终点分类器

终点分类器 \(p(S|\hat z_0,y)\) 只依赖一个 clean estimate。Doob 证据 \(h_t(z_t,y)\) 近似：

$$
\mathbb E[\mathbf 1_S(Z_0)|Z_t=z_t,y],
$$

因此它包含 posterior uncertainty。高噪声时它自动更保守，低噪声时它自动更尖锐。这个性质来自 diffusion 的层级噪声结构，而不是来自人工 schedule。

这个命题可以通过实验验证：比较 \(h_\phi(z_t,t,y)\) 和 \(p(S|\hat z_0,y)\) 在不同 \(t\) 下的 calibration。

---

## 16. 论文卖点表达

摘要中可以写：

> We propose Safety-Evidence Diffusion, a Doob-transformed diffusion sampler for dexterous grasp generation. Instead of injecting physical constraints as handcrafted energy penalties, we model grasp safety as terminal evidence and propagate it across denoising time through a learned survival function \(h_t(z_t,y)=P(S|z_t,y)\). This yields a principled score correction for sampling from the safety-conditioned grasp distribution.

中文主张：

> 本文将灵巧手安全抓取从“物理能量引导”改写为“终点安全证据条件化”。通过学习每个 diffusion 时刻通向安全终点的生存概率 \(h_t\)，我们得到一个 Doob-transformed reverse process，使物理安全以条件 score 的形式进入生成过程。

---

## 17. 边界与风险

这条路线不能声称无条件安全保证。它的边界应该主动写清楚：

- \(h_\phi\) 是近似模型，错误校准会导致错误引导；
- 如果安全标签 \(r\) 本身来自偏置仿真，方法会继承偏置；
- \(\nabla\log h_\phi\) 可能在 \(h_\phi\) 很小处不稳定，需要数值截断；
- 该方法采样的是 learned safety-conditioned distribution，不是形式化验证的安全控制器；
- 最小 baseline 只能证明安全抓取生成质量，不能直接声称真实机器人闭环安全。

推荐数值保护：

$$
\nabla\log h_\phi
=
\nabla\log(\operatorname{clip}(h_\phi,\epsilon,1-\epsilon)).
$$

并限制：

$$
\|\omega_t\nabla\log h_\phi\|\le c_t.
$$

---

## 18. 下一步可展开的两个方向

这份文档只讲第一点。后续可以分别写：

1. **Manifold Score Direction**：把安全抓取看成数据流形与安全流形的交集，研究 score 的切向生成分量和法向安全分量。
2. **Physics-Aware Forward Noising**：不只改 reverse guidance，而是设计 forward corruption，让物理不可行方向在噪声过程中被更快遗忘或显式标记。

这两个方向可以与 Doob 安全证据扩散并列，不需要现在合成一个复杂系统。

---

## 参考入口

- DDPM: [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)
- Score SDE: [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/abs/2011.13456)
- Classifier guidance: [Diffusion Models Beat GANs on Image Synthesis](https://arxiv.org/abs/2105.05233)
- Classifier-free guidance: [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598)
- Diffusion posterior/inverse-problem guidance: [Diffusion Posterior Sampling for General Noisy Inverse Problems](https://arxiv.org/abs/2209.14687)
- Manifold-constrained guidance reference: [CFG++: Manifold-constrained Classifier Free Guidance for Diffusion Models](https://arxiv.org/abs/2406.08070)
- Doob \(h\)-transform background: [Doob h-transform](https://en.wikipedia.org/wiki/Doob_h-transform)

---

## 当前版本结论

Doob 安全证据扩散最值得强调的不是“又加了一个安全分类器”，而是：

$$
\boxed{
\text{安全抓取}=
\text{对原始 diffusion 路径测度施加终点事件条件化}
}
$$

这个视角能把不可微、非局部、多因素的物理安全判断统一成 \(h_t(z_t,y)=P(S|z_t,y)\)，再通过 \(\nabla\log h_t\) 进入反向扩散 score。它比 penalty guidance 更接近 diffusion 的条件采样本质，也更适合构成理论创新型论文的第一条主线。
