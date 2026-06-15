/**
 * 构建期点阵采样：world-atlas land-110m → 陆地经纬度点阵 → public/globe-dots.json
 * 运行时零地理计算：3D 端只需把这些点转成球面 xyz。
 *
 * 采样：等面积网格（每行 dLon = dLat / cos(lat)），d3-geo geoContains 判陆地；
 * 输出：Int16 量化扁平数组 [lon×10, lat×10, ...]，~10k 点 ≈ 100KB 原始 / ~35KB gzip。
 */
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { geoContains } from 'd3-geo';
import { feature } from 'topojson-client';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const world = require('world-atlas/land-110m.json');

const here = dirname(fileURLToPath(import.meta.url));
const out = resolve(here, '../public/globe-dots.json');

const land = feature(world, world.objects.land);

const STEP = 1.05;          // 基础纬向间距（度）——密度旋钮
const LAT_MIN = -56;        // 剔除南极洲
const LAT_MAX = 84;

const dots = [];
for (let lat = LAT_MIN; lat <= LAT_MAX; lat += STEP) {
  const dLon = STEP / Math.max(0.18, Math.cos((lat * Math.PI) / 180));
  // 每行加半步交错，避免网格感过强
  const offset = ((lat / STEP) % 2) * (dLon / 2);
  for (let lon = -180 + offset; lon < 180; lon += dLon) {
    if (geoContains(land, [lon, lat])) {
      dots.push(Math.round(lon * 10), Math.round(lat * 10));
    }
  }
}

mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, JSON.stringify(dots));
console.log(`[gen-globe-dots] ${dots.length / 2} land dots -> public/globe-dots.json (${(JSON.stringify(dots).length / 1024).toFixed(0)}KB raw)`);
