---
tags:
  - 灵巧手专项
  - GraspQP
  - force_closure
  - quadratic_programming
  - physical_constraints
created: 2026-06-23
paper:
  title: "GraspQP: Differentiable Optimization of Force Closure for Diverse and Robust Dexterous Grasping"
  authors: "René Zurbrügg, Andrei Cramariuc, Marco Hutter"
  links:
    - "https://graspqp.github.io/"
    - "https://arxiv.org/abs/2508.15002"
    - "https://graspqp.github.io/static/graspqp.pdf"
local_pdf: "./GraspQP.pdf"
---

# GraspQP：按论文逻辑串联的物理约束理论分析

GraspQP 这篇论文的主线很清楚：作者认为灵巧手抓取数据生成中最核心的瓶颈，不只是采样效率，也不是单纯的神经网络表达能力，而是“稳定抓取”这个物理约束在很多已有方法里被过度简化了。很多方法可以生成看起来接触物体的手姿态，但它们使用的 force closure 指标要么忽略摩擦，要么假设每个接触点施加相同大小的力，要么把本来有硬物理含义的约束变成松散的可微软指标。这样做虽然方便优化，但会让生成结果偏向简单 power grasp，且难以稳定地产生 pinch、precision 等更精细的抓取形态。

因此，GraspQP 的逻辑不是从“怎样训练模型”开始，而是从“怎样把抓取得稳这件事写成一个足够准确、又能反传梯度的物理约束”开始。论文最后得到的核心形式是一个嵌入外层抓取优化中的可微 QP：给定当前手和物体的接触几何，构造 6D wrench matrix；在有界接触力约束下求一个最小残差的二次规划；再通过 KKT 隐式微分把这个 force closure 残差反传到手腕位姿、关节角、接触点和接触法向。下面按论文自身的推导顺序，把这个思想连成一条完整链路。

## 1. 论文为什么要重新定义抓取的物理约束

论文开头讨论的任务是大规模生成灵巧手抓取数据。一个抓取样本不仅要让手指接近物体表面，还要在物理上稳定，也就是物体受到外部扰动时，手指接触力能够抵消该扰动。传统采样方法可以尝试大量候选姿态，再用某种质量指标筛选；梯度方法则希望把质量指标写成可微能量，直接优化手姿态。问题在于，很多可微指标为了方便求导，把 force closure 的物理结构简化掉了。

例如 DexGraspNet 一类方法中的 force closure 项，本质上接近：

$$
E_{FC}^{simple}
=
\left\|
\sum_i w_i
\right\|_2^2
$$

其中 $w_i$ 是接触点产生的 wrench。这个形式隐含了两个很强的假设：第一，接触力方向基本固定，常常退化成只看接触法向；第二，每个接触点贡献的力大小相同，相当于所有 wrench 系数都是 1。真实灵巧手显然不是这样。不同手指可以输出不同大小的力，同一个接触点在摩擦作用下也不止能沿法向施力。对于 pinch 或 precision grasp 这种接触点更少、力矩臂更敏感的抓取，摩擦和接触力分配尤其关键。

所以论文的第一步是把“抓取得稳”还原成机器人学里更严谨的 force closure 条件：接触点在摩擦约束下产生的所有可能 wrench，其正锥能否覆盖整个 6D wrench space。只有先把这个条件写对，后面的可微优化才有物理意义。

## 2. 从接触力到 6D wrench：抓取稳定性的表示空间

刚体在空间中受到的扰动不是单纯的三维力，而是三维力加三维力矩。因此每个接触力都要提升到 6D wrench：

$$
w_i =
\begin{bmatrix}
f_i \\
c_i \times f_i
\end{bmatrix}
\in \mathbb{R}^6
$$

这里 $c_i$ 是接触点相对物体参考点的位矢，$f_i$ 是该接触点施加给物体的力，$c_i \times f_i$ 是该力产生的力矩。论文中有些地方使用 $[f_i;\ f_i \times x_i]$ 或 $[n_i;\ c_i \times n_i]$ 的写法；只要方向约定一致，本质都是把接触力映射成“力 + 力矩”的 6D 向量。

如果只有无摩擦接触，则接触力只能沿法向：

$$
f_i = \lambda_i n_i,\quad \lambda_i \ge 0
$$

此时每个接触点只产生一个法向 wrench：

$$
w_i =
\begin{bmatrix}
n_i \\
c_i \times n_i
\end{bmatrix}
$$

这种无摩擦情形对应 form closure，即仅靠几何法向限制物体的运动。但真实抓取通常依赖摩擦，因此论文进入 force closure：每个接触点的力不只沿法向，而是可以落在 Coulomb friction cone 中：

$$
\mathcal{F}_i
=
\{ f_i = f_{n,i} n_i + f_{t,i}
\mid
f_{n,i}\ge 0,\ \|f_{t,i}\|\le \mu f_{n,i}
\}
$$

其中 $\mu$ 是摩擦系数。对应的 wrench 集合是：

$$
\mathcal{W}_i
=
\left\{
\begin{bmatrix}
f_i \\
c_i \times f_i
\end{bmatrix}
\ \middle|\ f_i \in \mathcal{F}_i
\right\}
$$

所有接触点合起来得到：

$$
\mathcal{W}_{FC} = \bigcup_i \mathcal{W}_i
$$

force closure 的目标就是：

