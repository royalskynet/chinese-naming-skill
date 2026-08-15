---
name: chinese-naming
description: Use when analyzing or suggesting Chinese names (五格/三才/康熙筆畫).
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [chinese, naming, 姓名學, 五格, 三才, kangxi, 康熙筆畫, wuge, 起名]
---

# chinese-naming — 五格三才姓名學

分析或建議中文姓名，以**康熙字典筆畫**為基準計算五格（天/人/地/總/外），
查 81 數理吉凶、三才配置吉凶與漢字五行。資料與腳本 100% 本地（assets + stdlib Python），
無網路需求、無第三方套件。

## 何時用哪支腳本

| 需求 | 指令 | 輸出 |
|---|---|---|
| 分析一個姓名 | `python3 scripts/analyze.py <姓名>` | JSON：各字筆畫與五行、五格數值與 81 數理吉凶、三才配置吉凶與斷語 |
| 為姓氏找吉利名字 | `python3 scripts/suggest.py <姓> [--wuxing 水木] [--limit N]` | JSON：符合三才/五格條件的筆畫組合 + 每組合候選字 |

例：

```bash
python3 scripts/analyze.py 王小明
python3 scripts/suggest.py 王 --wuxing 水木 --limit 5
python3 scripts/suggest.py 歐陽 --chars 2
```

複姓（歐陽、司馬、上官、諸葛…）由內建複姓表自動辨識；3 字名自動拆「單姓+雙名」，
4 字名自動拆「複姓+雙名」。名字查不到康熙筆畫會明確報錯（不靜默）。

## 輸出怎麼解讀

### analyze.py 關鍵欄位

- `char_strokes`：各字康熙筆畫（例：`"王": 4`、`"明": 8`，與現代筆畫可能不同——康熙含部首補正，如氵算 4 畫、艹算 6 畫）。
- `ge.天格/人格/地格/總格/外格`：每格有 `value`（筆畫數）、`wuxing`（該數五行，尾數 1/2木 3/4火 5/6土 7/8金 9/0水）、`shuli_grade`（大吉/中吉/凶/平）、`shuli_traits`（該數理特質標籤，如首領運、財富運）。
- `sancai.config`：天+人+地三格五行組合；`sancai.result`：吉凶（大吉/中吉/吉/凶多于吉/…）；`sancai.evaluate`：斷語全文。

**判斷口訣**：人格、地格、總格、外格看 81 數理；天格不動（姓氏先天）。三才看五行生剋。
任何單格凶不必然全盤凶——以人/地/總/外 四格吉凶與三才吉凶綜合敘述，不要只報一個欄位。

### suggest.py 輸出

- `results[].strokes`：名兩字筆畫（康熙）；`ge`：五格數值；`sancai`/`sancai_result`：三才組合與吉凶。
- `results[].mid_candidates` / `last_candidates`：該筆畫的候選字（依 `--limit` 截斷；指定 `--wuxing` 時只列該五行字）。
- results 依三才吉凶排序（大吉最前）。

### 使用注意

- 資料範圍：康熙 50,927 字 + 五行 7,013 字 + 三才 125 配置 + 81 數理全表。
- 判斷為傳統姓名學參考，非科學預測；中介回覆時加一句「結果僅供參考」。
- 建議輸出名單後可自選候選字組合，用 analyze.py 逐名複驗（suggest 已內建吉過濾，回灌應全吉）。

## 方法論與資料來源

- 五格公式：天=姓+1、人=姓+名1、地=名1+名2、總=姓+名1+名2、外=總-人+1；複姓與單名規則見 `references/wuge-rules.md`。
- 筆畫：康熙字典（`samsonhoi/kangxi-dictionary`），stoke.dat（`NanBox/PiPiName`）補缺。
- 五行：`JakLiao/GoodGoodName` full_wuxing_dict；三才表：GoodGoodName sancai.txt（PiPiName wuge.py 補 4 缺配置）。
- 81 數理：GoodGoodName constants.py 分類（大吉/中吉/凶 + 特質標籤）。
- 上游全為 MIT；attribution 見 NOTICE.md。詳見 `references/interpretation.md` 與 `references/wuge-rules.md`。