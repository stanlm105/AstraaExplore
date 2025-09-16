![Logo](static/logo_main_2_nobg.png)

# 🌌 MessierExplore  
_Free Astronomy Tools & Mini-Projects — explore the night sky with smart, beginner-friendly utilities._  

[![Made with Python](https://img.shields.io/badge/Python-3.11+-informational)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Status](https://img.shields.io/badge/status-active-blue)]()
[![Last Commit](https://img.shields.io/github/last-commit/stanlm105/MessierExplore)]()
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)]()
![FastAPI](https://img.shields.io/badge/FastAPI-async-green)
![Cloud Run](https://img.shields.io/badge/Deployed%20on-Cloud%20Run-blue)
![Open-Meteo](https://img.shields.io/badge/Weather-Open--Meteo-lightblue)

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

### 2) Messier Target Guidance Computer (Web App)
- 📝 **Inputs:** location, passphrase  
- 📊 **Outputs:** ranked list of suggested Messier targets + tonight’s conditions  
- 🌐 **Try it:** (link when live)

> 🚀 **Why Target Guidance Computer is Exciting**  
> The Target Guidance Computer is more than a Messier checklist – it’s a smart companion that combines astronomy math with real-world conditions.  
> ✨ Shows you what you haven’t logged yet  
> 🌙 Highlights which objects sit high and clear of the Moon  
> ☁️ Explains how tonight’s clouds, darkness, and sky quality affect your session  
>  
> With nothing more than a passphrase and your postal code, the tool personalizes your observing journey, tracks your “seen” list, and serves up the best targets for **today at 9 PM local time**.  
> 💡 Lightweight, free, and built to grow – practical backend engineering powering human-friendly exploration of the night sky.

### 3) Dobsonian Astrophotography — Simple Stacking Utils (CLI, GUI.. tbd)
- **What it is:** Lightweight, beginner-friendly image stacking pipeline for Dobsonian + MFT DSLR. For myself I'm planning micro four thirds adapter to keep weight down. Dobsonian is not expected to be best choice for astrophotography, but like a manual transmission car, I'd like to explore what steps optimize the fun and results even if it might not outclass dedicated rigs and smartscopes.
- **Download:** (link to release binary or quickstart)

> Want something added? Open an issue with feature ideas ✨

---

## Code & Repo Structure
```text
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

---

⭐ If you like this project, give it a star and follow along — more tools are on the way!
