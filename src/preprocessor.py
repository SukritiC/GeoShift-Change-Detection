import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject


def load_image(filepath):
    """
    Loads a GeoTIFF image.
    
    Args:
        filepath (str): Path to the GeoTIFF file.
        
    Returns:
        tuple: (image_array, profile_metadata)
    """
    try:
        with rasterio.open(filepath) as src:
            image = src.read()
            profile = src.profile
        return image, profile
    except Exception as e:
        raise IOError(f"Failed to load image {filepath}: {e}")


def align_images(src_path, ref_path, output_path):
    """
    Aligns the source image to match the reference image's bounds, resolution, and CRS.
    
    Args:
        src_path (str): Path to the image to be aligned.
        ref_path (str): Path to the reference image.
        output_path (str): Path to save the aligned image.
        
    Returns:
        str: Path to the aligned output image.
    """
    try:
        with rasterio.open(ref_path) as ref:
            dst_crs = ref.crs
            dst_transform = ref.transform
            dst_width = ref.width
            dst_height = ref.height
            kwargs = ref.meta.copy()

        with rasterio.open(src_path) as src:
            kwargs.update(
                {
                    "crs": dst_crs,
                    "transform": dst_transform,
                    "width": dst_width,
                    "height": dst_height,
                }
            )

            with rasterio.open(output_path, "w", **kwargs) as dst:
                for i in range(1, src.count + 1):
                    reproject(
                        source=rasterio.band(src, i),
                        destination=rasterio.band(dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=dst_transform,
                        dst_crs=dst_crs,
                        resampling=Resampling.nearest,
                    )
        return output_path
    except Exception as e:
        raise RuntimeError(f"Alignment failed: {e}")
