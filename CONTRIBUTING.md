Contributing to Lagos Barrier Island Shoreline Change Detection

Thanks for your interest in this project! It's an open, in-progress research pipeline for detecting shoreline change along the Lagos Barrier Island coast using Sentinel-2 imagery — and contributions of all sizes are welcome, from fixing a typo to proposing a better shoreline-extraction method.

Ways to Contribute
Bug reports — something in a script doesn't run, or produces an obviously wrong result
Methodology suggestions — a better water index, thresholding method, or cloud-masking approach
Additional AOIs — adapting the pipeline to another Nigerian coastal site (e.g. Ondo State, Niger Delta with a SAR swap-in)
Documentation improvements — clarifying setup steps, fixing broken links, improving explanations
Result validation — cross-checking outputs against other published erosion studies
Code quality — refactoring, adding tests, improving reproducibility
Before You Start
Check the existing Issues to see if your idea or bug is already being discussed.
For anything non-trivial (a new methodology, a structural change), please open an Issue first to discuss the approach before submitting a large Pull Request — this avoids duplicated effort or conflicting design decisions.
Read the current README.md to understand the project's problem statement, pipeline, and current status before proposing changes.
How to Submit a Change
Fork the repository.
Create a branch with a descriptive name, e.g. fix-cloud-mask-threshold or add-ondo-aoi.
Make your changes, keeping commits small and messages clear (e.g. "Fix Otsu threshold edge case for low-tide scenes" rather than "update").
If you're changing processing logic, please note why in your Pull Request description — what problem it solves or improves.
If your change affects results (e.g. a different index or threshold), include a brief before/after comparison if possible.
Open a Pull Request against the main branch, referencing the related Issue if applicable.
Code Style
Python code should be reasonably readable and commented, especially around any Earth Engine logic (which can be non-obvious to newcomers).
Keep raw imagery and large intermediate files out of the repo (see .gitignore) — only lightweight final outputs (vectors, small rasters) belong in /data or /outputs.
Licensing Note

By contributing, you agree that:

Code contributions are licensed under the project's MIT License.
Data/output contributions are licensed under CC-BY 4.0.
Questions?

Open an Issue with the question label, or reach out via the contact info in the repository profile.