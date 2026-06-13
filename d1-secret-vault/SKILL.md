---
name: d1-secret-vault
description: "D1 加密密钥库 — 从 Cloudflare D1 解密读取密钥，不依赖任何私有仓库"
version: 1.0.0
---

# D1 Secret Vault

从 D1 `cortexos-brain-db` 加密密钥库解密读取密钥。纯 Python，零框架依赖。

## 前置条件

- 环境变量 `CF_API_TOKEN` 和 `CF_ACCOUNT_ID`
- Python 3 + `cryptography`（`pip install cryptography`）

## 用法

```bash
# 列出所有密钥元信息（不出明文）
python3 scripts/secretvault.py list

# 解密读取密钥明文
python3 scripts/secretvault.py get secret://platform/name
```

## 常用密钥

| 引用 | 用途 |
|------|------|
| `secret://feishu/nanzhu-token` | 南烛 |
| `secret://feishu/xiaonan-token` | 小楠 |
| `secret://feishu/guqiuyue-token` | 顾栖月 |
| `secret://feishu/xiaowei-token` | 小薇 |
| `secret://gitlab/personal-pat` | GitLab |
| `secret://github/personal-pat` | GitHub |
| `secret://cloudflare/api-token` | Cloudflare |
| `secret://zhipu/api-key` | 智谱 GLM |
| `secret://deepseek/api-key` | DeepSeek |

## 技术细节

- 加密：AES-256-GCM
- Master key：D1 `site_config` 表，key = `secret_vault_master_key`
- 密文表：D1 `secret_vault`
- D1 数据库：`cortexos-brain-db`（a43038ff-8fe7-4aaa-b661-23238458456a）
