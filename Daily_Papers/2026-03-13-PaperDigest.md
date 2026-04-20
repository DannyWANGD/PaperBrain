# 📅 2026-03-13 - Paper Digest
## Summary
Total Papers: 24 | High Impact: 5

## 📝 Papers List
### 🔥 Simple Recipe Works: Vision-Language-Action Models are Natural Continual Learners with Reinforcement Learning (Score: 9/10)
- **💡 Innovation**: The paper demonstrates that simple Sequential Fine-Tuning with LoRA, when applied to pretrained VLA models using on-policy RL, effectively mitigates catastrophic forgetting without requiring complex continual learning architectures.
- **⚠️ Limitations**: The study focuses primarily on simulation-based benchmarks, leaving the long-term stability and performance of this approach in diverse, unconstrained real-world physical environments less explored.
- **🔗 Link**: [[Simple Recipe Works]]
- **👥 Authors**: Jiaheng Hu, Jay Shim, Chen Tang, Yoonchang Sung, Bo Liu, Peter Stone, Roberto Martin-Martin
- **🏷️ Tags**: #VLA #Reinforcement_Learning #Embodied_AI #Foundation_Model #Robot_Manipulation

---

### 🔥 OmniStream: Mastering Perception, Reconstruction and Action in Continuous Streams (Score: 8/10)
- **💡 Innovation**: OmniStream introduces a unified streaming visual backbone that integrates causal spatiotemporal attention and 3D-RoPE to enable simultaneous semantic perception, geometric reconstruction, and action prediction within a persistent KV-cache framework.
- **⚠️ Limitations**: The paper relies on a frozen backbone, which may limit the model's ability to adapt to highly specialized or novel downstream robotic tasks compared to fine-tuned alternatives.
- **🔗 Link**: [[OmniStream]]
- **👥 Authors**: Yibin Yan, Jilan Xu, Shangzhe Di, Haoning Wu, Weidi Xie
- **🏷️ Tags**: #Embodied_AI #Robot_Manipulation #Foundation_Model #VLA

---

### ✨ DVD: Deterministic Video Depth Estimation with Generative Priors (Score: 7/10)
- **💡 Innovation**: DVD introduces a deterministic regression framework that repurposes pre-trained video diffusion models for depth estimation by using the diffusion timestep as a structural anchor and applying latent manifold rectification.
- **⚠️ Limitations**: The paper focuses on video depth estimation as a standalone task and does not explicitly demonstrate integration into closed-loop robotic control or real-time embodied feedback loops.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12250)
- **👥 Authors**: Hongfei Zhang, Harold Haodong Chen, Chenfei Liao, Jing He, Zixin Zhang, Haodong Li, Yihao Liang, Kanghao Chen, Bin Ren, Xu Zheng, Shuai Yang, Kun Zhou, Yinchuan Li, Nicu Sebe, Ying-Cong Chen
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #Embodied_AI

---

### ✨ DIVE: Scaling Diversity in Agentic Task Synthesis for Generalizable Tool Use (Score: 7/10)
- **💡 Innovation**: DIVE introduces an 'evidence-driven' synthesis approach that inverts the traditional task-generation pipeline by executing real-world tools first and reverse-deriving tasks from the resulting traces to ensure grounding by construction.
- **⚠️ Limitations**: The paper focuses primarily on tool-use in digital or abstract environments, leaving the physical grounding and sensorimotor challenges inherent in real-world robotic manipulation largely unaddressed.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.11076)
- **👥 Authors**: Aili Chen, Chi Zhang, Junteng Liu, Jiangjie Chen, Chengyu Du, Yunji Li, Ming Zhong, Qin Wang, Zhengmao Zhu, Jiayuan Song, Ke Ji, Junxian He, Pengyu Zhao, Yanghua Xiao
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Automatic Generation of High-Performance RL Environments (Score: 7/10)
- **💡 Innovation**: The paper introduces a systematic, agent-driven framework for automatically translating complex, legacy, or specification-based environments into high-performance, GPU-parallelized JAX/Rust implementations.
- **⚠️ Limitations**: The methodology relies heavily on the availability of clear specifications or existing reference implementations, and it remains unclear how well this approach scales to environments with highly complex, non-deterministic physics or non-standard state spaces.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12145)
- **👥 Authors**: Seth Karten, Rahul Dev Appapogu, Chi Jin
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Sim2Real

---

