/* =========================================================================
   Mad Dogs Germany — Progressive Enhancement JavaScript (Redesign 2026)
   - Accessible Hamburger Navigation with complete keyboard Focus Trap and Body Scroll Lock
   - Theme management (Sync light/dark theme preference with local storage)
   - IntersectionObserver for fluid Reveal-on-scroll animations
   - Accessible <dialog> native lightbox component for the gallery
   - Complete contact form validation with dynamic ARIA announcements
   ========================================================================= */

(function () {
  "use strict";

  // Check user preference for reduced motion
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------------------
     1. THEME SWITCHING (Light / Dark Mode)
     ------------------------------------------------------------------- */
  const themeToggleBtn = document.querySelector(".theme-toggle");
  const storedTheme = localStorage.getItem("theme");
  const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  
  // Set initial theme
  const initialTheme = storedTheme || (systemDark ? "dark" : "light");
  document.documentElement.setAttribute("data-theme", initialTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", function () {
      const currentTheme = document.documentElement.getAttribute("data-theme");
      const newTheme = currentTheme === "dark" ? "light" : "dark";
      
      document.documentElement.setAttribute("data-theme", newTheme);
      localStorage.setItem("theme", newTheme);
      
      // Update screen reader status announcement if desired
      announceToScreenReader(`Farbschema geändert zu ${newTheme === "dark" ? "Dunkelmodus" : "Hellmodus"}`);
    });
  }

  /* Screen Reader Live Politeness Helper */
  function announceToScreenReader(message) {
    let announcer = document.getElementById("sr-announcer");
    if (!announcer) {
      announcer = document.createElement("div");
      announcer.id = "sr-announcer";
      announcer.className = "sr-only";
      announcer.setAttribute("aria-live", "polite");
      document.body.appendChild(announcer);
    }
    announcer.textContent = message;
  }

  /* ---------------------------------------------------------------------
     2. ACCESSIBLE MOBILE DRAWER WITH SCROLL LOCK & FOCUS TRAP
     ------------------------------------------------------------------- */
  const toggleBtn = document.querySelector(".nav-toggle");
  const navMenu = document.querySelector(".nav-menu");
  const backdrop = document.querySelector(".backdrop");
  let previouslyFocusedEl = null;

  function getFocusableElements(element) {
    return Array.from(
      element.querySelectorAll(
        'a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
      )
    ).filter(el => el.offsetWidth > 0 || el.offsetHeight > 0 || el === document.activeElement);
  }

  function openMenu() {
    if (!toggleBtn || !navMenu || !backdrop) return;
    previouslyFocusedEl = document.activeElement;
    
    navMenu.classList.add("is-open");
    backdrop.classList.add("is-open");
    toggleBtn.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden"; // Scroll lock

    // Focus the first element inside the drawer
    const focusable = getFocusableElements(navMenu);
    if (focusable.length > 0) {
      setTimeout(() => focusable[0].focus(), 50);
    }

    document.addEventListener("keydown", trapFocus);
  }

  function closeMenu(shouldReturnFocus = false) {
    if (!toggleBtn || !navMenu || !backdrop) return;
    
    navMenu.classList.remove("is-open");
    backdrop.classList.remove("is-open");
    toggleBtn.setAttribute("aria-expanded", "false");
    document.body.style.overflow = ""; // Remove scroll lock

    document.removeEventListener("keydown", trapFocus);

    if (shouldReturnFocus && previouslyFocusedEl) {
      previouslyFocusedEl.focus();
    }
  }

  function trapFocus(e) {
    if (e.key === "Escape") {
      closeMenu(true);
      return;
    }
    if (e.key !== "Tab") return;

    // Combine toggle button and drawer list for the focus loop
    const focusable = [toggleBtn].concat(getFocusableElements(navMenu));
    if (focusable.length === 0) return;

    const firstEl = focusable[0];
    const lastEl = focusable[focusable.length - 1];

    if (e.shiftKey) {
      if (document.activeElement === firstEl) {
        e.preventDefault();
        lastEl.focus();
      }
    } else {
      if (document.activeElement === lastEl) {
        e.preventDefault();
        firstEl.focus();
      }
    }
  }

  if (toggleBtn && navMenu && backdrop) {
    toggleBtn.addEventListener("click", function () {
      const isOpen = toggleBtn.getAttribute("aria-expanded") === "true";
      if (isOpen) {
        closeMenu(false);
      } else {
        openMenu();
      }
    });

    backdrop.addEventListener("click", function () {
      closeMenu(true);
    });

    // Close on navigation link click (useful for same-page anchors or transition)
    navMenu.addEventListener("click", function (e) {
      const link = e.target.closest(".nav-link");
      if (link) {
        closeMenu(false);
      }
    });

    // Ensure menu is closed when viewport crosses the desktop threshold
    const mql = window.matchMedia("(min-width: 62em)");
    const handleMediaQueryChange = function (e) {
      if (e.matches) {
        closeMenu(false);
      }
    };
    if (mql.addEventListener) {
      mql.addEventListener("change", handleMediaQueryChange);
    } else if (mql.addListener) {
      mql.addListener(handleMediaQueryChange); // IE / Legacy Safari
    }
  }

  /* ---------------------------------------------------------------------
     3. INTERSECTION OBSERVER FOR REVEAL ANIMATIONS
     ------------------------------------------------------------------- */
  const revealElements = document.querySelectorAll(".reveal");
  if (revealElements.length > 0) {
    if (prefersReduced || !("IntersectionObserver" in window)) {
      // Gracefully show everything immediately if system prefers reduced motion
      revealElements.forEach(el => el.classList.add("is-visible"));
    } else {
      const observer = new IntersectionObserver((entries, observerInstance) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observerInstance.unobserve(entry.target); // Trigger animation once
          }
        });
      }, {
        rootMargin: "0px 0px -10% 0px",
        threshold: 0.1
      });

      revealElements.forEach(el => observer.observe(el));
    }
  }

  /* ---------------------------------------------------------------------
     4. GALLERY LIGHTBOX WITH NATIVE <DIALOG> (Progressive Enhancement)
     ------------------------------------------------------------------- */
  const gallery = document.querySelector("[data-gallery]");
  const lightboxDialog = document.getElementById("lightbox");

  if (gallery && lightboxDialog && typeof lightboxDialog.showModal === "function") {
    const lightboxImg = lightboxDialog.querySelector(".lightbox__img");
    let lastActiveTrigger = null;

    gallery.addEventListener("click", function (e) {
      const trigger = e.target.closest("[data-full-img]");
      if (!trigger) return;
      
      e.preventDefault();
      lastActiveTrigger = trigger;

      const fullImgUrl = trigger.getAttribute("data-full-img");
      const imgAlt = trigger.getAttribute("data-alt") || "";

      lightboxImg.setAttribute("src", fullImgUrl);
      lightboxImg.setAttribute("alt", imgAlt);

      // Open native accessible Modal
      lightboxDialog.showModal();
    });

    // Close logic
    lightboxDialog.addEventListener("click", function (e) {
      // Close modal on background backdrop click or explicit close trigger
      if (e.target === lightboxDialog || e.target.closest("[data-close]")) {
        lightboxDialog.close();
      }
    });

    lightboxDialog.addEventListener("close", function () {
      // Clear src to save memory / bandwidth and return focus
      lightboxImg.removeAttribute("src");
      lightboxImg.removeAttribute("alt");
      if (lastActiveTrigger) {
        lastActiveTrigger.focus();
      }
    });
  }

  /* ---------------------------------------------------------------------
     5. CONTACT FORM CLIENT-SIDE VALIDATION & MAILTO BACKDROP HANDLER
     ------------------------------------------------------------------- */
  const contactForm = document.querySelector("[data-contact-form]");

  if (contactForm) {
    const statusBox = contactForm.querySelector(".form-status");

    // Clear error styling on input focus / change
    const fields = contactForm.querySelectorAll("input, textarea");
    fields.forEach(field => {
      field.addEventListener("input", function () {
        clearFieldError(field);
      });
    });

    function setFieldError(field, errorMessage) {
      const fieldContainer = field.closest(".field");
      if (!fieldContainer) return;

      fieldContainer.classList.add("field--error");
      field.setAttribute("aria-invalid", "true");
      
      const errorLabel = fieldContainer.querySelector(".field__error");
      if (errorLabel) {
        errorLabel.textContent = errorMessage;
      }
    }

    function clearFieldError(field) {
      const fieldContainer = field.closest(".field");
      if (!fieldContainer) return;

      fieldContainer.classList.remove("field--error");
      field.removeAttribute("aria-invalid");
    }

    function displayFormStatus(state, message) {
      if (!statusBox) return;
      statusBox.setAttribute("data-state", state);
      statusBox.textContent = message;
      statusBox.removeAttribute("hidden");
      
      // Accessibility: Announce the form error/success state immediately to screen readers
      announceToScreenReader(`${state === "success" ? "Erfolg" : "Fehler"}: ${message}`);
    }

    function hideFormStatus() {
      if (!statusBox) return;
      statusBox.setAttribute("hidden", "true");
      statusBox.textContent = "";
      statusBox.removeAttribute("data-state");
    }

    contactForm.addEventListener("submit", function (e) {
      e.preventDefault();
      hideFormStatus();

      // Bot honeypot verification
      const honeypot = contactForm.querySelector('[name="company_name"]');
      if (honeypot && honeypot.value) {
        // Silently succeed for automated bots
        displayFormStatus("success", "Vielen Dank für Ihre Anfrage! Wir werden uns in Kürze melden.");
        contactForm.reset();
        return;
      }

      const nameEl = contactForm.querySelector('[name="name"]');
      const emailEl = contactForm.querySelector('[name="email"]');
      const messageEl = contactForm.querySelector('[name="message"]');
      const consentEl = contactForm.querySelector('[name="consent"]');
      
      let firstInvalidEl = null;

      // Validate Name
      if (nameEl && !nameEl.value.trim()) {
        setFieldError(nameEl, "Bitte geben Sie Ihren Namen ein.");
        firstInvalidEl = firstInvalidEl || nameEl;
      }

      // Validate Email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (emailEl && !emailRegex.test(emailEl.value.trim())) {
        setFieldError(emailEl, "Bitte geben Sie eine gültige E-Mail-Adresse ein.");
        firstInvalidEl = firstInvalidEl || emailEl;
      }

      // Validate Message length
      if (messageEl && messageEl.value.trim().length < 10) {
        setFieldError(messageEl, "Ihre Nachricht sollte mindestens 10 Zeichen lang sein.");
        firstInvalidEl = firstInvalidEl || messageEl;
      }

      // Validate Consent
      if (consentEl && !consentEl.checked) {
        setFieldError(consentEl, "Sie müssen der Datenschutzerklärung zustimmen.");
        firstInvalidEl = firstInvalidEl || consentEl;
      }

      if (firstInvalidEl) {
        firstInvalidEl.focus();
        displayFormStatus("error", "Bitte korrigieren Sie die markierten Felder vor dem Senden.");
        return;
      }

      // Form is fully validated!
      const endpoint = contactForm.getAttribute("data-endpoint");
      // Check if a real endpoint (e.g. Formspree / Web3Forms / send.php) is active, instead of the default placeholder
      const isEndpointConfigured = endpoint && !endpoint.includes("DEINE-ID") && !endpoint.includes("your-id");

      if (isEndpointConfigured && window.fetch) {
        const submitBtn = contactForm.querySelector('[type="submit"]');
        if (submitBtn) submitBtn.disabled = true;

        displayFormStatus("success", "Ihre Nachricht wird gesendet...");

        fetch(endpoint, {
          method: "POST",
          headers: { "Accept": "application/json" },
          body: new FormData(contactForm)
        })
        .then(response => {
          if (response.ok) {
            contactForm.reset();
            displayFormStatus("success", "Vielen Dank! Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns in Kürze bei Ihnen.");
          } else {
            throw new Error("Form submission error");
          }
        })
        .catch(() => {
          displayFormStatus("error", "Das Senden der Nachricht ist fehlgeschlagen. Bitte kontaktieren Sie uns direkt per WhatsApp oder E-Mail.");
        })
        .finally(() => {
          if (submitBtn) submitBtn.disabled = false;
        });
      } else {
        // Fallback: No cloud backend set. Open native mail client with secure structured body (static compliant)
        const recipientEmail = contactForm.getAttribute("data-mailto") || "info@mad-dogs-germany.de";
        const subject = "Anfrage über die Mad Dogs Website";
        const bodyText = 
          `Hallo Chris,\n\n` +
          `ich habe eine Anfrage über deine Website gesendet:\n\n` +
          `Name: ${nameEl ? nameEl.value.trim() : ""}\n` +
          `E-Mail: ${emailEl ? emailEl.value.trim() : ""}\n\n` +
          `Nachricht:\n${messageEl ? messageEl.value.trim() : ""}\n\n` +
          `Beste Grüße`;

        window.location.href = `mailto:${recipientEmail}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(bodyText)}`;
        displayFormStatus("success", "Ihr E-Mail-Programm wurde mit den Formulardaten geöffnet. Senden Sie die E-Mail ab, um die Anfrage abzuschließen. Alternativ erreichen Sie uns per WhatsApp.");
      }
    });
  }

  /* ---------------------------------------------------------------------
     6. CURRENT COPYRIGHT YEAR UPDATER
     ------------------------------------------------------------------- */
  const yearPlaceholders = document.querySelectorAll("[data-year]");
  yearPlaceholders.forEach(el => {
    el.textContent = String(new Date().getFullYear());
  });
})();
