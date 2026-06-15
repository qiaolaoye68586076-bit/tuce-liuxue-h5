/**
 * 地球本体：点阵陆地（单 Points 一次 draw call）+ 深色内球 + Fresnel 大气边缘光。
 */
import {
  BufferGeometry, Float32BufferAttribute, Points, ShaderMaterial, Color,
  Mesh, SphereGeometry, MeshBasicMaterial, AdditiveBlending, Vector3,
} from 'three';
import { CONFIG } from './config';

const DEG = Math.PI / 180;

/** 经纬度 → 球面坐标（globe 本地空间） */
export function lonLatToVec3(lon: number, lat: number, r: number): Vector3 {
  const phi = lat * DEG;
  const theta = lon * DEG;
  return new Vector3(
    r * Math.cos(phi) * Math.cos(theta),
    r * Math.sin(phi),
    -r * Math.cos(phi) * Math.sin(theta),
  );
}

export function createDots(dotsRaw: number[]) {
  const R = CONFIG.radius;
  const n = dotsRaw.length / 2;
  const positions = new Float32Array(n * 3);
  const rand = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    const v = lonLatToVec3(dotsRaw[i * 2] / 10, dotsRaw[i * 2 + 1] / 10, R);
    positions[i * 3] = v.x;
    positions[i * 3 + 1] = v.y;
    positions[i * 3 + 2] = v.z;
    rand[i] = Math.random();
  }
  const geo = new BufferGeometry();
  geo.setAttribute('position', new Float32BufferAttribute(positions, 3));
  geo.setAttribute('aRand', new Float32BufferAttribute(rand, 1));

  const mat = new ShaderMaterial({
    transparent: true,
    depthWrite: false,
    uniforms: {
      uSize: { value: CONFIG.dots.size },
      uScale: { value: 400 },                 // resize 时更新：canvasHeight/2
      uOpacity: { value: 0 },                 // 入场淡入
      uColor: { value: new Color(CONFIG.colors.dot) },
      uColorLit: { value: new Color(CONFIG.colors.dotLit) },
      uPulses: { value: Array.from({ length: 6 }, () => new Vector3(99, 99, 99)) },
      uPulseCount: { value: 0 },
      uLitRadius: { value: CONFIG.dots.litRadius },
    },
    vertexShader: /* glsl */ `
      attribute float aRand;
      uniform float uSize, uScale, uPulseCount, uLitRadius;
      uniform vec3 uPulses[6];
      varying float vBoost, vFace, vRand;
      void main() {
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        float boost = 0.0;
        for (int i = 0; i < 6; i++) {
          if (float(i) >= uPulseCount) break;
          float d = distance(position, uPulses[i]);
          boost += smoothstep(uLitRadius, 0.0, d);
        }
        vBoost = min(boost, 1.0);
        vec3 nView = normalize(normalMatrix * normalize(position));
        vFace = smoothstep(-0.08, 0.35, nView.z);   // 球缘柔和消隐
        vRand = aRand;
        gl_PointSize = uSize * (uScale / -mv.z) * (0.8 + 0.4 * aRand) * (1.0 + 0.5 * vBoost);
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: /* glsl */ `
      uniform vec3 uColor, uColorLit;
      uniform float uOpacity;
      varying float vBoost, vFace, vRand;
      void main() {
        float d = length(gl_PointCoord - 0.5);
        float a = smoothstep(0.5, 0.3, d);
        if (a < 0.01) discard;
        vec3 col = mix(uColor, uColorLit, vBoost * 0.9);
        gl_FragColor = vec4(col, a * uOpacity * vFace * (0.8 + 0.2 * vRand));
      }`,
  });
  return { points: new Points(geo, mat), material: mat };
}

export function createSphere() {
  // 近不可见深色球面：写深度，遮挡背面点阵/弧线/脉冲
  const mat = new MeshBasicMaterial({
    color: new Color(CONFIG.colors.sphere),
    transparent: true,
    opacity: 0,
  });
  const mesh = new Mesh(new SphereGeometry(CONFIG.radius * 0.992, 48, 48), mat);
  return { mesh, material: mat };
}

export function createAtmosphere() {
  // FrontSide 边缘 fresnel：视线掠射角（球缘）泛极淡墨绿光晕，球心透明
  const mat = new ShaderMaterial({
    transparent: true,
    depthWrite: false,
    depthTest: false,
    blending: AdditiveBlending,
    uniforms: {
      uColor: { value: new Color(CONFIG.colors.atmosphere) },
      uIntensity: { value: 0 },                // 入场淡入 → CONFIG.atmosphereIntensity
    },
    vertexShader: /* glsl */ `
      varying vec3 vN, vP;
      void main() {
        vN = normalize(normalMatrix * normal);
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        vP = mv.xyz;
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: /* glsl */ `
      uniform vec3 uColor;
      uniform float uIntensity;
      varying vec3 vN, vP;
      void main() {
        // 视线与法线夹角越大（球缘）越亮；球心 → 0
        float rim = 1.0 - abs(dot(normalize(-vP), normalize(vN)));
        float fres = pow(rim, 3.5);
        gl_FragColor = vec4(uColor, fres * uIntensity);
      }`,
  });
  const mesh = new Mesh(new SphereGeometry(CONFIG.radius * 1.018, 48, 48), mat);
  mesh.renderOrder = 10;                       // 最后叠加，纯 halo
  return { mesh, material: mat };
}
