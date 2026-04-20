# 📅 2026-04-17 - Paper Digest
## Summary
Total Papers: 37 | High Impact: 7

## 📝 Papers List
### ✨ Semantic Area Graph Reasoning for Multi-Robot Language-Guided Search (Score: 7/10)
- **💡 Innovation**: Introduces a hierarchical multi-robot coordination framework that uses an incrementally constructed semantic area graph as a compact topological interface for LLM-based room assignment, decoupling high-level semantic reasoning from low-level deterministic navigation.
- **⚠️ Limitations**: Relies heavily on pre-existing semantic occupancy mapping pipelines and restricts LLM reasoning to discrete room-level assignments, limiting adaptability to dynamic obstacles or fine-grained object-level tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16263v1)
- **👥 Authors**: Ruiyang Wang, Hao-Lun Hsu, Jiwoo Kim, Miroslav Pajic
- **🏷️ Tags**: #Embodied_AI #LLM #Foundation_Model

---

### ✨ Detecting and Suppressing Reward Hacking with Gradient Fingerprints (Score: 7/10)
- **💡 Innovation**: GRIFT introduces a gradient-based fingerprinting technique that compresses prompt-conditioned CoT gradients into a compact representation to detect implicit reward hacking in RLVR-trained LLMs.
- **⚠️ Limitations**: The approach relies on computationally expensive gradient computations over long reasoning traces and lacks demonstrated transferability to continuous control or embodied RL settings.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16242v1)
- **👥 Authors**: Songtao Wang, Quang Hieu Pham, Fangcong Yin, Xinpeng Wang, Jocelyn Qiaochu Chen, Greg Durrett, Xi Ye
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Sketching the Readout of Large Language Models for Scalable Data Attribution and Valuation (Score: 7/10)
- **💡 Innovation**: RISE leverages the outer-product structure of LM-head gradients and applies CountSketch to dual lexical/semantic channels, enabling scalable, forward-pass-only data attribution and valuation for LLMs up to 32B parameters.
- **⚠️ Limitations**: The method's reliance on output-layer gradient concentration may degrade attribution fidelity for tasks requiring deep internal layer reasoning or multi-step chain-of-thought dynamics.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16197v1)
- **👥 Authors**: Yide Ran, Jianwen Xie, Minghui Wang, Wenjin Zheng, Denghui Zhang, Chuan Li, Zhaozhuo Xu
- **🏷️ Tags**: #LLM #Foundation_Model #Data_Attribution

---

### ✨ HY-World 2.0: A Multi-Modal World Model for Reconstructing, Generating, and Simulating 3D Worlds (Score: 7/10)
- **💡 Innovation**: Integrates a memory-augmented keyframe generation model with explicit normal supervision and a feed-forward 3D prediction architecture to enable consistent, navigable 3D Gaussian Splatting scene synthesis from diverse modalities.
- **⚠️ Limitations**: The pipeline remains heavily focused on offline scene generation and rendering rather than closed-loop policy learning or real-time robotic interaction, limiting direct applicability to manipulation or RL tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.14268)
- **👥 Authors**: Team HY-World, Chenjie Cao, Xuhui Zuo, Zhenwei Wang, Yisu Zhang, Junta Wu, Zhenyang Liu, Yuning Gong, Yang Liu, Bo Yuan, Chao Zhang, Coopers Li, Dongyuan Guo, Fan Yang, Haiyu Zhang, Hang Cao, Jianchen Zhu, Jiaxin Lin, Jie Xiao, Jihong Zhang, Junlin Yu, Lei Wang, Lifu Wang, Lilin Wang, Linus, Minghui Chen, Peng He, Penghao Zhao, Qi Chen, Rui Chen, Rui Shao, Sicong Liu, Wangchen Qin, Xiaochuan Niu, Xiang Yuan, Yi Sun, Yifei Tang, Yifu Sun, Yihang Lian, Yonghao Tan, Yuhong Liu, Yuyang Yin, Zhiyuan Min, Tengfei Wang, Chunchao Guo
- **🏷️ Tags**: #World_Model #3D_Gaussian_Splatting #Embodied_AI

---

### ✨ RAD-2: Scaling Reinforcement Learning in a Generator-Discriminator Framework (Score: 7/10)
- **💡 Innovation**: The paper decouples trajectory generation and evaluation by pairing a diffusion-based generator with an RL-optimized discriminator, stabilized via temporally consistent group relative policy optimization and on-policy longitudinal feedback.
- **⚠️ Limitations**: The framework's reliance on a custom BEV-Warp simulator and driving-specific reward structures constrains its direct transferability to general-purpose robotic manipulation or non-automotive embodied AI tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.15308)
- **👥 Authors**: Hao Gao, Shaoyu Chen, Yifan Zhu, Yuehao Song, Wenyu Liu, Qian Zhang, Xinggang Wang
- **🏷️ Tags**: #Reinforcement_Learning #Diffusion_Model #Embodied_AI #Sim2Real

