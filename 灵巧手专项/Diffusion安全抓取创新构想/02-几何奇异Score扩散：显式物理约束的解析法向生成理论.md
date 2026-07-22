---
title: "接触分层奇异Score扩散：显式物理约束的本科生友好理论讲解"
created: 2026-06-23
updated: 2026-06-23
status: theory-draft-v6-theorem-backed
target_level: "top-conference theory concept"
tags:
  - dexterous_grasping
  - diffusion
  - contact_modes
  - singular_score
  - manifold_score
  - physical_constraints
---

# 接触分层奇异Score扩散：显式物理约束的本科生友好理论讲解

这份文档解释一条面向顶会理论工作的思路：**不要把灵巧手安全抓取中的物理约束看成 diffusion 外部额外加上的 penalty，也不要训练一个黑盒安全网络来替代物理公式；更好的视角是，把安全抓取分布本身看成由接触物理决定的几何对象，然后从 diffusion 的数学原理推出它应该具有怎样的 score。**

先给出最直接的判断：如果只看最初的优雅理论公式，这条路线大约是 **8.5/10**。它已经强于普通物理 guidance、黑盒 evaluator guidance 和单一流形 diffusion 的简单套用；但它还缺少几个审稿人会追问的闭环：投影 $\Pi_A(z)$ 怎么算、模式权重 $w_A$ 怎么算、不等式边界怎么落到采样里、以及它和普通 penalty guidance 到底差在哪里。本文后面会把这些点补上，把 CSSD 从“好看的理论”推进到“渐近可计算的理论”。这样它会更接近 **9/10 的投稿级主线**，但仍需要实验验证来支撑。

本文把这条路线命名为 **Contact-Stratified Singular Score Diffusion, CSSD**，中文可以叫“接触分层奇异 Score 扩散”。理想形式的核心公式是：

$$
s_{\mathrm{CSSD}}(z,t,y)
=
\sum_A
w_A(z,\sigma_t,y)
\left[
-\frac{z-\Pi_A(z)}{\sigma_t^2}
+
P_A s_\theta(z,t,y)
+
\mathcal C_A(z,y)
\right].
$$

这个公式一开始看起来抽象，但它其实只在说一件很自然的事：一个灵巧手抓取样本在去噪时，应该同时考虑多个可能的接触模式；每个接触模式都会给出一个“回到该模式物理可行层”的方向，也会给出一个“沿着该模式内部更像真实抓取”的方向；最后这些方向按照当前更可能属于哪个接触模式来加权平均。

为了让后面的推导容易理解，先把公式中的符号翻译成人话。$z$ 是抓取变量，可以包括手腕位姿和关节角；$y$ 是物体条件，可以是点云、SDF 或 mesh；$A$ 是一种接触模式，例如“拇指和食指接触，其他手指分离”；$\Pi_A(z)$ 表示把当前样本 $z$ 拉到模式 $A$ 的物理可行层上最近的位置；$P_A$ 表示沿着该接触层内部移动的切向投影；$s_\theta$ 是普通 diffusion 网络学到的 score；$w_A$ 是当前样本属于接触模式 $A$ 的概率权重；$\mathcal C_A$ 是曲率修正，可以先理解为“接触层弯曲带来的细微修正”。

这里有一个贯穿全文的直觉：如果真实数据只落在某个低维集合上，那么加噪之后，低维集合周围会形成一层“概率雾”。score 就像这层概率雾中的风向，告诉一个带噪点应该往哪里走才能回到高概率区域。CSSD 的理论贡献，就是把这层“概率雾”的风向拆开：垂直接触层的风由物理约束解析决定，沿接触层的风由数据分布学习得到，多个接触层之间的风由模式权重自动混合。

---

## 1. Score 在 diffusion 里到底是什么

Diffusion 模型的核心不是直接一步生成干净样本，而是从噪声中一步步去噪。假设某个时刻的带噪变量是 $z_t$，模型需要知道：为了让这个带噪变量变得更像真实数据，应该往哪个方向移动。这个方向就是 score。

如果某个分布的密度是 $p(z)$，它的 score 定义为：

$$
s(z)=\nabla_z\log p(z).
$$

可以把 $\log p(z)$ 理解为“当前位置像不像真实数据”的地形高度。score 就是让高度上升最快的方向。若 $z$ 处在低概率区域，score 会指向更高概率的区域；若 $z$ 已经处在高概率区域，score 会让它沿着数据分布的结构微调。

在普通 diffusion 中，网络 $s_\theta(z_t,t,y)$ 试图学习：

$$
s_\theta(z_t,t,y)\approx\nabla_{z_t}\log p_t(z_t|y).
$$

这里 $p_t(z_t|y)$ 是在第 $t$ 个噪声水平下的数据分布。噪声越大，分布越模糊；噪声越小，分布越接近真实抓取数据。反向采样就是不断沿着 score 指向的方向，从噪声走回真实数据分布。

本文关心的问题是：如果真实安全抓取数据不是分布在整个空间里，而是集中在满足物理约束的区域上，那么这个 score 会有什么特殊结构？这个问题直接决定“物理约束应该如何融入 diffusion”。如果 score 的物理部分可以从分布几何中推导出来，我们就不应该把它当成可随意调权重的经验项。CSSD 选择的就是这条路线：从数据支撑集的几何结构推导 score。

---

## 2. 为什么普通物理 guidance 不是最根本的答案

常见的做法是给 diffusion 加一个物理能量：

$$
s_{\mathrm{guided}}=s_\theta-\lambda\nabla E_{\mathrm{phys}}.
$$

这里 $E_{\mathrm{phys}}$ 可以包含穿透惩罚、接触距离惩罚、关节限位惩罚等。这个写法很直观：如果样本违反物理，就沿着能量下降方向把它拉回来。

但这个方法有两个理论问题。第一，$\lambda$ 很难有唯一解释。穿透深度的单位是长度，关节限位的单位是角度，摩擦锥违反程度又是力的比例；这些量混合在一个能量里，权重通常只能靠实验调。第二，这种写法把物理当成外部修正，而不是数据分布本身的结构。可是如果安全抓取数据本来就只存在于物理可行区域上，那么物理约束应该直接改变 score 的几何形状，而不是事后额外加上去。

CSSD 的思路是先不写 $E_{\mathrm{phys}}$。我们先问一个更根本的问题：如果真实安全抓取分布集中在物理可行集合上，前向 diffusion 加噪之后，这个分布的 score 会自然长成什么样？答案是：它会出现一个强烈的法向回归项，把样本拉回物理可行集合。

CSSD 并不是把 $E_{\mathrm{phys}}$ 换一个名字，也不是把 penalty 系数写成随时间变化的 schedule。它的主张更强：如果安全数据分布真的支撑在接触可行集合上，那么在低噪声极限下，score 的法向主导项必须接近 $-(z-\Pi(z))/\sigma^2$。这里的 $1/\sigma^2$ 不是人为选择，而是高斯平滑本身带来的尺度。这使得 CSSD 有概率分布层面的解释，而不只是优化层面的解释。

---

## 3. 灵巧手抓取为什么是“接触分层”的

为了理解 CSSD，先看一个最简单的接触点。设第 $i$ 个候选接触点到物体表面的 signed gap 是 $\phi_i(z,y)$。约定如下：$\phi_i(z,y)>0$ 表示手指点在物体外面，和物体分离；$\phi_i(z,y)=0$ 表示手指点刚好在物体表面上，发生接触；$\phi_i(z,y)<0$ 表示手指点进入物体内部，发生穿透。

