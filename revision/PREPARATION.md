# Preparation record

What four, five and six rim contacts identify about an elliptical aperture

Vedant Thaker · 21 November 2026

## Original work

Vedant Thaker is the sole author. He designed the original rim-contact localization study, wrote its manuscript, developed its original software, and requested the comparisons and checks reported in this revision.

The author reports that the research project began on 2 August 2026. The previous versions and the new revision represent different stages of the work.

## Revision activities

OpenAI Codex assisted with the identifiability analysis, numerical contact- and time-budget comparisons, the photographed-rim extraction and replay, and code and citation checks, as well as literature checks and preparation of the revised text. The author set the research question and requested the revision.

## Computational checks

The original re-execution matched the 96-row archived results.csv byte for byte. The independent implementation matched the 96 primary condition counts. The budget extension verifies center recovery from five and six generic noise-free points; its CSV records every method and both deadlines. The optical replay checks the image archive SHA-256 before reading measurements. Numeric checks used Python 3.12.14, NumPy 2.3.5 and Pillow 13.0.0.

## Data and version records

The baseline repository contains the original simulation and verifier. The accompanying supplement supplies the independent replay (run.py), contact_budgets.py, photo_rims.py, all resulting CSVs and hash-locked Linux requirements. Obtain the checksum-verified ring-board archive from [7] to repeat the optical analysis. The raw photographs remain with their provider.

[Original pinned software](https://github.com/VEDANT1602/aperture-contact-localization/tree/71f76e74192e47e6b9f4c19350aa7b4fb924cb4a) · [Revision code and data](https://github.com/VEDANT1602/aperture-contact-localization/tree/main/revision/supplement)

The reported checks are computational. No independent personal rerun or line-by-line review of these revisions by the author is asserted here.
