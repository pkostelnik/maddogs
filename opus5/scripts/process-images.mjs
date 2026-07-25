/**
 * Benennt die heruntergeladenen Originalbilder sprechend um, erzeugt
 * responsive AVIF/WebP/JPEG-Varianten und schreibt das Bildmanifest.
 *
 * Aufruf: node scripts/process-images.mjs
 */
import sharp from 'sharp'
import { mkdir, writeFile } from 'node:fs/promises'
import { existsSync } from 'node:fs'

const SRC = 'src/assets/images/original'
const OUT = 'src/assets/images'

/** uuid -> { name, alt, widths, formats } */
const MAP = {
  '72f4bee1-298d-4691-8647-9c872bdfbace': {
    name: 'logo-mad-dogs',
    alt: 'Logo Mad Dogs – Search and Workingdogs, gegründet 2023',
    widths: [96, 192, 384],
  },
  '999a8712-f19c-4bcf-9279-eadd998d021b': {
    name: 'logo-mad-dogs-alt',
    alt: 'Alternatives Mad-Dogs-Emblem mit Malinois-Portrait',
    widths: [192, 384],
  },
  '31d79bb4-5812-4317-ad5e-16cca65360e0': {
    name: 'logo-dogwalker-ndk',
    alt: 'Emblem Dogwalker NDK – Mad Dogs Niederkassel',
    widths: [240, 480, 720],
  },
  '3163b231-b6d5-4132-8d6a-c7135790430d': {
    name: 'hero-malinois-wiese',
    alt: 'Malinois liegt aufmerksam in einer blühenden Sommerwiese',
    widths: [640, 1024, 1600, 2000],
  },
  'b69a418b-cca5-4208-aa5e-9b13135dae47': {
    name: 'chris-fuehrt-malinois',
    alt: 'Chris führt einen Malinois an lockerer Leine über eine Straße',
    widths: [480, 800, 1333],
  },
  '108822df-b035-41c9-b645-921e73671901': {
    name: 'chris-mit-hund-umarmung',
    alt: 'Malinois springt Chris in die Arme, beide sichtlich vertraut',
    widths: [480, 690],
  },
  '29e1540b-aeb2-4a5a-9632-abbeb4c30d9c': {
    name: 'training-platzarbeit',
    alt: 'Chris arbeitet auf dem Hundeplatz konzentriert mit einem Hund',
    widths: [402],
  },
  '27f5f508-2d5b-40c9-a51f-3d7e27410a7d': {
    name: 'chris-portrait-hund',
    alt: 'Chris mit seinem schwarzen Schäferhund-Mischling im Freien',
    widths: [480, 800, 1500],
  },
  'd07fbcbf-17d3-40ae-9ce8-c394eb495c9d': {
    name: 'malinois-wald-fels',
    alt: 'Malinois sitzt auf einem bemoosten Felsen im Wald',
    widths: [480, 800, 1428],
  },
  '405ce143-79cf-4f43-ad09-a42da9da73cf': {
    name: 'hund-geschirr-einsatz',
    alt: 'Schwarzer Hund mit taktischem Arbeitsgeschirr im Gras',
    widths: [480, 800, 1500],
  },
  '59871152-e7af-40a9-b7c4-405306ec6f4b': {
    name: 'galerie-golden-retriever',
    alt: 'Golden Retriever blickt im Abendlicht erwartungsvoll nach oben',
    widths: [480, 800],
  },
  '8abf05db-4f7d-41f0-ad66-65ac521cd5a3': {
    name: 'galerie-hund-maulkorb',
    alt: 'Hund mit Maulkorb auf einem Feldweg, im Hintergrund ein zweiter Hund',
    widths: [480, 800],
  },
  '9a9da8ca-81af-4941-a3da-fe2ad290026b': {
    name: 'galerie-mischling-weg',
    alt: 'Aufmerksamer Mischling steht auf einem Schotterweg',
    widths: [480, 800],
  },
  '18111972-8cd4-84eb-876b-28b52fb90cd3': {
    name: 'galerie-pinscher-feld',
    alt: 'Pinscher-Mischling läuft ausgelassen durch ein Sommerfeld',
    widths: [480, 800],
  },
  '18111972-8cd4-44eb-876b-28b52fb90cd3': {
    name: 'galerie-pinscher-feld',
    alt: 'Pinscher-Mischling läuft ausgelassen durch ein Sommerfeld',
    widths: [480, 800],
  },
  'b6616ef5-e952-49db-b0c8-83852ccf74fc': {
    name: 'galerie-weisser-hund',
    alt: 'Weißer Hund lacht in die Kamera, dahinter ein weiter Himmel',
    widths: [480, 800],
  },
  '627b6baf-8aa8-49da-a374-82d818d00242': {
    name: 'galerie-hund-im-auto',
    alt: 'Malinois liegt entspannt auf dem Beifahrersitz',
    widths: [480, 800],
  },
  '08e641e5-bf06-4025-8aae-2fc80916bf64': {
    name: 'logo-reico-partner',
    alt: 'Partnerlogo Reico Vital-Systeme',
    widths: [200, 400],
  },
}