非穿透要求：

$$
\phi_i(z,y)\ge0.
$$

如果再考虑接触力，令 $\lambda_i$ 表示第 $i$ 个接触点的法向接触力强度。刚性接触里有一个基本关系：

$$
\phi_i(z,y)\ge0,\qquad
\lambda_i\ge0,\qquad
\lambda_i\phi_i(z,y)=0.
$$

这三条式子叫接触互补关系。它的意思其实很简单。若手指和物体分离，即 $\phi_i>0$，那么它不能产生接触力，所以 $\lambda_i=0$。若接触力为正，即 $\lambda_i>0$，那么手指必须真的贴在物体表面上，所以 $\phi_i=0$。同时 $\phi_i$ 不能小于零，因为那就是穿透。

这个关系已经告诉我们：接触不是一个单一连续状态，而是至少有两个分支。一个分支是“分离”：$\phi_i>0,\lambda_i=0$。另一个分支是“接触承载”：$\phi_i=0,\lambda_i>0$。这两个分支在 $\phi_i=0,\lambda_i=0$ 附近连接。

当手有多个候选接触点时，每个点都可以处在分离或接触状态。于是一个抓取会对应某个接触模式 $A$。例如 $A$ 可以表示“拇指、食指和中指接触，其他手指分离”。固定一个 $A$ 后，满足该接触模式的所有抓取形成一个局部可行层，记为 $\mathcal M_A$。所有可能模式的并集构成安全抓取空间：

$$
\mathcal S_y=\bigcup_A\mathcal M_A.
$$

这就是“接触分层”。为了更直观，可以想象一个二维平面。横轴表示 gap $\phi$，纵轴表示法向力 $\lambda$。互补关系允许两条分支：一条是横轴正半轴，表示 $\phi>0,\lambda=0$，也就是分离；另一条是纵轴正半轴，表示 $\phi=0,\lambda>0$，也就是接触承载。这两个分支拼成一个“L”形集合。灵巧手的多接触情况就是许多这种“L”形结构的组合。它不需要复杂符号才能表达，但它确实比普通光滑流形更贴近真实抓取物理。

---

## 4. 为什么安全抓取分布是“奇异”的

普通机器学习里，我们经常假设数据分布在整个空间里都有密度。但安全抓取不是这样。假设一个接触模式要求某个指尖必须贴在物体表面，那么它必须满足 $\phi_i(z,y)=0$。这是一条等式约束，会把可行样本限制在一个低维集合上。

举一个二维类比。假设数据只分布在平面中的一条曲线上，而不是整个平面上。这个分布相对于整个二维平面来说就是“奇异”的，因为它没有普通二维密度；它只在曲线上有密度。

对单个接触模式 $A$，可以把理想安全抓取分布写成：

$$
p_{0,A}(z|y)=\rho_A(z|y)\delta_{\mathcal M_A}(z).
$$

这里 $\rho_A$ 表示在接触层 $\mathcal M_A$ 内部，不同抓取的偏好密度；$\delta_{\mathcal M_A}$ 表示分布只支撑在 $\mathcal M_A$ 上。

因为真实抓取可能有多个接触模式，所以整体分布写成：

$$
p_0(z|y)=\sum_A\rho_A(z|y)\delta_{\mathcal M_A}(z).
$$

这里的 $\rho_A$ 可以理解为“在接触模式 $A$ 已经固定的前提下，哪些抓取更好”。例如同样是三指接触，有些关节姿态更自然，有些接触点分布更稳定，有些手腕姿态更常见。这些偏好属于层内数据分布。相反，“是否满足该接触模式”由 $\delta_{\mathcal M_A}$ 表达，它不是网络要重新学习的偏好，而是物理结构。

---

## 5. diffusion 平滑之后为什么会出现法向项

前向 diffusion 加噪可以理解为用高斯核平滑数据分布。为了让这一步从“形式推导”变成可以写进论文的定理，需要先说清楚讨论对象。固定物体条件 $y$ 后，把灵巧手的有效搜索空间限制在一个有限区域 $\mathcal X_y\subset\mathbb R^d$ 内，例如有限腕部工作空间和有限关节范围。对每个接触模式 $A$，假设它对应的可行层 $\mathcal M_A\subset\mathcal X_y$ 是一个 $C^2$ 的嵌入子流形，允许有光滑边界；在接触切换、grazing 或多个边界相交的点附近，我们先不声称单一流形定理成立，而是把它们交给后面的模式混合和边界项处理。

这里最关键的几何条件叫“管状邻域”。直观地说，若 $\mathcal M_A$ 足够光滑，并且我们只看它附近一圈足够薄的区域，那么这个区域里的每个点 $z$ 都有唯一的最近点投影 $\Pi_A(z)$。也就是存在一个半径 $r_A>0$，使得当 $\operatorname{dist}(z,\mathcal M_A)<r_A$ 时：

$$
\Pi_A(z)=\arg\min_{u\in\mathcal M_A}\|z-u\|
$$

存在且唯一。这个事实可以看成管状邻域定理或正 reach 条件的直接结果。对本科生来说，可以把它理解成：一条没有自交、没有尖点的光滑曲线，在足够近的地方，每个点都能沿法线找到唯一的最近点；高维流形也是同样的道理。这个条件非常重要，因为 $z-\Pi_A(z)$ 只有在投影唯一时才是明确的向量。

在这些条件下，对多个接触模式，平滑后的密度可以写成：

$$
p_\sigma(z|y)
=
\sum_A
\int_{\mathcal M_A}
\rho_A(u|y)
\varphi_\sigma(z-u)
d\operatorname{vol}_A(u).
$$

先只看一个模式 $A$。令 $k_A=d-\dim\mathcal M_A$ 表示模式 $A$ 的余维度，也就是该模式等式约束的数量。若 $z$ 位于 $\mathcal M_A$ 的管状邻域内，记 $u_A=\Pi_A(z)$，$n_A=z-u_A$，那么 $n_A$ 就是从接触层到当前点的法向偏离量。高斯核中最重要的距离项是：

$$
\exp\left(-\frac{\|z-\Pi_A(z)\|^2}{2\sigma^2}\right).
$$

更严格地说，在低噪声并且 $\|n_A\|=O(\sigma)$ 的区域内，流形上的 Laplace 型展开给出：

$$
p_{\sigma,A}(z|y)
=
(2\pi\sigma^2)^{-k_A/2}
\exp\left(-\frac{\|n_A\|^2}{2\sigma^2}\right)
\rho_A(u_A|y)
\left[1+O(\sigma)\right].
$$

这个式子里每一项都有清楚含义。指数项表示离接触层越远，概率下降越快；$(2\pi\sigma^2)^{-k_A/2}$ 表示余维度越高，低噪声下密度的尺度越尖；$\rho_A(u_A|y)$ 表示投影点附近真实抓取在该接触层内部的偏好；$O(\sigma)$ 是 Laplace 近似的余项，在 $\mathcal M_A$ 的曲率、$\rho_A$ 的导数和管状邻域半径有界时可以被统一控制。

现在对这个展开取 $\log$ 再求梯度，就会得到主导方向：

$$
-\frac{z-\Pi_A(z)}{\sigma^2}.
$$

