# Deliveries

The main page for the office. Every DO for your branch, grouped by where it is now. It opens on **today** and updates by itself when a driver changes something.

## The page at a glance

![Deliveries page with filters and status columns](./img/deliveries-overview.webp)

<div class="callouts">

- <span class="n">1</span> **Menu.** The **Outstanding** tab is red with a number while remarks are still open, and green when everything is cleared.
- <span class="n">2</span> **All / Not delivered / Delivered.** Show every DO, only the ones still to go, or only finished ones.
- <span class="n">3</span> **Show O/C.** Own-collection DOs (customer collects at the store) are hidden by default. Tap to show them.
- <span class="n">4</span> **Cross-branch.** DOs your branch sold that another branch is delivering. See [Cross-branch](#cross-branch-dos-another-branch-delivers).
- <span class="n">5</span> **Today / This week / All dates.** Quick date ranges.
- <span class="n">6</span> **Branch and date range.** Pick any dates, then tap **Go**. Admins can also switch branch here.
- <span class="n">7</span> **Search DO no.** Type part of a DO number to find it across all dates.
- <span class="n">8</span> **+ Special DO.** Add a delivery that isn't an AutoCount DO. See [Special DOs](#special-dos).
- <span class="n">9</span> **Status columns.** Unassigned → Assigned → Out for delivery → Delivered, plus Failed. The number is how many DOs are in each.

</div>

The line under the title shows the branch, the dates, how many are delivered, and when AutoCount last synced.

## Assign a driver, date and time

Each DO card that hasn't left yet can be planned right on the card.

<img src="./img/deliveries-card.webp" alt="A DO card with driver, date and time pickers" width="320">

<div class="callouts">

- <span class="n">1</span> **DO number.** Tap it to see the items and add a remark. See [Remarks](#add-a-remark-outstanding).
- <span class="n">2</span> **Choose driver.** Pick the driver (their lorry number shows next to the name). The DO moves to **Assigned** and appears on that driver's phone. Pick **O/C (customer collects)** if there's no delivery.
- <span class="n">3</span> **Delivery date.** Today, tomorrow, the day after, or **Pick a date…** for any other day.
- <span class="n">4</span> **Estimated time.** Optional time window (for example 11am–1pm). The driver sees it on their phone.

</div>

Changes save straight away. There's no Save button.

::: info
- Only the branch that **delivers** the DO can plan it. Other branches can see it but not change it.
- Once the driver taps **Start delivery**, the card no longer shows the pickers.
- A **Failed** DO can be given a driver and date again. It goes back to **Assigned**.
- A date in red with **· late** means the DO is past its date and still not delivered.
:::

To put several DOs in a trip together, or change their order, use [Driver status](./driver-status).

## Not delivered only

![Deliveries showing only DOs that are not delivered](./img/deliveries-not-delivered.webp)

<div class="callouts">

- <span class="n">1</span> **Not delivered** hides the Delivered column, so you only see what still needs doing. Combine it with **This week** to catch anything left behind.

</div>

## O/C (own collection)

DOs where the customer collects at the store are marked **O/C**. They're hidden unless you turn them on.

![Deliveries with O/C shown](./img/deliveries-oc.webp)

<div class="callouts">

- <span class="n">1</span> **Showing O/C** (dark) means O/C DOs are included. Tap again to hide them.
- <span class="n">2</span> O/C DOs show **· O/C** next to the DO number.

</div>

The app marks a DO as O/C when its remarks or address say "O/C" or "own collect". To change it, pick a driver (it becomes a delivery) or pick **O/C (customer collects)** in the driver box.

## Cross-branch: DOs another branch delivers

Sometimes we sell to a customer, but another branch delivers. For example, we ask Kempas to deliver our SO.

![Cross-branch view showing DOs delivered by Kempas for GP](./img/deliveries-cross-branch.webp)

<div class="callouts">

- <span class="n">1</span> **Cross-branch** (dark when on) shows only the DOs your branch sold that another branch is delivering.
- <span class="n">2</span> **for GP** means the DO was sold by GP. The grey tag before it (**KS**) is the branch delivering it.
- <span class="n">3</span> You can follow the status, driver and date, but you **can't** assign or change anything. Only the delivering branch can.

</div>

## Add a remark (Outstanding)

Use this when a DO needs to be fixed in AutoCount later (credit note, edit DO, delivery return) but you don't have time now. The remark stays visible until someone clears it.

**Step 1.** Tap the **DO number** on any card.

![DO popup with items and Add remark](./img/do-popup.webp)

<div class="callouts">

- <span class="n">1</span> **Items** on this DO, with quantities.
- <span class="n">2</span> **History** of who changed the DO and when (admins only).
- <span class="n">3</span> Tap **Add remark**.

</div>

**Step 2.** Fill in the remark.

![Add remark form](./img/add-remark.webp)

<div class="callouts">

- <span class="n">1</span> **Reason.** What happened, for example "Customer returned 2 bags".
- <span class="n">2</span> **To-do.** What needs doing in AutoCount: **Add Credit Note (CN)**, **Edit DO**, **Add Delivery Return (DR)**, or **Others** (then type what).
- <span class="n">3</span> **Description** (optional). Extra details, like the new quantity.
- <span class="n">4</span> **Save.**

</div>

**Step 3.** The DO card now has a red border and shows the remark, and the **Outstanding** tab turns red.

<img src="./img/deliveries-outstanding-card.webp" alt="DO card with a red outstanding remark" width="320">

<div class="callouts">

- <span class="n">1</span> The open remark: what to do · why.
- <span class="n">2</span> Tap the DO number again to see the remark and **Clear** it once it's fixed.

</div>

All open remarks are listed on the [Outstanding](./outstanding) page.

## Special DOs

For deliveries that aren't an AutoCount DO, such as a stock transfer to another branch or a pick-up from a supplier. They get an **SDO-** number and count toward the driver's deliveries like any other DO.

![New special DO form](./img/special-do.webp)

1. Tap **+ Special DO** at the top of Deliveries.
2. Fill in **Deliver to**, **Delivery address** (the driver gets Waze / Maps buttons for it), **Contact phone** and **Delivery date**.
3. Pick the **Branch** and a **Driver**, or leave it as **Assign later**.
4. Set **Points for the driver** (usually 3 if over 20 km, otherwise 2).
5. Add **Instructions to driver** if needed, for example "Collect 20 bags from supplier first".
6. Tap **Create special DO**.

You can **Edit** a special DO from its card until the driver starts it. Only the person who created it, or an admin, can edit it.
