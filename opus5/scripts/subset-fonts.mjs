/**
 * Verkleinert die beiden variablen Schriften auf die Zeichen, die auf den
 * Seiten tatsächlich vorkommen – plus einen Sicherheitsvorrat für Inhalte,
 * die später dazukommen.
 *
 * Aufruf: node scripts/subset-fonts.mjs
 */
import subsetFont from 'subset-font'
import { readFile, writeFile, stat } from 'node:fs/promises'
import { globSync } from 'glob'

const SRC = {
  archivo: 'node_modules/@fontsource-variable/archivo/files/archivo-latin-wdth-normal.woff2',
  inter: 'node_modules/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2',
}
const OUT = {
  archivo: 'src/assets/fonts/archivo-var.woff2',
  inter: 'src/assets/fonts/inter-var.woff2',
}

// Reserve: vollständiges deutsches Alphabet, Ziffern, gängige Satz- und
// Sonderzeichen. So bricht nichts, wenn später neue Texte dazukommen.
const RESERVE =
  'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' +
  'ÄÖÜäöüß0123456789' +
  ' .,;:!?()[]{}<>„“”‚‘’«»–—-−_/\\|@#&*+=%€$£§°²³' +
  "'\"`^~©®™→←↑↓·•…×÷±≥≤"

async function collectCharacters() {
  const chars = new Set(RESERVE)
  const files = [
    ...globSync('**/*.html', { ignore: ['node_modules/**', 'dist/**'] }),
    ...globSync('src/content/*.json'),
  ]
  for (const file of files) {
    const text = await readFile(file, 'utf8')
    for (const ch of text) chars.add(ch)
  }
  return [...chars].join('')
}

async function kb(path) {
  return Math.round((await stat(path)).size / 102.4) / 10
}

const text = await collectCharacters()
console.log(`${new Set(text).size} unterschiedliche Zeichen erfasst.`)

for (const [name, src] of Object.entries(SRC)) {
  const before = await kb(src)
  const buffer = await readFile(src)
  const subset = await subsetFont(buffer, text, {
    targetFormat: 'woff2',
    // Variable Achsen erhalten: Archivo braucht die Breitenachse fuer die
    // kondensierten Ueberschriften, Inter die Gewichtsachse.
    variationAxes:
      name === 'archivo' ? { wght: { min: 400, max: 900 }, wdth: { min: 70, max: 110 } } : undefined,
  })
  await writeFile(OUT[name], subset)
  const after = await kb(OUT[name])
  console.log(`${name}: ${before} kB → ${after} kB (−${Math.round((1 - after / before) * 100)} %)`)
}
