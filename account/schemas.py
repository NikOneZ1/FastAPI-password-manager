from account.models import Account


RequestAccount = Account.get_pydantic(exclude={"id": ...})
