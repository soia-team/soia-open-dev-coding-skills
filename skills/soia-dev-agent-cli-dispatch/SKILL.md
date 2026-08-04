---
name: soia-dev-agent-cli-dispatch
description: 外部 AI CLI 调度与模型路由，支持受控派活与用量回执。触发：「派活给外部 AI」「调用 agy」「多 CLI 派发」
dependencies:
  optional: [soia-meta-sync-skills]
version: 1.2.1
created_at: 2026-07-10 11:28:32
updated_at: 2026-08-04 11:13:15
created_by: claude opus 4.6
updated_by: gpt-5.6-sol
---

# soia-dev-agent-cli-dispatch

Use this skill when any host AI needs to dispatch coding, review, analysis,
research, documentation, or content work to an external AI model/CLI — Codex,
Antigravity CLI, Gemini CLI, Kimi CLI, OpenCode, Qwen Code, or a
separately-launched Claude Code process — instead of continuing directly in the
current agent session. This is about calling an external AI process; it is
**not** about a host's built-in sub-agents.

Do not use it when the current agent can just finish the task itself with no
external process involved, or when you only need a one-off local shell
command with no orchestration, monitoring, or prompt-injection concerns.

## 客户可读说明

### 这个技能可以做什么

调度外部 AI 模型/CLI（codex/claude/agy/gemini/kimi/opencode/qwen/pi，非宿主内置子代理，`qodercli` 也有命令模板但未纳入下方精简清单）进行受控派发，覆盖编码、审查、分析、研究、文档和内容任务：任务边界拆分、独立 workdir、防注入 prompt 写法、模型分级矩阵、Worktree 审批门、Anti-Fake-Fix 三步验证。在此之上，可显式指定执行器 + 模型 + 推理深度，或只给执行器家族由任务难度自动选型（见「自动路由」）；每次调用后输出 Token/费用汇总（见「调用总结回执」）、模型完整性检测（见「Model Integrity Gate」）、额度预检（见「额度预检」）与断点续跑（见「可恢复执行」）。各执行器详细命令模板在 `references/` 子目录下按需加载。

| 客户想要 | 技能会做 | 客户能看到 |
|---|---|---|
| 完成本技能覆盖的工作 | 读取用户请求、必要上下文和本技能正文流程，执行最小可靠步骤 | 客户会看到执行计划、命令输出摘要、代码/文档变更、验证结果和风险说明。 |
| 缺少依赖、权限、配置或 key | 停止需要外部状态的动作，明确指出缺什么 | 安装命令、申请地址、配置路径或需要客户确认的问题 |
| 执行完成 | 汇总成功、跳过、失败、文件变更和验证结果 | 一段可复制进工单/日志的完成回执 |

### 客户如何使用

1. 用自然语言说明目标，并提供必要输入：文件、URL、repo、workspace、proposal、vault 或平台账号状态。
2. 能 dry-run 或预览的动作先给预览；涉及删除、覆盖、发送、发布、写远端状态时先征求客户确认。

### 依赖与安装

安装（推荐：装整个领域插件，一次装好本仓全部技能）：

```bash
claude plugin marketplace add soia-team/soia-open-skills
```

```bash
claude plugin install soia-dev@soia
```

只要这一个技能时，可用 npx 路线。注意技能会落进共享真源 `~/.agents/skills`；若同时装了插件，同一技能会出现两份索引且各自漂移，建议二选一：

```bash
npx skills add soia-team/soia-open-dev-skills -g -a '*' -s soia-dev-agent-cli-dispatch -y
```

`npx skills` 会更新 `~/.agents/skills` 共享源，但不管理所有自定义目标。已安装开源 `soia-meta-sync-skills` 的环境可在明确指定目标后执行单项同步：

```bash
python3 ~/.agents/skills/soia-meta-sync-skills/scripts/sync_soia_skills.py \
  --source-dir ~/.agents/skills \
  --targets soia,workbuddy \
  --skills soia-dev-agent-cli-dispatch
```

