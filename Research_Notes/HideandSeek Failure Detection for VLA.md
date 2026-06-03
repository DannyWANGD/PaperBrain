---
tags:
- paper
- domain/embodied_ai
- domain/multimodal_perception
- domain/reinforcement_learning
- domain/robot_manipulation
- domain/vla
- impact/high_value
- impact/solid
- method/foundation_model
- method/reinforcement_learning
- review/auto_tagged
- status/unread
- task/manipulation
- task/navigation
- task/scene_understanding
- type/method
- type/system
aliases:
- 'Hide-and-Seek in Trajectories: Discovering Failure Signals for VLA Runtime Monitoring'
- Hide-and-Seek
- VLA Runtime Monitoring
- Contrastive Failure Detection
- Trajectory-Level Failure Localization
- Inter-Intra Trajectory Contrastive
- Failure Signal Discovery
- Step-Level Annotation Free
- Robot Execution Failure Detection
paper_id: arxiv:2605.30834
arxiv_id: '2605.30834'
url: https://huggingface.co/papers/2605.30834
pdf_url: https://arxiv.org/pdf/2605.30834.pdf
local_pdf: '[[HideandSeek in Trajectories Discovering Failure Signals for VLA Runtime
  Monitoring.pdf]]'
github: None
project_page: None
institutions:
- University of Wisconsin–Madison
- Georgia Institute of Technology
publication_date: '2026-06-01'
score: '8.1'
domains:
- embodied_ai
- multimodal_perception
- reinforcement_learning
- robot_manipulation
- vla
methods:
- reinforcement_learning
tasks:
- manipulation
- navigation
- scene_understanding
paper_type: system
impact_band: high_value
reading_status: unread
priority_score: 100
review_status: auto_tagged
next_action: inspect_protocol
year: 2026
metadata_publication_date: '2026-05-29'
---

# Hide-and-Seek in Trajectories: Discovering Failure Signals for VLA Runtime Monitoring

## 📌 Abstract
Vision-Language-Action (VLA) models enable robots to follow natural language instructions and generalize across diverse tasks, but they remain vulnerable to execution failures that compromise reliability in real-world deployment. Detecting such failures during execution is therefore critical for the robust deployment of embodied systems. Existing failure detection methods either rely on expensive action resampling or external models, while alternatives propagate trajectory-level labels uniformly across every timestep, obscuring localized failure signals. In this paper, we propose Hide-and-Seek, a framework that formulates VLA failure detection as a coarsely supervised learning problem. By combining inter-trajectory and intra-trajectory contrastive objectives, Hide-and-Seek localizes failure-indicative actions and induces temporally structured failure signals from trajectory-level supervision alone, without any step-level annotation. We evaluate Hide-and-Seek on LIBERO, VLABench, and a real-world robotic platform across three representative VLA policies: OpenVLA, π_0, and π_{0.5}.Our method achieves state-of-the-art multi-task failure detection performance with a practical accuracy--timeliness trade-off under conformal prediction, and generalizes well to both seen and unseen tasks.

## 🖼️ Architecture
![[HideandSeek in Trajectories Discovering Failure Signals for VLA Runtime Monitoring_arch.png]]

## 🧠 AI Analysis
## Abstract
Vision-Language-Action (VLA) models enable robots to follow natural language instructions and generalize across diverse tasks, but they remain vulnerable to execution failures that compromise reliability in real-world deployment. Detecting such failures during execution is therefore critical for the robust deployment of embodied systems. Existing failure detection methods either rely on expensive action resampling or external models, while alternatives propagate trajectory-level labels uniformly across every timestep, obscuring localized failure signals. In this paper, we propose Hide-and-Seek, a framework that formulates VLA failure detection as a coarsely supervised learning problem. By combining inter-trajectory and intra-trajectory contrastive objectives, Hide-and-Seek localizes failure-indicative actions and induces temporally structured failure signals from trajectory-level supervision alone, without any step-level annotation. We evaluate Hide-and-Seek on LIBERO, VLABench, and a real-world robotic platform across three representative VLA policies: OpenVLA, π0, and π0.5. Our method achieves state-of-the-art multi-task failure detection performance with a practical accuracy–timeliness trade-off under conformal prediction, and generalizes well to both seen and unseen tasks. Code and videos are available at our project page.

