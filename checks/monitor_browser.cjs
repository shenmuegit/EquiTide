/* Run against the local monitor preview; no account or exchange writes. */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const zlib = require('node:zlib');

(async () => {
  const root = path.resolve(__dirname, '..');
  const out = process.env.MONITOR_QA_DIR || path.join(root, 'data/runs/monitor-qa');
  fs.mkdirSync(out, { recursive: true });
  const snapshot = JSON.parse(fs.readFileSync(path.join(root, 'research/monitor/latest.json')));
  const research = JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(root, 'research/monitor/configs.json.gz'))));
  const expectedNav = Number(snapshot.paper.totals['1'].nav).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
  const expectedTop = research.filter(r => r.kind === 'combination' && r.capital_usdt === 2000 && r.start_utc === '2026-03-18T00:01:00Z' && r.end_utc === '2026-09-14T00:01:00Z').sort((a,b) => b.scenes['3'].return_pct - a.scenes['3'].return_pct)[0];
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROMIUM_PATH, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1080 }, deviceScaleFactor: 1, colorScheme: 'dark', reducedMotion: 'reduce' });
  const errors = [];
  const quotes = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', async response => {
    if (response.url().includes('/ticker/bookTicker') && response.ok()) quotes.push(await response.json());
  });
  try {
    await page.goto(process.env.MONITOR_URL || 'http://127.0.0.1:5178/monitor.html');
    await page.locator('.account-table tbody tr').last().waitFor({ timeout: 30000 });
    assert.equal(await page.locator('.account-table tbody tr').count(), 10);
    assert.ok((await page.locator('.metrics-strip').innerText()).includes(expectedNav));
    const costTabs = page.getByRole('tablist', { name: '成本情景', exact: true });
    await costTabs.getByRole('tab', { name: '3× 成本', exact: true }).click();
    const stressNav = Number(snapshot.paper.totals['3'].nav).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    assert.ok((await page.locator('.metrics-strip').innerText()).includes(stressNav));
    await costTabs.getByRole('tab', { name: '1× 主账户', exact: true }).click();
    await costTabs.getByRole('tab', { name: '1× 主账户', exact: true }).focus();
    await page.keyboard.press('ArrowRight');
    assert.equal(await costTabs.getByRole('tab', { name: '2× 成本', exact: true }).getAttribute('aria-selected'), 'true');
    await costTabs.getByRole('tab', { name: '1× 主账户', exact: true }).click();
    await page.locator('.quote-value').first().waitFor();
    await page.waitForFunction(() => [...document.querySelectorAll('.quote-value')].every(e => /\d/.test(e.textContent)), { timeout: 20000 });
    await page.screenshot({ path: path.join(out, 'paper-desktop.png'), fullPage: true });
    await page.getByRole('button', { name: '切换浅色主题', exact: true }).click();
    await page.screenshot({ path: path.join(out, 'paper-desktop-light.png'), fullPage: true });
    await page.getByRole('button', { name: '切换深色主题', exact: true }).click();
    await page.getByRole('button', { name: '查看 P02 详情', exact: true }).click();
    await page.getByRole('dialog').waitFor();
    const expectedEth = Number(snapshot.paper.accounts.find(a => a.id === 'P02').scenes['1'].positions.ETH.units).toFixed(8);
    assert.ok((await page.getByRole('dialog').innerText()).includes(expectedEth));
    await page.keyboard.press('Escape');
    await page.getByRole('button', { name: '策略研究', exact: true }).click();
    await page.locator('.research-table tbody tr').first().waitFor({ timeout: 30000 });
    assert.equal(await page.locator('.research-table tbody tr').count(), 25);
    assert.ok((await page.locator('.research-table tbody tr').first().innerText()).includes(expectedTop.scenes['3'].return_pct.toFixed(2) + '%'));
    await page.getByRole('searchbox', { name: '搜索技术指标、参数或权重', exact: true }).fill('EMA29');
    assert.ok(await page.locator('.research-table tbody tr').count() > 0);
    assert.match(await page.locator('.research-table tbody tr').first().innerText(), /EMA29/);
    await page.getByRole('searchbox', { name: '搜索技术指标、参数或权重', exact: true }).fill('');
    await page.getByRole('combobox', { name: '验证筛选' }).selectOption('rejected');
    assert.match(await page.locator('.research-table tbody tr').first().innerText(), /未通过/);
    await page.locator('.research-table .strategy-link').first().click();
    assert.match(await page.getByRole('dialog').innerText(), /未通过的预注册条件/);
    assert.equal(await page.locator('.fold-grid > div').count(), 6);
    await page.keyboard.press('Escape');
    await page.getByRole('combobox', { name: '验证筛选' }).selectOption('all');
    await page.screenshot({ path: path.join(out, 'research-desktop.png'), fullPage: true });
    await page.getByRole('button', { name: '运行记录', exact: true }).click();
    assert.equal(await page.locator('table tbody tr').count(), snapshot.paper.trades.filter(t => t.cost_multiplier === 1).length);
    assert.match(await page.locator('.provenance').innerText(), new RegExp(snapshot.paper.state_sha256));
    await page.getByRole('button', { name: '模拟盘', exact: true }).click();
    await page.setViewportSize({ width: 375, height: 812 });
    await page.waitForFunction(() => document.documentElement.scrollWidth <= innerWidth, { timeout: 5000 });
    await page.screenshot({ path: path.join(out, 'paper-mobile.png'), fullPage: true });
    const layout = await page.evaluate(() => ({ width: innerWidth, scroll: document.documentElement.scrollWidth,
      offenders: [...document.querySelectorAll('*')].filter(e => e.getBoundingClientRect().right > innerWidth + 1)
        .slice(0, 8).map(e => ({ tag: e.tagName, class: String(e.className), right: e.getBoundingClientRect().right })) }));
    assert.ok(layout.scroll <= layout.width, `mobile document overflows: ${JSON.stringify(layout)}`);
    await page.getByRole('button', { name: '切换浅色主题', exact: true }).click();
    await page.screenshot({ path: path.join(out, 'paper-mobile-light.png'), fullPage: true });
    await page.getByRole('button', { name: '切换深色主题', exact: true }).click();
    // Preserve ledger and quote values when requests fail; never present zero equity.
    await page.route('**/latest.json', route => route.fulfill({ status: 503, body: 'Unavailable' }));
    await page.route('**/api/v3/ticker/bookTicker?**', route => route.fulfill({ status: 503, body: '{}' }));
    await page.getByRole('button', { name: '立即刷新', exact: true }).click();
    await page.getByRole('alert').waitFor();
    assert.ok((await page.locator('.metrics-strip').innerText()).includes(expectedNav));
    assert.equal(await page.locator('.account-table tbody tr').count(), 10);
    await page.getByRole('button', { name: '暂停自动刷新', exact: true }).click();
    const requestsBefore = quotes.length;
    await page.waitForTimeout(11000);
    assert.equal(quotes.length, requestsBefore, 'pause still polls quotes');
    assert.equal(errors.length, 0, errors.join('\n'));
    assert.ok(quotes.some(q => q.symbol === 'BTCUSDT') && quotes.some(q => q.symbol === 'ETHUSDT'), 'live public quotes not observed');
    const result = { ok: true, accounts: 10, research_rows_per_page: 25, paper_state_sha256: snapshot.paper.state_sha256,
      actual_public_quote_responses: quotes.length, browser_errors: errors, mobile_overflow: false,
      ledger_preserved_on_failure: true, screenshots: out };
    fs.writeFileSync(path.join(out, 'result.json'), JSON.stringify(result, null, 2) + '\n');
    console.log(JSON.stringify(result));
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
