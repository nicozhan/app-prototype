#!/usr/bin/env python3
"""Generate 1:1 HTML replica from Figma JSON."""
import json, html, math

data = json.load(open('/Users/qian2/WorkBuddy/2026-10-18-08-05-28/figma_file.json'))
assets = json.load(open('/Users/qian2/WorkBuddy/2026-10-18-08-05-28/asset_map.json'))
doc = data['document']
OUT = '/Users/qian2/WorkBuddy/2026-10-18-08-05-28'

def rgba(c, op=1.0):
    r = round(c.get('r', 0) * 255); g = round(c.get('g', 0) * 255); b = round(c.get('b', 0) * 255)
    a = c.get('a', 1) * op
    if a >= 0.999:
        return f"rgb({r},{g},{b})"
    return f"rgba({r},{g},{b},{round(a,3)})"

def fill_css(f, w, h):
    t = f.get('type')
    if not f.get('visible', True):
        return None
    if t == 'SOLID':
        return f"background-color:{rgba(f['color'], f.get('opacity',1))};"
    if t == 'GRADIENT_RADIAL':
        hp = f['gradientHandlePositions']; stops = f['gradientStops']
        cx, cy = hp[0]['x'] * w, hp[0]['y'] * h
        rx = math.hypot((hp[1]['x'] - hp[0]['x']) * w, (hp[1]['y'] - hp[0]['y']) * h)
        if len(hp) > 2:
            ry = math.hypot((hp[2]['x'] - hp[0]['x']) * w, (hp[2]['y'] - hp[0]['y']) * h)
        else:
            ry = rx
        s = ','.join(f"{rgba(st['color'])} {st['position']*100:.1f}%" for st in stops)
        return f"background:radial-gradient({rx:.1f}px {ry:.1f}px at {cx:.1f}px {cy:.1f}px,{s});"
    if t == 'IMAGE':
        fn = assets.get(_cur_id)
        if fn:
            return f"background-image:url('{fn}');background-size:cover;background-position:center;"
    return None

def shadow_css(n):
    parts = []
    for s in n.get('strokes') or []:
        if s.get('visible', True) and s.get('type') == 'SOLID':
            wt = n.get('strokeWeight', 1)
            col = rgba(s['color'], s.get('opacity', 1))
            align = n.get('strokeAlign', 'INSIDE')
            if align == 'INSIDE':
                parts.append(f"inset 0 0 0 {wt:.2f}px {col}")
            else:
                parts.append(f"0 0 0 {wt:.2f}px {col}")
    for e in n.get('effects') or []:
        if e.get('type') == 'DROP_SHADOW' and e.get('visible', True):
            c = e['color']; off = e.get('offset', {})
            rad = e.get('radius', 0); sp = e.get('spread') or 0
            parts.append(f"{off.get('x',0):.2f}px {off.get('y',0):.2f}px {rad:.2f}px {sp:.2f}px {rgba(c)}")
    if parts:
        return "box-shadow:" + ",".join(parts) + ";"
    return ""

def radius_css(n, w, h):
    r = n.get('cornerRadius')
    if not r:
        return ""
    if r * 2 >= min(w, h) - 1:
        return "border-radius:9999px;"
    return f"border-radius:{r:.2f}px;"

FONT_MAP = {'Inter': 'Inter', 'Outfit': 'Outfit'}

def style_to_css(st, color_css):
    fam = st.get('fontFamily', 'Inter')
    fs = st.get('fontSize', 14)
    fw = st.get('fontWeight', 400)
    ls = st.get('letterSpacing', 0)
    css = f"font-family:'{FONT_MAP.get(fam, fam)}',sans-serif;font-size:{fs:.2f}px;font-weight:{fw};"
    if ls:
        css += f"letter-spacing:{ls:.2f}px;"
    lh = st.get('lineHeightPx')
    if st.get('lineHeightUnit') == 'PIXELS' and lh:
        css += f"line-height:{lh:.2f}px;"
    elif st.get('lineHeightPercentFontSize'):
        css += f"line-height:{st['lineHeightPercentFontSize']:.2f}%;"
    if color_css:
        css += f"color:{color_css};"
    return css

def text_color(st_fills, node_fills):
    for f in (st_fills or node_fills or []):
        if f.get('type') == 'SOLID' and f.get('visible', True):
            return rgba(f['color'], f.get('opacity', 1))
    return None

def text_html(n):
    st = n.get('style', {})
    chars = n.get('characters', '')
    table = n.get('styleOverrideTable') or {}
    over = n.get('characterStyleOverrides') or []
    base_color = text_color(None, n.get('fills'))
    align = {'LEFT':'left','CENTER':'center','RIGHT':'right','JUSTIFIED':'justify'}.get(st.get('textAlignHorizontal','LEFT'),'left')
    ws = "white-space:nowrap;" if (st.get('textAutoResize') == 'WIDTH_AND_HEIGHT' and '\n' not in chars) else "white-space:pre-wrap;"
    css = style_to_css(st, base_color) + f"text-align:{align};{ws}overflow:visible;"
    # build spans
    out = []
    run = ""
    run_oid = None
    def flush():
        nonlocal run, run_oid
        if run == "":
            return
        if run_oid is None:
            out.append(html.escape(run))
        else:
            ost = table.get(str(run_oid)) or table.get(run_oid) or {}
            merged_color = text_color(ost.get('fills'), None) or base_color
            m = dict(st); m.update({k: v for k, v in ost.items() if k != 'fills'})
            out.append(f"<span style=\"{style_to_css(m, merged_color)}\">{html.escape(run)}</span>")
        run = ""
    for i, ch in enumerate(chars):
        oid = over[i] if i < len(over) else 0
        oid = oid if oid else None
        if oid != run_oid and run:
            flush()
        run_oid = oid
        run += ch
    flush()
    return css, "".join(out)