The abstract describes a method called Hide-and-Seek that detects when a robot's vision-language-action model is about to fail during a task. Instead of needing detailed labels for every individual action or relying on slow external vision models, the approach uses only labels that say whether an entire trajectory succeeded or failed. It learns to spot the important failure moments by comparing actions across different trajectories and within the same trajectory.

## 1. Core Snapshot

### Problem Statement
The core problem is detecting failures during robot task execution when a VLA policy runs, using only coarse trajectory-level success or failure labels. At each timestep the VLA receives an observation composed of RGB images, a language instruction, and robot state, then outputs an action from which we extract an internal action embedding. The desired output is a binary decision at each timestep indicating whether the current prefix of the trajectory will result in task failure.

The real bottleneck is the **mismatch between supervision granularity and required detection granularity**. Step-level failure annotations are expensive because a human must identify the exact moment of error across long, stochastic trajectories. If instead we assign the trajectory label uniformly to every timestep—as done by prior work like SAFE—we mislabel all the normal actions that occur before failure onset. This injects substantial label noise, because a trajectory labeled “failure” may contain many perfectly correct steps. The challenge is to learn a per‑step detector that rises only near failure events, without any temporal annotations during training.

### Core Contribution
The central technical claim is that a contrastive learning framework can convert trajectory‑level labels into accurate per‑step failure detection. The framework uses two complementary losses:

- **Inter‑trajectory contrastive loss** forces the highest‑scoring step in a failure trajectory to be higher than the highest‑scoring step in a success trajectory. This guides the model to focus on the most failure‑indicative action across trajectories, rather than trying to separate all steps individually.
- **Intra‑trajectory contrastive loss** shapes the score dynamics within each failure trajectory: it encourages the average score after a *proxy failure onset* to be higher than the average score before it. The proxy onset is defined automatically as the timestep of the greatest score increase.

Together, these losses impose a strong structural regularity that uniform label propagation lacks. The detector discovers where the failure “hides” without requiring any temporal annotation.

This approach differs from prior classifier‑based monitors that naively label every step with the trajectory outcome, and from sampling‑based or VLM‑based monitors that suffer from high latency. Evidence for the contribution comes from consistent state‑of‑the‑art performance on LIBERO‑10, VLABench, and real‑robot tasks across three VLAs (OpenVLA, π0, π0.5). For example, on unseen VLABench tasks with π0.5, Hide‑and‑Seek achieves a balanced accuracy of 0.713 versus 0.641 for the strongest classifier baseline, and outperforms a VLM‑based monitor by +13.1% while running over 2000× faster.

### Innovation Origin & Rationale
The design originates from the observation that **failure trajectories contain many normal actions before the actual error begins**. Consequently, propagating the trajectory label uniformly to every timestep creates noise that can mislead a detector. The authors explicitly connect this to *coarsely supervised learning*, a paradigm previously used in video action localization and anomaly detection, where a single label for a “bag” of instances guides the discovery of the responsible instances (e.g., multiple instance learning). Without the contrastive structure, a detector would lack guidance on *when* the failure signal appears among mostly normal behavior. The inter‑trajectory loss provides discrimination at the coarse level, while the intra‑trajectory loss provides temporal structure. This rationale is a direct claim of the paper: the two losses together convert coarse supervision into a temporally structured and localized signal, whereas any single loss would be insufficient.

## 2. Reading Map
The paper targets readers interested in runtime monitoring for generalist robot policies, especially those working on weakly supervised learning for sequential decision tasks. The task domain is multi‑task failure detection on tabletop manipulation benchmarks and real hardware.

