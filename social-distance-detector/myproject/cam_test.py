import cv2

def test_camera():
    print("[INFO] Attempting to open webcam...")
    # Try to open the default webcam (index 0)
    vs = cv2.VideoCapture(0)
    
    if not vs.isOpened():
        print("[ERROR] Failed to open webcam. Please check if another application is using it or if the camera is properly connected.")
        return

    print("[INFO] Webcam opened successfully. Press 'q' to quit.")
    while True:
        # Read a frame from the video stream
        ret, frame = vs.read()

        if not ret:
            print("[ERROR] Failed to read a frame from the webcam.")
            break

        # Display the frame
        cv2.imshow("Webcam Test", frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vs.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()
