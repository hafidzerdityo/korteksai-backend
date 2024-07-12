import utils.auth as auth_utils
from datetime import datetime, timedelta
import api.schemas.auth as schemas
from repositories.postgres.crud import auth_crud
from fastapi import status, Depends
class AuthService:
    def __init__(self, repo: auth_crud.RepositoryAuth, database, logger):
        self.repo = repo
        self.database = database
        self.logger = logger

    async def get_token(self, username, password):
        mask_password = "*REDACTED*"
        self.logger.info(f"request: {username, mask_password} START: get_token")
        async with self.database.transaction():
            user = await self.repo.get_hashed_pass_by_username(username)
            if not user or not auth_utils.verify_password(password, user['hashed_password']):
                raise Exception("Incorrect username or password")
            access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = auth_utils.create_access_token(
                data={"username": user['username'], "role":user['role']}, expires_delta=access_token_expires
            )
            service_response = {"access_token": access_token, "token_type": "bearer"}
            response = schemas.ResponseLoginItem(**service_response)
            self.logger.info(f"response: {response} END: get_token")
            return response

def init_service_auth(database, db_model, logger):
    repo = auth_crud.RepositoryAuth(database, db_model, logger)
    return AuthService(repo,database,logger)