-- ing_nutr로 분리됐던 protein_g, kcal을 ing 테이블에 다시 추가
-- (20260811_split_ing_nutrition.sql의 부분 되돌리기: protein_g, kcal만 복원)
-- 멱등 적용은 apply_restore_ing_protein_kcal.py 권장.

ALTER TABLE `ing`
  ADD COLUMN IF NOT EXISTS `kcal` DECIMAL(8,2) NULL COMMENT '칼로리',
  ADD COLUMN IF NOT EXISTS `protein_g` DECIMAL(8,2) NULL COMMENT '단백질 g';

UPDATE `ing` i
JOIN `ing_nutr` n ON n.`ing_id` = i.`id`
SET i.`kcal` = n.`kcal`,
    i.`protein_g` = n.`protein_g`;
