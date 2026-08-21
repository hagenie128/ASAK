-- 품절 관리 API의 공통 카탈로그 View에 화면 이미지 URL을 포함한다.
-- 읽기는 vw_soldout_catalog, 쓰기는 menu/ing/opt_item.sold_out을 계속 사용한다.
CREATE OR REPLACE ALGORITHM = UNDEFINED VIEW `vw_soldout_catalog` AS
SELECT 'MENU' AS `target_type`,
       `m`.`id` AS `target_id`,
       `m`.`name` AS `name`,
       `c`.`name` AS `category`,
       `m`.`sold_out` AS `is_sold_out`,
       `m`.`price` AS `price`,
       `ma`.`url` AS `image_url`
FROM `menu` `m`
JOIN `category` `c` ON `c`.`id` = `m`.`cat_id`
LEFT JOIN `media_asset` `ma`
  ON `ma`.`id` = `m`.`image_asset_id` AND `ma`.`deleted_at` IS NULL
UNION ALL
SELECT 'INGREDIENT' AS `target_type`,
       `i`.`id` AS `target_id`,
       `i`.`name` AS `name`,
       `rt`.`name` AS `category`,
       `i`.`sold_out` AS `is_sold_out`,
       NULL AS `price`,
       `ia`.`url` AS `image_url`
FROM `ing` `i`
JOIN `common_code` `rt` ON `rt`.`id` = `i`.`type_id`
LEFT JOIN `media_asset` `ia`
  ON `ia`.`id` = `i`.`photo_asset_id` AND `ia`.`deleted_at` IS NULL
UNION ALL
SELECT 'OPTION_ITEM' AS `target_type`,
       `oi`.`id` AS `target_id`,
       `oi`.`name` AS `name`,
       `og`.`name` AS `category`,
       `oi`.`sold_out` AS `is_sold_out`,
       `oi`.`add_price` AS `price`,
       `oi`.`icon_url` AS `image_url`
FROM `opt_item` `oi`
JOIN `opt_group` `og` ON `og`.`id` = `oi`.`opt_group_id`;
