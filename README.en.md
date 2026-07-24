# SOIA Development Coding Skills

A reusable software-engineering skill set for task execution, code changes, review remediation, documentation sync, project scaffolding, AI CLI dispatch, and GitHub operations.

## Skill Catalog

| Skill | Summary |
|---|---|
| `soia-dev-agent-cli-dispatch` | Dispatch external AI CLIs with controlled routing, task handoff, and usage receipts. |
| `soia-dev-agent-md-advisor` | Diagnose, design, and rewrite AI project instructions such as AGENTS.md and CLAUDE.md. |
| `soia-dev-coding-protocol` | Apply minimal-change, validation-first, and anti-fake-fix contracts to engineering work. |
| `soia-dev-doc-sync` | Audit and repair drift in README, CHANGELOG, VERSION, and related documentation from explicit sources of truth. |
| `soia-dev-draft-test-doc` | Generate test plans, test cases, regression checklists, and acceptance mappings from requirements, PRDs, or change notes. |
| `soia-dev-fix-loop` | Resolve review or test findings through reproduction, decision, repair, regression checks, and receipts. |
| `soia-dev-github-ops` | Operate pull requests, CI, reviews, releases, and collaborator access with GitHub CLI. |
| `soia-dev-project-scaffold` | Create a minimal AI collaboration baseline and documentation navigation for new Git projects. |
| `soia-dev-review-panel` | Perform multi-lens, adversarial, read-only reviews of code diffs or skill packages. |
| `soia-dev-task-execute` | Execute general engineering tasks through scoped implementation, validation, independent review, and receipts. |
| `soia-dev-terminal-ops` | Manage POSIX/macOS/Linux long-running tasks, tmux sessions, log capture, stall diagnosis, and safe recovery. |

## Install

Use this template to install a specific skill:

```bash
npx skills add soia-team/soia-open-dev-coding-skills -g -a '*' -s <skill-name> -y
```

For example, install the coding protocol:

```bash
npx skills add soia-team/soia-open-dev-coding-skills -g -a '*' -s soia-dev-coding-protocol -y
```

## Ecosystem

See [soia-team/soia-open-skills](https://github.com/soia-team/soia-open-skills) for the canonical specifications and complete ecosystem catalog.

## License

[MIT License](LICENSE)
