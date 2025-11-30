import numpy as np
import rasterio


def calculate_ndvi(image):
    """
    Calculates NDVI from a 4-channel image (assuming R, G, B, NIR order).
    
    Args:
        image (numpy.ndarray): Image array of shape (channels, height, width).
        
    Returns:
        numpy.ndarray: NDVI map of shape (height, width).
        
    Raises:
        ValueError: If image has fewer than 4 bands.
    """
    # Assuming bands are: 1:Red, 2:Green, 3:Blue, 4:NIR
    if image.shape[0] < 4:
        raise ValueError(f"Image has {image.shape[0]} bands. Must have at least 4 bands (R, G, B, NIR) for NDVI.")

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
    
    Args:
        before_path (str): Path to the 'before' GeoTIFF.
        after_path (str): Path to the 'after' GeoTIFF.
        threshold (float): Threshold for significant change (0.0 to 1.0).
        
    Returns:
        tuple: (difference_map, change_mask)
    """
    with rasterio.open(before_path) as src_before:
        img_before = src_before.read()

    with rasterio.open(after_path) as src_after:
        img_after = src_after.read()

    # Ensure shapes match
    if img_before.shape != img_after.shape:
        raise ValueError(
            f"Dimension mismatch: Before {img_before.shape} vs After {img_after.shape}. Run preprocessing first."
        )

    ndvi_before = calculate_ndvi(img_before)
    ndvi_after = calculate_ndvi(img_after)

    # Calculate difference
    diff = ndvi_after - ndvi_before

    # Create mask: significant negative change (vegetation loss) or positive (growth)
    change_mask = np.abs(diff) > threshold

    return diff, change_mask


def save_results(diff, mask, profile, output_diff_path, output_mask_path):
    """
    Saves the difference map and change mask to GeoTIFFs.
    """
    # Update profile for single band output (Difference Map - Float32)
    # We keep the original nodata if it fits, or set to None if it doesn't make sense for diff
    # Usually diff map is float, so original nodata might be okay if it's float-compatible
    profile.update(count=1, dtype=rasterio.float32)
    
    with rasterio.open(output_diff_path, "w", **profile) as dst:
        dst.write(diff.astype(rasterio.float32), 1)

    # Update profile for Mask (UInt8)
    # IMPORTANT: Must update/clear nodata because original might be incompatible (e.g. -32768)
    profile.update(dtype=rasterio.uint8, nodata=None)
    
    with rasterio.open(output_mask_path, "w", **profile) as dst:
        dst.write(mask.astype(rasterio.uint8), 1)
