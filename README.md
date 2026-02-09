EcoFeast – Real-Time Food Waste Redistribution Platform
EcoFeast is a web-based platform that tackles food waste by creating a direct connection between businesses and individuals with surplus food and the NGOs that can distribute it to those in need. The system uses machine learning to assess food freshness and geospatial matching to optimize pickup logistics.
Problem Statement
Millions of tons of edible food are wasted annually while communities face food insecurity. The disconnect between surplus food sources and distribution networks, combined with concerns about food safety and logistics, prevents effective redistribution. EcoFeast bridges this gap through intelligent automation and real-time coordination.
What This Project Does
EcoFeast provides a complete workflow for food donation management:
For Donors (Restaurants, Grocery Stores, Event Organizers):

Submit surplus food listings with details about quantity, type, and storage conditions
Receive AI-calculated freshness scores that factor in local weather conditions
Auto-populate location data using reverse geocoding
Track donation status in real-time

For NGOs and Relief Organizations:

View available food donations on an interactive map
See freshness predictions to prioritize time-sensitive pickups
Claim donations with one-click assignment
Access route information for efficient collection

Intelligent Features:

Machine learning model predicts food freshness based on storage duration, temperature, and food category
Integration with Open-Meteo API pulls real-time local weather data to improve prediction accuracy
Hyperlocal geospatial matching shows nearest available donations
Live status synchronization prevents double-booking of donations

Technical Architecture
Backend Infrastructure

Django framework handles request routing, business logic, and database operations
RESTful API endpoints for donation submission, retrieval, and status updates
SQLite database for development with production-ready PostgreSQL support
Session management for user authentication and role-based access

Machine Learning Pipeline

scikit-learn Random Forest model trained on food freshness parameters
Feature engineering combines temporal data (hours since donation), environmental factors (temperature, humidity), and food-specific attributes (category, initial quality)
Pandas and NumPy for data preprocessing and transformation
Model outputs probability score (0-100%) indicating safe consumption window

Frontend and Mapping

Leaflet.js renders interactive maps with custom markers for donors and NGOs
JavaScript handles asynchronous updates for real-time status changes
OpenStreetMap API provides reverse geocoding for address completion
Responsive design using HTML5 and CSS3 for mobile and desktop compatibility

External API Integration

Open-Meteo API fetches hyperlocal weather data (temperature, humidity) based on GPS coordinates
OpenStreetMap Nominatim service converts latitude/longitude to human-readable addresses
Error handling and fallback mechanisms for API rate limits and downtime

Project Structure
EcoFeast/
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── donations/
│   ├── models.py          # Database schema for donations, users, and pickups
│   ├── views.py           # Request handlers and business logic
│   ├── ml_model.py        # Freshness prediction algorithm
│   ├── urls.py
│   └── templates/
│       ├── donate.html    # Donor submission form
│       ├── live_map.html  # Real-time pickup dashboard
│       └── base.html
├── static/
│   ├── css/
│   ├── js/
│   │   └── map.js        # Leaflet configuration and marker logic
│   └── images/
└── db.sqlite3
Installation and Setup
Prerequisites

Python 3.8 or higher
pip package manager
Git

Local Development
Clone the repository:
bashgit clone https://github.com/SairajPP/EcoFeast.git
cd EcoFeast
Create and activate a virtual environment:
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
bashpip install -r requirements.txt
Apply database migrations:
bashpython manage.py migrate
Create a superuser for admin access (optional):
bashpython manage.py createsuperuser
Start the development server:
bashpython manage.py runserver
Access the application at http://localhost:8000
Usage Guide
Submitting a Donation

Navigate to the donation form
Allow location access or manually enter coordinates
Fill in food details (type, quantity, storage time)
System automatically fetches local weather and calculates freshness score
Submit to make donation visible on the live map

Claiming a Donation (NGO)

View the live pickups dashboard
Donations appear as markers with freshness indicators
Click on a marker to see details
Click "Claim Donation" to assign it to your organization
Access route information for pickup

Future Enhancements

Mobile application for on-the-go donation submissions
SMS notifications for NGOs when high-priority donations are posted
Historical analytics dashboard showing impact metrics (meals saved, CO2 reduction)
Integration with routing APIs for multi-stop pickup optimization
Blockchain-based donation tracking for transparency and tax documentation
Gamification features to encourage consistent donor participation

Dependencies
Key packages (full list in requirements.txt):

Django 4.x
scikit-learn
pandas
numpy
requests (for API calls)
python-dotenv (for environment configuration)

Contributing
Contributions are welcome. Please fork the repository, create a feature branch, and submit a pull request with a clear description of changes.
Contact
Sairaj Pawar
Email: sairajpawar716@gmail.com
LinkedIn: linkedin.com/in/your-profile
GitHub: github.com/SairajPP
