# 📅 2026-02-16 - Paper Digest
## Summary
Total Papers: 43 | High Impact: 10

## 📝 Papers List
### 🔥 Xiaomi-Robotics-0: An Open-Sourced Vision-Language-Action Model with Real-Time Execution (Score: 8/10)
- **💡 Innovation**: The key novelty is the proposed combination of a cross-embodiment pre-training recipe that preserves underlying VLM visual-semantic knowledge, asynchronous post-training techniques to reduce inference latency, and timestep-aligned action chunk deployment strategies to enable seamless real-time VLA execution on consumer-grade GPUs for dexterous bimanual robot manipulation.
- **⚠️ Limitations**: The paper lacks ablation studies to quantify the individual contribution of each proposed training and deployment component, and does not explore integration with relevant advanced techniques including world models, 3D/4D Gaussian splatting, or diffusion models to further boost performance and generalization.
- **🔗 Link**: [[Xiaomi-Robotics-0]]
- **👥 Authors**: Rui Cai, Jun Guo, Xinze He, Piaopiao Jin, Jie Li, Bingxuan Lin, Futeng Liu, Wei Liu, Fei Ma, Kun Ma, Feng Qiu, Heng Qu, Yifei Su, Qiao Sun, Dong Wang, Donghao Wang, Yunhong Wang, Rujie Wu, Diyun Xiang, Yu Yang, Hangjun Ye, Yuan Zhang, Quanyun Zhou
- **🏷️ Tags**: 

---

### 🔥 Code2Worlds: Empowering Coding LLMs for 4D World Generation (Score: 8/10)
- **💡 Innovation**: The key novelty is the dual-stream Code2Worlds framework that disentangles retrieval-augmented object generation from hierarchical global scene orchestration, paired with a physics-aware closed-loop refinement pipeline using a PostProcess Agent and VLM-Motion Critic to eliminate physical hallucinations and improve dynamic fidelity of generated 4D simulation code.
- **⚠️ Limitations**: The work does not demonstrate downstream application of its generated 4D worlds to embodied AI, robot manipulation, or sim2real transfer tasks, nor does it explicitly specify if 4D Gaussian Splatting or other standard 4D representations are used for generated dynamic scenes, limiting its immediate applicability to your listed focus areas.
- **🔗 Link**: [[Code2Worlds]]
- **👥 Authors**: Yi Zhang, Yunshuang Wang, Zeyu Zhang, Hao Tang
- **🏷️ Tags**: 

---

### 🔥 GeneralVLA: Generalizable Vision-Language-Action Models with Knowledge-Guided Trajectory Planning (Score: 8/10)
- **💡 Innovation**: The key novelty is the proposed three-module hierarchical GeneralVLA architecture that combines an affordance segmentation module, knowledge-guided 3D trajectory planning agent, and 3D-aware low-level control policy to achieve zero-shot robot manipulation and scalable high-quality robotic demonstration generation without requiring any real-world robotic data or human demonstrations, outperforming existing state-of-the-art VLA methods like VoxPoser.
- **⚠️ Limitations**: The work does not report validation on physical real-world robot hardware, lacks evaluation of sim2real transfer robustness, and does not explore integration with advanced scene representation and generation techniques such as 3D/4D Gaussian Splatting or diffusion models to further boost performance.
- **🔗 Link**: [[GeneralVLA]]
- **👥 Authors**: Guoqing Ma, Siheng Wang, Zeyu Zhang, Shan Yu, Hao Tang
- **🏷️ Tags**: 

---

