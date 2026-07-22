---
tags:
  - 灵巧手专项
  - diffusion
  - physical_constraints
  - math_derivation
  - dexterous_hand
created: 2026-06-19
source_pdf: "[[灵巧手专项/物理约束分类.pdf]]"
related:
  - "[[灵巧手专项/灵巧手物理约束注入Diffusion论文清单.md]]"
---

# ABCD 物理约束如何注入 Diffusion：数学推导笔记

> 本文依据 `[[灵巧手专项/物理约束分类.pdf]]` 的 A/B/C/D 分类，只讨论理论建模和数学注入方式，刻意忽略工程实现、数据现状、代码路线和当前缓存统计。  
> 这里的目标不是“训练一个网络去学物理”，而是先把物理约束写成清楚的数学对象，再说明它如何进入 diffusion 的分布、score 或采样更新。

## 0. 总体框架：从物理约束到 guided diffusion

设 diffusion 生成变量为

$$
z.
$$

在不同任务里，$z$ 可以是不同对象：

- 若是 Diffusion Policy，$z=a_{0:H-1}$ 是未来 $H$ 步动作序列；
- 若是静态抓取生成，$z=q$ 是手部姿态、手腕位姿和关节角；
- 若是接触力学生成，$z=(q,c,f)$ 可以同时包含手姿态、接触点和接触力；
- 若是任务级轨迹生成，$z=(a_{0:H-1},q_{0:H},o_{0:H})$ 可以包含动作、手状态和物体状态。

给定条件 $y$，例如物体点云、目标位姿、阶段信息、当前观测，普通 diffusion 学习的是数据分布

$$
p_{data}(z|y).
$$

若我们希望生成结果满足物理约束，不应只学习 $p_{data}$，而应学习一个被物理能量重新加权后的分布：

$$
\tilde p(z|y)
=
\frac{1}{Z(y)}
p_{data}(z|y)
\exp[-E_{phys}(z,y)].
$$

其中

$$
E_{phys}(z,y)
=
\sum_k \lambda_k \Phi_k(z,y)
$$

是所有物理约束 penalty 的加权和。$\Phi_k$ 越大，表示违反第 $k$ 类物理约束越严重；$\lambda_k$ 控制该约束的重要性。

对 $\tilde p$ 求 score，可得

$$
\nabla_z\log \tilde p(z|y)
=
\nabla_z\log p_{data}(z|y)
-
\nabla_z E_{phys}(z,y).
$$

这就是物理约束注入 diffusion 的核心公式。普通 score 负责“像数据”，物理梯度 $-\nabla E_{phys}$ 负责“少违反物理”。如果按类别拆开：

$$
\nabla_z\log \tilde p(z|y)
=
\nabla_z\log p_{data}(z|y)
-
\lambda_A\nabla_zE_A
-
\lambda_B\nabla_zE_B
-
\lambda_C\nabla_zE_C
-
\lambda_D\nabla_zE_D.
$$

其中：

- $E_A$：动作层约束；
- $E_B$：接触力学约束；
- $E_C$：抓取质量与力封闭约束；
- $E_D$：物体层与任务成功约束。

在 DDPM 形式下，若正向扩散为

$$
z_t=\sqrt{\bar\alpha_t}z_0+\sqrt{1-\bar\alpha_t}\epsilon,
\quad \epsilon\sim\mathcal{N}(0,I),
$$

模型通常预测噪声 $\epsilon_\theta(z_t,t,y)$。Tweedie 形式的干净样本估计为

$$
\hat z_0(z_t,t)
=
\frac{z_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta(z_t,t,y)}
{\sqrt{\bar\alpha_t}}.
$$

物理 guidance 可以在 $\hat z_0$ 上计算：

$$
E_{phys}(\hat z_0(z_t,t),y),
$$

然后通过链式法则得到对 noisy sample 的修正方向：

$$
\nabla_{z_t}E_{phys}(\hat z_0(z_t,t),y)
=
\left(\frac{\partial \hat z_0}{\partial z_t}\right)^\top
\nabla_{\hat z_0}E_{phys}(\hat z_0,y).
$$

如果忽略网络项对 $z_t$ 的二阶依赖，常用近似是

$$
\frac{\partial \hat z_0}{\partial z_t}
\approx
\frac{1}{\sqrt{\bar\alpha_t}}I,
$$

于是

$$
\nabla_{z_t}E_{phys}(\hat z_0,y)
\approx
\frac{1}{\sqrt{\bar\alpha_t}}
\nabla_{\hat z_0}E_{phys}(\hat z_0,y).
$$

在采样时，就可以把物理修正加入 score：

$$
s_{guided}(z_t,t,y)
=
s_\theta(z_t,t,y)
-
\eta_t\nabla_{z_t}E_{phys}(\hat z_0(z_t,t),y).
$$