**Efficient reading path**:
1. Read the abstract, Section 1 (introduction), and Section 3 (problem setup) to understand the supervision mismatch and the coarsely supervised formulation.
2. Study Section 4 (method), particularly the loss equations and the conformal prediction deployment in Section 4.2; this is the technical core.
3. Skim Section 2 (related work) after grasping the method.
4. For empirical evidence, examine the main results tables in Section 5.2, then the ablation tables in Section 5.3 and the accuracy–timeliness curves in Figure 3.

Pay attention to how the two contrastive losses interact and how the proxy onset is defined, because these are the main innovations that enable learning from trajectory‑level labels.

## 3. Method Walkthrough

### Inputs, Outputs, and Assumptions
The method receives **per‑timestep action embeddings** extracted from a frozen VLA policy. Embeddings are aggregated over non‑overlapping windows to reduce redundancy. The only supervision is a trajectory‑level binary label indicating success (0) or failure (1). The detector outputs a scalar **failure score** between 0 and 1 for each trajectory prefix. At deployment, a binary alarm is raised when the score exceeds a conformal prediction threshold that varies with timestep.

The approach makes two important assumptions:
1. Every failure trajectory contains *at least one* step whose failure score can be pushed genuinely higher than the highest score in a success trajectory.
2. The likelihood of task success decreases after the moment failure begins; that is, the average score *after* a correctly identified onset should be higher than *before*.

If these assumptions do not hold—for example, if a failure trajectory is indistinguishable from a success trajectory until the very end, or if the onset proxy is wildly inaccurate—the losses lose their ability to guide localization.

### Pipeline from Data to Prediction
1. **Data collection**: A VLA policy executes on tasks, producing trajectories of action embeddings. Each trajectory gets only a success/failure outcome label.
2. **Embedding aggregation**: Embeddings are averaged over non‑overlapping windows to compress the temporal sequence.
3. **Detector backbone**: A lightweight sequence model, defaulting to a single‑layer LSTM, processes prefixes of windowed embeddings and produces per‑step failure scores $s_t$.
4. **Training**: Mini‑batches sample pairs of failure and success trajectories.
   - The inter‑trajectory loss computes the maximum score in each trajectory and pushes the failure max above the success max by a margin.
   - Within the failure trajectory, the proxy onset $t_{\text{onset}} = \arg\max_t (s_t - s_{t-1})$ is identified. The intra‑trajectory loss pushes the average score *after* this point above the average *before* it by a margin.
   - The combined objective is optimized on the frozen embeddings.
5. **Inference**: For a new rollout, the detector produces a running score sequence. Scores are compared against precomputed time‑varying conformal thresholds (calibrated on held‑out trajectories) to decide whether to raise an alarm.

### Key Design Choices
The choice of **contrastive rather than direct classification** is fundamental. A binary classifier trained to predict the trajectory label on every step would be forced to treat all steps as equally failure‑indicative or success‑indicative. That approach, evaluated in ablation, degrades sharply because normal actions before the failure receive an incorrect “failure” target. In contrast, the inter loss only cares about the *most* failure‑like step, leaving the other steps unconstrained; the intra loss then shapes the temporal profile without requiring step‑level labels.

The use of the **proxy onset based on the sharpest score difference** is another crucial design choice. It avoids any need for temporal annotation while still encouraging a score ramp that tends to align with actual failure moments. The paper verifies alignment by comparing with GPT‑annotated onsets (not described in detail in the provided text, but alluded to). Without the intra loss, the model might produce isolated high‑score peaks that do not cleanly separate normal and failure phases.

> [!note] Implementation detail
> The exact margin values and $\lambda$ weighting are given in the text: $m_r = 1.0$, $m_o = 0.5$. The LSTM’s hidden dimension and other hyperparameters are not specified in the main paper; they likely appear in the appendix or code release.

## 4. Core Theory and Formulas

### Main Objective
The central objective is to discover failure‑indicative actions from trajectory‑level supervision. This is achieved by contrasting the most salient failure signals across trajectories and shaping the score dynamics within a failure trajectory so that scores remain low during normal execution and rise around failure onset.

### Important Equations

