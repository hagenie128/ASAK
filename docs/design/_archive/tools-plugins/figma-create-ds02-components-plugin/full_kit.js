/**
 * ASAK Salady · DS-02 UI Kit — Y2K section layout, DS-02 tokens only.
 * Bundled into code.js before async function run().
 */

const FULL_KIT_FRAME_NAME = "ASAK Salady · DS-02 UI Kit";
const FULL_KIT_SECTION_PAD = 16;
const FULL_KIT_COL_W = 380;
const FULL_KIT_COL_GAP = 24;
const FULL_KIT_ROW_GAP = 24;

const Y2K_KIT_SECTIONS = [
  { id: "buttons", title: "Buttons" },
  { id: "segmented_c", title: "Segmented Control" },
  { id: "starring", title: "Rating / Stars" },
  { id: "notificatio", title: "Notifications" },
  { id: "badge", title: "Badge" },
  { id: "toggle", title: "Toggle" },
  { id: "text_field", title: "Text Field" },
  { id: "combobox", title: "Combobox" },
  { id: "menu", title: "Menu" },
  { id: "modal", title: "Modal" },
  { id: "card", title: "Card" },
  { id: "search", title: "Search" },
  { id: "icons", title: "Icons" },
  { id: "typography", title: "Typography" },
  { id: "shadows", title: "Shadows" },
  { id: "colour_pale", title: "Colour Palette" },
  { id: "icon_button", title: "Icon Button" },
  { id: "tooltip", title: "Tooltip" },
  { id: "progress_ba", title: "Progress Bar" },
  { id: "volume_bar", title: "Volume Bar" },
  { id: "toaster", title: "Toaster" },
  { id: "radio_check", title: "Radio + Checkboxes" },
  { id: "nav_bar", title: "Nav Bar" },
  { id: "section_tit", title: "Section Titles" },
];

const FULL_KIT_INVENTORY = { sections: 0, componentNodes: 0, sectionTitles: [] };

function resetFullKitInventory() {
  FULL_KIT_INVENTORY.sections = 0;
  FULL_KIT_INVENTORY.componentNodes = 0;
  FULL_KIT_INVENTORY.sectionTitles = [];
}

function countComponentNodes(root) {
  let n = 0;
  if (!root || root.removed) return 0;
  if (root.type === "COMPONENT" || root.type === "COMPONENT_SET") n++;
  if (root.children) {
    for (const ch of root.children) n += countComponentNodes(ch);
  }
  return n;
}

function removeExistingFullKit(page) {
  for (const child of [...page.children]) {
    if (child.type === "FRAME" && child.name === FULL_KIT_FRAME_NAME) {
      try {
        child.remove();
      } catch (_) {}
    }
  }
}

function kitSectionLabel(parent, text) {
  const lbl = createTextSafe(text, "Bold", 14, T.primary);
  lbl.x = FULL_KIT_SECTION_PAD;
  lbl.y = FULL_KIT_SECTION_PAD;
  parent.appendChild(lbl);
  return lbl;
}

function createKitSectionFrame(title) {
  const f = figma.createFrame();
  f.name = title;
  f.resize(FULL_KIT_COL_W, 200);
  f.fills = [{ type: "SOLID", color: hexToRgb(T.surface) }];
  f.cornerRadius = T.radiusMd;
  f.strokes = [{ type: "SOLID", color: hexToRgb(T.border) }];
  f.strokeWeight = 1;
  f.clipsContent = false;
  f.layoutMode = "NONE";
  kitSectionLabel(f, title);
  return f;
}

function placeInSection(section, nodes, startY) {
  let y = startY || FULL_KIT_SECTION_PAD + 28;
  let maxW = 0;
  let maxH = 0;
  for (const node of nodes) {
    if (!node) continue;
    node.x = FULL_KIT_SECTION_PAD;
    node.y = y;
    section.appendChild(node);
    const w = node.width || 200;
    const h = node.height || 48;
    maxW = Math.max(maxW, w);
    maxH = Math.max(maxH, h);
    y += h + GRID;
  }
  section.resize(FULL_KIT_COL_W, Math.max(y + FULL_KIT_SECTION_PAD, 120));
  return { w: maxW, h: y };
}

