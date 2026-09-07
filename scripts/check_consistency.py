#!/usr/bin/env python3
"""12 張圖卡一致性檢查。

核對 cards.json、templates/、tasks/ 與完整指南四份來源是否一致：
  - 12 張卡，每張 8 步驟
  - cards.json 的 fields 與 templates/NN-input.csv 表頭逐字相符
  - 每份 tasks/NN-task.md 含 goal / pilot / failure / 8 步驟標題 / 對應模板路徑
  - 完整指南含每張卡的 goal 與 8 步驟標題

用法：
  python scripts/check_consistency.py            # 一致性檢查
  python scripts/check_consistency.py --links    # 另外檢查官方文件連結（需連網）
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GUIDE = ROOT / "企業Agent_12張完整文案與實作指南.md"

errors: list[str] = []


def check() -> None:
    cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
    guide = GUIDE.read_text(encoding="utf-8")

    if len(cards) != 12:
        errors.append(f"cards.json 應有 12 張，實際 {len(cards)}")

    seen_ids = set()
    for card in cards:
        cid = card["id"]
        if cid in seen_ids:
            errors.append(f"卡片 id 重複：{cid}")
        seen_ids.add(cid)
        where = f"卡 {cid}"

        steps = card.get("steps", [])
        if len(steps) != 8:
            errors.append(f"{where}：步驟應為 8，實際 {len(steps)}")

        tmpl = ROOT / "templates" / f"{cid}-input.csv"
        if not tmpl.exists():
            errors.append(f"{where}：缺少 templates/{cid}-input.csv")
        else:
            header = tmpl.read_text(encoding="utf-8-sig").splitlines()[0].strip()
            if header != card["fields"]:
                errors.append(
                    f"{where}：模板表頭與 cards.json fields 不符\n"
                    f"  cards.json: {card['fields']}\n"
                    f"  template  : {header}"
                )

        task_path = ROOT / "tasks" / f"{cid}-task.md"
        if not task_path.exists():
            errors.append(f"{where}：缺少 tasks/{cid}-task.md")
            continue
        task = task_path.read_text(encoding="utf-8")
        for key in ("goal", "pilot", "failure"):
            if card[key] not in task:
                errors.append(f"{where}：任務書缺少 {key} 內容")
        if f"templates/{cid}-input.csv" not in task:
            errors.append(f"{where}：任務書未指向 templates/{cid}-input.csv")
        for step in steps:
            if step["title"] not in task:
                errors.append(f"{where}：任務書缺少步驟「{step['title']}」")

        if card["goal"] not in guide:
            errors.append(f"{where}：完整指南缺少 goal 內容")
        for step in steps:
            if step["title"] not in guide:
                errors.append(f"{where}：完整指南缺少步驟「{step['title']}」")


def check_links() -> None:
    import urllib.request

    guide = GUIDE.read_text(encoding="utf-8")
    urls = sorted(set(re.findall(r"\]\((https?://[^)]+)\)", guide)))
    for url in urls:
        try:
            req = urllib.request.Request(
                url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=25) as resp:
                code = resp.status
        except Exception as exc:  # noqa: BLE001
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req, timeout=25) as resp:
                    code = resp.status
            except Exception as exc2:  # noqa: BLE001
                errors.append(f"連結無法存取：{url}（{exc2 or exc}）")
                continue
        if code >= 400:
            errors.append(f"連結回應 {code}：{url}")


if __name__ == "__main__":
    check()
    if "--links" in sys.argv:
        check_links()

    if errors:
        print("一致性檢查未通過：\n")
        for err in errors:
            print(f"  ✗ {err}")
        sys.exit(1)
    print("一致性檢查通過：12 張卡、96 步驟，cards.json / templates / tasks / 指南 相符。")
