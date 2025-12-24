IZ – Gym Diet Daily Tracker
IZ is a simple beginner-level Python + Flask web application to track your daily gym diet, calories, and protein intake.
This project is intentionally kept easy, clean, and well-structured so that beginners can understand how a basic Python website works.
Features
	Add daily meals
	Track:
	Calories
	Protein (grams)
	View:
	All meals added for the day
	Total calories consumed
	Total protein consumed
	Data stored locally (no database needed)
	Clean and simple UI
	Beginner-friendly Python code

Tech Stack
  Backend: Python
	Framework: Flask
	Frontend: HTML + CSS
  Storage: JSON file (local storage)

No JavaScript, no database, no complex setup.

Project Structure

IZ/
│
├── app.py              # Main Flask application
├── data.json           # Stores meal data locally
│
├── templates/
│   └── index.html      # Main webpage
│
└── static/
    └── style.css       # Styling file


Installation & Setup

1.Clone or Download the Project

git clone <repo-link>
cd IZ

Or simply download and extract the ZIP.

2.Install Required Library

Make sure Python is installed, then run:

pip install flask

3.Run the Application

python app.py

4.Open in Browser

Go to:

[http://127.0.0.1:5000/](http://127.0.0.1:5002/login)

How It Works
	User enters:
	Meal name
  Calories
	Protein
  On submit:
  Data is saved to data.json
  Homepage displays:
	All meals added
  Total calories
	Total protein

Data Storage
	All data is stored in a simple JSON file
	No database is used
	Easy to read, edit, and reset
	Ideal for learning purposes
  
Who Is This For?
	Python beginners
	Students learning Flask
	Gym beginners tracking diet
	Anyone who wants a simple real-world project

Future Improvements (Optional)
	Daily calorie goal tracking
	Macronutrient breakdown
	Authentication (login system)
	Convert to SaaS product
	Deploy to cloud (Render / Railway)

License

This project is open-source and free to use for learning and personal projects.

Project Name Meaning

IZ represents:

Simple, personal, and consistent growth
Just like fitness 💯
