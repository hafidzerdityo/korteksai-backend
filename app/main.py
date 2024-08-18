from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from repositories.postgres.config import db_config
import api.routers.user_management
import api.routers.auth
import api.routers.transaction
from logs import logger



from dotenv import load_dotenv
import os
load_dotenv('service.env')

HOST = os.environ.get('SERVICE_HOST')
PORT = os.environ.get('SERVICE_PORT')
WORKERS = os.environ.get('SERVICE_WORKERS')


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_config.database.connect()
    yield
    await db_config.database.disconnect()

app = FastAPI(title="korteksAI Core API",
    description="author: Muhammad Hafidz Erdityo",
    version="0.0.1",
    terms_of_service=None,
    contact=None,
    license_info=None,
    lifespan=lifespan)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_config.metadata.create_all(db_config.engine)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    error_list = []
    for error in details:
        error_list.append(
            {
                "loc": error["loc"],
                "message": error["msg"],
                "type": error["type"],
            }
        )
    modified_response = {
        "resp_data": None,
        "resp_msg": error_list
    }
    logger.error(error_list) 
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(modified_response),
    )

app.include_router(api.routers.user_management.router,prefix="/api/v1/user_management")
app.include_router(api.routers.auth.router,prefix="/api/v1/auth")
app.include_router(api.routers.transaction.router,prefix="/api/v1/trx")

# if __name__ == '__main__':
#     uvicorn.run('main:app', host=HOST, port=int(PORT), workers=int(WORKERS), reload=True)
