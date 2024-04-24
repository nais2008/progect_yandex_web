import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    email = sqlalchemy.Column(
        sqlalchemy.String,
        index=True,
        unique=True,
    )
    full_name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    birthday = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now
    )
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    product = orm.relationship("Product", back_populates='user')
    feedback = orm.relationship("Feedback", back_populates='user')
    cart = orm.relationship("Cart", back_populates='user')

    def __repr__(self):
        return f"{self.id} - {self.email}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)