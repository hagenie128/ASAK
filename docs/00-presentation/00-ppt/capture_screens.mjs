/**
 * ASAK PPT용 화면 캡처
 * Kiosk 1080×1920 · Admin 1920×1080
 */
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(__dirname, "screenshots");
const KIOSK = "http://localhost:5173";
const ADMIN = "http://localhost:5174";

fs.mkdirSync(OUT, { recursive: true });

async function waitOk(url, tries = 40) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url);
      if (r.status < 500) return;
    } catch {}
    await new Promise((r) => setTimeout(r, 1000));
  }
  throw new Error(`not ready: ${url}`);
}

async function shot(page, file) {
  const dest = path.join(OUT, file);
  await page.screenshot({ path: dest, fullPage: false, type: "png" });
  console.log("saved", file);
}

async function captureKiosk(browser) {
  const context = await browser.newContext({
    viewport: { width: 1080, height: 1920 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();
  page.setDefaultTimeout(15000);

  await page.goto(`${KIOSK}/`, { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(800);
  await shot(page, "kiosk-01-home.png");

  await page.getByRole("button", { name: /매장에서 먹기/ }).click();
  await page.waitForURL("**/menu**");
  await page.waitForTimeout(1200);

  // 신메뉴(231)는 메뉴 0건 → 메뉴 있는 카테고리로 직행
  await page.goto(`${KIOSK}/menu?category=236`, { waitUntil: "domcontentloaded" });
  await page.waitForSelector(".menu-card:not(.isSoldOut)", { timeout: 20000 });
  await page.waitForTimeout(800);
  await shot(page, "kiosk-02-menuList.png");

  // 옵션이 풍부한 샐러드 상세 (카테고리 233)
  await page.goto(`${KIOSK}/menu/2114?category=233`, { waitUntil: "domcontentloaded" });
  await page.waitForSelector(".menu-detail-page", { timeout: 20000 });
  await page.waitForTimeout(1200);
  await shot(page, "kiosk-03-menuDetail.png");

  // 필수 옵션 그룹의 미선택 항목 클릭
  const optionItems = page.locator(".menu-detail-options button");
  const count = await optionItems.count();
  for (let i = 0; i < Math.min(count, 8); i++) {
    const btn = optionItems.nth(i);
    if (await btn.isEnabled()) {
      try {
        await btn.click({ timeout: 1500 });
      } catch {}
    }
  }
  await page.waitForTimeout(400);

  const addBtn = page.getByRole("button", { name: /장바구니에 담기/ });
  if (await addBtn.count()) {
    if (await addBtn.isEnabled()) {
      await addBtn.click();
      await page.waitForTimeout(800);
    } else {
      console.warn("add-to-cart still disabled — go cart anyway");
    }
  }

  const checkout = page.locator(".menu-list-footer__cta");
  if (await checkout.count()) {
    try {
      await checkout.click({ timeout: 3000 });
      await page.waitForTimeout(800);
    } catch {
      await page.goto(`${KIOSK}/cart`, { waitUntil: "domcontentloaded" });
    }
  } else {
    await page.goto(`${KIOSK}/cart`, { waitUntil: "domcontentloaded" });
  }
  await page.waitForTimeout(1000);
  await shot(page, "kiosk-04-cart.png");

  await page.goto(`${KIOSK}/payment`, { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(1000);
  await shot(page, "kiosk-05-payment.png");

  await context.close();
}

async function captureAdmin(browser) {
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();
  page.setDefaultTimeout(15000);

  await page.goto(`${ADMIN}/login`, { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(600);
  await page.getByRole("button", { name: /로그인/ }).click();
  await page.waitForTimeout(1800);
  await shot(page, "admin-01-liveOrders.png");

  await page.goto(`${ADMIN}/orders`, { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(1500);
  await shot(page, "admin-02-orders.png");

  await page.goto(`${ADMIN}/menus`, { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(1800);
  await shot(page, "admin-03-menus.png");

  await context.close();
}

async function main() {
  await waitOk(KIOSK);
  await waitOk(ADMIN);
  console.log("servers ready");

  const browser = await chromium.launch({ headless: true });
  try {
    await captureKiosk(browser);
    await captureAdmin(browser);
  } finally {
    await browser.close();
  }
  console.log("done →", OUT);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