这个方向就是从 $z$ 指向接触层的方向。它的强度与距离成正比，也与 $1/\sigma^2$ 成正比。噪声 $\sigma$ 越小，说明已经接近最终生成阶段，样本越应该严格回到物理可行层，因此法向回归越强。

因此可以把核心结论写成一个论文里的命题。

**命题 1：单接触层的平滑 score 展开。** 若 $\mathcal M_A$ 是 $C^2$ 光滑接触层，$\rho_A$ 在 $\mathcal M_A$ 上正且足够光滑，并且 $z$ 位于 $\mathcal M_A$ 的管状邻域内，则当 $\sigma\to0$ 时：

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

证明思路并不神秘。第一步，用管状邻域把 $z$ 附近的点分解成“投影点 $u_A$ 加法向偏移 $n_A$”。第二步，在 $u_A$ 附近给 $\mathcal M_A$ 建局部坐标，把高斯积分写成对切向坐标的积分。第三步，用 Laplace 方法保留指数中最小距离点的贡献，得到上面的密度展开。第四步，对 $\log p_{\sigma,A}$ 求梯度，指数项贡献 $-n_A/\sigma^2$，层内密度 $\rho_A$ 贡献切向 score，曲率和体积变化贡献 $\mathcal C_A$，余项保持为 $O(\sigma)$。

第一部分 $-\frac{z-\Pi_A(z)}{\sigma^2}$ 是法向项，负责让样本回到物理可行层。它不是手工 penalty，而是高斯平滑低维分布之后自然出现的 score 主导项。当 $z$ 离流形的距离是 $O(\sigma)$ 时，法向项量级是 $O(1/\sigma)$，而切向项和曲率项通常是 $O(1)$，所以低噪声下法向项必然主导。第二部分 $P_A\nabla_{\mathcal M_A}\log\rho_A$ 是切向项。它不改变样本是否满足该接触模式，而是在接触层内部移动，让样本更像真实抓取数据。第三部分 $\mathcal C_A$ 是曲率项，第一遍理解时可以先看成较小的几何修正。

多接触模式的情况不是简单地找一个全局投影。因为不同 $\mathcal M_A$ 可能相交或靠得很近，在接触模式切换处，最近层可能不唯一。正确做法是：在远离交界的区域，使用单层展开；在多个模式都能解释当前样本的区域，把各模式的 score 按它们的平滑密度贡献加权混合。于是：

$$
\nabla_z\log p_\sigma(z|y)
=
\sum_A
w_A(z,\sigma,y)
\nabla_z\log p_{\sigma,A}(z|y).
$$

这一步是 CSSD 的第一个理论支点：只要数据集中在低维接触层上，高斯平滑后的 score 就一定包含“回到接触层”的法向项。这不是灵巧手领域的经验规则，而是 score matching 和扩散平滑的数学结果。灵巧手的价值在于，它给这个数学结构提供了一个很自然、很重要的物理对象：接触可行层。

---

## 6. 显式物理约束如何给出解析法向

上面出现了 $\Pi_A(z)$，也就是“到接触层的最近点投影”。这个对象直观，但直接精确计算通常很难。因为接触层由非线性几何和互补条件定义，精确求：

$$
\Pi_A(z)=\arg\min_{u\in\mathcal M_A}\|z-u\|^2
$$

本身就是一个约束优化问题。尤其在接触模式切换附近，接触层可能不光滑，直接依赖精确投影会让理论很漂亮但方法不可落地。

因此，CSSD 应该使用一个更稳健的说法：**不要求精确投影，而使用投影 score 的局部一阶近似。** 如果接触层由显式等式约束定义：

$$
c_A(z,y)=0,
$$

令 $J_A=\nabla_zc_A$。这里 $c_A(z,y)\in\mathbb R^{k_A}$ 是模式 $A$ 的约束误差，$J_A$ 是这些误差对抓取变量 $z$ 的 Jacobian。比如指尖 signed distance 写成 $\phi_i(f_i(z),y)$ 时，$J_A$ 就是“物体表面法向”乘以“手指运动学 Jacobian”。

在 regular 接触层附近，如果 $J_A$ 满行秩，那么可以把 $c_A$ 在当前点线性化：

$$
c_A(z+\Delta z,y)
\approx
c_A(z,y)+J_A\Delta z.
$$

我们希望找到最小的修正 $\Delta z$，使得线性化约束满足 $c_A(z,y)+J_A\Delta z=0$。这个最小范数解是：

$$
\Delta z
=
-J_A^\top(J_AJ_A^\top)^{-1}c_A(z,y).
$$

所以从当前点到投影点的偏离量满足：

$$
z-\Pi_A(z)
\approx
J_A^\top(J_AJ_A^\top)^{-1}c_A(z,y).
$$

这个近似不是拍脑袋，它就是 Gauss-Newton 投影的一步线性化。更严谨地说，可以写成下面的命题。

**命题 2：自然法向近似的局部误差界。** 假设 $c_A$ 是 $C^2$，在 $\mathcal M_A$ 附近 $J_A$ 满行秩，并且 $J_AJ_A^\top$ 的最小特征值大于 $\gamma^2>0$，二阶导数有界。令：

$$
\delta_A(z)
=
J_A^\top(J_AJ_A^\top)^{-1}c_A(z,y).
$$

当 $z$ 位于 $\mathcal M_A$ 的足够小管状邻域内时，有：

$$
\left\|
(z-\Pi_A(z))-\delta_A(z)
\right\|
\le
C\|c_A(z,y)\|^2.
$$

这句话的意思是：约束误差越小，一阶解析法向越接近真实最近点投影；而且误差是二阶小量。需要注意的是，这里说的是向量误差。若进一步看两个方向之间的夹角，因为真实法向位移本身大小通常是 $O(\|c_A\|)$，所以夹角误差一般只能保证是 $O(\|c_A\|)$，不应过强地写成 $O(\|c_A\|^2)$。

但为了处理数值病态和接触切换附近的秩退化，更可计算的版本应写成阻尼形式：
$$
G_A=J_AJ_A^\top+\epsilon I,
$$

$$
s_N^A(z,t,y)
=
-\frac1{\sigma_t^2}
J_A^\top G_A^{-1}c_A(z,y).
$$

这里 $\epsilon>0$ 是一个小的阻尼系数。它的作用不是破坏理论，而是让公式在 $J_AJ_A^\top$ 接近奇异时仍然稳定。若 regular 区域里 $J_AJ_A^\top\succeq\gamma^2 I$，阻尼带来的偏差可以粗略控制为：

$$
\left\|
J_A^\top(J_AJ_A^\top+\epsilon I)^{-1}c_A
-
J_A^\top(J_AJ_A^\top)^{-1}c_A
\right\|
\le
C\frac{\epsilon}{\gamma^2}\|c_A\|.
$$

因此在光滑且条件数良好的区域，选择 $\epsilon\ll\gamma^2$ 时，阻尼版本几乎不改变真实自然法向；而在接触切换或 $J_A$ 退化的区域，$\epsilon$ 防止矩阵逆爆炸。事实上，对任意奇异值 $s$，系数 $s/(s^2+\epsilon)$ 都不超过 $1/(2\sqrt\epsilon)$，所以阻尼法向的大小是有界的。它不能神奇恢复已经丢失的秩，也不能保证在模式交界处给出唯一真实投影；它保证的是数值稳定，并且在仍然可辨认的有效约束方向上给出平滑修正。

