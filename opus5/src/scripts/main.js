import { initNav } from './nav.js'
import { initTheme } from './theme.js'
import { initReveal } from './reveal.js'
import { initLightbox } from './lightbox.js'
import { initForm } from './form.js'
import { initFilter } from './filter.js'

// Alle Module prüfen selbst, ob ihre Hooks vorhanden sind, und
// tun sonst nichts. So bleibt ein einziges Bundle für alle Seiten sinnvoll.
initTheme()
initNav()
initReveal()
initLightbox()
initForm()
initFilter()
