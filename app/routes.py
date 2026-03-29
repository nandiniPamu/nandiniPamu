from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import TalkMessage, Report
from .ai_engine import analyze_message

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/talk')
def talk():
    return render_template('talk.html')

@main.route('/analyze', methods=['POST'])
def analyze():
    message = request.form.get('message')
    if not message:
        return redirect(url_for('main.talk'))

    classification, response = analyze_message(message)

    # Save to database
    new_message = TalkMessage(message=message, classification=classification, response=response)
    db.session.add(new_message)
    db.session.commit()

    return render_template('analysis_result.html', classification=classification, response=response)

@main.route('/report')
def report():
    return render_template('report.html')

@main.route('/submit_report', methods=['POST'])
def submit_report():
    details = request.form.get('details')
    screenshot = request.files.get('screenshot')

    if not details:
        return redirect(url_for('main.report'))

    filename = None
    if screenshot and screenshot.filename:
        filename = screenshot.filename
        # In a real app, we would save the file to a secure location

    # Save to database
    new_report = Report(details=details, screenshot_filename=filename)
    db.session.add(new_report)
    db.session.commit()

    return redirect(url_for('main.report_success'))

@main.route('/report_success')
def report_success():
    return render_template('report_success.html')