最终验收应确认 `~/.soia/skills/soia-dev-agent-cli-dispatch` 与 `~/.workbuddy/skills/soia-dev-agent-cli-dispatch` 都是指向 `~/.agents/skills/soia-dev-agent-cli-dispatch` 的软链接；不要把本地源码 checkout 当成 npx 安装结果。

配置约定：

```text
~/.config/soia-skills/soia-dev-agent-cli-dispatch/config.yml
SOIA_DEV_AGENT_CLI_DISPATCH_CONFIG_FILE=<custom-config-path>
```

- 如果本技能不需要私有配置，可以不创建 `config.yml`。
- 如果需要 API key、cookie、session、provider home 或本机路径，只能放进私有 `config.yml`、进程环境或 provider 自己的登录态里，不能写进仓库、vault 正文或日志。
- 第三方 skill 只能声明依赖和安装方式，不直接修改第三方 skill 文件。
- 本技能不硬绑定任何具体编排系统；文中出现的“你的编排层”指调用本技能的上层 Agent/系统，不是某个特定产品。

### 私密信息与中间数据

- API key、cookie、session、provider home 与本机路径只进入私有 `~/.config/soia-skills/soia-dev-agent-cli-dispatch/config.yml`、进程环境或 provider 登录态，不写入仓库、vault 正文或日志。
- 派发 prompt 属于可追溯运行产物：一次性派发写入 `${TMPDIR:-/tmp}/soia-dev-agent-cli-dispatch/<task-id>/prompt.txt`（用完清理）；需要跨会话审计时改用 `${XDG_STATE_HOME:-~/.local/state}/soia-dev-agent-cli-dispatch/`（见 `DATA_STORAGE_SPEC.md` B 类）。
- `run_matrix.py` manifest 记录脱敏字段（状态、token、成本、模型回显），不保存命令输出正文与 prompt 内容。
- 回执与日志不得输出凭据、账号标识、私有路径或响应正文。

### 日志与完成回执

每次执行都要让客户看见过程和结果。最低回执格式：

```markdown
完成：<一句话说明本次完成了什么>。

日志摘要：
- started: <检查到的输入/配置/依赖，不打印秘密值>
- processed: <数量或范围>
- created/updated: <数量或路径>
- skipped/failed: <数量和原因>

文件变化：
- <绝对路径或“未改动文件”>

验证：
- <运行过的检查、命令或人工核对点>

问题与下一步：
- <缺 key / 缺依赖 / 需要客户确认 / 建议下一条命令；没有则写“无”>
```

## ⚡ 触发条件

满足任一即调用本技能（自然语言里常见的说法包括但不限于「派活给 codex」「让 claude 分析」「调用外部 AI」「多 CLI 派发」「后台跑任务」）：

| 条件 | 说明 |
|------|------|
| 需要把编码、审查、分析、研究、文档或内容子任务交给外部 AI CLI 执行 | 当前 host AI 不直接做，而是派给另一个外部 AI 进程 |
| 为子 agent 生成 prompt | 需要防注入的 temp 文件写法 |
| 后台启动长任务 | 需要受控 workdir + 进度监控 |
| 多 agent 并行 | 需要制定依赖 / 分配矩阵 / 派发计划 |

**不需要调用**：自己直接执行代码任务（无派发动作）。

## 如何自查你的外部 AI CLI 可用性

不要假设某个 CLI 一定可服务。派发前按下面顺序自查，把结果记在你自己的可用性记录里，而不是照抄本文档里的任何示例状态（示例会过期）：

1. **CLI 是否已安装**：`which <command>` 或 `<command> --version`；版本号以实际输出为准。**每次派发前都要跑，包括你昨天刚用过的执行器**——实战教训（2026-07-29）：codex 因用户迁移/重装从机器上整体消失，主控凭「昨天还在」直接后台派发，任务静默空跑失败。后台派发命令应内嵌护栏：`command -v <cli> >/dev/null || { echo "CLI missing"; exit 9; }`，让缺失立即显性失败而不是烧掉一轮等待。
2. **认证 / 套餐是否有效**：优先使用官方的本地状态命令。若 CLI 没有不调用模型的 auth-status 命令（当前 `agy` 即如此），不得把 `<command> -p "ping"` 伪装成“零额度只读检查”；模型调用可能消耗额度，必须先获客户确认。需要浏览器登录时在 PTY 启动，状态记为 `blocked_user_action`，由客户本人完成账号选择与授权。
3. **上一次派发是否失败**：如果最近一次该执行器的任务返回非预期错误或反复超时，先记为暂不可服务，等你验证修复后再恢复派发。
4. **维护你自己的可用性表**：建议自建一张「执行器 / CLI 可用 / 套餐-Key 状态 / 可服务 / 备注」的表格，随你的编排层状态变化更新。

