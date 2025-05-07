import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Departaments(SqlAlchemyBase):
    __tablename__ = 'departaments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey('users.id'))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    members = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relationship('User')