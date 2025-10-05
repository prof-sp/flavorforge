# FlavorForge - Personalized Flavor Generator

![Flask](https://img.shields.io/badge/Framework-Flask-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-green)

FlavorForge is a web application that generates personalized flavor blends based on user's mood and personality traits. It includes user authentication, flavor generation, and feedback collection features.

## Features

- **User Authentication**:
  - Secure registration with password hashing
  - Password strength validation (8+ chars, uppercase, lowercase, number, special char)
  - Session-based login/logout

- **Flavor Generation**:
  - Generates flavor blends based on mood and personality inputs
  - 5 flavor profiles: Sweet, Savory, Spicy, Umami, Tangy
  - Random selection of ingredients from matching profile

- **Data Persistence**:
  - SQLite database storage
  - Tracks user blends and feedback

## Installation

1. **Prerequisites**:
   - Python 3.7+
   - pip package manager

2. **Setup**:
   ```bash
   git clone [your-repository-url]
   cd flavorforge
   pip install -r requirements.txt

 File Structure
 flavorforge/
├── app.py                # Main application file
├── flavorforge.db        # SQLite database (created on first run)
├── templates/            # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── quiz.html
│   └── result.html
└── README.md
 Database Schema

users:

id (INTEGER PRIMARY KEY)

username (TEXT UNIQUE)

password (TEXT)

blends:

id (INTEGER PRIMARY KEY)

user_id (INTEGER)

flavor (TEXT)

ingredients (TEXT)

timestamp (TEXT)

feedback:

id (INTEGER PRIMARY KEY)

user_id (INTEGER)

blend_id (INTEGER)

rating (INTEGER)

comments (TEXT)

timestamp (TEXT)

Security Notes

Uses Werkzeug's password hashing

Requires strong passwords (8+ chars with complexity)

Session management with secret key

License

MIT License

live at:

https://flavorforge-0izq.onrender.com
