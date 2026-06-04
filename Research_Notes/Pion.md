---
tags:
- paper
- domain/multimodal_perception
- domain/reinforcement_learning
- domain/robot_manipulation
- domain/vla
- impact/high_value
- impact/solid
- method/foundation_model
- method/imitation_learning
- method/reinforcement_learning
- review/auto_tagged
- status/unread
- task/manipulation
- task/navigation
- task/scene_understanding
- type/method
- type/system
aliases:
- 'Rethinking Muon Beyond Pretraining: Spectral Failures and High-Pass Remedies for
  VLA and RLVR'
- Pion optimizer
- High-pass Newton-Schulz
- Muon spectral failures
- Per-head Pion mode
- Spectral gradient orthogonalization
- VLA RLVR optimizer
- Uniform spectral whitening
- Matrix-aware optimizer
- Pion for VLA
- High-pass spectral remedy
paper_id: arxiv:2605.19282
arxiv_id: '2605.19282'
url: https://huggingface.co/papers/2605.19282
pdf_url: https://arxiv.org/pdf/2605.19282.pdf
local_pdf: '[[Rethinking Muon Beyond Pretraining Spectral Failures and HighPass Remedies
  for VLA and RLVR.pdf]]'
github: None
project_page: None
institutions:
- Michigan State University
- Cisco
- University of Minnesota
- IBM Research
publication_date: '2026-05-25'
metadata_publication_date: '2026-05-19'
score: '8.0'
domains:
- multimodal_perception
- reinforcement_learning
- robot_manipulation
- vla
methods:
- foundation_model
- imitation_learning
- reinforcement_learning
tasks:
- manipulation
- navigation
- scene_understanding
paper_type: system
impact_band: high_value
reading_status: unread
priority_score: 99
review_status: auto_tagged
next_action: inspect_protocol
year: 2026
---

# Rethinking Muon Beyond Pretraining: Spectral Failures and High-Pass Remedies for VLA and RLVR

## 📌 Abstract
Muon is a matrix-aware optimizer that leverages Newton-Schulz (NS) iterations to enforce spectral gradient orthogonalization by driving all singular values of the momentum matrix toward 1. While this uniform spectral whitening enhances exploration and outperforms AdamW in LLM pretraining, we show it could lead to fundamental limitations beyond pretraining in two regimes: (i) cross-modality vision-language-action (VLA) training, where inherently low-rank action-module gradients cause amplification of noisy tail directions, and (ii) reinforcement learning with verifiable rewards (RLVR), where low-SNR gradients and the need to preserve per-head specialization from prior training make whitening unstable. To address these challenges, we propose Pion, a drop-in replacement for Muon that preserves its computational efficiency while replacing uniform spectral whitening with a two-stage Promotion+Suppression mechanism, which we call the high-pass NS iteration. This design induces a sharp spectral high-pass effect, anchoring dominant singular values at 1 while suppressing noisy tail components toward 0, with controllable filter strength. To preserve pretrained per-head heterogeneity, Pion also supports a per-head mode that applies updates independently across attention heads via a simple reshape, at no extra cost. In VLA training on LIBERO and LIBERO-Plus, Pion consistently outperforms both baselines across l_1-regression (VLA-Adapter) and flow-matching (VLANeXt) architectures, e.g., reaching 100% success rate on LIBERO Object after 1,500 training steps with VLA-Adapter, vs. 97.0% for Muon and only 32.2% for AdamW. The advantage of Pion further extends to a real Franka Research 3 robot with a pi_0.5 backbone under the DROID setup on three grasp-and-place tasks. In RLVR post-training on Qwen3-1.7B/4B with GRPO and GMPO, Pion also outperforms AdamW on MATH and GSM8K while Muon collapses to zero.

## 🖼️ Architecture


## 🧠 AI Analysis
## Abstract

Muon (MomentUm Orthogonalized by Newton–Schulz) is a matrix-aware optimizer that uses Newton–Schulz iterations to orthogonalize the momentum matrix – it drives every singular value toward 1. This uniform spectral whitening helps exploration and beats AdamW in large language model pretraining. However, the paper shows that the same uniform mapping introduces fundamental difficulties once training moves beyond pretraining.

