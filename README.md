# Kow Hock Guides

User guides for Kow Hock's apps, one section per app. Built with [VitePress](https://vitepress.dev): every page is a Markdown file, and the site is built from them.

## Run it on your computer

```bash
npm install
npm run dev
```

Open the link it prints (usually http://localhost:5173). Pages reload as you edit.

## Where things are

```
index.md                  home page (list of apps)
delivery-tracker/         one Markdown file per page
delivery-tracker/img/     screenshots (WebP)
.vitepress/config.mts     site title, sidebar and menu
.vitepress/theme/         colours and the orange callout numbers
tools/screenshots/        scripts that retake the screenshots with demo data
```

## Writing a page

- Screenshots: `![What it shows](./img/name.webp)`. Callout numbers in the text match the circles on the picture:
  ```md
  <div class="callouts">

  - <span class="n">1</span> **Button name.** What it does.

  </div>
  ```
- Add the page to the sidebar in `.vitepress/config.mts`.
- Use the screen's exact button names in **bold**, so people can find them.

## Adding another app

1. Make a folder, for example `stock/`, with an `index.md` and an `img/` folder.
2. Add it to `nav` and `sidebar` in `.vitepress/config.mts`, and to the home page in `index.md`.

## Deploy

The site is hosted on GitHub Pages at https://kowhock.github.io/docs/. Every push to `main` rebuilds it through `.github/workflows/deploy.yml`. You can follow each run in the repo's **Actions** tab.

One-time setup: in the repo, go to **Settings → Pages** and set **Source** to **GitHub Actions**.

If the repo is renamed, change `base` in `.vitepress/config.mts` (and the logo path in `head`) to match the new name.
