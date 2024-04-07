import utils.auth as auth_utils
from jose import jwt
from repositories.postgres.crud import um_crud
from utils.custom_exception import DataExist

class UserService:
    def __init__(self, repo, database, logger):
        self.repo = repo
        self.database = database
        self.logger = logger

    async def post_user(self, req_payload: dict[str,any]) -> dict[str,any]:
        async with self.database.transaction():
            user_exist = await self.repo.get_user(req_payload.get('username'))
            if user_exist:
                raise DataExist("Username is already exist")
            
            get_rekening = await self.repo.create_user(req_payload=req_payload)
        return get_rekening

    async def get_user(self, decoded_token: dict[str,any]) -> dict[str,any]:
        async with self.database.transaction():
            user_exist = await self.repo.get_user(decoded_token.get('username'))
            if not user_exist:
                raise Exception("Username Does Not Exist")
        return user_exist   
    
    async def select_users(self, decoded_token: dict[str,any]) -> list[dict[str,any]]:
        async with self.database.transaction():
            if decoded_token['role'] != 'admin':
                raise Exception("Unauthorized role")
            list_user = await self.repo.select_users()
            if not list_user:
                raise Exception("List of Users is not exist")
        return list_user   

def init_service_user(database, db_model, logger):
    repo = um_crud.RepositoryUser(database, db_model, logger)
    return UserService(repo,database,logger)