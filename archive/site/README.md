# 途策官网（Astro）— /cases 录取案例世界地图

纸面出版物风格的录取案例页：构建期用 d3-geo 把 Natural Earth 110m 世界地图投影成内联 SVG（太平洋中心视角），所有录取学校精确标注，并以从上海出发的飞行弧线动画连接。**d3-geo / topojson / world-atlas 仅为构建依赖，客户端零地图库**，交互脚本 gzip 后约 3KB。

## 命令

```bash
pnpm install        # 安装
pnpm dev            # 开发 http://localhost:4321/cases
pnpm build          # 构建到 dist/
pnpm preview        # 预览构建产物
```

## 部署（Cloudflare Pages · 域名 tuce.asia · 单项目承载两站）

`pnpm build` = `astro build` + `scripts/copy-h5.mjs`：构建后自动把仓库根目录的 H5 落地页
（`index.html` + `css/` + `js/` + `assets/`）并入 `dist/`，所以**一个 Pages 项目同时服务**：

- `https://tuce.asia/` → H5 落地页（源文件仍在仓库根目录，改它不用碰本目录）
- `https://tuce.asia/cases/` → 录取去向世界地图（H5 导航/页脚的「录取去向」相对链接天然生效）

| 设置 | 值 |
|---|---|
| Root directory | `site` |
| Build command | `pnpm build` |
| Output directory | `dist` |
| Custom domain | `tuce.asia` |

纯静态输出，无需任何 Functions / 服务端运行时。
（copy 脚本会剔除 assets/ 中未被引用的孤儿大文件，约省 9MB 产物体积。）

## 如何新增一条录取案例

打开 `src/data/cases.json`，按下面的结构追加一条即可——地图、弧线、动画、筛选器、语义列表、JSON-LD 全部数据驱动，**不需要改任何组件代码**：

```json
{
  "id": "2026-016",            // 唯一即可，建议「年份-序号」
  "student": "A同学",           // 隐私规则：只用「姓氏+同学」或英文首字母
  "school_zh": "杜克大学",
  "school_en": "Duke University",
  "program": "数据科学硕士",
  "degree": "MIDS",
  "year": 2026,
  "region": "us",              // us / uk / hk / sg；新地区先在
                               //   AdmissionMap.astro 的 REGIONS 和
                               //   cases.astro 的 REGION_META 各加一行
  "city": "Durham",            // 用于「同城散开」：同城多校请保持城市名一致
  "coordinates": [-78.94, 36.00]   // [经度, 纬度] ← 注意顺序！
}
```

### 如何获取学校经纬度

1. **Google Maps**：搜索学校 → 在校园中心右键 → 第一行即「纬度, 经度」→ **写入 JSON 时调换顺序为 [经度, 纬度]**，西经/南纬为负数。
2. **Wikipedia**：学校词条右上角 Coordinates，点开有十进制格式。
3. 精度保留 2–3 位小数即可（110m 比例尺下足够）。

### 同城多校（重要）

波士顿/伦敦/香港这类同城多校：把 `city` 字段写成**完全相同的字符串**（如都写 `"London"`），构建脚本会自动把标记点等角散开 9px，避免重叠。

## 隐私规则

学生一律以「姓氏+同学」或英文首字母呈现；不出现全名、照片或可反查身份的背景细节。当前 15 条为**占位示例数据**，上线前请替换为真实且获学员授权的案例。

## 3D 地球参数调节

3D 点阵地球的**全部可调参数集中在 `src/three/globe/config.ts`** 的 `CONFIG` 对象，常用项：

| 想调什么 | 改哪里 |
|---|---|
| 辉光强弱 | `bloom.strength`（0.6–0.9 区间，宁低勿高）/ `bloom.threshold` |
| 自转速度 | `rotationSecsPerTurn`（秒/圈，默认 60） |
| 弧线配色 | `colors.arcDeep / arcMid / arcTip`（保持墨绿系！禁蓝紫） |
| 弧线抬升 | `arc.altMin / altMax`（× 半径；长弧自动取高值） |
| 点阵密度 | `scripts/gen-globe-dots.mjs` 的 `STEP`（度，越小越密；改后重新 build） |
| 点的大小/提亮 | `dots.size` / `dots.litRadius` |
| 待机重播频率 | `idle.minGapS / maxGapS` |
| 视差幅度 | `parallaxDeg`（默认 2.5°） |
| 入场节奏 | `entrance.arcStagger / arcDraw / globeIn` |

**2D/3D 切换逻辑**（`AdmissionGlobe.astro` 脚本）：桌面（fine pointer 且 ≥768px）+ WebGL 可用 + 非低端
（`hardwareConcurrency>2` 且 `deviceMemory≥4`）才加载 3D；初始化抛错时 try-catch 自动回退 2D。
移动端始终 2D；`prefers-reduced-motion` 下 3D 渲染单帧静态。**2D 版（AdmissionMap.astro）永久保留，请勿删除。**

## 技术要点（维护者读）

- 投影：`geoNaturalEarth1().rotate([-150, 0])`（太平洋中心）。美/英/港/新的弧线都不跨投影反经线，无需断裂处理；陆地在 30°W 处的裁剪由 d3-geo 自动完成。改投影只动 `src/lib/geo.js`。
- 弧线：投影后 2D 二次贝塞尔，`pathLength="1"` + `stroke-dashoffset` 描线；光点用 CSS `offset-path`（`@supports` 守护）。
- 动画全部 CSS 原生；`prefers-reduced-motion` 与无 JS 环境均降级为静态完整地图。
- SEO/GEO：地图下方的语义列表 + `ItemList` JSON-LD 与 JSON 同源渲染——SVG 对爬虫不可读，这两者才是可抓取版本，**不要删**。
