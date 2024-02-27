import tkinter as tk
from tkinter import filedialog, PhotoImage, Canvas
import os
from annote import Annot, extract_yaml
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, mainWindow) -> None:
        self.mainWindow = mainWindow
        self.mainWindow.geometry(f"{1920}x{1080}")
        self.mainWindow.title("ANNOVISION")
        self.mainWindow.iconbitmap("icons/4023873-brain-learning-machine-machine-learning-ml_112855.ico")

        self.infoFrame = tk.Frame(self.mainWindow, relief="sunken", width=int(60), height=int(1080))
        ''' buttons frame '''
        self.buttons_frame = tk.Frame(self.infoFrame)

        self.openButtonImage = PhotoImage(file="icons/folder_open_21443.png")
        self.openButton = tk.Button(self.buttons_frame, image=self.openButtonImage, command=self.openFolderFunction, relief="flat")
        self.openButton.grid(row=0, column=0, padx=2, pady=0)

        self.annoteButtonImage = PhotoImage(file="icons/plan_architect_ruler_pencil_draw_icon_221353.png")
        self.annoteButton = tk.Button(self.buttons_frame, image=self.annoteButtonImage, command=self.start_annotation, relief="flat")
        self.annoteButton.grid(row=0, column=1, padx=2, pady=5)

        self.saveButtonImage = PhotoImage(file="icons/save_file_disk_open_searsh_loading_clipboard_1513.png")
        self.saveButton = tk.Button(self.buttons_frame, image=self.saveButtonImage, command=lambda: self.save_annotation, relief="flat")
        self.saveButton.grid(row=0, column=2, padx=2, pady=5)

        self.exportButtonImage = PhotoImage(file="icons/export_to_file_21450.png")
        self.exportButton = tk.Button(self.buttons_frame, image=self.exportButtonImage, command=lambda: extract_yaml(), relief="flat")
        self.exportButton.grid(row=0, column=3)

        self.buttons_frame.grid(row=0, column=0)
        ''' working files frame '''
        self.workFilesFrame = tk.Frame(self.infoFrame, height=int(1080), width=400)

        scroll_bar = tk.Scrollbar(self.workFilesFrame)
        scroll_bar.pack(side='right', fill='y')

        self.listbox = tk.Listbox(self.workFilesFrame, yscrollcommand=scroll_bar.set, height=int(100))
        self.listbox.pack(side='right', fill='both', expand=True)
        scroll_bar.config(command=self.listbox.yview, width=5)

        self.workFilesFrame.grid(row=1, column=0)

        self.infoFrame.grid(row=0, column=0, sticky="nw", pady=10) 
        ''' canvas frame '''
        self.canvasFrame = tk.Frame(self.mainWindow, borderwidth=1, relief="solid", width=int(1920 - 210), height=int(1080 - 100))

        self.canvasFrame.grid(row=0, column=1, padx=1, sticky="nw", pady=0)

    def openFolderFunction(self):
        self.workingFolder = filedialog.askdirectory(initialdir=os.listdir())
        for file in os.listdir(self.workingFolder):
            label = tk.Label(self.listbox, text=file)
            label.pack()
            label.bind('<Button-1>', lambda event, file=file: self.on_label_click(file))
    
    def resize_image(self, file):
        image = Image.open(file)
        resized_image = image.resize((int(1920 - 210), int(1080 - 100)))
        final_path = f"{file}"
        resized_image.save(final_path, "PNG")
        return final_path

    def on_label_click(self, file):
        final_path = self.resize_image(f"{self.workingFolder}/{file}")
        image = Image.open(final_path)
        self.theImage = ImageTk.PhotoImage(image=image)  # Corrected to pass the image object
        self.clickedImage = tk.Canvas(self.canvasFrame, width=int(1920-210), height=int(1080-100))
        self.clickedImage.create_image(0, 0, anchor='nw', image=self.theImage)
        self.clickedImage.grid(row=0, column=1)
        self.file_path = final_path
    
    def start_annotation(self):
        Annot(self.canvasFrame, self.clickedImage, self.file_path, self.theImage)

    def save_annotation(self):
        Annot.savingImages()

    def export_yaml(self):
        extract_yaml()

if __name__ == '__main__':
    if os.path.isdir("your_yolov8_dataset"):
        from tkinter import messagebox
        messagebox.showinfo(title="remove 'your_yolov8_dataset' from the Directory!", 
        message='Found A Previous model please remove your_yolov8_dataset from the Directory! Run main.py Again!')
    else:
        firstWindow = tk.Tk()
        MainWindow(firstWindow)
        firstWindow.mainloop()