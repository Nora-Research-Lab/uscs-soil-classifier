![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# USCS Soil Classifier
 
*For geotechnical engineers and engineering geologists: enter grain-size percentages and Atterberg limits to instantly get the Unified Soil Classification System (USCS) group symbol and name.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Geotechnical Engineering
 
The USCS Soil Classifier takes basic index properties of a soil sample and classifies it according to ASTM D2487. The user inputs: gravel percentage (>4.75 mm), sand percentage (0.075–4.75 mm), fines percentage (<0.075 mm, with silt vs clay distinguished via LL and PI), liquid limit (LL, %), plastic limit (PL, %), and for coarse soils (gravel+sand >50%): coefficient of uniformity (Cu) and coefficient of curvature (Cc). The core logic follows the USCS flow chart: first, if fines < 5%, classify based on Cu and Cc into well-graded (GW/SW) or poorly graded (GP/SP); if fines 5–12%, add dual symbols (e.g., SW-SC); if fines >12%, use plasticity chart (LL vs PI) to determine if fines are silt (M) or clay (C) and whether they are low (L) or high (H) plasticity. Also handle peat (PT) if organic content is indicated – a checkbox for organic. Output includes: USCS group symbol (e.g., SP-SM), group name (e.g., poorly graded sand with silt), and a simple text description (e.g., 'Sand with silt, low plasticity fines'). The Gradio UI has numeric inputs (sliders or text boxes) for percentages (constrained to sum 100), LL, PL, Cu, Cc, and a checkbox 'Organic?'. A 'Classify' button triggers the logic. Results are shown in a large text box and optionally a small bar chart of grain size distribution (simulated from percentages). No AI/ML component – pure rule-based classification. The tool is single-screen, responsive, and intended for quick field or lab classification.
 
## Run it
 
```bash
docker build -t uscs-soil-classifier .
docker run -p 7860:7860 uscs-soil-classifier
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-29.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