**Inter‑trajectory contrastive loss**:
$$L_{\text{inter}} = \frac{1}{|D_f| |D_s|} \sum_{\tau_f \in D_f} \sum_{\tau_s \in D_s} \max\left( 0,\; m_r - \max_{1 \leq t \leq N_{\tau_f}} s_t + \max_{1 \leq t \leq N_{\tau_s}} s_t \right)$$

- $D_f$: set of failure trajectories, $D_s$: set of success trajectories.
- $s_t$: failure score at (windowed) timestep $t$.
- $N_{\tau_f}$, $N_{\tau_s}$: number of windowed time steps in the respective trajectory.
- $m_r > 0$: margin (set to 1.0).

This loss becomes positive when the highest score in a failure trajectory is not greater than the highest score in a success trajectory by at least $m_r$. Minimizing it forces the detector to *select and elevate the most failure‑like action* in failure cases while suppressing the maximum score in successful rollouts. It thus provides the global discrimination needed to separate the two classes without forcing every timestep to be labeled.

> [!warning] Potential hard negatives
> If a success trajectory contains a genuinely awkward but recoverable moment that yields a high score, the inter loss may be misled and raise false positives. This is a hidden assumption: success trajectories must not contain steps that strongly resemble failure.

**Intra‑trajectory contrastive loss**:
$$L_{\text{intra}} = \frac{1}{|D_f|} \sum_{\tau_f \in D_f} \max\left( 0,\; m_o - \frac{1}{N_{\tau_f} - t_{\text{onset}} + 1} \sum_{t \geq t_{\text{onset}}} s_t + \frac{1}{t_{\text{onset}} - 1} \sum_{t < t_{\text{onset}}} s_t \right)$$

- $t_{\text{onset}} = \arg\max_t (s_t - s_{t-1})$: proxy failure onset, defined as the timestep of the largest score jump.
- $m_o > 0$: margin (set to 0.5).

The two inner averages are the mean score after the proxy onset and the mean score before it. The loss penalizes the detector when the post‑onset average is not sufficiently higher than the pre‑onset average. This encourages a temporally structured signal: low scores in the normal phase, a sharp rise at the onset, and sustained higher scores afterward. Because the onset is *derived from the scores themselves*, the loss is fully differentiable (with appropriate handling of the argmax; typically a soft approximation or gradient is not passed through the argmax—the paper likely uses a stop‑gradient or hard assignment, but the exact implementation is not stated in the provided text).

**Combined loss**:
$$L = L_{\text{inter}} + \lambda L_{\text{intra}}$$
where $\lambda$ balances the two terms (the exact value is not specified in the main text).

Together, the losses guide the detector to find both the globally most indicative step across trajectories and a locally consistent temporal boundary within each failure trajectory.

### Algorithmic Intuition
During training, each mini‑batch pairs one failure trajectory with one success trajectory. The detector computes per‑step scores, the inter loss compares the two maxima, and the intra loss locates the largest score jump in the failure trajectory to define the pseudo onset. The model then updates to widen the score gap. Over many batches, the detector learns to produce score sequences that are low and flat for success, and for failure they climb sharply around the moment where the failure signal becomes unambiguous—without ever seeing ground‑truth step‑level labels.

## 5. Architecture, Figures, and Implementation
The detector is described as a lightweight sequential model; the default is a single‑layer LSTM that consumes window‑aggregated action embeddings. For autoregressive VLAs like OpenVLA, embeddings are averaged across layers and action dimensions. For flow‑matching models (π0, π0.5), the hidden states before the velocity head at the final denoising step are used. The paper mentions a window size of 4 or 8 depending on the VLA, but precise architectural details (hidden dimension, dropout, optimizer settings) are not given in the main text.

Figure 2 in the paper illustrates the framework: input embeddings from a failure trajectory and a success trajectory both pass through the detector (the LSTM) to produce score sequences. The inter loss operates on the two maxima, while the intra loss operates on the pre‑ and post‑onset averages computed from the failure trajectory’s score sequence. The proxy onset is indicated as the point of maximum score difference.

