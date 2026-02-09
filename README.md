# EcoFeast – Real-Time Food Waste Redistribution Platform

**EcoFeast** is a web-based platform that tackles food waste by creating a direct connection between businesses and individuals with surplus food and the NGOs that can distribute it to those in need. The system uses machine learning to assess food freshness and geospatial matching to optimize pickup logistics.

## Problem Statement
Millions of tons of edible food are wasted annually while communities face food insecurity. The disconnect between surplus food sources and distribution networks, combined with concerns about food safety and logistics, prevents effective redistribution. EcoFeast bridges this gap through intelligent automation and real-time coordination.

## What This Project Does

EcoFeast provides a complete workflow for food donation management:

### For Donors (Restaurants, Grocery Stores, Event Organizers)
* Submit surplus food listings with details about quantity, type, and storage conditions.
* Receive AI-calculated freshness scores that factor in local weather conditions.
* Auto-populate location data using reverse geocoding.
* Track donation status in real-time.

### For NGOs and Relief Organizations
* View available food donations on an interactive map.
* See freshness predictions to prioritize time-sensitive pickups.
* Claim donations with one-click assignment.
* Access route information for efficient collection.

### Intelligent Features
* **Machine Learning Model:** Predicts food freshness based on storage duration, temperature, and food category.
* **Real-Time Weather:** Integration with Open-Meteo API pulls real-time local weather data to improve prediction accuracy.
* **Hyperlocal Matching:** Geospatial matching shows nearest available donations.
* **Live Synchronization:** Live status updates prevent double-booking of donations.

---

## Technical Architecture

### Backend Infrastructure
* **Django Framework:** Handles request routing, business logic, and database operations.
* **RESTful API:** Endpoints for donation submission, retrieval, and status updates.
* **Database:** SQLite for development with production-ready PostgreSQL support.
* **Security:** Session management for user authentication and role-based access.

### Machine Learning Pipeline
* **Scikit-Learn:** Random Forest model trained on food freshness parameters.
* **Feature Engineering:** Combines temporal data (hours since donation), environmental factors (temperature, humidity), and food-specific attributes.
* **Data Processing:** Pandas and NumPy for preprocessing and transformation.
* **Output:** Probability score (0-100%) indicating safe consumption window.

### Frontend and Mapping
* **Leaflet.js:** Renders interactive maps with custom markers for donors and NGOs.
* **JavaScript:** Handles asynchronous updates for real-time status changes.
* **OpenStreetMap API:** Provides reverse geocoding for address completion.
* **Responsive Design:** HTML5 and CSS3 for mobile and desktop compatibility.

### External API Integration
* **Open-Meteo API:** Fetches hyperlocal weather data based on GPS coordinates.
* **OpenStreetMap Nominatim:** Converts latitude/longitude to human-readable addresses.

---

## Project Structure

```bash
EcoFeast/
├── manage.py              # Django project manager
├── requirements.txt       # Python dependencies
├── config/                # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── donations/             # Main application app
│   ├── models.py          # Database schema (Donations, Users)
│   ├── views.py           # Business logic & Request handlers
│   ├── ml_model.py        # Freshness prediction algorithm (Scikit-Learn)
│   ├── urls.py            # API routing
│   └── templates/         # HTML Frontend
│       ├── donate.html    # Donor submission form
│       ├── live_map.html  # Real-time pickup dashboard
│       └── base.html      # Shared layout
└── static/                # CSS, JS, and Images
    └── css/
