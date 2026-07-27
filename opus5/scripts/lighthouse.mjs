/**
 * Startet Lighthouse CI mit dem Chromium, das Playwright ohnehin mitbringt.
 * Ohne diesen Umweg scheitert LHCI, wenn kein System-Chrome installiert ist.
 *
 * Aufruf: node scripts/lighthouse.mjs
 */
import { spawn } from 'node:child_process'
import { chromium } from 'playwright'

let executable
try {
  executable = chromium.executablePath()
} catch {
  console.error('Kein Chromium gefunden. Bitte "npx playwright install chromium" ausführen.')
  process.exit(1)
}

const child = spawn('npx', ['lhci', 'autorun'], {
  stdio: 'inherit',
  env: { ...process.env, CHROME_PATH: executable },
})

child.on('exit', (code) => process.exit(code ?? 1))
