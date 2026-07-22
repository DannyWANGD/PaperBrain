# 概率证书引导的灵巧手稳健抓取 Diffusion：完整论文主线与数学框架

> 英文候选题目：**Certificate-Guided Chance-Constrained Diffusion for Robust Dexterous Grasping**  
> 方法简称候选：**C3G-Diffusion**（Chance-Constrained Certificate-Guided Diffusion）  
> 文稿定位：计算机科学方法论文构想，面向 CoRL、RSS、ICRA、NeurIPS/ICLR，后续可扩展至 T-RO/IJRR。  
> 核心判断：该主线以六条路线中的“方向三：可行性证书联合生成”为主体，以“方向一：概率收紧的力封闭去噪”为安全机制。二者通过同一个稳健可行性证书统一，而不是两个独立模块的拼接。

## 1. 先回答：它是哪条思路，是否具有足够的数学价值

建议主线不是六条路线中的某一条原样照搬，而是“3 为主、1 为核”的组合。方向三负责改变 diffusion 的生成对象：模型不再只生成手腕位姿与关节角，而是同时生成能够解释该抓取为何稳定的接触力 witness。方向一负责改变安全定义：证书不能只在一个精确、名义的摩擦系数和接触几何下成立，而应在摩擦、接触点和法向存在不确定性时，以至少 $1-\delta$ 的概率成立。

这个组合有足够的数学空间，也有顶会价值，但不是天然成立。若实现方式只是“diffusion 输出姿态和接触力，再加几个 loss”，贡献仍然偏弱。真正能支撑顶会的版本必须满足三点。第一，证书是第三方求解器能够复核的物理 witness，而不是网络自报的 confidence。第二，必须证明或清楚说明，有限个 witness 为什么能够代表一个连续外部扰动集合。第三，概率收紧必须与后验不确定度、可微 QP 和去噪更新形成统一推导，而不是手工把安全系数调大。

本文采用“扰动多面体顶点证书”解决第二点。设任务需要抵抗的外部 wrench 集合是一个凸多面体；若对每一个顶点 wrench 都能找到满足摩擦、执行器和静力平衡约束的接触力，那么由凸性可知，该多面体中的任意 wrench 都可由相应接触力的凸组合抵抗。这样，连续的稳健抓取性质被转化为有限组、可核验的接触力 witness。随后再对不确定参数下的证书裕度做 chance constraint，便得到一个既有物理意义、又能进入 diffusion 去噪的数学对象。

