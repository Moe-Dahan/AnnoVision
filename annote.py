from tkinter.colorchooser import askcolor
import tkinter as tk
import os
import yaml
import shutil
from tkinter import messagebox
from PIL import Image

data = {}
annotationData = {}

class Annot:
    
    def __init__(self,workingCanvas, clickedImage, file_path, the_image) -> None:
        self.workingCanvas = workingCanvas
        self.clickedImage = clickedImage
        self.file_path = file_path
        self.the_image = the_image

        self.annotations = []
        self.rectangle = None
        self.start_x = None
        self.start_y = None

        # keybindings for shortcuts
        self.clickedImage.focus_set()
        self.clickedImage.bind("<ButtonPress-1>", self.on_button_press)
        self.clickedImage.bind("<B1-Motion>", self.on_button_move)
        self.clickedImage.bind("<ButtonRelease-1>", self.on_button_release) 
        self.clickedImage.bind("<Control-s>", self.savingImages) 
        self.clickedImage.bind("<Control-d>",self.delete_last_rectangle)

    def delete_last_rectangle(self, event=None):
        self.clickedImage.delete(self.rectangle)
        self.AnnoteWindow.destroy()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rectangle = self.clickedImage.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=1)

    def on_button_move(self, event):
        self.clickedImage.coords(self.rectangle, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):

        if self.clickedImage.winfo_exists():
            self.AnnoteWindow = tk.Toplevel(self.workingCanvas)
            self.AnnoteWindow.geometry("400x300")
            self.AnnoteWindow.title("ANNOVISION")
            self.AnnoteWindow.iconbitmap("icons/4023873-brain-learning-machine-machine-learning-ml_112855.ico")
            ''' taking data frame for class and color '''
            self.dataTakingFrame = tk.Frame(self.AnnoteWindow, borderwidth=1, relief="raised")

            self.dataName = tk.Label(self.dataTakingFrame, text="Data Name")
            self.dataName.grid(row=0, column=0, sticky="nw",  padx=5, pady=5)

            self.dataNameEntry = tk.StringVar()
            self.dataEntry = tk.Entry(self.dataTakingFrame, textvariable=self.dataNameEntry)
            self.dataEntry.grid(row=0, column=1, sticky="nw", padx=5, pady=5)

            self.addButton = tk.Button(self.dataTakingFrame, text="Class Color", command=lambda: self.chooseColor(event=event))
            self.addButton.grid(row=0, column=2, sticky="nw", padx=5, pady=5)

            self.dataTakingFrame.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
            ''' placing the saved classes frame '''
            self.objectDataFrame = tk.Frame(self.AnnoteWindow, borderwidth=1, relief="sunken")

            for objectDetectingData in data.keys():
                self.dataButton = tk.Button(self.objectDataFrame, text=objectDetectingData, command=lambda object=objectDetectingData: self.addData(object=object, event=event), width=10)
                self.dataButton.pack()
            self.objectDataFrame.grid(row=1, column=0, sticky="nw", padx=5, pady=5)

            self.AnnoteWindow.mainloop()
        else:
            self.workingImageWindow.destroy()

    def chooseColor(self, event):
        color = askcolor()
        chosenData = self.dataNameEntry.get()
        data.update({chosenData : color[1]})
        self.clickedImage.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=color[1], width=1)
        
        keys_list = list(data.keys())
        class_index = keys_list.index(chosenData)
        x_center, y_center, width, height = self.convert_to_yolo_format(self.start_x, self.start_y, event.x, event.y, int(1920 - 210), int(1080 - 100))
        annotation = f"{class_index} {x_center} {y_center} {width} {height}"
        
        self.annotations.append(annotation)

        annotationData.update({class_index: chosenData})
        self.AnnoteWindow.destroy()

    def addData(self, event, object):
        keys_list = list(data.keys())
        class_index = keys_list.index(object)
        if object in keys_list:
            for key, value in data.items():
                if value == object:
                    key_index = key
                    annotationData.update({key_index : object})
                    break

        objectColor = self.hex_to_rgb(data[object])  # Convert hex string to RGB tuple
        color = '#{:02x}{:02x}{:02x}'.format(*objectColor)
        self.clickedImage.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=color, width=1)
        x_center, y_center, width, height = self.convert_to_yolo_format(self.start_x, self.start_y, event.x, event.y, int(1920 - 210), int(1080 - 100))
        annotation = f"{class_index} {x_center} {y_center} {width} {height}"
        self.annotations.append(annotation)
        self.AnnoteWindow.destroy()

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def convert_to_yolo_format(self, x_min, y_min, x_max, y_max, image_width, image_height):
        x_center = (x_min + x_max) / (2 * image_width)
        y_center = (y_min + y_max) / (2 * image_height)
        width = abs(x_max - x_min) / image_width
        height = abs(y_max - y_min) / image_height
        width = min(width, 1.0)
        height = min(height, 1.0)
        return x_center, y_center, width, height
    
    def savingImages(self, event):
        if os.path.exists("count.txt"):
            with open("count.txt", "r") as file:
                count = int(file.read().strip())
        else:
            count = 0
        count += 1
        
        with open("count.txt", "w") as file:
            file.write(str(count))

        created_folder = os.makedirs(f"your_yolov8_dataset/images{count}", exist_ok=True)
        source_image_path = self.file_path
        destination_folder = f"your_yolov8_dataset/images{count}"
        new_image_filename = f"images{count}.jpg"
        
        # Copy the image to the destination folder
        shutil.copy(source_image_path, destination_folder)

        # Rename the copied image to the new filename
        os.rename(os.path.join(destination_folder, os.path.basename(source_image_path)), os.path.join(destination_folder, new_image_filename))

        # Write annotations to a text file
        with open(f"{destination_folder}/images{count}.txt", 'w') as fileOutput:
            for line in self.annotations:
                fileOutput.write(line + '\n')
        messagebox.showinfo(title="Saved Data", message='Saved Data Successfully!')
        self.annotations.clear()
        
def extract_yaml():
    root_folder = "your_yolov8_dataset"
    class_names = list(annotationData.keys())

    folders = [name for name in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, name))]
    total_folders = len(folders)
    half_folders = total_folders // 2
    for index, folder_name in enumerate(folders):
        source_folder = os.path.join(root_folder, folder_name)
        destination_folder = "train" if index < half_folders else "val"
        shutil.move(source_folder, os.path.join(root_folder, destination_folder, folder_name))

    yaml_data = {
        'path': root_folder,
        'train': f"{os.getcwd()}/your_yolov8_dataset/train",
        'val': f"{os.getcwd()}/your_yolov8_dataset/val",
        'names': annotationData
    }
        
    yaml_file = f"{root_folder}/dataset.yaml"
    with open(yaml_file, 'w') as f:
        yaml.dump(yaml_data, f)
    messagebox.showinfo(title="Extracted Successfully", 
    message='Model Extracted successfully to your_yolov8_dataset!')


if __name__ == '__main__':
    print("You Must Run main.py")

