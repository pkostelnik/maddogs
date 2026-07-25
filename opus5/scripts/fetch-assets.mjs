/**
 * Lädt die Originalbilder der Bestandsseite einmalig herunter.
 * Aufruf: node scripts/fetch-assets.mjs
 */
import { mkdir, writeFile } from 'node:fs/promises'
import { existsSync } from 'node:fs'

const ORIGIN = 'https://www.mad-dogs-germany.de'
const OUT = 'src/assets/images/original'

const PAGES = [
  '/',
  '/ueber-uns/',
  '/dogwalker-service/',
  '/dogwalker-service/galerie/',
  '/man-pet-trail/',
  '/spuerhunde/',
  '/sporthunde/',
  '/reico-hundefutter/',
  '/das-sagen-unsere-kunden/',
  '/mad-dogs-shop-/',
]

const uuidRe = /go-x\/u\/([0-9a-f-]{36})\/(?:[a-z0-9,]+\/)?image(?:-\d+x\d+)?\.(jpg|jpeg|png)/gi

async function collect() {
  const found = new Map()
  for (const page of PAGES) {
    let html
    try {
      const res = await fetch(ORIGIN + page)
      if (!res.ok) continue
      html = await res.text()
    } catch {
      continue
    }
    for (const m of html.matchAll(uuidRe)) {
      const [, uuid, ext] = m
      if (uuid === 'image-placeholder') continue
      found.set(uuid, ext.toLowerCase() === 'jpeg' ? 'jpg' : ext.toLowerCase())
    }
  }
  return found
}

async function main() {
  await mkdir(OUT, { recursive: true })
  const assets = await collect()
  console.log(`${assets.size} Bilder gefunden.`)
  let ok = 0
  for (const [uuid, ext] of assets) {
    const target = `${OUT}/${uuid}.${ext}`
    if (existsSync(target)) {
      ok++
      continue
    }
    const url = `${ORIGIN}/wp-content/uploads/go-x/u/${uuid}/image.${ext}`
    const res = await fetch(url)
    if (!res.ok) {
      console.warn(`  fehlgeschlagen: ${uuid} (${res.status})`)
      continue
    }
    await writeFile(target, Buffer.from(await res.arrayBuffer()))
    ok++
    console.log(`  ${uuid}.${ext}`)
  }
  console.log(`${ok} Bilder liegen unter ${OUT}/`)
}

main()
