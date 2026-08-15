# frontier — chinese-naming-skill

## 狀態：全部完成（t1–t10 done）

## 已完成
- [x] t1 讀 plan、環境確認、工作目錄、ACCEPTANCE.md、frontier.md
- [x] t2 上游資料下載到 /tmp/cns-scratch + 格式細讀
- [x] t3 轉換腳本 convert.py → 4 個 assets JSON（全部驗證）
  - strokes.json 50927 字（kangxi 46815 為主 + stoke 2219 補缺 + 簡體映射 1894）
  - wuxing.json 7013 字（20 衝突保留首見）
  - sancai.json 125 配置（sancai.txt 121 + PiPiName 補 4 缺）
  - shuli81.json 81 數理（大吉32/中吉14/凶35）
- [x] t4 analyze.py（A1 PASS：5 案例全數值正確）
- [x] t5 suggest.py（A2 PASS：137 組合回灌全吉）
- [x] t6 SKILL.md（description 恰 60 字元、無 platforms、A3 驗證全 ✓）
- [x] t7 references 兩檔 + README + LICENSE + NOTICE
- [x] t8 本地驗收 A1/A2/A3 全 PASS
- [x] t9 發布：git init → commit → `gh repo create royalskynet/chinese-naming-skill --public` → push
- [x] t10 本機安裝：`npx skills add ... --yes` 成功，lock.json 正常，`hermes skills list` 顯示 enabled

## 最終交付
- GitHub: https://github.com/royalskynet/chinese-naming-skill
- 本地安裝：`~/.hermes/skills/external/chinese-naming`（symlink）
- 技能名稱：`chinese-naming` (local, enabled)
- ACCEPTANCE: A1–A5 全 PASS