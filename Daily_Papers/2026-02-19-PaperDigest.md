# 📅 2026-02-19 - Paper Digest
## Summary
Total Papers: 30 | High Impact: 4

## 📝 Papers List
### 🔥 World Action Models are Zero-shot Policies (Score: 9/10)
- **💡 Innovation**: The key novelty is the development of DreamZero, a World Action Model built on a pretrained video diffusion backbone that jointly models future world states and actions from heterogeneous robot and human demonstration data to achieve superior zero-shot and few-shot cross-embodiment robot manipulation generalization that outperforms state-of-the-art VLAs.
- **⚠️ Limitations**: The work lacks comparisons to non-VLA world model-based robot policy baselines, does not evaluate performance on long-horizon complex manipulation tasks, and does not explore integration with 3D/4D Gaussian Splatting for more accurate 3D world state modeling.
- **🔗 Link**: [[World_Action_Models_are_Zero_shot_Policies]]
- **👥 Authors**: Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, Ayaan Malik, Kyungmin Lee, William Liang, Nadun Ranawaka, Jiasheng Gu, Yinzhen Xu, Guanzhi Wang, Fengyuan Hu, Avnish Narayan, Johan Bjorck, Jing Wang, Gwanghyun Kim, Dantong Niu, Ruijie Zheng, Yuqi Xie, Jimmy Wu, Qi Wang, Ryan Julian, Danfei Xu, Yilun Du, Yevgen Chebotar, Scott Reed, Jan Kautz, Yuke Zhu, Linxi "Jim" Fan, Joel Jang
- **🏷️ Tags**: #World_Action_Model #Video_Diffusion_Model #VLA #Cross_Embodiment_Transfer #Robot_Manipulation

---

### 🔥 RynnBrain: Open Embodied Foundation Models (Score: 8/10)
- **💡 Innovation**: The key novelty is the introduction of RynnBrain, a unified open-source spatiotemporal embodied foundation model family with multiple parameter scales and four task-specific post-trained variants that integrate perception, reasoning, and planning, outperforming existing embodied foundation models across 20 embodied and 8 general vision benchmarks.
- **⚠️ Limitations**: The abstract does not disclose underlying technical implementation details (such as whether it leverages diffusion models, 3D/4D Gaussian splatting, reinforcement learning, or sim2real transfer) and lacks validation of real-world physical robot manipulation performance to verify its physically grounded reasoning and planning claims.
- **🔗 Link**: [[RynnBrain]]
- **👥 Authors**: Ronghao Dang, Jiayan Guo, Bohan Hou, Sicong Leng, Kehan Li, Xin Li, Jiangpin Liu, Yunxuan Mao, Zhikai Wang, Yuqian Yuan, Minghao Zhu, Xiao Lin, Yang Bai, Qian Jiang, Yaxi Zhao, Minghua Zeng, Junlong Gao, Yuming Jiang, Jun Cen, Siteng Huang, Liuyi Wang, Wenqiao Zhang, Chengju Liu, Jianfei Yang, Shijian Lu, Deli Zhao
- **🏷️ Tags**: #Embodied_AI #VLA #Foundation_Models #Spatiotemporal_Reasoning #Robot_Planning

---

### ✨ Learning Situated Awareness in the Real World (Score: 7/10)
- **💡 Innovation**: The key novelty is the development of SAW-Bench, a real-world egocentric video benchmark with 2,071 human-annotated QA pairs designed to evaluate observer-centric situated spatial reasoning capabilities of multimodal foundation models, a capability largely ignored in existing environment-centric benchmarks.
- **⚠️ Limitations**: This work only evaluates existing multimodal foundation models on the proposed benchmark without introducing new methods to close the identified 37.66% human-model performance gap, and does not validate the utility of the benchmark for downstream robotic manipulation or embodied agent deployment tasks.
- **🔗 Link**: [[Learning_Situated_Awareness_in_the_Real_World]]
- **👥 Authors**: Chuhan Li, Ruilin Han, Joy Hsu, Yongyuan Liang, Rajiv Dhawan, Jiajun Wu, Ming-Hsuan Yang, Xin Eric Wang
- **🏷️ Tags**: #Multimodal_Foundation_Models #Embodied_AI #Egocentric_Spatial_Reasoning #Situated_Awareness_Benchmark

---

