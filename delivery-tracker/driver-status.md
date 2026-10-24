# Driver status

Each driver's DOs for the day, split into trips. This is where you arrange which DOs go together, in which order, and on which day.

## The page at a glance

![Driver status with trips for one driver](./img/drivers-overview.webp)

<div class="callouts">

- <span class="n">1</span> **Branch and dates.** Opens on today for your branch. Pick a **From** and **To** date to plan several days (up to 31), then tap **Go**.
- <span class="n">2</span> The **lorry** this driver is on. Set it on [Lorries](./lorries).
- <span class="n">3</span> **Points and commission** the driver has earned in these dates, from DOs already delivered. See [Points & commission](./points).
- <span class="n">4</span> A **trip**, with how many of its DOs are delivered. DOs are numbered in the order the driver will go.
- <span class="n">5</span> **+ Trip.** An empty space at the end of each day. Drag a DO here to start a new trip.
- <span class="n">6</span> **Calculate missing points.** Shows when some DOs have no points yet. Tap it to work them out from the distance.

</div>

Each day of the date range has its own row, so you can also drag a DO to another day.

## Arrange trips

![Trip with Best route button and a DO to drag](./img/drivers-trip.webp)

<div class="callouts">

- <span class="n">1</span> **🧭 Best route.** Works out the shortest order from the store, through every stop and back. It shows once a trip has 2 or more DOs that haven't left yet.
- <span class="n">2</span> **Drag a DO** to change its order in the trip, move it to another trip, another driver or another day.
- <span class="n">3</span> **Drop it here** to put it in a new trip.

</div>

How to move a DO:

1. Click and hold the DO card.
2. Drag it to where you want it. A blue line shows where it will land.
3. Let go. It saves straight away, and the driver's phone updates.

::: warning Can't drag it?
DOs that are **Out for delivery** or **Delivered** stay where they are. DOs another branch delivers can't be moved either.
:::

## Best route

Tap **🧭 Best route** on a trip.

![Best route result with distance and time](./img/drivers-best-route.webp)

<div class="callouts">

- <span class="n">1</span> The route: store → number of stops → back, total **km** and about how long it takes. **Open in Maps** shows the whole route in Google Maps (up to 9 stops).
- <span class="n">2</span> The DOs are **re-numbered in the new order**. The driver sees them in this order on their phone.

</div>

If an address can't be found on the map, that DO is put last and listed in red. Fix it with [Fix an address or points](#fix-an-address-or-points) below and run Best route again.

## Fix an address or points

Every DO has a ⭐ chip with its points. A **red "Set points"** chip means the map couldn't find the address, so there are no points yet. Click the chip to fix it.

<img src="./img/drivers-points.webp" alt="Points editor with points and address boxes" width="470">

<div class="callouts">

- <span class="n">1</span> **Points.** Type the points yourself if you know them.
- <span class="n">2</span> **Save** the points.
- <span class="n">3</span> **Address to find on the map.** Type an address Google can find. Adding the taman or town usually helps.
- <span class="n">4</span> **📍 Find.** Looks up the new address and works out the distance and points.

</div>

<img src="./img/drivers-points-found.webp" alt="DO card after the address was found" width="380">

<div class="callouts">

- <span class="n">1</span> A **📍** means the DO is using the address you typed. The driver's **Waze** and **Maps** buttons go to this address. The AutoCount address isn't changed.
- <span class="n">2</span> The points are filled in.

</div>

In the editor you can also tap **use it again** to go back to the AutoCount address, or **Use distance rule instead** to undo points you typed in.
