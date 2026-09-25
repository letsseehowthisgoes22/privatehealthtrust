# Private Health Trust: search and AI discoverability

Implemented September 18, 2026. Prepared for publication September 24, 2026. Search-engine submission remains separate from deployment.

## Natural-language search intent

These are editorial keyword targets based on the audience and content, not measured search-volume claims. They appear naturally in headings, answers, navigation, or metadata rather than a repeated keyword block.

| Parent's wording / query | Primary destination |
| --- | --- |
| How do I find the right rehab for my adult child? | /help-for-parents.html |
| My son needs help with addiction | /help-for-parents.html |
| My daughter needs mental health treatment | /help-for-parents.html |
| Who can help manage my adult child's mental health care? | /private-case-managers.html |
| Private mental health case manager | /private-case-managers.html |
| Help coordinating treatment for a family member | /private-case-managers.html |
| What if my adult child refuses rehab? | /help-for-parents.html |
| What questions should I ask a rehab? | /help-for-parents.html |
| What happens when my child comes home from rehab? | /family-guide.html |
| Can addiction treatment happen at home? | /in-home-treatment.html |
| Private rehab programs | /provider-directory.html |
| Caron inpatient programs Pennsylvania Florida | /caron-treatment-programs.html |
| How to choose rehab for a family member | /understanding-treatment.html |
| Case manager vs sober companion | /private-case-managers.html |

## Implemented

- Static HTML: content and all provider cards are present without JavaScript.
- Search filters progressively enhance the existing cards; no crawler needs to submit a form.
- One canonical URL, one title, one description and one H1 per page.
- Updated natural-language titles/descriptions on the five core guides.
- New WebSite, Organization, WebPage, BreadcrumbList, ItemList and visible-content-matched FAQPage JSON-LD on appropriate new pages.
- No invented star ratings, aggregate review counts, medical reviewers, accreditations, or clinical outcome scores.
- Parent hub, treatment directory, Caron guide and case-manager directory linked throughout the existing journal.
- Provider source links and a research date; old article dates retained.
- Sitemap lists all 59 canonical HTML URLs.
- robots.txt permits crawling and declares the sitemap.
- /llms.txt is a Markdown reading guide; /provider-directory.md exposes source-linked directory summaries.
- Social sharing image and metadata; responsive navigation and visible keyboard focus.
- Removed the nonfunctional G-XXXXXXXXXX analytics placeholder; existing Google site verification retained.

## Search-platform guidance

Google says established SEO practices remain relevant for its AI features; no special AI text file or schema is required for inclusion. The llms.txt file is an additional reading aid, not a promise of search ranking or AI citation. FAQ markup is not a promise of a Google FAQ rich result.

Sources:
- https://developers.google.com/search/docs/appearance/ai-features
- https://llmstxt.org/

## Review and release

Run `python3 scripts/build_site.py`, then `python3 scripts/validate_site.py` (requires BeautifulSoup), and `node --check directory.js`.

Before publication, confirm the deployment destination. After publication, verify live HTML/canonicals, sitemap and llms.txt responses, then use the domain's existing Search Console property to submit the sitemap. No deployment, indexing submission or ranking claim was made during this local update.
