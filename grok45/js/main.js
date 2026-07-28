(function () {
  const body = document.body;
  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("[data-nav]");
  const yearEls = document.querySelectorAll("[data-year]");
  yearEls.forEach((el) => {
    el.textContent = String(new Date().getFullYear());
  });

  if (!toggle || !nav) return;

  // Backdrop for mobile burger drawer (created once)
  let backdrop = document.querySelector("[data-nav-backdrop]");
  if (!backdrop) {
    backdrop = document.createElement("div");
    backdrop.className = "nav-backdrop";
    backdrop.setAttribute("data-nav-backdrop", "");
    backdrop.hidden = true;
    document.body.appendChild(backdrop);
  }

  const focusableSelector =
    'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])';

  let lastFocus = null;

  function isDesktopNav() {
    return window.matchMedia("(min-width: 1024px)").matches;
  }

  function getNavFocusable() {
    return Array.from(nav.querySelectorAll(focusableSelector)).filter((el) => {
      if (el.hasAttribute("disabled")) return false;
      // Skip non-interactive sub labels on mobile
      if (el.matches("[data-sub-toggle]") && !isDesktopNav()) return false;
      return el.offsetParent !== null;
    });
  }

  /** While open: toggle (close control) + nav items so Tab can reach "Menü schließen". */
  function getFocusable() {
    const navItems = getNavFocusable();
    if (!isOpen()) return navItems;
    return [toggle, ...navItems];
  }

  function openNav() {
    lastFocus = document.activeElement;
    body.classList.add("nav-open");
    toggle.setAttribute("aria-expanded", "true");
    if (backdrop) {
      backdrop.hidden = false;
    }
    const label = toggle.querySelector(".visually-hidden");
    if (label) label.textContent = "Menü schließen";
    // Mobile: nested menus always visible inside drawer
    revealAllSubmenus();
    const items = getNavFocusable();
    if (items[0]) items[0].focus();
  }

  function closeNav() {
    body.classList.remove("nav-open");
    toggle.setAttribute("aria-expanded", "false");
    if (backdrop) {
      backdrop.hidden = true;
    }
    const label = toggle.querySelector(".visually-hidden");
    if (label) label.textContent = "Menü öffnen";
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  function isOpen() {
    return body.classList.contains("nav-open");
  }

  function revealAllSubmenus() {
    nav.querySelectorAll("[data-sub-toggle]").forEach((btn) => {
      btn.setAttribute("aria-expanded", "true");
      const id = btn.getAttribute("aria-controls");
      const panel = id ? document.getElementById(id) : null;
      if (panel) {
        panel.hidden = false;
        panel.removeAttribute("hidden");
      }
    });
  }

  function prepareSubmenusForViewport() {
    // Always keep panels available; CSS handles hover (desktop) vs always-open (mobile)
    revealAllSubmenus();
    nav.querySelectorAll("[data-sub-toggle]").forEach((btn) => {
      if (isDesktopNav()) {
        btn.setAttribute("tabindex", "0");
        btn.removeAttribute("aria-disabled");
      } else {
        btn.setAttribute("tabindex", "-1");
        btn.setAttribute("aria-disabled", "true");
      }
    });
    // Leaving mobile width: force-close burger drawer
    if (isDesktopNav() && isOpen()) {
      body.classList.remove("nav-open");
      toggle.setAttribute("aria-expanded", "false");
      if (backdrop) backdrop.hidden = true;
      const label = toggle.querySelector(".visually-hidden");
      if (label) label.textContent = "Menü öffnen";
    }
  }

  toggle.addEventListener("click", () => {
    if (isOpen()) closeNav();
    else openNav();
  });

  if (backdrop) {
    backdrop.addEventListener("click", () => {
      if (isOpen()) closeNav();
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && isOpen()) {
      e.preventDefault();
      closeNav();
      return;
    }
    if (e.key !== "Tab" || !isOpen()) return;
    const items = getFocusable();
    if (!items.length) return;
    const first = items[0];
    const last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  // Submenus open via CSS hover/focus-within on desktop; no click-to-open.
  // Keep buttons from stealing clicks / toggling hidden state.
  nav.querySelectorAll("[data-sub-toggle]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
    });
  });

  // close mobile nav on internal link click
  nav.querySelectorAll("a[href]").forEach((link) => {
    link.addEventListener("click", () => {
      if (isOpen()) closeNav();
    });
  });

  // active nav: mark aria-current by pathname filename
  const file = (location.pathname.split("/").pop() || "index.html").toLowerCase();
  nav.querySelectorAll("a[href]").forEach((a) => {
    const href = (a.getAttribute("href") || "").toLowerCase();
    if (href === file || (file === "" && href === "index.html")) {
      a.setAttribute("aria-current", "page");
    }
  });

  prepareSubmenusForViewport();
  window.addEventListener("resize", prepareSubmenusForViewport);
})();