$$
\operatorname{pos}(\mathcal{W}_{FC}) = \mathbb{R}^6
$$

这句话是整篇论文物理理论的中心：抓取稳定性等价于接触 wrench 的非负组合能够生成任意 6D 外部扰动的反方向。换言之，不论外界施加怎样的力和力矩，手指都能在摩擦允许范围内组合出抵消它的接触 wrench。

## 3. 论文怎样把连续摩擦锥变成可计算的矩阵

真实 Coulomb friction cone 是连续二阶锥。为了把它放进高效优化，GraspQP 使用四棱锥对摩擦锥做内近似。设接触点处有法向 $n_i$ 和切向基 $t_{i,1}, t_{i,2}$，则可以取四个切向边方向 $s_{i,k}$，构造四条近似摩擦锥边：

$$
d_{i,k} = n_i + \mu s_{i,k},
\quad k=1,\dots,4
$$

每条边方向都对应一个 primitive wrench：

$$
w_{i,k}
=
\begin{bmatrix}
d_{i,k} \\
c_i \times d_{i,k}
\end{bmatrix}
$$

把所有接触点、所有摩擦锥边对应的 wrench 放成矩阵：

$$
W_{FC}
=
[w_{1,1},\dots,w_{1,4},w_{2,1},\dots,w_{N_c,4}]
\in \mathbb{R}^{6\times M}
$$

这里的四棱锥是内近似，所以它偏保守：如果四棱锥近似下已经满足 force closure，那么真实摩擦锥通常也满足；但真实摩擦锥满足时，四棱锥近似未必能检测出来。这个保守性换来了一个重要好处：连续接触力可行域变成有限个 wrench 列向量，后面就可以使用矩阵和二次规划处理。

到这里，论文已经完成了第一层转换：真实的接触力学问题被转化为一个有限维 wrench matrix 的几何问题。

## 4. 正锥张成定理如何连接 wrench matrix 和 force closure

论文接着引入 positive spanning set。这个概念初看抽象，但它想表达的事情很简单：**如果每个接触力只能以非负大小施加，那么这些接触力方向的组合，能不能覆盖空间里的所有方向？**

先给定一组向量：

$$
S=\{v_1,\dots,v_k\}\subset\mathbb{R}^n
$$

它的正锥定义为：

$$
\operatorname{pos}(S)
=
\left\{
\sum_{i=1}^k \lambda_i v_i
\ \middle|\ \lambda_i\ge 0
\right\}
$$

这个定义里最重要的是 $\lambda_i\ge0$。也就是说，我们只能把 $v_i$ 沿原方向放大后相加，不能使用负系数把它反过来。放到抓取里，这正好对应接触力的物理事实：手指可以推物体，但不能在接触点上“拉”物体，所以接触力大小必须是非负的。

现在问题变成：只允许非负组合，什么时候还能得到整个空间 $V$ 里的任意方向？这就是：

$$
\operatorname{pos}(S)=V
$$

直观地说，这要求向量集合 $S$ 必须在各个方向上形成“包围”。如果所有向量都偏向同一侧，那么非负相加只会继续落在那一侧，不可能生成反方向的向量；如果这些向量从不同方向围住了原点，那么通过调节不同向量的非负权重，就可以生成任意方向。

用一维例子最容易看清楚。若：

$$
S=\{1\}
$$

则：

$$
\operatorname{pos}(S)=[0,+\infty)
$$

它只能生成正方向，不能生成负方向，所以没有覆盖 $\mathbb{R}$。但如果：

$$
S=\{1,-1\}
$$

则非负组合为：

$$
\lambda_1\cdot 1+\lambda_2\cdot(-1)
$$

其中 $\lambda_1,\lambda_2\ge0$。通过让 $\lambda_1$ 大一些可以得到正数，让 $\lambda_2$ 大一些可以得到负数，让二者相等可以得到 0。因此它能覆盖整个 $\mathbb{R}$。同时也存在严格正系数：

$$
1\cdot 1+1\cdot(-1)=0
$$

这就是定理背后的直觉：**如果一组向量的正组合能覆盖正反所有方向，那么它们内部一定能用一组全为正的权重互相抵消到 0；反过来，如果它们能用全正权重抵消到 0，说明它们不是全在一侧，而是围住了原点。**

二维里也一样。若三个向量分别指向三角形的三个方向，并且原点在这个三角形内部，那么可以找到三个正数 $\alpha_1,\alpha_2,\alpha_3$，使：

$$
\alpha_1 v_1+\alpha_2 v_2+\alpha_3 v_3=0
$$

这表示三个方向的“推力”可以互相平衡。由于原点被包在中间，这些向量的非负组合就能向平面中的任意方向延展。相反，如果原点在三角形外面，说明所有向量大体偏在某一侧，它们的非负组合就会漏掉另一侧的方向。

因此，在这些向量本身已经线性张成某个子空间 $V$ 的前提下，下面两个说法等价：

第一，$S$ 的正锥覆盖 $V$：

$$
\operatorname{pos}(S)=V
$$

第二，存在严格正系数使这些向量加权和为零：

$$
\exists \alpha_i>0,\quad
\sum_{i=1}^k \alpha_i v_i=0
$$

这就是常说的“原点在这些向量的凸包内部”。这里的“内部”很关键：不是某些系数可以为 0 的边界平衡，而是所有 $\alpha_i$ 都严格大于 0，说明每个方向都参与了包围原点。