Two important post‑pretraining regimes are studied. In **vision‑language‑action** (VLA) training, the action head often receives inherently low‑rank gradients; Muon’s whitening amplifies noisy tail singular directions and degrades the policy. In **reinforcement learning with verifiable rewards** (RLVR), gradients have low signal‑to‑noise ratio and attention heads retain per‑head specialization from earlier training; Muon’s equal treatment of all singular values destroys that heterogeneity and can even cause collapse.

The authors propose **Pion** (sPectral hIgh‑pass Optimization on momeNtum), a drop‑in replacement that preserves Muon’s wall‑clock cost while replacing uniform whitening with a two‑stage Promotion＋Suppression mechanism – the **high‑pass Newton–Schulz iteration**. The design creates a sharp spectral high‑pass filter: dominant singular values are anchored near 1 while noisy tail components are pushed toward 0, with tunable filter strength. A **per‑head mode** reshapes attention projections along the head dimension and applies the high‑pass iteration independently to each head, allowing the optimizer to respect per‑head update scales with zero extra arithmetic.

Experiments show Pion consistently outperforming Muon and AdamW in both regimes. On VLA‑Adapter with LIBERO Object, Pion reaches 100 % success after 1 500 steps versus 97 % for Muon and only 32 % for AdamW; gains also appear on flow‑matching heads and a real Franka Research 3 robot. In RLVR post‑training on Qwen3‑1.7B/4B with GRPO and GMPO, Pion beats AdamW on MATH and GSM8K while Muon collapses to zero accuracy.

In simpler terms: Muon treats every gradient direction equally, which is harmful when gradients are low‑rank or noisy. Pion keeps Muon’s speed but adds a selective filter that preserves important information and suppresses noise.

## 1. Core Snapshot

### Problem Statement

Muon’s update rule maps every positive singular value of the momentum matrix to 1, producing a fully isotropic spectral update. This *uniform whitening* is beneficial during LLM pretraining where exploration is paramount, but it fails in VLA and RLVR for a shared reason: the informative signal concentrates in a few leading singular values while the remaining tail is dominated by noise.

In VLA training the action head receives a low‑rank gradient because each action is a low‑dimensional vector (e.g., seven joint angles). The singular‑value spectrum exhibits a sharp drop; the tail consists largely of a spectral floor or noise that carries no useful direction for the policy. Muon’s whitening inflates those noisy directions to the same magnitude as the informative head, corrupting the policy update. In RLVR the policy gradient is estimated from trajectory‑level rewards, yielding low signal‑to‑noise ratio. Again the leading singular vectors capture the meaningful part of the gradient while the remainder is stochastic. Uniform whitening amplifies this noise, which can destabilize training to the point of collapse.

>[!warning] Shared spectral signature  
>Both failure modes share the same signature: a **small informative head** and a **noisy tail**. This observation is the diagnostic that motivates the optimizer redesign.

An additional issue appears in RLVR: attention layers hold per‑head specialization inherited from pretraining and fine‑tuning. Treating the entire Q, K, V, or O matrix as a single block, as Muon does, forces a uniform update scale across heads. This destroys the heterogeneity needed to maintain the different update magnitudes that the base model has learned. The optimizer must therefore handle both the spectral imbalance and the per‑head structure.

### Core Contribution

The paper introduces Pion, which replaces Muon’s matrix sign operation with a **two‑stage high‑pass Newton–Schulz iteration**. Instead of applying the same polynomial across all steps, the iteration is split into a **Promotion stage** and a **Suppression stage**, using different scalar coefficient sets that shape the singular‑value map. The Promotion polynomial lifts dominant singular values toward 1, while the Suppression polynomial squeezes the tail toward 0. The result is a soft high‑pass filter anchored at σ = 1 for large values and decaying to 0 for small ones.

Crucially, this transformation is implemented with exactly the same five Newton–Schulz steps as Muon; only the polynomial coefficients change. The per‑step arithmetic cost remains identical. For attention layers, a simple reshape along the head dimension allows the high‑pass iteration to be applied independently per head, preserving per‑head specialization with no extra floating‑point operations.