### ✨ DexEvolve: Evolutionary Optimization for Robust and Diverse Dexterous Grasp Synthesis (Score: 7/10)
- **💡 Innovation**: The key novelty is a scalable generate-and-refine dexterous grasp synthesis pipeline that uses asynchronous gradient-free evolutionary optimization in high-fidelity Isaac Sim to improve suboptimal analytically generated grasps while preserving diversity, then distills the refined grasp distribution into a diffusion model for robust real-world deployment.
- **⚠️ Limitations**: The work does not provide explicit quantitative real-world robotic deployment validation results, does not support cross-gripper morphology grasp transfer, and does not integrate or evaluate against other relevant technologies from your listed interests including 3D Gaussian Splatting, foundation models, or reinforcement learning for grasp optimization.
- **🔗 Link**: [Web Link](https://arxiv.org/abs/2602.15201)
- **👥 Authors**: René Zurbrügg, Andrei Cramariuc, Marco Hutter
- **🏷️ Tags**: 

---

### ✨ ABot-M0: VLA Foundation Model for Robotic Manipulation with Action Manifold Learning (Score: 7/10)
- **💡 Innovation**: The key novelty lies in the proposed Action Manifold Hypothesis and corresponding Action Manifold Learning with a DiT backbone for efficient stable action prediction, paired with the large-scale cross-robot UniACT dataset and modular dual-stream perception pipeline for generalizable VLA-based robotic manipulation.
- **⚠️ Limitations**: The work lacks explicit SOTA performance comparisons against existing state-of-the-art robotic VLAs, does not validate sim2real transfer, 3D Gaussian Splatting integration, or reinforcement learning fine-tuning, and provides no quantitative cross-robot transfer performance results in the abstract.
- **🔗 Link**: [Web Link](https://arxiv.org/abs/2602.11236)
- **👥 Authors**: Yandan Yang, Shuang Zeng, Tong Lin, Xinyuan Chang, Dekang Qi, Junjin Xiao, Haoyun Liu, Ronghan Chen, Yuzhi Chen, Dongjie Huo, Feng Xiong, Xing Wei, Zhiheng Ma, Mu Xu
- **🏷️ Tags**: 

---

### ✨ RLinf-Co: Reinforcement Learning-Based Sim-Real Co-Training for VLA Models (Score: 7/10)
- **💡 Innovation**: The key novelty is the proposed RL-based sim-real co-training (RL-Co) framework for VLA models, which uses a two-stage pipeline combining SFT warm-start on mixed real and simulated demonstrations with RL fine-tuning in simulation paired with an auxiliary real-world supervised loss to mitigate catastrophic forgetting, delivering better real-world manipulation performance and generalization than SFT-only co-training baselines.
- **⚠️ Limitations**: The work is only evaluated on simple tabletop manipulation tasks, does not explore integration with advanced perceptual representations like 3D/4D Gaussian Splatting or world models, and lacks validation on diverse robot morphologies and long-horizon complex tasks.
- **🔗 Link**: [Web Link](https://arxiv.org/abs/2602.12628)
- **👥 Authors**: Liangzhi Shi, Shuaihang Chen, Feng Gao, Yinuo Chen, Kang Chen, Tonghe Zhang, Hongzhi Zhang, Weinan Zhang, Chao Yu, Yu Wang
- **🏷️ Tags**: 

---

### ✨ OneVision-Encoder: Codec-Aligned Sparsity as a Foundational Principle for Multimodal Intelligence (Score: 6/10)
- **💡 Innovation**: The key novelty is the codec-aligned patch-level sparsity based OneVision-Encoder, which allocates computation exclusively to high-entropy visual regions, uses 3D RoPE for unified spatio-temporal reasoning, and outperforms state-of-the-art dense vision backbones across image, video and document understanding benchmarks when integrated with LLMs while consuming far fewer compute resources.
- **⚠️ Limitations**: The work does not evaluate the proposed encoder on robotics, embodied perception, or 3D scene understanding tasks relevant to your core research interests, nor does it validate its utility for downstream use cases including VLAs, robot manipulation, world model construction, or sim2real transfer pipelines.
- **🔗 Link**: [Web Link](https://arxiv.org/abs/2602.08683)
- **👥 Authors**: Feilong Tang, Xiang An, Yunyao Yan, Yin Xie, Bin Qin, Kaicheng Yang, Yifei Shen, Yuanhan Zhang, Chunyuan Li, Shikun Feng, Changrui Chen, Huajie Tan, Ming Hu, Manyuan Zhang, Bo Li, Ziyong Feng, Ziwei Liu, Zongyuan Ge, Jiankang Deng
- **🏷️ Tags**: 

---

### ✨ What does RL improve for Visual Reasoning? A Frankenstein-Style Analysis (Score: 6/10)
- **💡 Innovation**: The key novelty is the proposed Frankenstein-style three-component analysis framework consisting of causal probing for functional localization, parameter comparison for update characterization, and model merging for transferability test, to systematically disentangle the exact capabilities reinforcement learning improves for visual reasoning in vision-language models relative to supervised fine-tuning initialization.
- **⚠️ Limitations**: The work is limited to analyzing RL improvements on general visual reasoning tasks, and does not extend its analysis to robotics-aligned use cases such as embodied AI, robot manipulation, or VLA deployment, nor does it validate its findings on real-world robotic systems.
- **🔗 Link**: [Web Link](https://arxiv.org/abs/2602.12395)
- **👥 Authors**: Xirui Li, Ming Li, Tianyi Zhou
- **🏷️ Tags**: 

---

### ✨ On Robustness and Chain-of-Thought Consistency of RL-Finetuned VLMs (Score: 6/10)
- **💡 Innovation**: This work uncovers a previously underexplored accuracy-faithfulness tradeoff in RL-finetuned vision language models, demonstrates that controlled textual perturbations significantly degrade model robustness and chain-of-thought consistency, and quantifies the limited efficacy of adversarial augmentation and faithfulness-aware rewards for mitigating these vulnerabilities.
- **⚠️ Limitations**: The study only evaluates general multimodal reasoning VLMs without testing its findings on VLAs, robot manipulation pipelines, or embodied AI scenarios, and does not assess the impact of visual input perturbations or 3D perception modalities relevant to real-world robotics use cases.
- **🔗 Link**: [Web Link](https://arxiv.org/abs/2602.12506)
- **👥 Authors**: Rosie Zhao, Anshul Shah, Xiaoyu Zhu, Xinke Deng, Zhongyu Jiang, Yang Yang, Joerg Liebelt, Arnab Mondal
- **🏷️ Tags**: 

---

### ✨ FLAC: Maximum Entropy RL via Kinetic Energy Regularized Bridge Matching (Score: 5/10)
- **💡 Innovation**: The key novelty is formulating maximum entropy reinforcement learning for iterative generative policies (e.g., diffusion models) as a Generalized Schrödinger Bridge problem with kinetic energy regularization, removing the requirement for explicit action log-density estimation.
- **⚠️ Limitations**: The work is only validated on standard continuous control benchmarks, with no exploration of integration with embodied AI pipelines, robot manipulation tasks, foundation models, VLAs, or other domains aligned with your stated research interests.
- **🔗 Link**: [Web Link](https://arxiv.org/abs/2602.12829)
- **👥 Authors**: Lei Lv, Yunfei Li, Yu Luo, Fuchun Sun, Xiao Ma
- **🏷️ Tags**: 

---

### 📄 Zero-shot HOI Detection with MLLM-based Detector-agnostic Interaction Recognition (Score: 4/10)
- **💡 Innovation**: The key novelty is a decoupled detector-agnostic zero-shot HOI detection framework that separates object localization from interaction recognition, formulates interaction recognition as a deterministic visual question answering task using MLLMs, and introduces a spatial-aware pooling module and one-pass deterministic matching to boost performance and efficiency without requiring retraining of the underlying object detector.
- **⚠️ Limitations**: The work is only validated on static 2D image datasets, lacks support for temporal or 3D HOI reasoning, and is not evaluated for deployment in real-world robotic or embodied AI scenarios, limiting its direct applicability to your core research areas.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15124v1)
- **👥 Authors**: Shiyu Xuan, Dongkai Wang, Zechao Li, Jinhui Tang
- **🏷️ Tags**: 

---

### 📄 Zooming without Zooming: Region-to-Image Distillation for Fine-Grained Multimodal Perception (Score: 4/10)
- **💡 Innovation**: The key novelty is reframing inference-time agentic zooming for fine-grained multimodal large language model perception as a training-time primitive via a region-to-image distillation pipeline that uses teacher model supervision on zoomed micro-crops to train a student model that delivers comparable performance in a single forward pass without tool use, alongside the new ZoomBench benchmark for quantifying global-regional perceptual gaps.
- **⚠️ Limitations**: The work does not evaluate the utility of its improved fine-grained perception on downstream robotics, embodied AI, or dynamic 3D perception tasks, and does not test performance on real-world robotic sensory inputs rather than static 2D images.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.11858)
- **👥 Authors**: Lai Wei, Liangbo He, Jun Lan, Lingzhong Dong, Yutong Cai, Siyuan Li, Huijia Zhu, Weiqiang Wang, Linghe Kong, Yue Wang, Zhuosheng Zhang, Weiran Huang
- **🏷️ Tags**: 

---

### 📄 Seeing to Generalize: How Visual Data Corrects Binding Shortcuts (Score: 3/10)
- **💡 Innovation**: The key novelty is the discovery that cross-modal visual training for VLMs can improve text-only out-of-distribution generalization performance by disrupting positional binding shortcuts learned during text-only training and forcing the model to adopt more robust symbolic binding mechanisms that persist even in text-only task settings.
- **⚠️ Limitations**: The work only validates its findings on controlled synthetic retrieval tasks and basic LLM-to-VLM transition cases, without exploring real-world complex reasoning applications or the transfer of the observed binding improvement to robotics, embodied AI, or other related domains in your research interests.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15183v1)
- **👥 Authors**: Nicolas Buzeta, Felipe del Rio, Cristian Hinostroza, Denis Parra, Hans Lobel, Rodrigo Toro Icarte
- **🏷️ Tags**: 

---

### 📄 Quantized Evolution Strategies: High-precision Fine-tuning of Quantized LLMs at Low-precision Cost (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposed Quantized Evolution Strategies (QES) optimization paradigm that supports full-parameter fine-tuning directly in the discrete quantized LLM parameter space, using accumulated error feedback to preserve high-precision gradient signals and stateless seed replay to reduce memory overhead to low-precision inference levels.
- **⚠️ Limitations**: The paper only validates QES on arithmetic reasoning tasks for LLMs, with no exploration of its applicability to other foundation model variants, embodied AI/robotics downstream tasks, or practical edge device deployment performance.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.03120)
- **👥 Authors**: Yinggan Xu, Risto Miikkulainen, Xin Qiu
- **🏷️ Tags**: 

---

### 📄 MyoInteract: A Framework for Fast Prototyping of Biomechanical HCI Tasks using Reinforcement Learning (Score: 2/10)
- **💡 Innovation**: The key novelty is the development of MyoInteract, a GUI-enabled biomechanical reinforcement learning framework guided by the Human Action Cycle design lens that cuts task prototyping and model training time by up to 98%, allowing non-expert interaction designers to build and evaluate muscle-actuated simulated user tasks in under an hour instead of multiple days.
- **⚠️ Limitations**: The work does not explore real-world transfer of trained biomechanical policies, nor does it integrate any modern robotics/AI techniques in your stated interest areas such as foundation models, 3D Gaussian Splatting or embodied AI to expand its use cases beyond HCI biomechanics prototyping.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15245v1)
- **👥 Authors**: Ankit Bhattarai, Hannah Selder, Florian Fischer, Arthur Fleig, Per Ola Kristensson
- **🏷️ Tags**: 

---

### 📄 Closing the Distribution Gap in Adversarial Training for LLMs (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed Distributional Adversarial Training (DAT) framework that leverages Diffusion LLMs to approximate the true joint distribution of prompts and responses to generate diverse high-likelihood training samples, addressing the distribution coverage gap of existing LLM adversarial training methods to improve adversarial robustness.
- **⚠️ Limitations**: The work lacks ablation studies on how Diffusion LLM sample quality and diversity impact DAT performance, does not evaluate generalization to non-adversarial downstream tasks, and has no demonstrated relevance to the embodied AI, robot manipulation, or 3D perception domains that are the core of the user's research interests.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15238v2)
- **👥 Authors**: Chengzhi Hu, Jonas Dornbusch, David Lüdke, Stephan Günnemann, Leo Schwinn
- **🏷️ Tags**: 

---

### 📄 Automatically Finding Reward Model Biases (Score: 2/10)
- **💡 Innovation**: The key novelty is an LLM-powered iterative evolutionary search pipeline that automatically identifies both known and previously unreported spurious biases in natural language reward models used for LLM post-training.
- **⚠️ Limitations**: The work only evaluates text-domain reward models, does not explore generalizability to multi-modal or robotics-related reward models, and does not provide concrete mitigation strategies for the detected biases.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15222v1)
- **👥 Authors**: Atticus Wang, Iván Arcuschin, Arthur Conmy
- **🏷️ Tags**: 

---

### 📄 Secure and Energy-Efficient Wireless Agentic AI Networks (Score: 2/10)
- **💡 Innovation**: The key novelty is two proposed resource allocation schemes, iterative ADMM-based ASC and LLM-powered LAW, that jointly optimize AI agent selection, base station beamforming, and agent transmission power to minimize network energy consumption while meeting latency, reasoning accuracy, and communication confidentiality constraints for wireless agentic AI networks.
- **⚠️ Limitations**: The work does not validate the generalizability of its LLM optimizer to non-wireless agentic workflows, does not explore applications to embodied AI or robotic use cases aligned with common agentic AI research directions, and lacks comparison to other foundation model-based resource allocation baselines.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15212v1)
- **👥 Authors**: Yuanyan Song, Kezhi Wang, Xinmian Xu
- **🏷️ Tags**: 

