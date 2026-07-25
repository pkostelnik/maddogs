/**
 * Erzeugt public/sitemap.xml aus den vorhandenen Seiten.
 * Aufruf: node scripts/build-sitemap.mjs
 */
import { globSync } from 'glob'
import { writeFile, readFile } from 'node:fs/promises'

const ORIGIN = 'https://www.mad-dogs-germany.de'

// Rechtstexte sind im Prototyp Entwuerfe und auf noindex gesetzt.
const EXCLUDE = ['/impressum/', '/datenschutz/', '/agb/']

const PRIORITY = { '/': '1.0', '/training/': '0.9', '/training/dogwalking/': '0.9', '/kontakt/': '0.8' }

const files = globSync('**/index.html', {
  ignore: ['node_modules/**', 'dist/**', 'src/**'],
})

const urls = []
for (const file of files) {
  const path = '/' + file.replace(/index\.html$/, '')
  if (EXCLUDE.includes(path)) continue

  const html = await readFile(file, 'utf8')
  if (/name="robots"[^>]*noindex/.test(html)) continue

  urls.push(path)
}

urls.sort((a, b) => a.length - b.length || a.localeCompare(b))

const today = new Date().toISOString().slice(0, 10)
const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls
  .map(
    (path) => `  <url>
    <loc>${ORIGIN}${path}</loc>
    <lastmod>${today}</lastmod>
    <priority>${PRIORITY[path] || '0.6'}</priority>
  </url>`
  )
  .join('\n')}
</urlset>
`

await writeFile('public/sitemap.xml', xml)
console.log(`sitemap.xml mit ${urls.length} URLs geschrieben.`)
