import cv2
import numpy as np
import imutils
import torch
from scipy.spatial.distance import euclidean

# -----------------------------------------------------------------------------
# File Paths and Configuration
# -----------------------------------------------------------------------------

# Path to the YOLOv5 repository folder (relative to detector_app)
MODEL_PATH = 'yolov5' # <-- CORRECTED PATH
# Path to the model weights file within the repository
WEIGHTS_PATH = 'yolov5s.pt' 

# Set the minimum social distance threshold in pixels.
MIN_DISTANCE = 100

# Global variables to hold the loaded model and video stream
MODEL = None
VS = None

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def load_model_once():
    """
    Loads the YOLOv5 model and stores it in a global variable.
    This function is called only once when the server starts.
    """
    global MODEL
    if MODEL is None:
        print("[INFO] Loading YOLOv5 model for the first time...")
        try:
            MODEL = torch.hub.load(MODEL_PATH, 'custom', path=WEIGHTS_PATH, source='local')
            MODEL.classes = [0]  # Filter for only the 'person' class
        except Exception as e:
            print(f"[ERROR] Failed to load YOLOv5 model: {e}")
            return None
    return MODEL

def detect_social_distancing(model):
    """
    This function handles the main video processing loop and yields
    JPEG-encoded frames for web streaming.
    """
    global VS
    if VS is None:
        print("[INFO] Starting video stream...")
        VS = cv2.VideoCapture(0)
    
    if model is None:
        # Yield an empty byte string if the model fails to load
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + b'' + b'\r\n\r\n')
        return

    while True:
        ret, frame = VS.read()
        if not ret:
            print("[ERROR] Failed to read frame from webcam.")
            break

        frame = imutils.resize(frame, width=800)
        (H, W) = frame.shape[:2]

        results = model(frame)
        person_boxes = []
        for *box, conf, cls in results.xyxy[0]:
            x1, y1, x2, y2 = [int(i) for i in box]
            person_boxes.append((x1, y1, x2 - x1, y2 - y1))

        violations = set()
        if len(person_boxes) > 1:
            for i in range(len(person_boxes)):
                for j in range(i + 1, len(person_boxes)):
                    box_a = person_boxes[i]
                    box_b = person_boxes[j]

                    center_a = (box_a[0] + box_a[2] // 2, box_a[1] + box_a[3])
                    center_b = (box_b[0] + box_b[2] // 2, box_b[1] + box_b[3])
                    
                    distance = euclidean(center_a, center_b)

                    if distance < MIN_DISTANCE:
                        violations.add(i)
                        violations.add(j)
                        cv2.line(frame, center_a, center_b, (0, 0, 255), 2)
        
        for i, box in enumerate(person_boxes):
            (x, y, w, h) = box
            color = (0, 0, 255) if i in violations else (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
        text = "Social Distancing Violations: {}".format(len(violations))
        cv2.putText(frame, text, (10, H - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
