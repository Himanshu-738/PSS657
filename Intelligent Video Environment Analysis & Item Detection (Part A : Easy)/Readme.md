

# 📁 Video Item Detection & Counting Web App

## ✅ Overview
This project provides a simple web application that allows users to upload a video file. The system analyzes the video, detects predefined items, and generates a downloadable CSV report with detected items and their counts.

---

## ⚡ Folder Structure

```
.
├── app.py
├── run_detection_counting.py
├── requirements.txt
├── templates/
│   └── index.html
├── results/
│   └── generated_report.csv (generated after processing)
```

---

## ⚡ How It Works

1. User uploads a video file via the web interface.
2. The backend calls the `analyze_video(video_path)` function from `run_detection_counting.py`.
3. A CSV report is generated with detected items and counts.
4. User can download the generated CSV file.

---

## ⚡ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2️⃣ Create Virtual Environment and Install Dependencies

```bash
mkdir video_count_demo
cd video_count_demo

# Create virtual environment
python3 -m venv venv

# Activate it:
# On macOS / Linux:
source venv/bin/activate
# On Windows (cmd):
# venv\Scripts\activate

# Upgrade pip and install required packages
pip install --upgrade pip
pip install ultralytics opencv-python numpy tqdm flask
```

> **Note:** Alternatively, you can use `pip install -r requirements.txt` if the file is up-to-date.

---

## ⚡ Run the Web App

```bash
python app.py
```

- Open your browser and visit:  
  👉 `http://127.0.0.1:5000`

- Upload a video file and click **Analyze**.
- After processing, download the generated CSV report.

---

## ⚡ Sample Output

The generated CSV file looks like this:

| Item      | Count |
|-----------|-------|
| fridge    | 1     |
| microwave | 2     |
| oven      | 1     |

---

## ⚡ Notes

- The current `analyze_video(video_path)` function contains dummy detection logic.  
  Replace it with your actual video processing implementation.

- The output CSV file is saved in `results/generated_report.csv`.

---

## ✅ Contact

For any questions, please contact:  
👤 **Your Name** – your.email@example.com
