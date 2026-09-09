Lagos Barrier Island Shoreline Change Detection (2017–2026)

Multi-temporal shoreline change detection using Sentinel-2 imagery for the Lagos Barrier Island coast, Nigeria.

🚧 Status: Week 3 complete — Shoreline change analysis done (transects, NSM/EPR/LRR, erosion/accretion map)

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
References
Licensing
Overview

Nigeria's coastline stretches roughly 853 km, and large stretches of it — including the Lagos Barrier Island coast — are undergoing measurable, ongoing erosion. This project builds a free, open-source, reproducible pipeline using Sentinel-2 optical satellite imagery to detect and quantify shoreline change over a nine-year period (2017–2026), and to visualize erosion/accretion risk along this coast.

Problem Statement

The Lagos Barrier Island segment — including Bar Beach, Ahmadu Bello Way, and Lekki — is experiencing ongoing coastal erosion, driven by a mix of natural coastal dynamics (wave action, longshore sediment transport, sea-level rise) and human activity (dredging of the Lekki-Ikoyi channel, jetty and breakwater construction disrupting sediment supply, unplanned coastal development). A prior SAR-based study (Tata & Isiaka, 2024) projecting shoreline change along this coast found substantial spatial variation rather than uniform erosion: communities such as Ojogun and Makoko were projected toward high erosion susceptibility (−32.3 to −5.1 m/yr), while Mobido was characterized as very low susceptibility and Okun-Ibese was actually projected toward accretion (+18 to +27.1 m/yr). This spatial heterogeneity — some stretches eroding while nearby stretches accrete — is itself a key motivation for a fine-grained, transect-based approach rather than treating the coast as uniformly at risk.

Despite this, there is no continuously updated, freely reproducible shoreline change dataset for this stretch of coast covering this period using optical satellite data. Existing studies tend to rely on radar (SAR) data or shorter time windows, and most Nigerian coastal monitoring relies on sparse field surveys or outdated aerial photography — expensive, slow, and infrequent.

Core question this project answers:

How can freely available Sentinel-2 optical imagery be used to build a reproducible, multi-year (2017–2026) shoreline change dataset for the Lagos Barrier Island coast, in order to quantify erosion/accretion rates at fine spatial resolution — using a low-cost, open-source Python + GIS workflow that could be replicated for any other Nigerian coastal site?

Data Limitations

Note on study period: The dataset begins in 2017 rather than 2016. Sentinel-2 L2A (surface reflectance) coverage is not available for the Lagos AOI prior to March 2017, confirmed by querying the COPERNICUS/S2_SR_HARMONIZED collection directly (zero images returned for the Nov 2016–Mar 2017 window, independent of cloud filtering). This is consistent with ESA's global rollout timeline for the L2A surface-reflectance product, rather than a gap specific to this AOI. The study period was adjusted to 2017–2026 accordingly, rather than substituting in an uncorrected (L1C) or cross-sensor (Landsat 8) alternative for a single year, to keep the dataset methodologically consistent across its full span.

Note on tidal variability: Each year's shoreline position is derived from a single Sentinel-2 scene (the lowest-cloud image in that year's dry-season window), rather than a tide-normalized composite. Tidal stage at the moment of image acquisition can shift the apparent water/land boundary by tens of meters independent of any real, gradual erosion or accretion trend. This contributes year-to-year noise that is reflected in generally low R² values for the linear regression rate (LRR) computed per transect — most transects show R² well under 0.5, meaning a straight-line trend only partially explains the observed variation. Transects with R² below 0.1 are flagged as lower-confidence in the erosion/accretion map (dashed style) rather than treated as equally reliable. A planned future improvement is compositing multiple dry-season scenes per year (e.g. a median MNDWI composite) to average out tidal noise — tracked as an open item for future work.

Note on community locations: The source SAR study (Tata & Isiaka, 2024) identifies at-risk and accreting communities only qualitatively (by rough position along the coast — e.g. "eastern" vs. "western" stretches), without publishing precise coordinates. As a result, this project does not attempt to plot exact community locations on the erosion/accretion map, since doing so would imply a level of spatial precision not supported by the available literature. Community names are referenced narratively in this documentation, not as mapped point locations.

Why This Site (AOI)

The Lagos Barrier Island coast was selected over other Nigerian coastal sites (e.g. the Niger Delta, Ondo State) for three reasons:

