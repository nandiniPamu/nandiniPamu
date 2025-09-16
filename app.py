from flask import Flask, render_template, request, redirect, url_for
from ai_engine import analyze_message

app = Flask(__name__)

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
    # Placeholder for report handling
    print(f"Report details: {details}")
    if screenshot:
        print(f"Screenshot filename: {screenshot.filename}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
