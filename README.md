# 🌌 Welcome to MessierExplore — Free Astronomy Tools & Mini-Projects (work-in-progress)  Last update: Sep 2025
Exploring the cosmos via accessibility materials, tools, pipelines, and more to come.
> Explore the night sky with beginner-friendly utilities.  
> **Free to use. Open to peek under the hood.**

[![Made with Python](https://img.shields.io/badge/Python-3.11+-informational)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Status](https://img.shields.io/badge/status-active-blue)]()
[![Last Commit](https://img.shields.io/github/last-commit/stanlm105/MessierExplore)]()
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)]()

![Sample Logbook](static/logbook_sample.png)


> Hi, my name is Mike. MessierExplore is a personal astronomy journey turned open toolkit — offering logbooks, sky guidance, and astrophotography utilities. Free, beginner-friendly, and built with Python + cloud tools.<br><br>
> There are many different avenues one could take in this topic, which is fascinating. I'm intrigued by Red Cat's high production products, I'm intrigued by the automated pipelines and precise EQ tracking of SmartScopes. That said, the focus of the explorations here will be through that of the classic dobsonian. <br><br>
> The first quest in this journey is the classic exercise of the Messier Observing Program for manually logging and sketching the 110 Messier objects of the night sky.<br><br>
> The side quest is exploring astrophotography and will share both triumphs and challenges.<br><br>
> I will freely add materials, tools, utilities here that aid in the journey.<br><br>

---

## Quick Links
- 📥 [Download / Use Tools](#tools-for-everyone)  
- 💻 [Peek at the Code](#code--repo-structure)  
- 🗺️ [Roadmap / What’s Next](#project-roadmap)
---

## Tools for Everyone

> One page, easy access. No install required.

### 1) Messier Observing Logbook (PDF)
- **What it is:** Printable, numbered logbook (110 objects), with full-page notes & sketch area, and a clean cover.
- **Get it Free:** https://ms-ms-gh-me-logbook-696367436779.us-east4.run.app
- **Code:** Located in this repository as a python command-line script, and then as a web service; see files named logbook.
- **Features:** personalized cover page, checklist, per-object log pages, clean typography.

### 2) Messier Target Guidance (Web)
- **What it is:** Suggests the next best Messier targets based on your location/time, remaining items in your checklist and any other factors I can think of (darkness? angle from zenith?)
- **Try it:** (link when live)  
- **Inputs:** location, time, horizon cutoff; **Outputs:** ranked list with dusk/dawn windows. Sky darkness info.

### 3) Dobsonian Astrophotography — Simple Stacking Utils (CLI, GUI.. tbd)
- **What it is:** Lightweight, beginner-friendly image stacking pipeline for Dobsonian + MFT DSLR. For myself I'm planning micro four thirds adapter to keep weight down. Dobsonian is not expected to be best choice for astrophotography, but like a manual transmission car, I'd like to explore what steps optimize the fun and results even if it might not outclass dedicated rigs and smartscopes.
- **Download:** (link to release binary or quickstart)

> Want something added? Open an issue with feature ideas ✨

---

## Code & Repo Structure
```
├── assets/          # templates, static files
├── services/        # tools (eg logbook) as web services
├── tools/           # tools (eg logbook) as command line apps
├── tests/           # pytest test suite
└── utils/           # shared logic between web service apps and CLI apps 
```
---

## Project Roadmap

### Quest 1: Messier Observing Program
- [ ] YouTube Channel (journey to Astronomical League certification)  
- [ ] Messier Logbook Generator (Docker / GCS / Cloud Run)  
- [ ] Messier Target Guidance Computer (location-based, Cloud Run + SQL)  

### Quest 2: Dobsonian Astrophotography
- [ ] Image Stacking Pipeline Utilities (Dobsonian + MFT DSLR)  

---
## 📄 License
- Code: MIT (see [LICENSE](LICENSE))  
- Documentation/screenshots: CC BY 4.0 (see docs/LICENSE)  
- Logo: All Rights Reserved (contact for permission)  
