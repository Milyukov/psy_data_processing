import os
import yaml
import pandas as pd
from io import BytesIO

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

from model import Model
from controller import Controller

app = FastAPI()

# create a model
model = Model()

# create a controller
controller = Controller(model)

@app.post("/file/upload-file")
def upload_file(file: UploadFile):
  sheets = pd.read_excel(BytesIO(file.file.read()), sheet_name=None)
  for sheet_name, sheet_content in sheets.items():
     sheet_content.to_excel('input.xlsx', sheet_name=sheet_name)
  return file

@app.post("/file/upload-config")
def upload_file(file: UploadFile):
  config = yaml.safe_load(BytesIO(file.file.read()))
  yaml.dump(config, open('input.yaml', 'w'), allow_unicode=True)
  return file

@app.get("/file/download")
def download_file():
    controller.run('input.xlsx', 'input.yaml')
    if os.path.exists('result.xlsx'):
        return FileResponse(path='result.xlsx', filename='result.xlsx', media_type='multipart/form-data')
