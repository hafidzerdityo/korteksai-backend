from sqlalchemy import select

class RepositoryAuth:
    def __init__(self, database, db_model, logger):
        self.database = database
        self.db_model = db_model
        self.logger = logger

    async def get_hashed_pass_by_username(self, username: str) -> dict[str,any]:
        try:
            mask_password = '*REDACTED*'
            self.logger.info(f"request: {username} START: get_hashed_pass_by_username")
            query = select(self.db_model.Account).where(self.db_model.Account.c.username == username)
            row = await self.database.fetch_one(query)
            response = {}
            if row:
                response = dict(row)
            self.logger.info(f"response: {mask_password} END: get_hashed_pass_by_username")
            return response
        except Exception as e:
            remark = 'Database Crud Error'
            self.logger.error(str(e))
            raise Exception(remark)
    
    