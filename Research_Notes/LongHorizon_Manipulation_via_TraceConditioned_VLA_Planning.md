---
tags:
  - paper
  - Robot_Manipulation
  - VLA
  - Embodied_AI
  - World_Model
aliases:
  - "Long-Horizon Manipulation via Trace-Conditioned VLA Planning"
  - "LoHo-Manip"
  - "Trace-Conditioned VLA"
  - "Progress-Aware Visual Trace"
  - "Long-Horizon VLA Planning"
  - "Modular VLA Framework"
  - "Trace-Conditioned Planning"
  - "Decoupled VLA Execution"
arxiv_id: "2604.21924"
url: http://arxiv.org/abs/2604.21924v1
pdf_url: https://arxiv.org/pdf/2604.21924v1
local_pdf: "[[LongHorizon Manipulation via TraceConditioned VLA Planning.pdf]]"
github: "None"
project_page: "None"
publication_date: "Unknown"
score: 8
---

# Long-Horizon Manipulation via Trace-Conditioned VLA Planning

## 📌 Abstract
Long-horizon manipulation remains challenging for vision-language-action (VLA) policies: real tasks are multi-step, progress-dependent, and brittle to compounding execution errors. We present LoHo-Manip, a modular framework that scales short-horizon VLA execution to long-horizon instruction following via a dedicated task-management VLM. The manager is decoupled from the executor and is invoked in a receding-horizon manner: given the current observation, it predicts a progress-aware remaining plan that combines (i) a subtask sequence with an explicit done + remaining split as lightweight language memory, and (ii) a visual trace -- a compact 2D keypoint trajectory prompt specifying where to go and what to approach next. The executor VLA is adapted to condition on the rendered trace, thereby turning long-horizon decision-making into repeated local control by following the trace. Crucially, predicting the remaining plan at each step yields an implicit closed loop: failed steps persist in subsequent outputs, and traces update accordingly, enabling automatic continuation and replanning without hand-crafted recovery logic or brittle visual-history buffers. Extensive experiments spanning embodied planning, long-horizon reasoning, trajectory prediction, and end-to-end manipulation in simulation and on a real Franka robot demonstrate strong gains in long-horizon success, robustness, and out-of-distribution generalization. Project page: https://www.liuisabella.com/LoHoManip

## 🖼️ Architecture
![[LongHorizon Manipulation via TraceConditioned VLA Planning_arch.png]]

## 🧠 AI Analysis
Analysis Failed: All models unavailable.

## 📂 Resources
- **Local PDF**: [[LongHorizon Manipulation via TraceConditioned VLA Planning.pdf]]
- [Online PDF](https://arxiv.org/pdf/2604.21924v1)
- [ArXiv Link](http://arxiv.org/abs/2604.21924v1)
