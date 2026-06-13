#!/usr/bin/env python3
"""
D1 Secret Vault — 独立解密工具
不依赖 cs / CortexOS，任何 agent 都能用。

用法:
  python3 secretvault.py list
  python3 secretvault.py get secret://platform/name

环境变量（必需）:
  CF_API_TOKEN
  CF_ACCOUNT_ID

可选:
  D1_DB_ID（默认 cortexos-brain-db）
"""

import sys
import os
import json
import base64
import urllib.request
import urllib.error

D1_DB_ID = os.environ.get("D1_DB_ID", "a43038ff-8fe7-4aaa-b661-23238458456a")


def d1_query(sql, params=None):
    token = os.environ.get("CF_API_TOKEN")
    account = os.environ.get("CF_ACCOUNT_ID")
    if not token or not account:
        print("错误: 需要 CF_API_TOKEN 和 CF_ACCOUNT_ID 环境变量", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.cloudflare.com/client/v4/accounts/{account}/d1/database/{D1_DB_ID}/query"
    body = json.dumps({"sql": sql, "params": params or []}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"D1 API 错误 {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

    if not data.get("success"):
        print(f"D1 查询失败: {data.get('errors', [])}", file=sys.stderr)
        sys.exit(1)

    results = data.get("result", [{}])
    return results[0].get("results", []) if results else []


def decrypt(ciphertext_b64, nonce_b64, key):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    ciphertext = base64.b64decode(ciphertext_b64)
    nonce = base64.b64decode(nonce_b64)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()


def get_master_key():
    rows = d1_query(
        "SELECT value FROM site_config WHERE key = ?1 LIMIT 1",
        ["secret_vault_master_key"],
    )
    if not rows:
        print("错误: D1 中没有 master key", file=sys.stderr)
        sys.exit(1)
    encoded = (rows[0]["value"] or "").strip()
    key = base64.b64decode(encoded)
    if len(key) != 32:
        print(f"错误: master key 长度异常: {len(key)}", file=sys.stderr)
        sys.exit(1)
    return key


def cmd_list():
    rows = d1_query(
        "SELECT id, kind, platform, name, account, last4, length, updated_at "
        "FROM secret_vault ORDER BY platform, name"
    )
    if not rows:
        print("密钥库为空")
        return
    print(f"{'引用':<42} {'类型':<10} {'账号':<18} {'LAST4':<6} {'长度':<5} {'更新时间'}")
    print("=" * 100)
    for r in rows:
        print(
            f"{r['id']:<42} {r.get('kind', '') or '':<10} "
            f"{r.get('account', '') or '—':<18} {r.get('last4', '') or '':<6} "
            f"{r.get('length', 0):<5} {(r.get('updated_at', '') or '')[:19]}"
        )


def cmd_get(ref):
    if not ref.startswith("secret://"):
        print(f"错误: 引用格式错误，应为 secret://platform/name", file=sys.stderr)
        sys.exit(1)

    rows = d1_query(
        "SELECT ciphertext, nonce FROM secret_vault WHERE id = ?1 LIMIT 1",
        [ref],
    )
    if not rows:
        print(f"错误: 未找到密钥: {ref}", file=sys.stderr)
        sys.exit(1)

    key = get_master_key()
    plaintext = decrypt(rows[0]["ciphertext"], rows[0]["nonce"], key)
    print(plaintext)


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
    elif cmd in ("-h", "--help", "help"):
        print(__doc__.strip())
    else:
        print(f"未知命令: {cmd}，可用: list, get", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
