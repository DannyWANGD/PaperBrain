# Tag Guide

PaperBrain uses Obsidian nested tags and properties as the main organization layer. A paper can belong to many facets at once, so do not force it into a single topic.

## Tag Families

- `domain/...`: research area, such as `domain/vla`, `domain/world_model`, `domain/robot_manipulation`.
- `method/...`: core method, such as `method/diffusion_policy`, `method/planning`, `method/reinforcement_learning`.
- `task/...`: task or setting, such as `task/manipulation`, `task/navigation`, `task/video_prediction`.
- `type/...`: paper type, such as `type/method`, `type/benchmark`, `type/dataset`, `type/system`.
- `impact/...`: reading priority, such as `impact/must_read`, `impact/high_value`, `impact/solid`.
- `status/...`: reading status, such as `status/unread`, `status/reading`, `status/read`.
- `review/...`: tag quality, such as `review/auto_tagged`, `review/needs_review`.

## Properties Worth Editing

- `reading_status`: change this to `reading` or `read` as you work through papers.
- `next_action`: use this as your next research move, for example `deep_read`, `try_reproduce`, `inspect_protocol`, or `review_tags`.
- `review_status`: set to `auto_tagged` after you manually verify tags.
- `priority_score`: generated ranking signal; usually do not edit manually.

## Obsidian Usage

Obsidian nested tags can be searched directly. For example, search `tag:domain/vla` to find VLA papers. In Bases, use tag filters or formulas such as `file.hasTag("domain/vla")` when you want parent/child tag-aware filtering.

Use the generated `Paper_Library.base` for day-to-day browsing. Use `Review_Queue` when tags look too broad or incomplete. Use `Reproduction_Queue` when you want a practical coding or reproduction target.
