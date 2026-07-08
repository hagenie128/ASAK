/**
 * kiosk_design — SCR frame 일괄 이름 변경 (Figma Plugin API)
 *
 * @deprecated 패키지 사용 권장: docs/design/figma-rename-scr-plugin/
 * 실행 가이드: docs/design/figma-rename-scr-plugin/README.md
 *
 * 현재 Figma 파일 구조: 모든 FRAME이 "Page 1" 등 단일/다중 페이지에 혼재.
 */

/** 현재 Figma 레이어 이름 → SCR-XXX 목표 이름 */
const RENAME_MAP = {
  "홈 화면": "SCR-001 홈",
  "먹고가기/포장 선택": "SCR-002 먹고가기 / 포장 선택",
  "메뉴 선택": "SCR-003 메뉴 선택",
  "메뉴상세": "SCR-004 메뉴 상세 / 옵션 선택",
  "옵션 선택": "SCR-004 옵션 선택",
  "장바구니": "SCR-005 장바구니",
  "주문 확인": "SCR-006 주문 확인",
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
};

function normalizeName(name) {
  return name.replace(/\s+/g, "").toLowerCase();
}

function buildLookup() {
  const lookup = {};
  for (const [from, to] of Object.entries(RENAME_MAP)) {
    lookup[normalizeName(from)] = { from, to };
  }
  return lookup;
}

const LOOKUP = buildLookup();

function resolveTargetName(frameName) {
  if (/^SCR-\d{3}\s/.test(frameName)) {
    return { action: "skip", reason: "already_scr" };
  }
  const hit = LOOKUP[normalizeName(frameName)];
  if (hit) {
    if (frameName === hit.to) {
      return { action: "skip", reason: "already_target" };
    }
    return { action: "rename", from: hit.from, to: hit.to };
  }
  return { action: "unmatched" };
}

function getFramesOnPage(page) {
  const frames = [];
  for (const node of page.children) {
    if (node.type === "FRAME") frames.push(node);
    if (node.type === "SECTION") {
      for (const child of node.children) {
        if (child.type === "FRAME") frames.push(child);
      }
    }
  }
  return frames;
}

function getAllFrames() {
  const frames = [];
  for (const page of figma.root.children) {
    if (page.type !== "PAGE") continue;
    for (const frame of getFramesOnPage(page)) {
      frames.push({ page, frame });
    }
  }
  return frames;
}

async function run() {
  const entries = getAllFrames();
  if (entries.length === 0) {
    figma.notify("최상위 FRAME을 찾지 못했습니다. Page 1에 화면 프레임이 있는지 확인하세요.", {
      error: true,
    });
    figma.closePlugin();
    return;
  }

  const log = [];
  let renamed = 0;
  let skipped = 0;
  const unmatched = [];

  for (const { page, frame } of entries) {
    const result = resolveTargetName(frame.name);
    if (result.action === "rename") {
      const old = frame.name;
      frame.name = result.to;
      log.push(`[${page.name}] ${old} → ${result.to}`);
      renamed += 1;
    } else if (result.action === "skip") {
      skipped += 1;
    } else {
      unmatched.push(`[${page.name}] ${frame.name}`);
    }
  }

  console.log("=== SCR Frame Rename ===");
  if (log.length) console.log(log.join("\n"));
  if (unmatched.length) console.log("미매칭:\n" + unmatched.join("\n"));

  if (renamed > 0) {
    const extra =
      unmatched.length > 0 ? `, ${unmatched.length}개 미매칭(콘솔 확인)` : "";
    figma.notify(`SCR 이름 변경 완료: ${renamed}개 변경${extra}`);
  } else if (skipped > 0 && unmatched.length === 0) {
    figma.notify(`이미 SCR-XXX 형식입니다. 변경 0건 (${skipped}개 확인)`);
  } else if (unmatched.length > 0) {
    figma.notify(
      `매칭 실패: ${unmatched.length}개 FRAME 이름을 확인하세요 (콘솔 확인)`,
      { error: true }
    );
  } else {
    figma.notify("변경할 FRAME이 없습니다.", { error: true });
  }

  figma.closePlugin();
}

run();