不可服务的执行器不得派发；等状态恢复、你自己验证通过后再更新记录、再派发。

**Google 认证通道不得混用**：Gemini CLI 的消费者 Google OAuth 自
2026-06-18 起已停止服务，应迁移到独立命令 `agy`；Gemini Code Assist
Standard/Enterprise、Gemini API Key 和 Vertex AI 通道仍保留在 `gemini`
执行器中。禁止 alias、静默替换命令、复制 OAuth 文件或把一个通道的
套餐/计费结论套到另一个通道。详见 `references/antigravity-cli.md` 与
`references/gemini-cli.md`。

### 全量 benchmark 覆盖闭环

声称“全模型 × 全推理档位已测试”前，必须同时具备：当前 CLI/账号的模型发现快照、每个模型支持档位的发现证据、完整笛卡尔积 case 清单、逐 case 原始 `manifest.json` 和聚合报告。缺少任一项，统一标记 `partial_coverage`，不得只凭聚合转述或 exit code 报告“全量完成”。价格目录中的 `availability` 只表示价格资料列出该模型，不等于当前账号/CLI 已验证可调用；实际执行能力以 `discovered_at`、`discovery_evidence` 和原始 manifest 为准。

## 适用 / 不适用

**适用**：
- 把一个工程任务拆给其他编码代理并行执行
- 把简单但需要外部 AI 执行、复核或留痕的任务受控派发出去
- 在受控工作目录中启动长时间运行的编码任务
- 对子任务执行结果做收集、汇总和复核

**不适用**：
- 不发生外部 AI 派发、只由当前 host 或本地工具直接完成的动作
- 需要立刻得到结果，无法承受异步后台执行
- 还没有明确子任务范围、工作目录和验收标准

任务简单不是排除条件：只要需要由外部 AI CLI 执行，就按风险、输入范围和验收要求选择最小充分的派发方式。

## 核心原则

1. 先定义任务边界，再启动代理
2. 每个代理必须有独立 `workdir`
3. 长任务默认后台运行，并定期汇报进度
4. **`git worktree` 必须事先获得用户明确批准才能开**（与 commit/push/merge 同级不可逆操作门）；未经批准不得执行 `git worktree add`
5. 禁止在凭据目录、用户配置目录或未知目录直接启动编码代理
6. **所有源代码文件必须携带元数据头** → 详见 `references/metadata-header.md`
7. 未经批准的高风险操作一旦发生，必须记录在你自己的治理/审计追踪里（工单、变更日志、违规记录文档等）——记录这一步不能省略

## 执行器派发与推荐组合（按需加载）

完整派发决策树、快速查表、推荐组合与自动路由判据见 `references/executor-routing.md`；各执行器支持状态以 `references/executor-capabilities.yml` 为准。每次派发前先核对实际支持状态，再选择执行器。

自动路由与显式指定的裁决：`scripts/route_model.py` 输出 `selected_model`、`selected_reasoning_effort`、`task_complexity`、`selection_reason`、`estimated_cost_range`、`catalog_version` 与 `selection_status`；没有 verified candidate 时返回阻断状态，不得从 `pending_benchmark` 候选中静默挑一个。

## 最小流程 / Minimum workflow

1. 定义子任务标题、目标、输入、验收标准
2. 输出依赖分析表（Step 1）
3. 输出分配矩阵（Step 2）
4. 输出派发计划（Step 3）
5. 按顺序/并行启动任务，记录 task ID
6. 等待通知，读取输出，失败时分析原因再重试
7. 每个任务完成后，在你的任务跟踪系统里确认状态已更新，再启动下一批

