/**
 * kiosk_design — 02. User Flow에 DS-01~07 프레임 7개 생성
 *
 * @see docs/design/kiosk-design-system-index.md
 * @see docs/design/kiosk-design-system-candidate-A.md … E
 * DS-05/06 hex: docs/design/color-swatches.html (SCR-001 Variables A/B 시각 비교용)
 */
const PAGE_NAME = "02. User Flow";
/** 레거시 DS frame명 (플러그인 재실행 시 제거) */
const LEGACY_DS_FRAME_NAMES = new Set([
  "DS-1 Fresh",
  "DS-2 Minimal Accent",
  "DS-3 Warm Bistro",
  "DS-4 Dark Trend",
  "DS Candidate A",
  "DS Candidate A — Fresh Greens",
  "DS Candidate B",
  "DS Candidate B — Modern Minimal",
  "DS Candidate C",
  "DS Candidate D",
  "DS Candidate D — Trend Forward",
  "DS Candidate E",
  "DS Candidate E — A+C Trend",
  "DS Trend-1",
  "DS Trend-1 — Pink-Green",
  "DS Trend-1 — Sage Coral",
  "DS Trend-4",
  "DS Trend-4 — Blush Forest",
  "DS Hybrid B×T1",
  "DS Hybrid B×T1 — Bold Pink-Lime",
  "DS Candidate F — B+Trend-1",
]);
/** SCR rename 플러그인과 동일 — User Flow로 취급하는 레거시 페이지명 */
const LEGACY_USER_FLOW_ALIASES = new Set([
  "00. Cover",
  "01. Design System",
  "05. Prototype",
  "06. Archive",
  "🎨 Design System",
  "🗑 Archive / References",
]);
const KIOSK_PAGE_NAMES = new Set([
  "03. Kiosk Screens",
  "📱 Customer",
  "Customer",
  "📐 Specs",
  "Page 1",
]);
const ADMIN_PAGE_NAMES = new Set(["04. Admin Screens", "🛠 Admin", "Admin"]);
const FRAME_WIDTH = 834;
const FRAME_HEIGHT = 1194;
const FRAME_GAP = 80;
const FONT_FAMILY = "Inter";
const FONT_STYLES = ["Regular", "Medium", "Semi Bold", "Bold", "Extra Bold"];
const fontCache = {};
/**
 * Colors sourced from candidate .md + kiosk-tokens-candidate-*.css (A~E only)
 */
