# 📅 2026-02-14 - Paper Digest
## Summary
Total Papers: 18 | High Impact: 3

## 📝 Papers List
### ✨ Semantic-Contact Fields for Category-Level Generalizable Tactile Tool Manipulation (Score: 7/10)
- **💡 Innovation**: The key novelty is the proposed Semantic-Contact Fields (SCFields), a unified 3D representation fusing visual semantics and dense contact estimates, paired with a two-stage sim-to-real contact learning pipeline that aligns simulation pre-trained contact physics with real sensor characteristics using small pseudo-labeled real data, enabling robust diffusion policy execution for category-level generalizable contact-rich tactile tool manipulation.
- **⚠️ Limitations**: The work does not explicitly integrate or evaluate compatibility with generalist VLA/foundation models, only tests on three narrow tool manipulation tasks, and does not explore advanced 3D representations like 3D Gaussian Splatting or reinforcement learning to further boost performance and cross-task generalization.
- **🔗 Link**: [[SemanticContact_Fields_for_CategoryLevel_Generalizable_Tactile_Tool_Manipulation]]
- **👥 Authors**: Kevin Yuchen Ma, Heng Zhang, Weisi Lin, Mike Zheng Shou, Yan Wu
- **🏷️ Tags**: #Diffusion_Model #Embodied_AI #Sim2Real #Robot_Manipulation

---

### ✨ Mean Flow Policy with Instantaneous Velocity Constraint for One-step Action Generation (Score: 7/10)
- **💡 Innovation**: The key novelty is the proposed Mean Velocity Policy (MVP), a one-step generative policy that leverages an instantaneous velocity constraint during training to retain high expressiveness while enabling fast one-step action generation, addressing the expressiveness-computational burden tradeoff of existing flow-based policies.
- **⚠️ Limitations**: The work does not evaluate real-world robot deployment performance, explore integration with foundation models or vision-language-action models, or validate generalization to unstructured embodied tasks beyond the controlled benchmark robotic manipulation tasks tested.
- **🔗 Link**: [[Mean_Flow_Policy_with_Instantaneous_Velocity_Constraint_for_Onestep_Action_Generation]]
- **👥 Authors**: Guojian Zhan, Letian Tao, Pengcheng Wang, Yixiao Wang, Yiheng Li, Yuxin Chen, Masayoshi Tomizuka, Shengbo Eben Li
- **🏷️ Tags**: #Reinforcement_Learning #Robot_Manipulation #Embodied_AI

---

### ✨ Gaussian Sequences with Multi-Scale Dynamics for 4D Reconstruction from Monocular Casual Videos (Score: 7/10)
- **💡 Innovation**: The key novelty is a layered Gaussian sequence representation with multi-scale motion factorization across object to particle levels, paired with complementary supervision from vision foundation models to reduce reconstruction ambiguity for monocular casual video 4D reconstruction.
- **⚠️ Limitations**: The work does not validate the direct utility of its reconstructed 4D scenes for downstream embodied AI tasks such as robot manipulation policy learning, reinforcement learning, or sim2real transfer.
- **🔗 Link**: [[Gaussian_Sequences_with_MultiScale_Dynamics_for_4D_Reconstruction_from_Monocular_Casual_Videos]]
- **👥 Authors**: Can Li, Jie Gu, Jingmin Chen, Fangzhou Qiu, Lei Sun
- **🏷️ Tags**: #3D_Gaussian_Splatting #Foundation_Model #Embodied_AI #Robot_Manipulation

---

### ✨ Enabling Option Learning in Sparse Rewards with Hindsight Experience Replay (Score: 6/10)
- **💡 Innovation**: The key novelty is the proposal of Dual Objectives Hindsight Experience Replay (2HER) that generates both object state-based and agent effector position-based virtual goals, integrated with Multi-updates Option Critic to achieve strong performance on sparse reward robotic manipulation tasks.
- **⚠️ Limitations**: The work is only evaluated in simulated robotic manipulation environments, lacks exploration of sim2real transfer, and does not integrate modern perception or foundation model techniques to improve cross-scenario generalizability.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13865v1)
- **👥 Authors**: Gabriel Romio, Mateus Begnini Melchiades, Bruno Castro da Silva, Gabriel de Oliveira Ramos
- **🏷️ Tags**: #Reinforcement_Learning #Robot_Manipulation #Embodied_AI

