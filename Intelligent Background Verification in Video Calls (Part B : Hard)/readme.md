
# 🎥 Video Analysis Web App (Hard Version)

This project provides a simple web interface to analyze videos and generate detailed CSV reports based on declared environments and items.

---

## ✅ Features

- Upload video file for analysis
- Specify declared environment , that the person tells he is in (e.g., `home`)
- Specify declared items in format: (not necessary) `item:count` (e.g., `fridge:1,microwave:1`)
- View analysis results on the webpage
- Download generated CSV report

---

## ⚡ Installation & Setup

### 1️⃣ Create Project Directory

```bash
mkdir video_count_demo
cd video_count_demo
```

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
```

### 3️⃣ Activate Virtual Environment

- **macOS / Linux:**

    ```bash
    source venv/bin/activate
    ```

- **Windows (cmd):**

    ```bash
    venv\Scripts\activate
    ```

### 4️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install ultralytics opencv-python numpy tqdm flask
```

---

## 🚀 Running the Web App

```bash
python app.py
```

Then open your browser and go to:  
👉 `http://127.0.0.1:5000`

---

## 🎯 How to Use

1. Upload a video file using the form.
2. Enter the declared environment (e.g., `home`).
3. Enter declared items in the format:  
   `fridge:1,microwave:1`  
   (comma-separated `item:count` pairs).
4. Click **Analyze Video**.
5. View results directly on the webpage.
6. Download the generated CSV report.

---

## 📂 Folder Structure

```text
video_count_demo/
│
├── app.py
├── run_detection_counting.py
├── requirements.txt
├── templates/
│   └── index.html
├── uploads/          # Stores uploaded video files
├── results/          # Stores generated CSV reports
```

---

## ✅ Notes

- Ensure the folders `uploads/` and `results/` exist (they are automatically created when the app runs).
- The project assumes the model file `run_detection_counting.py` is correctly implemented and returns a result dictionary containing a `'csv_file'` key.

---

## ❤️ Made with Python & Flask -- By Himanshu


