# Private Health Trust

Static editorial website, enhanced September 18, 2026.

## Preview

```sh
python3 -m http.server 8769 --bind 127.0.0.1
```

Open http://127.0.0.1:8769/.

## Update directory content

Edit `data/providers.json`; then run:

```sh
python3 scripts/build_site.py
python3 scripts/validate_site.py
node --check directory.js
```

The builder uses Python's standard library. The validator requires `beautifulsoup4`. The browser needs no package install, framework, CDN, or build step.

The builder owns the homepage, treatment directory, private-case-manager directory, Caron guide, parent guide, methodology, about page, sitemap, robots.txt, llms.txt, and Markdown directory. Existing article bodies remain editable HTML; the builder applies shared navigation, footer, and related-reading links. It also maintains titles and descriptions on five core guides.

Source URLs and research date are stored with directory content. Preserve the distinction between residential care, primary mental health treatment, diagnostic evaluation, detox, and nonresidential care coordination.

See SEO-NOTES.md for keyword intent and search implementation.

## Publication

Production domain: https://privatehealthtrust.com. Hosting: Netlify. GitHub repository: letsseehowthisgoes22/privatehealthtrust, branch devin/initial-site. Canonical tags and the sitemap use the production domain.

Publish HTML, CSS, JavaScript, social-card.png, robots.txt, sitemap.xml, llms.txt and provider-directory.md through the site's confirmed hosting workflow. No environment variables or server-side application are required. Keep `.git` and internal maintenance files out of the deployed document root.
