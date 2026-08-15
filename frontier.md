# frontier — chinese-naming-skill

## 狀態：t1–t8 完成，待 t9 發布（guard 攔截即停）、t10 安裝實測

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
- [x] t6 SKILL.md（description 恰 60 字元、無 platforms、無 body/大小問題）
- [x] t7 references 兩檔 + README + LICENSE + NOTICE
- [x] t8 本地驗收 A1/A2/A3 全 PASS

## 下一步
1. t9 發布：git init + commit + gh repo create royalskynet/chinese-naming-skill --public + push（guard 攔截即停）
2. t10 本機安裝：npx skills add https://github.com/royalskynet/chinese-naming-skill --skill chinese-naming + 確認 verdict/lock.json

## 已知事項
- 五格公式（GoodGoodName/PiPiName 一致）：天=姓+1, 人=姓+名1, 地=名1+名2, 總=姓+名1+名2, 外=總-人+1；單名外格=2
- 五行判定：尾數 1/2木、3/4火、5/6土、7/8金、9/0水
- 81 數理 grade：jixiang=大吉、xiaoji=中吉、xiong=凶（constants.py regex 解析）
- git push 不含 workflow 檔（token 缺 workflow scope）
- A1 初版 FAIL 是驗證腳本期望值錯誤（丰=4 畫非 5），非實作問題