放到 grasp 里，$v_i$ 就是各个 primitive wrench。每个 wrench 表示某个接触点沿某个摩擦锥边方向能对物体施加的 6D 力/力矩。如果存在一组正接触力强度：

$$
\sum_i \alpha_i w_i=0,\quad \alpha_i>0
$$

就说明这些接触 wrench 可以形成一个自平衡内力系统：有的接触在某些方向上推，有的接触在相反方向上抵消，最后总力和总力矩为 0。更进一步，如果这些 wrench 本身线性张成整个 $\mathbb{R}^6$，那么这个“围住原点”的结构就意味着它们的正锥覆盖整个 6D wrench space。也就是说，对任意外部扰动，都能找到一组非负接触力组合来产生反向 wrench 抵消它。这正是 force closure 的数学含义。

论文还使用了该定理的另一个等价形式：

$$
\exists \gamma_i\ge 0,\quad
\sum_{i=1}^k \gamma_i v_i
=
-\sum_{i=1}^k v_i
$$

移项可得：

$$
\sum_{i=1}^k (\gamma_i+1)v_i = 0
$$

令：

$$
\hat{\gamma}_i = \gamma_i+1
$$

就得到：

$$
\hat{\gamma}_i \ge 1,\quad
\sum_{i=1}^k \hat{\gamma}_i v_i = 0
$$

这一步看起来只是代数变形，但它是 GraspQP 物理约束设计的关键。它把“存在正系数”改成了“存在至少为 1 的系数”，从而避免所有系数同时趋近 0 的退化。

## 5. 为什么直接使用 $\alpha_i>0$ 会退化

前面已经说明，理想的 force closure 条件可以写成：

$$
\exists \alpha_i>0,\quad
\sum_i \alpha_i w_i=0
$$

这里的等号右边是 0，表示这些接触 wrench 经过正权重组合以后，总力和总力矩完全抵消。也就是说，接触系统内部形成了一个自平衡结构。

但在优化过程中，当前抓取姿态通常还没有满足这个条件。此时：

$$
\sum_i \alpha_i w_i \neq 0
$$

左边剩下的这个 6D 向量就是“没有被抵消掉的净 wrench”：

$$
r(\alpha)
=
\sum_i \alpha_i w_i
\in \mathbb{R}^6
$$

它的前三维是残余合力，后三维是残余合力矩。如果 $r(\alpha)=0$，说明这组接触力可以完全自平衡；如果 $r(\alpha)$ 很大，说明无论当前这些接触如何组合，仍然留下明显的净力或净力矩。

所以所谓 **force closure 残差**，不是一个新的物理量，而是对 force closure 条件未满足程度的连续度量：

$$
\text{force closure residual}
=
\left\|
\sum_i \alpha_i w_i
\right\|_2
$$

或者为了得到更平滑、非负且方便优化的能量，使用平方形式：

$$
E_{FC}
=
\left\|
\sum_i \alpha_i w_i
\right\|_2^2
$$

这个残差越接近 0，说明当前接触 wrench 越接近能够形成自平衡；残差越大，说明离 force closure 条件越远。因此，如果直接根据定理写 force closure 残差，最自然的形式是：

$$
E_{FC}
=
\left\|
\sum_i \alpha_i w_i
\right\|_2^2,
\quad
\alpha_i>0
$$

这个形式在逻辑上是对的：如果存在正系数让加权 wrench 和为零，就有自平衡接触力。但它作为优化能量时有一个严重问题：$\alpha_i$ 可以同时变得任意小。即便当前接触几何没有真正形成良好的 force closure，只要所有 $\alpha_i\to 0$，就会有：

$$
\left\|
\sum_i \alpha_i w_i
\right\|_2
\to 0
$$

于是能量变小并不代表抓取更稳定，而只是代表优化器把接触力系数缩小了。这会产生接近消失的梯度，外层手姿态也得不到有效的物理修正。

GraspQP 使用前面的等价形式来避免这个退化。它不优化任意正系数 $\alpha_i$，而是优化有下界的系数 $\hat{\gamma}_i$：

$$
\hat{\gamma}_i \ge 1
$$

并进一步加入上界：

$$
\hat{\gamma}_i \le u
$$

下界的意义是防止零力假解；上界的意义是表达真实机器人手指接触力或关节力矩能力有限。论文中实现使用的上界为 50。于是 force closure 约束不再只是“能否找到一组无限小的数学系数”，而是“能否在有物理幅值限制的接触力范围内形成自平衡”。

这就是论文从 positive span 定理走向 QP 的原因：它需要在有界接触力系数下寻找最小 wrench 残差。

## 6. GraspQP 的 QP 是怎样自然出现的

这一节的关键是理解：**QP 不是论文硬塞进去的优化技巧，而是 force closure 残差在矩阵形式下自然变成了二次规划。**

先固定一个当前抓取姿态 $G$。此时手腕位姿、关节角、接触点位置、接触法向都已经确定，因此每个接触点的摩擦锥边方向也确定。于是我们可以把所有 primitive wrench 都算出来：

$$
w_1,w_2,\dots,w_M\in\mathbb{R}^6
$$

这里 $M$ 是 primitive wrench 的总数。例如有 $N_c$ 个接触点，每个摩擦锥用 4 条边近似，那么通常有：