实际选择 $\epsilon$ 时，可以遵循一个简单准则：在 regular 区域让 $\epsilon$ 小于可靠特征值尺度，在奇异区域让最大修正步长不至于破坏采样稳定性。理论写法可以取 $\epsilon=\eta\gamma^2$ 且 $\eta\ll1$；工程写法可以用 $J_AJ_A^\top$ 的平均对角尺度乘一个小系数，再加一个很小的下界。

这个公式比普通的 $-\lambda J_A^\top c_A$ 更干净。$c_A(z,y)$ 是当前违反约束的程度；$J_A^\top$ 把约束误差转回抓取变量空间；$G_A^{-1}$ 起到自然归一化作用，避免不同约束因为单位或尺度不同而产生不合理影响；$1/\sigma_t^2$ 则来自 diffusion 噪声尺度，而不是手调权重。

这一步也回应了一个关键缺陷：CSSD 不应该假装精确 $\Pi_A(z)$ 总是可算。更可靠的版本是“理想理论用 $\Pi_A$ 表达，实际可计算形式用阻尼自然法向表达”。这样既保留了理论来源，也避免了不可操作。

---

## 7. 多个接触模式如何合在一起

真实抓取不会提前告诉我们接触模式 $A$ 是哪个。不同模式都可能解释当前 noisy 样本。于是总密度是各模式平滑密度的和：

$$
p_\sigma(z|y)=\sum_Ap_{\sigma,A}(z|y).
$$

对这个式子求 score，可以得到：

$$
\nabla_z\log p_\sigma(z|y)
=
\sum_A
w_A(z,\sigma,y)
\nabla_z\log p_{\sigma,A}(z|y),
$$

其中：

$$
w_A(z,\sigma,y)
=
\frac{p_{\sigma,A}(z|y)}
{\sum_Bp_{\sigma,B}(z|y)}.
$$

这个 $w_A$ 是“当前样本属于模式 $A$ 的软概率”。但是这里也有一个必须正视的问题：精确的 $p_{\sigma,A}$ 需要对接触层做积分，在高维灵巧手空间里不可直接计算。如果最后又用黑盒网络学习 $w_A$，就会削弱“显式物理”的主张。

更好的做法是使用 Laplace 近似，把 $w_A$ 近似成一个可计算的 softmax 权重。定义：

$$
d_A^2(z,y)=c_A(z,y)^\top G_A^{-1}c_A(z,y),
$$

其中 $G_A=J_AJ_A^\top+\epsilon I$。$d_A^2$ 可以理解为当前样本到模式 $A$ 的几何残差。残差越小，说明越接近该接触模式。但只看 $d_A^2$ 还不够，因为不同接触模式的维度不同。二指接触、三指接触、五指接触对应的约束数量不同，也就是余维度 $k_A$ 不同。高斯平滑一个点、一条线、一个面，得到的局部密度尺度并不一样，因此 Laplace 权重必须带上余维度因子。

更完整的近似应写成：

$$
\tilde w_A(z,\sigma_t,y)
=
\frac{\tilde q_A(z,\sigma_t,y)}
{\sum_B\tilde q_B(z,\sigma_t,y)},
$$

其中：

$$
\tilde q_A
=
\pi_A
\rho_A(\Pi_A(z)|y)
(2\pi\sigma_t^2)^{-k_A/2}
\det(G_A)^{-1/2}
\exp\left(
-\frac{d_A^2(z,y)}{2\sigma_t^2}
\right).
$$

如果实际不想显式建模 $\rho_A(\Pi_A(z)|y)$，可以先把它并入 $\pi_A$，得到简化的 softmax 形式：

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

这里 $\pi_A$ 是接触模式先验。它非常有用，因为它可以表达“不是五指全接触就一定最好”。例如可以让 $\pi_A$ 偏好接触数量适中、分布合理、关节不过度弯曲的模式。$-\frac{d_A^2}{2\sigma_t^2}$ 表示越接近该模式，权重越大；$-\frac{k_A}{2}\log(2\pi\sigma_t^2)$ 表示不同余维度的低噪声密度尺度；$-\frac12\log\det G_A$ 是局部几何体积修正；$\log\pi_A$ 是我们对接触模式的先验偏好。

**命题 3：Laplace 模式权重近似。** 若每个候选模式 $A$ 在 $z$ 附近有唯一投影，$\rho_A$ 平滑且非零，局部二阶几何量有界，并且模式间积分主要由 $\Pi_A(z)$ 附近贡献，则：

$$
w_A(z,\sigma,y)
=
\tilde w_A(z,\sigma,y)
\left[1+O(\sigma)\right]
$$

在各模式贡献没有指数级接近为零的区域成立。更直观地说，当噪声较小、当前点离几个候选接触层都不太远时，真实积分权重可以用“到每个层的距离 + 该层的局部体积 + 模式先验”来近似。

一个简单 toy case 能说明余维度因子为什么不能省略。在二维平面里，如果模式 $A$ 是一条线，模式 $B$ 是一个点，那么二者到当前点的最近距离可能相同，但加高斯噪声后的密度尺度不同。线流形沿着切向可以积累一整段概率质量，点流形只能从一个局部点贡献概率质量。因此权重不仅由距离决定，也由流形维度决定。灵巧手里，二指、三指、五指接触正是这种“不同维度模式竞争”的高维版本。

这样，CSSD 的模式权重不再是一个循环定义。理想理论中 $w_A$ 来自平滑密度贡献；可计算版本中 $\tilde w_A$ 来自 Laplace 近似。这个近似仍然保留了分布推导的含义，但不需要真的计算高维流形积分。

---

## 8. 不等式边界如何理解

有些物理约束不是等式，而是不等式。例如非穿透要求：

$$
\phi_i(z,y)\ge0.
$$

摩擦锥要求：

$$
\|\tau_i\|\le\mu_i\lambda_i.
$$

这些约束定义了安全域的边界。普通 penalty 方法会等样本越界后，再用惩罚项把它拉回来。CSSD 的理论解释更接近反射扩散，但这里必须说得严谨：真正的反射扩散不是普通 drift 完全能表示的，它通常包含边界 local time；在 Fokker-Planck 方程里，它体现为边界处的零通量或 Neumann 型条件。CSSD 采样器里使用的 $s_{\partial}$ 不是严格 local time，而是反射边界的一个可微边界层近似。

为了让这个思想可操作，可以把一般不等式写成：

$$
g_i(z,y)\ge0.
$$

其中 $g_i$ 可以是非穿透 gap、关节限位余量或摩擦锥余量。定义一个边界带宽 $\tau_t>0$，当 $g_i$ 远大于 $\tau_t$ 时，样本离边界很远，不需要修正；当 $g_i$ 接近零或小于零时，需要沿 $\nabla_z g_i$ 的方向推回安全域。一个简单的边界带 score 可以写成：

$$
s_{\partial}(z,t)
=
\sum_i
\alpha_t
\frac{[\tau_t-g_i(z,y)]_+}{\tau_t}
\nabla_z g_i(z,y).
$$

这里 $[\cdot]_+$ 表示只取正部。若 $g_i(z,y)\ge\tau_t$，该约束不作用；若 $g_i$ 接近边界，推回项逐渐变强；若 $g_i<0$，说明已经越界，推回项更强。$\alpha_t$ 可以随噪声调度，低噪声阶段更强调安全边界。

