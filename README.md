# 企業 AI to Agent 公開教學圖卡

[![一致性檢查](https://github.com/draiagent/AI-to-Agent-VAC-Task-12Cards/actions/workflows/consistency.yml/badge.svg?branch=main)](https://github.com/draiagent/AI-to-Agent-VAC-Task-12Cards/actions/workflows/consistency.yml)
[![授權: CC BY-SA 4.0](https://img.shields.io/badge/授權-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE)

AI Coach 益力康陳董｜2026 AI to Agent

用AI放大創意‧用Agent輕鬆執行

- 企業Agent_12張教學圖卡.pdf：12 頁固定版面，可直接教學。
- png/：12 張獨立圖卡，各 1800 × 2400 px。
- 企業Agent_12張圖卡.html：內嵌字體與品牌素材，可修改文字；列印時依瀏覽器調整。固定版面交付以 PDF／PNG 為準。
- 企業Agent_12張完整文案與實作指南.md：完整文案、工具分工、實作前提、錯誤修正與來源。
- tasks/：12 份可交給具工具能力 Agent 的任務書；不是已部署的程式或服務。
- templates/：12 份 UTF-8 CSV 輸入欄位骨架；填入資料並準備任務要求的附件後使用。
- cards.json：12 張卡的結構化內容。
- 企業Agent_12張總覽.jpg：整套預覽。

完成範圍：內容與工具能力查核、12 頁 PDF 與 PNG 版面檢查、輸入模板及任務書。
尚未執行：企業帳號串接、真實資料測試、12 項業務端到端驗收。

建議先挑一項任務，用提供的小型試作範圍跑通，再逐步擴大。不要把尚未驗證的方案或估計 ROI 當成已完成成果。

## 一致性檢查

`python scripts/check_consistency.py`：核對 cards.json、templates/、tasks/ 與完整指南四份來源是否一致（12 張卡、每張 8 步驟、模板表頭相符、任務書含步驟與模板路徑）。加 `--links` 另檢查官方文件連結。push 到 main 或開 PR 時由 GitHub Actions 自動執行。

## 授權

本教材（文件、圖卡、模板、任務書）以 [CC BY-SA 4.0](LICENSE) 釋出：可自由使用、修改與再散布，須標示出處並以相同條款分享。
署名：AI Coach 益力康陳董｜2026 AI to Agent。
