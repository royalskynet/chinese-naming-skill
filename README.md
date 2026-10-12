# chinese-naming-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Quick install / 快速安裝

一行取得並立刻跑起來（從 GitHub clone ＋ 實際執行入口，repo 內無安裝腳本）：

```bash
git clone https://github.com/royalskynet/chinese-naming-skill && cd chinese-naming-skill && python3 chinese-naming/scripts/analyze.py 王小明
```

裝成 agent skill（需要 npm）：

```bash
npx skills add https://github.com/royalskynet/chinese-naming-skill --skill chinese-naming
```

安裝後請**開新 session**，skill 才會進索引生效。裝法與用法的完整說明見下方任一語言段落。

---

## English

**chinese-naming-skill** is a Hermes Agent skill for traditional Chinese name analysis, following the Five Grids and Three Talents school (五格三才姓名學). It counts every character with **Kangxi Dictionary** stroke standards — radicals are counted in their original form, so strokes often differ from modern counts — and reports the Heavenly, Human, Earthly, Total and External grids, the fortune of numbers 1 through 81, the Three Talents configuration, and the Five Elements of each character. Everything runs offline: pure standard-library Python plus JSON data files, with no third-party packages and no network access.

**Data sources**: NanBox/PiPiName (strokes) · JakLiao/GoodGoodName (Five Elements, Three Talents, 81 numerology) · samsonhoi/kangxi-dictionary (Kangxi Dictionary). Attribution for these MIT-licensed upstream projects is listed in `NOTICE.md`.

### Install

```bash
npx skills add https://github.com/royalskynet/chinese-naming-skill --skill chinese-naming
```

If you do not have npm, clone the repository and run the entry point directly:

```bash
git clone https://github.com/royalskynet/chinese-naming-skill
cd chinese-naming-skill
python3 chinese-naming/scripts/analyze.py 王小明
```

Open a new session after installing so the skill enters the index. In conversation, prompts such as "analyze 王小明" or "suggest a name for the surname 王" will trigger the skill through its `SKILL.md`.

### Analyze a name

```bash
cd ~/.hermes/skills/chinese-naming/
python3 scripts/analyze.py 王小明
```

The output is JSON: stroke counts and Five Elements for each character, the five grid values with their 1–81 numerology grades, and the Three Talents configuration with a written interpretation.

### Suggest names

```bash
python3 scripts/suggest.py 王 --wuxing 水木 --limit 5
```

The script enumerates stroke combinations for the given name characters, keeps only those whose grids and Three Talents are auspicious, and lists candidate characters for each surviving combination. Compound surnames (歐陽, 司馬, 上官, 諸葛 and others) are recognised automatically:

```bash
python3 scripts/analyze.py 歐陽娜娜
python3 scripts/suggest.py 歐陽 --chars 2
```

### Reading the output

Judge the Human, Earthly, Total and External grids by their 81 numerology grade; the Heavenly grid is fixed by the surname and is not judged. The Three Talents are read through the productive and controlling relations of the Five Elements. A single inauspicious grid does not make the whole name inauspicious — combine the four judged grids with the Three Talents before drawing a conclusion. Results are traditional numerology for reference only, not a scientific prediction.

### Project layout

```
chinese-naming-skill/
├── README.md                 # this file (English + 繁體中文)
├── LICENSE                   # MIT
├── NOTICE.md                 # upstream attribution
└── chinese-naming/           # Hermes skill root
    ├── SKILL.md
    ├── scripts/
    │   ├── analyze.py        # five-grid name analysis
    │   └── suggest.py        # name suggestions
    ├── assets/
    │   ├── strokes.json      # Kangxi stroke dictionary (50,927 characters)
    │   ├── wuxing.json       # Five Elements per character (7,013 characters)
    │   ├── sancai.json       # Three Talents configurations (125)
    │   └── shuli81.json      # 1–81 numerology table
    └── references/
        ├── wuge-rules.md     # five-grid formulas
        └── interpretation.md # how to read the interpretations
```

### Methodology

- **Strokes**: Kangxi Dictionary first (radicals restored to their original form), PiPiName `stoke.dat` fills the gaps.
- **Five Elements**: GoodGoodName character table, validated against both stroke count and element.
- **Three Talents**: GoodGoodName `sancai.txt` (121 configurations), PiPiName `wuge.py` adds the 4 missing ones.
- **81 numerology**: GoodGoodName `constants.py` classification (greatly auspicious / moderately auspicious / inauspicious, plus trait labels).
- **Grid formulas**: shared by GoodGoodName and PiPiName; see `references/wuge-rules.md`.

