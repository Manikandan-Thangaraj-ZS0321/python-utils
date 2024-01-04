import os
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import FileResponse

from app.connection import getCommonConfig
from app.loggers import logger

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

        logger.info("File {} downloaded successfully".format(file.filename))
        return {"message": "File downloaded successfully", "filename": file.filename}
    except Exception as e:
        logger.error("Error in downloading multipart file {} with exception {}".format(file.filename, e))
        return {"error": str(e)}


@app.post("/multipart-download")
def do_upload_file(filepath: str):
    try:
        file_path = Path(filepath)
        logger.info({"message": "File uploaded"})
        return FileResponse(path=file_path)
    except Exception as e:
        logger.error(f"Error in uploading multipart file {filepath} with exception {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8002)