$$
M=4N_c
$$

每个 $w_i$ 都是一个 6 维向量：

$$
w_i=
\begin{bmatrix}
\text{该接触方向产生的力}\\
\text{该接触方向产生的力矩}
\end{bmatrix}
$$

然后把这些 wrench 作为列向量堆成矩阵：

$$
W=
\begin{bmatrix}
| & | & & |\\
w_1&w_2&\cdots&w_M\\
| & | & & |
\end{bmatrix}
\in\mathbb{R}^{6\times M}
$$

这个矩阵的含义非常具体：它把“每个接触方向可以贡献怎样的力/力矩”全部列出来。现在剩下的问题是：这些方向各自应该用多大的力？

于是引入接触力强度系数：

$$
z =
\begin{bmatrix}
\hat{\gamma}_1 & \cdots & \hat{\gamma}_M
\end{bmatrix}^\top
$$

其中：

$$
z_i=\hat{\gamma}_i
$$

表示第 $i$ 个 primitive wrench 对应的接触力强度。由于接触只能推不能拉，而且 GraspQP 为了避免零力退化，要求：

$$
z_i\ge1
$$

同时真实机器人接触力不能无限大，所以再加一个上界：

$$
z_i\le u
$$

因此 $z$ 不是任意数学变量，而是“每个接触方向允许施加的、有物理边界的力强度”。

给定 $W$ 和 $z$ 后，总接触 wrench 就是所有接触 wrench 的加权和：

$$
r(W,z)=Wz
=
\sum_i z_i w_i
$$

这里 $r(W,z)\in\mathbb{R}^6$。它的前三维是所有接触力加起来以后的净力，后三维是所有接触力矩加起来以后的净力矩。

force closure 希望存在一组合法的 $z$，让总 wrench 为零：

$$
Wz=0,\quad 1\le z_i\le u
$$

这句话的物理含义是：在每个接触方向都使用有限且非零的接触力时，所有接触力和接触力矩能够互相抵消，形成自平衡。

但当前抓取姿态未必满足这个条件。也就是说，可能不存在一个合法 $z$ 让 $Wz$ 精确等于 0。那我们就退一步问：

> 在所有合法接触力强度中，哪一组 $z$ 能让净 wrench 最接近 0？

这就得到：

$$
\min_z \|Wz\|_2^2
\quad
\text{s.t.}\quad
1\le z_i\le u
$$

这就是 GraspQP 的内层优化问题。它寻找的不是手姿态，而是在当前手姿态已经固定的情况下，寻找最能让接触 wrench 自平衡的接触力分配。

接下来把目标函数展开：

$$
\|Wz\|_2^2
=
(Wz)^\top(Wz)
=
z^\top W^\top Wz
$$

令：

$$
H=W^\top W
$$

则目标变成：

$$
z^\top H z
$$

由于 $H=W^\top W$，它一定是半正定矩阵：

$$
z^\top H z
=
\|Wz\|_2^2
\ge0
$$

这说明目标函数是一个凸二次函数。论文采用标准 QP 形式时通常写成：

$$
E_{QP}(W)
=
\min_z
\frac{1}{2}z^\top H z + g^\top z
\quad
\text{s.t.}\quad
1\le z_i\le u
$$

其中：

$$
H=W^\top W,\quad g=0
$$

前面的 $\frac{1}{2}$ 只是优化里的常规写法，方便求导，因为：

$$
\nabla_z\left(\frac{1}{2}z^\top H z\right)=Hz
$$

它不会改变最优解。

再看约束。$1\le z_i\le u$ 可以写成两组线性不等式：

$$
z_i\ge1
$$

和：

$$
-z_i\ge -u
$$

把所有维度合起来，可以写成：

$$
Az\ge b
$$

其中一种清晰写法是：

$$
A=
\begin{bmatrix}
I\\
-I
\end{bmatrix},
\quad
b=
\begin{bmatrix}
\mathbf{1}\\
-u\mathbf{1}
\end{bmatrix}
$$

于是完整 QP 是：

$$
E_{QP}(W)
=
\min_z
\frac{1}{2}z^\top W^\top Wz
\quad
\text{s.t.}\quad
\begin{cases}
z\ge \mathbf{1}\\
z\le u\mathbf{1}
\end{cases}
$$

或者等价地：

$$
E_{QP}(W)
=
\min_z
\frac{1}{2}\|Wz\|_2^2
\quad
\text{s.t.}\quad
1\le z_i\le u
$$

这就是 QP “自然出现”的原因：目标是净 wrench 的平方范数，所以是二次型；接触力幅值上下界是线性不等式；二次目标加线性约束正好就是 quadratic program。

这一层 QP 的物理意义可以直接读出来：当前这些接触 wrench 是否能通过一组有下界、有上界的接触力强度组合成零净 wrench。如果最优值接近 0，则说明这些接触点和摩擦锥方向可以形成自平衡系统；如果最优值较大，则说明无论怎样分配接触力，都会留下无法抵消的净力或净力矩。

更具体地说，QP 解出来两个东西。

第一个是最优接触力分配：

$$
z^\star(W)
$$

它告诉我们：在当前抓取几何下，每个 primitive wrench 应该承担多大的接触力强度，才能尽量让总 wrench 平衡。

第二个是最小残差：

$$
E_{QP}(W)
=
\frac{1}{2}\|Wz^\star\|_2^2
$$

