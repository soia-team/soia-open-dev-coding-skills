# Contributing to soia-open-dev-skills

本仓只发布通用 `soia-dev-*` 技能。开始前先读 `AGENTS.md`；创建或实质修改技能时读
`SKILL_SPEC.md`，涉及落盘与凭据时再读 `DATA_STORAGE_SPEC.md`。

## 1. 从模板创建

```bash
cp -R templates/skill-template skills/<skill-name>
mv skills/<skill-name>/SKILL.md.template skills/<skill-name>/SKILL.md
```

技能名使用 `soia-dev-<action>-<object>[-<qualifier>]`，总计 4–6 段。跨仓迁入时重新判断
域归属，不能沿用不匹配的历史前缀。

## 2. 选择正确的资源位置

| 内容 | 位置 | 规则 |
|---|---|---|
| 必需触发、边界、核心流程、回执 | `SKILL.md` | 跨宿主唯一核心契约，尽量少于 500 行 |
| OpenAI/Codex UI 元数据 | `agents/openai.yaml` | 可选；不得藏必需流程 |
| 供应商规范、机器可读能力事实 | `references/` | 可变列表只保留一份真源 |
| 客户复制的配置模板、静态输入 | `assets/` | 用占位符，不放真实私有配置 |
| 可复用公开实例 | `examples/` | 脱敏、可复现、与报告分开 |
| 带日期的 benchmark/调研证据 | `reports/` | 标明时间、样本、原始证据缺口；不作运行时真源 |
| 可执行逻辑与校验 | `scripts/` | 路径参数化、跨平台、错误显性 |

技能根目录只保留核心入口。不要新增 README、安装指南、CHANGELOG、快速参考、架构说明或
`metadata.json`。

## 3. 编写 frontmatter

```yaml
---
name: soia-dev-<action>-<object>
description: 一句核心职责。触发：「高区分度短语 1」「短语 2」
version: 0.1.0
created_at: <YYYY-MM-DD HH:mm:ss>
updated_at: <YYYY-MM-DD HH:mm:ss>
created_by: <concrete-model-name>
updated_by: <concrete-model-name>
---
```

- `description` 最多 150 个 Unicode 字符；它是路由索引，不是功能清单。
- 有真实安装级依赖时使用 `dependencies.hard/optional/external`；流程邻居不算依赖。
- 版本遵循 SemVer；实质修改同步更新时间和具体模型名。

## 4. 配置、凭据与运行数据

新写入只使用 v2 配置路径：

```text
~/.config/soia-skills/<skill-name>/config.yml
SOIA_<TYPE>_<SHORT>_CONFIG_FILE=<custom-config-path>
```

优先级：CLI 参数 → 进程环境 → 私有 config → provider 登录态指针 → 安全默认值。

- 普通 config 只放非秘密偏好、provider/profile 名和用户选择路径。
- key、token、cookie、session 留在 provider 官方登录态或系统凭据库。
- config/state/cache/temp 使用 `DATA_STORAGE_SPEC.md` 的跨平台解析器，不写仓库相对目录。
- state 必须脱敏并有保留上限；temp 在成功与失败路径都清理。

## 5. 编写与验证

先定义真实验收证据，再实现最小流程：

1. frontmatter 能准确触发且不与同仓技能竞争；
2. 客户首屏包含“能做什么、如何使用、依赖与安装、配置/私密数据、日志与回执”；
3. 主流程可仅凭 `SKILL.md` 执行，供应商细节最多再跳一层 reference；
4. 复杂技能至少有一个 fixture 或真实前向测试，验证输出内容；
5. 示例、报告、Markdown 与机器真源无重复漂移。

生成并检查目录：

```bash
python3 scripts/generate_skill_catalog.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/generate_skill_catalog.py --check
python3 scripts/audit_skills.py --strict
git diff --check
```

再运行改动技能自己的 `--selftest`、fixture 或真实前向测试。只报告实际运行过的验证；
“静态检查通过”“真实调用通过”“已提交”“已发布”是四种不同状态。

## 6. 提交 PR

- 从短期 `feat/`、`fix/` 或 `chore/` 分支向 `dev` 提 PR。
- PR 说明目标、触发词/行为变化、文件布局、验证证据与残余风险。
- 新增或删除技能时更新根 README/README.en，并重新生成 `skills/README.md`。
- 不直接 push `dev`/`main`；不把发布、市场 pin、客户端更新混入普通功能 PR。

安装远程正式版本与发版流程以元仓
[soia-open-skills/CONTRIBUTING.md](https://github.com/soia-team/soia-open-skills/blob/main/CONTRIBUTING.md)
和 `soia-meta-skill-release` 为准。

问题请提交到：https://github.com/soia-team/soia-open-dev-skills/issues
