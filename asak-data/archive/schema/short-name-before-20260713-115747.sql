-- ASAK schema snapshot before short-name migration

DROP TABLE IF EXISTS `allergen`;
CREATE TABLE `allergen` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=237 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `code_group`;
CREATE TABLE `code_group` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_code` (`group_code`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `common_code`;
CREATE TABLE `common_code` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code_group_id` bigint NOT NULL,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_common_code_group_code` (`code_group_id`,`code`),
  CONSTRAINT `fk_common_code_group` FOREIGN KEY (`code_group_id`) REFERENCES `code_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `ingredient`;
CREATE TABLE `ingredient` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type_id` bigint NOT NULL,
  `kcal` decimal(8,2) DEFAULT NULL,
  `protein_g` decimal(8,2) DEFAULT NULL,
  `is_sold_out` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `fk_ingredient_type` (`type_id`),
  CONSTRAINT `fk_ingredient_type` FOREIGN KEY (`type_id`) REFERENCES `common_code` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9816 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `ingredient_allergen`;
CREATE TABLE `ingredient_allergen` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ingredient_id` bigint NOT NULL,
  `allergen_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_ingredient_allergen` (`ingredient_id`,`allergen_id`),
  KEY `fk_ingredient_allergen_allergen` (`allergen_id`),
  CONSTRAINT `fk_ingredient_allergen_allergen` FOREIGN KEY (`allergen_id`) REFERENCES `allergen` (`id`),
  CONSTRAINT `fk_ingredient_allergen_ingredient` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=231 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `item_exclusion`;
CREATE TABLE `item_exclusion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_item_id` bigint NOT NULL,
  `ingredient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_item_exclusion` (`order_item_id`,`ingredient_id`),
  KEY `fk_item_exclusion_ingredient` (`ingredient_id`),
  CONSTRAINT `fk_item_exclusion_ingredient` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`id`),
  CONSTRAINT `fk_item_exclusion_order_item` FOREIGN KEY (`order_item_id`) REFERENCES `order_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category_id` bigint NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` int NOT NULL DEFAULT '0',
  `image_url` text COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `is_sold_out` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_menu_category` (`category_id`),
  CONSTRAINT `fk_menu_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10768 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `menu_ingredient`;
CREATE TABLE `menu_ingredient` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_id` bigint NOT NULL,
  `ingredient_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  `quantity` decimal(8,2) DEFAULT NULL,
  `unit_id` bigint DEFAULT NULL,
  `is_default` tinyint(1) NOT NULL DEFAULT '1',
  `can_remove` tinyint(1) NOT NULL DEFAULT '1',
  `sort_order` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_menu_ingredient_role` (`menu_id`,`ingredient_id`,`role_id`),
  KEY `fk_menu_ingredient_ingredient` (`ingredient_id`),
  KEY `fk_menu_ingredient_role` (`role_id`),
  KEY `fk_menu_ingredient_unit` (`unit_id`),
  CONSTRAINT `fk_menu_ingredient_ingredient` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`id`),
  CONSTRAINT `fk_menu_ingredient_menu` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`),
  CONSTRAINT `fk_menu_ingredient_role` FOREIGN KEY (`role_id`) REFERENCES `common_code` (`id`),
  CONSTRAINT `fk_menu_ingredient_unit` FOREIGN KEY (`unit_id`) REFERENCES `common_code` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10770 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `menu_nutrition`;
CREATE TABLE `menu_nutrition` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_id` bigint NOT NULL,
  `kcal` decimal(8,2) DEFAULT NULL,
  `protein_g` decimal(8,2) DEFAULT NULL,
  `carb_g` decimal(8,2) DEFAULT NULL,
  `fat_g` decimal(8,2) DEFAULT NULL,
  `sodium_mg` decimal(8,2) DEFAULT NULL,
  `source_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `menu_id` (`menu_id`),
  KEY `fk_menu_nutrition_source` (`source_id`),
  CONSTRAINT `fk_menu_nutrition_menu` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`),
  CONSTRAINT `fk_menu_nutrition_source` FOREIGN KEY (`source_id`) REFERENCES `common_code` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10769 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `menu_option_group_legacy_20260710`;