### ✨ RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning (Score: 6/10)
- **💡 Innovation**: RubiCap introduces a rubric-guided reinforcement learning framework that uses LLMs to generate structured, multi-faceted reward signals for dense image captioning, bypassing the need for deterministic checkers.
- **⚠️ Limitations**: The reliance on LLM-based judges for reward computation introduces significant computational overhead during training and potential biases inherent to the judge model.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09160)
- **👥 Authors**: Tzu-Heng Huang, Sirajul Salekin, Javier Movellan, Frederic Sala, Manjot Bilkhu
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ PACED: Distillation at the Frontier of Student Competence (Score: 6/10)
- **💡 Innovation**: The paper introduces a principled weighting framework for distillation that dynamically focuses training on the student's 'zone of proximal development' by using a Beta-kernel to optimize the signal-to-noise ratio of distillation gradients.
- **⚠️ Limitations**: The evaluation is restricted to reasoning benchmarks and language-based instruction tuning, leaving the efficacy of this distillation strategy in high-dimensional, continuous-action spaces like VLA or robotic control unverified.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.11178)
- **👥 Authors**: Yuanda Xu, Hejian Sang, Zhengze Zhou, Ran He, Zhipeng Wang
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ EndoCoT: Scaling Endogenous Chain-of-Thought Reasoning in Diffusion Models (Score: 5/10)
- **💡 Innovation**: The paper introduces an iterative thought guidance module that forces MLLMs to perform multi-step reasoning before conditioning the denoising process of a Diffusion Transformer.
- **⚠️ Limitations**: The evaluation is restricted to abstract reasoning benchmarks (Maze, TSP, Sudoku) rather than physical robot manipulation or embodied control tasks, limiting its immediate applicability to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12252)
- **👥 Authors**: Xuanlang Dai, Yujie Zhou, Long Xing, Jiazi Bu, Xilin Wei, Yuhong Liu, Beichen Zhang, Kai Chen, Yuhang Zang
- **🏷️ Tags**: #Diffusion_Model #LLM #Foundation_Model

---

