(() => {
  "use strict";

  const productData = document.querySelector("#product-data");
  if (!productData) return;

  const i18n = window.BuldakI18n;
  if (!i18n?.locales) return;
  const payload = JSON.parse(productData.textContent);
  const featuredProducts = payload.featured;
  const catalogProducts = payload.catalog;
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const root = document.documentElement;
  const catalogThemes = Object.freeze({
    "811140": { bgA: "#f5d9e1", bgB: "#fff8f4", glow: "#ffc1d2", ink: "#2b171e", accent: "#b3123f" },
    "811130": { bgA: "#e9f3f5", bgB: "#fff7f8", glow: "#f6cadb", ink: "#251b20", accent: "#cf527b" },
    "811200": { bgA: "#f6cf42", bgB: "#fff3b8", glow: "#ffe36a", ink: "#2c2110", accent: "#ce4b17" },
    "811150": { bgA: "#ee8a24", bgB: "#ffd27b", glow: "#ffb53c", ink: "#2b170e", accent: "#a51c19" },
    "811270": { bgA: "#f2b6c4", bgB: "#ffe9ed", glow: "#ff92ae", ink: "#351921", accent: "#b72453" },
    "811320": { bgA: "#d9c0ef", bgB: "#f7eafb", glow: "#d997e7", ink: "#2d1b35", accent: "#9e2878" },
    "811000": { bgA: "#e95a17", bgB: "#ffb248", glow: "#ff7d26", ink: "#2a130b", accent: "#8e1a13" },
    "811340": { bgA: "#4b2418", bgB: "#9b4f2d", glow: "#d05a2f", ink: "#fff4ed", accent: "#ff7a35" },
    "811220": { bgA: "#4f8a2f", bgB: "#dbe75a", glow: "#b7df44", ink: "#14240f", accent: "#df481a" },
    "811120": { bgA: "#1e1413", bgB: "#5c271d", glow: "#d94620", ink: "#fff4ef", accent: "#ff572e" },
    "811210": { bgA: "#220f10", bgB: "#8d121c", glow: "#f02b2b", ink: "#fff4f0", accent: "#ff493d" },
    "811616": { bgA: "#d9c0ef", bgB: "#f7eafb", glow: "#d997e7", ink: "#2d1b35", accent: "#9e2878" },
    "811618": { bgA: "#ee8a24", bgB: "#ffd27b", glow: "#ffb53c", ink: "#2b170e", accent: "#a51c19" },
    "811622": { bgA: "#f5d9e1", bgB: "#fff8f4", glow: "#ffc1d2", ink: "#2b171e", accent: "#b3123f" },
    "811624": { bgA: "#1e1413", bgB: "#5c271d", glow: "#d94620", ink: "#fff4ef", accent: "#ff572e" },
    "811640": { bgA: "#f2b6c4", bgB: "#ffe9ed", glow: "#ff92ae", ink: "#351921", accent: "#b72453" },
    "811650": { bgA: "#e7c9e9", bgB: "#fceff5", glow: "#eca9d5", ink: "#311b30", accent: "#a83172" },
    "811612": { bgA: "#1e1413", bgB: "#5c271d", glow: "#d94620", ink: "#fff4ef", accent: "#ff572e" },
    "811710": { bgA: "#f5d9e1", bgB: "#fff8f4", glow: "#ffc1d2", ink: "#2b171e", accent: "#b3123f" },
    "811720": { bgA: "#1e1413", bgB: "#5c271d", glow: "#d94620", ink: "#fff4ef", accent: "#ff572e" },
    "811910": { bgA: "#6e8f31", bgB: "#d3dc59", glow: "#b8d347", ink: "#17220e", accent: "#df481a" },
    "811920": { bgA: "#b51f25", bgB: "#ff7950", glow: "#ed3c2e", ink: "#fff8f2", accent: "#ffd15c" }
  });
  const featuredById = new Map(featuredProducts.map((product) => [String(product.id), product]));
  const products = catalogProducts.map((catalogProduct, index) => ({
    number: String(index + 1).padStart(2, "0"),
    description: "",
    heat: 0,
    heat_label: "—",
    ...catalogProduct,
    ...(featuredById.get(String(catalogProduct.id)) || {}),
    id: String(catalogProduct.id),
    sku: String(catalogProduct.sku)
  }));
  const productById = new Map(products.map((product) => [product.id, product]));

  const dom = {
    header: document.querySelector("[data-header]"),
    carousel: document.querySelector("[data-carousel]"),
    cards: [...document.querySelectorAll("[data-card]")],
    tabs: [...document.querySelectorAll("[data-select]")],
    lines: [...document.querySelectorAll("[data-flavor-line]")],
    productType: document.querySelector("[data-product-type]"),
    number: document.querySelector("[data-number]"),
    sku: document.querySelector("[data-sku]"),
    name: document.querySelector("[data-name]"),
    description: document.querySelector("[data-description]"),
    price: document.querySelector("[data-price]"),
    weight: document.querySelector("[data-weight]"),
    heatFill: document.querySelector("[data-heat-fill]"),
    heatLabel: document.querySelector("[data-heat-label]"),
    quantity: document.querySelector("[data-quantity]"),
    addSelected: document.querySelector("[data-add-selected]"),
    storyTitle: document.querySelector("[data-story-title]"),
    storySection: document.querySelector("[data-story-section]"),
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
    pairingTitles: [...document.querySelectorAll("[data-pairing-title]")],
    pairingTexts: [...document.querySelectorAll("[data-pairing-text]")],
    language: document.querySelector("[data-language]"),
    cartTrigger: document.querySelector("[data-cart-trigger]"),
    cartCount: document.querySelector("[data-cart-count]"),
    cartTitleCount: document.querySelector("[data-cart-title-count]"),
    cartDrawer: document.querySelector("[data-cart-drawer]"),
    cartScrim: document.querySelector("[data-cart-scrim]"),
    cartItems: document.querySelector("[data-cart-items]"),
    clearCart: document.querySelector("[data-clear-cart]"),
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
    checkoutSubmitLabel: document.querySelector("[data-checkout-submit-label]"),
    checkoutSuccessCopy: document.querySelector("[data-checkout-success-copy]"),
    legalDialog: document.querySelector("[data-legal-dialog]"),
    toast: document.querySelector("[data-toast]"),
    nav: document.querySelector("[data-nav]"),
    navToggle: document.querySelector("[data-nav-toggle]"),
    catalogFilters: [...document.querySelectorAll("[data-catalog-filter]")],
    catalogCards: [...document.querySelectorAll("[data-catalog-card]")],
    catalogAdds: [...document.querySelectorAll("[data-catalog-add]")],
    catalogSteppers: [...document.querySelectorAll("[data-catalog-stepper]")],
    catalogQuantityOutputs: [...document.querySelectorAll("[data-catalog-quantity]")],
    catalogQuantityMinuses: [...document.querySelectorAll("[data-catalog-qty-minus]")],
    catalogQuantityPluses: [...document.querySelectorAll("[data-catalog-qty-plus]")],
    catalogDetailButtons: [...document.querySelectorAll("[data-catalog-detail]")],
    catalogDetailLabels: [...document.querySelectorAll("[data-catalog-detail-label]")],
    catalogCategories: [...document.querySelectorAll("[data-catalog-category]")],
    catalogNames: [...document.querySelectorAll("[data-catalog-name]")],
    catalogImages: [...document.querySelectorAll("[data-catalog-image]")],
    catalogStatuses: [...document.querySelectorAll("[data-catalog-status]")],
    catalogMetas: [...document.querySelectorAll("[data-catalog-meta]")],
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
    language: loadLanguage(),
    cart: loadCart(),
    catalogQuantities: new Map(catalogProducts.map((product) => [String(product.id), 1])),
    detailProductId: String(products[0].id),
    toastTimer: null,
    cartAnimationTimer: null,
    lastCartFocus: null,
    lastOrder: null,
  };

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function modulo(value, size) {
    return ((value % size) + size) % size;
  }

  function loadLanguage() {
    try {
      const saved = localStorage.getItem("buldak-language");
      if (["es", "en", "zh"].includes(saved)) return saved;
    } catch {
      // Language preference remains available for this visit.
    }
    const browserLanguage = navigator.language?.toLowerCase() || "es";
    if (browserLanguage.startsWith("zh")) return "zh";
    if (browserLanguage.startsWith("en")) return "en";
    return "es";
  }

  function t(key, values = {}) {
    const table = i18n.locales[state.language] || i18n.locales.es;
    const fallback = i18n.locales.es[key] || key;
    return String(table[key] || fallback).replace(/\{(\w+)\}/g, (_, name) => values[name] ?? `{${name}}`);
  }

  function localizedProduct(product) {
    if (!product) return product;
    const translated = i18n.productContent?.[state.language]?.[product.id];
    const name = i18n.productNames?.[state.language]?.[product.id] || product.name;
    return { ...product, ...(translated || {}), name };
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function translateWeight(weight) {
    return state.language === "zh" ? String(weight).replace(/\s*g\b/gi, " 克") : weight;
  }

  function translateCase(caseSize) {
    if (state.language === "es") return caseSize;
    const value = String(caseSize);
    if (state.language === "en") {
      return value
        .replace(/paquetes/gi, "packs")
        .replace(/bolsas/gi, "bags")
        .replace(/SKU alterno/gi, "alternate SKU");
    }
    return value
      .replace(/paquetes/gi, "袋")
      .replace(/bolsas/gi, "袋")
      .replace(/bowls?/gi, "碗")
      .replace(/SKU alterno/gi, "备用 SKU");
  }

  function productDetail(product) {
    return i18n.productDetails?.[state.language]?.[product.id] || {};
  }

  function storyThemeFor(product) {
    return catalogThemes[product.id] || {
      bgA: product.colors?.bg_a || "#f5d9e1",
      bgB: product.colors?.bg_b || "#fff8f4",
      glow: product.colors?.glow || "#ffc1d2",
      ink: product.colors?.ink || "#2b171e",
      accent: product.colors?.accent || "#b3123f"
    };
  }

  function isDarkColor(hex) {
    const normalized = String(hex).replace("#", "");
    if (!/^[0-9a-f]{6}$/i.test(normalized)) return false;
    const [red, green, blue] = [0, 2, 4].map((offset) => Number.parseInt(normalized.slice(offset, offset + 2), 16));
    return (red * 299 + green * 587 + blue * 114) / 255000 < .48;
  }

  function setStoryStat(element, value) {
    const available = value !== undefined && value !== null && String(value).trim() !== "";
    element.textContent = available ? value : "—";
    element.closest("div")?.classList.toggle("is-unavailable", !available);
  }

  function updateCatalogDetailButtons() {
    dom.catalogDetailButtons.forEach((button) => {
      const active = button.dataset.catalogDetail === state.detailProductId;
      button.setAttribute("aria-pressed", String(active));
      button.closest("[data-catalog-card]")?.classList.toggle("is-detail-selected", active);
    });
    dom.catalogDetailLabels.forEach((label) => {
      const active = label.dataset.catalogDetailLabel === state.detailProductId;
      label.textContent = t(active ? "catalog.selected" : "catalog.details");
    });
  }

  function renderStoryById(id) {
    const baseProduct = productById.get(String(id));
    if (!baseProduct) return;
    const product = localizedProduct(baseProduct);
    const detail = productDetail(product);
    const nameEnding = state.language === "zh" ? "。" : ".";
    const title = Array.isArray(product.story_title)
      ? product.story_title
      : [`${product.name}${nameEnding}`, t("story.profile")];
    const theme = storyThemeFor(product);

    dom.storySection.dataset.detailId = String(product.id);
    dom.storySection.style.setProperty("--detail-bg-a", theme.bgA);
    dom.storySection.style.setProperty("--detail-bg-b", theme.bgB);
    dom.storySection.style.setProperty("--detail-glow", theme.glow);
    dom.storySection.style.setProperty("--detail-ink", theme.ink);
    dom.storySection.style.setProperty("--detail-accent", theme.accent);
    dom.storySection.classList.toggle("is-dark", isDarkColor(theme.bgA));
    dom.storySection.classList.remove("is-changing");
    requestAnimationFrame(() => dom.storySection.classList.add("is-changing"));

    dom.storyTitle.innerHTML = title.map(escapeHtml).join("<br>");
    dom.storyCopy.textContent = product.story || detail.description || product.description || "";
    dom.storyImage.src = product.image;
    dom.storyImage.alt = state.language === "zh"
      ? `Buldak ${product.name} 包装`
      : state.language === "en"
        ? `Buldak ${product.name} pack`
        : `Paquete Buldak ${product.name}`;
    setStoryStat(dom.shu, product.shu);
    setStoryStat(dom.kcal, product.kcal);
    setStoryStat(dom.cookTime, product.cook_time);
    setStoryStat(dom.storyWeight, translateWeight(product.weight).split(" · ")[0]);
    dom.storyNote.innerHTML = escapeHtml(product.story_note || detail.note || product.name).replace("\n", "<br>");
    dom.nutritionSource.href = product.nutrition_source_url || product.source_url || "#";
    state.detailProductId = String(product.id);
    document.title = `${t("meta.title").split("—")[0].trim()} — ${product.name}`;
    updateCatalogDetailButtons();
    updateHeader();
  }

  function showProductDetail(id) {
    renderStoryById(id);
    dom.storySection.scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
    window.setTimeout(() => dom.storyTitle.focus({ preventScroll: true }), reducedMotion ? 0 : 650);
  }

  function changeCatalogQuantity(id, delta) {
    id = String(id);
    const next = clamp((state.catalogQuantities.get(id) || 1) + delta, 1, 20);
    state.catalogQuantities.set(id, next);
    const output = dom.catalogQuantityOutputs.find((element) => element.dataset.catalogQuantity === id);
    if (output) output.textContent = String(next);
  }

  function applyLanguage(language, { persist = true } = {}) {
    state.language = ["es", "en", "zh"].includes(language) ? language : "es";
    root.lang = state.language === "zh" ? "zh-CN" : state.language;
    dom.language.value = state.language;
    if (persist) {
      try {
        localStorage.setItem("buldak-language", state.language);
      } catch {
        // A blocked storage API should not prevent translation.
      }
    }

    document.querySelectorAll("[data-i18n]").forEach((element) => {
      element.textContent = t(element.dataset.i18n, { count: catalogProducts.length });
    });
    document.querySelectorAll("[data-i18n-html]").forEach((element) => {
      element.innerHTML = t(element.dataset.i18nHtml, { count: catalogProducts.length });
    });
    document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
      element.setAttribute("aria-label", t(element.dataset.i18nAria));
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
      element.setAttribute("placeholder", t(element.dataset.i18nPlaceholder));
    });
    document.querySelector('[data-i18n-meta="meta.description"]')?.setAttribute("content", t("meta.description"));

    dom.catalogCategories.forEach((element) => {
      element.textContent = t(`category.${element.dataset.catalogCategory}`);
    });
    dom.catalogNames.forEach((element) => {
      const product = localizedProduct(productById.get(element.dataset.catalogName));
      element.textContent = product.name;
    });
    dom.catalogImages.forEach((element) => {
      const product = localizedProduct(productById.get(element.dataset.catalogImage));
      element.alt = state.language === "zh"
        ? `Buldak ${product.name}，SKU ${product.sku}`
        : `Buldak ${product.name}, SKU ${product.sku}`;
    });
    dom.catalogMetas.forEach((element) => {
      const product = productById.get(element.dataset.catalogMeta);
      element.textContent = `${translateWeight(product.weight)} · ${translateCase(product.case)}`;
    });
    dom.catalogStatuses.forEach((element) => {
      const product = productById.get(element.dataset.catalogStatus);
      element.textContent = t(product.is_available === false ? "catalog.soldOut" : "catalog.available");
    });
    dom.catalogAdds.forEach((button) => {
      const product = productById.get(button.dataset.catalogAdd);
      button.textContent = t(product.is_available === false ? "catalog.soldOut" : "catalog.add");
    });
    dom.catalogSteppers.forEach((stepper) => {
      const product = localizedProduct(productById.get(stepper.dataset.catalogStepper));
      stepper.setAttribute("aria-label", t("catalog.quantity", { name: product.name }));
    });
    dom.catalogQuantityMinuses.forEach((button) => {
      const product = localizedProduct(productById.get(button.dataset.catalogQtyMinus));
      button.setAttribute("aria-label", t("catalog.reduce", { name: product.name }));
    });
    dom.catalogQuantityPluses.forEach((button) => {
      const product = localizedProduct(productById.get(button.dataset.catalogQtyPlus));
      button.setAttribute("aria-label", t("catalog.increase", { name: product.name }));
    });
    dom.searchResults.forEach((result, index) => {
      const product = localizedProduct(products[index]);
      const name = result.querySelector("strong");
      const detail = result.querySelector("small");
      if (name) name.textContent = product.name;
      if (detail) {
        detail.textContent = product.heat_label && product.heat_label !== "—"
          ? `${product.heat_label} · ${product.price_label}`
          : `${t(`category.${product.category}`)} · ${product.price_label}`;
      }
    });
    dom.cards.forEach((card, index) => {
      const product = localizedProduct(products[index]);
      card.setAttribute("aria-label", t("hero.selectFlavor", { name: product.name }));
      const image = card.querySelector("img");
      if (image) image.alt = state.language === "zh"
        ? `Buldak ${product.name} 包装`
        : state.language === "en"
          ? `Buldak ${product.name} pack`
          : `Paquete Buldak ${product.name}`;
    });
    dom.tabs.forEach((tab, index) => {
      tab.textContent = localizedProduct(products[index]).name;
    });
    const suggestions = {
      es: [["carbonara", "carbonara"], ["picante", "picante"], ["queso", "queso"]],
      en: [["carbonara", "carbonara"], ["spicy", "spicy"], ["cheese", "cheese"]],
      zh: [["carbonara", "carbonara"], ["辣", "辣"], ["芝士", "芝士"]]
    }[state.language];
    document.querySelectorAll("[data-suggestion]").forEach((button, index) => {
      button.dataset.suggestion = suggestions[index][0];
      button.textContent = suggestions[index][1];
    });

    setTheme(state.selected, { syncDetail: false });
    renderStoryById(state.detailProductId);
    renderCart({ animate: false });
    filterSearch(dom.searchInput.value);
    if (state.lastOrder) {
      dom.checkoutSuccessCopy.textContent = t("checkout.successCopy", {
        id: state.lastOrder.id,
        total: state.lastOrder.total
      });
    }
  }

  function carouselDistance(value) {
    return modulo(value + products.length / 2, products.length) - products.length / 2;
  }

  function cycleTo(index) {
    const rounded = Math.round(state.target);
    const current = modulo(rounded, products.length);
    return rounded + carouselDistance(index - current);
  }

  function setTheme(index, { syncDetail = true } = {}) {
    const baseProduct = products[index];
    const product = localizedProduct(baseProduct);
    const detail = productDetail(product);
    const theme = storyThemeFor(product);
    state.selected = index;
    root.style.setProperty("--bg-a", theme.bgA);
    root.style.setProperty("--bg-b", theme.bgB);
    root.style.setProperty("--glow", theme.glow);
    root.style.setProperty("--ink", theme.ink);
    root.style.setProperty("--accent", theme.accent);

    const themeMeta = document.querySelector('meta[name="theme-color"]');
    if (themeMeta) themeMeta.setAttribute("content", theme.bgA);

    dom.productType.textContent = product.category === "bags" ? t("hero.type") : t(`category.${product.category}`);
    dom.number.textContent = product.number;
    dom.sku.textContent = product.sku;
    dom.name.textContent = product.name;
    dom.description.textContent = product.description || detail.description || "";
    dom.price.textContent = product.price_label;
    dom.weight.textContent = translateWeight(product.weight);
    dom.heatFill.style.width = `${product.heat || 0}%`;
    dom.heatLabel.textContent = product.heat_label || "—";
    dom.addSelected.disabled = product.is_available === false;
    const addLabel = dom.addSelected.querySelector("[data-i18n]");
    if (addLabel) addLabel.textContent = t(product.is_available === false ? "catalog.soldOut" : "hero.add");

    if (Array.isArray(product.directions) && product.directions.length === dom.directionTitles.length) {
      dom.directionsTitle.innerHTML = product.directions_title.join("<br>");
      dom.directionsIntro.textContent = product.directions_intro;
      dom.directionTitles.forEach((element, directionIndex) => {
        element.textContent = product.directions[directionIndex].title;
      });
      dom.directionTexts.forEach((element, directionIndex) => {
        element.textContent = product.directions[directionIndex].text;
      });
    }

    if (product.prepared_image && Array.isArray(product.recommendations)) {
      dom.preparedName.textContent = product.name;
      dom.preparedImage.src = product.prepared_image;
      dom.preparedImage.alt = product.prepared_alt;
      dom.pairingTitles.forEach((element, pairingIndex) => {
        element.textContent = product.recommendations[pairingIndex].title;
      });
      dom.pairingTexts.forEach((element, pairingIndex) => {
        element.textContent = product.recommendations[pairingIndex].text;
      });
    }
    document.title = `${t("meta.title").split("—")[0].trim()} — ${product.name}`;

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
    const activeTab = dom.tabs[index];
    if (activeTab) {
      const tabRail = activeTab.parentElement;
      const left = activeTab.offsetLeft - (tabRail.clientWidth - activeTab.offsetWidth) / 2;
      tabRail.scrollTo({ left, behavior: reducedMotion ? "auto" : "smooth" });
    }
    dom.lines.forEach((line, lineIndex) => line.classList.toggle("is-active", lineIndex === index));
    if (syncDetail) renderStoryById(baseProduct.id);
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
      const absoluteDistance = Math.abs(distance);
      const theta = clamp(distance, -4, 4) * 0.52;
      const x = Math.sin(theta) * radius;
      const z = (Math.cos(theta) - 1) * depth;
      const proximity = clamp(1 + z / (depth * 2.8), 0, 1);
      const visibility = clamp(1 - Math.max(0, absoluteDistance - 2) * 0.42, 0, 1);
      const scale = 0.68 + proximity * 0.32;
      const lookStrength = Math.pow(proximity, 8);
      const rotationY = distance * -24 + state.lookX * 14 * lookStrength;
      const rotationX = state.lookY * -8.5 * lookStrength;
      const float = reducedMotion ? 0 : Math.sin(performance.now() / 2100 + index * 2.1) * 5 * proximity;
      card.style.transform = `translate3d(${x.toFixed(1)}px, ${float.toFixed(1)}px, ${z.toFixed(1)}px) rotateY(${rotationY.toFixed(1)}deg) rotateX(${rotationX.toFixed(1)}deg) scale(${scale.toFixed(3)})`;
      card.style.opacity = String((0.22 + proximity * 0.78) * visibility);
      card.style.filter = proximity > 0.985 ? "none" : `blur(${((1 - proximity) * 5).toFixed(2)}px)`;
      card.style.zIndex = String(1000 + Math.round(z));
      card.style.pointerEvents = absoluteDistance <= 2.2 ? "auto" : "none";
      card.tabIndex = absoluteDistance < 0.55 ? 0 : -1;
      card.setAttribute("aria-hidden", String(absoluteDistance > 3.25));
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
        .filter((item) => productById.has(item.id) && productById.get(item.id).is_available !== false && Number.isInteger(item.quantity) && item.quantity > 0 && item.quantity <= 20);
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

  function celebrateCart() {
    dom.cartTrigger.classList.remove("is-celebrating");
    requestAnimationFrame(() => dom.cartTrigger.classList.add("is-celebrating"));
    window.clearTimeout(state.cartAnimationTimer);
    state.cartAnimationTimer = window.setTimeout(() => dom.cartTrigger.classList.remove("is-celebrating"), 650);
  }

  function animateAddToCart(source, product) {
    celebrateCart();
    if (!source || reducedMotion) return;
    source.classList.remove("is-added");
    requestAnimationFrame(() => source.classList.add("is-added"));
    window.setTimeout(() => source.classList.remove("is-added"), 650);

    const sourceRect = source.getBoundingClientRect();
    const targetRect = dom.cartTrigger.getBoundingClientRect();
    const flyer = document.createElement("img");
    flyer.className = "cart-flyer";
    flyer.src = product.image;
    flyer.alt = "";
    flyer.style.left = `${sourceRect.left + sourceRect.width / 2 - 31}px`;
    flyer.style.top = `${sourceRect.top + sourceRect.height / 2 - 31}px`;
    document.body.append(flyer);

    const deltaX = targetRect.left + targetRect.width / 2 - (sourceRect.left + sourceRect.width / 2);
    const deltaY = targetRect.top + targetRect.height / 2 - (sourceRect.top + sourceRect.height / 2);
    const animation = flyer.animate([
      { transform: "translate3d(0, 0, 0) scale(.72) rotate(-5deg)", opacity: 0 },
      { transform: "translate3d(0, -22px, 0) scale(1) rotate(3deg)", opacity: 1, offset: .18 },
      { transform: `translate3d(${deltaX}px, ${deltaY}px, 0) scale(.18) rotate(14deg)`, opacity: .2 }
    ], { duration: 720, easing: "cubic-bezier(.2,.75,.2,1)", fill: "forwards" });
    animation.finished.finally(() => flyer.remove());
  }

  function addToCart(id, quantity = 1, source = null) {
    id = String(id);
    const product = productById.get(id);
    if (!product || product.is_available === false) return;
    const amount = clamp(Number(quantity) || 1, 1, 20);
    const existing = state.cart.find((item) => item.id === id);
    if (existing?.quantity === 20) {
      showToast(t("cart.limit"));
      celebrateCart();
      return;
    }
    if (existing) existing.quantity = Math.min(20, existing.quantity + amount);
    else state.cart.push({ id, quantity: amount });
    saveCart();
    renderCart({ highlightId: id });
    animateAddToCart(source, product);
    showToast(t("cart.added", { name: localizedProduct(product).name }));
  }

  function changeCartQuantity(id, amount, source = null) {
    const item = state.cart.find((entry) => entry.id === id);
    if (!item) return;
    if (amount > 0 && item.quantity === 20) {
      showToast(t("cart.limit"));
      celebrateCart();
      return;
    }
    item.quantity = clamp(item.quantity + amount, 0, 20);
    if (item.quantity === 0) state.cart = state.cart.filter((entry) => entry.id !== id);
    saveCart();
    renderCart({ highlightId: id });
    if (amount > 0) {
      celebrateCart();
      source?.closest(".cart-item")?.classList.add("is-updated");
    }
  }

  function removeCartItem(id) {
    state.cart = state.cart.filter((item) => item.id !== id);
    saveCart();
    renderCart();
  }

  function clearCart() {
    if (state.cart.length === 0) return;
    state.cart = [];
    saveCart();
    renderCart();
    showToast(t("cart.cleared"));
  }

  function renderCart({ animate = true, highlightId = null } = {}) {
    const count = cartCount();
    dom.cartCount.textContent = String(count);
    dom.cartTitleCount.textContent = String(count);
    const subtotal = state.cart.reduce((total, item) => {
      const product = productById.get(item.id);
      return total + Number(product.price) * item.quantity;
    }, 0);
    dom.subtotal.textContent = `$${subtotal.toFixed(2)}`;
    dom.checkoutButton.disabled = count === 0;
    dom.clearCart.hidden = count === 0;
    dom.cartEmpty.classList.toggle("is-visible", count === 0);
    dom.cartItems.hidden = count === 0;
    dom.shippingMessage.textContent = count === 0
      ? t("cart.shippingEmpty")
      : t(count === 1 ? "cart.shippingOne" : "cart.shippingMany", { count });

    dom.cartItems.innerHTML = state.cart.map((item) => {
      const product = localizedProduct(productById.get(item.id));
      const safeId = escapeHtml(product.id);
      const safeName = escapeHtml(product.name);
      return `
        <article class="cart-item${highlightId === product.id ? " is-updated" : ""}" data-cart-item="${safeId}">
          <div class="cart-item__image"><img src="${escapeHtml(product.image)}" alt=""></div>
          <div class="cart-item__details">
            <div class="cart-item__top"><h3>${safeName}</h3><strong>$${(Number(product.price) * item.quantity).toFixed(2)}</strong></div>
            <p>${escapeHtml(translateWeight(product.weight))} · ${escapeHtml(product.price_label)} ${escapeHtml(t("cart.each"))}</p>
            <div class="cart-item__actions">
              <div class="mini-stepper" aria-label="${escapeHtml(t("cart.quantity", { name: product.name }))}">
                <button type="button" data-cart-minus="${safeId}" aria-label="${escapeHtml(t("cart.reduce", { name: product.name }))}">−</button>
                <span>${item.quantity}</span>
                <button type="button" data-cart-plus="${safeId}" aria-label="${escapeHtml(t("cart.increase", { name: product.name }))}">+</button>
              </div>
              <button class="remove-item" type="button" data-cart-remove="${safeId}">${escapeHtml(t("cart.remove"))}</button>
            </div>
          </div>
        </article>`;
    }).join("");

    if (animate) {
      dom.cartCount.classList.remove("is-bumping");
      requestAnimationFrame(() => dom.cartCount.classList.add("is-bumping"));
      window.setTimeout(() => dom.cartCount.classList.remove("is-bumping"), 420);
    }
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
    if (!dom.searchDialog.open && !dom.checkoutDialog.open && !dom.legalDialog.open) document.body.classList.remove("is-locked");
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
    if (!dom.checkoutDialog.open && !dom.legalDialog.open) document.body.classList.remove("is-locked");
  }

  function filterSearch(query) {
    const terms = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    dom.searchResults.forEach((result, index) => {
      const product = localizedProduct(products[index]);
      const detail = productDetail(product);
      const haystack = [result.dataset.keywords, product.name, product.tagline, product.description, product.story, detail.description]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
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

  function openLegal() {
    closeCart({ restoreFocus: false });
    if (dom.searchDialog.open) dom.searchDialog.close();
    if (!dom.legalDialog.open) dom.legalDialog.showModal();
    document.body.classList.add("is-locked");
  }

  function closeLegal() {
    if (dom.legalDialog.open) dom.legalDialog.close();
    if (!dom.checkoutDialog.open && !dom.searchDialog.open) document.body.classList.remove("is-locked");
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
    if (!dom.legalDialog.open && !dom.searchDialog.open) document.body.classList.remove("is-locked");
  }

  async function submitCheckout(event) {
    event.preventDefault();
    const submitButton = dom.checkoutForm.querySelector('button[type="submit"]');
    const formData = new FormData(dom.checkoutForm);
    dom.checkoutError.textContent = "";
    submitButton.disabled = true;
    dom.checkoutSubmitLabel.textContent = t("checkout.submitting");

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
      if (!response.ok) throw new Error(payload.error || t("checkout.error"));

      state.lastOrder = { id: payload.order_id, total: `$${payload.total}` };
      dom.checkoutSuccessCopy.textContent = t("checkout.successCopy", {
        id: state.lastOrder.id,
        total: state.lastOrder.total
      });
      dom.checkoutFormView.hidden = true;
      dom.checkoutSuccess.hidden = false;
      state.cart = [];
      saveCart();
      renderCart();
    } catch (error) {
      dom.checkoutError.textContent = error.message;
    } finally {
      submitButton.disabled = false;
      dom.checkoutSubmitLabel.textContent = t("checkout.submit");
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
    const footer = document.querySelector(".site-footer");
    const headerLine = y + 45;
    const overCatalog = headerLine >= catalog.offsetTop && headerLine < story.offsetTop;
    const overStory = headerLine >= story.offsetTop && headerLine < ritual.offsetTop;
    const overPrepared = headerLine >= prepared.offsetTop && headerLine < footer.offsetTop;
    const overFooter = headerLine >= footer.offsetTop;
    dom.header.classList.toggle("force-dark", overPrepared || (overStory && !story.classList.contains("is-dark")));
    dom.header.classList.toggle("force-light", overCatalog || overFooter || (overStory && story.classList.contains("is-dark")) || (headerLine >= ritual.offsetTop && headerLine < prepared.offsetTop));
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
    state.quantity = clamp(state.quantity - 1, 1, 20);
    dom.quantity.textContent = String(state.quantity);
  });
  document.querySelector("[data-quantity-plus]").addEventListener("click", () => {
    state.quantity = clamp(state.quantity + 1, 1, 20);
    dom.quantity.textContent = String(state.quantity);
  });
  document.querySelector("[data-add-selected]").addEventListener("click", (event) => addToCart(products[state.selected].id, state.quantity, event.currentTarget));
  document.querySelectorAll("[data-quick-add]").forEach((button) => button.addEventListener("click", (event) => addToCart(button.dataset.quickAdd, 1, event.currentTarget)));

  document.querySelectorAll("[data-open-cart]").forEach((button) => button.addEventListener("click", openCart));
  document.querySelector("[data-close-cart]").addEventListener("click", () => closeCart());
  dom.clearCart.addEventListener("click", clearCart);
  dom.cartScrim.addEventListener("click", () => closeCart());
  document.querySelector("[data-cart-shop]").addEventListener("click", () => {
    closeCart({ restoreFocus: false });
    document.querySelector("#catalog").scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth" });
  });
  dom.cartItems.addEventListener("click", (event) => {
    const minus = event.target.closest("[data-cart-minus]");
    const plus = event.target.closest("[data-cart-plus]");
    const remove = event.target.closest("[data-cart-remove]");
    if (minus) changeCartQuantity(minus.dataset.cartMinus, -1, minus);
    if (plus) changeCartQuantity(plus.dataset.cartPlus, 1, plus);
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
    button.addEventListener("click", (event) => {
      const id = button.dataset.catalogAdd;
      addToCart(id, state.catalogQuantities.get(id) || 1, event.currentTarget);
    });
  });
  dom.catalogQuantityMinuses.forEach((button) => {
    button.addEventListener("click", () => changeCatalogQuantity(button.dataset.catalogQtyMinus, -1));
  });
  dom.catalogQuantityPluses.forEach((button) => {
    button.addEventListener("click", () => changeCatalogQuantity(button.dataset.catalogQtyPlus, 1));
  });
  dom.catalogDetailButtons.forEach((button) => {
    button.addEventListener("click", () => showProductDetail(button.dataset.catalogDetail));
  });

  dom.language.addEventListener("change", () => applyLanguage(dom.language.value));

  document.querySelectorAll("[data-open-legal]").forEach((button) => button.addEventListener("click", openLegal));
  document.querySelector("[data-close-legal]").addEventListener("click", closeLegal);
  dom.legalDialog.addEventListener("click", (event) => {
    if (event.target === dom.legalDialog) closeLegal();
  });
  dom.legalDialog.addEventListener("close", () => {
    if (!dom.checkoutDialog.open && !dom.searchDialog.open) document.body.classList.remove("is-locked");
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
    const dialogOpen = dom.searchDialog.open || dom.checkoutDialog.open || dom.legalDialog.open;
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

  applyLanguage(state.language, { persist: false });
  setCatalogFilter("all");
  updateHeader();
  requestAnimationFrame(drawCarousel);
})();