const CANDIDATES = [
  {
    id: "a",
    frameName: "DS-01 Fresh Greens",
    subtitle: "회의 green #16A34A · cream · MVP 안전",
    colors: [
      { role: "Primary", hex: "#16A34A" },
      { role: "Primary Dark", hex: "#15803D" },
      { role: "Primary Light", hex: "#DCFCE7" },
      { role: "Secondary", hex: "#E8F5E9" },
      { role: "Accent Lime", hex: "#A3E635" },
      { role: "Accent Yellow", hex: "#FACC15" },
      { role: "Background", hex: "#FFFDF3" },
      { role: "Text", hex: "#1F2937" },
    ],
    typeScale: [
      { label: "Display 36/700", size: 36, weight: 700 },
      { label: "H1 32/700", size: 32, weight: 700 },
      { label: "H2 24/600", size: 24, weight: 600 },
      { label: "Body 18/400", size: 18, weight: 400 },
      { label: "Caption 14/500", size: 14, weight: 500 },
    ],
    buttonPrimary: { fill: "#16A34A", text: "#FFFFFF", label: "주문 시작하기" },
    buttonSecondary: { fill: "#FFFFFF", stroke: "#D1E7D4", text: "#1F2937", label: "장바구니" },
    bg: "#FFFDF3",
    mood: { hero: false, cornerRadius: 16, miniBtnRadius: 12 },
  },
  {
    id: "b",
    frameName: "DS-02 Modern Minimal",
    subtitle: "Charcoal + Electric Lime · Trend-3",
    colors: [
      { role: "Primary", hex: "#1A1C20" },
      { role: "Primary Light", hex: "#4A4E57" },
      { role: "Accent", hex: "#C8F135" },
      { role: "Accent Muted", hex: "#E8F5A0" },
      { role: "Background", hex: "#F0F1ED" },
      { role: "Surface", hex: "#FFFFFF" },
      { role: "Text", hex: "#1A1C20" },
      { role: "Border", hex: "#E5E7EB" },
    ],
    typeScale: [
      { label: "Display 40/800", size: 40, weight: 800 },
      { label: "H1 34/800", size: 34, weight: 800 },
      { label: "H2 24/700", size: 24, weight: 700 },
      { label: "Body 16/500", size: 16, weight: 500 },
      { label: "Caption 12/600", size: 12, weight: 600 },
    ],
    buttonPrimary: { fill: "#C8F135", text: "#1A1C20", label: "주문 시작하기" },
    buttonSecondary: { fill: "#FFFFFF", stroke: "#1A1C20", text: "#1A1C20", label: "장바구니" },
    bg: "#F0F1ED",
    mood: { hero: false, cornerRadius: 16, miniBtnRadius: 8, whiteSurface: true },
  },
  {
    id: "d",
    frameName: "DS-03 Trend Forward",
    subtitle: "Deep Forest + Mint Glass · dark · Trend-3/4",
    colors: [
      { role: "Primary", hex: "#0F2E1F" },
      { role: "Primary Dark", hex: "#081A12" },
      { role: "Accent Mint", hex: "#3DFFA8" },
      { role: "Accent Coral", hex: "#FF6B4A" },
      { role: "Accent Teal", hex: "#14B8A6" },
      { role: "Background", hex: "#F4F7F5" },
      { role: "Surface", hex: "#FFFFFF" },
      { role: "Text", hex: "#0A0F0D" },
    ],
    typeScale: [
      { label: "Display 44/800", size: 44, weight: 800 },
      { label: "H1 36/800", size: 36, weight: 800 },
      { label: "H2 26/700", size: 26, weight: 700 },
      { label: "Body 17/500", size: 17, weight: 500 },
      { label: "Caption 13/600", size: 13, weight: 600 },
    ],
    buttonPrimary: {
      gradient: true,
      fillStart: "#3DFFA8",
      fillEnd: "#14B8A6",
      fill: "#3DFFA8",
      text: "#081A12",
      label: "주문 시작하기",
    },
    buttonSecondary: { fill: "#FFFFFF", stroke: "#D4DED8", text: "#0A0F0D", label: "장바구니" },
    bg: "#F4F7F5",
    mood: { hero: false, cornerRadius: 20, miniBtnRadius: 16, whiteSurface: true },
  },
  {
    id: "e",
    frameName: "DS-04 A+C Trendy",
    subtitle: "Sage gradient + terracotta · A+C 트렌디",
    colors: [
      { role: "Primary Sage", hex: "#3D8B5F" },
      { role: "Forest", hex: "#2D6A4F" },
      { role: "Primary Light", hex: "#D4E8DC" },
      { role: "Secondary", hex: "#EDE6DB" },
      { role: "Accent Terra", hex: "#E07A5F" },
      { role: "Accent Soft", hex: "#F4A261" },
      { role: "Background", hex: "#FAF7F2" },
      { role: "Text", hex: "#2C2C2C" },
    ],
    typeScale: [
      { label: "Display 40/700", size: 40, weight: 700 },
      { label: "Menu 22/700", size: 22, weight: 700 },
      { label: "H1 32/700", size: 32, weight: 700 },
      { label: "Body 18/400", size: 18, weight: 400 },
      { label: "Caption 14/500", size: 14, weight: 500 },
    ],
    buttonPrimary: {
      gradient: true,
      fillStart: "#3D8B5F",
      fillEnd: "#2D6A4F",
      fill: "#3D8B5F",
      text: "#FFFFFF",
      label: "주문 시작하기",
    },
    buttonSecondary: { fill: "#FFFFFF", stroke: "#E5DDD3", text: "#2C2C2C", label: "장바구니" },
    bg: "#FAF7F2",
    mood: {
      hero: true,
      bg: "#F5F0E8",
      cornerRadius: 24,
      miniBtnRadius: 16,
      badgeColor: "#E07A5F",
    },
  },
  {
    id: "trend-1",
    frameName: "DS-05 Pink-Green",
    subtitle: "Vivid coral #FF5C7A→#FF4D8D gradient CTA + fresh sage #52D98A · SCR-001 Variables A",
    colors: [
      { role: "Primary Coral", hex: "#FF5C7A" },
      { role: "Hot Pink", hex: "#FF4D8D" },
      { role: "Sage", hex: "#52D98A" },
      { role: "Accent Pop", hex: "#FFD93D" },
      { role: "Sage Light", hex: "#C8F5DC" },
      { role: "Blush Tint", hex: "#FFE8F0" },
      { role: "Background", hex: "#FFFBFD" },
      { role: "Surface", hex: "#FFFFFF" },
      { role: "Text", hex: "#1E2028" },
    ],
    typeScale: [
      { label: "Display 40/800", size: 40, weight: 800 },
      { label: "H1 34/800", size: 34, weight: 800 },
      { label: "H2 26/700", size: 26, weight: 700 },
      { label: "Body 18/500", size: 18, weight: 500 },
      { label: "Caption 14/600", size: 14, weight: 600 },
    ],
    buttonPrimary: {
      gradient: true,
      fillStart: "#FF5C7A",
      fillEnd: "#FF4D8D",
      fill: "#FF5C7A",
      text: "#FFFFFF",
      label: "주문 시작하기",
    },
    buttonSecondary: { fill: "#FFFFFF", stroke: "#52D98A", text: "#1E2028", label: "장바구니" },
    bg: "#FFFBFD",
    mood: {
      hero: true,
      bg: "#FFFBFD",
      heroFill: "#FFE0EC",
      heroStroke: "#FF8CB0",
      cornerRadius: 20,
      miniBtnRadius: 14,
      badgeColor: "#FFD93D",
    },
  },
  {
    id: "trend-4",
    frameName: "DS-06 Blush Forest",
    subtitle: "Fresh forest #1B6B47 + vivid blush #FFE4EE + rose #FF6B9D · SCR-001 Variables B ⭐",
    colors: [
      { role: "Forest", hex: "#1B6B47" },
      { role: "Forest Dark", hex: "#145C3A" },
      { role: "Blush", hex: "#FFE4EE" },
      { role: "Rose", hex: "#FF6B9D" },
      { role: "Rose Soft", hex: "#FFC2D9" },
      { role: "Accent Pop", hex: "#FFD93D" },
      { role: "Background", hex: "#FFF0F7" },
      { role: "Surface", hex: "#FFFFFF" },
      { role: "Text", hex: "#145C3A" },
    ],
    typeScale: [
      { label: "Display 40/800", size: 40, weight: 800 },
      { label: "H1 34/800", size: 34, weight: 800 },
      { label: "H2 26/700", size: 26, weight: 700 },
      { label: "Body 18/500", size: 18, weight: 500 },
      { label: "Caption 14/600", size: 14, weight: 600 },
    ],
    buttonPrimary: { fill: "#1B6B47", text: "#FFFFFF", label: "주문 시작하기" },
    buttonSecondary: { fill: "#FFE4EE", stroke: "#FF6B9D", text: "#145C3A", label: "장바구니" },
    bg: "#FFF0F7",
    mood: {
      hero: true,
      bg: "#FFF0F7",
      heroFill: "#FFE4EE",
      heroStroke: "#FF6B9D",
      cornerRadius: 22,
      miniBtnRadius: 16,
      badgeColor: "#FF6B9D",
    },
  },
  {
    id: "hybrid-b-t1",
    frameName: "DS-07 Pink-Lime Hybrid",
    subtitle: "B charcoal+lime minimal · Trend-1 coral→pink CTA · 7번째 비교 프레임",
    colors: [
      { role: "Charcoal", hex: "#1A1C20" },
      { role: "Coral CTA", hex: "#FF5C7A" },
      { role: "Hot Pink", hex: "#FF4D8D" },
      { role: "Electric Lime", hex: "#C8F135" },
      { role: "Lime Muted", hex: "#E8F5A0" },
      { role: "Background", hex: "#F0F1ED" },
      { role: "Surface", hex: "#FFFFFF" },
      { role: "Text", hex: "#1A1C20" },
      { role: "Sage Pop", hex: "#52D98A" },
    ],
    typeScale: [
      { label: "Display 40/800", size: 40, weight: 800 },
      { label: "H1 34/800", size: 34, weight: 800 },
      { label: "H2 24/700", size: 24, weight: 700 },
      { label: "Body 16/500", size: 16, weight: 500 },
      { label: "Caption 12/600", size: 12, weight: 600 },
    ],
    buttonPrimary: {
      gradient: true,
      fillStart: "#FF5C7A",
      fillEnd: "#FF4D8D",
      fill: "#FF5C7A",
      text: "#FFFFFF",
      label: "주문 시작하기",
    },
    buttonSecondary: { fill: "#FFFFFF", stroke: "#C8F135", text: "#1A1C20", label: "장바구니" },
    bg: "#F0F1ED",
    mood: {
      hero: true,
      whiteSurface: true,
      heroFill: "#1A1C20",
      heroStroke: "#C8F135",
      cornerRadius: 16,
      miniBtnRadius: 8,
      badgeColor: "#C8F135",
    },
  },
];

