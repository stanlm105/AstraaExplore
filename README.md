# 🌌 Welcome to MessierExplore — Free Astronomy Tools & Mini-Projects (work-in-progress)  Last update: Sep 2025
Exploring the cosmos via accessibility materials, tools, pipelines, and more to come.
> Explore the night sky with beginner-friendly utilities.  
> **Free to use. Open to peek under the hood.**

[![Made with Python](https://img.shields.io/badge/Python-3.11+-informational)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Status](https://img.shields.io/badge/status-active-blue)]()

Hi, my name is Mike. This journey is notes about my personal exploration of the night sky with milestones and goals. 
There are many different avenues one could take in this topic, that's part of the beauty of it! I can't say whether or not the avenue that I present here will be best for everyone, just the way I wish to approach it for myself. 
In a nutshell, the avenue of my journey is exploring via an 8" manual dobsonian telescope, plus accessories. 
The first part of my new journey here is the classic exercise of the Messier Observing Program of logging and sketch the 110 Messier objects.
Along the way, I’m exploring astrophotography and will share both triumphs and challenges.
I will freely add materials, tools, utilities here that aid me in the journey.

## Quick Links
- 📥 **Download / Use Tools:** see **Tools for Everyone** below
- 💻 **Peek at the Code:** see **Code & Repo Structure**
- 🗺️ **Roadmap / What’s Next:** see **Project Roadmap**

---

## Tools for Everyone

> One page, easy access. No install required.

### 1) Messier Observing Logbook (PDF)
- **What it is:** Printable, numbered logbook (110 objects), with full-page notes & sketch area, and a clean cover.
- **Get it:** No code needed, free: https://ms-ms-gh-me-logbook-696367436779.us-east4.run.app
- **Code:** Also in this repository as a python command-line script, and then as a web service; see files named logbook.
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


General Roadmap:

Quest 1: Messier Observing Program
-    a. Youtube Channel
        Coming soon. For those opting for longer play background narration, documenting my journey to certification of the messier observing program by Astronomical League
-    b. Messier Logbook Generator
        Coming soon. Small utility to generate a personalized log book for recording one's journey.<br>
        Format: Docker / GCS / Cloud Run<br>
        User interface: Web<br>
        Free
-    c. Messier Target Guidance Computer
        Coming soon. Small utility to auto-suggest the best Messier target to try given one's current location and the remaining objects remaining in one's quest.<br>
        Format: Docker / GCS / Cloud Run / Cloud SQL<br>
        User interface: Web<br>
        Free

Quest 2: Dobsonian Astrophotography
-    a. Image Stacking Pipeline Utilities
        Aimed at stacking images geared towards output from Dobsonian mounted micro four thirds DSLR exposures (as opposed to FIPS/SmartScope sources)<br>
        Aimed at being pragmatic and simple, not that this will be better or not better than other resources, just wishing to help beginners and be an avenue for those that might like my little bit infra/cloud tools approach to the topic.<br>
        Format: TBD<br>
        User interface: TBD<br>
        Free<br>

License<br>
Code: MIT (see LICENSE).<br>
Documentation/screenshots: CC BY 4.0 (see docs/LICENSE).<br>
Logo (docs/images/galaxy_logo.png): All Rights Reserved. Contact for permission.<br>


