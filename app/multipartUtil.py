import os
import requests
import logging

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
        return {"message": "File downloaded successfully", "filename": file.filename}
    except Exception as e:
        logging.error("Error in downloading multipart file {} with exception {}".format(file.filename, e))
        return {"error": str(e)}


def do_upload_file(filepath: str):
    try:
        fileUploadUrl = CONFIG['vulcan.original.file.url']
        outputDir = os.path.dirname(filepath)
        files = {'file': open(filepath, 'rb')}
        url_with_params = f"{fileUploadUrl}?outputDir={outputDir}"
        response = requests.post(url_with_params, files=files)
        code = response.status_code
        logging.info("File {} uploaded successfully with status code {}".format(filepath, code))
        return {"message": "File uploaded successfully", "file": filepath, "responseCode": code}
    except Exception as e:
        logging.error("Error in uploading multipart file {} with exception {}".format(filepath, e))
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
