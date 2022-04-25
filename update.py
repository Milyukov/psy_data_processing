import os

if __name__ == '__main__':
    os.system("cd " + r"D:\python_script\psy_data_processing")
    os.system("git pull")
    os.system("pyinstaller --onefile gui.py")
    os.system("cp " + r"D:\python_script\psy_data_processing\dist\gui.exe C:\Users\at-ju\Desktop\gui.exe")
    os.system("cd -")
