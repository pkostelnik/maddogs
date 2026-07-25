import { readFileSync, existsSync } from 'node:fs'
import { resolve, dirname } from 'node:path'

const INCLUDE_RE = /<!--\s*#include\s+file="([^"]+)"\s*(\{[\s\S]*?\})?\s*-->/g

/**
 * Löst `<!--#include file="src/partials/header.html" {"key":"value"} -->` auf.
 * Optionales JSON-Objekt ersetzt `{{key}}`-Platzhalter im Partial.
 * Rekursiv, damit Partials selbst wieder Partials einbinden können.
 */
function expand(html, root, seen = new Set()) {
  return html.replace(INCLUDE_RE, (_match, file, rawVars) => {
    const path = resolve(root, file)
    if (!existsSync(path)) {
      throw new Error(`[html-includes] Partial nicht gefunden: ${file}`)
    }
    if (seen.has(path)) {
      throw new Error(`[html-includes] Zirkulärer Include: ${file}`)
    }
    let part = readFileSync(path, 'utf8')
    if (rawVars) {
      const vars = JSON.parse(rawVars)
      part = part.replace(/\{\{(\w+)\}\}/g, (m, key) =>
        Object.prototype.hasOwnProperty.call(vars, key) ? String(vars[key]) : m
      )
    }
    // Nicht ersetzte Platzhalter entfernen, damit sie nicht sichtbar werden.
    part = part.replace(/\{\{\w+\}\}/g, '')
    return expand(part, root, new Set([...seen, path]))
  })
}

export default function htmlIncludes() {
  let root = process.cwd()
  return {
    name: 'html-includes',
    enforce: 'pre',
    configResolved(config) {
      root = config.root
    },
    transformIndexHtml: {
      order: 'pre',
      handler(html) {
        return expand(html, root)
      },
    },
    handleHotUpdate({ file, server }) {
      if (file.includes('/src/partials/')) {
        server.ws.send({ type: 'full-reload' })
        return []
      }
    },
  }
}