---

### 📄 ÜberWeb: Insights from Multilingual Curation for a 20-Trillion-Token Dataset (Score: 2/10)
- **💡 Innovation**: The key novelty is demonstrating that targeted per-language multilingual data curation mitigates the so-called curse of multilinguality without requiring large proportions of non-English tokens, and introducing a 20-trillion-token public multilingual pretraining corpus that enables far more compute-efficient multilingual foundation model training than existing public baselines.
- **⚠️ Limitations**: The work does not evaluate the performance of the curated corpus for non-text or cross-modal foundation model use cases, nor does it provide granular analysis of curation efficacy for extremely low-resource languages with very limited public data availability.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15210v3)
- **👥 Authors**: DatologyAI, :, Aldo Gael Carranza, Kaleigh Mentzer, Ricardo Pio Monti, Alex Fang, Alvin Deng, Amro Abbas, Anshuman Suri, Brett Larsen, Cody Blakeney, Darren Teh, David Schwab, Diego Kiner, Fan Pan, Haakon Mongstad, Haoli Yin, Jack Urbanek, Jason Lee, Jason Telanoff, Josh Wills, Luke Merrick, Maximilian Böther, Parth Doshi, Paul Burstein, Pratyush Maini, Rishabh Adiga, Siddharth Joshi, Spandan Das, Tony Jiang, Vineeth Dorna, Zhengping Wang, Bogdan Gaza, Ari Morcos, Matthew Leavitt
- **🏷️ Tags**: 

