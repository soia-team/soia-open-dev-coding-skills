---
name: soia-dev-terminal-ops
description: 管理 POSIX/macOS/Linux 上的长任务、tmux 后台会话、日志抓取、停滞诊断与安全恢复；杀进程前用日志、CPU、网络多信号交叉判断，并走 TERM→复查→KILL 门。触发：「进程卡住了」「后台跑这个」「安全杀进程」
version: 1.1.3
created_at: 2026-07-07 14:44:10
updated_at: 2026-08-05 10:30:00
created_by: claude opus 4.6
updated_by: claude-opus-5
---

# soia-dev-terminal-ops

面向 POSIX shell、macOS 和 Linux 的长任务终端操作手册。它不虚标 Windows 原生兼容；Windows 用户应在 WSL 或其他 POSIX 环境中使用。

## 客户可读说明

### 这个技能可以做什么

| 客户想要 | 技能会做 | 客户能看到 |
|---|---|---|
| 启动或观察长任务 | 用参数化的 session、日志目录和命令启动 tmux/后台任务 | command、workdir、session/PID、日志路径和当前状态 |
| 判断任务是否停滞 | 在用户指定观察窗口内交叉检查日志、CPU、网络/子进程进展 | 每项信号的证据以及“运行中/疑似停滞/无法判断”结论 |
| 恢复或终止任务 | 先确认目标与数据风险，再按 TERM→复查→KILL 顺序处理 | 每个信号、确认点、退出状态和后续恢复建议 |

### 客户如何使用

提供以下输入；缺少会改变终止目标或日志落点的输入时，先询问，不猜：

- 要运行或诊断的命令、工作目录；
- 已有 PID 或 tmux session（如适用）；
- `session_name`、`log_dir`、`stall_window_seconds`、`term_grace_seconds`；
- 可选的 `fallback_command`，以及是否预先授权终止目标进程。

只查看短命令输出或文件内容时无需调用本技能。

### 依赖与安装

安装本技能：

```bash
claude plugin marketplace add soia-team/soia-open-skills
```

```bash
claude plugin install soia-dev@soia
```

只要这一个技能时，可用 npx 路线。注意技能会落进共享真源 `~/.agents/skills`；若同时装了插件，同一技能会出现两份索引且各自漂移，建议二选一：

```bash
npx skills add soia-team/soia-open-dev-skills -g -a '*' -s soia-dev-terminal-ops -y
```

强依赖：POSIX shell、`ps`、`kill`。tmux 工作流要求 `tmux`。网络连接检查可选使用 `lsof`；缺少时标为“网络信号未检查”，不能据此判死锁。

可选配置：

```text
~/.config/soia-skills/soia-dev-terminal-ops/config.yml
SOIA_DEV_TERMINAL_OPS_CONFIG_FILE=<custom-config-path>
```

建议配置结构：

```yaml
schema_version: 2
env:
  TERMINAL_OPS_LOG_DIR: "<user-log-dir>"
  TERMINAL_OPS_SESSION_NAME: "<session-name>"
  TERMINAL_OPS_STALL_WINDOW_SECONDS: "<seconds>"
  TERMINAL_OPS_TERM_GRACE_SECONDS: "<seconds>"
  TERMINAL_OPS_FALLBACK_COMMAND: "<optional-command>"
```

优先级：本次用户输入/CLI 参数 → 进程环境 → 配置文件。未给日志目录时才使用 `${TMPDIR}`；若 `TMPDIR` 也未设置，先请用户指定目录。普通配置只能保存非秘密参数；命令包含 token 或其他秘密时必须改用 Provider 官方登录态、系统凭据库或安全的进程环境传递，不能写入配置或日志。

