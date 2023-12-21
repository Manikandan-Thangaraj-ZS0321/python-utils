import gc
import time
import uuid

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_prometheus import PrometheusMiddleware, metrics

from app.file_bucketing.bucket import *
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
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "Request ended {} with TAT {}".format(response.status_code,
                                                  (round(time.time() - process_start_time, 2))))
        logger.debug("Garbage collection  {} for ID {}".format(gc.collect(), request_id))
        return response


@app.get("/")
def info():
    return {"App": "Copro Files Bucketing"}


class PreprocessRequest(BaseModel):
    inputDir: str
    outputDir: str
    low_effort_high_yield_min_page: int = 1
    low_effort_high_yield_max_page: int = 4
    high_effort_high_yield_min_page: int = 5
    high_effort_high_yield_max_page: int = 10
    high_effort_low_yield_min_page: int = 11


@app.post("/copro/bucket")
def files_bucket(request: PreprocessRequest):
    logger.info("given file bucketing inbound request  {}".format(request.__str__()))
    processed_files = None
    try:
        processed_files = bucketing(request.inputDir, request.outputDir,request.low_effort_high_yield_min_page,request.low_effort_high_yield_max_page,
                                    request.high_effort_high_yield_min_page,request.high_effort_high_yield_max_page, request.high_effort_low_yield_min_page)
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