### ✨ BiManiBench: A Hierarchical Benchmark for Evaluating Bimanual Coordination of Multimodal Large Language Models (Score: 7/10)
- **💡 Innovation**: The key novelty is the development of BiManiBench, the first hierarchical benchmark that evaluates multimodal large language model performance on bimanual robot manipulation tasks across three tiers (spatial reasoning, high-level planning, low-level end-effector control) to isolate unique dual-arm challenges and distinguish perceptual hallucinations from planning failures.
- **⚠️ Limitations**: The work does not evaluate non-LLM-based robot manipulation paradigms such as reinforcement learning or world model-driven pipelines, nor does it include sim2real transfer validation for the benchmark tasks to support real-world robot testing.
- **🔗 Link**: [Web Link](https://arxiv.org/abs/2602.08392)
- **👥 Authors**: Xin Wu, Zhixuan Liang, Yue Ma, Mengkang Hu, Zhiyuan Qin, Xiu Li
- **🏷️ Tags**: #Embodied_AI #Robot_Manipulation #Bimanual_Coordination #Foundation_Models #Large_Language_Models

---

### ✨ SLA2: Sparse-Linear Attention with Learnable Routing and QAT (Score: 5/10)
- **💡 Innovation**: The key novelty of SLA2 is three targeted improvements over existing sparse-linear attention: a learnable dynamic router that selects attention computation branches per token, a more faithful sparse-linear attention formulation with a learnable combination ratio between branches, and quantization-aware fine-tuning for low-bit sparse attention that reduces quantization error while delivering higher speedups for video diffusion.
- **⚠️ Limitations**: The work only evaluates SLA2 on video diffusion generation tasks, provides no exploration of its performance on other diffusion use cases relevant to your research interests such as 3D/4D generation or world models for embodied AI, and lacks detailed ablation of the independent contribution of each proposed component.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.12675)
- **👥 Authors**: Jintao Zhang, Haoxu Wang, Kai Jiang, Kaiwen Zheng, Youhe Jiang, Ion Stoica, Jianfei Chen, Jun Zhu, Joseph E. Gonzalez
- **🏷️ Tags**: #Diffusion_Models #Sparse_Attention #Quantization_Aware_Training #Attention_Acceleration #Video_Generation

---

### 📄 MePoly: Max Entropy Polynomial Policy Optimization (Score: 4/10)
- **💡 Innovation**: The key novelty is MePoly, a novel polynomial energy-based model policy parameterization that provides explicit, tractable probability density to enable exact entropy maximization, addressing the limitation of missing explicit probability density in diffusion-based multi-modal policies that complicates policy gradient optimization.
- **⚠️ Limitations**: The work does not validate MePoly on robot manipulation, embodied AI or other application scenarios aligned with your listed interests, and lacks comparative analysis against widely used policy architectures for robotics or diffusion-based policies for embodied tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17832v1)
- **👥 Authors**: Hang Liu, Sangli Teng, Maani Ghaffari
- **🏷️ Tags**: #Reinforcement_Learning #Maximum_Entropy_RL #Energy_Based_Models #Policy_Optimization

---

### 📄 CADEvolve: Creating Realistic CAD via Program Evolution (Score: 3/10)
- **💡 Innovation**: The key novelty is an evolution-based VLM-guided pipeline that incrementally grows valid complex executable CAD programs from simple primitives to construct a large high-quality dataset, enabling fine-tuning of VLMs that achieve state-of-the-art Image2CAD performance across multiple benchmarks.
- **⚠️ Limitations**: The work is limited to CadQuery parametric CAD generation, does not explore integration with 3D scene representations, robotic simulation or manipulation pipelines, and does not evaluate the utility of the generated CAD assets for downstream embodied AI or Sim2Real use cases.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.16317)
- **👥 Authors**: Maksim Elistratov, Marina Barannikov, Gregory Ivanov, Valentin Khrulkov, Anton Konushin, Andrey Kuznetsov, Dmitrii Zhemchuzhnikov
- **🏷️ Tags**: #VLM #Foundation_Models #Image2CAD #CAD_Program_Generation #Evolutionary_Pipeline

---

