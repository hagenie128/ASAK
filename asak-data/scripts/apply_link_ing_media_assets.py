#!/usr/bin/env python3
"""Link ing.icon_asset_id / ing.photo_asset_id to (deduped) media_asset rows.

Local source of truth: ASAK-Kiosk/public/assets/ingredients/{icons,photos}/{ing_id}.*
Cloud: Cloudinary asak/icon (icons) and asak/opt (photos) folders.

Matching is done by exact content hash (MD5), not filename, because Cloudinary
generates random public_ids on upload. Many ingredients intentionally reuse the
same icon/photo artwork, so identical-content assets are stored ONCE in
media_asset and shared by multiple ing rows via FK, instead of one row per ing.
Idempotent: safe to re-run.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import pymysql

ICON_DIR = Path(r"C:\ASAK-workspace\ASAK-Kiosk\public\assets\ingredients\icons")
PHOTO_DIR = Path(r"C:\ASAK-workspace\ASAK-Kiosk\public\assets\ingredients\photos")
ICON_FOLDER = "asak/icon"
PHOTO_FOLDER = "asak/opt"


def to_mysql_datetime(iso_ts: str | None) -> str | None:
    if not iso_ts:
        return None
    dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00")).astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


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


def local_hashes(directory: Path) -> dict[int, str]:
    out = {}
    for path in directory.glob("*.*"):
        if not path.stem.isdigit():
            continue
        out[int(path.stem)] = hashlib.md5(path.read_bytes()).hexdigest()
    return out


def cloud_hashes(resources: list[dict], folder: str) -> dict[str, str]:
    out = {}
    for r in resources:
        if r.get("asset_folder") != folder:
            continue
        with urllib.request.urlopen(r["secure_url"]) as resp:
            out[r["public_id"]] = hashlib.md5(resp.read()).hexdigest()
    return out


def build_hash_to_resource(resources: list[dict], folder: str, hashes: dict[str, str]) -> dict[str, dict]:
    by_id = {r["public_id"]: r for r in resources if r.get("asset_folder") == folder}
    hash_to_resource: dict[str, dict] = {}
    for public_id, h in sorted(hashes.items()):
        hash_to_resource.setdefault(h, by_id[public_id])
    return hash_to_resource


def table_exists(cur, table: str) -> bool:
    cur.execute(
        "SELECT 1 FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s",
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
        "SELECT 1 FROM information_schema.TABLE_CONSTRAINTS WHERE TABLE_SCHEMA = DATABASE() AND CONSTRAINT_NAME = %s",
        (name,),
    )
    return cur.fetchone() is not None


def get_cloudinary_provider_id(cur) -> int:
    cur.execute(
        """
        SELECT cc.id FROM common_code cc
        JOIN code_group cg ON cg.id = cc.code_grp_id
        WHERE cg.group_code = 'MEDIA_PROVIDER' AND cc.code = 'CLOUDINARY'
        """
    )
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("MEDIA_PROVIDER/CLOUDINARY common_code missing; run apply_create_media_asset.py first")
    return row[0]


def ensure_ing_columns(cur) -> None:
    for col, comment in [("icon_asset_id", "media_asset FK (아이콘)"), ("photo_asset_id", "media_asset FK (사진)")]:
        if not column_exists(cur, "ing", col):
            cur.execute(f"ALTER TABLE `ing` ADD COLUMN `{col}` BIGINT NULL COMMENT '{comment}'")
            print(f"added ing.{col}")
        else:
            print(f"ing.{col} already present")

    for col, fk in [("icon_asset_id", "fk_ing_icon_asset_id"), ("photo_asset_id", "fk_ing_photo_asset_id")]:
        if not constraint_exists(cur, fk):
            cur.execute(
                f"ALTER TABLE `ing` ADD CONSTRAINT `{fk}` FOREIGN KEY (`{col}`) REFERENCES `media_asset` (`id`)"
            )
            print(f"added {fk}")
        else:
            print(f"{fk} already present")


def upsert_media_asset(cur, provider_id: int, r: dict) -> int:
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
    return cur.lastrowid


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

    print("hashing local icon/photo files...")
    local_icon = local_hashes(ICON_DIR)
    local_photo = local_hashes(PHOTO_DIR)
    print(f"local icons: {len(local_icon)}, local photos: {len(local_photo)}")

    print("fetching Cloudinary resource list...")
    cloud = fetch_cloudinary_resources(cloud_name, api_key, api_secret)

    print("downloading + hashing cloud icon assets...")
    cloud_icon_h = cloud_hashes(cloud, ICON_FOLDER)
    print("downloading + hashing cloud photo assets...")
    cloud_photo_h = cloud_hashes(cloud, PHOTO_FOLDER)

    icon_hash_to_resource = build_hash_to_resource(cloud, ICON_FOLDER, cloud_icon_h)
    photo_hash_to_resource = build_hash_to_resource(cloud, PHOTO_FOLDER, cloud_photo_h)

    icon_unmatched = [ing_id for ing_id, h in local_icon.items() if h not in icon_hash_to_resource]
    photo_unmatched = [ing_id for ing_id, h in local_photo.items() if h not in photo_hash_to_resource]
    if icon_unmatched:
        print(f"warning: icon content with no cloud match, ing ids: {icon_unmatched}", file=sys.stderr)
    if photo_unmatched:
        print(f"warning: photo content with no cloud match, ing ids: {photo_unmatched}", file=sys.stderr)

    print(f"distinct icon assets to store: {len(icon_hash_to_resource)}")
    print(f"distinct photo assets to store: {len(photo_hash_to_resource)}")

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
            if not table_exists(cur, "media_asset"):
                print("media_asset table missing; run apply_create_media_asset.py first", file=sys.stderr)
                return 1
            provider_id = get_cloudinary_provider_id(cur)
            ensure_ing_columns(cur)

            icon_hash_to_row_id = {
                h: upsert_media_asset(cur, provider_id, r) for h, r in icon_hash_to_resource.items()
            }
            photo_hash_to_row_id = {
                h: upsert_media_asset(cur, provider_id, r) for h, r in photo_hash_to_resource.items()
            }

            icon_linked = 0
            for ing_id, h in local_icon.items():
                row_id = icon_hash_to_row_id.get(h)
                if row_id is None:
                    continue
                cur.execute("UPDATE `ing` SET `icon_asset_id` = %s WHERE `id` = %s", (row_id, ing_id))
                icon_linked += cur.rowcount

            photo_linked = 0
            for ing_id, h in local_photo.items():
                row_id = photo_hash_to_row_id.get(h)
                if row_id is None:
                    continue
                cur.execute("UPDATE `ing` SET `photo_asset_id` = %s WHERE `id` = %s", (row_id, ing_id))
                photo_linked += cur.rowcount

            print(f"ing rows linked to icon: {icon_linked}")
            print(f"ing rows linked to photo: {photo_linked}")
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
