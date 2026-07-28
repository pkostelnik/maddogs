(function () {
  const form = document.getElementById("contact-form");
  if (!form) return;

  const success = document.getElementById("form-success");
  const live = document.getElementById("form-live");

  function setError(fieldName, message) {
    const field = form.querySelector(`[data-field="${fieldName}"]`);
    if (!field) return;
    const input = field.querySelector("input, textarea");
    const err = field.querySelector(".error");
    field.classList.toggle("is-invalid", Boolean(message));
    if (err) {
      err.textContent = message || "";
      if (message) err.setAttribute("role", "alert");
      else err.removeAttribute("role");
    }
    if (input) {
      if (message) input.setAttribute("aria-invalid", "true");
      else input.removeAttribute("aria-invalid");
    }
  }

  function validateEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  form.setAttribute("novalidate", "");

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    let ok = true;
    const name = form.elements.namedItem("name");
    const email = form.elements.namedItem("email");
    const message = form.elements.namedItem("message");
    const consent = form.elements.namedItem("consent");

    setError("name", "");
    setError("email", "");
    setError("message", "");
    setError("consent", "");

    if (!name || !String(name.value).trim()) {
      setError("name", "Bitte Namen angeben.");
      ok = false;
    }
    if (!email || !String(email.value).trim()) {
      setError("email", "Bitte E-Mail angeben.");
      ok = false;
    } else if (!validateEmail(String(email.value).trim())) {
      setError("email", "Bitte eine gültige E-Mail-Adresse eingeben.");
      ok = false;
    }
    if (!message || !String(message.value).trim()) {
      setError("message", "Bitte eine Nachricht schreiben.");
      ok = false;
    }
    if (!consent || !consent.checked) {
      setError("consent", "Bitte Einwilligung zur Kontaktaufnahme bestätigen.");
      ok = false;
    }

    if (!ok) {
      if (live) live.textContent = "Bitte prüfe die markierten Felder.";
      const firstInvalid = form.querySelector(".is-invalid input, .is-invalid textarea, .is-invalid input[type=checkbox]");
      if (firstInvalid) firstInvalid.focus();
      return;
    }

    form.hidden = true;
    if (success) {
      success.hidden = false;
      success.focus();
    }
    if (live) live.textContent = "Nachricht wurde erfolgreich vorbereitet (Demo — kein Versand).";
  });
})();
