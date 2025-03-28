import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import pytesseract
import pyttsx3
import speech_recognition as sr
import threading

# Set Tesseract OCR path (Update if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load YOLO model
yolo_cfg = "yolo-cfg/yolov3.cfg"
yolo_weights = "yolo-cfg/yolov3.weights"
coco_names = "yolo-cfg/coco.names"

# Load class labels
with open(coco_names, "r") as f:
    class_names = [line.strip() for line in f.readlines()]

# Load YOLO model
net = cv2.dnn.readNet(yolo_weights, yolo_cfg)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def voice_command():
    with sr.Microphone() as source:
        text_box.insert(tk.END, "")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            
            if "capture" in command:
                capture_from_camera()
            elif "select" in command:
                open_image()
            elif "read" in command:
                speak_text(text_box.get("1.0", tk.END).strip())
            elif "exit" in command:
                close_app()
            else:
                text_box.insert(tk.END, "Command not recognized!\n")
        except sr.UnknownValueError:
            text_box.insert(tk.END, "Could not understand the command.\n")
        except sr.RequestError:
            text_box.insert(tk.END, "Speech recognition service unavailable.\n")
    
    # Keep listening after processing each command
    voice_command()

def start_voice_command_thread():
    threading.Thread(target=voice_command, daemon=True).start()

# Function to capture image from webcam with zoom
def capture_from_camera():
    cap = cv2.VideoCapture(0)  # Open webcam
    zoom_factor = 1  # Initial zoom factor

    def process_frame(frame):
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_pil = img_pil.resize((300, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_pil)
        image_label.config(image=img_tk)
        image_label.image = img_tk
        detected_objects = detect_objects(frame)
        extracted_text = pytesseract.image_to_string(img_pil).strip()
        result_text = "Detected Objects: " + ", ".join(set(detected_objects)) if detected_objects else "No objects detected"
        if extracted_text:
            result_text += f"\nDetected Text: {extracted_text}"
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, result_text)
        speak_text(result_text)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2
        zoomed_width = int(width / zoom_factor)
        zoomed_height = int(height / zoom_factor)
        x1 = max(0, center_x - zoomed_width // 2)
        x2 = min(width, center_x + zoomed_width // 2)
        y1 = max(0, center_y - zoomed_height // 2)
        y2 = min(height, center_y + zoomed_height // 2)
        frame_zoomed = frame[y1:y2, x1:x2]
        frame_zoomed = cv2.resize(frame_zoomed, (width, height))
        cv2.imshow('Live Webcam Feed', frame_zoomed)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            process_frame(frame_zoomed)
            break
        elif key == ord('q'):
            break
        elif key == ord('+'):
            zoom_factor = min(zoom_factor + 0.1, 3.0)
        elif key == ord('-'):
            zoom_factor = max(zoom_factor - 0.1, 1.0)
    cap.release()
    cv2.destroyAllWindows()

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        img = cv2.imread(file_path)
        process_image(img)

def process_image(image):
    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    img_pil = img_pil.resize((300, 300), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_pil)
    image_label.config(image=img_tk)
    image_label.image = img_tk
    detected_objects = detect_objects(image)
    extracted_text = pytesseract.image_to_string(img_pil).strip()
    result_text = "Detected Objects: " + ", ".join(set(detected_objects)) if detected_objects else "No objects detected"
    if extracted_text:
        result_text += f"\nDetected Text: {extracted_text}"
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, result_text)
    speak_text(result_text)

def detect_objects(image):
    height, width, _ = image.shape
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward(output_layers)
    detected_objects = []
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                label = class_names[class_id]
                detected_objects.append(label)
    return detected_objects

def speak_text(text):
    if text:
        engine.say(text)
        engine.runAndWait()

def close_app():
    root.destroy()

# Create UI window
root = tk.Tk()
root.title("SeeLight - Object & Text Recognition")
root.geometry("500x650")

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", font=("Arial", 12), background="#f4f4f4")
style.configure("TText", font=("Arial", 12))

def set_background():
    bg_image = Image.open(r"D:\SeeLight\Images\img.png") # Change this image as needed
    bg_image = bg_image.resize((1200, 650), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    background_label = tk.Label(root, image=bg_photo)
    background_label.image = bg_photo
    background_label.place(relwidth=1, relheight=1)  # Stretch to fit the window

# Apply background
set_background()

# UI Elements
btn_capture = ttk.Button(root, text="Capture from Camera", command=capture_from_camera)
btn_capture.pack(pady=10, padx=20)

btn_select = ttk.Button(root, text="Select Image", command=open_image)
btn_select.pack(pady=10, padx=20)

image_label = ttk.Label(root, text="[ Image will appear here ]", relief="solid", padding=10)
image_label.pack(pady=10, padx=20)

text_box = tk.Text(root, height=5, width=50, font=("Arial", 12))
text_box.pack(pady=10, padx=20)
text_box.insert(tk.END, "Results will be displayed here...")

btn_speak = ttk.Button(root, text="Read Aloud", command=lambda: speak_text(text_box.get("1.0", tk.END).strip()))
btn_speak.pack(pady=10, padx=20)

btn_exit = ttk.Button(root, text="Exit", command=close_app)
btn_exit.pack(pady=10, padx=20)

# Start voice command thread
start_voice_command_thread()

root.mainloop()