**命题 4：边界带 score 与反射扩散的形式对应。** 考虑单个光滑安全域：

$$
\Omega=\{z:g(z,y)\ge0\}.
$$

若边界 $\partial\Omega$ 上 $\nabla g\ne0$，则理想反射扩散要求概率流在边界处没有外向通量。形式上可以写成：

$$
\mathbf J(z,t)\cdot n_{\mathrm{out}}(z)=0,\qquad z\in\partial\Omega.
$$

其中 $\mathbf J$ 是 Fokker-Planck 方程里的概率流，$n_{\mathrm{out}}$ 是外法向。边界带 score 的作用，是在 $0\le g(z,y)\le\tau_t$ 的薄层内提供沿 $\nabla g$ 的内推力，减少采样轨迹穿出 $\Omega$ 的概率。若 $\tau_t\to0$，并且 $\alpha_t$ 随 $\tau_t$ 合理放大，使薄层内累计推回强度保持有限，那么这个 drift 在形式极限上逼近反射扩散的边界推回行为。

这里的“逼近”二字很重要。严格反射扩散的推回只在边界上通过 local time 发生，而 $s_{\partial}$ 在一个厚度为 $\tau_t$ 的边界带内连续作用。它牺牲了一点数学精确性，换来可微、可实现、可放进 diffusion 采样器的形式。

多不等式边界时，可以把各个边界带项相加：

$$
s_{\partial,A}(z,t)
=
\sum_{i\in\mathcal I_A}
\alpha_t
\frac{[\tau_t-g_i(z,y)]_+}{\tau_t}
\nabla_z g_i(z,y).
$$

如果同时激活的边界法向大致线性独立，并且没有强烈冲突，这个相加近似是合理的。但在角点、边界相切、摩擦锥退化或多个约束互相矛盾时，简单相加只能看作一阶近似；严格处理需要 Skorokhod map 或互补条件。论文里应诚实承认这一点，而不是宣称边界带 score 完全等价于反射扩散。

这个公式把“边界无外向通量”的思想变成了一个可放进采样器的近似项。它也比普通 penalty 更有针对性：它只在靠近边界时工作，远离边界时不会干扰生成多样性。


### 8.1 从物理约束到 $g_i(z,y)$ 的基本规则

为了让第八点真正可以实现，需要把每条物理规则都写成安全裕度函数：

$$
g_i(z,y)\ge0.
$$

这里统一约定：$g_i(z,y)>0$ 表示安全，$g_i(z,y)=0$ 表示刚好在边界上，$g_i(z,y)<0$ 表示已经违反约束。这个符号约定非常重要，因为边界带 score 使用的是 $\nabla_z g_i$。也就是说，$\nabla_z g_i$ 应该指向“让样本更安全”的方向。

并不是所有物理指标都适合直接当硬边界。手物不穿透、关节不过界、自碰撞距离为正、接触力不超过上限、摩擦锥裕度为正，这些属于硬安全约束，适合写进 $g_i(z,y)\ge0$。而接触数量、力封闭质量、低功耗程度更像抓取质量指标，可以写成 $g_i$，但第一版更建议把它们作为 ranking、模式权重或低强度 guidance，而不是全部当成硬边界。

本科生友好理解：$g_i$ 就是每条物理规则的“安全余量”。余量越大越安全，余量接近零说明快出事，余量为负说明已经违反规则。第八点做的事，就是在余量快变成负数之前，把样本沿着余量变大的方向推回去。

### 8.2 非穿透约束如何写成 $g$

设物体的 signed distance field 为 $\operatorname{SDF}_y(x)$，约定物体外部为正、表面为零、内部为负。令手表面采样点为 $x_j(z)$，它由手腕位姿和关节角通过前向运动学得到。第 $j$ 个手部采样点的非穿透裕度可以写成：

$$
g_{\mathrm{pen},j}(z,y)=\operatorname{SDF}_y(x_j(z))-\delta_{\mathrm{pen}}.
$$

要求：

$$
g_{\mathrm{pen},j}(z,y)\ge0.
$$

其中 $\delta_{\mathrm{pen}}\ge0$ 是安全余量。若 $\delta_{\mathrm{pen}}=0$，表示只要求不进入物体内部；若 $\delta_{\mathrm{pen}}>0$，表示希望离物体表面保留一点距离。它的梯度由链式法则得到：

$$
\nabla_z g_{\mathrm{pen},j}=J_{x_j}(z)^\top\nabla_x\operatorname{SDF}_y(x_j(z)).
$$

这里 $J_{x_j}(z)=\frac{\partial x_j(z)}{\partial z}$ 是手部采样点对抓取变量 $z$ 的 Jacobian，$\nabla_x\operatorname{SDF}_y$ 是物体 SDF 的空间梯度。在物体表面附近，$\nabla_x\operatorname{SDF}_y$ 近似就是物体外法向。所以这个梯度的直觉是：物体法向告诉手指点往空间哪里移动更安全，手部 Jacobian 再把这个空间移动方向转成手腕和关节应该怎么变。

如果手上采样点很多，不必每一步对所有点都反传。第一版可以只取 SDF 最小的 top-$K$ 个危险点，或者用 soft-min 聚合成一个整体裕度：

$$
g_{\mathrm{pen}}(z,y)=-\beta^{-1}\log\sum_j\exp[-\beta g_{\mathrm{pen},j}(z,y)].
$$

当 $\beta$ 较大时，它近似等于所有采样点中最小的非穿透裕度。它的梯度是各点梯度的 soft 加权平均，因此仍然可微，并且主要关注最危险的穿透点。

### 8.3 接触接近约束如何写成 $g$

接触和非穿透不能混为一谈。非穿透是硬安全要求，接触接近更像抓取质量要求。如果强迫所有手指点都接触物体，模型会倾向于不自然的五指全贴。因此接触约束应该只对候选接触点或某个接触模式 $A$ 中的点使用。

对候选接触点 $j$，令：

$$
\phi_j(z,y)=\operatorname{SDF}_y(x_j(z)).
$$

希望它位于表面附近薄壳内：

$$
0\le \phi_j(z,y)\le \delta_{\mathrm{con}}.
$$

这等价于两条不等式。第一条是不穿透：

$$
g_{\mathrm{con,in},j}(z,y)=\phi_j(z,y)\ge0.
$$

第二条是不要离物体表面太远：

$$
g_{\mathrm{con,out},j}(z,y)=\delta_{\mathrm{con}}-\phi_j(z,y)\ge0.
$$

它们的梯度分别为：

$$
\nabla_z g_{\mathrm{con,in},j}=J_{x_j}^\top\nabla_x\operatorname{SDF}_y(x_j),
$$

$$
\nabla_z g_{\mathrm{con,out},j}=-J_{x_j}^\top\nabla_x\operatorname{SDF}_y(x_j).
$$

这两个方向刚好相反。若手指进入物体，第一项把它推出去；若候选接触点离表面太远，第二项把它拉回来。实现时应该先选少量候选接触点，例如每个手指 SDF 最小的点、网络预测的 contact anchor，或当前模式 $A$ 中要求接触的指尖点。

### 8.4 关节限位如何写成 $g$

设第 $k$ 个关节满足：

$$
q_k^{\min}\le q_k\le q_k^{\max}.
$$

