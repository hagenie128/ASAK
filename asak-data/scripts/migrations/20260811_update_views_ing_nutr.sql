-- ing 영양 컬럼 → ing_nutr 분리 이후 영향 뷰 재생성
-- 영향 뷰: vw_menu_opt_policy_json (extra_kcal / protein_g)
-- 적용일: 2026-08-11

CREATE OR REPLACE VIEW `vw_menu_opt_policy_json` AS
SELECT `x`.`menu_id` AS `menu_id`,
       `x`.`option_group_id` AS `option_group_id`,
       `x`.`name` AS `name`,
       `x`.`policy_name` AS `policy_name`,
       `x`.`group_type` AS `group_type`,
       `x`.`select_type` AS `select_type`,
       `x`.`min_select` AS `min_select`,
       `x`.`max_select` AS `max_select`,
       `x`.`sort_order` AS `sort_order`,
       `x`.`is_required` AS `is_required`,
       json_arrayagg(
           json_object(
               'optionItemId', `x`.`option_item_id`,
               'ingredientId', `x`.`ingredient_id`,
               'name', `x`.`item_name`,
               'extraPrice', `x`.`extra_price`,
               'originalPrice', `x`.`original_price`,
               'servingAmount', `x`.`serving_amount`,
               'servingUnit', `x`.`serving_unit`,
               'iconUrl', `x`.`icon_url`,
               'colorHex', `x`.`color_hex`,
               'isSoldOut', `x`.`is_sold_out`,
               'extraKcal', `x`.`extra_kcal`,
               'proteinG', `x`.`protein_g`,
               'isRecommended', `x`.`is_recommended`,
               'isDefault', `x`.`is_default`
           )
       ) AS `items`
FROM (
    SELECT `mop`.`menu_id` AS `menu_id`,
           `op`.`opt_group_id` AS `option_group_id`,
           `og`.`name` AS `name`,
           `op`.`name` AS `policy_name`,
           `cg_group`.`code` AS `group_type`,
           (CASE WHEN (`og`.`max_select` = 1) THEN 'SINGLE' ELSE 'MULTI' END) AS `select_type`,
           `og`.`min_select` AS `min_select`,
           `og`.`max_select` AS `max_select`,
           `mop`.`sort_no` AS `sort_order`,
           `mop`.`required` AS `is_required`,
           `oi`.`id` AS `option_item_id`,
           `oi`.`ing_id` AS `ingredient_id`,
           `oi`.`name` AS `item_name`,
           `oi`.`add_price` AS `extra_price`,
           `oi`.`list_price` AS `original_price`,
           `oi`.`amount` AS `serving_amount`,
           `cc_unit`.`code` AS `serving_unit`,
           `oi`.`icon_url` AS `icon_url`,
           `oi`.`color_hex` AS `color_hex`,
           `oi`.`sold_out` AS `is_sold_out`,
           `n`.`kcal` AS `extra_kcal`,
           `n`.`protein_g` AS `protein_g`,
           coalesce(`moo`.`recommended`, `opi`.`recommended`, 0) AS `is_recommended`,
           coalesce(`moo`.`is_default`, `opi`.`is_default`, 0) AS `is_default`,
           coalesce(`moo`.`sort_no`, `opi`.`sort_no`, 9999) AS `item_sort_no`
    FROM `menu_opt_policy` `mop`
    JOIN `opt_policy` `op` ON `op`.`id` = `mop`.`policy_id`
    JOIN `opt_group` `og` ON `og`.`id` = `op`.`opt_group_id`
    LEFT JOIN `common_code` `cg_group` ON `cg_group`.`id` = `og`.`group_type_id`
    JOIN `opt_policy_item` `opi` ON `opi`.`policy_id` = `op`.`id`
    JOIN `opt_item` `oi` ON `oi`.`id` = `opi`.`opt_item_id`
    LEFT JOIN `ing` `i` ON `i`.`id` = `oi`.`ing_id`
    LEFT JOIN `ing_nutr` `n` ON `n`.`ing_id` = `i`.`id`
    LEFT JOIN `menu_opt_override` `moo`
        ON `moo`.`menu_id` = `mop`.`menu_id`
       AND `moo`.`opt_item_id` = `oi`.`id`
    LEFT JOIN `common_code` `cc_unit` ON `cc_unit`.`id` = `oi`.`unit_id`
    ORDER BY `mop`.`menu_id`,
             `mop`.`sort_no`,
             `op`.`opt_group_id`,
             coalesce(`moo`.`sort_no`, `opi`.`sort_no`, 9999),
             `oi`.`id`
) `x`
GROUP BY `x`.`menu_id`,
         `x`.`option_group_id`,
         `x`.`name`,
         `x`.`policy_name`,
         `x`.`group_type`,
         `x`.`select_type`,
         `x`.`min_select`,
         `x`.`max_select`,
         `x`.`sort_order`,
         `x`.`is_required`;
