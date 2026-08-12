#!/usr/bin/env python3
"""Create media_asset table and link menu images to their Cloudinary assets.

Matches local ASAK-Admin/public/assets/menu/{menu_id}.png files to Cloudinary
resources in the asak/menus folder by (width, height, bytes) -- exact enough to
be unambiguous for the current 50-image set. Idempotent: safe to re-run.
"""

from __future__ import annotations

import base64
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import pymysql


def to_mysql_datetime(iso_ts: str | None) -> str | None:
    if not iso_ts:
        return None
    dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00")).astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

LOCAL_MENU_DIR = Path(r"C:\ASAK-workspace\ASAK-Admin\public\assets\menu")
CLOUDINARY_FOLDER = "asak/menus"


def parse_jdbc_url(url: str) -> tuple[str, int, str]:
    raw = url.replace("jdbc:mysql://", "")
    host_port, _, rest = raw.partition("/")
    db = rest.split("?", 1)[0]
    if ":" in host_port:
        host, port_s = host_port.split(":", 1)
        port = int(port_s)
    else:
        host, port = host_port, 3306
    return host, port, db


def fetch_cloudinary_resources(cloud_name: str, api_key: str, api_secret: str) -> list[dict]:
    resources: list[dict] = []
    next_cursor = None
    auth = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()
    while True:
        url = f"https://api.cloudinary.com/v1_1/{cloud_name}/resources/image/upload?max_results=500"
        if next_cursor:
            url += f"&next_cursor={next_cursor}"
        req = urllib.request.Request(url, headers={"Authorization": f"Basic {auth}"})
        with urllib.request.urlopen(req) as resp:
            data = json.load(resp)
        resources.extend(data.get("resources", []))
        next_cursor = data.get("next_cursor")
        if not next_cursor:
            break
    return resources


def local_menu_files() -> dict[int, tuple[int, int, int]]:
    from PIL import Image

    out = {}
    for path in LOCAL_MENU_DIR.glob("*.png"):
        if not path.stem.isdigit():
            continue
        im = Image.open(path)
        out[int(path.stem)] = (im.size[0], im.size[1], path.stat().st_size)
    return out


def build_menu_id_to_asset(local: dict[int, tuple[int, int, int]], cloud: list[dict]) -> dict[int, dict]:
    menu_res = [r for r in cloud if r.get("asset_folder") == CLOUDINARY_FOLDER]
    by_dim_bytes = {(r["width"], r["height"], r["bytes"]): r for r in menu_res}

    mapping = {}
    unmatched = []
    for menu_id, (w, h, sz) in local.items():
        r = by_dim_bytes.get((w, h, sz))
        if r is None:
            unmatched.append(menu_id)
            continue
        mapping[menu_id] = r
    if unmatched:
        print(f"warning: no exact (w,h,bytes) match for menu ids: {unmatched}", file=sys.stderr)
    return mapping


def table_exists(cur, table: str) -> bool:
    cur.execute(
        """
        SELECT 1 FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s
        """,
        (table,),
    )
    return cur.fetchone() is not None


def column_exists(cur, table: str, column: str) -> bool:
    cur.execute(
        """
        SELECT 1 FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = %s
        """,
        (table, column),
    )
    return cur.fetchone() is not None


def constraint_exists(cur, name: str) -> bool:
    cur.execute(
        """
        SELECT 1 FROM information_schema.TABLE_CONSTRAINTS
        WHERE TABLE_SCHEMA = DATABASE() AND CONSTRAINT_NAME = %s
        """,
        (name,),
    )
    return cur.fetchone() is not None


def ensure_media_provider_code(cur) -> int:
    cur.execute("SELECT id FROM `code_group` WHERE `group_code` = 'MEDIA_PROVIDER'")
    row = cur.fetchone()
    if row is None:
        cur.execute(
            "INSERT INTO `code_group` (`group_code`, `name`) VALUES ('MEDIA_PROVIDER', %s)",
            ("미디어 저장소",),
        )
        group_id = cur.lastrowid
        print("added code_group MEDIA_PROVIDER")
    else:
        group_id = row[0]

    cur.execute(
        "SELECT id FROM `common_code` WHERE `code_grp_id` = %s AND `code` = 'CLOUDINARY'",
        (group_id,),
    )
    row = cur.fetchone()
    if row is None:
        cur.execute(
            """
            INSERT INTO `common_code` (`code_grp_id`, `code`, `name`, `sort_no`, `active`)
            VALUES (%s, 'CLOUDINARY', %s, 1, 1)
            """,
            (group_id, "Cloudinary"),
        )
        provider_id = cur.lastrowid
        print("added common_code CLOUDINARY")
    else:
        provider_id = row[0]
    return provider_id


