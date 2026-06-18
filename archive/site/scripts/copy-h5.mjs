/**
 * 统一部署：astro build 之后，把仓库根目录的 H5 落地页拷入 dist/，
 * 使同一个 Cloudflare Pages 项目（域名 tuce.asia）同时承载：
 *   /        ← H5 落地页（index.html + css/ + js/ + assets/）
 *   /cases/  ← Astro 录取去向世界地图
 *
 * H5 源文件唯一真源仍是仓库根目录 —— 改 H5 不需要碰本目录。
 */
import { cpSync, existsSync } from 'node:fs';
import { dirname, resolve, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(here, '../..');
const dist = resolve(here, '../dist');

// 不进入产物的孤儿/超重资源（仓库保留，部署剔除）
const EXCLUDE = new Set([
  '.DS_Store',
  'hero-bg.png',      // 已被 hero-bg.jpg 取代（1.9MB 孤儿）
  'logo-light.svg',   // 未引用（1.2MB 孤儿）
  'mentor-01.png', 'mentor-02.png', 'mentor-03.png', 'mentor-04.png', // 高清孤儿，共约 7MB
]);
const filter = (src) => !EXCLUDE.has(basename(src));

if (!existsSync(dist)) {
  console.error('[copy-h5] dist/ 不存在，请先运行 astro build');
  process.exit(1);
}

cpSync(resolve(repoRoot, 'index.html'), resolve(dist, 'index.html'));
for (const dir of ['css', 'js', 'assets']) {
  cpSync(resolve(repoRoot, dir), resolve(dist, dir), { recursive: true, filter });
}
console.log('[copy-h5] H5 已并入 dist/：/ → 落地页，/cases/ → 录取地图');