function placeGridInSection(section, nodes, cols, cellH) {
  const pad = FULL_KIT_SECTION_PAD;
  const innerW = FULL_KIT_COL_W - pad * 2;
  const gap = GRID;
  const colW = Math.floor((innerW - gap * (cols - 1)) / cols);
  let row = 0;
  let col = 0;
  let maxY = pad + 28;
  for (const node of nodes) {
    if (!node) continue;
    const nw = node.width || colW;
    const nh = node.height || cellH || 48;
    node.x = pad + col * (colW + gap);
    node.y = pad + 28 + row * ((cellH || nh) + gap);
    section.appendChild(node);
    maxY = Math.max(maxY, node.y + nh);
    col++;
    if (col >= cols) {
      col = 0;
      row++;
    }
  }
  section.resize(FULL_KIT_COL_W, maxY + pad);
}

/* ─── Kit-only component builders (sections without library equivalents) ─── */

function buildKitRatingSet() {
  const specs = [
    { Stars: "3" },
    { Stars: "4" },
    { Stars: "5" },
  ];
  const parts = specs.map((sp) => {
    const c = makeComp("rating", 200, touchSize(44));
    c.fills = [];
    const n = +sp.Stars;
    for (let i = 0; i < 5; i++) {
      const star = makeRect(c, 28, 28, i < n ? T.accent : T.border, T.radiusXs);
      star.x = i * 36;
      star.y = 8;
      appendCenteredText(star, "★", "Bold", 14, i < n ? T.primary : T.textMuted);
    }
    appendText(c, "맛 평가", "Medium", 12, T.textMuted, 0, 40);
    return c;
  });
  return combineVariantSet("DS-02 / Kit / Rating", parts, specs);
}

function buildKitNotificationSet() {
  const specs = [
    { Type: "Info", fill: T.info, icon: "i" },
    { Type: "Success", fill: T.accent, icon: "✓" },
    { Type: "Alert", fill: T.warning, icon: "!" },
  ];
  const parts = specs.map((sp) => {
    const c = makeComp("notif", 320, touchSize(56));
    c.cornerRadius = T.radiusMd;
    setSolidFill(c, T.surface);
    setStroke(c, T.border, 1);
    const dot = makeEllipse(c, 32, 32, sp.fill);
    dot.x = GRID * 2;
    dot.y = 12;
    appendCenteredText(dot, sp.icon, "Bold", 14, T.textInverse);
    appendText(c, "주문이 접수되었습니다", "Semi Bold", 14, T.text, 56, 14);
    appendText(c, "잠시만 기다려 주세요", "Medium", 12, T.textMuted, 56, 34);
    return c;
  });
  return combineVariantSet("DS-02 / Kit / Notification", parts, specs);
}

function buildKitToggleSet() {
  const specs = [
    { State: "Off" },
    { State: "On" },
  ];
  const parts = specs.map((sp) => {
    const on = sp.State === "On";
    const c = makeComp("toggle", 120, touchSize(44));
    c.fills = [];
    const track = makeRect(c, 56, 32, on ? T.primary : T.border, T.radiusPill);
    track.x = 0;
    track.y = 6;
    const knob = makeEllipse(c, 26, 26, T.surface);
    knob.x = on ? 28 : 2;
    knob.y = 9;
    setStroke(knob, T.border, 1);
    appendText(c, on ? "ON" : "OFF", "Semi Bold", 12, T.textMuted, 64, 14);
    return c;
  });
  return combineVariantSet("DS-02 / Kit / Toggle", parts, specs);
}

