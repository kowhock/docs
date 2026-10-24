import os
"""Screenshot helpers: log in, then draw numbered callouts with arrows onto the live page before capturing."""
import subprocess
from playwright.sync_api import Page

BASE = "http://localhost:3000"
STACK = os.path.dirname(os.path.abspath(__file__))

def reseed():
    subprocess.run(["psql", "-h", "127.0.0.1", "-U", "postgres", "-d", "kh", "-q", "-c",
        "truncate auth.users, public.lorries, public.sales_orders, public.sync_status cascade; alter sequence public.do_no_seq restart with 1;"], check=True)
    sql = subprocess.run(["node", f"{STACK}/seed.js"], capture_output=True, text=True, check=True).stdout
    subprocess.run(["psql", "-h", "127.0.0.1", "-U", "postgres", "-d", "kh", "-q", "-v", "ON_ERROR_STOP=1"], input=sql, text=True, check=True, capture_output=True)

def new_context(browser, mobile=False):
    common = dict(locale="en-MY", timezone_id="Asia/Kuala_Lumpur", device_scale_factor=2)
    if mobile:
        return browser.new_context(viewport={"width": 470 if mobile == "gutter" else 390, "height": 844}, is_mobile=True, has_touch=True, **common)
    return browser.new_context(viewport={"width": 1440, "height": 900}, **common)
 
def login(ctx, user):
    pg = ctx.new_page()
    pg.goto(BASE + "/login")
    pg.wait_for_load_state("networkidle")
    if pg.locator("input[name=login]:visible").count():
        pg.locator("input[name=login]:visible").fill(user)
    else:
        pg.locator("#login").fill(user)
        pg.get_by_role("button", name="Office staff? Use password").click()
    pg.locator("input[name=password]:visible").fill("demo")
    pg.locator("input[name=password]:visible").press("Enter")
    pg.wait_for_url(lambda u: "/login" not in u, timeout=20000)
    return pg

def go(pg: Page, path):
    pg.goto(BASE + path)
    pg.wait_for_load_state("networkidle")
    pg.wait_for_timeout(400)

JS = r"""
(items) => {
  document.querySelectorAll('.kh-annot').forEach(e => e.remove());
  const C = '#f97316';
  const layer = document.createElement('div');
  layer.className = 'kh-annot';
  const dlgs = document.querySelectorAll('dialog[open]');
  const host = dlgs.length ? dlgs[dlgs.length-1] : document.body;
  if (dlgs.length) { host.style.overflow = 'visible'; Object.assign(layer.style, {position:'fixed', left:0, top:0, width:'100vw', height:'100vh', pointerEvents:'none', zIndex: 2147483647}); }
  else Object.assign(layer.style, {position:'absolute', left:0, top:0, width:'100%', height: document.documentElement.scrollHeight+'px', pointerEvents:'none', zIndex: 2147483647});
  const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
  svg.setAttribute('width','100%'); svg.setAttribute('height','100%');
  svg.style.position='absolute'; svg.style.inset='0'; svg.style.overflow='visible';
  svg.innerHTML = `<defs><marker id="khArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="${C}"/></marker></defs>`;
  layer.appendChild(svg);
  for (const it of items) {
    const {x, y, w, h} = it.box; const pad = it.pad ?? 4;
    const r = document.createElementNS(svg.namespaceURI, 'rect');
    Object.entries({x:x-pad, y:y-pad, width:w+2*pad, height:h+2*pad, rx:8, fill:'none', stroke:C, 'stroke-width':3}).forEach(([k,v])=>r.setAttribute(k,v));
    if (!it.noBox) svg.appendChild(r);
    const d = it.dist ?? 56;
    const cx = x + w/2, cy = y + h/2;
    let bx, by, tx, ty;
    if (it.side === 'left')   { bx = x - pad - d; by = cy; tx = x - pad - 3; ty = cy; }
    if (it.side === 'right')  { bx = x + w + pad + d; by = cy; tx = x + w + pad + 3; ty = cy; }
    if (it.side === 'top')    { bx = cx; by = y - pad - d; tx = cx; ty = y - pad - 3; }
    if (it.side === 'bottom') { bx = cx; by = y + h + pad + d; tx = cx; ty = y + h + pad + 3; }
    if (it.dx) bx += it.dx; if (it.dy) by += it.dy;
    if (it.bx != null) bx = it.bx; if (it.by != null) by = it.by;
    const R = 15;
    const len = Math.hypot(tx-bx, ty-by) || 1;
    const sx = bx + (tx-bx)/len*R, sy = by + (ty-by)/len*R;
    const line = document.createElementNS(svg.namespaceURI, 'line');
    Object.entries({x1:sx, y1:sy, x2:tx, y2:ty, stroke:C, 'stroke-width':3, 'marker-end':'url(#khArrow)', 'stroke-linecap':'round'}).forEach(([k,v])=>line.setAttribute(k,v));
    if (len > R + 6) svg.appendChild(line);
    const b = document.createElement('div');
    b.textContent = it.n;
    Object.assign(b.style, {position:'absolute', left:(bx-R)+'px', top:(by-R)+'px', width:2*R+'px', height:2*R+'px', borderRadius:'50%', background:C, color:'#fff', font:'700 16px/30px system-ui, sans-serif', textAlign:'center', boxShadow:'0 0 0 3px #fff, 0 2px 8px rgba(0,0,0,.35)'});
    layer.appendChild(b);
  }
  host.appendChild(layer);
}
"""

def mark(pg: Page, items):
    """items: (locator, number, side, extra-options dict?)"""
    scroll = pg.evaluate("() => document.querySelector('dialog[open]') ? [0, 0] : [window.scrollX, window.scrollY]")
    data = []
    for it in items:
        loc, n, side = it[0], it[1], it[2]
        opts = it[3] if len(it) > 3 else {}
        if isinstance(loc, list):  # several locators → one box around them all
            bs = [l.bounding_box() for l in loc]
            x0 = min(b["x"] for b in bs); y0 = min(b["y"] for b in bs)
            bb = {"x": x0, "y": y0, "width": max(b["x"] + b["width"] for b in bs) - x0, "height": max(b["y"] + b["height"] for b in bs) - y0}
        else:
            bb = loc.bounding_box()
        if not bb:
            raise RuntimeError(f"no box for callout {n}")
        data.append({"box": {"x": bb["x"] + scroll[0], "y": bb["y"] + scroll[1], "w": bb["width"], "h": bb["height"]}, "n": n, "side": side, **opts})
    pg.evaluate(JS, data)

def clear(pg: Page):
    pg.evaluate("() => document.querySelectorAll('.kh-annot').forEach(e => e.remove())")

def space(pg: Page, loc, bottom=0, top=0):
    """Push content apart so callouts have room (screenshot only)."""
    loc.evaluate(f"e => {{ e.style.marginBottom = '{bottom}px'; e.style.marginTop = '{top}px'; }}")

def launch(p):
    return p.chromium.launch(args=["--lang=en-GB"], env={**os.environ, "LANG": "en_GB.UTF-8", "LANGUAGE": "en_GB"})

GUTTER_CSS = "html{width:390px !important;} body{overflow-x:visible !important} html,body{background:#fff}"
def gutter(pg: Page):
    """Phone page drawn 390px wide with an empty strip on the right for callouts."""
    pg.add_style_tag(content=GUTTER_CSS)
    pg.wait_for_timeout(200)
