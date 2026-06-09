---
name: sjtuguoxue-relay
version: 1.0.0
description: |
  上海交通大学国学社 Claude Code 中转站配置。
  通过社团自建中转服务使用 Claude Code，当前免费不限量提供 MiniMax-M3 模型。
  当用户需要配置国学社中转、连接社团 Claude 服务、或提到"国学社中转"时触发。
---

# 国学社 Claude Code 中转站

上海交通大学国学社自建的 Claude Code API 中转服务，供社员免费使用。

## 当前可用模型

| 模型 | 标识 | 状态 |
|------|------|------|
| MiniMax-M3 | `MiniMax-M3[1m]` | 免费不限量 |

## 配置方法

### 1. 获取 API Key

中转服务需要专用 API Key，请向管理员申请：

- 联系国学社技术负责人，说明用途
- 获取形如 `sk-xxxx` 的 Token

### 2. 写入 Claude Code 配置

在 `~/.claude/settings.json`（全局）或项目 `.claude/settings.json` 中添加：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "<向管理员申请的 API Key>",
    "ANTHROPIC_CUSTOM_HEADERS": "X-Sub-Module: claude-code-internal",
    "ANTHROPIC_BASE_URL": "https://s.sjtuguoxue.space/",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M3[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M3[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M3[1m]",
    "ANTHROPIC_MODEL": "MiniMax-M3[1m]",
    "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS": "1"
  }
}
```

### 3. 快速配置（一键写入全局 settings）

如果你已经拿到 Key，可以让 Claude Code 帮你配置：

```
请帮我把国学社中转配置写入全局 settings，我的 Key 是 sk-xxxx
```

Claude Code 会使用 `/update-config` skill 自动写入 `~/.claude/settings.json`。

## 注意事项

- **API Key 不要提交到公开仓库**，仅写入本地 settings 文件
- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` 关闭实验性功能，避免中转不支持的 API 调用
- 中转服务地址 `https://s.sjtuguoxue.space/` 由国学社维护，如遇故障请联系管理员
- 模型可用性可能随时调整，以管理员通知为准

## 故障排查

| 症状 | 可能原因 | 解决方法 |
|------|---------|---------|
| `401 Unauthorized` | Key 无效或过期 | 联系管理员重新申请 |
| `Connection refused` | 中转服务暂不可用 | 等待恢复或联系管理员 |
| `Model not found` | 模型标识有误 | 检查是否为 `MiniMax-M3[1m]` |
| 响应异常缓慢 | 网络问题 | 检查校园网/VPN 连接 |
