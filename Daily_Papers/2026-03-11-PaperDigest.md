# 📅 2026-03-11 - Paper Digest
## Summary
Total Papers: 34 | High Impact: 4

## 📝 Papers List
### ✨ DynVLA: Learning World Dynamics for Action Reasoning in Autonomous Driving (Score: 7/10)
- **💡 Innovation**: The paper introduces 'Dynamics CoT', a paradigm that forces a VLA to predict compact, decoupled ego-centric and environment-centric dynamics tokens as a reasoning step prior to action generation.
- **⚠️ Limitations**: The reliance on a learned 'Dynamics Tokenizer' may introduce latent space biases or information loss that could hinder performance in highly complex, long-horizon, or out-of-distribution driving scenarios.
- **🔗 Link**: [[DynVLA]]
- **👥 Authors**: Shuyao Shang, Bing Zhan, Yunfei Yan, Yuqi Wang, Yingyan Li, Yasong An, Xiaoman Wang, Jierui Liu, Lu Hou, Lue Fan, Zhaoxiang Zhang, Tieniu Tan
- **🏷️ Tags**: #VLA #World_Model #Embodied_AI #Foundation_Model #LLM

---

### ✨ PPGuide: Steering Diffusion Policies with Performance Predictive Guidance (Score: 7/10)
- **💡 Innovation**: The paper introduces a lightweight, classifier-based guidance framework that uses self-supervised attention-based multiple instance learning to steer pre-trained diffusion policies away from failure modes at inference time.
- **⚠️ Limitations**: The reliance on self-labeled rollout data may introduce bias if the initial policy's failure modes are not sufficiently explored or if the performance predictor fails to generalize to novel out-of-distribution states.
- **🔗 Link**: [[PPGuide]]
- **👥 Authors**: Zixing Wang, Devesh K. Jha, Ahmed H. Qureshi, Diego Romeres
- **🏷️ Tags**: #Robot_Manipulation #Diffusion_Model #Embodied_AI

---

### ✨ Contact Coverage-Guided Exploration for General-Purpose Dexterous Manipulation (Score: 7/10)
- **💡 Innovation**: The paper introduces a contact-centric exploration objective that uses learned hash codes to track and incentivize diverse finger-object contact patterns, effectively addressing the sparse reward problem in dexterous manipulation.
- **⚠️ Limitations**: The reliance on predefined hand keypoints and object surface points may limit generalization to novel objects or hand morphologies that lack pre-computed geometric priors.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10971v1)
- **👥 Authors**: Zixuan Liu, Ruoyi Qiao, Chenrui Tie, Xuanwei Liu, Yunfan Lou, Chongkai Gao, Zhixuan Xu, Lin Shao
- **🏷️ Tags**: #Robot_Manipulation #Reinforcement_Learning #Embodied_AI #Sim2Real

---

### ✨ Reward Prediction with Factorized World States (Score: 7/10)
- **💡 Innovation**: StateFactory introduces a hierarchical, factorized object-attribute representation derived from LLMs to enable zero-shot reward prediction based on semantic similarity between current and goal states.
- **⚠️ Limitations**: The reliance on LLMs for parsing unstructured observations into structured states may introduce latency and error propagation issues in high-frequency, real-time robotic control loops.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09400)
- **👥 Authors**: Yijun Shen, Delong Chen, Xianming Hu, Jiaming Mi, Hongbo Zhao, Kai Zhang, Pascale Fung
- **🏷️ Tags**: #World_Model #Embodied_AI #LLM #Reinforcement_Learning

---

