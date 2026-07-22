---
title: "安全截断后验去噪：面向灵巧手安全抓取的Diffusion理论"
created: 2026-06-23
updated: 2026-06-23
status: theory-draft-v1-safety-truncated-denoising
target_level: "top-conference theory concept"
tags:
  - dexterous_grasping
  - diffusion
  - safety_constraints
  - truncated_posterior
  - denoising_theory
  - physical_constraints
---

# 安全截断后验去噪：面向灵巧手安全抓取的Diffusion理论

这份文档彻底重构第 04 篇思路。前面的后验安全概率 guidance 已经有价值，但仍然容易被审稿人归到 classifier guidance、DPS 或 denoised loss guidance 一类。为了更有原创性，本文把核心从“给 score 加一项”升级为“重新定义安全 diffusion 中 denoiser 应该估计什么”。

新方案叫 **Safety-Truncated Posterior Denoising, STPD**，中文可以叫“安全截断后验去噪”。

它的核心主张是：

$$
\boxed{
\text{普通 diffusion denoiser 估计 } \mathbb E[z_0|z_t]\text{；安全 diffusion denoiser 应估计 } \mathbb E[z_0|z_t,z_0\in\Omega_y]\text{。}
}
$$

这句话是本文的中心。它不再把安全看成外部 guidance，也不再要求 noisy sample $z_t$ 自己满足物理约束。它说：既然最终要生成的是安全 clean grasp $z_0$，那么去噪器在每一步就不应该预测普通 clean posterior 的均值，而应该预测“被安全域截断之后”的 clean posterior 均值。

这条路线的理论对象不是反射扩散，不是 CBF-QP，不是 penalty guidance，也不是 learned safety classifier。它的理论对象是：

$$
\boxed{
\text{安全条件下的 clean posterior mean。}
}
$$

这比单纯加一个 $\nabla\log h$ 更进一步。$\nabla\log h$ 只是告诉采样往哪里推，而 STPD 直接给出“安全条件下应该去噪到哪里”。

---

## 1. 为什么普通 denoiser 在安全任务中不够

Diffusion 采样的每一步都在做去噪。给定当前 noisy sample $z_t$，模型会预测最终 clean sample $z_0$ 的某种估计，例如 $x_0$ prediction、epsilon prediction 换算出的 clean prediction，或者由 score 通过 Tweedie 公式得到的 posterior mean。

普通 denoiser 的目标可以抽象写成：

$$
\mu_\theta(z_t,t,y)\approx \mathbb E[z_0|z_t,y].
$$

这个估计没有错，但它回答的是普通生成问题：在所有可能 clean grasp 里，哪个是后验平均意义下最可能的结果？

安全抓取的问题不同。我们不想要所有可能 clean grasp 的平均，而只想要安全集合里的 clean grasp。设安全域为：

$$
\Omega_y=\{z_0:g_i(z_0,y)\ge0,\ i=1,\dots,m\}.
$$

那么安全去噪器真正应该估计：

$$
\mu_{\mathrm{safe}}(z_t,t,y)
=
\mathbb E[z_0|z_t,y,z_0\in\Omega_y].
$$

这就是本文和普通 guidance 的分界线。普通 guidance 仍然使用原 denoiser，然后额外加一个力；STPD 说，安全条件改变了 clean posterior 本身，因此 denoiser 的目标均值也应该改变。

---

## 2. 从普通后验到安全截断后验

为了得到清晰可计算的公式，我们从一个局部高斯近似开始：

$$
z_0|z_t,y
\approx
\mathcal N(\mu,\Sigma_t).
$$

这里 $\mu=\mu_\theta(z_t,t,y)$ 是原 denoiser 预测的 clean grasp，$\Sigma_t$ 是当前 clean posterior 的不确定性。第一版可以取：

$$
\Sigma_t=r_t^2I.
$$

更精细时可以用对角协方差或低秩协方差，但这不是第一版的核心。