或者等价地，在 epsilon-space 中将噪声预测修正为

$$
\epsilon_{guided}
=
\epsilon_\theta
+
\sqrt{1-\bar\alpha_t}\,
\eta_t\nabla_{z_t}E_{phys}(\hat z_0,y).
$$

这个总框架后面会分别落到 A/B/C/D 四类物理约束上。

---

# A. 动作层约束如何注入 Diffusion

A 类约束直接作用在动作序列上。设 diffusion 生成未来 $H$ 步动作：

$$
a_{0:H-1}=(a_0,a_1,\dots,a_{H-1}),
\quad a_t\in\mathbb{R}^m.
$$

将所有动作堆叠为一个向量：

$$
a=
\begin{bmatrix}
a_0\\a_1\\ \vdots\\ a_{H-1}
\end{bmatrix}
\in\mathbb{R}^{Hm}.
$$

A 类物理约束本质上是在限制动作序列的时间变化、幅值、饱和、关节限位和协调性。它最适合直接注入 action diffusion，因为所有 penalty 都可以直接对 $a$ 求梯度。

## A.1 动作平滑性

动作平滑性可由二阶差分定义：

$$
\Delta^2 a_t=a_{t+2}-2a_{t+1}+a_t.
$$

平滑性惩罚：

$$
E_{smooth}(a)
=
\sum_{t=0}^{H-3}\|\Delta^2 a_t\|_2^2.
$$

令 $D_2$ 为二阶差分矩阵，则

$$
E_{smooth}(a)=\|D_2a\|_2^2.
$$

其梯度为

$$
\nabla_aE_{smooth}(a)
=
2D_2^\top D_2a.
$$

因此在 guided score 中加入

$$
-\lambda_s\nabla_aE_{smooth}
=
-2\lambda_sD_2^\top D_2a.
$$

这个项等价于抑制动作序列中的高频振荡。$D_2^\top D_2$ 是离散双拉普拉斯算子，会把相邻时间步之间剧烈的加速度变化压平。

## A.2 动作能量 / 控制 effort

动作能量可定义为

$$
E_{energy}(a)
=
\sum_{t=0}^{H-1}\|a_t\|_2^2
=
\|a\|_2^2.
$$

梯度为

$$
\nabla_aE_{energy}(a)=2a.
$$

guidance 项为

$$
-2\lambda_e a.
$$

这会把动作往零附近收缩，避免过大控制输入。若 root 动作和 finger 动作应有不同权重，可写为

$$
E_{energy}(a)
=
\sum_t
\left(
\lambda_r\|a_t^{root}\|_2^2
+
\lambda_f\|a_t^{finger}\|_2^2
\right).
$$

对应梯度是逐块缩放：

$$
\nabla_{a_t^{root}}E=2\lambda_r a_t^{root},
\quad
\nabla_{a_t^{finger}}E=2\lambda_f a_t^{finger}.
$$

## A.3 动作饱和率

若动作被归一化到 $[-1,1]$，硬约束是

$$
|a_{t,j}|\le a_{\max}.
$$

可用 hinge penalty：

$$
E_{sat}(a)
=
\sum_{t,j}
\left[|a_{t,j}|-a_{\max}\right]_+^2.
$$

其中 $[r]_+=\max(r,0)$。对单个元素，有

$$
\frac{\partial E_{sat}}{\partial a_{t,j}}
=
2[|a_{t,j}|-a_{\max}]_+
\operatorname{sign}(a_{t,j})
\quad \text{if } |a_{t,j}|>a_{\max},
$$

若未饱和则梯度为 $0$。guided score 中的负梯度会把超过边界的动作拉回可行区间。

若希望更接近硬约束，可用 log-barrier：

$$
E_{barrier}(a)
=
-
\sum_{t,j}
\log(a_{\max}^2-a_{t,j}^2).
$$

其梯度为

$$
\frac{\partial E_{barrier}}{\partial a_{t,j}}
=
\frac{2a_{t,j}}{a_{\max}^2-a_{t,j}^2}.
$$

当 $|a_{t,j}|\to a_{\max}$ 时，梯度趋于无穷大，因此比 hinge 更像安全边界。

## A.4 关节限位余量

若动作是关节目标，或者动作通过动力学映射得到未来关节状态

$$
q_{0:H}=F_q(a_{0:H-1},q_0),
$$

关节限位为

$$
q_{\min}\le q_t\le q_{\max}.
$$

定义安全余量 $\delta>0$，希望关节不只是满足限位，而是远离限位：

$$
q_{\min}+\delta\le q_t\le q_{\max}-\delta.
$$

hinge penalty 为