---

### 📄 Embed-RL: Reinforcement Learning for Reasoning-Driven Multimodal Embeddings (Score: 4/10)
- **💡 Innovation**: The key novelty is the proposed Embedder-Guided Reinforcement Learning framework that optimizes the reasoning module to generate retrieval-aligned Traceability Chain-of-Thought to improve cross-modal semantic consistency and fine-grained matching performance of universal multimodal embeddings.
- **⚠️ Limitations**: The paper only evaluates its framework on general cross-modal retrieval benchmarks, provides no exploration of applicability to robotics or embodied AI tasks, and does not conduct detailed ablation of key components like the reinforcement learning algorithm or reasoning module backbone to verify the generalizability of the proposed approach.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13823v2)
- **👥 Authors**: Haonan Jiang, Yuji Wang, Yongjie Zhu, Xin Lu, Wenyu Qin, Meng Wang, Pengfei Wan, Yansong Tang
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### 📄 From Pixels to Policies: Reinforcing Spatial Reasoning in Language Models for Content-Aware Layout Design (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposed LaySPA reinforcement learning framework that equips LLMs with explicit interpretable spatial reasoning for content-aware graphic layout design by reformulating the task as policy learning over a structured textual spatial environment optimized via a multi-objective spatial critique and relative group optimization.
- **⚠️ Limitations**: The work is limited to 2D graphic layout design with no exploration of applicability to 3D spatial reasoning, embodied AI or robotics tasks, and does not validate whether the proposed spatial reasoning approach can generalize beyond layout design use cases.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13912v2)
- **👥 Authors**: Sha Li, Stefano Petrangeli, Yu Shen, Xiang Chen
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### 📄 GSRM: Generative Speech Reward Model for Speech RLHF (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposed Generative Speech Reward Model (GSRM) that decomposes speech naturalness evaluation into an interpretable acoustic feature extraction stage followed by feature-grounded chain-of-thought reasoning, delivering more explainable and higher-correlation naturalness judgments than existing evaluators for speech LLM RLHF.
- **⚠️ Limitations**: The work does not test the generalization of GSRM to low-resource or noisy speech scenarios, nor does it provide detailed ablation studies to quantify the contribution of each component of its reasoning pipeline to final prediction performance.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13891v1)
- **👥 Authors**: Maohao Shen, Tejas Jayashankar, Osama Hanna, Naoyuki Kanda, Yancheng Wang, Kateřina Žmolíková, Ruiming Xie, Niko Moritz, Anfeng Xu, Yashesh Gaur, Gregory Wornell, Qing He, Jilong Wu
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 High-Fidelity Causal Video Diffusion Models for Real-Time Ultra-Low-Bitrate Semantic Communication (Score: 3/10)
- **💡 Innovation**: The key novelty is a modular causal video diffusion framework with Semantic Control, Restoration Adapter, and Temporal Adapter modules, paired with an efficient temporal distillation procedure that enables real-time high-fidelity video generation at ultra-low bitrates for semantic communication.
- **⚠️ Limitations**: The work is only validated for general semantic communication tasks, with no exploration of applicability to robotics, embodied AI, 3D scene understanding, or other use cases aligned with your stated research interests, and no integration with modalities like language or 3D representations.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13837v1)
- **👥 Authors**: Cem Eteke, Batuhan Tosun, Alexander Griessel, Wolfgang Kellerer, Eckehard Steinbach
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 voice2mode: Phonation Mode Classification in Singing using Self-Supervised Speech Models (Score: 2/10)
- **💡 Innovation**: The key novelty is demonstrating that lower-layer embeddings from pre-trained self-supervised speech foundation models substantially outperform conventional handcrafted acoustic features for four-class singing phonation mode classification, reaching 95.7% accuracy on a public soprano dataset.
- **⚠️ Limitations**: The method is only evaluated on sustained vowel recordings from soprano singers, so its generalizability to other voice types, continuous singing segments, and non-singing speech contexts is unproven.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13928v1)
- **👥 Authors**: Aju Ani Justus, Ruchit Agrawal, Sudarsana Reddy Kadiri, Shrikanth Narayanan
- **🏷️ Tags**: #Foundation_Model

