/**
 * 构建期弧线引擎：投影后 2D 空间内生成二次贝塞尔航线 + 同城散开 + 距离排序 stagger。
 */
const SHANGHAI = [121.47, 31.23];
const FAN_RADIUS = 9; // 同城散开半径（SVG 单位）

/**
 * @param cases  cases.json 数组
 * @param project  geo.js 的投影函数
 * @returns { sx, sy, items }  items 按距离升序，含 x/y（散开后）、d（弧线 path）、delay（stagger 秒）
 */
export function buildScene(cases, project, origin = SHANGHAI) {
  const [sx, sy] = project(origin);

  // —— 同城散开：按 city 分组，n>1 时绕各自投影点等角偏移，避免标记重叠 ——
  const groups = {};
  for (const c of cases) (groups[c.city] ||= []).push(c);

  const placed = cases.map((c) => {
    const [bx, by] = project(c.coordinates);
    const g = groups[c.city];
    if (g.length === 1) return { ...c, x: bx, y: by };
    const i = g.indexOf(c);
    const angle = ((-90 + (360 / g.length) * i) * Math.PI) / 180;
    return {
      ...c,
      x: bx + FAN_RADIUS * Math.cos(angle),
      y: by + FAN_RADIUS * Math.sin(angle),
    };
  });

  // —— 弧线：中点沿垂直方向上抬（短弧扁、长弧高），pathLength=1 统一描线 ——
  const items = placed
    .map((c) => {
      const dx = c.x - sx;
      const dy = c.y - sy;
      const dist = Math.hypot(dx, dy) || 1;
      let px = dy / dist;
      let py = -dx / dist;
      if (py > 0) {
        px = -px;
        py = -py; // 保证控制点向上抬升
      }
      const lift = Math.min(dist * 0.22, 120);
      const cx = (sx + c.x) / 2 + px * lift;
      const cy = (sy + c.y) / 2 + py * lift;
      const d = `M ${sx.toFixed(1)} ${sy.toFixed(1)} Q ${cx.toFixed(1)} ${cy.toFixed(1)} ${c.x.toFixed(1)} ${c.y.toFixed(1)}`;
      return { ...c, dist, d };
    })
    .sort((a, b) => a.dist - b.dist)
    .map((c, i, arr) => {
      // stagger 随条数自适应：少量弧线 0.1s/条，多弧线压缩，总入场控制在 ~2.5s 内
      const step = Math.min(0.1, 2.4 / arr.length);
      return { ...c, delay: +(0.15 + i * step).toFixed(3) };
    });

  return { sx, sy, items };
}