$$
E_{joint}(q)
=
\sum_{t,j}
\left[q_{\min,j}+\delta-q_{t,j}\right]_+^2
+
\left[q_{t,j}-q_{\max,j}+\delta\right]_+^2.
$$

对关节状态的梯度为

$$
\frac{\partial E_{joint}}{\partial q_{t,j}}
=
-2[q_{\min,j}+\delta-q_{t,j}]_+
+
2[q_{t,j}-q_{\max,j}+\delta]_+.
$$

若 diffusion 变量是动作 $a$，则通过链式法则：

$$
\nabla_aE_{joint}
=
\left(\frac{\partial F_q}{\partial a}\right)^\top
\nabla_qE_{joint}.
$$

理论上，这就是把关节限位从 state constraint 传回 action diffusion 的方式。

## A.5 Receding-horizon 块间一致性

Diffusion Policy 每次预测一个 action chunk，但实际只执行前几步。设第 $k$ 次查询得到 chunk $a^{(k)}_{0:H-1}$，第 $k+1$ 次查询得到 $a^{(k+1)}_{0:H-1}$。两次预测在重叠时间段上应一致。设选择矩阵 $P_1,P_2$ 提取重叠区域，则

$$
E_{cons}(a^{(k)},a^{(k+1)})
=
\|P_1a^{(k)}-P_2a^{(k+1)}\|_2^2.
$$

对当前 chunk 的梯度是

$$
\nabla_{a^{(k+1)}}E_{cons}
=
2P_2^\top(P_2a^{(k+1)}-P_1a^{(k)}).
$$

这会让当前生成的动作 chunk 与上一轮已经承诺的未来计划保持一致，从而减少手指开合抖动和 root 漂移。

## A.6 Root-Finger 动作平衡

设动作分为 root 和 finger：

$$
a_t=(a_t^r,a_t^f).
$$

定义能量比

$$
R_t=
\frac{\|a_t^r\|_2^2}
{\|a_t^f\|_2^2+\varepsilon}.
$$

若某阶段期望比值为 $R_t^\star$，可定义

$$
E_{balance}
=
\sum_t (R_t-R_t^\star)^2.
$$

这是一个阶段条件物理协调约束：approach 阶段 root 可主导，close / stabilize 阶段 finger 应主导。若不希望使用比值导致数值不稳，也可用线性形式：

$$
E_{balance}
=
\sum_t
\left(
\|a_t^r\|_2^2
-\rho_t\|a_t^f\|_2^2
\right)^2.
$$

其中 $\rho_t$ 根据阶段设定。该约束保证“运输组分”和“握持组分”的物理时序协调。

## A 类总能量

A 类约束可统一写成：

$$
E_A(a)
=
\lambda_sE_{smooth}
+
\lambda_eE_{energy}
+
\lambda_{sat}E_{sat}
+
\lambda_jE_{joint}
+
\lambda_cE_{cons}
+
\lambda_bE_{balance}.
$$

注入 diffusion：

$$
s_{guided}
=
s_\theta
-
\nabla_aE_A(a).
$$

A 类约束是最适合先做的，因为它们基本不依赖接触法向、接触点、凸包或仿真 rollout，数学上最直接。

---

# B. 接触力学约束如何注入 Diffusion

B 类约束关注手指与物体之间的接触是否物理合理。设第 $i$ 个接触点为 $p_i(q)$，接触力为 $f_i$，物体表面 signed distance function 为

$$
\phi_o(p),
$$

约定 $\phi_o(p)>0$ 在物体外部，$\phi_o(p)=0$ 在表面，$\phi_o(p)<0$ 在物体内部。表面法向为

$$
n_i=\frac{\nabla \phi_o(p_i)}{\|\nabla \phi_o(p_i)\|}.
$$

接触力可分解为法向和切向：

$$
f_{n,i}=n_i^\top f_i,
$$

$$
f_{t,i}=(I-n_in_i^\top)f_i.
$$

B 类约束的核心是：接触点应在表面附近，接触力应满足非负法向力和摩擦锥约束，接触应稳定、持续、均衡。

## B.1 接触建立与非穿透

非穿透约束为

$$
\phi_o(p_i(q))\ge 0.
$$

如果希望某些指尖建立接触，还需要接近表面：

$$
\phi_o(p_i(q))\approx 0.
$$

二者可通过不同 penalty 表达。非穿透 penalty：

$$
E_{pen}(q)
=
\sum_i[-\phi_o(p_i(q))]_+^2.
$$

接触吸引 penalty：

$$
E_{contact}(q)
=
\sum_i w_i\phi_o(p_i(q))^2,
$$

其中 $w_i$ 是希望第 $i$ 个指尖接触时的权重。若不希望所有指尖都被强制吸到表面，可使用目标接触集合 $\mathcal{C}$：