/** Figma API expects RGB in 0–1 range, not 0–255 */
function rgb(r, g, b) {
  return { r: r / 255, g: g / 255, b: b / 255 };
}

function hexToRgb(hex) {
  const h = hex.replace("#", "");
  const n = parseInt(h, 16);
  return rgb((n >> 16) & 255, (n >> 8) & 255, n & 255);
}

function makeGradientFill(startHex, endHex) {
  return {
    type: "GRADIENT_LINEAR",
    gradientTransform: [
      [0.707, 0.707, 0],
      [-0.707, 0.707, 1],
    ],
    gradientStops: [
      { position: 0, color: { ...hexToRgb(startHex), a: 1 } },
      { position: 1, color: { ...hexToRgb(endHex), a: 1 } },
    ],
  };
}

function applyButtonFill(btn, spec) {
  if (spec.gradient && spec.fillStart && spec.fillEnd) {
    btn.fills = [makeGradientFill(spec.fillStart, spec.fillEnd)];
  } else {
    btn.fills = [{ type: "SOLID", color: hexToRgb(spec.fill) }];
  }
}

function getAllPages() {
  return figma.root.children.filter((p) => p.type === "PAGE");
}
/**
 * 02. User Flow 페이지 해석 — 새 페이지 생성 없음 (무료 3페이지 한도)
 * 1) 정확한 이름
 * 2) 레거시 별칭 (00 Cover, 01 Design System 등)
 * 3) Kiosk/Admin이 아닌 기존 페이지 이름 변경
 */