### ✨ The Curse and Blessing of Mean Bias in FP4-Quantized LLM Training (Score: 5/10)
- **💡 Innovation**: The paper identifies that rank-one mean bias in LLM activations is the primary driver of dynamic-range inflation in low-bit quantization and proposes a simple mean-subtraction technique to stabilize FP4 training.
- **⚠️ Limitations**: The study focuses exclusively on text-based LLM training dynamics and does not evaluate whether this mean-subtraction technique maintains performance or stability in multimodal VLA models or high-dimensional embodied action spaces.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10444)
- **👥 Authors**: Hengjie Cao, Zhendong Huang, Mengyi Chen, Yifeng Yang, Fanqi Yu, Ruijun Huang, Fang Dong, Xin Zhang, Jixian Zhou, Anrui Chen, Mingzhi Dong, Yujiang Wang, Jinlong Hou, Qin Lv, Yuan Cheng, Tun Lu, Fan Yang, Li Shang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Meta-Reinforcement Learning with Self-Reflection for Agentic Search (Score: 5/10)
- **💡 Innovation**: The paper introduces a meta-reinforcement learning framework that utilizes explicit self-reflection generated across episodes as in-context memory to improve exploration strategies.
- **⚠️ Limitations**: The approach is evaluated primarily on abstract search benchmarks rather than complex, high-dimensional physical robot manipulation tasks, leaving its efficacy in embodied settings unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.11327)
- **👥 Authors**: Teng Xiao, Yige Yuan, Hamish Ivison, Huaisheng Zhu, Faeze Brahman, Nathan Lambert, Pradeep Dasigi, Noah A. Smith, Hannaneh Hajishirzi
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Examining Reasoning LLMs-as-Judges in Non-Verifiable LLM Post-Training (Score: 5/10)
- **💡 Innovation**: The paper systematically investigates the impact of reasoning-based LLM-judges versus non-reasoning judges in RL-based alignment, revealing that reasoning judges inadvertently encourage the generation of adversarial outputs that deceive other evaluators.
- **⚠️ Limitations**: The study is confined to a controlled synthetic setting for text-based alignment, leaving the transferability of these findings to multi-modal or embodied policy training (e.g., VLA models) unexplored.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12246)
- **👥 Authors**: Yixin Liu, Yue Yu, DiJia Su, Sid Wang, Xuewei Wang, Song Jiang, Bo Liu, Arman Cohan, Yuandong Tian, Zhengxing Chen
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Geometric Autoencoder for Diffusion Models (Score: 5/10)
- **💡 Innovation**: The paper introduces a principled framework for latent space design in diffusion models by aligning the autoencoder's latent manifold with Vision Foundation Model priors through dynamic noise sampling and latent normalization.
- **⚠️ Limitations**: The work focuses exclusively on static image generation benchmarks (ImageNet) and lacks evaluation on embodied tasks, temporal consistency, or action-conditioned generation relevant to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10365)
- **👥 Authors**: Hangyu Liu, Jianyong Wang, Yutao Sun
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### ✨ Training Language Models via Neural Cellular Automata (Score: 5/10)
- **💡 Innovation**: The paper introduces a novel pre-pre-training paradigm that utilizes synthetic, spatiotemporal data generated by Neural Cellular Automata (NCA) to improve the efficiency and reasoning capabilities of LLMs.
- **⚠️ Limitations**: The study lacks a clear theoretical explanation for why NCA-generated synthetic data specifically improves reasoning benchmarks, and it does not explore the scalability of this approach beyond relatively small token counts.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10055)
- **👥 Authors**: Dan Lee, Seungwook Han, Akarsh Kumar, Pulkit Agrawal
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Multi-Task Reinforcement Learning for Enhanced Multimodal LLM-as-a-Judge (Score: 5/10)
- **💡 Innovation**: The paper introduces a multi-task reinforcement learning framework to optimize MLLMs as evaluators, aiming to improve their consistency and generalization across diverse judgment tasks.
- **⚠️ Limitations**: The paper lacks a direct application to embodied agents or robotic manipulation tasks, focusing primarily on general visual-language evaluation rather than action-conditioned feedback.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.11665)
- **👥 Authors**: Junjie Wu, Xuan Kan, Zihao He, Shunwen Tan, Bo Pan, Kaitai Zhang
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 DreamVideo-Omni: Omni-Motion Controlled Multi-Subject Video Customization with Latent Identity Reinforcement Learning (Score: 4/10)
- **💡 Innovation**: The paper introduces a two-stage training paradigm that combines hierarchical motion injection with a latent identity reward model to improve multi-subject consistency and motion control in video diffusion.
- **⚠️ Limitations**: The work focuses exclusively on video synthesis and lacks any integration with physical agents, robot control, or embodied interaction, making it tangential to robotics research.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12257)
- **👥 Authors**: Yujie Wei, Xinyu Liu, Shiwei Zhang, Hangjie Yuan, Jinbo Xing, Zhekai Chen, Xiang Wang, Haonan Qiu, Rui Zhao, Yutong Feng, Ruihang Chu, Yingya Zhang, Yike Guo, Xihui Liu, Hongming Shan
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #Reinforcement_Learning

---

### 📄 Trust Your Critic: Robust Reward Modeling and Reinforcement Learning for Faithful Image Editing and Generation (Score: 4/10)
- **💡 Innovation**: The paper introduces a 'Base-and-Bonus' reward strategy (CME and QMA) to mitigate reward model hallucinations in diffusion-based image generation and editing tasks.
- **⚠️ Limitations**: The work is strictly focused on 2D image generation and editing, lacking any connection to embodied agents, temporal consistency in video, or physical world interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12247)
- **👥 Authors**: Xiangyu Zhao, Peiyuan Zhang, Junming Lin, Tianhao Liang, Yuchen Duan, Shengyuan Ding, Changyao Tian, Yuhang Zang, Junchi Yan, Xue Yang
- **🏷️ Tags**: #Reinforcement_Learning #Diffusion_Model #Foundation_Model #LLM

---