function buildKitTextFieldSet() {
  const specs = [
    { State: "Empty", stroke: T.border },
    { State: "Filled", stroke: T.borderStrong },
    { State: "Error", stroke: T.error },
  ];
  const parts = specs.map((sp) => {
    const c = makeComp("textfield", 280, touchSize(52));
    c.cornerRadius = T.radiusMd;
    setSolidFill(c, T.surface);
    setStroke(c, sp.stroke, sp.State === "Error" ? 2 : 1);
    const placeholder =
      sp.State === "Empty" ? "이름을 입력하세요" : sp.State === "Filled" ? "김샐러드" : "필수 입력";
    appendText(
      c,
      placeholder,
      "Medium",
      16,
      sp.State === "Empty" ? T.textMuted : sp.State === "Error" ? T.error : T.text,
      GRID * 2,
      16
    );
    if (sp.State === "Error") appendText(c, "입력이 필요합니다", "Medium", 11, T.error, GRID * 2, 36);
    return c;
  });
  return combineVariantSet("DS-02 / Kit / TextField", parts, specs);
}

function buildKitComboboxSet() {
  const specs = [
    { State: "Closed" },
    { State: "Open" },
  ];
  const parts = specs.map((sp) => {
    const c = makeComp("combobox", 240, sp.State === "Open" ? 160 : touchSize(48));
    c.cornerRadius = T.radiusMd;
    setSolidFill(c, T.surface);
    setStroke(c, T.borderStrong, 1);
    appendText(c, "매장 선택", "Semi Bold", 14, T.text, GRID * 2, 14);
    appendText(c, "▼", "Bold", 12, T.primary, 200, 16);
    if (sp.State === "Open") {
      const opts = ["강남점", "판교점", "홍대점"];
      opts.forEach((o, i) => {
        const row = makeRect(c, 224, 36, i === 0 ? T.accentMuted : T.surfaceElevated, T.radiusSm);
        row.x = 8;
        row.y = 52 + i * 40;
        appendText(c, o, "Medium", 14, T.text, 16, 60 + i * 40);
      });
    }
    return c;
  });
  return combineVariantSet("DS-02 / Kit / Combobox", parts, specs);
}

function buildKitMenuDropdownSet() {
  const specs = [
    { State: "Collapsed" },
    { State: "Expanded" },
  ];
  const parts = specs.map((sp) => {
    const h = sp.State === "Expanded" ? 200 : touchSize(48);
    const c = makeComp("menu", 220, h);
    c.cornerRadius = T.radiusMd;
    setSolidFill(c, T.surface);
    setStroke(c, T.border, 1);
    appendText(c, "메뉴", "Bold", 14, T.text, GRID * 2, 14);
    if (sp.State === "Expanded") {
      ["샐러드", "그레인볼", "음료", "쿠폰"].forEach((item, i) => {
        const row = makeRect(c, 204, 36, i === 0 ? T.primary : "transparent", T.radiusSm);
        row.x = 8;
        row.y = 48 + i * 40;
        if (i !== 0) row.fills = [];
        appendText(c, item, "Semi Bold", 14, i === 0 ? T.accent : T.text, 16, 56 + i * 40);
      });
    }
    return c;
  });
  return combineVariantSet("DS-02 / Kit / MenuDropdown", parts, specs);
}

function buildKitTooltipSet() {
  const specs = [
    { Position: "Top" },
    { Position: "Bottom" },
    { Position: "Left" },
    { Position: "Right" },
  ];
  const parts = specs.map((sp) => {
    const c = makeComp("tooltip", 160, 72);
    c.fills = [];
    const bubble = makeRect(c, 140, 36, T.primary, T.radiusSm);
    bubble.x = 10;
    bubble.y = sp.Position === "Bottom" ? 28 : 8;
    appendCenteredText(bubble, "도움말", "Semi Bold", 12, T.accent);
    const anchor = makeEllipse(c, 20, 20, T.accent);
    anchor.x = 70;
    anchor.y = sp.Position === "Top" ? 48 : sp.Position === "Bottom" ? 4 : 26;
    return c;
  });
  return combineVariantSet("DS-02 / Kit / Tooltip", parts, specs);
}

