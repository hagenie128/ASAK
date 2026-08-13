#!/usr/bin/env python3
"""Apply only the Side/Drink rows from salady_menu_full_97.csv to seed-v3 and MySQL.

Scope is intentionally fixed: two categories and fifteen standalone menus.
Sets and the separate set-option CSV are documented, not imported.
"""
from __future__ import annotations

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pymysql


ROOT = Path(__file__).resolve().parents[2]
SEED = ROOT / "asak-data" / "seed-v3"
SOURCE = Path(r"C:\Users\Administrator\Downloads\salady_menu_full_97.csv")
REPORT = ROOT / "docs" / "ai-reports" / "2026-08-13" / "side-drink-menu-source-deferment.md"
CATEGORIES = (
    {"id": 237, "name": "사이드", "sort_no": 4, "active": True},
    {"id": 238, "name": "음료", "sort_no": 6, "active": True},
)


def normalized(value: str) -> str:
    return "".join((value or "").split())


def load_env() -> None:
    env_path = ROOT.parent / "ASAK-back" / ".env"
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if "=" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def parse_jdbc_url(url: str) -> tuple[str, int, str]:
    raw = url.replace("jdbc:mysql://", "")
    host_port, rest = raw.split("/", 1)
    host, port = host_port.split(":", 1)
    return host, int(port), rest.split("?", 1)[0]


def read_json(name: str) -> list[dict]:
    return json.loads((SEED / name).read_text(encoding="utf-8"))


def write_json(name: str, rows: list[dict]) -> None:
    (SEED / name).write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_rows() -> list[dict[str, str]]:
    with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["카테고리"] in {"사이드", "음료"}]
    if len(rows) != 15:
        raise RuntimeError(f"Expected 15 side/drink rows, found {len(rows)}")
    if len({normalized(row["메뉴"]) for row in rows}) != len(rows):
        raise RuntimeError("Side/drink source rows have duplicate normalized names")
    return rows


def build_rows(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict]]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    menus, nutrition = [], []
    for index, row in enumerate(rows):
        menu_id = 10776 + index
        menus.append(
            {
                "id": menu_id,
                "cat_id": 237 if row["카테고리"] == "사이드" else 238,
                "name": row["메뉴"].strip(),
                "price": int(row["가격"]),
                # Keep the supplied source URL until a media_asset is registered and linked.
                "image_url": row["이미지 링크"].strip(),
                "description": row["설명"].strip(),
                "sold_out": False,
                "created_at": now,
                "updated_at": now,
            }
        )
        # UserMenuMapper inner-joins menu_nutr; retain a nullable row so the menu is listable.
        nutrition.append(
            {
                "id": 10778 + index,
                "menu_id": menu_id,
                "source_id": 41,
                "serving_g": None,
                "kcal": None,
                "carb_g": None,
                "sugar_g": None,
                "protein_g": None,
                "fat_g": None,
                "saturated_fat_g": None,
                "sodium_mg": None,
            }
        )
    return menus, nutrition


def verify_seed(categories: list[dict], menus: list[dict], nutrition: list[dict], new_menus: list[dict]) -> None:
    ids = {int(row["id"]) for row in menus}
    names = {normalized(row["name"]) for row in menus}
    for row in new_menus:
        if int(row["id"]) in ids or normalized(row["name"]) in names:
            raise RuntimeError(f"Seed duplicate candidate: {row['id']} / {row['name']}")
    if any(int(row["id"]) in {237, 238} or row["name"] in {"사이드", "음료"} for row in categories):
        raise RuntimeError("Seed already contains a side/drink category; inspect before rerunning")
    if max(int(row["id"]) for row in nutrition) >= 10778:
        raise RuntimeError("Seed nutrition IDs already overlap the planned 10778+ range")


