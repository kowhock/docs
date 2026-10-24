import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from playwright.sync_api import sync_playwright
from annot import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "delivery-tracker", "img")
shot = lambda pg, name, **kw: pg.screenshot(path=f"{OUT}/{name}.png", **kw)
only = sys.argv[1:]  # optional: run just some sections
want = lambda k: not only or k in only

reseed()
with sync_playwright() as p:
    b = launch(p)
    ctx = new_context(b)
    pg = login(ctx, "meiling")

    if want("drivers"):
        go(pg, "/drivers")
        head = pg.locator("main > div > div").first
        ali = pg.locator("main section.card").filter(has_text="Ali").first
        rah = pg.locator("main section.card").filter(has_text="Rahman").first
        space(pg, pg.locator("main > div > div").first, bottom=30)
        mark(pg, [
            (pg.locator("main form"), 1, "left", {"dist": 50}),
            (ali.locator("header span.bg-amber-100"), 2, "right", {"dist": 50}),
            (ali.locator("header span.bg-yellow-50"), 3, "left", {"dist": 50}),
            (ali.locator("div.w-64").nth(0).locator("div").first, 4, "top", {"dist": 28, "dx": 90}),
            (ali.locator("div.w-64").nth(2), 5, "right", {"dist": 50}),
            (pg.get_by_role("button", name="📍 Calculate 1 missing points"), 6, "right", {"dist": 50}),
        ])
        shot(pg, "drivers-overview")
        clear(pg)

        # Trip lanes close up: drag + best route
        rah.scroll_into_view_if_needed()
        lane = rah.locator("div.w-64").first
        cards = lane.locator("article")
        mark(pg, [
            (lane.get_by_role("button", name="🧭 Best route"), 1, "right", {"dist": 60}),
            (cards.nth(1), 2, "right", {"dist": 60}),
            (rah.locator("div.w-64").nth(1), 3, "top", {"dist": 30}),
        ])
        bx = rah.bounding_box()
        shot(pg, "drivers-trip", clip={"x": bx["x"], "y": bx["y"], "width": 760, "height": min(bx["height"], 900)})
        clear(pg)

        # Run Best route
        lane.get_by_role("button", name="🧭 Best route").click()
        lane.locator("p", has_text="km").wait_for(timeout=15000)
        pg.wait_for_timeout(800)
        mark(pg, [(lane.locator("p", has_text="km"), 1, "right", {"dist": 60}),
                  (lane.locator("article").first.locator("span.mr-1"), 2, "left", {"dist": 34})])
        bx = rah.bounding_box()
        shot(pg, "drivers-best-route", clip={"x": bx["x"], "y": bx["y"], "width": 760, "height": min(bx["height"], 900)})
        clear(pg)

        # Points editor on the DO whose address Google can't find
        ali.scroll_into_view_if_needed()
        chip = ali.get_by_role("button", name="⭐ Set points")
        chip.click()
        ed = ali.locator("input[aria-label='Address for the map']")
        ed.fill("Lot 3, Jalan Kebun Teh 2, Taman Kebun Teh, 81550 Gelang Patah")
        art = ed.locator("xpath=ancestor::article")
        ali.locator("input[aria-label=Points]").fill("3")
        mark(pg, [(ali.locator("input[aria-label=Points]"), 1, "left", {"dist": 40}),
                  (art.get_by_role("button", name="Save"), 2, "top", {"dist": 34, "dx": 20}),
                  (ed, 3, "left", {"dist": 40}),
                  (art.get_by_role("button", name="📍 Find"), 4, "bottom", {"dist": 40})])
        ab = art.bounding_box()
        shot(pg, "drivers-points", clip={"x": ab["x"] - 90, "y": ab["y"] - 20, "width": ab["width"] + 230, "height": ab["height"] + 90})
        ali.locator("input[aria-label=Points]").fill("")
        clear(pg)
        art.get_by_role("button", name="📍 Find").click()
        pg.wait_for_timeout(2500)
        art2 = pg.locator("main article").filter(has_text="Hardware Sentosa").filter(has_text="Kebun Teh")
        if art2.count():
            mark(pg, [(art2.first.locator("p", has_text="📍"), 1, "right", {"dist": 50}), (art2.first.locator("button", has_text="pt"), 2, "right", {"dist": 70})])
            ab = art2.first.bounding_box()
            shot(pg, "drivers-points-found", clip={"x": ab["x"] - 20, "y": ab["y"] - 20, "width": ab["width"] + 140, "height": ab["height"] + 40})
            clear(pg)
        else:
            print("WARN: typed address card not found")

    if want("lorries"):
        go(pg, "/lorries")
        cards = pg.locator("main section.card")
        c46 = cards.filter(has=pg.get_by_role("heading", name="Lorry 46", exact=True)); c72 = cards.filter(has=pg.get_by_role("heading", name="Lorry 72", exact=True))
        c46.locator("details summary").click()
        space(pg, pg.locator("main > div > div").first, bottom=20)
        mark(pg, [
            (pg.get_by_role("button", name="+ Add lorry"), 1, "left", {"dist": 50}),
            (c46.locator("span.rounded-full").first, 2, "right", {"dist": 50}),
            (c46.locator("select"), 3, "right", {"dist": 34}),
            (c46.get_by_role("button", name="🔧 Maintenance"), 4, "right", {"dist": 50}),
            (c46.locator("details"), 5, "right", {"dist": 34}),
            (c72.locator("span.rounded-full").first, 6, "right", {"dist": 50}),
            (c72.get_by_role("button", name="✅ Back in service"), 7, "bottom", {"dist": 34}),
        ])
        shot(pg, "lorries", full_page=True)
        clear(pg)

        pg.get_by_role("button", name="+ Add lorry").click()
        dlg = pg.locator("dialog[open]"); dlg.wait_for()
        dlg.locator("input[name=lorry_no]").fill("80")
        dlg.locator("input[name=plate_no]").fill("JWE 3302")
        mark(pg, [(dlg.locator("input[name=lorry_no]"), 1, "left", {"dist": 50}),
                  (dlg.locator("input[name=plate_no]"), 2, "right", {"dist": 50}),
                  (dlg.locator("select[name=branch]"), 3, "left", {"dist": 50}),
                  (dlg.get_by_role("button", name="Save"), 4, "right", {"dist": 50})])
        shot(pg, "lorry-add")
        clear(pg)
        dlg.get_by_role("button", name="Save").click(); pg.wait_for_timeout(1500)

        c46 = pg.locator("main section.card").filter(has=pg.get_by_role("heading", name="Lorry 46", exact=True))
        c46.get_by_role("button", name="🔧 Maintenance").click()
        dlg = pg.locator("dialog[open]"); dlg.wait_for()
        dlg.locator("input[name=maintenance_note]").fill("Service + change 2 rear tyres")
        dlg.locator("input[name=maintenance_to]").fill("2026-10-25")
        mark(pg, [(dlg.locator("input[name=maintenance_from]"), 1, "left", {"dist": 50}),
                  (dlg.locator("input[name=maintenance_to]"), 2, "right", {"dist": 50}),
                  (dlg.locator("input[name=maintenance_note]"), 3, "left", {"dist": 50}),
                  (dlg.locator("p.bg-amber-50"), 4, "right", {"dist": 50}),
                  (dlg.get_by_role("button", name="Save"), 5, "right", {"dist": 50})])
        shot(pg, "lorry-maintenance")
        clear(pg)
        dlg.get_by_role("button", name="Cancel").click()

        c51 = pg.locator("main section.card").filter(has=pg.get_by_role("heading", name="Lorry 51", exact=True))
        c51.locator("select").select_option(label="Ali (on lorry 46)")
        dlg = pg.locator("dialog[open]"); dlg.wait_for()
        mark(pg, [(dlg.locator("ul"), 1, "left", {"dist": 50}), (dlg.get_by_role("button", name="Yes, change"), 2, "right", {"dist": 50})])
        shot(pg, "lorry-change-driver")
        clear(pg)
        dlg.get_by_role("button", name="Cancel").click()

    if want("tripform"):
        ali_id = pg.evaluate("() => null")
        go(pg, "/trip-form")
        # pick Ali + one day
        drv = pg.locator("main form select").last
        drv.select_option(label="Ali")
        pg.locator("input[name=from]").fill("2026-10-22")
        pg.locator("input[name=to]").fill("2026-10-22")
        pg.get_by_role("button", name="Go").click(); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(600)
        space(pg, pg.locator("main > div > div").first, bottom=40)
        form = pg.locator(".trip-page").first
        mark(pg, [([pg.locator("main form select").first, pg.locator("main form select").last], 1, "bottom", {"dist": 34}),
                  ([pg.locator("input[name=from]"), pg.locator("input[name=to]")], 2, "bottom", {"dist": 34}),
                  (pg.get_by_role("button", name="PDF / Print"), 3, "bottom", {"dist": 34, "dx": -30}),
                  (pg.get_by_role("button", name="Excel"), 4, "bottom", {"dist": 34, "dx": 30}),
                  (form.locator("table").nth(0), 5, "right", {"dist": 40}),
                  (form.locator("table").nth(2).locator("tbody").first, 6, "left", {"dist": 40})])
        shot(pg, "tripform-daily", full_page=True)
        clear(pg)

        pg.locator("input[name=from]").fill("2026-09-28")
        pg.locator("input[name=to]").fill("2026-10-27")
        pg.get_by_role("button", name="Go").click(); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(600)
        page = pg.locator(".trip-page").first
        pg.get_by_label("Remark for 08/10/2026").fill("mc")
        pg.get_by_label("Remark for 04/10/2026").fill("off")
        pg.get_by_label("Remark for 11/10/2026").fill("off")
        space(pg, pg.locator("main > div > div").first, bottom=40)
        mark(pg, [([pg.locator("input[name=from]"), pg.locator("input[name=to]")], 1, "bottom", {"dist": 34}),
                  (pg.locator("main span.mr-auto"), 2, "bottom", {"dist": 34}),
                  (pg.get_by_role("button", name="Excel"), 3, "bottom", {"dist": 34}),
                  (pg.get_by_label("Remark for 08/10/2026"), 4, "right", {"dist": 50}),
                  (page.locator("tbody tr").nth(1).locator("td").nth(1), 5, "left", {"dist": 50}),
                  (page.locator("tbody tr.font-bold"), 6, "left", {"dist": 50})])
        shot(pg, "tripform-monthly", full_page=True)
        clear(pg)
    b.close()
print("ok")
