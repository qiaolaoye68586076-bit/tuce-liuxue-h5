// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// 纯静态输出（Cloudflare Pages 直接托管 dist/，无服务端运行时）
export default defineConfig({
  site: 'https://tuce.asia',
  output: 'static',
  vite: {
    plugins: [tailwindcss()],
  },
});
