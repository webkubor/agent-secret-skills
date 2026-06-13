# Agent Secret Skills

Agent 共享密钥工具。公开仓库，任何 agent 都能用。

## 完整流程（从零到拿到密钥）

```bash
# ── ① 拉工具 ──
git clone https://github.com/webkubor/agent-secret-skills.git
cd agent-secret-skills
pip install cryptography -q

# ── ② 拿到 CF API Token（以下三选一）──
#
# 方式 A：你的 agent 注册时已经配好了，直接用
export CF_API_TOKEN="cfat_xxx"
#
# 方式 B：问管理员要（南烛/小楠）
#
# 方式 C：你已有 Cloudflare 账号权限，自己生成
# https://dash.cloudflare.com/profile/api-tokens

# Account ID 是固定的（团队共用）
export CF_ACCOUNT_ID="916ebb1b9f240bf4c8826021dd161692"

# ── ③ 查密钥 ──
python3 d1-secret-vault/scripts/secretvault.py list                    # 看有哪些
python3 d1-secret-vault/scripts/secretvault.py get secret://gitlab/personal-pat  # 解密读取
```

## 可用密钥

| 引用 | 用途 |
|------|------|
| `secret://feishu/nanzhu-token` | 南烛 |
| `secret://feishu/xiaonan-token` | 小楠 |
| `secret://feishu/guqiuyue-token` | 顾栖月 |
| `secret://feishu/xiaowei-token` | 小薇 |
| `secret://gitlab/personal-pat` | GitLab PAT |
| `secret://gitlab-modelgo/personal-pat` | GitLab ModelGo |
| `secret://gitlab-paylinker/personal-pat` | GitLab Paylinker |
| `secret://github/personal-pat` | GitHub PAT |
| `secret://cloudflare/api-token` | Cloudflare |
| `secret://zhipu/api-key` | 智谱 GLM |
| `secret://deepseek/api-key` | DeepSeek |
| `secret://volcengine/ark-api-key` | 火山方舟 |

## 架构

```
git clone（公开） → CF_API_TOKEN（管理员给） → D1 解密 → 拿到密钥

D1 cortexos-brain-db
  ├── secret_vault 表 → AES-256-GCM 密文
  └── site_config 表 → master key（解密钥匙）
```

不需要 CortexOS，不需要 cs CLI，不需要私有仓库权限。
