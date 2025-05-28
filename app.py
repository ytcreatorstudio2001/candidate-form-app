from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DB_NAME = "database.db"

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            aadhaar TEXT NOT NULL,
            recruiter TEXT NOT NULL,
            submitted_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    aadhaar = request.form['aadhaar']
    recruiter = request.form['recruiter']
    submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO candidates (name, phone, aadhaar, recruiter, submitted_at) VALUES (?, ?, ?, ?, ?)",
              (name, phone, aadhaar, recruiter, submitted_at))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
