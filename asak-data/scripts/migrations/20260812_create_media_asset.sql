-- 공용 미디어 자산 테이블 (menu/opt/ing 이미지 관리 2단계)
-- Cloudinary 등 외부 저장소에 올라간 파일의 메타데이터를 저장하고,
-- menu.image_asset_id로 참조한다. menu.image_url은 조회 편의를 위해
-- media_asset.url 값으로 함께 동기화한다(비정규화).
-- 저장소 종류(provider)는 이 프로젝트의 기존 컨벤션(common_code)을 따라
-- 새 code_group 'MEDIA_PROVIDER' 아래 common_code로 관리한다.
-- 멱등 적용은 apply_create_media_asset.py 권장.

INSERT INTO `code_group` (`group_code`, `name`)
SELECT 'MEDIA_PROVIDER', '미디어 저장소'
WHERE NOT EXISTS (SELECT 1 FROM `code_group` WHERE `group_code` = 'MEDIA_PROVIDER');

INSERT INTO `common_code` (`code_grp_id`, `code`, `name`, `sort_no`, `active`)
SELECT g.id, 'CLOUDINARY', 'Cloudinary', 1, 1
FROM `code_group` g
WHERE g.group_code = 'MEDIA_PROVIDER'
  AND NOT EXISTS (
    SELECT 1 FROM `common_code` c WHERE c.code_grp_id = g.id AND c.code = 'CLOUDINARY'
  );

CREATE TABLE IF NOT EXISTS `media_asset` (
    `id` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `provider_id` BIGINT NOT NULL COMMENT 'common_code(MEDIA_PROVIDER) FK',
    `public_id` VARCHAR(255) NOT NULL COMMENT '저장소 내 고유 식별자 (예: Cloudinary public_id)',
    `asset_folder` VARCHAR(255) NULL COMMENT '저장소 내 폴더 경로',
    `url` VARCHAR(500) NOT NULL COMMENT '공개 URL',
    `format` VARCHAR(20) NULL COMMENT '파일 포맷 (png, svg 등)',
    `width` INT NULL,
    `height` INT NULL,
    `bytes` INT NULL,
    `uploaded_at` TIMESTAMP NULL COMMENT '저장소 업로드 시각',
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '이 행이 DB에 생성된 시각',
    `deleted_at` TIMESTAMP NULL,
    UNIQUE KEY `uq_media_asset_provider_public_id` (`provider_id`, `public_id`),
    CONSTRAINT `fk_media_asset_provider_id` FOREIGN KEY (`provider_id`) REFERENCES `common_code` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `menu`
  ADD COLUMN IF NOT EXISTS `image_asset_id` BIGINT NULL COMMENT 'media_asset FK' AFTER `image_url`;

ALTER TABLE `menu`
  ADD CONSTRAINT `fk_menu_image_asset_id`
    FOREIGN KEY (`image_asset_id`) REFERENCES `media_asset` (`id`);
