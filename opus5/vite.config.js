import { defineConfig } from 'vite'
import { globSync } from 'glob'
import { resolve } from 'node:path'
import htmlIncludes from './plugins/html-includes.js'
import portableOutput from './plugins/portable-output.js'

const pages = Object.fromEntries(
  globSync('**/*.html', {
    ignore: ['node_modules/**', 'dist/**', 'src/partials/**'],
  }).map((file) => [file.replace(/\.html$/, '').replace(/\//g, '-'), resolve(file)])
)

export default defineConfig({
  // Relative Basis: der Build laeuft in jedem Unterverzeichnis und auch
  // direkt per Doppelklick ueber file://, ohne Server.
  base: './',
  appType: 'mpa',
  plugins: [htmlIncludes(), portableOutput()],
  build: {
    rollupOptions: { input: pages },
    modulePreload: false,
    cssCodeSplit: false,
    assetsInlineLimit: 2048,
    reportCompressedSize: true,
  },
  server: { open: true },
})