The contribution is validated by strong empirical results:
- VLA‑Adapter on LIBERO Object: 100 % success after 1 500 steps vs 97 % for Muon and 32 % for AdamW.
- Real‑robot Franka 3 trials: 85.6 % average success for Pion vs 38.9 % for Muon.
- RLVR on Qwen3‑1.7B/4B with GRPO/GMPO: Pion matches or exceeds AdamW while Muon collapses to zero accuracy.

>[!tip] What changes?  
>Think of Pion as Muon with a **different spectral filter** – a high‑pass instead of an all‑pass – plus an optional **per‑head reshape** for attention layers.

### Innovation Origin & Rationale

The design begins with a diagnostic: measuring the **effective rank** and **signal‑to‑noise ratio** of momentum matrices in VLA and RLVR. Those measurements reveal that informative energy is concentrated in the leading singular values, making a uniform sign operation harmful.

From this diagnosis, the authors ask: can we keep the Newton–Schulz iteration structure but redesign the scalar polynomial that each step applies to the singular values? Because each NS step evolves normalized singular values through a polynomial

$$ \sigma \leftarrow f(\sigma) = a\sigma + b\sigma^3 + c\sigma^5, $$

the problem reduces to choosing the coefficients $(a,b,c)$ appropriately. The insight is that a single polynomial cannot simultaneously anchor $\sigma=1$ and push small $\sigma$ to zero with a sharp transition; therefore the iteration is split into two stages. The coefficients are derived from fixed‑point constraints ($f(1)=1$, fixed point at 1) and derivative conditions that enforce a rapid fall‑off for small values.

The per‑head mode is a practical extension: attention projections have shape $[d_{\text{model}}, h\cdot d_{\text{head}}]$, so reshaping to $[h, d_{\text{head}}, d_{\text{model}}]$ and treating each head’s slice as an independent matrix preserves the heterogeneity that already exists in the weight norms. This is a zero‑cost mechanism that directly addresses the RLVR failure described in Section 4 of the paper.

## 2. Reading Map

This work sits at the intersection of **matrix‑aware optimization** and **post‑pretraining adaptation**. Researchers who have used AdamW or Muon for LLM pretraining and now wish to adapt models to robot control or reasoning post‑training will find the paper directly applicable.

**Sections 3 and 4** together explain *why* Muon fails in VLA and RLVR. Read them carefully – they provide the spectral measurements and analysis that justify the new optimizer.

**Section 5** presents the Pion algorithm. Pay close attention to the polynomial coefficients and the per‑head reshape; these are the concrete changes from Muon.

**Sections 6.2 and 6.3** report the experimental results. On a first pass you can skim them after understanding the spectral argument, but the learning curves in **Figure 5 and Figure 6** deserve a second look to judge convergence speed and robustness.

The **related‑work section** can be read quickly unless you are preparing a survey.

## 3. Method Walkthrough

### Inputs, Outputs, And Assumptions

**Inputs:**  
- Stochastic gradient $G_t$ at iteration $t$ for a weight matrix $\Theta \in \mathbb{R}^{m\times n}$.  
- Momentum buffer $M_t = \mu M_{t-1} + G_t$, where $\mu$ is the momentum coefficient.

**Output:**  
- An update direction $\Delta\Theta_t$ that is subtracted from $\Theta$ after scaling by the learning rate $\eta$:

  $$\Theta_t = \Theta_{t-1} - \eta \, \Delta\Theta_t.$$

**Assumptions about the momentum spectrum:**  
- In the intended VLA and RLVR regimes, $M_t$ is approximately **low‑rank** (VLA) or **low‑SNR** (RLVR): most of the informative signal lives in the top few singular values, while the tail contains noise, a spectral floor, or stochastic oscillations.  
- The leading singular vectors still point toward useful descent directions; the suppressor should not touch them beyond keeping them near 1.  
- After supervised fine‑tuning, attention projections retain **per‑head heterogeneity** in their Frobenius norms, so an optimizer that ignores the head structure would disrupt that specialization.

These assumptions matter because the high‑pass filter is deliberately asymmetric; if the informative signal were spread uniformly across the spectrum, the suppression stage would remove useful information.

### Pipeline From Data To Prediction

