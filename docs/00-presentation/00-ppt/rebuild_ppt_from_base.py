"""
정상 PPT(수정4)를 베이스로 COM 재구성 → PowerPoint 복구 프롬프트 없이 열리게 함.
"""

from __future__ import annotations

import os
import shutil
import time
from pathlib import Path

import win32com.client

BASE = Path(__file__).resolve().parent
BASE_PPT = BASE / "ASAK_샐러드_스마트키오스크_수정4_2026_0821.pptx"
OUT_PPT = BASE / "ASAK_샐러드_스마트키오스크_2026_0902.pptx"
SHOT = BASE.parent / "02-kiosk_screenshot"

MsoPicture = 13


def pt(emu: int) -> float:
    return emu / 914400 * 72


TITLE_TOP = pt(900000)
BODY_TOP_MIN = pt(1400000)
BODY_TOP_MAX = pt(2800000)
HIGHLIGHT_TOP_MIN = pt(3200000)
HIGHLIGHT_TOP_MAX = pt(4300000)
CAPTION_TOP_MIN = pt(5200000)
CAPTION_TOP_MAX = pt(5900000)
FOOT_TOP = pt(5900000)
PAGE_LEFT = pt(10000000)
PAGE_TOP = pt(6000000)

KIOSK_TEMPLATE = "메뉴 목록 및 카테고리 선택"
ADMIN_TEMPLATE = "관리자 주문 관리"

KIOSK_NEW = [
    {
        "title": "메뉴 및 옵션 품절 처리",
        "body": (
            "메뉴와 옵션의 품절 상태를\n"
            "주문 화면에서 각각 구분하여 표시합니다.\n\n"
            "품절된 메뉴는 주문을 제한하고,\n"
            "일부 옵션만 품절된 경우에는\n"
            "해당 옵션만 선택할 수 없도록 처리했습니다."
        ),
        "highlight": (
            "품절 범위에 따라 주문 가능 여부를 다르게 제어하여 "
            "불필요한 주문 실패를 방지했습니다."
        ),
        "caption": "메뉴 전체 품절 · 개별 옵션 품절 상태",
        "images": [
            ("10_메뉴품절상태.jpg", 5650991, 1233811, 2263073, 4032385),
            ("11_옵션품절상태.jpg", 8337593, 1233812, 2287735, 4076328),
        ],
    },
    {
        "title": "결제 프로세스 및 결제수단",
        "body": (
            "주문 내역을 최종 확인한 뒤\n"
            "결제수단을 선택하고 결제를 진행합니다.\n\n"
            "결제 진행 상태와 완료 결과를\n"
            "단계별 화면으로 구분하여\n"
            "사용자가 현재 상태를 확인할 수 있도록 구성했습니다."
        ),
        "highlight": (
            "주문 확인 → 결제수단 선택 → 결제 진행 → 결제 완료의 "
            "흐름을 단계별로 구성했습니다."
        ),
        "caption": "주문 내역 확인 · 결제수단 선택 · 결제 진행 · 결제 완료",
        "footnote": "현재 결제는 실제 PG가 아닌 가상 결제 프로세스로 구현했습니다.",
        "images": [
            ("06_주문내역확인.jpg", 438912, 1280160, 2700000, 3800000),
            ("07_결제수단선택.jpg", 3290000, 1280160, 2700000, 3800000),
            ("08_결제진행.jpg", 6141088, 1280160, 2700000, 3800000),
            ("09_결제완료.jpg", 8992176, 1280160, 2700000, 3800000),
        ],
    },
    {
        "title": "예외 상황 및 사용자 상태 처리",
        "body": (
            "키오스크 사용 중 발생할 수 있는\n"
            "입력 누락 · 장바구니 상태 · 사용자 미응답 상황을\n"
            "각각 구분하여 안내합니다.\n\n"
            "단순 오류 메시지가 아니라\n"
            "사용자가 다음 행동을 알 수 있도록\n"
            "상황별 안내 팝업을 구성했습니다."
        ),
        "highlight": (
            "사용자의 실수를 사전에 방지하고, "
            "중단된 주문 흐름을 자연스럽게 이어갈 수 있도록 처리했습니다."
        ),
        "caption": "타임아웃 · 장바구니 비우기 · 빈 장바구니 · 결제수단 미선택",
        "images": [
            ("12_타임아웃팝업.jpg", 5063112, 1180000, 2900000, 2100000),
            ("13_장바구니_비우기_팝업.jpg", 8200000, 1180000, 2900000, 2100000),
            ("14_빈장바구니_상태_팝업.jpg", 5063112, 3500000, 2900000, 2100000),
            ("15_결제수단미선택_팝업.jpg", 8200000, 3500000, 2900000, 2100000),
        ],
    },
    {
        "title": "주문 완료 및 영수증 출력",
        "body": (
            "결제가 완료되면 주문 완료 상태를 안내하고\n"
            "영수증 출력 과정을 사용자에게 표시합니다.\n\n"
            "주문 종료 이후에도\n"
            "출력 상태를 확인할 수 있도록\n"
            "상태 안내 UI를 구성했습니다."
        ),
        "highlight": (
            "결제 완료 → 주문 완료 안내 → 영수증 출력까지 "
            "주문 종료 흐름을 구성했습니다."
        ),
        "caption": "결제 완료 · 영수증 출력 상태 안내",
        "footnote": (
            "RTOS Simulator와 연동하여 영수증 출력 이벤트를 처리하고, "
            "출력 상태를 Kiosk 화면에 반영했습니다."
        ),
        "images": [
            ("09_결제완료.jpg", 5650991, 1233811, 2263073, 4032385),
            ("17_영수증출력_상태_토스트.jpg", 8337593, 1233812, 2287735, 4076328),
        ],
    },
]

