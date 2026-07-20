/**
 * kiosk_design — SCR 프레임 페이지 정리 + 이름 변경 (Figma Plugin API)
 *
 * Figma 무료 플랜: 페이지 최대 3개 → Notion 7페이지 구조를 3페이지로 통합
 *   02. User Flow — Cover·Design System·Prototype·Archive 요약 (수동 배치)
 *   03. Kiosk Screens — SCR-001~014, 020~021
 *   04. Admin Screens — SCR-015~019
 *
 * 1. 위 3개 페이지 해석(생성·이름변경·기존 사용) — 3페이지 한도 초과 시 생성 안 함
 * 2. SCR ID 기준 Kiosk / Admin 페이지로 이동 (구 📱 Customer / 🛠 Admin 포함)
 * 3. SCR-XXX 화면명 형식으로 이름 변경
 * 4. SCR-020·021 플레이스홀더 프레임 생성(없으면)
 *
 * documentAccess: dynamic-page → loadAllPagesAsync() 필수
 */

const PAGES = {
  USER_FLOW: "02. User Flow",
  KIOSK: "03. Kiosk Screens",
  ADMIN: "04. Admin Screens",
};

/** 플러그인이 생성·보장하는 페이지 (무료 플랜 3페이지 한도) */
const PAGE_ORDER = [PAGES.USER_FLOW, PAGES.KIOSK, PAGES.ADMIN];

/** 유료 플랜 7페이지 구조 — SCR 이동 시 레거시 소스로 취급 */
const LEGACY_EXTRA_PAGE_ALIASES = new Set([
  "00. Cover",
  "01. Design System",
  "05. Prototype",
  "06. Archive",
]);

/** 구버전 페이지명 — SCR 이동 시에도 동일하게 처리 */
const LEGACY_KIOSK_ALIASES = new Set([
  "📱 Customer",
  "Customer",
  "📐 Specs",
  "Page 1",
]);
const LEGACY_ADMIN_ALIASES = new Set(["🛠 Admin", "Admin"]);

const FRAME_WIDTH = 834;
const FRAME_HEIGHT = 1194;
const FRAME_GAP = 80;

/** 현재 Figma 레이어 이름 → SCR-XXX 목표 이름 */
const RENAME_MAP = {
  "홈 화면": "SCR-001 홈 (매장·포장)",
  "홈 (매장·포장)": "SCR-001 홈 (매장·포장)",
  "먹고가기/포장 선택": "SCR-002 먹고가기 / 포장 선택 [병합됨→001]",
  "메뉴 선택": "SCR-003 메뉴 선택",
  "메뉴상세": "SCR-004 메뉴 상세 / 옵션 선택",
  "옵션 선택": "SCR-004 옵션 선택",
  "장바구니": "SCR-005 장바구니·주문확인",
  "장바구니·주문확인": "SCR-005 장바구니·주문확인",
  "주문 확인": "SCR-006 주문 확인 [병합됨→005]",
  "결제": "SCR-007 결제",
  "주문 완료": "SCR-008 주문 완료",
  "관리자 주문관리": "SCR-009 관리자 주문 관리",
  "관리자 주문상세": "SCR-010 관리자 주문 상세",
  "관리자 판매 항목 품절처리": "SCR-011 관리자 판매 항목 품절 관리",
  "결제실패 / 재시도": "SCR-012 결제 실패 / 재시도",
  "타임아웃 안내/자동초기화": "SCR-013 타임아웃 안내 / 자동 초기화",
  "접근성 설정": "SCR-014 접근성 설정",
  "관리자 로그인": "SCR-015 관리자 로그인",
  "관리자 메뉴 관리": "SCR-016 관리자 메뉴 관리",
  "관리자 메뉴 등록/수정": "SCR-017 관리자 메뉴 등록/수정",
  "관리자 결제수단 설정": "SCR-018 관리자 결제수단 설정",
  "관리자 매출 요약": "SCR-019 관리자 매출 요약",
  "영수증 출력": "SCR-020 영수증 출력 여부 선택",
  "영수증 출력 여부 선택": "SCR-020 영수증 출력 여부 선택",
  "포인트·쿠폰 적립": "SCR-021 포인트·쿠폰 적립",
  "멤버십": "SCR-021 포인트·쿠폰 적립",
};

