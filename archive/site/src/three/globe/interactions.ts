/**
 * 交互：拖拽旋转（惯性阻尼）/ 鼠标视差 / raycast hover / 点击 slerp 转向。
 * 只操作 rotX/rotY 两个数（主循环每帧写回 group.rotation），与自转统一。
 */
import { Raycaster, Vector2, Vector3 } from 'three';
import type { PerspectiveCamera, Mesh, Group } from 'three';
import { CONFIG } from './config';

export interface InteractionState {
  rotX: number;
  rotY: number;
  velX: number;
  velY: number;
  dragging: boolean;
  lastDragAt: number;       // performance.now()，用于恢复自转
  parallaxX: number;        // 目标视差（弧度）
  parallaxY: number;
  curParX: number;
  curParY: number;
  hoveredId: string | null;
  slerp: null | { fromX: number; fromY: number; toX: number; toY: number; t: number };
}

export function createInteractions(opts: {
  container: HTMLElement;
  camera: PerspectiveCamera;
  globe: Group;
  hits: Mesh[];
  onHover: (id: string | null, x: number, y: number) => void;
  onSelect: (id: string) => void;
}) {
  const { container, camera, hits } = opts;
  const st: InteractionState = {
    rotX: CONFIG.initialRotX, rotY: CONFIG.initialRotY,   // 太平洋视角初始姿态
    velX: 0, velY: 0,
    dragging: false, lastDragAt: 0,
    parallaxX: 0, parallaxY: 0, curParX: 0, curParY: 0,
    hoveredId: null, slerp: null,
  };

  const ray = new Raycaster();
  const ndc = new Vector2();
  let downX = 0, downY = 0, moved = false;
  let lastX = 0, lastY = 0;

  function toNdc(e: PointerEvent) {
    const r = container.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    return { px: e.clientX - r.left, py: e.clientY - r.top };
  }

  function pick(e: PointerEvent) {
    const { px, py } = toNdc(e);
    ray.setFromCamera(ndc, camera);
    const hit = ray.intersectObjects(hits, false)[0];
    const id = hit ? (hit.object.userData.caseId as string) : null;
    if (id !== st.hoveredId) {
      st.hoveredId = id;
      opts.onHover(id, px, py);
      container.style.cursor = id ? 'pointer' : 'grab';
    } else if (id) {
      opts.onHover(id, px, py);              // 同一目标也回传坐标（卡片跟随）
    }
  }

  function onDown(e: PointerEvent) {
    st.dragging = true;
    moved = false;
    downX = lastX = e.clientX;
    downY = lastY = e.clientY;
    container.setPointerCapture(e.pointerId);
    container.style.cursor = 'grabbing';
  }
  function onMove(e: PointerEvent) {
    // 视差目标（全 hero 范围）
    const r = container.getBoundingClientRect();
    const nx = ((e.clientX - r.left) / r.width) * 2 - 1;
    const ny = ((e.clientY - r.top) / r.height) * 2 - 1;
    const maxRad = (CONFIG.parallaxDeg * Math.PI) / 180;
    st.parallaxY = nx * maxRad;
    st.parallaxX = ny * maxRad * 0.7;

    if (st.dragging) {
      const dx = e.clientX - lastX;
      const dy = e.clientY - lastY;
      lastX = e.clientX; lastY = e.clientY;
      st.rotY += dx * 0.005;
      st.rotX = clamp(st.rotX + dy * 0.003, -0.55, 0.55);
      st.velY = dx * 0.005;
      st.velX = dy * 0.003;
      st.lastDragAt = performance.now();
      if (Math.abs(e.clientX - downX) + Math.abs(e.clientY - downY) > 6) moved = true;
    } else {
      pick(e);
    }
  }
  function onUp(e: PointerEvent) {
    st.dragging = false;
    st.lastDragAt = performance.now();
    container.style.cursor = st.hoveredId ? 'pointer' : 'grab';
    if (!moved && st.hoveredId) opts.onSelect(st.hoveredId);
  }
  function onLeave() {
    if (st.hoveredId) { st.hoveredId = null; opts.onHover(null, 0, 0); }
    st.parallaxX = st.parallaxY = 0;
  }

  container.addEventListener('pointerdown', onDown);
  container.addEventListener('pointermove', onMove, { passive: true });
  container.addEventListener('pointerup', onUp);
  container.addEventListener('pointerleave', onLeave);
  container.style.cursor = 'grab';
  container.style.touchAction = 'pan-y';

  /** 点击某校 → 计算让该点面向相机的目标姿态（yaw/pitch 解析解） */
  function faceTo(markerLocal: Vector3) {
    const m = markerLocal.clone().normalize();
    let toY = Math.atan2(-m.x, m.z);
    const mz = Math.hypot(m.x, m.z);
    const toX = clamp(Math.atan2(m.y, mz), -0.5, 0.5);
    // 取最近等价角（避免绕远路）
    const twoPi = Math.PI * 2;
    while (toY - st.rotY > Math.PI) toY -= twoPi;
    while (toY - st.rotY < -Math.PI) toY += twoPi;
    st.slerp = { fromX: st.rotX, fromY: st.rotY, toX, toY, t: 0 };
  }

  /** 主循环每帧调用：返回是否应暂停自转 */
  function tick(dt: number): boolean {
    // 点击转向动画
    if (st.slerp) {
      st.slerp.t = Math.min(1, st.slerp.t + dt / CONFIG.clickSlerpS);
      const e = easeInOut(st.slerp.t);
      st.rotX = st.slerp.fromX + (st.slerp.toX - st.slerp.fromX) * e;
      st.rotY = st.slerp.fromY + (st.slerp.toY - st.slerp.fromY) * e;
      if (st.slerp.t >= 1) st.slerp = null;
      return true;
    }
    // 惯性
    if (!st.dragging && (Math.abs(st.velX) > 1e-4 || Math.abs(st.velY) > 1e-4)) {
      st.rotY += st.velY;
      st.rotX = clamp(st.rotX + st.velX, -0.55, 0.55);
      st.velX *= CONFIG.inertiaDamping;
      st.velY *= CONFIG.inertiaDamping;
    }
    // 视差平滑
    st.curParX += (st.parallaxX - st.curParX) * CONFIG.parallaxLerp;
    st.curParY += (st.parallaxY - st.curParY) * CONFIG.parallaxLerp;

    const pauseSpin =
      st.dragging ||
      st.hoveredId !== null ||
      performance.now() - st.lastDragAt < CONFIG.resumeAfterDragMs;
    return pauseSpin;
  }

  function dispose() {
    container.removeEventListener('pointerdown', onDown);
    container.removeEventListener('pointermove', onMove);
    container.removeEventListener('pointerup', onUp);
    container.removeEventListener('pointerleave', onLeave);
  }

  return { st, tick, faceTo, dispose };
}

function clamp(v: number, a: number, b: number) { return Math.max(a, Math.min(b, v)); }
function easeInOut(t: number) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
