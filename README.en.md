# SOIA Development Coding Skills

[中文](README.md) · English

Discipline for AI coding: scope the change before touching anything, produce evidence afterwards, never let "looks fine" count as done.

## What this is

`soia-open-dev-skills` is a set of engineering contracts covering the software development lifecycle. It does not write your business logic — it constrains *how* an AI changes code, above all to prevent fake fixes:

```text
Scope (smallest possible change, state what stays untouched)
    ↓
Change (match surrounding code, introduce no new style)
    ↓
Verify (run tests, cite file:line — "should be fine" is not evidence)
    ↓
Review (adversarial pass from independent angles)
    ↓
Receipt (what changed, which files, what is left)
```

The skills compose: `task-execute` is the general loop, `fix-loop` handles review findings, `review-panel` does the adversarial pass, and `coding-protocol` is the underlying contract.

### When to use it

- "Fix this bug — and don't refactor anything else along the way."
- "CI is failing; find out why."
- "Address every review comment on this PR, miss nothing."
- "Review this diff from several angles — I suspect it's fragile."
- "Set up an AGENTS.md baseline for this new project."
- "Docs drifted from the code; sync them."
- "Dispatch this task to an external AI CLI."

### What it does not do

- Does not make product decisions. What to change and why is yours; the skills only ensure it is done cleanly and verifiably.
- Does not merge or release on its own. Review, merge, and release all need your explicit approval.
- Does not touch production. Release skills produce checklists and pre-flight gates; you run them.
- Does not cover design or document pipelines — see [soia-open-dev-design-skills](https://github.com/soia-team/soia-open-dev-design-skills).
- Does not include internal company process; insurance-industry requirement, test, and release standards live in private repos.

## Where to start

Pick an entry point by what you are doing:

| Your task | Use | Done when |
|---|---|---|
| Fix a bug or build a feature | `soia-dev-task-execute` | Scope, minimal change, evidence, review, receipt all present |
| Work through review or test findings | `soia-dev-fix-loop` | Each finding has reproduce, decide, fix, regress recorded |
| Get your work picked apart | `soia-dev-review-panel` | Multi-angle findings, read-only |
| Inspect CI, manage PRs, cut a release | `soia-dev-github-ops` | gh CLI actions are traceable |
| Start a new project | `soia-dev-project-scaffold` | AGENTS.md and docs navigation in place |
| Hand work to another AI CLI | `soia-dev-agent-cli-dispatch` | Dispatch produces a receipt with usage |

`soia-dev-coding-protocol` is the underlying contract; most skills layer it automatically, so you rarely invoke it directly.

## Skill catalog

> **Ready to use**: ✅ works right after install · 🟡 needs an API key or a third-party login first

| Skill | Responsibility | Ready to use |
|---|---|---|
| `soia-dev-agent-cli-dispatch` | Dispatch external AI CLIs with controlled routing, task handoff, and usage receipts. | 🟡 |
| `soia-dev-agent-md-advisor` | Diagnose, design, and rewrite AI project instructions such as AGENTS.md and CLAUDE.md. | ✅ |
| `soia-dev-coding-protocol` | Apply minimal-change, validation-first, and anti-fake-fix contracts to engineering work. | ✅ |
| `soia-dev-doc-sync` | Audit and repair drift in README, CHANGELOG, VERSION, and related documentation from explicit sources of truth. | ✅ |
| `soia-dev-fix-loop` | Resolve review or test findings through reproduction, decision, repair, regression checks, and receipts. | ✅ |
| `soia-dev-github-ops` | Operate pull requests, CI, reviews, releases, and collaborator access with GitHub CLI. | 🟡 |
| `soia-dev-project-scaffold` | Create a minimal AI collaboration baseline and documentation navigation for new Git projects. | ✅ |
| `soia-dev-release-plan-checklist` | Produce release checklists, pre-flight gates, canary verification, and post-release reconciliation for web software. | ✅ |
| `soia-dev-review-panel` | Perform multi-lens, adversarial, read-only reviews of code diffs or skill packages. | ✅ |
| `soia-dev-task-execute` | Execute general engineering tasks through scoped implementation, validation, independent review, and receipts. | ✅ |
| `soia-dev-terminal-ops` | Manage POSIX/macOS/Linux long-running tasks, tmux sessions, log capture, stall diagnosis, and safe recovery. | ✅ |
| `soia-dev-test-draft-doc` | Generate test plans, test cases, and acceptance mappings from requirements, PRDs, or change notes. | ✅ |

## Install

Installing the whole domain plugin is recommended — it brings every skill in this repo:

```bash
claude plugin marketplace add soia-team/soia-open-skills
```

```bash
claude plugin install soia-dev@soia
```

For Codex:

```bash
codex plugin marketplace add soia-team/soia-open-skills
codex plugin add soia-dev@soia
```

For a single skill you can use the npx route. Note the skill lands in the shared
source `~/.agents/skills`; if the plugin is installed too, the same skill shows up
twice and the two copies drift apart — pick one:

```bash
npx skills add soia-team/soia-open-dev-skills -g -a '*' -s <skill-name> -y
```

## Ecosystem

Specifications, the full ecosystem catalog, and install guides live in [soia-team/soia-open-skills](https://github.com/soia-team/soia-open-skills).
The full maintenance workflow is in [CONTRIBUTING.md](https://github.com/soia-team/soia-open-skills/blob/main/CONTRIBUTING.md).

## License

MIT License — see [LICENSE](./LICENSE).