安全条件 $z_0\in\Omega_y$ 会把这个高斯后验截断掉一部分。于是安全后验变成：

$$
p_{\mathrm{safe}}(z_0|z_t,y)
\propto
\mathcal N(z_0;\mu,\Sigma_t)
\mathbf 1_{\Omega_y}(z_0).
$$

它的均值就是安全去噪目标：

$$
\mu_{\mathrm{safe}}
=
\mathbb E_{p_{\mathrm{safe}}}[z_0].
$$

这一步非常重要。安全不再是一个附加能量，而是直接改变了后验分布的支持。普通 denoiser 是未截断高斯的均值，安全 denoiser 是截断高斯的均值。

---

## 3. 单个安全约束下的闭式修正

先看一个安全不等式：

$$
g(z_0,y)\ge0.
$$

在 $\mu$ 附近对它做一阶线性化：

$$
g(z_0,y)
\approx
g(\mu,y)
+
a^\top(z_0-\mu),
$$

其中：

$$
a=\nabla_z g(\mu,y).
$$

于是安全条件近似为一个半空间：

$$
a^\top(z_0-\mu)+g(\mu,y)\ge0.
$$

对高斯分布来说，被一个半空间截断后的均值有闭式解。定义：

$$
v=a^\top\Sigma_t a,\qquad
\alpha=\frac{g(\mu,y)}{\sqrt{v+\eta}}.
$$

其中 $\eta$ 是很小的稳定项。则安全截断后验均值为：

$$
\boxed{
\mu_{\mathrm{safe}}
=
\mu
+
\Sigma_t a
\frac{1}{\sqrt{v+\eta}}
\frac{\varphi(\alpha)}{\Phi(\alpha)}.
}
$$

这里 $\varphi$ 是标准正态密度，$\Phi$ 是标准正态 CDF。这个公式就是 STPD 的核心公式。

它的直觉非常清楚。若 $\mu$ 离安全边界很远，$g(\mu,y)$ 很大，$\alpha$ 很大，$\frac{\varphi(\alpha)}{\Phi(\alpha)}$ 接近 $0$，于是 $\mu_{\mathrm{safe}}\approx\mu$，说明原 denoiser 已经安全，不需要改。若 $\mu$ 靠近边界或已经越界，$\alpha$ 变小甚至为负，$\frac{\varphi(\alpha)}{\Phi(\alpha)}$ 变大，均值会沿着 $\Sigma_t a$ 的方向被推回安全域内部。

这不是手工 penalty。它是截断高斯的条件均值。修正强度由三个东西自动决定：安全裕度 $g(\mu,y)$、后验不确定性 $\Sigma_t$、约束敏感方向 $a$。

---

## 4. 为什么它比后验安全概率 guidance 更强

后验安全概率 guidance 会写成：

$$
s_{\mathrm{guide}}
=
s_\theta+\nabla_{z_t}\log h_t(z_t,y).
$$

这个形式是正确的，但它仍然像 guidance：原模型给一个 score，我们再加一项。

STPD 的说法更靠近 denoising diffusion 的内部机制。它不是先有原 denoiser 再外加 guidance，而是直接说：在安全条件下，denoising target 应该从 $\mu$ 变成 $\mu_{\mathrm{safe}}$。

如果采样器使用 $x_0$ prediction，那么可以直接把原来的 $\hat z_0=\mu$ 替换为：

$$
\hat z_0^{\mathrm{safe}}=\mu_{\mathrm{safe}}.
$$

如果采样器使用 score，可以通过 Tweedie 型关系把安全 denoiser 转回 score。以简单 Gaussian corruption 为例：

$$
\mu=z_t+\sigma_t^2s_\theta(z_t,t,y).
$$

因此：

$$
s_{\mathrm{safe}}
=
\frac{\mu_{\mathrm{safe}}-z_t}{\sigma_t^2}.
$$

这说明 STPD 并不是另一个任意 guidance，而是在安全条件后验下重新构造 denoising score。

---

## 5. 多个安全约束如何处理