它告诉我们：当前抓取离 force closure 自平衡条件还差多少。如果：

$$
Wz^\star\approx0
$$

说明当前接触几何已经比较接近 force closure；如果：

$$
\|Wz^\star\|_2
$$

仍然很大，则说明当前接触点、法向或力矩臂几何结构不好，外层优化应该移动手姿态来改变 $W$。

因此，GraspQP 的外层优化不是直接优化 $z$，而是优化抓取姿态 $G$。$z$ 只是内层 QP 为当前 $W(G)$ 找到的最佳接触力解释：

$$
G\to W(G)\to z^\star(W)\to E_{QP}(W(G))
$$

这也是它比简单指标更精确的地方。简单指标相当于固定 $z_i=1$，直接看：

$$
\left\|
\sum_i w_i
\right\|_2^2
$$

而 GraspQP 允许不同接触方向有不同合法力强度：

$$
\left\|
\sum_i z_i w_i
\right\|_2^2,
\quad 1\le z_i\le u
$$

这更接近真实灵巧手：不同手指、不同接触点、不同摩擦锥边方向，本来就不应该被强行假设为施加相同大小的力。

论文正文里 QP 约束写成：

$$
Az\ge b,\quad
b=[1_{n_c};u_{n_c}],\quad
A=\operatorname{diag}(I,-I)
$$

按字面会得到 $z\ge1$ 且 $-z\ge u$，与 $z>0$ 冲突。结合前文公式 $u\ge\hat{\gamma}_i\ge1$ 和实现中使用 upper limit，可以判断这是符号或排版歧义。理解论文时应按物理目标读取为：

$$
1\le z_i\le u
$$

## 7. 为什么仅有 $Wz\approx0$ 还不够

positive spanning 定理还有一个前提：向量集合必须线性张成目标空间。对于抓取问题，目标空间是完整的 6D wrench space：

$$
\mathbb{R}^6
$$

因此除了存在有界正组合使：

$$
Wz\approx0
$$

还必须有：

$$
\operatorname{rank}(W)=6
$$

否则可能出现一种假稳定：这些 wrench 只在低维子空间里互相抵消，却无法抵抗另一些方向的扰动。例如所有接触点都集中在相近位置，或者所有接触法向方向相似，那么它们也许可以抵消某些平移力，但无法生成足够多样的力矩。此时 $Wz=0$ 并不代表完整 force closure。

GraspQP 用奇异值来引导 $W$ 满秩。设 $W$ 的六个奇异值为：

$$
\sigma_1(W),\dots,\sigma_6(W)
$$

满秩等价于：

$$
\sigma_j(W)>0,\quad j=1,\dots,6
$$

奇异值乘积：

$$
V_W=\prod_{j=1}^6\sigma_j(W)
$$

可以理解为 wrench matrix 在 6D 空间中撑开的体积。如果某个方向没有覆盖，某个奇异值会接近 0，体积也会塌缩。论文将 force closure 残差乘上一个与该体积相关的指数项：

$$
E_{FC}
=
\left\|
\sum_i \hat{\gamma}_i w_i
\right\|_2^2
\cdot
\exp\left(
-\prod_j\sigma_j(W)
\right)
$$

这个形式的逻辑是：最小化能量时，优化器一方面要让有界正组合的净 wrench 接近 0，另一方面会倾向于让 wrench space 的体积变大，因为体积越大，指数因子越小。于是 force closure 项同时包含两个物理要求：

$$
\text{有界正组合自平衡}
\quad+\quad
\text{完整 6D wrench 覆盖}
$$

这一步把论文的理论闭环补上了。没有奇异值体积项，QP 只能说明“这些 wrench 可以互相抵消”；加入满秩引导后，它才更接近“这些 wrench 可以抵抗任意方向扰动”。

需要注意的是，指数体积项更像优化引导，而不是单独的严格约束。当残差已经精确为 0 时，乘法项对不同体积解的区分会减弱。严格的 force closure 理论条件仍然是“正锥覆盖 $\mathbb{R}^6$”，也就是“正组合为零 + 线性满秩”共同成立。

## 8. 可微 QP 如何把物理约束反传到手姿态

到这里为止，论文已经把 force closure 写成了一个 QP 最优值：

$$
E_{QP}(W)
=
\min_z
\frac{1}{2}\|Wz\|_2^2
\quad
\text{s.t.}\quad
1\le z_i\le u
$$

这个式子本身只回答一个问题：**在当前接触几何 $W$ 已经固定的情况下，能不能找到一组合法接触力强度 $z$，让总 wrench 尽量接近 0？**

但 GraspQP 的最终目标不是求接触力 $z$，而是优化手的抓取姿态。也就是说，外层真正要更新的是：

$$
G=(\chi,q,\Delta q)
$$

其中 $\chi$ 是手腕位姿，$q$ 是关节角。手姿态一变，手指表面点的位置会变，接触点 $c_i$ 会变，接触法向 $n_i$ 会变，摩擦锥边方向 $d_{i,k}$ 会变，于是 primitive wrench 也会变：

$$
G
\to
c_i(G),\ n_i(G),\ d_{i,k}(G)
\to
w_{i,k}(G)
\to
W(G)
$$

因此，GraspQP 里的 force closure loss 实际上是一个复合函数：

$$
E_{FC}(G)
=
E_{QP}(W(G))
$$

