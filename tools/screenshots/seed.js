// Demo data for the guide's screenshots. Every name, address and phone number is made up.
const crypto = require("crypto");
const TODAY = new Date().toLocaleDateString("en-CA", { timeZone: "Asia/Kuala_Lumpur" }); // demo "today" = the real today
const id = () => crypto.randomUUID();
const q = (v) => (v === null || v === undefined ? "null" : typeof v === "number" || typeof v === "boolean" ? String(v) : `'${String(v).replace(/'/g, "''")}'`);
const out = [];
const ins = (table, row) => out.push(`insert into ${table} (${Object.keys(row).join(",")}) values (${Object.values(row).map(q).join(",")});`);

function addDays(d, n) { const x = new Date(d + "T00:00:00Z"); x.setUTCDate(x.getUTCDate() + n); return x.toISOString().slice(0, 10); }
const at = (day, hhmm) => `${day}T${hhmm}:00+08:00`;

// ---------- People ----------
const users = {};
function user(key, email, name, role, branch, phone) {
  const u = { id: id(), email, name, role, branch, phone };
  users[key] = u;
  ins("auth.users", { id: u.id, email, raw_user_meta_data: JSON.stringify({ full_name: name }) });
  out.push(`update public.profiles set full_name=${q(name)}, role=${q(role)}, branch=${q(branch)}, phone=${q(phone)} where id=${q(u.id)};`);
}
user("admin", "meiling@khdelivery.my", "Mei Ling", "admin", "GP", null);
user("disp", "aisyah@khdelivery.my", "Aisyah", "dispatcher", "GP", null);
user("ali", "ali@khdelivery.my", "Ali", "driver", "GP", "012-711 2034");
user("rahman", "rahman@khdelivery.my", "Rahman", "driver", "GP", "016-722 4410");
user("kumar", "kumar@khdelivery.my", "Kumar", "driver", "GP", "019-755 0981");
user("faizal", "faizal@khdelivery.my", "Faizal", "driver", "KS", "011-2633 8120");
user("siva", "siva@khdelivery.my", "Siva", "driver", "PD", "017-733 9052");

// ---------- Lorries ----------
const lorries = {};
function lorry(no, plate, branch, driver, extra = {}) {
  const l = { id: id(), lorry_no: no, plate_no: plate, branch, driver_id: driver ? users[driver].id : null, ...extra };
  lorries[no] = l;
  ins("public.lorries", l);
}
lorry("46", "JQN 9833", "GP", "ali");
lorry("51", "JRB 2210", "GP", "rahman");
lorry("63", "JTA 4471", "GP", "kumar");
lorry("72", "JUB 1187", "GP", null, { maintenance_from: addDays(TODAY, -2), maintenance_to: addDays(TODAY, 3), maintenance_note: "Gearbox repair at Tan Motor workshop" });
lorry("30", "JHK 5521", "KS", "faizal");
lorry("38", "JPD 6640", "PD", "siva");
const lev = (no, note, when) => ins("public.lorry_events", { lorry_id: lorries[no].id, note, actor_id: users.admin.id, created_at: when });
lev("72", `Maintenance ${addDays(TODAY, -2).split("-").reverse().join("/")} – ${addDays(TODAY, 3).split("-").reverse().join("/")}: Gearbox repair at Tan Motor workshop`, at(addDays(TODAY, -2), "08:10"));
lev("72", "Kumar taken off lorry 72", at(addDays(TODAY, -2), "08:05"));
lev("63", "Kumar put on lorry 63", at(addDays(TODAY, -2), "08:06"));
lev("46", "Ali put on lorry 46", at("2026-09-01", "09:00"));