可以写成两条安全裕度：

$$
g_{\mathrm{joint,low},k}(z)=q_k-q_k^{\min},
$$

$$
g_{\mathrm{joint,up},k}(z)=q_k^{\max}-q_k.
$$

若 $z=(\xi_w,q)$，并且 $q_k$ 是 $z$ 中的一个坐标，则梯度非常简单：

$$
\nabla_z g_{\mathrm{joint,low},k}=e_{q_k},
$$

$$
\nabla_z g_{\mathrm{joint,up},k}=-e_{q_k}.
$$

其中 $e_{q_k}$ 是第 $k$ 个关节坐标对应的单位向量。关节限位是第一版最值得实现的边界约束之一，因为它稳定、便宜、物理含义明确。

### 8.5 自碰撞和环境碰撞如何写成 $g$

若两个手部部件 $a$ 和 $b$ 的最近点距离为 $d_{ab}(z)$，自碰撞安全裕度可以写成：

$$
g_{\mathrm{self},ab}(z)=d_{ab}(z)-\delta_{\mathrm{self}}.
$$

若最近点分别为 $x_a(z)$ 和 $x_b(z)$，并近似：

$$
d_{ab}(z)=\|x_a(z)-x_b(z)\|,
$$

则在最近点不切换的局部区域内：

$$
\nabla_z d_{ab}=(J_{x_a}-J_{x_b})^\top\frac{x_a-x_b}{\|x_a-x_b\|+\eta}.
$$

环境碰撞类似。若环境 SDF 为 $\operatorname{SDF}_{\mathrm{env}}$，则：

$$
g_{\mathrm{env},j}(z)=\operatorname{SDF}_{\mathrm{env}}(x_j(z))-\delta_{\mathrm{env}},
$$

$$
\nabla_z g_{\mathrm{env},j}=J_{x_j}^\top\nabla_x\operatorname{SDF}_{\mathrm{env}}(x_j).
$$

这类距离函数通常是分段光滑的，因为最近点可能切换。工程上可以用稠密采样点、SDF 网格或 soft-min 聚合来缓和不连续。

### 8.6 摩擦锥如何写成 $g$

如果系统已经有接触力估计，摩擦锥可以写成硬安全边界。令第 $i$ 个接触点的法向力为 $f_{n,i}$，切向力为 $f_{t,i}$，摩擦系数为 $\mu_i$。Coulomb 摩擦条件是：

$$
\|f_{t,i}\|\le\mu_i f_{n,i}.
$$

对应裕度为：

$$
g_{\mathrm{fric},i}(z,f,y)=\mu_i f_{n,i}-\|f_{t,i}\|.
$$

若接触力 $f_i$ 是变量，梯度为：

$$
\nabla_{f_{n,i}}g_{\mathrm{fric},i}=\mu_i,
$$

$$
\nabla_{f_{t,i}}g_{\mathrm{fric},i}=-\frac{f_{t,i}}{\|f_{t,i}\|+\eta}.
$$

若 diffusion 只生成姿态 $z$，不生成接触力，那么必须通过接触力估计器继续链式反传：

$$
\nabla_z g_{\mathrm{fric},i}=\left(\frac{\partial f_i}{\partial z}\right)^\top\nabla_{f_i}g_{\mathrm{fric},i}.
$$

如果你的 demo 目前没有真实触觉或仿真接触力，第一版不建议把摩擦锥当成硬边界。更稳妥的做法是先实现非穿透、关节限位和接触薄壳；等仿真里能得到接触力之后，再加入摩擦裕度。

### 8.7 低功耗和力封闭能否写成 $g$

可以，但要谨慎。若有一个任务方向最坏功耗指标 $P^\star(z,y;\mathcal D)$，希望它不超过阈值 $P_{\max}$，可以写成：

$$
g_{\mathrm{power}}(z,y)=P_{\max}-P^\star(z,y;\mathcal D).
$$

梯度为：

$$
\nabla_z g_{\mathrm{power}}=-\nabla_z P^\star(z,y;\mathcal D).
$$

如果 $P^\star$ 来自内层 QP 或 SOCP，就需要 KKT 隐式微分；如果第一版不想这么复杂，可以用可微代理指标，例如关节力矩平方、法向内力平方或任务方向 wrench 残差。

GraspQP residual 也可以写成 $g$。若 $E_{\mathrm{QP}}(z,y)$ 越小越好，则：

$$
g_{\mathrm{fc}}(z,y)=E_{\max}-E_{\mathrm{QP}}(z,y).
$$

于是：

$$
\nabla_z g_{\mathrm{fc}}=-\nabla_z E_{\mathrm{QP}}(z,y).
$$

但如果论文核心只围绕这个 $g_{\mathrm{fc}}$ 展开，就会非常接近 GraspQP-guided diffusion。因此建议把 GraspQP residual 放在扩展实验或强 baseline 中，第一版安全边界先用更基础的非穿透、关节限位、接触薄壳和自碰撞。

### 8.8 边界带 score 的工程形式

为了避免不同约束的单位不一致，可以使用归一化内法向：

$$
\hat n_i(z,y)=\frac{\nabla_z g_i(z,y)}{\|\nabla_z g_i(z,y)\|+\eta}.
$$

边界带 score 写成：

$$
s_{\partial}(z,t,y)=\sum_i\alpha_{i,t}\frac{[\tau_{i,t}-g_i(z,y)]_+}{\tau_{i,t}}\hat n_i(z,y).
$$

其中 $\tau_{i,t}$ 是第 $i$ 类约束的边界带宽，$\alpha_{i,t}$ 是推回强度。一个自然设置是：

$$
\tau_{i,t}=c_i\sigma_t+\tau_{i,\min},
$$

$$
\alpha_{i,t}=\min\left(\frac{a_i}{\tau_{i,t}+\eta},\alpha_{i,\max}\right).
$$

这样噪声大时边界带较宽，噪声小时边界带较窄；低噪声阶段更接近真实安全边界。完整采样 score 为：

$$
s_{\mathrm{safe}}(z,t,y)=s_\theta(z,t,y)+s_{\partial}(z,t,y).
$$

若使用 epsilon prediction，且：

$$
s_\theta(z_t,t,y)\approx-\frac{\epsilon_\theta(z_t,t,y)}{\sqrt{1-\bar\alpha_t}},
$$

则可以写成：

$$
\epsilon_{\mathrm{safe}}=\epsilon_\theta-\sqrt{1-\bar\alpha_t}\ s_{\partial}(z_t,t,y).
$$

更推荐的实现是在 denoised estimate $\hat z_0$ 上计算物理约束，因为高噪声的 $z_t$ 本身未必是一个有物理意义的手姿态。先计算 $g_i(\hat z_0,y)$ 和 $\nabla_{\hat z_0}g_i(\hat z_0,y)$，再修正 clean prediction：

$$
\hat z_0^{\mathrm{safe}}=\hat z_0+\rho_t s_{\partial}(\hat z_0,t,y).
$$

最后把 $\hat z_0^{\mathrm{safe}}$ 放回 DDIM 或 DDPM 更新。这里 $\rho_t$ 是修正步长。低噪声阶段可以大一些，高噪声阶段应小一些，甚至只在后 $30\%$ 到 $50\%$ 的 denoising steps 使用边界带。

### 8.9 PyTorch 实现伪代码