$$
E_{contact}(q)
=
\sum_{i\in\mathcal{C}}\phi_o(p_i(q))^2.
$$

梯度通过链式法则传回手姿态：

$$
\nabla_qE_{pen}
=
\sum_i
2[-\phi_i]_+
(-\nabla_q\phi_i),
$$

其中

$$
\nabla_q\phi_i
=
\left(\frac{\partial p_i}{\partial q}\right)^\top
\nabla_p\phi_o(p_i)
=
J_i(q)^\top\nabla_p\phi_o(p_i).
$$

$J_i(q)$ 是第 $i$ 个指尖位置对手部关节的雅可比矩阵。这个公式说明：穿透惩罚如何通过物体 SDF 法向和手部雅可比，转化为对关节/手腕姿态的修正。

## B.2 法向力非负与摩擦锥

物理接触要求法向力非负：

$$
f_{n,i}=n_i^\top f_i\ge 0.
$$

Coulomb 摩擦锥要求：

$$
\|f_{t,i}\|_2\le \mu_i f_{n,i}.
$$

可以定义摩擦锥违反量：

$$
r_i(f_i,q)
=
\|f_{t,i}\|_2-\mu_i f_{n,i}.
$$

摩擦 penalty：

$$
E_{fric}
=
\sum_i
[r_i]_+^2
+
[-f_{n,i}]_+^2.
$$

当 $r_i>0$ 时，接触力落在摩擦锥外，有滑移风险。对 $f_i$ 求梯度，在忽略 $n_i$ 对 $q$ 的依赖时：

$$
\nabla_{f_i} r_i
=
\frac{f_{t,i}}{\|f_{t,i}\|_2}
-
\mu_i n_i.
$$

因此

$$
\nabla_{f_i}E_{fric}
=
2[r_i]_+
\left(
\frac{f_{t,i}}{\|f_{t,i}\|_2}
-
\mu_i n_i
\right)
-2[-f_{n,i}]_+n_i.
$$

guided score 中的负梯度会把切向力压低、法向力提高，使接触力回到摩擦锥内部。

## B.3 活跃接触数量的可微化

活跃接触数量本来是离散指标：

$$
N_c=\sum_i\mathbf{1}(\|f_i\|>\tau).
$$

为了注入 diffusion，可用 sigmoid 近似：

$$
\tilde N_c
=
\sum_i
\sigma(\kappa(\|f_i\|-\tau)).
$$

若希望至少 $N_{\min}$ 个活跃接触：

$$
E_{count}
=
[N_{\min}-\tilde N_c]_+^2.
$$

这个约束的梯度会鼓励更多指尖形成有效接触。它不是严格的力封闭，但对灵巧手抓取非常实用，因为少于一定数量的接触通常无法形成稳定抓取。

## B.4 接触力平衡与对称性

设指尖力幅值为

$$
F_i=\|f_i\|_2.
$$

可以用方差衡量接触分布不均：

$$
E_{sym}
=
\frac{1}{N}\sum_i(F_i-\bar F)^2,
\quad
\bar F=\frac{1}{N}\sum_iF_i.
$$

也可以显式建模拇指与四指的拮抗：

$$
E_{opp}
=
\left(
F_{thumb}
-
\sum_{i\in fingers}F_i
\right)^2.
$$

这类约束不会保证力封闭，但会减少“一根手指过度用力、其他手指没有参与”的不良接触模式。

## B.5 接触持续性与力振荡

若接触强度为软变量

$$
s_{i,t}=\sigma(\kappa(\|f_{i,t}\|-\tau)),
$$

接触持续性可写为

$$
E_{persist}
=
\sum_{i,t}(s_{i,t+1}-s_{i,t})^2.
$$

接触力振荡可写为

$$
E_{force\_osc}
=
\sum_{i,t}\|f_{i,t+1}-f_{i,t}\|_2^2.
$$

二者的负梯度都会抑制接触闪烁和力 chatter。对 diffusion policy 而言，这些项可直接作用在生成的接触力序列或通过仿真状态反传到动作序列。

## B 类总能量

$$
E_B
=
\lambda_{pen}E_{pen}
+
\lambda_{contact}E_{contact}
+
\lambda_{fric}E_{fric}
+
\lambda_{count}E_{count}
+
\lambda_{sym}E_{sym}
+
\lambda_{pers}E_{persist}
+
\lambda_{osc}E_{force\_osc}.
$$

B 类的核心难点不是公式本身，而是 $p_i,n_i,f_i$ 是否作为生成变量或可微函数可获得。理论上，只要它们可表达为 $z$ 的函数，便可用

$$
\nabla_zE_B
=
\left(\frac{\partial (p,n,f)}{\partial z}\right)^\top
\nabla_{p,n,f}E_B
$$

注入 diffusion。

---

