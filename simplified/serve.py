import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from io import BytesIO
import shutil
import yaml
import pandas as pd
from model import Model
from controller import Controller

# create a model
model = Model()

# create a controller
controller = Controller(model)

app = FastAPI()

# Serve static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

result_file_path = './'
result_file_name = 'result.xlsx'

uploaded_files = {"yaml": False, "excel": False}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI Web App</title>
        <link rel="stylesheet" href="/static/styles.css">
        <script>
            async function uploadFile(endpoint, fileInputId, paramName) {
                const fileInput = document.getElementById(fileInputId);
                const formData = new FormData();
                formData.append(paramName, fileInput.files[0]);
                
                const response = await fetch(endpoint, { method: "POST", body: formData });
                const result = await response.json();
                
                if (response.ok) {
                    document.getElementById(fileInputId + "_status").innerText = "Uploaded";
                    localStorage.setItem(fileInputId + "_uploaded", "true");
                } else {
                    document.getElementById(fileInputId + "_status").innerText = "Failed";
                    localStorage.setItem(fileInputId + "_uploaded", "false");
                }
                checkFilesUploaded();
            }
            
            function checkFilesUploaded() {
                const yamlUploaded = localStorage.getItem("yaml_file_uploaded") === "true";
                const excelUploaded = localStorage.getItem("excel_file_uploaded") === "true";
                const executeButton = document.getElementById("execute_button");
                executeButton.disabled = !(yamlUploaded && excelUploaded);
            }
            
            async function executeApp() {
                const response = await fetch("/execute_app", { method: "POST" });
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = "result.xlsx";
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                } else {
                    alert("Execution failed");
                }
            }
            
            window.onload = function() {
                localStorage.setItem("yaml_file_uploaded", "false");
                localStorage.setItem("excel_file_uploaded", "false");
                checkFilesUploaded();
            };
        </script>
    </head>
    <body>
        <h1>FastAPI Web App</h1>
        <p>Upload YAML and Excel files, then execute the app.</p>
        
        <label for="yaml_file">Upload YAML config:</label>
        <input type="file" id="yaml_file" accept=".yaml, .yml" required>
        <button type="button" onclick="uploadFile('/upload_yaml', 'yaml_file', 'yaml_file')">Upload YAML</button>
        <span id="yaml_file_status"></span>
        
        <br><br>
        
        <label for="excel_file">Upload Excel file:</label>
        <input type="file" id="excel_file" accept=".xlsx, .xls" required>
        <button type="button" onclick="uploadFile('/upload_excel', 'excel_file', 'excel_file')">Upload Excel</button>
        <span id="excel_file_status"></span>
        
        <br><br>
        
        <button type="button" id="execute_button" onclick="executeApp()" disabled>Execute the app</button>
    </body>
    </html>
    """

@app.post("/upload_yaml")
async def upload_yaml(yaml_file: UploadFile = File(...)):
    with open("input.yaml", "wb") as f:
        shutil.copyfileobj(yaml_file.file, f)
    uploaded_files["yaml"] = True
    return {"message": "YAML file uploaded successfully"}

@app.post("/upload_excel")
async def upload_excel(excel_file: UploadFile = File(...)):
    with open("input.xlsx", "wb") as f:
        shutil.copyfileobj(excel_file.file, f)
    uploaded_files["excel"] = True
    return {"message": "Excel file uploaded successfully"}

@app.post("/execute_app")
async def execute_app():
    if not (uploaded_files["yaml"] and uploaded_files["excel"]):
        return JSONResponse(status_code=400, content={"message": "Both files must be uploaded first."})
    
    try:
        controller.run('input.xlsx', 'input.yaml')
    except Exception as e:
        return JSONResponse(status_code=400, content=repr(e))
    
    if os.path.exists(result_file_path + result_file_name):
        return FileResponse(path=result_file_path + result_file_name, filename=result_file_name, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
