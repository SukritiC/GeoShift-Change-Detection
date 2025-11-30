import streamlit as st
import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from src.differencer import compute_change, save_results
from src.preprocessor import align_images
from src.demo_data import fetch_demo_data, check_cached_demo_data

st.set_page_config(page_title="GeoShift Change Detection", layout="wide")

st.title("GeoShift Change Detection MVP")
st.markdown("### Satellite-Based Before vs After Change Detection")

# --- Sidebar Configuration ---
st.sidebar.header("Configuration")

# Initialize session state
if "demo_loaded" not in st.session_state:
    st.session_state.demo_loaded = False
if "before_path" not in st.session_state:
    st.session_state.before_path = None
if "after_path" not in st.session_state:
    st.session_state.after_path = None

# Check for cached demo data
cached_before, cached_after = check_cached_demo_data()
demo_available = cached_before is not None

# Sidebar Logic
if not st.session_state.demo_loaded:
    st.sidebar.subheader("Data Source")
    if demo_available:
        if st.sidebar.button("Use Cached Demo Data (Cold Springs Fire)"):
            st.session_state.before_path = cached_before
            st.session_state.after_path = cached_after
            st.session_state.demo_loaded = True
            st.rerun()
        st.sidebar.caption("✅ Demo data found locally.")
    else:
        if st.sidebar.button("Download & Load Demo Data"):
            with st.spinner("Fetching demo data..."):
                try:
                    b_path, a_path = fetch_demo_data()
                    st.session_state.before_path = b_path
                    st.session_state.after_path = a_path
                    st.session_state.demo_loaded = True
                    st.success("Demo data loaded!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Manual Upload")
    uploaded_before = st.sidebar.file_uploader(
        "Upload 'Before' Image (GeoTIFF)", type=["tif", "tiff"], key="up_before"
    )
    uploaded_after = st.sidebar.file_uploader(
        "Upload 'After' Image (GeoTIFF)", type=["tif", "tiff"], key="up_after"
    )
else:
    st.sidebar.success("Using Demo Data")
    if st.sidebar.button("Clear / Reset"):
        st.session_state.demo_loaded = False
        st.session_state.before_path = None
        st.session_state.after_path = None
        st.rerun()
    uploaded_before = None
    uploaded_after = None

threshold = st.sidebar.slider("Change Threshold", 0.0, 1.0, 0.2, 0.05)
st.sidebar.info(
    """
    **Threshold Guide:**
    - **Lower (e.g., 0.1):** More sensitive.
    - **Higher (e.g., 0.5):** Less sensitive.
    """
)

def save_uploaded_file(uploaded_file, filename):
    with open(filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filename

# Determine files to process
before_path_to_process = None
after_path_to_process = None

if st.session_state.demo_loaded:
    before_path_to_process = st.session_state.before_path
    after_path_to_process = st.session_state.after_path
elif uploaded_before and uploaded_after:
    os.makedirs("data/temp", exist_ok=True)
    before_path_to_process = save_uploaded_file(uploaded_before, "data/temp/before_upload.tif")
    after_path_to_process = save_uploaded_file(uploaded_after, "data/temp/after_upload.tif")

# Main Content Area
if before_path_to_process and after_path_to_process:
    
    tab1, tab2, tab3 = st.tabs(["📊 Analysis Results", "🗺️ Map View", "ℹ️ Details"])
    
    with st.spinner("Processing analysis..."):
        try:
            # Align images
            aligned_after_path = "data/temp/after_aligned.tif"
            os.makedirs("data/temp", exist_ok=True)
            align_images(after_path_to_process, before_path_to_process, aligned_after_path)

            # Compute change
            diff, mask = compute_change(before_path_to_process, aligned_after_path, threshold)

            # Metrics
            total_pixels = mask.size
            changed_pixels = np.count_nonzero(mask)
            pct_changed = (changed_pixels / total_pixels) * 100

            with tab1:
                st.metric(label="Area Changed", value=f"{pct_changed:.2f}%")
                st.caption(f"Significant change detected above threshold {threshold}.")
                
                col1, col2 = st.columns(2)
                
                # Display Difference Heatmap
                fig, ax = plt.subplots()
                im = ax.imshow(diff, cmap="RdYlGn", vmin=-1, vmax=1)
                plt.colorbar(im, ax=ax)
                plt.axis("off")
                col1.pyplot(fig, use_container_width=True)
                col1.caption("NDVI Difference (Red=Loss, Green=Gain)")

                # Display Change Mask
                mask_display = mask.astype(np.uint8) * 255
                col2.image(mask_display, caption="Change Mask (White = Change)", use_container_width=True)
                
                # Download
                os.makedirs("results", exist_ok=True)
                with rasterio.open(before_path_to_process) as src:
                    profile = src.profile
                    save_results(diff, mask, profile, "results/diff.tif", "results/mask.tif")

                with open("results/mask.tif", "rb") as file:
                    st.download_button(
                        label="Download Change Mask",
                        data=file,
                        file_name="change_mask.tif",
                        mime="image/tiff",
                    )

            with tab2:
                col1, col2 = st.columns(2)
                with rasterio.open(before_path_to_process) as src:
                    if src.count >= 3:
                        img_before = src.read([1, 2, 3])
                        img_before = np.moveaxis(img_before, 0, -1)
                    else:
                        img_before = src.read(1)
                    
                    if img_before.max() > 1:
                        img_before = img_before / 255.0 if img_before.max() > 255 else img_before / img_before.max()
                    col1.image(img_before, caption="Before Image", use_container_width=True, clamp=True)

                with rasterio.open(aligned_after_path) as src:
                    if src.count >= 3:
                        img_after = src.read([1, 2, 3])
                        img_after = np.moveaxis(img_after, 0, -1)
                    else:
                        img_after = src.read(1)
                    
                    if img_after.max() > 1:
                        img_after = img_after / 255.0 if img_after.max() > 255 else img_after / img_after.max()
                    col2.image(img_after, caption="After Image", use_container_width=True, clamp=True)

            with tab3:
                st.info(
                    """
                    **Methodology:**
                    - **Spectral Change Detection:** Uses NDVI (Normalized Difference Vegetation Index).
                    - **Formula:** `Change = NDVI_after - NDVI_before`
                    - **Thresholding:** Filters out noise based on user input.
                    """
                )

        except Exception as e:
            st.error(f"An error occurred during processing: {e}")

else:
    st.info("👈 Please select a data source from the sidebar to begin.")
