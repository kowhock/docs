import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from playwright.sync_api import sync_playwright
from annot import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "delivery-tracker", "img")
os.makedirs(OUT, exist_ok=True)
shot = lambda pg, name, **kw: pg.screenshot(path=f"{OUT}/{name}.png", **kw)

reseed()
with sync_playwright() as p:
    b = launch(p)

    # ---- Sign in (phone: username + PIN) ----
    m = new_context(b, mobile=True)
    pg = m.new_page(); go(pg, "/login")
    pg.locator("#login").fill("ali")
    for k in "381": pg.get_by_role("button", name=k, exact=True).click()
    dots = pg.locator("[aria-label$='digits entered'] span")
    mark(pg, [(pg.locator("#login"), 1, "top", {"dx": 110, "dist": 40}),
              ([dots.first, dots.last], 2, "left", {"dist": 50}),
              (pg.locator("div.grid.grid-cols-3"), 3, "left", {"dist": 30}),
              (pg.get_by_role("button", name="Office staff? Use password"), 4, "bottom", {"dist": 40})])
    shot(pg, "login-phone")
    m.close()
    # ---- Sign in (computer) ----
    d = new_context(b)
    pg = d.new_page(); go(pg, "/login")
    mark(pg, [(pg.locator("input[name=login]:visible"), 1, "left", {"dist": 60}),
              (pg.locator("input[name=password]:visible"), 2, "left", {"dist": 60})])
    shot(pg, "login-computer")
    d.close()

    ctx = new_context(b)
    pg = login(ctx, "meiling")

    # ---- Deliveries overview ----
    go(pg, "/deliveries")
    bar = pg.locator("div.card").first
    space(pg, bar, bottom=60)
    mark(pg, [
        (pg.locator("header nav"), 1, "right", {"dist": 50}),
        (bar.locator("nav").first, 2, "bottom", {"dist": 50}),
        (pg.get_by_role("link", name="Show O/C"), 3, "bottom", {"dist": 50}),
        (pg.get_by_role("link", name="Cross-branch"), 4, "bottom", {"dist": 50}),
        (bar.locator("nav").nth(1), 5, "bottom", {"dist": 50}),
        (bar.locator("form").first.locator("select, input[type=date], button"), 6, "bottom", {"dist": 50}) if False else (bar.locator("form").first, 6, "bottom", {"dist": 50, "dx": 60}),
        (pg.get_by_placeholder("🔍 Search DO no."), 7, "bottom", {"dist": 50}),
        (pg.get_by_role("link", name="+ Special DO"), 8, "left", {"dist": 50}),
        ([pg.locator("main section h2").nth(0), pg.locator("main section h2").nth(4)], 9, "left", {"dist": 40}),
    ])
    shot(pg, "deliveries-overview")
    clear(pg)

    # ---- One card: assign driver / date / time ----
    card = pg.locator("main section").nth(0).locator("article").first
    card.scroll_into_view_if_needed()
    sel = card.locator("select")
    mark(pg, [
        (card.locator("button").first, 1, "left", {"dist": 40}),
        (sel.nth(0), 2, "left", {"dist": 40}),
        (sel.nth(1), 3, "left", {"dist": 40}),
        (sel.nth(2), 4, "left", {"dist": 40}),
    ])
    box = card.bounding_box()
    shot(pg, "deliveries-card", clip={"x": box["x"] - 80, "y": box["y"] - 16, "width": box["width"] + 100, "height": box["height"] + 32})
    clear(pg)

    # ---- Outstanding card (red) and read-only card ----
    red = pg.locator("article.border-rose-500").first
    red.scroll_into_view_if_needed()
    mark(pg, [(red.locator("p.bg-rose-50").first, 1, "left", {"dist": 40}), (red.locator("button").first, 2, "left", {"dist": 40})])
    box = red.bounding_box()
    shot(pg, "deliveries-outstanding-card", clip={"x": box["x"] - 80, "y": box["y"] - 16, "width": box["width"] + 100, "height": box["height"] + 32})
    clear(pg)

    # ---- Show O/C ----
    go(pg, "/deliveries?oc=show")
    ocs = pg.locator("article", has_text="· O/C")
    mark(pg, [(pg.get_by_role("link", name="Showing O/C"), 1, "bottom", {"dist": 50}),
              (ocs.last.locator("span", has_text="O/C").last, 2, "left", {"dist": 60})])
    shot(pg, "deliveries-oc")
    clear(pg)

    # ---- Cross-branch ----
    go(pg, "/deliveries?xb=1")
    ro = pg.locator("article", has_text="is delivering this DO").first
    mark(pg, [(pg.get_by_role("link", name="Cross-branch"), 1, "bottom", {"dist": 50}),
              (ro.locator("span.bg-amber-50"), 2, "right", {"dist": 50}),
              (ro.locator("p", has_text="is delivering this DO"), 3, "right", {"dist": 50})])
    shot(pg, "deliveries-cross-branch")
    clear(pg)

    # ---- Not delivered filter ----
    go(pg, "/deliveries?show=undelivered")
    mark(pg, [(pg.get_by_role("link", name="Not delivered"), 1, "bottom", {"dist": 50})])
    shot(pg, "deliveries-not-delivered")
    clear(pg)

    # ---- DO popup + Add remark ----
    go(pg, "/deliveries")
    pg.locator("main article").filter(has_text="Medini Site Office").locator("button").first.click()
    dlg = pg.locator("dialog[open]")
    dlg.wait_for(); pg.wait_for_timeout(800)
    mark(pg, [(dlg.locator("h3", has_text="Items"), 1, "left", {"dist": 60}),
              (dlg.locator("h3", has_text="History"), 2, "left", {"dist": 60}),
              (dlg.get_by_role("button", name="Add remark"), 3, "left", {"dist": 70})])
    shot(pg, "do-popup")
    clear(pg)
    dlg.get_by_role("button", name="Add remark").click()
    rem = pg.locator("dialog[open]").last
    rem.wait_for()
    rem.locator("input[name=reason]").fill("Short 5 pcs Y10 steel bar, customer only received 15")
    rem.locator("select[name=todo]").select_option("edit_do")
    rem.locator("textarea").fill("Change Y10 qty from 20 to 15 in AutoCount")
    mark(pg, [(rem.locator("input[name=reason]"), 1, "left", {"dist": 60}),
              (rem.locator("select[name=todo]"), 2, "left", {"dist": 60}),
              (rem.locator("textarea"), 3, "left", {"dist": 60}),
              (rem.get_by_role("button", name="Save"), 4, "right", {"dist": 60})])
    shot(pg, "add-remark")
    clear(pg)
    rem.get_by_role("button", name="Save").click()
    pg.wait_for_timeout(1500)

    # ---- Outstanding page ----
    go(pg, "/outstanding")
    first = pg.locator("main li").first
    space(pg, pg.locator("main div.card").first, bottom=90)
    mark(pg, [(pg.get_by_role("link", name="Outstanding"), 1, "bottom", {"dist": 40}),
              (pg.locator("main nav"), 2, "bottom", {"dist": 34}),
              (pg.locator("main form"), 3, "bottom", {"dist": 34}),
              (first.locator("span.rounded-full").first, 4, "top", {"dist": 30, "dx": 60}),
              (first.get_by_role("button", name="Clear"), 5, "left", {"dist": 60})])
    shot(pg, "outstanding")
    clear(pg)
    # clear everything → tab turns green
    for _ in range(5):
        btn = pg.get_by_role("button", name="Clear")
        if btn.count() == 0: break
        btn.first.click(); pg.wait_for_timeout(1500)
    go(pg, "/outstanding?show=cleared")
    mark(pg, [(pg.get_by_role("link", name="Outstanding"), 1, "bottom", {"dist": 40}),
              (pg.locator("main li").first.locator("p.text-right"), 2, "left", {"dist": 60})])
    shot(pg, "outstanding-cleared")
    clear(pg)

    # ---- Special DO ----
    go(pg, "/deliveries/new")
    shot(pg, "special-do")
    b.close()
print("ok")