### 📄 MMA: Multimodal Memory Agent (Score: 3/10)
- **💡 Innovation**: The key novelty is the proposal of the Multimodal Memory Agent (MMA) that assigns dynamic reliability scores to retrieved memory items via combining source credibility, temporal decay, and conflict-aware network consensus to reweight evidence and abstain when support is insufficient, alongside the new MMA-Bench for evaluating belief dynamics and the discovery of the Visual Placebo Effect in RAG-based multimodal agents.
- **⚠️ Limitations**: The work does not explore applications to embodied AI, robot manipulation, or other robotics-related tasks relevant to your stated interests, nor does it integrate with key techniques you listed such as 3D/4D Gaussian Splatting, diffusion models, or reinforcement learning.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.16493)
- **👥 Authors**: Yihao Lu, Wanru Cheng, Zeyu Zhang, Hao Tang
- **🏷️ Tags**: #Multimodal_RAG #Foundation_Models #LLM #Memory_Augmented_Agents #Belief_Dynamics

---

### 📄 Efficient Text-Guided Convolutional Adapter for the Diffusion Model (Score: 3/10)
- **💡 Innovation**: The key novelty is two parameter-efficient text-guided diffusion adapters (Nexus Prime and Slim) that embed cross-attention modules in each Nexus Block to jointly model text prompt and structural input conditioning, achieving better generation performance than the T2I-Adapter baseline with significantly fewer additional parameters.
- **⚠️ Limitations**: This work is only validated on 2D structure-preserving conditional image generation tasks, lacks exploration of extensions to 3D generation, robotics or embodied AI downstream use cases, and does not benchmark against more recent efficient diffusion adapter architectures beyond T2I-Adapter.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.14514)
- **👥 Authors**: Aryan Das, Koushik Biswas, Swalpa Kumar Roy, Badri Narayana Patro, Vinay Kumar Verma
- **🏷️ Tags**: #Diffusion_Models #Efficient_Adapter #Text_Guided_Conditional_Generation #Cross_Attention #Conditional_Image_Generation

---

### 📄 El Agente Gráfico: Structured Execution Graphs for Scientific Agents (Score: 2/10)
- **💡 Innovation**: The key novelty is an LLM-driven single scientific agent framework that embeds decision-making within a type-safe execution environment and dynamic knowledge graphs, using typed symbolic identifiers instead of raw text for context management to improve consistency, provenance tracking, and tool orchestration for complex multi-step scientific workflows.
- **⚠️ Limitations**: The work is only validated on narrow computational scientific tasks (quantum chemistry, conformer generation, metal-organic framework design) and provides no exploration of applicability to robotics, embodied AI, or the other specialized modeling and learning techniques specified in your research interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17902v1)
- **👥 Authors**: Jiaru Bai, Abdulrahman Aldossary, Thomas Swanick, Marcel Müller, Yeonghun Kang, Zijian Zhang, Jin Won Lee, Tsz Wai Ko, Mohammad Ghazi Vakili, Varinia Bernales, Alán Aspuru-Guzik
- **🏷️ Tags**: #LLM_Agents #Knowledge_Graphs #Scientific_Workflow_Automation #Structured_Execution_Graphs

---

### 📄 Understanding the Fine-Grained Knowledge Capabilities of Vision-Language Models (Score: 2/10)
- **💡 Innovation**: This work systematically ablates factors impacting vision-language model fine-grained performance, finding that improved vision encoders disproportionately boost fine-grained classification results while better large language models improve all benchmark scores equally, and that unfreezing LLM weights during pretraining further enhances fine-grained capabilities.
- **⚠️ Limitations**: The study only evaluates performance on generic fine-grained image classification benchmarks and does not explore the applicability of its findings to downstream domain-specific use cases such as embodied perception or robot manipulation.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17871v1)
- **👥 Authors**: Dhruba Ghosh, Yuhui Zhang, Ludwig Schmidt
- **🏷️ Tags**: #Vision_Language_Models #LLM #Fine_Grained_Visual_Classification #Multimodal_Pretraining #Vision_Encoder

---

### 📄 Learning Compact Video Representations for Efficient Long-form Video Understanding in Large Multimodal Models (Score: 2/10)
- **💡 Innovation**: The key novelty is an end-to-end long-form video understanding framework that integrates an information-density-based adaptive video sampler and an autoencoder-based spatiotemporal video compressor with multimodal large language models to achieve high video compression rates while preserving critical discriminative information for understanding tasks.
- **⚠️ Limitations**: The work only evaluates performance on general video understanding benchmarks, lacks validation for downstream use cases relevant to your research interests such as embodied perception or robot manipulation, and does not explore integration with 3D scene representations or robotics-focused foundation models.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17869v1)
- **👥 Authors**: Yuxiao Chen, Jue Wang, Zhikang Zhang, Jingru Yi, Xu Zhang, Yang Zou, Zhaowei Cai, Jianbo Yuan, Xinyu Li, Hao Yang, Davide Modolo
- **🏷️ Tags**: #Multimodal_Large_Language_Models #Long_form_Video_Understanding #Video_Representation_Learning #Adaptive_Video_Sampling #Spatiotemporal_Video_Compression

