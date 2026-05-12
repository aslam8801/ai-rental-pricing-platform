# AI-Powered Rental Pricing & Comparable Retrieval Platform

## Overview

This project is an AI-powered real estate intelligence platform that predicts rental prices, retrieves semantically similar properties using vector search, and provides an interactive analytics dashboard.

The system combines:

* Machine Learning (XGBoost)
* Vector Search (pgvector)
* Semantic Embeddings
* FastAPI Backend
* React Frontend
* Supabase PostgreSQL
* LLM-based Query Understanding

---

# Features

## AI Rental Prediction

Predicts rental prices based on:

* Square footage
* Bedrooms
* School score
* Noise level

Uses:

* XGBoost Regressor

---

## Semantic Comparable Retrieval

Finds similar properties using:

* Sentence embeddings
* pgvector
* Cosine similarity search

This is similar to:

* Zillow recommendations
* Airbnb retrieval systems
* RAG-style retrieval pipelines

---

## LLM-Based Filtering

Supports natural language property filtering.

Example:

```text
remove noisy properties
```

LLM converts query into structured filters.

Uses:

* Groq API
* Llama 3

---

## Interactive Dashboard

Frontend dashboard includes:

* Prediction cards
* Charts
* Maps
* Comparable properties table
* Analytics visualization

---

## Feedback Learning System

Stores:

* Accepted comparables
* Rejected comparables
* Final selected rent

This creates a human-in-the-loop learning pipeline.

---

# Tech Stack

## Frontend

* React
* Tailwind CSS
* Axios
* Recharts
* React Leaflet

## Backend

* FastAPI
* Python
* XGBoost
* Sentence Transformers
* psycopg2

## Database

* Supabase PostgreSQL
* pgvector

## AI / ML

* XGBoost Regressor
* all-MiniLM-L6-v2 embeddings
* Llama 3 via Groq

---

# System Architecture

```text
React Dashboard
       ↓
FastAPI Backend
       ↓
ML Prediction + Vector Retrieval
       ↓
Supabase PostgreSQL + pgvector
       ↓
Semantic Similarity Search
```

---

# Project Structure

```text
Properties/
│
├── backend/
│   ├── main.py
│   ├── upload_properties.py
│   ├── intent_parser.py
│   ├── properties.csv
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   └── Dashboard.jsx
│   │   └── App.jsx
│   └── package.json
│
└── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone YOUR_GITHUB_REPO_URL
cd Properties
```

---

# Backend Setup

## 1. Navigate to Backend

```bash
cd backend
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

## 3. Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Configure Environment Variables

Create:

```text
backend/.env
```

Add:

```env
DB_HOST=YOUR_SUPABASE_HOST
DB_NAME=postgres
DB_USER=YOUR_SUPABASE_USER
DB_PASSWORD=YOUR_PASSWORD
DB_PORT=6543

GROQ_API_KEY=YOUR_GROQ_API_KEY
```

---

## 6. Start Backend

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

## 1. Navigate to Frontend

```bash
cd frontend
```

## 2. Install Dependencies

```bash
npm install
```

---

## 3. Start Frontend

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

# API Endpoints

## Predict Rent

```http
POST /predict
```

Example:

```json
{
  "sqft": 2000,
  "bedrooms": 3,
  "school_score": 8,
  "noise": 2
}
```

---

## Save Feedback

```http
POST /feedback
```

---

## Retrieve Similar Properties

```http
POST /similar-properties
```

Returns semantically similar comparable properties.

---

# Deployment

## Recommended Stack

| Layer    | Platform |
| -------- | -------- |
| Frontend | Vercel   |
| Backend  | Render   |
| Database | Supabase |

---

# Future Improvements

* SHAP explainability
* Authentication
* Real-world datasets
* Image embeddings
* LangChain agents
* Redis caching
* Docker support
* CI/CD pipelines

---

# Resume Description

```text
Built an AI-powered rental pricing platform using FastAPI, React, XGBoost, pgvector, and semantic embeddings. Implemented vector similarity search for comparable property retrieval, ML-based rent prediction, LLM-powered filtering, feedback learning, and interactive analytics dashboards with maps and charts.
```

---

# Author

Aslam Kureshi