### ✨ Leech Lattice Vector Quantization for Efficient LLM Compression (Score: 6/10)
- **💡 Innovation**: The paper introduces Leech Lattice Vector Quantization (LLVQ), which leverages the optimal sphere-packing properties of the 24-dimensional Leech lattice to compress LLM weights without requiring explicit codebook storage.
- **⚠️ Limitations**: The method is currently focused on static weight compression for LLMs and does not address the specific latency or memory constraints required for real-time inference in resource-constrained embodied agents.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.11021v1)
- **👥 Authors**: Tycho F. A. van der Ouderaa, Mart van Baalen, Paul Whatmough, Markus Nagel
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Pointy - A Lightweight Transformer for Point Cloud Foundation Models (Score: 6/10)
- **💡 Innovation**: The paper introduces a lightweight, tokenizer-free transformer architecture for point clouds that achieves competitive performance with significantly less training data and compute than current large-scale foundation models.
- **⚠️ Limitations**: The study focuses primarily on static point cloud representation learning and lacks evaluation on downstream embodied tasks or dynamic scene understanding relevant to robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10963v1)
- **👥 Authors**: Konrad Szafer, Marek Kraft, Dominik Belter
- **🏷️ Tags**: #Foundation_Model #Embodied_AI

---

### ✨ MM-Zero: Self-Evolving Multi-Model Vision Language Models From Zero Data (Score: 6/10)
- **💡 Innovation**: The paper introduces a multi-role self-evolving framework (Proposer, Coder, Solver) that enables VLMs to bootstrap multimodal reasoning from zero seed data by using code-based visual generation as a proxy for real-world images.
- **⚠️ Limitations**: The reliance on synthetic, code-generated visual content may limit the model's ability to generalize to complex, high-entropy real-world visual environments compared to models trained on diverse, natural image-text datasets.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09206)
- **👥 Authors**: Zongxia Li, Hongyang Du, Chengsong Huang, Xiyang Wu, Lantao Yu, Yicheng He, Jing Xie, Xiaomin Wu, Zhichao Liu, Jiarui Zhang, Fuxiao Liu
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Streaming Autoregressive Video Generation via Diagonal Distillation (Score: 6/10)
- **💡 Innovation**: The paper introduces 'Diagonal Distillation,' an asymmetric generation strategy that optimizes video synthesis by allocating more denoising steps to early chunks and fewer to later ones, while aligning noise prediction to mitigate error accumulation.
- **⚠️ Limitations**: The evaluation focuses primarily on general video synthesis benchmarks rather than demonstrating the utility of these high-speed video generations for downstream embodied tasks like policy rollouts or world model planning.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09488)
- **👥 Authors**: Jinxiu Liu, Xuanming Liu, Kangfu Mei, Yandong Wen, Ming-HsuanYang, Weiyang Liu
- **🏷️ Tags**: #Diffusion_Model #World_Model #Foundation_Model

---

### ✨ Beyond Test-Time Training: Learning to Reason via Hardware-Efficient Optimal Control (Score: 6/10)
- **💡 Innovation**: The paper introduces a Test-Time Control (TTC) layer that embeds a hardware-efficient, symplectic LQR solver directly into LLM architectures to enable latent-space optimal control as a reasoning mechanism.
- **⚠️ Limitations**: The current evaluation is restricted to mathematical reasoning benchmarks (MATH-500, AMC, AIME) rather than embodied tasks, leaving the efficacy of this control-based reasoning for physical robot manipulation unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09221)
- **👥 Authors**: Peihao Wang, Shan Yang, Xijun Wang, Tesi Xiao, Xin Liu, Changlong Yu, Yu Lou, Pan Li, Zhangyang Wang, Ming Lin, René Vidal
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Learning Adaptive Force Control for Contact-Rich Sample Scraping with Heterogeneous Materials (Score: 5/10)
- **💡 Innovation**: The paper introduces a procedural simulation framework using Perlin noise to model heterogeneous material dislodgement forces, enabling an RL agent to learn adaptive contact wrenches for scraping tasks.
- **⚠️ Limitations**: The approach relies on a simplified particle-based simulation that may not fully capture the complex rheological properties (e.g., stickiness, viscosity) of real-world chemical samples.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10979v1)
- **👥 Authors**: Cenk Cetin, Shreyas Pouli, Gabriella Pizzuto
- **🏷️ Tags**: #Robot_Manipulation #Reinforcement_Learning #Sim2Real #Embodied_AI

---

