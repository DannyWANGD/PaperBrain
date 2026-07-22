---
tags:
  - paper/SRG
  - topic/MILP
  - topic/constraint_guidance
  - topic/diffusion_model
  - 灵巧手专项
created: 2026-06-19
updated: 2026-06-19
source_note: "[[灵巧手专项/SRG 1.md]]"
source_pdf: "[[PDFs/SRG Scorebased Relaxationguided Generation for Mixed Integer Linear Programming.pdf]]"
aliases:
  - SRG约束信息融入机制
  - SRG constraint guidance
---

# SRG 约束信息注入机制：数学公式推导笔记

> 本笔记重构自 [[灵巧手专项/SRG 约束信息融入机制详解.md]]，依据 [[灵巧手专项/SRG 1.md]] 与 [[PDFs/SRG Scorebased Relaxationguided Generation for Mixed Integer Linear Programming.pdf]]。本文只保留 SRG 中“约束信息如何进入生成模型”的核心数学逻辑，不展开实验、资源、PaS 背景和额外评论。

## 0. 十个部分之间的逻辑关系

这十个部分不是并列罗列，而是在推导同一条主线：**SRG 如何把原本写在 MILP 里的外部约束，逐步变成扩散模型内部可学习、可采样的生成方向。** 可以把全文理解成一条从“硬约束”到“训练目标”的转换链：

```text
MILP 原始约束 Ax ≥ b
→ 连续松弛后可在 x_t 上计算违反程度
→ 定义可行性惩罚 P(x) 和最优性惩罚 O(x)
→ 把 P(x), O(x) 加入 KL 生成目标
→ 等价得到重加权目标分布 \tilde p(x|g)
→ 对 \tilde p_t 求 score
→ 近似得到 relaxation-guided score
→ 转换成 epsilon-space 训练目标
→ 推理时通过 learned score 体现约束偏好
→ 最后类比到灵巧手物理约束注入
```

因此，阅读时可以按“三次转换”来抓住整体逻辑。**第一次转换**是第 1、2 节完成的：从 MILP 的硬约束 $Ax\ge b$ 出发，通过连续松弛，把“是否违反约束”变成一个可计算的惩罚函数 $P(x)$。**第二次转换**是第 3、4、5 节完成的：把 $P(x)$ 和 $O(x)$ 放进生成目标，推导出重加权分布 $\tilde p$，再把这个分布的偏好变成 score 中的梯度引导项。**第三次转换**是第 6、7、8 节完成的：把理论上的 guided score 落到扩散模型实际训练使用的 epsilon-space 目标里，并解释为什么推理阶段不需要每一步重新显式计算约束梯度。

更具体地说，**第 1 节**先确定 SRG 的对象和输入：约束来自 $Ax\ge b$，问题结构通过 $g=\tau_\phi(A,b,c)$ 进入网络。**第 2 节**定义 $P(x)$ 和 $O(x)$，解决“约束和目标如何数值化”的问题。**第 3 节**说明这些惩罚如何改变模型学习的概率分布。**第 4 节**把分布变化进一步转化成 score 变化。**第 5 节**单独解释 $\nabla P(x)$ 为什么能通过 $A^\top$ 把约束违反信息传回变量。**第 6 节**把 score 公式写成实际训练损失。**第 7 节**补充引导强度的数值校准。**第 8 节**说明训练注入和推理采样的关系。**第 9 节**压缩回顾整条链条。**第 10 节**则跳出论文，讨论这套 penalty-to-score 的范式和灵巧手物理约束注入之间的关系。

所以，全文最核心的一句话是：**SRG 先把约束写成 penalty，再把 penalty 写进目标分布，最后把目标分布的变化写成 score guidance。**

## 1. 问题起点：MILP 约束如何成为可学习对象

SRG 面向的对象是混合整数线性规划（MILP）。论文采用如下形式描述一个实例：

$$
\min_{x\in\mathbb{R}^n} c^\top x
$$

$$
\text{s.t.}\quad Ax\ge b,\quad l\le x\le u,\quad x_j\in\mathbb{Z},\ \forall j\in I .
$$

