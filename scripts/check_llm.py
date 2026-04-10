#!/usr/bin/env python3
"""One-shot LLM connectivity check (same endpoint as app/services/ai_service.py)."""

import asyncio
import json
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL  # noqa: E402


async def main() -> int:
    if not LLM_API_KEY or not LLM_API_KEY.strip():
        env_path = ROOT / ".env"
        hint = ""
        if env_path.is_file():
            raw = env_path.read_text(encoding="utf-8")
            for line in raw.splitlines():
                if line.strip().startswith("LLM_API_KEY="):
                    val = line.split("=", 1)[-1].strip()
                    if not val:
                        hint = "\n提示：.env 里有一行 LLM_API_KEY=，但等号后面是空的——请在编辑器里填好密钥后按 Cmd+S 保存，再重跑本脚本。"
                    break
        print(
            "未配置 LLM_API_KEY：请在项目根目录的 .env 里填写，或 export LLM_API_KEY=..."
            + hint
        )
        return 1

    url = f"{LLM_BASE_URL.rstrip('/')}/chat/completions"
    print(f"请求: {url}")
    print(f"模型: {LLM_MODEL}")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                url,
                headers={"Authorization": f"Bearer {LLM_API_KEY}"},
                json={
                    "model": LLM_MODEL,
                    "messages": [
                        {"role": "user", "content": "只回复一个字：好"},
                    ],
                    "max_tokens": 8,
                },
            )
    except httpx.RequestError as e:
        print(f"网络错误: {e}")
        return 2

    if resp.status_code != 200:
        print(f"HTTP {resp.status_code}: {resp.text[:500]}")
        return 3

    try:
        data = resp.json()
        text = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"响应解析失败: {e}\n原始: {resp.text[:500]}")
        return 4

    print("连接成功，模型回复片段:", repr(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