从论文定位看，这条路线介于三个成熟方向之间，但不等同于其中任何一个。[DexGrasp Anything](https://arxiv.org/abs/2503.08257) 已经把几何物理能量放入抓取 diffusion 的训练和采样；[GraspQP](https://arxiv.org/abs/2508.15002) 已经给出了严谨可微的力封闭 QP；[Constrained Diffusers](https://arxiv.org/abs/2506.12544) 已经给出通用投影、原始-对偶和增广拉格朗日受约束采样。本文的独立贡献必须是：将“任务扰动集的可行接触力证书”作为生成变量，并在感知与接触不确定性下，将该证书转化为 clean-sample denoising 中的概率安全约束。

### 1.1 全文理论只需要记住四步

为了避免后文公式掩盖主线，整套方法可以先压缩为四步。第一，任务扰动不是一个点，而是由有限顶点构成的凸集：

$$
\mathcal D=\operatorname{conv}\{w^{(1)},\ldots,w^{(K)}\}.
$$

第二，为每个顶点寻找合法接触力 $z^{(k)}$，使接触 wrench 抵消外部扰动：

$$
W(x,u)z^{(k)}+w^{(k)}=0,
\qquad z^{(k)}\in\mathcal Z(x,u).
$$

第三，把最坏顶点的平衡余量写成可微的保守标量 $g_{\mathrm{smooth}}$，并按参数不确定度收紧为

$$
m_\delta(x)=g_{\mathrm{smooth}}(x,\bar u)
-\Phi^{-1}(1-\delta)
\sqrt{\nabla_u g_{\mathrm{smooth}}^T\Sigma_u\nabla_u g_{\mathrm{smooth}}}.
$$

第四，当 diffusion 的原始更新会使 $m_\delta<0$ 时，只做刚好足以回到局部安全侧的最小修正。全文其他内容都只是在说明这四步为什么成立、怎样计算和怎样验证，不再另设平行理论主线。

## 2. 研究问题：现有抓取生成为什么缺少可信的安全含义

灵巧手 grasp diffusion 通常学习

$$
p_\theta(x\mid o),
$$

其中 $o$ 是点云、深度图或对象特征，$x=(T,q)$ 包含手腕位姿 $T\in SE(3)$ 与关节角 $q$。模型善于表达多模态抓取分布，但它生成的是“姿态候选”，不是“物理证明”。即使某个 $x$ 在训练数据中常见，仍无法直接回答：哪些接触力能够抵抗重力？摩擦系数降低后是否仍然稳定？所需接触力是否超过电机力矩限制？接触点偏移两毫米后，力封闭是否还成立？

现有 physics guidance 通常定义一个能量 $E_{\mathrm{phys}}(x,o)$，在反向扩散中加入

$$
-\lambda_k\nabla_x E_{\mathrm{phys}}(\hat x_0,o).
$$

这种做法存在三个结构性问题。首先，一个低能量标量不一定给出可解释的可行力分配。其次，固定权重 $\lambda_k$ 很难处理碰撞、接触、力封闭和力矩约束之间的冲突。最后，绝大多数能量使用估计几何与固定摩擦系数计算，得到的是 nominal feasibility，而不是真实系统所需要的 robust feasibility。

因此本文要解决的问题可以表述为：给定不完整对象观测 $o$ 和任务扰动描述 $\mathcal D$，学习一个条件生成模型，同时生成多样抓取 $x$ 与物理证书 $c$；证书应能由显式接触力学约束核验，并使生成抓取在不确定接触参数 $u$ 下，以高概率抵抗 $\mathcal D$ 中的全部扰动。

## 3. 建模对象：抓取、接触力证书与不确定参数

### 3.1 抓取变量

令

$$
x=(T,q),
$$

其中 $T$ 是手腕相对物体的位姿，$q\in\mathbb R^{n_q}$ 是关节角。第一版不生成离散接触模式，而是由前向运动学和手物距离确定候选接触。这样可以把研究重点放在“给定候选接触，怎样生成并验证抗扰接触力”，避免同时引入组合接触搜索。

关节限位、非穿透与自碰撞记为

$$
h_{\mathrm{kin}}(x)\ge 0.
$$

这里的 $h_{\mathrm{kin}}$ 可以是多个标量约束的集合。为避免符号混乱，全文统一采用“$h\ge 0$ 表示安全”。

### 3.2 不确定参数

令

$$
u=(\mu,\Delta p,\Delta n),
$$

分别表示摩擦系数、接触点误差与接触法向误差。物体位姿误差可先传播为 $\Delta p$ 和 $\Delta n$，不再单独增加随机变量。感知网络或离线标定模块给出后验

$$
q_\psi(u\mid o).
$$

第一版采用局部高斯近似。接触点和法向误差均在各自的局部坐标中参数化，从而避免直接对单位法向量使用无约束高斯。重要的是，不确定度不能只是网络输出一个未经校准的方差；它需要通过仿真扰动和真实标定数据校准，否则后续概率解释没有可信基础。多峰后验属于后续扩展，不进入主理论。

这里写成 $q_\psi(u\mid o)$ 并不意味着第一版必须从单张图像准确识别摩擦系数。更可行的实现是：接触位置和法向误差由点云重建误差统计得到，摩擦系数使用材质类别的校准区间，或直接使用覆盖目标场景的保守先验。只有当这些分布在独立数据上表现出合理覆盖率时，才把它们代入 chance constraint。换句话说，概率证书依赖的是“可校准的不确定度模型”，而不是必须依赖一个复杂的端到端后验网络。

### 3.3 接触 wrench 表示

设抓取形成 $N_c$ 个接触。对第 $i$ 个接触，用多面体内近似表示 Coulomb 摩擦锥：

$$
f_i=\sum_{r=1}^{R}\alpha_{ir}d_{ir}(x,u),
\qquad \alpha_{ir}\ge 0.
$$

$d_{ir}$ 是第 $i$ 个接触局部摩擦锥的第 $r$ 条生成射线。将所有系数堆叠为 $z\in\mathbb R^{N_cR}$，将每条射线映射到物体坐标系中的六维 wrench，可得 grasp wrench matrix

$$
W(x,u)=
\begin{bmatrix}
d_1 & \cdots & d_M\\
p_1\times d_1 & \cdots & p_M\times d_M
\end{bmatrix},
$$

其中 $M=N_cR$。于是接触对物体施加的合 wrench 为 $W(x,u)z$。

为了避免无限增大接触力，加入

$$
0\le z\le \bar z.
$$

若需要考虑电机可执行性，可将接触力通过接触 Jacobian 映射到关节力矩：

$$
\tau=J_c(x)^T D(x,u)z,
\qquad
\tau_{\min}\le \tau\le\tau_{\max},
$$

其中 $D$ 把锥系数还原为各接触的三维力。这样，证书不仅说明“数学上存在接触力”，还说明所需接触力在执行器能力范围内。

## 4. 关键数学巧思：用有限顶点 witness 证明连续扰动集可抵抗

### 4.1 任务扰动多面体

这里的“扰动”不是一个抽象分数，而是物体受到的外部 wrench。一个 wrench 同时包含三个方向的力和三个方向的力矩：

$$
w=(F_x,F_y,F_z,M_x,M_y,M_z)\in\mathbb R^6.
$$

因此，“一个扰动点”表示一种确定工况，例如“向右推 3 N，同时绕竖直轴扭转 0.2 N·m”。真实任务不会只出现这一种工况。提杯时，物体可能同时受到重力、手臂加减速造成的惯性力以及轻微倾覆力矩；旋拧工具时，轴向扭矩和侧向力也会在一定范围内变化。本文用集合 $\mathcal D$ 表示任务中希望抓取能够承受的全部外部 wrench。

先看一维例子。若只考虑左右推力，并希望抓取承受 $[-4,4]$ N 内的任意推力，那么这个区间的两个端点 $-4$ N 和 $+4$ N 就是顶点。二维时，若横向力和纵向力组成一个矩形，顶点就是矩形的四个角。六维 wrench 空间无法直接画出来，但定义完全相同：顶点是扰动集合的极端工况，而不是物体网格或点云上的几何顶点。

本文把任务扰动集合写成有限顶点的凸包：

$$
\mathcal D=\operatorname{conv}\{w^{(1)},\ldots,w^{(K)}\},
$$

其中 $\operatorname{conv}$ 表示凸包，即所有顶点凸组合形成的集合。展开写就是

$$
\mathcal D=
\left\{
\sum_{k=1}^{K}\beta_k w^{(k)}:
\beta_k\ge0,\ \sum_{k=1}^{K}\beta_k=1
\right\}.
$$

“凸组合”可以理解为在若干极端工况之间做非负加权平均。因此，由四个角构成的矩形不仅包含四个角，也包含边和内部所有点。所谓“有限顶点代表连续扰动集合”，并不是说现实只有有限种扰动，而是用有限个边界工况定义一个内部含有无限多个点的连续安全范围。

顶点必须由任务物理范围构造，不能随意选取。提杯任务可以根据质量区间、最大手臂加速度和允许的倾覆力矩确定极端组合；旋拧任务则根据最大正负轴向扭矩及侧向载荷确定顶点。若仅取六维坐标轴的十二个正负端点，得到的是一个六维 cross-polytope，只覆盖其凸包，并不等于覆盖每个分量都能同时达到上界的六维 box。论文必须明确自己认证的是哪一个 $\mathcal D$，不能把稀疏方向测试夸大为任意扰动保证。

传统 force closure 通常要求能够抵抗原点附近所有方向的小扰动。本文的定义更一般：若 $\mathcal D$ 包含原点的一个全维邻域，它可以作为有限分辨率的 force-closure 检验；若 $\mathcal D$ 只覆盖某项任务的主要载荷方向，它证明的是 task-oriented wrench resistance，而不是完整的全方向 force closure。

对每个顶点 $w^{(k)}$，定义接触力 witness $z^{(k)}$，要求

$$
W(x,u)z^{(k)}+w^{(k)}=0,
$$

并满足相同的摩擦、接触力上界和关节力矩约束。完整证书为

$$
c=Z=\{z^{(1)},\ldots,z^{(K)}\}.
$$

这里采用符号约定：$w^{(k)}$ 是外界施加给物体的 wrench，$Wz^{(k)}$ 是手指接触力施加给物体的 wrench。二者相加为零，表示准静态平衡。$z^{(k)}$ 不是一个“稳定概率”，而是一组可以代入上述方程、摩擦锥和力矩限制逐项检查的具体接触力系数。

### 4.2 顶点充分性命题

**命题 1：凸扰动集的顶点 witness 充分性。** 固定抓取 $x$ 与物理参数 $u$。若可行接触力系数集合

$$
\mathcal Z(x,u)=\{z:A(x,u)z\le b(x,u)\}
$$

是凸集，并且对 $\mathcal D$ 的每个顶点 $w^{(k)}$ 都存在 $z^{(k)}\in\mathcal Z(x,u)$ 使

$$
W(x,u)z^{(k)}+w^{(k)}=0,
$$

则对任意 $w\in\mathcal D$，均存在 $z\in\mathcal Z(x,u)$ 使 $W(x,u)z+w=0$。

证明很直接。任意 $w\in\mathcal D$ 可写成

$$
w=\sum_{k=1}^{K}\beta_k w^{(k)},
\qquad \beta_k\ge0,\quad \sum_k\beta_k=1.
$$

取

$$
z=\sum_{k=1}^{K}\beta_k z^{(k)}.
$$

由于 $\mathcal Z$ 为凸集，$z\in\mathcal Z$；同时

$$
W(x,u)z+w
=\sum_k\beta_k\left(W(x,u)z^{(k)}+w^{(k)}\right)=0.
$$

命题得证。

这个命题是整篇论文最重要的逻辑支点。它把“对连续扰动集都稳定”转化为“生成并核验有限个顶点接触力”。但适用边界必须写清：它依赖固定接触模式、线性 grasp map、凸摩擦锥近似以及准静态平衡。若接触模式随扰动改变、考虑大变形或动态冲击，命题不再直接成立。

## 5. 可微证书求解器：用一个小型 QP 计算 witness

### 5.1 顶点 QP

理想证书要求精确满足平衡方程，但对一个不好的候选抓取，可能根本不存在合法接触力。为了连续地衡量“离可行还差多远”，对每个顶点 $w^{(k)}$ 求解一个小型凸 QP：

$$
z_k^*(x,u)=\arg\min_z
\frac12\|S(W(x,u)z+w^{(k)})\|_2^2
+\frac{\varepsilon_z}{2}\|z\|_2^2,
$$

约束为

$$
A(x,u)z\le b(x,u).
$$

$A(x,u)z\le b(x,u)$ 汇总 $0\le z\le\bar z$、关节力矩上下界及其他线性可执行约束。矩阵 $S$ 是 wrench 归一化矩阵，例如用参考力 $F_{\mathrm{ref}}$ 归一化前三个力分量，用参考力矩 $M_{\mathrm{ref}}$ 归一化后三个力矩分量。这个步骤不可省略，因为牛顿和牛顿米量纲不同，直接做六维欧氏范数会让残差权重没有明确物理意义。

QP 的第一项寻找最能抵消当前外部扰动的接触力，第二项只使用很小的 $\varepsilon_z>0$ 来避免解不唯一并改善数值稳定性。由于正则项会轻微偏向较小的力，是否通过证书最终必须根据平衡残差和显式约束判断，而不能直接根据总 QP objective 判断。最终复核时还应将求得的 $z_k^*$ 重新代入原始、未归一化的力和力矩方程，分别报告物理单位下的误差。

定义每个顶点的无量纲平方平衡残差

$$
r_k(x,u)=
\left\|S\left(W(x,u)z_k^*(x,u)+w^{(k)}\right)\right\|_2^2.
$$

如果 $r_k=0$，说明该顶点在模型和数值精度下可以完全平衡；$r_k$ 越大，说明当前抓取越难抵抗该工况。于是“最坏顶点”定义为残差最大的顶点，而不一定是外力数值最大的顶点：

$$
r_{\max}(x,u)=\max_k r_k(x,u)
$$

例如，一个很大的竖直重力可能恰好沿抓取最擅长的方向，残差很小；另一个较小的侧向扭矩可能落在 grasp wrench space 的薄弱方向，反而成为最坏顶点。精确证书裕度定义为

$$
g_{\mathrm{cert}}(x,u)
=\epsilon_{\mathrm{bal}}^2-r_{\max}(x,u).
$$

$g_{\mathrm{cert}}\ge0$ 是最终复核使用的判据。由于最大值在最坏顶点发生切换时不可微，为去噪提供梯度时，用 log-sum-exp 构造 $r_{\max}$ 的光滑上界：

$$
\tilde r_\beta(x,u)=
\frac1\beta\log\sum_{k=1}^{K}\exp(\beta r_k(x,u)).
$$

因为 log-sum-exp 不小于真正的最大值，可定义光滑裕度

$$
g_{\mathrm{smooth}}(x,u)
=\epsilon_{\mathrm{bal}}^2-\tilde r_\beta(x,u)
\le g_{\mathrm{cert}}(x,u).
$$

$\epsilon_{\mathrm{bal}}$ 是允许的无量纲平衡误差阈值。$g_{\mathrm{cert}}>0$ 表示最坏顶点的残差仍低于阈值，且数值越大，安全余量越充足；$g_{\mathrm{cert}}=0$ 表示恰好位于认证边界；$g_{\mathrm{cert}}<0$ 表示至少有一个顶点无法在允许误差内被平衡。训练和去噪使用更保守且可微的 $g_{\mathrm{smooth}}$，最终认证使用精确的 $g_{\mathrm{cert}}$，二者不能混为同一个结论。

一个简单数值例子可以帮助理解。假设三个顶点的平方残差分别为 $0.01,0.04,0.09$，允许阈值为 $\epsilon_{\mathrm{bal}}^2=0.10$。忽略光滑近似的微小差别，最坏残差为 $0.09$，证书裕度约为 $0.10-0.09=0.01$。这个抓取虽然通过，但非常靠近边界；若最坏残差升到 $0.12$，裕度变为 $-0.02$，证书失败。

### 5.2 为什么该裕度可以用于去噪

由于目标函数是强凸二次函数，QP 在可行时具有唯一最优解。在约束激活集合不发生变化的局部区域，$z_k^*$ 对抓取 $x$ 和参数 $u$ 可微，因此可以通过标准可微 QP 求解器或隐式微分得到

$$
\nabla_x g_{\mathrm{smooth}}
\quad\text{和}\quad
\nabla_u g_{\mathrm{smooth}}.
$$

前者告诉去噪器“怎样改变手姿态可以提高抗扰能力”，后者衡量证书对摩擦和接触误差有多敏感。约束激活集合切换时，该映射通常只是分段光滑，因此本文只使用局部梯度，不声称其处处可微，也不生成任何额外的优化变量。

## 6. 概率安全：从名义证书到 chance-constrained certificate

### 6.1 概率约束

上一节的光滑裕度 $g_{\mathrm{smooth}}(x,u)$ 仍依赖物理参数 $u$。如果只把估计均值 $\bar u$ 代进去，我们只能得到“在名义摩擦和名义接触位置下是否通过”。现实中，同一个抓取在 $\mu=0.6$ 时可能稳定，在 $\mu=0.4$ 时却会滑动。因此去噪阶段的概率目标不是简单要求

$$
g_{\mathrm{smooth}}(x,\bar u)\ge0,
$$

而是

$$
\Pr_{u\sim q_\psi(u\mid o)}
\left[g_{\mathrm{smooth}}(x,u)\ge0\right]
\ge1-\delta.
$$

其中 $\delta$ 是允许的证书失败概率。例如 $\delta=0.05$ 表示希望在所建模的参数不确定性下，至少有 $95\%$ 的概率满足证书。这里的概率只针对 $q_\psi(u\mid o)$ 所描述的摩擦和接触误差，不自动覆盖未建模的柔性、冲击或传感器故障。

直接计算该概率通常很贵。若在 $\bar u$ 附近采用一阶近似

$$
g_{\mathrm{smooth}}(x,u)
\approx g_{\mathrm{smooth}}(x,\bar u)
+a(x)^T(u-\bar u),
$$

其中

$$
a(x)=\nabla_u g_{\mathrm{smooth}}(x,\bar u),
$$

且 $u\sim\mathcal N(\bar u,\Sigma_u)$，则线性化后的 $g$ 为一维高斯变量。其确定性等价收紧为

$$
m_\delta(x)=
g_{\mathrm{smooth}}(x,\bar u)
-\Phi^{-1}(1-\delta)
\sqrt{a(x)^T\Sigma_u a(x)}
\ge0.
$$

$\Phi^{-1}$ 是标准正态分布分位数。这个公式给出一个清楚的解释：名义证书裕度必须大于“不确定度沿最危险物理方向投影后的标准差”乘以风险系数。

更直观地说，先定义

$$
\sigma_g(x)=\sqrt{a(x)^T\Sigma_u a(x)}.
$$

$\sigma_g$ 不是全部参数方差的简单相加，而是“这些参数误差最终会让证书裕度波动多少”。如果摩擦估计很不确定，但当前抓取对摩擦不敏感，$\sigma_g$ 仍可能较小；反之，接触位置误差虽然数值很小，但若恰好显著改变力臂，$\sigma_g$ 可能很大。

所谓“收紧”，就是把原来的通过条件

$$
g_{\mathrm{smooth}}(x,\bar u)\ge0
$$

改成更严格的条件

$$
g_{\mathrm{smooth}}(x,\bar u)
\ge \Phi^{-1}(1-\delta)\sigma_g(x).
$$

右侧就是根据目标风险和当前不确定度自动形成的安全缓冲区。它不是统一给所有抓取乘一个经验系数：观测越不确定、抓取越敏感或目标失败概率越低，需要留下的缓冲越大。

例如，某个抓取的名义裕度为 $0.12$，估计得到 $\sigma_g=0.04$。若 $\delta=0.05$，则 $\Phi^{-1}(0.95)\approx1.645$，收紧后的裕度约为

$$
m_{0.05}=0.12-1.645\times0.04\approx0.054>0.
$$

它仍然通过。另一个抓取的名义裕度为 $0.08$，但 $\sigma_g=0.06$，则

$$
m_{0.05}=0.08-1.645\times0.06\approx-0.019<0.
$$

第二个抓取在平均参数下看似可行，却对参数误差太敏感，所以概率证书拒绝它。这就是“把最坏顶点的平衡余量按参数不确定度收紧”的完整含义：先找当前抓取最薄弱的外部扰动方向，再判断该薄弱余量能否覆盖摩擦和接触估计造成的波动。

### 6.2 概率公式的适用边界

上述确定性收紧对“一阶线性化后的证书裕度”和“局部高斯参数误差”是准确的；对原始非线性接触模型，它是局部近似而不是全局概率保证。因此实验必须检查目标风险 $\delta$ 与实际违规率是否一致。若验证集显示系统性低估风险，可增加一个由独立校准集确定的固定余量 $\rho_{\mathrm{cal}}$：

$$
m_{\mathrm{safe}}(x)=m_\delta(x)-\rho_{\mathrm{cal}}.
$$

论文的理论承诺限定为：在局部线性高斯假设下得到可解释的 chance constraint；在真实非线性系统中，通过独立校准和压力测试验证它是否可靠。非穿透、关节限位和自碰撞继续作为确定性约束处理，不与概率证书混在一起。

## 7. Diffusion 如何联合生成抓取与证书

### 7.1 联合随机变量

定义生成变量

$$
y=(x,Z),
$$

其中 $Z\in\mathbb R^{K\times M}$ 包含 $K$ 个扰动顶点对应的接触力系数。若不同抓取的接触数变化，可固定每根手指若干摩擦锥射线，并使用 contact mask；也可以把 $Z$ 编码到低维 latent certificate 中，再由结构化 decoder 恢复。

模型学习

$$
p_\theta(x,Z\mid o,\mathcal D).
$$

联合生成的意义不是替代 QP 求解器，而是让模型学习抓取姿态与可行力分配之间的统计耦合。推理时，预测的 $Z$ 提供 warm start；精确 QP 负责最终复核。一个成功的模型应同时提高证书通过率并减少精确求解器的修正步数。

### 7.2 训练数据构造

对每个训练抓取 $x_0$，首先根据对象、任务和手型建立候选接触，再对所有 $w^{(k)}$ 离线求解顶点 QP，得到 $Z_0$ 和平衡残差。数据构造时应同时保留具有较大安全裕度的正样本、接近边界的 hard samples，以及因摩擦、力矩或平衡失败的负样本；下一段会区分它们各自的用途。

更准确地说，联合 diffusion 只使用已经通过证书或接近证书边界的样本学习 $p(x,Z)$；失败样本不应作为要生成的目标，可仅用于训练可选的快速 certificate proxy。由于给定姿态后的 QP 是凸问题，力分配本身不会因为随机初始化产生不同抓取模式。真正需要保证多样性的是姿态数据 $x_0$：训练集应按 power、pinch、tripod 等抓取类型和接触组合分层采样，避免可认证数据被 power grasp 主导。

### 7.3 基础去噪损失

以 DDPM 为例，对标准化后的 $y_0=(x_0,Z_0)$ 加噪：

$$
y_t=\sqrt{\bar\alpha_t}y_0
+\sqrt{1-\bar\alpha_t}\epsilon,
\qquad \epsilon\sim\mathcal N(0,I).
$$

基础损失为

$$
\mathcal L_{\mathrm{diff}}
=\mathbb E\|\epsilon-\epsilon_\theta(y_t,o,\mathcal D,t)\|^2.
$$

由于位姿、关节角和接触力系数量纲不同，应分别白化或使用 block-wise noise schedule。不能直接让同一个欧氏尺度同时处理旋转、平移、关节角和牛顿量级的力。旋转可采用连续 6D 表示、Lie algebra 局部增量或与现有 backbone 一致的表示。

### 7.4 clean-sample 证书一致性

由网络预测 clean sample

$$
\hat y_0=(\hat x_0,\hat Z_0).
$$

只在 $\hat y_0$ 上计算物理量，因为 noisy $y_t$ 不对应真实接触几何。证书一致性损失可写为

$$
\mathcal L_{\mathrm{wit}}
=\frac1K\sum_{k=1}^{K}
\|W(\hat x_0,\bar u)\hat z_0^{(k)}+w^{(k)}\|^2,
$$

再加可行性 penalty

$$
\mathcal L_{\mathrm{feas}}
=\frac1K\sum_{k=1}^{K}
\left\|[A(\hat x_0,\bar u)\hat z_0^{(k)}-b(\hat x_0,\bar u)]_+\right\|^2.
$$

证书损失在训练初期不应权重过大，否则模型会忽略数据分布并坍缩到少数容易满足的 power grasp。一个合理的时间权重是让物理监督在低噪声阶段更强：

$$
\lambda_{\mathrm{phys}}(t)
=\lambda_{\max}\,\mathrm{SNR}(t)^\gamma
$$

并做截断，避免接近 $t=0$ 时数值爆炸。直觉是：早期样本仍接近随机姿态，精确接触力学意义有限；后期 clean estimate 已接近对象表面，证书约束才应主导局部修正。

## 8. 推理算法：概率约束下的最小干预去噪

### 8.1 先验更新与安全过滤

每个反向步中，diffusion 先给出一个未约束的干净抓取估计 $\hat x_0$。本文不直接给 score 叠加一个固定权重的大梯度，而是检查 $\hat x_0$ 的概率证书裕度 $m_{\mathrm{safe}}(\hat x_0)$。若裕度非负，说明当前估计已经位于局部安全侧，保持原样；若裕度为负，则寻找距离 $\hat x_0$ 最近的局部安全姿态 $x_0^{\mathrm{safe}}$：

$$
x_0^{\mathrm{safe}}
=\arg\min_{x'}\frac12\|x'-\hat x_0\|_M^2,
$$

满足证书裕度在 $\hat x_0$ 附近的一阶安全条件

$$
m_{\mathrm{safe}}(\hat x_0)
+\nabla_x m_{\mathrm{safe}}(\hat x_0)^T
(x'-\hat x_0)\ge0.
$$

$M$ 是姿态空间的度量矩阵，用于平衡平移、旋转和关节角的尺度。第一版可在标准化坐标中取 $M=I$。这个投影只修改抓取姿态 $x$，不直接投影网络预测的 $Z$；姿态改变后，使用预测 $Z$ 作为 warm start 重新求一次顶点 QP，得到与新姿态一致的 witness。这样不会把旧接触几何下的接触力错误地当成新姿态的证书。

### 8.2 单约束的闭式解释

为了看清算法含义，令 $M=I$。如果 $m_{\mathrm{safe}}(\hat x_0)\ge0$，则

$$
x_0^{\mathrm{safe}}=\hat x_0.
$$

如果 $m_{\mathrm{safe}}(\hat x_0)<0$，最小投影具有闭式形式

$$
x_0^{\mathrm{safe}}
=\hat x_0
+\frac{-m_{\mathrm{safe}}(\hat x_0)}
{\|\nabla_x m_{\mathrm{safe}}(\hat x_0)\|^2+\varepsilon_p}
\nabla_x m_{\mathrm{safe}}(\hat x_0).
$$

$\varepsilon_p$ 只是防止梯度范数过小时除零的数值项。该公式表示沿着“证书裕度增长最快”的方向移动刚好足够的距离，到达线性化边界。修正强度由当前违反量 $-m_{\mathrm{safe}}$ 自动决定，不是人工指定固定 guidance 权重。由于原始约束是非线性的，实际实现还应限制最大修正步长，并在修正后重新计算真实 margin；必要时做少量迭代，而不能把一次线性投影视为全局安全投影。

### 8.3 从 clean estimate 返回 noisy state

物理投影作用在 $\hat x_0$，但反向扩散状态仍是联合变量 $y_t=(x_t,Z_t)$。实现时只替换 clean estimate 中的姿态块，证书块由重新求解的 $Z^{\mathrm{safe}}$ 更新，得到

$$
y_0^{\mathrm{safe}}=(x_0^{\mathrm{safe}},Z^{\mathrm{safe}}).
$$

然后用与 backbone 参数化一致的映射，把 $y_0^{\mathrm{safe}}$ 重新转换为噪声预测或 posterior mean。例如 epsilon prediction 下，修正噪声为

$$
\epsilon^{\mathrm{safe}}
=\frac{y_t-\sqrt{\bar\alpha_t}y_0^{\mathrm{safe}}}
{\sqrt{1-\bar\alpha_t}}.
$$

随后使用标准 scheduler 得到 $y_{t-1}$。这样无需改变预训练 backbone，只在采样器中加入证书过滤器。

### 8.4 计算预算控制

每一步都求完整 $K$ 个 QP 会很慢。建议采用三级计算结构。早期用学习到的 certificate proxy；中期只对最危险的 top-$L$ 个扰动顶点调用精确 QP；末期对全部顶点复核。若 proxy 的不确定度高或 margin 接近零，则提前触发精确 oracle。最终输出必须经过全顶点 QP、精确碰撞和力矩检查，才能被标记为“certified candidate”。

## 9. 算法流程

### 9.1 离线阶段

1. 从 DexGraspNet、DexGrasp Anything 数据或自建仿真数据获得多样抓取姿态。
2. 为每个对象与任务构造扰动多面体 $\mathcal D$。
3. 在多种摩擦、位姿和接触误差下计算接触几何与 grasp wrench matrix。
4. 对每个扰动顶点求解带摩擦和力矩约束的 QP，保存接触力 witness 与平衡残差。
5. 训练不确定度后验 $q_\psi(u\mid o)$ 并在 held-out perturbations 上校准。
6. 训练联合 grasp-certificate diffusion；可先冻结 grasp backbone，只学习 certificate head，再联合微调。

### 9.2 在线采样阶段

1. 输入对象观测 $o$ 与任务扰动集 $\mathcal D$，估计 $q_\psi(u\mid o)$。
2. 从噪声初始化 $y_T=(x_T,Z_T)$。
3. 每个反向步预测 $\hat y_0$，计算名义证书裕度与不确定度收紧量。
4. 若先验更新将违反线性化安全条件，求解最小干预 QP；否则保留原始更新。
5. 将安全 clean estimate 映射回 scheduler 所需参数，得到 $y_{t-1}$。
6. 最后用精确顶点 QP、碰撞检测和力矩约束复核，并按 robust margin、diversity 与任务代价排序。

## 10. 可以建立的理论结果，以及不能过度声称的内容

### 10.1 可建立的结果

第一项是前述顶点 witness 充分性。它是一个精确的凸性结论，不依赖 diffusion，能说明证书为什么有物理意义。

第二项是线性高斯近似下 chance constraint 的确定性等价。若 $g$ 对 $u$ 一阶线性且 $u$ 为高斯，则

$$
g(x,\bar u)-\Phi^{-1}(1-\delta)
\sqrt{\nabla_u g^T\Sigma_u\nabla_u g}\ge0
$$

与线性化模型下的单约束概率条件等价。对原始非线性模型，使用独立验证集检查并校准实际违规率。

第三项是最小干预性质。局部安全 QP 的解在所用 metric 下，是满足线性化约束的更新中距离 diffusion prior 最近者。因此它比固定 guidance 更有明确的“保留生成先验”解释。

第四项可研究采样阶段的局部可行性保持：若当前 clean estimate 有正 margin，梯度 Lipschitz，线性化误差有界，且每步 trust region 足够小，则投影后下一 clean estimate 仍满足收紧后的局部约束。该结果只能称为 local invariance 或 one-step feasibility，不应写成整个真实机器人系统的全局安全保证。

### 10.2 不能过度声称

不能声称严格覆盖真实 Coulomb 接触，除非使用精确二阶锥且接触模型成立。摩擦锥多面体内近似可以给保守性，但真实摩擦仍可能时变。不能把准静态 wrench balance 等同于动态抓取成功；高速碰撞、柔性变形和控制延迟不在基本证书内。不能把高斯 posterior 下的一阶 chance constraint 写成任意分布下的严格保证。不能声称联合生成的 witness 本身就是证书，只有通过显式约束复核的 witness 才是 certificate。

## 11. 为什么这不是已有工作的简单组合

与 DexGrasp Anything 相比，本文不是用表面吸引和穿透排斥改善姿态，而是生成可抵抗任务扰动集合的接触力 witness，并对 witness 的可靠性做概率收紧。与 DexDiffuser 相比，本文不依赖黑盒 success evaluator，而是使用可分解、可核验的摩擦、平衡和力矩条件。

与 GraspQP 相比，两者都可使用可微 QP，但研究对象不同。GraspQP 主要从候选姿态出发，用内层 QP 定义严谨的 force-closure energy 并优化抓取；本文学习 $p(x,Z\mid o,\mathcal D)$，把任务扰动顶点对应的 witness 作为生成分布的一部分，并研究其在不确定参数下的概率有效性。GraspQP 是本文最重要的物理基础和强 baseline，论文中必须承认其贡献。

与 Constrained Diffusers 相比，本文不把约束写成任意 $g(x)\le0$ 后直接套通用算法，而是提出灵巧抓取特有的有限顶点 witness、可核验 QP 和 uncertainty tightening。通用 constrained sampling 是算法工具，证书结构才是领域创新。

与 2026 年的 EFF-Grasp、NDPP-Grasp 和 optimization-guided diffusion 相比，本文不把卖点放在“能量进入去噪”“不可微约束进入去噪”或“优化替代采样扰动”。真正差异是 certificate-carrying generation 与 calibrated chance constraint。投稿前仍须再次检索 2026 年下半年是否出现直接的 certificate-generating grasp diffusion。

## 12. 实验设计：每一组实验应证明什么

### 12.1 研究问题

实验应围绕五个问题组织，而不是只报一个平均成功率。

**RQ1：联合生成证书是否比姿态生成后再求解更容易得到可行抓取？** 比较仅生成 $x$、生成 $x$ 后 GraspQP refinement，以及联合生成 $(x,Z)$。报告精确 QP 通过率、平均残差、求解迭代数和推理时间。

**RQ2：概率收紧是否真的降低不确定性下的尾部失败？** 系统扫描摩擦系数、物体位姿误差、接触点与法向误差。比较 nominal certificate、固定 heuristic margin、delta-method margin、校准 margin。报告 violation rate、CVaR、最坏 5% 成功率及目标 $\delta$ 与实际违规率的 reliability diagram。

**RQ3：最小干预是否比固定能量 guidance 更好地保留多样性？** 在相同安全通过率下比较 unique contact modes、joint-space coverage、precision/power grasp 比例和 pairwise diversity。若方法只产生强力包覆抓取，就没有解决灵巧手生成的核心价值。

**RQ4：任务扰动多面体是否带来任务相关抓取？** 对同一对象设置提起、倾倒、旋拧和交接等不同 $\mathcal D$，检查接触布局、力分配、关节力矩和任务成功是否随任务变化。

**RQ5：证书是否能预测真实机器人上的失败？** 将预测 robust margin 与真实滑落、峰值触觉比、扰动恢复和关节力矩进行相关性与校准分析。证书不仅要提高成功率，还应成为有用的 failure predictor。

### 12.2 Baseline

基础生成 baseline 包括 vanilla grasp diffusion、DexDiffuser 式 evaluator guidance、DexGrasp Anything 式物理能量。约束 baseline 包括 fixed penalty guidance、projected diffusion、primal-dual constrained diffusion 和 augmented Lagrangian sampling。物理优化 baseline 包括生成后 GraspQP refinement、只用名义 GraspQP energy 的 denoising，以及最终仿真筛选。若代码可用，还应加入 EFF-Grasp、NDPP-Grasp 和 2026 optimization-guided diffusion。

所有 baseline 必须使用相同 backbone、数据、候选数和最终物理 oracle 预算，防止本文因调用更多 QP 或仿真而不公平获益。对 wall-clock 和 oracle calls 的匹配尤其重要。

### 12.3 数据、手型与扰动

第一阶段可在 ShadowHand 或 Allegro Hand 上使用 DexGraspNet 对象和公开抓取数据；第二阶段至少增加一种不同自由度手型，证明证书表示不是只适配单一手。对象划分要按实例而不是抓取随机划分，避免同一对象泄漏。最好增加几何 OOD、材质 OOD 与质量 OOD 三类测试。

扰动集应可解释。各向同性实验可用六维 wrench 球的对称多面体近似；任务实验使用由质量、加速度和工具作用力构造的 polytope。随机化参数至少包括 $\mu$、对象质量、质心、物体位姿、点云遮挡和控制延迟。训练分布与 OOD 分布要明确分开。

### 12.4 指标

物理指标包括全顶点平衡残差、摩擦锥违反、力矩违反、碰撞与穿透、robust margin。风险指标包括均值成功率、worst-quantile success、CVaR、实际 violation rate 与 calibration error。生成指标包括覆盖度、抓取模式数、precision grasp 比例和 diversity。系统指标包括采样延迟、QP 调用次数、最终 refinement 步数与真实闭环频率。

### 12.5 真实机器人 stress tests

真实实验不应只展示正常条件。建议设计四个可重复压力测试：为同一物体更换不同摩擦表面；给对象位置加入已知毫米级偏差；抓取后施加方向和大小可控的侧向 wrench；将对象质量或质心改变而不更新视觉几何。每次同步记录触觉、关节力矩、对象六维运动和是否滑落。这样可以直接检验证书 margin 是否与真实稳健性一致。

## 13. 消融实验与预期失败模式

最关键的消融不是删掉网络层，而是破坏数学结构。去掉 $Z$ 联合生成，可验证 certificate-carrying representation 的作用；只保留一个重力 wrench，可验证扰动多面体的必要性；去掉 torque constraints，可观察数学力封闭但硬件不可执行的比例；将 posterior covariance 设为零，可检验 chance tightening；用固定 $\lambda\nabla E$ 替代最小投影，可检验多样性保持；去掉 calibration margin，可检验风险是否被系统性低估。

预期失败模式也应主动报告。薄物体和尖锐边缘可能导致接触法向不稳定；软物体违反刚体接触假设；高噪声早期 clean estimate 可能产生错误接触；多面体顶点数过多会增加证书维度和 QP 成本；明显多峰的不确定性会破坏局部高斯近似。第一版分别通过法向平滑、限制为刚体对象、只在去噪后段激活证书、控制顶点数量和筛除明显多峰样本来保持问题边界。

## 14. 最小可发表版本与增强版本

### 14.1 最小可发表版本

第一篇不宜一次解决所有问题。建议固定一种手型和准静态刚体接触，生成 $(x,Z)$，使用一个任务扰动多面体；以高斯参数不确定性构造 delta-method margin；在 clean estimate 上做最小干预 QP；最终由精确 QP 复核。理论只承诺顶点充分性、线性高斯 chance constraint 和局部最小投影性质。只要在多种不确定性扫描下显著降低尾部失败，同时保持抓取多样性，就具备扎实的 CoRL/ICRA/RSS 论文骨架。

### 14.2 增强版本

增强版只建议加入触觉闭环：执行初次接触后更新 $q(u\mid o,y_{1:t})$，再 warm-start 去噪剩余动作。多峰后验和接触模式切换可以分别研究，但不应与第一篇论文同时展开，否则中心理论会再次发散。

## 15. 实施路线与里程碑

第一阶段先实现证书 oracle，而不是先训练 diffusion。需要验证给定 $x$ 时，接触提取、摩擦锥离散、grasp wrench matrix、顶点 QP 和 torque constraints 是否数值稳定；并用小型解析例子验证命题。若 oracle 本身不能可靠区分稳定与不稳定抓取，后面的生成模型没有意义。

第二阶段在现有 backbone 上实现“生成后最小投影”，暂不联合生成 $Z$。这一步建立强 baseline，也验证 chance margin 和 clean-sample projection 是否有效。第三阶段加入 certificate head，比较预测 $Z$ 是否减少 QP 迭代、提高可行率。第四阶段才联合微调整个 diffusion，并做不确定性校准。第五阶段完成跨对象、跨扰动和真实机器人 stress tests。

一个合理的 go/no-go 标准是：在相同生成数量和 oracle 预算下，相比“vanilla diffusion + final GraspQP refinement”，方法必须同时实现更低的 OOD violation、更少的最终修正和相近或更高的 diversity。若只提高名义成功率而不能改善尾部风险，说明概率证书没有发挥作用；若只减少 QP 时间而不提高稳健性，则论文更接近加速工作而非安全抓取方法。

### 15.1 可行性硬审计：第一版必须删掉什么、保留什么

为了保证路线可落地，第一版主动删除三个高风险部分：不生成对偶变量，不做接触模式离散扩散，也不做触觉在线 belief update。每根手指只选一个候选接触邻域，并采用固定数量的摩擦锥射线；不确定度来自仿真参数随机化和少量真实标定。这些删减不会破坏“证书联合生成 + 概率收紧”的核心主张。

第一版只保留四个能够独立测试的模块。模块 A 是现有 grasp diffusion backbone，输出 $x$；即使不修改网络，也能先跑通。模块 B 是确定性的证书 oracle：给定 $x$ 和 $u$，接触提取后为 $K$ 个扰动顶点解凸 QP。模块 C 是 certificate head，预测 $Z$ 作为 QP warm start；若联合训练不稳定，可先冻结 backbone 单独训练。模块 D 是 clean-sample 最小投影器；若多约束 QP 数值不稳，可先只投影一个 smooth robust certificate margin，其余碰撞和关节约束沿用 backbone 已有处理。

这四个模块形成逐级可交付链路：

$$
\text{现有抓取生成}
\rightarrow
\text{最终证书筛选}
\rightarrow
\text{证书 warm start}
\rightarrow
\text{名义证书去噪}
\rightarrow
\text{概率收紧去噪}.
$$

任何后一级失败，前一级都仍然是可运行 baseline，不会导致整个项目无法产出。尤其是，联合 $Z$ 生成若未提高最终成功率，它仍可通过减少 QP 求解时间证明 warm-start 价值；概率投影若暂时无法稳定训练，也可作为 training-free sampler 插入预训练 backbone，而不必重训整个模型。

### 15.2 为什么核心 QP 在计算上可行

摩擦锥采用 $R=4$ 条射线、四个有效指尖时，每个顶点 QP 只有约 $M=16$ 个主要接触力系数。即使加入上下界和关节力矩约束，仍属于小规模强凸 QP。扰动多面体第一版可取 $K=12$ 个对称顶点，对应六维 wrench 的正负基方向，或取任务相关的 8–16 个顶点。各顶点 QP 条件独立，可以在 GPU batch 或 CPU 多线程中并行。最终论文应测量实际 wall-clock，而不预先承诺固定实时频率；但从变量规模上看，它远小于高自由度轨迹优化或完整接触仿真。

还可将 $Z$ 解释为精确求解器的 warm start，而不是完全替代求解器。这样即使网络预测存在误差，最终 feasibility 仍由凸 QP 决定。生成器负责把候选送到可行区域附近，求解器负责可信复核，二者职责清晰。这种“learning proposes, optimization certifies”的结构是可行性的关键保障。

### 15.3 数据可行性

该方法不要求真实机器人提供大规模接触力标签。$Z$ 标签可由已有稳定抓取姿态离线求 QP 自动生成；参数不确定性也可通过摩擦、接触点、法向和物体位姿随机化构造。真实数据只用于校准和最终 stress test，而不是从零训练模型。第一版可以从公开抓取数据的一个受控子集开始，例如单一手型、数百个训练对象和固定接触提取规则，验证方法成立后再扩展。

必须提前处理一个现实问题：几何数据中的“近接触”不一定形成可靠接触。可设置接触距离阈值并对表面法向做平滑；接触不足的抓取直接标为无证书，而不是强行求解。这样会损失一部分训练数据，但能防止伪接触污染 QP 标签。

### 15.4 可行性验收门槛

在训练完整 diffusion 前设置四个硬门槛。第一，解析物体上的 QP 平衡残差与手工构造稳定/不稳定抓取排序一致。第二，离线抓取集上至少存在足量、且包含不止 power grasp 的可认证样本，否则应先改接触提取或扰动集，而不是训练网络。第三，QP 对接触点与摩擦的小扰动产生连续、方向合理的 margin 变化。第四，单个对象批量求解的耗时足以支持离线标签生成和推理阶段末端复核。

只有通过这四项，才进入 certificate head 和 chance projection。这个顺序保证最不确定的学习模块不会掩盖底层物理建模错误。所谓“保证可行性”在科研上不能理解为预先保证实验一定优于所有 baseline，而应理解为：算法每个子问题都有明确求解方法、数据可以自动构造、失败可以在早期被检测，且存在不依赖高风险扩展的最小发表闭环。

## 16. 论文贡献的推荐写法

论文可以将贡献收敛为三条。

第一，提出 certificate-carrying dexterous grasp diffusion，联合建模抓取姿态与任务扰动多面体顶点的接触力 witness；通过凸性说明有限顶点 witness 足以证实整个扰动多面体的准静态可抵抗性。

第二，提出 uncertainty-tightened clean-sample denoising，根据摩擦、接触几何和物体状态后验构造 chance-constrained certificate margin，并通过最小干预投影在安全性与生成多样性之间取得可解释平衡。

第三，建立以证书有效性和尾部风险为中心的评测协议，在摩擦、感知、接触与任务扰动的系统变化下，验证证书校准、抓取多样性、求解效率和真实机器人稳健性。

不要把贡献写成四五个网络模块。审稿人应当看到一个中心对象：**带概率语义的可行性证书**。有限顶点 witness、chance tightening 和最小投影都是围绕这个对象展开的必要环节。

## 17. 最终判断

该主线具有足够的数学思路和顶会价值，原因不是公式数量多，而是它提出了一个可以被证明、被核验、被实验反驳的新生成对象。顶点 witness 提供精确的凸性逻辑；可微 QP 将接触力学连接到生成梯度；chance constraint 将接触不确定性转化为安全余量；最小干预投影说明如何尽量不破坏 diffusion 的原始分布。四者围绕同一个证书展开，没有必要再增加额外理论层。

其最主要的投稿风险有两个。第一，2026 年 physics-guided grasp diffusion 发展很快，必须避免把新意表述为一般的约束 guidance。第二，真实接触模型与不确定度校准若做得不扎实，理论会停留在仿真假设里。因此，论文成败不取决于再增加一个网络，而取决于是否能证明证书在真实扰动下确实比名义能量更能预测和避免失败。

在合理收缩范围后，这是一条值得优先投入的主线。第一版固定为“联合 contact-force witness + 概率收紧 + 最小投影”，不加入对偶生成、接触模式扩散或触觉闭环。只有核心结论成立后，再单独研究 tactile belief update。

## 参考边界论文

1. Weng et al., [DexDiffuser: Generating Dexterous Grasps with Diffusion Models](https://arxiv.org/abs/2402.02989), IEEE RA-L, 2024.
2. Zhong et al., [DexGrasp Anything: Towards Universal Robotic Dexterous Grasping with Physics Awareness](https://arxiv.org/abs/2503.08257), CVPR, 2025.
3. Xiao et al., [SafeDiffuser: Safe Planning with Diffusion Probabilistic Models](https://arxiv.org/abs/2306.00148), ICLR, 2025.
4. Zhang et al., [Constrained Diffusers for Safe Planning and Control](https://arxiv.org/abs/2506.12544), NeurIPS, 2025.
5. Zurbrügg et al., [GraspQP: Differentiable Optimization of Force Closure for Diverse and Robust Dexterous Grasping](https://arxiv.org/abs/2508.15002), 2025.
6. Zhong et al., [Grasp2Grasp: Vision-Based Dexterous Grasp Translation via Schrödinger Bridges](https://arxiv.org/abs/2506.02489), NeurIPS, 2025.
7. [EFF-Grasp: Energy-Field Flow Matching for Physics-Aware Dexterous Grasp Generation](https://arxiv.org/abs/2603.16151), 2026 preprint.
8. [NDPP-Grasp: Non-Differentiable Physical Plausibility Constraint-Guided Task-Oriented Dexterous Grasp Generation](https://arxiv.org/abs/2606.02432), 2026 preprint.
9. [Grounding Generative Policies in Physics: Optimization-Guided Diffusion for Robot Control](https://arxiv.org/abs/2606.24208), 2026 preprint.
10. [CoorGrasp: Coordinated Contact Control for Adaptive Dexterous Grasping Under Uncertainty](https://arxiv.org/abs/2607.03557), 2026 preprint.