这里 $x$ 是待求解的决策变量，$c^\top x$ 是线性目标函数，$Ax\ge b$ 是线性约束，$l,u$ 是变量上下界，$I$ 表示必须取整数值的变量索引集合。SRG 所说的“约束信息”主要来自 $A,b$ 以及变量上下界和整数结构；其中最核心的是线性约束 $Ax\ge b$。

如果直接让神经网络学习从 MILP 实例到最优解 $x^*$ 的映射，模型很容易退化成“模仿标签”：训练时接近已知最优解，但并没有显式理解某个候选解为什么违反约束、违反多少、应该往哪个方向修正。SRG 的关键想法是：把 MILP 的可行性约束转化为连续空间中的惩罚函数，再把惩罚函数的梯度写入 score-based diffusion 的训练目标，使模型在去噪生成候选解时天然偏向可行且高质量的区域。

为了让不同 MILP 实例能被统一输入网络，论文先将实例表示成变量—约束二部图，并用 GNN 编码为结构条件：

$$
g=\tau_\phi(A,b,c).
$$

这个 $g$ 并不是单独保证可行性的机制，而是告诉后续 score network 当前问题的结构：哪些变量参与哪些约束、约束系数如何、目标函数如何。后续生成模型实际学习的是条件 score：

$$
s_\theta(x_t,t,g),
$$

即在给定问题结构 $g$ 和扩散时间步 $t$ 的情况下，如何把当前带噪声的候选解 $x_t$ 推向更合理的解区域。

## 2. 连续松弛：为什么约束惩罚可以被计算

MILP 的整数变量使原问题不可直接作为平滑连续优化对象。SRG 采用连续松弛的思想：在建模和扩散过程中，先允许整数变量暂时落在连续空间中，例如把二元变量 $x_j\in\{0,1\}$ 放松为 $x_j\in[0,1]$。这样即使 $x_t$ 还不是严格整数解，也可以评价它的目标值和约束违反程度。

对单条不等式约束

$$
a_i^\top x\ge b_i,
$$

自然的违反量是

$$
\hat v_i(x)=\max\{b_i-a_i^\top x,0\}.
$$

如果 $a_i^\top x\ge b_i$，则 $b_i-a_i^\top x\le 0$，违反量为 $0$；如果 $a_i^\top x<b_i$，则 $b_i-a_i^\top x>0$，违反量正好等于距离满足约束还差多少。因此 $\max\{b_i-a_i^\top x,0\}$ 把硬约束转化成了一个非负连续惩罚。把所有约束合在一起，得到 SRG 使用的可行性惩罚项：

$$
P(x)=\lambda\|\max\{b-Ax,0\}\|_1 .
$$

这里 $b-Ax$ 是所有约束的违反方向，$\max\{b-Ax,0\}$ 只保留真正违反的部分，$\|\cdot\|_1$ 将各条约束的违反量相加，$\lambda$ 控制约束惩罚强度。于是，原本的硬条件 $Ax\ge b$ 被替换为一个数值函数 $P(x)$：当 $x$ 越不可行，$P(x)$ 越大；当 $x$ 满足这些不等式时，$P(x)=0$。

SRG 同时定义一个最优性惩罚项，用来衡量候选解与参考最优解 $x^*$ 的偏离：

$$
O(x)=\|c\odot(x-x^*)\|_1 .
$$

其中 $\odot$ 表示逐元素乘法。这个定义不是直接计算目标差 $c^\top x-c^\top x^*$，而是用目标系数 $c$ 加权每个变量相对 $x^*$ 的偏离。它的作用是告诉生成模型：那些目标系数更重要的变量，如果偏离参考最优解，应当受到更强惩罚。这样，SRG 同时拥有了两个可微或可用次梯度处理的信号：$P(x)$ 表示“是否可行”，$O(x)$ 表示“是否接近优质解”。

## 3. 从模仿数据到重加权目标分布

普通条件生成模型可以被理解为学习一个分布 $q_\theta(x|g)$，使它接近训练数据中的高质量解分布 $p_{data}(x|g)$。若只做数据模仿，可以写成：

$$
\min_{q_\theta}D_{KL}\big(q_\theta(x|g)\|p_{data}(x|g)\big).
$$