这就是“反传到手姿态”的含义。我们不是只想知道当前抓取的 $E_{QP}$ 数值有多大，而是想知道：如果我稍微移动手腕、弯曲某个关节、改变某个指尖接触位置，这个 force closure 残差会变大还是变小？用公式说，就是需要：

$$
\frac{\partial E_{FC}}{\partial G}
=
\frac{\partial E_{QP}}{\partial W}
\frac{\partial W}{\partial G}
$$

更准确地写，右侧是链式法则中的乘积关系：

$$
dE_{FC}
=
\left\langle
\frac{\partial E_{QP}}{\partial W},
dW
\right\rangle,
\quad
dW
=
\frac{\partial W}{\partial G}dG
$$

所以真正的难点是第一项：

$$
\frac{\partial E_{QP}}{\partial W}
$$

因为 $E_{QP}(W)$ 不是一个普通显式函数。它不是像 $E(W)=\|W\|^2$ 那样直接由公式算出来，而是“先解一个 QP，再把 QP 最优值当成 loss”。也就是说：

$$
W
\to
H=W^\top W
\to
z^\star(W)
\to
E_{QP}(W)=\frac{1}{2}\|Wz^\star(W)\|_2^2
$$

这里最棘手的是 $z^\star(W)$。当 $W$ 变化时，QP 的最优接触力分配 $z^\star$ 也会变化。可微 QP 要解决的正是这个问题：**如何知道 QP 的最优解会随着输入矩阵 $W$ 怎样变化。**

一种朴素做法是把 QP 求解器的每一步迭代都展开，然后像神经网络一样反传。但这会依赖具体求解器、内存开销大，而且梯度质量受迭代步数影响。GraspQP 采用的是更标准的思路：不反传求解器的迭代过程，而是利用最优解必须满足的 KKT 条件，对这个“最优性方程”做隐式微分。

把 QP 写成标准形式：

$$
\min_z
\frac{1}{2}z^\top Hz+g^\top z
\quad
\text{s.t.}\quad
Az-b\ge0
$$

其中在 GraspQP 中：

$$
H=W^\top W,\quad g=0
$$

约束 $Az-b\ge0$ 表示：

$$
1\le z_i\le u
$$

对应的拉格朗日函数可以写成：

$$
\mathcal{L}(z,\lambda)
=
\frac{1}{2}z^\top Hz+g^\top z
-\lambda^\top(Az-b)
$$

这里 $\lambda$ 是约束对应的拉格朗日乘子。它可以理解成“约束对最优解施加的反作用力”。如果某个 $z_i$ 处在上下界内部，那么这个约束没有真正限制它，乘子通常为 0；如果某个 $z_i$ 正好卡在下界 $1$ 或上界 $u$，说明这个边界正在阻止最优解继续往外走，对应乘子可能非零。

QP 最优解 $z^\star$ 必须满足 KKT 条件：

$$
Hz^\star+g-A^\top\lambda^\star=0
$$

$$
Az^\star-b\ge0,\quad \lambda^\star\ge0
$$

$$
\lambda_i^\star(Az^\star-b)_i=0
$$

第一行叫 stationarity。它的意思是：在最优点处，目标函数想继续下降的方向，已经被约束边界的反作用力抵消了。第二行是可行性：$z^\star$ 没有违反上下界，乘子也非负。第三行是互补松弛：只有真正贴住边界的约束才会产生非零乘子；没有贴住边界的约束不参与最优性平衡。

隐式微分的核心思想是：既然 $z^\star$ 是通过 KKT 方程定义的，那么当 $W$ 发生一个小变化时，$H=W^\top W$ 也发生小变化；为了继续满足 KKT 方程，$z^\star$ 和 $\lambda^\star$ 必须跟着发生小变化。于是我们可以对 KKT 方程两边求微分，解出：

$$
dz^\star
\quad\text{和}\quad
d\lambda^\star
$$

关于：

$$
dH,\ dg,\ dA,\ db
$$

的关系。

在 active set 不变的局部区域内，可以把当前贴住边界的约束记作 $A_{\mathcal{A}}z=b_{\mathcal{A}}$。这时 KKT 微分会形成一个线性系统：

$$
\begin{bmatrix}
H & -A_{\mathcal{A}}^\top\\
A_{\mathcal{A}} & 0
\end{bmatrix}
\begin{bmatrix}
dz\\
d\lambda_{\mathcal{A}}
\end{bmatrix}
=
-
\begin{bmatrix}
dH\,z + dg - dA_{\mathcal{A}}^\top\lambda_{\mathcal{A}}\\
dA_{\mathcal{A}}z - db_{\mathcal{A}}
\end{bmatrix}
$$

这条式子不需要死记，重要的是理解它在做什么：**它把“输入 QP 的参数变了一点”转化成“最优解 $z^\star$ 会怎么变”。** 可微 QP 层的 backward pass 本质上就是解这个 KKT 线性系统，或者解它的转置伴随系统，从而得到 loss 对 $H,g,A,b$ 的梯度。由于 $H=W^\top W$，再继续用链式法则，就能得到 loss 对 $W$ 的梯度。

如果只想看物理直觉，可以暂时忽略 active set 切换带来的非光滑性。令：

$$
r^\star = Wz^\star
$$

其中 $r^\star$ 是 QP 最优后仍然没有抵消掉的残余净 wrench。最优值为：