真实灵巧手抓取有多个安全约束。直接计算多半空间截断高斯的精确均值会变复杂，因此第一版不应该追求完整精确解。更稳妥的是使用逐约束闭式修正。

对每个约束 $g_i(z_0,y)\ge0$，在当前 $\mu$ 附近线性化：

$$
g_i(z_0,y)\approx g_i(\mu,y)+a_i^\top(z_0-\mu),
$$

其中 $a_i=\nabla g_i(\mu,y)$。每个约束都给出一个截断均值修正：

$$
\Delta_i
=
\Sigma_t a_i
\frac{1}{\sqrt{a_i^\top\Sigma_t a_i+\eta}}
\frac{\varphi(\alpha_i)}{\Phi(\alpha_i)},
$$

其中：

$$
\alpha_i=
\frac{g_i(\mu,y)}
{\sqrt{a_i^\top\Sigma_t a_i+\eta}}.
$$

第一版可以采用加权叠加：

$$
\boxed{
\mu_{\mathrm{safe}}
=
\mu
+
\sum_i
\omega_i\Delta_i.
}
$$

权重 $\omega_i$ 不需要复杂设计，可以让危险约束自动占主导：

$$
\omega_i
=
\frac{\rho_i}{\sum_j\rho_j+\eta},
\qquad
\rho_i=\frac{\varphi(\alpha_i)}{\Phi(\alpha_i)}.
$$

这表示越危险的约束，inverse Mills ratio 越大，修正权重越高。这样多约束版本仍然保持简洁，不需要 QP，不需要反射 SDE，也不需要黑盒安全网络。

更严格的版本可以把多约束截断高斯均值作为附录讨论，但主文第一版用逐约束闭式修正就足够清楚。

---

## 6. 为什么 STPD 不是 penalty、反射、CBF-QP 或普通 DPS

STPD 和 penalty guidance 不同。Penalty 写成：

$$
s_{\mathrm{pen}}
=
s_\theta-\lambda\nabla E_{\mathrm{safe}}.
$$

它需要人为设定能量和权重。STPD 不从能量出发，而从安全条件 posterior 出发；修正幅度由截断高斯均值公式自动给出。

STPD 和 reflected diffusion 不同。Reflected diffusion 要求扩散过程在受限域中反射，核心是边界 local time 和 reflected SDE。STPD 不要求 noisy trajectory $z_t$ 始终在安全域中，因为 $z_t$ 本来不是物理抓取。它只修正 clean posterior 的去噪均值。

STPD 和 CBF-QP 不同。CBF-QP 把当前动力学投影到安全控制集合里。STPD 不把 score 当控制输入，也不解 QP；它计算的是安全截断后验均值。

STPD 和普通 DPS 或 denoised loss guidance 也不同。DPS 类方法通常用观测一致性或外部 loss 对 denoised sample 施加梯度。STPD 的核心不是“对 $\hat z_0$ 加 loss”，而是“在局部高斯后验被安全域截断后，后验均值应该如何移动”。这给出了闭式均值修正，而不是手工 loss 梯度。

可以把区别压缩成一句话：

$$
\boxed{
\text{STPD 不是引导原 denoiser，而是推导安全条件下的新 denoiser。}
}
$$

---

## 7. 理论命题

**命题 1：安全 denoiser 是截断后验均值。** 若目标是从安全 clean grasp 分布采样，则在任意噪声状态 $z_t$ 下，最小均方误差意义下的安全 clean prediction 是：

$$
\mu_{\mathrm{safe}}
=
\mathbb E[z_0|z_t,y,z_0\in\Omega_y].
$$

证明很直接：在给定条件下，均方误差最优估计就是条件期望。普通 denoiser 对应条件 $z_t,y$；安全 denoiser 对应额外条件 $z_0\in\Omega_y$。

**命题 2：单线性约束下有闭式安全修正。** 若 $z_0|z_t,y\sim\mathcal N(\mu,\Sigma_t)$，且安全约束局部为 $g(\mu)+a^\top(z_0-\mu)\ge0$，则安全截断后验均值为：