---

### ✨ HiVLA: A Visual-Grounded-Centric Hierarchical Embodied Manipulation System (Score: 7/10)
- **💡 Innovation**: The framework introduces a cascaded cross-attention mechanism within a flow-matching DiT that sequentially fuses global context, high-resolution object crops, and skill semantics to bridge VLM-generated bounding boxes with precise low-level motor control.
- **⚠️ Limitations**: The explicit reliance on bounding box grounding restricts applicability to tasks requiring implicit spatial reasoning or continuous visual feedback without accurate external localization.
- **🔗 Link**: [[HiVLA]]
- **👥 Authors**: Tianshuo Yang, Guanyu Chen, Yutian Chen, Zhixuan Liang, Yitian Liu, Zanxin Chen, Chunpu Xu, Haotian Liang, Jiangmiao Pang, Yao Mu, Ping Luo
- **🏷️ Tags**: #VLA #Robot_Manipulation #Diffusion_Model #Embodied_AI

---

### ✨ Reinforcement Learning via Value Gradient Flow (Score: 7/10)
- **💡 Innovation**: Formulates behavior-regularized RL as an optimal transport problem solved via discrete value-gradient flow over particles, eliminating explicit policy parameterization and enabling implicit regularization through transport budget control.
- **⚠️ Limitations**: The particle-based gradient flow approach may face scalability bottlenecks in high-dimensional continuous action spaces or require careful tuning of the transport budget for stable convergence.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.14265)
- **👥 Authors**: Haoran Xu, Kaiwen Hu, Somayeh Sojoudi, Amy Zhang
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Diffusion_Model

---

### ✨ Repurposing 3D Generative Model for Autoregressive Layout Generation (Score: 6/10)
- **💡 Innovation**: The paper presents a well-specified 3D diffusion framework for physically plausible layout generation with strong empirical results, offering clear downstream relevance to embodied AI and world modeling despite not directly targeting manipulation or VLA architectures.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16299v1)
- **👥 Authors**: Haoran Feng, Yifan Niu, Zehuan Huang, Yang-Tian Sun, Chunchao Guo, Yuxin Peng, Lu Sheng
- **🏷️ Source**: #arXiv

---

### ✨ Learning to Reason with Insight for Informal Theorem Proving (Score: 6/10)
- **💡 Innovation**: The paper directly targets LLM reasoning with a clear dataset and training methodology, warranting a second-stage review despite its lack of robotics or embodied AI focus.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16278v1)
- **👥 Authors**: Yunhe Li, Hao Shi, Bowen Deng, Wei Wang, Mengzhe Ruan, Hanxu Hou, Zhongxiang Dai, Siyang Gao, Chao Wang, Shuang Qiu, Linqi Song
- **🏷️ Source**: #arXiv

---

### ✨ Beyond Distribution Sharpening: The Importance of Task Rewards (Score: 6/10)
- **💡 Innovation**: The paper directly investigates RL training paradigms for LLMs and foundation models with theoretical and empirical validation, making it highly relevant to the RL and LLM interests despite lacking explicit robotics experiments.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16259v1)
- **👥 Authors**: Sarthak Mittal, Leo Gagnon, Guillaume Lajoie
- **🏷️ Source**: #arXiv

---

### ✨ Find, Fix, Reason: Context Repair for Video Reasoning (Score: 6/10)
- **💡 Innovation**: The paper presents a well-specified RL-driven context repair framework for large multimodal models that directly aligns with the Reinforcement Learning and Foundation Model/LLM interests, warranting deeper evaluation despite lacking explicit robotics or embodied AI components.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16243v1)
- **👥 Authors**: Haojian Huang, Chuanyu Qin, Yinchuan Li, Yingcong Chen
- **🏷️ Source**: #arXiv

---

### ✨ Beyond Surface Statistics: Robust Conformal Prediction for LLMs via Internal Representations (Score: 6/10)
- **💡 Innovation**: The paper directly addresses LLM reliability and uncertainty quantification using a novel internal representation-based conformal prediction method, aligning well with the Foundation Model/LLM interests despite lacking robotics-specific applications.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16217v1)
- **👥 Authors**: Yanli Wang, Peng Kuang, Xiaoyu Han, Kaidi Xu, Haohan Wang
- **🏷️ Source**: #arXiv

