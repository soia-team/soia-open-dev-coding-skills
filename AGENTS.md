# AGENTS.md — soia-open-dev-skills

本文件只定义本仓特有边界。通用技能契约见 `SKILL_SPEC.md`，数据落盘规则见
`DATA_STORAGE_SPEC.md`，贡献步骤见 `CONTRIBUTING.md`；不要把这些长规范复制回本文件。

## 仓库定位

本仓发布通用 `soia-dev-*` 工程技能。技能必须能被不了解维护者机器、账号、vault
和内部 workspace 的客户独立安装与使用。SOIA 产品 proposal/board 治理不因仓名自动触发。

## 开始前

1. 检查当前分支与工作树，保留并隔离无关改动。
2. 修改技能前读取该技能完整 `SKILL.md`；只按需读取它直接链接的 reference。
3. 新增、拆分、改名或实质重构技能时读取 `SKILL_SPEC.md` 和模板。
4. 涉及 config、state、cache、temp、凭据或交付物时读取 `DATA_STORAGE_SPEC.md`。

## 本仓硬边界

- 只接受 `soia-dev-*` 技能；域归属和 4–6 段命名由 `scripts/audit_skills.py` 校验。
- 不提交真实 key、token、cookie、session、密码、账号标识、私有 `config.yml` 或 `.env`。
- 不提交维护者绝对路径、私有目录结构、家庭/健康/财务等个人上下文。
- 客户差异通过 CLI 参数、环境变量或 v2 私有配置处理：
  `~/.config/soia-skills/<skill-name>/config.yml`。
- provider 凭据留在官方登录态或系统凭据库，不复制进普通配置或日志。
- 删除、覆盖、发送、发布、授权、远端写入和创建 worktree 前必须获得明确授权。
- 不把外部 Agent 自报“完成”当作完成；主控必须独立验证真实产物。

## 技能目录契约

```text
skills/<skill-name>/
├── SKILL.md                    # 唯一跨宿主核心流程
├── agents/openai.yaml          # 可选 UI 元数据，不承载必需流程
├── references/                # 持久规范、机器可读能力事实
├── assets/                    # 客户复制模板、静态输入资产
├── examples/                  # 可复用且脱敏的实例
├── reports/                   # 带日期的历史测试/调研报告，不作运行时真源
└── scripts/                   # 可执行实现与校验器
```

技能根目录不要散放配置、报告或快速说明。禁止新增 per-skill README、INSTALL、
CHANGELOG、QUICK_REFERENCE、ARCHITECTURE 或 `metadata.json`。

## 真源与同步顺序

- 可执行行为：代码、schema、机器可读配置、测试。
- 稳定流程：`SKILL.md`。
- 供应商差异和说明：`references/`。
- 历史证据：`reports/`，必须标日期和证据边界。
- `skills/README.md` 是生成物，只能运行生成器更新。
- 同一可变列表只保留一份机器可读真源，Markdown 只链接和解释。

## 验证

提交前运行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/generate_skill_catalog.py --check
python3 scripts/audit_skills.py --strict
git diff --check
```

复杂技能还要运行其自检以及至少一个 fixture 或真实前向测试，核对输出内容而不只看退出码。

通用 `quick_validate.py` 只接受 skills.sh 标准 frontmatter，当前不识别本仓强制的
`version`、时间、作者和依赖字段；它只能作辅助检查，不能替代本仓 audit，也不能为让它
通过而删除本仓字段。

## Git 与发布

- `dev` 是集成分支；功能 PR 指向 `dev`，等待 `audit` 通过后再合并。
- `main` 永远等于最新正式版，只接受由 `soia-meta-skill-release` 驱动的发版 PR。
- 不直接 push `dev`/`main`，不在 feature PR 修改插件 `-SNAPSHOT` 版本。
- 本地 checkout 安装只能称为“本地调试安装”；最终安装验收必须使用已推送远程仓。
- 合并、发布和客户端更新是独立动作，不因代码检查通过而自动执行。

## Git Workflow

- **Branch off `main`** (the latest formal release), then open the PR against
  `dev` and wait for the `audit` check. `main` is always an ancestor of `dev`,
  so such a branch always merges cleanly. Branch off `dev` only when your change
  genuinely builds on unreleased work, and say so in the PR body.
- `main` never receives PRs. It moves only by **fast-forward from `dev`** during
  a formal release driven by `soia-meta-skill-release`, so `main` and `dev` then
  point at the same commit. Never push directly to `main` or `dev`.
- Plugin manifests on `dev` carry a `-SNAPSHOT` version naming the next release
  target. Do not change manifest versions in feature PRs; versions move only
  during a release.
