---
title: "CSSD理论说明：接触分层奇异Score扩散"
source: "02-几何奇异Score扩散：显式物理约束的解析法向生成理论.md"
purpose: "与学长沟通用简洁版"
created: 2026-06-23
---

# CSSD理论说明：接触分层奇异Score扩散

## 1. 一句话主张

这条思路不是把物理约束作为 diffusion 采样时额外添加的 penalty，而是把灵巧手安全抓取分布本身看成由接触物理决定的几何对象。  

核心观点是：

$$
\boxed{
\text{物理约束不是外部修正项，而是决定 diffusion score 几何结构的分布支撑。}
}
$$

换句话说，如果真实可行抓取只存在于接触可行层上，那么高斯加噪后的 score 会天然出现一个指向该接触层的法向回归项。CSSD 的目标就是把这个法向项、层内切向项、以及多接触模式权重显式写出来。

## 2. 为什么普通物理 guidance 不够优雅

常见做法是：

$$
s_{\mathrm{guided}}=s_\theta-\lambda\nabla E_{\mathrm{phys}}.
$$

这种方法能用，但理论上有两个问题：

1. $\lambda$ 缺少自然解释。穿透深度、关节限位、接触距离、摩擦锥违反程度的单位不同，权重通常只能靠调参。
2. 它把物理看成 diffusion 外部的事后修正，而不是数据分布本身的结构。

CSSD 反过来问：如果安全抓取数据本来就支撑在物理可行集合上，那么前向 diffusion 平滑之后，它的 score 应该长什么样？

答案是：低噪声下会出现由物理约束解析决定的法向主导项。

## 3. 接触为什么形成“分层”结构

对一个候选接触点，设 signed gap 为：

$$
\phi_i(z,y).
$$

其中 $\phi_i>0$ 表示分离，$\phi_i=0$ 表示接触，$\phi_i<0$ 表示穿透。刚性接触满足互补关系：

$$
\phi_i(z,y)\ge0,\qquad
\lambda_i\ge0,\qquad
\lambda_i\phi_i(z,y)=0.
$$

这说明接触状态不是一个普通光滑状态，而是由不同分支组成：

- 分离分支：$\phi_i>0,\lambda_i=0$；
- 接触承载分支：$\phi_i=0,\lambda_i>0$。

多指灵巧手中，每个指尖都可以处在不同接触状态，因此整体抓取空间由多个接触模式层组成：

$$
\mathcal S_y=\bigcup_A\mathcal M_A.
$$

这里 $A$ 表示一种接触模式，例如“拇指、食指、中指接触，其余手指分离”；$\mathcal M_A$ 是该模式对应的局部物理可行层。

这就是 CSSD 的核心几何对象：**接触分层的低维奇异分布**。

## 4. 安全抓取分布为什么是“奇异”的

普通 diffusion 默认数据在整个空间中有密度。但接触抓取不是这样。若某个指尖必须接触物体表面，就要求：

$$
\phi_i(z,y)=0.
$$

这是等式约束，会把样本限制在低维集合上。因此单个接触模式下的理想分布可以写成：

$$
p_{0,A}(z|y)=\rho_A(z|y)\delta_{\mathcal M_A}(z).
$$

多个接触模式合起来：

$$
p_0(z|y)=\sum_A\rho_A(z|y)\delta_{\mathcal M_A}(z).
$$

其中 $\rho_A$ 表示在接触层内部哪些抓取更常见、更自然、更稳定；$\delta_{\mathcal M_A}$ 表示概率质量只支撑在该接触层上。

这个表达的意义是：网络不需要重新学习“什么叫接触约束”，物理约束已经决定了分布支撑；网络主要学习的是接触层内部的偏好。

## 5. 核心定理直觉：高斯平滑后出现法向 score

前向 diffusion 可以理解为用高斯核平滑原始数据分布。对某个接触层 $\mathcal M_A$，平滑后的密度近似为：

$$
p_{\sigma,A}(z|y)
\approx
(2\pi\sigma^2)^{-k_A/2}
\exp\left(-\frac{\|z-\Pi_A(z)\|^2}{2\sigma^2}\right)
\rho_A(\Pi_A(z)|y).
$$

对其取 $\log$ 再求梯度，得到主导项：