---

### ✨ JumpLoRA: Sparse Adapters for Continual Learning in Large Language Models (Score: 6/10)
- **💡 Innovation**: Introduces a learnable JumpReLU gating mechanism to dynamically sparsify LoRA weight updates, enabling fine-grained parameter isolation for continual learning in LLMs.
- **⚠️ Limitations**: The approach relies on dense-to-sparse thresholding during training which may introduce optimization instability or require careful hyperparameter tuning for the gating thresholds across diverse task streams.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16171v1)
- **👥 Authors**: Alexandra Dragomir, Ioana Pintilie, Antonio Barbalau, Marius Dragoi, Florin Brad, Cristian Daniel Paduraru, Alexandru Tifrea, Elena Burceanu, Radu Tudor Ionescu
- **🏷️ Tags**: #LLM #Foundation_Model #Continual_Learning

---

### ✨ ASGuard: Activation-Scaling Guard to Mitigate Targeted Jailbreaking Attack (Score: 6/10)
- **💡 Innovation**: Proposes a mechanistically-guided pipeline that isolates tense-jailbreak-vulnerable attention heads via circuit analysis and applies a channel-wise activation scaling vector to enforce robust refusal through preventative fine-tuning.
- **⚠️ Limitations**: The method addresses only a specific syntactic attack vector and relies on mechanistic interpretability assumptions that may not transfer to complex semantic or multimodal adversarial prompts.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2509.25843)
- **👥 Authors**: Yein Park, Jungwoo Park, Jaewoo Kang
- **🏷️ Tags**: #LLM #Foundation_Model #AI_Safety

---

### ✨ UniDoc-RL: Coarse-to-Fine Visual RAG with Hierarchical Actions and Dense Rewards (Score: 6/10)
- **💡 Innovation**: The paper presents a well-specified RL framework for training LVLMs on visual RAG tasks, strongly aligning with the Reinforcement Learning and Foundation Model/LLM interests despite lacking robotics or embodied AI focus.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.14967)
- **👥 Authors**: Jun Wang, Shuo Tan, Zelong Sun, Tiancheng Gu, Yongle Zhao, Ziyong Feng, Kaicheng Yang, Cewu Lu
- **🏷️ Source**: #HuggingFace

---

### ✨ KV Packet: Recomputation-Free Context-Independent KV Caching for LLMs (Score: 6/10)
- **💡 Innovation**: Although it aligns with the LLM interest, the work focuses purely on inference caching optimization without any robotics, embodiment, or action-generation components, making it a weak fit for this pipeline.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.13226)
- **👥 Authors**: Chuangtao Chen, Grace Li Zhang, Xunzhao Yin, Cheng Zhuo, Bing Li, Ulf Schlichtmann
- **🏷️ Source**: #HuggingFace

---

### ✨ Boosting Visual Instruction Tuning with Self-Supervised Guidance (Score: 6/10)
- **💡 Innovation**: The paper presents a clear, empirically validated data-centric method for improving MLLM visual reasoning, aligning well with the Foundation Models and LLM interests despite lacking direct robotics applications.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.12966)
- **👥 Authors**: Sophia Sirko-Galouchenko, Monika Wysoczanska, Andrei Bursuc, Nicolas Thome, Spyros Gidaris
- **🏷️ Source**: #HuggingFace

---

### ✨ Representations Before Pixels: Semantics-Guided Hierarchical Video Prediction (Score: 6/10)
- **💡 Innovation**: The paper directly targets world modeling and diffusion-based video prediction with a clear two-stage architecture and empirical validation, making it a strong candidate for deeper review despite its autonomous driving focus.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.11707)
- **👥 Authors**: Efstathios Karypidis, Spyros Gidaris, Nikos Komodakis
- **🏷️ Source**: #HuggingFace

---

### ✨ LongAct: Harnessing Intrinsic Activation Patterns for Long-Context Reinforcement Learning (Score: 6/10)
- **💡 Innovation**: The paper directly targets RL and LLM interests with a clearly defined saliency-guided sparse update mechanism and strong benchmark results, warranting deeper review despite lacking a robotics focus.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.14922)
- **👥 Authors**: Bowen Ping, Zijun Chen, Tingfeng Hui, Qize Yu, Chenxuan Li, Junchi Yan, Baobao Chang
- **🏷️ Source**: #HuggingFace

---

