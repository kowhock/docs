# Delivery Tracker

Delivery Tracker (KH Delivery) follows every delivery order (DO) from AutoCount to the customer's door. DOs come in from AutoCount on their own every few minutes, so nobody keys them in twice.

**App link:** [delivery-tracker-fawn.vercel.app](https://delivery-tracker-fawn.vercel.app)

::: tip About the screenshots
Every screenshot here uses made-up demo data. The orange numbers on each picture match the numbered notes under it.
:::

## Who uses what

| You are | You use | Pages |
|---|---|---|
| **Office staff** (dispatcher) | A computer | [Deliveries](./deliveries), [Outstanding](./outstanding), [Driver status](./driver-status), [Lorries](./lorries), [Trip form](./trip-form) |
| **Admin** | A computer | Everything the office sees, for every branch, plus DO history |
| **Driver** | A phone | [Driver phone view](./driver) |

Office staff only see their own branch. Admins can switch between branches.

## A delivery from start to finish

1. **The DO arrives from AutoCount.** It shows on [Deliveries](./deliveries) under **Unassigned**.
2. **The office picks a driver, date and time.** The DO moves to **Assigned** and shows up on the driver's phone.
3. **The office arranges trips** on [Driver status](./driver-status): which DOs go together, in what order. **Best route** works out the shortest order.
4. **The driver taps Start delivery**, drives there with Waze or Google Maps and can WhatsApp the customer.
5. **The driver taps Delivered** and takes a photo of the signed DO. The office sees it change to **Delivered** straight away.
6. **At the end of the day or month**, the office prints the driver's [trip form](./trip-form).

If something on a DO still needs fixing in AutoCount (a credit note, an edited DO), add a remark on it. It stays on [Outstanding](./outstanding) until someone clears it.

## Quick links

- [Assign a driver](./deliveries#assign-a-driver-date-and-time)
- [Plan trips and find the best route](./driver-status#arrange-trips)
- [Fix an address the map can't find](./driver-status#fix-an-address-or-points)
- [Mark a lorry under maintenance](./lorries#maintenance)
- [Print or export a monthly trip form](./trip-form#monthly-trip-form)
- [What drivers do on their phone](./driver)
