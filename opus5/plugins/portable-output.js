/**
 * Macht den Build ortsunabhängig, damit er ohne Server läuft –
 * per Doppelklick über file:// ebenso wie in einem Unterverzeichnis.
 *
 * Drei Eingriffe, jeweils nach Vite ('post'):
 *
 * 1. Wurzelabsolute Verweise (`/training/`) werden relativ (`../training/`).
 *    So bleiben die Quelldateien lesbar, das Ergebnis aber portabel.
 *
 * 2. `crossorigin` wird von Stylesheet und Skript entfernt. Über file://
 *    erzwingt das Attribut eine CORS-Prüfung, die dort immer fehlschlägt.
 *    Bei eigenen Dateien gleicher Herkunft bringt es ohnehin nichts.
 *
 * 3. `type="module"` wird zu `defer`. Module lädt der Browser grundsätzlich
 *    per CORS – über file:// unmöglich. Das gebündelte Skript enthält keine
 *    import- oder export-Anweisungen und ist damit gültiges klassisches
 *    JavaScript; `defer` erhält die verzögerte Ausführung.
 *
 * Absolute URLs (https://, //, mailto:, tel:) bleiben unangetastet.
 */
const ATTR_RE = /\b(href|src|content)="(\/(?!\/)[^"]*)"/g

export default function portableOutput() {
  return {
    name: 'portable-output',
    apply: 'build',

    transformIndexHtml: {
      order: 'post',
      handler(html, ctx) {
        // ctx.path ist z. B. "/training/dogwalking/index.html".
        const depth = ctx.path.replace(/^\//, '').split('/').length - 1
        const prefix = depth === 0 ? './' : '../'.repeat(depth)

        html = html.replace(ATTR_RE, (match, attr, value) => {
          // Meta-Angaben tragen vollständige URLs; nur echte Pfade umschreiben.
          if (attr === 'content' && !value.endsWith('.webmanifest')) return match
          return `${attr}="${prefix}${value.slice(1)}"`
        })

        html = html.replace(/<script\b[^>]*>/g, (tag) =>
          tag.includes('src=')
            ? tag.replace(/\s+type="module"/, ' defer').replace(/\s+crossorigin/, '')
            : tag
        )

        html = html.replace(/(<link\b[^>]*rel="stylesheet"[^>]*>)/g, (tag) =>
          tag.replace(/\s+crossorigin/, '')
        )

        return html
      },
    },
  }
}
