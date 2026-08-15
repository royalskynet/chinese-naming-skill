# chinese-naming-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

五格三才姓名學 — Hermes Agent skill。以**康熙字典筆畫**為基準，
計算中文姓名的天/人/地/總/外五格、81 數理吉凶、三才配置吉凶與漢字五行。

**資料來源**：NanBox/PiPiName（筆畫）· JakLiao/GoodGoodName（五行/三才/81數理）· samsonhoi/kangxi-dictionary（康熙字典）

**技能類型**：Hermes Agent skill（純 stdlib Python + JSON 資料，無套件依賴）

## 安裝

```bash
npx skills add https://github.com/royalskynet/chinese-naming-skill --skill chinese-naming
```

安裝後**開新 session** 才會進索引生效。

## 使用

### 分析姓名

```bash
cd ~/.hermes/skills/chinese-naming/
python3 scripts/analyze.py 王小明
```

輸出 JSON：各字筆畫與五行、五格數值與 81 數理吉凶、三才配置吉凶與斷語。

### 取名建議

```bash
python3 scripts/suggest.py 王 --wuxing 水木 --limit 5
```

枚舉筆畫組合 → 過濾三才吉、五格吉 → 輸出候選字。

也支援複姓（歐陽、司馬、上官、諸葛…）：

```bash
python3 scripts/analyze.py 歐陽娜娜
python3 scripts/suggest.py 歐陽 --chars 2
```

### 在 Hermes session 中使用

SKILL.md 會自動進索引。裝好後在對話中輸入「分析 王小明」或「幫王姓取名」等
觸發此 skill。

## 專案結構

```
chinese-naming-skill/
├── README.md                # 本檔案
├── LICENSE                  # MIT
├── NOTICE.md                # 上游 MIT 專案 attribution
└── chinese-naming/          # Hermes skill 根目錄
    ├── SKILL.md
    ├── scripts/
    │   ├── analyze.py       # 姓名五格分析
    │   └── suggest.py       # 取名建議
    ├── assets/
    │   ├── strokes.json     # 康熙筆畫字典（50,927 字）
    │   ├── wuxing.json      # 漢字五行（7,013 字）
    │   ├── sancai.json      # 三才配置吉凶（125 配置）
    │   └── shuli81.json     # 81 數理吉凶表
    └── references/
        ├── wuge-rules.md    # 五格計算規則
        └── interpretation.md # 吉凶斷語解讀指南
```

## 方法論

- **筆畫**：康熙字典為首（部首偏旁還原計算，與現代筆畫不同），PiPiName stoke.dat 補缺
- **五行**：GoodGoodName 漢字五行表（筆畫+五行雙鍵驗證）
- **三才**：GoodGoodName sancai.txt（121 配置），PiPiName wuge.py 補 4 缺配置
- **81 數理**：GoodGoodName constants.py 分類（大吉/中吉/凶 + 特質標籤）
- **五格公式**：GoodGoodName/PiPiName 共用公式（詳見 references/wuge-rules.md）

## 驗收狀態

| 項目 | 結果 |
|---|---|
| 五格數值（5 已知案例） | ✓ 全數值正確 |
| suggest 回灌 analyze | ✓ 137 組合全吉 |
| SKILL.md frontmatter 驗證 | ✓ description 60 字元 / ±100k / name 合規 |

## License

MIT。上游資料來源的 License 見 NOTICE.md。