Cloud-free imagery is achievable. The Niger Delta is documented as persistently cloud-heavy and data-deficient for optical sensors, pushing researchers there toward SAR instead. Lagos has a genuine dry-season window (Nov–March) yielding usable Sentinel-2 scenes.
Simpler coastal geometry. An open barrier/spit coast (rather than a fragmented mangrove-creek system) produces cleaner, less noisy water-index thresholding and shoreline vectorization.
A validation benchmark already exists. A prior Sentinel-1 SAR-based DSAS study (Tata & Isiaka, 2024) found erosion rates of roughly 1.45 m/year along this coast on average, with substantial spatial variation. This project's optical-based results can be directly compared against that benchmark.
Objectives
✅ Build a multi-year (2017–2026), cloud-filtered Sentinel-2 shoreline dataset for the Lagos Barrier Island coast.
✅ Quantify shoreline change using standard metrics (NSM, EPR, LRR).
✅ Produce an erosion/accretion risk map.
✅ Validate results against existing SAR-based literature.
⬜ Deliver an open, reproducible pipeline that can be adapted to other Nigerian coastal sites.
Pipeline
Sentinel-2
    ↓
Cloud masking            ✅ done
    ↓
Water index               ✅ done (MNDWI)
    ↓
Shoreline extraction       ✅ done (Otsu thresholding + vectorization + noise cleanup)
    ↓
2017–2026 shoreline dataset ✅ done (599 features)
    ↓
Shoreline change analysis  ✅ done (transects, NSM/EPR/LRR)
    ↓
Erosion/accretion map      ✅ done (see /outputs)
    ↓
Python + GIS visualisation ✅ done (this pipeline, end to end)
Tools & Stack
Google Earth Engine — server-side Sentinel-2 querying, filtering, and processing
Python — earthengine-api, geemap, rasterio, geopandas, shapely, numpy, matplotlib, scipy
QGIS — cartographic visualization and manual QA
GitHub — version control, documentation, and public collaboration
VS Code — development environment
Repository Structure
/data          → final lightweight outputs (shorelines, masks) — no raw imagery
    lagos_shoreline_dataset_2017_2026.gpkg   — 599 shoreline features, 2017–2026

/notebooks     → Python/GEE notebooks, one per pipeline stage
    pipeline_utils.py          → shared, reusable functions (scene selection,
                                  cloud masking, MNDWI, Otsu thresholding,
                                  vectorization, noise cleanup) used across
                                  all three acquisition/processing notebooks
    01_data_acquisition.ipynb  → Sentinel-2 scene selection per year, visual QA
    02_preprocessing.ipynb     → cloud masking, MNDWI water index, visual QA
    03_shoreline_extraction.ipynb → Otsu thresholding, vectorization, noise
                                  cleanup, final dataset assembly and export
    04_change_analysis.ipynb  → baseline, transects, NSM/EPR/LRR,
                                  erosion/accretion map

/docs          → methodology write-up, weekly video links
/outputs       → final maps, figures
    lagos_erosion_accretion_map_2017_2026.png
Getting Started
bash
git clone https://github.com/hosea-ML/lagos-shoreline-change-sentinel2.git
cd lagos-shoreline-change-sentinel2
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# or: source venv/bin/activate # Mac/Linux
pip install -r requirements.txt

Earth Engine setup: the first run of any notebook requires a one-time Earth Engine authentication (a browser prompt will appear). If a later notebook stage needs to export data to Google Drive, request the Drive scope explicitly during authentication — see the authentication cell in 01_data_acquisition.ipynb (or any of the notebooks) for the exact scoped-authentication call used in this project.

Progress Log / Weekly Videos
Week	Focus	Video
1	Inspiration, AOI selection, problem statement, tooling	link pending
2	Sentinel-2 acquisition, cloud masking, MNDWI, Otsu-thresholded shoreline extraction, study period adjusted to 2017–2026, full dataset assembled (599 features), pipeline split into staged notebooks	link pending
3	Shoreline change analysis: reference baseline, transects, NSM/EPR/LRR computed per transect, erosion/accretion map produced and saved to /outputs. Diagnosed and fixed a transect-orientation bug; identified tidal variability as the main source of remaining measurement noise; corrected problem statement after reviewing the source SAR study more closely (erosion risk is spatially variable, not uniform across all named communities)	link pending
Contributing

This project is open to contributions — bug fixes, alternative index methods, additional AOIs, documentation improvements, and result validation are all welcome. See CONTRIBUTING.md for details on how to get involved.

References
Tata H, Isiaka IO (2024). Futuristic prediction of the lagoon coast shorelines using spaceborne Synthetic Aperture Radar (SAR) imagery. Nova Geodesia 4(2):184. https://novageodesia.ro/index.php/ng/article/download/184/66
Licensing
Code (scripts, notebooks): MIT License
Data & outputs (shoreline datasets, maps, figures): CC-BY 4.0