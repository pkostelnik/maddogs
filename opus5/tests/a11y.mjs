/**
 * Barrierefreiheits- und Tastaturprüfung über alle Seiten.
 * Aufruf: node tests/a11y.mjs  (Preview-Server muss auf Port 4321 laufen)
 */
import { chromium } from 'playwright'
import AxeBuilder from '@axe-core/playwright'

const BASE = process.env.BASE_URL || 'http://localhost:4321'

const PAGES = [
  '/',
  '/training/',
  '/training/dogwalking/',
  '/training/man-pet-trail/',
  '/training/spuerhunde/',
  '/training/sporthunde/',
  '/shop/',
  '/shop/halsbaender/',
  '/ernaehrung/',
  '/ueber-uns/',
  '/kundenstimmen/',
  '/galerie/',
  '/kontakt/',
  '/impressum/',
  '/datenschutz/',
  '/agb/',
]

const browser = await chromium.launch()
let violations = 0
let checked = 0

for (const theme of ['dark', 'light']) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    colorScheme: theme,
  })

  for (const path of PAGES) {
    const page = await context.newPage()
    await page.goto(BASE + path, { waitUntil: 'networkidle' })

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'])
      .analyze()

    checked++
    if (results.violations.length) {
      violations += results.violations.length
      console.log(`\n✗ ${theme} ${path}`)
      for (const v of results.violations) {
        console.log(`   [${v.impact}] ${v.id}: ${v.help}`)
        v.nodes.slice(0, 3).forEach((n) => console.log(`      ${n.target.join(' ')}`))
      }
    }
    await page.close()
  }
  await context.close()
}

// --- Strukturprüfungen, die axe nicht abdeckt -----------------------------
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } })
const page = await context.newPage()
const structural = []

for (const path of PAGES) {
  await page.goto(BASE + path, { waitUntil: 'domcontentloaded' })

  const info = await page.evaluate(() => {
    const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map((h) =>
      Number(h.tagName[1])
    )
    let skips = 0
    for (let i = 1; i < headings.length; i++) {
      if (headings[i] - headings[i - 1] > 1) skips++
    }
    const desc = document.querySelector('meta[name="description"]')?.content || ''
    return {
      h1: document.querySelectorAll('h1').length,
      skips,
      title: document.title,
      descLen: desc.length,
      main: document.querySelectorAll('main').length,
      skip: !!document.querySelector('.skip-link'),
      lang: document.documentElement.lang,
      imgsNoAlt: [...document.querySelectorAll('img')].filter((i) => !i.hasAttribute('alt')).length,
      // Das Lightbox-Bild ist ausgenommen: Seitenverhaeltnisse variieren, und
      // als Overlay kann es kein Layout verschieben.
      imgsNoDim: [...document.querySelectorAll('img:not([data-lightbox-image])')].filter(
        (i) => !i.hasAttribute('width') || !i.hasAttribute('height')
      ).length,
      unresolved: document.documentElement.innerHTML.includes('#include'),
    }
  })

  const problems = []
  if (info.h1 !== 1) problems.push(`h1-Anzahl ${info.h1}`)
  if (info.skips) problems.push(`${info.skips} Sprünge in der Überschriftenhierarchie`)
  if (info.main !== 1) problems.push(`main-Anzahl ${info.main}`)
  if (!info.skip) problems.push('Skip-Link fehlt')
  if (info.lang !== 'de') problems.push(`lang="${info.lang}"`)
  if (info.imgsNoAlt) problems.push(`${info.imgsNoAlt} Bilder ohne alt`)
  if (info.imgsNoDim) problems.push(`${info.imgsNoDim} Bilder ohne width/height`)
  if (info.descLen < 50 || info.descLen > 165)
    problems.push(`Meta-Description ${info.descLen} Zeichen`)
  if (info.unresolved) problems.push('nicht aufgelöste Include-Direktive')
  if (problems.length) structural.push(`✗ ${path}: ${problems.join(', ')}`)
}