第一版 demo 可以按下面流程实现：

```text
z0_hat.requires_grad_(True)

hand_points = forward_kinematics_points(z0_hat)
sdf_values = object_sdf(hand_points)
g_pen = sdf_values - delta_pen

q = extract_joint_angles(z0_hat)
g_joint_low = q - q_min
g_joint_up = q_max - q

contact_points = select_contact_candidates(hand_points, sdf_values)
phi = object_sdf(contact_points)
g_contact_out = delta_contact - phi

all_g = [topk_or_softmin(g_pen), g_joint_low, g_joint_up, g_contact_out]

s_boundary = 0
for g in all_g:
    active = relu(tau_t - g) / tau_t
    grad_g = autograd_grad(g.sum(), z0_hat)
    direction = grad_g / (norm(grad_g) + eta)
    s_boundary += alpha_t * active_mean_or_broadcast(active) * direction

s_boundary = clip_norm(s_boundary, max_norm_t)
z0_safe = z0_hat + rho_t * s_boundary
use z0_safe in DDIM/DDPM update
```

实现时有四个注意点。第一，$g$ 可以逐点计算，也可以用 soft-min 聚合；为了速度，第一版建议只取 top-$K$ 危险点。第二，$s_{\partial}$ 必须做范数裁剪，避免某一步更新过大破坏采样。第三，接触接近项只对候选接触点使用，不要对所有手表面点使用。第四，如果某个 $g_i$ 的梯度接近零，说明该约束当前不可辨认或数值不稳定，可以跳过它或增大 $\eta$。

### 8.10 与 penalty guidance、GraspQP 和反射扩散的区别

边界带 score 和普通 penalty guidance 表面上都用了 $\nabla g_i$，但逻辑不同。Penalty 通常先构造全局能量：

$$
E_{\mathrm{pen}}(z,y)=\sum_i[-g_i(z,y)]_+^2,
$$

然后用 $-\nabla_z E_{\mathrm{pen}}$ 修正样本。它主要在越界之后惩罚坏样本。边界带 score 则在 $0\le g_i\le\tau_t$ 时就提前介入，目标是模拟安全域边界附近的内法向推回。远离边界时 $s_{\partial}=0$，不会干扰 diffusion 原本的生成多样性。

它和 GraspQP 也不同。GraspQP 的核心是判断接触 wrench 是否能形成 force closure，并通过 QP residual 优化抓取稳定性。边界带 score 的核心是防止样本越过显式安全边界，例如穿透、关节越界、摩擦锥违反。GraspQP 更像抓取质量和稳定性评价器；边界带更像采样过程中的安全护栏。二者可以组合，但不应混为一个贡献。

它和严格反射扩散也不同。严格反射扩散的边界推回由 boundary local time 表示，只在边界上发生，并对应连续过程中的零通量条件。本文的 $s_{\partial}$ 是边界带近似，它在厚度为 $\tau_t$ 的薄层内连续作用。这样牺牲了严格路径不变性，换来可微、稳定、容易接入 DDPM/DDIM sampler 的实现形式。论文里应该说它是 reflection-inspired boundary-layer guidance，而不是宣称已经实现严格 reflected diffusion。

### 8.11 最小可行版本

如果要马上接现有 diffusion demo，建议第一版只实现四类 $g$：

$$
g_{\mathrm{pen},j}=\operatorname{SDF}_y(x_j(z))-\delta_{\mathrm{pen}},
$$

$$
g_{\mathrm{joint,low},k}=q_k-q_k^{\min},
$$

$$
g_{\mathrm{joint,up},k}=q_k^{\max}-q_k,
$$

$$
g_{\mathrm{con,out},j}=\delta_{\mathrm{con}}-\operatorname{SDF}_y(x_j(z)).
$$

其中 $g_{\mathrm{con,out},j}$ 只对少量候选接触点使用。这样可以先验证三个关键结果：穿透是否减少，关节越界是否减少，有效接触是否增加。等这三项稳定后，再加入自碰撞、摩擦锥、接触力上限和低功耗边界。

这一节最终想表达的是：

$$
\boxed{
\text{不等式物理约束进入 diffusion 的关键，是把每条规则写成安全裕度 }g_i(z,y)\ge0\text{，再用 }\nabla_z g_i\text{ 构造边界带内法向推回。}
}
$$

---

## 9. 四个核心理论结论

**结论一：分层平滑 score 展开。** 如果安全抓取分布由多个接触模式层组成：

$$
p_0(z|y)=\sum_A\rho_A(z|y)\delta_{\mathcal M_A}(z),
$$

并且每个 $\mathcal M_A$ 在局部是 $C^2$ 接触层、具有管状邻域，那么高斯平滑后的 score 是各模式 score 的加权平均：

$$
\nabla_z\log p_\sigma(z|y)
=
\sum_A
w_A(z,\sigma,y)
\left[
-\frac{z-\Pi_A(z)}{\sigma^2}
+
P_A\nabla_{\mathcal M_A}\log\rho_A
+
\mathcal C_A
\right]
+
O(\sigma).
$$

这里的关键不是形式上的加权平均，而是低噪声下每个模式都有主导法向项 $-(z-\Pi_A(z))/\sigma^2$。这说明物理约束不是额外 penalty，而是低维安全分布被高斯平滑后必然出现的 score 结构。

**结论二：显式约束决定法向 score。** 若某个模式的约束为 $c_A(z,y)=0$，可计算版本使用阻尼自然法向：

$$
s_N^A(z,t,y)
=
-\frac1{\sigma_t^2}
J_A^\top G_A^{-1}c_A(z,y).
$$

在 regular 区域，无阻尼版本与真实投影方向的向量误差是 $O(\|c_A\|^2)$；阻尼版本引入小偏差，但保证 $J_AJ_A^\top$ 近奇异时不会数值爆炸。因此 CSSD 不依赖“精确投影可算”这个不现实假设。

**结论三：模式权重可用 Laplace 近似。** 精确 $w_A$ 不直接可算，但可以用：

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

其中 $k_A$ 是模式 $A$ 的余维度。这个项不能随便省略，因为不同接触数量对应不同维度的可行层。Laplace 权重的意义是：接触模式竞争由距离、局部体积、维度尺度和先验共同决定，而不是简单地偏向“五指全接触”。

**结论四：不等式边界用边界带修正。** 对 $g_i(z,y)\ge0$，使用：

$$
s_{\partial}(z,t)
=
\sum_i
\alpha_t
\frac{[\tau_t-g_i(z,y)]_+}{\tau_t}
\nabla_z g_i(z,y).
$$

它不是严格反射扩散本身，而是反射边界 local time 的可微边界层近似。它对应的理论目标是逼近边界零通量行为：远离边界不干预，靠近危险区域才沿安全域内侧推回。

这四个结论合在一起，得到更接近可计算方法的 CSSD 公式：

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

这也是当前最值得作为论文方法核心的版本。它既保留了分布平滑推导，又避开了精确投影和精确模式积分不可计算的问题。

---

## 10. 这项工作目前值不值 9/10

我的判断是：**作为理论方向，它具备 9/10 的潜力；作为已经完成的论文理论，它目前接近但还没有完全稳到 9/10。** 加入分层 score 定理、阻尼自然法向误差界、Laplace 模式权重和边界带修正之后，它比最初版本更完整，已经具备一个顶会方法的形状。