Real‑robot figures show a UFactory xArm 6 with a parallel gripper and a RealSense D435 camera, handling objects such as a carrot plush, bowl, plate, and blocks. These images establish the visual domain and the task setups, but they do not contain internal model computations.

> [!note] Missing reproducibility details
> The value of $\lambda$, the LSTM hidden dimension, the exact conformal calibration procedure, and the gradient handling for the proxy onset are not specified in the provided text. A full reproduction would require the supplementary material or code release.

## 6. Experiments and Evidence
The evaluation covers LIBERO‑10 and VLABench in simulation and two real‑robot task suites (CUBE and KITCHEN), using OpenVLA, π0, and π0.5. Metrics include balanced accuracy (bACC), weighted accuracy, and time‑weighted accuracy, all computed under conformal prediction thresholds averaged over three significance levels (α around 0.15–0.25) and three random seeds.

The main tables report that Hide‑and‑Seek achieves the highest scores across seen and unseen task splits. For instance, on unseen VLABench tasks with π0.5, it reaches 0.713 bACC versus 0.641 for the next-best classifier baseline. The accuracy–timeliness curves (Figure 3) show that Hide‑and‑Seek lies closest to the top‑left corner, indicating it detects failures early without sacrificing correctness. Ablation experiments (Table 5) confirm that removing either contrastive loss degrades performance, and that a context‑aware backbone (LSTM) outperforms a per‑step MLP. A direct comparison with a VLM‑based monitor shows a +13.1% accuracy advantage while the VLM method operates at 2000× slower speed.

The evidence strongly supports the claims on the benchmarks presented. One open question is whether the embedding extraction strategy influences results; the paper describes two strategies but does not compare them as an ablation.

## 7. Strengths, Limitations, and Failure Cases
A primary strength is achieving higher accuracy and better timeliness than uniform‑label baselines and external VLM monitors while remaining computationally light enough for real‑time deployment. The method also generalizes well to unseen tasks and to real‑robot execution, where the performance gap relative to baselines is maintained.

The main limitation is the reliance on the two assumptions: that failure trajectories contain at least one salient high‑score step, and that a sharp score increase reliably marks the failure onset. If these assumptions are violated—for example, if failure manifests gradually without a clear spike, or if the largest score jump occurs at a wrong time—the intra loss could provide misleading temporal structure. The paper does not report explicit failure cases where the proxy onset deviates substantially from the true failure moment. Scalability to very long‑horizon tasks or to VLAs with fundamentally different action representations (e.g., discrete actions) is also not addressed.

A hidden assumption is that success trajectories contain no steps that resemble failure. Hard negatives in the success set could cause the inter loss to push the success max higher, potentially raising false alarms during deployment.

## 8. Reproduction Notes
**Data**: LIBERO‑10, VLABench, and custom real‑robot CUBE and KITCHEN suites collected with π0.5.
**Preprocessing**: Action embeddings are extracted and then averaged over non‑overlapping windows (window size 4 or 8). Failure and success trajectories are paired for training.
**Model**: A single‑layer LSTM (hidden dimension not reported).
**Training**: Contrastive losses with margins $m_r=1.0$, $m_o=0.5$, weight $\lambda$ (unspecified). Optimization details (learning rate, batch size, scheduler) are not in the main text.
**Evaluation**: Conformal prediction thresholds are determined from calibration trajectories, with α around 0.15–0.25. Results are averaged over three random seeds.
**Baselines**: Five OOD detectors, four multi‑sampling methods (e.g., ensemble uncertainty), and two SAFE classifier variants.
**Missing details**: Exact LSTM hidden dimension, full hyperparameter schedule, precise implementation of embedding extraction for each VLA model, and the code repository link (the paper states “available at our project page” but no URL appears in the excerpt).

## 9. What to Read Closely
==Focus on Section 4.1 and the two loss equations, because they contain the technical novelty.== Examine Table 5 for the loss‑component ablation and Figure 3 for the accuracy–timeliness trade‑off; these directly support the claim that the contrastive formulation improves both accuracy and timeliness. The real‑robot results in Table 3 are important for assessing sim‑to‑real transfer. Skim Section 2 (related work) on a first pass, and defer the supplementary sections until you have understood the main method and results.