def ensure_schema(cur) -> int:
    if table_exists(cur, "media_asset") and not column_exists(cur, "media_asset", "provider_id"):
        cur.execute("SELECT COUNT(*) FROM `media_asset`")
        if cur.fetchone()[0] == 0:
            if constraint_exists(cur, "fk_menu_image_asset_id"):
                cur.execute(
                    "ALTER TABLE `menu` DROP FOREIGN KEY `fk_menu_image_asset_id`"
                )
                print("dropped stale fk_menu_image_asset_id")
            cur.execute("DROP TABLE `media_asset`")
            print("dropped stale empty media_asset (pre provider_id schema)")
        else:
            raise RuntimeError(
                "media_asset exists with legacy 'provider' column and has data; "
                "manual migration required"
            )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS `media_asset` (
            `id` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `provider_id` BIGINT NOT NULL,
            `public_id` VARCHAR(255) NOT NULL,
            `asset_folder` VARCHAR(255) NULL,
            `url` VARCHAR(500) NOT NULL,
            `format` VARCHAR(20) NULL,
            `width` INT NULL,
            `height` INT NULL,
            `bytes` INT NULL,
            `uploaded_at` TIMESTAMP NULL,
            `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `deleted_at` TIMESTAMP NULL,
            UNIQUE KEY `uq_media_asset_provider_public_id` (`provider_id`, `public_id`),
            CONSTRAINT `fk_media_asset_provider_id`
                FOREIGN KEY (`provider_id`) REFERENCES `common_code` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    )
    print("ok table media_asset")

    provider_id = ensure_media_provider_code(cur)

    if not column_exists(cur, "menu", "image_asset_id"):
        cur.execute(
            "ALTER TABLE `menu` ADD COLUMN `image_asset_id` BIGINT NULL AFTER `image_url`"
        )
        print("added menu.image_asset_id")
    else:
        print("menu.image_asset_id already present")

    if not constraint_exists(cur, "fk_menu_image_asset_id"):
        cur.execute(
            """
            ALTER TABLE `menu`
              ADD CONSTRAINT `fk_menu_image_asset_id`
                FOREIGN KEY (`image_asset_id`) REFERENCES `media_asset` (`id`)
            """
        )
        print("added fk_menu_image_asset_id")
    else:
        print("fk_menu_image_asset_id already present")

    return provider_id


def upsert_media_assets(cur, provider_id: int, mapping: dict[int, dict]) -> dict[int, int]:
    menu_id_to_asset_row_id: dict[int, int] = {}
    for menu_id, r in mapping.items():
        cur.execute(
            """
            INSERT INTO `media_asset`
                (`provider_id`, `public_id`, `asset_folder`, `url`, `format`, `width`, `height`, `bytes`, `uploaded_at`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                `asset_folder` = VALUES(`asset_folder`),
                `url` = VALUES(`url`),
                `format` = VALUES(`format`),
                `width` = VALUES(`width`),
                `height` = VALUES(`height`),
                `bytes` = VALUES(`bytes`),
                `uploaded_at` = VALUES(`uploaded_at`),
                `id` = LAST_INSERT_ID(`id`)
            """,
            (
                provider_id,
                r["public_id"],
                r.get("asset_folder"),
                r["secure_url"],
                r.get("format"),
                r.get("width"),
                r.get("height"),
                r.get("bytes"),
                to_mysql_datetime(r.get("created_at")),
            ),
        )
        menu_id_to_asset_row_id[menu_id] = cur.lastrowid
    return menu_id_to_asset_row_id


def link_menu_rows(cur, menu_id_to_asset_row_id: dict[int, int], mapping: dict[int, dict]) -> int:
    updated = 0
    for menu_id, asset_row_id in menu_id_to_asset_row_id.items():
        url = mapping[menu_id]["secure_url"]
        cur.execute(
            "UPDATE `menu` SET `image_asset_id` = %s, `image_url` = %s WHERE `id` = %s",
            (asset_row_id, url, menu_id),
        )
        updated += cur.rowcount
    return updated


def main() -> int:
    db_url = os.environ.get("DB_URL")
    db_user = os.environ.get("DB_USERNAME")
    db_password = os.environ.get("DB_PASSWORD")
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    api_key = os.environ.get("CLOUDINARY_API_KEY")
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")

    missing = [
        name
        for name, val in [
            ("DB_URL", db_url),
            ("DB_USERNAME", db_user),
            ("CLOUDINARY_CLOUD_NAME", cloud_name),
            ("CLOUDINARY_API_KEY", api_key),
            ("CLOUDINARY_API_SECRET", api_secret),
        ]
        if not val
    ]
    if missing:
        print(f"missing env vars: {missing}", file=sys.stderr)
        return 1

    print("fetching local menu image dimensions...")
    local = local_menu_files()
    print(f"local menu files: {len(local)}")

    print("fetching Cloudinary resources...")
    cloud = fetch_cloudinary_resources(cloud_name, api_key, api_secret)
    print(f"cloud resources: {len(cloud)}")

    mapping = build_menu_id_to_asset(local, cloud)
    print(f"matched: {len(mapping)}/{len(local)}")

    host, port, db = parse_jdbc_url(db_url)
    conn = pymysql.connect(
        host=host,
        port=port,
        user=db_user,
        password=db_password or "",
        database=db,
        charset="utf8mb4",
        autocommit=False,
    )
    try:
        with conn.cursor() as cur:
            provider_id = ensure_schema(cur)
            if not table_exists(cur, "media_asset"):
                print("media_asset table missing after ensure_schema", file=sys.stderr)
                return 1
            menu_id_to_asset_row_id = upsert_media_assets(cur, provider_id, mapping)
            updated = link_menu_rows(cur, menu_id_to_asset_row_id, mapping)
            print(f"menu rows linked: {updated}")
        conn.commit()
        print("done")
        return 0
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
