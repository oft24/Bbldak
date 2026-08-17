create table if not exists public.products (
  sku text primary key,
  name text not null,
  category text not null check (category in ('bags', 'bowls', 'tteokbokki', 'snacks')),
  category_label text not null,
  weight text not null,
  case_size text not null,
  image text not null,
  source_url text not null,
  status text not null default 'Disponible',
  price numeric(10, 2) not null default 0.01 check (price >= 0),
  sort_order integer not null unique,
  is_available boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists products_category_idx on public.products (category);
create index if not exists products_available_idx on public.products (is_available);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
security invoker
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists products_set_updated_at on public.products;
create trigger products_set_updated_at
before update on public.products
for each row execute function public.set_updated_at();

alter table public.products enable row level security;

drop policy if exists "Public products are readable" on public.products;
create policy "Public products are readable"
on public.products
for select
to anon, authenticated
using (true);

grant select on table public.products to anon, authenticated;

insert into public.products
  (sku, name, category, category_label, weight, case_size, image, source_url, status, price, sort_order, is_available)
values
  ('811140', 'Carbonara', 'bags', 'Bolsa', '130 g', '40 paquetes', '/assets/carbonara.png?v=2', 'https://samyangamerica.com/buldak/carbonara', 'Disponible', 0.01, 1, true),
  ('811130', 'Cream Carbonara', 'bags', 'Bolsa', '140 g', '40 paquetes', '/assets/catalog/cream-carbonara.jpg?v=1', 'https://getzh.de/samyang-buldak-cream-carbonara-140g', 'Disponible', 0.01, 2, true),
  ('811200', 'Cheese', 'bags', 'Bolsa', '140 g', '40 paquetes', '/assets/catalog/cheese.jpg?v=1', 'https://jasminemarket.fi/vi/products/sam-yang-hot-chicken-ramen-cheese-140g', 'Disponible', 0.01, 3, true),
  ('811150', 'Quattro Cheese', 'bags', 'Bolsa', '145 g', '40 paquetes', '/assets/quattro.png?v=2', 'https://samyangamerica.com/buldak/quattro-cheese', 'Disponible', 0.01, 4, true),
  ('811270', 'Rosé', 'bags', 'Bolsa', '140 g', '40 paquetes', '/assets/catalog/rose.webp?v=1', 'https://megaswalayan.com/web/products/1aea53af-2b9b-43de-ad5d-3526135062a1', 'Disponible', 0.01, 5, true),
  ('811320', 'Sweet & Spicy', 'bags', 'Bolsa', '140 g', '40 paquetes', '/assets/catalog/sweet-spicy.webp?v=1', 'https://midiminuit-epinal.com/products/samyang-buldak-sweet-spicy-140g', 'Disponible', 0.01, 6, true),
  ('811000', 'Taco', 'bags', 'Bolsa', '140 g', '40 paquetes', '/assets/catalog/taco.png?v=1', 'https://www.walmart.com.mx/ip/sopa-instantanea-samyang-buldak-pollo-taco-135g/00880107311714', 'Disponible', 0.01, 7, true),
  ('811340', 'Yakisoba', 'bags', 'Bolsa', '150 g', '40 paquetes', '/assets/catalog/yakisoba.webp?v=1', 'https://dongsong.com.mx/productos/ramen-samyang-hot-sabor-yakisoba/', 'Disponible', 0.01, 8, true),
  ('811220', 'Habanero Lime', 'bags', 'Bolsa', '135 g', '40 paquetes', '/assets/catalog/habanero-lime.jpg?v=1', 'https://lsplace.com.vn/products/samyang-mi-buldak-vi-ga-kho-chua-cay', 'Disponible', 0.01, 9, true),
  ('811120', 'Original', 'bags', 'Bolsa', '140 g', '40 paquetes', '/assets/original.png?v=2', 'https://buldak.com/us/product/buldak-ramen-original/', 'Disponible', 0.01, 10, true),
  ('811210', '2X Spicy', 'bags', 'Bolsa', '140 g', '40 paquetes', '/assets/catalog/2x-spicy.png?v=1', 'https://buldak.com/au/product/buldak-ramen-2x/', 'Disponible', 0.01, 11, true),
  ('811616', 'Sweet & Spicy Korean Chicken', 'bowls', 'Big Bowl', '115 g', '6 bowls', '/assets/catalog/sweet-spicy-bowl.webp?v=1', 'https://mam-shop.de/products/samyang-buldak-sweet-spicy-chicken-bowl-115g', 'Disponible', 0.01, 12, true),
  ('811618', 'Quattro Cheese Big Bowl', 'bowls', 'Big Bowl', '110 g', '6 bowls', '/assets/catalog/quattro-bowl.png?v=1', 'https://www.talabat.com/kuwait/talabat-mart/product/samyang-buldak-quattro-cheese-hot-chicken-flavor-ramen-stir-fried-noodles-big-bowl-110g/s/934873', 'Disponible', 0.01, 13, true),
  ('811622', 'Carbonara Big Bowl', 'bowls', 'Big Bowl', '105 g', '6 bowls', '/assets/catalog/carbonara-bowl.png?v=1', 'https://www.hmart.com/carbo-hot-chicken-ramen-big-bowl-3-7-oz--105g-/p', 'Disponible', 0.01, 14, true),
  ('811624', 'Original Big Bowl', 'bowls', 'Big Bowl', '105 g', '6 bowls', '/assets/catalog/original-bowl.webp?v=1', 'https://m.yami.com/en/p/samyang-hot-chicken-flavor-ramen-big-bowl-105g/1021027581', 'Disponible', 0.01, 15, true),
  ('811640', 'Rosé Big Bowl', 'bowls', 'Big Bowl', '105 g', '6 bowls', '/assets/catalog/rose-bowl.jpeg?v=1', 'https://www.walmart.ca/en/ip/Samyang-Buldak-Ros-Bowl-105/1KX4LU0M5PWW', 'Disponible', 0.01, 16, true),
  ('811650', 'Rosé Wide Glass Noodle', 'bowls', 'Wide Glass Noodle', '169.4 g', '16 bowls', '/assets/catalog/wide-glass-noodle.webp?v=1', 'https://www.yami.com/en/p/buldak-wild-glass-noodle-rose-hot-chicken-flavor-bowl-5-98-oz/1021110221', 'Disponible', 0.01, 17, true),
  ('811612', 'Original Big Bowl', 'bowls', 'Big Bowl · SKU alterno', '105 g', '6 bowls', '/assets/catalog/original-bowl.webp?v=1', 'https://m.yami.com/en/p/samyang-hot-chicken-flavor-ramen-big-bowl-105g/1021027581', 'Disponible', 0.01, 18, true),
  ('811710', 'Carbonara Tteokbokki', 'tteokbokki', 'Tteokbokki', '179 g', '16 bowls', '/assets/catalog/carbonara-tteokbokki.jpg?v=1', 'https://online.citysuper.com.hk/products/samyang-carbonara-stir-fried-hot-spicy-chicken-sauce-with-rice-cake-bowl-301431327', 'Disponible', 0.01, 19, true),
  ('811720', 'Original Tteokbokki', 'tteokbokki', 'Tteokbokki', '179 g', '16 bowls', '/assets/catalog/original-tteokbokki.jpg?v=1', 'https://bekndy.com/tienda/samyang-buldak-toppoki-bowl-original-16p179g/', 'Agotado · 14 jul 2026', 0.01, 20, false),
  ('811910', 'Potato Chips Habanero Lime', 'snacks', 'Snack', '120 g', '12 bolsas', '/assets/catalog/chips-habanero.png?v=1', 'https://buldak.com/us/blog/buldak-potato-chip-guide/', 'Disponible', 0.01, 21, true),
  ('811920', 'Potato Chips Original', 'snacks', 'Snack', '120 g', '12 bolsas', '/assets/catalog/chips-original.png?v=1', 'https://popshoplife.com/products/samyang-buldak-potato-chips-original-spicy-chicken-120g-south-korea', 'Disponible', 0.01, 22, true)
on conflict (sku) do update set
  name = excluded.name,
  category = excluded.category,
  category_label = excluded.category_label,
  weight = excluded.weight,
  case_size = excluded.case_size,
  image = excluded.image,
  source_url = excluded.source_url,
  status = excluded.status,
  price = excluded.price,
  sort_order = excluded.sort_order,
  is_available = excluded.is_available;
