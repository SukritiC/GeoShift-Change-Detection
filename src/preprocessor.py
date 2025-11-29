import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject


def load_image(filepath):
    """
    Loads a GeoTIFF image.
    Returns the dataset object and the image array (channels, height, width).
    """
    with rasterio.open(filepath) as src:
        image = src.read()
        profile = src.profile
    return image, profile


def align_images(src_path, ref_path, output_path):
    """
    Aligns the source image to match the reference image's bounds, resolution, and CRS.
    Saves the aligned image to output_path.
    """
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