$$
E_{QP}(W)
=
\frac{1}{2}\|r^\star\|_2^2
$$

在局部光滑情况下，value function 的梯度可以直观理解为：

$$
\frac{\partial E_{QP}}{\partial W}
\approx
r^\star(z^\star)^\top
=
(Wz^\star)(z^\star)^\top
$$

这个式子的物理含义非常清楚。矩阵 $\partial E/\partial W$ 的第 $i$ 列近似为：

$$
\frac{\partial E}{\partial w_i}
\approx
z_i^\star r^\star
$$

也就是说，第 $i$ 个 primitive wrench 的梯度大小由两个因素决定：第一，当前还剩多少残余 wrench $r^\star$；第二，这个接触方向在最优力分配中承担了多大权重 $z_i^\star$。如果某个接触方向在最优平衡里很重要，但它仍然无法抵消残差，那么优化器会强烈推动与这个 wrench 相关的接触几何发生变化。

再把 $w_i$ 展开：

$$
w_i=
\begin{bmatrix}
f_i\\
c_i\times f_i
\end{bmatrix}
$$

可以看到，一个 wrench 由两部分组成：力方向 $f_i$，以及接触点位置 $c_i$ 与力方向共同决定的力矩 $c_i\times f_i$。因此，loss 对 $w_i$ 的梯度会继续传到两个几何来源。

第一，它会传到力方向或摩擦锥边方向 $f_i$。改变 $f_i$ 会同时改变 wrench 的力分量和力矩分量：

$$
\delta w_i
=
\begin{bmatrix}
\delta f_i\\
c_i\times \delta f_i
\end{bmatrix}
$$

这对应优化接触法向、摩擦锥方向，或者让手指接触到物体表面上法向更合适的位置。

第二，它会传到接触点位置 $c_i$。接触点移动不会直接改变力分量，但会改变力矩臂：

$$
\delta(c_i\times f_i)
=
\delta c_i\times f_i
$$

这对应优化手指在物体上的落点。比如当前抓取能抵消平移力，但对某个旋转扰动缺少力矩，那么梯度会倾向于移动接触点，增加合适方向的力矩臂。

再往前，$c_i$ 和 $f_i$ 又来自手的前向运动学和物体几何：

$$
c_i=c_i(\chi,q),
\quad
f_i=f_i(\chi,q,\text{object normal})
$$

所以最终可以得到：

$$
\frac{\partial E_{FC}}{\partial q},
\quad
\frac{\partial E_{FC}}{\partial \chi}
$$

这才是“物理约束反传到手姿态”的完整含义：QP 先告诉我们当前接触 wrench 离自平衡还差哪个 6D 残差；KKT 隐式微分告诉我们这个残差对每个 wrench 列的敏感性；几何链式法则再把这个敏感性传给接触点、法向、手腕位姿和关节角。

这和普通距离 loss 的区别很大。距离 loss 只能告诉手指“离物体表面更近一点”；穿透 loss 只能告诉手指“不要插进物体”；而可微 QP 的 force closure loss 能告诉优化器：当前抓取缺少的是某个方向的抗力，还是某个方向的抗力矩；应该改变接触力方向，还是改变接触点位置来增加力矩臂。也正因为如此，GraspQP 的物理约束不是简单的几何贴合约束，而是一个能把 6D 接触力学稳定性信息传回手姿态的可微物理层。

最后还要注意一点：由于 QP 中有上下界约束，当最优解从“某个约束未激活”切换到“贴住下界或上界”时，梯度可能是分段光滑的，而不是处处光滑。这不是 GraspQP 特有的问题，而是所有带不等式约束的可微优化层都会遇到的现象。实际实现中，可微 QP 通常在局部 active set 固定的区域内提供稳定梯度；在边界切换点附近，梯度可以理解为一种局部近似或次梯度信号。

## 9. 总能量中其他约束如何服务 force closure

论文完整的抓取优化能量写作：

$$
E
=
E_{FC}
+w_{dis}E_{dis}
+w_{reg}E_{reg}
$$

其中 $E_{FC}$ 是上面推导出的 force closure 物理稳定项，$E_{dis}$ 和 $E_{reg}$ 则保证这个稳定性不是通过不合法几何得到的。

$E_{dis}$ 要求激活接触点靠近物体表面。如果没有它，优化器可能会在空间中构造出数学上有利的 wrench matrix，但手指并没有真实接触物体。$E_{pen}$ 惩罚手和物体穿透，否则优化器可能把手指插入物体内部获得更好的法向和力矩臂。$E_{joints}$ 保证关节角不超过限位，$E_{spen}$ 保证手自身不发生自穿透。

因此，这些项不是与 force closure 并列的零散指标，而是共同构成一条物理可行链：

$$
\text{接触点在物体表面}
\to
\text{手姿态运动学和碰撞可行}
\to
\text{接触 wrench 能抵抗任意扰动}
$$

GraspQP 真正新增的理论重点是最后一环，但前两环保证最后一环不是建立在虚假接触和非法手姿态上。

## 10. 论文之后为什么还需要 MALA*

在得到可微 force closure 能量后，论文继续讨论优化策略 MALA*。这一部分不是物理约束理论的核心，但它在论文逻辑中承担一个实际作用：即使能量项更物理，外层抓取优化仍然是高度非凸的。不同初始抓取可能陷入局部极小值，很多样本可能收敛到相似 power grasp，造成 mode collapse。