$$
-\frac{z-\Pi_A(z)}{\sigma^2}.
$$

因此：

$$
\nabla_z\log p_{\sigma,A}(z|y)
=
-\frac{z-\Pi_A(z)}{\sigma^2}
+
P_A\nabla_{\mathcal M_A}\log\rho_A
+
\mathcal C_A
+
O(\sigma).
$$

这三个部分分别对应：

- 法向项：把样本拉回接触可行层；
- 切向项：沿接触层内部生成更像真实数据的抓取；
- 曲率项：接触层弯曲带来的几何修正。

最重要的是，法向项的强度 $1/\sigma^2$ 来自 diffusion 的高斯平滑，而不是人为调出来的 penalty 权重。

## 6. 可计算形式：不用精确投影

理想公式里有 $\Pi_A(z)$，也就是到接触层的最近点投影。但精确投影通常很难算。因此 CSSD 使用显式约束的一阶近似。

若接触模式 $A$ 由等式约束定义：

$$
c_A(z,y)=0,
$$

令：

$$
J_A=\nabla_z c_A.
$$

则局部自然法向近似为：

$$
z-\Pi_A(z)
\approx
J_A^\top(J_AJ_A^\top)^{-1}c_A(z,y).
$$

为了数值稳定，实际使用阻尼版本：

$$
G_A=J_AJ_A^\top+\epsilon I,
$$

$$
s_N^A(z,t,y)
=
-\frac1{\sigma_t^2}
J_A^\top G_A^{-1}c_A(z,y).
$$

这个式子比普通 $-\lambda J_A^\top c_A$ 更合理，因为 $G_A^{-1}$ 提供自然归一化，可以缓解不同约束尺度不一致的问题。

## 7. 多接触模式如何自动混合

真实抓取不会提前知道属于哪个接触模式，所以 CSSD 不硬选一个模式，而是对多个模式做 soft mixture：

$$
\nabla_z\log p_\sigma(z|y)
=
\sum_A
w_A(z,\sigma,y)
\nabla_z\log p_{\sigma,A}(z|y).
$$

精确 $w_A$ 需要高维积分，不可直接算。因此使用 Laplace 近似：

$$
d_A^2=c_A^\top G_A^{-1}c_A,
$$

$$
\tilde w_A
=
\operatorname{softmax}_A
\left(
-\frac{d_A^2}{2\sigma_t^2}
-\frac{k_A}{2}\log(2\pi\sigma_t^2)
-\frac12\log\det G_A
+
\log\pi_A
\right).
$$

这个权重表达了四件事：

- 当前样本离模式 $A$ 越近，权重越大；
- 不同接触数对应不同余维度 $k_A$，不能只看距离；
- 局部几何体积由 $\det G_A$ 修正；
- $\pi_A$ 可以表达接触模式先验，避免盲目偏向五指全接触。

## 8. 不等式边界如何进入

非穿透、关节限位、摩擦锥等很多约束是不等式：

$$
g_i(z,y)\ge0.
$$

CSSD 不把它们简单写成全局 penalty，而是用边界带 score：

$$
s_{\partial}(z,t)
=
\sum_i
\alpha_t
\frac{[\tau_t-g_i(z,y)]_+}{\tau_t}
\nabla_z g_i(z,y).
$$

直觉是：

- 远离边界时不干预；
- 靠近边界时逐渐推回安全域；
- 越界时提供更强推回。

它不是严格的反射扩散 local time，而是可微、可实现的边界层近似。

## 9. 最终可计算公式

CSSD 最适合作为方法核心的公式是：

$$
\boxed{
s_{\mathrm{CSSD}}
=
\sum_A
\tilde w_A
\left[
-\frac{1}{\sigma_t^2}
J_A^\top G_A^{-1}c_A
+
P_As_\theta
+
s_{\partial,A}
\right].
}
$$

其中：

$$
G_A=J_AJ_A^\top+\epsilon I,\qquad
d_A^2=c_A^\top G_A^{-1}c_A.
$$

这一公式的解释是：

- $-J_A^\top G_A^{-1}c_A/\sigma_t^2$：物理约束给出的解析法向；
- $P_As_\theta$：保留 diffusion 网络在接触层内的切向生成能力；
- $s_{\partial,A}$：处理不等式边界；
- $\tilde w_A$：在多个接触模式之间做可解释的软选择。