function buildKitSliderSet() {
  const specs = [
    { Value: "25" },
    { Value: "50" },
    { Value: "75" },
  ];
  const parts = specs.map((sp) => {
    const pct = +sp.Value;
    const c = makeComp("slider", 280, touchSize(48));
    c.fills = [];
    const track = makeRect(c, 240, 8, T.border, T.radiusPill);
    track.x = 20;
    track.y = 20;
    const fill = makeRect(c, (240 * pct) / 100, 8, T.accent, T.radiusPill);
    fill.x = 20;
    fill.y = 20;
    const thumb = makeEllipse(c, 28, 28, T.primary);
    thumb.x = 20 + (240 * pct) / 100 - 14;
    thumb.y = 10;
    appendText(c, "음량 " + pct + "%", "Medium", 12, T.textMuted, 20, 36);
    return c;
  });
  return combineVariantSet("DS-02 / Kit / Slider", parts, specs);
}

function buildKitShadowSet() {
  const elevations = [
    { Level: "1", y: 1, radius: 4, opacity: 0.06 },
    { Level: "2", y: 3, radius: 8, opacity: 0.08 },
    { Level: "3", y: 6, radius: 16, opacity: 0.1 },
    { Level: "4", y: 10, radius: 28, opacity: 0.14 },
  ];
  const parts = elevations.map((el) => {
    const c = makeComp("shadow", 80, 80);
    c.cornerRadius = T.radiusMd;
    setSolidFill(c, T.surface);
    c.effects = [
      {
        type: "DROP_SHADOW",
        color: { r: 0, g: 0, b: 0, a: el.opacity },
        offset: { x: 0, y: el.y },
        radius: el.radius,
        spread: 0,
        visible: true,
        blendMode: "NORMAL",
      },
    ];
    appendCenteredText(c, "E" + el.Level, "Bold", 12, T.textMuted);
    return c;
  });
  return combineVariantSet("DS-02 / Kit / Shadow", parts, elevations);
}

function buildKitColorSwatchSet() {
  const swatches = [
    { Role: "Primary", hex: T.primary },
    { Role: "Accent", hex: T.accent },
    { Role: "AccentMuted", hex: T.accentMuted },
    { Role: "Background", hex: "#F0F1ED" },
    { Role: "Surface", hex: T.surface },
    { Role: "TextMuted", hex: T.textMuted },
    { Role: "Error", hex: T.error },
    { Role: "Warning", hex: T.warning },
  ];
  const parts = swatches.map((sw) => {
    const c = makeComp("swatch", 88, 72);
    c.cornerRadius = T.radiusSm;
    setSolidFill(c, sw.hex);
    if (sw.hex === T.surface || sw.hex === "#F0F1ED") setStroke(c, T.border, 1);
    appendText(c, sw.Role, "Semi Bold", 9, sw.hex === T.primary ? T.accent : T.primary, 6, 52);
    appendText(c, sw.hex, "Regular", 8, sw.hex === T.primary ? T.accent : T.textMuted, 6, 62);
    return c;
  });
  return combineVariantSet("DS-02 / Kit / ColorSwatch", parts, swatches);
}

function buildKitButtonRowSet() {
  const specs = [
    { Label: "확인", Variant: "Accent" },
    { Label: "취소", Variant: "Ghost" },
    { Label: "메뉴", Variant: "Primary" },
    { Label: "장바구니", Variant: "Accent" },
  ];
  const parts = specs.map((sp) => {
    const c = makeComp("btn", 140, touchSize(48));
    c.cornerRadius = T.radiusMd;
    if (sp.Variant === "Accent") setSolidFill(c, T.accent);
    else if (sp.Variant === "Primary") setSolidFill(c, T.primary);
    else {
      c.fills = [];
      setStroke(c, T.borderStrong, 2);
    }
    const tc =
      sp.Variant === "Accent" ? T.primary : sp.Variant === "Primary" ? T.textInverse : T.primary;
    appendCenteredText(c, sp.Label, "Bold", 16, tc);
    return c;
  });
  return combineVariantSet("DS-02 / Kit / ButtonRow", parts, specs);
}