---

### 📄 ADAPT: Hybrid Prompt Optimization for LLM Feature Visualization (Score: 2/10)
- **💡 Innovation**: The key novelty is ADAPT, a hybrid prompt optimization framework combining beam search initialization and adaptive gradient-guided mutation that mitigates local minima issues to outperform prior methods for LLM feature visualization on Sparse Autoencoder latents.
- **⚠️ Limitations**: The work is only evaluated on Sparse Autoencoder latents from Gemma 2 2B, lacks exploration of cross-modal applicability, and has no relevance to robotics or embodied AI use cases.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17867v1)
- **👥 Authors**: João N. Cardoso, Arlindo L. Oliveira, Bruno Martins
- **🏷️ Tags**: #LLM #Prompt_Optimization #Feature_Visualization #Sparse_Autoencoder #Activation_Analysis

---

### 📄 Quad Length Codes for Lossless Compression of e4m3 (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed Quad Length Codes, a hybrid lossless compression scheme that uses 3 prefix bits to divide 256 e4m3 symbols into 8 areas with distinct code lengths, delivering near-Huffman compression efficiency while enabling much faster decoding and simpler hardware implementation via a 256-entry lookup table instead of complex Huffman tree traversal.
- **⚠️ Limitations**: The work only validates performance on the e4m3 data type, and lacks end-to-end benchmarks of actual LLM training or serving throughput gains when deploying the proposed coding scheme in real distributed computing environments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17849v2)
- **👥 Authors**: Aditya Agrawal, Albert Magyar, Hiteshwar Eswaraiah, Patrick Sheridan, Pradeep Janedula, Ravi Krishnan Venkatesan, Krishna Nair, Ravi Iyer
- **🏷️ Tags**: #Lossless_Compression #LLM #e4m3 #Quad_Length_Codes

---

### 📄 Two Calm Ends and the Wild Middle: A Geometric Picture of Memorization in Diffusion Models (Score: 2/10)
- **💡 Innovation**: The key novelty is a geometric framework that partitions the diffusion model noise schedule into three distinct regimes to characterize non-uniform memorization risk across noise levels, along with a targeted geometry-informed intervention to mitigate memorization in the high-risk medium noise regime.
- **⚠️ Limitations**: The work lacks empirical validation of its proposed framework and intervention on large-scale real-world diffusion models, and does not explore any applications to the robotics, embodied AI or foundation model use cases aligned with your research interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17846v1)
- **👥 Authors**: Nick Dodson, Xinyu Gao, Qingsong Wang, Yusu Wang, Zhengchao Wan
- **🏷️ Tags**: #Diffusion_Models #Diffusion_Memorization_Analysis #Geometric_Diffusion_Framework #Memorization_Mitigation

---

### 📄 TFL: Targeted Bit-Flip Attack on Large Language Model (Score: 2/10)
- **💡 Innovation**: The key novelty is the TFL targeted bit-flip attack framework that leverages a keyword-focused attack loss and auxiliary utility score to achieve precise, low-collateral targeted LLM output manipulation with fewer than 50 bit flips, outperforming prior state-of-the-art bit-flip attack methods.
- **⚠️ Limitations**: The work only evaluates the proposed attack on text-only LLMs and standard NLP benchmarks, and does not explore its applicability to multimodal foundation models, robotics-aligned VLAs, or real-world physical DRAM fault injection environments.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17837v1)
- **👥 Authors**: Jingkai Guo, Chaitali Chakrabarti, Deliang Fan
- **🏷️ Tags**: #Large_Language_Models #Bit_Flip_Attack #Adversarial_Attack #LLM_Robustness

---

