---
tags:
  - 灵巧手专项
  - paperlocus
  - safe_reinforcement_learning
  - constrained_policy_optimization
  - trust_region
paper:
  title: "Constrained Policy Optimization"
  authors: "Joshua Achiam, David Held, Aviv Tamar, Pieter Abbeel"
  venue: "ICML 2017"
  arxiv: "1705.10528"
local_pdf: "../PDFs/Constrained Policy Optimization.pdf"
created: 2026-07-05
status: learning-note
---

# CPO 核心算法理论逐步推导：输入如何变成安全策略更新

这份笔记围绕 Achiam 等人的论文 **Constrained Policy Optimization** 展开，目标不是只复述论文摘要，而是把 CPO 的核心算法理论按“输入如何一步步变成输出”的顺序拆开讲清楚。你可以把 CPO 理解成 TRPO 的安全约束版本：TRPO 关心“新策略不要离旧策略太远，所以训练不要崩”，CPO 进一步关心“新策略不要离旧策略太远，并且这一小步更新以后，安全成本也不要超过限制”。这两个要求合在一起，就形成了 CPO 的核心：在一个 KL 信任域内，同时最大化奖励并满足成本约束。

为了适合本科生阅读，下面会先从强化学习的输入输出开始，再进入 CMDP、性能差分公式、CPO 的理论界、局部二次规划、对偶求解、回溯线搜索和恢复步骤。读这篇笔记时，不需要先完全掌握凸优化或自然梯度，但最好知道基本的 MDP、策略、回报、梯度下降这些概念。遇到公式时，先抓住它在算法链条里的作用，再回头看它的严格推导，会轻松很多。

## 1. CPO 想解决的到底是什么问题

普通强化学习通常只给智能体一个奖励函数 $R$，然后让它寻找一个策略 $\pi$，使长期累计奖励 $J(\pi)$ 尽可能大。这个设定在游戏里常常够用，因为智能体可以随便试错，失败了重新开始就行。但在机器人、灵巧手、自动驾驶、人机交互这些场景中，“随便试错”是不现实的，因为某些探索动作可能会损坏硬件、撞到人、超过关节力矩限制，或者让手指和物体发生危险接触。

因此，CPO 采用的是 **Constrained Markov Decision Process, CMDP** 的设定。这个设定不只给奖励函数，还额外给一个或多个成本函数 $C_i$，每个成本函数都有一个允许上限 $d_i$。算法的目标不再只是“奖励最大”，而是“在所有安全成本都不超过阈值的前提下，让奖励最大”。这就是 CPO 和普通 policy gradient、TRPO、PPO 最关键的区别。

用一句话概括，CPO 的核心任务是：给定当前策略、采样轨迹、奖励信号、安全成本信号和约束阈值，计算一个新的策略参数，使奖励尽量上升，同时成本约束在每次迭代中都接近满足。它不是等训练结束后才希望策略安全，而是在训练过程中的每一步都试图控制约束违反。

## 2. 输入和输出先摆清楚

在第 $k$ 次迭代时，CPO 的直接输入可以理解为一组对象。第一类输入是环境和任务定义，包括状态空间 $S$、动作空间 $A$、转移概率 $P$、奖励函数 $R$、折扣因子 $\gamma$、成本函数 $C_1,\dots,C_m$ 以及对应的成本上限 $d_1,\dots,d_m$。这些东西定义了“什么叫做任务做得好”和“什么叫做违反安全限制”。

第二类输入是当前策略 $\pi_{\theta_k}$，其中 $\theta_k$ 是神经网络策略的参数。策略输入状态 $s$，输出动作分布 $\pi_{\theta_k}(a|s)$。在连续控制任务中，这个动作分布常常是高斯分布，神经网络输出均值，方差可以是单独学习的参数。CPO 每次并不是从零训练一个策略，而是在当前策略附近找一个小更新。

第三类输入是一批由当前策略采样得到的轨迹数据 $D=\{\tau\}$。每条轨迹大致长这样：

$$
\tau=(s_0,a_0,r_0,c_{1,0},\dots,s_1,a_1,r_1,c_{1,1},\dots)
$$

这些轨迹提供了算法估计梯度、优势函数、当前成本违反程度和 KL 曲率所需的数据。由于 CPO 是 on-policy 算法，它主要依赖当前策略采出来的数据，而不是依赖一个长期 replay buffer。这个特点很重要，因为它后面的理论界就是围绕“用当前策略的数据估计新策略局部变化”展开的。

最终输出是新的策略参数 $\theta_{k+1}$。更具体地说，CPO 先求一个候选参数变化量 $\Delta\theta$，然后通过**回溯线搜索**把这一步缩小到足够可靠，最后得到：

$$
\theta_{k+1}=\theta_k+\alpha_{\text{line}}\Delta\theta
$$

这里的 $\alpha_{\text{line}}$ 是线搜索选出的缩放系数。这个输出不是一个最终答案，而是下一轮训练的起点；CPO 就是反复执行“采样、估计、求安全更新、线搜索、更新策略”这个循环。

## 3. 从 MDP 到 CMDP：为什么要引入成本回报

在普通 MDP 中，策略 $\pi$ 的目标函数通常写成折扣累计奖励：

$$
J(\pi)=\mathbb{E}_{\tau\sim\pi}\left[\sum_{t=0}^{\infty}\gamma^t R(s_t,a_t,s_{t+1})\right]
$$

这里 $\tau\sim\pi$ 表示轨迹是由策略 $\pi$ 和环境转移共同产生的。$\gamma\in[0,1)$ 是折扣因子，它让越晚发生的奖励权重越小。强化学习的普通目标就是找一个策略 $\pi^\star$，使 $J(\pi)$ 最大。

在 CMDP 中，每个成本函数 $C_i$ 也有自己的折扣累计成本：

$$
J_{C_i}(\pi)=\mathbb{E}_{\tau\sim\pi}\left[\sum_{t=0}^{\infty}\gamma^t C_i(s_t,a_t,s_{t+1})\right]
$$

如果 $C_i$ 表示撞墙、越界、碰到危险区域、超力矩或接触不稳定，那么 $J_{C_i}(\pi)$ 就是在长期意义上衡量策略有多“不安全”。约束阈值 $d_i$ 表示我们最多允许多少这样的成本。于是可行策略集合写成：

$$
\Pi_C=\{\pi\in\Pi:\forall i,\ J_{C_i}(\pi)\le d_i\}
$$

CMDP 的理想优化问题就是：

$$
\pi^\star=\arg\max_{\pi\in\Pi_C}J(\pi)
$$

这句话非常关键。它说明 CPO 不是把安全写成一个普通 reward penalty，而是把安全写成约束。惩罚项的思想是“违反了就扣分”，但约束的思想是“这个边界不能轻易越过”。这也是为什么 CPO 要求解带约束的优化问题，而不是只把成本乘上一个固定系数加到 reward 里面。

## 4. 局部策略搜索：为什么只在当前策略附近找下一步

对于神经网络策略，直接在所有策略中求 $\pi^\star$ 不现实，因为策略参数维度很高，环境动态未知，真实回报也只能通过采样估计。CPO 采用的是局部策略搜索思路：不要一次跳到全局最优，而是在当前策略 $\pi_k$ 附近找一个更好的策略 $\pi_{k+1}$。这个思路和 TRPO 一样，背后的直觉是“每次小心迈一步，长期就能稳定进步”。

论文把普通局部策略搜索写成：

$$
\pi_{k+1}=\arg\max_{\pi\in\Pi_\theta} J(\pi)
\quad
\text{s.t.}\quad
D(\pi,\pi_k)\le\delta
$$

这里 $D(\pi,\pi_k)$ 表示新旧策略之间的距离，$\delta$ 是允许迈出的最大步长。TRPO 选择平均 KL 散度作为距离，因此“新策略在旧策略附近”就变成“新旧策略的平均 KL 不超过一个小常数”。这会防止神经网络策略一次更新太大，导致性能突然崩掉。

在 CMDP 中，我们还要加上成本约束，于是理想的局部更新变成：

$$
\pi_{k+1}=\arg\max_{\pi\in\Pi_\theta} J(\pi)
$$

$$
\text{s.t.}\quad
J_{C_i}(\pi)\le d_i,\ i=1,\dots,m,
\quad
D(\pi,\pi_k)\le\delta
$$

