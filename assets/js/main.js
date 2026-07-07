/**
 * Mad Dogs Germany — main.js
 * ---------------------------------------------------------------
 * Progressive Enhancement: Die Website funktioniert vollständig ohne
 * JavaScript (Navigation ist ohne JS über :target/Server-Klick nicht
 * nötig, da sie unter 1024px als einfache Liste sichtbar gemacht
 * werden kann – siehe Noscript-Fallback in der Nav). Dieses Skript
 * verbessert lediglich die Bedienung:
 *   - Mobile Navigation (Disclosure-Pattern, ARIA-konform)
 *   - Lightbox-Galerie auf Basis von <dialog> (native Fokus-Falle)
 *   - Kontaktformular: Fetch-Enhancement mit zugänglichem Feedback
 *   - Footer-Jahr automatisch aktuell halten
 * Keine Abhängigkeiten, kein Tracking, kein Cookie-Einsatz.
 * ---------------------------------------------------------------
 */
(function () {
  "use strict";

  /* -------------------------------------------------------------
   * 1. Mobile Navigation
   * ------------------------------------------------------------- */
  function initNav() {
    var toggle = document.querySelector("[data-nav-toggle]");
    var nav = document.querySelector("[data-primary-nav]");
    if (!toggle || !nav) return;

    var desktopQuery = window.matchMedia("(min-width: 1024px)");

    function closeNav(options) {
      var restoreFocus = options && options.restoreFocus;
      toggle.setAttribute("aria-expanded", "false");
      nav.setAttribute("data-open", "false");
      if (restoreFocus) toggle.focus();
    }

    function openNav() {
      toggle.setAttribute("aria-expanded", "true");
      nav.setAttribute("data-open", "true");
      var firstLink = nav.querySelector("a");
      if (firstLink) firstLink.focus();
    }

    toggle.addEventListener("click", function () {
      var isOpen = toggle.getAttribute("aria-expanded") === "true";
      if (isOpen) {
        closeNav({ restoreFocus: false });
      } else {
        openNav();
      }
    });

    nav.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closeNav({ restoreFocus: true });
      }
    });

    document.addEventListener("click", function (event) {
      if (desktopQuery.matches) return;
      var isOpen = toggle.getAttribute("aria-expanded") === "true";
      if (!isOpen) return;
      var clickedInside = nav.contains(event.target) || toggle.contains(event.target);
      if (!clickedInside) closeNav({ restoreFocus: false });
    });

    // Menü schließen, sobald ein Link angeklickt wird (mobile)
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (!desktopQuery.matches) closeNav({ restoreFocus: false });
      });
    });

    // Zustand zurücksetzen, wenn über den Desktop-Breakpoint hinweg
    // vergrößert/verkleinert wird (verhindert CSS-Spezifitäts-Edgecase).
    function handleBreakpointChange() {
      closeNav({ restoreFocus: false });
    }
    if (typeof desktopQuery.addEventListener === "function") {
      desktopQuery.addEventListener("change", handleBreakpointChange);
    } else if (typeof desktopQuery.addListener === "function") {
      desktopQuery.addListener(handleBreakpointChange); // Safari < 14 Fallback
    }
  }

  /* -------------------------------------------------------------
   * 2. Sticky-Header: dezenter Schatten nach dem Scrollen
   * ------------------------------------------------------------- */
  function initHeaderShadow() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var ticking = false;

    function update() {
      header.classList.toggle("is-scrolled", window.scrollY > 4);
      ticking = false;
    }

    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          window.requestAnimationFrame(update);
          ticking = true;
        }
      },
      { passive: true }
    );
    update();
  }

  /* -------------------------------------------------------------
   * 3. Lightbox-Galerie (basiert auf <dialog>)
   * ------------------------------------------------------------- */
  function initLightbox() {
    var dialog = document.querySelector("[data-lightbox]");
    var triggers = document.querySelectorAll("[data-lightbox-trigger]");
    if (!dialog || !triggers.length || typeof dialog.showModal !== "function") return;

    var img = dialog.querySelector("[data-lightbox-image]");
    var caption = dialog.querySelector("[data-lightbox-caption]");
    var closeBtn = dialog.querySelector("[data-lightbox-close]");
    var lastTrigger = null;

    function openFrom(trigger) {
      var full = trigger.getAttribute("data-full");
      var fullWebp = trigger.getAttribute("data-full-webp");
      var alt = trigger.getAttribute("data-alt") || "";
      lastTrigger = trigger;
      img.src = fullWebp && !supportsWebpFallbackNeeded ? fullWebp : full;
      img.setAttribute("data-src-jpg", full);
      img.alt = alt;
      caption.textContent = alt;
      dialog.showModal();
    }

    var supportsWebpFallbackNeeded = false; // <picture> übernimmt Fallback im Markup; hier nur <img> Ziel

    triggers.forEach(function (trigger) {
      trigger.addEventListener("click", function () {
        openFrom(trigger);
      });
    });

    if (closeBtn) {
      closeBtn.addEventListener("click", function () {
        dialog.close();
      });
    }

    // Klick auf Backdrop schließt (Klick direkt auf <dialog>, nicht auf Inhalt)
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) dialog.close();
    });

    dialog.addEventListener("close", function () {
      img.src = "";
      if (lastTrigger) lastTrigger.focus();
    });
  }

  /* -------------------------------------------------------------
   * 4. Kontaktformular: zugängliche Validierung + Fetch-Enhancement
   * ------------------------------------------------------------- */
  function initContactForm() {
    var form = document.querySelector("[data-contact-form]");
    if (!form) return;

    var status = form.querySelector("[data-form-status]");
    var submitBtn = form.querySelector('button[type="submit"]');

    function setFieldError(field, message) {
      var row = field.closest(".form__row");
      var errorEl = row ? row.querySelector(".form__error") : null;
      if (!row || !errorEl) return;
      if (message) {
        row.setAttribute("data-invalid", "true");
        field.setAttribute("aria-invalid", "true");
        errorEl.textContent = message;
        errorEl.hidden = false;
      } else {
        row.removeAttribute("data-invalid");
        field.removeAttribute("aria-invalid");
        errorEl.textContent = "";
        errorEl.hidden = true;
      }
    }

    function validate() {
      var valid = true;
      form.querySelectorAll("[required]").forEach(function (field) {
        if (field.type === "checkbox") {
          if (!field.checked) {
            setFieldError(field, "Bitte bestätigen, um fortzufahren.");
            valid = false;
          } else {
            setFieldError(field, "");
          }
          return;
        }
        if (field.value.trim() === "") {
          setFieldError(field, "Dieses Feld ist erforderlich.");
          valid = false;
        } else if (field.type === "email" && !field.validity.valid) {
          setFieldError(field, "Bitte eine gültige E-Mail-Adresse angeben.");
          valid = false;
        } else {
          setFieldError(field, "");
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
        if (status) {
          status.textContent = "Bitte überprüfe deine Angaben.";
          status.setAttribute("data-state", "error");
        }
        var firstInvalid = form.querySelector('[aria-invalid="true"]');
        if (firstInvalid) firstInvalid.focus();
        return;
      }

      var formData = new FormData(form);
      var action = form.getAttribute("action");

      if (submitBtn) submitBtn.setAttribute("aria-disabled", "true");
      if (status) {
        status.textContent = "Nachricht wird gesendet …";
        status.removeAttribute("data-state");
      }

      fetch(action, {
        method: "POST",
        body: formData,
        headers: { Accept: "application/json" },
      })
        .then(function (response) {
          if (!response.ok) throw new Error("request-failed");
          return response.json().catch(function () {
            return { ok: true };
          });
        })
        .then(function () {
          if (status) {
            status.textContent =
              "Danke für deine Nachricht! Wir melden uns so schnell wie möglich.";
            status.setAttribute("data-state", "success");
          }
          form.reset();
        })
        .catch(function () {
          if (status) {
            status.textContent =
              "Die Nachricht konnte nicht automatisch gesendet werden. Bitte schreibe uns direkt per E-Mail, Anruf oder WhatsApp (siehe Kontaktdaten oben) — oder versuche es gleich noch einmal.";
            status.setAttribute("data-state", "error");
          }
        })
        .finally(function () {
          if (submitBtn) submitBtn.removeAttribute("aria-disabled");
        });
    });
  }

  /* -------------------------------------------------------------
   * 5. Footer-Jahr
   * ------------------------------------------------------------- */
  function initFooterYear() {
    var year = String(new Date().getFullYear());
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = year;
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initNav();
    initHeaderShadow();
    initLightbox();
    initContactForm();
    initFooterYear();
  });
})();
