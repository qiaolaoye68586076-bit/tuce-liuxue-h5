/**
 * 生产站案例页数据导出：src/data/cases.json → frontend/assets/cases-data.json
 * 供 frontend/cases.html 的录取去向板块（3D 地球 + 名录）客户端渲染。
 * 与 cases.astro / AdmissionGlobe 的聚合逻辑保持一致。
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { groupSchools, programLine } from '../src/lib/schools.js';

const here = dirname(fileURLToPath(import.meta.url));
const cases = JSON.parse(readFileSync(resolve(here, '../src/data/cases.json'), 'utf8'));
const out = resolve(here, '../../../frontend/assets/cases-data.json');

const REGION_META = {
  us: { zh: '美国', en: 'United States' },
  uk: { zh: '英国', en: 'United Kingdom' },
  hk: { zh: '中国香港', en: 'Hong Kong SAR' },
  sg: { zh: '新加坡', en: 'Singapore' },
  au: { zh: '澳大利亚', en: 'Australia' },
  ca: { zh: '加拿大', en: 'Canada' },
};
const regionOrder = ['us', 'uk', 'hk', 'sg', 'au', 'ca'];

// 目录：区内按院校（Offer 数降序），校内按年份降序
const regions = regionOrder.map((key) => {
  const list = cases.filter((c) => c.region === key);
  const bySchool = new Map();
  for (const c of list) {
    if (!bySchool.has(c.school_en)) bySchool.set(c.school_en, []);
    bySchool.get(c.school_en).push(c);
  }
  const schools = [...bySchool.values()]
    .map((cs) => ({
      school_zh: cs[0].school_zh,
      school_en: cs[0].school_en,
      cases: cs
        .sort((a, b) => b.year - a.year)
        .map((c) => ({ program: c.program, degree: c.degree, year: c.year, student: c.student })),
    }))
    .sort((a, b) => b.cases.length - a.cases.length);
  return { key, ...REGION_META[key], count: list.length, schools };
}).filter((g) => g.count > 0);

const total = cases.length;
const schoolsCount = new Set(cases.map((c) => c.school_en)).size;
const years = [...new Set(cases.map((c) => c.year))].sort((a, b) => a - b);
const yearRange = `${years[0]}–${years[years.length - 1]}`;

// 地球弧线数据（一校一弧）
const payload = groupSchools(cases).map((g) => ({
  id: g.sid,
  school_zh: g.school_zh,
  school_en: g.school_en,
  region: g.region,
  years: g.years,
  count: g.count,
  programs: programLine(g),
  yearSpan: g.years.length > 1 ? `${g.years[0]}–${g.years[g.years.length - 1]}` : String(g.years[0]),
  coordinates: g.coordinates,
}));

const data = {
  total,
  schoolsCount,
  yearRange,
  filterRegions: regions.map((g) => ({ key: g.key, zh: g.zh })),
  regions,
  payload,
};

writeFileSync(out, JSON.stringify(data));
console.log(`[gen-cases-data] ${total} cases / ${schoolsCount} schools / ${regions.length} regions -> frontend/assets/cases-data.json (${(JSON.stringify(data).length / 1024).toFixed(0)}KB)`);
