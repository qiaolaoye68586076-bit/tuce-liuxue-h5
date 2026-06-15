/**
 * Selective Bloom 管线（layers 隔离）：
 *   Layer 1（BLOOM）仅：脉冲头 / 落点涟漪 / 上海源点 + 内球（近黑，仅用于遮挡，
 *   亮度低于 threshold 不发光——这样脉冲转到地球背面不会透球泛光）。
 *   bloom pass 用 camera.layers 只渲 BLOOM 层 → UnrealBloomPass →
 *   final pass 正常渲全场景后加法合成。无需材质交换。
 */
import { Vector2, ShaderMaterial } from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import type { WebGLRenderer, Scene, PerspectiveCamera } from 'three';
import { CONFIG, BLOOM_LAYER } from './config';

export function createPost(renderer: WebGLRenderer, scene: Scene, camera: PerspectiveCamera) {
  const size = renderer.getSize(new Vector2());

  const bloomComposer = new EffectComposer(renderer);
  bloomComposer.renderToScreen = false;
  bloomComposer.addPass(new RenderPass(scene, camera));
  const bloomPass = new UnrealBloomPass(
    size.clone().multiplyScalar(0.5),          // half-res，足够柔
    CONFIG.bloom.strength,
    CONFIG.bloom.radius,
    CONFIG.bloom.threshold,
  );
  bloomComposer.addPass(bloomPass);

  const finalComposer = new EffectComposer(renderer);
  finalComposer.addPass(new RenderPass(scene, camera));
  const composite = new ShaderPass(
    new ShaderMaterial({
      uniforms: {
        tDiffuse: { value: null },
        uBloom: { value: bloomComposer.renderTarget2.texture },
      },
      transparent: true,
      vertexShader: /* glsl */ `
        varying vec2 vUv;
        void main() { vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }`,
      fragmentShader: /* glsl */ `
        uniform sampler2D tDiffuse, uBloom;
        varying vec2 vUv;
        void main() {
          vec4 base = texture2D(tDiffuse, vUv);
          vec3 glow = texture2D(uBloom, vUv).rgb;
          float gl = dot(glow, vec3(0.299, 0.587, 0.114));
          gl_FragColor = vec4(base.rgb + glow, clamp(base.a + gl, 0.0, 1.0));
        }`,
    }),
    'tDiffuse',
  );
  finalComposer.addPass(composite);

  function render() {
    camera.layers.set(BLOOM_LAYER);
    bloomComposer.render();
    camera.layers.set(0);
    camera.layers.enable(BLOOM_LAYER);        // 基础渲染包含双层对象（头/涟漪本体）
    finalComposer.render();
    camera.layers.set(0);
  }

  function setSize(w: number, h: number) {
    bloomComposer.setSize(w, h);
    finalComposer.setSize(w, h);
  }

  function dispose() {
    bloomComposer.dispose();
    finalComposer.dispose();
    bloomPass.dispose();
  }

  return { render, setSize, dispose, bloomPass };
}