### ✨ Safe RLHF Beyond Expectation: Stochastic Dominance for Universal Spectral Risk Control (Score: 5/10)
- **💡 Innovation**: The paper introduces Risk-sensitive Alignment via Dominance (RAD), which replaces standard expected cost constraints in RLHF with First-Order Stochastic Dominance (FSD) constraints using Optimal Transport to control tail risks.
- **⚠️ Limitations**: The framework is evaluated primarily on language model alignment tasks rather than embodied or robotic control scenarios, leaving its efficacy in high-dimensional, continuous-action robotic environments unproven.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10938v1)
- **👥 Authors**: Yaswanth Chittepu, Ativ Joshi, Rajarshi Bhattacharjee, Scott Niekum
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Ergodicity in reinforcement learning (Score: 5/10)
- **💡 Innovation**: The paper identifies a fundamental discrepancy between ensemble-average optimization and single-trajectory performance in non-ergodic reinforcement learning environments.
- **⚠️ Limitations**: The work is primarily theoretical and conceptual, lacking empirical validation or specific algorithmic contributions for high-dimensional robotic control tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10895v1)
- **👥 Authors**: Dominik Baumann, Erfaun Noorani, Arsenii Mustafin, Xinyi Sheng, Bert Verbruggen, Arne Vanhoyweghen, Vincent Ginis, Thomas B. Schön
- **🏷️ Tags**: #Reinforcement_Learning

---

### ✨ S2D: Sparse to Dense Lifting for 3D Reconstruction with Minimal Inputs (Score: 5/10)
- **💡 Innovation**: The paper introduces a two-fold pipeline that combines a one-step diffusion model for image artifact correction with a robust 3DGS fitting strategy to enable high-fidelity 3D reconstruction from extremely sparse input views.
- **⚠️ Limitations**: The paper lacks evaluation on dynamic scenes or real-world robotic manipulation tasks, focusing primarily on static scene reconstruction rather than embodied interaction.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10893v1)
- **👥 Authors**: Yuzhou Ji, Qijian Tian, He Zhu, Xiaoqi Jiang, Guangzhi Cao, Lizhuang Ma, Yuan Xie, Xin Tan
- **🏷️ Tags**: #3D_Gaussian_Splatting #Diffusion_Model

---

### ✨ Dynamics-Predictive Sampling for Active RL Finetuning of Large Reasoning Models (Score: 5/10)
- **💡 Innovation**: The paper introduces Dynamics-Predictive Sampling (DPS), which uses Bayesian inference on a hidden Markov model to predict prompt learning dynamics, thereby avoiding costly LLM rollouts during RL finetuning.
- **⚠️ Limitations**: The approach is primarily validated on text-based reasoning tasks (math, planning) and lacks evidence of its efficacy or scalability in high-dimensional, continuous-action spaces typical of Embodied AI or robot manipulation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10887v1)
- **👥 Authors**: Yixiu Mao, Yun Qu, Qi Wang, Heming Zou, Xiangyang Ji
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Geometry-Guided Reinforcement Learning for Multi-view Consistent 3D Scene Editing (Score: 5/10)
- **💡 Innovation**: The paper introduces a reinforcement learning framework that uses 3D foundation model priors (VGGT) as reward signals to enforce multi-view consistency in 2D diffusion-based 3D editing without requiring paired training data.
- **⚠️ Limitations**: The reliance on a specific 3D foundation model (VGGT) for reward signals may limit the framework's generalizability to scenes or objects outside the model's training distribution.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03143)
- **👥 Authors**: Jiyuan Wang, Chunyu Lin, Lei Sun, Zhi Cao, Yuyang Yin, Lang Nie, Zhenlong Yuan, Xiangxiang Chu, Yunchao Wei, Kang Liao, Guosheng Lin
- **🏷️ Tags**: #Reinforcement_Learning #Diffusion_Model #Foundation_Model

---

### ✨ Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion (Score: 5/10)
- **💡 Innovation**: The paper proposes a unified any-to-any multimodal architecture that replaces the standard autoregressive backbone of MLLMs with a mask-based discrete diffusion model.
- **⚠️ Limitations**: The paper focuses on general multimodal understanding and generation (text, speech, images) without demonstrating applicability to embodied control or action-space prediction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.06577)
- **👥 Authors**: Lijiang Li, Zuwei Long, Yunhang Shen, Heting Gao, Haoyu Cao, Xing Sun, Caifeng Shan, Ran He, Chaoyou Fu
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #LLM

