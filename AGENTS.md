# Agent Notes

This repository is a static artist website for `lyahelia.art`.

## Project Type

- Static HTML/CSS/JS site.
- No npm, Vite, React, or build step is required.
- The site is intended to work on GitHub Pages.

## Local Preview

Important: do not open `index.html` directly. Do not use `file://`.

Run from the repository root:

```sh
python3 -m http.server 5173 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:5173
```

Use the local HTTP server so relative paths behave like production. If asked to "open site", start the server first, then open `http://127.0.0.1:5173`.

In Zed, use the project task:

```text
Start site
```

## Important Files

- `index.html` - homepage.
- `css/style.css` - main styles for the whole site.
- `js/main.js` - shared frontend behavior.
- `pages/` - inner pages.
- `images/` - site images and artwork assets.
- `video/` - video assets.

## Editing Guidelines

- Keep the site simple and static unless explicitly asked otherwise.
- Preserve existing page URLs and relative links.
- Do not introduce a JS framework or package manager for small edits.
- Avoid broad auto-formatting of HTML/CSS; keep diffs focused.
- Keep image and video paths unchanged unless intentionally replacing assets.
- Check both desktop and mobile layouts after visual changes.

## Git Notes

- `.zed/` is local editor config and is ignored by Git.
