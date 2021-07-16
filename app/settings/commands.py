import click
from flask import Flask
from flask.cli import AppGroup
from faker import Faker
from faker.providers.ssn import pt_BR
from faker.providers import ssn

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
                "cpf": fake.cpf(),
                "phone": fake.msisdn(),
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


def cli_notices(app: Flask):
    cli_notices_group = AppGroup("notices")

    @cli_notices_group.command("del")
    def cli_notices_delete():
        session = app.db.session

        session.query(NoticesModel).delete()
        session.commit()

        echo("NoticesModel table data was deleted!")

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

        for _ in range(int(amount)):
            count = 1
            poll_option = {"name": f"Option {count}"}
            #TODO [ ] poll_id = COMO PUXAR OS VALORES DA RELAÇÃO ENTRE AS TABELAS 

            poll_option: PollOptionsModel = PollOptionsModel(**poll_option)

            session.add(poll_option)
            session.commit()

            count += 1

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