// Transliterierte Umlaute in sichtbarem Text. Kuratierte Liste statt Heuristik,
// damit echte Woerter wie "aktuell" oder "Rasse" nicht faelschlich anschlagen.
const TRANSLIT =
  /\b(ueber|Ueber|fuer|Fuer|koenn\w*|Koenn\w*|naechst\w*|klaeren|Gespraech\w*|laeuft|wofuer|Ausruestung|Erzaehl\w*|traegt|muessen|waere|gehoert|moecht\w*|Groesse|draussen|regelmaessig|heisst|weisst|schliesslich|Spuerhund\w*|Ernaehrung|Halsbaender|Datenschutzerklaerung|Gelaendelauf|Oesterreich|Hundefuehrung|Diensthundefuehrer)\b/

for (const path of PAGES) {
  await page.goto(BASE + path, { waitUntil: 'domcontentloaded' })
  const found = await page.evaluate(
    (src) => {
      const re = new RegExp(src, 'g')
      const hits = new Set()
      for (const m of (document.body.innerText || '').matchAll(re)) hits.add(m[0])
      const title = document.title.match(re)
      if (title) title.forEach((t) => hits.add(t + ' (Titel)'))
      const desc = document.querySelector('meta[name="description"]')?.content || ''
      for (const m of desc.matchAll(re)) hits.add(m[0] + ' (Description)')
      return [...hits]
    },
    TRANSLIT.source.replace(/^\\b|\\b$/g, '\\b')
  )
  if (found.length) structural.push(`✗ ${path}: transliterierte Umlaute: ${found.join(', ')}`)
}

// Tastaturbedienung des Mobile-Menüs
await page.setViewportSize({ width: 390, height: 844 })
await page.goto(BASE + '/', { waitUntil: 'networkidle' })
await page.click('[data-nav-toggle]')
const drawerOpen = await page.getAttribute('[data-nav-drawer]', 'data-open')
await page.keyboard.press('Escape')
const drawerClosed = await page.getAttribute('[data-nav-drawer]', 'data-open')
const focusBack = await page.evaluate(
  () => document.activeElement?.getAttribute('data-nav-toggle') !== null
)
if (drawerOpen !== 'true') structural.push('✗ Mobile-Menü öffnet nicht')
if (drawerClosed !== 'false') structural.push('✗ Escape schließt das Mobile-Menü nicht')
if (!focusBack) structural.push('✗ Fokus kehrt nach dem Schließen nicht zum Auslöser zurück')

// Lightbox
await page.goto(BASE + '/galerie/', { waitUntil: 'networkidle' })
await page.click('[data-lightbox-open]')
const lbOpen = await page.evaluate(() => document.querySelector('[data-lightbox]')?.open)
await page.keyboard.press('Escape')
const lbClosed = await page.evaluate(() => !document.querySelector('[data-lightbox]')?.open)
if (!lbOpen) structural.push('✗ Lightbox öffnet nicht')
if (!lbClosed) structural.push('✗ Escape schließt die Lightbox nicht')

// Formularvalidierung
await page.goto(BASE + '/kontakt/', { waitUntil: 'networkidle' })
await page.click('[data-contact-form] button[type="submit"]')
const invalidCount = await page.evaluate(
  () => document.querySelectorAll('.field[data-invalid="true"]').length
)
const statusText = await page.textContent('[data-form-status]')
if (invalidCount < 3) structural.push(`✗ Formular markiert nur ${invalidCount} Pflichtfelder`)
if (!statusText?.trim()) structural.push('✗ Formular meldet keinen Status')

// Shop-Filter
await page.goto(BASE + '/shop/halsbaender/', { waitUntil: 'networkidle' })
const before = await page.evaluate(
  () => document.querySelectorAll('[data-filter-list] > li:not([hidden])').length
)
await page.click('[data-filter]:not([data-filter="alle"])')
const after = await page.evaluate(
  () => document.querySelectorAll('[data-filter-list] > li:not([hidden])').length
)
if (!(after > 0 && after < before)) structural.push(`✗ Shop-Filter wirkt nicht (${before} → ${after})`)

await browser.close()

console.log(`\n${checked} Seitenprüfungen mit axe (dark + light).`)
console.log(violations ? `${violations} axe-Verstöße.` : 'Keine axe-Verstöße.')
if (structural.length) {
  console.log('\nStrukturprobleme:')
  structural.forEach((s) => console.log('  ' + s))
} else {
  console.log('Keine Strukturprobleme.')
}

process.exit(violations || structural.length ? 1 : 0)
