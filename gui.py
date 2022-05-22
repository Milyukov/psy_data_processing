import tkinter as tk
from tkinter import filedialog

from app import run

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
try:
    run(file_path)
except BaseException as err:
    print(err)
input("Press Enter to exit...")
