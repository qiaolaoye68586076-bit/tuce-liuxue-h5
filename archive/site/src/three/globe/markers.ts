/**
 * 学校标记（小光点 + 极细垂直光柱，克制、不进 bloom）+ 上海呼吸源点（bloom）
 * + 每校不可见 hit 球（raycast 命中区域）。
 */
import {
  Mesh, SphereGeometry, MeshBasicMaterial, CylinderGeometry, ShaderMaterial,
  Color, Vector3, Quaternion, AdditiveBlending, RingGeometry,
} from 'three';
import { CONFIG, BLOOM_LAYER, SHANGHAI } from './config';
import { lonLatToVec3 } from './globe';

const Y_AXIS = new Vector3(0, 1, 0);
const Z_AXIS = new Vector3(0, 0, 1);

export interface Marker {
  id: string;
  dot: Mesh;
  dotMat: MeshBasicMaterial;
  pillar: Mesh;
  pillarMat: ShaderMaterial;
  hit: Mesh;
  pos: Vector3;
  popT: number;            // -1 = 未弹出；0..1 弹出动画
}

export function buildMarker(id: string, lonLat: [number, number]): Marker {
  const normal = lonLatToVec3(lonLat[0], lonLat[1], 1).normalize();
  const surface = normal.clone().multiplyScalar(CONFIG.radius * 1.001);
  const orient = new Quaternion().setFromUnitVectors(Y_AXIS, normal);

  const dotMat = new MeshBasicMaterial({ color: new Color(CONFIG.colors.marker) });
  const dot = new Mesh(new SphereGeometry(CONFIG.markerRadius, 10, 10), dotMat);
  dot.position.copy(surface);
  dot.scale.setScalar(0.0001);

  // 极细光柱：底亮顶隐，加法混合，几像素的辉光感（不进 bloom）
  const h = CONFIG.pillarHeight;
  const pillarMat = new ShaderMaterial({
    transparent: true,
    depthWrite: false,
    blending: AdditiveBlending,
    uniforms: {
      uColor: { value: new Color(CONFIG.colors.pillar) },
      uAlpha: { value: 0 },                    // 随 marker 弹出淡入
    },
    vertexShader: /* glsl */ `
      varying float vY;
      void main() {
        vY = uv.y;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }`,
    fragmentShader: /* glsl */ `
      uniform vec3 uColor;
      uniform float uAlpha;
      varying float vY;
      void main() {
        gl_FragColor = vec4(uColor, (1.0 - vY) * uAlpha);
      }`,
  });
  const pillar = new Mesh(new CylinderGeometry(0.0014, 0.0014, h, 6, 1, true), pillarMat);
  pillar.position.copy(normal.clone().multiplyScalar(CONFIG.radius + h / 2));
  pillar.quaternion.copy(orient);

  const hit = new Mesh(
    new SphereGeometry(0.032, 8, 8),
    new MeshBasicMaterial({ transparent: true, opacity: 0, depthWrite: false }),
  );
  hit.position.copy(surface);
  hit.userData.caseId = id;

  return { id, dot, dotMat, pillar, pillarMat, hit, pos: surface, popT: -1 };
}

/** 标记弹出动画（overshoot），主循环每帧调用 */
export function tickMarker(m: Marker, dt: number) {
  if (m.popT < 0) return;
  m.popT = Math.min(1, m.popT + dt / 0.55);
  const t = m.popT;
  // back-out overshoot
  const c1 = 1.70158, c3 = c1 + 1;
  const s = 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
  m.dot.scale.setScalar(Math.max(0.0001, s));
  m.pillarMat.uniforms.uAlpha.value = t * CONFIG.pillarAlpha;
  if (t >= 1) m.popT = -1 - 1e-9, m.dot.scale.setScalar(1); // 固定终态
}

export function buildBeacon() {
  const pos = lonLatToVec3(SHANGHAI[0], SHANGHAI[1], CONFIG.radius * 1.002);
  const mat = new MeshBasicMaterial({
    color: new Color(CONFIG.colors.beacon),
    transparent: true,
    opacity: 0,
  });
  const mesh = new Mesh(new SphereGeometry(0.022, 16, 16), mat);   // 放大源点，bloom 更亮、更醒目
  mesh.position.copy(pos);
  mesh.layers.enable(BLOOM_LAYER);
  return { mesh, material: mat, pos };
}

export interface Ping { mesh: Mesh; mat: ShaderMaterial; }

/** 上海源点的外扩声呐环（数枚错相位循环扩散，强化"从此处辐射"的观感） */
export function buildBeaconPings(count = 3): Ping[] {
  const normal = lonLatToVec3(SHANGHAI[0], SHANGHAI[1], 1).normalize();
  const pos = normal.clone().multiplyScalar(CONFIG.radius * 1.004);
  const quat = new Quaternion().setFromUnitVectors(Z_AXIS, normal); // 环面贴上海切平面
  const pings: Ping[] = [];
  for (let i = 0; i < count; i++) {
    const mat = new ShaderMaterial({
      transparent: true, depthWrite: false, depthTest: false,
      blending: AdditiveBlending,
      uniforms: {
        uColor: { value: new Color(CONFIG.colors.beacon) },
        uAlpha: { value: 0 },
      },
      vertexShader: /* glsl */ `
        void main() { gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
      fragmentShader: /* glsl */ `
        uniform vec3 uColor; uniform float uAlpha;
        void main() { gl_FragColor = vec4(uColor, uAlpha); }`,
    });
    const mesh = new Mesh(new RingGeometry(0.86, 1.0, 64), mat); // 细环，实际大小由 scale 控制
    mesh.position.copy(pos);
    mesh.quaternion.copy(quat);
    mesh.renderOrder = 9;
    mesh.layers.enable(BLOOM_LAYER);
    pings.push({ mesh, mat });
  }
  return pings;
}
