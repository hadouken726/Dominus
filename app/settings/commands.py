import click
import random
from flask import Flask
from flask.cli import AppGroup
from faker import Faker
from faker.providers.ssn import pt_BR
from faker.providers import ssn
from werkzeug.security import generate_password_hash

from click import argument, echo
from datetime import datetime, timedelta

from app.models.notices_model import NoticesModel
from app.models.users_model import UsersModel
from app.models.polls_model import PollsModel
from app.models.poll_options_model import PollOptionsModel

fake = Faker("pt_BR")
fake.add_provider(ssn)


def cli_users(app: Flask):
    cli_users_group = AppGroup("users")

    # ** Delete table
    @cli_users_group.command("del")
    def cli_users_delete():
        session = app.db.session

        session.query(UsersModel).delete()
        session.commit()

        echo("UsersModel table data was deleted!")

    # ** Populate with amount
    @cli_users_group.command("populate")
    @click.argument("amount")
    def cli_users_populate(amount: str):
        session = app.db.session

        for _ in range(int(amount)):
            user = {
                "cpf": "%0.11d" % random.randint(0,99999999999),
                "phone": fake.msisdn()[2:],
                "name": fake.name(),
                "password": "123456",
            }

            password_to_hash = user.pop("password")
            new_user = UsersModel(**user)

            new_user.password = generate_password_hash(password_to_hash)

            session.add(new_user)
            session.commit()

            click.echo(f"The table UsersModel was populated with {amount} users!")

    # ** Create User ADMIN
    @cli_users_group.command("create_admin")
    def cli_users_create_admin():
        session = app.db.session

        user = {
            "cpf": "%0.11d" % random.randint(0,99999999999),
            "phone": fake.msisdn()[2:],
            "name": fake.name(),
            "password": "654321",
            "is_admin": True,
        }

        password_to_hash = user.pop("password")
        new_user = UsersModel(**user)
        new_user.password = generate_password_hash(password_to_hash)

        session.add(new_user)
        session.commit()

        click.echo("Admin was created!")
        click.echo(f"Admin --> {new_user.name}")
        click.echo(f"CPF --> {new_user.cpf}")
        click.echo(f"Password --> {new_user.password}")

    app.cli.add_command(cli_users_group)


def cli_notices(app: Flask):
    cli_notices_group = AppGroup("notices")

    @cli_notices_group.command("del")
    def cli_notices_delete():
        session = app.db.session

        session.query(NoticesModel).delete()
        session.commit()

        click.echo("NoticesModel table data was deleted!")

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

            session.add(notice)
            session.commit()

    app.cli.add_command(cli_notices_group)


def cli_polls(app: Flask):
    cli_polls_group = AppGroup("polls")

    @cli_polls_group.command("populate")
    @click.argument("amount")
    def cli_polls_populate(amount: str):
        session = app.db.session

        for _ in range(int(amount)):
            poll = {
                "start_at": str(datetime.utcnow()),
                "end_at": str(datetime.utcnow() + timedelta(days=2)),
                "desc": fake.paragraph(
                    nb_sentences=5, variable_nb_sentences=True, ext_word_list=None
                ),
                "title": fake.paragraph(
                    nb_sentences=1, variable_nb_sentences=True, ext_word_list=None
                ).title(),
            }

            poll = PollsModel(**poll)

            session.add(poll)
            session.commit()

        click.echo(f"The table PollsModel was populated with {amount} poll(s)!")

    @cli_polls_group.command("del")
    def cli_polls_delete():
        session = app.db.session

        session.query(PollsModel).delete()
        session.commit()

        echo("PollsModel table data was deleted!")

    app.cli.add_command(cli_polls_group)


def cli_poll_options(app: Flask):
    cli_poll_options_group = AppGroup("poll_options")

    @cli_poll_options_group.command("populate")
    @click.argument("amount")
    def cli_poll_options_populate(amount: str):
        session = app.db.session

        for count in range(int(amount)):
            poll_option = {"name": f"Option {count}"}
            # TODO [ ] poll_id = COMO PUXAR OS VALORES DA RELAÇÃO ENTRE AS TABELAS

            poll_option: PollOptionsModel = PollOptionsModel(**poll_option)

            session.add(poll_option)
            session.commit()

        click.echo(
            f"The table PollOptionsModel was populated with {amount} poll(s) options!"
        )

    @cli_poll_options_group.command("del")
    def cli_poll_options_delete():
        session = app.db.session

        session.query(PollOptionsModel).delete()
        session.commit()

        echo("PollOptionsModel table data was deleted!")

    app.cli.add_command(cli_poll_options_group)


def init_app(app: Flask):
    cli_users(app)
    cli_notices(app)
    cli_polls(app)
    cli_poll_options(app)
