"""Replaces _default_theme_definitions in theme_manager.py with 16-theme structure."""
import re

NEW_DEFS = '''    def _default_theme_definitions(self):
        return [
            # 1. 具身智能系统与平台
            {
                "id": "Theme_Embodied_AI_System",
                "title": "具身智能系统与平台",
                "parent": "Embodied AI",
                "keywords": [
                    "embodied ai", "robot system", "humanoid", "mobile manipulation",
                    "whole-body control", "cross-embodiment", "universal embodiment",
                    "multi-robot", "robot platform", "system integration",
                ],
                "tags": ["Embodied_AI"],
            },
            # 2. 通用机器人操作
            {
                "id": "Theme_Robot_Manipulation_General",
                "title": "通用机器人操作",
                "parent": "Robot Manipulation",
                "keywords": [
                    "robot manipulation", "manipulation", "pick-and-place",
                    "object manipulation", "tabletop", "bimanual", "tool use",
                    "generalist manipulation", "open-world manipulation",
                ],
                "tags": ["Robot_Manipulation", "Embodied_AI"],
            },
            # 3. 灵巧操作与接触丰富任务
            {
                "id": "Theme_Dexterous_Contact",
                "title": "灵巧操作与接触丰富任务",
                "parent": "Robot Manipulation",
                "keywords": [
                    "dexterous", "in-hand", "contact-rich", "grasping", "hand",
                    "tactile", "force control", "assembly", "deformable",
                    "extrinsic dexterity",
                ],
                "tags": ["Robot_Manipulation"],
            },
            # 4. VLA 策略学习与控制
            {
                "id": "Theme_VLA_Policy",
                "title": "VLA 策略学习与控制",
                "parent": "VLA",
                "keywords": [
                    "vision-language-action", "vla", "action model", "openvla",
                    "rt-2", "pi0", "generalist policy", "pretrained policy",
                    "action chunking", "flow matching vla",
                ],
                "tags": ["VLA", "Embodied_AI"],
            },
            # 5. VLA 推理、规划与泛化
            {
                "id": "Theme_VLA_Reasoning",
                "title": "VLA 推理、规划与泛化",
                "parent": "VLA",
                "keywords": [
                    "reasoning", "planning", "chain-of-thought", "affordance",
                    "high-level planning", "task planning", "zero-shot generalization",
                    "open-vocabulary", "language grounding",
                ],
                "tags": ["VLA", "LLM"],
            },
            # 6. 世界模型与潜在动力学
            {
                "id": "Theme_World_Model_Dynamics",
                "title": "世界模型与潜在动力学",
                "parent": "World Model",
                "keywords": [
                    "world model", "latent dynamics", "predictive model",
                    "imagination", "rssm", "latent world model",
                    "model-based", "environment model",
                ],
                "tags": ["World_Model"],
            },
            # 7. 视频生成式世界模型
            {
                "id": "Theme_Video_World_Model",
                "title": "视频生成式世界模型",
                "parent": "World Model",
                "keywords": [
                    "video world model", "video diffusion", "world action model",
                    "action-conditioned video", "video generation", "video prediction",
                    "4d world", "interactive video",
                ],
                "tags": ["World_Model", "Diffusion_Model"],
            },
            # 8. 基于模型的规划与决策
            {
                "id": "Theme_Model_Based_Planning",
                "title": "基于模型的规划与决策",
                "parent": "World Model",
                "keywords": [
                    "model-based planning", "trajectory optimization", "lookahead",
                    "rollout", "mpc", "tree search", "latent planning",
                    "imagination-based planning",
                ],
                "tags": ["World_Model", "Reinforcement_Learning"],
            },
            # 9. 强化学习算法
            {
                "id": "Theme_RL_Algorithms",
                "title": "强化学习算法",
                "parent": "Reinforcement Learning",
                "keywords": [
                    "reinforcement learning", "rl", "ppo", "sac", "grpo",
                    "policy gradient", "actor-critic", "online rl",
                    "offline rl", "model-free rl",
                ],
                "tags": ["Reinforcement_Learning"],
            },
            # 10. 奖励建模与信用分配
            {
                "id": "Theme_Reward_Credit",
                "title": "奖励建模与信用分配",
                "parent": "Reinforcement Learning",
                "keywords": [
                    "reward model", "reward shaping", "credit assignment",
                    "value function", "return decomposition", "intrinsic reward",
                    "vlm reward", "preference learning",
                ],
                "tags": ["Reinforcement_Learning"],
            },
            # 11. 扩散策略与生成式动作
            {
                "id": "Theme_Diffusion_Policy",
                "title": "扩散策略与生成式动作",
                "parent": "Diffusion Model",
                "keywords": [
                    "diffusion policy", "ddpm", "denoising", "flow matching",
                    "score matching", "action diffusion", "dit policy",
                    "consistency policy",
                ],
                "tags": ["Diffusion_Model", "Robot_Manipulation"],
            },
            # 12. 基础模型与 LLM 驱动机器人
            {
                "id": "Theme_Foundation_LLM",
                "title": "基础模型与 LLM 驱动机器人",
                "parent": "Foundation Models",
                "keywords": [
                    "foundation model", "large language model", "llm", "vlm",
                    "multimodal", "gpt", "code as policy", "saycan",
                    "language conditioned", "instruction following",
                ],
                "tags": ["Foundation_Model", "LLM"],
            },
            # 13. Sim-to-Real 迁移
            {
                "id": "Theme_Sim2Real",
                "title": "Sim-to-Real 迁移",
                "parent": "Sim2Real",
                "keywords": [
                    "sim2real", "domain randomization", "sim-to-real",
                    "synthetic data", "domain adaptation", "zero-shot transfer",
                    "physics simulation", "isaac gym", "mujoco",
                ],
                "tags": ["Sim2Real", "Embodied_AI"],
            },
            # 14. 3D/4D 感知与场景表征
            {
                "id": "Theme_3D_Perception",
                "title": "3D/4D 感知与场景表征",
                "parent": "3D Perception",
                "keywords": [
                    "3d gaussian", "gaussian splatting", "nerf", "4d reconstruction",
                    "point cloud", "depth estimation", "3d representation",
                    "scene reconstruction", "monocular", "multi-view", "spatial",
                ],
                "tags": ["3D_Gaussian_Splatting", "Embodied_AI"],
            },
            # 15. 模仿学习与人机交互
            {
                "id": "Theme_Imitation_HRI",
                "title": "模仿学习与人机交互",
                "parent": "Imitation Learning",
                "keywords": [
                    "imitation learning", "behavior cloning", "demonstration",
                    "teleoperation", "human motion", "mocap",
                    "hand-object interaction", "hoi", "egocentric",
                ],
                "tags": ["Robot_Manipulation", "Embodied_AI"],
            },
            # 16. 多模态感知与表征学习
            {
                "id": "Theme_Multimodal_Perception",
                "title": "多模态感知与表征学习",
                "parent": "Foundation Models",
                "keywords": [
                    "multimodal", "visual representation", "vision encoder",
                    "contrastive learning", "clip", "siglip", "visual pretraining",
                    "tactile", "multi-sensor", "situated awareness",
                ],
                "tags": ["Foundation_Model", "Embodied_AI"],
            },
        ]
'''

