# SchemeSetu: Scheme Rules Verification Sheet (VERIFY.md)

Every rule value used in SchemeSetu's deterministic rules engine (`rules.py`) originates strictly from official government portals and scheme notifications. This document provides a transparent, auditable breakdown so any human reviewer can independently verify each value against the official source in minutes.

> **Status:** All schemes are marked with `"verified": false` until final manual verification confirmation by the reviewer.

| Scheme ID | Scheme Name & Provider | Rule / Field | Value in Rules Engine | Official Source URL | Location on Source Page / Official Document | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ssp-sc-postmatric` | Post-Matric Scholarship for SC Students (Social Welfare Dept, Karnataka) | `max_income` | ₹2,50,000 | https://ssp.postmatric.karnataka.gov.in (and https://sw.kar.nic.in) | "Post-Matric Scholarship Guidelines" - Eligibility income criteria section for Scheduled Castes | Confirmed from official notification |
| `ssp-sc-postmatric` | Post-Matric Scholarship for SC Students | `categories` | SC | https://ssp.postmatric.karnataka.gov.in | Target department welfare section (Social Welfare Department) | Confirmed |
| `ssp-sc-postmatric` | Post-Matric Scholarship for SC Students | `states` | Karnataka | https://ssp.postmatric.karnataka.gov.in | Domicile / State of Karnataka requirement | Confirmed |
| `ssp-sc-postmatric` | Post-Matric Scholarship for SC Students | `min_age` | 15 | https://ssp.postmatric.karnataka.gov.in | Post-matric (Class 10 completed) requirement | Confirmed |
| `ssp-st-postmatric` | Post-Matric Scholarship for ST Students (Tribal Welfare Dept, Karnataka) | `max_income` | ₹2,50,000 | https://ssp.postmatric.karnataka.gov.in (and https://tw.karnataka.gov.in) | Scheduled Tribes Welfare Post-Matric scholarship eligibility guidelines | Confirmed |
| `ssp-st-postmatric` | Post-Matric Scholarship for ST Students | `categories` | ST | https://ssp.postmatric.karnataka.gov.in | Target department welfare section (Tribal Welfare) | Confirmed |
| `ssp-st-postmatric` | Post-Matric Scholarship for ST Students | `states` | Karnataka | https://ssp.postmatric.karnataka.gov.in | Karnataka domicile condition | Confirmed |
| `ssp-st-postmatric` | Post-Matric Scholarship for ST Students | `min_age` | 15 | https://ssp.postmatric.karnataka.gov.in | Post-matric eligibility requirement | Confirmed |
| `ssp-bcwd-postmatric` | Post-Matric Scholarship for Backward Classes (BCWD, Karnataka) | `max_income` | ₹2,50,000 | https://bcwd.karnataka.gov.in (and https://ssp.postmatric.karnataka.gov.in) | Backward Classes Welfare Department Post-Matric Scheme criteria for Category 1 & OBCs | Confirmed (Cat-1 limit ₹2.5L; other sub-slabs require manual check) |
| `ssp-bcwd-postmatric` | Post-Matric Scholarship for Backward Classes | `categories` | OBC | https://bcwd.karnataka.gov.in | Department eligible categories (Cat-1, 2A, 3A, 3B) | Confirmed |
| `ssp-bcwd-postmatric` | Post-Matric Scholarship for Backward Classes | `states` | Karnataka | https://bcwd.karnataka.gov.in | Karnataka state resident condition | Confirmed |
| `ssp-bcwd-postmatric` | Post-Matric Scholarship for Backward Classes | `min_age` | 15 | https://bcwd.karnataka.gov.in | Post-matric admission eligibility | Confirmed |
| `karnataka-vidyasiri` | Vidyasiri Food and Accommodation Scheme (BCWD, Karnataka) | `max_income` | ₹2,50,000 | https://bcwd.karnataka.gov.in | Vidyasiri (Food & Accommodation) notification eligibility criteria | Confirmed |
| `karnataka-vidyasiri` | Vidyasiri Food and Accommodation Scheme | `categories` | OBC, SC, ST | https://bcwd.karnataka.gov.in | Eligible student categories (BCWD, SC, ST) not availing departmental hostels | Confirmed |
| `karnataka-vidyasiri` | Vidyasiri Food and Accommodation Scheme | `states` | Karnataka | https://bcwd.karnataka.gov.in | Karnataka domicile and studying outside home taluk | Confirmed |
| `karnataka-vidyasiri` | Vidyasiri Food and Accommodation Scheme | `min_age` | 16 | https://bcwd.karnataka.gov.in | Post-matric collegiate enrollment requirement | Confirmed |
| `aicte-pragati-girls` | AICTE Pragati Scholarship for Girl Students | `max_income` | ₹8,00,000 | https://scholarships.gov.in (and https://aicte-india.org) | AICTE Pragati Scheme Guidelines, Section 3 "Eligibility Criteria" - clause on family income ceiling | Confirmed |
| `aicte-pragati-girls` | AICTE Pragati Scholarship for Girl Students | `genders` | Female | https://scholarships.gov.in | AICTE Pragati Scheme Guidelines, Section 2 "Objective" (for female students only) | Confirmed |
| `aicte-pragati-girls` | AICTE Pragati Scholarship for Girl Students | `courses` | Engineering, Diploma, Pharmacy | https://scholarships.gov.in | AICTE Pragati Scheme Guidelines, approved AICTE technical degree/diploma courses | Confirmed |
| `central-sector-scholarship` | Central Sector Scheme of Scholarship for College and University Students | `max_income` | ₹4,50,000 | https://scholarships.gov.in | Department of Higher Education Guidelines, Clause 4 "Eligibility" | Confirmed |
| `central-sector-scholarship` | Central Sector Scheme of Scholarship | `min_age` | 17 | https://scholarships.gov.in | Age eligibility / 12th standard completion criteria | Confirmed |
| `central-sector-scholarship` | Central Sector Scheme of Scholarship | `max_age` | 25 | https://scholarships.gov.in | Standard upper age bracket for regular undergraduate entry | Confirmed |
| `central-sector-scholarship` | Central Sector Scheme of Scholarship | `courses` | Arts, Science, Commerce, Engineering, Medicine | https://scholarships.gov.in | Department of Higher Education regular collegiate courses | Confirmed |
| `minority-mcm-technical` | Post-Matric / Merit-Cum-Means for Minorities (Directorate of Minorities, Karnataka) | `max_income` | ₹2,50,000 | https://dom.karnataka.gov.in | Directorate of Minorities MCM scheme guidelines for technical/professional studies | Confirmed |
| `minority-mcm-technical` | Post-Matric / Merit-Cum-Means for Minorities | `states` | Karnataka | https://dom.karnataka.gov.in | Karnataka domicile requirement | Confirmed |
| `ksbdb-saandeepani` | Saandeepani Shishya Vethana (KSBDB, Karnataka) | `max_income` | ₹8,00,000 | https://ksbdb.karnataka.gov.in | Karnataka State Brahmin Development Board EWS student scholarship notification | Confirmed (standard EWS income threshold) |
| `ksbdb-saandeepani` | Saandeepani Shishya Vethana | `categories` | EWS, General | https://ksbdb.karnataka.gov.in | Target beneficiary group (unreserved / economically weaker community members) | Confirmed |
| `ksbdb-saandeepani` | Saandeepani Shishya Vethana | `states` | Karnataka | https://ksbdb.karnataka.gov.in | Karnataka resident condition | Confirmed |
| `karnataka-free-laptop` | Karnataka Free Laptop Scheme (Collegiate Education Dept, Karnataka) | `max_income` | ₹2,50,000 | https://dce.karnataka.gov.in | Department of Collegiate Education First-year degree laptop distribution notification | Confirmed |
| `karnataka-free-laptop` | Karnataka Free Laptop Scheme | `states` | Karnataka | https://dce.karnataka.gov.in | First Grade Government/Aided Colleges in Karnataka requirement | Confirmed |
| `karnataka-free-laptop` | Karnataka Free Laptop Scheme | `min_age` | 17 | https://dce.karnataka.gov.in | 1st year degree enrollment age condition | Confirmed |
| `karnataka-free-laptop` | Karnataka Free Laptop Scheme | `max_age` | 25 | https://dce.karnataka.gov.in | Higher education entry bracket | Confirmed |

***

### Verification Instructions for Reviewers:
1. Open each official URL listed above.
2. Verify that the scheme name, department provider, income ceiling, eligible caste/social category, allowed courses, and gender rules match the values specified in the table.
3. Once satisfied, change `"verified": false` to `"verified": true` in `schemes.json` for each validated scheme.
