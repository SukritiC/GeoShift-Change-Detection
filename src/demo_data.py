import os
import requests
import zipfile
import io
import glob
import rasterio
import streamlit as st

def stack_landsat_bands(scene_dir, output_path):
    """
    Stacks Landsat 8 bands (4, 3, 2, 5) into a single GeoTIFF.
    
    Args:
        scene_dir (str): Directory containing the single-band TIFs.
        output_path (str): Path to save the stacked GeoTIFF.
    """
    # Bands: 4=Red, 3=Green, 2=Blue, 5=NIR
    try:
        band_files = {
            4: glob.glob(os.path.join(scene_dir, "*band4*.tif"))[0],
            3: glob.glob(os.path.join(scene_dir, "*band3*.tif"))[0],
            2: glob.glob(os.path.join(scene_dir, "*band2*.tif"))[0],
            5: glob.glob(os.path.join(scene_dir, "*band5*.tif"))[0],
        }
    except IndexError:
        raise FileNotFoundError(f"Could not find all required bands (2, 3, 4, 5) in {scene_dir}")
    
    # Read metadata from one band
    with rasterio.open(band_files[4]) as src0:
        meta = src0.meta.copy()
        
    meta.update(count=4)
    
    with rasterio.open(output_path, 'w', **meta) as dst:
        for i, b in enumerate([4, 3, 2, 5], start=1):
            with rasterio.open(band_files[b]) as src:
                dst.write(src.read(1), i)
                dst.set_band_description(i, f"Band {b}")

def fetch_demo_data(demo_dir="data/demo"):
    """
    Downloads and extracts the Cold Springs Fire dataset for demo purposes.
    
    Args:
        demo_dir (str): Directory to store the demo data.
        
    Returns:
        tuple: (before_path, after_path) if successful, else (None, None).
    """
    data_url = "https://ndownloader.figshare.com/files/10960109"
    os.makedirs(demo_dir, exist_ok=True)
    
    try:
        # 1. Download if not exists (check for a marker file or directory)
        if not os.path.exists(os.path.join(demo_dir, "landsat_collect")):
            r = requests.get(data_url)
            r.raise_for_status()
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(demo_dir)
        
        # 2. Identify Landsat Scenes
        # Pre-fire: July 7, 2016 (LC08...20160707...)
        # Post-fire: July 23, 2016 (LC08...20160723...)
        landsat_base = os.path.join(demo_dir, "landsat_collect")
        scenes = glob.glob(os.path.join(landsat_base, "LC08*"))
        
        pre_scene = next((s for s in scenes if "20160707" in s), None)
        post_scene = next((s for s in scenes if "20160723" in s), None)
        
        if pre_scene and post_scene:
            # Look into the 'crop' subdirectory usually
            pre_crop_dir = os.path.join(pre_scene, "crop")
            post_crop_dir = os.path.join(post_scene, "crop")
            
            # Stack bands
            before_tif = os.path.join(demo_dir, "before_stacked.tif")
            after_tif = os.path.join(demo_dir, "after_stacked.tif")
            
            if not os.path.exists(before_tif):
                stack_landsat_bands(pre_crop_dir, before_tif)
            if not os.path.exists(after_tif):
                stack_landsat_bands(post_crop_dir, after_tif)
            
            return before_tif, after_tif
        else:
            raise FileNotFoundError("Could not find expected Landsat scenes in the dataset.")
            
    except Exception:
        raise

def check_cached_demo_data(demo_dir="data/demo"):
    """Checks if processed demo data exists."""
    before_cached = os.path.join(demo_dir, "before_stacked.tif")
    after_cached = os.path.join(demo_dir, "after_stacked.tif")
    if os.path.exists(before_cached) and os.path.exists(after_cached):
        return before_cached, after_cached
    return None, None
