import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from playwright.sync_api import sync_playwright
from annot import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "delivery-tracker", "img")
W = 470
shot = lambda pg, name, **kw: pg.screenshot(path=f"{OUT}/{name}.png", **kw)
R = lambda loc, n, **o: (loc, n, "right", {"bx": 432, **o})  # badge in the right-hand gutter

def card(pg, name):
    return pg.locator("article").filter(has=pg.get_by_role("heading", name=name, exact=True))

def clip_of(loc, pad=12, top=None, bottom=None):
    bb = loc.bounding_box()
    y0 = bb["y"] - pad if top is None else top
    y1 = bb["y"] + bb["height"] + pad if bottom is None else bottom
    return {"x": 0, "y": max(y0, 0), "width": W, "height": y1 - max(y0, 0)}

def page_go(pg, path):
    go(pg, path); gutter(pg)

reseed()
with sync_playwright() as p:
    b = launch(p)
    ctx = new_context(b, mobile="gutter")
    pg = login(ctx, "ali")
    page_go(pg, "/driver")

    # ---- Home ----
    hdr = pg.locator("header")
    mark(pg, [
        R(pg.get_by_role("group", name="Language"), 1),
        R(hdr.locator("div.mt-3"), 2),
        R(hdr.locator("div.mt-4"), 3),
        R(pg.locator("details.group").first.locator("xpath=preceding-sibling::*[1]"), 4),
        R(pg.locator("details.group").first.locator("> summary"), 5),
        R(pg.locator("article").first, 6),
    ])
    shot(pg, "driver-home")
    clear(pg)
    pg.add_style_tag(content="header{position:static !important}")  # close-ups: no sticky header on top

    t2 = pg.locator("details.group").nth(1).locator("> summary")
    t2.scroll_into_view_if_needed()
    mark(pg, [R(t2, 1)])
    shot(pg, "driver-trip-later", clip=clip_of(t2, pad=60))
    clear(pg)

    # ---- Out for delivery ----
    c = card(pg, "Kampung Ladang Mahsuri")
    c.scroll_into_view_if_needed()
    c.locator("details summary").click(); pg.wait_for_timeout(300)
    mark(pg, [
        R([c.get_by_role("link", name="Waze"), c.get_by_role("link", name="Call")], 1),
        R(c.locator("details"), 2),
        R(c.get_by_role("link", name="Tell customer I'm on the way"), 3),
        (c.get_by_role("button", name="Can't deliver"), 4, "bottom", {"dist": 26}),
        R(c.get_by_role("button", name="Delivered"), 5),
    ])
    shot(pg, "driver-job-on-the-way", clip=clip_of(c, pad=16, bottom=c.bounding_box()["y"] + c.bounding_box()["height"] + 50))
    clear(pg)

    # ---- Assigned: Start ----
    s = card(pg, "Medini Site Office (Block C)")
    s.scroll_into_view_if_needed()
    mark(pg, [R(s.locator("p.text-sky-700"), 1), R(s.locator("p.bg-amber-50"), 2), R(s.get_by_role("button", name="Start delivery"), 3)])
    shot(pg, "driver-job-start", clip=clip_of(s, pad=16))
    clear(pg)

    # ---- Delivered: photo + note ----
    c.get_by_role("button", name="Delivered").click()
    c.locator("input[type=file]").set_input_files(os.path.join(HERE, "do-photo.jpg"))
    c.get_by_placeholder("Received by / note (optional)").fill("Received by Pak Hamid")
    mark(pg, [R(c.locator("label", has_text="do-photo"), 1), R(c.get_by_placeholder("Received by / note (optional)"), 2), R(c.get_by_role("button", name="Confirm"), 3)])
    bb = c.bounding_box()
    shot(pg, "driver-deliver-photo", clip=clip_of(c, top=bb["y"] + bb["height"] - 330))
    clear(pg)
    c.get_by_role("button", name="Confirm").click()
    pg.wait_for_timeout(2500)
    page_go(pg, "/driver")
    pg.add_style_tag(content="header{position:static !important}")
    c = card(pg, "Kampung Ladang Mahsuri")
    c.scroll_into_view_if_needed()
    mark(pg, [R(c.locator("span", has_text="Delivered").last, 1), R(c.get_by_role("link", name="Send “delivered” WhatsApp"), 2)])
    shot(pg, "driver-delivered", clip=clip_of(c, pad=16))
    clear(pg)

    # ---- Can't deliver ----
    s = card(pg, "Medini Site Office (Block C)")
    s.get_by_role("button", name="Start delivery").click()
    pg.wait_for_timeout(2000)
    s = card(pg, "Medini Site Office (Block C)")
    s.get_by_role("button", name="Can't deliver").click()
    s.locator("select").select_option("Shop closed")
    mark(pg, [R(s.locator("select"), 1), R(s.get_by_role("button", name="Mark failed"), 2)])
    bb = s.bounding_box()
    shot(pg, "driver-cant-deliver", clip=clip_of(s, top=bb["y"] + bb["height"] - 230))
    clear(pg)
    s.get_by_role("button", name="Cancel").click()

    # ---- Bahasa Melayu ----
    pg.get_by_role("button", name="BM").click()
    pg.wait_for_timeout(1500)
    page_go(pg, "/driver")
    mark(pg, [R(pg.get_by_role("group", name="Language"), 1)])
    shot(pg, "driver-bm")
    clear(pg)
    pg.get_by_role("button", name="EN").click()
    pg.wait_for_timeout(800)
    ctx.close()

    # ---- Office sees it live ----
    d = new_context(b)
    pg = login(d, "meiling")
    go(pg, "/deliveries")
    col = pg.locator("main section").nth(3)
    k = col.locator("article").filter(has_text="Kampung Ladang Mahsuri")
    mark(pg, [(k, 1, "left", {"dist": 40})])
    bb = col.bounding_box()
    shot(pg, "office-sees-delivered", clip={"x": bb["x"] - 90, "y": bb["y"] - 10, "width": bb["width"] + 110, "height": min(bb["height"], 760) + 20})
    clear(pg)
    b.close()
print("ok")
