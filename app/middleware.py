from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import time
import logging
import traceback

#configure logging
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"{request.method} - {request.url.path}")

    try:
        response = await call_next(request)
    except Exception:
        logger.error("Request failed during processing")
        raise

    process_time = time.time() - start_time
    logger.info(f"Completed in {process_time:.5f}s - Status: {response.status_code}")

    response.headers["X-Process-Time"] = str(process_time)
    return response

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error on {request.method} {request.url.path}")
    
    cleaned_errors = []
    for error in exc.errors():
        cleaned_errors.append({
            "field": error.get("loc"),
            "message": error.get("msg"),
            "type": error.get("type")
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "Invalid input data provided",
            "details": cleaned_errors,
            "path": str(request.url.path)
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions (404, 503, etc.)
    """
    logger.error(f"HTTP {exc.status_code} error on {request.method} {request.url.path}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": str(exc.detail),
            "status_code": exc.status_code,
            "path": str(request.url.path)
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected errors
    """
    logger.error(f"Unexpected error on {request.method} {request.url.path}: {str(exc)}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "path": str(request.url.path),
            "type": type(exc).__name__
        }
    )