$$
\mu_{\mathrm{safe}}
=
\mu
+
\Sigma_t a
\frac{1}{\sqrt{a^\top\Sigma_t a+\eta}}
\frac{\varphi(\alpha)}{\Phi(\alpha)},
\qquad
\alpha=\frac{g(\mu)}{\sqrt{a^\top\Sigma_t a+\eta}}.
$$

这是 STPD 的核心定理。

**命题 3：远离边界时不干预，危险时自动增强。** 当 $\alpha\to+\infty$ 时，$\frac{\varphi(\alpha)}{\Phi(\alpha)}\to0$，所以 $\mu_{\mathrm{safe}}\to\mu$。当 $\alpha$ 变小或为负时，修正项变大，denoiser 自动向安全半空间内部移动。

**命题 4：低噪声极限退化为硬安全修正。** 当 $\Sigma_t\to0$ 且 $\mu$ 已在安全域内部时，修正消失；当 $\mu$ 靠近或越过边界时，修正沿局部内法向集中。这说明 STPD 与 diffusion 噪声尺度自然耦合。

---

## 8. 灵巧手安全抓取中的最小实现

STPD 的第一版只需要三类显式安全约束。

第一，非穿透约束。对手表面采样点 $x_j(z_0)$：

$$
g_{\mathrm{pen},j}(z_0,y)=\mathrm{SDF}_y(x_j(z_0)).
$$

第二，关节限位约束。对第 $k$ 个关节：

$$
g_{\mathrm{joint},k}(z_0,y)
=
\operatorname{softmin}
\left(q_k-q_k^{\min},q_k^{\max}-q_k\right).
$$

第三，自碰撞约束。对不应相交的手指部件，使用它们之间的距离：

$$
g_{\mathrm{self},l}(z_0,y)=d_l(z_0).
$$

这些约束都作用在 denoiser 预测的 $\mu$ 上，而不是 noisy sample $z_t$ 上。实现时每一步采样先得到 $\mu_\theta$，再计算 $g_i(\mu_\theta,y)$ 和 $a_i=\nabla g_i(\mu_\theta,y)$，最后用截断后验公式得到 $\mu_{\mathrm{safe}}$，并替换原来的 clean prediction。

---

## 9. 最小算法流程

STPD 的采样流程可以写得很简单。

第一步，用原 diffusion 网络得到 clean prediction：

$$
\mu=\mu_\theta(z_t,t,y).
$$

第二步，对每个安全约束计算：

$$
g_i(\mu,y),\qquad a_i=\nabla g_i(\mu,y).
$$

第三步，计算危险系数：

$$
\alpha_i=\frac{g_i(\mu,y)}
{\sqrt{a_i^\top\Sigma_t a_i+\eta}},
\qquad
\rho_i=\frac{\varphi(\alpha_i)}{\Phi(\alpha_i)}.
$$

第四步，得到安全去噪修正：

$$
\Delta_i=
\Sigma_t a_i
\frac{\rho_i}
{\sqrt{a_i^\top\Sigma_t a_i+\eta}}.
$$

第五步，构造：

$$
\mu_{\mathrm{safe}}
=
\mu+\sum_i\omega_i\Delta_i.
$$

最后，把 $\mu_{\mathrm{safe}}$ 放回采样器，替代原来的 clean prediction $\mu$。这就是最小可实现版本。

---

## 10. 实验逻辑

实验应该证明一个清晰问题：**安全截断后验去噪是否比对当前点或 denoised point 加 penalty 更合理？**

最小对比包括：

**Base Diffusion**：不加安全。

**Penalty on $z_t$**：直接惩罚当前 noisy sample。

**Penalty on $\hat z_0$**：对 denoiser prediction 加普通安全 loss。

**Denoised guidance**：用 $\nabla_{\hat z_0}E_{\mathrm{safe}}$ 通过 denoiser 回传。