---

### 📄 Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposal of Colosseum, a formal auditing framework that quantifies collusive behavior in LLM-based cooperative multi-agent systems using regret metrics relative to the Distributed Constraint Optimization Problem (DCOP) cooperative optimum across varied objectives, persuasion tactics, and agent network topologies.
- **⚠️ Limitations**: This work is limited to abstract text-only LLM multi-agent interactions in simulated DCOP settings, with no validation in embodied or real-world task environments, and does not propose any mitigations for detected collusive behavior.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15198v1)
- **👥 Authors**: Mason Nakamura, Abhinav Kumar, Saswat Das, Sahar Abdelnabi, Saaduddin Mahmud, Ferdinando Fioretto, Shlomo Zilberstein, Eugene Bagdasarian
- **🏷️ Tags**: 

---

### 📄 OpaqueToolsBench: Learning Nuances of Tool Behavior Through Interaction (Score: 2/10)
- **💡 Innovation**: The key novelty is the introduction of OpaqueToolsBench, a benchmark for evaluating LLM agent performance on underspecified opaque tool use, alongside ToolObserver, an iterative framework that refines tool documentation from execution feedback to outperform baselines with 3.5-7.5x lower token consumption.
- **⚠️ Limitations**: The work is limited exclusively to text-based tool calling scenarios, with no evaluation of generalization to embodied AI tasks, physical robot tool manipulation, or integration with robotics-related foundation models like VLAs, so it has no applicability to most of your stated research interests.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15197v1)
- **👥 Authors**: Skyler Hallinan, Thejas Venkatesh, Xiang Ren, Sai Praneeth Karimireddy, Ashwin Paranjape, Yuhao Zhang, Jack Hessel
- **🏷️ Tags**: 

