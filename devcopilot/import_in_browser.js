/**
 * DevCopilot 시나리오 일괄 입력 스크립트
 *
 * 사용법:
 * 1. https://devcopilot.ai.kr/workspace/2/scenarios 에 로그인(Admin)
 * 2. F12 → Console 탭
 * 3. 이 파일 전체를 복사해서 붙여넣고 Enter
 * 4. importAllScenarios() 실행 (또는 importMvpOnly() 로 MVP만)
 *
 * 주의: 진행 중 브라우저 탭을 닫지 마세요.
 */

const SCENARIOS = /* JSON_DATA_START */ null; /* JSON_DATA_END - 아래 loadScenariosFromJson() 사용 권장 */

async function loadScenariosFromJson() {
  // scenarios_import.json 내용을 아래 배열에 붙여넣거나,
  // 로컬에서 fetch로 불러올 수 없으므로 generate_browser_script.py 로 재생성하세요.
  throw new Error(
    "SCENARIOS 데이터가 비어 있습니다. python devcopilot/generate_browser_script.py 를 실행한 뒤\n" +
      "생성된 import_in_browser.generated.js 를 사용하세요."
  );
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function setReactInputValue(el, value) {
  if (!el) return false;
  const proto =
    el.tagName === "TEXTAREA"
      ? window.HTMLTextAreaElement.prototype
      : window.HTMLInputElement.prototype;
  const setter = Object.getOwnPropertyDescriptor(proto, "value")?.set;
  if (setter) setter.call(el, value);
  else el.value = value;
  el.dispatchEvent(new Event("input", { bubbles: true }));
  el.dispatchEvent(new Event("change", { bubbles: true }));
  el.dispatchEvent(new Event("blur", { bubbles: true }));
  return true;
}

function findFieldByLabel(partialLabel) {
  const labels = [...document.querySelectorAll("label")];
  const label = labels.find((l) =>
    l.textContent.replace(/\s+/g, " ").trim().includes(partialLabel)
  );
  if (!label) return null;

  if (label.htmlFor) {
    const byId = document.getElementById(label.htmlFor);
    if (byId) return byId;
  }

  const container = label.closest("div")?.parentElement || label.parentElement;
  const input = container?.querySelector("input, textarea, select");
  if (input) return input;

  return label.parentElement?.querySelector("input, textarea, select") || null;
}

function clickButtonByText(...texts) {
  const buttons = [...document.querySelectorAll("button, a, [role='button']")];
  const btn = buttons.find((b) => {
    const t = b.textContent.replace(/\s+/g, " ").trim();
    return texts.some((x) => t === x || t.includes(x));
  });
  if (btn) {
    btn.click();
    return true;
  }
  return false;
}

async function fillScenarioForm(scenario) {
  const fields = [
    ["시나리오 ID", scenario.scenarioId],
    ["시나리오 제목", scenario.title],
    ["시작 조건", scenario.preCondition],
    ["종료 조건", scenario.postCondition],
    ["기본 흐름", scenario.normalFlow],
    ["예외 흐름", scenario.alternativeFlow],
    ["Mermaid", scenario.mermaid],
  ];

  for (const [label, value] of fields) {
    const el = findFieldByLabel(label);
    if (!el) {
      console.warn(`[경고] 필드를 찾지 못함: ${label}`);
      continue;
    }
    setReactInputValue(el, value ?? "");
    await sleep(80);
  }

  // 상태 선택 (DRAFT / APPROVED)
  const status = (scenario.status || "DRAFT").toUpperCase();
  const statusButtons = [...document.querySelectorAll("button, label, span")];
  const statusEl = statusButtons.find((el) => {
    const t = el.textContent.replace(/\s+/g, " ").trim();
    return t.includes(status) || t.includes(status === "DRAFT" ? "임시" : "검토완료");
  });
  if (statusEl) statusEl.click();

  await sleep(200);
}

async function saveCurrentScenario() {
  const saved =
    clickButtonByText("저장", "등록", "추가 완료", "Save") ||
    clickButtonByText("확인");
  if (!saved) console.warn("[경고] 저장 버튼을 찾지 못했습니다. 수동으로 저장해 주세요.");
  await sleep(1200);
}

async function importScenarios(scenarios, { startIndex = 0 } = {}) {
  if (!scenarios?.length) {
    console.error("시나리오 데이터가 없습니다.");
    return;
  }

  console.log(`총 ${scenarios.length}개 시나리오 입력 시작 (index ${startIndex})`);

  for (let i = startIndex; i < scenarios.length; i++) {
    const s = scenarios[i];
    console.log(`[${i + 1}/${scenarios.length}] ${s.scenarioId} - ${s.title}`);

    // 새 시나리오 추가
    const added = clickButtonByText("추가", "새 시나리오", "New");
    if (!added) {
      console.error("추가 버튼을 찾지 못했습니다. 시나리오 목록 탭이 열려 있는지 확인하세요.");
      break;
    }
    await sleep(800);

    await fillScenarioForm(s);
    await saveCurrentScenario();
    await sleep(500);
  }

  console.log("완료!");
}

// MVP 우선 시나리오 ID (10일 MVP 기준)
const MVP_IDS = new Set([
  "SC-001", "SC-002", "SC-003", "SC-004", "SC-005",
  "SC-007", "SC-008", "SC-009", "SC-012", "SC-014",
]);

async function importAllScenarios(data) {
  const list = data || (typeof SCENARIOS !== "undefined" && SCENARIOS) || null;
  if (!list) await loadScenariosFromJson();
  return importScenarios(list);
}

async function importMvpOnly(data) {
  const list = (data || SCENARIOS || []).filter((s) => MVP_IDS.has(s.scenarioId));
  return importScenarios(list);
}

console.log(
  "DevCopilot import 준비됨.\n" +
    "- 전체: importAllScenarios(SCENARIOS)\n" +
    "- MVP만: importMvpOnly(SCENARIOS)\n" +
    "※ SCENARIOS 변수에 JSON 배열을 먼저 붙여넣거나 generated 파일을 사용하세요."
);
