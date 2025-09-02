from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import random 
import re
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_key') # Replace with a secure key

# --- Initialize DB ---
def init_db():
    conn = sqlite3.connect('flavorforge.db')
    c = conn.cursor()

    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )''')

    # Blends table
    c.execute('''CREATE TABLE IF NOT EXISTS blends (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    flavor TEXT,
                    ingredients TEXT,
                    timestamp TEXT
                )''')

    # Feedback table
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    blend_id INTEGER,
                    rating INTEGER,
                    comments TEXT,
                    timestamp TEXT
                )''')

    conn.commit()
    conn.close()

init_db()
#strong password 
def is_strong_password(password):
    """Validate password strength: min 8 chars, upper, lower, digit, special char."""
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password)

# --- Routes ---
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect('/quiz')
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        raw_password = request.form['password']

        if not is_strong_password(raw_password):
            return "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character."

        password = generate_password_hash(raw_password)

        conn = sqlite3.connect('flavorforge.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists."
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('flavorforge.db')
        c = conn.cursor()
        c.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return redirect('/quiz')
        else:
            return "Invalid credentials."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/quiz')
def quiz():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('quiz.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'user_id' not in session:
        return redirect('/login')

    mood = request.form.get('mood')
    personality = request.form.get('personality')

    score_map = {
        'Relaxed': 'Sweet',
        'Adventurous': 'Spicy',
        'Focused': 'Umami',
        'Playful': 'Tangy',
        'Grounded': 'Savory'
    }

    flavor_profiles = {
        'Sweet': ['Honey', 'Vanilla', 'Cinnamon', 'Maple Syrup'],
        'Savory': ['Garlic', 'Thyme', 'Soy Sauce', 'Rosemary'],
        'Spicy': ['Chili', 'Black Pepper', 'Ginger', 'Wasabi'],
        'Umami': ['Miso', 'Parmesan', 'Mushroom', 'Anchovy'],
        'Tangy': ['Lemon', 'Tamarind', 'Vinegar', 'Yogurt']
    }

    mood_score = score_map.get(mood, 'Sweet')
    personality_score = score_map.get(personality, 'Savory')
    final_flavor = mood_score if mood_score == personality_score else random.choice([mood_score, personality_score])
    blend = random.sample(flavor_profiles[final_flavor], 2)

    conn = sqlite3.connect('flavorforge.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO blends (user_id, flavor, ingredients, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (session['user_id'], final_flavor, ', '.join(blend), datetime.now().isoformat()))
    blend_id = c.lastrowid
    conn.commit()
    conn.close()

    return render_template('result.html', flavor=final_flavor, blend=blend, blend_id=blend_id)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'user_id' not in session:
        return redirect('/login')

    rating = request.form.get('rating')
    comments = request.form.get('comments')
    blend_id = request.form.get('blend_id')

    conn = sqlite3.connect('flavorforge.db')
    c = conn.cursor()
    c.execute('''INSERT INTO feedback (user_id, blend_id, rating, comments, timestamp)
                 VALUES (?, ?, ?, ?, ?)''',
              (session['user_id'], blend_id, rating, comments, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return redirect('/quiz')

if __name__ == '__main__':
    app.run(debug=True)