SRG 认为这一步没有显式利用 MILP 本身的可行性和最优性信息，因此在 KL 目标后加入期望惩罚：

$$
\min_{q_\theta}\left[
D_{KL}\big(q_\theta(x|g)\|p_{data}(x|g)\big)
+\mathbb{E}_{x\sim q_\theta}\big[\gamma_oO(x)+\gamma_cP(x)\big]
\right].
$$

其中 $\gamma_o>0$ 和 $\gamma_c>0$ 分别控制最优性引导和可行性引导的强度。这个目标的意义非常直接：模型不只要生成像训练样本的解，还要避免生成 $O(x)$ 大或 $P(x)$ 大的候选解。也就是说，数据模仿、目标质量、约束可行性三者共同决定模型应该把概率质量放在哪里。

这个正则化目标可以等价地改写为匹配一个重加权后的目标分布。定义

$$
\tilde p(x|g)=\frac{1}{Z}p_{data}(x|g)\exp\big(-\gamma_oO(x)-\gamma_cP(x)\big),
$$

其中

$$
Z=\int p_{data}(x|g)\exp\big(-\gamma_oO(x)-\gamma_cP(x)\big)dx
$$

是归一化常数。下面展开即可看到等价关系：

$$
\begin{aligned}
&D_{KL}\big(q(x)\|p_{data}(x|g)\big)
+\mathbb{E}_{x\sim q}\big[\gamma_oO(x)+\gamma_cP(x)\big] \\
&=\mathbb{E}_{x\sim q}\left[\log\frac{q(x)}{p_{data}(x|g)}+\gamma_oO(x)+\gamma_cP(x)\right] \\
&=\mathbb{E}_{x\sim q}\left[\log q(x)-\log p_{data}(x|g)-\log\exp\big(-\gamma_oO(x)-\gamma_cP(x)\big)\right] \\
&=\mathbb{E}_{x\sim q}\left[\log q(x)-\log\left(p_{data}(x|g)\exp\big(-\gamma_oO(x)-\gamma_cP(x)\big)\right)\right] \\
&=\mathbb{E}_{x\sim q}\left[\log q(x)-\log\big(Z\tilde p(x|g)\big)\right] \\
&=D_{KL}\big(q(x)\|\tilde p(x|g)\big)-\log Z.
\end{aligned}
$$

由于 $Z$ 与 $q$ 无关，最小化原来的正则化目标等价于最小化

$$
D_{KL}\big(q(x)\|\tilde p(x|g)\big).
$$

这一步是 SRG 约束注入逻辑的核心转折：约束没有被作为后处理规则附加到模型外面，而是通过指数重加权改变了模型要学习的目标分布。若某个 $x$ 违反约束严重，则 $P(x)$ 大，因子 $\exp(-\gamma_cP(x))$ 小，$x$ 在 $\tilde p$ 中的概率被压低；若某个 $x$ 同时接近高质量数据、目标偏离小、约束违反小，它在 $\tilde p$ 中的概率就更高。

## 4. 从重加权分布到 relaxation-guided score

SRG 采用 score-based diffusion 进行采样。设正向扩散过程从 $x_0$ 加噪得到 $x_t$，VP-SDE 或 DDPM 形式可写为：

$$
x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon,
\quad \epsilon\sim\mathcal{N}(0,I).
$$

模型最终希望从重加权分布 $\tilde p(x|g)$ 中采样。反向 SDE 的漂移项需要目标分布在时间 $t$ 的 score：

$$
\nabla_{x_t}\log\tilde p_t(x_t|g).
$$

论文先给出一个精确分解。记原始数据分布经正向扩散后的边缘分布为 $p_t(x_t|g)$，重加权函数为

$$
w(x)=\exp\big(-\gamma_oO(x)-\gamma_cP(x)\big).
$$

根据 $\tilde p_0(x|g)=\frac{1}{Z}p_{data}(x|g)w(x)$，有

$$
\begin{aligned}
\tilde p_t(x_t|g)
&=\int q_t(x_t|x_0)\tilde p_0(x_0|g)dx_0 \\
&=\frac{1}{Z}\int q_t(x_t|x_0)p_{data}(x_0|g)w(x_0)dx_0 .
\end{aligned}
$$

另一方面，原始扩散边缘分布为

