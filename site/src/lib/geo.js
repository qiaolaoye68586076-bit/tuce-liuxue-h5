/**
 * 构建期地理引擎（仅在 Astro frontmatter/SSG 阶段运行，绝不进入客户端 bundle）。
 *
 * 投影决策：geoNaturalEarth1 + rotate([-150, 0]) —— 太平洋中心视角（中心经线 150°E）。
 * 这样上海居中偏左、美国在右、英国在左缘：
 *   上海→美国弧线向右跨太平洋（真实航向），上海→英国弧线向左跨亚欧，
 *   所有目标地区（美/英/港/新）的弧线均不跨越投影反经线，无需断裂双段绘制。
 * 陆地多边形在反经线（30°W，大西洋/格陵兰）处由 d3-geo 自动裁剪。
 */
import { geoNaturalEarth1, geoPath } from 'd3-geo';
import { feature, mesh } from 'topojson-client';
import world from 'world-atlas/countries-110m.json';

export const SIZE = { W: 1200, H: 560 };

const countries = feature(world, world.objects.countries);
// 移除南极洲，纵向更紧凑
const land = {
  type: 'FeatureCollection',
  features: countries.features.filter((f) => f.properties.name !== 'Antarctica'),
};
// 仅内部国境线（共享边界），天然不含南极洲
const borders = mesh(world, world.objects.countries, (a, b) => a !== b);

export const projection = geoNaturalEarth1()
  .rotate([-150, 0])
  .fitExtent(
    [
      [8, 8],
      [SIZE.W - 8, SIZE.H - 8],
    ],
    land
  );

const path = geoPath(projection);

export const landPath = path(land);
export const bordersPath = path(borders);

/** 经纬度 → SVG 坐标。coordinates: [lon, lat] */
export function project([lon, lat]) {
  return projection([lon, lat]);
}
