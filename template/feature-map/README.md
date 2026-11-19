# feature-map

The feature map for {{PROJECT_NAME}}: one place that describes **what** every feature does, with its status on each platform. How the code implements it is in [`docs/`](../docs/README.md).

- [INDEX.md](INDEX.md): all features, their status per platform and where their spec lives
- [features/](features/): one spec per feature, started from [features/_template.md](features/_template.md)
- [GLOSSARY.md](GLOSSARY.md) and [principles.md](principles.md): shared terms and the rules every feature follows
- [decisions/](decisions/): short records of product decisions, numbered in order
- [reference/](reference/): documents kept as received (research, pricing, a roadmap); background, not rules
- [AGENTS.md](AGENTS.md): how to read and maintain the specs, written for coding agents and useful for humans too

`make lint` and `make test` run [scripts/check.py](scripts/check.py), which checks the frontmatter, the requirement IDs, INDEX.md and the links.
