#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chinese-naming analyze.py — 姓名五格三才分析

CLI:  python3 analyze.py 王小明
      python3 analyze.py 歐陽娜娜

輸出 JSON：
  - 各字康熙筆畫、五行
  - 天/人/地/總/外格數值、五行、81 數理吉凶與特質
  - 三才配置（天+人+地五行）、吉凶與斷語

五格公式（單姓雙名）：
  天格 = 姓 + 1
  人格 = 姓 + 名1
  地格 = 名1 + 名2
  總格 = 姓 + 名1 + 名2
  外格 = 總格 - 人格 + 1
複姓：天格 = 複姓和；人格 = 複姓第2字 + 名1；地格、總格同；外格 = 總格 - 人格 + 1

五行判定（尾數）：1/2=木 3/4=火 5/6=土 7/8=金 9/0=水
81 數理：>81 時以 81 為週期取餘（1..81 循環）
"""
import json
import os
import sys

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')

# 常用複姓表（前二字命中即視為複姓）
COMPOUND_SURNAMES = {
    '歐陽', '司馬', '上官', '諸葛', '東方', '獨孤', '南宮', '西門', '司徒', '司空',
    '夏侯', '皇甫', '公孫', '慕容', '尉遲', '長孫', '宇文', '呼延', '端木', '令狐',
    '百里', '赫連', '聞人', '濮陽', '公冶', '申屠', '太叔', '鍾離', '軒轅', '鮮于',
    '閭丘', '万俟', '樂正', '壤駟', '公良', '拓跋', '夾谷', '宰父', '穀梁', '段干',
    '東郭', '南門', '羊舌', '微生', '梁丘', '左丘', '東門', '南榮', '巫馬', '公西',
    '漆雕', '東野', '毌丘',
}

WUXING_BY_TAIL = {1: '木', 2: '木', 3: '火', 4: '火', 5: '土', 6: '土', 7: '金', 8: '金', 9: '水', 0: '水'}


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
    return WUXING_BY_TAIL[num % 10]


def shuli_lookup(num, shuli):
    key = str(num if num <= 81 else (num - 1) % 81 + 1)
    return shuli.get(key, {'grade': '未知', 'traits': []})


def split_name(name, compound):
    """回傳 (is_compound, surname, given)。"""
    if len(name) == 2:
        return False, name[0], name[1]
    if len(name) >= 4 and name[:2] in compound:
        return True, name[:2], name[2:]
    if len(name) == 3:
        # 前兩字是複姓（如歐陽娜）單名
        if name[:2] in compound:
            return True, name[:2], name[2]
        return False, name[0], name[1:]
    # 4 字以上非複姓：當單姓雙名處理（取前 1 字為姓）
    return False, name[0], name[1:]


def compute_wuge(is_compound, surname, given, strokes):
    """計算五格。回傳 dict: 天/人/地/總/外 數值。"""
    s_strokes = [strokes.get(c) for c in surname]
    g_strokes = [strokes.get(c) for c in given]
    if any(v is None for v in s_strokes + g_strokes):
        missing = [c for c, v in zip(surname + given, s_strokes + g_strokes) if v is None]
        raise ValueError('無法查得康熙筆畫: ' + ', '.join(missing))
    if is_compound:
        tian = sum(s_strokes)
        ren = s_strokes[1] + g_strokes[0]
    else:
        tian = s_strokes[0] + 1
        ren = s_strokes[0] + g_strokes[0]
    di = sum(g_strokes) if len(g_strokes) > 1 else g_strokes[0] + 1
    zong = sum(s_strokes) + sum(g_strokes)
    if len(g_strokes) > 1:
        wai = zong - ren + 1
    else:
        # 單名：外格固定為 2（標準五格規則；總格-人格+1 在此會失真）
        wai = 2
    return {'天格': tian, '人格': ren, '地格': di, '總格': zong, '外格': wai}


def analyze(name):
    strokes, wuxing, sancai, shuli = load_assets()
    is_compound, surname, given = split_name(name, COMPOUND_SURNAMES)
    ge = compute_wuge(is_compound, surname, given, strokes)

    sancai_config = ''.join(ge_wuxing(ge['天格']) + ge_wuxing(ge['人格']) + ge_wuxing(ge['地格']))
    sancai_info = sancai.get(sancai_config, {'result': '未知配置', 'evaluate': '此三才配置不在資料表中。', 'nums': ''})

    result = {
        'name': name,
        'surname': surname,
        'given': given,
        'surname_type': '複姓' if is_compound else '單姓',
        'char_strokes': {c: strokes[c] for c in surname + given},
        'char_wuxing': {c: wuxing.get(c, '未知') for c in surname + given},
        'ge': {},
        'sancai': {
            'config': sancai_config,
            'result': sancai_info['result'],
            'evaluate': sancai_info['evaluate'],
            'nums': sancai_info.get('nums', ''),
        },
    }
    for gname, num in ge.items():
        sl = shuli_lookup(num, shuli)
        result['ge'][gname] = {
            'value': num,
            'wuxing': ge_wuxing(num),
            'shuli_grade': sl['grade'],
            'shuli_traits': sl['traits'],
        }
    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': '用法: python3 analyze.py <姓名>'}, ensure_ascii=False))
        sys.exit(1)
    name = sys.argv[1]
    try:
        print(json.dumps(analyze(name), ensure_ascii=False, indent=2))
    except ValueError as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()