from flask import Flask
from flask_restful import Api,Resource
from flask_restful.reqparse import RequestParser
from marshmallow import Schema
from sqlalchemy import Column, Integer, String
from base import Base, session_factory

app = Flask(__name__)
api = Api(app)

class AddUser(Resource):
    def post(self):
        parser = RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        email = args['email']

        session = session_factory()
        test = session.query(User).filter_by(email=email).first()
        if test:
            return { 'msg': 'email already exists' } , 401
        else:
            noman = User(
            first_name = args['first_name'],
            last_name = args['last_name'],
            email = args['email'],
            password = args['password'],
            )
            session.add(noman)
            session.commit()
            session.close()
            return { 'msg': 'user created' } , 201

class RemoveUser(Resource):
    def delete(self,id):
        session = session_factory()
        test = session.query(User).filter_by(id=id).first()
        if test:
            session.delete(test)
            session.commit()
            session.close()
            return {'msg':'user deleted'} , 200
        else:
            session.close()
            return {'msg': 'user id invalid'}, 400



class UpdateUser(Resource):
    def put(self):
        parser = RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        email = args['email']

        session = session_factory()
        user = session.query(User).filter_by(email=email).first()
        if user:
            user.first_name = args['first_name']
            user.last_name =  args['last_name']
            user.email = args['email']
            user.password = args['password']

            session.commit()
            session.close()
            return {'msg': 'user record updated'}, 200
        else:
            session.close()
            return {'msg': 'user id invalid'}, 400


class GetUser(Resource):
    def get(self):
        session = session_factory()
        list = session.query(User).all()
        users = UserSchema(many=True)
        result = users.dump(list)
        return { 'list': result } , 200

# Model For SQLAlchemy
class User(Base):

    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

# Schema For Serialization
class UserSchema(Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

# CRUD Operations
api.add_resource(GetUser, '/get')
api.add_resource(AddUser, '/add')
api.add_resource(UpdateUser, '/update')
api.add_resource(RemoveUser, '/remove/<int:id>')

app.run(debug=True)