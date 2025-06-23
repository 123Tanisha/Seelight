# SeeLight - Object & Text Recognition GUI Application

**SeeLight** is an intelligent desktop GUI application designed to assist users (especially the visually impaired) by detecting and reading out objects and text from images or live webcam feed using YOLOv3 and Tesseract OCR, integrated with voice command control and text-to-speech.

## 🔍 Features

- 🧠 **Object Detection** using YOLOv3
- 📖 **Text Recognition** using Tesseract OCR
- 🎤 **Voice Command Support** for hands-free control
- 🗣️ **Text-to-Speech** output of results
- 📸 **Webcam Capture** with dynamic zoom functionality
- 🖼️ **Image Upload** and processing
- 🪟 Simple and user-friendly **Tkinter GUI**

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV** – For image/video processing
- **YOLOv3** – For object detection
- **Tesseract OCR** – For text recognition
- **Pyttsx3** – For text-to-speech
- **SpeechRecognition** – For processing voice commands
- **Tkinter** – For GUI
- **Pillow** – For image handling in GUI

---

## 📁 Directory Structure

- **SeeLight**
- ├── seelight_gui5.py # Main application code
- ├── yolo-cfg/
- ├── yolov3.cfg
- ├── yolov3.weights
- └── coco.names
- └── README.md # Project documentation

---

## 🚀 How It Works

1. **Run the App**: Launch `seelight_gui5.py`.
2. **Choose an Action**:
   - Press **"Capture from Camera"** to detect objects and text via webcam (Press `s` to scan, `+/-` to zoom).
   - Press **"Select Image"** to upload and analyze any image.
3. **Voice Control**: Say commands like:
   - `"capture"` – to use webcam
   - `"select"` – to open image file
   - `"read"` – to read out the detected content
   - `"exit"` – to close the application
4. **Results**: Detected objects and text are shown in the result box and can be spoken aloud using TTS.

---

## 🧠 Example Use Cases

- Assistive tool for visually impaired users
- Educational demo for Computer Vision beginners
- Light-weight object-text recognition system
- Voice-controlled desktop utilities

---

## 🔧 Requirements

- Python 3.x
- Install dependencies:
  ```bash
  pip install opencv-python pillow pytesseract pyttsx3 SpeechRecognition
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