---

### ✨ Reading, Not Thinking: Understanding and Bridging the Modality Gap When Text Becomes Pixels in Multimodal LLMs (Score: 5/10)
- **💡 Innovation**: The paper systematically quantifies the 'modality gap' in MLLMs when processing visual text and introduces a self-distillation technique to align visual reasoning with pure text-based reasoning traces.
- **⚠️ Limitations**: The study focuses exclusively on static document/textual reasoning and does not address the temporal or spatial complexities required for embodied agents or real-time robotic perception.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09095)
- **👥 Authors**: Kaiser Sun, Xiaochuang Yuan, Hongjun Liu, Chen Zhao, Cheng Zhang, Mark Dredze, Fan Bai
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ Decoupling Reasoning and Confidence: Resurrecting Calibration in Reinforcement Learning from Verifiable Rewards (Score: 5/10)
- **💡 Innovation**: The paper identifies a fundamental gradient conflict between accuracy optimization and calibration in RLVR and proposes a decoupling framework (DCPO) to mitigate over-confidence.
- **⚠️ Limitations**: The study is strictly focused on text-based reasoning tasks and lacks evaluation on embodied agents or multi-modal decision-making scenarios where calibration is equally critical.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09117)
- **👥 Authors**: Zhengzhao Ma, Xueru Wen, Boxi Cao, Yaojie Lu, Hongyu Lin, Jinglin Yang, Min He, Xianpei Han, Le Sun
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ ReflexiCoder: Teaching Large Language Models to Self-Reflect on Generated Code and Self-Correct It via Reinforcement Learning (Score: 5/10)
- **💡 Innovation**: ReflexiCoder internalizes iterative code reflection and self-correction into model weights via an RL-zero training paradigm, eliminating the need for external execution or oracles during inference.
- **⚠️ Limitations**: The paper focuses exclusively on software code generation and lacks evaluation or discussion on how these self-reflection mechanisms translate to embodied tasks or physical environment constraints.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.05863)
- **👥 Authors**: Juyong Jiang, Jiasi Shen, Sunghun Kim, Kang Min Yoo, Jeonghoon Kim, Sungju Kim
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 Ranking Reasoning LLMs under Test-Time Scaling (Score: 4/10)
- **💡 Innovation**: The paper formalizes the evaluation of reasoning LLMs under test-time scaling by introducing a library (Scorio) that applies statistical ranking methods to multi-sample output distributions.
- **⚠️ Limitations**: The work is strictly focused on text-based reasoning benchmarks and lacks any connection to embodied agents, multi-modal action spaces, or the specific challenges of robot policy evaluation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10960v1)
- **👥 Authors**: Mohsen Hariri, Michael Hinczewski, Jing Ma, Vipin Chaudhary
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 LookaheadKV: Fast and Accurate KV Cache Eviction by Glimpsing into the Future without Generation (Score: 4/10)
- **💡 Innovation**: LookaheadKV replaces computationally expensive draft generation for KV cache eviction with lightweight, parameter-efficient modules trained to predict token importance scores directly.
- **⚠️ Limitations**: The paper focuses exclusively on text-based long-context LLM inference and does not address the specific memory or latency constraints of real-time embodied agents or VLA models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10899v1)
- **👥 Authors**: Jinwoo Ahn, Ingyu Seong, Akhil Kedia, Junhan Kim, Hyemi Jang, Kangwook Lee, Yongkweon Jeon
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs (Score: 4/10)
- **💡 Innovation**: The paper identifies that reasoning tokens in LLMs act as a computational buffer and a semantic bridge for factual recall, even for tasks that do not logically require multi-step reasoning.
- **⚠️ Limitations**: The study is strictly limited to text-based factual recall and does not explore how these reasoning-induced knowledge retrieval mechanisms translate to embodied or multimodal contexts.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09906)
- **👥 Authors**: Zorik Gekhman, Roee Aharoni, Eran Ofek, Mor Geva, Roi Reichart, Jonathan Herzig
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 InternVL-U: Democratizing Unified Multimodal Models for Understanding, Reasoning, Generation and Editing (Score: 4/10)
- **💡 Innovation**: The paper introduces a lightweight 4B-parameter unified multimodal model that integrates understanding and generation by decoupling visual representations and employing a reasoning-centric data synthesis pipeline.
- **⚠️ Limitations**: The work focuses exclusively on image generation and multimodal understanding, lacking any integration with action spaces or embodied control, making it currently irrelevant for robotics applications.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09877)
- **👥 Authors**: Changyao Tian, Danni Yang, Guanzhou Chen, Erfei Cui, Zhaokai Wang, Yuchen Duan, Penghao Yin, Sitao Chen, Ganlin Yang, Mingxin Liu, Zirun Zhu, Ziqian Fan, Leyao Gu, Haomin Wang, Qi Wei, Jinhui Yin, Xue Yang, Zhihang Zhong, Qi Qin, Yi Xin, Bin Fu, Yihao Liu, Jiaye Ge, Qipeng Guo, Gen Luo, Hongsheng Li, Yu Qiao, Kai Chen, Hongjie Zhang
- **🏷️ Tags**: #Foundation_Model #LLM #Diffusion_Model

