/*!
 * Mad Dogs Germany — main.js
 * ---------------------------------------------------------------------
 * Reines Vanilla JavaScript ohne Abhängigkeiten. Jede Funktion ist eine
 * PROGRESSIVE ENHANCEMENT: die Seite bleibt ohne JavaScript vollständig
 * nutzbar (Navigation ist dann dauerhaft sichtbar, das Kontaktformular
 * sendet ganz normal per HTML-Formular-Submit, Galerie-Links öffnen das
 * Originalbild direkt). Dieses Skript wird per `defer` geladen.
 * ---------------------------------------------------------------------
 */
(function () {
  "use strict";

  /* -------------------------------------------------------------
   * Hilfsfunktionen
   * ----------------------------------------------------------- */
  var prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  function scrollIntoViewA11y(target) {
    if (!target) return;
    target.scrollIntoView({
      behavior: prefersReducedMotion ? "auto" : "smooth",
      block: "start",
    });
    if (!target.hasAttribute("tabindex")) {
      target.setAttribute("tabindex", "-1");
    }
    target.focus({ preventScroll: true });
  }

  /* -------------------------------------------------------------
   * 1) Mobiles Navigations-Disclosure
   * ----------------------------------------------------------- */
  function initNav() {
    var toggle = document.querySelector("[data-nav-toggle]");
    var nav = document.querySelector("[data-primary-nav]");
    var header = document.querySelector(".site-header");
    if (!toggle || !nav) return;

    var desktopQuery = window.matchMedia("(min-width: 64em)");

    function setOpen(open) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      nav.setAttribute("data-open", open ? "true" : "false");
    }

    function isOpen() {
      return toggle.getAttribute("aria-expanded") === "true";
    }

    toggle.addEventListener("click", function () {
      setOpen(!isOpen());
    });

    // Menü schließen, wenn ein Link angeklickt wird (mobile Ansicht).
    nav.addEventListener("click", function (event) {
      if (event.target.closest("a") && !desktopQuery.matches) {
        setOpen(false);
      }
    });

    // Escape schließt das Menü und gibt den Fokus zurück auf den Button.
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && isOpen()) {
        setOpen(false);
        toggle.focus();
      }
    });

    // Klick außerhalb des Headers schließt das Menü.
    document.addEventListener("click", function (event) {
      if (isOpen() && header && !header.contains(event.target)) {
        setOpen(false);
      }
    });

    // Beim Wechsel über die Breakpoint-Grenze immer sauber zurücksetzen.
    function handleBreakpointChange() {
      setOpen(false);
    }
    if (typeof desktopQuery.addEventListener === "function") {
      desktopQuery.addEventListener("change", handleBreakpointChange);
    }

    // Header bekommt beim Scrollen einen dezenten Schatten.
    if (header) {
      var onScroll = function () {
        header.classList.toggle("is-scrolled", window.scrollY > 4);
      };
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });
    }
  }

  /* -------------------------------------------------------------
   * 2) Footer-Jahr
   * ----------------------------------------------------------- */
  function initYear() {
    var el = document.querySelector("[data-year]");
    if (el) el.textContent = String(new Date().getFullYear());
  }

  /* -------------------------------------------------------------
   * 3) Lightbox-Galerie (natives <dialog>)
   * ----------------------------------------------------------- */
  function initLightbox() {
    var dialog = document.querySelector("[data-lightbox]");
    var links = Array.prototype.slice.call(
      document.querySelectorAll("[data-lightbox-trigger]")
    );
    if (!dialog || links.length === 0) return;

    var imageEl = dialog.querySelector("[data-lightbox-image]");
    var captionEl = dialog.querySelector("[data-lightbox-caption]");
    var closeBtn = dialog.querySelector("[data-lightbox-close]");
    var prevBtn = dialog.querySelector("[data-lightbox-prev]");
    var nextBtn = dialog.querySelector("[data-lightbox-next]");
    var lastTrigger = null;
    var currentIndex = 0;

    function show(index) {
      currentIndex = (index + links.length) % links.length;
      var link = links[currentIndex];
      var fullSrc = link.getAttribute("href");
      var caption = link.getAttribute("data-caption") || "";
      imageEl.setAttribute("src", fullSrc);
      imageEl.setAttribute("alt", caption);
      captionEl.textContent = caption;
    }

    function open(index, trigger) {
      lastTrigger = trigger || null;
      show(index);
      if (typeof dialog.showModal === "function") {
        dialog.showModal();
      } else {
        dialog.setAttribute("open", "");
      }
    }

    function close() {
      if (typeof dialog.close === "function" && dialog.open) {
        dialog.close();
      } else {
        dialog.removeAttribute("open");
      }
    }

    links.forEach(function (link, index) {
      link.addEventListener("click", function (event) {
        event.preventDefault();
        open(index, link);
      });
    });

    if (closeBtn) closeBtn.addEventListener("click", close);
    if (nextBtn) nextBtn.addEventListener("click", function () { show(currentIndex + 1); });
    if (prevBtn) prevBtn.addEventListener("click", function () { show(currentIndex - 1); });

    // Klick auf den Backdrop (außerhalb von .lightbox__inner) schließt.
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) close();
    });

    dialog.addEventListener("keydown", function (event) {
      if (event.key === "ArrowRight") show(currentIndex + 1);
      if (event.key === "ArrowLeft") show(currentIndex - 1);
      // Escape wird von <dialog> nativ verarbeitet (schließt automatisch).
    });

    dialog.addEventListener("close", function () {
      imageEl.setAttribute("src", "");
      if (lastTrigger) lastTrigger.focus();
    });
  }

  /* -------------------------------------------------------------
   * 4) Kontaktformular: Validierung + mailto-Versand ohne Backend
   * ----------------------------------------------------------- */
  function initContactForm() {
    var form = document.querySelector("[data-contact-form]");
    if (!form) return;

    var statusEl = form.querySelector("[data-form-status]");
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // Erst nach dem ersten Sende-Versuch wird live (on blur/input) validiert.
    // So werden Nutzer:innen nicht schon beim bloßen Durchtabben mit
    // Fehlermeldungen konfrontiert, und es gibt keinen überraschenden
    // Layout-Sprung, während noch niemand "Senden" gedrückt hat.
    var hasAttemptedSubmit = false;

    var rules = {
      name: function (value) {
        return value.trim().length >= 2 ? "" : "Bitte gib deinen Namen ein.";
      },
      email: function (value) {
        return emailPattern.test(value.trim())
          ? ""
          : "Bitte gib eine gültige E-Mail-Adresse ein.";
      },
      message: function (value) {
        return value.trim().length >= 10
          ? ""
          : "Bitte beschreibe dein Anliegen in ein paar Worten (mind. 10 Zeichen).";
      },
    };

    function fieldError(field) {
      return form.querySelector("#" + field.id + "-error");
    }

    function validateField(field) {
      var rule = rules[field.name];
      if (!rule) return true;
      var message = rule(field.value);
      var errorEl = fieldError(field);
      field.setAttribute("data-touched", "true");
      if (message) {
        field.setAttribute("aria-invalid", "true");
        if (errorEl) errorEl.textContent = message;
        return false;
      }
      field.removeAttribute("aria-invalid");
      if (errorEl) errorEl.textContent = "";
      return true;
    }

    ["name", "email", "message"].forEach(function (fieldName) {
      var field = form.elements.namedItem(fieldName);
      if (!field) return;
      field.addEventListener("blur", function () {
        if (hasAttemptedSubmit) validateField(field);
      });
      field.addEventListener("input", function () {
        if (hasAttemptedSubmit && field.getAttribute("data-touched") === "true") {
          validateField(field);
        }
      });
    });

    function setStatus(message, state) {
      if (!statusEl) return;
      statusEl.textContent = message;
      statusEl.setAttribute("data-state", state);
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      hasAttemptedSubmit = true;

      // Honeypot: Wenn ausgefüllt, stillschweigend abbrechen (Spam-Bot).
      var honeypot = form.elements.namedItem("website");
      if (honeypot && honeypot.value) {
        form.reset();
        return;
      }

      var nameField = form.elements.namedItem("name");
      var emailField = form.elements.namedItem("email");
      var messageField = form.elements.namedItem("message");
      var consentField = form.elements.namedItem("consent");

      var validations = [
        validateField(nameField),
        validateField(emailField),
        validateField(messageField),
      ];

      var consentOk = !consentField || consentField.checked;
      if (consentField) {
        var consentError = fieldError(consentField);
        if (!consentOk) {
          if (consentError) {
            consentError.textContent =
              "Bitte stimme der Verarbeitung deiner Daten zu, damit wir antworten können.";
          }
        } else if (consentError) {
          consentError.textContent = "";
        }
      }

      var allValid = validations.every(Boolean) && consentOk;
      if (!allValid) {
        setStatus(
          "Bitte prüfe deine Angaben — einige Felder benötigen noch eine Korrektur.",
          "error"
        );
        var firstInvalid = form.querySelector('[aria-invalid="true"]');
        if (firstInvalid) firstInvalid.focus();
        return;
      }

      var subject = "Kontaktanfrage über die Website von " + nameField.value.trim();
      var body =
        "Name: " + nameField.value.trim() +
        "\nE-Mail: " + emailField.value.trim() +
        "\n\nNachricht:\n" + messageField.value.trim();

      var mailtoUrl =
        "mailto:info@mad-dogs-germany.de" +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);

      setStatus(
        "Dein E-Mail-Programm sollte sich jetzt mit einer vorausgefüllten Nachricht öffnen. " +
          "Falls sich nichts öffnet, schreib uns gerne direkt an info@mad-dogs-germany.de " +
          "oder per WhatsApp/Telefon.",
        "success"
      );

      window.location.href = mailtoUrl;
    });
  }

  /* -------------------------------------------------------------
   * 5) Sanftes Scrollen zu Sprungmarken + Fokusverwaltung
   * ----------------------------------------------------------- */
  function initAnchorFocus() {
    document.querySelectorAll('a[href*="#"]').forEach(function (link) {
      var url;
      try {
        url = new URL(link.href, window.location.href);
      } catch (e) {
        return;
      }
      var samePage =
        url.pathname === window.location.pathname && url.hash.length > 1;
      if (!samePage) return;

      link.addEventListener("click", function (event) {
        var target = document.querySelector(url.hash);
        if (!target) return;
        event.preventDefault();
        history.pushState(null, "", url.hash);
        scrollIntoViewA11y(target);
      });
    });
  }

  /* -------------------------------------------------------------
   * Start
   * ----------------------------------------------------------- */
  document.addEventListener("DOMContentLoaded", function () {
    initNav();
    initYear();
    initLightbox();
    initContactForm();
    initAnchorFocus();
  });
})();