它强在三个地方。第一，它抓住了 diffusion 的数学本质：score 来自平滑后的数据分布，而不是任意引导项。第二，它抓住了灵巧手的物理本质：接触模式是分层的，不是单一光滑流形。第三，它把物理约束和学习任务分开：物理给出法向约束，网络学习切向分布。

它还差在证明和验证层面的完整性。要真正稳到 9/10，需要把本文的四个命题进一步写成论文里的正式定理或 proposition：分层 score 展开要控制 $O(\sigma)$ 余项；阻尼自然法向要给出清楚误差界；Laplace 权重要说明余维度因子和可靠条件；边界带 score 要明确它只是反射扩散的薄层近似。这些不是方向性问题，而是论文严谨度问题。

如果从投稿策略看，这项工作的强度不应该靠“用了很多物理约束”来体现，而应该靠“给出了一个现有 diffusion 理论没有直接覆盖的物理几何对象”来体现。这个对象就是接触模式分层的安全抓取分布。只要论文能把分层平滑 score 展开写严谨，并说明它如何退化到已有流形 score 理论、又如何超出单一流形理论，它就有机会达到 9/10 的理论水准。

---

## 11. 与已有理论的关系

CSSD 和普通 Riemannian diffusion 的区别在于：Riemannian diffusion 通常假设数据生活在一个给定光滑流形上，而 CSSD 认为灵巧手安全抓取生活在多个接触模式层的并集上。每个模式内部可以使用流形 score 的思想，但模式之间的权重 $\tilde w_A$ 和接触切换是 CSSD 的新增内容。

CSSD 和 constrained diffusion 或 reflected diffusion 的关系在于：这些理论说明边界可以作为扩散过程的一部分，而不是样本生成后的修复。CSSD 借用了这个思想，但边界来自具体接触物理，例如非穿透和摩擦锥，并通过边界带 score 给出一个可实现近似。

CSSD 和 classifier guidance 的区别在于：classifier guidance 学的是某个类别或成功概率的梯度，而 CSSD 不用黑盒安全分类器替代物理。它用显式几何对象 $\phi_i$、$c_A$、$J_A$、$G_A$ 和 $P_A$ 解释 score 的结构。

CSSD 和普通 penalty guidance 的区别也应正面说明。在单一约束、权重调得很好的情况下，二者可能给出相似方向；但 CSSD 的优势在于自然度规 $G_A^{-1}$、噪声尺度 $1/\sigma_t^2$、模式权重 $\tilde w_A$ 和边界带 $s_{\partial,A}$。这些结构共同让它更适合多接触模式和约束尺度不一致的灵巧手抓取。

---

## 12. 诚实边界

这条理论不应该声称解决所有真实接触问题。它默认每个接触模式层在局部足够光滑，具有管状邻域，并避开特别复杂的 grazing 状态；它默认阻尼自然法向在 regular 区域可以近似局部投影方向，在秩退化区域只保证稳定而不保证完全正确；它使用 Laplace 近似来替代高维流形积分，因此最可靠的区域是低噪声、局部投影明确、模式贡献由投影点附近主导的区域；它把边界带 score 作为反射扩散的可微薄层近似，而不是严格 local time；它把摩擦锥和刚性接触作为近似物理模型；它讨论的是连续时间或低噪声渐近结构，离散采样仍会有误差。

这些边界不是缺点，而是理论工作必须讲清楚的条件。一个可靠的顶会理论主张不应说“我们完美解决所有安全抓取”，而应说“在明确的接触几何假设下，我们证明显式物理约束如何决定 diffusion score 的结构，并给出可计算的渐近近似”。

---

## 13. 最终总结

CSSD 的可计算主公式是：

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

这两个公式共同表达本文最重要的结论：

$$
\boxed{
\text{安全抓取生成的关键不是学习物理约束，而是利用物理约束揭示 diffusion score 的奇异几何。}
}
$$

更通俗地说，CSSD 的逻辑链条是：

$$
\boxed{
\text{接触模式分层}
\Rightarrow
\text{多层奇异分布}
\Rightarrow
\text{高斯平滑}
\Rightarrow
\text{score 分解}
\Rightarrow
\text{物理法向 + 数据切向 + 模式权重}
}
$$

---

## 14. 实验验证逻辑：基于已有 diffusion demo 如何推进

你目前已经跑通了一个基于 diffusion 的灵巧手抓取最基本 demo，这正好可以作为 CSSD 的起点。实验不需要一开始就验证完整接触力学，也不需要马上处理所有复杂物理。第一阶段只需要证明一个核心问题：**CSSD 是否比普通 diffusion 和普通 penalty guidance 更好地减少不安全样本，同时保留合理接触模式和多样性。**

实验可以分三组。第一组是 **Base Diffusion**，也就是你现在已有的模型，只输入物体条件 $y$，生成抓取构型 $z=(T_w,q)$。这一组用于说明原始 diffusion 的基础能力和物理缺陷，例如穿透、接触不足或关节越界。

第二组是 **Penalty Guidance**，在采样时加入普通物理惩罚，例如穿透惩罚、接触距离惩罚和关节限位惩罚。这是必须有的强 baseline，因为审稿人会问：为什么不用更简单的 penalty？如果 CSSD 不能明显优于它，理论优势就很难转化成方法优势。

第三组是 **CSSD Guidance**，加入三件东西：阻尼自然法向 $-J_A^\top G_A^{-1}c_A/\sigma_t^2$，模式权重 $\tilde w_A$，以及不等式边界带 $s_{\partial,A}$。第一版不需要枚举所有接触模式，可以只选择少量候选模式，例如二指、三指、四指和五指接触中的 top-k 模式，或者根据当前 gap 最小的几个指尖构造候选模式。

评价指标保持简单。至少报告穿透率和最大穿透深度，用来说明安全性；报告有效接触数量和接触分布，用来说明不是盲目五指全接触；报告关节限位违反率，用来说明可执行性；报告生成多样性，用来说明 CSSD 没有把样本全部压到同一种抓取；如果已有仿真环境，再报告简单 lift 成功率或扰动稳定率。

实验逻辑应当这样讲：Base Diffusion 证明原始模型会生成多样但不一定安全的抓取；Penalty Guidance 证明简单物理修正确实有帮助，但可能牺牲多样性或强迫不合理接触；CSSD 证明利用自然法向、模式权重和边界带，可以在安全性、接触模式合理性和多样性之间取得更好的平衡。

第一阶段实验的目标不是证明“完整灵巧手力学安全已经解决”，而是证明 CSSD 的核心理论预测成立：**物理法向应该由约束几何给出，接触模式应该通过权重竞争选择，不等式边界应该只在靠近危险区域时介入。**

---

## 参考入口

- [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/abs/2011.13456)
- [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)
- [Riemannian Score-Based Generative Modelling](https://arxiv.org/abs/2202.02763)
- [Riemannian Diffusion Models](https://arxiv.org/abs/2208.07949)
- [Score-Based Generative Models Detect Manifolds](https://arxiv.org/abs/2206.01018)
- [Diffusion Models for Constrained Domains](https://arxiv.org/abs/2304.05364)
- [Reflected Schrödinger Bridge for Constrained Generative Modeling](https://arxiv.org/abs/2401.03228)
- [CFG++: Manifold-constrained Classifier Free Guidance for Diffusion Models](https://arxiv.org/abs/2406.08070)