def update_seed(new_menus: list[dict], new_nutrition: list[dict]) -> None:
    categories = read_json("category.json")
    menus = read_json("menu.json")
    nutrition = read_json("menu_nutr.json")
    verify_seed(categories, menus, nutrition, new_menus)
    write_json("category.json", categories + list(CATEGORIES))
    write_json("menu.json", menus + new_menus)
    write_json("menu_nutr.json", nutrition + new_nutrition)
    manifest_path = SEED / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["counts"]["category"] = len(categories) + len(CATEGORIES)
    manifest["counts"]["menu"] = len(menus) + len(new_menus)
    manifest["counts"]["menu_nutr"] = len(nutrition) + len(new_nutrition)
    manifest["side_drink_applied_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def apply_database(new_menus: list[dict], new_nutrition: list[dict]) -> None:
    load_env()
    host, port, database = parse_jdbc_url(os.environ["DB_URL"])
    connection = pymysql.connect(
        host=host,
        port=port,
        user=os.environ["DB_USERNAME"],
        password=os.environ["DB_PASSWORD"],
        database=database,
        charset="utf8mb4",
        autocommit=False,
    )
    names = [row["name"] for row in new_menus]
    placeholders = ", ".join(["%s"] * len(names))
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM category WHERE name IN ('사이드', '음료')")
            if cursor.fetchall():
                raise RuntimeError("DB already has the target categories; no automatic merge was attempted")
            cursor.execute(f"SELECT id, name FROM menu WHERE name IN ({placeholders})", names)
            if cursor.fetchall():
                raise RuntimeError("DB already has a target menu name; no automatic merge was attempted")
            cursor.execute("SELECT MAX(id) FROM menu")
            if cursor.fetchone()[0] != 10775:
                raise RuntimeError("DB menu ID changed after precheck; rerun a read-only audit before applying")
            cursor.execute("SELECT MAX(id) FROM menu_nutr")
            if cursor.fetchone()[0] != 10777:
                raise RuntimeError("DB menu_nutr ID changed after precheck; rerun a read-only audit before applying")

            # These snapshots are recovery evidence and are deliberately retained.
            cursor.execute("CREATE TABLE IF NOT EXISTS backup_category_20260813_before_side_drink AS SELECT * FROM category")
            cursor.execute(f"CREATE TABLE IF NOT EXISTS backup_menu_20260813_before_side_drink AS SELECT * FROM menu WHERE name IN ({placeholders})", names)
            cursor.execute(f"CREATE TABLE IF NOT EXISTS backup_menu_nutr_20260813_before_side_drink AS SELECT mn.* FROM menu_nutr mn JOIN menu m ON m.id=mn.menu_id WHERE m.name IN ({placeholders})", names)

            cursor.executemany(
                "INSERT INTO category (id, name, sort_no, active) VALUES (%s, %s, %s, %s)",
                [(row["id"], row["name"], row["sort_no"], row["active"]) for row in CATEGORIES],
            )
            cursor.executemany(
                """INSERT INTO menu (id, cat_id, name, price, image_url, description, sold_out)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                [
                    (row["id"], row["cat_id"], row["name"], row["price"], row["image_url"], row["description"], row["sold_out"])
                    for row in new_menus
                ],
            )
            cursor.executemany(
                """INSERT INTO menu_nutr
                   (id, menu_id, kcal, protein_g, carb_g, fat_g, sodium_mg, source_id, serving_g, sugar_g, saturated_fat_g)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                [
                    (row["id"], row["menu_id"], row["kcal"], row["protein_g"], row["carb_g"], row["fat_g"], row["sodium_mg"], row["source_id"], row["serving_g"], row["sugar_g"], row["saturated_fat_g"])
                    for row in new_nutrition
                ],
            )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def write_document(rows: list[dict[str, str]], menus: list[dict]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    all_rows = []
    with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
        all_rows = list(csv.DictReader(handle))
    deferred = [row for row in all_rows if row["카테고리"] not in {"사이드", "음료"}]
    lines = [
        "# 2026-08-13 사이드·음료 메뉴 반영 및 나머지 CSV 보류 기록",
        "",
        "## 반영됨",
        "",
        "- 입력: `C:\\Users\\Administrator\\Downloads\\salady_menu_full_97.csv`",
        "- DB·`asak-data/seed-v3`에 카테고리 `사이드`(237), `음료`(238)와 단품 메뉴 15개만 반영했다.",
        "- 메뉴 ID: 10776~10790. 목록 SQL의 `menu_nutr` inner join을 통과하도록 영양값은 미확정(null)인 행을 함께 만들었다.",
        "- 제공된 외부 이미지 URL은 `menu.image_url`에 보관했다. 현재 Kiosk 목록은 `media_asset`만 사용하므로 이미지 asset 등록·연결은 별도 작업이다.",
        "",
        "## 보류됨",
        "",
        f"- 원본 97행 중 이번 범위 밖 행: {len(deferred)}행. 기존 시드와의 중복·갱신 여부를 별도 대조하지 않았다.",
        "- `올데이 세트` 37개와 `고추장_제육_간장메밀_누들볼_세트_옵션.csv`의 60개 옵션 행은 반영하지 않았다.",
        "- 세트 옵션은 `opt_group`/`opt_item`/`opt_policy`/`menu_opt_policy`의 정책 모델과 가격·필수·최대선택수 매핑을 먼저 확정한 뒤 별도 transaction으로 반영한다.",
        "",
        "## 반영 메뉴",
        "",
    ]
    lines.extend(f"- `{menu['id']}` {menu['name']} — {menu['price']}원" for menu in menus)
    lines.extend(["", "## 검증", "", "- DB category/menu/menu_nutr 행 수와 `/api/kiosk/categories`, `/api/kiosk/menuList` 응답을 확인한다."])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = source_rows()
    menus, nutrition = build_rows(rows)
    apply_database(menus, nutrition)
    update_seed(menus, nutrition)
    write_document(rows, menus)
    print(json.dumps({"categories": [row["name"] for row in CATEGORIES], "menus": len(menus), "menu_ids": [row["id"] for row in menus], "report": str(REPORT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
