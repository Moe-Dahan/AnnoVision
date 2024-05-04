import tkinter as tk
from tkinter import filedialog, PhotoImage, Canvas, Menu
import os
from PIL import Image, ImageTk
from annote import Annot, extract_yaml


class MainWindow:
    def __init__(self, window):
        self.window = window
        self.window.geometry(f"{1920}x{1080}")
        self.window.title("ANNOVISION")
        self.window.iconbitmap("icons/4023873-brain-learning-machine-machine-learning-ml_112855.ico")

        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        file_menu = Menu(menubar, tearoff= False)
        menubar.add_cascade(label="File", menu=file_menu, underline=0)
        file_menu.add_command(label='Open Project', command=self.openFolderFunction) # need to create the code to reopen a saved project
        file_menu.add_command(label='Annot Images', command=self.openFolderFunction)
        file_menu.add_command(label='Annot Video', command=self.window.destroy) # need to create a annotation for video slicing
        file_menu.add_separator()
        file_menu.add_command(label='Close', command=self.window.destroy)
        
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')
        menubar.add_cascade(label="Help", menu=help_menu)

        exit_menu = Menu(menubar, tearoff=0)
        exit_menu.add_command(label='Exit', command=self.window.destroy)
        menubar.add_cascade(label="Exit", menu=exit_menu)
        
        self.work_files_frame = tk.Frame(self.window, height=int(1080- 98), width=140, border=1, relief="solid")
        scroll_bar = tk.Scrollbar(self.work_files_frame)
        scroll_bar.pack(side='right', fill='y')
        self.listbox = tk.Listbox(self.work_files_frame, yscrollcommand=scroll_bar.set, height=int(61))
        self.listbox.pack(side='right', fill='both', expand=True)
        self.listbox.pack_propagate(False)
        scroll_bar.config(command=self.listbox.yview)
        self.work_files_frame.grid(row=0, column=0, padx=5)
        self.work_files_frame.grid_propagate(False)

        self.working_space_frame = tk.Frame(self.window, border=1, relief="solid", bg="LightGray")

        self.buttons_annote_frame = tk.Frame(self.working_space_frame, height=40, width=130, bg="LightGray")

        self.annote_button_image = PhotoImage(file="icons/note.png")
        self.annote_button = tk.Button(self.buttons_annote_frame, image=self.annote_button_image, relief="flat", command=self.start_annotation, bg="LightGray")
        self.annote_button.grid(row=0, column=1, padx=5)

        self.save_button_image = PhotoImage(file="icons/folder.png")
        self.save_button = tk.Button(self.buttons_annote_frame, image=self.save_button_image, relief="flat", command=lambda: self.save_annotation, bg="LightGray")
        self.save_button.grid(row=0, column=2, padx=5)

        self.export_button_image = PhotoImage(file="icons/share.png")
        self.export_button = tk.Button(self.buttons_annote_frame, image=self.export_button_image, relief="flat", command=lambda: extract_yaml(), bg="LightGray")
        self.export_button.grid(row=0, column=3, padx=5)

        self.buttons_annote_frame.grid(row=0, column=0)

        self.canvas_frame = tk.Frame(self.working_space_frame, width=1750, height=905, bg="LightGray")

        self.canvas_frame.grid(row=1, column=0, padx=1, sticky="nw", pady=1)

        self.working_space_frame.grid(row=0, column=1, sticky="nw", padx=5)

    def openFolderFunction(self):
        self.working_folder = filedialog.askdirectory(initialdir=os.listdir())
        for file in os.listdir(self.working_folder):
            if file.endswith(".png") or file.endswith(".jpg"):
                self.listbox.insert(tk.END, file)
                self.listbox.bind("<<ListboxSelect>>", self.on_label_click)

    def resize_image(self, file):
        image = Image.open(file)
        resized_image = image.resize((1750, 905))
        final_path = f"{file}"
        resized_image.save(final_path, "PNG")
        return final_path
    
    def on_label_click(self, event):
        file = self.listbox.curselection()
        selected_file = self.listbox.get(file)
        self.final_file_path = os.path.join(self.working_folder, selected_file)
        final_path = self.resize_image(self.final_file_path)
        image = Image.open(final_path)
        self.the_image = ImageTk.PhotoImage(image=image)
        self.clicked_image = tk.Canvas(self.canvas_frame, width=1750, height=905)
        self.clicked_image.create_image(0, 0, anchor='nw', image=self.the_image)
        self.clicked_image.grid(row=0, column=1)
        
    def start_annotation(self):
        Annot(self.window, self.canvas_frame, self.clicked_image, self.final_file_path, self.the_image)

    def save_annotation(self):
        Annot.saving_images()

    def export_yaml(self):
        extract_yaml()

if __name__ == '__main__':
    if os.path.isdir("your_yolov8_dataset"):
        from tkinter import messagebox
        result = messagebox.askquestion(title="remove 'your_yolov8_dataset' from the Directory!", 
                message='Found A Previous model would you like to delete it?')
        if result=='yes':
            import shutil
            shutil.rmtree("your_yolov8_dataset")
            if os.path.isfile("count.txt"):
                os.remove("count.txt")
            print("Deleted")
        else:
            messagebox.showinfo(title="Move or reopen Project", message="Remove the Project or Open it from the File menu to continue Project dataset will be broken")
            app = tk.Tk()
            MainWindow(app)
            app.mainloop()
    else:
        app = tk.Tk()
        MainWindow(app)
        app.mainloop()