这个式子表达了 CPO 最原始的目标：在当前策略附近找一个新策略，让奖励更大，同时所有成本都不超过限制。问题是，这个目标看起来清楚，实际却很难直接求解，因为我们不知道任意候选新策略 $\pi$ 的真实 $J(\pi)$ 和 $J_{C_i}(\pi)$。如果每试一个候选策略都要去环境里重新采样评估，计算量会非常大，估计方差也会很高。

## 5. 第一个关键公式：性能差分恒等式

CPO 的理论从一个经典公式开始，它说明两个策略的回报差异可以用旧策略的 advantage 来表示。先定义当前策略 $\pi$ 下的价值函数和优势函数：

$$
V^\pi(s)=\mathbb{E}_{\tau\sim\pi}[R(\tau)|s_0=s]
$$

$$
Q^\pi(s,a)=\mathbb{E}_{\tau\sim\pi}[R(\tau)|s_0=s,a_0=a]
$$

$$
A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s)
$$

优势函数 $A^\pi(s,a)$ 的意思是：在状态 $s$ 下采取动作 $a$，比按照当前策略平均行动要好多少。如果 $A^\pi(s,a)>0$，说明这个动作比当前策略的平均表现更好；如果小于 0，说明它比较差。policy gradient 类算法本质上就是想提高高优势动作的概率，降低低优势动作的概率。

论文使用的性能差分恒等式是：