**STPD**：使用安全截断后验均值。

指标包括穿透率、最大穿透深度、关节越界率、自碰撞率、多样性、每一步对原 denoiser 的平均改变量，以及最终抓取成功率。如果 STPD 正确，应该看到：它在安全性上接近或优于 penalty，同时对原 denoiser 的扰动更小，并且高噪声阶段不过度收缩样本。

---

## 11. 为什么这条路线更有 9/10 潜力

STPD 的理论价值在于它改变了问题定义。

已有许多方法问：

$$
\text{如何给 diffusion sample 加安全 guidance？}
$$

STPD 问：

$$
\text{在安全条件下，denoiser 本来应该预测什么？}
$$

这个问题更靠近 diffusion 的数学本质。Denoising diffusion 的核心对象就是 posterior mean 或 score。若目标分布被安全域截断，那么 posterior mean 必然从普通均值变成截断均值。STPD 把这个变化写成了显式公式。

理论链条很短：

$$
\boxed{
\text{安全 clean domain}
\Rightarrow
\text{truncated clean posterior}
\Rightarrow
\text{closed-form truncated Gaussian mean}
\Rightarrow
\text{safe denoiser}
}
$$

它不依赖复杂符号，也不需要大型工程系统。它只需要原 denoiser、显式安全函数、梯度和一个后验协方差尺度。

这条路线仍不能在没有系统文献审查前声称绝对世界首创，但它比“加 guidance”更有独立理论形状。它的潜在顶会卖点是：**首次把灵巧手安全约束解释为 denoising posterior 的截断均值修正，而不是外部引导项。**

---

## 12. 诚实边界

STPD 依赖局部高斯后验近似。如果真实 clean posterior 是多峰的，单个均值和协方差不能完整描述它。第一版可以接受这个近似，因为 diffusion 采样的许多 denoiser 公式本来就使用局部后验均值解释；但论文中必须诚实说明。

STPD 也依赖安全约束的一阶线性化。如果边界曲率很大，线性化会产生误差。可以通过更小步长、更保守的 $\Sigma_t$ 或迭代一次修正来缓解。

多约束叠加版本不是精确多元截断高斯均值。它是一个可实现的一阶近似。若要更严谨，可以在附录讨论多半空间截断高斯的精确积分或数值近似，但第一版不应把主文复杂化。

这些边界不削弱主线。它们只是说明 STPD 是一个“局部安全截断后验去噪”理论，而不是万能安全求解器。

---

## 最终公式

STPD 的核心可以压缩为三行。

普通 denoiser：

$$
\mu=\mathbb E[z_0|z_t,y].
$$

安全 denoiser：

$$
\boxed{
\mu_{\mathrm{safe}}
=
\mathbb E[z_0|z_t,y,z_0\in\Omega_y].
}
$$

单约束局部高斯闭式近似：

$$
\boxed{
\mu_{\mathrm{safe}}
=
\mu
+
\Sigma_t\nabla g(\mu,y)
\frac{1}{\sqrt{\nabla g^\top\Sigma_t\nabla g+\eta}}
\frac{\varphi(\alpha)}{\Phi(\alpha)},
\quad
\alpha=
\frac{g(\mu,y)}
{\sqrt{\nabla g^\top\Sigma_t\nabla g+\eta}}.
}
$$

这就是本文最重要的结论：

$$
\boxed{
\text{安全不是对采样点加力，而是把 denoiser 的目标从普通后验均值换成安全截断后验均值。}
}
$$

---

## 参考入口

- [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)
- [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/abs/2011.13456)
- [Diffusion Posterior Sampling for General Noisy Inverse Problems](https://arxiv.org/abs/2209.14687)
- [Universal Guidance for Diffusion Models](https://arxiv.org/abs/2302.07121)
- [Truncated Normal Distribution](https://en.wikipedia.org/wiki/Truncated_normal_distribution)
- [Approximating the Mean of a Truncated Normal Distribution](https://arxiv.org/abs/1307.0680)
