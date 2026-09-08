Lagos Barrier Island Shoreline Change Detection (2017–2026)

Multi-temporal shoreline change detection using Sentinel-2 imagery for the Lagos Barrier Island coast, Nigeria.

🚧 Status: Week 2 — Data acquisition

Table of Contents
Overview
Problem Statement
Data Limitations
Why This Site (AOI)
Objectives
Pipeline
Tools & Stack
Repository Structure
Getting Started
Progress Log / Weekly Videos
Contributing
Licensing
Overview

Nigeria's coastline stretches roughly 853 km, and large stretches of it — including the Lagos Barrier Island coast — are undergoing measurable, ongoing erosion. This project builds a free, open-source, reproducible pipeline using Sentinel-2 optical satellite imagery to detect and quantify shoreline change over a nine-year period (2017–2026), and to visualize erosion/accretion risk for communities along this coast.

Problem Statement

The Lagos Barrier Island segment — including Bar Beach, Ahmadu Bello Way, Lekki, and lagoon-fringe communities such as Ojogun, Okun-Ibese, Makoko, and Mobido — is experiencing ongoing coastal erosion, driven by a mix of natural coastal dynamics (wave action, longshore sediment transport, sea-level rise) and human activity (dredging of the Lekki-Ikoyi channel, jetty and breakwater construction disrupting sediment supply, unplanned coastal development).

Despite this, there is no continuously updated, freely reproducible shoreline change dataset for this stretch of coast covering this period using optical satellite data. Existing studies tend to rely on radar (SAR) data or shorter time windows, and most Nigerian coastal monitoring relies on sparse field surveys or outdated aerial photography — expensive, slow, and infrequent.

Core question this project answers:

How can freely available Sentinel-2 optical imagery be used to build a reproducible, multi-year (2017–2026) shoreline change dataset for the Lagos Barrier Island coast, in order to quantify erosion/accretion rates and identify at-risk communities — using a low-cost, open-source Python + GIS workflow that could be replicated for any other Nigerian coastal site?

Data Limitations

Note on study period: The dataset begins in 2017 rather than 2016. Sentinel-2 L2A (surface reflectance) coverage is not available for the Lagos AOI prior to March 2017, confirmed by querying the COPERNICUS/S2_SR_HARMONIZED collection directly (zero images returned for the Nov 2016–Mar 2017 window, independent of cloud filtering). This is consistent with ESA's global rollout timeline for the L2A surface-reflectance product, rather than a gap specific to this AOI. The study period was adjusted to 2017–2026 accordingly, rather than substituting in an uncorrected (L1C) or cross-sensor (Landsat 8) alternative for a single year, to keep the dataset methodologically consistent across its full span.

Why This Site (AOI)

The Lagos Barrier Island coast was selected over other Nigerian coastal sites (e.g. the Niger Delta, Ondo State) for three reasons:

Cloud-free imagery is achievable. The Niger Delta is documented as persistently cloud-heavy and data-deficient for optical sensors, pushing researchers there toward SAR instead. Lagos has a genuine dry-season window (Nov–March) yielding usable Sentinel-2 scenes.
Simpler coastal geometry. An open barrier/spit coast (rather than a fragmented mangrove-creek system) produces cleaner, less noisy water-index thresholding and shoreline vectorization.
A validation benchmark already exists. A prior Sentinel-1 SAR-based DSAS study found erosion rates of roughly 1.45 m/year along this coast, naming at-risk communities. This project's optical-based results can be directly compared against that benchmark.
Objectives
Build a multi-year (2017–2026), cloud-filtered Sentinel-2 shoreline dataset for the Lagos Barrier Island coast.
Quantify shoreline change using standard metrics (NSM, EPR, LRR).
Produce an erosion/accretion risk map identifying at-risk communities.
Validate results against existing SAR-based literature.
Deliver an open, reproducible pipeline that can be adapted to other Nigerian coastal sites.
Pipeline
Sentinel-2
    ↓
Cloud masking
    ↓
Water index
    ↓
Shoreline extraction
    ↓
2017–2026 shoreline dataset
    ↓
Shoreline change analysis
    ↓
Erosion/accretion map
    ↓
Python + GIS visualisation
Tools & Stack
Google Earth Engine — server-side Sentinel-2 querying, filtering, and processing
Python — earthengine-api, geemap, rasterio, geopandas, shapely, numpy, matplotlib
QGIS — cartographic visualization and manual QA
GitHub — version control, documentation, and public collaboration
VS Code — development environment
Repository Structure
/data          → final lightweight outputs only (shorelines, masks) — no raw imagery
/notebooks     → Python/GEE notebooks, one per pipeline stage
/docs          → methodology write-up, weekly video links
/outputs       → final maps, figures
Getting Started
bash
git clone https://github.com/<hosea-ML>/lagos-shoreline-change-sentinel2.git
cd lagos-shoreline-change-sentinel2
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# or: source venv/bin/activate # Mac/Linux
pip install -r requirements.txt
Progress Log / Weekly Videos
Week	Focus	Video
1	Inspiration, AOI selection, problem statement, tooling	link pending
2	Sentinel-2 data acquisition, study period adjusted to 2017–2026	link pending
Contributing

This project is open to contributions — bug fixes, alternative index methods, additional AOIs, documentation improvements, and result validation are all welcome. See CONTRIBUTING.md for details on how to get involved.

Licensing
Code (scripts, notebooks): MIT License
Data & outputs (shoreline datasets, maps, figures): CC-BY 4.0