## Prompt 注入防护（通用）

含单引号、特殊字符或 YAML frontmatter 的 prompt **不能**直接嵌入 `bash -c "..."`，也不能不加参数终止符就作为位置参数传入。prompt 以 `-` / `---` 开头时，CLI 可能把正文误判成命令选项。**必须**先写独立文件，并优先通过 stdin 传入：

```bash
# 1. 把 prompt 写入临时文件（按任务 ID 隔离）
# 这是一次性运行产物（SKILL_SPEC.md「脚本写盘决策规则」A 类），用完即可清理
mkdir -p "${TMPDIR:-/tmp}/soia-dev-agent-cli-dispatch/<task-id>/"
cat > "${TMPDIR:-/tmp}/soia-dev-agent-cli-dispatch/<task-id>/prompt.txt" << 'PROMPT_EOF'
你的 prompt 内容，可以包含任意引号和特殊字符...
PROMPT_EOF

# 2a. Codex：用 `-` 明确从 stdin 读取
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check - \
  < "${TMPDIR:-/tmp}/soia-dev-agent-cli-dispatch/<task-id>/prompt.txt"

# 2b. Claude：用本技能脚本从 stdin 读取，prompt 不进入 argv / ps 输出
python3 scripts/run_claude_prompt.py \
  --prompt-file "${TMPDIR:-/tmp}/soia-dev-agent-cli-dispatch/<task-id>/prompt.txt" \
  --model <model-id> --effort high --permission-mode dontAsk \
  --tools Read,Grep,Glob --output-format json

# 2c. Pi：原生 @file 读取 prompt，--mode json 留下模型与 usage 证据
pi -p --mode json --no-session \
  --provider deepseek --model deepseek-v4-flash --thinking low \
  "@${TMPDIR:-/tmp}/soia-dev-agent-cli-dispatch/<task-id>/prompt.txt"
```

如果某个 CLI 不支持 stdin、只能接收位置参数，必须写成 `command [options] -- "$(< "$PROMPT_FILE")"`；其中 `--` 不得省略。长 prompt 仍优先 stdin，避免命令行长度上限和正文暴露在进程列表中。

**prompt 文件命名规范**：`${TMPDIR:-/tmp}/soia-dev-agent-cli-dispatch/<task-id>/prompt.txt`
- 不同任务放不同子目录（按 task-id 隔离），避免并行派发互相覆盖
- 必须先 `mkdir -p` 目标目录
- 如果你的编排层需要跨会话追溯这些 prompt（审计场景），改用 `${XDG_STATE_HOME:-~/.local/state}/soia-dev-agent-cli-dispatch/` 之类的持久位置（SKILL_SPEC.md B 类），不要默认落盘临时目录

## ⛔ Worktree 审批门

`git worktree add` 属于**不可逆操作**，执行前必须：

1. 向用户展示：目标路径 / 分支名 / 用途说明
2. **等待用户明确回复**（“go” / “批准” / “可以”）
3. 收到批准后才能执行

未经批准自行开 worktree 属于违规操作；把违规记录写进你自己的治理/审计追踪（工单、变更日志、违规记录文档等），不要略过这一步只靠事后补救。

## 输出契约 / Output contract

派发时至少输出：

- 子任务标题
- 执行器
- 工作目录
- 启动方式（foreground / background）
- 当前状态（RUNNING / BLOCKED / DONE）
- 下一次检查点

## 统一调用契约 / Unified invocation contract

统一调用的字段、状态、预检、模型完整性、断点恢复、回执、危险目录和反虚假修复门禁集中在 [references/dispatch-contract.md](references/dispatch-contract.md)。

调用前只保留这条主流程：