$$
p_t(x_t|g)=\int q_t(x_t|x_0)p_{data}(x_0|g)dx_0.
$$

因此上式可以写成

$$
\tilde p_t(x_t|g)=\frac{1}{Z}p_t(x_t|g)\mathbb{E}_{x_0\sim p(x_0|x_t,g)}[w(x_0)].
$$

对数求梯度得到精确分解：

$$
\nabla_{x_t}\log\tilde p_t(x_t|g)
=
\nabla_{x_t}\log p_t(x_t|g)
+
\nabla_{x_t}\log\mathbb{E}_{x_0\sim p(x_0|x_t,g)}[w(x_0)].
$$

第一项是普通数据 score，它负责让样本像训练数据；第二项来自重加权函数 $w$，它包含最优性和可行性惩罚，因此正是约束信息进入 score 的理论入口。

问题在于，$\mathbb{E}_{x_0\sim p(x_0|x_t,g)}[w(x_0)]$ 通常不可解析计算。SRG 因此采用一个实用近似：用当前带噪样本 $x_t$ 处的重加权函数梯度近似该项，即

$$
\nabla_{x_t}\log\mathbb{E}_{x_0\sim p(x_0|x_t,g)}[w(x_0)]
\approx
\nabla_{x_t}\log w(x_t).
$$

由于

$$
\log w(x_t)=-\gamma_oO(x_t)-\gamma_cP(x_t),
$$

于是

$$
\nabla_{x_t}\log w(x_t)
=-\gamma_o\nabla_{x_t}O(x_t)-\gamma_c\nabla_{x_t}P(x_t).
$$

最终得到 SRG 的近似 relaxation-guided score：

$$
s^*(x_t,t,g)
\approx
\nabla_{x_t}\log p_t(x_t|g)
-
\gamma_o\nabla_{x_t}O(x_t)
-
\gamma_c\nabla_{x_t}P(x_t).
$$

这个公式完整表达了约束注入的方向性含义：普通 score 把样本推向数据分布高密度区域，$-\gamma_o\nabla O$ 把样本推向更接近高质量目标的区域，$-\gamma_c\nabla P$ 把样本推向更少违反约束的区域。约束不再只是判断生成结果是否合格的外部标准，而成为了去噪方向的一部分。

## 5. 约束惩罚与最优性惩罚的梯度如何作用到变量上

对

$$
P(x)=\lambda\|\max\{b-Ax,0\}\|_1
$$

而言，若第 $i$ 条约束 $a_i^\top x\ge b_i$ 被违反，即 $a_i^\top x<b_i$，该条约束贡献的惩罚是

$$
\lambda(b_i-a_i^\top x).
$$

对 $x$ 求梯度得到

$$
\nabla_x\lambda(b_i-a_i^\top x)=-\lambda a_i.
$$

若第 $i$ 条约束没有违反，则该条对应的 ReLU 项为 $0$，梯度也为 $0$。把所有约束合并起来，可写为

$$
\nabla_xP(x)=-\lambda A^\top\mathbf{1}[Ax<b],
$$

其中 $\mathbf{1}[Ax<b]$ 表示哪些约束当前被违反。这个式子说明，约束层面的违反信息通过 $A^\top$ 被传回变量层面：某条约束被违反后，与这条约束相关的变量都会收到相应的修正信号。

在 guided score 中使用的是负梯度项

$$
-\gamma_c\nabla_xP(x).
$$

代入上式可得，在严格按违反指示计算时：

$$
-\gamma_c\nabla_xP(x)=\gamma_c\lambda A^\top\mathbf{1}[Ax<b].
$$

对于 $Ax\ge b$ 型约束，这个方向会推动相关变量使 $Ax$ 增大，从而减小 $b-Ax$ 的正部，也就是降低约束违反量。这就是 SRG 中可行性引导的数学含义。

类似地，最优性惩罚项

$$
O(x)=\|c\odot(x-x^*)\|_1
=\sum_{j=1}^n |c_j(x_j-x_j^*)|
$$

也会对每个变量产生一个逐坐标的修正信号。对第 $j$ 个变量而言，在非零且非光滑点之外，有

