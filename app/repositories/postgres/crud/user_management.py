import utils.crud as crud_utils
import utils.auth as auth_utils
from sqlalchemy import select, insert


class RepositoryUser:
    def __init__(self, database, db_model, logger):
        self.db_model = db_model
        self.database = database
        self.logger = logger

    async def create_user(self, req_payload:dict[str,any]) -> dict[str,any]:
        try:
            query = insert(self.db_model.Account).values(
                username = req_payload.get('username'),
                hashed_password = auth_utils.get_password_hash(req_payload.get('password')),
                nama = req_payload.get('nama'),
                email = req_payload.get('email'),
                role = req_payload.get('role'),
                credit = 0,
                created_at = crud_utils.current_datetime(),
                updated_at = None,
                is_deleted = False
            )
            await self.database(query)
            return {
                'success' : True
            }
               
            
        except Exception as e:
            remark = 'Database Crud Error'
            self.logger.error(str(e))
            raise Exception(remark)


    # # RAW Query Example
    # async def check_user(self, username: str):
    #     try:
    #         query = f"""
    #             SELECT username, nama, role, divisi, jabatan, created_at, is_deleted
    #             FROM "user"
    #             WHERE username = :username
    #         """
    #         user_exist = await self.database.fetch_one(query=query, values={"username": username})
            
    #         if user_exist:
    #             user_exist = dict(user_exist)
    #             user_exist['created_at'] = user_exist['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f")
    #         else:
    #             user_exist = {}
    #         return user_exist
    #     except Exception as e:
    #         remark = 'Database Crud Error'
    #         self.logger.error(str(e))
    #         raise Exception(remark)
        
    async def get_user(self, username: str) -> dict[str,any]:
        try:
            query = select(self.db_model.Account).where(
                (self.db_model.Account.c.username == username)
            )
            user_exist = await self.database.fetch_one(query)
            
            if user_exist:
                user_exist = dict(user_exist)
                user_exist['created_at'] = user_exist['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f")
            else:
                user_exist = {}
            return user_exist
        except Exception as e:
            remark = 'Database Crud Error'
            self.logger.error(str(e))
            raise Exception(remark)
        
    async def select_users(self) -> list[dict]:
        try:
            query = select(self.db_model.Account)
            user_list = await self.database.fetch_all(query)
            user_dicts = []
            for row in user_list:
                user_dict = dict(row)
                user_dict['created_at'] = user_dict['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f")
                user_dicts.append(user_dict)
            return user_dicts
        except Exception as e:
            remark = 'Database Crud Error'
            self.logger.error(str(e))
            raise Exception(remark)


