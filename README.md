# Gym Diet Daily Tracker

A simple Python + Flask beginner project to track daily meals, calories, and protein.

Features
	•	Add meals
	•	Track calories & protein
	•	Daily totals
	•	Local file storage (JSON)

### Run Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   # Default port 5002
   python IZ/app.py
   
   # Or use a custom port
   PORT=5003 python IZ/app.py
   ```

### Vercel Deployment

This project is configured for Vercel. 

> [!NOTE]
> **Data Persistence**: Because this app uses local JSON files, data is **not persistent** on Vercel. For long-term storage, consider migrating to a database (e.g., Supabase, MongoDB).

Stack

Python • Flask • HTML • CSS

IZ — eat clean, train consistent 