$$
J(\pi')-J(\pi)
=
\frac{1}{1-\gamma}
\mathbb{E}_{s\sim d^{\pi'},a\sim\pi'}[A^\pi(s,a)]
$$

这里 $d^{\pi'}$ 是新策略 $\pi'$ 诱导的折扣状态访问分布。这个公式非常漂亮，因为它把“新策略比旧策略好多少”转化成“新策略会访问哪些状态，并在这些状态下选择了旧策略看来多有优势的动作”。如果新策略经常选择旧策略认为 advantage 为正的动作，那么它的回报就会提升。

但是这个公式不能直接用来做更新，因为期望里的状态分布是 $d^{\pi'}$，也就是新策略的状态分布。我们现在只有旧策略 $\pi$ 采出来的数据，并没有新策略 $\pi'$ 的轨迹。如果为了评估每个候选 $\pi'$ 都重新采样，那局部优化就不可行了。因此 CPO 和 TRPO 都要解决同一个核心困难：如何用旧策略数据近似新策略表现，同时知道这个近似误差不会太离谱。

## 6. CPO 的理论界：用策略距离控制近似误差

CPO 的核心理论贡献之一，是给出了一个把回报差异和策略平均散度联系起来的界。直观讲，它说的是：如果新策略 $\pi'$ 和旧策略 $\pi$ 在平均意义下差得不远，那么用旧策略状态分布 $d^\pi$ 来近似新策略状态分布 $d^{\pi'}$，误差是可以被控制的。这个“差得不远”先用 total variation 距离表示，后来通过 Pinsker 不等式转成 KL 距离，这就和 TRPO 的 KL trust region 接上了。

对于奖励，CPO 得到的下界可以写成直观形式：

$$
J(\pi')-J(\pi)
\ge
\frac{1}{1-\gamma}
\mathbb{E}_{s\sim d^\pi,a\sim\pi'}[A^\pi(s,a)]
-
\text{一个和策略距离有关的误差项}
$$

这条式子的含义是：如果用旧策略访问过的状态来估计新策略动作的 advantage，那么这只是一个 surrogate，不是精确回报提升。为了让这个 surrogate 可靠，必须减掉一个保守误差项。新旧策略越接近，这个误差项越小；新旧策略差得越远，这个误差项越大。

对于成本，CPO 使用的是类似的上界：

$$
J_{C_i}(\pi')-J_{C_i}(\pi)
\le
\frac{1}{1-\gamma}
\mathbb{E}_{s\sim d^\pi,a\sim\pi'}[A^\pi_{C_i}(s,a)]
+
\text{一个和策略距离有关的误差项}
$$

奖励要用下界，是因为我们想保证“最差情况下奖励也不会降太多”；成本要用上界，是因为我们想保证“最差情况下成本也不会超过太多”。这就是 CPO 设计中很精妙的一点：它不是对奖励和成本做同一种近似，而是按优化目标的方向选择保守界。奖励是越大越好，所以看保守下界；成本是越小越好，所以看保守上界。

论文进一步用 Pinsker 不等式把 TV 距离换成 KL 距离：

$$
D_{\mathrm{TV}}(p\|q)
\le
\sqrt{\frac{1}{2}D_{\mathrm{KL}}(p\|q)}
$$

这一步的意义非常大。TRPO 已经使用平均 KL 散度作为信任域约束，所以 CPO 可以继承 TRPO 的几何结构。换句话说，CPO 不需要发明一个全新的“策略距离”，而是在 TRPO 的 KL 球内加入成本约束，并用理论界说明：只要新策略留在这个 KL 球里，用旧数据构造的 surrogate 就有可解释的误差控制。

## 7. 从理论界到 CPO 的信任域更新

有了上面的理论界，CPO 的理论更新可以写成一个 trust-region 约束优化问题。它的目标是最大化奖励 advantage 的 surrogate：

$$
\max_{\pi\in\Pi_\theta}
\mathbb{E}_{s\sim d^{\pi_k},a\sim\pi}
\left[A^{\pi_k}(s,a)\right]
$$

这个目标的意思是：在旧策略 $\pi_k$ 经常访问的状态上，让新策略更偏向旧策略认为 advantage 高的动作。这里的优势函数来自旧策略，所以可以用当前采样数据估计。这个目标是 TRPO 里常见的 surrogate objective，CPO 沿用了它。

然后 CPO 给每个成本都加上 surrogate 约束：

$$
J_{C_i}(\pi_k)
+
\frac{1}{1-\gamma}
\mathbb{E}_{s\sim d^{\pi_k},a\sim\pi}
\left[A^{\pi_k}_{C_i}(s,a)\right]
\le d_i
$$

这条约束的意思是：当前策略已经有一个成本 $J_{C_i}(\pi_k)$，新策略相对于当前策略会造成一个估计的成本变化。如果这个“当前成本 + 预测成本变化”不超过阈值 $d_i$，我们就认为新策略在局部近似下是安全的。注意它约束的是成本 surrogate，而不是直接约束真实 $J_{C_i}(\pi)$，因为真实值在候选策略上很难直接评估。

最后加入平均 KL 信任域：

$$
\bar{D}_{\mathrm{KL}}(\pi\|\pi_k)\le\delta
$$

这三个部分合起来，就是论文中的 CPO update。用自然语言说，它每次都在问：在不离当前策略太远的所有候选策略里，有没有一个策略能提高奖励，并且预测出来的成本不超过限制？如果有，就选择其中奖励 surrogate 最大的那个。这个问题就是 CPO 从理论到算法的中心桥梁。

## 8. 为什么还要近似成参数空间里的 QP

上面的 CPO update 仍然是在“策略函数空间”里写的，也就是直接对 $\pi$ 做优化。但实际训练中，我们并不能任意指定一个抽象策略函数，而是有一个神经网络策略 $\pi_\theta$。所以真正能改的是神经网络参数 $\theta$，而不是直接改 $\pi$ 本身。第 $k$ 轮当前策略是 $\pi_{\theta_k}$，下一轮策略是 $\pi_{\theta}$，于是我们把参数变化写成：

$$
x=\theta-\theta_k
$$

接下来要做的事情，就是把论文中的策略空间 CPO update：

$$
\pi_{k+1}
=
\arg\max_{\pi\in\Pi_\theta}
\mathbb{E}_{s\sim d^{\pi_k},a\sim\pi}
\left[A^{\pi_k}(s,a)\right]
$$

$$
\text{s.t.}\quad
J_{C_i}(\pi_k)
+
\frac{1}{1-\gamma}
\mathbb{E}_{s\sim d^{\pi_k},a\sim\pi}
\left[A^{\pi_k}_{C_i}(s,a)\right]
\le d_i,\quad i=1,\dots,m
$$

$$
\bar D_{\mathrm{KL}}(\pi\|\pi_k)\le\delta
$$

转换成参数空间里的优化问题。这个转换分三步：先把 $\pi$ 换成 $\pi_\theta$，再在 $\theta_k$ 附近做 Taylor 展开，最后丢掉对优化没有影响的常数项。这样就会自然得到一个目标线性、成本约束线性、KL 约束二次的 QP。

先看奖励目标。把 $\pi$ 写成 $\pi_\theta$ 后，奖励 surrogate 是：

$$
L(\theta)
=
\mathbb{E}_{s\sim d^{\pi_k},a\sim\pi_\theta}
\left[A^{\pi_k}(s,a)\right]
$$

这个式子里，状态分布固定为旧策略的 $d^{\pi_k}$，但是动作来自新策略 $\pi_\theta$。训练时我们手里的样本动作其实是旧策略 $\pi_{\theta_k}$ 采出来的，所以为了用旧数据估计这个新策略期望，需要用 importance sampling ratio 改写：

$$
L(\theta)
=
\mathbb{E}_{s\sim d^{\pi_k},a\sim\pi_{\theta_k}}
\left[
\frac{\pi_\theta(a|s)}{\pi_{\theta_k}(a|s)}
A^{\pi_k}(s,a)
\right]
$$

这里的比例

$$
r_\theta(s,a)
=
\frac{\pi_\theta(a|s)}{\pi_{\theta_k}(a|s)}
$$

表示新策略相对于旧策略，是更重视还是更不重视旧数据里采到的这个动作。现在 $L(\theta)$ 已经变成了一个关于参数 $\theta$ 的函数。因为 CPO 每次只允许在 KL 信任域里走小步，所以我们在 $\theta_k$ 附近对它做一阶 Taylor 展开：

$$
L(\theta_k+x)
\approx
L(\theta_k)
+
\nabla_\theta L(\theta)\big|_{\theta=\theta_k}^{\top}x
$$

定义：

$$
g
=
\nabla_\theta L(\theta)\big|_{\theta=\theta_k}
$$

于是奖励目标近似为：

$$
L(\theta_k+x)
\approx
L(\theta_k)+g^\top x
$$

优化时 $L(\theta_k)$ 是常数，不会影响哪个 $x$ 最优，所以可以丢掉。于是奖励目标就变成：

$$
\max_x\quad g^\top x
$$

这就是 $g^\top x$ 的来源。它不是凭空写出来的，而是把奖励 surrogate 当作参数函数以后，在当前参数附近做一阶 Taylor 展开得到的。$g$ 是当前点的斜率，$x$ 是你准备走的一小步，$g^\top x$ 就是“这一步预计让奖励 surrogate 增加多少”。

接着看第 $i$ 个成本约束。CPO 的成本 surrogate 可以写成：

$$
G_i(\theta)
=
J_{C_i}(\pi_{\theta_k})
+
\frac{1}{1-\gamma}
\mathbb{E}_{s\sim d^{\pi_k},a\sim\pi_\theta}
\left[A^{\pi_k}_{C_i}(s,a)\right]
-d_i
$$

约束就是：

$$
G_i(\theta)\le0
$$

这里要注意，第一项 $J_{C_i}(\pi_{\theta_k})$ 是当前旧策略的成本回报，是固定数；第二项是新策略相对于旧策略的预测成本变化；最后减去阈值 $d_i$。和奖励一样，第二项也可以用旧策略样本加 ratio 改写：

$$
G_i(\theta)
=
J_{C_i}(\pi_{\theta_k})-d_i
+
\frac{1}{1-\gamma}
\mathbb{E}_{s\sim d^{\pi_k},a\sim\pi_{\theta_k}}
\left[
\frac{\pi_\theta(a|s)}{\pi_{\theta_k}(a|s)}
A^{\pi_k}_{C_i}(s,a)
\right]
$$

现在它也是一个关于 $\theta$ 的函数。对它在 $\theta_k$ 附近做一阶 Taylor 展开：

$$
G_i(\theta_k+x)
\approx
G_i(\theta_k)
+
\nabla_\theta G_i(\theta)\big|_{\theta=\theta_k}^{\top}x
$$

因为在精确 advantage 下，每个状态处都有：

$$
\mathbb{E}_{a\sim\pi_{\theta_k}}
\left[A^{\pi_k}_{C_i}(s,a)\right]
=0
$$

所以当 $\theta=\theta_k$ 时，ratio 等于 1，成本 advantage 的期望为 0，约束函数的当前值就只剩下：

$$
G_i(\theta_k)
=
J_{C_i}(\pi_{\theta_k})-d_i
$$

定义：

$$
c_i
=
J_{C_i}(\pi_{\theta_k})-d_i
$$

再定义成本约束的局部梯度：

$$
b_i
=
\nabla_\theta G_i(\theta)\big|_{\theta=\theta_k}
$$

于是成本约束就变成：

$$
c_i+b_i^\top x\le0
$$

这一步正是从非线性的、含条件期望的成本约束变成线性约束的关键。$c_i$ 负责告诉你当前策略已经离安全线多远，$b_i^\top x$ 负责预测如果参数走 $x$ 这一步，成本会增加还是减少。二者相加仍然必须小于等于 0，表示这一步更新后在局部近似下仍然满足约束。

KL 约束做二阶展开：

$$
\bar{D}_{\mathrm{KL}}(\pi_{\theta_k+x}\|\pi_{\theta_k})
\approx
\frac{1}{2}x^\top Hx
$$

这一段是 CPO/TRPO 从“策略不能变太多”走向“参数空间椭球约束”的关键。先把平均 KL 写完整。旧策略是 $\pi_{\theta_k}$，候选新策略是 $\pi_{\theta}$，论文中的平均 KL 可以理解为在旧策略访问到的状态上，对新旧动作分布的 KL 做平均：

$$
\bar D_{\mathrm{KL}}(\pi_\theta\|\pi_{\theta_k})
=
\mathbb{E}_{s\sim d^{\pi_k}}
\left[
D_{\mathrm{KL}}
\left(
\pi_\theta(\cdot|s)
\|
\pi_{\theta_k}(\cdot|s)
\right)
\right]
$$

这里的 $D_{\mathrm{KL}}(\pi_\theta(\cdot|s)\|\pi_{\theta_k}(\cdot|s))$ 比较的是同一个状态 $s$ 下，两个策略输出的动作分布差多少。比如连续控制里常用高斯策略，$\pi_\theta(\cdot|s)$ 和 $\pi_{\theta_k}(\cdot|s)$ 就是两个高斯分布；如果新策略的均值或方差变化很大，KL 就会变大。平均 KL 的作用就是：不是只看某一个状态，而是在旧策略经常访问的状态上整体限制策略变化。

现在令：

$$
K(\theta)
=
\bar D_{\mathrm{KL}}(\pi_\theta\|\pi_{\theta_k})
$$

我们想在 $\theta_k$ 附近近似 $K(\theta_k+x)$。对任意足够光滑的标量函数，二阶 Taylor 展开是：

$$
K(\theta_k+x)
\approx
K(\theta_k)
+
\nabla_\theta K(\theta)\big|_{\theta=\theta_k}^{\top}x
+
\frac{1}{2}
x^\top
\nabla_\theta^2K(\theta)\big|_{\theta=\theta_k}
x
$$

接下来逐项看。第一项 $K(\theta_k)$ 等于 0，因为当 $\theta=\theta_k$ 时，新策略和旧策略完全一样：

$$
K(\theta_k)
=
\bar D_{\mathrm{KL}}(\pi_{\theta_k}\|\pi_{\theta_k})
=0
$$

第二项也等于 0，因为 KL 散度在两个分布相同时达到最小值。直观说，如果你站在 $\theta_k$ 这个点上，往任意方向走一点点，KL 不可能出现“一阶线性下降”，因为它已经是最小的 0 了；所以它在这个点的一阶导数为 0：

$$
\nabla_\theta K(\theta)\big|_{\theta=\theta_k}
=0
$$

于是 Taylor 展开只剩下二阶项：

$$
K(\theta_k+x)
\approx
\frac{1}{2}
x^\top
\nabla_\theta^2K(\theta)\big|_{\theta=\theta_k}
x
$$

定义：

$$
H
=
\nabla_\theta^2K(\theta)\big|_{\theta=\theta_k}
$$

就得到：

$$
\bar{D}_{\mathrm{KL}}(\pi_{\theta_k+x}\|\pi_{\theta_k})
\approx
\frac{1}{2}x^\top Hx
$$

所以这里的 $H$ 不是任意矩阵，而是“平均 KL 在当前策略参数处的二阶曲率”。它告诉我们：参数往某个方向变化时，策略分布会变得多快。如果某个方向上 $x^\top Hx$ 很大，说明参数虽然可能只动了一点，但策略输出分布已经变化很明显；如果某个方向上 $x^\top Hx$ 很小，说明这个方向对策略分布影响较小。

这也是为什么 $H$ 常被称为 Fisher information matrix。更直观地说，Fisher 矩阵衡量的是“参数变化对概率分布的敏感程度”。在策略梯度里，我们不是真的关心参数的欧氏距离 $\|x\|_2$ 有多大，而是关心策略分布到底变了多少。两个参数向量在欧氏距离上可能差不多，但一个方向会让动作分布剧烈变化，另一个方向只让动作分布轻微变化；KL 二阶项正是用来区分这两种情况的。

如果只做一阶展开，会发生什么？因为 $K(\theta_k)=0$ 且 $\nabla K(\theta_k)=0$，一阶近似会给出：

$$
K(\theta_k+x)
\approx
0
$$

这就完全失去了约束作用。无论 $x$ 取多大，一阶近似都说 KL 近似为 0，优化器就不知道“新策略不能离旧策略太远”。因此 reward 和 cost 可以用一阶展开，是因为它们的一阶项已经能描述局部增减趋势；但 KL 作为距离函数，在当前点的一阶项天然消失，必须保留二阶项才能形成有效的 trust region。

最后看这个约束的几何意义：

$$
\frac{1}{2}x^\top Hx\le\delta
$$

如果 $H=I$，它就是普通欧氏球：

$$
\frac{1}{2}\|x\|_2^2\le\delta
$$

但实际 $H$ 通常不是单位矩阵，所以它定义的是一个椭球。椭球在某些方向上窄，表示那些方向会让策略分布快速变化，因此只能走小步；在另一些方向上宽，表示那些方向对策略分布影响较小，因此可以走得稍大。这就是 TRPO/CPO 里的“信任域”：它不是限制参数本身不要动太多，而是限制策略行为分布不要变太多。

于是 CPO 的实际近似问题变成论文中的二次规划：

$$
\max_x\quad g^\top x
$$

$$
\text{s.t.}\quad c_i+b_i^\top x\le 0,\ i=1,\dots,m
$$

$$
\frac{1}{2}x^\top Hx\le\delta
$$

这就是 CPO 算法的核心计算问题。输入是 $g,b_i,c_i,H,\delta$，输出是参数更新方向 $x^\star$。它的目标是线性的，成本约束是线性的，KL 信任域是二次的；由于 $H$ 半正定或近似正定，这个问题可以看作一个凸优化问题，因此可以用对偶方法高效求解。

## 9. 这些量如何从轨迹数据中估计出来

现在把算法链条再往前推一层。第 8 节说明了，只要有 $g,b_i,c_i,H$，CPO 就能构造局部 QP。但这些量并不是环境直接给出的，而是由当前策略采样到的轨迹估计出来的。第 $k$ 轮先用 $\pi_{\theta_k}$ 和环境交互，得到一批轨迹：

$$
D
=
\{\tau_j\}_{j=1}^{M},
\quad
\tau_j=(s_0,a_0,r_0,c_{1,0},\dots,s_1,a_1,r_1,c_{1,1},\dots)
$$

这些轨迹同时服务于四件事：估计当前成本违反量 $c_i$，估计奖励 advantage，估计成本 advantage，估计平均 KL 的二阶曲率 $H$。它们共同把“环境交互数据”变成“QP 的系数”。

先看 $c_i$。它来自当前策略的真实成本回报估计，不需要求梯度。对每条轨迹，先算第 $i$ 个成本的折扣累计值：

$$
\widehat{J}_{C_i}^{(j)}
=
\sum_{t=0}^{T-1}
\gamma^t
C_i(s_t^{(j)},a_t^{(j)},s_{t+1}^{(j)})
$$

然后对 $M$ 条轨迹取平均：

$$
\widehat{J}_{C_i}(\pi_{\theta_k})
=
\frac{1}{M}
\sum_{j=1}^{M}
\widehat{J}_{C_i}^{(j)}
$$

于是：

$$
\hat c_i
=
\widehat{J}_{C_i}(\pi_{\theta_k})-d_i
$$

如果使用 cost shaping，那么这里的 $C_i$ 会换成更保守的 $C_i^+$。无论用原始成本还是 shaped cost，$c_i$ 的意义都一样：它是当前策略相对于约束阈值的余量或违反量。

接着看 advantage。奖励 advantage 可以粗略理解为：

$$
A^{\pi_k}(s_t,a_t)
\approx
\text{从 }t\text{ 开始实际得到的未来奖励}
-
\text{当前状态的平均未来奖励}
$$

最朴素的 Monte Carlo 估计是：

$$
\hat A_t
=
\left(
\sum_{\ell=0}^{T-t-1}
\gamma^\ell r_{t+\ell}
\right)
-
V_{\psi}(s_t)
$$

实际实现里常用 GAE-$\lambda$ 降低方差。先定义奖励 TD residual：

$$
\delta_t^R
=
r_t+\gamma V_{\psi}(s_{t+1})-V_{\psi}(s_t)
$$

再累加得到：

$$
\hat A_t
=
\sum_{\ell=0}^{T-t-1}
(\gamma\lambda)^\ell
\delta_{t+\ell}^R
$$

成本 advantage 完全类似，只是把 reward value function 换成 cost value function。对第 $i$ 个成本，先训练或估计一个 $V_{C_i,\phi}(s)$，再定义：

$$
\delta_{t}^{C_i}
=
C_i(s_t,a_t,s_{t+1})
+
\gamma V_{C_i,\phi}(s_{t+1})
-
V_{C_i,\phi}(s_t)
$$

然后：

$$
\hat A^{C_i}_t
=
\sum_{\ell=0}^{T-t-1}
(\gamma\lambda_C)^\ell
\delta_{t+\ell}^{C_i}
$$

有了这些 advantage，就能估计 $g$ 和 $b_i$。第 8 节里我们把奖励 surrogate 写成样本形式：

$$
\hat L(\theta)
=
\frac{1}{N}
\sum_{t=1}^{N}
\frac{\pi_\theta(a_t|s_t)}
{\pi_{\theta_k}(a_t|s_t)}
\hat A_t
$$

这里 $N$ 是所有轨迹中采样 transition 的总数。对 $\theta$ 求梯度，并在 $\theta=\theta_k$ 处计算：

$$
\hat g
=
\nabla_\theta \hat L(\theta)\big|_{\theta=\theta_k}
$$

利用：

$$
\nabla_\theta
\frac{\pi_\theta(a_t|s_t)}
{\pi_{\theta_k}(a_t|s_t)}
=
\frac{\pi_\theta(a_t|s_t)}
{\pi_{\theta_k}(a_t|s_t)}
\nabla_\theta\log\pi_\theta(a_t|s_t)
$$

而在 $\theta=\theta_k$ 时，ratio 等于 1，所以：

$$
\hat g
=
\frac{1}{N}
\sum_{t=1}^{N}
\nabla_\theta
\log\pi_\theta(a_t|s_t)
\big|_{\theta=\theta_k}
\hat A_t
$$

这就是 policy gradient 的样本估计形式。它说明 $g$ 不是额外假设出来的，而是“对 ratio surrogate 求导”自然得到的。正 advantage 动作会推动参数增加其概率，负 advantage 动作会推动参数降低其概率。

成本梯度 $b_i$ 也是同一个过程。第 $i$ 个成本约束 surrogate 的样本形式可以写成：

$$
\hat G_i(\theta)
=
\hat c_i
+
\frac{1}{N}
\sum_{t=1}^{N}
\frac{\pi_\theta(a_t|s_t)}
{\pi_{\theta_k}(a_t|s_t)}
\hat A^{C_i}_t
$$

这里为了讲解简洁，把论文中由 $d^{\pi_k}$ 归一化带来的常数因子吸收到 advantage 或样本平均的尺度里；实现时只要 $g,b_i,c_i$ 的尺度和约束阈值保持一致即可。对这个约束 surrogate 求梯度：

$$
\hat b_i
=
\nabla_\theta \hat G_i(\theta)\big|_{\theta=\theta_k}
\approx
\frac{1}{N}
\sum_{t=1}^{N}
\nabla_\theta\log\pi_\theta(a_t|s_t)
\big|_{\theta=\theta_k}
\hat A^{C_i}_t
$$

这个式子和 $\hat g$ 几乎一样，只是 reward advantage 换成了 cost advantage。它告诉 CPO：哪些参数变化会让第 $i$ 个成本升高或降低。后面求 QP 时，如果一个更新方向同时让 $g^\top x$ 很大、但也让 $b_i^\top x$ 很大，CPO 就会通过约束或对偶变量把这一步压回来。

最后看 $H$。先用当前采样到的状态构造平均 KL 的样本估计：

$$
\hat K(\theta)
=
\frac{1}{N}
\sum_{t=1}^{N}
D_{\mathrm{KL}}
\left(
\pi_\theta(\cdot|s_t)
\|
\pi_{\theta_k}(\cdot|s_t)
\right)
$$

在 $\theta=\theta_k$ 时，新旧策略相同，所以 $\hat K(\theta_k)=0$，并且：

$$
\nabla_\theta \hat K(\theta)\big|_{\theta=\theta_k}
=
0
$$

于是 $H$ 定义为它的 Hessian：

$$
\hat H
=
\nabla_\theta^2
\hat K(\theta)\big|_{\theta=\theta_k}
$$

这就是 KL 二阶近似的矩阵。对高斯策略来说，$D_{\mathrm{KL}}$ 通常有闭式表达，因此 $\hat K(\theta)$ 可以直接由网络输出的均值和方差算出来。由于神经网络参数很多，实际实现通常不会显式存储完整 $H$，而是只计算 Hessian-vector product：

$$
v\mapsto \hat H v
$$

然后用 conjugate gradient 近似求 $\hat H^{-1}\hat g$ 和 $\hat H^{-1}\hat b_i$。这就是为什么论文说不用真正反转 Fisher 矩阵。最终，轨迹数据经过这些估计步骤，形成：

$$
D
\to
\hat A_t,\hat A^{C_i}_t,\hat c_i,\hat K(\theta)
\to
\hat g,\hat b_i,\hat H
\to
\max_x \hat g^\top x
\quad
\text{s.t.}\quad
\hat c_i+\hat b_i^\top x\le0,\quad
\frac12x^\top\hat Hx\le\delta
$$

这就是从含条件期望和 $J$ 的公式，落到简洁 QP 形式的完整计算链。它的本质是：固定旧策略的状态分布，用 ratio 处理动作分布变化，用一阶 Taylor 近似 reward/cost surrogate，用二阶 Taylor 近似 KL trust region，再用采样平均替代理论期望。

## 10. 二次规划的几何直觉

这个 QP 可以用一个二维图像来理解，虽然真实参数空间可能有几千维。目标 $g^\top x$ 希望沿着奖励上升最快的方向走；KL 约束 $\frac{1}{2}x^\top Hx\le\delta$ 把可走范围限制在一个椭球里；每个成本约束 $c_i+b_i^\top x\le0$ 又把椭球切掉一部分，只留下不会让成本超过阈值的半空间。

如果没有成本约束，最优方向就是 TRPO 的自然梯度方向：

$$
x_{\text{TRPO}}
\propto
H^{-1}g
$$

这表示先用 $H^{-1}$ 把普通梯度变成自然梯度，再按 KL 半径缩放。自然梯度的直觉是：不要在参数空间里按欧氏距离看步长，而要按策略分布实际变化的大小看步长。这样更新更符合“策略不要变化太大”的目标。

加入成本约束后，CPO 不一定能沿着 $H^{-1}g$ 走。如果这个方向会让 $c_i+b_i^\top x$ 变成正数，也就是预计成本超过阈值，那么算法必须把方向往降低成本的方向拉回来。这个“拉回来”的强度不是手动调的，而是通过对偶变量 $\nu_i$ 自动算出来的。

## 11. 对偶问题：CPO 如何自动选择安全惩罚系数

上一节得到的局部 QP 是 CPO 的计算核心。为了看清楚对偶变量为什么像“自动安全惩罚系数”，我们先把这个 QP 重新写一遍。令 $x=\theta-\theta_k$ 表示本轮参数更新量，CPO 想解的是：

$$
\max_x\quad g^\top x
$$

$$
\text{s.t.}\quad
c_i+b_i^\top x\le0,\quad i=1,\dots,m
$$

$$
\frac{1}{2}x^\top Hx\le\delta
$$

这个问题的每一项都有明确含义。目标 $g^\top x$ 是“这一步预计能增加多少 reward surrogate”；线性约束 $c_i+b_i^\top x\le0$ 是“当前第 $i$ 个成本离安全线的距离，加上本步预计造成的成本变化，不能超过 0”；二次约束 $\frac12x^\top Hx\le\delta$ 是“新旧策略的平均 KL 不能太大”。所以这个 QP 实际上是在问：**在 KL 允许的小椭球里，找一个最能提高奖励、又不越过成本边界的方向。**

为了让符号更紧凑，先把多个成本梯度拼成矩阵：

$$
B=[b_1,\dots,b_m]
$$

这里 $B$ 的每一列是一个成本约束的梯度。如果策略参数有 $n$ 维，并且有 $m$ 个成本约束，那么：

$$
B\in\mathbb{R}^{n\times m}
$$

再把当前违反量或余量拼成向量：

$$
c=[c_1,\dots,c_m]^\top
$$

于是所有成本约束可以合写为：

$$
B^\top x+c\le0
$$

注意这里是不等式向量，也就是每个分量都要小于等于 0。这样写以后，CPO 的 QP 变成：

$$
\max_x\quad g^\top x
$$

$$
\text{s.t.}\quad
B^\top x+c\le0,\quad
\frac12x^\top Hx\le\delta
$$

接下来进入对偶。对偶方法的核心思想是：把约束放进目标函数里，并给每个约束一个非负乘子。CPO 这里有两类约束，所以有两类乘子。

第一类是成本约束乘子：

$$
\nu=[\nu_1,\dots,\nu_m]^\top,\quad \nu_i\ge0
$$

每个 $\nu_i$ 对应一个成本约束 $c_i+b_i^\top x\le0$。它可以理解为“如果这个成本约束重要，本轮更新要给它多大的惩罚权重”。第二类是 KL 信任域乘子：

$$
\lambda\ge0
$$

它对应 $\frac12x^\top Hx\le\delta$，控制整体步长。$\lambda$ 越大，最后的 $x$ 越小；$\lambda$ 越小，更新步可以更大。

因为我们现在是最大化问题，对形如 $h(x)\le0$ 的约束，可以用 $-\nu h(x)$ 放进拉格朗日函数。对可行点来说 $h(x)\le0$，所以 $-\nu h(x)\ge0$，这相当于构造一个带约束惩罚的上界形式。CPO 的拉格朗日函数可以写成：

$$
\mathcal{L}(x,\lambda,\nu)
=
g^\top x
-
\nu^\top(B^\top x+c)
-
\lambda\left(
\frac12x^\top Hx-\delta
\right)
$$

把和 $x$ 有关的项整理一下：

$$
\mathcal{L}(x,\lambda,\nu)
=
(g-B\nu)^\top x
-
\frac{\lambda}{2}x^\top Hx
-
\nu^\top c
+
\lambda\delta
$$

这一步非常关键。它告诉我们，一旦给定 $\nu$，原来的奖励梯度 $g$ 会被改成：

$$
g-B\nu
$$

其中：

$$
B\nu=\nu_1b_1+\nu_2b_2+\dots+\nu_mb_m
$$

也就是说，$B\nu$ 是所有成本梯度的加权组合。于是 $g-B\nu$ 就可以理解为“扣掉危险方向后的奖励梯度”。如果某个成本约束的乘子 $\nu_i$ 很大，那么对应的成本梯度 $b_i$ 会被强烈扣除，更新方向就会远离会增加该成本的方向。这就是“安全惩罚系数”这个说法的来源。

现在固定 $\lambda,\nu$，对 $x$ 求最优。对 $\mathcal{L}$ 关于 $x$ 求导：

$$
\nabla_x\mathcal{L}
=
g-B\nu-\lambda Hx
$$

最优点满足一阶条件：

$$
g-B\nu-\lambda Hx=0
$$

于是：

$$
\lambda Hx=g-B\nu
$$

如果 $H$ 正定或经过阻尼后近似正定，就可以两边乘 $H^{-1}$：

$$
x
=
\frac{1}{\lambda}H^{-1}(g-B\nu)
$$

因此，求解对偶以后，CPO 的候选更新可以写成：

$$
x^\star
=
\frac{1}{\lambda^\star}
H^{-1}(g-B\nu^\star)
$$

这个式子非常值得细读。$g$ 是奖励梯度，表示如果不考虑安全，我们想往哪里走；$B\nu^\star$ 是成本梯度的加权组合，表示为了满足安全约束，需要从奖励方向中扣掉多少危险成分；$H^{-1}$ 表示在 KL 几何下计算自然方向，而不是在普通欧氏参数空间里走；$\frac{1}{\lambda^\star}$ 表示根据 KL 信任域缩放整体步长。

如果所有成本约束都不重要，也就是 $\nu^\star=0$，那么：

$$
x^\star
=
\frac{1}{\lambda^\star}H^{-1}g
$$

这就退化成 TRPO 的自然梯度方向。CPO 相比 TRPO 多出来的东西，正是 $-B\nu^\star$ 这一项。它让更新方向从“只顾奖励”变成“奖励方向减去安全风险方向”。

接下来要看 $\lambda,\nu$ 怎么被“自动选择”。把上面的最优 $x$ 代回拉格朗日函数，就可以得到只关于 $\lambda,\nu$ 的对偶问题。为了书写清楚，令：

$$
a(\nu)=g-B\nu
$$

则：

$$
x(\lambda,\nu)
=
\frac{1}{\lambda}H^{-1}a(\nu)
$$

代回后，关于 $x$ 的最大值为：

$$
\phi(\lambda,\nu)
=
\frac{1}{2\lambda}
a(\nu)^\top H^{-1}a(\nu)
-
\nu^\top c
+
\lambda\delta
$$

这是最大化原问题的一个对偶上界形式。不同教材或论文会把符号改写成等价的“最大化负对偶目标”，并且因为 KL 约束写成 $x^\top Hx\le\delta$ 或 $\frac12x^\top Hx\le\delta$ 的约定不同，$\lambda\delta$ 前可能出现一个常数因子；这些不影响核心结论。核心结构始终是：

$$
a(\nu)^\top H^{-1}a(\nu)
=
(g-B\nu)^\top H^{-1}(g-B\nu)
$$

这个式子说明，选 $\nu$ 本质上是在选择一个“修正后的梯度” $g-B\nu$，并且看它在 KL 几何下的大小。展开它：

$$
(g-B\nu)^\top H^{-1}(g-B\nu)
=
g^\top H^{-1}g
-
2g^\top H^{-1}B\nu
+
\nu^\top B^\top H^{-1}B\nu
$$

定义：

$$
q=g^\top H^{-1}g
$$

$$
r=B^\top H^{-1}g
$$

$$
S=B^\top H^{-1}B
$$

则展开式可以写成：

$$
q-2r^\top\nu+\nu^\top S\nu
$$

这样，对偶问题只需要在 $\lambda$ 和 $\nu$ 上求解。这里最重要的是维度变化：原来的 $x$ 是神经网络参数维度，可能是几万、几十万甚至更多；而 $\nu$ 的维度只是成本约束个数 $m$，$\lambda$ 只是 1 个标量。如果安全约束只有 1 到几个，对偶问题就比原始高维 QP 小得多。

再从 KKT 条件看 $\nu$ 的意义会更直观。对最优解，成本约束和乘子满足互补松弛：

$$
\nu_i^\star\ge0
$$

$$
c_i+b_i^\top x^\star\le0
$$

$$
\nu_i^\star(c_i+b_i^\top x^\star)=0
$$

第三行最关键。它表示两种情况只能二选一。

第一种情况：第 $i$ 个约束没有贴边，也就是：

$$
c_i+b_i^\top x^\star<0
$$

这说明更新后仍然有安全余量。为了让乘积为 0，必须有：

$$
\nu_i^\star=0
$$

也就是说，如果某个成本约束不紧，CPO 自动不给它惩罚权重。这时它不会干扰奖励优化。

第二种情况：第 $i$ 个约束正好贴边，也就是：

$$
c_i+b_i^\top x^\star=0
$$

这说明这个安全约束已经成为阻止继续沿奖励方向前进的边界。此时 $\nu_i^\star$ 可以大于 0，它就像一个“边界反作用力”，把更新方向从危险一侧推回来。

所以 $\nu_i^\star$ 不是普通手调 penalty，而是由当前局部几何自动决定的 shadow price。它回答的问题是：

> 如果我想多提高一点奖励，会让第 $i$ 个成本约束承受多大压力？

如果压力很小，$\nu_i^\star=0$；如果压力很大，$\nu_i^\star$ 变大，更新方向就会被明显修正。

再看 $\lambda$。KL 约束也有互补松弛：

$$
\lambda^\star\ge0
$$

$$
\frac12(x^\star)^\top Hx^\star\le\delta
$$

$$
\lambda^\star\left(
\frac12(x^\star)^\top Hx^\star-\delta
\right)=0
$$

通常只要 $g-B\nu^\star$ 不为 0，算法会把允许的 KL 半径用满，也就是：

$$
\frac12(x^\star)^\top Hx^\star=\delta
$$

这时 $\lambda^\star>0$，负责把方向缩放到信任域边界上。如果 $\lambda^\star$ 很大，说明为了满足 KL 限制，需要把步子缩得更小；如果 $\lambda^\star$ 较小，说明可以走得更大。

现在可以把整个对偶机制理解成一个“力平衡”问题。奖励梯度 $g$ 像一股拉力，想把策略往高奖励方向拉。每个成本约束的梯度 $b_i$ 像一条安全边界的法向量，告诉你往哪个方向走会让这个成本增加。乘子 $\nu_i$ 决定这个边界施加多大的反作用力。KL 矩阵 $H$ 则定义真实的运动几何：不是普通参数空间，而是策略分布空间。最终一阶最优条件：

$$
g-B\nu^\star-\lambda^\star Hx^\star=0
$$

可以改写成：

$$
g
=
B\nu^\star+\lambda^\star Hx^\star
$$

这句话非常有解释力：奖励想推动的方向 $g$，在最优点被两部分平衡了。一部分是成本约束的反作用 $B\nu^\star$，另一部分是 KL 信任域的反作用 $\lambda^\star Hx^\star$。如果没有成本边界反作用，就回到 TRPO；如果成本边界变得重要，$B\nu^\star$ 就会分走一部分奖励推动力。

这也是 CPO 与 primal-dual 方法的关键不同。普通 primal-dual 方法通常把 $\nu$ 当成跨迭代慢慢学习的参数，例如：

$$
\nu_{k+1}=(\nu_k+\alpha(J_C(\pi_k)-d))_+
$$

这种方法的问题是它只看已经发生的违反量，并且依赖学习率 $\alpha$ 慢慢调节。如果策略突然学会一种高奖励但高成本的行为，$\nu$ 可能还没来得及变大，策略就已经越过安全边界，出现 overshoot。CPO 不这样做。CPO 在每一轮都根据当前的：

$$
g,\quad B,\quad c,\quad H
$$

重新解一次局部约束优化问题，直接得到本轮的 $\lambda^\star,\nu^\star$。也就是说，它不是问“过去几轮违反了多少，所以我慢慢调 penalty”，而是问：

> 在当前策略附近，如果我要走一步，哪些成本约束会立刻变成瓶颈？为了不越界，本轮每个成本应该施加多大的反作用力？

这就是“自动选择安全惩罚系数”的真正含义。

如果只看单约束情形，直觉会更清楚。此时：

$$
B=b,\quad \nu\in\mathbb{R}_{\ge0}
$$

更新方向是：

$$
x^\star
=
\frac{1}{\lambda^\star}
H^{-1}(g-\nu^\star b)
$$

如果 $\nu^\star=0$，方向就是 TRPO：

$$
x^\star\propto H^{-1}g
$$

如果奖励方向会增加成本，$\nu^\star$ 会变大，方向就会从 $H^{-1}g$ 逐渐转向更少增加成本、甚至降低成本的方向。这里的 $\nu^\star b$ 就像从奖励梯度里扣掉一部分“危险分量”。这比固定 penalty 更灵活，因为 $\nu^\star$ 不是预设常数，而是由当前 $c$、$g$、$b$、$H$ 联合决定。

直观地说，$c$ 决定你离安全边界还有多远，$b$ 决定成本边界朝哪个方向，$g$ 决定奖励想往哪里走，$H$ 决定策略变化的真实几何。CPO 的对偶问题把这四件事放在一起，算出一个本轮最合适的安全惩罚强度 $\nu^\star$。这就是它比“固定惩罚项”或“慢慢学乘子”的 primal-dual 方法更稳的原因。


## 12. 单约束解析解的直觉

论文实验中主要使用一个成本约束，因此附录给了单约束情形的解析解。此时 QP 可以写成：

$$
\max_x\quad g^\top x
$$

$$
\text{s.t.}\quad b^\top x+c\le0,\quad x^\top Hx\le 2\delta
$$

为了理解解析解，论文定义了三个标量：

$$
q=g^\top H^{-1}g
$$

$$
r=g^\top H^{-1}b
$$

$$
s=b^\top H^{-1}b
$$

$q$ 可以看成奖励梯度在 KL 几何下的大小，表示如果只追求奖励，上升方向有多强。$s$ 可以看成成本梯度在 KL 几何下的大小，表示成本约束对参数变化有多敏感。$r$ 则表示奖励方向和成本方向的对齐程度：如果 $r$ 很大，说明提高奖励的方向也容易提高成本；如果 $r$ 较小或为负，说明提高奖励未必危险，甚至可能顺便降低成本。

对偶求解会得到类似下面的形式：

$$
\nu^\star(\lambda)
=
\left(\frac{\lambda c-r}{s}\right)_+
$$

这里 $(\cdot)_+$ 表示小于 0 就截断为 0。这个式子直观上很清楚：如果当前违反量 $c$ 越大，或者给定 $\lambda$ 下成本约束越紧，$\nu^\star$ 就越可能变大；如果奖励方向与成本方向的冲突不强，$\nu^\star$ 就可能为 0。然后算法再选择最合适的 $\lambda^\star$，得到最终步长。

本科阶段不必把附录里的所有分段投影公式一次背下来，但要抓住它的作用：解析解不是 CPO 理论的核心思想，而是让单约束版本更容易高效实现。真正关键的是，CPO 把“提高奖励但不能越过成本边界”转成了一个局部凸 QP，再通过对偶变量自动平衡奖励和成本。

## 13. 不可行时的恢复方向

有时当前策略已经违反约束，或者线性近似下的 QP 根本没有可行解。比如 $c>0$ 表示当前成本已经超过阈值，而在当前 KL 球内又找不到一个既满足线性成本约束又提高奖励的方向。这时继续追求奖励没有意义，算法需要先把策略拉回可行区域。

在单约束实验中，CPO 使用恢复方向：

$$
x_{\text{rec}}
=
-
\sqrt{\frac{2\delta}{b^\top H^{-1}b}}
H^{-1}b
$$

这个式子可以这样理解。$b$ 是成本梯度，沿着 $b$ 走会增加成本，因此沿着 $-H^{-1}b$ 的自然梯度方向走，会尽量降低成本。前面的平方根系数把这一步缩放到 KL 信任域边界上，让恢复动作在允许的最大局部步长内尽量有效。

恢复方向不追求奖励提升，它只解决一个问题：先让策略重新靠近安全可行区域。等策略不再明显违反约束，下一轮再回到正常 CPO 更新。论文也指出，这个恢复步骤在主文算法中主要针对单约束情形；如果多个成本约束同时违反，就需要更一般的 QP 投影或更复杂的恢复机制。

## 14. 回溯线搜索：为什么求出 QP 解后还不能直接更新

QP 解 $x^\star$ 来自局部近似，而真实神经网络策略和真实环境并不完全等于这个局部模型。一阶 reward 近似可能有误差，一阶 cost 近似可能有误差，二阶 KL 近似也可能不完全准确。尤其在采样噪声较大、优势估计不准或策略网络非线性很强时，直接使用 $x^\star$ 可能会造成实际 KL 超标或成本 surrogate 违反。

所以 CPO 在得到候选步以后，还要做 backtracking line search。它先尝试完整步长：

$$
\theta_{\text{try}}=\theta_k+x^\star
$$

如果这个候选策略通过了检查，也就是 KL 不超过限制、成本 surrogate 满足约束、奖励 surrogate 没有明显坏掉，就接受它。如果不通过，就把步长乘上一个小于 1 的系数，比如 $\beta$，再试：

$$
\theta_{\text{try}}=\theta_k+\beta x^\star
$$

如果还不行，就继续缩小为 $\beta^2x^\star,\beta^3x^\star$，直到通过检查或达到最大回溯次数。线搜索不是理论最漂亮的部分，但它是实践中非常重要的安全阀。它承认局部模型会犯错，并用更保守的实际检查来降低坏更新的概率。

## 15. Cost shaping：为什么要约束成本上界而不只是原始成本

论文还提出了 cost shaping，用一个更保守的成本 $C_i^+$ 替代原始成本：

$$
C_i^+(s,a,s')
=
C_i(s,a,s')+\Delta_i(s,a,s')
$$

这里 $\Delta_i$ 是额外的安全余量项。在实验中，作者把状态分成 safe 和 unsafe，并训练一个预测网络估计智能体在未来固定时间窗口内进入 unsafe 状态的概率。这个概率被加到成本里，相当于不仅惩罚已经发生的不安全事件，也提前惩罚“快要进入危险区域”的状态。

这样做有两个好处。第一，它让稀疏安全成本变得更平滑。如果只有真正撞到危险区域才有成本，成本信号可能太稀疏，算法很难提前学会避开危险。第二，它给近似误差留出安全缓冲。因为 CPO 的约束是基于 surrogate 和采样估计的，约束更保守一些可以减少真实成本越界的概率。

不过 cost shaping 也不是免费的。它引入了一个额外预测模型，模型本身可能有偏差；如果预测器在某些状态上不准，保守成本也可能误导策略。因此可以把 cost shaping 理解为工程上加强 CPO 稳定性的安全边际，而不是 CPO 理论本身不可缺少的核心。

## 16. Algorithm 1 逐行解释：输入如何一步步变成输出

下面按论文 Algorithm 1 的顺序，把 CPO 的完整迭代过程拆成“每一行在做什么”。这一节可以当作你之后读代码或复现算法时的主地图。

**Input: Initial policy $\pi_0\in\Pi_\theta$, tolerance $\alpha$。**  
算法从一个初始策略开始，通常是随机初始化的神经网络策略，也可以是预训练策略。这里的 tolerance 可以理解为线搜索或约束检查中的容忍参数，用来处理采样噪声和数值误差。初始策略最好是可行的，也就是成本不超过约束上限；如果一开始就严重违反约束，CPO 会更依赖恢复步骤。

**for $k=0,1,2,\dots$ do。**  
CPO 是迭代式算法，不会一次求出最终策略。每一轮都把当前策略当作局部参考点，在它附近建立一个可解的近似优化问题。完成更新后，新策略又成为下一轮的参考点。

**Sample a set of trajectories $D=\{\tau\}\sim\pi_k=\pi(\theta_k)$。**  
这一行把当前策略放进环境里运行，收集状态、动作、奖励和成本。所有后续估计都来自这批 on-policy 数据，所以采样质量非常重要。如果轨迹太少，优势估计和成本估计会很噪；如果轨迹覆盖不到危险边界附近，成本梯度也可能不可靠。

**Form sample estimates $\hat{g},\hat{b},\hat{H},\hat{c}$ with $D$。**  
这一行把原始轨迹转成 QP 所需的四类量。$\hat{g}$ 表示奖励提升方向，$\hat{b}$ 表示成本变化方向，$\hat{c}$ 表示当前离成本阈值还有多远，$\hat{H}$ 表示 KL 信任域的局部几何。到这一步，原始的“轨迹数据”已经变成了一个局部优化问题的参数。

**if approximate CPO is feasible then。**  
算法检查线性成本约束和二次 KL 球是否存在交集。如果存在可行解，说明在当前信任域内有希望找到一个既满足成本 surrogate 又提高奖励的更新。这个检查对应几何上的问题：椭球和成本半空间有没有重叠。

**Solve dual problem for $\lambda_k^\star,\nu_k^\star$。**  
如果近似问题可行，CPO 不直接在高维参数空间里暴力求 $x$，而是求低维对偶变量。$\lambda^\star$ 控制 KL 步长，$\nu^\star$ 控制成本约束的权重。由于成本约束数量 $m$ 通常远小于神经网络参数维度，解对偶问题比直接解原始高维 QP 更高效。

**Compute policy proposal $\theta^\star$ with the primal solution。**  
求出对偶变量后，算法用公式

$$
x^\star=\frac{1}{\lambda^\star}H^{-1}(g-B\nu^\star)
$$

得到候选更新，再令 $\theta^\star=\theta_k+x^\star$。这一步完成了“优化问题输出方向”的转换。注意 $\theta^\star$ 还不是最终接受的参数，因为它仍然基于近似模型。

**else compute recovery policy proposal。**  
如果近似 CPO 问题不可行，算法转向恢复步骤，沿着降低成本的自然梯度方向移动。此时 CPO 暂时不追求奖励最大化，而是优先让策略回到可行区域。对安全强化学习来说，这个分支非常合理，因为当策略已经不安全时，继续追求奖励会让问题更糟。

**Obtain $\theta_{k+1}$ by backtracking line search。**  
最后，算法对候选步做回溯线搜索，逐步缩小步长，直到采样估计下的 KL 和成本约束满足要求。通过检查后，接受该步并得到 $\theta_{k+1}$。这就是最终输出，它会作为下一轮采样的策略。

把这些行连起来，CPO 的输入输出链条是：

$$
\text{当前策略与约束任务}
\to
\text{采样轨迹}
\to
\text{估计 }g,b,c,H
\to
\text{构造局部 QP}
\to
\text{求对偶变量}
\to
\text{得到候选更新}
\to
\text{线搜索检查}
\to
\text{新策略}
$$

这个链条就是“输入如何变成输出”的完整算法逻辑。CPO 的每一轮输出并不是一个孤立动作，而是一个经过 KL 信任域和成本约束共同筛选的策略参数更新。

## 17. 用灵巧手任务类比 CPO 的每个量

虽然 CPO 论文实验主要是 Point、Ant、Humanoid 的 Circle/Gather 任务，但它的形式对灵巧手也很有启发。假设我们要训练一个灵巧手策略，让它抓取物体并避免危险接触。奖励 $R$ 可以鼓励抓取成功、物体抬起、姿态稳定或任务完成；成本 $C_i$ 可以表示碰撞、穿透、过大接触力、关节超限、力矩超限、物体滑落风险等。

在这个类比下，$J(\pi)$ 是长期任务表现，$J_{C_i}(\pi)$ 是长期安全风险。$d_i$ 是你愿意接受的风险上限，例如平均每回合穿透次数不能超过某个阈值，或累计力矩超限成本必须很小。CPO 每一轮都会问：这次策略更新是否会提高抓取成功率，同时不会让这些安全风险超过上限？

$g$ 可以理解成“提高抓取成功率的方向”，$b_i$ 可以理解成“增加某类风险的方向”。如果某个更新方向会让抓取更成功，但同时让手指更容易穿透物体或超过力矩限制，CPO 的对偶变量 $\nu_i$ 会自动提高，把这个危险方向从更新中扣掉。这样，策略学习不是靠固定惩罚系数硬调，而是每一轮根据当前安全边界动态平衡。

## 18. CPO 与 TRPO、固定惩罚、primal-dual 的区别

TRPO 只解决“策略更新不要太大”的问题，它用 KL 信任域稳定训练，但不显式处理安全成本。如果无约束最优策略会进入危险区域，TRPO 本身不会阻止它。CPO 保留了 TRPO 的 KL 信任域，同时在同一个 KL 球里加入成本约束，因此它解决的是“稳定更新 + 安全约束”两个问题。

固定惩罚方法会把目标改成：

$$
R'(s,a,s')=R(s,a,s')-\lambda C(s,a,s')
$$

这个方法看起来简单，但最大问题是 $\lambda$ 很难选。如果 $\lambda$ 太小，策略会为了奖励无视安全成本；如果 $\lambda$ 太大，策略会过度保守，什么都不敢做。论文实验也展示了固定惩罚对系数非常敏感，而 CPO 的 $\nu$ 是每轮通过优化问题自动算出来的。

primal-dual 方法比固定惩罚更聪明，它会根据约束违反情况更新惩罚系数。但它的乘子是跨迭代慢慢学的，可能落后于策略快速变化。CPO 的不同之处在于每一轮都重新求解对偶变量，不依赖上一次的乘子状态，因此能更快响应当前策略附近的安全边界。

## 19. CPO 的核心理论贡献到底是哪几件事

第一，CPO 给出了一个用平均策略散度控制回报差异的理论界。这个界把“旧策略数据上的 surrogate”与“新策略真实表现”联系起来，解释了为什么 KL trust region 不只是工程技巧，而是可以控制近似误差的理论工具。

第二，CPO 把同样的思想用于成本上界。奖励用下界来保证性能不会太差，成本用上界来保证约束不会太离谱，这让安全约束可以被放进 trust-region 更新中。这个方向上的保守性，是 CPO 区别于普通 reward penalty 的关键。

第三，CPO 把理论更新近似成一个可计算的局部 QP。这个 QP 的输入来自 on-policy 轨迹估计，输出是神经网络参数更新方向。通过 $g,b,c,H$ 四类量，算法把原始轨迹数据转成了奖励、成本和策略分布几何之间的平衡问题。

第四，CPO 通过每轮求解对偶变量实现自动安全权衡。$\nu$ 不是手动调的固定惩罚，也不是慢慢学习的滞后参数，而是在当前局部模型下直接算出“为了满足约束，本轮应该压制多少成本方向”。这就是它相对于 primal-dual 基线更少超调的原因。

## 20. 需要警惕的局限

CPO 的保证是“近似约束满足”，不是现实世界中的绝对安全保证。理论界里有一项和 $\sqrt{\delta}/(1-\gamma)^2$ 相关的误差，当 $\gamma$ 很接近 1 时，这个界可能很松。也就是说，论文的理论能说明方向是合理的，但不代表每次真实机器人执行都绝不会违反安全条件。

算法还依赖优势估计和成本估计的质量。如果价值函数学得不好，轨迹数量不足，或者成本信号非常稀疏，那么 $g$ 和 $b$ 都可能有较大误差。此时 QP 解出来的方向在局部模型里看似安全，但真实执行可能仍然有偏差，这也是为什么论文加入 line search 和 cost shaping。

另外，论文主算法的恢复步骤主要针对单约束情形。灵巧手任务往往有很多约束，例如接触力、关节角、速度、力矩、碰撞、穿透、滑移等。如果多个约束同时激活，单约束解析恢复方向就不够用了，需要更一般的多约束 QP 或投影方法。这个问题对把 CPO 思想迁移到灵巧手安全抓取尤其重要。

## 21. 最后一遍总览：CPO 的算法本质

如果把 CPO 压缩成一条主线，它就是：

$$
\text{安全强化学习任务}
\to
\text{CMDP：奖励最大化 + 成本约束}
\to
\text{性能差分公式}
\to
\text{用 KL/TV 界控制 surrogate 误差}
\to
\text{TRPO 式 KL 信任域}
\to
\text{加入成本线性约束}
\to
\text{局部 QP}
\to
\text{对偶求解}
\to
\text{线搜索确认}
\to
\text{安全策略更新}
$$

它的核心不是“多加一个安全 loss”，而是把安全成本作为约束放进每一步策略更新的优化问题里。奖励梯度告诉算法往哪里能变好，成本梯度告诉算法哪里会变危险，KL 曲率告诉算法这一步最多能走多远，对偶变量告诉算法本轮应该如何平衡奖励和安全。最终输出的 $\theta_{k+1}$，就是这四类信息共同决定的一步策略更新。

对于本科生学习来说，可以先记住一个最重要的公式：

$$
x^\star
=
\frac{1}{\lambda^\star}
H^{-1}(g-B\nu^\star)
$$

这行公式几乎浓缩了 CPO 的实际算法。$g$ 是“想提高奖励”，$B\nu^\star$ 是“别违反安全约束”，$H^{-1}$ 是“按照策略分布的几何来走”，$\lambda^\star$ 是“控制步长别超过信任域”。理解了这行公式，再回头读性能界、surrogate 和 QP，就会发现论文的大部分理论都在为它服务。

## 22. 推荐阅读顺序

第一次读论文时，建议先读 Abstract 和 Introduction，抓住“safe exploration”和“每次迭代近似满足约束”的问题意识。然后读第 3、4 节，确认 MDP、CMDP、$J(\pi)$、$J_C(\pi)$、advantage 和 discounted state distribution 的定义。接着读第 5.1 节，不必一次吃透所有证明，但要理解新旧策略回报差异为什么能被平均散度控制。

第二遍读时，把注意力放在第 5.3 和第 6.1 节。第 5.3 是从理论界走到 CPO update，第 6.1 是从 CPO update 走到实际 QP，这两节是输入变输出的核心桥段。最后再读 Algorithm 1、6.2 的 recovery、6.3 的 cost shaping，以及附录 10.2 的单约束解析解。这样读下来，CPO 就不再是一堆公式，而是一条完整的计算链。
