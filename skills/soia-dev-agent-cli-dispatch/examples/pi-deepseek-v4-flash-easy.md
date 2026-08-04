# Pi + DeepSeek V4 Flash：easy 派发实例

这是一个可复用的公开实例，不包含真实项目路径、prompt、账号或响应正文。

## 适用任务

- 小范围 bug 修复
- 简单脚本或配置修改
- 测试、lint、格式化
- 摘要、分类、提取、翻译

不用于删除、覆盖、发布、安全边界变更或复杂架构决策。

## 1. 准备 prompt 文件

```bash
prompt_file="${TMPDIR:-/tmp}/soia-dev-agent-cli-dispatch/<task-id>/prompt.txt"
mkdir -p "$(dirname "$prompt_file")"
cat > "$prompt_file" <<'PROMPT_EOF'
请在当前工作目录完成一个小范围、可回退的编码任务：
1. 先读取相关文件；
2. 只做必要修改；
3. 运行最窄的相关测试；
4. 回报修改文件、测试命令和结果。
PROMPT_EOF
```

## 2. 自动路由

```bash
python3 scripts/route_model.py \
  --executor pi \
  --complexity easy
```

当前已验证的自动路由结果是：

```text
selected_model: deepseek-v4-flash
selected_reasoning_effort: low
selection_status: verified_auto
```

## 3. 结构化派发

```bash
command -v pi >/dev/null || exit 9
pi -p --mode json --no-session \
  --provider deepseek \
  --model deepseek-v4-flash \
  --thinking low \
  "@$prompt_file"
```

## 4. 验收重点

不能只看退出码。必须从最终 assistant `message_end` 核对：

- `provider=deepseek`
- `model=deepseek-v4-flash`
- `usage.input`
- `usage.cacheRead`
- `usage.cacheWrite`
- `usage.output`
- `usage.totalTokens`
- `usage.cost.total`

文本模式没有模型回显证据时，结果必须标记为
`actual_model_unverified`；不能报告成已验证成功。

## 证据边界

该实例只证明 Pi + DeepSeek V4 Flash 的 easy/low 调用链、模型回显和 usage 解析可用，
不证明 V4 Flash 的复杂任务质量，也不开放 medium/hard 或 V4 Pro 自动路由。
