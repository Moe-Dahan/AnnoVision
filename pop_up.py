import tkinter as tk
import subprocess
import os

class PopUpAlerts:
    def __init__(self, workingCanvas) -> None:
        self.workingCanvas = workingCanvas
        self.previous_window = tk.Toplevel(self.workingCanvas)
        self.previous_window.title("ANNOVISION")
        #self.previous_window.iconbitmap("icons/4023873-brain-learning-machine-machine-learning-ml_112855.ico")

    def removing(self):
        subprocess.run(['explorer', os.path.realpath(os.getcwd())])
        self.previous_window.destroy()

def already_exists_error(self):
    found_frame = tk.Frame(self.previous_window)
    found_label = tk.Label(found_frame, text="Found A Previous model please remove \n 'your_yolov8_dataset' from the Directory!".upper(), font=("Open-sans", 12, "bold"), fg="Red")
    found_label.grid(row=0, column=0, sticky="nw")
    continue_button = tk.Button(found_frame, text="Got it Thanks!", font=("Open-sans", 10, "bold"), fg="white", bg="Green", width=25, command=PopUpAlerts.removing)
    continue_button.grid(row=1, column=0, sticky="nw", padx=100)

    found_frame.grid(row=0, column=0, sticky="nw", padx=50, pady=50)

def saved_image():
    button = tk.Button(previous_window, text="click Me")
    button.grid(row=0, column=0)

previous_window = tk.Tk()
previous_window.title("ANNOVISION")
#previous_window.iconbitmap("icons/4023873-brain-learning-machine-machine-learning-ml_112855.ico")

# Call your functions here as needed
# Example: already_exists_error()

previous_window.mainloop()
