# Retaking the Delivery Tracker screenshots

The screenshots come from a copy of the app running on your own computer with **made-up demo data**, so no real customer shows up in the guide. The scripts sign in, click through each page, draw the orange numbered callouts and save the pictures.

Retake them when a page in the app changes.

## What's here

| File | What it does |
|---|---|
| `shim.sql` | The bits of Supabase the schema needs (auth, roles, storage), for a plain local Postgres |
| `seed.js` | Demo data: users, lorries, today's DOs, a month of Ali's deliveries. Every user's password is `demo` |
| `gateway.js` | A tiny stand-in for the Supabase API on port 54321 (database via PostgREST, sign-in, photo uploads) |
| `fake-google.js` | Answers the Google Maps calls locally so Best route and Find address work |
| `annot.py` | Helpers: sign in, draw callouts |
| `cap_deliveries.py` | Sign in, Deliveries, Outstanding, Special DO |
| `cap_office.py` | Driver status, Lorries, Trip form (`python3 cap_office.py drivers` for one section) |
| `cap_driver.py` | Driver phone view |
| `to_webp.py` | Converts the PNGs to the WebP files the guide uses |

## Steps

1. **Postgres.** Start a local Postgres 15+ (any install works) and create the database:
   ```bash
   createdb -h 127.0.0.1 -U postgres kh
   psql -h 127.0.0.1 -U postgres -d kh -f shim.sql
   psql -h 127.0.0.1 -U postgres -d kh -f ../../../delivery-tracker/supabase/schema.sql
   psql -h 127.0.0.1 -U postgres -d kh -f ../../../delivery-tracker/supabase/upgrade.sql
   ```
   (Adjust the path to wherever the Delivery-Tracker repo is.)
2. **PostgREST + gateway.** Download [PostgREST](https://github.com/PostgREST/postgrest/releases), then:
   ```bash
   npm install
   # pgrst.conf:
   #   db-uri = "postgres://authenticator:x@127.0.0.1:5432/kh"
   #   db-schemas = "public"
   #   db-anon-role = "anon"
   #   jwt-secret = "super-secret-jwt-token-with-at-least-32-characters-long"
   #   server-port = 3001
   ./postgrest pgrst.conf &
   node gateway.js &
   ```
3. **The app.** In the Delivery-Tracker repo, make a `.env.local` that points at the gateway:
   ```
   NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
   NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon JWT signed with the jwt-secret above, role "anon">
   NEXT_PUBLIC_COMPANY_NAME=Kow Hock Building Materials
   GOOGLE_MAPS_API_KEY=local-demo
   ```
   Then build and start it with the fake Google Maps loaded:
   ```bash
   npx next build
   NODE_OPTIONS="--require /path/to/fake-google.js" npx next start -p 3000
   ```
4. **Take the screenshots** (needs Python with Playwright and Pillow):
   ```bash
   python3 cap_deliveries.py
   python3 cap_office.py
   python3 cap_driver.py
   python3 to_webp.py
   ```
   Each script resets the demo data first, so they can run in any order.

The demo data follows the real date: "today" in the demo is the day you run it. `cap_office.py` picks fixed dates for the trip form, so update those to dates inside the last month.