def render_node(n, px, py, out):
    """Nested rendering; coordinates relative to parent bbox origin (px, py)."""
    if n.get('visible') is False:
        return
    bb = n.get('absoluteBoundingBox')
    if not bb:
        return
    x = bb['x'] - px; y = bb['y'] - py; w = bb['width']; h = bb['height']
    t = n.get('type')
    pos = f"position:absolute;left:{x:.2f}px;top:{y:.2f}px;width:{w:.2f}px;height:{h:.2f}px;"
    op = n.get('opacity')
    opcss = f"opacity:{op:.3f};" if op is not None and op < 0.999 else ""
    global _cur_id
    _cur_id = n['id']
    if t == 'TEXT':
        css, inner = text_html(n)
        out.append(f"<div style=\"{pos}{css}{opcss}\">{inner}</div>\n")
        return
    if t == 'VECTOR':
        fn = assets.get(n['id'])
        if fn:
            out.append(f"<img src=\"{fn}\" style=\"{pos}{opcss}display:block;\" alt=\"\">\n")
        return
    # FRAME / RECTANGLE
    fills = n.get('fills') or []
    bg = ""
    for f in fills:
        c = fill_css(f, w, h)
        if c:
            bg += c
    css = pos + bg + shadow_css(n) + radius_css(n, w, h) + opcss
    clip = n.get('clipsContent', True) if t == 'FRAME' else False
    if clip:
        css += "overflow:hidden;"
    child_list = []
    for c in n.get('children') or []:
        render_node(c, bb['x'], bb['y'], child_list)
    children = "".join(child_list)
    out.append(f"<div style=\"{css}\">{children}</div>\n")

def render_screen(frame):
    bb = frame['absoluteBoundingBox']
    ox, oy, w, h = bb['x'], bb['y'], bb['width'], bb['height']
    bg = ""
    for f in frame.get('fills') or []:
        c = fill_css(f, w, h)
        if c:
            bg += c
    inner_list = []
    for c in frame.get('children') or []:
        render_node(c, ox, oy, inner_list)
    inner = "".join(inner_list)
    return w, h, f"<div class=\"screen\" style=\"width:{w:.2f}px;height:{h:.2f}px;{bg}\">{inner}</div>"

HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VendSolution App - 1:1 复刻</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Outfit:wght@500&display=swap" rel="stylesheet">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:'Inter',sans-serif; background:#c9cddb; -webkit-font-smoothing:antialiased; }
  .screen { position:relative; overflow:hidden; flex-shrink:0; }
</style>
</head>
<body>
"""

frames = []
for page in doc['children']:
    for f in page['children']:
        if f['type'] == 'FRAME':
            frames.append(f)

order = {'Login': 0, 'restock-': 1, 'restock4': 2, 'my-': 3}
def sortkey(f):
    for k, v in order.items():
        if f['name'].startswith(k):
            return v
    return 9
frames.sort(key=sortkey)

slugs = {}
for f in frames:
    slug = {'Login':'login','restock-':'restock','restock4':'restock-done','my-':'my'}[[k for k in order if f['name'].startswith(k)][0]]
    slugs[f['id']] = (slug, f['name'])

# individual pages
for f in frames:
    slug, name = slugs[f['id']]
    w, h, screen = render_screen(f)
    page = HEAD.replace('<title>VendSolution App - 1:1 复刻</title>', f'<title>{html.escape(name)}</title>')
    page += f"{screen}\n</body></html>"
    open(f"{OUT}/{slug}.html", "w").write(page)
    print("wrote", slug + ".html", f"{w:.0f}x{h:.0f}")

# index with all four side by side
idx = HEAD
idx += """<div style="padding:48px 32px;">
<h1 style="font:800 28px Inter,sans-serif;color:#0B102F;margin-bottom:8px;">VendSolution 补货 App — Figma 1:1 HTML 复刻</h1>
<p style="font:400 14px Inter,sans-serif;color:#697095;margin-bottom:32px;">按 Figma 源文件样式、颜色、字体、坐标像素级复刻 · 共 4 屏</p>
<div style="display:flex;gap:32px;align-items:flex-start;overflow-x:auto;padding-bottom:24px;">
"""
for f in frames:
    slug, name = slugs[f['id']]
    w, h, screen = render_screen(f)
    idx += f"<div><div style=\"font:600 13px Inter,sans-serif;color:#697095;margin-bottom:10px;\">{html.escape(name)} · {w:.0f}×{h:.0f} · <a href=\"{slug}.html\" style=\"color:#2434C8;\">单独打开</a></div>{screen}</div>\n"
idx += "</div></div>\n</body></html>"
open(f"{OUT}/index.html", "w").write(idx)
print("wrote index.html")