CREATE TABLE `menu_option_group_legacy_20260710` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_id` bigint NOT NULL,
  `option_group_id` bigint NOT NULL,
  `sort_order` int NOT NULL DEFAULT '0',
  `is_required` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_menu_option_group` (`menu_id`,`option_group_id`),
  KEY `fk_menu_option_group_group` (`option_group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10771 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `menu_option_legacy_20260710`;
CREATE TABLE `menu_option_legacy_20260710` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_id` bigint NOT NULL,
  `option_item_id` bigint NOT NULL,
  `is_recommended` tinyint(1) NOT NULL DEFAULT '0',
  `is_default` tinyint(1) NOT NULL DEFAULT '0',
  `sort_order` int NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_menu_option` (`menu_id`,`option_item_id`),
  KEY `fk_menu_option_item` (`option_item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10828 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `menu_option_override`;
CREATE TABLE `menu_option_override` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_id` bigint NOT NULL,
  `option_item_id` bigint NOT NULL,
  `is_recommended` tinyint(1) DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT NULL,
  `sort_order` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `note` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_menu_option_override` (`menu_id`,`option_item_id`),
  KEY `fk_menu_option_override_item` (`option_item_id`),
  CONSTRAINT `fk_menu_option_override_item` FOREIGN KEY (`option_item_id`) REFERENCES `option_item` (`id`),
  CONSTRAINT `fk_menu_option_override_menu` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `menu_option_policy`;
CREATE TABLE `menu_option_policy` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_id` bigint NOT NULL,
  `policy_id` bigint NOT NULL,
  `sort_order` int NOT NULL DEFAULT '0',
  `is_required` tinyint(1) NOT NULL DEFAULT '0',
  `priority` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_menu_option_policy` (`menu_id`,`policy_id`),
  KEY `fk_menu_option_policy_policy` (`policy_id`),
  CONSTRAINT `fk_menu_option_policy_menu` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`),
  CONSTRAINT `fk_menu_option_policy_policy` FOREIGN KEY (`policy_id`) REFERENCES `option_policy` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=468 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `menu_tag`;
CREATE TABLE `menu_tag` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_id` bigint NOT NULL,
  `tag_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_menu_tag` (`menu_id`,`tag_id`),
  KEY `fk_menu_tag_tag` (`tag_id`),
  CONSTRAINT `fk_menu_tag_menu` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`),
  CONSTRAINT `fk_menu_tag_tag` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6685 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `option_group`;
CREATE TABLE `option_group` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `group_type_id` bigint NOT NULL,
  `min_select` int NOT NULL DEFAULT '0',
  `max_select` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `fk_option_group_type` (`group_type_id`),
  CONSTRAINT `fk_option_group_type` FOREIGN KEY (`group_type_id`) REFERENCES `common_code` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=247 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `option_item`;
CREATE TABLE `option_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `option_group_id` bigint NOT NULL,
  `ingredient_id` bigint DEFAULT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `extra_price` int NOT NULL DEFAULT '0',
  `original_price` int DEFAULT NULL,
  `amount` decimal(8,2) DEFAULT NULL,
  `unit_id` bigint DEFAULT NULL,
  `icon_url` text COLLATE utf8mb4_unicode_ci,
  `color_hex` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_sold_out` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_option_item_group` (`option_group_id`),
  KEY `fk_option_item_ingredient` (`ingredient_id`),
  KEY `fk_option_item_unit` (`unit_id`),
  CONSTRAINT `fk_option_item_group` FOREIGN KEY (`option_group_id`) REFERENCES `option_group` (`id`),
  CONSTRAINT `fk_option_item_ingredient` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`id`),
  CONSTRAINT `fk_option_item_unit` FOREIGN KEY (`unit_id`) REFERENCES `common_code` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9818 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `option_item_component`;
CREATE TABLE `option_item_component` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `option_item_id` bigint NOT NULL,
  `ingredient_id` bigint DEFAULT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` decimal(8,2) DEFAULT NULL,
  `unit_id` bigint DEFAULT NULL,
  `sort_order` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_option_item_component_item` (`option_item_id`),
  KEY `fk_option_item_component_ingredient` (`ingredient_id`),
  KEY `fk_option_item_component_unit` (`unit_id`),
  CONSTRAINT `fk_option_item_component_ingredient` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`id`),
  CONSTRAINT `fk_option_item_component_item` FOREIGN KEY (`option_item_id`) REFERENCES `option_item` (`id`),
  CONSTRAINT `fk_option_item_component_unit` FOREIGN KEY (`unit_id`) REFERENCES `common_code` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `option_policy`;
