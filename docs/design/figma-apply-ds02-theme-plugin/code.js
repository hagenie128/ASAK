/**
 * Apply DS-02 Theme — recolor duplicated Y2K UI Kit (or generated DS frames) to
 * ASAK Salady kiosk · DS-02 Modern Minimal (charcoal + electric lime).
 *
 * Run on user's copy inside kiosk_design · page `02. User Flow`.
 */
const PAGE_NAME = "02. User Flow";
const FONT_FAMILY = "Inter";
const FONT_STYLES = ["Regular", "Medium", "Semi Bold", "Bold", "Extra Bold"];

const DS02 = {
  primary: "#1A1C20",
  accent: "#C8F135",
  accentMuted: "#E8F5A0",
  background: "#F5F5F0",
  surface: "#FFFFFF",
  text: "#1A1C20",
  border: "#E5E7EB",
  warning: "#FACC15",
};

/** Exact Y2K / bubblegum hex → DS-02 */
const EXACT_MAP = {
  "#FF69B4": DS02.accent,
  "#FF1493": DS02.accent,
  "#E91E8C": DS02.accent,
  "#FF4D8D": DS02.accent,
  "#FF5C7A": DS02.accent,
  "#FF00FF": DS02.accent,
  "#Fuchsia": DS02.accent,
  "#FF85C0": DS02.accentMuted,
  "#FFB6C1": DS02.accentMuted,
  "#FFC0CB": DS02.accentMuted,
  "#FFE8F0": DS02.background,
  "#FFFBFD": DS02.background,
  "#FFF0F5": DS02.background,
  "#9B59B6": DS02.primary,
  "#8E24AA": DS02.primary,
  "#BA68C8": DS02.primaryLight || "#4A4E57",
  "#7B1FA2": DS02.primary,
  "#E040FB": DS02.accentMuted,
  "#00BCD4": DS02.border,
  "#03A9F4": DS02.border,
  "#2196F3": DS02.primary,
  "#4CAF50": DS02.accent,
  "#FFEB3B": DS02.warning,
  "#FF9800": DS02.warning,
  "#F44336": "#DC2626",
};

DS02.primaryLight = "#4A4E57";

const SEMANTIC_ROW_HEXES = [
  DS02.primary,
  DS02.accent,
  DS02.surface,
  DS02.background,
  DS02.primaryLight,
  DS02.accentMuted,
  DS02.border,
  DS02.warning,
];

const BRAND_PATTERNS = [
  [/Retro\s*Bubblegum/gi, "ASAK Salady · DS-02"],
  [/Y2K\s*UI\s*Kit/gi, "ASAK Salady · DS-02"],
  [/Bubblegum\s*UI/gi, "ASAK Salady · DS-02"],
  [/Y2K\s*Design\s*System/gi, "ASAK Salady · DS-02"],
];

const SECTION_TITLE_RE =
  /^(Foundations|Colour\s*Palette|Color\s*Palette|Typography|Shadows|Buttons|Components)$/i;

let fontsReady = false;
const fontCache = {};

function hexToRgb(hex) {
  const h = hex.replace("#", "");
  return {
    r: parseInt(h.slice(0, 2), 16) / 255,
    g: parseInt(h.slice(2, 4), 16) / 255,
    b: parseInt(h.slice(4, 6), 16) / 255,
  };
}

function rgbToHex(r, g, b) {
  const clamp = (v) => Math.max(0, Math.min(255, Math.round(v * 255)));
  return (
    "#" +
    [r, g, b]
      .map(function (c) {
        return clamp(c).toString(16).padStart(2, "0");
      })
      .join("")
      .toUpperCase()
  );
}

function paintToHex(paint) {
  if (!paint || paint.type !== "SOLID" || !paint.color) return null;
  const { r, g, b } = paint.color;
  const a = paint.opacity !== undefined ? paint.opacity : 1;
  if (a < 0.08) return null;
  return rgbToHex(r, g, b);
}

function rgbToHsl(r, g, b) {
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0;
  let s = 0;
  const l = (max + min) / 2;
  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r:
        h = (g - b) / d + (g < b ? 6 : 0);
        break;
      case g:
        h = (b - r) / d + 2;
        break;
      default:
        h = (r - g) / d + 4;
    }
    h /= 6;
  }
  return { h: h * 360, s, l };
}

