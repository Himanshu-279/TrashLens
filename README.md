<div align="center">

<img src="https://img.shields.io/badge/TrashLens-Smart%20Waste%20AI-2ea44f?style=for-the-badge&logo=leaf&logoColor=white" alt="TrashLens"/>

# ♻️ TrashLens
### *AI-Powered Intelligent Waste Classification & Management System*

[![Live Demo](https://img.shields.io/badge/🌐%20Live%20Demo-trashlens.onrender.com-blue?style=for-the-badge)](https://trashlens.onrender.com)
[![GitHub](https://img.shields.io/badge/GitHub-Himanshu--279-181717?style=for-the-badge&logo=github)](https://github.com/Himanshu-279/TrashLens)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10.1-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

> **TrashLens** is a production-grade, end-to-end intelligent waste classification platform powered by **EfficientNetV2-L** (95.6% accuracy). It classifies waste into **12 fine-grained categories**, helps users locate nearby recycling facilities, and continuously improves itself through an admin-triggered retraining pipeline — all deployable both as a web app and a fully **offline Android application**.

<br/>

---

</div>

## 📑 Table of Contents

- [✨ Key Highlights](#-key-highlights)
- [🧠 Model & Architecture](#-model--architecture)
- [🚀 Features](#-features)
- [🏗️ System Architecture](#️-system-architecture)
- [🛠️ Tech Stack](#️-tech-stack)
- [📂 Project Structure](#-project-structure)
- [⚡ Quick Start (Local)](#-quick-start-local)
- [🐳 Docker Setup](#-docker-setup)
- [📱 Android Application](#-android-application)
- [🌍 Deployment on Render](#-deployment-on-render)
- [🔁 Admin Panel & Retraining](#-admin-panel--retraining)
- [📊 Results](#-results)
- [🤝 Contributing](#-contributing)
- [📬 Contact](#-contact)

---

## ✨ Key Highlights

| | |
|---|---|
| 🎯 **95.6% Validation Accuracy** | EfficientNetV2-L on 12-class Kaggle Garbage Dataset |
| 📦 **15,515 Training Images** | battery · biological · brown-glass · cardboard · clothes · green-glass · metal · paper · plastic · shoes · trash · white-glass |
| 📡 **Fully Offline Android App** | TFLite model runs on-device — no internet needed after first launch |
| 🔁 **Self-Improving System** | Admin-triggered retraining on real user feedback — deploys automatically |
| ☁️ **Production Deployed** | Docker + Render + Supabase + Cloudinary |
| 🗺️ **Recycling Center Locator** | Haversine-based nearest facility finder by waste type |

---

## 🧠 Model & Architecture

TrashLens went through a systematic model evaluation before settling on the final architecture:

| Architecture | Val. Accuracy | Notes |
|---|---|---|
| Custom CNN (4-block) | 72.3% | Insufficient capacity for 12 classes |
| MobileNetV2 | 83.1% | Fast but limited representational depth |
| ResNet50 | 86.4% | Better, but plateaued below 90% |
| **EfficientNetV2-L** ✅ | **95.6%** | **Selected — compound scaling wins** |

### Two-Phase Transfer Learning Strategy

```
Phase 1 — Feature Extraction
  ├── Backbone: FROZEN (base_model.trainable = False)
  ├── Head trained: GAP → Dropout(0.3) → Dense(12, softmax)
  ├── Optimizer: Adam (lr=1e-4), Batch: 32
  └── Early stopping (patience=3), up to 10 epochs

Phase 2 — Progressive Fine-Tuning
  ├── Last 50 backbone layers: UNFROZEN
  ├── Optimizer: Adam (lr=1e-5), Batch: 8
  ├── mixed_float16 precision → ~50% GPU memory reduction
  └── Early stopping (patience=3), up to 10 epochs
```

**Dataset:** Kaggle Garbage Classification · 15,515 images · 80/20 split · seed=123  
**Class imbalance handled** via `compute_class_weight(strategy='balanced')` from scikit-learn

---

## 🚀 Features

- 🔍 **AI Waste Classification** — Upload any waste image; EfficientNetV2-L instantly predicts its category with confidence score
- 📍 **Recycling Center Locator** — Haversine distance-based nearest facility finder from `centers.csv`, filtered by waste type
- 📱 **Offline Android App** — Fully functional TFLite model runs on-device; no network dependency post-download
- 🔁 **Admin Retraining Loop** — One-click retraining on accumulated user feedback; updated model auto-deploys
- 📊 **Performance Dashboard** — Live per-class metrics, error distribution, and feedback analytics
- 🐳 **Dockerized** — Fully containerized; runs identically in any environment
- ☁️ **Cloud-Native** — Render deployment + Supabase (PostgreSQL) + Cloudinary CDN
- 📱 **Responsive UI** — Clean, mobile-friendly interface built with HTML5/CSS3/JavaScript

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     TrashLens Platform                      │
├─────────────────┬──────────────────┬────────────────────────┤
│   Web App       │  Android App     │   Admin Panel          │
│   (Django)      │  (Java/TFLite)   │   (Streamlit)          │
├─────────────────┼──────────────────┼────────────────────────┤
│ User uploads    │ Camera/Gallery   │ Feedback monitor       │
│ image via browser│ input (offline) │ Performance dashboard  │
│        │        │       │          │ Retraining trigger     │
│        ▼        │       ▼          │        │               │
│  Cloudinary CDN │ On-device TFLite │        ▼               │
│  (image store)  │ Interpreter      │  Supabase DB           │
│        │        │       │          │  (feedback store)      │
│        ▼        │       │          │        │               │
│  EfficientNetV2-L (keras)          │        ▼               │
│  Inference Engine                  │  Auto-retrain &        │
│        │                           │  redeploy model        │
│        ▼                           └────────────────────────┘
│  Supabase (PostgreSQL)
│  Classification logs + sessions
│        │
│        ▼
│  Recycling Center Locator
│  (centers.csv + Haversine)
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Deep Learning** | TensorFlow 2.10.1 / Keras · EfficientNetV2-L |
| **Web Backend** | Python 3.10 · Django 4.x · Gunicorn |
| **Mobile** | Android SDK (Java) · TensorFlow Lite |
| **Database** | Supabase (PostgreSQL) |
| **Media Storage** | Cloudinary CDN |
| **Containerization** | Docker |
| **Deployment** | Render |
| **Frontend** | HTML5 · CSS3 · JavaScript |
| **Training Hardware** | NVIDIA GPU (CUDA + TF 2.10.1) |

---

## 📂 Project Structure

```
TrashLens/
│
├── core/                          # Main Django application
│   ├── views.py                   # Classification + feedback views
│   ├── models.py                  # DB models (feedback, history)
│   ├── urls.py                    # URL routing
│   ├── utils.py                   # Preprocessing + inference helpers
│   └── templates/                 # HTML templates
│       ├── index.html             # Home page
│       ├── classify.html          # Upload + classify interface
│       ├── result.html            # Prediction output
│       ├── map_feedback.html      # Map + feedback form
│       └── admin_panel.html       # Admin dashboard
│
├── trashlens_project/             # Django project configuration
│   ├── settings.py                # App settings (Supabase, Cloudinary)
│   ├── urls.py                    # Root URL config
│   └── wsgi.py                    # WSGI entry point
│
├── Effi_WRM.keras                 # Trained EfficientNetV2-L model
├── Effi_WRM.tflite                # TFLite model for Android
├── centers.csv                    # Recycling center geospatial data
│
├── Dockerfile                     # Docker build config
├── build.sh                       # Render build script
├── requirements.txt               # Python dependencies
└── manage.py                      # Django CLI utility
```

---

## ⚡ Quick Start (Local)

### Prerequisites
- Python 3.10+
- Git
- (Optional) Docker

### 1. Clone the Repository

```bash
git clone https://github.com/Himanshu-279/TrashLens.git
cd TrashLens
```

### 2. Create & Activate Virtual Environment

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
CLOUDINARY_CLOUD_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Run the Server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser. 🎉

---

## 🐳 Docker Setup

```bash
# Build the image
docker build -t trashlens .

# Run the container
docker run -p 8000:8000 \
  -e SUPABASE_URL=your_url \
  -e SUPABASE_KEY=your_key \
  trashlens
```

Visit [http://localhost:8000](http://localhost:8000)

---

## 📱 Android Application

The TrashLens Android app uses a **TFLite version of EfficientNetV2-L** and supports **fully offline classification** after the initial model download.

```
First Launch:
  └── Model downloaded & saved to device storage

Every Subsequent Launch (even offline):
  └── TFLite Interpreter loads local model
  └── Camera / Gallery → Preprocess → Infer → Result
  └── Zero network requests for classification
```

> **Why offline?** API-dependent apps fail in low-connectivity zones — particularly relevant for rural India. TrashLens Android runs classification entirely on-device, making it reliable regardless of network availability.

**Download:** Available via the web app's homepage → *Download Android App* button.

---

## 🌍 Deployment on Render

This project is pre-configured for one-click deployment on [Render](https://render.com).

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a **New Web Service** and select this repo
4. Set the following:

| Setting | Value |
|---|---|
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn trashlens_project.wsgi:application` |
| **Environment** | Add your `.env` variables in Render's dashboard |

5. Click **Deploy** — Render handles the rest ✅

---

## 🔁 Admin Panel & Retraining

TrashLens includes a built-in Admin Panel that makes the system **self-improving**:

```
User submits feedback (correct / incorrect prediction)
         │
         ▼
Feedback stored in Supabase
         │
         ▼
Admin reviews dashboard (accuracy trends, error classes)
         │
         ▼
Admin clicks "Trigger Retraining"
         │
         ▼
System pulls misclassified samples from feedback DB
         │
         ▼
EfficientNetV2-L retrained on original + corrected data
         │
         ▼
Updated .keras model auto-deployed to web server
Android TFLite refreshes on next app launch ♻️
```

No manual ML engineering needed — just one button press.

---

## 📊 Results

### Per-Class Performance (EfficientNetV2-L · Validation Set · 3,103 images)

| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| battery | 0.95 | 0.94 | 0.94 | 189 |
| biological | 0.92 | 0.93 | 0.92 | 197 |
| brown-glass | 0.94 | 0.92 | 0.93 | 121 |
| cardboard | 0.94 | 0.95 | 0.94 | 178 |
| clothes | 0.97 | 0.98 | **0.97** | 1067 |
| green-glass | 0.93 | 0.91 | 0.92 | 131 |
| metal | 0.93 | 0.92 | 0.92 | 154 |
| paper | 0.94 | 0.95 | 0.94 | 214 |
| plastic | 0.92 | 0.91 | 0.92 | 173 |
| shoes | 0.96 | 0.97 | 0.96 | 402 |
| trash | 0.92 | 0.91 | 0.91 | 141 |
| white-glass | 0.94 | 0.93 | 0.93 | 136 |
| **Macro Avg** | **0.95** | **0.95** | **0.95** | **3103** |

---

## 🤝 Contributing

Contributions are warmly welcome! Here's how to get started:

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes and commit
git commit -m "feat: add your feature description"

# 4. Push to your branch
git push origin feature/your-feature-name

# 5. Open a Pull Request on GitHub
```

Please follow conventional commits and make sure your code is clean and documented.

---

## 📬 Contact

<div align="center">

**Himanshu Verma**  
B.Tech CSE · School of Management Sciences, Lucknow · AKTU 2026

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Himanshu%20Verma-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/himanshu-verma-1711)
[![GitHub](https://img.shields.io/badge/GitHub-Himanshu--279-181717?style=for-the-badge&logo=github)](https://github.com/Himanshu-279)

</div>

---

<div align="center">

Made with ❤️ for a cleaner planet 🌍

⭐ **Star this repo if you found it helpful!**

</div>