RELATIONS = '''THEME_RELATIONS = {
    "Theme_Embodied_AI_System":       ["Theme_Robot_Manipulation_General", "Theme_Sim2Real", "Theme_VLA_Policy", "Theme_Foundation_LLM"],
    "Theme_Robot_Manipulation_General": ["Theme_Embodied_AI_System", "Theme_Dexterous_Contact", "Theme_Diffusion_Policy", "Theme_Sim2Real"],
    "Theme_Dexterous_Contact":        ["Theme_Robot_Manipulation_General", "Theme_Sim2Real", "Theme_Imitation_HRI"],
    "Theme_VLA_Policy":               ["Theme_VLA_Reasoning", "Theme_Foundation_LLM", "Theme_Diffusion_Policy", "Theme_World_Model_Dynamics"],
    "Theme_VLA_Reasoning":            ["Theme_VLA_Policy", "Theme_Foundation_LLM", "Theme_Model_Based_Planning"],
    "Theme_World_Model_Dynamics":     ["Theme_Video_World_Model", "Theme_Model_Based_Planning", "Theme_RL_Algorithms"],
    "Theme_Video_World_Model":        ["Theme_World_Model_Dynamics", "Theme_Diffusion_Policy", "Theme_VLA_Policy"],
    "Theme_Model_Based_Planning":     ["Theme_World_Model_Dynamics", "Theme_RL_Algorithms", "Theme_VLA_Reasoning"],
    "Theme_RL_Algorithms":            ["Theme_Reward_Credit", "Theme_Model_Based_Planning", "Theme_Sim2Real"],
    "Theme_Reward_Credit":            ["Theme_RL_Algorithms", "Theme_VLA_Policy"],
    "Theme_Diffusion_Policy":         ["Theme_VLA_Policy", "Theme_Video_World_Model", "Theme_Robot_Manipulation_General"],
    "Theme_Foundation_LLM":           ["Theme_VLA_Policy", "Theme_VLA_Reasoning", "Theme_Multimodal_Perception"],
    "Theme_Sim2Real":                 ["Theme_Embodied_AI_System", "Theme_RL_Algorithms", "Theme_Robot_Manipulation_General"],
    "Theme_3D_Perception":            ["Theme_Embodied_AI_System", "Theme_World_Model_Dynamics", "Theme_Robot_Manipulation_General"],
    "Theme_Imitation_HRI":            ["Theme_Robot_Manipulation_General", "Theme_Foundation_LLM", "Theme_Dexterous_Contact"],
    "Theme_Multimodal_Perception":    ["Theme_Foundation_LLM", "Theme_VLA_Policy", "Theme_3D_Perception"],
}
'''

with open('src/theme_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace THEME_RELATIONS block
content = re.sub(
    r'THEME_RELATIONS\s*=\s*\{[\s\S]*?\}\s*\n',
    RELATIONS,
    content
)

# Replace _default_theme_definitions method
lines = content.split('\n')
start, end = None, None
for i, line in enumerate(lines):
    if '    def _default_theme_definitions(self):' in line:
        start = i
    if start is not None and i > start and line.startswith('    def ') and '_default_theme_definitions' not in line:
        end = i
        break

new_lines = lines[:start] + NEW_DEFS.split('\n') + lines[end:]
content = '\n'.join(new_lines)

with open('src/theme_manager.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done: 16 themes + updated THEME_RELATIONS written.")
