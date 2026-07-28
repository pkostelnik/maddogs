(function () {
  const items = Array.from(document.querySelectorAll("[data-gallery-item]"));
  const lb = document.getElementById("lightbox");
  if (!items.length || !lb) return;

  const img = lb.querySelector("[data-lightbox-img]");
  const title = lb.querySelector("#lightbox-title");
  const btnClose = lb.querySelector("[data-lightbox-close]");
  const btnPrev = lb.querySelector("[data-lightbox-prev]");
  const btnNext = lb.querySelector("[data-lightbox-next]");
  const focusableSelector =
    'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])';
  let index = 0;
  let lastFocus = null;

  function getFocusable() {
    return Array.from(lb.querySelectorAll(focusableSelector)).filter(
      (el) => !el.hasAttribute("disabled") && el.offsetParent !== null
    );
  }

  function show(i) {
    index = (i + items.length) % items.length;
    const el = items[index];
    const src = el.getAttribute("data-full");
    const alt = el.getAttribute("data-alt") || "";
    if (img) {
      img.src = src;
      img.alt = alt;
    }
    if (title) title.textContent = alt || "Galeriebild";
  }

  function open(i) {
    lastFocus = document.activeElement;
    show(i);
    lb.hidden = false;
    lb.classList.add("is-open");
    document.body.classList.add("lightbox-open");
    document.body.classList.remove("nav-open");
    if (btnClose) btnClose.focus();
  }

  function close() {
    lb.hidden = true;
    lb.classList.remove("is-open");
    document.body.classList.remove("lightbox-open");
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  function isOpen() {
    return !lb.hidden && lb.classList.contains("is-open");
  }

  items.forEach((el, i) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      open(i);
    });
  });

  if (btnClose) btnClose.addEventListener("click", close);
  if (btnPrev) btnPrev.addEventListener("click", () => show(index - 1));
  if (btnNext) btnNext.addEventListener("click", () => show(index + 1));

  lb.addEventListener("click", (e) => {
    if (e.target === lb) close();
  });

  document.addEventListener("keydown", (e) => {
    if (!isOpen()) return;
    if (e.key === "Escape") {
      e.preventDefault();
      close();
      return;
    }
    if (e.key === "ArrowLeft") {
      e.preventDefault();
      show(index - 1);
      return;
    }
    if (e.key === "ArrowRight") {
      e.preventDefault();
      show(index + 1);
      return;
    }
    if (e.key !== "Tab") return;
    const focusable = getFocusable();
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
})();
