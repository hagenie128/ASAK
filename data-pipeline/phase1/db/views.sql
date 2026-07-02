-- Convenience views for app/query layer

CREATE OR REPLACE VIEW v_menu_with_dressing AS
SELECT
    m.id,
    m.name_ko,
    m.name_en,
    oc.name AS category_name,
    nc.name AS nav_category_name,
    m.menu_type,
    MAX(CASE WHEN dp.code = 'recommended' THEN d.name END) AS recommended_dressing,
    MAX(CASE WHEN dp.code = 'included' THEN d.name END) AS included_dressing,
    MAX(CASE WHEN dp.code = 'default' THEN d.name END) AS default_dressing
FROM menus m
LEFT JOIN menu_categories oc ON oc.id = m.category_id
LEFT JOIN menu_categories nc ON nc.id = m.nav_category_id
LEFT JOIN menu_dressing_policies mdp ON mdp.menu_id = m.id
LEFT JOIN dressings d ON d.id = mdp.dressing_id
LEFT JOIN dressing_policies dp ON dp.id = mdp.policy_id
GROUP BY m.id, m.name_ko, m.name_en, oc.name, nc.name, m.menu_type;

CREATE OR REPLACE VIEW v_store_menu_current_price AS
SELECT
    s.id AS store_id,
    s.name AS store_name,
    p.code AS platform,
    smi.id AS store_menu_item_id,
    smi.name,
    smi.menu_id,
    m.name_ko AS official_menu_name,
    sp.price_krw,
    sp.price_text,
    sp.valid_from
FROM store_menu_items smi
JOIN stores s ON s.id = smi.store_id
JOIN platforms p ON p.id = s.platform_id
LEFT JOIN menus m ON m.id = smi.menu_id
LEFT JOIN LATERAL (
    SELECT price_krw, price_text, valid_from
    FROM store_menu_prices
    WHERE store_menu_item_id = smi.id
    ORDER BY valid_from DESC
    LIMIT 1
) sp ON TRUE;

CREATE OR REPLACE VIEW v_menu_nutrition_compare AS
SELECT
    m.id,
    m.name_ko,
    w.calories_kcal AS web_kcal,
    p.calories_kcal AS pdf_kcal,
    w.sodium_mg AS web_sodium_mg,
    p.sodium_mg AS pdf_sodium_mg
FROM menus m
LEFT JOIN menu_nutrition w ON w.menu_id = m.id AND w.source = 'web'
LEFT JOIN menu_nutrition p ON p.menu_id = m.id AND p.source = 'pdf';