$$
\frac{\partial O(x)}{\partial x_j}
=c_j\,\operatorname{sign}\big(c_j(x_j-x_j^*)\big).
$$

写成向量形式就是

$$
\nabla_x O(x)=c\odot \operatorname{sign}\big(c\odot(x-x^*)\big).
$$

若记

$$
\delta_O=\operatorname{sign}\big(c\odot(x-x^*)\big),
$$

则

$$
\nabla_xO(x)=c\odot\delta_O.
$$

在 guided score 中使用的是

$$
-\gamma_o\nabla_xO(x).
$$

因此，$O(x)$ 的作用可以理解为：它把每个变量往参考最优解 $x^*$ 的对应坐标拉回去，并且拉回力度由目标系数 $c_j$ 的大小调节。如果某个变量 $x_j$ 偏离 $x_j^*$，且该变量在目标函数中权重较大，那么 $|c_j|$ 大，对应的梯度修正也更强；如果该变量对目标函数影响较小，那么修正更弱。与 $P(x)$ 不同，$P(x)$ 通过 $A^\top$ 把“约束层面的违反信息”传回多个相关变量，而 $O(x)$ 更像是一个逐变量的“朝参考最优解靠拢”的吸引项。

需要注意，$O(x)$ 并不是直接对原目标函数 $c^\top x$ 求梯度；它惩罚的是候选解 $x$ 与参考解 $x^*$ 的加权距离。因此它的含义不是单纯“让 $c^\top x$ 下降”，而是“让重要变量不要偏离已知优质解太远”。在训练实现中，论文还会对整数坐标先投影得到 $\tilde x_t$，再用 $c\odot\operatorname{sign}(c\odot(\tilde x_t-x^*))$ 作为目标引导方向，以便让这个逐变量修正更符合 MILP 的离散结构。

由于 $O(x)$ 和 $P(x)$ 都包含 $L_1$、ReLU 或符号函数等非光滑结构，论文在非光滑点使用 Clarke subgradient 的解释。也就是说，SRG 并不要求每个点都存在经典光滑梯度，而是使用可行的次梯度方向作为训练信号。

## 6. 写入 epsilon-space 训练目标

SRG 的 score network 实际采用噪声预测形式。正向扩散写作：

$$
x_t=\sqrt{\bar\alpha_t}x^*+\sqrt{1-\bar\alpha_t}\epsilon_t,
\quad \epsilon_t\sim\mathcal{N}(0,I).
$$

在普通 DDPM 中，若网络预测噪声 $\epsilon_\theta(x_t,t,g)$，则 score 与噪声预测之间近似满足：

$$
\nabla_{x_t}\log p_t(x_t|g)\approx -\frac{\epsilon_t}{\sqrt{1-\bar\alpha_t}}.
$$

现在目标 score 不是普通 score，而是

$$
s^*(x_t,t,g)
\approx
-\frac{\epsilon_t}{\sqrt{1-\bar\alpha_t}}
-
\gamma_o\nabla_{x_t}O(x_t)
-
\gamma_c\nabla_{x_t}P(x_t).
$$

如果用 epsilon 形式训练，就希望网络预测的噪声目标满足

$$
-\frac{\epsilon_{target}}{\sqrt{1-\bar\alpha_t}}
\approx
s^*(x_t,t,g).
$$

两边乘以 $-\sqrt{1-\bar\alpha_t}$，得到

$$
\epsilon_{target}
=
\epsilon_t
+
\sqrt{1-\bar\alpha_t}\gamma_o\nabla_{x_t}O(x_t)
+
\sqrt{1-\bar\alpha_t}\gamma_c\nabla_{x_t}P(x_t).
$$

这就是为什么 SRG 的训练目标不再只是原始噪声 $\epsilon_t$，而是原始噪声加上目标和约束对应的修正项。

论文进一步对离散变量和约束梯度做了实用简化。对于整数变量，先将 $x_t$ 的整数坐标投影到最近的离散值，得到 $\tilde x_t$，再计算目标偏离符号：

$$
\tilde\delta_O=\operatorname{sign}\big(c\odot(\tilde x_t-x^*)\big),
$$

从而近似

$$
\nabla_{x_t}O(\tilde x_t)=c\odot\tilde\delta_O.
$$

