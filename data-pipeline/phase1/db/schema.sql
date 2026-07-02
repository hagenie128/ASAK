-- Salady menu data model (3NF)
-- Target: PostgreSQL 14+ (SQLite 호환 시 BOOLEAN→INTEGER, TIMESTAMPTZ→TEXT)

BEGIN;

-- ---------------------------------------------------------------------------
-- 1. Reference / lookup (재사용 마스터)
-- ---------------------------------------------------------------------------

CREATE TABLE brands (
    id              SMALLSERIAL PRIMARY KEY,
    code            VARCHAR(32) NOT NULL UNIQUE,          -- e.g. 'salady'
    name            VARCHAR(100) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE platforms (
    id              SMALLSERIAL PRIMARY KEY,
    code            VARCHAR(32) NOT NULL UNIQUE,          -- official | passorder | naver_order
    name            VARCHAR(100) NOT NULL
);

CREATE TABLE menu_category_types (
    id              SMALLSERIAL PRIMARY KEY,
    code            VARCHAR(32) NOT NULL UNIQUE,          -- official | nav | store
    name            VARCHAR(100) NOT NULL
);

CREATE TABLE menu_categories (
    id              SERIAL PRIMARY KEY,
    brand_id        SMALLINT NOT NULL REFERENCES brands(id),
    category_type_id SMALLINT NOT NULL REFERENCES menu_category_types(id),
    name            VARCHAR(120) NOT NULL,
    parent_id       INT REFERENCES menu_categories(id),
    UNIQUE (brand_id, category_type_id, name)
);

CREATE TABLE tags (
    id              SMALLSERIAL PRIMARY KEY,
    code            VARCHAR(32) NOT NULL UNIQUE,          -- NEW, BEST, LOW_SUGAR
    label           VARCHAR(100) NOT NULL
);

CREATE TABLE allergens (
    id              SMALLSERIAL PRIMARY KEY,
    name            VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE ingredients (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(120) NOT NULL UNIQUE,         -- 토핑·베이스·세트 구성품
    ingredient_kind VARCHAR(32) NOT NULL DEFAULT 'topping'
        CHECK (ingredient_kind IN ('topping', 'base', 'set_component', 'beverage', 'side'))
);

CREATE TABLE dressings (
    id              SMALLSERIAL PRIMARY KEY,
    name            VARCHAR(80) NOT NULL UNIQUE,
    name_normalized VARCHAR(80) NOT NULL UNIQUE,
    is_low_sugar    BOOLEAN NOT NULL DEFAULT FALSE,
    is_vegan        BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE dressing_policies (
    id              SMALLSERIAL PRIMARY KEY,
    code            VARCHAR(32) NOT NULL UNIQUE,          -- default | recommended | included | selection | amount | extra_purchase
    name            VARCHAR(80) NOT NULL
);

CREATE TABLE calorie_addon_types (
    id              SMALLSERIAL PRIMARY KEY,
    code            VARCHAR(32) NOT NULL UNIQUE,          -- vegetable, grain, buckwheat, noodles
    name_ko         VARCHAR(50) NOT NULL
);

CREATE TABLE option_group_kinds (
    id              SMALLSERIAL PRIMARY KEY,
    code            VARCHAR(40) NOT NULL UNIQUE,
    -- base_selection, base_extra, dressing_selection, dressing_amount,
    -- dressing_extra_purchase, topping_extra, soup_extra, set_side
    name_ko         VARCHAR(80) NOT NULL
);

-- ---------------------------------------------------------------------------
-- 2. Official menu catalog (브랜드 공식 메뉴)
-- ---------------------------------------------------------------------------

CREATE TABLE menus (
    id              INT PRIMARY KEY,                     -- salady.com idx
    brand_id        SMALLINT NOT NULL REFERENCES brands(id),
    category_id     INT REFERENCES menu_categories(id),
    nav_category_id INT REFERENCES menu_categories(id),
    menu_type       VARCHAR(20) NOT NULL DEFAULT 'main'
        CHECK (menu_type IN ('main', 'base', 'dressing', 'side', 'beverage')),
    name_ko         VARCHAR(200) NOT NULL,
    name_en         VARCHAR(200),
    description     TEXT,
    base_text       VARCHAR(200),                         -- "곡물, 채소" (비정규 요약; 상세는 menu_ingredients)
    url             TEXT,
    image_url       TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE menu_tags (
    menu_id         INT NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    tag_id          SMALLINT NOT NULL REFERENCES tags(id),
    PRIMARY KEY (menu_id, tag_id)
);

CREATE TABLE menu_allergens (
    menu_id         INT NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    allergen_id     SMALLINT NOT NULL REFERENCES allergens(id),
    source          VARCHAR(20) NOT NULL DEFAULT 'web'
        CHECK (source IN ('web', 'pdf', 'manual')),
    PRIMARY KEY (menu_id, allergen_id, source)
);

CREATE TABLE menu_ingredients (
    menu_id         INT NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    ingredient_id   INT NOT NULL REFERENCES ingredients(id),
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    role            VARCHAR(20) NOT NULL DEFAULT 'topping'
        CHECK (role IN ('topping', 'base', 'default_included')),
    PRIMARY KEY (menu_id, ingredient_id)
);

-- 영양: 출처별 1행 (웹/PDF 중복 허용, 동일 menu에 source UNIQUE)
CREATE TABLE menu_nutrition (
    menu_id         INT NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    source          VARCHAR(20) NOT NULL
        CHECK (source IN ('web', 'pdf')),
    weight_g        NUMERIC(8,1),
    calories_kcal   NUMERIC(8,1),
    carbs_g         NUMERIC(8,1),
    sugar_g         NUMERIC(8,1),
    protein_g       NUMERIC(8,1),
    fat_g           NUMERIC(8,1),
    saturated_fat_g NUMERIC(8,1),
    sodium_mg       NUMERIC(8,1),
    pdf_category    VARCHAR(40),                         -- SANDWICH, DAILY BOWL 등 (PDF 전용)
    PRIMARY KEY (menu_id, source)
);

CREATE TABLE menu_calorie_addons (
    menu_id         INT NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    addon_type_id   SMALLINT NOT NULL REFERENCES calorie_addon_types(id),
    kcal            NUMERIC(8,2) NOT NULL,
    PRIMARY KEY (menu_id, addon_type_id)
);

-- 메뉴별 드레싱 정책 (공식 default + enrichment 결과)
CREATE TABLE menu_dressing_policies (
    id              SERIAL PRIMARY KEY,
    menu_id         INT NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    dressing_id     SMALLINT REFERENCES dressings(id),
    policy_id       SMALLINT NOT NULL REFERENCES dressing_policies(id),
    source          VARCHAR(20) NOT NULL DEFAULT 'official'
        CHECK (source IN ('official', 'store', 'inferred')),
  UNIQUE (menu_id, policy_id, source)
);

CREATE TABLE dressing_nutrition (
    dressing_id     SMALLINT PRIMARY KEY REFERENCES dressings(id) ON DELETE CASCADE,
    weight_g        NUMERIC(8,1),
    calories_kcal   NUMERIC(8,1),
    carbs_g         NUMERIC(8,1),
    sugar_g         NUMERIC(8,1),
    protein_g       NUMERIC(8,1),
    fat_g           NUMERIC(8,1),
    saturated_fat_g NUMERIC(8,1),
    sodium_mg       NUMERIC(8,1)
);

-- ---------------------------------------------------------------------------
-- 3. Stores & sellable items (매장·채널)
-- ---------------------------------------------------------------------------

CREATE TABLE stores (
    id              VARCHAR(40) PRIMARY KEY,              -- passorder_sinchon, naver_mapo
    brand_id        SMALLINT NOT NULL REFERENCES brands(id),
    platform_id     SMALLINT NOT NULL REFERENCES platforms(id),
    name            VARCHAR(120) NOT NULL,
    external_business_id VARCHAR(40),
    external_item_id     VARCHAR(40),
    order_url       TEXT,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE store_categories (
    id              SERIAL PRIMARY KEY,
    store_id        VARCHAR(40) NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    name            VARCHAR(120) NOT NULL,
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    UNIQUE (store_id, name)
);

CREATE TABLE store_menu_items (
    id              BIGSERIAL PRIMARY KEY,
    store_id        VARCHAR(40) NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    store_category_id INT REFERENCES store_categories(id),
    menu_id         INT REFERENCES menus(id),             -- 공식 메뉴 매칭 (nullable)
    name            VARCHAR(200) NOT NULL,
    name_normalized VARCHAR(200) NOT NULL,
    description     TEXT,
    image_url       TEXT,
    is_set          BOOLEAN NOT NULL DEFAULT FALSE,
    is_store_exclusive BOOLEAN NOT NULL DEFAULT FALSE,
    stock_qty       INT,
    collected_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (store_id, name_normalized, is_set)
);

CREATE TABLE store_menu_item_badges (
    store_menu_item_id BIGINT NOT NULL REFERENCES store_menu_items(id) ON DELETE CASCADE,
    badge_text      VARCHAR(50) NOT NULL,
    PRIMARY KEY (store_menu_item_id, badge_text)
);

CREATE TABLE store_menu_prices (
    id              BIGSERIAL PRIMARY KEY,
    store_menu_item_id BIGINT NOT NULL REFERENCES store_menu_items(id) ON DELETE CASCADE,
    price_krw       INT NOT NULL,
    price_text      VARCHAR(30),
    valid_from      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (store_menu_item_id, valid_from)
);

CREATE TABLE store_external_ids (
    store_menu_item_id BIGINT NOT NULL REFERENCES store_menu_items(id) ON DELETE CASCADE,
    platform_id     SMALLINT NOT NULL REFERENCES platforms(id),
    external_key    VARCHAR(40) NOT NULL,                 -- naver_menu_id, passorder_uuid
    external_value  VARCHAR(80) NOT NULL,
    PRIMARY KEY (store_menu_item_id, platform_id, external_key)
);

-- 세트: 단품 메뉴 + 구성품
CREATE TABLE store_sets (
    store_menu_item_id BIGINT PRIMARY KEY REFERENCES store_menu_items(id) ON DELETE CASCADE,
    base_menu_id    INT REFERENCES menus(id),
    base_menu_name  VARCHAR(200) NOT NULL,
    base_price_krw  INT,
    set_premium_krw INT,
    total_price_krw INT NOT NULL
);

CREATE TABLE store_set_components (
    store_menu_item_id BIGINT NOT NULL REFERENCES store_sets(store_menu_item_id) ON DELETE CASCADE,
    ingredient_id   INT REFERENCES ingredients(id),
    component_name  VARCHAR(120) NOT NULL,                -- ingredient 미등록 시 이름만
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    PRIMARY KEY (store_menu_item_id, sort_order)
);

-- ---------------------------------------------------------------------------
-- 4. Store options (네이버/패스오더 옵션 그룹)
-- ---------------------------------------------------------------------------

CREATE TABLE store_option_groups (
    id              BIGSERIAL PRIMARY KEY,
    store_menu_item_id BIGINT NOT NULL REFERENCES store_menu_items(id) ON DELETE CASCADE,
    kind_id         SMALLINT NOT NULL REFERENCES option_group_kinds(id),
    name            VARCHAR(120) NOT NULL,
    is_required     BOOLEAN NOT NULL DEFAULT FALSE,
    max_select      SMALLINT,                             -- NULL = 단일/무제한
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    UNIQUE (store_menu_item_id, name)
);

CREATE TABLE store_option_choices (
    id              BIGSERIAL PRIMARY KEY,
    option_group_id BIGINT NOT NULL REFERENCES store_option_groups(id) ON DELETE CASCADE,
    name            VARCHAR(200) NOT NULL,
    price_delta_krw INT NOT NULL DEFAULT 0,
    dressing_id     SMALLINT REFERENCES dressings(id),     -- "크리미칠리 변경" 파싱 결과
    sort_order      SMALLINT NOT NULL DEFAULT 0,
    UNIQUE (option_group_id, name)
);

-- 매장별 드레싱 정책 (store description / naver_options 기반)
CREATE TABLE store_menu_dressing_policies (
    store_menu_item_id BIGINT NOT NULL REFERENCES store_menu_items(id) ON DELETE CASCADE,
    dressing_id     SMALLINT NOT NULL REFERENCES dressings(id),
    policy_id       SMALLINT NOT NULL REFERENCES dressing_policies(id),
    PRIMARY KEY (store_menu_item_id, policy_id)
);

-- ---------------------------------------------------------------------------
-- 5. Indexes
-- ---------------------------------------------------------------------------

CREATE INDEX idx_menus_brand ON menus(brand_id);
CREATE INDEX idx_menus_name_ko ON menus(name_ko);
CREATE INDEX idx_store_items_store ON store_menu_items(store_id);
CREATE INDEX idx_store_items_menu ON store_menu_items(menu_id);
CREATE INDEX idx_store_prices_item ON store_menu_prices(store_menu_item_id);
CREATE INDEX idx_option_groups_item ON store_option_groups(store_menu_item_id);
CREATE INDEX idx_menu_dressing_menu ON menu_dressing_policies(menu_id);

COMMIT;