# C. 抓取质量与力封闭如何注入 Diffusion

C 类约束是最核心也最难的部分。它关注接触是否能抵抗任意外部扰动，也就是 grasp quality 和 force closure。

## C.1 抓取扳手矩阵

设物体质心为参考点，第 $i$ 个接触点相对质心的位置为

$$
r_i=p_i-p_{com}.
$$

接触力方向为 $d_{i\ell}$，例如由摩擦锥多面体近似得到第 $\ell$ 条锥边方向。该单位力产生的扳手为

$$
w_{i\ell}
=
\begin{bmatrix}
d_{i\ell}\\
r_i\times d_{i\ell}
\end{bmatrix}
\in\mathbb{R}^6.
$$

把所有 primitive wrench 作为列，得到 grasp wrench matrix：

$$
G=
\begin{bmatrix}
w_{11}&w_{12}&\cdots&w_{i\ell}&\cdots
\end{bmatrix}
\in\mathbb{R}^{6\times M}.
$$

如果接触力非负组合系数为 $\alpha\ge 0$，物体受到的合扳手是

$$
w=G\alpha.
$$

力封闭要求接触力锥的正组合可以抵消任意外部扰动。一个常见判据是：原点位于 primitive wrenches 的凸包内部。

## C.2 力封闭的 QP 残差能量

最适合 diffusion guidance 的方式，是将力封闭写成连续优化残差：

$$
E_{fc}(G)
=
\min_{\alpha}
\|G\alpha\|_2^2
$$

约束为

$$
\alpha\ge 0,\quad \mathbf{1}^\top\alpha=1.
$$

如果存在非零接触力组合使合扳手接近零，则 $E_{fc}$ 小；若无论如何组合都无法平衡，$E_{fc}$ 大。这个形式避免直接计算高维凸包，适合作为可微 proxy。

令最优解为 $\alpha^\star(G)$，则

$$
E_{fc}(G)=\|G\alpha^\star\|_2^2.
$$

若暂时忽略 $\alpha^\star$ 对 $G$ 的隐式依赖，根据 envelope theorem 可得近似梯度：

$$
\frac{\partial E_{fc}}{\partial G}
\approx
2G\alpha^\star(\alpha^\star)^\top.
$$

更严格地，若使用可微 QP solver，可以通过 KKT 条件对 $\alpha^\star(G)$ 做隐式微分。设 QP 写成标准形式

$$
\min_\alpha \frac{1}{2}\alpha^\top H\alpha
\quad
\text{s.t. } A_{eq}\alpha=b,\ \alpha\ge 0,
$$

其中

$$
H=2G^\top G.
$$

KKT 条件为

$$
\begin{bmatrix}
H & A_{eq}^\top & A_I^\top\\
A_{eq} & 0 & 0\\
A_I & 0 & 0
\end{bmatrix}
\begin{bmatrix}
d\alpha\\ d\nu\\ d\mu
\end{bmatrix}
=
-
\begin{bmatrix}
dH\,\alpha\\0\\0
\end{bmatrix},
$$

由此可精确得到 $d\alpha/dG$。这就是 GraspQP 类方法最适合作为 C 类约束注入 diffusion 的原因。

最终对生成变量 $z$ 的梯度为

$$
\nabla_zE_{fc}
=
\left(\frac{\partial G}{\partial z}\right)^\top
\nabla_GE_{fc}.
$$

其中 $G$ 又依赖接触点 $p_i(q)$、法向 $n_i(q)$、摩擦锥方向 $d_{i\ell}$ 等。

## C.3 最小奇异值约束

另一个简单 proxy 是让 $G$ 满秩且最弱方向不退化。设奇异值为

$$
\sigma_1\ge \sigma_2\ge \cdots \ge \sigma_6.
$$

定义

$$
E_{\sigma}
=
[\sigma_0-\sigma_{\min}(G)]_+^2.
$$

若 $\sigma_{\min}$ 太小，说明某些扳手方向难以产生。对非退化奇异值，若

$$
Gv_{\min}=\sigma_{\min}u_{\min},
$$

则

$$
\nabla_G\sigma_{\min}
=
u_{\min}v_{\min}^\top.
$$

因此当 $\sigma_{\min}<\sigma_0$ 时：

$$
\nabla_GE_{\sigma}
=
-2[\sigma_0-\sigma_{\min}]_+
u_{\min}v_{\min}^\top.
$$

负梯度会提高最小奇异值，使 grasp wrench matrix 在最弱方向上更强。但需要注意：满秩是力封闭的必要条件，不是充分条件；正组合和摩擦锥约束仍然需要 QP/LP 检查。

## C.4 Wrench space volume

可用

$$
E_{vol}
=
-\log\det(GG^\top+\varepsilon I)
$$

或

