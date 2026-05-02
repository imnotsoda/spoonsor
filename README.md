# Spoonsor 🥄
**CS348 Semester Project — Campus Fundraising Deals App**

Spoonsor is a web app where West Lafayette restaurants partner with Purdue student orgs. Students use promo codes when dining out, and a percentage of their purchase is donated to the org.

## Live Demo
**App:** http://3.133.85.104:8000/static/index.html  
**API Docs:** http://3.133.85.104:8000/docs  
**Deployed on:** AWS EC2 + RDS (PostgreSQL)

## Tech Stack
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL (psycopg2)
- **Frontend:** Vanilla HTML/CSS/JS, Leaflet.js
- **Hosting:** AWS EC2 (app) + AWS RDS (database)

## Features
- **Requirement 1:** Full CRUD interface for managing deals (create, edit, delete)
- **Requirement 2:** Filterable report showing active deals by org, restaurant, and category — with summary stats

## Project Structure
```
spoonsor/
├── main.py          # FastAPI routes and endpoints
├── database.py      # Database connection and query helpers
├── schema.sql       # Table definitions, sample data, and indexes
├── requirements.txt # Python dependencies
└── static/          # Frontend HTML/CSS/JS files
```

## Setup (Local)

### Prerequisites
- Python 3.9+
- PostgreSQL

### Installation
```bash
# Clone the repo
git clone https://github.com/imnotsoda/spoonsor.git
cd spoonsor

# Install dependencies
pip install -r requirements.txt

# Set up the database
psql -d your_database -f schema.sql

# Set environment variables
export DB_HOST=localhost
export DB_NAME=fundraising_db
export DB_USER=your_username
export DB_PASSWORD=your_password

# Run the app
uvicorn main:app --reload
```

Then open: http://localhost:8000/static/index.html

## Database Schema
- **Organizations** — Purdue student orgs running fundraisers
- **Restaurants** — West Lafayette restaurants participating in deals
- **Deals** — Links orgs and restaurants with promo codes and donation percentages

## Security
- All queries use **parameterized statements** via psycopg2 — protected against SQL injection
- Database credentials stored as **environment variables**, not hardcoded in source

## Indexes
| Index | Table | Column | Supports |
|---|---|---|---|
| `idx_deals_org_id` | Deals | org_id | Report filtered by org |
| `idx_deals_restaurant_id` | Deals | restaurant_id | Report filtered by restaurant |
| `idx_deals_is_active` | Deals | is_active | Active deals filter (default report view) |
| `idx_restaurants_category` | Restaurants | category | Category filter on deals report |

## AI Usage
This project was built with assistance from:
- **Claude (Anthropic)** — FastAPI backend structure, debugging assistance, and generated the first draft of this README.md!
- **Google Antigravity** — Code formatting, sample data generation, frontend HTML/CSS implementation (layout and Purdue color scheme designed by the developer)

All AI-generated output was reviewed, tested, and modified to fit the project requirements.