## 10. 和现有 demo 的连接方式

如果已有 demo 是 diffusion 生成灵巧手抓取构型：

$$
z=(T_w,q),
$$

第一阶段不需要重训模型，可以只改采样器。

建议先实现最小 CSSD 版本：

1. 选少量候选接触模式 $A$，例如二指、三指、四指、五指，或当前 gap 最小的 top-k 指尖组合。
2. 用指尖到物体表面的 signed distance 构造 $c_A$。
3. 用手指运动学 Jacobian 和物体表面法向构造 $J_A$。
4. 用 $G_A=J_AJ_A^\top+\epsilon I$ 得到自然法向。
5. 用 $\tilde w_A$ 做模式权重。
6. 加入简单边界带项，例如关节限位和穿透边界。

实验上至少比较：

- Base Diffusion；
- 普通 Penalty Guidance；
- 只加自然法向的 CSSD-N；
- 加自然法向与切向投影的 CSSD-N+T；
- 加模式权重和边界带的 CSSD-Full。

## 11. 最应该验证的实验现象

这条理论不是只看最终成功率，而是要验证 CSSD 的结构预测。

建议重点画五类结果：

1. 法向残差随 denoising 下降：$\|c_A(z_t)\|$ 或 $d_A^2$ 应逐步变小。
2. 模式权重随 denoising 变尖锐：高噪声阶段多个模式共存，低噪声阶段逐渐收敛到合理接触模式。
3. 切向投影保留多样性：CSSD-N 可能更安全但多样性下降，CSSD-N+T 应在安全和多样性之间更平衡。
4. 自然度规带来尺度鲁棒性：人为缩放某个约束后，普通 penalty 更敏感，CSSD 应更稳定。
5. 边界带只在危险区域激活：远离边界时不干预，靠近穿透或关节限位时才推回。

## 12. 这条理论该怎么对外表述

推荐表述：

> 我们提出 Contact-Stratified Singular Score Diffusion，把灵巧手抓取看成由多个接触模式层组成的奇异分布。通过分析该分布在 Gaussian diffusion 平滑下的 score 结构，我们推导出由显式物理约束决定的法向项、由数据分布学习的切向项，以及由 Laplace 近似得到的接触模式权重。

不推荐表述：

> 我们保证 diffusion 生成结果安全。

更稳妥的 claim 是：

> 在明确的接触几何假设下，CSSD 证明并实现了显式物理约束如何进入 diffusion score；它提供的是渐近一致的物理几何引导，而不是形式化安全控制器。

## 13. 当前优势与风险

优势：

- 理论主线比普通 penalty guidance 更优雅；
- 物理约束不是外挂，而是决定 score 的几何结构；
- 接触分层适合灵巧手，不是简单套用单一流形 diffusion；
- 自然法向、模式权重、边界带都能落到现有 demo 的采样器里。

风险：

- 不能声称严格安全保证；
- 需要把四个命题写得更正式；
- 实验必须证明 CSSD 优于 penalty guidance，而不只是优于 base diffusion；
- 接触模式枚举、Jacobian、SDF 和边界项的工程实现会影响效果；
- 在接触切换、grazing、摩擦锥退化等区域，理论只能给近似解释。

## 14. 给学长沟通时的核心话术

可以这样讲：

> 我现在考虑的 02 思路不是单纯给 diffusion 加物理 penalty，而是从分布几何出发：灵巧手可行抓取天然落在多个接触模式层上，所以它是一个接触分层的奇异分布。这个分布经过 diffusion 的高斯平滑后，score 会自然分解成物理法向、数据切向和模式权重。这样物理约束不是后处理，而是决定了 score 的结构。我的 demo 目前已经有 base diffusion，下一步可以只改采样器，实现阻尼自然法向、模式权重和边界带，然后和 penalty guidance 比较安全性、接触模式合理性和多样性。

最短版：

$$
\boxed{
\text{接触模式分层}
\Rightarrow
\text{奇异物理分布}
\Rightarrow
\text{高斯平滑}
\Rightarrow
\text{score 分解}
\Rightarrow
\text{解析法向 + 数据切向 + 模式权重}
}
$$

