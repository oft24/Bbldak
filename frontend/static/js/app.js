(() => {
  "use strict";

  const productData = document.querySelector("#product-data");
  if (!productData) return;

  const payload = JSON.parse(productData.textContent);
  const products = payload.featured;
  const catalogProducts = payload.catalog;
  const productById = new Map(catalogProducts.map((product) => [product.id, product]));
  products.forEach((product) => {
    productById.set(product.id, { ...productById.get(product.id), ...product });
  });
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const root = document.documentElement;

  const dom = {
    header: document.querySelector("[data-header]"),
    carousel: document.querySelector("[data-carousel]"),
    cards: [...document.querySelectorAll("[data-card]")],
    tabs: [...document.querySelectorAll("[data-select]")],
    lines: [...document.querySelectorAll("[data-flavor-line]")],
    number: document.querySelector("[data-number]"),
    sku: document.querySelector("[data-sku]"),
    name: document.querySelector("[data-name]"),
    description: document.querySelector("[data-description]"),
    price: document.querySelector("[data-price]"),
    weight: document.querySelector("[data-weight]"),
    heatFill: document.querySelector("[data-heat-fill]"),
    heatLabel: document.querySelector("[data-heat-label]"),
    quantity: document.querySelector("[data-quantity]"),
    storyTitle: document.querySelector("[data-story-title]"),
    storyCopy: document.querySelector("[data-story-copy]"),
    storyImage: document.querySelector("[data-story-image]"),
    shu: document.querySelector("[data-shu]"),
    kcal: document.querySelector("[data-kcal]"),
    cookTime: document.querySelector("[data-cook-time]"),
    storyWeight: document.querySelector("[data-story-weight]"),
    storyNote: document.querySelector("[data-story-note]"),
    nutritionSource: document.querySelector("[data-nutrition-source]"),
    directionsTitle: document.querySelector("[data-directions-title]"),
    directionsIntro: document.querySelector("[data-directions-intro]"),
    directionTitles: [...document.querySelectorAll("[data-direction-title]")],
    directionTexts: [...document.querySelectorAll("[data-direction-text]")],
    preparedName: document.querySelector("[data-prepared-name]"),
    preparedImage: document.querySelector("[data-prepared-image]"),
    preparedSource: document.querySelector("[data-prepared-source]"),
    pairingTitles: [...document.querySelectorAll("[data-pairing-title]")],
    pairingTexts: [...document.querySelectorAll("[data-pairing-text]")],
    phoneImage: document.querySelector("[data-phone-image]"),
    phoneName: document.querySelector("[data-phone-name]"),
    phoneTagline: document.querySelector("[data-phone-tagline]"),
    phonePrice: document.querySelector("[data-phone-price]"),
    phoneHeat: document.querySelector("[data-phone-heat]"),
    cartCount: document.querySelector("[data-cart-count]"),
    mobileCartCount: document.querySelector("[data-mobile-cart-count]"),
    cartTitleCount: document.querySelector("[data-cart-title-count]"),
    cartDrawer: document.querySelector("[data-cart-drawer]"),
    cartScrim: document.querySelector("[data-cart-scrim]"),
    cartItems: document.querySelector("[data-cart-items]"),
    cartEmpty: document.querySelector("[data-cart-empty]"),
    subtotal: document.querySelector("[data-subtotal]"),
    shippingMessage: document.querySelector("[data-shipping-message]"),
    checkoutButton: document.querySelector("[data-open-checkout]"),
    searchDialog: document.querySelector("[data-search-dialog]"),
    searchInput: document.querySelector("[data-search-input]"),
    searchResults: [...document.querySelectorAll("[data-search-result]")],
    noResults: document.querySelector("[data-no-results]"),
    checkoutDialog: document.querySelector("[data-checkout-dialog]"),
    checkoutForm: document.querySelector("[data-checkout-form]"),
    checkoutFormView: document.querySelector("[data-checkout-form-view]"),
    checkoutSuccess: document.querySelector("[data-checkout-success]"),
    checkoutError: document.querySelector("[data-checkout-error]"),
    orderId: document.querySelector("[data-order-id]"),
    orderTotal: document.querySelector("[data-order-total]"),
    toast: document.querySelector("[data-toast]"),
    nav: document.querySelector("[data-nav]"),
    navToggle: document.querySelector("[data-nav-toggle]"),
    catalogFilters: [...document.querySelectorAll("[data-catalog-filter]")],
    catalogCards: [...document.querySelectorAll("[data-catalog-card]")],
    catalogAdds: [...document.querySelectorAll("[data-catalog-add]")],
  };

  const state = {
    selected: 0,
    quantity: 1,
    angle: 0,
    target: 0,
    velocity: 0,
    dragging: false,
    dragStartX: 0,
    dragStartAngle: 0,
    lastX: 0,
    moved: 0,
    lookX: 0,
    lookY: 0,
    lookTargetX: 0,
    lookTargetY: 0,
    cart: loadCart(),
    toastTimer: null,
    lastCartFocus: null,
  };

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function modulo(value, size) {
    return ((value % size) + size) % size;
  }

  function carouselDistance(value) {
    return modulo(value + products.length / 2, products.length) - products.length / 2;
  }

  function cycleTo(index) {
    const rounded = Math.round(state.target);
    const current = modulo(rounded, products.length);
    return rounded + carouselDistance(index - current);
  }

  function setTheme(index) {
    const product = products[index];
    state.selected = index;
    root.style.setProperty("--bg-a", product.colors.bg_a);
    root.style.setProperty("--bg-b", product.colors.bg_b);
    root.style.setProperty("--glow", product.colors.glow);
    root.style.setProperty("--ink", product.colors.ink);
    root.style.setProperty("--accent", product.colors.accent);

    const themeMeta = document.querySelector('meta[name="theme-color"]');
    if (themeMeta) themeMeta.setAttribute("content", product.colors.bg_a);

    dom.number.textContent = product.number;
    dom.sku.textContent = product.sku;
    dom.name.textContent = product.name;
    dom.description.textContent = product.description;
    dom.price.textContent = product.price_label;
    dom.weight.textContent = product.weight;
    dom.heatFill.style.width = `${product.heat}%`;
    dom.heatLabel.textContent = product.heat_label;
    dom.storyTitle.innerHTML = product.story_title.join("<br>");
    dom.storyCopy.textContent = product.story;
    dom.storyImage.src = product.image;
    dom.storyImage.alt = `Paquete Buldak ${product.name}`;
    dom.shu.textContent = product.shu;
    dom.kcal.textContent = product.kcal;
    dom.cookTime.textContent = product.cook_time;
    dom.storyWeight.textContent = product.weight.split(" · ")[0];
    dom.storyNote.innerHTML = product.story_note.replace("\n", "<br>");
    dom.nutritionSource.href = product.nutrition_source_url;
    dom.directionsTitle.innerHTML = product.directions_title.join("<br>");
    dom.directionsIntro.textContent = product.directions_intro;
    dom.directionTitles.forEach((element, directionIndex) => {
      element.textContent = product.directions[directionIndex].title;
    });
    dom.directionTexts.forEach((element, directionIndex) => {
      element.textContent = product.directions[directionIndex].text;
    });

    dom.preparedName.textContent = product.name;
    dom.preparedImage.src = product.prepared_image;
    dom.preparedImage.alt = product.prepared_alt;
    dom.preparedSource.textContent = product.prepared_source;
    dom.preparedSource.href = product.prepared_source_url;
    dom.pairingTitles.forEach((element, pairingIndex) => {
      element.textContent = product.recommendations[pairingIndex].title;
    });
    dom.pairingTexts.forEach((element, pairingIndex) => {
      element.textContent = product.recommendations[pairingIndex].text;
    });
    dom.phoneImage.src = product.image;
    dom.phoneImage.alt = `Buldak ${product.name} ramen pack`;
    dom.phoneName.textContent = product.name;
    dom.phoneTagline.textContent = product.tagline;
    dom.phonePrice.textContent = product.price_label;
    dom.phoneHeat.style.width = `${product.heat}%`;
    document.title = `BuldakShop — ${product.name}`;

    dom.cards.forEach((card, cardIndex) => {
      const active = cardIndex === index;
      card.classList.toggle("is-active", active);
      card.setAttribute("aria-pressed", String(active));
    });
    dom.tabs.forEach((tab, tabIndex) => {
      const active = tabIndex === index;
      tab.classList.toggle("is-active", active);
      tab.setAttribute("aria-pressed", String(active));
    });
    dom.lines.forEach((line, lineIndex) => line.classList.toggle("is-active", lineIndex === index));
  }

  function goTo(index, options = {}) {
    const normalized = modulo(index, products.length);
    state.target = cycleTo(normalized);
    state.velocity += carouselDistance(normalized - state.selected) * 0.015;
    setTheme(normalized);
    if (options.scrollTop) {
      document.querySelector("#top").scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth" });
    }
  }

  function step(direction) {
    goTo(state.selected + direction);
  }

  function drawCarousel() {
    if (!state.dragging) {
      const delta = state.target - state.angle;
      state.velocity += delta * 0.038;
      state.velocity *= 0.84;
      state.angle += state.velocity;
      if (Math.abs(delta) < 0.0008 && Math.abs(state.velocity) < 0.0008) {
        state.angle = state.target;
        state.velocity = 0;
      }
    }

    const radius = clamp(window.innerWidth * 0.29, 260, 445);
    const depth = clamp(window.innerWidth * 0.25, 230, 390);
    state.lookX += (state.lookTargetX - state.lookX) * 0.09;
    state.lookY += (state.lookTargetY - state.lookY) * 0.09;
    dom.cards.forEach((card, index) => {
      const distance = carouselDistance(index - state.angle);
      const theta = distance * ((Math.PI * 2) / products.length);
      const x = Math.sin(theta) * radius;
      const z = (Math.cos(theta) - 1) * depth;
      const proximity = clamp(1 + z / (depth * 2.8), 0, 1);
      const scale = 0.68 + proximity * 0.32;
      const lookStrength = Math.pow(proximity, 8);
      const rotationY = distance * -24 + state.lookX * 14 * lookStrength;
      const rotationX = state.lookY * -8.5 * lookStrength;
      const float = reducedMotion ? 0 : Math.sin(performance.now() / 2100 + index * 2.1) * 5 * proximity;
      card.style.transform = `translate3d(${x.toFixed(1)}px, ${float.toFixed(1)}px, ${z.toFixed(1)}px) rotateY(${rotationY.toFixed(1)}deg) rotateX(${rotationX.toFixed(1)}deg) scale(${scale.toFixed(3)})`;
      card.style.opacity = String(0.36 + proximity * 0.64);
      card.style.filter = proximity > 0.985 ? "none" : `blur(${((1 - proximity) * 4).toFixed(2)}px)`;
      card.style.zIndex = String(1000 + Math.round(z));
    });

    requestAnimationFrame(drawCarousel);
  }

  function nearestSelectionFromAngle() {
    const selected = modulo(Math.round(state.angle), products.length);
    if (selected !== state.selected) setTheme(selected);
  }

  function onPointerDown(event) {
    if (event.pointerType === "mouse" && event.button !== 0) return;
    state.dragging = true;
    state.dragStartX = event.clientX;
    state.lastX = event.clientX;
    state.dragStartAngle = state.angle;
    state.moved = 0;
    state.velocity = 0;
    dom.carousel.classList.add("is-dragging");
    dom.carousel.setPointerCapture?.(event.pointerId);
  }

  function onPointerMove(event) {
    if (event.pointerType !== "touch") {
      state.lookTargetX = clamp((event.clientX / window.innerWidth) * 2 - 1, -1, 1);
      state.lookTargetY = clamp((event.clientY / window.innerHeight) * 2 - 1, -1, 1);
      state.lookX += (state.lookTargetX - state.lookX) * 0.68;
      state.lookY += (state.lookTargetY - state.lookY) * 0.68;
    }

    if (!state.dragging) return;
    const delta = event.clientX - state.dragStartX;
    state.moved = Math.max(state.moved, Math.abs(delta));
    state.angle = state.dragStartAngle - delta / clamp(window.innerWidth * 0.25, 210, 340);
    state.velocity = -(event.clientX - state.lastX) / 310;
    state.lastX = event.clientX;
    nearestSelectionFromAngle();
  }

  function onPointerUp(event) {
    if (!state.dragging) return;
    state.dragging = false;
    dom.carousel.classList.remove("is-dragging");
    dom.carousel.releasePointerCapture?.(event.pointerId);
    state.target = Math.round(state.angle + state.velocity * 2.4);
    goTo(modulo(state.target, products.length));
  }

  function loadCart() {
    try {
      const stored = JSON.parse(localStorage.getItem("buldak-cart") || "[]");
      if (!Array.isArray(stored)) return [];
      const legacyIds = { carbonara: "811140", original: "811120", quattro: "811150" };
      return stored
        .map((item) => ({ id: legacyIds[item.id] || String(item.id), quantity: Number(item.quantity) }))
        .filter((item) => productById.has(item.id) && Number.isInteger(item.quantity) && item.quantity > 0 && item.quantity <= 20);
    } catch {
      return [];
    }
  }

  function saveCart() {
    try {
      localStorage.setItem("buldak-cart", JSON.stringify(state.cart));
    } catch {
      // A blocked storage API should not prevent shopping during this visit.
    }
  }

  function cartCount() {
    return state.cart.reduce((total, item) => total + item.quantity, 0);
  }

  function addToCart(id, quantity = 1) {
    const product = productById.get(id);
    if (!product || product.is_available === false) return;
    const existing = state.cart.find((item) => item.id === id);
    if (existing) existing.quantity = Math.min(20, existing.quantity + quantity);
    else state.cart.push({ id, quantity: clamp(quantity, 1, 20) });
    saveCart();
    renderCart();
    showToast(`${product.name} se agregó al carrito.`);
  }

  function changeCartQuantity(id, amount) {
    const item = state.cart.find((entry) => entry.id === id);
    if (!item) return;
    item.quantity = clamp(item.quantity + amount, 0, 20);
    if (item.quantity === 0) state.cart = state.cart.filter((entry) => entry.id !== id);
    saveCart();
    renderCart();
  }

  function removeCartItem(id) {
    state.cart = state.cart.filter((item) => item.id !== id);
    saveCart();
    renderCart();
  }

  function renderCart() {
    const count = cartCount();
    dom.cartCount.textContent = String(count);
    dom.mobileCartCount.textContent = String(count);
    dom.cartTitleCount.textContent = String(count);
    const subtotal = state.cart.reduce((total, item) => {
      const product = productById.get(item.id);
      return total + Number(product.price) * item.quantity;
    }, 0);
    dom.subtotal.textContent = `$${subtotal.toFixed(2)}`;
    dom.checkoutButton.disabled = count === 0;
    dom.cartEmpty.classList.toggle("is-visible", count === 0);
    dom.cartItems.hidden = count === 0;
    dom.shippingMessage.textContent = count === 0
      ? "Envío provisional: $0.00."
      : `${count} ${count === 1 ? "artículo" : "artículos"} · envío provisional $0.00.`;

    dom.cartItems.innerHTML = state.cart.map((item) => {
      const product = productById.get(item.id);
      return `
        <article class="cart-item" data-cart-item="${product.id}">
          <div class="cart-item__image"><img src="${product.image}" alt=""></div>
          <div class="cart-item__details">
            <div class="cart-item__top"><h3>${product.name}</h3><strong>$${(Number(product.price) * item.quantity).toFixed(2)}</strong></div>
            <p>${product.weight} · ${product.price_label} c/u</p>
            <div class="cart-item__actions">
              <div class="mini-stepper" aria-label="Cantidad de ${product.name}">
                <button type="button" data-cart-minus="${product.id}" aria-label="Reducir cantidad de ${product.name}">−</button>
                <span>${item.quantity}</span>
                <button type="button" data-cart-plus="${product.id}" aria-label="Aumentar cantidad de ${product.name}">+</button>
              </div>
              <button class="remove-item" type="button" data-cart-remove="${product.id}">Eliminar</button>
            </div>
          </div>
        </article>`;
    }).join("");

    dom.cartCount.classList.remove("is-bumping");
    requestAnimationFrame(() => dom.cartCount.classList.add("is-bumping"));
    window.setTimeout(() => dom.cartCount.classList.remove("is-bumping"), 300);
  }

  function openCart() {
    if (dom.searchDialog.open) dom.searchDialog.close();
    state.lastCartFocus = document.activeElement;
    dom.cartDrawer.classList.add("is-open");
    dom.cartScrim.classList.add("is-open");
    dom.cartDrawer.setAttribute("aria-hidden", "false");
    document.body.classList.add("is-locked");
    window.setTimeout(() => dom.cartDrawer.querySelector("[data-close-cart]")?.focus(), 100);
  }

  function closeCart({ restoreFocus = true } = {}) {
    dom.cartDrawer.classList.remove("is-open");
    dom.cartScrim.classList.remove("is-open");
    dom.cartDrawer.setAttribute("aria-hidden", "true");
    if (!dom.searchDialog.open && !dom.checkoutDialog.open) document.body.classList.remove("is-locked");
    if (restoreFocus) state.lastCartFocus?.focus?.();
  }

  function showToast(message) {
    dom.toast.textContent = message;
    dom.toast.classList.add("is-visible");
    window.clearTimeout(state.toastTimer);
    state.toastTimer = window.setTimeout(() => dom.toast.classList.remove("is-visible"), 2200);
  }

  function openSearch() {
    closeCart({ restoreFocus: false });
    if (!dom.searchDialog.open) dom.searchDialog.showModal();
    document.body.classList.add("is-locked");
    filterSearch("");
    window.setTimeout(() => dom.searchInput.focus(), 80);
  }

  function closeSearch() {
    if (dom.searchDialog.open) dom.searchDialog.close();
    if (!dom.checkoutDialog.open) document.body.classList.remove("is-locked");
  }

  function filterSearch(query) {
    const terms = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    dom.searchResults.forEach((result, index) => {
      const haystack = `${result.dataset.keywords} ${products[index].name} ${products[index].tagline}`.toLowerCase();
      const matches = terms.length === 0 || terms.every((term) => haystack.includes(term));
      result.hidden = !matches;
      if (matches) visible += 1;
    });
    dom.noResults.hidden = visible > 0;
  }

  function selectSearchResult(index) {
    goTo(index, { scrollTop: true });
    closeSearch();
  }

  function openCheckout() {
    if (cartCount() === 0) return;
    closeCart({ restoreFocus: false });
    dom.checkoutFormView.hidden = false;
    dom.checkoutSuccess.hidden = true;
    dom.checkoutError.textContent = "";
    if (!dom.checkoutDialog.open) dom.checkoutDialog.showModal();
    document.body.classList.add("is-locked");
  }

  function setCatalogFilter(category) {
    dom.catalogFilters.forEach((button) => {
      const active = button.dataset.catalogFilter === category;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    dom.catalogCards.forEach((card) => {
      card.hidden = category !== "all" && card.dataset.category !== category;
    });
  }

  function closeCheckout() {
    if (dom.checkoutDialog.open) dom.checkoutDialog.close();
    document.body.classList.remove("is-locked");
  }

  async function submitCheckout(event) {
    event.preventDefault();
    const submitButton = dom.checkoutForm.querySelector('button[type="submit"]');
    const formData = new FormData(dom.checkoutForm);
    dom.checkoutError.textContent = "";
    submitButton.disabled = true;
    submitButton.firstChild.textContent = "Confirmando… ";

    try {
      const response = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer: { name: formData.get("name"), email: formData.get("email") },
          cart: state.cart,
        }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || "No pudimos confirmar este pedido.");

      dom.orderId.textContent = payload.order_id;
      dom.orderTotal.textContent = `$${payload.total}`;
      dom.checkoutFormView.hidden = true;
      dom.checkoutSuccess.hidden = false;
      state.cart = [];
      saveCart();
      renderCart();
    } catch (error) {
      dom.checkoutError.textContent = error.message;
    } finally {
      submitButton.disabled = false;
      submitButton.firstChild.textContent = "Confirmar pedido demo ";
    }
  }

  function toggleNavigation(force) {
    const open = typeof force === "boolean" ? force : !dom.nav.classList.contains("is-open");
    dom.nav.classList.toggle("is-open", open);
    dom.navToggle.setAttribute("aria-expanded", String(open));
    document.body.classList.toggle("is-locked", open);
  }

  function updateHeader() {
    const y = window.scrollY;
    dom.header.classList.toggle("is-scrolled", y > 20);
    const catalog = document.querySelector("#catalog");
    const story = document.querySelector("#story");
    const ritual = document.querySelector("#ritual");
    const prepared = document.querySelector("#prepared");
    const mobile = document.querySelector(".mobile-showcase");
    const headerLine = y + 45;
    const overCatalog = headerLine >= catalog.offsetTop && headerLine < story.offsetTop;
    const overPrepared = headerLine >= prepared.offsetTop && headerLine < mobile.offsetTop;
    dom.header.classList.toggle("force-dark", overPrepared);
    dom.header.classList.toggle("force-light", overCatalog || (headerLine >= ritual.offsetTop && headerLine < prepared.offsetTop));
  }

  dom.carousel.addEventListener("pointerdown", onPointerDown);
  window.addEventListener("pointermove", onPointerMove, { passive: true });
  window.addEventListener("pointerup", onPointerUp);
  window.addEventListener("pointercancel", onPointerUp);
  document.documentElement.addEventListener("pointerleave", () => {
    state.lookTargetX = 0;
    state.lookTargetY = 0;
  });
  window.addEventListener("blur", () => {
    state.lookTargetX = 0;
    state.lookTargetY = 0;
  });
  dom.carousel.addEventListener("wheel", (event) => {
    if (Math.abs(event.deltaX) <= Math.abs(event.deltaY)) return;
    event.preventDefault();
    state.target += event.deltaX / 450;
    state.target = Math.round(state.target);
    goTo(modulo(state.target, products.length));
  }, { passive: false });

  document.querySelector("[data-previous]").addEventListener("click", () => step(-1));
  document.querySelector("[data-next]").addEventListener("click", () => step(1));
  dom.tabs.forEach((tab, index) => tab.addEventListener("click", () => goTo(index)));
  dom.cards.forEach((card, index) => card.addEventListener("click", () => {
    if (state.moved < 7) goTo(index);
  }));
  dom.lines.forEach((line, index) => line.addEventListener("click", () => goTo(index, { scrollTop: true })));
  document.querySelectorAll("[data-shop-select]").forEach((button) => {
    button.addEventListener("click", () => goTo(Number(button.dataset.shopSelect), { scrollTop: true }));
  });

  document.querySelector("[data-quantity-minus]").addEventListener("click", () => {
    state.quantity = clamp(state.quantity - 1, 1, 9);
    dom.quantity.textContent = String(state.quantity);
  });
  document.querySelector("[data-quantity-plus]").addEventListener("click", () => {
    state.quantity = clamp(state.quantity + 1, 1, 9);
    dom.quantity.textContent = String(state.quantity);
  });
  document.querySelector("[data-add-selected]").addEventListener("click", () => addToCart(products[state.selected].id, state.quantity));
  document.querySelector("[data-phone-add]").addEventListener("click", () => addToCart(products[state.selected].id));
  document.querySelectorAll("[data-quick-add]").forEach((button) => button.addEventListener("click", () => addToCart(button.dataset.quickAdd)));

  document.querySelectorAll("[data-open-cart]").forEach((button) => button.addEventListener("click", openCart));
  document.querySelector("[data-close-cart]").addEventListener("click", () => closeCart());
  dom.cartScrim.addEventListener("click", () => closeCart());
  document.querySelector("[data-cart-shop]").addEventListener("click", () => {
    closeCart({ restoreFocus: false });
    document.querySelector("#catalog").scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth" });
  });
  dom.cartItems.addEventListener("click", (event) => {
    const minus = event.target.closest("[data-cart-minus]");
    const plus = event.target.closest("[data-cart-plus]");
    const remove = event.target.closest("[data-cart-remove]");
    if (minus) changeCartQuantity(minus.dataset.cartMinus, -1);
    if (plus) changeCartQuantity(plus.dataset.cartPlus, 1);
    if (remove) removeCartItem(remove.dataset.cartRemove);
  });

  document.querySelectorAll("[data-open-search]").forEach((button) => button.addEventListener("click", openSearch));
  document.querySelector("[data-close-search]").addEventListener("click", closeSearch);
  dom.searchDialog.addEventListener("click", (event) => {
    if (event.target === dom.searchDialog) closeSearch();
  });
  dom.searchDialog.addEventListener("close", () => {
    if (!dom.checkoutDialog.open && !dom.cartDrawer.classList.contains("is-open")) document.body.classList.remove("is-locked");
  });
  dom.searchInput.addEventListener("input", () => filterSearch(dom.searchInput.value));
  dom.searchInput.addEventListener("keydown", (event) => {
    if (event.key !== "Enter") return;
    const firstVisible = dom.searchResults.find((result) => !result.hidden);
    if (firstVisible) selectSearchResult(Number(firstVisible.dataset.searchResult));
  });
  document.querySelectorAll("[data-suggestion]").forEach((button) => button.addEventListener("click", () => {
    dom.searchInput.value = button.dataset.suggestion;
    filterSearch(button.dataset.suggestion);
    dom.searchInput.focus();
  }));
  dom.searchResults.forEach((result) => result.addEventListener("click", () => selectSearchResult(Number(result.dataset.searchResult))));

  dom.catalogFilters.forEach((button) => {
    button.addEventListener("click", () => setCatalogFilter(button.dataset.catalogFilter));
  });
  dom.catalogAdds.forEach((button) => {
    button.addEventListener("click", () => addToCart(button.dataset.catalogAdd));
  });

  dom.checkoutButton.addEventListener("click", openCheckout);
  document.querySelector("[data-close-checkout]").addEventListener("click", closeCheckout);
  document.querySelector("[data-finish-checkout]").addEventListener("click", closeCheckout);
  dom.checkoutDialog.addEventListener("click", (event) => {
    if (event.target === dom.checkoutDialog) closeCheckout();
  });
  dom.checkoutDialog.addEventListener("close", () => document.body.classList.remove("is-locked"));
  dom.checkoutForm.addEventListener("submit", submitCheckout);

  dom.navToggle.addEventListener("click", () => toggleNavigation());
  dom.nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => toggleNavigation(false)));

  window.addEventListener("keydown", (event) => {
    const dialogOpen = dom.searchDialog.open || dom.checkoutDialog.open;
    if (event.key === "Escape" && dom.cartDrawer.classList.contains("is-open")) closeCart();
    if (dialogOpen || ["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName)) return;
    if (event.key === "ArrowRight") step(1);
    if (event.key === "ArrowLeft") step(-1);
  });

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-visible");
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach((element) => revealObserver.observe(element));

  window.addEventListener("scroll", updateHeader, { passive: true });
  window.addEventListener("resize", updateHeader);

  setTheme(0);
  setCatalogFilter("all");
  renderCart();
  updateHeader();
  requestAnimationFrame(drawCarousel);
})();
