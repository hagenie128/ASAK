-- 재료 영양정보를 ing → ing_nutr(1:1)로 분리
-- menu_nutr 패턴과 동일. 멱등 적용은 apply_ing_nutr_split.py 권장.

CREATE TABLE IF NOT EXISTS `ing_nutr` (
    `id` BIGINT NOT NULL PRIMARY KEY,
    `ing_id` BIGINT NOT NULL,
    `serving_g` DECIMAL(8,2) NULL COMMENT '표준 제공량 g',
    `kcal` DECIMAL(8,2) NULL COMMENT '칼로리',
    `carb_g` DECIMAL(8,2) NULL COMMENT '탄수화물 g',
    `sugar_g` DECIMAL(8,2) NULL COMMENT '당류 g',
    `protein_g` DECIMAL(8,2) NULL COMMENT '단백질 g',
    `fat_g` DECIMAL(8,2) NULL COMMENT '지방 g',
    `saturated_fat_g` DECIMAL(8,2) NULL COMMENT '포화지방 g',
    `sodium_mg` DECIMAL(8,2) NULL COMMENT '나트륨 mg',
    `source_id` BIGINT NULL COMMENT '데이터 출처 코드 ID',
    UNIQUE KEY `uq_ing_nutr_ing_id` (`ing_id`),
    CONSTRAINT `fk_ing_nutr_ing_id` FOREIGN KEY (`ing_id`) REFERENCES `ing` (`id`),
    CONSTRAINT `fk_ing_nutr_source_id` FOREIGN KEY (`source_id`) REFERENCES `common_code` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 기존 ing 영양 컬럼이 있을 때만 수동으로 이관·드롭한다.
-- INSERT INTO ing_nutr (id, ing_id, serving_g, kcal, carb_g, sugar_g, protein_g, fat_g, saturated_fat_g, sodium_mg)
-- SELECT id, id, serving_g, kcal, carb_g, sugar_g, protein_g, fat_g, saturated_fat_g, sodium_mg
-- FROM ing
-- WHERE serving_g IS NOT NULL OR kcal IS NOT NULL OR carb_g IS NOT NULL
--    OR sugar_g IS NOT NULL OR protein_g IS NOT NULL OR fat_g IS NOT NULL
--    OR saturated_fat_g IS NOT NULL OR sodium_mg IS NOT NULL;
--
-- ALTER TABLE ing
--   DROP COLUMN serving_g,
--   DROP COLUMN kcal,
--   DROP COLUMN carb_g,
--   DROP COLUMN sugar_g,
--   DROP COLUMN protein_g,
--   DROP COLUMN fat_g,
--   DROP COLUMN saturated_fat_g,
--   DROP COLUMN sodium_mg;
