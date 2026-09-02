"""
PPT 스타일 복구: PowerPoint COM으로 템플릿 슬라이드 복제 후 텍스트/이미지만 교체.
"""

from __future__ import annotations

import os
import shutil
import time
from pathlib import Path

import win32com.client

BASE = Path(__file__).resolve().parent
PPT = BASE / "ASAK_샐러드_스마트키오스크_2026_0902.pptx"
SHOT = BASE.parent / "02-kiosk_screenshot"

# EMU -> PowerPoint Points
def pt(emu: int) -> float:
    return emu / 914400 * 72


KIOSK_TEMPLATE_TITLE = "메뉴 목록 및 카테고리 선택"
ADMIN_TEMPLATE_TITLE = "관리자 주문 관리"

KIOSK_SLIDES = [
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

ADMIN_SLIDES = [
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

# 레이아웃 기준 (Points)
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

DELETE_TITLES = [
    "메뉴 및 옵션 품절 처리",
    "결제 프로세스 및 결제수단",
    "예외 상황 및 사용자 상태 처리",
    "주문 완료 및 영수증 출력",
    "관리자 품절 관리",
    "관리자 매출 관리",
]


def find_slide(pres, title: str) -> int | None:
    for i in range(1, pres.Slides.Count + 1):
        slide = pres.Slides(i)
        for j in range(1, slide.Shapes.Count + 1):
            sh = slide.Shapes(j)
            if sh.HasTextFrame and sh.TextFrame.HasText:
                if sh.Top < TITLE_TOP and title in sh.TextFrame.TextRange.Text:
                    return i
    return None


def replace_shape_text(shape, text: str) -> None:
    if not shape.HasTextFrame:
        return
    tr = shape.TextFrame.TextRange
    tr.Text = text


def fill_kiosk_slide(slide, data: dict) -> None:
    title_shape = body_shape = highlight_shape = caption_shape = foot_shape = None
    for i in range(1, slide.Shapes.Count + 1):
        sh = slide.Shapes(i)
        if not sh.HasTextFrame or not sh.TextFrame.HasText:
            continue
        top = sh.Top
        text = sh.TextFrame.TextRange.Text.strip()
        if top < TITLE_TOP and "핵심 기능" not in text and "ASAK" not in text and "수행 경과" not in text:
            if len(text) > 3 and not text.isdigit():
                title_shape = sh
        elif BODY_TOP_MIN < top < BODY_TOP_MAX and len(text) > 20:
            body_shape = sh
        elif HIGHLIGHT_TOP_MIN < top < HIGHLIGHT_TOP_MAX and len(text) > 10:
            highlight_shape = sh
        elif CAPTION_TOP_MIN < top < CAPTION_TOP_MAX and "·" in text:
            caption_shape = sh
        elif top > FOOT_TOP and len(text) > 15:
            foot_shape = sh

    if title_shape:
        replace_shape_text(title_shape, data["title"])
    if body_shape:
        replace_shape_text(body_shape, data["body"])
    if highlight_shape:
        replace_shape_text(highlight_shape, data["highlight"])
    if caption_shape:
        replace_shape_text(caption_shape, data["caption"])
    if data.get("footnote") and foot_shape:
        replace_shape_text(foot_shape, data["footnote"])

    # 기존 사진 제거 (msoPicture = 13)
    to_delete = []
    for i in range(1, slide.Shapes.Count + 1):
        sh = slide.Shapes(i)
        if sh.Type == 13:
            to_delete.append(sh.Name)
    for name in to_delete:
        slide.Shapes(name).Delete()

    for fname, left, top, width, height in data["images"]:
        path = str((SHOT / fname).resolve())
        slide.Shapes.AddPicture(
            path, False, True, pt(left), pt(top), pt(width), pt(height)
        )


def fill_admin_slide(slide, data: dict) -> None:
    title_shape = body_shape = highlight_shape = caption_shape = foot_shape = None
    for i in range(1, slide.Shapes.Count + 1):
        sh = slide.Shapes(i)
        if not sh.HasTextFrame or not sh.TextFrame.HasText:
            continue
        top = sh.Top
        text = sh.TextFrame.TextRange.Text.strip()
        if top < TITLE_TOP and "핵심 기능" not in text and "ASAK" not in text:
            if len(text) > 3 and not text.isdigit():
                title_shape = sh
        elif BODY_TOP_MIN < top < BODY_TOP_MAX:
            body_shape = sh
        elif HIGHLIGHT_TOP_MIN < top < HIGHLIGHT_TOP_MAX:
            highlight_shape = sh
        elif CAPTION_TOP_MIN < top < CAPTION_TOP_MAX:
            caption_shape = sh
        elif top > FOOT_TOP:
            foot_shape = sh

    if title_shape:
        replace_shape_text(title_shape, data["title"])
    if body_shape:
        replace_shape_text(body_shape, data["body"])
    if highlight_shape:
        replace_shape_text(highlight_shape, data["highlight"])
    if caption_shape:
        replace_shape_text(caption_shape, data["caption"])
    if foot_shape:
        replace_shape_text(foot_shape, data["footnote"])


def renumber_slides(pres) -> None:
    for i in range(1, pres.Slides.Count + 1):
        slide = pres.Slides(i)
        for j in range(1, slide.Shapes.Count + 1):
            sh = slide.Shapes(j)
            if sh.HasTextFrame and sh.TextFrame.HasText:
                if sh.Left > PAGE_LEFT and sh.Top > PAGE_TOP:
                    t = sh.TextFrame.TextRange.Text.strip()
                    if t.isdigit():
                        sh.TextFrame.TextRange.Text = str(i)
                        return


def main() -> None:
    backup = PPT.with_suffix(".before_style_fix.pptx")
    shutil.copy2(PPT, backup)

    app = win32com.client.Dispatch("PowerPoint.Application")
    pres = app.Presentations.Open(str(PPT.resolve()))

    # 깨진 슬라이드 삭제
    for title in DELETE_TITLES:
        while True:
            idx = find_slide(pres, title)
            if not idx:
                break
            pres.Slides(idx).Delete()

    kiosk_tpl = find_slide(pres, KIOSK_TEMPLATE_TITLE)
    admin_tpl = find_slide(pres, ADMIN_TEMPLATE_TITLE)
    detail_idx = find_slide(pres, "메뉴 상세 및 옵션 선택")
    cart_idx = find_slide(pres, "장바구니 및 결제 이동")
    admin_order_idx = find_slide(pres, "관리자 주문 관리")

    if not all([kiosk_tpl, admin_tpl, detail_idx, cart_idx, admin_order_idx]):
        raise RuntimeError("필수 슬라이드를 찾지 못했습니다.")

    # Kiosk 신규 4장: 상세 다음에 삽입 (품절 → 장바구니 앞)
    insert_at = detail_idx + 1
    for data in KIOSK_SLIDES:
        dup = pres.Slides(kiosk_tpl).Duplicate()
        new_idx = dup.SlideIndex
        if new_idx != insert_at:
            pres.Slides(new_idx).MoveTo(insert_at)
        fill_kiosk_slide(pres.Slides(insert_at), data)
        insert_at += 1

    # Admin 품절/매출: 주문 관리 다음에 삽입
    insert_at = admin_order_idx + 1
    for data in ADMIN_SLIDES:
        dup = pres.Slides(admin_tpl).Duplicate()
        new_idx = dup.SlideIndex
        if new_idx != insert_at:
            pres.Slides(new_idx).MoveTo(insert_at)
        fill_admin_slide(pres.Slides(insert_at), data)
        insert_at += 1

    # 장바구니 캡처 갱신
    cart_slide = pres.Slides(find_slide(pres, "장바구니 및 결제 이동"))
    pics = []
    for i in range(1, cart_slide.Shapes.Count + 1):
        if cart_slide.Shapes(i).Type == 13:
            pics.append(cart_slide.Shapes(i))
    files = ["04_장바구니.jpg", "06_주문내역확인.jpg"]
    for pic, fname in zip(pics[:2], files):
        l, t, w, h = pic.Left, pic.Top, pic.Width, pic.Height
        pic.Delete()
        cart_slide.Shapes.AddPicture(
            str((SHOT / fname).resolve()), False, True, l, t, w, h
        )

    for i in range(12, pres.Slides.Count + 1):
        renumber_slides(pres)

    out = PPT.with_suffix(".style_fixed.pptx")
    pres.SaveAs(str(out.resolve()))
    pres.Close()
    app.Quit()
    shutil.move(out, PPT)
    print(f"복구 완료: {PPT}")
    print(f"백업: {backup}")


if __name__ == "__main__":
    main()
