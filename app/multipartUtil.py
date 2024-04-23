import gc
import os
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.responses import StreamingResponse

from app.connection import get__common__config
from app.loggers import logger

app = FastAPI()
CONFIG = get__common__config()


@app.post("/multipart-upload")
async def create_papers(file: UploadFile = File(...), outputDir: str = Query(...)) -> dict:
    try:
        if not os.path.exists(outputDir):
            os.makedirs(outputDir, exist_ok=True)
        output_file = os.path.join(outputDir, file.filename)
        if os.path.exists(output_file):
            logger.info("File {} already exists".format(file.filename))
            return {"message": "File already downloaded", "filename": file.filename, "filepath": output_file,
                    "status": "Success"}
        with open(output_file, "wb") as f:
            f.write(file.file.read())
        logger.info("File {} downloaded successfully".format(file.filename), exc_info=True)
        return {"message": "File downloaded successfully", "filename": file.filename, "filepath": output_file,
                "status": "Success"}
    except Exception as e:
        logger.error("Error in downloading multipart file {} with exception {}".format(file.filename, e), exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        gc.collect()


@app.post("/multipart-download")
async def do_upload_file(filepath: str) -> StreamingResponse:
    try:
        file_path = Path(filepath)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found at path: {file_path}")
        filename = os.path.basename(file_path)
        logger.info({"message": "File uploaded"}, exc_info=True)

        def file_iterator(file_p):
            with open(file_p, "rb") as file:
                while chunk := file.read(65536):
                    yield chunk

        return StreamingResponse(file_iterator(file_path), media_type="application/octet-stream",
                                 headers={"Content-Disposition": f"attachment; filename={filename}"})
    except Exception as ex:
        logger.error(f"Error in uploading multipart file {filepath} with exception {ex}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        gc.collect()


@app.delete("/multipart-delete")
async def delete_files(filepath: str = Query(...)) -> dict:
    logger.info(f"Request to delete multipart file {filepath}")
    try:
        if os.path.exists(filepath) and os.path.isfile(filepath):
            os.remove(filepath)
            logger.info(f"File {filepath} deleted successfully", exc_info=True)
        else:
            logger.info(f"File {filepath} not found", exc_info=True)
        return {"status": "Success", "message": "Files deleted successfully", "filepath": filepath}
    except Exception as e:
        logger.error(f"Error deleting files: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        gc.collect()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8002)