1. 先做 CLI 版本和认证/额度预检，结果为 `hold` 或 `skip` 时停止并说明原因。
2. 固定 `requested_model` 与 `actual_model` 两个字段；无法从执行器输出验证时写 `unknown`，不能用请求值冒充实际值。codex 的 actual_model 以会话头 `model:` 行为唯一权威（models cache 损坏时其自报身份不可信，详见 `references/codex.md`「实战控制规程」）。
3. 批量任务使用可恢复 manifest；每个 case 完成后原子写入状态，失败、降级、超时和未测试不得伪装成通过。
4. 完成回执必须同时给出执行器、模型、用量状态、异常/降级、问题和下一步；未知值保持未知。
5. 涉及危险目录、外部写入或代码代理任务时，先执行参考文件中的安全门禁和真实输出验证。

## 🔴 Codex Prompt 卫生规则（防止 CLI 读治理文件而非写代码）

**多数编码 CLI 在启动时会扫描工作目录**。无关的治理/技能文件会占用 context，但目标仓的适用规则和目标文件不能因此被删掉。

**禁止在代码修复 prompt 里出现以下无关内容**：
- 与目标任务无关的产品 workspace、board、proposal、`AGENTS.md` 或其他 skill 路径
- 与目标无关的技能/子代理调用指令（如 `@xxx-skill`、内部技能前缀名）
- 不适用于目标仓的产品治理流程说明（阶段编号、门禁名称等内部术语）
- 回写指令（可选：需要回写时简化为单行命令）

若目标本身就是 skill package 或 AGENTS 配置，prompt **必须**包含目标仓适用的 `AGENTS.md` 规则和精确 `skills/<skill-name>/...` / 配置文件路径；只排除无关的 SOIA 产品 board/proposal 上下文，不能因路径名含 `skills/` 或 `AGENTS.md` 就删除任务必要输入。

**代码修复 prompt 应只包含**：
1. 工作目录
2. 要修改的文件路径 + 行号
3. 要执行的编辑操作（精确的 before/after）
4. 验证命令（如 `cargo check` / `npm test` / 对应项目的测试命令）
5. 简单回写（可选，一行命令）

**工作目录选择**：
- 派发代码修复任务时，尽量指定较窄的子目录（如具体模块目录而非仓库根），避免 CLI 扫到治理/技能目录
- 若目标是仓级规则、跨 skill 测试或 catalog，仓库根就是必要 workdir；用目标文件 allowlist 和明确禁区控制范围，不得伪造更窄目录

---

## 🔴 CLI 停止处理规程（uncommitted changes 场景）

部分编码 CLI 有治理检查行为：发现工作目录有未提交改动时，可能停下来请求确认。

**触发场景**：工作目录有 staged/unstaged 改动（如另一个并行任务或会话留下的未提交修复）

**处理选项**（在 prompt 末尾写明其中一个）：

```
选项 A — 明确授权继续：
"以下未提交改动是已知用户/上游工作：[列表]。全部保留；只修改本任务 allowlist。若发生文件重叠或基线不符，停止并回报。"

选项 B — 提前 commit 再派：
只有用户在当前任务明确授权 commit，且逐项确认已有改动均属于该提交时，才能在派发前精确 git add + git commit。禁止为了“清理工作目录”打包未知或他人的改动。

选项 C — 在 prompt 里列出改动文件并说明：
"以下文件有未提交改动：[列表]。它们属于其他任务，请保留不动，继续执行本任务。"
```

**推荐**：优先使用经用户批准的隔离 worktree/临时 clone；不能隔离时用选项 C 或带 allowlist 的 A。选项 B 不是默认清理手段，只在 commit 已被明确授权且提交边界已核实时使用。

---

## 价格资料说明 / Pricing reference

- `references/model-pricing-2026-07-10.md` 原样收录 2026-07-10 版模型价格调研原文（未改写数字），顶部注明来源与「正式预算以官方定价页为准」的声明。
- `references/model-catalog.yml` 是从上述原文规范化提取的**运行时单一事实源**：`scripts/estimate_cost.py`、`scripts/run_matrix.py` 只读取这个 YAML 文件，不解析 Markdown。人工核对价格时，请以 Markdown 原文为准；脚本计算以 YAML 为准；两者数字不一致时先修 YAML 再核对来源，不要各自为政。
- 更新价格时：先改 `model-pricing-2026-07-10.md`（或新增一份带日期的新快照文件），再同步改 `model-catalog.yml`，改完跑 `python3 scripts/catalog_lib.py --selftest` 确认结构仍然合法。
- 「codex 5.6 系实测分级」一节（见上文）是**初步单日样本**，与本节的官方/半官方价格资料性质不同，不要混用：分级节是"哪个模型/档位在这次测试里表现更好"，本节是"这个模型每 1M token 官方标价多少"。分级节待全矩阵覆盖（P3 `scripts/run_matrix.py` 批量结果）后需要更新。

