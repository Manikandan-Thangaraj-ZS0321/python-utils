import gc
import time
import uuid

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_prometheus import PrometheusMiddleware, metrics

from app.file_bucketing.bucket import bucketing
from app.loggers import logger

COPRO_APP = "Copro App"

app = FastAPI(title=COPRO_APP)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    logger.info(
        "Request started for url {} with ID {}".format(request.url, request_id))
    process_start_time = time.time()
    response = None
    try:
        response = await call_next(request)
    except Exception as ex:
        logger.error(f"Request ID {request_id} for file bucketing api failed: {ex}")
        raise JSONResponse(content={"success": False}, status_code=500)
    finally:
        #response.headers["X-Request-ID"] = request_id
        logger.info(
            "Request ended with TAT {}".format((round(time.time() - process_start_time, 2))))
        logger.debug("Garbage collection  {} for ID {}".format(gc.collect(), request_id))
        return response


@app.get("/")
def info():
    return {"App": "Copro Files Bucketing"}


class PreprocessRequest(BaseModel):
    inputDir: str
    outputDir: str
    low_effort_min_page: list
    high_effort_max_page: list

@app.post("/file-bucket")
def files_bucket(request: PreprocessRequest):
    logger.info("given file bucketing inbound request  {}".format(request.__str__()))
    processed_files = None
    try:
        processed_files = bucketing(request.inputDir, request.outputDir,request.low_effort_min_page,request.high_effort_max_page)
        logger.info(
            "File Bucketing completed for the given input {} and stored the result in {}".format(request.inputDir,
                                                                                         request.outputDir))
        return {'bucketedfiles': processed_files}
    except Exception as ex:
        raise ex
    finally:
        if processed_files is not None:
            del processed_files
        logger.debug("Garbage collection {}".format(gc.collect()))
