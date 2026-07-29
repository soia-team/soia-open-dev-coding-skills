# SOIA 开发编码技能库

[English](README.en.md) · 中文

给 AI 编码定纪律：改动前先划边界，改完必须拿出证据，不许把「看起来成功」当完成。

## 这是什么

`soia-open-dev-skills` 是一套面向软件开发全流程的工程契约。它不替你写业务代码，而是约束 AI 怎么改代码——尤其是防止「假修复」：

```text
定边界（最小范围、明确不动什么）
    ↓
改动（按周围代码的写法，不引入新风格）
    ↓
验证（跑测试、给 file:line 证据，不用「应该没问题」交差）
    ↓
复核（独立视角对抗式检查，找没改干净的地方）
    ↓
回执（做了什么、改了哪些文件、还剩什么）
```

技能之间可组合：`task-execute` 是通用闭环，`fix-loop` 处理评审发现，`review-panel` 做对抗式复核，`coding-protocol` 是底层契约。

### 适合什么场景

- 「这个 bug 你改一下，别顺手重构别的。」
- 「CI 挂了，查一下是什么原因。」
- 「把这个 PR 的评审意见逐条改掉，别遗漏。」
- 「多角度审一下这个改动，我怕有坑。」
- 「给这个新项目建个 AGENTS.md 基线。」
- 「文档和代码对不上了，同步一下。」
- 「这个任务派给外部 AI CLI 跑。」

### 不负责什么

- 不替你做产品决策。要改什么、为什么改，由你定；技能只保证改得干净、有据可查。
- 不自动 merge 或发布。评审、合并、发版都需要你明确授权。
- 不碰生产环境。发版技能产出的是清单与预检门，执行由你来。
- 不做设计与文档产线，那在 [soia-open-dev-design-skills](https://github.com/soia-team/soia-open-dev-design-skills)。
- 不包含公司内部流程。保险行业的需求、测试、发版规范在私有仓。

## 从哪里开始

按你手头的事挑入口：

| 你要做的 | 用这个 | 完成标准 |
|---|---|---|
| 改一个 bug 或实现一个功能 | `soia-dev-task-execute` | 边界、最小改动、验证证据、复核、回执五项齐全 |
| 处理评审或测试发现 | `soia-dev-fix-loop` | 每条发现都有复现、决策、修复、回归四步记录 |
| 想让人挑毛病 | `soia-dev-review-panel` | 多视角意见，只读不改 |
| 查 CI / 管 PR / 发 release | `soia-dev-github-ops` | gh CLI 操作有据可查 |
| 新项目起步 | `soia-dev-project-scaffold` | AGENTS.md 与 docs 导航就位 |
| 把活派给别的 AI CLI | `soia-dev-agent-cli-dispatch` | 派发有回执、用量可见 |

`soia-dev-coding-protocol` 是底层契约，多数技能会自动叠加它，通常不需要你单独调用。

## 技能清单

> **开箱可用**：✅ 装完即可使用 · 🟡 还需申请 API key 或完成第三方登录

| 技能 | 一句话职责 | 开箱可用 |
|---|---|---|
| `soia-dev-agent-cli-dispatch` | 外部 AI CLI 调度与模型路由，支持受控派活与用量回执。 | 🟡 |
| `soia-dev-agent-md-advisor` | AI 项目指令与配置设计顾问，提供诊断、起草和改写建议。 | ✅ |
| `soia-dev-coding-protocol` | 为普通工程代码改动建立最小范围、验证前置、anti-fake-fix 与写后复核契约；适用于修复、重构、实现和评审。 | ✅ |
| `soia-dev-doc-sync` | 审计并修复任意代码仓的 docs、README、CHANGELOG、VERSION 与明确真源之间的事实漂移；先建立真源优先级与证据，再按依赖顺序同步派生文档。 | ✅ |
| `soia-dev-fix-loop` | 用五步闭环处理代码审查或测试发现：复现、决策、修复、回归复核与回执，防止遗漏、假修复和无证据收口。 | ✅ |
| `soia-dev-github-ops` | GitHub gh CLI 运维、PR 合规审查与修复。 | 🟡 |
| `soia-dev-project-scaffold` | 为任意新 Git 项目生成最小 AI 协作基线：可编辑的 AGENTS.md 和 docs 导航目录；在写入前确认目标路径。 | ✅ |
| `soia-dev-release-plan-checklist` | 为互联网软件发版生成发布清单、预检门、灰度验证与发布后核对；适用于上线、部署、回滚规划。 | ✅ |
| `soia-dev-review-panel` | 从多视角对代码 diff 或技能包进行对抗式复核，只读且不编辑、合并或发布。 | ✅ |
| `soia-dev-task-execute` | 执行任意工程任务的通用闭环：定义边界、实施最小改动、验证、独立复核与回执。 | ✅ |
| `soia-dev-terminal-ops` | 管理 POSIX/macOS/Linux 上的长任务、tmux 后台会话、日志抓取、停滞诊断与安全恢复；在终止进程前用日志、CPU、网络等多信号交叉判断，并执行 TERM→复查→KILL 确认门。 | ✅ |
| `soia-dev-test-draft-doc` | 从需求、PRD 或变更说明生成测试计划、测试用例与验收对照；适用于测试设计、回归清单和质量评审。 | ✅ |

## 安装

推荐装整个领域插件，一次装好本仓全部技能：

```bash
claude plugin marketplace add soia-team/soia-open-skills
```

```bash
claude plugin install soia-dev@soia
```

Codex 用户：

```bash
codex plugin marketplace add soia-team/soia-open-skills
codex plugin add soia-dev@soia
```

只要单个技能时可用 npx 路线。注意技能会落进共享真源 `~/.agents/skills`；
若同时装了插件，同一技能会出现两份索引且各自漂移，建议二选一：

```bash
npx skills add soia-team/soia-open-dev-skills -g -a '*' -s <技能名> -y
```

## 生态导航

规范真源、全生态技能目录与安装指南见 [soia-team/soia-open-skills](https://github.com/soia-team/soia-open-skills)。
维护本仓技能的完整流程见 [CONTRIBUTING.md](https://github.com/soia-team/soia-open-skills/blob/main/CONTRIBUTING.md)。

## License

MIT License — see [LICENSE](./LICENSE).
