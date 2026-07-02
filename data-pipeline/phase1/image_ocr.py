"""이미지 OCR 및 구조화 파싱 (세트메뉴 배너, 멤버십 등급표)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image, ImageEnhance, ImageOps

try:
    from rapidocr_onnxruntime import RapidOCR
except ImportError:  # pragma: no cover
    RapidOCR = None  # type: ignore[misc, assignment]

KNOWN_MEMBERSHIP_GRADES: list[dict[str, Any]] = [
    {
        "level": 1,
        "name_ko": "달팽이",
        "name_en": "Snail",
        "stamps_required": 0,
        "benefits": ["신규회원 2,000원 쿠폰 (가입 시 증정)"],
    },
    {
        "level": 2,
        "name_ko": "토끼",
        "name_en": "Rabbit",
        "stamps_required": 5,
        "benefits": ["생일축하 2,000원 쿠폰 (연 1회)"],
    },
    {
        "level": 3,
        "name_ko": "판다",
        "name_en": "Panda",
        "stamps_required": 40,
        "benefits": [
            "생일축하 2,000원 쿠폰 1장 (연 1회)",
            "무료 드링크 쿠폰 1장 (월 1회)",
        ],
    },
    {
        "level": 4,
        "name_ko": "기린",
        "name_en": "Giraffe",
        "stamps_required": 80,
        "benefits": [
            "생일축하 2,000원 쿠폰 1장 (연 1회)",
            "무료 드링크 쿠폰 1장 (월 1회)",
            "2,000원 쿠폰 1장 (월 1회)",
        ],
    },
]

SET_MENU_BANNER_HINTS: dict[str, dict[str, Any]] = {
    "SALADY 대표메뉴": {
        "banner_title_en": "Signature Menu",
        "tagline": "실패 없는 샐러디 베스트 PICK!",
        "composition": "랩 또는 샌드위치 제품",
        "components": ["랩", "샌드위치"],
        "note": "다른 메뉴를 원하시는 경우 주문 요청사항에 작성해주세요",
        "menu_source": "representative_menus",
    },
    "ALL DAY 세트메뉴": {
        "banner_title_en": "All-Day SET",
        "tagline": "사이드 메뉴와 음료로 더욱 든든하게!",
        "composition": "메인메뉴 + 카사바칩 + 음료 SET",
        "components": ["메인메뉴", "카사바칩", "음료"],
    },
    "하프 밸런스 세트메뉴": {
        "banner_title_en": "Half Balance",
        "tagline": "반반으로 즐기는 균형 잡힌 한 끼!",
        "composition": "미니 샐러디 1/2 + 랩 1/2 또는 샌드위치 1/2",
        "components": ["미니 샐러디 1/2", "랩 1/2", "샌드위치 1/2"],
    },
}


@dataclass
class OcrLine:
    text: str
    confidence: float
    center_x: float
    center_y: float


class ImageOcrParser:
    def __init__(self, cache_dir: Path | None = None):
        self.cache_dir = cache_dir
        self._ocr: Any | None = None

    def _engine(self) -> Any:
        if RapidOCR is None:
            raise RuntimeError(
                "rapidocr-onnxruntime 패키지가 필요합니다. "
                "pip install rapidocr-onnxruntime pillow opencv-python-headless"
            )
        if self._ocr is None:
            self._ocr = RapidOCR()
        return self._ocr

    def _preprocess(self, image: Image.Image, scale: float = 2.0) -> Image.Image:
        if image.mode != "RGB":
            image = image.convert("RGB")
        if scale != 1.0:
            image = image.resize(
                (int(image.width * scale), int(image.height * scale)),
                Image.Resampling.LANCZOS,
            )
        gray = ImageOps.grayscale(image)
        return ImageEnhance.Contrast(gray).enhance(1.4)

    def ocr_image_bytes(self, data: bytes, scale: float = 2.0) -> list[OcrLine]:
        image = Image.open(BytesIO(data))
        processed = self._preprocess(image, scale=scale)
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

        buffer = BytesIO()
        processed.save(buffer, format="PNG")
        result, _ = self._engine()(buffer.getvalue())
        lines: list[OcrLine] = []
        for item in result or []:
            box, text, score = item
            xs = [point[0] for point in box]
            ys = [point[1] for point in box]
            cleaned = re.sub(r"\s+", " ", str(text)).strip()
            if not cleaned:
                continue
            lines.append(
                OcrLine(
                    text=cleaned,
                    confidence=float(score),
                    center_x=sum(xs) / 4,
                    center_y=sum(ys) / 4,
                )
            )
        return lines

    def ocr_image_file(self, path: Path, scale: float = 2.0) -> list[OcrLine]:
        return self.ocr_image_bytes(path.read_bytes(), scale=scale)

    @staticmethod
    def lines_to_text(lines: list[OcrLine]) -> str:
        return "\n".join(line.text for line in lines)

    def parse_membership_grades(self, lines: list[OcrLine]) -> list[dict[str, Any]]:
        level_markers = []
        for line in lines:
            match = re.search(r"LEVEL\s*(\d+)", line.text, re.I)
            if match:
                level_markers.append((int(match.group(1)), line.center_y))

        level_markers.sort(key=lambda item: item[1])
        stamp_numbers = [
            int(match.group(1))
            for line in lines
            for match in [re.search(r"^\s*(\d{1,3})\s*$", line.text)]
            if match and int(match.group(1)) in {5, 40, 80}
        ]

        grades: list[dict[str, Any]] = []
        for base in KNOWN_MEMBERSHIP_GRADES:
            grade = dict(base)
            level = grade["level"]
            section_lines = self._lines_for_level(lines, level_markers, level)
            section_text = self.lines_to_text(section_lines)

            stamps = self._extract_stamp_requirement(section_text, grade["stamps_required"])
            if stamps is not None:
                grade["stamps_required"] = stamps

            amounts = re.findall(r"2[, ]?000", section_text)
            if amounts:
                grade["ocr_amounts_won"] = [2000] * len(amounts)

            grade["ocr_text"] = section_text
            grades.append(grade)

        if stamp_numbers:
            for grade in grades:
                if grade["stamps_required"] in stamp_numbers:
                    grade["stamps_required_ocr_confirmed"] = True

        return grades

    @staticmethod
    def _lines_for_level(
        lines: list[OcrLine],
        level_markers: list[tuple[int, float]],
        level: int,
    ) -> list[OcrLine]:
        y_start = None
        y_end = None
        for idx, (marker_level, marker_y) in enumerate(level_markers):
            if marker_level != level:
                continue
            y_start = marker_y - 20
            if idx + 1 < len(level_markers):
                y_end = level_markers[idx + 1][1] - 20
            else:
                y_end = float("inf")
            break
        if y_start is None:
            return []
        return [
            line
            for line in lines
            if y_start <= line.center_y < (y_end or float("inf"))
        ]

    @staticmethod
    def _extract_stamp_requirement(text: str, default: int) -> int | None:
        match = re.search(r"(\d+)\s*개", text)
        if match:
            return int(match.group(1))
        lone = re.search(r"(?<!\d)(5|40|80)(?!\d)", text)
        if lone:
            return int(lone.group(1))
        return default

    def parse_set_menu_banner(
        self,
        title: str,
        lines: list[OcrLine],
    ) -> dict[str, Any]:
        hints = SET_MENU_BANNER_HINTS.get(title, {})
        ocr_text = self.lines_to_text(lines)
        parsed: dict[str, Any] = {
            "ocr_text": ocr_text,
            "ocr_lines": [
                {
                    "text": line.text,
                    "confidence": round(line.confidence, 3),
                    "center_x": round(line.center_x, 1),
                    "center_y": round(line.center_y, 1),
                }
                for line in lines
            ],
        }
        parsed.update(hints)

        english_titles = re.findall(r"[A-Za-z][A-Za-z\s&-]+", ocr_text)
        if english_titles:
            parsed["ocr_title_en"] = english_titles[0].strip()

        plus_parts = re.findall(r"[^\n+]{2,30}\+[^\n+]{2,30}", ocr_text)
        if plus_parts and "composition" not in parsed:
            parsed["composition_ocr"] = plus_parts[0].strip()

        return parsed

    def enrich_set_menus(
        self,
        set_menus: list[dict[str, Any]],
        image_fetcher,
    ) -> list[dict[str, Any]]:
        enriched: list[dict[str, Any]] = []
        for item in set_menus:
            data = dict(item)
            image_url = (data.get("images") or {}).get("pc") or ""
            ocr_block: dict[str, Any] = {"image_url": image_url, "status": "skipped"}
            if image_url:
                try:
                    image_bytes = image_fetcher(image_url)
                    if self.cache_dir:
                        self.cache_dir.mkdir(parents=True, exist_ok=True)
                        suffix = Path(urlparse_name(image_url)).suffix or ".png"
                        cache_name = safe_filename(data.get("title", "set")) + suffix
                        (self.cache_dir / cache_name).write_bytes(image_bytes)
                    lines = self.ocr_image_bytes(image_bytes, scale=2.5)
                    parsed = self.parse_set_menu_banner(data.get("title", ""), lines)
                    ocr_block = {
                        "image_url": image_url,
                        "status": "ok",
                        **parsed,
                    }
                except Exception as exc:  # pragma: no cover
                    ocr_block = {
                        "image_url": image_url,
                        "status": "error",
                        "error": str(exc),
                        **SET_MENU_BANNER_HINTS.get(data.get("title", ""), {}),
                    }
            else:
                ocr_block.update(SET_MENU_BANNER_HINTS.get(data.get("title", ""), {}))
            data["banner_ocr"] = ocr_block
            enriched.append(data)
        return enriched

    def enrich_membership(
        self,
        membership: dict[str, Any],
        image_fetcher,
    ) -> dict[str, Any]:
        data = dict(membership)
        images = data.get("images") or []
        pc_image = next((url for url in images if "_pc." in url or "1280" in url), images[0] if images else "")
        grade_block: dict[str, Any] = {"image_url": pc_image, "status": "skipped"}

        if pc_image:
            try:
                image_bytes = image_fetcher(pc_image)
                if self.cache_dir:
                    self.cache_dir.mkdir(parents=True, exist_ok=True)
                    (self.cache_dir / "membership_pc.jpg").write_bytes(image_bytes)
                lines = self.ocr_image_bytes(image_bytes, scale=2.0)
                grades = self.parse_membership_grades(lines)
                grade_block = {
                    "image_url": pc_image,
                    "status": "ok",
                    "ocr_text": self.lines_to_text(lines),
                    "grades": grades,
                }
            except Exception as exc:  # pragma: no cover
                grade_block = {
                    "image_url": pc_image,
                    "status": "error",
                    "error": str(exc),
                    "grades": [dict(grade) for grade in KNOWN_MEMBERSHIP_GRADES],
                }
        else:
            grade_block["grades"] = [dict(grade) for grade in KNOWN_MEMBERSHIP_GRADES]

        data["grade_table"] = grade_block
        return data


def urlparse_name(url: str) -> str:
    return url.rsplit("/", 1)[-1]


def safe_filename(text: str) -> str:
    cleaned = re.sub(r"[^\w가-힣]+", "_", text, flags=re.UNICODE).strip("_")
    return cleaned or "image"
