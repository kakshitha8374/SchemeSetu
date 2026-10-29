# SchemeSetu: Scheme Verification Sheet

Last reviewed: 2026-10-29. Every scheme in `schemes.json` is still `"verified": false`.
Set a scheme to `true` only after you have opened its official page and confirmed each value below.

"Secondhand" means the value was seen on a third-party listing that cites official sources. It is not a substitute for checking the official page.

## Schemes removed after review

| Scheme | Reason |
| --- | --- |
| Karnataka Free Laptop Scheme | Reported discontinued by the Deputy CM in the Assembly (Deccan Herald, 19 March 2020). No current notice found. |
| Saandeepani Shishya Vethana (KSBDB) | Open to the Brahmin community only, not to all EWS or General students. The app has no community field. |
| Minority Post-Matric / MCM (Karnataka) | Needs a minority-community condition the app cannot check. Official page could not be opened. |

## Values still in use

| Scheme | Value | Status | Where to confirm |
| --- | --- | --- | --- |
| SSP SC Post-Matric | Income cap Rs 2.5 lakh | Not confirmed | https://ssp.postmatric.karnataka.gov.in |
| SSP SC Post-Matric | Benefit amount | Not stated in app (varies by course) | https://ssp.postmatric.karnataka.gov.in |
| SSP ST Post-Matric | Income cap Rs 2.5 lakh | Not confirmed | https://ssp.postmatric.karnataka.gov.in |
| BCWD Post-Matric | Income cap: Cat-1 Rs 2.5 lakh; Cat-2A, 3A, 3B Rs 1 lakh | Secondhand (Buddy4Study) | https://bcwd.karnataka.gov.in |
| BCWD Post-Matric | Benefit up to Rs 20,000 per year | Secondhand (Buddy4Study) | https://bcwd.karnataka.gov.in |
| Vidyasiri | Income cap, categories, Rs 1,500 per month | Not confirmed (page could not be opened) | https://bcwd.karnataka.gov.in |
| AICTE Pragati | Income cap Rs 8 lakh, courses, Rs 50,000 per year | Not confirmed (guidelines PDF could not be opened) | https://aicte.gov.in and https://scholarships.gov.in |
| Central Sector Scholarship | Income cap Rs 4.5 lakh | Secondhand (IndiaScholarships.in) | https://scholarships.gov.in |
| Central Sector Scholarship | Rs 12,000 per year (graduation), Rs 20,000 (post-graduation) | Secondhand (IndiaScholarships.in) | https://scholarships.gov.in |
| Central Sector Scholarship | Deadline 31-10-2026 | Listed on scholarships.gov.in; unclear if it applies to new or renewal applications | https://scholarships.gov.in |

## Known limits of the app

- Central Sector Scholarship also requires being in the top 80th percentile of the board stream. The app does not check this.
- BCWD Post-Matric uses the Rs 2.5 lakh Category 1 cap for all OBC students. Students in Cat-2A, 3A and 3B have a Rs 1 lakh cap, so the card text warns about this.
- Age and course conditions were removed where no source confirmed them.

## How to verify

1. Open each URL above and find the eligibility section.
2. Compare the value in the table with the page.
3. If it matches, note the date. If not, correct `schemes.json`.
4. Change `"verified"` to `true` only for schemes where every value matches.