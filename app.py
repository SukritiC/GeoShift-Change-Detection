import streamlit as st
import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from src.differencer import compute_change, save_results
from src.preprocessor import align_images

st.set_page_config(page_title="GeoShift Change Detection", layout="wide")

st.title("GeoShift Change Detection MVP")
st.markdown("### Satellite-Based Before vs After Change Detection")

st.sidebar.header("Configuration")
uploaded_before = st.sidebar.file_uploader(
    "Upload 'Before' Image (GeoTIFF)", type=["tif", "tiff"]
)
uploaded_after = st.sidebar.file_uploader(
    "Upload 'After' Image (GeoTIFF)", type=["tif", "tiff"]
)

threshold = st.sidebar.slider("Change Threshold", 0.0, 1.0, 0.2, 0.05)
st.sidebar.info(
    """
    **Threshold Guide:**
    - **Lower (e.g., 0.1):** More sensitive. Detects subtle changes but may include noise.
    - **Higher (e.g., 0.5):** Less sensitive. Detects only significant changes.
    """
)


def save_uploaded_file(uploaded_file, filename):
    with open(filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filename


if uploaded_before and uploaded_after:
    with st.spinner("Processing images..."):
        # Save uploaded files temporarily
        os.makedirs("data/temp", exist_ok=True)
        before_path = save_uploaded_file(uploaded_before, "data/temp/before_upload.tif")
        after_path = save_uploaded_file(uploaded_after, "data/temp/after_upload.tif")

        # Align images (using 'before' as reference)
        # In a real scenario, we might want to align both to a common grid, but for MVP aligning 'after' to 'before' is fine.
        # Note: If images are already aligned (like our mock data), this might be redundant but safe.
        try:
            aligned_after_path = "data/temp/after_aligned.tif"
            align_images(after_path, before_path, aligned_after_path)

            # Compute change
            diff, mask = compute_change(before_path, aligned_after_path, threshold)

            # Calculate % Area Changed
            total_pixels = mask.size
            changed_pixels = np.count_nonzero(mask)
            pct_changed = (changed_pixels / total_pixels) * 100

            st.metric(label="Area Changed", value=f"{pct_changed:.2f}%")
            st.caption(
                f"**{pct_changed:.2f}%** of the total area has significant change (above threshold {threshold})."
            )

            # Visualization
            col1, col2, col3, col4 = st.columns(4)

            with rasterio.open(before_path) as src:
                # Display RGB (Bands 1, 2, 3) - Normalize for display
                img_before = src.read([1, 2, 3])
                img_before = np.moveaxis(img_before, 0, -1)
                # Normalize to 0-1 for display if not already
                if img_before.max() > 1:
                    img_before = img_before / 255.0
                col1.image(img_before, caption="Before Image", use_container_width=True)

            with rasterio.open(aligned_after_path) as src:
                img_after = src.read([1, 2, 3])
                img_after = np.moveaxis(img_after, 0, -1)
                if img_after.max() > 1:
                    img_after = img_after / 255.0
                col2.image(img_after, caption="After Image", use_container_width=True)

            # Display Difference Heatmap (Raw NDVI difference)
            # Normalize diff (-1 to 1) to 0-1 for display with colormap
            # We'll use matplotlib to apply a colormap
            fig, ax = plt.subplots()
            im = ax.imshow(diff, cmap="RdYlGn", vmin=-1, vmax=1)
            plt.colorbar(im, ax=ax)
            plt.axis("off")
            col3.pyplot(fig, use_container_width=True)
            col3.caption("NDVI Difference (Red=Loss, Green=Gain)")

            # Display Change Mask
            # Convert boolean mask to 0-255 for display
            mask_display = mask.astype(np.uint8) * 255
            col4.image(
                mask_display,
                caption="Change Mask (White = Change)",
                use_container_width=True,
            )

            st.success("Change detection complete!")

            st.info(
                """
            **Note on MVP Scope:**
            - This tool performs **spectral change detection** using NDVI.
            - It assumes images are relatively cloud-free.
            - Advanced features like automatic cloud masking or API-based downloading are part of the future roadmap.
            """
            )

            # Option to download results
            # Save to results folder first
            os.makedirs("results", exist_ok=True)
            with rasterio.open(before_path) as src:
                profile = src.profile
                save_results(
                    diff, mask, profile, "results/diff.tif", "results/mask.tif"
                )

            with open("results/mask.tif", "rb") as file:
                st.download_button(
                    label="Download Change Mask",
                    data=file,
                    file_name="change_mask.tif",
                    mime="image/tiff",
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    st.warning("Please upload both 'Before' and 'After' images to start.")
    st.markdown(
        """
    **Note:**
    - Images should be 4-band GeoTIFFs (Red, Green, Blue, NIR).
    - If you don't have images, you can generate mock data using `python src/generate_mock_data.py` and upload the files from `data/`.
    """
    )