## References（按需加载）

| 主题 | 文件 | 何时加载 |
|------|------|----------|
| Codex 执行规范（常用编码主力） | `references/codex.md` | 派发给 codex 时 |
| Claude Code 执行规范 | `references/claude-code.md` | 派发给 claude 时 |
| Antigravity CLI 执行规范 | `references/antigravity-cli.md` | 派发给 agy 或迁移消费者 Google 账号时 |
| Gemini CLI 执行规范 | `references/gemini-cli.md` | 派发给 gemini 时 |
| Kimi CLI 执行规范 | `references/kimi-cli.md` | 派发给 kimi 时 |
| qodercli 执行规范 | `references/qodercli.md` | 派发给 qodercli 时 |
| Pi (pi-coding-agent) 执行规范 | `references/pi.md` | 派发给 pi 时 |
| 执行器派发与推荐组合 | `references/executor-routing.md` | 需要决策树/快速查表/自动路由判据/推荐组合时 |
| 执行器支持能力矩阵 | `references/executor-capabilities.yml` | 核对执行器实际支持状态时 |
| OpenCode + Qwen 执行规范 | `references/opencode-qwen.md` | 派发给 opencode/qwen 时 |
| 代码文件元数据头规范 | `references/metadata-header.md` | 任何代码写入前 |
| 模型价格资料原文（2026-07-10 快照） | `references/model-pricing-2026-07-10.md` | 需要人工核对官方定价、或价格资料更新时 |
| 模型价格/推理档运行时目录 | `references/model-catalog.yml` | `scripts/estimate_cost.py` / `scripts/run_matrix.py` 运行时读取；人工修改前后都跑一次 `scripts/catalog_lib.py --selftest` |
| P4 部分覆盖路由证据（2026-07-10 smoke matrix 聚合结果） | `references/benchmark-2026-07-10.md` | 需要查已覆盖组合、聚合数字、原始 manifest 缺口或下一轮范围时 |

**加载原则**：派发决策确定执行器后，只加载对应执行器的 reference，不要全部加载。

## Scripts（按需调用）

| 脚本 | 用途 | 自检命令 |
|------|------|----------|
| `scripts/catalog_lib.py` | 受限 YAML 子集解析器 + `model-catalog.yml` schema 校验（重复 model_id / 缺字段 / 负价拒绝，未知 reasoning level 标记为 WARN） | `python3 scripts/catalog_lib.py --selftest` |
| `scripts/estimate_cost.py` | 给定 model + token 数，输出 API 等价费用估算（分项 + 总额 + `confidence`），未知模型给出近似候选并以 exit code 2 退出 | `python3 scripts/estimate_cost.py --selftest` |
| `scripts/run_matrix.py` | 可恢复的串行派发矩阵执行器；支持 Codex、Claude 与 Pi 的模型完整性证据，其中 Pi 解析 `--mode json` JSONL | `python3 scripts/run_matrix.py --selftest` |
| `scripts/route_model.py` | 从已验证 catalog 记录机械选择模型/推理档并输出固定路由回执；显式指定优先 | `python3 scripts/route_model.py --selftest` |
| `scripts/run_claude_prompt.py` | 从 UTF-8 prompt 文件经 stdin 调用 Claude Code，防 YAML `---` 被误判为选项，并保留结构化 stdout | `python3 scripts/run_claude_prompt.py --selftest` |

所有脚本均为纯 Python 标准库实现，无第三方依赖。修改任意一个后，先跑对应 `--selftest`，再跑其余脚本的自检，确认没有连带破坏（`estimate_cost.py` 和 `run_matrix.py` 都从 `catalog_lib.py` 导入解析/校验逻辑）。