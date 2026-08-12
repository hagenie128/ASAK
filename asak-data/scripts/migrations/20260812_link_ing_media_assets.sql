-- 재료(ing)에 아이콘/사진 자산 연결
-- 동일 콘텐츠(SVG 아이콘, 사진)는 media_asset에 한 번만 저장하고
-- 여러 ing가 같은 자산을 공유 참조한다 (중복 업로드/중복 행 방지).
-- 멱등 적용은 apply_link_ing_media_assets.py 권장.

ALTER TABLE `ing`
  ADD COLUMN IF NOT EXISTS `icon_asset_id` BIGINT NULL COMMENT 'media_asset FK (아이콘)' AFTER `protein_g`;

ALTER TABLE `ing`
  ADD COLUMN IF NOT EXISTS `photo_asset_id` BIGINT NULL COMMENT 'media_asset FK (사진)' AFTER `icon_asset_id`;

ALTER TABLE `ing`
  ADD CONSTRAINT `fk_ing_icon_asset_id`
    FOREIGN KEY (`icon_asset_id`) REFERENCES `media_asset` (`id`);

ALTER TABLE `ing`
  ADD CONSTRAINT `fk_ing_photo_asset_id`
    FOREIGN KEY (`photo_asset_id`) REFERENCES `media_asset` (`id`);
