import tkinter as tk
import threading
import subprocess
import os
import sys
from tkinter import messagebox

# Get the path to the main detector script
DETECTOR_SCRIPT = "detector.py"

# Get the full path to the python executable
PYTHON_EXECUTABLE = sys.executable

class SocialDistanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Distance Detector")
        self.root.geometry("400x150")
        self.root.configure(bg="#2c3e50")

        self.detector_process = None
        self.is_running = False

        # Create a frame for the buttons
        button_frame = tk.Frame(root, bg="#2c3e50")
        button_frame.pack(pady=20)

        # Start Button
        self.start_button = tk.Button(
            button_frame,
            text="Start Detector",
            command=self.start_detector_thread,
            font=("Arial", 14),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            relief="raised",
            bd=3,
            padx=10,
            pady=5
        )
        self.start_button.pack(side=tk.LEFT, padx=10)

        # Stop Button
        self.stop_button = tk.Button(
            button_frame,
            text="Stop Detector",
            command=self.stop_detector,
            font=("Arial", 14),
            bg="#c0392b",
            fg="white",
            activebackground="#e74c3c",
            relief="raised",
            bd=3,
            padx=10,
            pady=5,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)

        # Label to show status
        self.status_label = tk.Label(
            root,
            text="Status: Idle",
            font=("Arial", 12),
            bg="#2c3e50",
            fg="white"
        )
        self.status_label.pack(pady=10)

    def start_detector_thread(self):
        """
        Starts the detector script in a separate thread to prevent the GUI from freezing.
        """
        if not self.is_running:
            self.status_label.config(text="Status: Starting...")
            self.start_button.config(state=tk.DISABLED)
            
            # Use a thread to run the subprocess call so the GUI remains responsive
            thread = threading.Thread(target=self.run_detector)
            thread.daemon = True
            thread.start()

    def run_detector(self):
        """
        Launches the detector.py script as a subprocess.
        """
        try:
            self.is_running = True
            self.status_label.config(text="Status: Running")
            self.stop_button.config(state=tk.NORMAL)
            
            # Run the detector script using the same Python executable
            self.detector_process = subprocess.Popen([PYTHON_EXECUTABLE, DETECTOR_SCRIPT])
            self.detector_process.wait()  # Wait for the process to finish

        except FileNotFoundError:
            messagebox.showerror("Error", f"Could not find {DETECTOR_SCRIPT}. Please check your file path.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.is_running = False
            self.status_label.config(text="Status: Stopped")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def stop_detector(self):
        """
        Stops the detector subprocess.
        """
        if self.is_running and self.detector_process:
            self.status_label.config(text="Status: Stopping...")
            self.stop_button.config(state=tk.DISABLED)
            
            # Terminate the subprocess
            self.detector_process.terminate()
            self.detector_process.wait() # Wait for the process to terminate gracefully
            
            self.is_running = False
            self.status_label.config(text="Status: Idle")
            self.start_button.config(state=tk.NORMAL)
            messagebox.showinfo("Detector", "Detector has been stopped.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialDistanceGUI(root)
    root.mainloop()

