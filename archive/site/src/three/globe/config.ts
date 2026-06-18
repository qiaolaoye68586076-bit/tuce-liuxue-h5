/**
 * ★ 3D 地球全部可调参数（README「3D 地球参数调节」章节对应此文件）
 * 品牌约束：仅墨绿系（#005839 → #00a86b → #7fdcb0），禁蓝/紫/霓虹粉。
 */
export const CONFIG = {
  radius: 1,

  /* 相机与构图（球径 ≈ 舞台高度的 ~75%，留呼吸感） */
  fov: 38,
  cameraZ: 3.95,

  /* 运动 */
  rotationSecsPerTurn: 60,   // 自转一圈秒数
  parallaxDeg: 2.5,          // 鼠标视差最大倾斜（度）
  parallaxLerp: 0.05,
  idleFloatAmp: 0.012,       // 相机正弦微浮幅度（world 单位）
  inertiaDamping: 0.93,      // 拖拽惯性阻尼
  resumeAfterDragMs: 2000,   // 松手后恢复自转的延时

  /* 配色（全部墨绿系） */
  colors: {
    dot: '#3d4a42',          // 陆地点：低饱和暖灰绿
    dotLit: '#7fdcb0',       // 脉冲经过时点的提亮色
    sphere: '#0d1411',       // 内球（近不可见的深色球面）
    atmosphere: '#00a86b',   // Fresnel 大气边缘光
    arcDeep: '#005839',
    arcMid: '#00a86b',
    arcTip: '#7fdcb0',
    marker: '#00a86b',
    pillar: '#00a86b',
    beacon: '#7fdcb0',       // 上海源点
    ripple: '#00a86b',
  },

  /* 辉光（Selective Bloom，宁低勿高） */
  bloom: { strength: 0.8, radius: 0.4, threshold: 0.1 },

  /* 大气强度 */
  atmosphereIntensity: 0.5,

  /* 点阵 */
  dots: {
    size: 0.012,             // 基础点径（world 单位，≈2px @ 默认相机距离）
    litRadius: 0.24,         // 脉冲提亮的影响半径（world 单位）
  },

  /* 初始姿态：北太平洋视角——上海光点居中偏左，跨洋弧线向右上扇出，港新短弧落左下 */
  initialRotX: 0.42,
  initialRotY: 1.32,

  /* 弧线 */
  arc: {
    segments: 64,
    altMin: 0.08,            // 短弧抬升（× R）
    altMax: 0.3,             // 跨太平洋长弧抬升（× R）
    baseAlpha: 0.8,
    dimAlpha: 0.15,          // hover 聚焦时其余弧线透明度
    trailWidth: 9.0,         // 拖尾高斯宽度（越大越短）
  },

  /* 标记 */
  markerRadius: 0.0085,
  pillarHeight: 0.05,        // 光柱高度（克制）
  pillarAlpha: 0.32,
  beaconBreathSecs: 3,

  /* 入场编排 */
  entrance: {
    startDelay: 0.25,
    globeIn: 1.2,            // 地球浮现时长
    arcStagger: 0.1,         // 弧线发出间隔
    arcDraw: 1.15,           // 单条描线时长
  },

  /* 待机重播 */
  idle: { minGapS: 4.5, maxGapS: 6.5, pulseDurS: 1.5 },

  /* 交互 */
  clickSlerpS: 0.8,
};

export const SHANGHAI: [number, number] = [121.47, 31.23];
export const BLOOM_LAYER = 1;
