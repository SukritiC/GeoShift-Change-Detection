import numpy as np
import rasterio
from rasterio.transform import from_origin
import os


def create_mock_geotiff(filename, width=100, height=100, scenario="default"):
    """
    Creates a mock 4-band GeoTIFF (R, G, B, NIR).
    Scenarios:
    - "default": Standard deforestation (center square)
    - "small": Small deforestation (small square)
    - "large": Large deforestation (big square)
    - "growth": Vegetation growth (inverse of deforestation)
    - "no_change": No significant change
    """
    bands = 4
    # Base: Healthy vegetation (Low Red, High NIR)
    data = np.zeros((bands, height, width), dtype=rasterio.float32)
    data[0, :, :] = 50  # Red
    data[1, :, :] = 100  # Green
    data[2, :, :] = 50  # Blue
    data[3, :, :] = 200  # NIR (NDVI ~ 0.6)

    center_x, center_y = width // 2, height // 2

    if scenario == "default":
        size = 20
        # Deforestation: Moderate change (NDVI ~ 0.0)
        # Red 100, NIR 100 -> NDVI 0.0. Diff = 0.6
        data[
            0, center_y - size : center_y + size, center_x - size : center_x + size
        ] = 100
        data[
            3, center_y - size : center_y + size, center_x - size : center_x + size
        ] = 100

    elif scenario == "small":
        size = 5
        data[
            0, center_y - size : center_y + size, center_x - size : center_x + size
        ] = 100
        data[
            3, center_y - size : center_y + size, center_x - size : center_x + size
        ] = 100

    elif scenario == "large":
        size = 40
        data[
            0, center_y - size : center_y + size, center_x - size : center_x + size
        ] = 100
        data[
            3, center_y - size : center_y + size, center_x - size : center_x + size
        ] = 100

    elif scenario == "growth":
        size = 20
        # Growth in center: Red decreases, NIR increases
        data[
            0, center_y - size : center_y + size, 
            center_x - size : center_x + size
        ] = 50
        data[
            3, center_y - size : center_y + size, 
            center_x - size : center_x + size
        ] = 200

    elif scenario == "all_soil":
        # Bare soil everywhere (NDVI ~ 0.0)
        data[0, :, :] = 100
        data[3, :, :] = 100

    elif scenario == "no_change":
        pass  # Do nothing to the base

    # Add random noise
    rng = np.random.default_rng(42)
    # Increase noise slightly to +/- 30 to ensure it crosses low thresholds
    noise = rng.integers(-30, 30, (bands, height, width))
    data = data + noise
    data = np.clip(data, 0, 255).astype(rasterio.uint8)

    transform = from_origin(0, 0, 1, 1)
    crs = {"init": "epsg:4326"}

    with rasterio.open(
        filename,
        "w",
        driver="GTiff",
        height=height,
        width=width,
        count=bands,
        dtype=data.dtype,
        crs=crs,
        transform=transform,
    ) as dst:
        dst.write(data)


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    print("Generating diverse mock data...")

    # 1. Standard Deforestation (Medium Change)
    create_mock_geotiff(
        "data/case1_before.tif", scenario="no_change"
    )  # Base vegetation
    create_mock_geotiff("data/case1_after.tif", scenario="default")
    print(
        "- Case 1: Standard Deforestation (data/case1_before.tif, data/case1_after.tif)"
    )

    # 2. Small Change
    create_mock_geotiff("data/case2_before.tif", scenario="no_change")
    create_mock_geotiff("data/case2_after.tif", scenario="small")
    print("- Case 2: Small Change (data/case2_before.tif, data/case2_after.tif)")

    # 3. Large Change
    create_mock_geotiff("data/case3_before.tif", scenario="no_change")
    create_mock_geotiff("data/case3_after.tif", scenario="large")
    print("- Case 3: Large Change (data/case3_before.tif, data/case3_after.tif)")

    # 4. Vegetation Growth (Soil -> Vegetation)
    create_mock_geotiff("data/case4_before.tif", scenario="all_soil")
    create_mock_geotiff("data/case4_after.tif", scenario="growth")
    print("- Case 4: Vegetation Growth (data/case4_before.tif, data/case4_after.tif)")

    # 5. No Change
    create_mock_geotiff("data/case5_before.tif", scenario="no_change")
    create_mock_geotiff("data/case5_after.tif", scenario="no_change")
    print("- Case 5: No Change (data/case5_before.tif, data/case5_after.tif)")