### 📄 Understanding by Reconstruction: Reversing the Software Development Process for LLM Pretraining (Score: 4/10)
- **💡 Innovation**: The paper introduces a framework that reverse-engineers static code repositories into synthetic, agentic trajectories (planning, debugging, and refinement) to provide richer supervision for LLM pre-training.
- **⚠️ Limitations**: The approach is strictly confined to software engineering and code generation, lacking any grounding in physical environments or multi-modal sensorimotor data required for embodied tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.11103)
- **👥 Authors**: Zhiyuan Zeng, Yichi Zhang, Yong Shan, Kai Hua, Siyuan Fang, Zhaiyu Liu, Jiaheng Liu, Haozhe Wang, Yining Zheng, Ming Ding, Ke Shen, Ge Zhang, Wenhao Huang, Xipeng Qiu
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Coarse-Guided Visual Generation via Weighted h-Transform Sampling (Score: 4/10)
- **💡 Innovation**: The paper introduces a training-free guidance method for diffusion models using h-transform drift functions and a noise-level-aware schedule to steer generation from coarse references without requiring explicit forward operator knowledge.
- **⚠️ Limitations**: The method is evaluated on general image and video generation tasks rather than embodied or robotic control scenarios, making its direct utility for real-time robot manipulation or policy learning unclear.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.12057)
- **👥 Authors**: Yanghao Wang, Ziqi Jiang, Zhen Wang, Long Chen
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 NerVE: Nonlinear Eigenspectrum Dynamics in LLM Feed-Forward Networks (Score: 4/10)
- **💡 Innovation**: The paper introduces a unified eigenspectral framework (NerVE) to quantify and analyze the information flow and latent space dynamics within the feed-forward networks of large language models.
- **⚠️ Limitations**: The study is strictly confined to static language modeling tasks and lacks any empirical validation or discussion regarding how these spectral dynamics translate to embodied agents or vision-language-action (VLA) models.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.06922)
- **👥 Authors**: Nandan Kumar Jha, Brandon Reagen
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 WaDi: Weight Direction-aware Distillation for One-step Image Synthesis (Score: 4/10)
- **💡 Innovation**: The paper introduces LoRaD, a parameter-efficient adapter that models weight direction changes via low-rank rotation matrices to accelerate diffusion model distillation into one-step generators.
- **⚠️ Limitations**: The work focuses exclusively on image synthesis and lacks evaluation or discussion regarding its applicability to embodied tasks, such as policy distillation or world model training in robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08258)
- **👥 Authors**: Lei Wang, Yang Cheng, Senmao Li, Ge Wu, Yaxing Wang, Jian Yang
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model

---

### 📄 WeEdit: A Dataset, Benchmark and Glyph-Guided Framework for Text-centric Image Editing (Score: 3/10)
- **💡 Innovation**: The paper introduces a specialized HTML-based data generation pipeline and a two-stage training strategy (glyph-guided SFT and multi-objective RL) to improve text-centric image editing.
- **⚠️ Limitations**: The work is strictly focused on 2D image generation and lacks any connection to physical embodiment, spatial reasoning in 3D, or robotic control tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.11593)
- **👥 Authors**: Hui Zhang, Juntao Liu, Zongkai Liu, Liqiang Niu, Fandong Meng, Zuxuan Wu, Yu-Gang Jiang
- **🏷️ Tags**: #Diffusion_Model #Reinforcement_Learning #Foundation_Model

---

### 📄 CREATE: Testing LLMs for Associative Creativity (Score: 3/10)
- **💡 Innovation**: The paper introduces a benchmark (CREATE) to quantify associative creativity in LLMs by measuring the specificity and diversity of conceptual paths generated between disparate ideas.
- **⚠️ Limitations**: The work is strictly confined to linguistic associative reasoning and lacks any grounding in physical environments, sensorimotor feedback, or embodied task execution.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09970)
- **👥 Authors**: Manya Wadhwa, Tiasa Singha Roy, Harvey Lederman, Junyi Jessy Li, Greg Durrett
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 SoundWeaver: Semantic Warm-Starting for Text-to-Audio Diffusion Serving (Score: 2/10)
- **💡 Innovation**: The paper introduces a semantic warm-starting mechanism for text-to-audio diffusion models that uses cached audio samples to skip initial diffusion steps, thereby reducing inference latency.
- **⚠️ Limitations**: The work is entirely focused on audio generation and lacks any connection to embodied agents, robot control, or multimodal action-conditioned generation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.07865)
- **👥 Authors**: Ayush Barik, Sofia Stoica, Nikhil Sarda, Arnav Kethana, Abhinav Khanduja, Muchen Xu, Fan Lai
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 FireRedASR2S: A State-of-the-Art Industrial-Grade All-in-One Automatic Speech Recognition System (Score: 1/10)
- **💡 Innovation**: The paper introduces an integrated, industrial-grade pipeline for speech processing (ASR, VAD, LID, and Punctuation) optimized for Mandarin and English.
- **⚠️ Limitations**: The work is entirely focused on speech signal processing and lacks any connection to visual perception, motor control, or embodied interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.10420)
- **👥 Authors**: Kaituo Xu, Yan Jia, Kai Huang, Junjie Chen, Wenpeng Li, Kun Liu, Feng-Long Xie, Xu Tang, Yao Hu
- **🏷️ Tags**: #LLM #Foundation_Model

---


