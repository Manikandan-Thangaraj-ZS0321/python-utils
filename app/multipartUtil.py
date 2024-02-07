import os
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse

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
            read = file.file.read()
            f.write(read)

            # Flush and close the file stream to ensure all data is written
            f.flush()
            f.close()

        logger.info("File {} downloaded successfully".format(file.filename))
        return {"message": "File downloaded successfully", "filename": file.filename}
    except Exception as e:
        logger.error("Error in downloading multipart file {} with exception {}".format(file.filename, e))
        return {"error": str(e)}


@app.post("/multipart-download")
async def do_upload_file(filepath: str):
    try:
        file_path = Path(filepath)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found at path: {file_path}")
        filename = os.path.basename(file_path)
        logger.info({"message": "File uploaded"})

        def file_iterator(filepath):
            with open(filepath, "rb") as file:
                while chunk := file.read(65536):
                    yield chunk

        return StreamingResponse(file_iterator(file_path), media_type="application/octet-stream",
                                 headers={"Content-Disposition": f"attachment; filename={filename}"})

    except Exception as ex:
        logger.error(f"Error in uploading multipart file {filepath} with exception {ex}")
        raise ex

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8002)