The pipeline modifies Muon’s NS update without altering the outer training loop.

1. **Momentum accumulation**: exactly as in Muon, $M_t \leftarrow \mu M_{t-1} + G_t$.  
2. **Frobenius normalisation**: $M_t$ is scaled so that $\|M_t\|_F = 1$, which brings all singular values into $[0,1]$.  
3. **High‑pass NS iteration**:  
   - Run $k_p$ steps with the **Promotion polynomial** coefficients $(a_p, b_p, c_p)$.  
   - Run the remaining $k_s = 5 - k_p$ steps with the **Suppression polynomial** coefficients $(a_s, b_s, c_s)$.  
   This produces the update direction matrix $H_t$.  
4. **Weight update**: $\Theta_t = \Theta_{t-1} - \eta \, H_t$.  
5. **Per‑head mode** (optional, for attention layers):  
   - Reshape the projection matrix $\Theta$ from shape $[d_{\text{model}}, h \cdot d_{\text{head}}]$ to $[h, d_{\text{head}}, d_{\text{model}}]$.  
   - Apply steps 1–4 independently to each head’s $[d_{\text{head}}, d_{\text{model}}]$ slice.  
   - Reshape the resulting update back to the original shape.

The per‑head mode adds **no extra arithmetic** beyond the reshape operations; the high‑pass NS cost per head is exactly the same as if the layer were treated as a single block.

### Key Design Choices

**Two‑stage polynomial design.** Instead of searching for a single $f(\sigma)$ that would flatten the tail while preserving $\sigma=1$, the method explicitly separates Promotion and Suppression. This yields a sharper transition near the passband edge and avoids the gradient flattening that a weaker single polynomial would cause. A single‑polynomial alternative would either be too aggressive (risking signal loss) or too weak (not suppressing noise enough).

**No SVD or sketching.** The paper deliberately avoids Low‑Rank Muon’s approach of projecting the momentum onto a fixed top‑$k$ subspace before applying NS. That approach (i) requires a pre‑specified rank $k$ that cannot adapt across layers or training steps, and (ii) incurs expensive SVD or sketching at every step. Pion retains the $O(mn)$ cost of the original NS loop while achieving a similar spectral high‑pass effect through the polynomial coefficients.

**Per‑head mode is active only for RLVR.** In VLA training, the diagnostic points to the low‑rank nature of the action head as the dominant problem; default Pion already suffices. For RLVR, the additional per‑head heterogeneity is critical: without the reshape, the optimizer would impose a single update scale across heads, destroying the specialised scales that the model has learned and contributing to Muon’s collapse. The paper shows that turning on the per‑head mode restores stable convergence and matches AdamW’s performance in RLVR.

>[!question] Fixed $k_p$ vs. adaptive filtering  
>The number of promotion steps $k_p$ is a hyperparameter chosen empirically (e.g., $k_p=1$ used in many experiments). The paper does not yet explore an automatic way to set $k_p$ based on, say, the observed effective rank. An adaptive scheme could further remove hyperparameter tuning but might introduce instability early in training.

## 4. Core Theory And Formulas

The core of the method is the scalar polynomial map applied to singular values by each NS iteration, and the two‑stage design that turns it into a high‑pass filter.

**Muon’s baseline.** Muon updates a weight matrix as

$$ \Theta_t = \Theta_{t-1} - \eta \, \operatorname{msign}(M_t), $$

where $\eta > 0$ is the learning rate. The matrix sign operator $\operatorname{msign}(M)$ is defined through the singular value decomposition (SVD) $M = U \Sigma V^\top$ as

$$ \operatorname{msign}(M) = U \, \operatorname{sign}(\Sigma) \, V^\top = U V^\top, $$

which sets every strictly positive singular value to 1. This is equivalent to finding the nearest orthogonal matrix in the spectral norm, also written as $\operatorname{msign}(M) = M (M^\top M)^{-1/2}$.

To avoid the cost of SVD, Muon approximates the matrix sign via **Newton–Schulz iterations**. After normalizing the momentum to unit Frobenius norm, the matrix $X$ (initialized to $M/\|M\|_F$) is updated repeatedly as

