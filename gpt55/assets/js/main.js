(function () {
  "use strict";

  function initNav() {
    var toggle = document.querySelector("[data-nav-toggle]");
    var nav = document.querySelector("[data-primary-nav]");
    if (!toggle || !nav) return;

    var desktop = window.matchMedia("(min-width: 62rem)");

    function setOpen(open, restoreFocus) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      nav.setAttribute("data-open", open ? "true" : "false");
      toggle.querySelector(".nav-toggle__label").textContent = open ? "Menü schließen" : "Menü öffnen";
      if (open) {
        var firstLink = nav.querySelector("a");
        if (firstLink) firstLink.focus();
      } else if (restoreFocus) {
        toggle.focus();
      }
    }

    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true", false);
    });

    nav.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setOpen(false, true);
    });

    document.addEventListener("click", function (event) {
      if (desktop.matches || toggle.getAttribute("aria-expanded") !== "true") return;
      if (!nav.contains(event.target) && !toggle.contains(event.target)) setOpen(false, false);
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (!desktop.matches) setOpen(false, false);
      });
    });

    function resetForBreakpoint() {
      setOpen(false, false);
    }

    if (desktop.addEventListener) {
      desktop.addEventListener("change", resetForBreakpoint);
    } else if (desktop.addListener) {
      desktop.addListener(resetForBreakpoint);
    }
  }

  function initHeader() {
    var header = document.querySelector("[data-site-header]");
    if (!header) return;

    function update() {
      header.classList.toggle("is-scrolled", window.scrollY > 6);
    }

    update();
    window.addEventListener("scroll", update, { passive: true });
  }

  function initLightbox() {
    var dialog = document.querySelector("[data-lightbox]");
    var triggers = document.querySelectorAll("[data-lightbox-trigger]");
    if (!dialog || !triggers.length) return;

    var image = dialog.querySelector("[data-lightbox-image]");
    var caption = dialog.querySelector("[data-lightbox-caption]");
    var close = dialog.querySelector("[data-lightbox-close]");
    var lastTrigger = null;

    function open(trigger) {
      var src = trigger.getAttribute("data-full");
      var alt = trigger.getAttribute("data-alt") || "";
      if (!src || !image) return;
      lastTrigger = trigger;
      image.src = src;
      image.alt = alt;
      if (caption) caption.textContent = alt;
      if (typeof dialog.showModal === "function") dialog.showModal();
      else window.location.href = src;
    }

    triggers.forEach(function (trigger) {
      trigger.addEventListener("click", function () {
        open(trigger);
      });
    });

    if (close) {
      close.addEventListener("click", function () {
        dialog.close();
      });
    }

    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) dialog.close();
    });

    dialog.addEventListener("close", function () {
      if (image) image.removeAttribute("src");
      if (lastTrigger) lastTrigger.focus();
    });
  }

  function initContactForm() {
    var form = document.querySelector("[data-contact-form]");
    if (!form) return;

    var status = form.querySelector("[data-form-status]");
    var submit = form.querySelector('button[type="submit"]');

    function setStatus(message, state) {
      if (!status) return;
      status.textContent = message || "";
      if (state) status.setAttribute("data-state", state);
      else status.removeAttribute("data-state");
    }

    function setError(field, message) {
      var id = field.getAttribute("aria-describedby");
      var error = id ? document.getElementById(id) : null;
      if (message) {
        field.setAttribute("aria-invalid", "true");
        if (error) {
          error.textContent = message;
          error.hidden = false;
        }
      } else {
        field.removeAttribute("aria-invalid");
        if (error) {
          error.textContent = "";
          error.hidden = true;
        }
      }
    }

    function validate() {
      var valid = true;
      form.querySelectorAll("[required]").forEach(function (field) {
        if (field.type === "checkbox") {
          if (!field.checked) {
            setError(field, "Bitte bestätige die Datenschutzhinweise.");
            valid = false;
          } else {
            setError(field, "");
          }
          return;
        }

        if (field.value.trim() === "") {
          setError(field, "Dieses Feld ist erforderlich.");
          valid = false;
        } else if (field.type === "email" && !field.validity.valid) {
          setError(field, "Bitte gib eine gültige E-Mail-Adresse ein.");
          valid = false;
        } else {
          setError(field, "");
        }
      });
      return valid;
    }

    form.querySelectorAll("input, textarea").forEach(function (field) {
      field.addEventListener("blur", function () {
        if (field.hasAttribute("required")) validate();
      });
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!validate()) {
        setStatus("Bitte überprüfe die markierten Felder.", "error");
        var firstInvalid = form.querySelector('[aria-invalid="true"]');
        if (firstInvalid) firstInvalid.focus();
        return;
      }

      var action = form.getAttribute("action");
      if (!action || typeof window.fetch !== "function") {
        form.submit();
        return;
      }

      if (submit) submit.setAttribute("aria-disabled", "true");
      setStatus("Nachricht wird gesendet ...", "");

      fetch(action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" },
      })
        .then(function (response) {
          if (!response.ok) throw new Error("request failed");
          return response.json().catch(function () {
            return { ok: true };
          });
        })
        .then(function () {
          form.reset();
          setStatus("Danke für deine Nachricht. Wir melden uns so schnell wie möglich.", "success");
        })
        .catch(function () {
          setStatus("Das Senden hat nicht geklappt. Bitte kontaktiere uns direkt per Telefon, E-Mail oder WhatsApp.", "error");
        })
        .finally(function () {
          if (submit) submit.removeAttribute("aria-disabled");
        });
    });
  }

  function initYear() {
    var year = document.querySelector("[data-current-year]");
    if (year) year.textContent = String(new Date().getFullYear());
  }

  initNav();
  initHeader();
  initLightbox();
  initContactForm();
  initYear();
})();