// ---------- Customers (fictional) around southern Johor ----------
const C = [
  ["Syarikat Binaan Teguh Sdn Bhd", "No. 12, Jalan Nusa Bestari 2/4, Taman Nusa Bestari, 81300 Skudai, Johor", 1.5179, 103.6585, 14.2],
  ["Lim Renovation Works", "23, Jalan Bukit Indah 15/8, Taman Bukit Indah, 81200 Johor Bahru, Johor", 1.4810, 103.6545, 9.8],
  ["Kedai Besi Ah Seng", "8, Jalan Gelang Patah 3, Taman Pulai Indah, 81550 Gelang Patah, Johor", 1.4475, 103.5911, 3.1],
  ["Pembinaan Mutiara Jaya", "Lot 5521, Jalan Kampung Pulai, 81110 Kangkar Pulai, Johor", 1.5432, 103.5866, 18.6],
  ["Tan Brothers Construction", "45, Jalan Perling 6, Taman Perling, 81200 Johor Bahru, Johor", 1.4847, 103.6831, 16.4],
  ["Medini Site Office (Block C)", "Jalan Medini Utara 4, Medini, 79250 Iskandar Puteri, Johor", 1.4258, 103.6280, 7.9],
  ["Hardware Sentosa Kulai", "17, Jalan Kenari 3, Bandar Putra, 81000 Kulai, Johor", 1.6421, 103.6058, 32.5],
  ["Rumah Encik Hafiz", "No. 9, Jalan Ekoflora 7/2, Taman Ekoflora, 81100 Johor Bahru, Johor", 1.4931, 103.7360, 24.7],
  ["Wong Plumbing & Sanitary", "31, Jalan Pendekar 10, Taman Ungku Tun Aminah, 81300 Skudai, Johor", 1.5047, 103.6649, 13.1],
  ["Projek Kondo Puteri Harbour", "Persiaran Puteri Selatan, Puteri Harbour, 79000 Iskandar Puteri, Johor", 1.4170, 103.6567, 10.6],
  ["Kampung Ladang Mahsuri", "Jalan Mahsuri, Kampung Ladang, 81550 Gelang Patah, Johor", 1.4627, 103.5732, 5.4],
  ["Seng Hup Tiles Trading", "6, Jalan Mutiara Emas 9/3, Taman Mount Austin, 81100 Johor Bahru, Johor", 1.5603, 103.7795, 34.8],
  ["Bina Setia Engineering", "20, Jalan Indah 15/2, Bukit Indah, 81200 Johor Bahru, Johor", 1.4788, 103.6489, 9.2],
  ["Puan Rosnah", "Lot 77, Kampung Pendas Laut, 81550 Gelang Patah, Johor", 1.3826, 103.6037, 7.0],
  ["Chong Kee Builder", "102, Jalan Harmonium 23/1, Taman Desa Tebrau, 81100 Johor Bahru, Johor", 1.5469, 103.7984, 38.9],
  ["Excel Interior Design", "15, Jalan Sutera Tanjung 8/2, Taman Sutera Utama, 81300 Skudai, Johor", 1.5135, 103.6699, 15.0],
];
const cust = (i) => C[i % C.length];

const ITEMS = [
  ["CEM-YTL50", "CEMENT YTL 50KG", "BAG"],
  ["STB-Y10", "STEEL BAR Y10 x 12M", "PCS"],
  ["STB-Y12", "STEEL BAR Y12 x 12M", "PCS"],
  ["BRC-A7", "BRC A7 2.4M x 4.8M", "PCS"],
  ["SND-RIV", "RIVER SAND (5 TON LORRY)", "LOAD"],
  ["PVC-4IN", 'PVC PIPE 4" x 20FT CLASS D', "PCS"],
  ["BRK-CL", "CLAY BRICK (1000PCS)", "PALLET"],
  ["PLY-12", "PLYWOOD 12MM 4' x 8'", "PCS"],
  ["SKM-25", "SKIM COAT 25KG", "BAG"],
  ["WPF-20", "WATERPROOFING 20KG", "TIN"],
];

