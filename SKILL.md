---
name: agent-secret-skills
version: 3.0.0
description: "加密密钥管理 — Agent 通过 cs secrets 安全读取/写入云端密钥，AES-256-GCM 加密。触发条件: 需要读取密钥、写入密钥、管理 API Token 时触发。触发词: 密钥、secret、token、API key、cs secrets、secret vault。"
license: MIT
author: webkubor
category: security
platforms: [linux, macos]
metadata:
  openclaw:
    tags: [security, secrets, encryption, vault]
    requires:
      env: [AGENT_TOKEN]
      bins: [cs]
---

# Agent Secret Skills

D1 加密密钥库 — 统一走 `cs secrets`（CortexOS，Go），唯一实现，所有 Agent 框架共用。

## 触发条件

- 用户说"查密钥"、"读取 secret"、"设置 token"
- 任何 Agent 需要 API key 时
- `cs secrets get|list|set` 调用

## 快速开始

```bash
# 安装 CortexOS
brew install webkubor/cortexos/cs

# 设置 agent token
export AGENT_TOKEN="***"

# 读取密钥
cs secrets get secret://platform/name

# 列出所有密钥（不显示明文）
cs secrets list

# 写入新密钥
cs secrets set --platform github --name personal-pat --value "***" --kind "API Key"
```

## 架构

```
Agent → cs secrets → HTTPS → api.webkubor.online/content/secrets → D1 cortexos-brain-db
```

- 加密: AES-256-GCM（客户端加解密，API 只存密文）
- 鉴权: Agent Bearer Token → D1 `agents.token_sha256` 查表
- 密钥类型: API Key / Password / Token / Certificate

## 环境要求

- `cs`（CortexOS）在 PATH 中
- `AGENT_TOKEN` 环境变量或 `~/.fleet-creds.json`

## 相关 Skills

- 无（本 Skill 是基础安全设施）
