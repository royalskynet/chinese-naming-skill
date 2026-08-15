#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chinese-naming suggest.py — 取名建議（筆畫組合 + 三才/五格吉過濾 + 候選字）

CLI:  python3 suggest.py 王
      python3 suggest.py 王 --wuxing 水木
      python3 suggest.py 歐陽 --limit 5

流程：
  1. 枚舉名兩字康熙筆畫組合 (a, b)，a/b ∈ 1..40
  2. 以姓氏算五格；人格/地格/總格/外格 81 數理須為吉（大吉或中吉）
  3. 三才配置 result 不得屬凶（大凶/凶/凶多于吉/凶多吉少）
  4. 依筆畫查候選字（可選 --wuxing 過濾名兩字五行）
輸出 JSON 陣列（組合 + 三才 + 每格數值 + 候選字，每組合候選上限 --limit）
"""
import argparse
import json
import os

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')

BAD_SANCAI = {'大凶', '凶', '凶多于吉', '凶多吉少'}
GOOD_GRADE = {'大吉', '中吉'}
STROKE_RANGE = range(1, 41)


def load_assets():
    with open(os.path.join(ASSETS, 'strokes.json'), encoding='utf-8') as f:
        strokes = json.load(f)['strokes']
    with open(os.path.join(ASSETS, 'wuxing.json'), encoding='utf-8') as f:
        wuxing = json.load(f)['wuxing']
    with open(os.path.join(ASSETS, 'sancai.json'), encoding='utf-8') as f:
        sancai = json.load(f)['sancai']
    with open(os.path.join(ASSETS, 'shuli81.json'), encoding='utf-8') as f:
        shuli = json.load(f)['shuli']
    return strokes, wuxing, sancai, shuli


def ge_wuxing(num):
    return {1: '木', 2: '木', 3: '火', 4: '火', 5: '土', 6: '土', 7: '金', 8: '金', 9: '水', 0: '水'}[num % 10]


def suggest(surname, wuxing_filter=None, limit=10, chars=2):
    strokes, wuxing, sancai, shuli = load_assets()
    if any(c not in strokes for c in surname):
        missing = [c for c in surname if c not in strokes]
        raise ValueError('姓氏無法查得康熙筆畫: ' + ', '.join(missing))

    s_strokes = [strokes[c] for c in surname]
    is_compound = len(surname) >= 2
    results = []

    for a in STROKE_RANGE:
        for b in STROKE_RANGE:
            if is_compound:
                tian = sum(s_strokes)
                ren = s_strokes[1] + a
            else:
                tian = s_strokes[0] + 1
                ren = s_strokes[0] + a
            if chars == 2:
                di = a + b
                zong = sum(s_strokes) + a + b
                wai = zong - ren + 1
            else:
                di = a + 1
                zong = sum(s_strokes) + a
                wai = 2

            # 81 數理吉凶檢查：人/地/總/外
            ge_values = {'天格': tian, '人格': ren, '地格': di, '總格': zong, '外格': wai}
            checked = ['人格', '地格', '總格', '外格']
            ok = True
            for g in checked:
                num = ge_values[g]
                key = str(num if num <= 81 else (num - 1) % 81 + 1)
                if shuli.get(key, {}).get('grade') not in GOOD_GRADE:
                    ok = False
                    break
            if not ok:
                continue

            # 三才檢查
            config = ''.join(ge_wuxing(ge_values['天格']) + ge_wuxing(ge_values['人格']) + ge_wuxing(ge_values['地格']))
            si = sancai.get(config)
            if si is None or si['result'] in BAD_SANCAI:
                continue

            # 候選字
            mid_cands = [c for c in wuxing if strokes.get(c) == a]
            last_cands = [c for c in wuxing if strokes.get(c) == b]
            if wuxing_filter and len(wuxing_filter) >= 1:
                mid_cands = [c for c in mid_cands if wuxing.get(c) == wuxing_filter[0]]
            if wuxing_filter and len(wuxing_filter) >= 2:
                last_cands = [c for c in last_cands if wuxing.get(c) == wuxing_filter[1]]
            if not mid_cands or not last_cands:
                continue

            results.append({
                'strokes': [a, b],
                'ge': {k: {'value': v, 'wuxing': ge_wuxing(v)} for k, v in ge_values.items()},
                'sancai': config,
                'sancai_result': si['result'],
                'mid_candidates': mid_cands[:limit],
                'last_candidates': last_cands[:limit],
            })

    # 依三才吉凶排序：非「大吉/中吉/吉」的往後排
    priority = {'大吉': 0, '吉': 1, '中吉': 2, '吉多于凶': 3, '吉凶参半': 4, '凶多于吉': 5, '大凶': 6, '凶': 7, '凶多吉少': 8}
    results.sort(key=lambda r: (priority.get(r['sancai_result'], 9), r['strokes'][0], r['strokes'][1]))
    return results


def main():
    ap = argparse.ArgumentParser(description='chinese-naming suggest')
    ap.add_argument('surname', help='姓氏（單姓或複姓）')
    ap.add_argument('--chars', type=int, default=2, choices=[1, 2], help='名字字數（預設 2）')
    ap.add_argument('--wuxing', help='名兩字五行，如 水木（可只給一字）')
    ap.add_argument('--limit', type=int, default=10, help='每組合候選字上限（預設 10）')
    args = ap.parse_args()

    wf = list(args.wuxing) if args.wuxing else None
    if wf and len(wf) > args.chars:
        wf = wf[:args.chars]
    try:
        out = suggest(args.surname, wuxing_filter=wf, limit=args.limit, chars=args.chars)
        print(json.dumps({'total': len(out), 'results': out}, ensure_ascii=False, indent=2))
    except ValueError as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False))
        raise SystemExit(1)


if __name__ == '__main__':
    main()