## 10. Research Ideas and Open Questions

**1. Learned soft onset instead of argmax proxy.** The current proxy $t_{\text{onset}} = \arg\max_t(s_t - s_{t-1})$ can be brittle on noisy score sequences. A small extension could train a lightweight module to predict onset location while regularizing with the intra loss. The evaluation would measure alignment with human‑annotated failure onsets on held‑out trajectories. Risk: additional parameters might overfit limited failure data.

**2. Multi‑sample inter‑trajectory contrastive loss.** The loss currently pairs one failure trajectory with one success trajectory, which may miss hard negative success examples. Modifying the computation to use in‑batch negatives (contrasting one failure trajectory against all success trajectories in the mini‑batch) could widen the score gap and reduce false alarms. A quick experiment would track whether $\max(s_t)$ in failure rises further above the success max and whether false‑alarm rates drop at the same conformal α. Risk: larger batch sizes could exceed GPU memory.

**3. Test on raw visual observations.** To determine if the gains require VLA‑internal representations, one could train the same LSTM detector on features from a frozen vision encoder (e.g., CLIP) using the same trajectory labels. Balanced accuracy on the unseen LIBERO split would serve as the metric. Risk: without policy‑specific information, the inter loss might latch onto irrelevant visual distractors, degrading temporal structure.

## Knowledge Graph & Connections

### Related Work Connections

**Connection to [[PPGuide]]**  
Both Hide‑and‑Seek and PPGuide tackle the problem of detecting or preempting failures in VLA-driven manipulation, and both rely on *coarsely supervised learning*—using only trajectory-level outcome labels to localize failure-indicative segments without step‑level annotations. PPGuide employs an attention‑based multiple‑instance learning (MIL) formulation to estimate which observation‑action chunks are relevant to success or failure, then trains a performance predictor that can steer the diffusion policy away from poor actions at inference time. Hide‑and‑Seek instead frames failure detection as a contrastive learning problem over per‑step action embeddings, with an inter‑trajectory loss that discriminates the most salient failure step and an intra‑trajectory loss that shapes the temporal score profile using a proxy onset. The key difference is that Hide‑and‑Seek is designed purely as a *monitor* that raises alarms, while PPGuide actively *guides* the policy. This distinction opens an opportunity: the contrastively learned failure scores from Hide‑and‑Seek could serve as a lightweight guidance signal similar to PPGuide’s predictor, combining detection with closed‑loop correction. Moreover, PPGuide’s MIL attention provides an alternative way to locate failure‑relevant chunks; comparing MIL‑based localization with contrastive onset discovery across the same benchmarks would shed light on which weak‑supervision mechanism yields more temporally precise and generalizable failure indicators.

**Connection to [[FASTER]]**  
FASTER focuses on reducing reaction latency in flow‑based VLAs by introducing a Horizon‑Aware Schedule that adaptively prioritizes near‑term actions during the flow‑matching denoising process. Hide‑and‑Seek evaluates its detector extensively on flow‑based policies (π0, π0.5) and extracts action embeddings from the hidden states just before the velocity head at the final denoising step. The two works are complementary at the deployment level: FASTER shortens the time‑to‑first‑action, while Hide‑and‑Seek monitors whether the executed actions are likely to fail. A more subtle connection lies in the fact that FASTER’s altered denoising schedule changes the internal state from which action embeddings are drawn; a detector trained on a default schedule might need recalibration when paired with a Horizon‑Aware Schedule, because the per‑step features and the timing of failure cues could shift. Investigating whether failure detection performance remains stable under FASTER‑accelerated rollouts would be a practical evaluation for future work. Conversely, if a detector signals an impending failure early enough, one could trigger a FASTER‑style fast resample or replan, merging detection with rapid recovery—a research avenue that bridges the two papers’ concerns with execution robustness.

