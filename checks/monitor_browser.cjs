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
  const formatSigned = (v, digits) => `${Number(v) > 0 ? '+' : Number(v) < 0 ? '−' : ''}${Math.abs(Number(v)).toLocaleString('en-US', {minimumFractionDigits: digits, maximumFractionDigits: digits})}`;
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
    // Use the saved, hash-verified real evidence for deterministic UI checks; live quotes still use Binance GET.
    await page.route('https://raw.githubusercontent.com/shenmuegit/EquiTide/**/research/monitor/*', route => {
      const name = new URL(route.request().url()).pathname.endsWith('latest.json') ? 'latest.json' : 'configs.json.gz';
      return route.fulfill({ status: 200, headers: { 'Access-Control-Allow-Origin': '*' }, contentType: name.endsWith('.gz') ? 'application/gzip' : 'application/json', body: fs.readFileSync(path.join(root, 'research/monitor', name)) });
    });
    await page.goto(process.env.MONITOR_URL || 'http://127.0.0.1:5178/monitor.html');
    await page.locator('.account-table tbody tr').last().waitFor({ timeout: 30000 });
    assert.equal(await page.locator('.account-table tbody tr').count(), 10);
    assert.ok((await page.locator('.metrics-strip').innerText()).includes(expectedNav));
    assert.equal(await page.locator('.segmented').count(), 0, 'cost switches remain');
    for (const account of snapshot.paper.accounts) {
      const row = page.locator('.account-table tbody tr').filter({ has: page.getByRole('button', { name: `查看 ${account.id} 详情`, exact: true }) });
      for (const cost of ['1', '2', '3']) {
        assert.equal(await row.locator(`.scenario-${cost} .scenario-return`).innerText(), formatSigned(account.scenes[cost].return_pct, 4) + '%');
        assert.equal(await row.locator(`.scenario-${cost} .scenario-pnl`).innerText(), formatSigned(account.scenes[cost].pnl, 4));
      }
    }
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
    for (const cost of ['1', '2', '3']) {
      assert.equal(await page.locator(`.research-table tbody tr .scenario-${cost} .scenario-return`).first().innerText(), formatSigned(expectedTop.scenes[cost].return_pct, 2) + '%');
    }
    assert.equal(await page.locator('.segmented').count(), 0, 'research still needs cost switching');
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
    assert.equal(await page.locator('table tbody tr').count(), snapshot.paper.trades.length);
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
    const responsive = [];
    for (const width of [320, 375, 768, 1024, 1440]) {
      await page.setViewportSize({ width, height: 900 });
      for (const view of ['模拟盘', '策略研究', '运行记录']) {
        await page.getByRole('button', { name: view, exact: true }).click();
        if (view === '模拟盘') await page.locator('.account-table tbody tr').last().waitFor();
        if (view === '策略研究') await page.locator('.research-table tbody tr').first().waitFor();
        const measured = await page.evaluate(() => ({
          document: document.documentElement.scrollWidth, viewport: innerWidth,
          tables: [...document.querySelectorAll('.table-scroll')].map(e => ({ client: e.clientWidth, scroll: e.scrollWidth })),
          contained_rows: [...document.querySelectorAll('.scenario-table tbody tr, .trade-table tbody tr')].every(row => [...row.children].every(cell => cell.getBoundingClientRect().bottom <= row.getBoundingClientRect().bottom + 1)),
          scenarios: [...document.querySelectorAll('.scenario-table tbody tr')].map(row => [...row.querySelectorAll('.scenario-cell')].filter(e => getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().width > 0).length),
        }));
        assert.ok(measured.document <= measured.viewport, `${view} document overflows at ${width}: ${JSON.stringify(measured)}`);
        assert.ok(measured.tables.every(t => t.scroll <= t.client), `${view} has an internal horizontal scroller at ${width}: ${JSON.stringify(measured)}`);
        assert.ok(measured.contained_rows, `${view} row content overlaps following rows at ${width}: ${JSON.stringify(measured)}`);
        assert.ok(measured.scenarios.every(n => n === 3), `${view} hides a scenario at ${width}`);
        responsive.push({ view, width, horizontal_scroll: false, all_scenarios_visible: true, row_content_overlaps: false });
      }
    }
    await page.setViewportSize({ width: 375, height: 812 });
    await page.getByRole('button', { name: '策略研究', exact: true }).click();
    await page.screenshot({ path: path.join(out, 'research-mobile.png'), fullPage: true });
    await page.locator('.research-table .strategy-link').first().click();
    await page.getByRole('dialog').waitFor();
    const detailWidth = await page.getByRole('dialog').evaluate(e => ({ client: e.clientWidth, scroll: e.scrollWidth }));
    assert.ok(detailWidth.scroll <= detailWidth.client, `detail dialog overflows: ${JSON.stringify(detailWidth)}`);
    assert.equal(await page.locator('.fold-costs > div').count(), 18);
    assert.equal(await page.locator('.segmented').count(), 0, 'fold details still need cost switching');
    await page.screenshot({ path: path.join(out, 'research-detail-mobile.png'), fullPage: true });
    await page.keyboard.press('Escape');
    await page.getByRole('button', { name: '模拟盘', exact: true }).click();
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
      ledger_preserved_on_failure: true, all_cost_columns_visible: true, responsive, evidence_source: 'unchanged saved real account/research records', screenshots: out };
    fs.writeFileSync(path.join(out, 'result.json'), JSON.stringify(result, null, 2) + '\n');
    console.log(JSON.stringify(result));
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