$$
E_{vol}
=
-\sum_{i=1}^{6}\log(\sigma_i+\varepsilon)
$$

鼓励 grasp wrench space 体积变大。梯度为

$$
\nabla_GE_{vol}
=
-2(GG^\top+\varepsilon I)^{-1}G.
$$

负梯度会扩大 $G$ 的有效张成空间，使抓取对多方向扰动更有抵抗力。

## C.5 Ferrari-Canny epsilon 的平滑替代

经典 Ferrari-Canny epsilon 指标表示原点周围能放入 grasp wrench space 的最大球半径。直接计算涉及凸包，通常不可微或代价高。可构造 soft 版本。对单位扰动方向 $u$，抗扰能力可写成

$$
m(u)=\max_j u^\top w_j.
$$

最坏方向：

$$
\epsilon=\min_{\|u\|=1}m(u).
$$

可用采样方向集合 $\mathcal{U}$ 和 softmax / softmin 近似：

$$
\tilde m(u)
=
\tau\log\sum_j\exp\left(\frac{u^\top w_j}{\tau}\right),
$$

$$
\tilde\epsilon
=
-\tau'\log\sum_{u\in\mathcal{U}}
\exp\left(-\frac{\tilde m(u)}{\tau'}\right).
$$

然后定义

$$
E_{\epsilon}
=
[\epsilon_0-\tilde\epsilon]_+^2.
$$

这个指标比 $E_\sigma$ 更贴近 Ferrari-Canny，但计算更重。

## C.6 任务导向力封闭

完整 6D 力封闭可能过强。若任务只要求抵抗某些方向扰动，例如抗重力提升，可定义任务扳手子空间投影矩阵

$$
S\in\mathbb{R}^{6\times d}.
$$

任务相关 wrench matrix 为

$$
G_T=S^\top G.
$$

然后在 $G_T$ 上定义 QP 残差：

$$
E_{taskFC}
=
\min_{\alpha\in\Delta}\|G_T\alpha\|_2^2.
$$

其中

$$
\Delta=\{\alpha:\alpha\ge 0,\mathbf{1}^\top\alpha=1\}.
$$

这适合 D 类任务导向抓取，例如只需抵抗竖直重力和主要旋转扰动。

## C 类总能量

$$
E_C
=
\lambda_{fc}E_{fc}
+
\lambda_{\sigma}E_{\sigma}
+
\lambda_{vol}E_{vol}
+
\lambda_{\epsilon}E_{\epsilon}
+
\lambda_T E_{taskFC}.
$$

C 类最重要的原则是：不要把“接触数量多”误当作“力封闭”。真正的力封闭需要检查接触扳手能否张成并平衡外部扰动。对 diffusion 来说，QP residual 是最值得优先采用的可微形式。

---

# D. 物体层与任务成功约束如何注入 Diffusion

D 类约束关注生成动作或抓取最终是否让物体完成任务。设物体状态轨迹为

$$
o_{0:H}=(p_{0:H},R_{0:H},v_{0:H},\omega_{0:H}).
$$

若 diffusion 直接生成物体轨迹，则 D 类约束直接对 $o$ 求梯度；若 diffusion 生成动作，则物体轨迹由动力学映射给出：

$$
o_{0:H}=F_o(a_{0:H-1},q_0,o_0).
$$

此时

$$
\nabla_aE_D
=
\left(\frac{\partial F_o}{\partial a}\right)^\top
\nabla_oE_D.
$$

理论上，D 类是最接近任务目标的约束；但它通常依赖动力学 rollout，因此数学上可写，实际可微性更难。

## D.1 物体提升高度

设初始高度为 $z_0$，最终高度为 $z_H$，希望提升至少 $h_{\min}$：

$$
z_H-z_0\ge h_{\min}.
$$

hinge penalty：

$$
E_{lift}
=
[h_{\min}-(z_H-z_0)]_+^2.
$$

若未达到提升高度，则

$$
\frac{\partial E_{lift}}{\partial z_H}
=
-2[h_{\min}-(z_H-z_0)]_+.
$$

guided score 的负梯度会推动生成结果提高最终物体高度。

## D.2 目标位姿误差

目标位置 $p^\star$，目标姿态 $R^\star$。位置误差：

$$
E_{pos}
=
\|p_H-p^\star\|_2^2.
$$

姿态误差可用李群测地距离：

$$
E_{rot}
=
\|\log((R^\star)^\top R_H)\|_2^2.
$$

综合：

$$
E_{goal}
=
\lambda_pE_{pos}
+
\lambda_RE_{rot}.
$$

这比直接用欧拉角差更严格，因为 $SO(3)$ 上的姿态误差应按旋转群测地线衡量。

## D.3 物体穿透与环境碰撞

若桌面高度为 $z_{table}$，物体所有表面点集合为 $\mathcal{V}_o$，某点世界坐标为 $x_v(o_t)$，则物体-桌面穿透为

$$
E_{table}
=
\sum_{t,v}
[z_{table}-e_z^\top x_v(o_t)]_+^2.
$$

手-物体穿透可用物体 SDF：

$$
E_{hand-obj}
=
\sum_{t,i}
[-\phi_o(p_i(q_t))]_+^2.
$$

这与 B 类非穿透相同，但 D 类更关注整个物体和环境层面的物理合理性。

## D.4 物体姿态稳定性

设物体局部竖直轴在世界坐标系中为

$$
u_t=R_te_z.
$$

与世界竖直方向夹角：

$$
\theta_t=\arccos(e_z^\top u_t).
$$

稳定性 penalty：

$$
E_{tilt}
=
\sum_t[\theta_t-\theta_{\max}]_+^2.
$$

也可惩罚晃动：

$$
E_{tilt-var}
=
\sum_t(\theta_t-\bar\theta)^2.
$$

其中 $\bar\theta$ 是稳定阶段平均倾角。该项鼓励物体在抓取后保持姿态稳定，而不是被手指夹得摇摆。

## D.5 物体速度平滑与冲击

物体线速度和角速度记为

$$
\xi_t=(v_t,\omega_t).
$$

速度平滑：

$$
E_{vel}
=
\sum_t\|\xi_{t+1}-\xi_t\|_2^2.
$$

jerk 形式：

$$
E_{jerk}
=
\sum_t\|\xi_{t+2}-2\xi_{t+1}+\xi_t\|_2^2.
$$

这类约束抑制冲击、弹飞、滑移导致的速度尖峰。其数学形式和 A 类动作平滑类似，只是对象从动作换成了物体状态。

## D.6 阶段进度约束

抓取通常分为 approach、close、lift、stabilize。可以为每个阶段定义应满足的物理不等式：

Approach 阶段：

$$
d_{hand,obj}(t)\downarrow,
\quad
\phi_o(p_i(q_t))\ge 0.
$$

Close 阶段：

$$
\text{contact count increases},
\quad
\|p_{obj,t}-p_{obj,0}\|\le \delta_{move}.
$$

Lift 阶段：

$$
z_{obj,t+1}-z_{obj,t}>0.
$$

可统一写为阶段 penalty：

$$
E_{phase}
=
\sum_s
\sum_{t\in\mathcal{T}_s}
\sum_k
[g_{s,k}(z_t)]_+^2.
$$

其中 $s$ 是阶段，$g_{s,k}$ 是该阶段不应违反的物理条件。阶段约束的意义是防止不同阶段的物理目标相互冲突，例如 approach 阶段不应强制接触力，close 阶段不应过早提升物体。

## D.7 抓取鲁棒性

鲁棒性可以定义为对扰动的最坏情况或期望性能。设扰动为 $\delta\in\mathcal{D}$，扰动后的物体轨迹为

$$
o^\delta_{0:H}=F_o^\delta(z).
$$

鲁棒 penalty 可以写成

$$
E_{robust}(z)
=
\mathbb{E}_{\delta\sim\mathcal{D}}
\left[
[d(o^\delta_H,o_H)-d_{\max}]_+^2
\right].
$$

更严格的 worst-case 形式：

$$
E_{robust}^{wc}(z)
=
\max_{\delta\in\mathcal{D}}
[d(o^\delta_H,o_H)-d_{\max}]_+^2.
$$

若直接对扰动 rollout 不可微，可以用 C 类 wrench margin 作为鲁棒性的解析代理：抓取可抵抗的最小扰动扳手越大，鲁棒性越高。

## D 类总能量

$$
E_D
=
\lambda_lE_{lift}
+
\lambda_gE_{goal}
+
\lambda_pE_{penetration}
+
\lambda_tE_{tilt}
+
\lambda_vE_{vel}
+
\lambda_{ph}E_{phase}
+
\lambda_rE_{robust}.
$$

D 类约束最适合作为任务级 posterior guidance：

$$
\tilde p(z|y,success)
\propto
p_{data}(z|y)
\exp[-E_D(z,y)].
$$

但若 $E_D$ 必须通过不可微仿真才能计算，则可以把 $E_D$ 作为离线标签训练 evaluator，再通过 classifier guidance 近似：

$$
\nabla_z\log p(success|z,y)
\approx
-\nabla_zE_D(z,y).
$$

---

# 5. 四类约束如何组合

最终可以定义完整物理能量：

$$
E_{phys}(z,y)
=
\lambda_AE_A(z,y)
+
\lambda_BE_B(z,y)
+
\lambda_CE_C(z,y)
+
\lambda_DE_D(z,y).
$$

对应目标分布：

$$
\tilde p(z|y)
=
\frac{1}{Z}
p_{data}(z|y)
\exp[-E_{phys}(z,y)].
$$

对应 guided score：

$$
s_{guided}(z_t,t,y)
=
s_\theta(z_t,t,y)
-
\eta_t\nabla_{z_t}E_{phys}(\hat z_0(z_t,t),y).
$$

如果希望更接近硬约束，可以把物理限制写成等式和不等式：

$$
h_j(z)=0,\quad g_i(z)\le 0.
$$

然后使用增广拉格朗日：

$$
\mathcal{L}_\rho(z,\lambda,\nu)
=
E_{task}(z)
+
\sum_i \lambda_i[g_i(z)]_+
+
\frac{\rho}{2}\sum_i[g_i(z)]_+^2
+
\sum_j \nu_jh_j(z)
+
\frac{\rho}{2}\sum_jh_j(z)^2.
$$

再用

$$
s_{guided}
=
s_\theta-\eta_t\nabla_z\mathcal{L}_\rho.
$$

这个形式比单纯 penalty 更严谨，因为它区分了软偏好、硬不等式约束和等式约束。对灵巧手而言，可以这样划分：

| 类别 | 适合作为硬约束 | 适合作为软约束 |
|---|---|---|
| A | 关节限位、动作饱和 | 平滑性、能量、root-finger 平衡 |
| B | 非穿透、摩擦锥、法向力非负 | 接触数量、接触对称、接触持续 |
| C | 力封闭 QP 残差阈值 | 最小奇异值、wrench volume、任务方向封闭 |
| D | 桌面穿透、目标安全区 | lift score、姿态稳定、速度平滑、鲁棒性 |

---

# 6. 最推荐的理论路线

如果你要写成研究方案，我建议不要从“训练一个物理 classifier”开始，而从以下更清晰的数学路线开始：

## 路线一：可微物理能量 guidance

对 A/B/C 中可微的项，直接构造

$$
E_{phys}(z)=E_A+E_B+E_C
$$

并在 diffusion sampling 中使用

$$
-\nabla E_{phys}.
$$

优先项：

1. $E_{smooth}$、$E_{energy}$、$E_{sat}$、$E_{joint}$；
2. $E_{pen}$、$E_{contact}$、$E_{fric}$；
3. $E_{fc}$、$E_\sigma$、$E_{vol}$。

## 路线二：任务级 posterior guidance

对 D 类任务成功项，定义

$$
E_D=E_{lift}+E_{goal}+E_{tilt}+E_{robust}.
$$

如果可微，则直接 guidance；如果不可微，则训练 evaluator：

$$
p_\psi(success|z,y)
$$

并使用

$$
\nabla_z\log p_\psi(success|z,y).
$$

## 路线三：约束分层

不要把所有约束混在一个大 loss 里。更合理的是分层：

```text
低层 A：先保证动作可执行
中层 B：再保证接触物理合理
核心 C：再保证抓取具备力封闭/抗扰动能力
高层 D：最后保证物体完成任务
```

数学上对应：

$$
E_{phys}
=
\lambda_A(t,s)E_A
+
\lambda_B(t,s)E_B
+
\lambda_C(t,s)E_C
+
\lambda_D(t,s)E_D,
$$

其中权重可以依赖 diffusion step $t$ 和任务阶段 $s$。例如：

- early denoising：几何/动作范围约束权重大；
- middle denoising：接触和摩擦约束权重大；
- late denoising：力封闭和任务成功约束权重大。

这不是网络技巧，而是因为不同物理约束在不同噪声水平下可解释性不同。高噪声时接触点和力封闭不可靠，低噪声时这些高阶物理量才有明确意义。

---

# 7. 总结

ABCD 四类约束可以统一到一个数学框架中：

$$
\boxed{
\tilde p(z|y)
\propto
p_{data}(z|y)
\exp[-E_A(z)-E_B(z)-E_C(z)-E_D(z)]
}
$$

对应的 diffusion guidance 为：

$$
\boxed{
s_{guided}
=
s_\theta
-
\nabla_z(E_A+E_B+E_C+E_D)
}
$$

其中：

- A 类主要是动作序列上的二次型、barrier、hinge penalty；
- B 类主要是接触几何、摩擦锥、非穿透、接触持续性；
- C 类主要是 grasp wrench matrix、force closure QP、奇异值和 wrench volume；
- D 类主要是物体提升、目标位姿、稳定性、穿透和扰动鲁棒性。

最重要的理论启发是：**物理约束注入 diffusion 的本质不是增加一个模糊的“物理网络”，而是改变目标分布的能量形状；只要能把约束写成 $E_{phys}$，就能通过 $-\nabla E_{phys}$ 改变 denoising 方向。**