function mapColorHex(hex) {
  if (!hex) return null;
  const upper = hex.toUpperCase();
  if (EXACT_MAP[upper]) return EXACT_MAP[upper];
  const rgb = hexToRgb(upper);
  const { h, s, l } = rgbToHsl(rgb.r, rgb.g, rgb.b);

  if (l > 0.94 && s < 0.12) return DS02.surface;
  if (l > 0.88 && s < 0.2) return DS02.background;

  if (s < 0.12) {
    if (l < 0.2) return DS02.primary;
    if (l < 0.45) return DS02.primaryLight;
    return DS02.border;
  }

  if (h >= 300 && h <= 360 || h >= 0 && h < 30) {
    if (l > 0.72) return DS02.accentMuted;
    if (l > 0.45) return DS02.accent;
    return DS02.primary;
  }
  if (h >= 270 && h < 300) {
    return l > 0.55 ? DS02.accentMuted : DS02.primary;
  }
  if (h >= 30 && h < 70) return l > 0.6 ? DS02.warning : DS02.accent;
  if (h >= 70 && h < 170) return l > 0.55 ? DS02.accent : DS02.accentMuted;
  if (h >= 170 && h < 250) return DS02.border;
  if (h >= 250 && h < 270) return l > 0.5 ? DS02.primaryLight : DS02.primary;

  return null;
}

function applyHexToPaint(paint, targetHex) {
  if (!paint || paint.type !== "SOLID" || !targetHex) return paint;
  const next = JSON.parse(JSON.stringify(paint));
  next.color = hexToRgb(targetHex);
  if (next.opacity !== undefined && next.opacity < 0.35) next.opacity = 0.35;
  return next;
}

function remapPaints(paints) {
  if (!paints || paints === figma.mixed || !Array.isArray(paints)) return paints;
  let changed = false;
  const out = paints.map(function (paint) {
    if (paint.type !== "SOLID" || paint.visible === false) return paint;
    const hex = paintToHex(paint);
    const mapped = mapColorHex(hex);
    if (mapped && mapped !== hex) {
      changed = true;
      return applyHexToPaint(paint, mapped);
    }
    return paint;
  });
  return changed ? out : paints;
}

async function loadFonts() {
  fontsReady = false;
  for (const style of FONT_STYLES) {
    try {
      await figma.loadFontAsync({ family: FONT_FAMILY, style });
      fontCache[style] = style;
    } catch (e) {
      console.warn("font", style, e.message || e);
    }
  }
  if (!fontCache.Regular) {
    await figma.loadFontAsync({ family: FONT_FAMILY, style: "Regular" });
    fontCache.Regular = "Regular";
  }
  fontsReady = true;
}

function resolveFontStyle(requested) {
  return fontCache[requested] || fontCache.Regular || "Regular";
}

function replaceBranding(text) {
  let out = text;
  BRAND_PATTERNS.forEach(function (pair) {
    out = out.replace(pair[0], pair[1]);
  });
  return out;
}

function styleSectionTitle(node) {
  if (!fontsReady || node.type !== "TEXT") return false;
  const t = (node.characters || "").trim();
  if (!SECTION_TITLE_RE.test(t)) return false;
  try {
    node.fontName = { family: FONT_FAMILY, style: resolveFontStyle("Extra Bold") };
    node.fontSize = Math.max(node.fontSize || 18, 16);
    node.fills = [{ type: "SOLID", color: hexToRgb(DS02.primary) }];
    return true;
  } catch (e) {
    return false;
  }
}

function isSwatchRect(node) {
  return (
    (node.type === "RECTANGLE" || node.type === "ELLIPSE") &&
    node.width >= 12 &&
    node.width <= 220 &&
    node.height >= 10 &&
    node.height <= 80
  );
}

function remapRainbowGrid(parent) {
  const rects = parent.children.filter(isSwatchRect);
  if (rects.length < 12) return 0;

  const rows = {};
  rects.forEach(function (r) {
    const key = Math.round(r.y / 8) * 8;
    if (!rows[key]) rows[key] = [];
    rows[key].push(r);
  });
  const rowKeys = Object.keys(rows)
    .map(Number)
    .sort(function (a, b) {
      return a - b;
    });
  if (rowKeys.length < 4) return 0;

  let remapped = 0;
  rowKeys.slice(0, SEMANTIC_ROW_HEXES.length).forEach(function (key, ri) {
    const row = rows[key].sort(function (a, b) {
      return a.x - b.x;
    });
    const ramp = generateShadeRamp(SEMANTIC_ROW_HEXES[ri], row.length);
    row.forEach(function (sw, si) {
      const hex = ramp[si] || SEMANTIC_ROW_HEXES[ri];
      sw.fills = [{ type: "SOLID", color: hexToRgb(hex) }];
      sw.name = "ds02-ramp / " + (ri + 1) + "-" + (si + 1);
      remapped++;
    });
  });
  return remapped;
}