**Tangential link to [[Not All Features Are Created Equal]]**  
The mechanistic study of VLA representations reveals that spatial visual features dominate action generation and that language sensitivity depends on task structure, but it does not directly engage with failure detection or weak supervision. The paper’s findings could inform *which* internal representations Hide‑and‑Seek should use: for instance, if the detector were trained on features from a layer that encodes more task‑relevant semantics rather than low‑level spatial coordinates, it might generalize better to visual distractor shifts. Currently, Hide‑and‑Seek simply aggregates embeddings from the action head or hidden states before the velocity head; a systematic analysis of how different VLA layers affect failure localization accuracy, guided by mechanistic insights, remains an open question and is not a strong methodological parallel.

### Concept Map

```mermaid
graph LR
    A[VLA Policy Rollout] --> B[Action Embeddings (per-step)]
    B --> C[Windowed Aggregation]
    C --> D[LSTM Detector]
    D --> E[Per-Step Failure Scores]
    E --> F[Inter-trajectory Contrastive Loss]
    E --> G[Intra-trajectory Contrastive Loss]
    F & G --> H[Training with Trajectory Labels Only]
    H --> D
    E --> I[Conformal Thresholds]
    I --> J[Binary Failure Alarm]
    L[PPGuide: MIL Attention for Weak Supervision] -.-> F
    M[FASTER: Horizon-Aware Schedule for Flow VLAs] -.-> A
```

*Solid lines* represent the core Hide‑and‑Seek pipeline; *dashed lines* connect to related concepts from the vault. PPGuide’s attention‑based MIL offers an alternative weak‑supervision localization mechanism, while FASTER’s schedule affects the VLA rollout from which embeddings are extracted.

### Questions For Future Reading

1. **How do failure detection methods that rely on weak temporal supervision (contrastive, MIL, etc.) scale to extremely long‑horizon tasks where failure may occur gradually over hundreds of steps without a sharp onset?**  
   Hide‑and‑Seek’s intra‑trajectory loss assumes a detectable jump in failure scores, but many real‑world failures (e.g., slowly drifting gripper, progressive slippage) lack a discrete moment. Evidence from future papers on long‑horizon manipulation could show whether contrastive onset proxies still align with human‑annotated failure points, or whether new temporal modeling techniques (e.g., continuous score smoothing, learned onset modules) are needed to maintain detection timeliness without increasing false positives.

2. **Can the failure signals learned from one VLA policy be transferred to another, especially across different action representations (autoregressive vs. flow‑matching), and what properties of the embedding space determine transferability?**  
   Hide‑and‑Seek extracts embeddings from frozen policies, but the paper shows it works on three different VLAs with separate training. Investigating whether a detector trained on π0 embeddings can detect failures in OpenVLA rollouts, perhaps after a lightweight adapter, would reveal if the detection is tied to policy‑specific idiosyncrasies or captures task‑level failure patterns. Future papers might benchmark transfer and analyze whether shared visual features or action‑prediction errors form the basis of generalizable failure signals.

3. **How should a failure detector and a policy guidance mechanism be combined to create a robust closed‑loop system, and what are the trade‑offs between early alarm thresholds and recovery latency?**  
   Hide‑and‑Seek stops at raising an alarm, while PPGuide uses predictor gradients to steer actions. If a detector triggers a recovery action (e.g., replanning, human takeover, or a PPGuide‑like guidance step), the optimal point to intervene depends on the cost of false alarms and the available recovery time. Evidence could compare systems where the detector’s conformal threshold is tuned jointly with a recovery policy’s success rate, showing whether the accuracy–timeliness trade‑off curves (Figure 3 in the paper) translate into improved task completion when paired with active interventions. This question links monitoring to control and highlights the need for holistic benchmarking of detection‑and‑recovery pipelines.

---
*Analysis by PaperBrain (x-ai/grok-4.3; refinement: deepseek/deepseek-v4-pro)*

## 📂 Resources
- **Local PDF**: [[HideandSeek in Trajectories Discovering Failure Signals for VLA Runtime Monitoring.pdf]]
- [Online PDF](https://arxiv.org/pdf/2605.30834.pdf)
- [ArXiv Link](https://huggingface.co/papers/2605.30834)
