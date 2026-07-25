/**
 * Blendet Elemente beim Scrollen sanft ein.
 * Ohne IntersectionObserver oder bei reduzierter Bewegung bleibt alles sichtbar.
 */
export function initReveal() {
  const items = document.querySelectorAll('[data-reveal]')
  if (!items.length) return

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduced || !('IntersectionObserver' in window)) {
    items.forEach((el) => el.classList.add('is-revealed'))
    return
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return
        entry.target.classList.add('is-revealed')
        observer.unobserve(entry.target)
      })
    },
    { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
  )

  items.forEach((el, index) => {
    // Leichte Staffelung innerhalb einer Gruppe, gedeckelt bei 240 ms.
    const group = el.closest('[data-reveal-group]')
    if (group) {
      const siblings = Array.from(group.querySelectorAll('[data-reveal]'))
      el.style.setProperty('--reveal-delay', `${Math.min(siblings.indexOf(el) * 70, 240)}ms`)
    } else if (el.dataset.reveal) {
      el.style.setProperty('--reveal-delay', `${Math.min(Number(el.dataset.reveal) || 0, 240)}ms`)
    }
    observer.observe(el)
    void index
  })
}
