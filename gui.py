from app import run
import tkinter as tk
from tkinter import filedialog

class View(tk.Frame):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent

        self.r_var = tk.IntVar()
        self.r_var.set(0)
        self.C1 = tk.Radiobutton(text = "Show cells with text intro", variable = self.r_var, value=0)
        self.C2 = tk.Radiobutton(text = "Show cells without text intro", variable = self.r_var, value=1)
        self.C1.pack()
        self.C2.pack()
        B = tk.Button(text ="Open file with data", command = self.open_file_dialog)
        B.pack()

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename()
        try:
            run(self.file_path, self.r_var.get())
        except BaseException as err:
            print(err)
            input("Press Enter to exit...")
        self.parent.destroy()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Psychological data processor')

        # create a view and place it on the root window
        view = View(self)

if __name__ == '__main__':
    app = App()
    app.mainloop()
