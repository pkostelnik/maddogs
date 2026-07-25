/**
 * Kontaktformular: Validierung auf Basis der Constraint Validation API,
 * mit deutschsprachigen Meldungen und Live-Region für den Status.
 * Es wird nichts versendet – der Prototyp hat kein Backend.
 */
const MESSAGES = {
  valueMissing: {
    default: 'Bitte füllen Sie dieses Feld aus.',
    checkbox: 'Bitte bestätigen Sie diesen Punkt, um fortzufahren.',
  },
  typeMismatch: {
    email: 'Bitte geben Sie eine gültige E-Mail-Adresse ein, zum Beispiel name@beispiel.de.',
  },
  tooShort: {
    default: 'Bitte schreiben Sie etwas ausführlicher.',
  },
  patternMismatch: {
    tel: 'Bitte geben Sie eine gültige Telefonnummer ein.',
  },
}

function messageFor(input) {
  const v = input.validity
  const type = input.type === 'checkbox' ? 'checkbox' : input.type
  if (v.valueMissing) return MESSAGES.valueMissing[type] || MESSAGES.valueMissing.default
  if (v.typeMismatch) return MESSAGES.typeMismatch[type] || 'Die Eingabe hat das falsche Format.'
  if (v.tooShort) return MESSAGES.tooShort.default
  if (v.patternMismatch) return MESSAGES.patternMismatch[type] || 'Die Eingabe passt nicht.'
  return 'Bitte prüfen Sie diese Eingabe.'
}

function setFieldState(input, valid, message) {
  const field = input.closest('.field')
  if (!field) return
  const error = field.querySelector('.field__error')
  field.dataset.invalid = String(!valid)
  input.setAttribute('aria-invalid', String(!valid))
  if (error) error.textContent = valid ? '' : message
}

export function initForm() {
  const form = document.querySelector('[data-contact-form]')
  if (!form) return

  const status = form.querySelector('[data-form-status]')
  const honeypot = form.querySelector('[data-honeypot]')
  const inputs = Array.from(form.querySelectorAll('input, textarea, select')).filter(
    (el) => el !== honeypot
  )

  // Browser-eigene Bubbles abschalten, wir zeigen eigene Meldungen.
  form.setAttribute('novalidate', '')

  inputs.forEach((input) => {
    input.addEventListener('blur', () => {
      if (input.value === '' && !input.required) return
      setFieldState(input, input.checkValidity(), messageFor(input))
    })

    input.addEventListener('input', () => {
      if (input.closest('.field')?.dataset.invalid === 'true') {
        setFieldState(input, input.checkValidity(), messageFor(input))
      }
    })
  })

  form.addEventListener('submit', (event) => {
    event.preventDefault()

    if (honeypot && honeypot.value !== '') return // Bot erkannt, stillschweigend ignorieren.

    let firstInvalid = null
    inputs.forEach((input) => {
      const valid = input.checkValidity()
      setFieldState(input, valid, messageFor(input))
      if (!valid && !firstInvalid) firstInvalid = input
    })

    if (firstInvalid) {
      status.dataset.state = 'error'
      status.textContent =
        'Das Formular konnte nicht gesendet werden. Bitte prüfen Sie die markierten Felder.'
      firstInvalid.focus()
      return
    }

    status.dataset.state = 'success'
    status.textContent =
      'Danke! Im Prototyp wird nichts versendet – im Livebetrieb ginge Ihre Anfrage jetzt raus. Für sofortige Antwort: WhatsApp an 0173 3649143.'
    form.reset()
    inputs.forEach((input) => setFieldState(input, true, ''))
  })
}