function generateShadeRamp(baseHex, steps) {
  const base = hexToRgb(baseHex);
  const ramp = [];
  for (let i = 0; i < steps; i++) {
    const t = steps <= 1 ? 0 : i / (steps - 1);
    const mix = t <= 0.5 ? 1 - t * 1.6 : (t - 0.5) * 1.4;
    const toward = t <= 0.5 ? { r: 1, g: 1, b: 1 } : { r: 0, g: 0, b: 0 };
    const amt = t <= 0.5 ? (0.5 - t) * 1.75 : (t - 0.5) * 1.5;
    ramp.push(
      rgbToHex(
        base.r + (toward.r - base.r) * amt,
        base.g + (toward.g - base.g) * amt,
        base.b + (toward.b - base.b) * amt
      )
    );
  }
  return ramp;
}

const stats = {
  fills: 0,
  strokes: 0,
  texts: 0,
  titles: 0,
  swatches: 0,
};

function processNode(node) {
  if (!node || node.removed) return;

  if ("fills" in node && node.fills !== figma.mixed) {
    const next = remapPaints(node.fills);
    if (next !== node.fills) {
      node.fills = next;
      stats.fills++;
    }
  }
  if ("strokes" in node && node.strokes !== figma.mixed) {
    const next = remapPaints(node.strokes);
    if (next !== node.strokes) {
      node.strokes = next;
      stats.strokes++;
    }
  }

  if (node.type === "TEXT") {
    let changed = false;
    const replaced = replaceBranding(node.characters || "");
    if (replaced !== node.characters) {
      node.characters = replaced;
      stats.texts++;
      changed = true;
    }
    if (styleSectionTitle(node)) stats.titles++;
    if (!changed && styleSectionTitle(node)) {
      /* counted above */
    }
    const hex = paintToHex(node.fills && node.fills[0]);
    const mapped = mapColorHex(hex);
    if (mapped && mapped !== hex) {
      node.fills = [{ type: "SOLID", color: hexToRgb(mapped) }];
      stats.fills++;
    }
  }

  if (node.type === "FRAME" || node.type === "GROUP" || node.type === "COMPONENT" || node.type === "INSTANCE") {
    const name = (node.name || "").toLowerCase();
    if (name.indexOf("colour") >= 0 || name.indexOf("color") >= 0 || name.indexOf("palette") >= 0) {
      stats.swatches += remapRainbowGrid(node);
    }
    if ("children" in node) {
      for (const child of node.children) processNode(child);
    }
  } else if ("children" in node) {
    for (const child of node.children) processNode(child);
  }
}

function collectRoots(mode) {
  if (mode === "selection") {
    const sel = figma.currentPage.selection;
    if (!sel.length) {
      throw new Error("프레임 또는 섹션을 선택한 뒤 다시 실행하세요.");
    }
    return sel;
  }
  return figma.currentPage.children;
}

async function run(mode) {
  await figma.loadAllPagesAsync();
  await loadFonts();

  const page = figma.currentPage;
  if (page.name !== PAGE_NAME) {
    figma.notify(`현재 페이지: ${page.name} — 권장: ${PAGE_NAME}`, { timeout: 5000 });
  }

  stats.fills = 0;
  stats.strokes = 0;
  stats.texts = 0;
  stats.titles = 0;
  stats.swatches = 0;

  const roots = collectRoots(mode);
  roots.forEach(processNode);

  const msg =
    `DS-02 적용 — fill ${stats.fills} · stroke ${stats.strokes} · text ${stats.texts} · title ${stats.titles} · swatch ${stats.swatches}`;
  figma.notify(msg, { timeout: 8000 });
  console.log("[apply-ds02]", JSON.stringify(stats));
  figma.closePlugin(msg);
}

if (typeof figma !== "undefined" && typeof figma.on === "function") {
  figma.on("run", function (evt) {
    const cmd = evt.command || "apply-page";
    run(cmd === "apply-selection" ? "selection" : "page").catch(function (err) {
      figma.notify("오류: " + (err.message || err), { error: true });
      figma.closePlugin();
    });
  });
}

if (typeof globalThis !== "undefined" && globalThis.__APPLY_DS02_TEST__) {
  globalThis.__APPLY_DS02_EXPORTS__ = {
    DS02,
    mapColorHex,
    replaceBranding,
    paintToHex,
    generateShadeRamp,
    remapPaints,
    EXACT_MAP,
  };
}