$$ X \leftarrow a X + b X X^\top X + c X (X^\top X)^2. $$

Each iteration reshapes singular values through the scalar map

$$ f(\sigma) = a\sigma + b\sigma^3 + c\sigma^5, $$

where $\sigma \in [0,1]$ is a normalized singular value of $M$. Standard Muon uses coefficients (e.g., $a=1.5$, $b=-0.5$, $c=0$) that drive all $\sigma$ toward 1.

**Pion’s high‑pass polynomial.** Pion redesigns the coefficients for a two‑stage sequence. Let $k_p$ be the number of early Promotion steps and $k_s = 5 - k_p$ the number of later Suppression steps. The **Promotion polynomial** is

$$ f_p(\sigma) = 1.875\,\sigma \;-\; 1.25\,\sigma^3 \;+\; 0.375\,\sigma^5. $$

It is monotonically non‑decreasing on $[0,1]$ and has a fixed point at $\sigma = 1$ with $f_p(1) = 1$, so large singular values stay anchored near 1.

The **Suppression polynomial** is

$$ f_s(\sigma) = 2.5\,\sigma^3 \;-\; 1.5\,\sigma^5. $$

Notice the linear term is absent: $f_s(0)=0$ and the polynomial grows slowly near the origin, so small singular values are heavily damped (higher‑order terms dominate). At $\sigma=1$, $f_s(1)=1$, so the fixed point is still preserved.

Chaining $k_p$ Promotion steps followed by $k_s$ Suppression steps yields the composite map

$$ \sigma \mapsto (f_s \circ f_s \circ \dots \circ f_s) \circ (f_p \circ \dots \circ f_p)(\sigma) $$

which produces the high‑pass shape shown in Figure 3‑(d) of the paper: values close to 1 remain near 1, while values below roughly 0.4 are suppressed toward 0.

**Per‑head mode (RLVR).** For an attention projection matrix of shape $[d_{\text{model}}, h\cdot d_{\text{head}}]$, the matrix is reshaped to $[h, d_{\text{head}}, d_{\text{model}}]$ and the high‑pass NS iteration runs independently on each $d_{\text{head}}\! \times \! d_{\text{model}}$ slice. This preserves the Frobenius norm differences between heads, which encode pretrained specialization.

>[!note] Practical interpretation  
>The Promotion stage essentially “aligns” the dominant directions without destroying their relative magnitudes, while the Suppression stage “erases” directions that are likely noise. The resulting update matrix has a spectrum that resembles a **high‑pass filtered** version of the momentum.

## 5. Architecture, Figures, And Implementation

In VLA training, Pion is applied only to the **action‑module** weight matrices; the vision and language modules continue to use the standard Muon optimizer. For RLVR, the **per‑head variant** of Pion is applied to the Q, K, V, and O projections of every attention layer. The paper does not include a block diagram of the optimizer pipeline, but the algorithm is completely specified by the polynomial coefficients and the value of $k_p$.

The five figures in the paper are qualitative rollout frames from the real‑robot DROID evaluation, showing a Franka arm performing grasp‑and‑place tasks under the Pion policy. They illustrate successful collision‑free placement into a basket.

## 6. Experiments And Evidence

**VLA training** used VLA‑Adapter (ℓ₁‑regression head) and VLANeXt (flow‑matching head) on the four LIBERO suites and LIBERO‑Plus, with perturbation conditions that vary background, camera, language, layout, light, noise, and robot instance. Key results:

- **LIBERO Object**: after 1 500 training steps, Pion achieves **100 % success**, Muon 97.0 %, AdamW 32.2 %.
- **LIBERO‑Plus**: the advantage of Pion widens under language and noise perturbations, where Muon’s uniform whitening becomes more harmful.
- **Real‑robot (Franka Research 3 with π0.5 backbone)**: on three grasp‑and‑place tasks under the DROID setup, Pion averages 85.6 % success versus **38.9 % for Muon**. Note that the text does not report variance across multiple seeds for these robot trials; statistical reliability of the 85.6 % figure would need further verification.

