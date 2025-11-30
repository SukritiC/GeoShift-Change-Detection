# GeoShift Change Detection - Presentation Materials

This document contains separate content for a **PowerPoint Presentation** and a **Video Demo Script**.

---

## Part 1: PowerPoint Presentation Content

**Slide 1: Title Slide**
*   **Main Title:** GeoShift Change Detection
*   **Subtitle:** Satellite-Based Landscape Monitoring using Geospatial ML
*   **Presenter Name:** [Your Name]
*   **Visual:** GeoShift Logo or a split-screen satellite image (Before/After).

**Slide 2: The Challenge**
*   **Heading:** Why Landscape Monitoring Matters?
*   **Bullet Points:**
    *   Rapid environmental changes (Deforestation, Urbanization, Climate Change).
    *   Manual monitoring is slow, expensive, and error-prone.
    *   Need for automated, scalable, and data-driven insights.
*   **Visual:** Iconography representing "Time", "Cost", and "Scale".

**Slide 3: Introducing GeoShift**
*   **Heading:** Automated Change Detection System
*   **Core Value Proposition:** An MVP system that detects and visualizes landscape transformations using multi-temporal satellite imagery.
*   **Key Capabilities:**
    *   Compares "Before" vs "After" scenes.
    *   Highlights significant changes automatically.
    *   Quantifies change (Area %).
*   **Visual:** Screenshot of the App Home Screen.

**Slide 4: How It Works (Methodology)**
*   **Heading:** Spectral Change Detection
*   **Bullet Points:**
    *   **Input:** Two GeoTIFF images (Time T1 & Time T2).
    *   **Alignment:** Automated image registration (Rasterio).
    *   **Analysis:** NDVI (Normalized Difference Vegetation Index) Differencing.
    *   **Logic:** `Change = |NDVI_after - NDVI_before| > Threshold`.
*   **Visual:** Simple flow diagram: Image 1 + Image 2 -> Preprocessing -> NDVI Calc -> Difference Map.

**Slide 5: Key Features**
*   **Heading:** Feature Overview
*   **Bullet Points:**
    *   **One-Click Demo:** Integrated "Load Demo Data" feature fetching real satellite imagery (Cold Springs Fire).
    *   **Smart Caching:** Automatically caches downloaded data for instant subsequent access.
    *   **Interactive Analysis:** Adjustable sensitivity threshold.
    *   **Tabbed Interface:** Organized views for "Analysis Results", "Map View", and "Details".
    *   **Visualizations:**
        *   Side-by-Side Comparison.
        *   Difference Heatmaps (Red=Loss, Green=Gain).
        *   Binary Change Masks.
*   **Visual:** Screenshot showing the new Tabbed UI and the "Use Cached Demo Data" button.

**Slide 6: Technology Stack**
*   **Heading:** Built With
*   **Content:**
    *   **Language:** Python 🐍
    *   **Frontend:** Streamlit (Tabbed Layout).
    *   **Geospatial:** Rasterio, NumPy (for raster data manipulation).
    *   **Computer Vision:** OpenCV (for image processing).
    *   **Data Fetching:** Requests & Zipfile (for automated dataset download).
    *   **Plotting:** Matplotlib (for heatmaps).

**Slide 7: Live Demo**
*   **Heading:** GeoShift in Action
*   **Content:** [Switch to Live Demo / Play Video]
*   **Talking Points:**
    *   Clicking "Load Demo Data" to fetch the Cold Springs Fire dataset.
    *   Exploring the "Analysis Results" tab for metrics and heatmaps.
    *   Switching to "Map View" for detailed visual inspection.
    *   Tuning the threshold slider and downloading results.

**Slide 8: Future Roadmap**
*   **Heading:** What's Next?
*   **Bullet Points:**
    *   **Deep Learning:** Implementing Siamese CNNs for semantic change detection.
    *   **Cloud Integration:** Auto-fetch satellite data (Sentinel/Landsat APIs).
    *   **Cloud Masking:** Robust handling of atmospheric noise.
    *   **Multi-class Detection:** Distinguishing between deforestation, construction, and water.

**Slide 9: Conclusion**
*   **Heading:** Thank You
*   **Call to Action:** Check out the code on GitHub!
*   **Links:** [GitHub Repository Link], [LinkedIn Profile]
*   **Visual:** QR Code to the Repo.

---

## Part 2: Video Presentation Script (Approx. 2-3 Minutes)

**[0:00 - 0:30] Intro & Problem Statement**
*   **Visual:** Face to camera or montage of satellite timelapse footage.
*   **Audio:** "Hi everyone! Did you know that our planet's landscape is changing faster than ever before? From rapid urbanization to critical deforestation, tracking these changes manually is nearly impossible. Today, I’m excited to introduce **GeoShift**—a satellite-based change detection system designed to automate this process using Geospatial Machine Learning."

**[0:30 - 1:00] What is GeoShift? (The Solution)**
*   **Visual:** Screen recording of the GeoShift Home Page, showing the clean UI.
*   **Audio:** "GeoShift is an MVP tool built with Python and Streamlit. It allows users to upload two satellite images taken at different times—a 'Before' shot and an 'After' shot. By leveraging spectral analysis, specifically NDVI differencing, the system automatically identifies and highlights areas that have undergone significant transformation."

**[1:00 - 1:45] Technical Deep Dive**
*   **Visual:** Slide showing the 'Methodology' diagram or code snippets from `differencer.py`.
*   **Audio:** "Under the hood, GeoShift uses **Rasterio** for handling geospatial raster data. When you upload images, the system first aligns them to ensure pixel-perfect correspondence. It then calculates the Normalized Difference Vegetation Index (NDVI) for both timestamps. By computing the difference and applying a user-defined threshold, we can isolate real changes from mere noise."

**[1:45 - 2:30] Live Demo Walkthrough**
*   **Visual:** Screen recording of the actual workflow.
    1.  *Cursor clicks 'Load Demo Data (Cold Springs Fire)'.*
    2.  *Shows the loading spinner, then the results appear.*
    3.  *Clicks through the tabs: 'Analysis Results', 'Map View', 'Details'.*
    4.  *Adjusts the 'Threshold' slider.*
*   **Audio:** "Let's see it in action. I've integrated a **One-Click Demo** feature. By clicking this button, the app automatically fetches the Cold Springs Fire dataset from EarthPy.
    Once processed, the results are organized into these clean tabs.
    In **Analysis Results**, we see the Heatmap—red areas indicate vegetation loss.
    Switching to **Map View**, we can compare the Before and After images side-by-side.
    And notice, if I reload, the app recognizes the data is already cached, so it loads instantly!"

**[2:30 - 3:00] Use Cases & Future Scope**
*   **Visual:** Show the "Future Roadmap" slide or return to face-to-camera.
*   **Audio:** "This tool is perfect for environmental monitoring, urban planning, and disaster assessment. While this MVP uses spectral methods, the next version will incorporate Deep Learning models like Siamese Networks for even higher accuracy.
    Thanks for watching! You can find the full source code on my GitHub linked below. Don't forget to star the repo if you find it useful!"