function buildKitIconRowComponents() {
  const labels = ["Home", "Menu", "Cart", "Search", "Check"];
  const drawers = {
    Home: drawIconHome,
    Menu: drawIconMenu,
    Cart: drawIconCart,
    Search: drawIconSearch,
    Check: drawIconCheck,
  };
  return labels.map((label) => {
    const c = makeComp("icon", touchSize(48), touchSize(48));
    c.cornerRadius = T.radiusMd;
    setSolidFill(c, T.surface);
    setStroke(c, T.border, 1);
    const inner = figma.createFrame();
    inner.resize(24, 24);
    inner.fills = [];
    inner.x = 12;
    inner.y = 12;
    c.appendChild(inner);
    drawers[label](inner, T.primary, 24);
    return registerSingle("DS-02 / Kit / Icon / " + label, c);
  });
}

function buildKitTypographyRowSet() {
  const specs = [
    { Style: "H1", text: "메뉴 선택", size: 32, weight: "Bold" },
    { Style: "H2", text: "추가 옵션", size: 24, weight: "Bold" },
    { Style: "Body", text: "신선한 채소", size: 16, weight: "Medium" },
    { Style: "Caption", text: "알레르기 정보", size: 12, weight: "Semi Bold" },
  ];
  const parts = specs.map((sp) => {
    const c = makeComp("typo", 280, 48);
    c.fills = [];
    appendText(c, sp.text, sp.weight, sp.size, T.text, 0, 8);
    return c;
  });
  return combineVariantSet("DS-02 / Kit / TypographyRow", parts, specs);
}

function buildKitOrderFlowProgressSet() {
  const steps = ["홈", "메뉴", "옵션", "장바구니", "결제"];
  const parts = steps.map((_, idx) => {
    const stepNum = idx + 1;
    const c = makeComp("orderflow", 360, 56);
    c.fills = [];
    for (let i = 0; i < 5; i++) {
      const active = i < stepNum;
      const dot = makeEllipse(c, 28, 28, active ? T.accent : T.border);
      dot.x = i * 72 + 4;
      dot.y = 6;
      if (active) appendCenteredText(dot, String(i + 1), "Bold", 11, T.primary);
      if (i < 4 && active && i < stepNum - 1) {
        const line = makeRect(c, 40, 3, T.accent, 0);
        line.x = i * 72 + 36;
        line.y = 18;
      }
    }
    appendText(c, steps[idx], "Semi Bold", 12, T.text, stepNum * 72 - 48, 40);
    return c;
  });
  const propsList = steps.map((_, i) => ({ Step: String(i + 1) }));
  return combineVariantSet("DS-02 / Kit / OrderFlowProgress", parts, propsList);
}

/* ─── Section assemblers ─── */

function sectionButtons() {
  const frame = createKitSectionFrame("Buttons");
  const nodes = [buildKitButtonRowSet(), buildButtonSet()];
  placeInSection(frame, nodes);
  return frame;
}

function sectionSegmented() {
  const frame = createKitSectionFrame("Segmented Control");
  placeInSection(frame, [buildSegmentedControlSet(), buildCategoryTabSet()]);
  return frame;
}

function sectionStarring() {
  const frame = createKitSectionFrame("Rating / Stars");
  placeInSection(frame, [buildKitRatingSet()]);
  return frame;
}

function sectionNotification() {
  const frame = createKitSectionFrame("Notifications");
  placeInSection(frame, [buildKitNotificationSet()]);
  return frame;
}

function sectionBadge() {
  const frame = createKitSectionFrame("Badge");
  placeGridInSection(frame, [buildBadgeSet(), buildQuantityBadgeSet()], 1);
  return frame;
}

