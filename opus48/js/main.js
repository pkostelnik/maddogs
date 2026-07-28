/* =========================================================================
   Mad Dogs Germany — main.js
   Progressive enhancement only. The site is fully usable without JavaScript.
   - Accessible mobile navigation (focus trap, Esc, backdrop, body-lock)
   - Reveal-on-scroll via IntersectionObserver
   - Accessible gallery lightbox using <dialog>
   - Client-side contact-form validation with mailto fallback
   - Sticky-header shadow + current year
   ========================================================================= */
(function () {
  "use strict";

  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------------------
     Mobile navigation
     ------------------------------------------------------------------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  var backdrop = document.querySelector(".nav-backdrop");
  var desktopQuery = window.matchMedia("(min-width: 62em)");

  function focusableIn(el) {
    return Array.prototype.slice.call(
      el.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])')
    ).filter(function (n) { return n.offsetParent !== null || n === document.activeElement; });
  }

  function openNav() {
    if (!nav || !toggle) return;
    nav.classList.add("is-open");
    if (backdrop) backdrop.classList.add("is-open");
    toggle.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
    var first = nav.querySelector("a, button");
    if (first) first.focus();
    document.addEventListener("keydown", onNavKeydown);
  }

  function closeNav(returnFocus) {
    if (!nav || !toggle) return;
    nav.classList.remove("is-open");
    if (backdrop) backdrop.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
    document.removeEventListener("keydown", onNavKeydown);
    if (returnFocus) toggle.focus();
  }

  function onNavKeydown(e) {
    if (e.key === "Escape") { closeNav(true); return; }
    if (e.key !== "Tab") return;
    // Simple focus trap across the toggle + nav panel
    var items = [toggle].concat(focusableIn(nav));
    if (!items.length) return;
    var firstEl = items[0];
    var lastEl = items[items.length - 1];
    if (e.shiftKey && document.activeElement === firstEl) {
      e.preventDefault(); lastEl.focus();
    } else if (!e.shiftKey && document.activeElement === lastEl) {
      e.preventDefault(); firstEl.focus();
    }
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      if (open) closeNav(false); else openNav();
    });
    if (backdrop) backdrop.addEventListener("click", function () { closeNav(true); });
    nav.addEventListener("click", function (e) {
      var link = e.target.closest("a");
      if (link) closeNav(false);
    });
    // Reset when moving to desktop layout
    var onChange = function () {
      if (desktopQuery.matches) closeNav(false);
    };
    if (desktopQuery.addEventListener) desktopQuery.addEventListener("change", onChange);
    else if (desktopQuery.addListener) desktopQuery.addListener(onChange);
  }

  /* ---------------------------------------------------------------------
     Sticky header shadow on scroll
     ------------------------------------------------------------------- */
  var header = document.querySelector(".site-header");
  if (header) {
    var lastScroll = -1;
    var onScroll = function () {
      var y = window.pageYOffset || document.documentElement.scrollTop;
      if (y > 4 && lastScroll <= 4) header.classList.add("is-scrolled");
      else if (y <= 4 && lastScroll > 4) header.classList.remove("is-scrolled");
      lastScroll = y;
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------------------------------------------------------------------
     Reveal on scroll
     ------------------------------------------------------------------- */
  var revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length) {
    if (prefersReduced || !("IntersectionObserver" in window)) {
      revealEls.forEach(function (el) { el.classList.add("is-visible"); });
    } else {
      var io = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            obs.unobserve(entry.target);
          }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.1 });
      revealEls.forEach(function (el) { io.observe(el); });
    }
  }

  /* ---------------------------------------------------------------------
     Gallery lightbox (<dialog>)
     ------------------------------------------------------------------- */
  var gallery = document.querySelector("[data-gallery]");
  var lightbox = document.getElementById("lightbox");
  if (gallery && lightbox && typeof lightbox.showModal === "function") {
    var lbImg = lightbox.querySelector(".lightbox__img");
    var lastTrigger = null;
    gallery.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-full]");
      if (!btn) return;
      e.preventDefault();
      lastTrigger = btn;
      lbImg.src = btn.getAttribute("data-full");
      lbImg.alt = btn.getAttribute("data-alt") || "";
      lightbox.showModal();
    });
    lightbox.addEventListener("click", function (e) {
      // click outside the image content closes
      if (e.target === lightbox || e.target.hasAttribute("data-close")) lightbox.close();
    });
    lightbox.addEventListener("close", function () {
      lbImg.removeAttribute("src");
      if (lastTrigger) lastTrigger.focus();
    });
  }

  /* ---------------------------------------------------------------------
     Contact form: accessible validation + graceful submit
     ------------------------------------------------------------------- */
  var form = document.querySelector("[data-contact-form]");
  if (form) {
    var status = form.querySelector(".form__status");

    var setError = function (field, msg) {
      var wrap = field.closest(".field");
      if (!wrap) return;
      wrap.classList.add("field--error");
      field.setAttribute("aria-invalid", "true");
      var err = wrap.querySelector(".field__error");
      if (err && msg) err.textContent = msg;
    };
    var clearError = function (field) {
      var wrap = field.closest(".field");
      if (!wrap) return;
      wrap.classList.remove("field--error");
      field.removeAttribute("aria-invalid");
    };

    form.querySelectorAll("input, textarea").forEach(function (f) {
      f.addEventListener("input", function () { clearError(f); });
    });

    var showStatus = function (state, msg) {
      if (!status) return;
      status.dataset.state = state;
      status.textContent = msg;
      status.hidden = false;
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (status) { status.hidden = true; status.textContent = ""; status.removeAttribute("data-state"); }

      // Honeypot: silently succeed for bots
      var hp = form.querySelector('[name="company"]');
      if (hp && hp.value) { showStatus("success", "Vielen Dank für deine Nachricht!"); return; }

      var name = form.querySelector('[name="name"]');
      var email = form.querySelector('[name="email"]');
      var message = form.querySelector('[name="message"]');
      var consent = form.querySelector('[name="consent"]');
      var firstInvalid = null;

      if (name && !name.value.trim()) { setError(name, "Bitte gib deinen Namen an."); firstInvalid = firstInvalid || name; }
      var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (email && !emailRe.test(email.value.trim())) { setError(email, "Bitte gib eine gültige E-Mail-Adresse ein."); firstInvalid = firstInvalid || email; }
      if (message && message.value.trim().length < 5) { setError(message, "Bitte schreib uns kurz, worum es geht."); firstInvalid = firstInvalid || message; }
      if (consent && !consent.checked) { setError(consent, "Bitte stimme der Verarbeitung zu."); firstInvalid = firstInvalid || consent; }

      if (firstInvalid) {
        firstInvalid.focus();
        showStatus("error", "Bitte prüfe die markierten Felder.");
        return;
      }

      var endpoint = form.getAttribute("data-endpoint");
      var configured = endpoint && endpoint.indexOf("DEINE-ID") === -1 && endpoint.indexOf("your-id") === -1;

      if (configured && window.fetch) {
        var submitBtn = form.querySelector('[type="submit"]');
        if (submitBtn) submitBtn.disabled = true;
        fetch(endpoint, {
          method: "POST",
          headers: { "Accept": "application/json" },
          body: new FormData(form)
        }).then(function (res) {
          if (res.ok) {
            form.reset();
            showStatus("success", "Danke! Deine Nachricht wurde gesendet – wir melden uns zeitnah.");
          } else {
            throw new Error("bad response");
          }
        }).catch(function () {
          showStatus("error", "Senden fehlgeschlagen. Bitte per WhatsApp oder E-Mail melden.");
        }).finally(function () {
          if (submitBtn) submitBtn.disabled = false;
        });
      } else {
        // No backend configured → open the user's mail client (works offline/static)
        var to = form.getAttribute("data-mailto") || "info@mad-dogs-germany.de";
        var subject = "Anfrage über die Website";
        var body =
          "Name: " + (name ? name.value.trim() : "") + "\n" +
          "E-Mail: " + (email ? email.value.trim() : "") + "\n\n" +
          (message ? message.value.trim() : "");
        window.location.href = "mailto:" + to +
          "?subject=" + encodeURIComponent(subject) +
          "&body=" + encodeURIComponent(body);
        showStatus("success", "Dein E-Mail-Programm öffnet sich mit der vorausgefüllten Nachricht. Alternativ erreichst du uns direkt per WhatsApp.");
      }
    });
  }

  /* ---------------------------------------------------------------------
     Current year in footer
     ------------------------------------------------------------------- */
  var yearEls = document.querySelectorAll("[data-year]");
  yearEls.forEach(function (el) { el.textContent = String(new Date().getFullYear()); });
})();