CREATE TABLE `option_policy` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `policy_key` char(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `option_group_id` bigint NOT NULL,
  `sort_order` int NOT NULL DEFAULT '0',
  `is_required` tinyint(1) NOT NULL DEFAULT '0',
  `min_select` int NOT NULL DEFAULT '0',
  `max_select` int NOT NULL DEFAULT '1',
  `item_count` int NOT NULL DEFAULT '0',
  `menu_count` int NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `policy_key` (`policy_key`),
  KEY `fk_option_policy_group` (`option_group_id`),
  CONSTRAINT `fk_option_policy_group` FOREIGN KEY (`option_group_id`) REFERENCES `option_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `option_policy_item`;
CREATE TABLE `option_policy_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `policy_id` bigint NOT NULL,
  `option_item_id` bigint NOT NULL,
  `is_recommended` tinyint(1) NOT NULL DEFAULT '0',
  `is_default` tinyint(1) NOT NULL DEFAULT '0',
  `sort_order` int NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_option_policy_item` (`policy_id`,`option_item_id`),
  KEY `fk_option_policy_item_item` (`option_item_id`),
  CONSTRAINT `fk_option_policy_item_item` FOREIGN KEY (`option_item_id`) REFERENCES `option_item` (`id`),
  CONSTRAINT `fk_option_policy_item_policy` FOREIGN KEY (`policy_id`) REFERENCES `option_policy` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=735 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `order_item`;
CREATE TABLE `order_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint NOT NULL,
  `menu_id` bigint NOT NULL,
  `quantity` int NOT NULL DEFAULT '1',
  `price` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_order_item_order` (`order_id`),
  KEY `fk_order_item_menu` (`menu_id`),
  CONSTRAINT `fk_order_item_menu` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`),
  CONSTRAINT `fk_order_item_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `order_item_option`;
CREATE TABLE `order_item_option` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_item_id` bigint NOT NULL,
  `option_item_id` bigint NOT NULL,
  `quantity` int NOT NULL DEFAULT '1',
  `price` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_order_item_option` (`order_item_id`,`option_item_id`),
  KEY `fk_order_item_option_option` (`option_item_id`),
  CONSTRAINT `fk_order_item_option_item` FOREIGN KEY (`order_item_id`) REFERENCES `order_item` (`id`),
  CONSTRAINT `fk_order_item_option_option` FOREIGN KEY (`option_item_id`) REFERENCES `option_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_type_id` bigint NOT NULL,
  `status_id` bigint NOT NULL,
  `total_price` int NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no` (`order_no`),
  KEY `fk_orders_type` (`order_type_id`),
  KEY `fk_orders_status` (`status_id`),
  CONSTRAINT `fk_orders_status` FOREIGN KEY (`status_id`) REFERENCES `common_code` (`id`),
  CONSTRAINT `fk_orders_type` FOREIGN KEY (`order_type_id`) REFERENCES `common_code` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `payment`;
CREATE TABLE `payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint NOT NULL,
  `method_id` bigint NOT NULL,
  `status_id` bigint NOT NULL,
  `amount` int NOT NULL DEFAULT '0',
  `paid_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  KEY `fk_payment_method` (`method_id`),
  KEY `fk_payment_status` (`status_id`),
  CONSTRAINT `fk_payment_method` FOREIGN KEY (`method_id`) REFERENCES `common_code` (`id`),
  CONSTRAINT `fk_payment_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `fk_payment_status` FOREIGN KEY (`status_id`) REFERENCES `common_code` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `payment_method_config`;
CREATE TABLE `payment_method_config` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `method_id` bigint NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `sort_order` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `method_id` (`method_id`),
  CONSTRAINT `fk_payment_method_config_method` FOREIGN KEY (`method_id`) REFERENCES `common_code` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10829 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color_hex` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=240 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