### ✨ TRACER: Trace-Based Adaptive Cost-Efficient Routing for LLM Classification (Score: 6/10)
- **💡 Innovation**: The paper presents a well-specified, empirically validated LLM routing system that aligns with the LLM interest, but lacks direct applicability to robotics or embodied AI, warranting a cautious second-stage review.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.14531)
- **👥 Authors**: Adam Rida
- **🏷️ Source**: #HuggingFace

---

### ✨ Don't Retrieve, Navigate: Distilling Enterprise Knowledge into Navigable Agent Skills for QA and RAG (Score: 6/10)
- **💡 Innovation**: The paper aligns with the LLM interest by introducing a structured hierarchical navigation approach for RAG, warranting further review despite its lack of direct robotics or embodied AI components.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.14572)
- **👥 Authors**: Yiqun Sun, Pengfei Wei, Lawrence B. Hsieh
- **🏷️ Source**: #HuggingFace

---

### ✨ Cross-Tokenizer LLM Distillation through a Byte-Level Interface (Score: 6/10)
- **💡 Innovation**: The paper presents a clear, empirically validated method for LLM distillation that aligns with the LLM and Foundation Model interests, warranting further review despite its lack of robotics-specific focus.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.07466)
- **👥 Authors**: Avyav Kumar Singh, Yen-Chen Wu, Alexandru Cioba, Alberto Bernacchia, Davide Buffelli
- **🏷️ Source**: #HuggingFace

---

### ✨ Model Capability Dominates: Inference-Time Optimization Lessons from AIMO 3 (Score: 6/10)
- **💡 Innovation**: The paper provides a rigorous empirical analysis of LLM inference-time optimization and capability scaling, aligning with the explicit LLM/Foundation Model interests despite lacking robotics or embodied AI components.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.27844)
- **👥 Authors**: Natapong Nitarach
- **🏷️ Source**: #HuggingFace

---

### ✨ ASMR-Bench: Auditing for Sabotage in ML Research (Score: 5/10)
- **💡 Innovation**: The paper focuses on AI safety and code auditing benchmarks rather than the target robotics, embodied AI, or core LLM capability research, making it a poor fit for the pipeline.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16286v1)
- **👥 Authors**: Eric Gan, Aryan Bhatt, Buck Shlegeris, Julian Stastny, Vivek Hebbar
- **🏷️ Source**: #arXiv

---

### ✨ Evaluating the Progression of Large Language Model Capabilities for Small-Molecule Drug Design (Score: 5/10)
- **💡 Innovation**: The paper focuses exclusively on computational chemistry and drug discovery, making it clearly off-topic for a robotics and embodied AI pipeline despite its use of LLMs and RL.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16279v1)
- **👥 Authors**: Shriram Chennakesavalu, Kirill Shmilovich, Hayley Weir, Colin Grambow, John Bradshaw, Patricia Suriana, Chen Cheng, Kangway Chuang
- **🏷️ Source**: #arXiv

---

### ✨ From Benchmarking to Reasoning: A Dual-Aspect, Large-Scale Evaluation of LLMs on Vietnamese Legal Text (Score: 5/10)
- **💡 Innovation**: Although it aligns with the LLM interest, the paper focuses exclusively on Vietnamese legal text evaluation and lacks any connection to robotics, embodied AI, or foundational model methodology, making it off-topic for this pipeline.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16270v1)
- **👥 Authors**: Van-Truong Le
- **🏷️ Source**: #arXiv

---

### ✨ neuralCAD-Edit: An Expert Benchmark for Multimodal-Instructed 3D CAD Model Editing (Score: 5/10)
- **💡 Innovation**: The paper is a CAD editing benchmark rather than a robotics or embodied AI method, offering limited direct relevance to the target pipeline despite evaluating foundation models.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16170v1)
- **👥 Authors**: Toby Perrett, Matthew Bouchard, William McCarthy
- **🏷️ Source**: #arXiv

---

### ✨ AtManRL: Towards Faithful Reasoning via Differentiable Attention Saliency (Score: 5/10)
- **💡 Innovation**: The paper introduces a differentiable attention mask optimized via reinforcement learning to derive a saliency reward that enforces chain-of-thought faithfulness in LLMs.
- **⚠️ Limitations**: The approach is evaluated only on standard NLP benchmarks with a small 3B model, lacking validation in embodied or robotic reasoning contexts where causal faithfulness is critical.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16158v1)
- **👥 Authors**: Max Henning Höth, Kristian Kersting, Björn Deiseroth, Letitia Parcalabescu
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ Motion-Adapter: A Diffusion Model Adapter for Text-to-Motion Generation of Compound Actions (Score: 5/10)
- **💡 Innovation**: The paper focuses on human motion synthesis for animation rather than robotic control or embodied AI, making it a poor fit for the specified robotics/AI pipeline despite its diffusion model contribution.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16135v1)
- **👥 Authors**: Yue Jiang, Mingyu Yang, Liuyuxin Yang, Yang Xu, Bingxin Yun, Yuhe Zhang
- **🏷️ Source**: #arXiv