---

### 📄 Weight space Detection of Backdoors in LoRA Adapters (Score: 2/10)
- **💡 Innovation**: The key novelty is a data-agnostic backdoor detection approach for LoRA adapters that directly analyzes weight matrix singular value statistics instead of requiring test inputs or known backdoor triggers, achieving high detection accuracy with low false positive rates.
- **⚠️ Limitations**: The method is only validated on LoRA adapters fine-tuned for the Llama-3.2-3B LLM on NLP tasks, with no evaluation of its generalizability to other model architectures, adapter types, or non-NLP use cases relevant to your research interests.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15195v2)
- **👥 Authors**: David Puertolas Merenciano, Ekaterina Vasyagina, Raghav Dixit, Kevin Zhu, Ruizhe Li, Javier Ferrando, Maheep Chaudhary
- **🏷️ Tags**: 

---

### 📄 Time-Archival Camera Virtualization for Sports and Visual Performances (Score: 2/10)
- **💡 Innovation**: The key novelty is a neural volume rendering formulation for dynamic scene representation that supports time-archival retrospective novel view synthesis for fast-paced non-rigid scenes such as sports and stage performances, addressing tracking failures of existing 3D/4D Gaussian Splatting variants for rapid multi-subject motions.
- **⚠️ Limitations**: The provided abstract lacks quantitative benchmark comparisons against state-of-the-art dynamic novel view synthesis methods, and does not explore any use cases relevant to your core research interests in robotics, embodied AI, foundation models, or reinforcement learning.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15181v1)
- **👥 Authors**: Yunxiao Zhang, William Stone, Suryansh Kumar
- **🏷️ Tags**: 

---

### 📄 Mind the (DH) Gap! A Contrast in Risky Choices Between Reasoning and Conversational LLMs (Score: 2/10)
- **💡 Innovation**: The key novelty is a large-scale comparative study across 20 frontier and open LLMs paired with matched human subject experiments that identifies two distinct LLM clusters (reasoning models vs conversational models) with divergent risky choice behavior, and links the observed performance gap to mathematical reasoning training.
- **⚠️ Limitations**: The work only evaluates LLMs on abstract hypothetical risky choice tasks, does not test the generalizability of its findings to real-world agentic, robotic, or embodied AI use cases, and does not fully isolate other fine-tuning factors beyond mathematical reasoning training that could drive the observed behavioral differences.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15173v1)
- **👥 Authors**: Luise Ge, Yongyan Zhang, Yevgeniy Vorobeychik
- **🏷️ Tags**: 

---

### 📄 Panini: Continual Learning in Token Space via Structured Memory (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed Panini non-parametric continual learning framework, which represents incoming documents as entity- and event-aware Generative Semantic Workspace networks of QA pairs to eliminate the need for verbatim chunk retrieval, cutting inference context token usage while improving QA performance and reducing hallucinations.
- **⚠️ Limitations**: The work is only validated on text-only question answering benchmarks, does not explore applicability to multi-modal or embodied AI scenarios, and lacks comparison against state-of-the-art parametric LLM continual learning baselines.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15156v1)
- **👥 Authors**: Shreyas Rajesh, Pavan Holur, Mehmet Yigit Turali, Chenda Duan, Vwani Roychowdhury
- **🏷️ Tags**: 

---

### 📄 Protecting Language Models Against Unauthorized Distillation through Trace Rewriting (Score: 2/10)
- **💡 Innovation**: The key novelty is a suite of dynamic LLM reasoning trace rewriting methods including instruction-based LLM rewriting and gradient-based techniques that simultaneously achieve strong anti-distillation effects to deter unauthorized knowledge distillation and reliable verifiable API watermarking, while preserving or even improving teacher model response correctness and semantic coherence.
- **⚠️ Limitations**: The work does not evaluate robustness against adaptive adversaries that explicitly attempt to reverse the trace rewriting to recover usable distillation data or remove embedded watermarks, nor does it explore applicability to multimodal, embodied, or robotics-related LLM use cases aligned with your stated interests.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15143v1)
- **👥 Authors**: Xinhang Ma, William Yeoh, Ning Zhang, Yevgeniy Vorobeychik
- **🏷️ Tags**: 

---

