"""
pipeline_utils.py
Lagos Barrier Island Shoreline Change Detection Project
 
Shared, reusable functions for the Sentinel-2 processing pipeline.
Imported by each stage-specific notebook (01, 02, 03...) so the core
logic lives in one place, rather than being copy-pasted across notebooks.
"""
 
import ee
 
 
def get_best_scene(year, aoi, start_month=11, end_month=3, cloud_limit=20):
    """Returns the lowest-cloud-cover Sentinel-2 L2A image for the given
    dry-season window spanning (year) Nov through (year+1) March."""
    start_date = ee.Date.fromYMD(year, start_month, 1)
    end_date = ee.Date.fromYMD(year + 1, end_month, 1).advance(1, "month")
 
    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_limit))
        .sort("CLOUDY_PIXEL_PERCENTAGE")
    )
 
    count = collection.size().getInfo()
    if count == 0:
        print(f"No scenes found for {year}-{year+1} dry season "
              f"under {cloud_limit}% cloud cover.")
        return None
 
    best = collection.first()
    cloud_pct = best.get("CLOUDY_PIXEL_PERCENTAGE").getInfo()
    scene_date = best.date().format("YYYY-MM-dd").getInfo()
    print(f"{year}-{year+1}: selected scene from {scene_date} "
          f"({cloud_pct:.1f}% cloud, {count} candidates in window)")
 
    return best.clip(aoi)
 
 
def mask_clouds_scl(image):
    """Masks cloud/shadow/snow pixels using the Sentinel-2 SCL band.
 
    SCL class values excluded:
        3  = cloud shadow
        8  = cloud, medium probability
        9  = cloud, high probability
        10 = thin cirrus
        11 = snow/ice
    """
    scl = image.select("SCL")
    mask = (
        scl.neq(3).And(scl.neq(8)).And(scl.neq(9))
        .And(scl.neq(10)).And(scl.neq(11))
    )
    return image.updateMask(mask)
 
 
def compute_mndwi(image):
    """Computes MNDWI = (Green - SWIR) / (Green + SWIR) and adds it as
    a new 'MNDWI' band. Sentinel-2 bands: B3 = Green, B11 = SWIR1."""
    mndwi = image.normalizedDifference(["B3", "B11"]).rename("MNDWI")
    return image.addBands(mndwi)
 
 
def otsu_threshold(histogram):
    """Computes the optimal threshold value from a histogram using Otsu's
    method - maximizing the between-class variance of two groups
    (water vs. land pixels)."""
    counts = ee.Array(ee.Dictionary(histogram).get("histogram"))
    means = ee.Array(ee.Dictionary(histogram).get("bucketMeans"))
    size = means.length().get([0])
    total = counts.reduce(ee.Reducer.sum(), [0]).get([0])
    total_sum = means.multiply(counts).reduce(ee.Reducer.sum(), [0]).get([0])
    mean = total_sum.divide(total)
 
    indices = ee.List.sequence(1, size.subtract(1))
 
    def bss_function(i):
        a_counts = counts.slice(0, 0, i)
        a_count = a_counts.reduce(ee.Reducer.sum(), [0]).get([0])
        a_means = means.slice(0, 0, i)
        a_mean = (
            a_means.multiply(a_counts)
            .reduce(ee.Reducer.sum(), [0])
            .get([0])
            .divide(a_count)
        )
        b_count = total.subtract(a_count)
        b_mean = total_sum.subtract(a_count.multiply(a_mean)).divide(b_count)
        return a_count.multiply(a_mean.subtract(mean).pow(2)).add(
            b_count.multiply(b_mean.subtract(mean).pow(2))
        )
 
    bss = indices.map(bss_function)
    return means.slice(0, 0, size.subtract(1)).sort(bss).get([-1])
 
 
def extract_water_mask(image, aoi):
    """Computes an Otsu threshold from the image's own MNDWI histogram,
    then returns a binary water mask (1 = water, 0 = land) and the
    threshold value used."""
    histogram = image.select("MNDWI").reduceRegion(
        reducer=ee.Reducer.histogram(255),
        geometry=aoi,
        scale=10,
        bestEffort=True,
    )
    threshold = otsu_threshold(histogram.get("MNDWI"))
    water_mask = image.select("MNDWI").gt(threshold)
    return water_mask, threshold
 
 
def mask_to_shoreline(water_mask, aoi, scale=10):
    """Converts a binary water mask into vector polygons - the boundary
    of these polygons is the shoreline."""
    return water_mask.selfMask().reduceToVectors(
        geometry=aoi,
        scale=scale,
        geometryType="polygon",
        eightConnected=True,
        maxPixels=1e9,
    )
 
 
def clean_shoreline_vectors(vectors, min_area_m2=2000):
    """Removes small speckle polygons below a minimum area (default
    2000 m^2, roughly 20 Sentinel-2 pixels at 10m resolution)."""
    vectors_with_area = vectors.map(
        lambda f: f.set("area_m2", f.geometry().area(maxError=1))
    )
    return vectors_with_area.filter(ee.Filter.gte("area_m2", min_area_m2))
 
 
def process_year(year, aoi):
    """Runs the complete pipeline for a single year: acquire -> mask
    clouds -> compute MNDWI -> threshold -> vectorize -> clean noise.
    Returns (cleaned_shoreline_vectors, threshold_value) or None if no
    scene was found for that year."""
    scene = get_best_scene(year, aoi)
    if scene is None:
        return None
 
    masked = mask_clouds_scl(scene)
    mndwi_img = compute_mndwi(masked)
    water_mask, threshold = extract_water_mask(mndwi_img, aoi)
    raw_vectors = mask_to_shoreline(water_mask, aoi)
    clean_vectors = clean_shoreline_vectors(raw_vectors)
 
    return clean_vectors, threshold.getInfo()