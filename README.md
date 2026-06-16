# 🔐 Agent Secret Skills — AI Agent 密钥管理

> **告别 .env 泄露，让任何 AI Agent 安全读取加密密钥。** AES-256-GCM 云端加密，一行命令解密。

[![Stars](https://img.shields.io/github/stars/webkubor/agent-secret-skills?style=social)](https://github.com/webkubor/agent-secret-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Works%20With-Any%20AI%20Agent-blue)]()
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

---

## 🔥 3 句话说明白

1. **API Key 硬编码在代码里 = 定时炸弹**
2. **Agent Secret Skills 把密钥加密存云端，Agent 一行命令解密读取**
3. **支持 20+ 种密钥类型，任何 Agent 框架都能用**

---

## ⚡ 30 秒接入

```bash
# 1. 安装 CortexOS CLI
brew install webkubor/cortexos/cs

# 2. 设置 Agent Token
export AGENT_TOKEN="***"

# 3. 读取密钥
cs secrets get secret://github/personal-pat
```

---

## 🛡️ 安全架构

```
Agent (你的电脑)              Cloudflare D1 (云端)
     │                              │
     ├── cs secrets get ──────────► │
     │   (Bearer Token 鉴权)        │ ← 只存 AES-256-GCM 密文
     │                              │ ← master key 分离存储
     │ ◄──────── 解密后的明文 ────── │ ← 传输全程 TLS 1.3
     │                              │
     ▼                              
   安全使用密钥                      
   用完即弃，不落盘                   
```

---

## 🎯 适用场景

| 谁 | 痛点 | 本 Skill 解决 |
|----|------|-------------|
| 🧑‍💻 Agent 开发者 | 密钥散落各处，.env 不安全 | 统一加密管理，一行命令读 |
| 🏢 团队 | 共享密钥靠复制粘贴 | Agent Token 权限管理，即时生效 |
| 🔒 安全敏感项目 | 密钥泄露 = 灾难 | AES-256-GCM，只存密文 |

---

## 📦 支持的密钥类型

GitHub PAT · GitLab Token · Cloudflare API · DeepSeek · 智谱 · 火山引擎 · 飞书 · Jenkins · SSH Key · 自定义

---

## 🧩 兼容

OpenClaw · Claude Code · Cursor · Codex · OpenCode · 任何能调 HTTP 的 Agent

---

## ⚠️ 与 .env 的区别

| | .env | Agent Secret Skills |
|--|------|---------------------|
| 加密 | ❌ 明文 | ✅ AES-256-GCM |
| 多 Agent 共享 | ❌ 需要手动复制 | ✅ 统一 Token 鉴权 |
| 泄露风险 | 🔴 一次 git push 就完 | 🟢 密文 + Token 分离 |
| 方便程度 | 读文件 | 一行 `cs secrets get` |

---

Built with 🔐 by [webkubor](https://github.com/webkubor) · Powered by [CortexOS](https://github.com/webkubor/CortexOS)
