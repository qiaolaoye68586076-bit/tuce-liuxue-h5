/**
 * ★ 3D 地球全部可调参数（README「3D 地球参数调节」章节对应此文件）
 * 品牌约束：仅墨绿系（#005839 → #00a86b → #7fdcb0），禁蓝/紫/霓虹粉。
 */
export const CONFIG = {
  radius: 1,

  /* 相机与构图：方形取景，球径约占框 ~70%，上下左右给跨洋长弧留出头（避免弧线被截） */
  fov: 38,
  cameraZ: 4.1,

  /* 运动 */
  rotationSecsPerTurn: 60,   // 自转一圈秒数
  parallaxDeg: 2.5,          // 鼠标视差最大倾斜（度）
  parallaxLerp: 0.05,
  idleFloatAmp: 0.012,       // 相机正弦微浮幅度（world 单位）
  inertiaDamping: 0.93,      // 拖拽惯性阻尼
  resumeAfterDragMs: 2000,   // 松手后恢复自转的延时

  /* 配色（全部墨绿系） */
  colors: {
    dot: '#5d8472',          // 陆地点：提亮墨绿（陆块更清晰，看得出是地球）
    dotLit: '#9bf0c6',       // 脉冲经过时点的提亮色
    sphere: '#0e1d17',       // 内球（深墨绿球面，给出地球轮廓/海洋底色）
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

  /* 大气强度（球缘绿色光晕，强化"这是个球"的体积感） */
  atmosphereIntensity: 1.0,

  /* 点阵 */
  dots: {
    size: 0.02,              // 基础点径（配合降密度，陆块成片更易辨认）
    litRadius: 0.24,         // 脉冲提亮的影响半径（world 单位）
  },

  /* 初始姿态：东亚视角——上海居中、亚欧大陆铺满左半（不再正对空旷太平洋），
     跨洋弧线向右扇出落向美洲 */
  initialRotX: 0.42,
  initialRotY: 2.70,

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