### 📄 EditCtrl: Disentangled Local and Global Control for Real-Time Generative Video Editing (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed EditCtrl framework, which adopts a local-first computation paradigm only operating on masked edit tokens paired with a lightweight temporal global context embedder, achieving 10x higher compute efficiency and better editing quality than prior full-attention based generative video editing methods.
- **⚠️ Limitations**: The work is only validated on standard 2D generative video editing tasks, lacks exploration of applications to 3D dynamic scene editing or embodied perception scenarios, and does not report performance on extremely long-form videos or ultra-fine-grained sparse edits.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15031v1)
- **👥 Authors**: Yehonathan Litman, Shikun Liu, Dario Seyb, Nicholas Milef, Yang Zhou, Carl Marshall, Shubham Tulsiani, Caleb Leak
- **🏷️ Tags**: 

---

### 📄 Image Generation with a Sphere Encoder (Score: 2/10)
- **💡 Innovation**: The key novelty is a lightweight generative framework that maps natural images to a uniform spherical latent space, enabling high-fidelity image generation in fewer than 5 forward passes with far lower inference cost than comparable multi-step diffusion models.
- **⚠️ Limitations**: This work is restricted to 2D image generation tasks, provides no applications or extensions to robotics, embodied AI, or 3D content generation use cases aligned with the user's interests, and does not evaluate the generalizability of its spherical latent space to cross-modal or sequential decision-making settings.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15030v1)
- **👥 Authors**: Kaiyu Yue, Menglin Jia, Ji Hou, Tom Goldstein
- **🏷️ Tags**: 

---

### 📄 Less is Enough: Synthesizing Diverse Data in Feature Space of LLMs (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposal of the Feature Activation Coverage (FAC) metric to quantify LLM post-training data diversity in interpretable feature space, paired with a FAC Synthesis framework that uses sparse autoencoders to identify missing features in seed datasets and generate targeted synthetic data covering these features to improve downstream LLM performance.
- **⚠️ Limitations**: The work only validates its approach on text-only LLM tasks, does not explore applicability to multi-modal foundation models or robotics/embodied AI use cases, and fails to analyze the computational overhead tradeoff of the sparse autoencoder-based feature identification and synthesis pipeline.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.10388)
- **👥 Authors**: Zhongzhi Li, Xuansheng Wu, Yijiang Li, Lijie Hu, Ninghao Liu
- **🏷️ Tags**: 

---

### 📄 MedXIAOHE: A Comprehensive Recipe for Building Medical MLLMs (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed entity-aware continual pretraining framework for organizing heterogeneous medical corpora, paired with reinforcement learning and tool-augmented agentic training, to build a medical vision-language foundation model that achieves state-of-the-art performance across diverse medical benchmarks with verifiable reasoning traces and low hallucination.
- **⚠️ Limitations**: The work is entirely focused on the medical domain, does not explore applications or generalizability to robotics, embodied AI, or other subfields relevant to the user's stated interests, and does not release the full model weights for independent third-party validation.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.12705)
- **👥 Authors**: Baorong Shi, Bo Cui, Boyuan Jiang, Deli Yu, Fang Qian, Haihua Yang, Huichao Wang, Jiale Chen, Jianfei Pan, Jieqiong Cao, Jinghao Lin, Kai Wu, Lin Yang, Shengsheng Yao, Tao Chen, Xiaojun Xiao, Xiaozhong Ji, Xu Wang, Yijun He, Zhixiong Yang
- **🏷️ Tags**: 

---

### 📄 GeoAgent: Learning to Geolocate Everywhere with Reinforced Geographic Characteristics (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposal of the expert-annotated GeoSeek geolocation chain-of-thought dataset paired with custom geographic-similarity and consistency rewards for reinforcement learning training, leading to a geolocation model that outperforms existing baselines and general VLLMs.
- **⚠️ Limitations**: The work lacks ablation studies to disentangle the individual contribution of each proposed reward function, does not evaluate performance on occluded or low-quality geolocation inputs, and does not explore cross-domain applicability to non-geographic reasoning tasks.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.12617)
- **👥 Authors**: Modi Jin, Yiming Zhang, Boyuan Sun, Dingwen Zhang, MingMing Cheng, Qibin Hou
- **🏷️ Tags**: 

---

### 📄 BPDQ: Bit-Plane Decomposition Quantization on a Variable Grid for Large Language Models (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed Bit-Plane Decomposition Quantization (BPDQ) framework that uses a variable rather than fixed shape-invariant quantization grid, paired with approximate second-order iterative refinement and progressive quantization error compensation, to improve 2-3 bit post-training quantization performance for large language models.
- **⚠️ Limitations**: The work only validates performance on standard LLM reasoning benchmarks like GSM8K, does not evaluate applicability to downstream robotics or embodied AI use cases, and lacks comparison to the full range of state-of-the-art low-bit LLM quantization methods across more diverse task categories and model sizes.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.04163)
- **👥 Authors**: Junyu Chen, Jungang Li, Jing Xiong, Wenjie Wang, Qingyao Yang, He Xiao, Zhen Li, Taiqiang Wu, Mengzhao Chen, Zhen Peng, Chaofan Tao, Long Shi, Hongxia Yang, Ngai Wong
- **🏷️ Tags**: 

---

