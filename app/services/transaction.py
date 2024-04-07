import utils.auth as auth_utils
from jose import jwt
from repositories.postgres.crud import trx_crud
from utils.custom_exception import DataExist

class TransactionService:
    def __init__(self, repo, database, logger):
        self.repo = repo
        self.database = database
        self.logger = logger

    async def update_credit(self, req_payload: dict[str,any]) -> dict[str,any]:
        async with self.database.transaction():
            try:
                account_data = await self.repo.get_user(req_payload.get('username'))
                if not account_data:
                    raise DataExist("Username is not exist")
                service_response = await self.repo.update_credit(req_payload)
            except Exception as e:
                self.logger.error(str(e)) 
                raise Exception(f"service_error: {str(e)}")

        return service_response


def init_transaction_user(database, db_model, logger):
    repo = trx_crud.RepositoryTransaction(database, db_model, logger)
    return TransactionService(repo,database,logger)