let doSeq = 45120, soSeq = 31260;
const dos = {};
function makeDo(key, o) {
  const c = cust(o.c);
  const branch = o.branch ?? "GP";
  const prefix = { GP: "GPD", KS: "KSD", PD: "PDD" }[branch];
  const soBranch = o.sales_branch ?? branch;
  const soPrefix = { GP: "GPS", KS: "KSS", PD: "PDS" }[soBranch];
  const d = {
    id: id(),
    do_no: `${prefix}-000${doSeq++}`,
    so_no: `${soPrefix}-000${soSeq++}`,
    customer_name: c[0],
    contact_phone: o.phone === undefined ? `01${(o.c % 9) + 1}-7${String(100 + o.c * 37).slice(-3)} ${String(1000 + o.c * 271).slice(-4)}` : o.phone,
    address: o.address ?? c[1],
    map_address: o.map_address ?? null,
    remarks: o.remarks ?? null,
    delivery_date: o.date ?? TODAY,
    time_slot: o.slot ?? null,
    branch,
    sales_branch: soBranch,
    source: "autocount",
    created_user: "MEILING",
    total: o.total ?? Math.round(800 + o.c * 413.7) / 1,
    driver_id: o.driver ? users[o.driver].id : null,
    trip_no: o.trip ?? 1,
    trip_seq: o.seq ?? 0,
    status: o.status ?? (o.driver ? "assigned" : "pending"),
    failed_reason: o.failed_reason ?? null,
    delivered_at: o.delivered_at ?? null,
    lorry_id: o.lorry ?? null,
    own_collection: o.oc ?? null,
    instructions: o.instructions ?? null,
    created_at: o.created_at ?? at(o.date ?? TODAY, "07:3" + (doSeq % 10)),
  };
  if (o.notFound) Object.assign(d, { geo_status: "not_found", geo_input: d.address, points: null });
  else if (o.manualPoints != null) Object.assign(d, { points: o.manualPoints, points_manual: true });
  else {
    const km = o.km ?? c[4];
    Object.assign(d, { distance_km: km, points: km > 20 ? 3 : 2, geo_status: "ok", geo_input: d.map_address || d.address, geo_address: c[1].replace(/^No\. /, ""), geo_lat: c[2], geo_lng: c[3] });
  }
  dos[key] = d;
  ins("public.delivery_orders", d);
  ins("public.do_sales_orders", { do_id: d.id, so_no: d.so_no });
  const n = 1 + ((o.c * 7) % 4);
  for (let i = 0; i < n; i++) {
    const it = ITEMS[(o.c * 3 + i * 5) % ITEMS.length];
    ins("public.do_items", { do_id: d.id, item_code: it[0], description: it[1], uom: it[2], qty: [10, 20, 5, 50, 2, 1, 30][(o.c + i) % 7] });
  }
  ev(d, "do_created", null, users.admin.id, at(d.delivery_date, "07:30"));
  return d;
}
function ev(d, status, note, actor, when) { ins("public.status_events", { do_id: d.id, status, note, actor_id: actor, created_at: when }); }

// ---------- Today ----------
// Ali: trip 1 underway, trip 2 waiting
const a1 = makeDo("a1", { c: 2, driver: "ali", trip: 1, seq: 0, status: "delivered", delivered_at: at(TODAY, "09:42"), lorry: lorries["46"].id, slot: "0845-1100" });
const a2 = makeDo("a2", { c: 10, driver: "ali", trip: 1, seq: 1, status: "out_for_delivery", slot: "0845-1100", remarks: "Call before arrive. Unload at back gate." });
const a3 = makeDo("a3", { c: 5, driver: "ali", trip: 1, seq: 2, status: "assigned", slot: "1100-1300", remarks: "Site office closes 12pm for lunch" });
const a4 = makeDo("a4", { c: 3, driver: "ali", trip: 2, seq: 0, slot: "1300-1500" });
const a5 = makeDo("a5", { c: 15, driver: "ali", trip: 2, seq: 1, slot: "1500-1700" });
const a6 = makeDo("a6", { c: 6, driver: "ali", trip: 2, seq: 2, notFound: true, address: "Lot 3, Jln Kebun Teh 2, Gelang Patah", remarks: "Near the new petrol station" });
ev(a1, "trip", "Ali · trip 1", users.admin.id, at(TODAY, "07:45"));
ev(a1, "assigned", "Ali", users.admin.id, at(TODAY, "07:44"));
ev(a1, "out_for_delivery", null, users.ali.id, at(TODAY, "08:55"));
ev(a1, "delivered", "Received by Mr Lee", users.ali.id, at(TODAY, "09:42"));
ev(a2, "out_for_delivery", null, users.ali.id, at(TODAY, "09:50"));
// Rahman: one trip, not started — good for Best route
makeDo("r1", { c: 4, driver: "rahman", seq: 0 });
makeDo("r2", { c: 1, driver: "rahman", seq: 1, slot: "1100-1300" });
makeDo("r3", { c: 9, driver: "rahman", seq: 2 });
makeDo("r4", { c: 12, driver: "rahman", seq: 3, remarks: "Ask for Mr Tan at hardware counter" });
// Kumar: one failed, one delivered
makeDo("k1", { c: 13, driver: "kumar", status: "failed", failed_reason: "Customer not available", seq: 0 });
makeDo("k2", { c: 0, driver: "kumar", status: "delivered", delivered_at: at(TODAY, "10:15"), lorry: lorries["63"].id, seq: 1 });
// Not assigned yet
makeDo("p1", { c: 7, remarks: "Deliver before 3pm, customer pouring slab" });
makeDo("p2", { c: 8 });
makeDo("p3", { c: 14, total: 4580 });
// O/C — customer collects, hidden unless "Show O/C"
makeDo("oc1", { c: 11, remarks: "O/C - customer collect at store" });
makeDo("oc2", { c: 13, remarks: "Own collect, lorry 1 ton", status: "delivered", delivered_at: at(TODAY, "08:40") });
// Cross-branch: GP sold, Kempas delivers
makeDo("x1", { c: 14, branch: "KS", sales_branch: "GP", driver: "faizal", status: "out_for_delivery", slot: "1100-1300" });
makeDo("x2", { c: 11, branch: "KS", sales_branch: "GP", driver: "faizal", status: "delivered", delivered_at: at(TODAY, "09:20") });
makeDo("x3", { c: 7, branch: "KS", sales_branch: "GP", status: "pending", date: TODAY });
// Kempas's own (not shown on GP)
makeDo("ks1", { c: 12, branch: "KS", driver: "faizal" });