function sectionToggle() {
  const frame = createKitSectionFrame("Toggle");
  placeInSection(frame, [buildKitToggleSet()]);
  return frame;
}

function sectionTextField() {
  const frame = createKitSectionFrame("Text Field");
  placeInSection(frame, [buildKitTextFieldSet()]);
  return frame;
}

function sectionCombobox() {
  const frame = createKitSectionFrame("Combobox");
  placeInSection(frame, [buildKitComboboxSet()]);
  return frame;
}

function sectionMenu() {
  const frame = createKitSectionFrame("Menu");
  placeInSection(frame, [buildKitMenuDropdownSet(), buildChipSet()]);
  return frame;
}

function sectionModal() {
  const frame = createKitSectionFrame("Modal");
  placeInSection(frame, [buildModalConfirmSet(), buildModalAlert()]);
  return frame;
}

function sectionCard() {
  const frame = createKitSectionFrame("Card");
  placeInSection(frame, [buildMenuCardSet(), buildUpsellCard(), buildOrderCompleteCard()]);
  return frame;
}

function sectionSearch() {
  const frame = createKitSectionFrame("Search");
  placeInSection(frame, [buildSearchBarSet(), buildEmptyStateSet()]);
  return frame;
}

function sectionIcons() {
  const frame = createKitSectionFrame("Icons");
  const icons = buildKitIconRowComponents();
  placeGridInSection(frame, icons, 5, touchSize(48));
  return frame;
}

function sectionTypography() {
  const frame = createKitSectionFrame("Typography");
  placeInSection(frame, [buildKitTypographyRowSet(), buildTypographySet()]);
  return frame;
}

function sectionShadows() {
  const frame = createKitSectionFrame("Shadows");
  const shadowSet = buildKitShadowSet();
  placeInSection(frame, [shadowSet]);
  return frame;
}

function sectionColourPalette() {
  const frame = createKitSectionFrame("Colour Palette");
  placeInSection(frame, [buildKitColorSwatchSet()]);
  return frame;
}

function sectionIconButton() {
  const frame = createKitSectionFrame("Icon Button");
  placeInSection(frame, [buildIconButtonSet()]);
  return frame;
}

function sectionTooltip() {
  const frame = createKitSectionFrame("Tooltip");
  placeGridInSection(frame, [buildKitTooltipSet()], 2, 72);
  return frame;
}

function sectionProgressBar() {
  const frame = createKitSectionFrame("Progress Bar");
  placeInSection(frame, [buildKitOrderFlowProgressSet(), buildProgressStepSet(), buildLoadingOverlaySet()]);
  return frame;
}

function sectionVolumeBar() {
  const frame = createKitSectionFrame("Volume Bar");
  placeInSection(frame, [buildKitSliderSet()]);
  return frame;
}

function sectionToaster() {
  const frame = createKitSectionFrame("Toaster");
  placeInSection(frame, [buildToastSet()]);
  return frame;
}

function sectionRadioCheck() {
  const frame = createKitSectionFrame("Radio + Checkboxes");
  placeInSection(frame, [buildOptionRadioSet(), buildOptionCheckboxSet()]);
  return frame;
}

function sectionNavBar() {
  const frame = createKitSectionFrame("Nav Bar");
  placeInSection(frame, [buildTopBarSet(), buildBottomBarSet()]);
  return frame;
}

function sectionSectionTitles() {
  const frame = createKitSectionFrame("Section Titles");
  placeInSection(frame, [buildSectionHeaderSet(), buildDividerSet()]);
  return frame;
}

