from tkinter.colorchooser import askcolor
import tkinter as tk
import os
import yaml
import shutil
from tkinter import messagebox
from PIL import Image

data = {}
annotation_data = {}

class Annot:
    def __init__(self, window, canvas_frame, clicked_image, final_file_path, the_image) -> None:
        self.window = window
        self.canvas_frame = canvas_frame
        self.clicked_image = clicked_image
        self.final_file_path = final_file_path
        self.the_image = the_image

        self.annotations = []
        self.rectangle = None
        self.button_pressed = False
        self.start_x = None
        self.start_y = None
        self.h_line = None
        self.v_line = None

        # keybindings for shortcuts
        self.clicked_image.focus_set()
        self.clicked_image.bind("<ButtonPress-1>", self.on_button_press)
        self.clicked_image.bind("<B1-Motion>", self.on_button_move)
        self.clicked_image.bind("<ButtonRelease-1>", self.on_button_release) 
        self.clicked_image.bind("<Control-s>", self.saving_images) 
        self.clicked_image.bind("<Control-d>", self.delete_last_rectangle)

    def delete_last_rectangle(self, event=None):
        self.clicked_image.delete(self.rectangle)
        self.annote_window.destroy()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.button_pressed = True
        if self.button_pressed:
            self.h_line = self.clicked_image.create_line(0, event.y, self.clicked_image.winfo_width(), event.y)
            self.clicked_image.itemconfig(self.h_line, fill="orange")
            self.v_line = self.clicked_image.create_line(event.x, 0, event.x, self.clicked_image.winfo_height())
            self.clicked_image.itemconfig(self.v_line, fill="orange")
            self.rectangle = self.clicked_image.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=1)
        

    def on_button_move(self, event):
        if self.button_pressed:
            self.clicked_image.coords(self.h_line, 0, event.y, self.clicked_image.winfo_width(), event.y)
            self.clicked_image.itemconfig(self.h_line, fill="Yellow")
            self.clicked_image.coords(self.v_line, event.x, 0, event.x, self.clicked_image.winfo_height())
            self.clicked_image.itemconfig(self.v_line, fill="Yellow")
            self.clicked_image.coords(self.rectangle, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        self.button_pressed = False
        self.clicked_image.delete(self.h_line)
        self.clicked_image.delete(self.v_line)

        if self.clicked_image.winfo_exists():
            self.annote_window = tk.Toplevel(self.window)
            self.annote_window.geometry("400x300")
            self.annote_window.title("ANNOVISION")
            self.annote_window.iconbitmap("icons/4023873-brain-learning-machine-machine-learning-ml_112855.ico")
            ''' taking data frame for class and color '''
            self.data_taking_frame = tk.Frame(self.annote_window, borderwidth=1, relief="raised")

            self.data_name = tk.Label(self.data_taking_frame, text="Data Name")
            self.data_name.grid(row=0, column=0, sticky="nw",  padx=5, pady=5)

            self.data_name_entry = tk.StringVar()
            self.data_entry = tk.Entry(self.data_taking_frame, textvariable=self.data_name_entry)
            self.data_entry.grid(row=0, column=1, sticky="nw", padx=5, pady=5)

            self.add_button = tk.Button(self.data_taking_frame, text="Class Color", command=lambda: self.choose_color(event=event))
            self.add_button.grid(row=0, column=2, sticky="nw", padx=5, pady=5)

            self.data_taking_frame.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
            ''' placing the saved classes frame '''
            self.object_data_frame = tk.Frame(self.annote_window, borderwidth=1, relief="sunken")

            for object_detecting_data in data.keys():
                self.data_button = tk.Button(self.object_data_frame, text=object_detecting_data, command=lambda object=object_detecting_data: self.add_data(object=object, event=event), width=10)
                self.data_button.pack()
            self.object_data_frame.grid(row=1, column=0, sticky="nw", padx=5, pady=5)

            self.annote_window.mainloop()
        
    def choose_color(self, event):
        color = askcolor()
        chosen_data = self.data_name_entry.get()
        data.update({chosen_data : color[1]})
        self.clicked_image.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=color[1], width=1)
        
        keys_list = list(data.keys())
        class_index = keys_list.index(chosen_data)
        x_center, y_center, width, height = self.convert_to_yolo_format(self.start_x, self.start_y, event.x, event.y, int(1920 - 210), int(1080 - 100))
        annotation = f"{class_index} {x_center} {y_center} {width} {height}"
        
        self.annotations.append(annotation)

        annotation_data.update({class_index: chosen_data})
        self.annote_window.destroy()
    
    def add_data(self, event, object):
        keys_list = list(data.keys())
        class_index = keys_list.index(object)
        if object in keys_list:
            for key, value in data.items():
                if value == object:
                    key_index = key
                    annotation_data.update({key_index : object})
                    break

        object_color = self.hex_to_rgb(data[object])
        color = '#{:02x}{:02x}{:02x}'.format(*object_color)
        self.clicked_image.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=color, width=1)
        x_center, y_center, width, height = self.convert_to_yolo_format(self.start_x, self.start_y, event.x, event.y, int(1920 - 210), int(1080 - 100))
        annotation = f"{class_index} {x_center} {y_center} {width} {height}"
        self.annotations.append(annotation)
        self.annote_window.destroy()

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
    
    def saving_images(self, event):
        if os.path.exists("count.txt"):
            with open("count.txt", "r") as file:
                count = int(file.read().strip())
        else:
            count = 0
        count += 1
        
        with open("count.txt", "w") as file:
            file.write(str(count))

        created_folder = os.makedirs(f"your_yolov8_dataset/images{count}", exist_ok=True)
        source_image_path = self.final_file_path
        destination_folder = f"your_yolov8_dataset/images{count}"
        new_image_filename = f"images{count}.jpg"
        
        shutil.copy(source_image_path, destination_folder)

        os.rename(os.path.join(destination_folder, os.path.basename(source_image_path)), os.path.join(destination_folder, new_image_filename))

        with open(f"{destination_folder}/images{count}.txt", 'w') as file_output:
            for line in self.annotations:
                file_output.write(line + '\n')
        messagebox.showinfo(title="Saved Data", message='Saved Data Successfully!')
        self.annotations.clear()

def extract_yaml():
        root_folder = "your_yolov8_dataset"
        class_names = list(annotation_data.keys())

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
            'names': annotation_data
        }
            
        yaml_file = f"{root_folder}/dataset.yaml"
        with open(yaml_file, 'w') as f:
            yaml.dump(yaml_data, f)
        messagebox.showinfo(title="Extracted Successfully", 
        message='Model Extracted successfully to your_yolov8_dataset!')