**RLVR post‑training** used GRPO and GMPO on Qwen3‑1.7B and 4B models, evaluated on MATH levels 3–5 and GSM8K. Across all eight settings Pion **outperforms AdamW**, while **Muon collapses to zero accuracy**. An important ablation compared Pion to its “low‑pass” mirror (coefficients that promote tail and suppress head); that variant also collapses, confirming that the high‑pass direction is essential.

>[!warning] Limited robustness reporting  
>The real‑robot studies only report mean success rates without information on per‑task variance, number of trials, or seed variation. This makes it hard to assess whether the 85.6 % vs 38.9 % difference is statistically reliable.  
>Additionally, the optimal $k_p$ (the number of promotion steps) is chosen empirically and the paper does not discuss sensitivity to this choice for the robot experiments.

## 7. Strengths, Limitations, And Failure Cases

**Strengths**  
- **Cost‑neutral upgrade**: Pion uses exactly the same five NS iterations as Muon; only the coefficients are swapped. The per‑head reshape adds zero extra FLOPs.  
- **Targeted remedy**: Directly fixes the two failure modes identified in VLA (low‑rank action gradient) and RLVR (low‑SNR gradients, per‑head heterogeneity) with a clear spectral design.  
- **Empirical gains**: Large improvements over Muon on both benchmarks (100 % vs 97 % on LIBERO Object; non‑collapse vs collapse in RLVR) and on a real robot.

**Limitations**  
- The evaluation is restricted to **action modules in VLA** and **attention projections in RLVR**. Whether the same high‑pass coefficients work equally well for other low‑rank modules (e.g., MLP layers in different architectures) is not tested.  
- The hyperparameter $k_p$ (number of promotion steps) must be **chosen empirically**, and its optimal value may depend on model size or task distribution. No adaptive scheme is provided.  
- The paper does **not test Pion in standard LLM pretraining**, leaving open the question of whether the high‑pass filter would hurt performance in the high‑SNR, high‑rank regime where uniform whitening has been shown beneficial.  
- **Reproducibility details** such as learning rates, momentum coefficients, batch sizes, and the SVD rank schedule used for the Low‑Rank Muon baseline are not listed in the provided text. The GitHub link is mentioned but no URL is given.

**Known failure cases**  
- When the high‑pass filter is **reversed** (low‑pass coefficients), the optimizer collapses just like Muon in RLVR, confirming that suppressing the tail is critical.  
- For VLA, the paper does not report failure cases where Pion underperforms Muon; the improvements are consistent across conditions.

## 8. Reproduction Notes

**Datasets**: LIBERO suites (four tasks), LIBERO‑Plus with seven perturbations, DROID setup for real‑robot evaluation, GSM8K, and MATH levels 3–5.  
**Backbones**: VLA‑Adapter, VLANeXt, π0.5, and Qwen3‑1.7B/4B.  
**Training objectives**: ℓ₁ regression (VLA‑Adapter), flow matching (VLANeXt), GRPO and GMPO (RLVR).  
**Metrics**: success rate (VLA) and accuracy (RLVR).  
**Baselines**: AdamW (global), Muon (applied to 2‑D weight matrices), and Low‑Rank Muon (for comparison).  

Many hyperparameters are absent from the text: exact values of $k_p$, momentum $\mu$, learning rates, batch sizes, number of rollouts per GRPO update, and the SVD rank schedule for Low‑Rank Muon. Code and data availability statements are missing; only mentions of a GitHub link and project page exist without URLs. Detailed reproduction would require additional information from the authors.

>[!failure] Missing implementation details  
>Without explicit hyperparameters, reproducing the exact results is difficult. The paper’s main value lies in the method design and the spectral analysis; practitioners should be ready to tune $k_p$ and learning rates on their own setups.

## 9. What To Read Closely

1. **Section 4** – the effective‑rank and SNR diagnostics. These measurements provide the evidence that the momentum spectrum is indeed imbalanced, directly motivating the new optimizer.  
2. **Section 5** – the derivation of the Promotion and Suppression polynomials and the per‑head mode. Focus on **Figure 3** (the composite high‑pass map) and the coefficients $f_p$ and $f_s$.  
3. **Figure 5‑(b) and Figure 6** – learning curves for VLA and RLVR, which show not only final performance but also convergence speed and stability.  
4. **Figure 8** – the ablation that compares Pion with its low‑pass mirror; this confirms that the high‑pass direction is essential.  

