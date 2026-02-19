from flask import Flask, render_template, request, redirect, url_for
from ai_engine import analyze_message
from config import Config
from models import db, Report, Conversation
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/talk')
def talk():
    return render_template('talk.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    message = request.form.get('message', '')
    classification, response = analyze_message(message)

    # Save to database
    new_convo = Conversation(message=message, classification=classification, response=response)
    db.session.add(new_convo)
    db.session.commit()

    return render_template('analysis_result.html', classification=classification, response=response)

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/submit_report', methods=['POST'])
def submit_report():
    details = request.form.get('details', '')
    screenshot = request.files.get('screenshot')

    filename = None
    if screenshot and screenshot.filename != '':
        filename = secure_filename(screenshot.filename)
        # In a real app, we would save the file to an 'uploads' folder

    new_report = Report(details=details, screenshot_filename=filename)
    db.session.add(new_report)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