### Verification status

| Item | Result |
|---|---|
| Five-grid values (5 known names) | ✓ all values correct |
| suggest output fed back into analyze | ✓ 137 combinations all auspicious |
| SKILL.md frontmatter validation | ✓ description 60 chars / within ±100k / name compliant |

### License

MIT. Licenses of the upstream data sources are documented in `NOTICE.md`.

---

## 繁體中文

**chinese-naming-skill** 是一個 Hermes Agent skill，用來分析中文姓名，依據傳統的**五格三才姓名學**。它以**康熙字典筆畫**為基準（偏旁按原部首計算，因此常與現代筆畫不同），計算姓名的天格、人格、地格、總格、外格五格，查 1 至 81 的數理吉凶、三才配置吉凶與每個漢字的五行。全程離線執行：純標準函式庫的 Python 加上 JSON 資料檔，不需安裝任何第三方套件，也不需要網路。

**資料來源**：NanBox/PiPiName（筆畫）· JakLiao/GoodGoodName（五行／三才／81 數理）· samsonhoi/kangxi-dictionary（康熙字典）。這些 MIT 授權的上游專案之歸屬聲明列於 `NOTICE.md`。

### 安裝

```bash
npx skills add https://github.com/royalskynet/chinese-naming-skill --skill chinese-naming
```

沒有 npm 的話，直接 clone 本 repo 並執行入口腳本：

```bash
git clone https://github.com/royalskynet/chinese-naming-skill
cd chinese-naming-skill
python3 chinese-naming/scripts/analyze.py 王小明
```

安裝後**開新 session** 才會進索引生效。在對話中輸入「分析 王小明」或「幫王姓取名」等句子，就會觸發此 skill（透過 `SKILL.md`）。

### 分析姓名

```bash
cd ~/.hermes/skills/chinese-naming/
python3 scripts/analyze.py 王小明
```

輸出 JSON：各字的康熙筆畫與五行、五格數值與其 81 數理吉凶、三才配置吉凶與斷語全文。

### 取名建議

```bash
python3 scripts/suggest.py 王 --wuxing 水木 --limit 5
```

腳本枚舉名字兩字的筆畫組合，過濾掉五格或三才不吉的組合，只保留吉的組合並列出候選字（`--limit` 控制每組合候選數，`--wuxing` 只列出指定五行的字）。複姓（歐陽、司馬、上官、諸葛…等）由內建複姓表自動辨識：

```bash
python3 scripts/analyze.py 歐陽娜娜
python3 scripts/suggest.py 歐陽 --chars 2
```

### 輸出怎麼解讀

人格、地格、總格、外格看 81 數理吉凶；天格由姓氏先天決定，不列入吉凶判斷。三才則看五行生剋關係。任何單一格為凶，不必然代表整體為凶——應把四個受判的格與三才吉凶綜合判讀。此為傳統姓名學參考，非科學預測，結果僅供參考。

### 專案結構

```
chinese-naming-skill/
├── README.md                # 本檔案（English + 繁體中文）
├── LICENSE                  # MIT
├── NOTICE.md                # 上游專案歸屬聲明
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

### 方法論

- **筆畫**：以康熙字典為首（部首偏旁還原計算，與現代筆畫不同），PiPiName `stoke.dat` 補缺。
- **五行**：GoodGoodName 漢字五行表（筆畫＋五行雙鍵驗證）。
- **三才**：GoodGoodName `sancai.txt`（121 配置），PiPiName `wuge.py` 補 4 個缺配置。
- **81 數理**：GoodGoodName `constants.py` 分類（大吉／中吉／凶，並附特質標籤）。
- **五格公式**：GoodGoodName 與 PiPiName 共用公式，詳見 `references/wuge-rules.md`。

### 驗收狀態

| 項目 | 結果 |
|---|---|
| 五格數值（5 個已知案例） | ✓ 全數值正確 |
| suggest 回灌 analyze | ✓ 137 組合全吉 |
| SKILL.md frontmatter 驗證 | ✓ description 60 字元 / ±100k 內 / name 合規 |

### License

MIT。上游資料來源的 License 見 `NOTICE.md`。
