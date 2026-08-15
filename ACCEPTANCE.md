# ACCEPTANCE — chinese-naming-skill

| # | 驗收項 | 判準 | 狀態 | 證據 |
|---|--------|------|------|------|
| A1 | `analyze.py` 已知案例 | 王力宏、陳大明等 5 案例五格數值/三才與標準公式一致 | **PASS** | verify_a1.py 全 ✓（王力宏 5/6/9/13/8、陳大明 17/19/11/27/9、張三丰 12/14/7/18/5、歐陽娜娜 32/27/20/52/26、王力 5/6/3/6/2） |
| A2 | `suggest.py` 回灌 | 輸出組合逐一回灌 analyze.py 全為吉 | **PASS** | verify_a2.py：137 組合回灌，五格非吉 0、三才屬凶 0 |
| A3 | frontmatter 合規 | description ≤60 字元、name ≤64、無 platforms、全檔 ≤100k 字元 | **PASS** | verify_a3.py：13 項檢查全 ✓（desc 60 字元、name 合規、無 platforms、SKILL.md 3.5KB） |
| A4 | 安裝進索引 | `npx skills add` 成功 + lock.json 記錄 + 新 session 可見 | PENDING | |
| A5 | 發布 | GitHub public repo 存在、MIT、README/NOTICE 完整 | PENDING | |