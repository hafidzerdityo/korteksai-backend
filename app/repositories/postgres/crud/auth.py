from sqlalchemy import select

class RepositoryAuth:
    def __init__(self, database, db_model, logger):
        self.database = database
        self.db_model = db_model
        self.logger = logger

    async def get_hashed_pass_by_username(self, username: str) -> dict[str,any]:
        try:
            query = select(self.db_model.Account).where(self.db_model.Account.c.username == username)
            row = await self.database.fetch_one(query)
            if row:
                return dict(row)
            else:
                return {}
        except Exception as e:
            remark = 'Database Crud Error'
            self.logger.error(str(e))
            raise Exception(remark)
    
    