from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from . import db_session
from .users import User


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('full_name', required=True)
parser.add_argument('email', required=True)
parser.add_argument('birthday', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'news': user.to_dict(
            only=('id', 'full_name', 'email', 'birthday'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'full_name', 'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            id=args['id'],
            full_name=args['full_name'],
            email=args['email'],
            birthday=args['birthday']
        )
        session.add(users)
        session.commit()
        return jsonify({'id': users.id})