from fastapi.responses import JSONResponse

def handle_exception(logger, status_code, error_message):
    logger.error(error_message)
    return JSONResponse(
        status_code=status_code,
        content={"resp_msg": error_message, "resp_data": None},
    )

class DataExist(Exception):
    pass
class FailedToken(Exception):
    pass