对于约束项，理论梯度是

$$
\nabla_xP(x)=-\lambda A^\top\mathbf{1}[Ax<b],
$$

但论文为了稳定训练，将其简化为一个由约束矩阵决定的整体可行性方向：

$$
\nabla_{x_t}\tilde P(x_t)=-\lambda A^\top.
$$

于是得到 epsilon-space 中的简化监督目标：

$$
L_{simplified}
=
\left\|s_\epsilon(x_t,t,g)-\operatorname{sg}(\epsilon_t+v_o+v_c)\right\|_2^2,
$$

其中

$$
v_o=\gamma_o\sqrt{1-\bar\alpha_t}\, c\odot\tilde\delta_O,
$$

$$
v_c=-\gamma_c\sqrt{1-\bar\alpha_t}\,\lambda A^\top.
$$

$\operatorname{sg}(\cdot)$ 表示 stop-gradient。这个损失函数是 SRG 约束注入在训练层面的最终落点：网络被要求预测的不是纯粹去噪方向，而是包含最优性修正 $v_o$ 和可行性修正 $v_c$ 的方向。换句话说，约束矩阵 $A$ 不只是作为输入条件存在，还直接进入了训练标签。

## 7. 引导强度的尺度校准

由于 $v_o$ 和 $v_c$ 的大小依赖于问题数据的尺度，例如 $\|c\|$、$\|A\|$、变量数量 $n$ 和时间步 $t$，固定的 $\gamma_o,\gamma_c$ 可能导致引导项压过普通扩散噪声信号。若可行性引导过强，模型可能无法学习数据分布；若目标引导过强，模型可能追求目标改进而损害可行性。为避免这种尺度失衡，论文引入实例自适应和时间相关的缩放规则。

定义原始引导方向

$$
u_o=c\odot\tilde\delta_O,
$$

$$
u_c=-\lambda A^\top\mathbf{1}.
$$

然后将有效引导系数归一化为

$$
\gamma_o\leftarrow\gamma_o\frac{\rho_o\sqrt n}{\|u_o\|_2+\varepsilon},
$$

$$
\gamma_c\leftarrow\gamma_c\frac{\rho_c\sqrt n}{\|u_c\|_2+\varepsilon}.
$$

这里 $\rho_o,\rho_c$ 是可调的引导强度参数，$\varepsilon$ 用于数值稳定。这个步骤不是约束注入的理论核心，但对训练稳定性很重要；它保证不同规模、不同系数大小的 MILP 实例中，目标引导和约束引导不会因为数值尺度差异而失控。

## 8. 推理阶段：约束信息以 learned score 的形式存在

训练完成后，SRG 在推理阶段从高斯噪声开始反向采样：

$$
x_T\sim\mathcal{N}(0,I),
$$

然后使用已训练好的 score network 逐步去噪，得到 relaxed candidate：

$$
\tilde x_0\sim\tilde p(x|g).
$$

论文中特别强调，推理采样时不需要额外的 guidance module，也不需要在每一步显式重新计算约束违反量和约束梯度。原因是可行性和最优性引导已经在训练阶段被写入了 score network 的监督目标中。因此，推理阶段的约束信息并不是以外部硬投影或每步优化的形式出现，而是以 learned guided score 的形式隐含在网络输出里。

不过，这并不意味着 SRG 的神经网络本身保证输出严格可行。SRG 生成的是候选解，且通常仍处在 relaxed space。随后论文将候选解用于构造紧凑的 trust-region 子问题，并交给标准 MILP 求解器（如 SCIP 或 Gurobi）完成最终搜索。严格的整数性、可行性和最终解质量仍然依赖求解器。SRG 的角色是把搜索起点和搜索区域推向更可能可行、更可能高质量的位置，而不是单独替代精确求解器。

## 9. 约束注入逻辑的完整链条

SRG 的约束注入可以概括为一条连续的数学链条。首先，MILP 约束 $Ax\ge b$ 通过连续松弛变成可在 relaxed candidate 上评价的违反量；其次，违反量被写成惩罚函数

$$
P(x)=\lambda\|\max\{b-Ax,0\}\|_1;
$$

然后，它与最优性惩罚