### 📄 Influence-Preserving Proxies for Gradient-Based Data Selection in LLM Fine-tuning (Score: 2/10)
- **💡 Innovation**: The key novelty is the two-stage Iprox framework that first applies low-rank compression to the target LLM to preserve influence information, then aligns the gradients and logits of the compressed proxy with the target model to enable low-cost, accurate gradient-based data selection for LLM supervised fine-tuning.
- **⚠️ Limitations**: The work only evaluates the proposed framework on general LLM fine-tuning tasks, and does not explore its applicability to other large model types such as vision-language models or robotics foundation models, nor validate its performance on domain-specific datasets for embodied AI or robot manipulation scenarios.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17835v1)
- **👥 Authors**: Sirui Chen, Yunzhe Qi, Mengting Ai, Yifan Sun, Ruizhong Qiu, Jiaru Zou, Jingrui He
- **🏷️ Tags**: #LLM #Supervised_Fine_Tuning #Gradient_Based_Data_Selection #Low_Rank_Model_Compression #Influence_Functions

---

### 📄 Drift Estimation for Stochastic Differential Equations with Denoising Diffusion Models (Score: 2/10)
- **💡 Innovation**: The key novelty is framing time-homogeneous SDE drift estimation as a conditional denoising task, and deriving an effective drift estimator as a by-product of training a conditional diffusion model for dynamic trajectory simulation that outperforms classical methods in high-dimensional settings.
- **⚠️ Limitations**: The work only tests on synthetic SDE drift classes with pre-known diffusion coefficients, and does not explore real-world use cases, integration with dynamical system modeling for robotics, or cross-validation against alternative modern non-diffusion estimation approaches.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17830v1)
- **👥 Authors**: Marcos Tapia Costa, Nikolas Kantas, George Deligiannidis
- **🏷️ Tags**: #Diffusion_Models #Stochastic_Differential_Equations #Drift_Estimation #Conditional_Denoising #Trajectory_Simulation

---

### 📄 Causality by Abstraction: Symbolic Rule Learning in Multivariate Timeseries with Large Language Models (Score: 2/10)
- **💡 Innovation**: The key novelty is the ruleXplain framework, which leverages Large Language Models with a constrained temporal symbolic rule language and simulator-generated counterfactual trajectories to extract verifiable, interpretable causal rules for multivariate timeseries with delayed effects.
- **⚠️ Limitations**: The framework requires access to a fully functional ground-truth simulator for counterfactual generation, is only validated on non-robotic, non-embodied domains (epidemiology and building energy simulation), and does not demonstrate utility for downstream robotics or embodied AI tasks.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17829v1)
- **👥 Authors**: Preetom Biswas, Giulia Pedrielli, K. Selçuk Candan
- **🏷️ Tags**: #Large_Language_Models #Causal_Rule_Learning #Multivariate_Timeseries_Analysis #Symbolic_Reasoning #Counterfactual_Generation

---

### 📄 Sketch2Feedback: Grammar-in-the-Loop Framework for Rubric-Aligned Feedback on Student STEM Diagrams (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposed grammar-in-the-loop Sketch2Feedback framework that decomposes rubric-aligned student STEM diagram feedback generation into four cascaded stages (hybrid perception, symbolic graph construction, constraint checking, constrained VLM feedback) to eliminate ungrounded hallucinations common in end-to-end large multimodal models.
- **⚠️ Limitations**: The work only evaluates on two small synthetic diagram datasets, lacks validation on real student-drawn diagrams, does not generalize to other STEM diagram types, and does not explore adaptation to dynamic or more complex rubric requirements.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.18520v1)
- **👥 Authors**: Aayam Bansal
- **🏷️ Tags**: #LLM #Large_Multimodal_Models #Hallucination_Mitigation #Symbolic_Constraint_Checking #Diagram_Perception

---

### 📄 VQPP: Video Query Performance Prediction Benchmark (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposal of the first dedicated benchmark for video query performance prediction, consisting of 56K text queries, 51K videos across two text-to-video retrieval datasets, two CBVR systems, standard splits, and evaluated baseline predictors for the previously under-explored video domain QPP task.
- **⚠️ Limitations**: The benchmark only covers two text-to-video retrieval datasets and two CBVR systems, lacks exploration of cross-modal query types beyond text, and does not demonstrate applicability to use cases aligned with robotics or embodied AI research.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17814v1)
- **👥 Authors**: Adrian Catalin Lutu, Eduard Poesina, Radu Tudor Ionescu
- **🏷️ Tags**: #Large_Language_Models #Direct_Preference_Optimization #Text_to_Video_Retrieval #Video_Query_Performance_Prediction #Query_Reformulation

---

