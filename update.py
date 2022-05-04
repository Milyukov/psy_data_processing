import os
import shutil

if __name__ == '__main__':
    os.system("cd " + r"D:\python_script\psy_data_processing")
    os.system("git pull origin master")
    os.system("pyinstaller --onefile gui.py")
    shutil.move(r"D:\python_script\psy_data_processing\dist\gui.exe", r"C:\Users\at-ju\Desktop\gui.exe")
    os.system("cd -")
