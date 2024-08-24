import utils.crud as crud_utils
import utils.auth as auth_utils
from sqlalchemy import select, insert, update
from databases import Database


class RepositoryTransaction:
    def __init__(self, database, db_model, logger):
        self.db_model = db_model
        self.database: Database = database
        self.logger = logger

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

    async def update_credit(self, req_payload: dict[str,any]) -> dict[str,any]:
        try:
            account_data = await self.database.execute(
                update(self.db_model.Account)
                .where(self.db_model.Account.c.username == req_payload.get("username"))
                .values(credit=self.db_model.Account.c.credit + req_payload.get('nominal'))
                .returning(self.db_model.Account.c.credit)
            )

            self.logger.info(account_data)
            return {
                'credit' : account_data
            }
               
        except Exception as e:
            remark = 'Database Crud Error'
            self.logger.error(str(e))
            raise Exception(remark)
