# SOIA 开发编码技能库

面向通用软件工程的编码协作技能集，覆盖任务执行、代码变更、审查修复、文档同步、项目脚手架、AI CLI 调度与 GitHub 运维。

## 技能目录

| 技能名 | 一句话简介 |
|---|---|
| `soia-dev-agent-cli-dispatch` | 受控调度外部 AI CLI，完成模型路由、任务派发与用量回执。 |
| `soia-dev-agent-md-advisor` | 诊断、设计和改写 AGENTS.md、CLAUDE.md 等 AI 项目指令。 |
| `soia-dev-coding-protocol` | 为修复、重构和实现建立最小改动、验证前置与防伪修复契约。 |
| `soia-dev-doc-sync` | 根据明确真源审计并修复 README、CHANGELOG、VERSION 等文档漂移。 |
| `soia-dev-fix-loop` | 以复现、决策、修复、回归复核和回执闭环处理评审或测试发现。 |
| `soia-dev-github-ops` | 使用 GitHub CLI 管理 PR、CI、评审、发布与协作者权限操作。 |
| `soia-dev-project-scaffold` | 为新 Git 项目生成最小 AI 协作基线与文档导航结构。 |
| `soia-dev-review-panel` | 对代码差异或技能包执行多视角、对抗式只读审查。 |
| `soia-dev-task-execute` | 以边界定义、最小实施、验证、复核和回执执行通用工程任务。 |

## 安装

使用以下模板安装指定技能：

```bash
npx skills add soia-team/soia-open-dev-coding-skills -g -a '*' -s <技能名> -y
```

例如，安装通用编码协议：

```bash
npx skills add soia-team/soia-open-dev-coding-skills -g -a '*' -s soia-dev-coding-protocol -y
```

## 生态导航

规范真源与全生态目录见 [soia-team/soia-open-skills](https://github.com/soia-team/soia-open-skills)。

## License

[MIT License](LICENSE)
