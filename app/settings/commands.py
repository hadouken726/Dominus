import click
from flask import Flask
from flask.cli import AppGroup
from faker import Faker

from click import argument, echo

from app.models.notices_model import NoticesModel
from app.models.users_model import UsersModel

fake = Faker()

# TODO Create commands to DELETE, POPULATE and CREATE ADMIN tables: NoticesModel and UsersModel
def cli_users(app: Flask):
    cli_users_group = AppGroup("users")

    # ** Delete table
    @cli_users_group.command("del")
    def cli_users_delete():
        session = app.db.session

        session.query(UsersModel).delete()
        session.commit()

        echo("UsersModel table was deleted!")

    # ** Populate with amount
    @cli_users_group.command("populate")
    @click.argument("amount")
    def cli_users_populate(amount: str):
        session = app.db.session

        for _ in range(int(amount)):
            user = {
                "cpf": fake.cpf(),
                "phone": fake.cellphone_number(),
                "name": fake.name(),
                "password": fake.password(
                    length=10,
                    special_chars=True,
                    digits=True,
                    upper_case=True,
                    lower_case=True,
                ),
                "home_number": fake.pyint(min_value=101, max_value=108, step=1),
            }

            user = UsersModel(**user)

            session.add(user)
            session.commit()

            click.echo(f"The table UsersModel was populated with {amount} users!")

    # ** Create User ADMIN
    @cli_users_group.command("create_admin")
    def cli_users_create_admin():
        session = app.db.session

        for _ in range(int(amount)):
            user = {
                "cpf": fake.cpf(),
                "phone": fake.cellphone_number(),
                "name": fake.name(),
                "password": fake.password(
                    length=10,
                    special_chars=True,
                    digits=True,
                    upper_case=True,
                    lower_case=True,
                ),
                "is_admin": True,
                "home_number": fake.pyint(min_value=201, max_value=208, step=1),
            }

            user = UsersModel(**user)

            session.add(user)
            session.commit()

            click.echo("Admin was created!")
            click.echo(f"Admin --> {user.name}")
            click.echo(f"CPF --> {user.cpf}")
            click.echo(f"Password --> {user.password}")

    app.cli.add_command(cli_users_group)


# TODO Create commands to DELETE and POPULATE Notifications on table NoticesModel
def cli_notices(app: Flask):
    cli_notices_group = AppGroup("notices")

    @cli_notices_group.command("del")
    def cli_notices_delete():
        session = app.db.session

        session.query(NoticesModel).delete()
        session.commit()

        echo("NoticesModel table was deleted!")

    @cli_notices_group.command("populate")
    @click.argument("amount")
    def cli_notices_populate(amount: str):
        session = app.db.session

        for _ in range(int(amount)):
            notice = {
                "title": fake.sentence(
                    nb_words=6, variable_nb_words=True, ext_word_list=None
                ),
                "desc": fake.paragraphs(nb=5, ext_word_list=None),
                "updated_at": fake.date_time(tzinfo=None, end_datetime=None),
            }

            notice = NoticesModel(**notice)

            session.add(user)
            session.commit()

    app.cli.add_command(cli_notices_group)

def init_app(app:Flask):
    cli_users(app)
    cli_notices(app)