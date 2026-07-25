/**
 * Kategoriefilter im Shop. Rein clientseitig, ohne Seitenwechsel.
 * Der Trefferzähler wird über eine Live-Region angesagt.
 */
export function initFilter() {
  const bar = document.querySelector('[data-filter-bar]')
  const list = document.querySelector('[data-filter-list]')
  if (!bar || !list) return

  const chips = Array.from(bar.querySelectorAll('[data-filter]'))
  const items = Array.from(list.children)
  const count = document.querySelector('[data-filter-count]')

  function apply(value) {
    let visible = 0
    items.forEach((item) => {
      const match = value === 'alle' || (item.dataset.tags || '').split(' ').includes(value)
      item.hidden = !match
      if (match) visible++
    })
    if (count) {
      count.textContent = `${visible} ${visible === 1 ? 'Produkt' : 'Produkte'}`
    }
  }

  chips.forEach((chip) => {
    chip.addEventListener('click', () => {
      chips.forEach((other) => other.setAttribute('aria-pressed', String(other === chip)))
      apply(chip.dataset.filter)
    })
  })

  apply('alle')
}
