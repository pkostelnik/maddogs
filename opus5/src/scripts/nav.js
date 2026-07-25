import { trapFocus, getFocusable } from './focus-trap.js'

/** Markiert den aktuellen Menüpunkt anhand des Pfads. */
function markCurrent() {
  const path = window.location.pathname.replace(/index\.html$/, '')
  document.querySelectorAll('.nav__link[href], .nav__submenu a[href]').forEach((link) => {
    const href = new URL(link.getAttribute('href'), window.location.origin).pathname
    if (href === path) {
      link.setAttribute('aria-current', 'page')
    }
  })
}

/** Desktop-Dropdown: Klick, Escape, Klick außerhalb, Fokusverlust. */
function initDropdowns() {
  const dropdowns = document.querySelectorAll('[data-nav-dropdown]')

  dropdowns.forEach((dropdown) => {
    const trigger = dropdown.querySelector('[data-nav-dropdown-trigger]')
    if (!trigger) return

    const close = () => trigger.setAttribute('aria-expanded', 'false')

    trigger.addEventListener('click', () => {
      const open = trigger.getAttribute('aria-expanded') === 'true'
      dropdowns.forEach((other) =>
        other.querySelector('[data-nav-dropdown-trigger]')?.setAttribute('aria-expanded', 'false')
      )
      trigger.setAttribute('aria-expanded', String(!open))
    })

    dropdown.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && trigger.getAttribute('aria-expanded') === 'true') {
        close()
        trigger.focus()
      }
      // Pfeil runter springt in die erste Option.
      if (event.key === 'ArrowDown' && document.activeElement === trigger) {
        event.preventDefault()
        trigger.setAttribute('aria-expanded', 'true')
        dropdown.querySelector('.nav__submenu a')?.focus()
      }
    })

    dropdown.addEventListener('focusout', (event) => {
      if (!dropdown.contains(event.relatedTarget)) close()
    })

    document.addEventListener('click', (event) => {
      if (!dropdown.contains(event.target)) close()
    })
  })
}

/** Mobile-Drawer inklusive Fokus-Falle und Scroll-Lock. */
function initDrawer() {
  const toggle = document.querySelector('[data-nav-toggle]')
  const drawer = document.querySelector('[data-nav-drawer]')
  if (!toggle || !drawer) return

  let releaseTrap = null

  function setOpen(open) {
    toggle.setAttribute('aria-expanded', String(open))
    drawer.dataset.open = String(open)
    toggle.querySelector('.visually-hidden').textContent = open
      ? 'Menü schließen'
      : 'Menü öffnen'

    if (open) {
      document.body.dataset.scrollLocked = 'true'
      releaseTrap = trapFocus(drawer)
      getFocusable(drawer)[0]?.focus()
    } else {
      delete document.body.dataset.scrollLocked
      releaseTrap?.()
      releaseTrap = null
    }
  }

  toggle.addEventListener('click', () =>
    setOpen(toggle.getAttribute('aria-expanded') !== 'true')
  )

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && drawer.dataset.open === 'true') {
      setOpen(false)
      toggle.focus()
    }
  })

  drawer.querySelectorAll('a').forEach((link) =>
    link.addEventListener('click', () => setOpen(false))
  )

  // Aufklappbare Gruppen im Drawer.
  drawer.querySelectorAll('.nav-drawer__toggle').forEach((groupToggle) => {
    groupToggle.addEventListener('click', () => {
      const open = groupToggle.getAttribute('aria-expanded') === 'true'
      groupToggle.setAttribute('aria-expanded', String(!open))
    })
  })

  // Beim Wechsel auf Desktop den Drawer sicher schließen.
  const desktop = window.matchMedia('(min-width: 60rem)')
  desktop.addEventListener('change', (event) => {
    if (event.matches && drawer.dataset.open === 'true') setOpen(false)
  })
}

/** Sticky-CTA erscheint erst, wenn der Seitenkopf vollständig weggescrollt ist. */
function initStickyCta() {
  const cta = document.querySelector('[data-sticky-cta]')
  const sentinel = document.querySelector('.hero, .page-head')
  if (!cta || !sentinel) return

  const observer = new IntersectionObserver(
    ([entry]) => {
      // Sichtbar, sobald der Kopfbereich nach oben aus dem Viewport gelaufen ist.
      const scrolledPast = !entry.isIntersecting && entry.boundingClientRect.top < 0
      cta.dataset.visible = String(scrolledPast)
    },
    { threshold: 0 }
  )
  observer.observe(sentinel)
}

export function initNav() {
  markCurrent()
  initDropdowns()
  initDrawer()
  initStickyCta()
}
