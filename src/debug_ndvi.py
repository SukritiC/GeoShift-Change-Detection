import rasterio
import numpy as np
from src.differencer import calculate_ndvi, compute_change

def debug_values():
    before_path = "data/before.tif"
    after_path = "data/after.tif"
    
    print(f"Loading {before_path} and {after_path}...")
    
    with rasterio.open(before_path) as src:
        img_before = src.read()
        print(f"Before Image Stats: Min={img_before.min()}, Max={img_before.max()}, Mean={img_before.mean()}")
        print(f"Before Image Shape: {img_before.shape}")

    with rasterio.open(after_path) as src:
        img_after = src.read()
        print(f"After Image Stats: Min={img_after.min()}, Max={img_after.max()}, Mean={img_after.mean()}")

    # Calculate NDVI manually to check values
    ndvi_before = calculate_ndvi(img_before)
    print(f"NDVI Before Stats: Min={ndvi_before.min()}, Max={ndvi_before.max()}, Mean={ndvi_before.mean()}")
    
    ndvi_after = calculate_ndvi(img_after)
    print(f"NDVI After Stats: Min={ndvi_after.min()}, Max={ndvi_after.max()}, Mean={ndvi_after.mean()}")
    
    diff = ndvi_after - ndvi_before
    print(f"Difference Stats: Min={diff.min()}, Max={diff.max()}, Mean={diff.mean()}")
    
    # Check mask with default threshold
    threshold = 0.2
    mask = np.abs(diff) > threshold
    print(f"Mask with threshold {threshold}: Unique values={np.unique(mask)}")
    print(f"Total changed pixels: {np.sum(mask)}")

if __name__ == "__main__":
    debug_values()
