from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from run_detection_counting import analyze_video
import os
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    csv_url = None

    if request.method == 'POST':
        video = request.files['video']
        declared_env = request.form['declared_env']
        declared_items = request.form['declared_items']

        video_path = os.path.join(UPLOAD_FOLDER, secure_filename(video.filename))
        video.save(video_path)

        # Call analyze_video and store the result
        analysis_result = analyze_video(video_path, declared_env=declared_env, declared_items=declared_items)
        print("ANALYSIS RESULT:", analysis_result)  # Debugging line

        # Ensure valid return format
        if isinstance(analysis_result, dict) and 'csv_file' in analysis_result:
            result = analysis_result
            csv_file_path = analysis_result['csv_file']

            # Copy CSV to results folder for download
            final_csv_path = os.path.join(RESULT_FOLDER, 'analysis_report.csv')
            shutil.copy(csv_file_path, final_csv_path)

            csv_url = '/results/analysis_report.csv'
        else:
            result = {"error": "analyze_video() did not return expected dictionary."}

    return render_template('index.html', result=result, csv_url=csv_url)

@app.route('/results/<filename>')
def download_file(filename):
    return send_file(os.path.join(RESULT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