ADMIN_NEW = [
    {
        "title": "관리자 품절 관리",
        "body": (
            "메뉴와 재료의 품절 상태를 \n"
            "관리자 화면에서 확인하고 관리합니다.\n\n"
            "품절 상태가 변경되면 Kiosk 주문 화면에도 \n"
            "동일한 기준을 적용해 주문할 수 없는 메뉴나 \n"
            "옵션의 선택을 제한합니다."
        ),
        "highlight": "Admin 품절 관리 → 서버 데이터 반영 → \nKiosk 주문 제한",
        "caption": "메뉴 · 재료 품절 조회 및 상태 관리",
        "footnote": (
            "운영 중 발생하는 품절 상황을 빠르게 반영하여 "
            "고객이 주문 단계에서 품절 상품을 선택하는 오류를 줄였습니다"
        ),
    },
    {
        "title": "관리자 매출 관리",
        "body": (
            "주문 데이터를 기반으로\n"
            "일별 · 월별 · 시간대별 매출 현황을 조회합니다.\n\n"
            "기간별 매출과 주문 흐름을 시각화하여\n"
            "운영자가 매장의 주요 매출 추이를\n"
            "한눈에 확인할 수 있도록 구성했습니다."
        ),
        "highlight": "주문 데이터 → 매출 집계 → 운영 지표 확인",
        "caption": "매출 현황 · 기간별 통계 · 주문 추이",
        "footnote": (
            "주문 데이터가 단순히 저장되는 데 그치지 않고 "
            "운영에 필요한 정보로 활용될 수 있도록 관리자 화면에 시각화 했습니다."
        ),
    },
]

EXISTING_IMAGES = {
    "메뉴 목록 및 카테고리 선택": ["01_메뉴리스트.jpg", "03_메뉴선택후_메뉴리스트.jpg"],
    "메뉴 상세 및 옵션 선택": ["02_메뉴디테일.jpg", "03_메뉴선택후_메뉴리스트.jpg"],
    "장바구니 및 결제 이동": ["04_장바구니.jpg", "06_주문내역확인.jpg"],
    "화면설계서 — 키오스크 주문 흐름": ["01_메뉴리스트.jpg", "02_메뉴디테일.jpg", "04_장바구니.jpg"],
}


def find_slide(pres, title: str) -> int:
    for i in range(1, pres.Slides.Count + 1):
        slide = pres.Slides(i)
        for j in range(1, slide.Shapes.Count + 1):
            sh = slide.Shapes(j)
            if sh.HasTextFrame and sh.TextFrame.HasText:
                if sh.Top < TITLE_TOP and title in sh.TextFrame.TextRange.Text:
                    return i
    raise RuntimeError(f"slide not found: {title}")


def set_text(shape, text: str) -> None:
    if shape.HasTextFrame:
        shape.TextFrame.TextRange.Text = text


def fill_feature_slide(slide, data: dict, is_admin: bool = False) -> None:
    shapes = {}
    extras = []
    for i in range(1, slide.Shapes.Count + 1):
        sh = slide.Shapes(i)
        if not sh.HasTextFrame or not sh.TextFrame.HasText:
            continue
        top = sh.Top
        text = sh.TextFrame.TextRange.Text.strip()
        if top < TITLE_TOP and "핵심 기능" not in text and "ASAK" not in text and "수행 경과" not in text:
            if len(text) > 3 and not text.isdigit():
                shapes["title"] = sh
        elif BODY_TOP_MIN < top < BODY_TOP_MAX:
            if "body" not in shapes:
                shapes["body"] = sh
            else:
                extras.append(sh)
        elif HIGHLIGHT_TOP_MIN < top < HIGHLIGHT_TOP_MAX:
            shapes["highlight"] = sh
        elif CAPTION_TOP_MIN < top < CAPTION_TOP_MAX:
            shapes["caption"] = sh
        elif FOOT_TOP < top < pt(6350000) and "ASAK" not in text and "그린컴퓨터" not in text:
            shapes["footnote"] = sh

    for key in ("title", "body", "highlight", "caption", "footnote"):
        if key in data and key in shapes:
            set_text(shapes[key], data[key])

    for sh in extras:
        sh.Delete()

    if "images" in data:
        names = []
        for i in range(1, slide.Shapes.Count + 1):
            if slide.Shapes(i).Type == MsoPicture:
                names.append(slide.Shapes(i).Name)
        for name in names:
            slide.Shapes(name).Delete()
        for fname, l, t, w, h in data["images"]:
            slide.Shapes.AddPicture(str((SHOT / fname).resolve()), False, True, pt(l), pt(t), pt(w), pt(h))


