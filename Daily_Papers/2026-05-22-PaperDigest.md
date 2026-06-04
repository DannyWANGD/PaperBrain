# 📅 2026-05-22 - Paper Digest
## Summary
Total Papers: 5 | High Impact: 1

## 📝 Papers List
### ✨ Afford-VLA: Action-Aligned Visual Planning via Internalized Affordance (Score: 7.5/10)
- **💡 Innovation**: Internalizing task-conditioned affordance as learnable tokens that decode masks and directly condition action generation in a tightly coupled VLA framework.
- **⚠️ Limitations**: The approach may rely on the quality of affordance mask supervision and may not generalize to tasks where affordance is ambiguous or not visually salient.
- **🔗 Link**: [[AffordVLA]]
- **👥 Authors**: Runze Wang, Yuqian Fu, Yu Li, Tao Lin, Tianwen Qian, Mohamed Elhoseiny, Bo Zhao, Yanwei Fu, Yu-Gang Jiang, Xiangyang Xue
- **Institutions**: Fudan University, KAUST, SJTU, East China Normal University
- **🏷️ Tags**: #domain/vla #domain/robot_manipulation #domain/embodied_ai #method/foundation_model #method/planning #task/manipulation #task/planning_reasoning #type/method #impact/solid

---
### ✨ SpaceDG: Benchmarking Spatial Intelligence under Visual Degradation (Score: 6.8/10)
- **💡 Innovation**: Physically grounded degradation synthesis engine using 3DGS to create a large-scale benchmark for spatial reasoning under visual degradation.
- **⚠️ Limitations**: Benchmark is limited to static spatial reasoning tasks and does not evaluate dynamic or interactive scenarios, reducing direct applicability to embodied action.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2605.22536)
- **👥 Authors**: Xiaolong Zhou, Yifei Liu, Ziyang Gong, Jiarui Li, Qiyue Zhao, Muyao Niu, Yuanyuan Gao, Le Ma, Xue Yang, Hongjie Zhang, Zhihang Zhong
- **Institutions**: Unknown
- **🏷️ Tags**: #type/benchmark #domain/multimodal_perception #domain/3d_perception #task/scene_understanding #method/foundation_model #impact/solid

---
### ✨ PhysX-Omni: Unified Simulation-Ready Physical 3D Generation for Rigid, Deformable, and Articulated Objects (Score: 6.7/10)
- **💡 Innovation**: Unified framework generating simulation-ready 3D assets with physical properties across rigid, deformable, and articulated categories using a novel VLM-tailored geometry representation.
- **⚠️ Limitations**: The generated assets may require additional manual tuning for specific physics simulators, and the evaluation of physical fidelity is limited to benchmark metrics rather than real-world physics tasks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2605.21572)
- **👥 Authors**: Ziang Cao, Yinghao Liu, Haitian Li, Runmao Yao, Fangzhou Hong, Zhaoxi Chen, Liang Pan, Ziwei Liu
- **Institutions**: Unknown
- **🏷️ Tags**: #domain/embodied_ai #domain/robot_manipulation #domain/3d_perception #method/simulation #method/benchmark #type/dataset #type/method

---
### ✨ WorldKV: Efficient World Memory with World Retrieval and Compression (Score: 6.5/10)
- **💡 Innovation**: A training-free KV-cache retrieval and compression framework that uses camera/action correspondence and key-key similarity to maintain long-term consistency in autoregressive video diffusion world models.
- **⚠️ Limitations**: The method is only tested on game-like benchmarks and may not scale to complex, real-world robotic manipulation scenarios without further validation.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2605.22718)
- **👥 Authors**: Jung Yi, Minjae Kim, Paul Hyunbin Cho, Wooseok Jang, Sangdoo Yun, Seungryong Kim
- **Institutions**: Unknown
- **🏷️ Tags**: #domain/world_model #domain/embodied_ai #method/diffusion_policy #method/memory #type/method #impact/solid

---
### ✨ Efficient Agentic Reasoning Through Self-Regulated Simulative Planning (Score: 5.7/10)
- **💡 Innovation**: Introduces a self-regulated configurator that decides when and how deeply to plan within an LLM's chain-of-thought, using the LLM as a world model for simulative planning.
- **⚠️ Limitations**: Relies on LLM as world model in language space, which may not capture physical dynamics, and evaluation is restricted to non-embodied reasoning benchmarks.
- **🔗 Link**: [Web Link](https://huggingface.co/papers/2605.22138)
- **👥 Authors**: Mingkai Deng, Jinyu Hou, Lara Sá Neves, Varad Pimpalkhute, Taylor W. Killian, Zhengzhong Liu, Eric P. Xing
- **Institutions**: Unknown
- **🏷️ Tags**: #domain/world_model #method/planning #method/reinforcement_learning #method/foundation_model #task/planning_reasoning #type/method #impact/solid

---

