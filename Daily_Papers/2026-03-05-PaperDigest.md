# 📅 2026-03-05 - Paper Digest
## Summary
Total Papers: 13 | High Impact: 2

## 📝 Papers List
### ✨ ArtHOI: Articulated Human-Object Interaction Synthesis by 4D Reconstruction from Video Priors (Score: 7/10)
- **💡 Innovation**: ArtHOI introduces a decoupled 4D reconstruction pipeline that uses monocular video diffusion priors to recover articulated object states and human motion without 3D supervision.
- **⚠️ Limitations**: The reliance on monocular video priors may lead to geometric drift or failure in complex, self-occluded interactions where the diffusion model's temporal consistency is insufficient.
- **🔗 Link**: [[ArtHOI]]
- **👥 Authors**: Zihao Huang, Tianqi Liu, Zhaoxi Chen, Shaocong Xu, Saining Zhang, Lixing Xiao, Zhiguo Cao, Wei Li, Hao Zhao, Ziwei Liu
- **🏷️ Tags**: #Diffusion_Model #Embodied_AI #Robot_Manipulation

---

### ✨ Memex(RL): Scaling Long-Horizon LLM Agents via Indexed Experience Memory (Score: 7/10)
- **💡 Innovation**: Memex introduces an indexed experience memory mechanism that allows LLM agents to maintain a compact working context by offloading full-fidelity interactions to an external database, which is then optimized via reinforcement learning (MemexRL) to manage retrieval and summarization.
- **⚠️ Limitations**: The paper lacks empirical validation in physical robotic environments, focusing primarily on abstract long-horizon tasks, which leaves the efficacy of the retrieval latency and memory management in real-time embodied control loops unproven.
- **🔗 Link**: [[Memex]]
- **👥 Authors**: Zhenting Wang, Huancheng Chen, Jiayun Wang, Wei Wei
- **🏷️ Tags**: #LLM #Foundation_Model #Reinforcement_Learning

---

### ✨ Helios: Real Real-Time Long Video Generation Model (Score: 6/10)
- **💡 Innovation**: Helios introduces a 14B autoregressive diffusion model that achieves real-time long-video generation by simulating drifting during training and implementing infrastructure-level memory optimizations without relying on standard acceleration heuristics.
- **⚠️ Limitations**: The paper focuses primarily on video generation quality and inference efficiency, lacking explicit evaluation or integration within embodied control loops or robotic manipulation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.04379)
- **👥 Authors**: Shenghai Yuan, Yuanyang Yin, Zongjian Li, Xinwei Huang, Xiao Yang, Li Yuan
- **🏷️ Tags**: #Diffusion_Model #Foundation_Model #World_Model

---

### ✨ RIVER: A Real-Time Interaction Benchmark for Video LLMs (Score: 6/10)
- **💡 Innovation**: The paper introduces a novel benchmark framework (RIVER) that shifts video LLM evaluation from static, offline analysis to a dynamic, real-time interactive paradigm involving retrospective memory and proactive anticipation.
- **⚠️ Limitations**: The benchmark focuses primarily on video comprehension and dialogue rather than physical interaction or closed-loop control, limiting its direct applicability to embodied agents in physical environments.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03985)
- **👥 Authors**: Yansong Shi, Qingsong Zhao, Tianxiang Jiang, Xiangyu Zeng, Yi Wang, Limin Wang
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ BeamPERL: Parameter-Efficient RL with Verifiable Rewards Specializes Compact LLMs for Structured Beam Mechanics Reasoning (Score: 6/10)
- **💡 Innovation**: The paper introduces a parameter-efficient reinforcement learning framework (BeamPERL) that uses symbolic solvers to provide verifiable rewards for training compact LLMs on complex physics reasoning tasks without human-annotated traces.
- **⚠️ Limitations**: The study demonstrates that outcome-level alignment via RL leads to procedural template matching rather than true physical reasoning, failing to generalize to topological shifts in the problem domain.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.04124)
- **👥 Authors**: Tarjei Paule Hage, Markus J. Buehler
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### ✨ Heterogeneous Agent Collaborative Reinforcement Learning (Score: 5/10)
- **💡 Innovation**: HACRL introduces a collaborative reinforcement learning paradigm that enables bidirectional knowledge transfer between heterogeneous agents through shared rollouts without requiring coordinated deployment at inference time.
- **⚠️ Limitations**: The paper focuses on general multi-agent reinforcement learning benchmarks rather than demonstrating the efficacy of the proposed mechanisms in complex, high-dimensional embodied robotic tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.02604)
- **👥 Authors**: Zhixia Zhang, Zixuan Huang, Xin Xia, Deqing Wang, Fuzhen Zhuang, Shuai Ma, Ning Ding, Yaodong Yang, Jianxin Li, Yikun Ban
- **🏷️ Tags**: #Reinforcement_Learning

---

