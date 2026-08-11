-- nutrition_260715.pdf 기준 누락 영양 컬럼 추가
-- 재료 영양은 ing_nutr로 분리됨. 신규 환경은 20260811_split_ing_nutrition.sql 참고.
-- 이미 있으면 컬럼이면 Duplicate column 오류가 날 수 있으니, apply_nutrition_schema.py 사용을 권장합니다.

ALTER TABLE ing_nutr ADD COLUMN serving_g DECIMAL(8,2) NULL COMMENT '표준 제공량 g';
ALTER TABLE ing_nutr ADD COLUMN carb_g DECIMAL(8,2) NULL COMMENT '탄수화물 g';
ALTER TABLE ing_nutr ADD COLUMN sugar_g DECIMAL(8,2) NULL COMMENT '당류 g';
ALTER TABLE ing_nutr ADD COLUMN fat_g DECIMAL(8,2) NULL COMMENT '지방 g';
ALTER TABLE ing_nutr ADD COLUMN saturated_fat_g DECIMAL(8,2) NULL COMMENT '포화지방 g';
ALTER TABLE ing_nutr ADD COLUMN sodium_mg DECIMAL(8,2) NULL COMMENT '나트륨 mg';

ALTER TABLE menu_nutr ADD COLUMN serving_g DECIMAL(8,2) NULL COMMENT '표준 제공량 g';
ALTER TABLE menu_nutr ADD COLUMN sugar_g DECIMAL(8,2) NULL COMMENT '당류 g';
ALTER TABLE menu_nutr ADD COLUMN saturated_fat_g DECIMAL(8,2) NULL COMMENT '포화지방 g';
