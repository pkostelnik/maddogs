import { chromium } from 'playwright'

const [, , url = 'http://localhost:4321/', name = 'shot'] = process.argv

const browser = await chromium.launch()

for (const [label, viewport] of [
  ['mobile', { width: 390, height: 844 }],
  ['desktop', { width: 1440, height: 900 }],
]) {
  const page = await browser.newPage({ viewport, deviceScaleFactor: 1 })
  await page.goto(url, { waitUntil: 'networkidle' })
  // Lazy geladene Bilder anstoßen, sonst bleiben sie im Fullpage-Shot leer.
  await page.evaluate(async () => {
    const step = window.innerHeight
    for (let y = 0; y < document.body.scrollHeight; y += step) {
      window.scrollTo(0, y)
      await new Promise((r) => setTimeout(r, 120))
    }
    window.scrollTo(0, 0)
  })
  await page.evaluate(() => {
    document.querySelectorAll('[data-reveal]').forEach((el) => el.classList.add('is-revealed'))
    // Sticky-CTA stört den Fullpage-Shot, im echten Betrieb ist er korrekt.
    document.querySelector('[data-sticky-cta]')?.remove()
  })
  await page.waitForTimeout(600)
  await page.screenshot({ path: `/tmp/shots/${name}-${label}.png`, fullPage: true })
  await page.close()
}

await browser.close()
console.log('ok')
