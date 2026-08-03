# pi 执行规范 / pi (pi-coding-agent) rules

> **注意**：实际命令是 `pi`（安装路径 `~/.npm-global/bin/pi`，`@earendil-works/pi-coding-agent`）。非交互执行必须加 `-p/--print`，否则进入交互式 TUI 挂起等待输入。

## 模式选择

- **非交互单轮执行**：`pi -p '<prompt>'` —— 处理 prompt 后退出
- **指定模型**：`--model <pattern>`（支持 `provider/id`，如 `deepseek/deepseek-v4-flash`；默认取用户 settings 的 defaultModel）
- **控制推理深度**：`--thinking <level>`（off/minimal/low/medium/high/xhigh/max）
- **限制工具面**：`--no-tools`（纯文本回答）或 `--tools a,b`（白名单）
- **隔离会话**：`--session-dir <dir> --no-session` 防止污染主会话

## 推荐命令模板

### 1. 标准非交互执行

```bash
cd /path/to/project
pi -p "$(cat "${TMPDIR:-/tmp}/soia-dev-agent-cli-dispatch/<task-id>/prompt.txt")"
```

适用：

- 自动化编码/分析任务，无需人工确认每步。
- prompt 内容较长（含特殊字符）时必须走 temp 文件传入（见 Prompt 注入防护）。

### 2. 指定模型与推理深度

```bash
cd /path/to/project
pi -p "$(cat "${TMPDIR:-/tmp}/soia-dev-agent-cli-dispatch/<task-id>/prompt.txt")" \
  --model deepseek/deepseek-v4-flash --thinking high
```

适用：

- 需要更强推理能力（--thinking high/xhigh）。
- 需要固定模型与推理深度时（与主控会话的默认配置解耦）。

### 3. 纯文本/无工具回答

```bash
cd /path/to/project
pi -p "总结这个仓库的 README 讲了什么" --no-tools
```

适用：

- 只读分析、总结、评审类任务，避免工具调用产生副作用。

## 关键约束

- `pi` 是 coding harness（带 read/bash/edit/write 工具），非纯聊天 CLI。派发前必须 `cd` 到目标工作目录，或在 prompt 中明确指明路径。
- **每次派发前先验证 CLI 存在**：`pi --version`（缺失立即显性失败，不要烧掉一轮等待）。
- 含特殊字符的 prompt 必须通过 temp 文件传入（见 Prompt 注入防护）。
- 默认会加载 AGENTS.md/CLAUDE.md 与 skills——若派发子任务不需要本机项目上下文，可加 `--no-context-files --no-skills` 减少噪音与 token。
- `pi` 的模型由用户 settings（`~/.pi/agent/settings.json` 的 defaultProvider/defaultModel）决定，`--model` 可覆盖；模型 catalog 中的 deepseek 定价仅作 API 等价值估算（`estimate_cost.py` 永远报告 api_equivalent_estimate，不假设订阅扣费）。
- 不要把你的 AI 工具配置目录（如 `~/.claude/`、`~/.codex/`、`~/.pi/agent/` 等）作为工作目录。