def replace_slide_images(pres, title: str, files: list[str]) -> None:
    slide = pres.Slides(find_slide(pres, title))
    pics = []
    for i in range(1, slide.Shapes.Count + 1):
        if slide.Shapes(i).Type == MsoPicture:
            pics.append(slide.Shapes(i))
    for pic, fname in zip(pics, files):
        l, t, w, h = pic.Left, pic.Top, pic.Width, pic.Height
        pic.Delete()
        slide.Shapes.AddPicture(str((SHOT / fname).resolve()), False, True, l, t, w, h)


def insert_duplicate(pres, template_idx: int, at_idx: int):
    dup = pres.Slides(template_idx).Duplicate()
    new_idx = dup.SlideIndex
    if new_idx != at_idx:
        pres.Slides(new_idx).MoveTo(at_idx)
    return at_idx


def renumber(pres) -> None:
    for i in range(1, pres.Slides.Count + 1):
        slide = pres.Slides(i)
        for j in range(1, slide.Shapes.Count + 1):
            sh = slide.Shapes(j)
            if sh.HasTextFrame and sh.TextFrame.HasText:
                if sh.Left > PAGE_LEFT and sh.Top > PAGE_TOP:
                    t = sh.TextFrame.TextRange.Text.strip()
                    if t.isdigit():
                        sh.TextFrame.TextRange.Text = str(i)
                        break


def main() -> None:
    broken_backup = OUT_PPT.with_suffix(".broken.pptx")
    if OUT_PPT.exists():
        shutil.copy2(OUT_PPT, broken_backup)

    work = OUT_PPT.with_suffix(".rebuild.pptx")
    shutil.copy2(BASE_PPT, work)

    app = win32com.client.Dispatch("PowerPoint.Application")
    pres = app.Presentations.Open(str(work.resolve()))

    kiosk_tpl = find_slide(pres, KIOSK_TEMPLATE)
    admin_tpl = find_slide(pres, ADMIN_TEMPLATE)
    detail_idx = find_slide(pres, "메뉴 상세 및 옵션 선택")

    # 품절 → (기존 장바구니) → 결제/예외/영수증
    insert_at = detail_idx + 1
    fill_feature_slide(pres.Slides(insert_duplicate(pres, kiosk_tpl, insert_at)), KIOSK_NEW[0])
    insert_at += 1

    cart_idx = find_slide(pres, "장바구니 및 결제 이동")
    replace_slide_images(pres, "장바구니 및 결제 이동", EXISTING_IMAGES["장바구니 및 결제 이동"])

    insert_at = cart_idx + 1
    for data in KIOSK_NEW[1:]:
        fill_feature_slide(pres.Slides(insert_duplicate(pres, kiosk_tpl, insert_at)), data)
        insert_at += 1

    menu_admin_idx = find_slide(pres, "관리자 메뉴 관리")
    insert_at = menu_admin_idx + 1
    for data in ADMIN_NEW:
        fill_feature_slide(
            pres.Slides(insert_duplicate(pres, admin_tpl, insert_at)),
            data,
            is_admin=True,
        )
        insert_at += 1

    for title, files in EXISTING_IMAGES.items():
        if title in ("장바구니 및 결제 이동",):
            continue
        try:
            replace_slide_images(pres, title, files)
        except RuntimeError:
            pass

    renumber(pres)
    pres.SaveAs(str(OUT_PPT.resolve()))
    pres.Close()
    app.Quit()

    work.unlink(missing_ok=True)
    print("rebuilt:", OUT_PPT)
    print("broken backup:", broken_backup)

    # 검증
    app2 = win32com.client.Dispatch("PowerPoint.Application")
    p2 = app2.Presentations.Open(str(OUT_PPT.resolve()))
    print("PowerPoint open OK, slides:", p2.Slides.Count)
    p2.Close()
    app2.Quit()


if __name__ == "__main__":
    main()
