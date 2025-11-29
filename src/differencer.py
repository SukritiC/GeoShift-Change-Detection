import numpy as np
import rasterio

def calculate_ndvi(image):
    """
    Calculates NDVI from a 4-channel image (assuming R, G, B, NIR order).
    Formula: (NIR - Red) / (NIR + Red)
    """
    # Assuming bands are: 1:Red, 2:Green, 3:Blue, 4:NIR (Standard for many satellite products, but can vary)
    # Adjust indices based on actual data. For this MVP we'll assume 4 bands: R, G, B, NIR.
    # If 3 bands, we can't calculate NDVI properly without NIR.
    
    # Let's assume input is (channels, height, width)
    if image.shape[0] < 4:
        raise ValueError("Image must have at least 4 bands (R, G, B, NIR) for NDVI.")
        
    red = image[0].astype(float)
    nir = image[3].astype(float)
    
    # Avoid division by zero
    denominator = nir + red
    denominator[denominator == 0] = 0.0001
    
    ndvi = (nir - red) / denominator
    return ndvi

def compute_change(before_path, after_path, threshold=0.2):
    """
    Computes the difference in NDVI between two images.
    Returns the difference map and a binary change mask.
    """
    with rasterio.open(before_path) as src_before:
        img_before = src_before.read()
        
    with rasterio.open(after_path) as src_after:
        img_after = src_after.read()
        
    # Ensure shapes match (preprocessing should handle this, but good to check)
    if img_before.shape != img_after.shape:
        raise ValueError("Images must have the same dimensions. Run preprocessing first.")
        
    ndvi_before = calculate_ndvi(img_before)
    ndvi_after = calculate_ndvi(img_after)
    
    # Calculate difference
    diff = ndvi_after - ndvi_before
    
    # Create mask: significant negative change (vegetation loss) or positive (growth)
    # For general change, we can take absolute difference
    change_mask = np.abs(diff) > threshold
    
    return diff, change_mask

def save_results(diff, mask, profile, output_diff_path, output_mask_path):
    """
    Saves the difference map and change mask to GeoTIFFs.
    """
    # Update profile for single band output
    profile.update(count=1, dtype=rasterio.float32)
    
    with rasterio.open(output_diff_path, 'w', **profile) as dst:
        dst.write(diff.astype(rasterio.float32), 1)
        
    profile.update(dtype=rasterio.uint8)
    with rasterio.open(output_mask_path, 'w', **profile) as dst:
        dst.write(mask.astype(rasterio.uint8), 1)
