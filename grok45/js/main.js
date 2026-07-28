(function () {
  const body = document.body;
  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("[data-nav]");
  const header = document.querySelector("[data-header]");
  const yearEls = document.querySelectorAll("[data-year]");
  yearEls.forEach((el) => {
    el.textContent = String(new Date().getFullYear());
  });

  if (!toggle || !nav) return;

  const focusableSelector =
    'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])';

  let lastFocus = null;

  function getFocusable() {
    return Array.from(nav.querySelectorAll(focusableSelector)).filter(
      (el) => !el.hasAttribute("disabled") && el.offsetParent !== null
    );
  }

  function openNav() {
    lastFocus = document.activeElement;
    body.classList.add("nav-open");
    toggle.setAttribute("aria-expanded", "true");
    const label = toggle.querySelector(".visually-hidden");
    if (label) label.textContent = "Menü schließen";
    const items = getFocusable();
    if (items[0]) items[0].focus();
  }

  function closeNav() {
    body.classList.remove("nav-open");
    toggle.setAttribute("aria-expanded", "false");
    const label = toggle.querySelector(".visually-hidden");
    if (label) label.textContent = "Menü öffnen";
    // close submenus
    nav.querySelectorAll("[data-sub-toggle]").forEach((btn) => {
      btn.setAttribute("aria-expanded", "false");
      const id = btn.getAttribute("aria-controls");
      const panel = id ? document.getElementById(id) : null;
      if (panel) panel.hidden = true;
    });
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  function isOpen() {
    return body.classList.contains("nav-open");
  }

  toggle.addEventListener("click", () => {
    if (isOpen()) closeNav();
    else openNav();
  });

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

  // submenu toggles
  nav.querySelectorAll("[data-sub-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const expanded = btn.getAttribute("aria-expanded") === "true";
      const id = btn.getAttribute("aria-controls");
      const panel = id ? document.getElementById(id) : null;
      // close siblings
      nav.querySelectorAll("[data-sub-toggle]").forEach((other) => {
        if (other === btn) return;
        other.setAttribute("aria-expanded", "false");
        const oid = other.getAttribute("aria-controls");
        const op = oid ? document.getElementById(oid) : null;
        if (op) op.hidden = true;
      });
      btn.setAttribute("aria-expanded", expanded ? "false" : "true");
      if (panel) panel.hidden = expanded;
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

  // desktop: close submenus on outside click
  document.addEventListener("click", (e) => {
    if (!header || header.contains(e.target)) return;
    nav.querySelectorAll("[data-sub-toggle]").forEach((btn) => {
      btn.setAttribute("aria-expanded", "false");
      const id = btn.getAttribute("aria-controls");
      const panel = id ? document.getElementById(id) : null;
      if (panel) panel.hidden = true;
    });
  });
})();