/** SCR-020·021 — Kiosk Screens 플레이스홀더 */
const PLACEHOLDER_TARGETS = [
  { scrId: "SCR-020", name: "SCR-020 영수증 출력 여부 선택" },
  { scrId: "SCR-021", name: "SCR-021 포인트·쿠폰 적립" },
];

const RENAME_NODE_TYPES = new Set(["FRAME", "COMPONENT"]);

function normalizeName(name) {
  return String(name)
    .replace(/[\u200b-\u200d\ufeff\u00a0]/g, "")
    .trim()
    .replace(/[／\\|]/g, "/")
    .replace(/\s*\/\s*/g, "/")
    .replace(/\s+/g, "")
    .replace(/\//g, "")
    .toLowerCase();
}

function buildLookup() {
  const exact = {};
  const entries = [];
  for (const [from, to] of Object.entries(RENAME_MAP)) {
    const key = normalizeName(from);
    exact[key] = { from, to };
    entries.push({ from, to, key });
  }
  entries.sort((a, b) => b.key.length - a.key.length);
  return { exact, entries };
}

const LOOKUP = buildLookup();

function isScrPrefixed(name) {
  return /^SCR-\d{3}(\s|$)/.test(String(name).trim());
}

/** 병합됨·Archive 대상 — 이름변경·페이지 이동 스킵 (2026-07-06 SCR-002→001, SCR-006→005) */
function isMergedOrArchivedFrame(name, pageName) {
  const trimmed = String(name).trim();
  const page = String(pageName || "").trim();
  if (/\[병합됨[→\->]/.test(trimmed) || /【병합됨/.test(trimmed)) return true;
  if (/병합됨/.test(trimmed) && /^SCR-00[26](\s|$)/.test(trimmed)) return true;
  if (/ARCHIVED/i.test(trimmed) || /\[ARCHIVE\]/i.test(trimmed)) return true;
  if (/archive/i.test(page) || page === "06. Archive" || page === "🗑 Archive / References") {
    return true;
  }
  return false;
}

/** SCR-002·006 레거시 ID — 활성 화면이 아니므로 이동·플레이스홀더 대상 제외 */
function isMergedScrId(scrId) {
  return scrId === "SCR-002" || scrId === "SCR-006";
}

/** DS-02 라이브러리·UI Kit 프레임 — SCR 화면이 아니므로 스킵 */
function isDsSkipFrame(name) {
  const trimmed = String(name).trim();
  if (trimmed === "Design System" || trimmed === "🎨 Design System") return true;
  if (/^DS\s+Candidate/i.test(trimmed)) return true;
  return false;
}

function extractScrId(name) {
  const m = String(name).trim().match(/^SCR-(\d{3})/);
  return m ? `SCR-${m[1]}` : null;
}

/** SCR ID → 목표 페이지 (figma-links.template.json · Notion 정본) */
function targetPageForScrId(scrId) {
  const num = parseInt(scrId.slice(4), 10);
  if (num >= 1 && num <= 14) return PAGES.KIOSK;
  if (num >= 15 && num <= 19) return PAGES.ADMIN;
  if (num === 20 || num === 21) return PAGES.KIOSK;
  return null;
}

function resolveTargetName(nodeName) {
  const trimmed = String(nodeName).trim();

  if (isScrPrefixed(trimmed)) {
    const scrId = extractScrId(trimmed);
    if (scrId && isMergedScrId(scrId)) {
      const mergedTarget =
        scrId === "SCR-002"
          ? "SCR-002 먹고가기 / 포장 선택 [병합됨→001]"
          : "SCR-006 주문 확인 [병합됨→005]";
      if (trimmed !== mergedTarget && !/\[병합됨/.test(trimmed)) {
        return { action: "rename", from: trimmed, to: mergedTarget, match: "merged_scr" };
      }
      return { action: "skip", reason: "merged_scr" };
    }
    return { action: "skip", reason: "already_scr" };
  }

  const norm = normalizeName(trimmed);
  const exactHit = LOOKUP.exact[norm];
  if (exactHit) {
    if (trimmed === exactHit.to) {
      return { action: "skip", reason: "already_target" };
    }
    return { action: "rename", from: exactHit.from, to: exactHit.to, match: "exact" };
  }

  for (const { from, to, key } of LOOKUP.entries) {
    if (norm.length < 2 || key.length < 2) continue;
    if (norm === key) {
      return { action: "rename", from, to, match: "normalized" };
    }
    if (norm.includes(key) || key.includes(norm)) {
      const shorter = Math.min(norm.length, key.length);
      const longer = Math.max(norm.length, key.length);
      if (shorter / longer >= 0.75) {
        return { action: "rename", from, to, match: "partial" };
      }
    }
  }

  if (isDsSkipFrame(trimmed)) {
    return { action: "skip", reason: "ds_candidate" };
  }

  return { action: "unmatched" };
}

function walkNodes(node, pageName, depth, out) {
  if (RENAME_NODE_TYPES.has(node.type)) {
    out.push({
      page: pageName,
      node,
      depth,
      type: node.type,
      name: node.name,
    });
  }
  if ("children" in node) {
    for (const child of node.children) {
      walkNodes(child, pageName, depth + 1, out);
    }
  }
}

function collectAllCandidates() {
  const candidates = [];
  for (const page of figma.root.children) {
    if (page.type !== "PAGE") continue;
    for (const child of page.children) {
      walkNodes(child, page.name, 1, candidates);
    }
  }
  return candidates;
}

const MAX_PAGES = 3;

function getAllPages() {
  return figma.root.children.filter((p) => p.type === "PAGE");
}

/**
 * 무료 플랜 3페이지 한도 대응 페이지 해석:
 * 1) 정확한 이름(02/03/04) 있으면 사용
 * 2) 3개 미만이면 createPage 시도 (실패해도 계속)
 * 3) 정확히 3개면 기존 페이지 이름 변경 (레거시명 우선 매핑 후 순서 매핑)
 * 4) 3개 초과면 경고 후 앞 3개만 사용·이름 변경
 */
function resolvePages() {
  const warnings = [];
  const log = [];
  const pageMap = {};
  const assigned = new Set();

  function refreshPages() {
    return getAllPages();
  }

  function assignPage(targetName, page, reason) {
    if (!page || assigned.has(page.id) || pageMap[targetName]) return false;
    const oldName = page.name;
    if (oldName !== targetName) page.name = targetName;
    pageMap[targetName] = page;
    assigned.add(page.id);
    log.push(
      reason === "exact"
        ? `[페이지 사용] ${targetName}`
        : `[페이지 이름변경] ${oldName} → ${targetName}`
    );
    return true;
  }

  let pages = refreshPages();

  for (const name of PAGE_ORDER) {
    const found = pages.find((p) => p.name === name);
    if (found) assignPage(name, found, "exact");
  }

  let missingTargets = PAGE_ORDER.filter((name) => !pageMap[name]);
  if (missingTargets.length === 0) {
    return { pageMap, warnings, log };
  }

  const pageCount = pages.length;

  if (pageCount < MAX_PAGES) {
    for (const name of missingTargets) {
      if (refreshPages().length >= MAX_PAGES) break;
      if (pageMap[name]) continue;
      try {
        const page = figma.createPage();
        page.name = name;
        pageMap[name] = page;
        assigned.add(page.id);
        log.push(`[페이지 생성] ${name}`);
      } catch (err) {
        const msg = err && err.message ? err.message : String(err);
        warnings.push(`페이지 "${name}" 생성 실패: ${msg}`);
        log.push(`[페이지 생성 실패] ${name}: ${msg}`);
      }
    }
    missingTargets = PAGE_ORDER.filter((name) => !pageMap[name]);
    if (missingTargets.length === 0) {
      return { pageMap, warnings, log };
    }
  }

  pages = refreshPages();
  const unassigned = pages.filter((p) => !assigned.has(p.id));

  const legacyMap = [
    { aliases: LEGACY_KIOSK_ALIASES, target: PAGES.KIOSK },
    { aliases: LEGACY_ADMIN_ALIASES, target: PAGES.ADMIN },
    { aliases: new Set([...LEGACY_EXTRA_PAGE_ALIASES, "🎨 Design System", "🗑 Archive / References"]), target: PAGES.USER_FLOW },
  ];

  for (const { aliases, target } of legacyMap) {
    if (pageMap[target]) continue;
    const hit = unassigned.find((p) => aliases.has(p.name));
    if (hit) {
      assignPage(target, hit, "rename");
      const idx = unassigned.indexOf(hit);
      if (idx >= 0) unassigned.splice(idx, 1);
    }
  }

  missingTargets = PAGE_ORDER.filter((name) => !pageMap[name]);
  const stillUnassigned = refreshPages().filter((p) => !assigned.has(p.id));

  if (missingTargets.length > 0 && stillUnassigned.length > 0) {
    if (pageCount > MAX_PAGES) {
      warnings.push(
        `페이지가 ${pageCount}개입니다 (무료 플랜 최대 ${MAX_PAGES}개). ` +
          `초과 ${pageCount - MAX_PAGES}개를 수동 삭제한 뒤 다시 실행하세요. 앞 ${MAX_PAGES}개만 사용합니다.`
      );
    } else if (pageCount === MAX_PAGES) {
      warnings.push(
        `페이지 ${MAX_PAGES}개 한도 — 새 페이지 대신 기존 페이지 이름을 02/03/04로 변경했습니다.`
      );
    }

    const renamePool =
      pageCount > MAX_PAGES
        ? refreshPages().slice(0, MAX_PAGES).filter((p) => !assigned.has(p.id))
        : stillUnassigned;

    let poolIdx = 0;
    for (const targetName of missingTargets) {
      if (pageMap[targetName]) continue;
      const page = renamePool[poolIdx++];
      if (page) assignPage(targetName, page, "rename");
    }
  }

  const finalMissing = PAGE_ORDER.filter((name) => !pageMap[name]);
  if (finalMissing.length > 0) {
    warnings.push(
      `목표 페이지 없음: ${finalMissing.join(", ")}. ` +
        `수동으로 페이지 이름을 02/03/04로 맞추거나 불필요한 페이지를 삭제하세요.`
    );
  }

  return { pageMap, warnings, log };
}

/** pageMap에 없을 때 SCR 이동용 최선의 페이지 */
function fallbackPageForScr(scrId, pageMap) {
  const targetName = targetPageForScrId(scrId);
  if (targetName && pageMap[targetName]) return pageMap[targetName];

  const pages = getAllPages();
  if (targetName === PAGES.KIOSK) {
    return (
      pages.find((p) => LEGACY_KIOSK_ALIASES.has(p.name)) ||
      pages.find((p) => p.name === PAGES.KIOSK) ||
      pages[1] ||
      pages[0] ||
      null
    );
  }
  if (targetName === PAGES.ADMIN) {
    return (
      pages.find((p) => LEGACY_ADMIN_ALIASES.has(p.name)) ||
      pages.find((p) => p.name === PAGES.ADMIN) ||
      pages[2] ||
      pages[pages.length - 1] ||
      null
    );
  }
  return pages[0] || null;
}

function getPageByName(name) {
  return figma.root.children.find((p) => p.type === "PAGE" && p.name === name) || null;
}

function moveNodeToPage(node, targetPage) {
  if (!targetPage || node.parent === targetPage) return false;
  targetPage.appendChild(node);
  return true;
}

function collectBoundsOnPage(page) {
  const bounds = [];
  function walk(node) {
    if (RENAME_NODE_TYPES.has(node.type)) {
      bounds.push({ x: node.x, y: node.y, w: node.width, h: node.height });
    }
    if ("children" in node) {
      for (const child of node.children) walk(child);
    }
  }
  for (const child of page.children) walk(child);
  return bounds;
}

function nextPlaceholderPosition(page) {
  const bounds = collectBoundsOnPage(page);
  if (bounds.length === 0) return { x: 0, y: 0 };
  let maxRight = 0;
  let minY = 0;
  for (const b of bounds) {
    maxRight = Math.max(maxRight, b.x + b.w);
    minY = Math.min(minY, b.y);
  }
  return { x: maxRight + FRAME_GAP, y: minY };
}

async function createPlaceholderFrame(page, name, position) {
  const frame = figma.createFrame();
  frame.name = name;
  frame.resize(FRAME_WIDTH, FRAME_HEIGHT);
  frame.x = position.x;
  frame.y = position.y;
  frame.fills = [{ type: "SOLID", color: { r: 1, g: 0.992, b: 0.953 } }];
  frame.strokes = [{ type: "SOLID", color: { r: 0.82, g: 0.82, b: 0.82 } }];
  frame.strokeWeight = 2;
  frame.dashPattern = [12, 8];
  page.appendChild(frame);

  try {
    await figma.loadFontAsync({ family: "Inter", style: "Regular" });
    const label = figma.createText();
    label.characters = name + "\n(플레이스홀더 — 디자인 추가)";
    label.fontSize = 28;
    label.fills = [{ type: "SOLID", color: { r: 0.4, g: 0.4, b: 0.4 } }];
    label.textAlignHorizontal = "CENTER";
    label.textAlignVertical = "CENTER";
    label.resize(FRAME_WIDTH - 64, FRAME_HEIGHT - 64);
    label.x = 32;
    label.y = FRAME_HEIGHT / 2 - 60;
    frame.appendChild(label);
  } catch (_err) {
    // 폰트 없으면 빈 프레임만 생성
  }

  return frame;
}

function isLegacySourcePage(pageName) {
  return (
    LEGACY_KIOSK_ALIASES.has(pageName) ||
    LEGACY_ADMIN_ALIASES.has(pageName) ||
    LEGACY_EXTRA_PAGE_ALIASES.has(pageName) ||
    pageName === "🎨 Design System" ||
    pageName === "🗑 Archive / References"
  );
}

function notifySummary(renamed, moved, placeholders, skippedScr, dsSkip, unmatched, pageWarnings) {
  const dsHint = dsSkip > 0 ? ` · DS후보 스킵 ${dsSkip}` : "";
  const unmatchedHint =
    unmatched.length > 0 ? ` · 미매칭 ${unmatched.length}` : "";
  const summary =
    `이름 ${renamed} · 이동 ${moved} · 생성 ${placeholders} · SCR스킵 ${skippedScr}${dsHint}${unmatchedHint}`;
  const webNote =
    " (Desktop 권장 · Web에서도 이름변경·이동 가능 · 콘솔 Ctrl+Shift+I)";
  const allScrOk =
    renamed === 0 &&
    moved === 0 &&
    placeholders === 0 &&
    skippedScr > 0 &&
    unmatched.length === 0;

  if (pageWarnings.length > 0) {
    const pageHint = pageWarnings[0];
    const workDone = renamed > 0 || moved > 0 || placeholders > 0;
    figma.notify(
      pageHint +
        (workDone ? ` · ${summary}` : " — 프레임 정리는 계속 진행됨") +
        webNote,
      { error: true, timeout: 15000 }
    );
    return;
  }

  if (renamed > 0 || moved > 0 || placeholders > 0) {
    figma.notify(summary + webNote, { timeout: 12000 });
  } else if (allScrOk) {
    const dsNote = dsSkip > 0 ? ` · DS후보 스킵 ${dsSkip}` : "";
    figma.notify(`이미 SCR 형식 (${skippedScr}개 확인)${dsNote}` + webNote, {
      timeout: 8000,
    });
  } else if (unmatched.length > 0) {
    figma.notify(summary + " — 콘솔(Ctrl+Shift+I) 확인" + webNote, {
      error: true,
      timeout: 12000,
    });
  } else {
    figma.notify(
      "FRAME/COMPONENT 없음 — 03. Kiosk Screens 등 화면 페이지를 확인하세요." + webNote,
      { error: true, timeout: 8000 }
    );
  }
}

async function run() {
  await figma.loadAllPagesAsync();
  figma.notify("페이지 로드 완료 · 스캔 중…", { timeout: 4000 });

  try {
    figma.root.setRelaunchData({ rename: "" });
  } catch (err) {
    console.warn("setRelaunchData 건너뜀 (manifest id 확인):", err.message || err);
  }

  await figma.loadFontAsync({ family: "Inter", style: "Regular" }).catch(() => {});

  const { pageMap, warnings: pageWarnings, log: pageLog } = resolvePages();
  const kioskPage = pageMap[PAGES.KIOSK] || fallbackPageForScr("SCR-001", pageMap);
  const adminPage = pageMap[PAGES.ADMIN] || fallbackPageForScr("SCR-015", pageMap);

  if (pageLog.length) console.log("=== 페이지 해석 ===\n" + pageLog.join("\n"));
  if (pageWarnings.length) console.warn("페이지 경고:\n" + pageWarnings.join("\n"));

  const candidates = collectAllCandidates();
  const log = [];
  let renamed = 0;
  let skippedScr = 0;
  let skippedTarget = 0;
  let dsSkip = 0;
  let moved = 0;
  let placeholders = 0;
  const unmatched = [];
  const renamedById = new Set();

  for (const { page, node, name } of candidates) {
    if (renamedById.has(node.id)) continue;

    if (isMergedOrArchivedFrame(name, page)) {
      skippedScr += 1;
      log.push(`[스킵] [${page}] ${name} (병합됨/Archive)`);
      renamedById.add(node.id);
      continue;
    }

    const result = resolveTargetName(name);
    if (result.action === "rename") {
      const old = node.name;
      node.name = result.to;
      renamedById.add(node.id);
      renamed += 1;
      log.push(`[이름] [${page}] ${old} → ${result.to} (${result.match})`);
    } else if (result.action === "skip") {
      if (result.reason === "already_scr") skippedScr += 1;
      else if (result.reason === "merged_scr") skippedScr += 1;
      else if (result.reason === "ds_candidate") dsSkip += 1;
      else skippedTarget += 1;
    } else {
      unmatched.push(`${page}/${name} (${node.type})`);
    }
  }

  const refreshed = collectAllCandidates();
  const scrIdsPresent = new Set();

  for (const { page, node, name } of refreshed) {
    const scrId = extractScrId(name);
    if (!scrId) continue;
    scrIdsPresent.add(scrId);

    if (isMergedOrArchivedFrame(name, page) || isMergedScrId(scrId)) {
      continue;
    }

    const targetPageName = targetPageForScrId(scrId);
    if (!targetPageName) continue;

    const targetPage =
      (targetPageName === PAGES.KIOSK ? kioskPage : adminPage) ||
      fallbackPageForScr(scrId, pageMap);
    const currentPage = getPageByName(page);
    if (currentPage && targetPage && currentPage !== targetPage) {
      if (moveNodeToPage(node, targetPage)) {
        const legacy = isLegacySourcePage(page) ? " (구 페이지)" : "";
        moved += 1;
        log.push(`[이동] ${scrId}: ${page} → ${targetPage.name}${legacy}`);
      }
    }
  }

  const placeholderPage = kioskPage || getAllPages()[0];
  if (placeholderPage) {
    for (const { scrId, name } of PLACEHOLDER_TARGETS) {
      if (scrIdsPresent.has(scrId)) continue;

      const pos = nextPlaceholderPosition(placeholderPage);
      try {
        await createPlaceholderFrame(placeholderPage, name, pos);
        placeholders += 1;
        scrIdsPresent.add(scrId);
        log.push(`[생성] ${scrId} 플레이스홀더 @ ${placeholderPage.name} (${pos.x}, ${pos.y})`);
      } catch (err) {
        log.push(`[생성 실패] ${scrId}: ${err.message || err}`);
      }
    }
  }

  console.log("=== SCR Frame Rename (무료 플랜 3페이지) — 결과 ===");
  console.log(
    `발견 ${candidates.length}개 · 이름변경 ${renamed} · 이동 ${moved} · 플레이스홀더 ${placeholders} · SCR스킵 ${skippedScr} · DS후보 스킵 ${dsSkip}`
  );
  if (log.length) console.log(log.join("\n"));
  if (dsSkip > 0) console.log(`DS후보 스킵 ${dsSkip}개 (SCR 화면 아님)`);
  if (unmatched.length) console.log("미매칭:\n" + unmatched.join("\n"));

  notifySummary(renamed, moved, placeholders, skippedScr, dsSkip, unmatched, pageWarnings);
}

/** 즉시 피드백 + 타임아웃 폴백 + try/catch로 무응답·조용한 실패 방지 */
function main() {
  figma.notify("플러그인 시작…", { timeout: 5000 });

  const slowTimer = setTimeout(function () {
    figma.notify(
      "처리 중… 페이지가 많으면 1~2분 걸릴 수 있습니다. 콘솔(Ctrl+Shift+I)을 열어 두세요.",
      { timeout: 15000 }
    );
  }, 8000);

  run()
    .catch(function (err) {
      console.error("SCR Frame Rename 오류:", err);
      const msg = err && err.message ? err.message : String(err);
      figma.notify("플러그인 오류: " + msg, { error: true, timeout: 20000 });
    })
    .finally(function () {
      clearTimeout(slowTimer);
      figma.closePlugin();
    });
}

main();
