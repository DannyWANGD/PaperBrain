# Review Queue

These notes need manual tag/property review. They usually have missing facets or too many automatically inferred tags.

## Needs Review

| Paper | Score | Tags | Date |
|---|---:|---|---|
| [[Kinema4D]] | 8.0 | `#domain/3d_perception` `#domain/embodied_ai` `#domain/multimodal_perception` `#domain/reinforcement_learning` `#domain/robot_manipulation` `#domain/sim2real` | 2026-03-17 |
| [[SemanticContact Fields for CategoryLevel Generalizable Tactile Tool Manipulation]] | 7.0 | `#domain/3d_perception` `#domain/embodied_ai` `#domain/multimodal_perception` `#domain/reinforcement_learning` `#domain/robot_manipulation` `#domain/sim2real` | 2026-02-14 |
| [[Soft Contamination]] | 7.0 | `#domain/embodied_ai` `#domain/vla` `#method/benchmark` `#method/foundation_model` | 2026-02-12 |
| [[SRG]] | 4.9 | `#domain/reinforcement_learning` `#method/benchmark` `#method/diffusion_policy` `#method/reinforcement_learning` | 2026-03-25 |

```dataview
TABLE score, domains, methods, tasks, next_action
FROM "Research_Notes"
WHERE contains(file.tags, "#review/needs_review")
SORT score DESC
```
