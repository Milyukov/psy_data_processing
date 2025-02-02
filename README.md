# psy_data_processing
Scripts for psychological data processing

# Environment configuration
Install Python 3.11.9 and execute the following:
```sh
python3 -m venv psy_data_processing
source psy_data_processing/bin/activate
psy_data_processing/bin/python3 -m pip install -r requirements.txt
```

To prepare environment for server deploy:
```sh
psy_data_processing/bin/python3 -m pip install "fastapi[standard]"
```

# Deploy

## Executable

To create executable file:
```sh
 psy_data_processing/bin/python3 -m pip install pyinstaller==6.10.0
 cd simplified/
 pyinstaller --onefile application.py
```

Executable can be found in 
```sh
./dist/application(.exe)
```

## Server
```sh
uvicorn serve:app --reload
```
