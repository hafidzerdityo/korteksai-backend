from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from api.schemas import um_schemas
import services.user_management as um_services
import utils.auth as auth_utils
from utils import custom_exception
from repositories.postgres.config import db_config
from repositories.postgres.config import db_model
from logs import logger

router = APIRouter()

user_service = um_services.init_service_user(db_config.database,db_model,logger)

@router.post('/user', tags=["User Management"], status_code=status.HTTP_201_CREATED, response_model=um_schemas.ResponseDaftar)
async def create_user(request_payload: um_schemas.RequestDaftar) -> um_schemas.ResponseDaftar:
    try:
        request_payload_dict = dict(request_payload)
        request_payload_log = request_payload_dict.copy()
        
        if 'password' in request_payload_log:
            request_payload_log['password'] = '***REDACTED***'

        logger.info(request_payload_log)

        _ = await user_service.post_user(request_payload_dict)
        response = {
            'resp_msg': 'Pendaftaran Berhasil',
            'resp_data': None
        }

        logger.info(response)

        return um_schemas.ResponseDaftar(
            **response
        ) 
    
    except custom_exception.DataExist as e:
        return custom_exception.handle_exception(logger, status.HTTP_409_CONFLICT, str(e))
    except Exception as e:
        return custom_exception.handle_exception(logger, status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
    
@router.get('/user', tags=["User Management"], status_code=status.HTTP_200_OK, response_model=um_schemas.ResponseUser)
async def get_user(decoded_token: dict[str,any] = Depends(auth_utils.get_current_user)) -> um_schemas.ResponseUser:
    try:
        logger.info(decoded_token)
        if decoded_token.get('error'):
            raise Exception(decoded_token.get('msg'))
        data_fetch_success = await user_service.get_user(decoded_token)
        data_fetch_success = um_schemas.ResponseUserItem(**data_fetch_success)
        response = {
            'resp_msg': 'Get Data Berhasil',
            'resp_data': data_fetch_success
        }
        return um_schemas.ResponseUser(
            **response
        ) 
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code= status.HTTP_401_UNAUTHORIZED,
            content={"resp_msg": str(e),
                     "resp_data":  None
                     },
        )
    
@router.get('/users', tags=["User Management"], status_code=status.HTTP_200_OK, response_model=um_schemas.ResponseUsers)
async def get_user(decoded_token: dict[str,any] = Depends(auth_utils.get_current_user)) -> um_schemas.ResponseUsers:
    try:
        logger.info(decoded_token)
        if decoded_token.get('error'):
            raise Exception(decoded_token.get('msg'))
        data_fetch_success = await user_service.select_users(decoded_token)
        data_fetch_success = [um_schemas.ResponseUserItem(**i) for i in data_fetch_success]
        return um_schemas.ResponseUsers(
            resp_msg = "Get Data Berhasil",
            resp_data = data_fetch_success
        )
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code= status.HTTP_401_UNAUTHORIZED,
            content={"resp_msg": str(e),
                     "resp_data":  None
                     },
        )
    

