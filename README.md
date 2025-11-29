# GeoShift Change Detection
Satellite-Based Before vs After Change Detection using Geospatial ML

---

## Overview
GeoShift is an MVP system that detects and visualizes landscape changes using multi-temporal satellite imagery.
By comparing “Before vs After” scenes, the system automatically highlights areas that have undergone transformations such as:

✔ Deforestation
✔ New constructions & roads
✔ Water body shrinkage
✔ Urban expansion
✔ Agricultural land-use shift

The project demonstrates **remote sensing + machine learning + temporal analysis**, making it suitable for environmental monitoring & geospatial AI portfolios.

---

## Key Features
| Module | Capability |
|-------|------------|
| Data Acquisition | Download multi-date satellite images (Sentinel-2 / Landsat-8/9) |
| Pre-processing | Cloud masking • Band selection • Raster alignment |
| Change Detection Engine | NDVI differencing or Siamese CNN-based change mapping |
| Visualization Layer | Heatmaps + Before/After overlays + Swipe comparison |
| Output Metrics | % area changed, geospatial polygon extraction, GeoTIFF mask export |

---

## Methodology

### Option A — **Spectral Change Detection (MVP baseline)**
- Compute NDVI/NDWI/NBR for both timestamps
- Generate difference raster: `delta = im_after - im_before`
- Threshold differences to create change mask
- Overlay mask on original scene for visualization

### Option B — **Siamese Change Detection Model (Advanced)**
```
Image T1 → CNN Encoder ─┐
│→ Feature Difference → Upsampling Decoder → Change Mask
Image T2 → CNN Encoder ─┘
```
Loss Used: **Binary Cross Entropy + Dice**
Output: Pixel-level change classification heatmap

---

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| Geospatial Processing | Rasterio, GDAL, GeoPandas, Shapely |
| ML / DL | PyTorch / TensorFlow, Scikit-learn, OpenCV |
| Data Source | Google Earth Engine, Sentinel Hub API |
| Visualization | Folium/Leaflet, Matplotlib, Kepler.gl |
| Deployment | FastAPI/Streamlit + Docker (optional) |

---

## Project Structure
```
GeoShift-Change-Detection/
│── data/ # input imagery + output masks
│── notebooks/ # experimentation + visualization
│── src/
│ ├── preprocessor.py # image alignment + band extraction
│ ├── differencer.py # NDVI/NBR change computation
│ ├── model_siamese.py # deep learning architecture
│ ├── inference.py # run change predictions on new AOIs
│── results/ # heatmaps, overlays, reports
│── app.py # optional Streamlit/FastAPI frontend
│── README.md
```

---

## How to Run
```
git clone https://github.com/<username>/GeoShift-Change-Detection
cd GeoShift-Change-Detection

pip install -r requirements.txt
python src/differencer.py --t1 image_before.tif --t2 image_after.tif
streamlit run app.py
```

## License

This documentation and conceptual content are distributed under the **MIT License**.
See the [LICENSE](./LICENSE) file for more information.

---
## Connect with Me

I’m always open to connecting with **developers**, **AI enthusiasts**, and **innovators** working on **Generative AI projects**.
Let’s connect, collaborate, and create impact together!

<p align="center">
  <a href="https://www.linkedin.com/in/sukritichatterjee/" target="_blank" style="margin-right: 15px;">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="40" height="40" alt="LinkedIn"/>
  </a>
  <a href="https://github.com/SukritiC" target="_blank" style="margin-right: 15px;">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="40" height="40" alt="GitHub"/>
  </a>
   <a href="https://sukriti-speaks.medium.com/" target="_blank" style="margin-right: 15px;">
    <img src="src/medium.png" width="40" height="40" alt="Medium"/>
  </a>
  <a href="https://x.com/SukritiSpeak" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/9/95/Twitter_new_X_logo.png" width="40" height="40" alt="X (Twitter)"/>
  </a>
</p>

---

<p align="center">
  Let’s exchange ideas on <b>Generative AI</b> and build something extraordinary together. 🌍
</p>

---