---

### 📄 GREPO: A Benchmark for Graph Neural Networks on Repository-Level Bug Localization (Score: 2/10)
- **💡 Innovation**: The key novelty is the introduction of GREPO, the first dedicated benchmark for applying Graph Neural Networks to repository-scale bug localization, consisting of 86 Python repositories and 47294 preprocessed graph-structured bug-fixing tasks ready for direct GNN processing.
- **⚠️ Limitations**: The work only evaluates GNN performance against traditional information retrieval baselines, fails to compare against modern retrieval-augmented LLM-based bug localization methods, and is restricted exclusively to Python code repositories.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13921v1)
- **👥 Authors**: Juntong Wang, Libin Chen, Xiyuan Wang, Shijia Kang, Haotong Yang, Da Zheng, Muhan Zhang
- **🏷️ Tags**: #LLM

---

### 📄 Diagnosing Pathological Chain-of-Thought in Reasoning Models (Score: 2/10)
- **💡 Innovation**: The key novelty is the development of simple, computationally inexpensive, task-agnostic metrics to discriminate three identified chain-of-thought reasoning pathologies in LLMs, validated using deliberately trained model organisms that exhibit specific target pathologies.
- **⚠️ Limitations**: The work does not validate the proposed metrics on state-of-the-art large-scale deployed LLMs, nor does it explore applicability to multi-modal foundation models, embodied reasoning systems or robotics-related use cases.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13904v1)
- **👥 Authors**: Manqing Liu, David Williams-King, Ida Caspary, Linh Le, Hannes Whittingham, Puria Radmard, Cameron Tice, Edward James Young
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Experimentation Accelerator: Interpretable Insights and Creative Recommendations for A/B Testing with Content-Aware ranking (Score: 2/10)
- **💡 Innovation**: The key novelty is a unified end-to-end framework that leverages treatment embeddings, a context-adjusted CTR ranking model, sparse Lasso-based semantic interpretability, and LLMs to prioritize A/B test variants, explain winning variant drivers, and generate high-potential new test variants, deployed as a commercial Adobe product.
- **⚠️ Limitations**: The work only evaluates on marketing-focused A/B test datasets from Adobe's business customers, lacks ablation studies to isolate the performance contribution of each framework component, and does not demonstrate generalizability to other domains including the robotics and embodied AI areas of your interest.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13852v1)
- **👥 Authors**: Zhengmian Hu, Lei Shi, Ritwik Sinha, Justin Grover, David Arbour
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 Evaluating LLM-Generated ACSL Annotations for Formal Verification (Score: 2/10)
- **💡 Innovation**: The key novelty is a large-scale controlled empirical evaluation comparing rule-based systems and three state-of-the-art large language models for automated ACSL specification generation, with standardized verification conditions to enable direct, unbiased comparison of annotation quality, solver sensitivity, and proof stability across systems.
- **⚠️ Limitations**: This work is restricted to evaluating ACSL annotation generation for C programs only, does not test generalizability to other programming languages or formal specification frameworks, and provides no insights relevant to the core robotics, 3D vision, or embodied AI research areas of the target audience.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13851v1)
- **👥 Authors**: Arshad Beg, Diarmuid O'Donoghue, Rosemary Monahan
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 DTBench: A Synthetic Benchmark for Document-to-Table Extraction (Score: 2/10)
- **💡 Innovation**: The key novelty is the design of a reverse Table2Doc multi-agent synthesis workflow to generate DTBench, a capability-aware synthetic benchmark for document-to-table extraction that covers a two-level taxonomy of 5 major and 13 subcategories of required extraction capabilities.
- **⚠️ Limitations**: The benchmark only includes synthetically generated documents, lacks real-world unstructured document test cases, and does not evaluate the cross-domain generalization performance of models to document types outside the predefined capability taxonomy.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13812v2)
- **👥 Authors**: Yuxiang Guo, Zhuoran Du, Nan Tang, Kezheng Tang, Congcong Ge, Yunjun Gao
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 AnomaMind: Agentic Time Series Anomaly Detection with Tool-Augmented Reasoning (Score: 2/10)
- **💡 Innovation**: The key novelty is reformulating time series anomaly detection as an agentic sequential decision-making process with multi-turn tool augmentation for adaptive feature preparation, self-reflective decision refinement, and a hybrid inference mechanism combining general-purpose reasoning models and reinforcement learning optimized via workflow-level feedback.
- **⚠️ Limitations**: The paper does not specify the exact general-purpose models used for tool interaction and self-reflection, lacks detailed ablation studies quantifying the contribution of each component of its framework, and does not evaluate performance on any robotics or embodied AI related time series datasets relevant to your stated interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13807v1)
- **👥 Authors**: Xiaoyu Tao, Yuchong Wu, Mingyue Cheng, Ze Guo, Tian Gao
- **🏷️ Tags**: #Reinforcement_Learning #Foundation_Model #LLM