MALA* 的作用是利用整个样本分布的能量统计来调节优化过程。能量明显差的样本会被重置，能量较差的样本在接受 Metropolis-Hastings 步时使用更高温度，从而更容易跳出局部区域。对本文的物理约束主线来说，可以这样理解：QP 提供“某个抓取是否物理稳定”的局部梯度，MALA* 负责让一批抓取样本不要全部沿着同一个稳定模式塌缩。

所以如果只关心物理理论，MALA* 可以放在次要位置。它不是 force closure 的定义来源，而是配合这个物理能量做多样化优化的外层采样策略。

## 11. GraspQP 思路的本质

沿着论文逻辑看下来，GraspQP 的本质可以概括为四次转化。

第一次转化是从真实接触到 wrench geometry。论文不直接问“这个手姿态看起来能不能抓住”，而是问接触点在摩擦约束下生成的 wrench 正锥是否覆盖 $\mathbb{R}^6$。这把稳定性从视觉或几何直觉转成 6D 凸几何问题。

第二次转化是从布尔判定到连续能量。force closure 原本是 yes/no 条件，不适合梯度优化。GraspQP 用：

$$
\min_{1\le z_i\le u}\frac{1}{2}\|Wz\|_2^2
$$

把它变成“距离有界自平衡还有多远”。这样当前抓取即使不稳定，也能产生有方向的修正梯度。

第三次转化是从软启发式到硬约束优化。论文没有把接触力系数固定为 1，也没有只用 softmax 或 penalty 做近似，而是保留 $1\le z_i\le u$ 这样的硬边界。下界避免零力退化，上界表达真实执行器能力，QP 则允许不同接触方向自适应分配力强度。

第四次转化是从不可导物理检查器到可微物理层。通过 KKT 隐式微分，force closure 不再只是生成后的筛选器，而是可以直接驱动手腕、关节、接触点和法向优化的物理 loss：

$$
G \to W(G) \to \operatorname{QP}(W) \to E_{FC}
$$

这就是 GraspQP 最值得借鉴的部分：它把“抓得稳”从经验式距离/穿透指标，提升为可微的准静态接触力学约束。

## 12. 这种物理约束的边界

GraspQP 的理论比很多简化指标更严谨，但它仍然是一个准静态解析模型，不等于完整真实世界物理。

首先，它主要处理静态 wrench 抵抗能力，不直接描述动态抓取过程中的冲击、滑移、接触建立顺序和控制闭环。其次，它依赖准确的物体几何、接触点和法向；如果 mesh 或 SDF 法向有误，构造出的 $W$ 也会有误。第三，摩擦锥被四棱锥内近似，且依赖固定摩擦系数 $\mu$，真实接触材料和表面状态会让摩擦变化很大。

还有一个更深的硬件层限制：论文用 $1\le z_i\le u$ 表示接触力幅值边界，但真实灵巧手的可施力集合还受关节力矩、接触雅可比和姿态相关力传递能力约束。更完整的模型可能需要加入：

$$
\tau = J_c(q)^\top f,\quad
\tau_{\min}\le\tau\le\tau_{\max}
$$

这会把简单的接触力上下界扩展成 torque-feasible wrench constraint。也就是说，GraspQP 已经比固定系数或无摩擦指标更物理，但距离完整硬件可执行性仍有空间。

## 13. 对灵巧手物理约束注入的启发

如果把 GraspQP 用到灵巧手生成模型或 diffusion 框架里，最关键的不是照搬整套 MALA* 优化流程，而是借用它对 force closure 的可微建模方式：

$$
E_{phys}(G)
=
\min_{1\le z_i\le u}
\frac{1}{2}\|W_{FC}(G)z\|_2^2
\cdot
\exp\left(-\prod_j\sigma_j(W_{FC}(G))\right)
$$

这个能量可以作为生成阶段的 guidance、训练阶段的辅助 loss、采样后的物理 refinement，或者作为数据集过滤与重打分指标。它的优势是物理含义清晰：每一项都能解释为接触 wrench 的平衡能力、力幅值可行性和 6D 空间覆盖能力。

但实际嵌入 diffusion 时要注意计算成本。每个 denoising step 都求 QP 会很重，较实际的做法可能是只在后期 step 使用、只对候选 top-k 使用、将 QP 能量蒸馏成轻量网络，或用更便宜的对偶 margin 近似替代内层 QP。

## 14. 总结

按论文逻辑串起来，GraspQP 的理论路线是：

$$
\text{真实抓取稳定性}
\to
\text{摩擦锥接触 wrench}
\to
\text{positive span / force closure}
\to
\text{有界正系数自平衡}
\to
\text{QP 残差能量}
\to
\text{KKT 隐式微分}
\to
\text{可优化的物理约束}
$$

一句话概括：GraspQP 用摩擦锥生成 6D 接触 wrench 集合，用 positive span 判定 force closure，用带上下界的 QP 寻找物理可行的自平衡接触力，用奇异值体积引导完整 6D 覆盖，再通过 KKT 隐式微分把这个稳定性条件变成可以驱动抓取生成的梯度。

这套方法的本质不是“多加一个 loss”，而是把抓取稳定性的核心物理命题转写成一个可微的、带硬约束的准静态接触力学层。
