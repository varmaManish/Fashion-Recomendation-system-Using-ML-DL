# Fashion Recommendation System Using ML & DL

A full-stack Machine Learning + Deep Learning system that delivers **image-based fashion recommendations** while demonstrating a **complete ML lifecycle** — from **automated data collection and metadata normalization** to **model retraining and API-driven inference**, modeled after real-world eCommerce AI pipelines.

---

## 🚀 Project Overview

This repository implements a **production-style Fashion Recommendation Engine** that goes beyond basic similarity search. It includes a **data ingestion layer, preprocessing automation, model training pipeline, and deployment-ready backend API**.

The system:
- Scrapes product images and metadata from eCommerce platforms (Flipkart)  
- Normalizes and renames image datasets using structured metadata  
- Retrains deep learning models on newly ingested data  
- Serves real-time visual similarity recommendations via an API interface  

This mirrors how **AI teams in retail companies maintain continuously learning recommendation systems.**

---

## 🧰 Key Features

- 🔍 **Image-Based Recommendation Engine**  
  Uses Deep Learning feature extraction (CNN embeddings) to return visually similar fashion items.

- 🕸 **Flipkart Data Scraper**  
  Automated script to collect **product images, titles, and metadata** to build and expand the training dataset.

- 🏷 **Metadata-Based File Renaming Pipeline**  
  Renames and organizes image files using scraped product metadata — enabling **clean dataset structure and traceability** for ML training and evaluation.

- 🔄 **Model Retraining Automation**  
  Scripted workflow to **retrain the recommendation model** when new data is added — simulating real-world continuous learning systems.

- ⚙ **Modular ML Architecture**  
  Clean separation between:
  - Data ingestion scripts  
  - Training & retraining logic  
  - Model inference API  
  - Frontend/UI layer  

- 🧪 **Production-Oriented Design**  
  Built with scalability and maintainability in mind — not just experimentation.

---

## 🏗 ML Pipeline Architecture
Flipkart Scraper
↓
Metadata Cleaner & File Renamer
↓
Image Dataset
↓
Deep Learning Feature Extractor
↓
Similarity Engine (Cosine / KNN)
↓
Backend API (Flask / FastAPI)
↓
Web UI

---

## 📦 Dependencies & Setup

```bash
git clone https://github.com/varmaManish/Fashion-Recomendation-system-Using-ML-DL.git
cd Fashion-Recomendation-system-Using-ML-DL
pip install -r requirement.txt
```
---
## Future Enhancements

-Cloud deployment (AWS / GCP / Azure)

-User personalization and recommendation history

-Model performance monitoring dashboard

-Multi-platform eCommerce scraping support

-CI/CD for automated model retraining

---
