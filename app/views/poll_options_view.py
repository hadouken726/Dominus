from app.models.users_model import UsersModel
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm import session
from app.models.poll_options_model import PollOptionsModel, PollOptionSchema
from http import HTTPStatus
from flask_restful import Resource
import sqlalchemy.exc as e


class PollOptions(Resource):
    def get(self, poll_option_id=None):
        if poll_option_id is None:
            poll_options: PollOptionsModel = PollOptionsModel().query.all()
            poll_options_schema = PollOptionSchema()
            return {
                "poll_options": poll_options_schema.dump(poll_options, many=True)
            }, HTTPStatus.OK

        else:
            try: 
                poll_option: PollOptionsModel = PollOptionsModel.query.get_or_404(poll_option_id)
                poll_option_schema = PollOptionSchema()
                return poll_option_schema.dump(poll_option), HTTPStatus.OK

            except e.DataError:
                return {
                     "message": "invalid number, just accept int with register ids",
                        "error": "DataError"
                }, HTTPStatus.BAD_REQUEST

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        current_user = UsersModel.query.get_or_404(current_user_id, description='Invalid user!')
        data = request.get_json()
        if current_user.is_admin:
            try:
                session = current_app.db.session


                new_poll_option = PollOptionSchema().load(data, session=session)
                if not new_poll_option.poll_id:
                    return {'message':'poll_id is necessary!'}

                session.add(new_poll_option)
                session.commit()

                return PollOptionSchema().dump(new_poll_option)

            except ValidationError as VE:
                return VE.messages
        return {"message": "user don't have admin permission to create a new poll option"}, HTTPStatus.UNAUTHORIZED
            
            

    
    @jwt_required()
    def delete(self, poll_option_id=None):
        current_user_id = get_jwt_identity()
        current_user = UsersModel.query.get_or_404(current_user_id, description='Invalid user!')
        if current_user.is_admin:
            session = current_app.db.session
            poll_option = PollOptionsModel().query.get_or_404(poll_option_id)
            session.delete(poll_option)
            session.commit()

            return {
                "message": f"Poll option {poll_option.id} has been deleted"
            }

        
        return {
                "message": "user don't have admin permission to delete a poll option"
        }, HTTPStatus.UNAUTHORIZED

    @jwt_required()
    def patch(self, poll_option_id=None):
        current_user_id = get_jwt_identity()
        current_user = UsersModel.query.get_or_404(current_user_id, description='Invalid user!')
        if current_user.is_admin:
            try:
                session = current_app.db.session
                data = request.get_json()
                poll_option = PollOptionsModel.query.get_or_404(poll_option_id)
                new_poll_option = PollOptionSchema(only=["name"]).load(data ,partial=True, session=session, instance=poll_option)            
                session.add(new_poll_option)
                session.commit()

                return PollOptionSchema().dump(new_poll_option)

            except ValidationError as VE:
                return VE.messages
        return {
                "message": "user don't have admin permission to patch a poll option"
        }, HTTPStatus.UNAUTHORIZED