function resolveUserFlowPage() {
  const log = [];
  const pages = getAllPages();
  const exact = pages.find((p) => p.name === PAGE_NAME);
  if (exact) {
    log.push(`[페이지 사용] ${PAGE_NAME}`);
    return { page: exact, log, warnings: [] };
  }
  const legacy = pages.find((p) => LEGACY_USER_FLOW_ALIASES.has(p.name));
  if (legacy) {
    const oldName = legacy.name;
    try {
      legacy.name = PAGE_NAME;
    } catch (err) {
      const msg = err && err.message ? err.message : String(err);
      return {
        page: legacy,
        log: [`[페이지 사용] ${oldName} (이름 변경 실패: ${msg})`],
        warnings: [`페이지 이름을 "${PAGE_NAME}"으로 바꾸지 못했습니다. 수동으로 변경하세요.`],
      };
    }
    log.push(`[페이지 이름변경] ${oldName} → ${PAGE_NAME}`);
    return { page: legacy, log, warnings: [] };
  }
  const nonScr = pages.find(
    (p) => !KIOSK_PAGE_NAMES.has(p.name) && !ADMIN_PAGE_NAMES.has(p.name)
  );
  if (nonScr) {
    const oldName = nonScr.name;
    try {
      nonScr.name = PAGE_NAME;
      log.push(`[페이지 이름변경] ${oldName} → ${PAGE_NAME}`);
    } catch (err) {
      const msg = err && err.message ? err.message : String(err);
      log.push(`[페이지 사용] ${oldName} (이름 변경 실패)`);
      return {
        page: nonScr,
        log,
        warnings: [`페이지 "${oldName}"을(를) "${PAGE_NAME}"으로 바꾸지 못했습니다: ${msg}`],
      };
    }
    return { page: nonScr, log, warnings: [] };
  }
  if (pages.length > 0) {
    const fallback = pages[0];
    const oldName = fallback.name;
    try {
      fallback.name = PAGE_NAME;
      log.push(`[페이지 이름변경] ${oldName} → ${PAGE_NAME} (폴백)`);
    } catch (err) {
      const msg = err && err.message ? err.message : String(err);
      log.push(`[페이지 사용] ${oldName} (폴백, 이름 변경 실패)`);
      return {
        page: fallback,
        log,
        warnings: [`User Flow 페이지를 찾지 못해 "${oldName}"을(를) 사용합니다.`],
      };
    }
    return {
      page: fallback,
      log,
      warnings: [`"${PAGE_NAME}" 페이지가 없어 첫 페이지를 User Flow로 사용했습니다.`],
    };
  }
  throw new Error(
    "페이지가 없습니다. kiosk_design 파일을 열었는지 확인하거나 SCR Frame Rename 플러그인을 먼저 실행하세요."
  );
}
async function loadFonts() {
  const warnings = [];
  for (const style of FONT_STYLES) {
    try {
      await figma.loadFontAsync({ family: FONT_FAMILY, style });
      fontCache[style] = style;
    } catch (err) {
      const msg = err && err.message ? err.message : String(err);
      warnings.push(`폰트 ${FONT_FAMILY} ${style} 로드 실패: ${msg}`);
      console.warn(`폰트 로드 실패 (${style}):`, msg);
    }
  }
  if (!fontCache.Regular) {
    try {
      await figma.loadFontAsync({ family: FONT_FAMILY, style: "Regular" });
      fontCache.Regular = "Regular";
    } catch (err) {
      throw new Error(
        `Inter Regular 폰트를 로드할 수 없습니다. Figma Desktop에서 다시 시도하세요. (${err.message || err})`
      );
    }
  }
  return warnings;
}
function resolveFontStyle(requestedStyle) {
  if (fontCache[requestedStyle]) return fontCache[requestedStyle];
  if (fontCache.Regular) return fontCache.Regular;
  return "Regular";
}
function weightToStyle(weight) {
  if (weight >= 800) return resolveFontStyle("Extra Bold");
  if (weight >= 700) return resolveFontStyle("Bold");
  if (weight >= 600) return resolveFontStyle("Semi Bold");
  if (weight >= 500) return resolveFontStyle("Medium");
  return resolveFontStyle("Regular");
}
function createTextSafe(characters, style, fontSize, color, opacity) {
  const label = figma.createText();
  label.fontName = { family: FONT_FAMILY, style: resolveFontStyle(style) };
  label.characters = characters;
  label.fontSize = fontSize;
  const fill = { type: "SOLID", color: hexToRgb(color) };
  if (opacity !== undefined) fill.opacity = opacity;
  label.fills = [fill];
  return label;
}
function removeExistingDsFrames(page) {
  const names = new Set(CANDIDATES.map((c) => c.frameName));
  for (const legacy of LEGACY_DS_FRAME_NAMES) names.add(legacy);
  for (const child of [...page.children]) {
    if (child.type === "FRAME" && names.has(child.name)) {
      try {
        child.remove();
      } catch (err) {
        console.warn(`기존 프레임 삭제 실패 (${child.name}):`, err.message || err);
      }
    }
  }
}
function addSectionLabel(parent, text, x, y, size, color) {
  const label = createTextSafe(text, "Semi Bold", size, color);
  label.x = x;
  label.y = y;
  parent.appendChild(label);
  return label;
}
function addSwatches(parent, colors, startX, startY, textColor) {
  const swatchW = 88;
  const swatchH = 56;
  const gap = 12;
  const cols = 4;
  colors.forEach((c, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = startX + col * (swatchW + gap);
    const y = startY + row * (swatchH + 36);
    const swatch = figma.createFrame();
    swatch.name = `swatch / ${c.role}`;
    swatch.resize(swatchW, swatchH);
    swatch.x = x;
    swatch.y = y;
    swatch.fills = [{ type: "SOLID", color: hexToRgb(c.hex) }];
    swatch.cornerRadius = 8;
    if (c.hex.toUpperCase() === "#FFFFFF") {
      swatch.strokes = [{ type: "SOLID", color: hexToRgb("#E5E7EB") }];
      swatch.strokeWeight = 1;
    }
    parent.appendChild(swatch);
    const role = createTextSafe(c.role, "Medium", 11, textColor);
    role.x = x;
    role.y = y + swatchH + 4;
    parent.appendChild(role);
    const hexLabel = createTextSafe(c.hex, "Regular", 10, textColor, 0.6);
    hexLabel.x = x;
    hexLabel.y = y + swatchH + 18;
    parent.appendChild(hexLabel);
  });
}
function addTypeScale(parent, scale, startX, startY, textColor) {
  let y = startY;
  scale.forEach((t) => {
    const sample = createTextSafe(`${t.label} — 아삭하게`, weightToStyle(t.weight), t.size, textColor);
    sample.x = startX;
    sample.y = y;
    parent.appendChild(sample);
    y += t.size * 1.4 + 8;
  });
}
function addButton(parent, spec, x, y, width) {
  const height = 56;
  const btn = figma.createFrame();
  btn.name = `button / ${spec.label}`;
  btn.resize(width, height);
  btn.x = x;
  btn.y = y;
  btn.cornerRadius = spec.gradient ? 16 : 12;
  applyButtonFill(btn, spec);
  if (spec.stroke) {
    btn.strokes = [{ type: "SOLID", color: hexToRgb(spec.stroke) }];
    btn.strokeWeight = 1.5;
  }
  parent.appendChild(btn);
  const label = createTextSafe(spec.label, "Semi Bold", 18, spec.text);
  label.textAlignHorizontal = "CENTER";
  label.textAlignVertical = "CENTER";
  label.resize(width, height);
  label.x = x;
  label.y = y;
  parent.appendChild(label);
}
function buildCandidateFrame(candidate, index) {
  const frame = figma.createFrame();
  frame.name = candidate.frameName;
  frame.resize(FRAME_WIDTH, FRAME_HEIGHT);
  frame.x = index * (FRAME_WIDTH + FRAME_GAP);
  frame.y = 0;
  frame.fills = [{ type: "SOLID", color: hexToRgb(candidate.bg) }];
  frame.clipsContent = true;
  const pad = 24;
  const textEntry = candidate.colors.find((c) => c.role === "Text" || c.role.startsWith("Text"));
  const textColor = textEntry ? textEntry.hex : "#1F2937";
  const moodCfg = candidate.mood || {};
  const title = createTextSafe(candidate.frameName, "Bold", 24, textColor);
  title.x = pad;
  title.y = pad;
  frame.appendChild(title);
  const sub = createTextSafe(candidate.subtitle, "Regular", 14, textColor, 0.7);
  sub.x = pad;
  sub.y = pad + 32;
  frame.appendChild(sub);
  const spec = createTextSafe("834×1194 · touch ≥44px · Pretendard", "Regular", 12, textColor, 0.5);
  spec.x = pad;
  spec.y = pad + 54;
  frame.appendChild(spec);
  let sectionY = pad + 96;
  addSectionLabel(frame, "Colors", pad, sectionY, 16, textColor);
  addSwatches(frame, candidate.colors, pad, sectionY + 28, textColor);
  sectionY = 420;
  addSectionLabel(frame, "Typography", pad, sectionY, 16, textColor);
  addTypeScale(frame, candidate.typeScale, pad, sectionY + 28, textColor);
  sectionY = 720;
  addSectionLabel(frame, "Buttons", pad, sectionY, 16, textColor);
  const btnW = FRAME_WIDTH - pad * 2;
  addButton(frame, candidate.buttonPrimary, pad, sectionY + 32, btnW);
  addButton(frame, candidate.buttonSecondary, pad, sectionY + 32 + 56 + 16, btnW);
  const moodHeight = moodCfg.hero ? 240 : 200;
  const moodFrame = figma.createFrame();
  moodFrame.name = "mood / SCR-001 preview";
  moodFrame.resize(btnW, moodHeight);
  moodFrame.x = pad;
  moodFrame.y = sectionY + 32 + 56 + 16 + 56 + 32;
  moodFrame.cornerRadius = moodCfg.cornerRadius || 16;
  if (moodCfg.whiteSurface) {
    moodFrame.fills = [{ type: "SOLID", color: hexToRgb("#FFFFFF") }];
  } else if (moodCfg.bg) {
    moodFrame.fills = [{ type: "SOLID", color: hexToRgb(moodCfg.bg) }];
  } else {
    moodFrame.fills = [{ type: "SOLID", color: hexToRgb(candidate.bg) }];
  }
  moodFrame.strokes = [
    { type: "SOLID", color: hexToRgb(candidate.buttonSecondary.stroke || "#E5E7EB") },
  ];
  moodFrame.strokeWeight = 1;
  frame.appendChild(moodFrame);
  const moodLabel = createTextSafe("SCR-001 홈 무드 (단일 CTA)", "Medium", 12, textColor, 0.6);
  moodLabel.x = pad;
  moodLabel.y = moodFrame.y - 20;
  frame.appendChild(moodLabel);
  if (moodCfg.hero) {
    const hero = figma.createFrame();
    hero.name = "hero / bowl photo placeholder";
    hero.resize(btnW - 48, 72);
    hero.x = moodFrame.x + 24;
    hero.y = moodFrame.y + 16;
    hero.cornerRadius = 20;
    hero.fills = [{ type: "SOLID", color: hexToRgb(moodCfg.heroFill || "#EDE6DB") }];
    hero.strokes = [{ type: "SOLID", color: hexToRgb(moodCfg.heroStroke || "#E5DDD3") }];
    hero.strokeWeight = 1;
    moodFrame.appendChild(hero);
    const heroLabel = createTextSafe("fresh bowl hero", "Regular", 11, "#6B6560", 0.7);
    heroLabel.textAlignHorizontal = "CENTER";
    heroLabel.textAlignVertical = "CENTER";
    heroLabel.resize(hero.width, hero.height);
    heroLabel.x = hero.x;
    heroLabel.y = hero.y;
    frame.appendChild(heroLabel);
    const badgeColor = moodCfg.badgeColor || "#E8A0B4";
    const badge = figma.createFrame();
    badge.name = "badge / accent";
    badge.resize(36, 18);
    badge.x = hero.x + hero.width - 44;
    badge.y = hero.y + 8;
    badge.cornerRadius = 9;
    badge.fills = [{ type: "SOLID", color: hexToRgb(badgeColor) }];
    moodFrame.appendChild(badge);
    const badgeLabel = createTextSafe("NEW", "Semi Bold", 9, "#FFFFFF");
    badgeLabel.textAlignHorizontal = "CENTER";
    badgeLabel.textAlignVertical = "CENTER";
    badgeLabel.resize(36, 18);
    badgeLabel.x = badge.x;
    badgeLabel.y = badge.y;
    frame.appendChild(badgeLabel);
    const brand = createTextSafe("ASAK", "Bold", 18, textColor);
    brand.x = moodFrame.x + (btnW - 48) / 2;
    brand.y = moodFrame.y + 96;
    frame.appendChild(brand);
  }
  const miniBtn = figma.createFrame();
  miniBtn.resize(280, 48);
  miniBtn.x = pad + (btnW - 280) / 2;
  miniBtn.y = moodFrame.y + (moodCfg.hero ? 168 : 120);
  miniBtn.cornerRadius = moodCfg.miniBtnRadius || 12;
  applyButtonFill(miniBtn, candidate.buttonPrimary);
  moodFrame.appendChild(miniBtn);
  const miniLabel = createTextSafe("주문 시작하기", "Semi Bold", 16, candidate.buttonPrimary.text);
  miniLabel.textAlignHorizontal = "CENTER";
  miniLabel.textAlignVertical = "CENTER";
  miniLabel.resize(280, 48);
  miniLabel.x = miniBtn.x;
  miniLabel.y = miniBtn.y;
  frame.appendChild(miniLabel);
  return frame;
}
async function run() {
  await figma.loadAllPagesAsync();
  figma.notify("페이지 로드 완료 · DS 후보 생성 중…", { timeout: 5000 });
  try {
    figma.root.setRelaunchData({ create: "" });
  } catch (err) {
    console.warn("setRelaunchData 건너뜀 (manifest id 확인):", err.message || err);
  }
  const fontWarnings = await loadFonts();
  if (fontWarnings.length) {
    console.warn("폰트 경고:\n" + fontWarnings.join("\n"));
  }
  const { page, log, warnings } = resolveUserFlowPage();
  if (log.length) console.log("=== 페이지 해석 ===\n" + log.join("\n"));
  if (warnings.length) console.warn("페이지 경고:\n" + warnings.join("\n"));
  try {
    await figma.setCurrentPageAsync(page);
  } catch (err) {
    console.warn("currentPage 설정 실패:", err.message || err);
  }
  removeExistingDsFrames(page);
  const created = [];
  for (let i = 0; i < CANDIDATES.length; i++) {
    try {
      const frame = buildCandidateFrame(CANDIDATES[i], i);
      page.appendChild(frame);
      created.push(CANDIDATES[i].frameName);
    } catch (err) {
      const msg = err && err.message ? err.message : String(err);
      console.error(`프레임 생성 실패 (${CANDIDATES[i].frameName}):`, msg);
      throw new Error(`${CANDIDATES[i].frameName} 생성 실패: ${msg}`);
    }
  }
  if (created.length > 0) {
    try {
      figma.viewport.scrollAndZoomIntoView(
        page.children.filter((c) => created.includes(c.name))
      );
    } catch (err) {
      console.warn("뷰포트 이동 실패:", err.message || err);
    }
  }
  const summary = `DS 후보 ${created.length}개 생성: ${created.join(" · ")}`;
  const webNote = " (Desktop 권장 · 콘솔 Ctrl+Shift+I)";
  if (warnings.length > 0) {
    figma.notify(warnings[0] + " · " + summary + webNote, { error: true, timeout: 15000 });
  } else if (fontWarnings.length > 0) {
    figma.notify(summary + " · 일부 폰트 스타일 누락 (Regular로 대체)" + webNote, {
      timeout: 12000,
    });
  } else {
    figma.notify(summary + webNote, { timeout: 12000 });
  }
}
/** 즉시 피드백 + 타임아웃 폴백 + try/catch로 무응답·조용한 실패 방지 */
function main() {
  figma.notify("플러그인 시작…", { timeout: 5000 });
  const frameCount = CANDIDATES.length;
  const slowTimer = setTimeout(function () {
    figma.notify(
      `처리 중… 프레임 ${frameCount}개 생성에 20~45초 걸릴 수 있습니다. 콘솔(Ctrl+Shift+I)을 열어 두세요.`,
      { timeout: 15000 }
    );
  }, 8000);
  run()
    .catch(function (err) {
      console.error("Create DS Candidates 오류:", err);
      const msg = err && err.message ? err.message : String(err);
      figma.notify("플러그인 오류: " + msg, { error: true, timeout: 20000 });
    })
    .finally(function () {
      clearTimeout(slowTimer);
      figma.closePlugin();
    });
}
main();