const EXTS = ['jpg', 'png']

async function findSource(uuid) {
  for (const ext of EXTS) {
    const p = `${SRC}/${uuid}.${ext}`
    if (existsSync(p)) return p
  }
  return null
}

async function main() {
  await mkdir(OUT, { recursive: true })
  const manifest = {}
  const seen = new Set()

  for (const [uuid, cfg] of Object.entries(MAP)) {
    if (seen.has(cfg.name)) continue
    const src = await findSource(uuid)
    if (!src) continue
    seen.add(cfg.name)

    const meta = await sharp(src).metadata()
    const variants = { avif: [], webp: [], fallback: null }
    const widths = cfg.widths.filter((w) => w <= meta.width)
    if (!widths.length) widths.push(meta.width)

    for (const w of widths) {
      const base = sharp(src).resize({ width: w, withoutEnlargement: true })
      await base.clone().avif({ quality: 55, effort: 6 }).toFile(`${OUT}/${cfg.name}-${w}.avif`)
      await base.clone().webp({ quality: 74 }).toFile(`${OUT}/${cfg.name}-${w}.webp`)
      variants.avif.push({ w, src: `/src/assets/images/${cfg.name}-${w}.avif` })
      variants.webp.push({ w, src: `/src/assets/images/${cfg.name}-${w}.webp` })
    }

    const fallbackWidth = widths[widths.length - 1]
    // `hasAlpha` ist bei vielen PNG-Fotos gesetzt, obwohl sie deckend sind.
    // Nur echte Transparenz rechtfertigt den teureren PNG-Fallback.
    const isTransparent = meta.hasAlpha && !(await sharp(src).stats()).isOpaque
    const fallbackExt = isTransparent ? 'png' : 'jpg'
    const pipe = sharp(src).resize({ width: fallbackWidth, withoutEnlargement: true })
    if (isTransparent) {
      await pipe.png({ compressionLevel: 9, palette: true }).toFile(`${OUT}/${cfg.name}.png`)
    } else {
      await pipe.jpeg({ quality: 78, mozjpeg: true }).toFile(`${OUT}/${cfg.name}.jpg`)
    }
    variants.fallback = `/src/assets/images/${cfg.name}.${fallbackExt}`

    const ratio = meta.height / meta.width
    manifest[cfg.name] = {
      alt: cfg.alt,
      width: fallbackWidth,
      height: Math.round(fallbackWidth * ratio),
      ...variants,
    }
    console.log(`${cfg.name}: ${widths.join('/')} px`)
  }

  await writeFile('src/content/images.json', JSON.stringify(manifest, null, 2) + '\n')
  console.log(`\nManifest: ${Object.keys(manifest).length} Bilder`)
}

main()