On a first pass you can skip the related‑work section and the appendix.

## 10. Research Ideas And Open Questions

**Module‑specific high‑pass filtering**  
The paper applies Pion only to action heads in VLA and attention projections in RLVR. Effective rank varies across layers, so a single $k_p$ might be sub‑optimal. A small follow‑up experiment could sweep $k_p$ independently for each module in VLA‑Adapter on LIBERO Object and measure final success rate after 1 500 steps. The question is whether module‑specific $k_p$ yields a further improvement beyond the reported numbers. The risk is that the extra hyperparameter search could reduce the simplicity advantage if optimal $k_p$ values differ sharply across modules.

**Adaptive $k_p$ via cheap rank estimation**  
Because erank varies during training, one could replace the fixed $k_p$ with a running estimate of the number of singular values above a small threshold (e.g., fraction of norm). The idea would be to keep the high‑pass character but adapt the filter strength per layer and per step, potentially capturing benefits similar to Low‑Rank Muon without the SVD cost. A feasible experiment would test this adaptive scheme on LIBERO‑Plus and measure success rate and wall‑clock time. The main risk is that the estimator itself introduces noise that destabilizes early training when singular value estimates are unreliable.

**Pion in standard LLM pretraining**  
The work leaves open whether uniform whitening remains optimal when gradients are high‑rank and high‑SNR. An experiment could continue pretraining a ~1B model on a small subset of the original pretraining corpus for 5 000 steps, comparing validation perplexity under AdamW, Muon, and Pion with the same total compute. The observation to watch is whether Pion’s suppression stage hurts perplexity; if it does, that would indicate the high‑pass design is regime‑specific rather than universally superior to Muon.

## Knowledge Graph & Connections

### Related Work Connections

The provided related notes sit in the broader area of vision-language-action models and continual reinforcement learning, not directly on optimizer design. Nevertheless, Pion operates at the interface where these topics meet—training action heads and performing RL post-training on large pretrained models. The connections are therefore thematic rather than technical, but they highlight complementary insights.

First, the note [[Rethinking VLM Representation for VLA Initialization]] studies how VLM representations, update strategies (LoRA vs full fine-tune), and robot-data pretraining affect VLA policy performance. A key message is that the original pretrained VLM representation is critical, and overly reshaping it (e.g., via full fine-tune) can weaken the initialization. Pion’s contribution is orthogonal but potentially synergistic: it targets the *optimizer* used to train the action head, which is often the main module adapted on top of a frozen VLM backbone. The paper identifies that action heads suffer from low-rank gradients that can corrupt the update when a uniform whitening optimizer like Muon is used, and Pion’s spectral high-pass filter directly addresses this. Thus, a VLA practitioner who follows the advice of the representation paper and uses LoRA or selective adaptation may still benefit from applying Pion to the action-module matrices to further stabilize training, especially when the gradient is heavily low-rank. This complementarity suggests that future VLA training recipes could combine representation-preserving strategies with optimizers that are aware of the spectral structure of the gradient.

Second, [[Simple Recipe Works]] finds that, for continual RL with VLAs, simple sequential fine-tuning with LoRA is remarkably robust and avoids catastrophic forgetting, outperforming more complex strategies. Pion’s focus is on post-training with verifiable rewards (RLVR) using full-weight optimization, and it too confronts a collapse phenomenon—in that regime Muon collapses to zero accuracy while Pion matches AdamW. The two works are connected by the shared goal of stable RL fine-tuning, but they approach the problem from different angles: one leverages parameter-efficient adaptation, the other a matrix-aware optimizer. An open question is whether Pion’s high-pass filtering, perhaps combined with LoRA or other low-rank adapter methods, could push robustness even further in the continual RL setting explored in that note. Conversely, the success of simple LoRA in that work hints that the collapse observed in Muon under RLVR may be mitigated not only by spectral filtering but also by constraining the update’s degrees of freedom—a hypothesis worth testing.

