#!/usr/bin/env python3
"""
从《2024-2026录取案例清单.xlsx》(sheet: 录取明细) 重新生成 src/data/cases.json。
Excel 更新后重跑：python3 scripts/import-cases.py [xlsx路径]

列：序号 | 年份 | 类别 | 国家地区 | 录取学校(英文) | 录取学校(中文) | 录取专业 | 学生
学生列须已匿名（X同学）。新学校请在下方 SCHOOL_GEO 加一行坐标（[经度, 纬度]）。
"""
import json, sys, unicodedata
from pathlib import Path
import openpyxl

XLSX = sys.argv[1] if len(sys.argv) > 1 else str(Path.home() / 'Downloads/2024-2026录取案例清单.xlsx')
OUT = Path(__file__).resolve().parent.parent / 'src/data/cases.json'

REGION = {'美国': 'us', '英国': 'uk', '中国香港': 'hk', '香港': 'hk',
          '新加坡': 'sg', '澳大利亚': 'au', '加拿大': 'ca'}

# 学校 → (城市, [经度, 纬度])。城市字符串相同的学校会在 2D 地图上自动散开。
SCHOOL_GEO = {
    # —— 美国 ——
    'Cornell University': ('Ithaca', [-76.48, 42.45]),
    'University of Chicago': ('Chicago', [-87.60, 41.79]),
    'Emory University': ('Atlanta', [-84.32, 33.79]),
    'New York University': ('New York', [-74.00, 40.73]),
    'Columbia University': ('New York', [-73.96, 40.81]),
    'Boston University': ('Boston', [-71.11, 42.35]),
    'Northeastern University': ('Boston', [-71.09, 42.34]),
    'Boston College': ('Boston', [-71.17, 42.34]),
    'Brandeis University': ('Boston', [-71.26, 42.37]),
    'Ohio State University': ('Columbus', [-83.03, 40.00]),
    'Michigan State University': ('East Lansing', [-84.48, 42.70]),
    'Case Western Reserve University': ('Cleveland', [-81.61, 41.50]),
    'Rensselaer Polytechnic Institute': ('Troy', [-73.68, 42.73]),
    'Santa Clara University': ('Santa Clara', [-121.94, 37.35]),
    'University of Minnesota Twin Cities': ('Minneapolis', [-93.24, 44.97]),
    'Penn State University': ('University Park', [-77.86, 40.80]),
    'Virginia Tech': ('Blacksburg', [-80.42, 37.23]),
    'Carnegie Mellon University': ('Pittsburgh', [-79.94, 40.44]),
    'Duke University': ('Durham NC', [-78.94, 36.00]),
    'University of Southern California': ('Los Angeles', [-118.29, 34.02]),
    'University of Maryland, College Park': ('College Park', [-76.94, 38.99]),
    'Vanderbilt University': ('Nashville', [-86.80, 36.14]),
    'College of William & Mary': ('Williamsburg', [-76.71, 37.27]),
    'NC State University': ('Raleigh', [-78.68, 35.78]),
    'Purdue University': ('West Lafayette', [-86.92, 40.43]),
    'University of Pennsylvania': ('Philadelphia', [-75.19, 39.95]),
    'Northwestern University': ('Evanston', [-87.68, 42.06]),
    'Georgetown University': ('Washington DC', [-77.07, 38.91]),
    'Johns Hopkins University': ('Baltimore', [-76.62, 39.33]),
    # —— 英国 ——
    'UCL': ('London', [-0.134, 51.524]),
    'Imperial College London': ('London', [-0.176, 51.499]),
    "King's College London": ('London', [-0.116, 51.512]),
    'LSE': ('London', [-0.117, 51.514]),
    'University of Manchester': ('Manchester', [-2.234, 53.467]),
    'University of York': ('York', [-1.05, 53.95]),
    'University of Edinburgh': ('Edinburgh', [-3.19, 55.94]),
    'Durham University': ('Durham UK', [-1.57, 54.77]),
    'University of Warwick': ('Coventry', [-1.56, 52.38]),
    'University of Southampton': ('Southampton', [-1.40, 50.93]),
    'University of Oxford': ('Oxford', [-1.254, 51.754]),
    'University of Sheffield': ('Sheffield', [-1.49, 53.38]),
    'University of Leeds': ('Leeds', [-1.55, 53.81]),
    'University of Birmingham': ('Birmingham', [-1.93, 52.45]),
    'University of Cambridge': ('Cambridge UK', [0.114, 52.205]),
    'University of Bristol': ('Bristol', [-2.60, 51.46]),
    'University of Glasgow': ('Glasgow', [-4.29, 55.87]),
    # —— 中国香港 ——
    'The University of Hong Kong': ('Hong Kong', [114.137, 22.283]),
    'The Chinese University of Hong Kong': ('Hong Kong', [114.207, 22.420]),
    'HKUST': ('Hong Kong', [114.263, 22.336]),
    'City University of Hong Kong': ('Hong Kong', [114.172, 22.337]),
    'The Hong Kong Polytechnic University': ('Hong Kong', [114.180, 22.304]),
    # —— 新加坡 ——
    'National University of Singapore': ('Singapore', [103.776, 1.297]),
    'Nanyang Technological University': ('Singapore', [103.683, 1.348]),
    # —— 澳大利亚 ——
    'University of Sydney': ('Sydney', [151.187, -33.889]),
    'University of Melbourne': ('Melbourne', [144.961, -37.796]),
    'Australian National University': ('Canberra', [149.118, -35.278]),
    # —— 加拿大 ——
    'University of Toronto': ('Toronto', [-79.395, 43.663]),
    'McGill University': ('Montreal', [-73.577, 45.505]),
    'University of British Columbia': ('Vancouver', [-123.246, 49.261]),
}

def norm(s):
    return unicodedata.normalize('NFKC', str(s).strip()) if s is not None else ''

wb = openpyxl.load_workbook(XLSX, data_only=True)
ws = wb['录取明细']
out, missing = [], set()
for r in ws.iter_rows(min_row=2, values_only=True):
    if r[0] is None:
        continue
    seq, year, kind, region_zh, en, zh, program, student = [norm(x) for x in r[:8]]
    en_key = en
    if en_key not in SCHOOL_GEO:
        missing.add(en_key)
        continue
    city, coords = SCHOOL_GEO[en_key]
    out.append({
        'id': f'{year}-{int(float(seq)):03d}',
        'student': student,
        'school_zh': zh,
        'school_en': en,
        'program': program,
        'degree': kind,            # 本科 / 研究生
        'year': int(float(year)),
        'region': REGION[region_zh],
        'city': city,
        'coordinates': coords,
    })

if missing:
    print('!! SCHOOL_GEO 缺坐标，未导入：', missing)
    sys.exit(1)

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
schools = {(c['school_en']) for c in out}
print(f'[import-cases] {len(out)} cases / {len(schools)} schools -> {OUT}')
