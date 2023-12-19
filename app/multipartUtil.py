import os
import requests

from fastapi import FastAPI, File, UploadFile, Query
from app.connection import getCommonConfig

app = FastAPI()
CONFIG = getCommonConfig()


@app.post("/multipart-upload")
async def create_papers(file: UploadFile = File(...), outputDir: str = Query(...)):
    try:
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        outputFile = os.path.join(outputDir, file.filename)
        with open(outputFile, "wb") as f:
            f.write(file.file.read())
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        return {"error": str(e)}


def do_upload_file(filepath: str):

    fileUploadUrl = CONFIG['vulcan.original.file.url']
    outputDir = os.path.dirname(filepath)
    files = {'file': open(filepath, 'rb')}
    url_with_params = f"{fileUploadUrl}?outputDir={outputDir}"
    response = requests.post(url_with_params, files=files)
    print(response.status_code)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