### 📄 Promptable segmentation with region exploration enables minimal-effort expert-level prostate cancer delineation (Score: 2/10)
- **💡 Innovation**: The key novelty is a reinforcement learning guided region-growing segmentation framework that leverages user-provided point prompts and a reward function balancing segmentation accuracy and voxel-wise uncertainty to achieve expert-level prostate cancer MR image segmentation with drastically reduced annotation effort.
- **⚠️ Limitations**: The framework requires fully supervised training on large expert-annotated medical datasets, only demonstrates performance on prostate MR imaging segmentation tasks, and has no applicability or validation for the robotics and specific AI research areas you are interested in.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17813v1)
- **👥 Authors**: Junqing Yang, Natasha Thorley, Ahmed Nadeem Abbasi, Shonit Punwani, Zion Tse, Yipeng Hu, Shaheer U. Saeed
- **🏷️ Tags**: #Reinforcement_Learning #Medical_Image_Segmentation #Point_Prompted_Segmentation #Region_Growing_Segmentation #Uncertainty_Aware_Reward

---

### 📄 Enabling Training-Free Text-Based Remote Sensing Segmentation (Score: 2/10)
- **💡 Innovation**: The key novelty is a fully training-free or lightweight LoRA-tuned pipeline that integrates contrastive CLIP, generative VLMs (GPT-5, Qwen-VL) and Segment Anything Model to achieve state-of-the-art zero-shot open-vocabulary, referring, and reasoning-based text-guided remote sensing segmentation without extra dedicated trainable components.
- **⚠️ Limitations**: The work is restricted to 2D remote sensing imagery segmentation tasks, provides no insights relevant to robotics, embodied perception or 3D/4D scene understanding, and is not validated on any non-remote-sensing datasets.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17799v1)
- **👥 Authors**: Jose Sosa, Danila Rukhovich, Anis Kacem, Djamila Aouada
- **🏷️ Tags**: #Vision_Language_Models #Segment_Anything_Model #Zero_Shot_Semantic_Segmentation #LoRA #Foundation_Models

---

### 📄 Reinforcement-Learning-Based Assistance Reduces Squat Effort with a Modular Hip--Knee Exoskeleton (Score: 2/10)
- **💡 Innovation**: The key novelty is a reinforcement learning-based neural controller trained in physics simulation for a modular hip-knee exoskeleton that delivers personalized real-time assistance torques to reduce metabolic effort during squatting, validated via in-human subject trials.
- **⚠️ Limitations**: This work has limitations including a small sample size of only 5 healthy adult participants, reduced squat depth observed in assisted trials, no testing of generalizability to other lower-limb movements or user populations with mobility impairments, and no optimization of the control policy to maintain consistent squat depth.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17794v1)
- **👥 Authors**: Neethan Ratnakumar, Mariya Huzaifa Tohfafarosh, Saanya Jauhri, Xianlian Zhou
- **🏷️ Tags**: #Reinforcement_Learning #Sim2Real #Exoskeleton_Control #Human_Robot_Interaction

---

### 📄 Multi-agent cooperation through in-context co-player inference (Score: 2/10)
- **💡 Innovation**: The key novelty is leveraging the in-context learning capabilities of sequence models trained against diverse co-player distributions to achieve multi-agent cooperation without hardcoded co-player learning assumptions or explicit timescale separation between meta-learners and naive learners.
- **⚠️ Limitations**: The work is only validated in abstract multi-agent game settings, with no exploration of applications to embodied AI, robot manipulation, or integration with the diffusion models, 3D/4D Gaussian Splatting, or robotics foundation models relevant to your research interests.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.16301)
- **👥 Authors**: Marissa A. Weis, Maciej Wołczyk, Rajai Nasser, Rif A. Saurous, Blaise Agüera y Arcas, João Sacramento, Alexander Meulemans
- **🏷️ Tags**: #Multi_Agent_Reinforcement_Learning #In_Context_Learning #Sequence_Models #Cooperative_AI #Meta_Learning

---

### 📄 Empty Shelves or Lost Keys? Recall Is the Bottleneck for Parametric Factuality (Score: 2/10)
- **💡 Innovation**: The key novelty is a behavioral framework that profiles LLM factual knowledge at the individual fact level to distinguish between failures from missing encoded knowledge and failures from limited access to encoded facts, paired with the automated WikiProfile benchmark for standardized factuality evaluation.
- **⚠️ Limitations**: The work only evaluates factuality on general Wikipedia-sourced facts, does not explore recall performance in domain-specific use cases relevant to robotics or embodied AI, and does not propose concrete systematic methods to improve LLM recall beyond noting the benefit of inference-time thinking.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.14080)
- **👥 Authors**: Nitay Calderon, Eyal Ben-David, Zorik Gekhman, Eran Ofek, Gal Yona
- **🏷️ Tags**: #LLM #Factual_Knowledge_Profiling #Knowledge_Recall #WikiProfile_Benchmark #Inference_Time_Reasoning

