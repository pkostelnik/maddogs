const STORAGE_KEY = 'md-theme'

function currentTheme() {
  if (document.documentElement.dataset.theme) return document.documentElement.dataset.theme
  return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'
}

function apply(theme, toggle) {
  document.documentElement.dataset.theme = theme
  document
    .querySelector('meta[name="theme-color"]')
    ?.setAttribute('content', theme === 'light' ? '#f7f5f1' : '#0d0f12')

  toggle.setAttribute('aria-pressed', String(theme === 'light'))
  toggle.querySelector('.visually-hidden').textContent =
    theme === 'light' ? 'Dunkles Farbschema aktivieren' : 'Helles Farbschema aktivieren'
}

export function initTheme() {
  const toggle = document.querySelector('[data-theme-toggle]')
  if (!toggle) return

  apply(currentTheme(), toggle)

  toggle.addEventListener('click', () => {
    const next = currentTheme() === 'light' ? 'dark' : 'light'
    apply(next, toggle)
    try {
      localStorage.setItem(STORAGE_KEY, next)
    } catch {
      /* Speichern nicht möglich – Auswahl gilt für diese Sitzung. */
    }
  })
}
