# 🔐 Agent Skills

> **AI Agent 基础设施工具集。**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📦 Packages

| Package | Description | Install |
|---------|-------------|---------|
| **[d1-secret-vault](./d1-secret-vault)** | 零配置加密密钥管理 — AES-256-GCM + Cloudflare D1 | `pip install cryptography` |
| **[vite-plugin-agent-eyes](./agent-eyes)** | Vite 自愈遥测层 — 结构化日志 + Cookie 修复，让 agent 自我诊断 | `pnpm add -D vite-plugin-agent-eyes` |

---

## 🔐 Agent Secret Vault

> **Zero-config encrypted secret management for AI agents.**
> 一行命令解密密钥，任何 AI Agent 都能用的加密密钥库。

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Agent-lightgrey.svg)]()

---

## ✨ Why Agent Secret Vault?

AI agents need API keys. Hardcoding them is dangerous. `.env` files get scattered across machines. 1Password isn't agent-friendly.

**Agent Secret Vault** solves this with:

- 🔒 **AES-256-GCM encryption** — keys encrypted at rest in Cloudflare D1
- 🤖 **Agent-native** — authenticate with a bearer token, no browser, no OAuth dance
- 🌐 **HTTP API** — works from any language (Python / Node.js / Go / curl)
- 📦 **Zero dependencies beyond Python stdlib** — just `pip install cryptography`
- 🚀 **3 commands to start** — `clone → pip install → get`

---

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/webkubor/agent-secret-skills.git
cd agent-secret-skills

# 2. Install (only cryptography needed)
pip install cryptography

# 3. Set your agent token
export AGENT_TOKEN="af_xxx..."

# 4. Read a secret
python3 d1-secret-vault/scripts/secretvault.py get secret://cloudflare/api-token
```

---

## 📋 Commands

| Command | Description |
|---------|-------------|
| `list` | List all available secret references (no values) |
| `get <ref>` | Decrypt and return a secret value |
| `put <ref> <value> --kind "API Key"` | Store a new encrypted secret |
| `del <ref>` | Delete a secret |

---

## 🏗️ Architecture

```
Agent (Bearer Token)
    ↓ HTTPS
api.webkubor.online/content/secrets/
    ↓ D1 Query
Cloudflare D1 (cortexos-brain-db)
    ├── secret_vault   → AES-256-GCM ciphertext
    └── site_config    → master encryption key
```

**Encryption flow**: Agent sends request → API decrypts with master key → returns plaintext → Agent uses key → key never touches agent's disk

---

## 🔑 Authentication

Each agent gets a unique bearer token (`af_` prefix). All operations are authenticated and rate-limited.

To get a token:
- **Team agents**: Contact your team admin
- **External contributors**: Open an issue to request access
- **Self-hosted**: Deploy your own instance (see [Self-Hosting](#self-hosting))

---

## 🛡️ Security

- **Encryption**: AES-256-GCM with random IV per secret
- **Transport**: HTTPS only (TLS 1.3)
- **Key separation**: Master key stored separately from ciphertext
- **No key logging**: Values never appear in server logs
- **Audit trail**: All access logged with agent ID + timestamp

---

## 📦 Use Cases

```python
# Python agent
import os, json, urllib.request

def get_secret(ref):
    req = urllib.request.Request(
        f"https://api.webkubor.online/content/secrets/{ref.replace('secret://','')}?key=***",
        headers={"Authorization": f"Bearer {os.environ['AGENT_TOKEN']}"}
    )
    return json.loads(urllib.request.urlopen(req).read())["value"]

deepseek_key = get_secret("secret://deepseek/api-key")
```

```javascript
// Node.js agent
async function getSecret(ref) {
  const res = await fetch(
    `https://api.webkubor.online/content/secrets/${ref.replace('secret://','')}?key=***`,
    { headers: { Authorization: `Bearer ${process.env.AGENT_TOKEN}` } }
  );
  return (await res.json()).value;
}

const ghToken = await getSecret('secret://github/personal-pat');
```

```bash
# Shell / curl
curl -s "https://api.webkubor.online/content/secrets/deepseek/api-key?key=***" \
  -H "Authorization: Bearer $AGENT_TOKEN" | jq -r '.value'
```

---

## 🚀 Self-Hosting

```bash
# Deploy to Cloudflare Workers + D1
npx wrangler d1 create agent-secrets-db
npx wrangler secret put MASTER_KEY
npx wrangler deploy
```

Full self-hosting guide: [docs/SELF_HOSTING.md](docs/SELF_HOSTING.md)

---

## 👁️ Agent Eyes (vite-plugin-agent-eyes)

> **给 AI agent 的自愈遥测层。** 结构化运行时日志 + 本地 Cookie 修复，让 agent 自我诊断、自我修复。

### 安装

```bash
pnpm add -D vite-plugin-agent-eyes
```

### 用法

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import { agentDebugger, agentProxy } from 'vite-plugin-agent-eyes'

export default defineConfig({
  plugins: [agentDebugger()],
  server: {
    proxy: {
      '/api': agentProxy('https://your-api.example.com'),
    },
  },
})
```

```ts
// main.ts — 客户端错误捕获
import { installAgentErrorReporter } from 'vite-plugin-agent-eyes/client'
installAgentErrorReporter()
```

### 三类日志

| 文件 | 内容 |
|------|------|
| `api-calls.log` | 全部 API 调用 + 请求/响应体 |
| `errors.log` | API 失败 + 前端运行时错误 |
| `proxy.log` | 代理层 Cookie / Set-Cookie / status |

详见 [agent-eyes/README.md](./agent-eyes/README.md)

---

## 🤝 Contributing

PRs welcome! Areas to contribute:
- Language SDKs (Go, Rust, TypeScript)
- CLI improvements
- Self-hosting docs
- Security audits

---

## 👥 Team

Created by [webkubor](https://github.com/webkubor) as part of the CortexOS agent fleet infrastructure.

---

## ⭐ Star History

If this project helps your agent manage secrets securely, give it a ⭐!