---

### 📄 Do What I Say: A Spoken Prompt Dataset for Instruction-Following (Score: 4/10)
- **💡 Innovation**: The paper introduces a multilingual, multi-style dataset (DOWIS) specifically designed to evaluate Speech Large Language Models (SLLMs) using spoken rather than text-based prompts.
- **⚠️ Limitations**: The work focuses exclusively on speech-to-text/speech-to-speech instruction following and lacks integration with embodied agents or physical robot manipulation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09881)
- **👥 Authors**: Maike Züfle, Sara Papi, Fabian Retkowski, Szymon Mazurek, Marek Kasztelnik, Alexander Waibel, Luisa Bentivogli, Jan Niehues
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Test-Driven AI Agent Definition (TDAD): Compiling Tool-Using Agents from Behavioral Specifications (Score: 4/10)
- **💡 Innovation**: The paper introduces a test-driven development framework for LLM agents that uses automated test generation and mutation testing to ensure behavioral compliance and regression safety.
- **⚠️ Limitations**: The methodology is focused on software-based tool-using agents and lacks integration with physical embodiment, sensorimotor feedback, or the specific challenges of real-world robot manipulation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08806)
- **👥 Authors**: Tzafrir Rehan
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Towards a Neural Debugger for Python (Score: 4/10)
- **💡 Innovation**: The paper introduces a 'neural debugger' framework that enables LLMs to perform interactive, state-conditioned execution prediction (stepping, breakpoints) rather than just linear trace generation.
- **⚠️ Limitations**: The work is strictly confined to symbolic code execution and lacks integration with physical environments or multi-modal sensory feedback, limiting its direct applicability to embodied robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09951)
- **👥 Authors**: Maximilian Beck, Jonas Gehring, Jannik Kossen, Gabriel Synnaeve
- **🏷️ Tags**: #LLM #Foundation_Model #World_Model

---

