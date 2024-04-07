from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse

from api.schemas import auth_schemas
from services import auth_services
import utils.auth as auth_utils
from repositories.postgres.config import db_config
from repositories.postgres.config import db_model
from logs import logger

router = APIRouter()
user_service = auth_services.init_service_auth(db_config.database, db_model, logger)

@router.post("/token", tags=["Authentication"], response_model=auth_schemas.ResponseLogin)
async def login_for_access_token(form_data: auth_utils.OAuth2PasswordRequestForm = Depends()) -> auth_schemas.ResponseLogin:
    try:
        get_token_data = await user_service.get_token(form_data.username, form_data.password)
        return auth_schemas.ResponseLogin(
            resp_msg="Login Berhasil",
            resp_data=get_token_data
        )
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            content={
                "resp_msg": str(e),
                "resp_data": None
            },
        )
    
@router.get('/protected/admin', tags=["Authorization"], status_code=status.HTTP_200_OK, response_model=auth_schemas.ResponseProtected)
async def admin_authorization(decoded_token: dict[str,any] = Depends(auth_utils.get_current_user)):
    try:
        if decoded_token.get('role') != 'admin':
            raise Exception('Unauthorized')
        return auth_schemas.ResponseProtected(
            resp_msg = "welcome admin",
            resp_data = None 
        )
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code= status.HTTP_401_UNAUTHORIZED,
            content={"resp_msg": str(e),
                     "resp_data":  None
                     },
        )
    
@router.get('/protected/view', tags=["Authorization"], status_code=status.HTTP_200_OK, response_model=auth_schemas.ResponseProtected)
async def view_authorization(decoded_token: dict[str,any] = Depends(auth_utils.get_current_user)):
    try:
        if decoded_token.get('role') != 'view':
            raise Exception('Unauthorized')
        return auth_schemas.ResponseProtected(
            resp_msg = "welcome view only",
            resp_data = None 
        )
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code= status.HTTP_401_UNAUTHORIZED,
            content={"resp_msg": str(e),
                     "resp_data":  None
                     },
        )
    
@router.get('/current', tags=["Authorization"], status_code=status.HTTP_200_OK, response_model=auth_schemas.ResponseProtected)
async def check_current_token(token: str = Depends(auth_utils.oauth2_scheme)):
    try:
        _ = auth_utils.jwt.decode(token, auth_utils.SECRET_KEY, algorithms=["HS256"])
        return auth_schemas.ResponseProtected(
            resp_msg = "Current Token is Valid",
            resp_data = None 
        )
    except Exception as e:
        logger.error(str(e)) 
        return JSONResponse(
            status_code= status.HTTP_401_UNAUTHORIZED,
            content={"resp_msg": str(e),
                     "resp_data":  None
                     },
        )
    