**WorkBuddy** 的装载单位是角色化专家而不是插件，`npx skills add -a '*'` 覆盖不到它，需要单独安装，见 [docs/install/workbuddy.md](https://github.com/soia-team/soia-open-skills/blob/main/docs/install/workbuddy.md)。

### 私密信息与中间数据

- 命令、环境、进程列表和日志可能暴露源码、路径、账号或秘密；执行前识别敏感参数，回执只显示脱敏后的命令与最小日志摘要。
- A 类运行日志写入客户指定目录；未指定时使用 `${TMPDIR}/soia-dev-terminal-ops/<session>/`。任务结束后默认清理本技能创建的临时日志，客户明确要求保留时除外。
- 高影响动作确需持久审计时，写入客户指定 state 根目录，或 `${XDG_STATE_HOME:-~/.local/state}/soia-skills/soia-dev-terminal-ops/`；只记录时间、目标标识、授权和结果，不记录环境变量、完整命令秘密或日志正文。
- 客户要求的诊断包是交付物，只写其指定路径；目标项目自身日志遵循项目规则。本技能不创建未声明的 cache 或 prompt/响应存档。
- B 类审计记录在客户确认保留策略前不自动删除；A 类临时数据只清理本技能创建且已复核目标的目录。

### 日志与完成回执

每次报告：

```markdown
完成：<启动、诊断、恢复或终止结果>。

日志摘要：
- command/workdir: <命令与目录>
- session/pid: <会话名或 PID>
- log: <日志路径或“纯 stdout”>
- signals: <日志/CPU/网络/子进程证据>
- status: running / suspected-stall / inconclusive / completed / terminated / killed

验证：<退出码、复查命令和最后输出摘要>
问题与下一步：<fallback 或待确认项；没有则写“无”>
```

## 触发条件

- 启动或监控预计运行超过 30 秒的命令；
- 管理 tmux 会话、后台 build/test 或持续日志；
- 诊断进程无输出、工具调用挂起或终端不可恢复；
- 在明确确认门下终止或降级长任务。

## 参数解析

在执行前解析并回显非秘密参数：

```sh
SESSION_NAME="${TERMINAL_OPS_SESSION_NAME:?set session name}"
LOG_DIR="${TERMINAL_OPS_LOG_DIR:-${TMPDIR:?set TERMINAL_OPS_LOG_DIR or TMPDIR}}"
STALL_WINDOW_SECONDS="${TERMINAL_OPS_STALL_WINDOW_SECONDS:?set observation window}"
TERM_GRACE_SECONDS="${TERMINAL_OPS_TERM_GRACE_SECONDS:?set TERM grace period}"
FALLBACK_COMMAND="${TERMINAL_OPS_FALLBACK_COMMAND:-}"
```

验证 session 名只含字母、数字、点、下划线或连字符；创建目录前展示解析后的绝对路径。不要把 agent 名、执行器状态、超时值或日志文件名写死在技能中。

## 命令风险分级

默认只读/幂等：

```sh
tmux list-sessions
ps -o pid,ppid,stat,etime,time,command -p <PID>
tail -n <LINES> <LOG_FILE>
lsof -nP -p <PID> -i  # 可选
```

高影响动作必须先说明目标、依据和数据风险，并获得用户确认（或引用本次请求中的明确预授权）：

- `kill -TERM <PID>`；
- `kill -KILL <PID>`；
- `tmux kill-session -t <SESSION_NAME>`；
- 执行 `FALLBACK_COMMAND`，因为它可能产生费用、远端状态或重复工作。

确认 PID 后再次读取完整命令与父 PID，避免 PID 复用或选错进程。不得用宽泛的 `pkill`/`killall` 代替精确 PID。

## 后台会话管理

日志名由调用者指定，不从产品名或 agent 名推导：

```sh
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/<log-name>.log"
tmux new-session -d -s "$SESSION_NAME" \
  "cd '<workdir>' && <command> 2>&1 | tee '$LOG_FILE'"
tmux list-sessions
tmux capture-pane -p -t "$SESSION_NAME" -S -50
tail -n 50 "$LOG_FILE"
```

命令、目录或路径含用户输入时，应使用宿主工具安全传参；不要直接拼接未经检查的 shell 片段。若必须运行复合命令，先把最终命令原样展示给用户。

## 多信号停滞诊断

`S` 只表示可中断睡眠，长时间处于 `S` 也可能是正常等待。elapsed time 或单一超时永远不是 kill 条件。

在 `STALL_WINDOW_SECONDS` 覆盖的至少两个采样点检查：

1. **日志进展**：日志 mtime、大小或最后一条业务进度是否变化；没有日志时明确记录缺口。
2. **CPU 进展**：累计 CPU time 是否增加；单次低 CPU 只说明当时空闲。
3. **网络/IPC 进展**：若任务依赖网络，检查连接是否存在、状态是否变化；`lsof` 不可用时不要伪造结论。
4. **子进程进展**：检查子进程是否仍在工作、退出或产生新输出。
5. **任务特定心跳**：测试数、构建目标、下载字节或队列计数等是否变化。

只有“观察窗口已超过阈值”并且至少两个独立进展信号持续无变化，且没有合理的正常等待解释时，才标为 `suspected-stall`。信号不足时标为 `inconclusive`，继续观察或请用户判断。

示例采样（命令在 macOS/Linux 上的列名可能略有差异，按实际输出解释）：

```sh
ps -o pid,ppid,stat,etime,time,command -p <PID>
wc -c < "$LOG_FILE"
tail -n 20 "$LOG_FILE"
lsof -nP -p <PID> -i 2>/dev/null || true
TARGET_PID=<PID>
ps -o pid,ppid,stat,etime,time,command -ax | awk -v p="$TARGET_PID" '$2 == p'
```

等待用户配置的观察窗口后重新采样并做差分。不要把“命令没有退出”误写成“没有进展”。

## 安全终止与恢复

1. 展示 PID、完整命令、父 PID、工作目录（能取得时）和多信号证据。
2. 说明 TERM 可能中断写入，KILL 不给清理机会；取得确认。
3. 发送 TERM。
4. 在 `TERM_GRACE_SECONDS` 内重复复查进程是否退出，并检查日志/落盘状态。
5. 若仍存活，展示复查证据和潜在数据损失，再次取得 KILL 确认。
6. 仅对同一已复核 PID 发送 KILL；随后确认进程消失、会话状态和输出完整性。
7. 如配置了 fallback，先说明上下文如何传递、是否会重复副作用和费用，再征得确认后执行。

```sh
kill -TERM <PID>
# 按 TERM_GRACE_SECONDS 轮询：
ps -p <PID> >/dev/null 2>&1 || echo "terminated"
# 仍存活且再次确认后：
kill -KILL <PID>
ps -p <PID> >/dev/null 2>&1 && echo "still alive" || echo "killed"
```

## 输出文件五分类

| 类别 | 本技能中的例子 | 落点 |
|---|---|---|
| A 临时 | 本轮 build/test 日志、采样快照 | 用户指定日志目录；否则 `${TMPDIR}/soia-dev-terminal-ops/<session>/` |
| B 审计 | kill、会话清理、fallback 等高影响动作记录 | 用户指定 state 目录或 `${XDG_STATE_HOME:-~/.local/state}/soia-skills/soia-dev-terminal-ops/`；未配置时先询问 |
| C 交付物 | 用户要求保留的完整诊断包 | 用户明确指定路径 |
| D 产品功能即日志 | 目标项目定义的任务日志 | 仅服从目标项目已记录的约定，不由本技能发明 |
| E 纯 stdout | 短状态检查、无需留存的摘要 | 不写磁盘 |

不得把相对 cwd 当默认日志目录。A 类可轮转；B 类在保留策略确认前不得删除。