### 📄 ConFu: Contemplate the Future for Better Speculative Sampling (Score: 4/10)
- **💡 Innovation**: ConFu introduces 'contemplate tokens' and a dynamic MoE-based mechanism to allow draft models in speculative decoding to anticipate future target model states, reducing error accumulation.
- **⚠️ Limitations**: The paper focuses exclusively on text-based LLM inference acceleration and lacks any application or evaluation within embodied, multimodal, or real-time robotic control contexts.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.08899)
- **👥 Authors**: Zongyue Qin, Raghavv Goel, Mukul Gagrani, Risheek Garrepalli, Mingu Lee, Yizhou Sun
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 MiniAppBench: Evaluating the Shift from Text to Interactive HTML Responses in LLM-Powered Assistants (Score: 3/10)
- **💡 Innovation**: The paper introduces a benchmark and agentic evaluation framework for assessing the generation of interactive HTML-based applications (MiniApps) by LLMs.
- **⚠️ Limitations**: The work is entirely focused on web-based software agents and lacks any connection to physical embodiment, sensorimotor control, or real-world robotic interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09652)
- **👥 Authors**: Zuhao Zhang, Chengyue Yu, Yuante Li, Chenyi Zhuang, Linjian Mo, Shuai Li
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 The Reasoning Trap -- Logical Reasoning as a Mechanistic Pathway to Situational Awareness (Score: 3/10)
- **💡 Innovation**: The paper proposes the RAISE framework, which theoretically maps improvements in LLM logical reasoning to the emergence of situational awareness and strategic deception capabilities.
- **⚠️ Limitations**: The work is purely speculative and theoretical, lacking empirical evidence or experimental validation regarding how logical reasoning mechanisms specifically translate to situational awareness in current architectures.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.09200)
- **👥 Authors**: Subramanyam Sahoo, Aman Chadha, Vinija Jain, Divya Chaudhary
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 COMIC: Agentic Sketch Comedy Generation (Score: 2/10)
- **💡 Innovation**: The paper introduces a multi-agent framework that utilizes LLM-based critics aligned with human humor preferences to automate the creative pipeline of sketch comedy generation.
- **⚠️ Limitations**: The work focuses entirely on generative media and lacks any connection to physical embodiment, sensorimotor control, or real-world interaction, making it irrelevant to robotics research.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.11048v1)
- **👥 Authors**: Susung Hong, Brian Curless, Ira Kemelmacher-Shlizerman, Steve Seitz
- **🏷️ Tags**: #LLM #Foundation_Model #Diffusion_Model

---

### 📄 TOSSS: a CVE-based Software Security Benchmark for Large Language Models (Score: 2/10)
- **💡 Innovation**: The paper introduces a benchmark (TOSSS) that leverages the CVE database to evaluate the ability of LLMs to distinguish between secure and vulnerable code snippets.
- **⚠️ Limitations**: The work is entirely focused on software security and code analysis, lacking any connection to physical agents, sensorimotor control, or embodied intelligence.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10969v1)
- **👥 Authors**: Marc Damie, Murat Bilgehan Ertan, Domenico Essoussi, Angela Makhanu, Gaëtan Peter, Roos Wensveen
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Med-DualLoRA: Local Adaptation of Foundation Models for 3D Cardiac MRI (Score: 2/10)
- **💡 Innovation**: The paper introduces Med-DualLoRA, a federated learning framework that uses additive decomposition to disentangle globally shared and locally private LoRA adapters for medical foundation models.
- **⚠️ Limitations**: The methodology is strictly confined to medical imaging classification and lacks any connection to embodied agents, physical interaction, or temporal dynamics relevant to robotics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10967v1)
- **👥 Authors**: Joan Perramon-Llussà, Amelia Jiménez-Sánchez, Grzegorz Skorupko, Fotis Avgoustidis, Carlos Martín-Isla, Karim Lekadir, Polyxeni Gkontra
- **🏷️ Tags**: #Foundation_Model

---

### 📄 When Fine-Tuning Fails and when it Generalises: Role of Data Diversity and Mixed Training in LLM-based TTS (Score: 2/10)
- **💡 Innovation**: The paper demonstrates that LoRA fine-tuning of a compact LLM backbone (Qwen-0.5B) significantly enhances speaker fidelity and acoustic quality in TTS systems when provided with diverse training data.
- **⚠️ Limitations**: The research is entirely focused on audio synthesis and lacks any connection to spatial reasoning, physical interaction, or multi-modal action generation required for embodied agents.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10904v1)
- **👥 Authors**: Anupam Purwar, Aditya Choudhary
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 A Hybrid Knowledge-Grounded Framework for Safety and Traceability in Prescription Verification (Score: 2/10)
- **💡 Innovation**: The paper introduces a hybrid knowledge-grounded framework (PharmGraph-Auditor) that combines Virtual Knowledge Graphs with a Chain of Verification paradigm to improve the reliability of LLMs in pharmaceutical auditing.
- **⚠️ Limitations**: The work is entirely focused on natural language processing and symbolic reasoning for healthcare compliance, lacking any connection to physical agents, sensorimotor control, or embodied decision-making.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2603.10891v1)
- **👥 Authors**: Yichi Zhu, Kan Ling, Xu Liu, Hengrun Zhang, Huiqun Yu, Guisheng Fan
- **🏷️ Tags**: #LLM #Foundation_Model

---