### ✨ Proact-VL: A Proactive VideoLLM for Real-Time AI Companions (Score: 5/10)
- **💡 Innovation**: The paper introduces a framework for proactive, low-latency multimodal interaction by optimizing the decision-making process of when and how a VideoLLM should respond in real-time streaming environments.
- **⚠️ Limitations**: The work focuses on gaming commentary and guidance rather than physical agent control, lacking the action-space grounding required for embodied robotics or manipulation tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03447)
- **👥 Authors**: Weicai Yan, Yuhong Dai, Qi Ran, Haodong Li, Wang Lin, Hao Liao, Xing Xie, Tao Jin, Jianxun Lian
- **🏷️ Tags**: #LLM #Foundation_Model

---

### ✨ MemSifter: Offloading LLM Memory Retrieval via Outcome-Driven Proxy Reasoning (Score: 5/10)
- **💡 Innovation**: MemSifter introduces an outcome-driven proxy reasoning framework that uses Reinforcement Learning to optimize memory retrieval for LLMs, offloading the retrieval burden from the primary model to a smaller, specialized proxy.
- **⚠️ Limitations**: The paper focuses exclusively on text-based LLM benchmarks and lacks evaluation in embodied or multimodal contexts, making its direct applicability to robotics or VLA systems unproven.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03379)
- **👥 Authors**: Jiejun Tan, Zhicheng Dou, Liancheng Zhang, Yuyang Hu, Yiruo Cheng, Ji-Rong Wen
- **🏷️ Tags**: #LLM #Reinforcement_Learning #Foundation_Model

---

### ✨ MIBURI: Towards Expressive Interactive Gesture Synthesis (Score: 5/10)
- **💡 Innovation**: The paper introduces a causal, two-dimensional autoregressive framework that generates hierarchical, body-part-aware motion tokens in real-time, conditioned on LLM-based speech embeddings.
- **⚠️ Limitations**: The framework focuses on virtual agents rather than physical robot hardware, lacking integration with real-world sensorimotor loops or physical constraints typical of embodied robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03282)
- **👥 Authors**: M. Hamza Mughal, Rishabh Dabral, Vera Demberg, Christian Theobalt
- **🏷️ Tags**: #LLM #Embodied_AI #Foundation_Model

---

### ✨ Specificity-aware reinforcement learning for fine-grained open-world classification (Score: 5/10)
- **💡 Innovation**: The paper introduces a reinforcement learning framework (SpeciaRL) that uses a dynamic, verifier-based reward signal to steer Large Multimodal Models toward more specific, fine-grained classifications without sacrificing accuracy.
- **⚠️ Limitations**: The approach is limited to static image classification tasks and does not address the temporal or physical reasoning requirements necessary for embodied agents or robotic interaction.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03197)
- **👥 Authors**: Samuele Angheben, Davide Berasi, Alessandro Conti, Elisa Ricci, Yiming Wang
- **🏷️ Tags**: #Reinforcement_Learning #LLM #Foundation_Model

---

### 📄 CubeComposer: Spatio-Temporal Autoregressive 4K 360° Video Generation from Perspective Video (Score: 4/10)
- **💡 Innovation**: The paper introduces a spatio-temporal autoregressive diffusion framework that decomposes 360° video into cubemap faces to enable native 4K resolution generation while maintaining temporal and spatial coherence.
- **⚠️ Limitations**: The work focuses exclusively on video generation for VR/immersive media and lacks any integration with embodied agents, physical interaction, or world modeling for decision-making.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.04291)
- **👥 Authors**: Lingen Li, Guangzhi Wang, Xiaoyu Li, Zhaoyang Zhang, Qi Dou, Jinwei Gu, Tianfan Xue, Ying Shan
- **🏷️ Tags**: #Diffusion_Model

---

### 📄 SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration (Score: 4/10)
- **💡 Innovation**: The paper introduces a benchmark that shifts the evaluation of LLM-based software agents from static, one-shot bug fixing to long-term, iterative codebase maintenance within a Continuous Integration (CI) framework.
- **⚠️ Limitations**: The work is strictly focused on software engineering and lacks any connection to physical world interaction, embodied agents, or multi-modal sensorimotor control.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.03823)
- **👥 Authors**: Jialong Chen, Xander Xu, Hu Wei, Chuan Chen, Bing Zhao
- **🏷️ Tags**: #LLM #Foundation_Model

---

### 📄 MUSE: A Run-Centric Platform for Multimodal Unified Safety Evaluation of Large Language Models (Score: 4/10)
- **💡 Innovation**: The paper introduces a run-centric evaluation platform that utilizes Inter-Turn Modality Switching (ITMS) to test the robustness of multimodal LLMs against cross-modal adversarial attacks.
- **⚠️ Limitations**: The research is strictly focused on safety and red-teaming of multimodal LLMs, lacking any connection to embodied control, action spaces, or physical world grounding relevant to robotics.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2603.02482)
- **👥 Authors**: Zhongxi Wang, Yueqian Lin, Jingyang Zhang, Hai Helen Li, Yiran Chen
- **🏷️ Tags**: #LLM #Foundation_Model

---


