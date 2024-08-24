from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import json

import services.transaction as trx_service
import utils.auth as auth_utils
from repositories.postgres.config import db_config
from repositories.postgres.config import db_model
from logs import logger
from api.schemas import trx_schemas
from utils import custom_exception

router = APIRouter()

transaction_service = trx_service.init_transaction_user(db_config.database,db_model,logger)


@router.post('/topup', tags=["Transaction"], status_code=status.HTTP_201_CREATED, response_model=trx_schemas.ResponseTopup)
async def update_credit(request_payload: trx_schemas.RequestTopup, decoded_token: dict[str,any] = Depends(auth_utils.get_current_user)) -> trx_schemas.ResponseTopup:
    try:
        if decoded_token.get('error'):
            raise custom_exception.FailedToken(decoded_token.get('msg'))
        request_payload_dict = dict(request_payload)
        request_payload_dict["username"] = decoded_token.get("username")
        logger.info(request_payload_dict)
        service_response = await transaction_service.update_credit(request_payload_dict)
        response = {
            'resp_msg': 'Top up Berhasil',
            'resp_data': service_response
        }
        logger.info(response)
        return trx_schemas.ResponseTopup(
            **response
        ) 
    except custom_exception.FailedToken as e:
        return custom_exception.handle_exception(logger, status.HTTP_401_UNAUTHORIZED, str(e))
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content={"resp_msg": str(e),
                     "resp_data":  None
                     },
        )
    