// Answers the app's Google Maps calls locally (Geocoding + Routes) so Best route and
// "Find address" work in the demo. Distances are straight-line × 1.35, ~38 km/h.
const STORES = {
  "Gelang Patah": { lat: 1.4446, lng: 103.5895 },
  "Kempas": { lat: 1.5402, lng: 103.7203 },
  "Kangkar Tebrau": { lat: 1.5631, lng: 103.7801 },
};
const PLACES = [
  ["Kebun Teh", 1.4532, 103.5994], ["Nusa Bestari", 1.5179, 103.6585], ["Bukit Indah", 1.481, 103.6545],
  ["Pulai Indah", 1.4475, 103.5911], ["Kangkar Pulai", 1.5432, 103.5866], ["Perling", 1.4847, 103.6831],
  ["Medini", 1.4258, 103.628], ["Kulai", 1.6421, 103.6058], ["Ekoflora", 1.4931, 103.736],
  ["Ungku Tun Aminah", 1.5047, 103.6649], ["Puteri Harbour", 1.417, 103.6567], ["Mahsuri", 1.4627, 103.5732],
  ["Mount Austin", 1.5603, 103.7795], ["Pendas", 1.3826, 103.6037], ["Desa Tebrau", 1.5469, 103.7984],
  ["Sutera", 1.5135, 103.6699],
];
const km = (a, b) => {
  const R = 6371, r = (x) => (x * Math.PI) / 180;
  const h = Math.sin(r(b.lat - a.lat) / 2) ** 2 + Math.cos(r(a.lat)) * Math.cos(r(b.lat)) * Math.sin(r(b.lng - a.lng) / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(h)) * 1.35;
};
const realFetch = globalThis.fetch;
const reply = (body) => new Response(JSON.stringify(body), { status: 200, headers: { "content-type": "application/json" } });
globalThis.fetch = async (input, init) => {
  const url = String(input instanceof Request ? input.url : input);
  if (url.startsWith("https://maps.googleapis.com/maps/api/geocode")) {
    const address = new URL(url).searchParams.get("address") || "";
    const store = Object.entries(STORES).find(([k]) => address.includes(k) && /^(Lot 261|Jalan Kangkar|Lot 44565)/.test(address));
    const place = store ? [store[0], store[1].lat, store[1].lng] : PLACES.find(([k]) => address.toLowerCase().includes(k.toLowerCase()));
    if (!place) return reply({ status: "ZERO_RESULTS", results: [] });
    const [, lat, lng] = place.length === 3 && typeof place[1] === "number" ? place : [null, place[1].lat, place[1].lng];
    return reply({ status: "OK", results: [{ types: ["street_address"], formatted_address: address, geometry: { location: { lat, lng }, location_type: "ROOFTOP" } }] });
  }
  if (url.startsWith("https://routes.googleapis.com/")) {
    const body = JSON.parse(init.body);
    const p = (w) => ({ lat: w.location.latLng.latitude, lng: w.location.latLng.longitude });
    const origin = p(body.origin), dest = p(body.destination);
    const mids = (body.intermediates || []).map(p);
    // nearest-neighbour order from the store
    let order = mids.map((_, i) => i);
    if (body.optimizeWaypointOrder) {
      order = []; const left = new Set(mids.map((_, i) => i)); let cur = origin;
      while (left.size) { let best = null; for (const i of left) if (best === null || km(cur, mids[i]) < km(cur, mids[best])) best = i; order.push(best); left.delete(best); cur = mids[best]; }
    }
    const path = [origin, ...order.map((i) => mids[i]), dest];
    let total = 0; for (let i = 1; i < path.length; i++) total += km(path[i - 1], path[i]);
    return reply({ routes: [{ distanceMeters: Math.round(total * 1000), duration: `${Math.round((total / 38) * 3600)}s`, optimizedIntermediateWaypointIndex: body.optimizeWaypointOrder ? order : undefined }] });
  }
  return realFetch(input, init);
};
