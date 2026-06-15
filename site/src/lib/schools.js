/**
 * 构建期聚合：220 条案例 → 59 所唯一院校（地图视觉按院校聚合，一校一弧线）。
 * 语义列表 / JSON-LD 仍使用全量 cases；本聚合只服务 2D/3D 地图与 hover 卡片。
 */
export function groupSchools(cases) {
  const map = new Map();
  for (const c of cases) {
    let g = map.get(c.school_en);
    if (!g) {
      g = {
        sid: c.school_en.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
        school_zh: c.school_zh,
        school_en: c.school_en,
        region: c.region,
        city: c.city,
        coordinates: c.coordinates,
        count: 0,
        years: new Set(),
        programs: [],
        cases: [],
      };
      map.set(c.school_en, g);
    }
    g.count++;
    g.years.add(c.year);
    if (!g.programs.includes(c.program)) g.programs.push(c.program);
    g.cases.push(c);
  }
  return [...map.values()].map((g) => ({
    ...g,
    years: [...g.years].sort(),
  }));
}

/** hover 卡片的代表专业行：前 3 个 + 「等」 */
export function programLine(g) {
  const head = g.programs.slice(0, 3).join(' / ');
  return g.programs.length > 3 ? `${head} 等` : head;
}
