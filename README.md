# 🚗 Vehicle Detection, Tracking & Counting System

A computer vision project that detects, tracks, and counts vehicles in video footage using **YOLO, Supervision, and OpenCV**. The system tracks individual vehicles, identifies their movement across a virtual tripwire, and generates structured telemetry data for analysis.

## 📌 Project Overview

This project implements an automated vehicle monitoring pipeline using computer vision and object tracking.

It processes input video footage, detects vehicles, assigns tracking IDs, and counts vehicles crossing a predefined virtual line. It also generates an annotated output video and a CSV file containing vehicle tracking and counting information.

## ✨ Features

- **Vehicle Detection:** Detects vehicles in video frames using YOLO.
- **Object Tracking:** Tracks individual vehicles across multiple frames.
- **Unique Tracking IDs:** Assigns IDs to detected vehicles.
- **Virtual Tripwire:** Defines a virtual line to monitor vehicle movement.
- **Vehicle Counting:** Counts vehicles crossing the tripwire.
- **Direction Detection:** Records the direction in which vehicles cross the line.
- **Telemetry Logging:** Saves timestamped vehicle tracking and counting information in CSV format.
- **Annotated Video Output:** Generates a processed video with bounding boxes, tracking trails, and the virtual tripwire.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| YOLO (Ultralytics) | Vehicle detection |
| Supervision | Object tracking and detection visualization |
| OpenCV | Video processing |
| Pandas | Telemetry data management |
| CSV | Structured output logging |

## 🏗️ Project Workflow

```text
       Input Video
            |
            v
      Video Processing
         (OpenCV)
            |
            v
      Vehicle Detection
          (YOLO)
            |
            v
       Object Tracking
       (Supervision)
            |
            v
      Assign Tracking IDs
            |
            v
      Virtual Tripwire
            |
            v
   Vehicle Crossing Detection
            |
            v
      Vehicle Counting
            |
       +----+----+
       |         |
       v         v
  CSV Telemetry  Annotated Video
       |         |
       v         v
 telemetry_log  output_tracked.mp4
    .csv
```

## 📂 Project Structure

```text
Vehicle-Detection-Tracking/
│
├── main.py
├── input_video.mp4
├── telemetry_log.csv
├── output_tracked.mp4
├── requirements.txt
└── README.md
```

*Note: The exact project structure may vary depending on your implementation.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### 2. Navigate to the project directory

```bash
cd Vehicle-Detection-Tracking
```

### 3. Create a virtual environment (Recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install ultralytics supervision opencv-python pandas
```

Alternatively, if a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

### 5. Add an input video

Place your input video inside the project directory.

Make sure the input video path is correctly configured in your Python script.

### 6. Run the pipeline

Execute the main processing script:

```bash
python main.py
```

**Note:** Ensure that the input video path, YOLO model configuration, and virtual tripwire coordinates are correctly specified in your script.

## 📊 Output Files

After successful execution, the pipeline generates the following output files:

### 1. `telemetry_log.csv`

Contains structured vehicle tracking and counting information, such as:

- Timestamps
- Vehicle tracking IDs
- Vehicle counting information
- Crossing directions

### 2. `output_tracked.mp4`

The processed video containing:

- Vehicle bounding boxes
- Tracking IDs
- Tracking trails
- Virtual tripwire line
- Vehicle counting visualization (if enabled in the implementation)

## 🎯 Applications

- Intelligent traffic monitoring
- Vehicle flow analysis
- Smart city traffic management
- Road surveillance systems
- Traffic congestion analysis
- Automated vehicle counting

## 🚀 Future Improvements

- Real-time vehicle detection using live camera feeds.
- Vehicle classification (car, bus, truck, motorcycle).
- Multiple virtual tripwires for different lanes.
- Vehicle speed estimation.
- Traffic density analysis.
- Interactive traffic analytics dashboard.
- Improved performance for low-light and crowded traffic conditions.

## ⚠️ Limitations

- Detection and tracking accuracy depend on video quality and camera positioning.
- Occlusion and overlapping vehicles may affect tracking performance.
- Incorrect tripwire placement may lead to inaccurate vehicle counts.
- Processing speed depends on hardware capabilities and model configuration.

## 👩‍💻 Author

**Khushi Rajora**

GitHub: https://github.com/Khushirajora

---

⭐ If you find this project useful, consider giving the repository a star!