The third note, [[Not All Features Are Created Equal]], provides mechanistic insights into how VLA models decompose visual and language information across layers and heads. While it does not discuss optimization, its observation that attention heads exhibit specialized roles and that visual pathways dominate action generation indirectly supports Pion’s design choice of a *per-head mode* for attention layers. Preserving per-head update magnitudes, as Pion does, respects the heterogeneity that the mechanistic study suggests is functionally important. This alignment is intriguing, but the mechanistic note offers no evidence that uniform treatment of heads would hurt the learned specialization; that remains a plausible rationale rather than a proven link.

Overall, the three notes and the Pion paper collectively depict a landscape where stable adaptation of large pretrained models for embodied tasks depends on careful handling of representation, optimization, and parameter allocation. Pion’s spectral filter adds a new knob to this landscape, specifically for regimes where gradients are low-rank or noisy.

### Concept Map

```mermaid
graph LR
    G[Stochastic Gradient G_t] --> M[Momentum M_t]
    M --> N[Normalize to unit Frobenius norm]
    N --> P[Promotion NS f_p]
    P --> S[Suppression NS f_s]
    S --> H[High-pass Update H_t]
    H --> W[Weight Update]
    
    W --> app1[VLA Action Head<br/>(low-rank grad)]
    W --> app2[RLVR Attention<br/>(per-head mode)]
    
    %% Weak connections to related notes
    app1 -.- r1[[Rethinking VLM Representation]] 
    app2 -.- r2[[Simple Recipe Works]]
    
    style r1 dashed
    style r2 dashed
```

The pipeline is straightforward: momentum is accumulated and normalized, then passed through two stages of Newton–Schulz with distinct polynomials to create a spectral high-pass filter, yielding the update. The two primary application points—action heads in VLA and attention layers in RLVR—are shown. Dashed lines link to related notes that share the application context but not the optimizer methodology, underlining that Pion provides a new tool for those problems.

### Questions For Future Reading

1. **How universal is the benefit of spectral high-pass filtering across different types of low-rank or noisy gradients?**  
   The paper demonstrates gains when the informative signal lies in the top singular values and the tail is noise. But what if the gradient spectrum is not strictly low-rank plus noise—for instance, in continual learning or task-switching scenarios where the tail contains older task information? Would suppression of the tail cause forgetting, or could a tunable filter be designed to preserve long-tail memory? Future papers should explore the spectrum of gradients in more varied training regimes and test whether adaptive promotion/suppression thresholds are needed.

2. **Can the core idea of a tunable spectral map be generalized to other matrix-aware optimizers beyond Muon-style Newton–Schulz iterations, such as Shampoo, K-FAC, or low-rank projection methods?**  
   Pion shows that replacing the uniform sign map with a high-pass polynomial inside the NS loop is simple and cost-free. It is natural to ask whether similar spectral shaping—via different eigen- or singular-value transformations—could be embedded into preconditioners that use matrix square roots or Kronecker approximations. The answer would indicate whether “spectral awareness” is a broadly applicable design axis for optimizers or a peculiarity of the momentum-orthogonalization framework.

3. **What is the interaction between Pion’s spectral update and parameter-efficient fine-tuning (e.g., LoRA) when applied to the same model?**  
   In RLVR, Pion is used with full-weight training, while [[Simple Recipe Works]] shows that LoRA alone already stabilizes continual RL. Would combining Pion’s high-pass filtering with LoRA adapters (e.g., applying Pion to the LoRA matrices or to the frozen weight updates) yield further improvement, or would the low-rank constraint of LoRA render spectral filtering redundant? A systematic study of this interaction could lead to a more robust recipe for RL post-training that resists both collapse and catastrophic forgetting.

These questions push beyond the immediate findings of the paper and encourage examination of the underlying spectral dynamics when new training paradigms are introduced.

---
*Analysis by PaperBrain (x-ai/grok-4.3; refinement: deepseek/deepseek-v4-pro)*

## 📂 Resources
- **Local PDF**: [[Rethinking Muon Beyond Pretraining Spectral Failures and HighPass Remedies for VLA and RLVR.pdf]]
- [Online PDF](https://arxiv.org/pdf/2605.19282.pdf)
- [ArXiv Link](https://huggingface.co/papers/2605.19282)
