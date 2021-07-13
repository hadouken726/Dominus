from app.models.users_model import UsersModel


class UsersServices:
    @staticmethod
    def hashing(data):
        password_to_hash = data.pop("password")
        new_user: UsersModel = UsersModel(**data)
        new_user.password_hash = password_to_hash

        return new_user

