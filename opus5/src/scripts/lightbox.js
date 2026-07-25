import { trapFocus } from './focus-trap.js'

/**
 * Galerie-Lightbox auf Basis von <dialog>.
 * Bedienbar per Maus, Tastatur (Pfeile, Escape, Tab) und Touch.
 */
export function initLightbox() {
  const gallery = document.querySelector('[data-gallery]')
  const dialog = document.querySelector('[data-lightbox]')
  if (!gallery || !dialog || typeof dialog.showModal !== 'function') return

  const buttons = Array.from(gallery.querySelectorAll('[data-lightbox-open]'))
  const image = dialog.querySelector('[data-lightbox-image]')
  const caption = dialog.querySelector('[data-lightbox-caption]')
  const counter = dialog.querySelector('[data-lightbox-counter]')
  const prevBtn = dialog.querySelector('[data-lightbox-prev]')
  const nextBtn = dialog.querySelector('[data-lightbox-next]')
  const closeBtn = dialog.querySelector('[data-lightbox-close]')

  let index = 0
  let releaseTrap = null

  function show(next) {
    index = (next + buttons.length) % buttons.length
    const source = buttons[index].querySelector('img')
    image.src = buttons[index].dataset.full || source.currentSrc || source.src
    image.alt = source.alt
    caption.textContent = source.alt
    counter.textContent = `${index + 1} von ${buttons.length}`
  }

  function open(at) {
    show(at)
    dialog.showModal()
    releaseTrap = trapFocus(dialog)
    closeBtn.focus()
  }

  buttons.forEach((button, i) => button.addEventListener('click', () => open(i)))

  prevBtn.addEventListener('click', () => show(index - 1))
  nextBtn.addEventListener('click', () => show(index + 1))
  closeBtn.addEventListener('click', () => dialog.close())

  dialog.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') {
      event.preventDefault()
      show(index + 1)
    }
    if (event.key === 'ArrowLeft') {
      event.preventDefault()
      show(index - 1)
    }
  })

  // Klick auf den Backdrop schließt.
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close()
  })

  dialog.addEventListener('close', () => {
    releaseTrap?.()
    releaseTrap = null
    buttons[index]?.focus()
  })
}
