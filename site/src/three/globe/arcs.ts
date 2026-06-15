/**
 * 飞行弧线：上海→各校大圆弧（slerp + sin 抬升），自定义 shader。
 * - 线身：墨绿渐变 + uProgress 描线 + uPulseT 高斯拖尾（不进 bloom）
 * - 脉冲头：独立小球，BLOOM 层（对象级隔离 → 头亮尾隐）
 * - 落点涟漪：球面切向圆环，BLOOM 层
 */
import {
  BufferGeometry, Float32BufferAttribute, Line, ShaderMaterial, Color, Vector3,
  Mesh, SphereGeometry, MeshBasicMaterial, RingGeometry, AdditiveBlending,
  DoubleSide, Quaternion,
} from 'three';
import { CONFIG, BLOOM_LAYER, SHANGHAI } from './config';
import { lonLatToVec3 } from './globe';

export interface CaseInput {
  id: string;                // 院校聚合后的 sid
  region: string;
  years: number[];           // 该校有录取的年份集合（筛选用）
  coordinates: [number, number];
}

export interface Arc {
  id: string;
  region: string;
  years: number[];
  line: Line;
  lineMat: ShaderMaterial;
  head: Mesh;
  headMat: MeshBasicMaterial;
  ripple: Mesh;
  rippleMat: MeshBasicMaterial;
  end: Vector3;            // 终点（球面）
  angle: number;           // 角距（排序用）
  getPoint(t: number): Vector3;
  active: boolean;         // 筛选可见性
  rippleT: number;         // -1 = 未播放
}

export function buildArc(c: CaseInput): Arc {
  const R = CONFIG.radius;
  const a = lonLatToVec3(SHANGHAI[0], SHANGHAI[1], 1).normalize();
  const b = lonLatToVec3(c.coordinates[0], c.coordinates[1], 1).normalize();
  const angle = a.angleTo(b);
  const alt = CONFIG.arc.altMin + (angle / Math.PI) * (CONFIG.arc.altMax - CONFIG.arc.altMin);
  const sinA = Math.sin(angle);

  const getPoint = (t: number): Vector3 => {
    // 大圆 slerp
    const A = Math.sin((1 - t) * angle) / sinA;
    const B = Math.sin(t * angle) / sinA;
    const p = new Vector3(
      a.x * A + b.x * B,
      a.y * A + b.y * B,
      a.z * A + b.z * B,
    ).normalize();
    return p.multiplyScalar(R * (1 + alt * Math.sin(Math.PI * t)));
  };

  const N = CONFIG.arc.segments;
  const positions = new Float32Array((N + 1) * 3);
  const aT = new Float32Array(N + 1);
  for (let i = 0; i <= N; i++) {
    const t = i / N;
    const p = getPoint(t);
    positions[i * 3] = p.x;
    positions[i * 3 + 1] = p.y;
    positions[i * 3 + 2] = p.z;
    aT[i] = t;
  }
  const geo = new BufferGeometry();
  geo.setAttribute('position', new Float32BufferAttribute(positions, 3));
  geo.setAttribute('aT', new Float32BufferAttribute(aT, 1));

  const lineMat = new ShaderMaterial({
    transparent: true,
    depthWrite: false,
    uniforms: {
      uProgress: { value: 0 },
      uPulseT: { value: -10 },                  // <0 = 无脉冲
      uBaseAlpha: { value: CONFIG.arc.baseAlpha },
      uDeep: { value: new Color(CONFIG.colors.arcDeep) },
      uMid: { value: new Color(CONFIG.colors.arcMid) },
      uTip: { value: new Color(CONFIG.colors.arcTip) },
      uTrailW: { value: CONFIG.arc.trailWidth },
    },
    vertexShader: /* glsl */ `
      attribute float aT;
      varying float vT;
      void main() {
        vT = aT;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }`,
    fragmentShader: /* glsl */ `
      uniform float uProgress, uPulseT, uBaseAlpha, uTrailW;
      uniform vec3 uDeep, uMid, uTip;
      varying float vT;
      void main() {
        if (vT > uProgress) discard;
        vec3 col = vT < 0.5 ? mix(uDeep, uMid, vT * 2.0) : mix(uMid, uTip, vT * 2.0 - 1.0);
        float behind = step(vT, uPulseT);        // 仅头后方留拖尾
        float trail = exp(-pow((uPulseT - vT) * uTrailW, 2.0)) * behind;
        col += uTip * trail * 0.9;
        float alpha = uBaseAlpha * (0.45 + 0.55 * vT) + trail * 0.4;
        gl_FragColor = vec4(col, min(alpha, 1.0));
      }`,
  });
  const line = new Line(geo, lineMat);

  // 脉冲头（BLOOM 层 + 基础层都渲染）
  const headMat = new MeshBasicMaterial({
    color: new Color(CONFIG.colors.arcTip),
    transparent: true,
    opacity: 0,
  });
  const head = new Mesh(new SphereGeometry(0.013, 8, 8), headMat);
  head.layers.enable(BLOOM_LAYER);

  // 落点涟漪：贴球面圆环
  const end = getPoint(1);
  const normal = end.clone().normalize();
  const rippleMat = new MeshBasicMaterial({
    color: new Color(CONFIG.colors.ripple),
    transparent: true,
    opacity: 0,
    blending: AdditiveBlending,
    side: DoubleSide,
    depthWrite: false,
  });
  const ripple = new Mesh(new RingGeometry(0.02, 0.027, 40), rippleMat);
  ripple.position.copy(normal.clone().multiplyScalar(CONFIG.radius * 1.003));
  ripple.quaternion.copy(new Quaternion().setFromUnitVectors(new Vector3(0, 0, 1), normal));
  ripple.layers.enable(BLOOM_LAYER);

  return {
    id: c.id, region: c.region, years: c.years,
    line, lineMat, head, headMat, ripple, rippleMat,
    end, angle, getPoint, active: true, rippleT: -1,
  };
}

/** 每帧推进涟漪动画（在主循环里调用） */
export function tickRipple(arc: Arc, dt: number) {
  if (arc.rippleT < 0) return;
  arc.rippleT += dt / 0.9;                     // 0.9s 一次扩散
  if (arc.rippleT >= 1) {
    arc.rippleT = -1;
    arc.rippleMat.opacity = 0;
    return;
  }
  const t = arc.rippleT;
  const s = 1 + t * 1.8;
  arc.ripple.scale.setScalar(s);
  arc.rippleMat.opacity = (1 - t) * 0.85;
}
