import tkinter as tk
from tkinter import filedialog

from app import run

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
run(file_path)
