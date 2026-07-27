import { readFileSync, existsSync, readdirSync } from 'node:fs'
import { resolve, join, basename } from 'node:path'

/*
 * Kleine Template-Schicht für statische Seiten.
 *
 *   <!--#include file="src/partials/x.html" {"titel": "Wert"} -->
 *   <!--#each in="testimonials.items" file="src/partials/quote.html" -->
 *   {{pfad.zum.wert}}      – HTML-escaped
 *   {{{pfad.zum.wert}}}    – roh, für bewusst gesetztes Markup
 *   {{#if feld}} … {{/if}} / {{#unless feld}} … {{/unless}}
 *
 * Werte werden zuerst im lokalen Gültigkeitsbereich gesucht (Schleifen-Element,
 * Include-Variablen), danach in den globalen Daten aus src/content/*.json.
 */

const CONTENT_DIR = 'src/content'
const MAX_DEPTH = 12

const INCLUDE_RE = /<!--\s*#include\s+file="([^"]+)"\s*(\{[\s\S]*?\})?\s*-->/g
const EACH_RE = /<!--\s*#each\s+in="([^"]+)"\s+file="([^"]+)"\s*(\{[\s\S]*?\})?\s*-->/g
const IF_RE = /\{\{#(if|unless)\s+([\w.@[\]]+)\}\}([\s\S]*?)\{\{\/\1\}\}/g
const RAW_RE = /\{\{\{\s*([\w.@[\]]+)\s*\}\}\}/g
const VAR_RE = /\{\{\s*([\w.@[\]]+)\s*\}\}/g

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function lookup(path, scopes) {
  // Segmente der Form [name] werden zunaechst selbst aufgeloest. Damit kann
  // ein Schleifenelement per Schluessel in globale Daten zeigen:
  //   {{images.[image].alt}}  ->  images[<Wert von image>].alt
  const segments = path.split('.').map((segment) => {
    const indirect = segment.match(/^\[(.+)\]$/)
    if (!indirect) return segment
    const resolved = lookup(indirect[1], scopes)
    if (resolved === undefined) {
      throw new Error(`[html-includes] Indirekter Schluessel "${indirect[1]}" ist nicht gesetzt.`)
    }
    return String(resolved)
  })

  for (const scope of scopes) {
    let value = scope
    let found = true
    for (const key of segments) {
      if (value != null && typeof value === 'object' && key in value) {
        value = value[key]
      } else {
        found = false
        break
      }
    }
    if (found && value !== undefined) return value
  }
  return undefined
}

function truthy(value) {
  return Array.isArray(value) ? value.length > 0 : Boolean(value)
}

function loadContent(root) {
  const dir = join(root, CONTENT_DIR)
  const data = {}
  if (!existsSync(dir)) return data
  for (const file of readdirSync(dir)) {
    if (!file.endsWith('.json')) continue
    const key = basename(file, '.json')
    try {
      data[key] = JSON.parse(readFileSync(join(dir, file), 'utf8'))
    } catch (error) {
      throw new Error(`[html-includes] ${CONTENT_DIR}/${file} ist kein gültiges JSON: ${error.message}`)
    }
  }
  return data
}

function readPartial(root, file) {
  const path = resolve(root, file)
  if (!existsSync(path)) throw new Error(`[html-includes] Partial nicht gefunden: ${file}`)
  return readFileSync(path, 'utf8')
}

function parseVars(raw, file) {
  if (!raw) return {}
  try {
    return JSON.parse(raw)
  } catch (error) {
    throw new Error(`[html-includes] Ungültiges JSON bei ${file}: ${error.message}`)
  }
}

function render(html, root, scopes, depth = 0) {
  if (depth > MAX_DEPTH) {
    throw new Error('[html-includes] Zu tiefe Verschachtelung – vermutlich ein Zirkelbezug.')
  }

  // 1. Schleifen: erzeugen neuen Inhalt, der selbst Includes enthalten kann.
  html = html.replace(EACH_RE, (_m, path, file, rawVars) => {
    const items = lookup(path, scopes)
    if (items === undefined) {
      throw new Error(`[html-includes] Unbekannte Sammlung "${path}" in #each.`)
    }
    if (!Array.isArray(items)) {
      throw new Error(`[html-includes] "${path}" ist keine Liste (#each).`)
    }
    const shared = parseVars(rawVars, file)
    const template = readPartial(root, file)
    return items
      .map((item, index) => {
        const local = {
          ...shared,
          ...(item && typeof item === 'object' ? item : { wert: item }),
          '@index': index,
          '@number': index + 1,
          '@nummer': String(index + 1).padStart(2, '0'),
          '@first': index === 0,
          '@last': index === items.length - 1,
        }
        return render(template, root, [local, ...scopes], depth + 1)
      })
      .join('\n')
  })

  // 2. Includes.
  html = html.replace(INCLUDE_RE, (_m, file, rawVars) => {
    const local = parseVars(rawVars, file)
    return render(readPartial(root, file), root, [local, ...scopes], depth + 1)
  })

  // 3. Bedingungen.
  let previous
  do {
    previous = html
    html = html.replace(IF_RE, (_m, kind, path, body) => {
      const hit = truthy(lookup(path, scopes))
      return (kind === 'if') === hit ? body : ''
    })
  } while (html !== previous)

  // 4. Werte einsetzen.
  html = html.replace(RAW_RE, (m, path) => {
    const value = lookup(path, scopes)
    return value === undefined ? m : String(value)
  })
  html = html.replace(VAR_RE, (m, path) => {
    const value = lookup(path, scopes)
    return value === undefined ? m : escapeHtml(value)
  })

  return html
}

export default function htmlIncludes() {
  let root = process.cwd()
  let data = null

  return {
    name: 'html-includes',
    enforce: 'pre',

    configResolved(config) {
      root = config.root
    },

    buildStart() {
      data = loadContent(root)
    },

    transformIndexHtml: {
      order: 'pre',
      handler(html) {
        if (!data) data = loadContent(root)
        const out = render(html, root, [data])

        // Uebrig gebliebene Platzhalter sind fast immer Tippfehler und
        // wuerden sonst unbemerkt auf der Seite landen.
        const leftovers = [...out.matchAll(/\{\{[^}]+\}\}/g)].map((m) => m[0])
        if (leftovers.length) {
          throw new Error(
            `[html-includes] Nicht aufgelöste Platzhalter: ${[...new Set(leftovers)].join(', ')}`
          )
        }
        return out
      },
    },

    handleHotUpdate({ file, server }) {
      if (file.includes('/src/partials/') || file.includes('/src/content/')) {
        data = loadContent(root)
        server.ws.send({ type: 'full-reload' })
        return []
      }
    },
  }
}