---

### ✨ Tabular foundation models for in-context prediction of molecular properties (Score: 5/10)
- **💡 Innovation**: The paper focuses on molecular property prediction for drug discovery using tabular foundation models, which is entirely outside the target robotics, embodied AI, and control-related interests.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16123v1)
- **👥 Authors**: Karim K. Ben Hicham, Jan G. Rittig, Martin Grohe, Alexander Mitsos
- **🏷️ Source**: #arXiv

---

### ✨ SuperLocalMemory V3.3: The Living Brain -- Biologically-Inspired Forgetting, Cognitive Quantization, and Multi-Channel Retrieval for Zero-LLM Agent Memory Systems (Score: 5/10)
- **💡 Innovation**: The paper focuses on local memory architectures for AI coding agents rather than robotics, embodied AI, or the specified target interests, making it off-topic for this pipeline.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.04514)
- **👥 Authors**: Varun Pratap Bhardwaj
- **🏷️ Source**: #HuggingFace

---

### ✨ Towards Autonomous Mechanistic Reasoning in Virtual Cells (Score: 5/10)
- **💡 Innovation**: The paper focuses exclusively on computational biology and virtual cells using LLMs, making it clearly off-topic for the target robotics and embodied AI interests.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2604.11661)
- **👥 Authors**: Yunhui Jang, Lu Zhu, Jake Fawkes, Alisandra Kaye Denton, Dominique Beaini, Emmanuel Noutahi
- **🏷️ Source**: #HuggingFace

---

### 📄 Using Large Language Models and Knowledge Graphs to Improve the Interpretability of Machine Learning Models in Manufacturing (Score: 4/10)
- **💡 Innovation**: The paper focuses on explainable AI for manufacturing using LLMs and knowledge graphs, lacking any connection to robotics, embodied AI, or the specified target research areas.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16280v1)
- **👥 Authors**: Thomas Bayer, Alexander Lohr, Sarah Weiß, Bernd Michelberger, Wolfram Höpken
- **🏷️ Source**: #arXiv

---

### 📄 Characterising LLM-Generated Competency Questions: a Cross-Domain Empirical Study using Open and Closed Models (Score: 4/10)
- **💡 Innovation**: The paper focuses on ontology engineering and evaluating LLM-generated competency questions, lacking any connection to robotics, embodied AI, or the core AI methodologies of interest.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16258v1)
- **👥 Authors**: Reham Alharbi, Valentina Tamma, Terry R. Payne, Jacopo de Berardinis
- **🏷️ Source**: #arXiv

---

### 📄 ChemGraph-XANES: An Agentic Framework for XANES Simulation and Analysis (Score: 4/10)
- **💡 Innovation**: The paper focuses on computational chemistry workflow automation using LLM agents and lacks any connection to robotics, embodied AI, or the specified target interests.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16205v1)
- **👥 Authors**: Vitor F. Grizzi, Thang Duc Pham, Luke N. Pretzie, Jiayi Xu, Murat Keceli, Cong Liu
- **🏷️ Source**: #arXiv

---

### 📄 Sentiment Analysis of German Sign Language Fairy Tales (Score: 4/10)
- **💡 Innovation**: The paper focuses on sign language sentiment analysis using traditional ML and basic video features, which falls entirely outside the specified robotics, embodied AI, and advanced generative/LLM research interests.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16138v1)
- **👥 Authors**: Fabrizio Nunnari, Siddhant Jain, Patrick Gebhard
- **🏷️ Source**: #arXiv

---

### 📄 Can LLMs Understand the Impact of Trauma? Costs and Benefits of LLMs Coding the Interviews of Firearm Violence Survivors (Score: 3/10)
- **💡 Innovation**: The paper applies LLMs to qualitative social science coding rather than robotics, embodied AI, or foundational model research, making it off-topic for this pipeline.
- **⚠️ Limitations**: Not promoted to rigorous re-screening.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2604.16132v1)
- **👥 Authors**: Jessica H. Zhu, Shayla Stringfield, Vahe Zaprosyan, Michael Wagner, Michel Cukier, Joseph B. Richardson
- **🏷️ Source**: #arXiv

---


