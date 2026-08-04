# DeepCode CLI 执行规范 / DeepCode CLI rules

> 目标命令是 `deepcode`，对应社区项目 `lessweb/deepcode-cli` / npm 包
> `@vegamo/deepcode-cli`。不要把它与 HKUDS、Snyk 或其他同名产品混用。

## 当前支持边界

- 已核对本机 `deepcode --version` 与 `deepcode --help`，确认支持 `-p/--prompt` 非交互入口。
- DeepCode 的模型、API 地址和 API key 由 provider 配置管理，默认位置是
  `~/.deepcode/settings.json`；本技能不读取或写入 key。
- 当前只提供**显式派发模板**，不加入自动路由。
- 当前没有稳定的结构化模型回显、Token 或费用证据，结果不得伪报为 Model Integrity Gate 已验证。

## 派发模板

```bash
command -v deepcode >/dev/null || { echo "CLI missing: deepcode" >&2; exit 9; }
deepcode --version
cd <project-path>
deepcode -p "$(< "${PROMPT_FILE}")"
```

`PROMPT_FILE` 应是按 task-id 隔离的 UTF-8 文件；不要把长 prompt 直接拼进未转义的 shell 字符串。

## 适用任务

适合显式派发：

- DeepSeek 生态下的代码解释
- 小范围编码建议和测试建议
- 代码库问答与计划草稿
- 需要 DeepCode 原生 skills 的任务

不适合作为当前自动路由候选：

- 复杂多文件修改
- 删除、覆盖、发布等高风险动作
- 需要精确模型回显、Token、成本或降级证据的 benchmark

## 配置与安全

DeepCode 的 provider 配置属于 provider-owned 配置，不是本技能的 `config.yml`：

```json
{
  "env": {
    "MODEL": "deepseek-v4-pro",
    "BASE_URL": "https://api.deepseek.com",
    "API_KEY": "<仅在本机填写>"
  }
}
```

示例中的 key 只能由客户在本机填写；不得提交项目内 `.deepcode/settings.json`，也不得把 key、账号、响应正文写进回执或日志。

## 验收

至少记录：

- `deepcode --version` 的版本
- 认证状态：已验证 / 未配置 / 被阻塞（不记录 key）
- 退出码与任务状态
- 模型、Token、费用证据：当前写 `unavailable`，除非 CLI 输出可独立核验的结构化证据
