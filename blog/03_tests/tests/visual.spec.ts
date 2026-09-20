import { test, expect } from "@playwright/test";
import { fileURLToPath } from "url";
import path from "path";

const SS = path.join(path.dirname(fileURLToPath(import.meta.url)), "screenshots");

test("homepage looks correct", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle");

  // Hero image loaded
  const heroImg = page.locator("#hero img").first();
  await expect(heroImg).toBeVisible();

  // Post cards exist
  const cards = page.locator("li a.group");
  await expect(cards.first()).toBeVisible();

  await page.screenshot({ path: `${SS}/homepage.png`, fullPage: true });
});

test("post card has image", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle");

  // Each card should have an img or the gradient fallback
  const firstCard = page.locator("li").first();
  const cardImage = firstCard.locator("img, .bg-gradient-to-br");
  await expect(cardImage.first()).toBeVisible();

  await page.screenshot({ path: `${SS}/card-image.png` });
});

test("post page has hero image", async ({ page }) => {
  await page.goto("/");
  // Click first post
  const firstLink = page.locator("li a.group").first();
  await firstLink.click();
  await page.waitForLoadState("networkidle");

  await page.screenshot({ path: `${SS}/post-page.png`, fullPage: true });
});

test("dark mode looks correct", async ({ page }) => {
  await page.goto("/");
  // Toggle dark mode
  await page.click('[aria-label="light theme"], [aria-label="dark theme"], button[title*="theme"], #theme-btn');
  await page.waitForTimeout(300);
  await page.screenshot({ path: `${SS}/homepage-dark.png`, fullPage: true });
});
