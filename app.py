import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from ai_engine import analyze_message
from database import init_db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/talk')
def talk():
    return render_template('talk.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    message = request.form['message']
    classification, response = analyze_message(message)
    return render_template('analysis_result.html', classification=classification, response=response)

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/submit_report', methods=['POST'])
def submit_report():
    details = request.form['details']
    screenshot = request.files['screenshot']
    screenshot_filename = None
    if screenshot:
        screenshot_filename = secure_filename(screenshot.filename)
        screenshot.save(os.path.join(app.config['UPLOAD_FOLDER'], screenshot_filename))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO reports (details, screenshot) VALUES (?, ?)",
              (details, screenshot_filename))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reports")
    reports = c.fetchall()
    conn.close()
    return render_template('admin.html', reports=reports)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