---

### 📄 Cast-R1: Learning Tool-Augmented Sequential Decision Policies for Time Series Forecasting (Score: 2/10)
- **💡 Innovation**: The key novelty is reformulating time series forecasting as a sequential decision-making problem, paired with a memory-based state management mechanism, a tool-augmented agentic prediction workflow, and a two-stage training strategy combining supervised fine-tuning, multi-turn reinforcement learning, and curriculum learning to improve performance in complex evolving settings.
- **⚠️ Limitations**: This work is only validated on time series forecasting tasks, lacks exploration of its applicability to robotics or embodied AI scenarios, and does not benchmark against state-of-the-art foundation model or LLM-based agentic forecasting approaches.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13802v1)
- **👥 Authors**: Xiaoyu Tao, Mingyue Cheng, Chuang Jiang, Tian Gao, Huanjian Zhang, Yaguo Liu
- **🏷️ Tags**: #Reinforcement_Learning #Time_Series_Forecasting #Sequential_Decision_Making #Tool_Augmented_Agents #Agentic_Workflow

---

### 📄 Joint Orientation and Weight Optimization for Robust Watertight Surface Reconstruction via Dirichlet-Regularized Winding Fields (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed Dirichlet Winding Reconstruction (DiWR) pipeline that jointly optimizes point orientations, per-point area weights, and confidence coefficients while minimizing the Dirichlet energy of the generalized winding number field to enable robust watertight surface reconstruction from noisy, non-uniform unoriented point clouds without separate preprocessing steps.
- **⚠️ Limitations**: The paper does not explore downstream applications of the reconstructed surfaces for robotics or embodied AI use cases, and only evaluates performance on static 3D reconstruction benchmarks without testing on dynamic 4D data or real-world robot perception pipelines.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13801v1)
- **👥 Authors**: Jiaze Li, Daisheng Jin, Fei Hou, Junhui Hou, Zheng Liu, Shiqing Xin, Wenping Wang, Ying He
- **🏷️ Tags**: #3D_Gaussian_Splatting #3D_Reconstruction #Point_Cloud_Processing #Implicit_Surface_Representation #Generalized_Winding_Number

---

### 📄 An end-to-end agentic pipeline for smart contract translation and quality evaluation (Score: 1/10)
- **💡 Innovation**: The key novelty is an end-to-end CrewAI-style agent pipeline that converts natural language smart contract specifications to Solidity code and conducts multi-dimensional automated quality evaluation with full provenance metadata tracking.
- **⚠️ Limitations**: The framework does not support formal verification of generated smart contracts, is limited to the Solidity language, and does not validate performance on complex industry-grade smart contract use cases.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.13808v1)
- **👥 Authors**: Abhinav Goel, Chaitya Shah, Agostino Capponi, Alfio Gliozzo
- **🏷️ Tags**: #LLM #Foundation_Model

---