### 📄 Towards Universal Video MLLMs with Attribute-Structured and Quality-Verified Instructions (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposal of the 1M-sample ASID-1M structured fine-grained audiovisual instruction dataset, the scalable ASID-Verify annotation curation pipeline with automatic semantic and temporal consistency verification, and the ASID-Captioner video MLLM that achieves state-of-the-art performance among open-source video understanding models.
- **⚠️ Limitations**: The work is only evaluated on general audiovisual understanding tasks, with no exploration of applications to embodied AI, robot manipulation or other robotics scenarios relevant to your interests, and does not involve any of the 3D/4D Gaussian Splatting, diffusion model, reinforcement learning or sim2real techniques you focus on.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.13013)
- **👥 Authors**: Yunheng Li, Hengrui Zhang, Meng-Hao Guo, Wenzhao Gao, Shaoyong Jia, Shaohui Jiao, Qibin Hou, Ming-Ming Cheng
- **🏷️ Tags**: 

---

### 📄 SciAgentGym: Benchmarking Multi-Step Scientific Tool-use in LLM Agents (Score: 2/10)
- **💡 Innovation**: The key novelty lies in the proposal of SciAgentGym, a scalable interactive scientific tool-use environment with 1,780 cross-domain tools, paired with the tiered SciAgentBench evaluation suite and the SciForge dependency-graph based logic-aware training trajectory synthesis method to boost LLM agents' multi-step scientific workflow performance.
- **⚠️ Limitations**: The work is restricted to text-only LLM scientific tool-use tasks, has no integration or evaluation for embodied AI, robot manipulation, 3D perception or other core research areas of your interest, and does not verify the generalizability of its proposed method to non-scientific agent workflows.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.12984)
- **👥 Authors**: Yujiong Shen, Yajie Yang, Zhiheng Xi, Binze Hu, Huayu Sha, Jiazheng Zhang, Qiyuan Peng, Junlin Shang, Jixuan Huang, Yutao Fan, Jingqi Tong, Shihan Dou, Ming Zhang, Lei Bai, Zhenfei Yin, Tao Gui, Xingjun Ma, Qi Zhang, Xuanjing Huang, Yu-Gang Jiang
- **🏷️ Tags**: 

---

### 📄 DICE: Diffusion Large Language Models Excel at Generating CUDA Kernels (Score: 2/10)
- **💡 Innovation**: The key novelty is the construction of the CuKe augmented supervised fine-tuning dataset optimized for high-performance CUDA kernels and the proposed bi-phase curated reinforcement learning (BiC-RL) framework to train DICE, a series of diffusion large language models that achieve new state-of-the-art CUDA kernel generation performance.
- **⚠️ Limitations**: The work does not explore generalization of DICE to other code generation domains, lacks ablation studies to disentangle the performance contribution of the CuKe dataset versus the BiC-RL training framework, and does not validate real-world utility of generated kernels in downstream applications like robotics simulation acceleration.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.11715)
- **👥 Authors**: Haolei Bai, Lingcheng Kong, Xueyi Chen, Jianmian Wang, Zhiqiang Tao, Huan Wang
- **🏷️ Tags**: 

---

### 📄 Principled Synthetic Data Enables the First Scaling Laws for LLMs in Recommendation (Score: 2/10)
- **💡 Innovation**: The key novelty is a layered pedagogical synthetic data generation framework for recommendation tasks that addresses noise, bias and incompleteness flaws in real user interaction data, enabling the first empirical demonstration of robust power-law scaling for continually pre-trained LLMs in the recommendation domain, with models trained on the synthetic data significantly outperforming those trained on real user data on downstream ranking tasks.
- **⚠️ Limitations**: The work does not validate whether its synthetic data framework and observed scaling laws generalize to domains outside of recommendation, nor does it assess potential downstream biases or fairness issues arising from the curated synthetic training data distribution.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.07298)
- **👥 Authors**: Benyu Zhang, Qiang Zhang, Jianpeng Cheng, Hong-You Chen, Qifei Wang, Wei Sun, Shen Li, Jia Li, Jiahao Wu, Xiangjun Fan, Hong Yan
- **🏷️ Tags**: 

---

### 📄 Self-EvolveRec: Self-Evolving Recommender Systems with LLM-based Directional Feedback (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed Self-EvolveRec framework, which implements a directional LLM-powered feedback loop combining qualitative user simulator critiques and quantitative model diagnosis verification, plus a model co-evolution strategy that dynamically updates evaluation criteria as recommender architectures evolve to address the limitations of fixed search spaces and scalar-only feedback in existing automated recommender system design methods.
- **⚠️ Limitations**: The work is restricted exclusively to the recommender system domain, has no applicability to the listed robotics, embodied AI, 3D vision, or robot manipulation research interests, and provides no analysis of whether its co-evolution feedback paradigm generalizes to non-recommendation task settings.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.12612)
- **👥 Authors**: Sein Kim, Sangwu Park, Hongseok Kang, Wonjoong Kim, Jimin Seo, Yeonjun In, Kanghoon Yoon, Chanyoung Park
- **🏷️ Tags**: 