---

### 📄 Reinforced Fast Weights with Next-Sequence Prediction (Score: 2/10)
- **💡 Innovation**: The key novelty is the proposal of REFINE, a reinforcement learning framework that adopts the next-sequence prediction objective, entropy-based informative token selection, self-supervised sequence-level rewards, and group relative policy optimization to train fast weight models, addressing the suboptimal long-context representation issue caused by traditional next-token prediction training.
- **⚠️ Limitations**: The work is only validated on text-based long-context tasks, does not explore applicability to non-text modalities or downstream robotics/embodied AI scenarios, and lacks comparison against state-of-the-art long-context transformer baselines to verify its general competitiveness beyond fast weight architectures.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2602.16704)
- **👥 Authors**: Hee Seung Hwang, Xindi Wu, Sanghyuk Chun, Olga Russakovsky
- **🏷️ Tags**: #Reinforcement_Learning #Large_Language_Models #Fast_Weight_Architectures #Long_Context_Modeling #Group_Relative_Policy_Optimization

---

### 📄 MeDUET: Disentangled Unified Pretraining for 3D Medical Image Synthesis and Analysis (Score: 1/10)
- **💡 Innovation**: The key novelty is the MeDUET 3D medical imaging pretraining framework that explicitly disentangles domain-invariant anatomical content from domain-specific style in the VAE latent space via a token demixing mechanism and two novel proxy tasks, enabling unified self-supervised pretraining for both 3D medical image synthesis and analysis.
- **⚠️ Limitations**: The work is restricted exclusively to 3D medical imaging applications, does not demonstrate generalizability to non-medical 3D vision or robotics domains, and lacks validation of the disentanglement approach on datasets outside of multi-center medical imaging collections.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17901v1)
- **👥 Authors**: Junkai Liu, Ling Shao, Le Zhang
- **🏷️ Tags**: #Self_Supervised_Learning #Variational_Autoencoder #Disentangled_Representation_Learning #3D_Medical_Imaging #Contrastive_Learning

---

### 📄 MantisV2: Closing the Zero-Shot Gap in Time Series Classification with Synthetic Data and Test-Time Strategies (Score: 1/10)
- **💡 Innovation**: The key novelty includes the synthetically pre-trained time series encoder Mantis+, a refined lightweight encoder architecture MantisV2, and enhanced test-time strategies leveraging intermediate representations, self-ensembling, and cross-model embedding fusion to achieve state-of-the-art zero-shot time series classification performance.
- **⚠️ Limitations**: The work does not explore the generalizability of its proposed methods to any downstream tasks outside time series classification, and has no relevance to the robotics and embodied AI research areas specified in the user's interests.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.17868v1)
- **👥 Authors**: Vasilii Feofanov, Songkang Wen, Jianfeng Zhang, Lujia Pan, Ievgen Redko
- **🏷️ Tags**: #Time_Series_Classification #Foundation_Models #Zero_Shot_Learning #Synthetic_Data_Pretraining #Test_Time_Adaptation

---

### 📄 Measuring the Prevalence of Policy Violating Content with ML Assisted Sampling and LLM Labeling (Score: 1/10)
- **💡 Innovation**: The key novelty is an unbiased design-based content policy violation prevalence measurement system that leverages ML-assisted weighted sampling to optimize label budget allocation, multimodal LLM labeling with gold-set validation, and post-stratified estimation to support multi-segment analysis from a single global daily sample.
- **⚠️ Limitations**: The work does not provide comprehensive comparative benchmarking against traditional human-labeled prevalence measurement pipelines, nor does it address its robustness to rapidly evolving content policy definitions or zero-day violation types.
- **🔗 Link**: [Web Link](http://arxiv.org/abs/2602.18518v1)
- **👥 Authors**: Attila Dobi, Aravindh Manickavasagam, Benjamin Thompson, Xiaohan Yang, Faisal Farooq
- **🏷️ Tags**: #Multimodal_LLM #LLM_Labeling #ML_Assisted_Sampling #Prevalence_Measurement

---

