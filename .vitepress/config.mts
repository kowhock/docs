import { defineConfig } from "vitepress";

export default defineConfig({
  title: "Kow Hock Guides",
  description: "How to use Kow Hock's apps",
  lang: "en-MY",
  base: "/docs/",
  cleanUrls: true,
  srcExclude: ["tools/**", "README.md"],
  lastUpdated: true,
  head: [["link", { rel: "icon", href: "/docs/logo.png" }]],
  themeConfig: {
    logo: "/logo.png",
    nav: [{ text: "Delivery Tracker", link: "/delivery-tracker/" }],
    sidebar: {
      "/delivery-tracker/": [
        {
          text: "Delivery Tracker",
          items: [
            { text: "Start here", link: "/delivery-tracker/" },
            { text: "Signing in", link: "/delivery-tracker/sign-in" },
          ],
        },
        {
          text: "Office",
          items: [
            { text: "Deliveries", link: "/delivery-tracker/deliveries" },
            { text: "Outstanding", link: "/delivery-tracker/outstanding" },
            { text: "Driver status", link: "/delivery-tracker/driver-status" },
            { text: "Lorries", link: "/delivery-tracker/lorries" },
            { text: "Trip form", link: "/delivery-tracker/trip-form" },
          ],
        },
        {
          text: "Drivers",
          items: [{ text: "Driver phone view", link: "/delivery-tracker/driver" }],
        },
        {
          text: "Help",
          items: [
            { text: "Points & commission", link: "/delivery-tracker/points" },
            { text: "Common problems", link: "/delivery-tracker/faq" },
          ],
        },
      ],
    },
    search: { provider: "local" },
    outline: { level: [2, 3], label: "On this page" },
    footer: { message: "Kow Hock Building Materials (M) Sdn Bhd · internal guides" },
  },
});
