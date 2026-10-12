import html, json
from pathlib import Path

R = Path(__file__).resolve().parent
d = json.loads((R / "report.json").read_text())
entries = [(5, "RSI≤5"), (10, "RSI≤10"), (15, "RSI≤15")]
lookbacks = [100, 150, 200]
W, H = 1120, 790
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<rect width="100%" height="100%" fill="#101820"/>',
       '<style>text{font-family:Arial,sans-serif;fill:#edf2f4}.small{font-size:13px}.head{font-size:20px;font-weight:bold}.title{font-size:26px;font-weight:bold}</style>',
       '<text x="32" y="42" class="title">Cost-adjusted net return sensitivity · repeated-history OOS</text>']
colors = {"BTC": "#47c9b0", "ETH": "#ffbf69"}
panel_w, panel_h, cell_w, cell_h = 510, 315, 135, 70
for ai, asset in enumerate(("BTC", "ETH")):
    x0 = 32 + ai * 545
    for mi, mult in enumerate(("1", "2", "3")):
        y0 = 84 + mi * 220
        svg.append(f'<text x="{x0}" y="{y0}" class="head" fill="{colors[asset]}">{asset} · {mult}× costs</text>')
        for ri, (cut, lab) in enumerate(entries):
            for ci, sma in enumerate(lookbacks):
                name = f"cutler_rsi2_{asset.lower()}_entry{cut}_sma{sma}"
                val = d["configs"][name]["scenarios"][mult]["net_return_pct"]
                # Diverging palette around zero, with the sign obvious even in grayscale.
                positive = val >= 0
                intensity = min(1.0, abs(val) / 12.0)
                if positive:
                    fill = f"rgb({int(25+25*intensity)},{int(90+110*intensity)},{int(75+75*intensity)})"
                else:
                    fill = f"rgb({int(90+110*intensity)},{int(45+10*intensity)},{int(55+15*intensity)})"
                x, y = x0 + ci * cell_w, y0 + 14 + ri * cell_h
                svg.append(f'<rect x="{x}" y="{y}" width="{cell_w-5}" height="{cell_h-5}" rx="4" fill="{fill}" stroke="#d9e2e8" stroke-width="1"/>')
                svg.append(f'<text x="{x+10}" y="{y+27}" class="small">{html.escape(lab)}</text>')
                svg.append(f'<text x="{x+10}" y="{y+49}" class="head">{val:+.2f}%</text>')
        for ci, sma in enumerate(lookbacks):
            svg.append(f'<text x="{x0+ci*cell_w+15}" y="{y0+14+3*cell_h+12}" class="small">SMA {sma}d</text>')
svg.append('<text x="32" y="775" class="small">Entry uses RSI(2) Cutler ≤ threshold; exit at RSI≥50 or close≤trend SMA. Green: positive; red: negative. Values are net after modeled fees, spread, slippage and square-root impact.</text>')
svg.append('</svg>')
(R / "sensitivity_surface.svg").write_text("\n".join(svg) + "\n")