---

### 📄 Favia: Forensic Agent for Vulnerability-fix Identification and Analysis (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed Favia framework, which pairs an efficient initial commit ranking stage with a ReAct-based LLM agent that iteratively navigates pre-commit codebase environments and uses specialized tools to establish causal alignment between code changes and vulnerability root causes, outperforming existing baselines on a new large-scale realistic dataset of real-world commits.
- **⚠️ Limitations**: The paper does not assess Favia's generalization to low-resource programming languages or smaller niche repository ecosystems, and it does not quantify the latency and computational overhead of the iterative LLM reasoning step for deployment in real-time enterprise security workflows.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.12500)
- **👥 Authors**: André Storhaug, Jiamou Sun, Jingyue Li
- **🏷️ Tags**: 

---

### 📄 Scaling Laws for Masked-Reconstruction Transformers on Single-Cell Transcriptomics (Score: 1/10)
- **💡 Innovation**: This work presents the first systematic empirical demonstration that power-law neural scaling laws analogous to those observed in natural language processing emerge for masked-reconstruction transformers trained on large single-cell RNA sequencing datasets when sufficient training data is available.
- **⚠️ Limitations**: The study only tests scaling behavior across two narrow scRNA-seq experimental regimes, does not validate whether the observed loss scaling translates to improved performance on practical downstream single-cell analysis tasks, and only provides an unrefined preliminary estimate of per-masked-gene entropy.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15253v1)
- **👥 Authors**: Ihor Kendiukhov
- **🏷️ Tags**: 

---

### 📄 ScrapeGraphAI-100k: A Large-Scale Dataset for LLM-Based Web Information Extraction (Score: 1/10)
- **💡 Innovation**: The key novelty is the release of ScrapeGraphAI-100k, a large-scale curated real-world dataset of LLM web information extraction events containing Markdown content, prompts, JSON schemas, LLM responses and validation metadata, which addresses the limitations of existing small, synthetic, text-only datasets in the web information extraction domain.
- **⚠️ Limitations**: The work is exclusively focused on web information extraction use cases, lacks multimodal web content such as visual UI elements, and has no applicability to the user's core research interests including robotics, embodied AI and 3D perception for robotics.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15189v1)
- **👥 Authors**: William Brach, Francesco Zuppichini, Marco Vinciguerra, Lorenzo Padoan
- **🏷️ Tags**: 

---

### 📄 Beyond Reinforcement Learning: Fast and Scalable Quantum Circuit Synthesis (Score: 1/10)
- **💡 Innovation**: The key novelty is combining a lightweight supervised learning model that approximates the minimum description length of residual unitaries with stochastic beam search to achieve low-training-overhead, zero-shot quantum unitary synthesis that outperforms prior state-of-the-art methods on both synthesis speed and success rate.
- **⚠️ Limitations**: The work lacks ablation studies validating the contribution of individual core components, and does not test the performance of synthesized circuits on real quantum hardware to confirm real-world applicability.
- **🔗 Link**: [Link](http://arxiv.org/abs/2602.15146v2)
- **👥 Authors**: Lukas Theißinger, Thore Gerlach, David Berghaus, Christian Bauckhage
- **🏷️ Tags**: 

---

### 📄 TADA! Tuning Audio Diffusion Models through Activation Steering (Score: 1/10)
- **💡 Innovation**: The key novelty is identifying that high-level semantic musical concepts including instruments, vocals, genre, tempo and mood are controlled by a small shared subset of attention layers in state-of-the-art audio diffusion models, and demonstrating that steering activations in these layers via contrastive activation addition and sparse autoencoders enables highly precise control over generated audio properties.
- **⚠️ Limitations**: The work only validates its activation steering approach on audio diffusion models for music generation, does not explore generalizability to other diffusion application domains, and lacks formal theoretical justification for the observed specialization of the identified attention layers.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.11910)
- **👥 Authors**: Łukasz Staniszewski, Katarzyna Zaleska, Mateusz Modrzejewski, Kamil Deja
- **🏷️ Tags**: 

---

### 📄 scPilot: Large Language Model Reasoning Toward Automated Single-Cell Analysis and Discovery (Score: 1/10)
- **💡 Innovation**: The key novelty is the proposal of scPilot, the first systematic omics-native LLM reasoning framework that automates core single-cell RNA-seq analysis tasks via iterative, justifiable step-by-step reasoning, along with the curated scBench benchmark suite for evaluating LLM omics reasoning performance.
- **⚠️ Limitations**: This work is entirely focused on the computational biology domain with no application or relevance to your interested robotics and embodied AI research areas, and only evaluates performance on closed-source state-of-the-art LLMs without testing on smaller, open-access model variants.
- **🔗 Link**: [Link](https://huggingface.co/papers/2602.11609)
- **👥 Authors**: Yiming Gao, Zhen Wang, Jefferson Chen, Mark Antkowiak, Mengzhou Hu, JungHo Kong, Dexter Pratt, Jieyuan Liu, Enze Ma, Zhiting Hu, Eric P. Xing
- **🏷️ Tags**: 

---

