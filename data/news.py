import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user = orm.relation('User')
    categories = orm.relation("Category",
                              secondary="category_to_news",
                              backref="news")

    def __repr__(self):
        return f'<News> {self.title}'