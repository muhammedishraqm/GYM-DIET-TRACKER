from flask import Flask, render_template, request, redirect, session, url_for, flash
import json
import os
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)
# SECRET KEY is required for 'session' (logging in) to work. 
# It keeps the data safe. In a real app, make this a long random string.
app.secret_key = "my_super_secret_gym_key"

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
DATA_FILE = 'data.json'
USERS_FILE = 'users.json'


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def load_data(filename, default):
    """Generic function to read JSON data from a file"""
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except:
        return default

def save_data(filename, data):
    """Generic function to save JSON data to a file"""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def get_user_meals(username):
    """Get meals ONLY for the specific user"""
    all_meals = load_data(DATA_FILE, [])
    # Filter list: Keep meal only if meal['username'] matches
    user_meals = [m for m in all_meals if m.get('username') == username]
    return user_meals

# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

# 1. Homepage (The Dashboard)
@app.route('/')
def index():
    # Check if user is logged in
    if 'username' not in session:
        return redirect(url_for('login')) # Send to login page if not logged in
    
    current_user = session['username']
    
    # Get ONLY this user's meals
    user_meals = get_user_meals(current_user)
    
    # Get today's date
    today_str = datetime.now().strftime("%Y-%m-%d")
    current_date_display = datetime.now().strftime("%B %d, %Y")

    # Initialize counters
    today_calories = 0
    today_protein = 0
    
    total_lifetime_calories = 0
    total_lifetime_protein = 0
    
    # For Average Calculation
    daily_stats = {} # Format: {'2023-10-27': {'calories': 2000, 'protein': 150}}

    today_meals_list = []

    for meal in user_meals:
        # Handle legacy data without date (assume today, or skip? Let's assume today for now to not lose data visibility)
        meal_date = meal.get('date', today_str) 
        
        m_cals = int(meal.get('calories', 0))
        m_prot = int(meal.get('protein', 0))
        
        # Lifetime totals
        total_lifetime_calories += m_cals
        total_lifetime_protein += m_prot
        
        # Aggregate for Daily Averages
        if meal_date not in daily_stats:
            daily_stats[meal_date] = {'calories': 0, 'protein': 0}
        daily_stats[meal_date]['calories'] += m_cals
        daily_stats[meal_date]['protein'] += m_prot
        
        # Today's Specifics
        if meal_date == today_str:
            today_calories += m_cals
            today_protein += m_prot
            today_meals_list.append(meal)

    # Calculate Averages
    days_logged = len(daily_stats)
    if days_logged > 0:
        avg_calories = int(total_lifetime_calories / days_logged)
        avg_protein = int(total_lifetime_protein / days_logged)
    else:
        avg_calories = 0
        avg_protein = 0

    return render_template('index.html', 
                         meals=today_meals_list, 
                         today_calories=today_calories, 
                         today_protein=today_protein,
                         avg_calories=avg_calories,
                         avg_protein=avg_protein,
                         total_calories=total_lifetime_calories,
                         total_protein=total_lifetime_protein,
                         date=current_date_display,
                         username=current_user)

# 2. Add Meal Route
@app.route('/add', methods=['POST'])
def add_meal():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get form data
    meal_name = request.form.get('meal_name')
    calories = request.form.get('calories')
    protein = request.form.get('protein')
    
    # Create the new meal entry
    new_meal = {
        'username': session['username'], # Attach the username!
        'name': meal_name,
        'calories': calories,
        'protein': protein,
        'time': datetime.now().strftime("%I:%M %p"),
        'date': datetime.now().strftime("%Y-%m-%d") # Store the date!
    }
    
    # Load ALL meals, add new one, and save back
    all_meals = load_data(DATA_FILE, [])
    all_meals.append(new_meal)
    save_data(DATA_FILE, all_meals)
    
    return redirect('/')

# 3. Reset (Clear only MY data)
@app.route('/reset')
def reset():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    current_user = session['username']
    all_meals = load_data(DATA_FILE, [])
    
    # Keep meals that do NOT belong to this user
    # (i.e., Delete only this user's meals)
    remaining_meals = [m for m in all_meals if m.get('username') != current_user]
    
    save_data(DATA_FILE, remaining_meals)
    return redirect('/')

# ---------------------------------------------------------
# LOGIN SYSTEM ROUTES
# ---------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        users = load_data(USERS_FILE, {})
        
        # Check if user exists and password matches
        if username in users and users[username] == password:
            session['username'] = username # Log them in!
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid username or password")
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        users = load_data(USERS_FILE, {})
        
        if username in users:
            return render_template('register.html', error="Username already taken!")
        
        # Add new user
        users[username] = password
        save_data(USERS_FILE, users)
        
        # Log them in automatically
        session['username'] = username
        return redirect('/')
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None) # Remove user from session
    return redirect(url_for('login'))

# Start the server
if __name__ == '__main__':
    # host='0.0.0.0' allows other devices on the same WiFi to connect!
    app.run(debug=True, host='0.0.0.0', port=5002)

