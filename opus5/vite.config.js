import { defineConfig } from 'vite'
import { globSync } from 'glob'
import { resolve } from 'node:path'
import htmlIncludes from './plugins/html-includes.js'

const pages = Object.fromEntries(
  globSync('**/*.html', {
    ignore: ['node_modules/**', 'dist/**', 'src/partials/**'],
  }).map((file) => [file.replace(/\.html$/, '').replace(/\//g, '-'), resolve(file)])
)

export default defineConfig({
  appType: 'mpa',
  plugins: [htmlIncludes()],
  build: {
    rollupOptions: { input: pages },
    cssCodeSplit: false,
    assetsInlineLimit: 2048,
    reportCompressedSize: true,
  },
  server: { open: true },
})