// Tomorrow
makeDo("t1", { c: 1, driver: "ali", date: addDays(TODAY, 1) });
makeDo("t2", { c: 8, driver: "ali", date: addDays(TODAY, 1), seq: 1 });
makeDo("t3", { c: 4, driver: "rahman", date: addDays(TODAY, 1) });

// ---------- Outstanding ----------
function outstanding(d, reason, todo, desc, when, cleared) {
  ins("public.do_outstanding", { do_id: d.id, reason, todo, description: desc, created_by: users.admin.id, created_at: when, cleared_at: cleared ?? null, cleared_by: cleared ? users.admin.id : null });
}
outstanding(a1, "Customer returned 2 bags cement (damaged)", "cn", "Issue CN for 2 x CEMENT YTL 50KG", at(TODAY, "10:05"));
outstanding(dos.k1, "Customer asked to change delivery address", "edit_do", "New address: Lot 80, Kampung Pendas Laut", at(TODAY, "10:40"));

// ---------- Ali's past month, for the trip forms ----------
let histSeq = 0;
for (let n = 1; n <= 26; n++) {
  const day = addDays(TODAY, -n);
  const dow = new Date(day + "T00:00:00Z").getUTCDay();
  if (dow === 0) continue; // Sundays off
  if (n === 15) continue; // a day off sick (MC)
  const count = 7 + ((n * 3) % 4);
  const trips = 2;
  let clock = 8 * 60 + 40;
  for (let i = 0; i < count; i++) {
    const trip = trips === 2 && i >= Math.ceil(count / 2) ? 2 : 1;
    const c = (n * 3 + i * 5) % C.length;
    const start = clock; clock += 35 + ((i * 13 + n) % 30);
    const back = clock; clock += 10;
    const hm = (m) => `${String(Math.floor(m / 60)).padStart(2, "0")}:${String(m % 60).padStart(2, "0")}`;
    const d = makeDo("h" + histSeq++, { c, driver: "ali", date: day, trip, seq: i, status: "delivered", delivered_at: at(day, hm(back)), lorry: lorries["46"].id, created_at: at(day, "07:20") });
    ev(d, "out_for_delivery", null, users.ali.id, at(day, hm(start)));
  }
}
// One historical DO with a typed address
out.push(`update public.delivery_orders set map_address='Lot 3, Jalan Kebun Teh 2, Taman Kebun Teh, 81550 Gelang Patah' where id=${q(dos.h5.id)};`);

out.push(`insert into public.sync_status (source, synced_at) values ('autocount', now() - interval '3 minutes') on conflict (source) do update set synced_at = excluded.synced_at;`);
console.log("begin;\n" + out.join("\n") + "\ncommit;");
