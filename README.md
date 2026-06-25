# 🔐 Keyring — AI 时代密钥管理

> **你存一次，AI 永远看不到明文。**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com/webkubor/agent-secret-skills/releases)

---

## ⚡ 30 秒上手

```bash
# 安装
pip install keyring-cli

# 初始化
keyring init

# 存密钥
keyring set secret://github/my-pat "ghp_xxxxxxxxxxxx"

# 建别名（AI 只认识这个）
keyring alias set github_token secret://github/my-pat

# AI 用
keyring run --env GITHUB_TOKEN=github_token -- git push
```

**AI 看到的是 `github_token`，永远看不到 `ghp_xxx`。**

---

## 🎯 为什么需要 Keyring？

| 方案 | AI 能读明文？ | 安全性 |
|------|--------------|--------|
| `.env` 文件 | ✅ 能 | ❌ 危险 |
| 环境变量 | ✅ 能 | ⚠️ 有风险 |
| **Keyring** | **❌ 不能** | **✅ 安全** |

### 痛点

```
你: 帮我推代码到 GitHub
AI: 好的，我看到你的 token 是 ghp_abc123...（已泄露）
```

### 解决

```
你: 帮我推代码到 GitHub  
AI: keyring run --env GITHUB_TOKEN=github_token -- git push
    （只看到别名，看不到明文）
```

---

## 🔥 核心亮点

| 特性 | 说明 |
|------|------|
| 🔒 **AI 安全** | 别名注入，明文不暴露 |
| ⚡ **极速** | 纯本地，毫秒级响应 |
| 🎯 **精准** | 按平台/类型管理密钥 |
| 📦 **零依赖** | 只需 Python 3.10+ |
| 🔄 **兼容** | 支持 .env 导入 |

---

## 📖 使用指南

### 存密钥

```bash
# GitHub Token
keyring set secret://github/my-pat "ghp_xxx" --kind "Token"

# 数据库密码
keyring set secret://mysql/production "xxx" --kind "Password" --account "admin"

# SSH 密钥
keyring set secret://ssh/server "$(cat ~/.ssh/id_rsa)" --kind "SSH Key"
```

### 查密钥

```bash
# 列出所有
keyring list

# 按平台过滤
keyring list --platform github

# 查看平台统计
keyring platforms
```

### AI 集成

```bash
# 推代码
keyring run --env GITHUB_TOKEN=github_token -- git push

# 调 API
keyring run --env DEEPSEEK_API_KEY=deepseek_key -- python app.py

# 多个密钥
keyring run --env TOKEN1=alias1 --env TOKEN2=alias2 -- python script.py
```

### 从 .env 迁移

```bash
# 预览（不实际导入）
keyring import --file .env --dry-run

# 导入全部
keyring import --file .env

# 只导入 GitHub 相关
keyring import --file .env --prefix GITHUB_
```

---

## 🤖 AI Agent 集成

### Claude Code / Cursor / Copilot

AI 助手遇到需要 token 时：

```
用户: 帮我部署到 GitHub
AI:   我需要 GitHub Token。请运行：
      keyring set secret://github/my-pat "你的token" --kind "Token"
用户: （已设置）
AI:   keyring run --env GITHUB_TOKEN=github_token -- git push
```

### 自动化脚本

```bash
#!/bin/bash
# deploy.sh — AI 生成的部署脚本
keyring run --env GITHUB_TOKEN=github_token \
            --env DOCKER_PASSWORD=docker_pass \
            -- bash deploy.sh
```

---

## 📁 安全架构

```
~/.keyring/
├── master.key       # AES-256 密钥（chmod 600）
├── secrets.json     # 加密后的密钥（AES-256-GCM）
└── aliases.json     # 别名映射（纯文本）
```

- **加密算法**: AES-256-GCM（认证加密）
- **密钥派生**: SHA-256
- **存储**: 纯本地，零网络
- **权限**: master.key 仅所有者可读

---

## 📋 命令速查

| 命令 | 用途 | 示例 |
|------|------|------|
| `keyring init` | 初始化 | `keyring init` |
| `keyring wizard` | 交互向导 | `keyring wizard` |
| `keyring set` | 存密钥 | `keyring set secret://github/pat "ghp_xxx"` |
| `keyring get` | 读密钥 | `keyring get github_token` |
| `keyring delete` | 删密钥 | `keyring delete secret://github/pat` |
| `keyring list` | 列出所有 | `keyring list -p github` |
| `keyring platforms` | 平台统计 | `keyring platforms` |
| `keyring alias set` | 建别名 | `keyring alias set github_token secret://github/pat` |
| `keyring alias list` | 列别名 | `keyring alias list` |
| `keyring run` | 注入env | `keyring run --env X=alias -- cmd` |
| `keyring import` | 导入.env | `keyring import -f .env` |

---

## 🏆 对比

| 功能 | Keyring | .env | 1Password | Vault |
|------|---------|------|-----------|-------|
| AI 安全 | ✅ | ❌ | ✅ | ✅ |
| 本地存储 | ✅ | ✅ | ❌ | ❌ |
| 零依赖 | ✅ | ✅ | ❌ | ❌ |
| 免费开源 | ✅ | ✅ | ❌ | ⚠️ |
| 命令行 | ✅ | ✅ | ⚠️ | ⚠️ |
| 别名系统 | ✅ | ❌ | ✅ | ✅ |

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)。

```bash
# 开发环境
git clone https://github.com/webkubor/agent-secret-skills.git
cd agent-secret-skills
pip install -e .
pip install pytest
pytest
```

---

## 📄 许可证

[MIT License](LICENSE)

---

<p align="center">
  Built with 🔐 by <a href="https://github.com/webkubor">webkubor</a>
</p>
