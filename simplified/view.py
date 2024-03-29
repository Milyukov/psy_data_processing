import tkinter as tk
from tkinter import filedialog

class View(tk.Frame):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        B = tk.Button(text ="Open files with data", command = self.open_file_dialog)
        B.pack()

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        self.config_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.yaml")])
        try:
            self.controller.run(self.file_path, self.config_path)
        except BaseException as err:
            print(err)
            input("Press Enter to exit...")
        self.parent.destroy()
