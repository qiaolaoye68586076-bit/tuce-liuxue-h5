/**
 * 3D 录取地球 · 编排层（动态 import 的 chunk 入口）
 * init / 入场时间轴 / 脉冲引擎 / 待机重播 / 筛选 / RAF 生命周期 / dispose
 */
import {
  WebGLRenderer, Scene, PerspectiveCamera, Group, Clock, ColorManagement, Vector3,
  LinearSRGBColorSpace,
} from 'three';
import { CONFIG } from './config';
import { createDots, createSphere, createAtmosphere } from './globe';
import { buildArc, tickRipple, type Arc, type CaseInput } from './arcs';
import { buildMarker, tickMarker, buildBeacon, buildBeaconPings, type Marker } from './markers';
import { createPost } from './post';
import { createInteractions } from './interactions';

ColorManagement.enabled = false; // 全自定义 shader 风格化场景：所见 hex 即所得

interface Pulse { arc: Arc; t: number; dur: number; entrance: boolean }

export interface GlobeAPI {
  setFilter(region: string, year: string): void;
  destroy(): void;
  frameCount(): number;       // 供测试断言渲染循环状态
}

export async function createGlobe(opts: {
  container: HTMLElement;
  canvas: HTMLCanvasElement;
  cases: CaseInput[];
  dotsUrl: string;
  reduced: boolean;
  onHover: (id: string | null, x: number, y: number) => void;
}): Promise<GlobeAPI> {
  const { container, canvas, cases, reduced } = opts;

  /* ---------- 基础 ---------- */
  const renderer = new WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.outputColorSpace = LinearSRGBColorSpace; // 与 ColorManagement=false 配套：全链 WYSIWYG，内置材质不再被输出端提亮
  renderer.setClearColor(0x000000, 0);
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));

  const scene = new Scene();
  const camera = new PerspectiveCamera(CONFIG.fov, 1, 0.1, 20);
  camera.position.set(0, 0, CONFIG.cameraZ);

  const globe = new Group();
  scene.add(globe);

  /* ---------- 内容 ---------- */
  const dotsRaw: number[] = await fetch(opts.dotsUrl).then((r) => r.json());
  const dots = createDots(dotsRaw);
  const sphere = createSphere();
  sphere.mesh.layers.enable(1);               // 进 bloom pass 仅作遮挡（近黑不发光）
  const atmo = createAtmosphere();
  globe.add(sphere.mesh, atmo.mesh, dots.points);

  const arcs: Arc[] = cases.map(buildArc).sort((a, b) => a.angle - b.angle);
  const markers = new Map<string, Marker>();
  for (const c of cases) markers.set(c.id, buildMarker(c.id, c.coordinates));
  const beacon = buildBeacon();
  globe.add(beacon.mesh);
  const pings = buildBeaconPings(3);
  for (const p of pings) globe.add(p.mesh);
  for (const a of arcs) globe.add(a.line, a.head, a.ripple);
  for (const m of markers.values()) globe.add(m.dot, m.pillar, m.hit);

  const post = createPost(renderer, scene, camera);

  // 调试开关：?nopost 绕过 bloom 管线；?noatmo 隐藏大气层（隔离视觉问题用）
  const qs = new URLSearchParams(location.search);
  const noPost = qs.has('nopost');
  if (qs.has('noatmo')) atmo.mesh.visible = false;
  if (qs.has('nodots')) dots.points.visible = false;
  if (qs.has('rx')) (CONFIG as any).initialRotX = parseFloat(qs.get('rx')!);
  if (qs.has('ry')) (CONFIG as any).initialRotY = parseFloat(qs.get('ry')!);
  if (qs.has('nosphere')) sphere.mesh.visible = false;
  const renderFrame = noPost ? () => renderer.render(scene, camera) : post.render;

  /* ---------- 交互 ---------- */
  let hoverFocusId: string | null = null;
  function applyFocus() {
    for (const a of arcs) {
      if (!a.active) continue;
      a.lineMat.uniforms.uBaseAlpha.value =
        hoverFocusId === null ? CONFIG.arc.baseAlpha
        : a.id === hoverFocusId ? 1.0
        : CONFIG.arc.dimAlpha;
    }
  }
  const inter = reduced
    ? null
    : createInteractions({
        container, camera, globe,
        hits: [...markers.values()].map((m) => m.hit),
        onHover: (id, x, y) => {
          hoverFocusId = id;
          applyFocus();
          opts.onHover(id, x, y);
        },
        onSelect: (id) => {
          const m = markers.get(id);
          if (m && inter) inter.faceTo(m.pos);
        },
      });

  /* ---------- 入场时间轴（Clock 驱动，无动画库） ---------- */
  const E = CONFIG.entrance;
  const pulses: Pulse[] = [];
  // stagger 随弧线数自适应（59 校时 ~0.034s/条，总入场仍 <5s）
  const stagger = Math.min(E.arcStagger, 2.0 / Math.max(1, arcs.length));
  const arcStart = (i: number) => E.startDelay + E.globeIn * 0.7 + i * stagger;
  const entranceTotal = arcStart(arcs.length - 1) + E.arcDraw + 0.4;
  let elapsed = 0;
  let entranceDone = reduced;
  let nextIdleAt = Infinity;

  function easeOut(t: number) { return 1 - Math.pow(1 - t, 3); }

  function setFinalState() {
    dots.material.uniforms.uOpacity.value = 1;
    sphere.material.opacity = 0.94;
    atmo.material.uniforms.uIntensity.value = CONFIG.atmosphereIntensity;
    beacon.material.opacity = 1;
    globe.scale.setScalar(1);
    for (const a of arcs) a.lineMat.uniforms.uProgress.value = 1;
    for (const m of markers.values()) {
      m.dot.scale.setScalar(1);
      m.pillarMat.uniforms.uAlpha.value = CONFIG.pillarAlpha;
    }
  }

  function tickEntrance() {
    const gT = Math.min(1, Math.max(0, (elapsed - E.startDelay) / E.globeIn));
    const g = easeOut(gT);
    dots.material.uniforms.uOpacity.value = g;
    sphere.material.opacity = g * 0.94;
    atmo.material.uniforms.uIntensity.value = g * CONFIG.atmosphereIntensity;
    beacon.material.opacity = g;
    globe.scale.setScalar(0.92 + 0.08 * g);

    arcs.forEach((a, i) => {
      const t0 = arcStart(i);
      if (elapsed < t0) return;
      const p = Math.min(1, (elapsed - t0) / E.arcDraw);
      const eased = easeOut(p);
      a.lineMat.uniforms.uProgress.value = eased;
      // 入场期间脉冲头随描线头部
      a.lineMat.uniforms.uPulseT.value = eased;
      a.head.position.copy(a.getPoint(eased));
      a.headMat.opacity = p < 1 ? 0.95 : 0;
      if (p >= 1 && a.rippleT < 0 && !a.line.userData.arrived) {
        a.line.userData.arrived = true;
        a.rippleT = 0;
        const m = markers.get(a.id);
        if (m) m.popT = 0;
        a.lineMat.uniforms.uPulseT.value = -10;
      }
    });

    if (elapsed >= entranceTotal) {
      entranceDone = true;
      scheduleIdle();
    }
  }

  /* ---------- 待机脉冲 ---------- */
  function scheduleIdle() {
    nextIdleAt = elapsed + CONFIG.idle.minGapS + Math.random() * (CONFIG.idle.maxGapS - CONFIG.idle.minGapS);
  }
  function tickIdle() {
    if (!entranceDone || elapsed < nextIdleAt) return;
    const candidates = arcs.filter((a) => a.active && !pulses.some((p) => p.arc === a));
    if (candidates.length) {
      const arc = candidates[(Math.random() * candidates.length) | 0];
      pulses.push({ arc, t: 0, dur: CONFIG.idle.pulseDurS, entrance: false });
    }
    scheduleIdle();
  }
  function tickPulses(dt: number) {
    const lit: Vector3[] = [];
    for (let i = pulses.length - 1; i >= 0; i--) {
      const p = pulses[i];
      p.t += dt / p.dur;
      if (p.t >= 1) {
        p.arc.lineMat.uniforms.uPulseT.value = -10;
        p.arc.headMat.opacity = 0;
        p.arc.rippleT = 0;
        pulses.splice(i, 1);
        continue;
      }
      p.arc.lineMat.uniforms.uPulseT.value = p.t;
      const pos = p.arc.getPoint(p.t);
      p.arc.head.position.copy(pos);
      p.arc.headMat.opacity = Math.sin(Math.PI * p.t) * 0.95;
      lit.push(pos);
    }
    // 弧线经过区域的点阵提亮
    const u = dots.material.uniforms;
    u.uPulseCount.value = Math.min(6, lit.length);
    for (let i = 0; i < Math.min(6, lit.length); i++) (u.uPulses.value[i] as Vector3).copy(lit[i]);
  }

  /* ---------- 筛选 ---------- */
  const shown = new Map<string, boolean>(arcs.map((a) => [a.id, true]));
  const fades: { mat: { value: number } | null; from: number; to: number; t: number; dur: number; apply: (v: number) => void }[] = [];
  function fade(apply: (v: number) => void, from: number, to: number, dur = 0.4) {
    fades.push({ mat: null, from, to, t: 0, dur, apply });
  }
  function tickFades(dt: number) {
    for (let i = fades.length - 1; i >= 0; i--) {
      const f = fades[i];
      f.t = Math.min(1, f.t + dt / f.dur);
      f.apply(f.from + (f.to - f.from) * easeOut(f.t));
      if (f.t >= 1) fades.splice(i, 1);
    }
  }
  function setFilter(region: string, year: string) {
    let replayIdx = 0;
    for (const a of arcs) {
      const ok = (region === 'all' || a.region === region) && (year === 'all' || a.years.includes(+year));
      const was = shown.get(a.id)!;
      const m = markers.get(a.id)!;
      if (ok === was) continue;
      shown.set(a.id, ok);
      a.active = ok;
      m.hit.visible = ok;
      if (!ok) {
        fade((v) => { a.lineMat.uniforms.uBaseAlpha.value = v; }, a.lineMat.uniforms.uBaseAlpha.value as number, 0);
        fade((v) => { m.dot.scale.setScalar(Math.max(1e-4, v)); m.pillarMat.uniforms.uAlpha.value = v * CONFIG.pillarAlpha; }, 1, 0, 0.35);
        a.headMat.opacity = 0;
        a.lineMat.uniforms.uPulseT.value = -10;
      } else {
        // 重播入场：描线 + 脉冲 + 落点
        a.lineMat.uniforms.uBaseAlpha.value = CONFIG.arc.baseAlpha;
        a.lineMat.uniforms.uProgress.value = 0;
        a.line.userData.arrived = false;
        const delay = replayIdx++ * 0.08;
        fade((v) => {
          a.lineMat.uniforms.uProgress.value = v;
          a.lineMat.uniforms.uPulseT.value = v;
          a.head.position.copy(a.getPoint(Math.min(1, v)));
          a.headMat.opacity = v > 0 && v < 1 ? 0.95 : 0;
          if (v >= 1 && !a.line.userData.arrived) {
            a.line.userData.arrived = true;
            a.rippleT = 0;
            m.popT = 0;
            a.lineMat.uniforms.uPulseT.value = -10;
          }
        }, -delay * (1 / 1.1), 1, 1.1 + delay);
      }
    }
  }

  /* ---------- 主循环 ---------- */
  const clock = new Clock();
  let frames = 0;
  let rafId = 0;
  let running = false;
  let spin = 0;
  const spinSpeed = (Math.PI * 2) / CONFIG.rotationSecsPerTurn;

  function frame() {
    rafId = requestAnimationFrame(frame);
    // 时间轴用墙钟（低帧率设备入场仍按真实时间推进）；dt 钳制只用于物理/动画步进
    const now = clock.getElapsedTime();
    const dt = Math.min(0.1, now - elapsed);
    elapsed = now;
    frames++;

    if (!entranceDone) tickEntrance();
    tickIdle();
    tickPulses(dt);
    tickFades(dt);
    for (const a of arcs) tickRipple(a, dt);
    for (const m of markers.values()) tickMarker(m, dt);

    // 上海源点呼吸（3s）
    const breathe = Math.sin((elapsed * Math.PI * 2) / CONFIG.beaconBreathSecs);
    beacon.mesh.scale.setScalar(1 + 0.22 * breathe);
    if (entranceDone) beacon.material.opacity = 0.78 + 0.22 * breathe;

    // 上海源点：外扩声呐环（3 枚错相位循环，强化"从此处辐射"）
    const pingVis = entranceDone ? 1 : 0;
    const PING_DUR = 2.8;
    for (let i = 0; i < pings.length; i++) {
      const ph = (elapsed / PING_DUR + i / pings.length) % 1;
      pings[i].mesh.scale.setScalar(0.018 + ph * 0.13);            // 世界尺度由内向外扩散
      pings[i].mat.uniforms.uAlpha.value = (1 - ph) * (1 - ph) * 0.55 * pingVis; // 外扩渐隐
    }

    // 姿态：拖拽/视差/自转
    let pauseSpin = false;
    if (inter) pauseSpin = inter.tick(dt);
    if (!pauseSpin && entranceDone) spin += spinSpeed * dt;
    if (inter) {
      globe.rotation.x = inter.st.rotX + inter.st.curParX;
      globe.rotation.y = inter.st.rotY + spin + inter.st.curParY;
    } else {
      globe.rotation.x = CONFIG.initialRotX;
      globe.rotation.y = CONFIG.initialRotY + spin;
    }

    // 相机 idle 微浮
    camera.position.y = Math.sin(elapsed * 0.5) * CONFIG.idleFloatAmp;
    camera.lookAt(0, 0, 0);

    renderFrame();
  }
  function start() { if (!running && !reduced) { running = true; clock.getDelta(); rafId = requestAnimationFrame(frame); } }
  function stop() { running = false; cancelAnimationFrame(rafId); }

  /* ---------- 尺寸 ---------- */
  function resize() {
    const w = container.clientWidth, h = container.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    post.setSize(w, h);
    dots.material.uniforms.uScale.value = (h * Math.min(devicePixelRatio || 1, 2)) / 2;
    if (reduced) renderFrame();
  }
  const ro = new ResizeObserver(resize);
  ro.observe(container);
  resize();

  /* ---------- 生命周期 ---------- */
  const onVis = () => { document.hidden ? stop() : start(); };
  document.addEventListener('visibilitychange', onVis);
  const io = new IntersectionObserver((en) => { en[0].isIntersecting ? start() : stop(); }, { threshold: 0.02 });
  io.observe(container);

  if (reduced) {
    setFinalState();
    globe.rotation.set(CONFIG.initialRotX, CONFIG.initialRotY, 0);
    renderFrame();                              // 单帧静态
  } else {
    start();
  }

  function destroy() {
    stop();
    document.removeEventListener('visibilitychange', onVis);
    ro.disconnect();
    io.disconnect();
    inter?.dispose();
    scene.traverse((o: any) => {
      o.geometry?.dispose?.();
      if (o.material) (Array.isArray(o.material) ? o.material : [o.material]).forEach((m: any) => m.dispose?.());
    });
    post.dispose();
    renderer.dispose();
  }

  return { setFilter, destroy, frameCount: () => frames };
}
