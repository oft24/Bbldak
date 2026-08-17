(() => {
  "use strict";

  const locales = {
    es: {
      "meta.title": "BuldakShop — Elige tu sabor",
      "meta.description": "BuldakShop: sabor, preparación y recomendaciones para cada Buldak.",
      "skip": "Saltar al contenido",
      "nav.catalog": "Catálogo",
      "nav.buy": "Comprar",
      "nav.info": "Información",
      "nav.preparation": "Preparación",
      "header.changeFlavor": "Cambiar sabor",
      "header.cart": "Carrito",
      "header.openCart": "Abrir carrito",
      "header.language": "Idioma",
      "hero.type": "Ramen salteado",
      "hero.heat": "Picor",
      "hero.presentation": "Presentación",
      "hero.individualPack": "Paquete individual",
      "hero.quantity": "Cantidad",
      "hero.reduceQuantity": "Reducir cantidad",
      "hero.increaseQuantity": "Aumentar cantidad",
      "hero.add": "Agregar al carrito",
      "hero.provisional": "Precio provisional por artículo",
      "hero.viewCatalog": "Ver catálogo completo",
      "hero.carousel": "Selector de sabores Buldak",
      "hero.selectFlavor": "Seleccionar {name}",
      "hero.drag": "Arrastra para girar",
      "hero.chooseFlavor": "Elegir un sabor",
      "hero.previous": "Sabor anterior",
      "hero.next": "Siguiente sabor",
      "hero.scroll": "Arrastra la bolsa · baja para conocerla",
      "catalog.index": "02 — Catálogo de julio",
      "catalog.title": "Todos los productos.<br><span>Listos para tu carrito.</span>",
      "catalog.copy": "{count} productos disponibles. Cada artículo usa el precio provisional de $0.01 hasta recibir la lista final.",
      "catalog.filter": "Filtrar catálogo",
      "filter.all": "Todos",
      "filter.bags": "Bolsas",
      "filter.bowls": "Bowls",
      "filter.tteokbokki": "Tteokbokki",
      "filter.snacks": "Snacks",
      "category.bags": "Bolsa",
      "category.bowls": "Bowl",
      "category.tteokbokki": "Tteokbokki",
      "category.snacks": "Snack",
      "catalog.available": "Disponible",
      "catalog.soldOut": "Agotado",
      "catalog.add": "Agregar",
      "catalog.quantity": "Cantidad de {name}",
      "catalog.reduce": "Reducir cantidad de {name}",
      "catalog.increase": "Aumentar cantidad de {name}",
      "catalog.details": "Ver descripción",
      "catalog.selected": "Descripción abierta",
      "story.index": "03 — La bolsa seleccionada",
      "story.profile": "Su perfil.",
      "story.cook": "Cocción",
      "story.portion": "Porción",
      "story.nutrition": "Valores por paquete. La información puede cambiar por mercado; confirma siempre la etiqueta de tu bolsa.",
      "story.source": "Fuente del producto",
      "ritual.index": "04 — Preparación exacta",
      "prepared.index": "05 — Servida y acompañada",
      "prepared.title": "Así queda",
      "prepared.pairings": "Va bien con",
      "footer.description": "Una tienda con la colección del catálogo y una ficha precisa para el sabor seleccionado.",
      "footer.explore": "Explorar",
      "footer.buy": "Comprar",
      "footer.products": "Todos los productos",
      "footer.looks": "Cómo queda",
      "footer.cart": "Tu carrito",
      "footer.terms": "Términos y condiciones",
      "footer.disclaimer": "BuldakShop es un concepto independiente y no está afiliado, patrocinado ni respaldado por Samyang Foods o la marca Buldak.",
      "search.index": "Cambiar sabor",
      "search.close": "Cerrar",
      "search.title": "¿Qué bolsa quieres ver?",
      "search.label": "Buscar sabores",
      "search.placeholder": "Prueba “queso” o “picante”",
      "search.try": "Prueba",
      "search.noResults": "Ningún sabor coincide. Prueba “carbonara”, “picante” o “queso”.",
      "cart.title": "Tu carrito",
      "cart.close": "Cerrar",
      "cart.clear": "Vaciar todo",
      "cart.cleared": "El carrito quedó vacío.",
      "cart.emptyTitle": "Tu carrito está vacío.",
      "cart.emptyCopy": "Elige cualquier producto del catálogo para agregarlo.",
      "cart.shop": "Ver catálogo",
      "cart.subtotal": "Subtotal",
      "cart.shippingEmpty": "Envío provisional: $0.00.",
      "cart.shippingOne": "1 artículo · envío provisional $0.00.",
      "cart.shippingMany": "{count} artículos · envío provisional $0.00.",
      "cart.checkout": "Confirmar pedido demo",
      "cart.remove": "Eliminar",
      "cart.each": "c/u",
      "cart.quantity": "Cantidad de {name}",
      "cart.reduce": "Reducir cantidad de {name}",
      "cart.increase": "Aumentar cantidad de {name}",
      "cart.added": "{name} se agregó al carrito.",
      "cart.limit": "Puedes agregar hasta 20 unidades por producto.",
      "checkout.close": "Cerrar pedido",
      "checkout.index": "Pedido de prueba",
      "checkout.title": "Confirma tu carrito.",
      "checkout.copy": "Los artículos usan el precio provisional de $0.01 y no se realizará ningún cobro.",
      "checkout.name": "Nombre completo",
      "checkout.email": "Correo",
      "checkout.submit": "Confirmar pedido demo",
      "checkout.submitting": "Confirmando…",
      "checkout.error": "No pudimos confirmar este pedido.",
      "checkout.successIndex": "Pedido confirmado",
      "checkout.successTitle": "Tu pedido demo quedó registrado.",
      "checkout.successCopy": "Pedido {id} · total {total}.",
      "checkout.continue": "Seguir explorando",
      "legal.open": "Abrir términos y condiciones",
      "legal.close": "Cerrar términos",
      "legal.index": "Información legal",
      "legal.title": "Términos y condiciones.",
      "legal.updated": "Última actualización: 17 de agosto de 2026",
      "legal.independentTitle": "Sitio independiente",
      "legal.independentCopy": "BuldakShop es un proyecto independiente. No está afiliado, asociado, patrocinado, autorizado ni respaldado por Samyang Foods Co., Ltd. ni por la marca Buldak.",
      "legal.catalogTitle": "Catálogo y precios",
      "legal.catalogCopy": "El contenido es informativo y demostrativo. Los precios de $0.01 son provisionales, no constituyen una oferta comercial y pueden cambiar antes de habilitar ventas reales.",
      "legal.orderTitle": "Pedidos de demostración",
      "legal.orderCopy": "El checkout actual registra pedidos de prueba y no procesa pagos. Una confirmación no crea una obligación de venta, envío o entrega.",
      "legal.productTitle": "Marcas e información de producto",
      "legal.productCopy": "Las marcas, nombres de producto e imágenes pertenecen a sus respectivos titulares. Ingredientes, alérgenos, valores nutricionales, disponibilidad y preparación pueden variar por mercado; siempre prevalece el empaque oficial.",
      "legal.dataTitle": "Datos y responsabilidad",
      "legal.dataCopy": "Los datos ingresados se usan únicamente para procesar la demostración solicitada. BuldakShop no garantiza que el contenido esté libre de errores y no asume responsabilidad por decisiones tomadas sin verificar el empaque o la información oficial del fabricante.",
      "legal.acceptance": "Al utilizar este sitio aceptas estos términos y entiendes que se trata de una experiencia de demostración.",
      "noscript": "Esta tienda interactiva necesita JavaScript activado."
    },
    en: {
      "meta.title": "BuldakShop — Choose your flavor",
      "meta.description": "BuldakShop: flavor, preparation and pairing notes for each Buldak.",
      "skip": "Skip to content",
      "nav.catalog": "Catalog",
      "nav.buy": "Shop",
      "nav.info": "Information",
      "nav.preparation": "Preparation",
      "header.changeFlavor": "Change flavor",
      "header.cart": "Cart",
      "header.openCart": "Open cart",
      "header.language": "Language",
      "hero.type": "Stir-fried ramen",
      "hero.heat": "Heat",
      "hero.presentation": "Format",
      "hero.individualPack": "Individual pack",
      "hero.quantity": "Quantity",
      "hero.reduceQuantity": "Decrease quantity",
      "hero.increaseQuantity": "Increase quantity",
      "hero.add": "Add to cart",
      "hero.provisional": "Provisional price per item",
      "hero.viewCatalog": "View full catalog",
      "hero.carousel": "Buldak flavor selector",
      "hero.selectFlavor": "Select {name}",
      "hero.drag": "Drag to rotate",
      "hero.chooseFlavor": "Choose a flavor",
      "hero.previous": "Previous flavor",
      "hero.next": "Next flavor",
      "hero.scroll": "Drag the pack · scroll to learn more",
      "catalog.index": "02 — July catalog",
      "catalog.title": "Every product.<br><span>Ready for your cart.</span>",
      "catalog.copy": "{count} products available. Every item uses the provisional $0.01 price until the final price list arrives.",
      "catalog.filter": "Filter catalog",
      "filter.all": "All",
      "filter.bags": "Packs",
      "filter.bowls": "Bowls",
      "filter.tteokbokki": "Tteokbokki",
      "filter.snacks": "Snacks",
      "category.bags": "Pack",
      "category.bowls": "Bowl",
      "category.tteokbokki": "Tteokbokki",
      "category.snacks": "Snack",
      "catalog.available": "Available",
      "catalog.soldOut": "Sold out",
      "catalog.add": "Add",
      "catalog.quantity": "Quantity of {name}",
      "catalog.reduce": "Reduce quantity of {name}",
      "catalog.increase": "Increase quantity of {name}",
      "catalog.details": "View description",
      "catalog.selected": "Description open",
      "story.index": "03 — Selected pack",
      "story.profile": "Flavor profile.",
      "story.cook": "Cook time",
      "story.portion": "Serving",
      "story.nutrition": "Values are per pack. Information may vary by market; always confirm the label on your package.",
      "story.source": "Product source",
      "ritual.index": "04 — Exact preparation",
      "prepared.index": "05 — Served and paired",
      "prepared.title": "The finished",
      "prepared.pairings": "Pairs well with",
      "footer.description": "A shop with the complete catalog and precise information for the selected flavor.",
      "footer.explore": "Explore",
      "footer.buy": "Shop",
      "footer.products": "All products",
      "footer.looks": "Finished dish",
      "footer.cart": "Your cart",
      "footer.terms": "Terms and conditions",
      "footer.disclaimer": "BuldakShop is an independent concept and is not affiliated with, sponsored by or endorsed by Samyang Foods or the Buldak brand.",
      "search.index": "Change flavor",
      "search.close": "Close",
      "search.title": "Which pack would you like to see?",
      "search.label": "Search flavors",
      "search.placeholder": "Try “cheese” or “spicy”",
      "search.try": "Try",
      "search.noResults": "No flavor matched. Try “carbonara”, “spicy” or “cheese”.",
      "cart.title": "Your cart",
      "cart.close": "Close",
      "cart.clear": "Remove all",
      "cart.cleared": "Your cart is now empty.",
      "cart.emptyTitle": "Your cart is empty.",
      "cart.emptyCopy": "Choose any catalog product to add it.",
      "cart.shop": "View catalog",
      "cart.subtotal": "Subtotal",
      "cart.shippingEmpty": "Provisional shipping: $0.00.",
      "cart.shippingOne": "1 item · provisional shipping $0.00.",
      "cart.shippingMany": "{count} items · provisional shipping $0.00.",
      "cart.checkout": "Confirm demo order",
      "cart.remove": "Remove",
      "cart.each": "each",
      "cart.quantity": "Quantity of {name}",
      "cart.reduce": "Decrease quantity of {name}",
      "cart.increase": "Increase quantity of {name}",
      "cart.added": "{name} was added to your cart.",
      "cart.limit": "You can add up to 20 units per product.",
      "checkout.close": "Close order",
      "checkout.index": "Demo order",
      "checkout.title": "Confirm your cart.",
      "checkout.copy": "Items use the provisional $0.01 price and no payment will be processed.",
      "checkout.name": "Full name",
      "checkout.email": "Email",
      "checkout.submit": "Confirm demo order",
      "checkout.submitting": "Confirming…",
      "checkout.error": "We could not confirm this order.",
      "checkout.successIndex": "Order confirmed",
      "checkout.successTitle": "Your demo order was recorded.",
      "checkout.successCopy": "Order {id} · total {total}.",
      "checkout.continue": "Keep exploring",
      "legal.open": "Open terms and conditions",
      "legal.close": "Close terms",
      "legal.index": "Legal information",
      "legal.title": "Terms and conditions.",
      "legal.updated": "Last updated: August 17, 2026",
      "legal.independentTitle": "Independent website",
      "legal.independentCopy": "BuldakShop is an independent project. It is not affiliated, associated, sponsored, authorized or endorsed by Samyang Foods Co., Ltd. or the Buldak brand.",
      "legal.catalogTitle": "Catalog and prices",
      "legal.catalogCopy": "The content is informational and demonstrative. The $0.01 prices are provisional, do not constitute a commercial offer and may change before real sales are enabled.",
      "legal.orderTitle": "Demo orders",
      "legal.orderCopy": "The current checkout records test orders and does not process payments. A confirmation does not create an obligation to sell, ship or deliver.",
      "legal.productTitle": "Trademarks and product information",
      "legal.productCopy": "Trademarks, product names and images belong to their respective owners. Ingredients, allergens, nutrition, availability and preparation may vary by market; the official package always takes precedence.",
      "legal.dataTitle": "Data and liability",
      "legal.dataCopy": "Submitted data is used only to process the requested demonstration. BuldakShop does not guarantee error-free content and accepts no liability for decisions made without checking the package or the manufacturer’s official information.",
      "legal.acceptance": "By using this site, you accept these terms and understand that this is a demonstration experience.",
      "noscript": "This interactive shop requires JavaScript."
    },
    zh: {
      "meta.title": "BuldakShop — 选择口味",
      "meta.description": "BuldakShop：每款火鸡面的口味、烹饪方法与搭配建议。",
      "skip": "跳到主要内容",
      "nav.catalog": "商品目录",
      "nav.buy": "购买",
      "nav.info": "产品信息",
      "nav.preparation": "烹饪方法",
      "header.changeFlavor": "更换口味",
      "header.cart": "购物车",
      "header.openCart": "打开购物车",
      "header.language": "语言",
      "hero.type": "干拌拉面",
      "hero.heat": "辣度",
      "hero.presentation": "规格",
      "hero.individualPack": "单袋装",
      "hero.quantity": "数量",
      "hero.reduceQuantity": "减少数量",
      "hero.increaseQuantity": "增加数量",
      "hero.add": "加入购物车",
      "hero.provisional": "每件商品暂定价格",
      "hero.viewCatalog": "查看完整目录",
      "hero.carousel": "Buldak 口味选择器",
      "hero.selectFlavor": "选择 {name}",
      "hero.drag": "拖动旋转",
      "hero.chooseFlavor": "选择口味",
      "hero.previous": "上一个口味",
      "hero.next": "下一个口味",
      "hero.scroll": "拖动包装 · 向下了解详情",
      "catalog.index": "02 — 七月商品目录",
      "catalog.title": "全部商品。<br><span>等待加入购物车。</span>",
      "catalog.copy": "共有 {count} 件商品。正式价格表发布前，每件商品暂定为 $0.01。",
      "catalog.filter": "筛选商品",
      "filter.all": "全部",
      "filter.bags": "袋装",
      "filter.bowls": "碗装",
      "filter.tteokbokki": "辣炒年糕",
      "filter.snacks": "零食",
      "category.bags": "袋装",
      "category.bowls": "碗装",
      "category.tteokbokki": "辣炒年糕",
      "category.snacks": "零食",
      "catalog.available": "有货",
      "catalog.soldOut": "售罄",
      "catalog.add": "添加",
      "catalog.quantity": "{name} 的数量",
      "catalog.reduce": "减少 {name} 的数量",
      "catalog.increase": "增加 {name} 的数量",
      "catalog.details": "查看描述",
      "catalog.selected": "正在查看",
      "story.index": "03 — 当前选择",
      "story.profile": "风味档案。",
      "story.cook": "烹饪时间",
      "story.portion": "每份",
      "story.nutrition": "数值以每袋为准。不同市场的信息可能有所不同，请始终核对包装标签。",
      "story.source": "产品来源",
      "ritual.index": "04 — 精确烹饪",
      "prepared.index": "05 — 成品与搭配",
      "prepared.title": "完成后的",
      "prepared.pairings": "推荐搭配",
      "footer.description": "提供完整商品目录及当前所选口味的详细信息。",
      "footer.explore": "浏览",
      "footer.buy": "购买",
      "footer.products": "全部商品",
      "footer.looks": "成品展示",
      "footer.cart": "购物车",
      "footer.terms": "条款与条件",
      "footer.disclaimer": "BuldakShop 是独立概念项目，与 Samyang Foods 或 Buldak 品牌无隶属、赞助或背书关系。",
      "search.index": "更换口味",
      "search.close": "关闭",
      "search.title": "想查看哪一款？",
      "search.label": "搜索口味",
      "search.placeholder": "试试“芝士”或“辣”",
      "search.try": "试试",
      "search.noResults": "没有匹配的口味。请尝试“carbonara”“辣”或“芝士”。",
      "cart.title": "购物车",
      "cart.close": "关闭",
      "cart.clear": "清空购物车",
      "cart.cleared": "购物车已清空。",
      "cart.emptyTitle": "购物车是空的。",
      "cart.emptyCopy": "从商品目录中选择任意商品加入购物车。",
      "cart.shop": "查看商品目录",
      "cart.subtotal": "小计",
      "cart.shippingEmpty": "暂定运费：$0.00。",
      "cart.shippingOne": "1 件商品 · 暂定运费 $0.00。",
      "cart.shippingMany": "{count} 件商品 · 暂定运费 $0.00。",
      "cart.checkout": "确认演示订单",
      "cart.remove": "删除",
      "cart.each": "每件",
      "cart.quantity": "{name} 的数量",
      "cart.reduce": "减少 {name} 的数量",
      "cart.increase": "增加 {name} 的数量",
      "cart.added": "{name} 已加入购物车。",
      "cart.limit": "每种商品最多可添加 20 件。",
      "checkout.close": "关闭订单",
      "checkout.index": "演示订单",
      "checkout.title": "确认购物车。",
      "checkout.copy": "商品采用 $0.01 暂定价格，不会进行任何付款。",
      "checkout.name": "姓名",
      "checkout.email": "电子邮箱",
      "checkout.submit": "确认演示订单",
      "checkout.submitting": "正在确认…",
      "checkout.error": "无法确认此订单。",
      "checkout.successIndex": "订单已确认",
      "checkout.successTitle": "演示订单已记录。",
      "checkout.successCopy": "订单 {id} · 总计 {total}。",
      "checkout.continue": "继续浏览",
      "legal.open": "打开条款与条件",
      "legal.close": "关闭条款",
      "legal.index": "法律信息",
      "legal.title": "条款与条件。",
      "legal.updated": "最后更新：2026 年 8 月 17 日",
      "legal.independentTitle": "独立网站",
      "legal.independentCopy": "BuldakShop 是独立项目，与 Samyang Foods Co., Ltd. 或 Buldak 品牌无隶属、关联、赞助、授权或背书关系。",
      "legal.catalogTitle": "商品目录与价格",
      "legal.catalogCopy": "本网站内容仅供信息与演示使用。$0.01 为暂定价格，不构成商业报价，在启用真实销售前可能更改。",
      "legal.orderTitle": "演示订单",
      "legal.orderCopy": "当前结账仅记录测试订单，不处理付款。确认信息不产生销售、发货或交付义务。",
      "legal.productTitle": "商标与产品信息",
      "legal.productCopy": "商标、产品名称和图片归各自权利人所有。配料、过敏原、营养、库存与烹饪方法可能因市场而异，始终以官方包装为准。",
      "legal.dataTitle": "数据与责任",
      "legal.dataCopy": "提交的数据仅用于处理所请求的演示。BuldakShop 不保证内容完全无误；如未核对包装或制造商官方信息而作出决定，本网站不承担责任。",
      "legal.acceptance": "使用本网站即表示你接受这些条款，并理解这是演示体验。",
      "noscript": "此互动商店需要启用 JavaScript。"
    }
  };

  // Display names are localized in the browser; API and Supabase values stay unchanged.
  const productNames = {
    es: {
      "811140": "Carbonara",
      "811130": "Carbonara cremosa",
      "811200": "Queso",
      "811150": "Cuatro quesos",
      "811270": "Rosé",
      "811320": "Dulce y picante",
      "811000": "Taco",
      "811340": "Yakisoba",
      "811220": "Habanero y lima",
      "811120": "Original",
      "811210": "Doble picante",
      "811616": "Dulce y picante · tazón grande",
      "811618": "Cuatro quesos · tazón grande",
      "811622": "Carbonara · tazón grande",
      "811624": "Original · tazón grande",
      "811640": "Rosé · tazón grande",
      "811650": "Fideos de cristal anchos Rosé",
      "811612": "Original · tazón grande",
      "811710": "Tteokbokki Carbonara",
      "811720": "Tteokbokki Original",
      "811910": "Papas fritas Habanero y lima",
      "811920": "Papas fritas Original"
    },
    en: {
      "811140": "Carbonara",
      "811130": "Cream Carbonara",
      "811200": "Cheese",
      "811150": "Quattro Cheese",
      "811270": "Rosé",
      "811320": "Swicy",
      "811000": "Taco",
      "811340": "Yakisoba",
      "811220": "Habanero Lime",
      "811120": "Original",
      "811210": "2X Spicy",
      "811616": "Swicy Big Bowl",
      "811618": "Quattro Cheese Big Bowl",
      "811622": "Carbonara Big Bowl",
      "811624": "Original Big Bowl",
      "811640": "Rosé Big Bowl",
      "811650": "Rosé Wide Glass Noodle",
      "811612": "Original Big Bowl",
      "811710": "Carbonara Tteokbokki",
      "811720": "Original Tteokbokki",
      "811910": "Habanero Lime Potato Chips",
      "811920": "Original Potato Chips"
    },
    zh: {
      "811140": "奶油味火鸡面",
      "811130": "奶油干酪味火鸡面",
      "811200": "芝士味火鸡面",
      "811150": "芝士联盟火鸡面",
      "811270": "玫瑰奶油味火鸡面",
      "811320": "焦糖甜辣味火鸡面",
      "811000": "塔可味火鸡面",
      "811340": "日式炒面味火鸡面",
      "811220": "哈瓦那辣椒青柠味火鸡面",
      "811120": "原味火鸡面",
      "811210": "双倍辣火鸡面",
      "811616": "焦糖甜辣味火鸡面（大碗）",
      "811618": "芝士联盟火鸡面（大碗）",
      "811622": "奶油味火鸡面（大碗）",
      "811624": "原味火鸡面（大碗）",
      "811640": "玫瑰奶油味火鸡面（大碗）",
      "811650": "玫瑰奶油味宽粉",
      "811612": "原味火鸡面（大碗）",
      "811710": "奶油味火鸡炒年糕",
      "811720": "原味火鸡炒年糕",
      "811910": "哈瓦那辣椒青柠味火鸡薯片",
      "811920": "原味火鸡薯片"
    }
  };

  const productDetails = {
    es: {
      "811140": {
        description: "Carbonara combina la salsa picante Buldak con un perfil cremoso y sabroso. El queso suaviza el golpe inicial y deja un final cálido y ligeramente dulce.",
        note: "Cremosa.\nPicor amable."
      },
      "811130": {
        description: "Carbonara cremosa lleva el perfil lácteo todavía más lejos. Es más suave, redonda y untuosa que la Carbonara clásica, sin perder el carácter picante de Buldak.",
        note: "Más crema.\nMenos filo."
      },
      "811200": {
        description: "Queso mezcla una base salada y reconfortante con el picor característico de Buldak. El resultado es directo, intenso y pensado para quienes quieren que el queso siga presente hasta el final.",
        note: "Queso primero.\nPicor después."
      },
      "811150": {
        description: "Cuatro quesos ofrece una salsa más densa y profunda que la versión de queso. Su perfil cremoso envuelve los fideos antes de dar paso a un picor medio y persistente.",
        note: "Cuatro quesos.\nUn final picante."
      },
      "811270": {
        description: "Rosé se inspira en la salsa coreana del mismo nombre: cremosa, ligeramente dulce y con picor equilibrado. Es una opción suave para quienes prefieren una textura sedosa.",
        note: "Suave.\nSedosa."
      },
      "811320": {
        description: "Dulce y picante equilibra una entrada azucarada con un picor ligero. Su salsa es más accesible que Original y mantiene un acabado sabroso sin resultar pesada.",
        note: "Dulce al inicio.\nPicante al final."
      },
      "811000": {
        description: "Taco lleva Buldak hacia un perfil inspirado en especias mexicanas. Combina notas tostadas, chile y un acabado sabroso que funciona especialmente bien con ingredientes frescos.",
        note: "Especiada.\nEstilo taco."
      },
      "811340": {
        description: "Yakisoba toma como referencia los fideos salteados japoneses. Su salsa es dulce, salada y llena de umami, con un picor firme que aparece después del primer bocado.",
        note: "Dulce y salada.\nMucho umami."
      },
      "811220": {
        description: "Habanero y lima combina un picor alto con una acidez cítrica brillante. La lima refresca el final y hace que el calor se sienta más ligero y directo.",
        note: "Cítrica.\nPicante."
      },
      "811120": {
        description: "Original es la referencia clásica de Buldak: una salsa espesa, sabrosa y muy picante que cubre cada fideo. El sésamo y el alga tostada completan el acabado.",
        note: "La clásica.\nSin atajos."
      },
      "811210": {
        description: "Doble picante concentra el perfil de Original en una experiencia mucho más intensa. Está pensada para quienes buscan calor extremo y un picor que permanece después de comer.",
        note: "Doble intensidad.\nPicor extremo."
      },
      "811616": {
        description: "La versión en tazón grande de Dulce y picante conserva el equilibrio entre dulzor y calor suave, con una presentación práctica para preparar y comer directamente.",
        note: "Dulce y picante.\nFormato grande."
      },
      "811618": {
        description: "Cuatro quesos en tazón grande reúne una salsa cremosa y profunda con una porción práctica. El queso domina al principio y el picor aparece de forma gradual.",
        note: "Cuatro quesos.\nTazón grande."
      },
      "811622": {
        description: "Carbonara en tazón grande mantiene el perfil cremoso, sabroso y ligeramente picante de la bolsa rosa, en un formato cómodo para una preparación rápida.",
        note: "Cremosa.\nLista en su tazón."
      },
      "811624": {
        description: "Original en tazón grande conserva la salsa clásica, intensa y sin caldo de Buldak. Es el mismo perfil de picor directo en una presentación lista para preparar.",
        note: "Original.\nFormato grande."
      },
      "811640": {
        description: "Rosé en tazón grande combina una salsa sedosa, dulzor moderado y picor suave. El formato amplio permite mezclar la salsa de forma uniforme antes de comer.",
        note: "Rosé cremoso.\nTazón grande."
      },
      "811650": {
        description: "Los fideos de cristal anchos Rosé cambian el fideo de trigo por una textura ancha, transparente y elástica. La salsa cremosa se adhiere a cada pliegue con un picor equilibrado.",
        note: "Textura elástica.\nSalsa Rosé."
      },
      "811612": {
        description: "Esta referencia alterna de Original en tazón grande mantiene el sabor clásico, sabroso y muy picante. Cambia el SKU, no el perfil principal del producto.",
        note: "Mismo perfil.\nSKU alterno."
      },
      "811710": {
        description: "Tteokbokki Carbonara combina pastel de arroz coreano, elástico y denso, con una salsa cremosa de picor moderado. Cada pieza queda cubierta por una capa suave y sabrosa.",
        note: "Pastel de arroz.\nCarbonara cremosa."
      },
      "811720": {
        description: "Tteokbokki Original lleva la salsa clásica Buldak a pasteles de arroz masticables. El resultado concentra el picor y la textura en bocados cortos e intensos.",
        note: "Textura firme.\nSalsa original."
      },
      "811910": {
        description: "Las papas fritas Habanero y lima trasladan el perfil cítrico y picante a una botana crujiente. Primero aparece la lima y después sube el calor del habanero.",
        note: "Crujientes.\nCítricas."
      },
      "811920": {
        description: "Las papas fritas Original convierten el sabor clásico Buldak en una botana crujiente. Mantienen el equilibrio entre notas sabrosas, dulces y un picor directo.",
        note: "Crujientes.\nSabor original."
      }
    },
    en: {
      "811140": {
        description: "Carbonara combines Buldak's spicy sauce with a creamy, savory profile. Cheese softens the first hit and leaves a warm, lightly sweet finish.",
        note: "Creamy.\nFriendly heat."
      },
      "811130": {
        description: "Cream Carbonara pushes the dairy profile even further. It is smoother, rounder and richer than classic Carbonara while keeping the unmistakable Buldak character.",
        note: "More cream.\nSofter edges."
      },
      "811200": {
        description: "Cheese blends a salty, comforting base with Buldak's signature heat. It is direct and intense, with cheese flavor that remains present through the finish.",
        note: "Cheese first.\nHeat follows."
      },
      "811150": {
        description: "Quattro Cheese delivers a thicker, deeper sauce than the standard Cheese flavor. Creaminess coats the noodles before a medium, lasting heat comes through.",
        note: "Four cheeses.\nOne spicy finish."
      },
      "811270": {
        description: "Rosé is inspired by the Korean sauce of the same name: creamy, gently sweet and balanced in heat. It suits anyone looking for a smoother, silkier bowl.",
        note: "Smooth.\nSilky."
      },
      "811320": {
        description: "Swicy balances a sweet opening with mild heat. Its sauce is more approachable than Original and keeps a savory finish without feeling heavy.",
        note: "Sweet first.\nSpicy finish."
      },
      "811000": {
        description: "Taco moves Buldak toward a Mexican-inspired spice profile. Toasted notes and chili create a savory finish that pairs especially well with fresh toppings.",
        note: "Spiced.\nTaco inspired."
      },
      "811340": {
        description: "Yakisoba takes cues from Japanese stir-fried noodles. The sauce is sweet, savory and rich in umami, followed by firm heat after the first bite.",
        note: "Sweet and savory.\nDeep umami."
      },
      "811220": {
        description: "Habanero Lime combines high heat with bright citrus acidity. Lime freshens the finish and makes the burn feel lighter and more direct.",
        note: "Citrusy.\nHot."
      },
      "811120": {
        description: "Original is the classic Buldak benchmark: a thick, savory and very spicy sauce that coats every noodle, finished with sesame and toasted seaweed.",
        note: "The classic.\nNo shortcuts."
      },
      "811210": {
        description: "2X Spicy concentrates the Original profile into a far more intense experience. It is made for people who want extreme, lingering heat.",
        note: "Double intensity.\nExtreme heat."
      },
      "811616": {
        description: "Swicy Big Bowl keeps the balance of sweetness and gentle heat in a practical format designed to be prepared and eaten straight from the bowl.",
        note: "Sweet and spicy.\nBig bowl."
      },
      "811618": {
        description: "Quattro Cheese Big Bowl pairs a deep creamy sauce with a convenient serving. Cheese leads and the Buldak heat builds gradually.",
        note: "Four cheeses.\nBig bowl."
      },
      "811622": {
        description: "Carbonara Big Bowl preserves the creamy, savory and gently spicy character of the pink pouch in a convenient quick-prep format.",
        note: "Creamy.\nReady in its bowl."
      },
      "811624": {
        description: "Original Big Bowl keeps the classic intense, brothless Buldak sauce in a ready-to-prepare format with the same direct heat.",
        note: "Original.\nBig bowl."
      },
      "811640": {
        description: "Rosé Big Bowl combines a silky sauce, moderate sweetness and mild heat. The larger format gives the sauce room to coat the noodles evenly.",
        note: "Creamy Rosé.\nBig bowl."
      },
      "811650": {
        description: "Rosé Wide Glass Noodle replaces wheat noodles with a wide, translucent and chewy texture. Creamy sauce clings to every fold with balanced heat.",
        note: "Chewy texture.\nRosé sauce."
      },
      "811612": {
        description: "This alternate Original Big Bowl reference keeps the classic savory and very spicy flavor. The SKU changes, not the product's main profile.",
        note: "Same profile.\nAlternate SKU."
      },
      "811710": {
        description: "Carbonara Tteokbokki combines dense, chewy Korean rice cakes with a creamy sauce and moderate heat. Every piece is coated in a smooth, savory layer.",
        note: "Rice cakes.\nCreamy Carbonara."
      },
      "811720": {
        description: "Original Tteokbokki brings classic Buldak sauce to chewy rice cakes, concentrating bold heat and dense texture into short, intense bites.",
        note: "Firm chew.\nOriginal sauce."
      },
      "811910": {
        description: "Habanero Lime Potato Chips turn the bright, spicy profile into a crisp snack. Lime arrives first, followed by a rising habanero burn.",
        note: "Crisp.\nCitrusy."
      },
      "811920": {
        description: "Original Potato Chips translate the classic Buldak flavor into a crisp snack, balancing savory and sweet notes with direct heat.",
        note: "Crisp.\nOriginal flavor."
      }
    },
    zh: {
      "811140": {
        description: "奶油味火鸡面将 Buldak 辣酱与浓郁顺滑的奶香结合。芝士缓和入口辣感，并留下温暖、微甜的尾韵。",
        note: "浓郁奶香。\n柔和辣感。"
      },
      "811130": {
        description: "奶油干酪味火鸡面进一步强化乳香，比经典奶油味更顺滑、更圆润，同时保留鲜明的 Buldak 辣味。",
        note: "奶香更浓。\n口感更柔。"
      },
      "811200": {
        description: "芝士味火鸡面将咸香芝士与招牌辣味结合。入口直接浓郁，芝士风味一直延续到最后。",
        note: "芝士在前。\n辣味随后。"
      },
      "811150": {
        description: "芝士联盟火鸡面比普通芝士味更加浓厚，酱汁包裹面条后，中等辣度逐渐出现并持续停留。",
        note: "多重芝士。\n香辣收尾。"
      },
      "811270": {
        description: "玫瑰奶油味火鸡面采用韩式 Rosé 风格，口感顺滑、微甜，辣度均衡，适合偏爱丝滑酱汁的人。",
        note: "柔和。\n丝滑。"
      },
      "811320": {
        description: "焦糖甜辣味火鸡面以甜味开场，再带出轻柔辣感。相比原味更容易入口，尾韵依然鲜香。",
        note: "先甜。\n后辣。"
      },
      "811000": {
        description: "塔可味火鸡面采用墨西哥风格香料方向，烘烤香气与辣椒带来咸香尾韵，搭配新鲜配料尤其合适。",
        note: "香料丰富。\n塔可风格。"
      },
      "811340": {
        description: "日式炒面味火鸡面借鉴日式炒面风格，酱汁甜咸平衡、鲜味浓郁，第一口后辣度逐渐增强。",
        note: "甜咸平衡。\n鲜味浓郁。"
      },
      "811220": {
        description: "哈瓦那辣椒青柠味火鸡面把强烈辣感与明亮酸香结合，青柠让尾韵更清爽，也让灼热感更直接。",
        note: "清新柑橘。\n强烈辣感。"
      },
      "811120": {
        description: "原味火鸡面是 Buldak 的经典基准：浓稠、鲜香且非常辣的酱汁包裹每根面条，并以芝麻和烤海苔收尾。",
        note: "经典原味。\n毫不妥协。"
      },
      "811210": {
        description: "双倍辣火鸡面将原味浓缩成更强烈的体验，适合追求极致、持久热感的辣味爱好者。",
        note: "双倍强度。\n极致辣感。"
      },
      "811616": {
        description: "焦糖甜辣味火鸡面大碗装保留甜味与柔和辣感的平衡，可直接在碗中冲泡食用，更加方便。",
        note: "甜辣平衡。\n大碗装。"
      },
      "811618": {
        description: "芝士联盟火鸡面大碗装将浓郁奶香与方便份量结合，芝士先出现，Buldak 辣味随后逐渐增强。",
        note: "多重芝士。\n大碗装。"
      },
      "811622": {
        description: "奶油味火鸡面大碗装保留粉色袋装的浓郁、鲜香和柔和辣感，适合快速冲泡享用。",
        note: "浓郁奶香。\n碗中即食。"
      },
      "811624": {
        description: "原味火鸡面大碗装保留经典无汤辣酱与直接辣感，以方便冲泡的形式呈现。",
        note: "经典原味。\n大碗装。"
      },
      "811640": {
        description: "玫瑰奶油味火鸡面大碗装结合丝滑酱汁、适度甜味和柔和辣感，宽大碗身便于均匀拌面。",
        note: "奶香 Rosé。\n大碗装。"
      },
      "811650": {
        description: "玫瑰奶油味宽粉以宽、透明且弹韧的粉条替代小麦面，浓郁酱汁附着在每个褶皱上，辣度均衡。",
        note: "弹韧口感。\nRosé 酱汁。"
      },
      "811612": {
        description: "这一备用 SKU 的原味火鸡面大碗装依然保持经典鲜香和高辣度，变化的是编号，不是主要风味。",
        note: "相同风味。\n备用 SKU。"
      },
      "811710": {
        description: "奶油味火鸡炒年糕将弹韧紧实的韩式年糕与浓郁酱汁结合，辣度适中，每块年糕都裹满顺滑咸香。",
        note: "弹韧年糕。\n奶油酱汁。"
      },
      "811720": {
        description: "原味火鸡炒年糕把经典 Buldak 辣酱带到弹牙年糕上，在短小浓缩的每一口中呈现强烈辣味。",
        note: "紧实弹牙。\n原味辣酱。"
      },
      "811910": {
        description: "哈瓦那辣椒青柠味火鸡薯片把清新酸辣风味变成酥脆零食，先尝到青柠，随后哈瓦那辣感升高。",
        note: "酥脆。\n清新酸香。"
      },
      "811920": {
        description: "原味火鸡薯片把经典 Buldak 风味变成酥脆零食，在鲜香、微甜与直接辣感之间取得平衡。",
        note: "酥脆。\n经典原味。"
      }
    }
  };

  const productContent = {
    en: {
      "811140": {
        description: "Spicy chicken sauce with milk, butter, mozzarella and black pepper.",
        heat_label: "Creamy heat · 2/5",
        weight: "130 g · individual pack",
        story_title: ["Creamy.", "Spicy.", "Pure Carbonara."],
        story: "The pink pack blends Buldak sauce with cheese and cream powder. Mozzarella and butter arrive first, followed by chili, garlic and black pepper.",
        story_note: "Cheese first.\nHeat follows.",
        directions_title: ["Five minutes.", "Exact creaminess."],
        directions_intro: "Preparation for one 130 g Carbonara pack.",
        directions: [
          { title: "Boil", text: "Bring 600 ml of water to a boil." },
          { title: "Cook", text: "Add the noodles and cook for 5 minutes." },
          { title: "Reserve", text: "Drain, leaving 8 tablespoons of water." },
          { title: "Mix", text: "Add the sauce and cheese powder; mix and serve." }
        ],
        recommendations: [
          { title: "Soft egg", text: "The yolk deepens the creamy texture without hiding the chili." },
          { title: "Scallions and mushrooms", text: "They add freshness and umami to the cheese sauce." },
          { title: "Cold cucumber", text: "A crisp, tangy side cleans the palate." }
        ],
        prepared_alt: "Prepared Buldak Carbonara in a bowl beside its pink pack"
      },
      "811120": {
        description: "Spicy chicken sauce, red chili, sesame and toasted seaweed without a creamy layer.",
        heat_label: "Very spicy · 5/5",
        weight: "140 g · individual pack",
        story_title: ["Direct.", "Toasted.", "The original."],
        story: "The black pack is the recipe that started the Buldak challenge. The brothless sauce coats every noodle: seasoned chicken and curry come first, then chili rises with sesame and toasted seaweed at the finish.",
        story_note: "No broth.\nHeat up front.",
        directions_title: ["Five minutes.", "Thirty seconds in the pan."],
        directions_intro: "Preparation for one 140 g Original pack.",
        directions: [
          { title: "Boil", text: "Bring 600 ml of water to a boil." },
          { title: "Cook", text: "Add the noodles and cook for 5 minutes." },
          { title: "Reserve", text: "Drain, leaving about 1/2 cup (120 ml) of water." },
          { title: "Stir-fry", text: "Add the sauce, stir-fry for 30 seconds and finish with the flakes." }
        ],
        recommendations: [
          { title: "Fried egg", text: "The yolk rounds out the heat and adds body to the noodles." },
          { title: "Seaweed and scallions", text: "They reinforce the toasted finish and add freshness." },
          { title: "Cold milk drink", text: "Dairy fat helps soften the capsaicin sensation." }
        ],
        prepared_alt: "Prepared Original Buldak in a pan beside its black pack"
      },
      "811150": {
        description: "Mozzarella, cheddar, gouda and camembert over spicy Buldak sauce.",
        heat_label: "Cheesy heat · 3/5",
        weight: "145 g · individual pack",
        story_title: ["Four cheeses.", "One sauce.", "Late heat."],
        story: "Mozzarella, cheddar, gouda and camembert form a thick, savory sauce. The first impression is creamy; the chili follows and lingers. The catalog pack contains 145 g.",
        story_note: "Four cheeses.\nOne spicy finish.",
        directions_title: ["Five and a half.", "All the cheese."],
        directions_intro: "Preparation for one 145 g Quattro Cheese pack.",
        directions: [
          { title: "Boil", text: "Bring 600 ml of water to a boil." },
          { title: "Cook", text: "Add the noodles and cook for 5 minutes 30 seconds." },
          { title: "Reserve", text: "Drain, leaving about 6 tablespoons (90 ml) of water." },
          { title: "Mix", text: "Add the sauce and four-cheese powder; mix and serve." }
        ],
        recommendations: [
          { title: "Golden corn", text: "Its sweetness balances the chili and matches the four cheeses." },
          { title: "Grilled chicken", text: "It adds protein without competing with the creamy sauce." },
          { title: "Crunchy pickles", text: "Their acidity cuts through the richness and refreshes each bite." }
        ],
        prepared_alt: "Prepared Buldak Quattro Cheese with melted cheese in a yellow bowl"
      }
    },
    zh: {
      "811140": {
        description: "辣鸡酱搭配牛奶、黄油、马苏里拉芝士与黑胡椒。",
        heat_label: "奶香辣度 · 2/5",
        weight: "130 克 · 单袋装",
        story_title: ["浓郁。", "香辣。", "Carbonara 风味。"],
        story: "粉色包装将 Buldak 辣酱与芝士奶油粉结合。入口先是马苏里拉与黄油，随后出现辣椒、大蒜和黑胡椒。",
        story_note: "芝士在前。\n辣味随后。",
        directions_title: ["五分钟。", "刚好的浓郁。"],
        directions_intro: "130 克 Carbonara 单袋烹饪方法。",
        directions: [
          { title: "煮水", text: "将 600 毫升水煮沸。" },
          { title: "煮面", text: "放入面条，煮 5 分钟。" },
          { title: "留水", text: "沥水，保留 8 汤匙面汤。" },
          { title: "拌匀", text: "加入酱料和芝士粉，拌匀后食用。" }
        ],
        recommendations: [
          { title: "溏心蛋", text: "蛋黄增强奶油质感，同时不会掩盖辣味。" },
          { title: "葱花与蘑菇", text: "为芝士酱增添清新感与鲜味。" },
          { title: "冰镇黄瓜", text: "清脆酸爽，帮助刷新味蕾。" }
        ],
        prepared_alt: "Carbonara Buldak 成品，旁边放有粉色包装"
      },
      "811120": {
        description: "辣鸡酱、红辣椒、芝麻和烤海苔，不含奶油层次。",
        heat_label: "非常辣 · 5/5",
        weight: "140 克 · 单袋装",
        story_title: ["直接。", "焦香。", "经典原味。"],
        story: "黑色包装是开启 Buldak 挑战的经典配方。无汤酱汁包裹面条，先尝到香料鸡肉和咖喱，随后辣椒升温，并以芝麻与烤海苔收尾。",
        story_note: "无汤。\n辣味直接。",
        directions_title: ["五分钟。", "翻炒三十秒。"],
        directions_intro: "140 克 Original 单袋烹饪方法。",
        directions: [
          { title: "煮水", text: "将 600 毫升水煮沸。" },
          { title: "煮面", text: "放入面条，煮 5 分钟。" },
          { title: "留水", text: "沥水，保留约半杯（120 毫升）面汤。" },
          { title: "翻炒", text: "加入酱料翻炒 30 秒，最后撒上配料。" }
        ],
        recommendations: [
          { title: "煎蛋", text: "蛋黄让辣味更圆润，并增加面条的饱满感。" },
          { title: "海苔与葱花", text: "强化焦香收尾并增添清新感。" },
          { title: "冰凉乳饮", text: "乳脂有助于缓和辣椒素带来的灼热感。" }
        ],
        prepared_alt: "Original Buldak 锅中成品，旁边放有黑色包装"
      },
      "811150": {
        description: "马苏里拉、切达、高达和卡芒贝尔芝士搭配 Buldak 辣酱。",
        heat_label: "芝士辣度 · 3/5",
        weight: "145 克 · 单袋装",
        story_title: ["四种芝士。", "一份酱汁。", "后段辣味。"],
        story: "马苏里拉、切达、高达与卡芒贝尔组成浓厚咸香的酱汁。入口先是奶香，辣椒随后出现并停留在口中。单袋净含量 145 克。",
        story_note: "四种芝士。\n香辣收尾。",
        directions_title: ["五分半。", "满满芝士。"],
        directions_intro: "145 克 Quattro Cheese 单袋烹饪方法。",
        directions: [
          { title: "煮水", text: "将 600 毫升水煮沸。" },
          { title: "煮面", text: "放入面条，煮 5 分 30 秒。" },
          { title: "留水", text: "沥水，保留约 6 汤匙（90 毫升）面汤。" },
          { title: "拌匀", text: "加入酱料和四芝士粉，拌匀后食用。" }
        ],
        recommendations: [
          { title: "香甜玉米", text: "甜味平衡辣椒，并与四种芝士相配。" },
          { title: "烤鸡肉", text: "增加蛋白质，又不会抢走奶油酱汁的风味。" },
          { title: "爽脆酸黄瓜", text: "酸味解腻，让每一口更清爽。" }
        ],
        prepared_alt: "Quattro Cheese Buldak 成品，黄色碗中覆盖融化芝士"
      }
    }
  };

  window.BuldakI18n = Object.freeze({ locales, productNames, productDetails, productContent });
})();