$$
O(x)=\|c\odot(x-x^*)\|_1
$$

一起进入正则化生成目标；接着，该目标等价于学习重加权分布

$$
\tilde p(x|g)=\frac{1}{Z}p_{data}(x|g)\exp[-\gamma_oO(x)-\gamma_cP(x)];
$$

再进一步，重加权分布的 score 被近似为

$$
s^*(x_t,t,g)
\approx
\nabla_{x_t}\log p_t(x_t|g)
-
\gamma_o\nabla_{x_t}O(x_t)
-
\gamma_c\nabla_{x_t}P(x_t);
$$

最后，在 epsilon-space 中，网络学习的目标变成

$$
\epsilon_t+v_o+v_c,
$$

其中 $v_c$ 直接由约束矩阵 $A$ 给出。因此，约束信息从原始 MILP 公式出发，依次经历“约束违反量—惩罚函数—分布重加权—score 梯度—epsilon 训练目标”这五个环节，最终进入神经网络参数。

## 10. 与灵巧手物理约束注入的关系

SRG 原论文并没有直接处理灵巧手中的物理约束。它的约束主要是 MILP 里的线性约束，例如 $Ax\ge b$，而灵巧手任务中的关键限制往往包括关节角范围、接触不穿透、摩擦锥、力闭合、力矩限制、动力学一致性、物体姿态稳定性等。这些约束多数是非线性的、非凸的，甚至在接触切换处是非光滑的，因此不能简单地等同于 SRG 中的线性 MILP 约束。

但是，SRG 提供了一种非常清晰的“约束注入范式”：不要只让生成模型模仿数据，而是把约束违反程度写成一个 penalty，再把 penalty 的梯度融入 score 或 denoising target。若将灵巧手的候选动作、轨迹、抓取参数或接触力记为 $z$，可以类比构造一个物理约束惩罚：

$$
P_{phys}(z)
=
\alpha_1P_{joint}(z)
+
\alpha_2P_{penetration}(z)
+
\alpha_3P_{friction}(z)
+
\alpha_4P_{dynamics}(z),
$$

其中 $P_{joint}$ 可以惩罚关节越界，$P_{penetration}$ 可以惩罚几何穿透，$P_{friction}$ 可以惩罚违反摩擦锥，$P_{dynamics}$ 可以惩罚动力学不一致。若再定义任务质量项 $O_{task}(z)$，例如抓取稳定性、轨迹长度或执行代价，则可以得到与 SRG 类似的重加权分布：

$$
\tilde p(z|y)
\propto
p_{data}(z|y)
\exp[-\gamma_{task}O_{task}(z)-\gamma_{phys}P_{phys}(z)],
$$

其中 $y$ 可以是物体形状、点云、初始姿态、任务目标等条件信息。对应的 guided score 形式为：

$$
s^*(z_t,t,y)
\approx
\nabla_{z_t}\log p_t(z_t|y)
-
\gamma_{task}\nabla_{z_t}O_{task}(z_t)
-
\gamma_{phys}\nabla_{z_t}P_{phys}(z_t).
$$

这正是 SRG 思路对灵巧手问题最有价值的启发：把“物理规则”从自然语言或后验检查，转化为可计算的约束惩罚，再通过梯度方向影响生成过程。这样做有可能让 diffusion policy、grasp generation model 或 trajectory generator 在采样阶段更偏向物理可行的动作区域。

但这种迁移也有明显边界。第一，灵巧手物理约束通常比 $Ax\ge b$ 复杂得多，$P_{phys}$ 的设计本身就是难点；第二，接触、碰撞和摩擦往往非光滑，梯度可能不稳定或不可用，需要可微仿真、平滑近似、SDF、接触模型或投影优化器支持；第三，像 SRG 一样，仅靠神经网络内化约束通常不能保证最终严格满足物理约束，因此仍然需要后端检查、轨迹优化、MPC、仿真验证或安全控制器。最稳妥的理解是：SRG 不是给出了灵巧手物理约束注入的现成答案，而是给出了一条可借鉴的数学路线——**把约束写成 penalty，把 penalty 变成 score guidance，把 guided score 写入生成模型训练，并在推理后用专门的优化器或物理验证模块兜底**。
