#!/usr/bin/env python3
"""
D1 Secret Vault — 加密密钥库客户端
只依赖 agent token + api.webkubor.online，不需要 CF API token。
任何 agent 都能用。

用法:
  python3 secretvault.py list                        # 列出所有密钥元信息
  python3 secretvault.py get secret://platform/name  # 解密读取密钥明文
  python3 secretvault.py put secret://platform/name <value> [--account X] [--kind Y]  # 加密存储密钥
  python3 secretvault.py del secret://platform/name  # 删除密钥

环境变量:
  AGENT_TOKEN   — agent 的 af_ token（必需）
  VAULT_API     — API 地址（默认 https://api.webkubor.online/content/secrets）
"""

import sys
import os
import json
import base64
import urllib.request
import urllib.error

API_BASE = os.environ.get(
    "VAULT_API", "https://api.webkubor.online/content/secrets"
)


# ─── API helpers ────────────────────────────────────────────

def api_request(path, agent_token, method="GET", data=None):
    """Call api.webkubor.online/content/secrets/<path>."""
    url = f"{API_BASE}/{path}" if path else API_BASE
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {agent_token}")
    req.add_header("User-Agent", "secretvault/2.0")
    if data:
        req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"API 错误 {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def decrypt(ciphertext_b64, nonce_b64, master_key_b64):
    """AES-256-GCM decrypt."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    key = base64.b64decode(master_key_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    nonce = base64.b64decode(nonce_b64)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()


def encrypt(plaintext, master_key_b64):
    """AES-256-GCM encrypt → (ciphertext_b64, nonce_b64)."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    key = base64.b64decode(master_key_b64)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return (
        base64.b64encode(ciphertext).decode(),
        base64.b64encode(nonce).decode(),
    )


def get_agent_token():
    token = os.environ.get("AGENT_TOKEN")
    if not token:
        print("错误: 需要 AGENT_TOKEN 环境变量（af_ 开头的 agent token）", file=sys.stderr)
        sys.exit(1)
    return token


def parse_ref(ref):
    """secret://platform/name → (platform, name)"""
    if not ref.startswith("secret://"):
        print("错误: 引用格式错误，应为 secret://platform/name", file=sys.stderr)
        sys.exit(1)
    path = ref[len("secret://"):]
    parts = path.split("/")
    if len(parts) != 2:
        print(f"错误: 引用格式错误: {ref}", file=sys.stderr)
        sys.exit(1)
    return parts[0], parts[1]


def get_master_key(token):
    """Fetch master key from API."""
    mk_data = api_request("master-key", token)
    if not mk_data.get("ok"):
        print("错误: 未找到 master key", file=sys.stderr)
        sys.exit(1)
    return mk_data["masterKey"]


# ─── Commands ───────────────────────────────────────────────

def cmd_list():
    token = get_agent_token()
    data = api_request("list", token)
    secrets = data.get("secrets", [])
    if not secrets:
        print("密钥库为空")
        return

    print(f"{'引用':<42} {'类型':<10} {'账号':<18} {'LAST4':<6} {'更新时间'}")
    print("=" * 100)
    for r in secrets:
        print(
            f"{r['id']:<42} {(r.get('kind') or ''):<10} "
            f"{r.get('account') or '—':<18} {(r.get('last4') or ''):<6} "
            f"{(r.get('updated_at') or '')[:19]}"
        )


def cmd_get(ref):
    token = get_agent_token()
    platform, name = parse_ref(ref)

    ct_data = api_request(f"{platform}/{name}", token)
    if not ct_data.get("ok"):
        print(f"错误: 未找到密钥: {ref}", file=sys.stderr)
        sys.exit(1)

    mk = get_master_key(token)
    plaintext = decrypt(ct_data["ciphertext"], ct_data["nonce"], mk)
    print(plaintext)


def cmd_put(ref, value, account=None, kind=None):
    token = get_agent_token()
    platform, name = parse_ref(ref)

    mk = get_master_key(token)
    ciphertext_b64, nonce_b64 = encrypt(value, mk)

    last4 = value[-4:] if len(value) >= 4 else value
    body = {
        "ciphertext": ciphertext_b64,
        "nonce": nonce_b64,
        "last4": last4,
        "length": len(value),
    }
    if account:
        body["account"] = account
    if kind:
        body["kind"] = kind

    result = api_request(f"{platform}/{name}", token, method="POST", data=body)
    if result.get("ok"):
        print(f"✓ 已存储 {ref} (last4={last4}, len={len(value)})")
    else:
        print(f"✗ 存储失败: {result}", file=sys.stderr)
        sys.exit(1)


def cmd_del(ref):
    token = get_agent_token()
    platform, name = parse_ref(ref)

    result = api_request(f"{platform}/{name}", token, method="DELETE")
    if result.get("ok"):
        print(f"✓ 已删除 {ref}")
    else:
        print(f"✗ 删除失败: {result}", file=sys.stderr)
        sys.exit(1)


# ─── CLI ────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        cmd_list()

    elif cmd == "get":
        if len(sys.argv) < 3:
            print("用法: python3 secretvault.py get secret://platform/name", file=sys.stderr)
            sys.exit(1)
        cmd_get(sys.argv[2])

    elif cmd == "put":
        if len(sys.argv) < 4:
            print("用法: python3 secretvault.py put secret://platform/name <value> [--account X] [--kind Y]", file=sys.stderr)
            sys.exit(1)
        ref = sys.argv[2]
        value = sys.argv[3]
        account = None
        kind = None
        for i in range(4, len(sys.argv) - 1):
            if sys.argv[i] == "--account":
                account = sys.argv[i + 1]
            elif sys.argv[i] == "--kind":
                kind = sys.argv[i + 1]
        cmd_put(ref, value, account=account, kind=kind)

    elif cmd in ("del", "delete", "rm"):
        if len(sys.argv) < 3:
            print("用法: python3 secretvault.py del secret://platform/name", file=sys.stderr)
            sys.exit(1)
        cmd_del(sys.argv[2])

    elif cmd in ("-h", "--help", "help"):
        print(__doc__.strip())

    else:
        print(f"未知命令: {cmd}，可用: list, get, put, del", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
