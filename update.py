import os

if __name__ == '__main__':
    os.system(r"D:\python_script\psy_data_processing")
    os.system("git pull")
    os.system("pyinstaller --onefile gui.py")
    os.system(r"cp D:\python_script\psy_data_processing\dist\gui.exe C:\Users\at-ju\Desktop\gui.exe")
    os.system("cd -")