const KIT_SECTION_BUILDERS = {
  buttons: sectionButtons,
  segmented_c: sectionSegmented,
  starring: sectionStarring,
  notificatio: sectionNotification,
  badge: sectionBadge,
  toggle: sectionToggle,
  text_field: sectionTextField,
  combobox: sectionCombobox,
  menu: sectionMenu,
  modal: sectionModal,
  card: sectionCard,
  search: sectionSearch,
  icons: sectionIcons,
  typography: sectionTypography,
  shadows: sectionShadows,
  colour_pale: sectionColourPalette,
  icon_button: sectionIconButton,
  tooltip: sectionTooltip,
  progress_ba: sectionProgressBar,
  volume_bar: sectionVolumeBar,
  toaster: sectionToaster,
  radio_check: sectionRadioCheck,
  nav_bar: sectionNavBar,
  section_tit: sectionSectionTitles,
};

function buildY2KStyleFullKit(page) {
  resetFullKitInventory();
  const master = figma.createFrame();
  master.name = FULL_KIT_FRAME_NAME;
  master.resize(4800, 3200);
  master.fills = [{ type: "SOLID", color: hexToRgb("#F0F1ED") }];
  master.clipsContent = false;
  page.appendChild(master);

  const pad = GRID * 3;
  const title = createTextSafe("ASAK Salady · DS-02 UI Kit", "Extra Bold", 28, T.primary);
  title.x = pad;
  title.y = pad;
  master.appendChild(title);
  const sub = createTextSafe(
    "Charcoal #1A1C20 + Electric Lime #C8F135 · Y2K bubbly radius · 키오스크 44px+ · 한국어 라벨",
    "Medium",
    13,
    T.textMuted
  );
  sub.x = pad;
  sub.y = pad + 36;
  master.appendChild(sub);

  const cols = 3;
  let col = 0;
  let x = pad;
  let y = pad + 72;
  let rowMaxH = 0;

  for (const sec of Y2K_KIT_SECTIONS) {
    const builder = KIT_SECTION_BUILDERS[sec.id];
    if (!builder) continue;
    const sectionFrame = builder();
    sectionFrame.x = x;
    sectionFrame.y = y;
    master.appendChild(sectionFrame);
    FULL_KIT_INVENTORY.sections++;
    FULL_KIT_INVENTORY.sectionTitles.push(sec.title);
    FULL_KIT_INVENTORY.componentNodes += countComponentNodes(sectionFrame);

    rowMaxH = Math.max(rowMaxH, sectionFrame.height);
    col++;
    if (col >= cols) {
      y += rowMaxH + FULL_KIT_ROW_GAP;
      x = pad;
      col = 0;
      rowMaxH = 0;
    } else {
      x += FULL_KIT_COL_W + FULL_KIT_COL_GAP;
    }
  }

  const finalH = y + rowMaxH + pad + 48;
  master.resize(Math.max(pad * 2 + cols * (FULL_KIT_COL_W + FULL_KIT_COL_GAP), 1200), Math.max(finalH, 800));
  return master;
}

function getFullKitSummary() {
  return {
    sections: FULL_KIT_INVENTORY.sections,
    componentNodes: FULL_KIT_INVENTORY.componentNodes,
    sectionTitles: [...FULL_KIT_INVENTORY.sectionTitles],
    targetSections: Y2K_KIT_SECTIONS.length,
  };
}

async function runFullKit() {
  await figma.loadAllPagesAsync();
  const fontWarnings = await loadFonts();
  if (fontWarnings.length) console.warn(fontWarnings.join("\n"));

  const { page, log } = resolveUserFlowPage();
  if (log.length) console.log(log.join("\n"));
  await figma.setCurrentPageAsync(page);
  removeExistingFullKit(page);

  await loadKioskIconSheet();
  const kit = buildY2KStyleFullKit(page);
  const summary = getFullKitSummary();

  figma.viewport.scrollAndZoomIntoView([kit]);
  const msg = `DS-02 UI Kit · 섹션 ${summary.sections} · 컴포넌트 ${summary.componentNodes}개`;
  figma.notify(msg, { timeout: 8000 });
  console.log("[DS-02 full kit]", JSON.stringify(summary, null, 2));
  figma.closePlugin(msg);
}
