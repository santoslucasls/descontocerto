from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

USERS = {
    '1': {'nome': 'Martinalia', 'cpf': '111111111111', "email": 'martinalia@gmail.com'},
    '2': {'nome': 'Zeca Pagodinho', 'cpf': '222222222222', "email": 'martinalia@gmail.com'},
    '3': {'nome': 'Thiaguinho', 'cpf': '333333333333', "email": 'martinalia@gamil.com'},
}


def abort_if_todo_doesnt_exist(user_id):
    if user_id not in USERS:
        abort(404, message="Usuario {} não existe".format(user_id))

parser = reqparse.RequestParser()
parser.add_argument('user')
parser.add_argument('nome')
parser.add_argument('cpf')
parser.add_argument('email')

# User
# shows a single user item and lets you delete a user item
class User(Resource):
    def get(self, user_id):
        abort_if_todo_doesnt_exist(user_id)
        return USERS[user_id]

    def delete(self, user_id):
        abort_if_todo_doesnt_exist(user_id)
        del USERS[user_id]
        return '', 204

    def put(self, user_id):

        args = parser.parse_args()
        print(args)
        user = {'nome': args['nome'], "cpf":args['cpf'], "email":args["email"]}
        USERS[user_id] = user
        return user, 201


# TodoList
# shows a list of all users, and lets you POST to add new user
class UserList(Resource):
    def get(self):
        return USERS

    def post(self):
        args = parser.parse_args()
        user_id = str(int(max(USERS.keys())) + 1)
        user = {'nome': args['nome'], "cpf": args['cpf'], "email": args["email"]}
        USERS[user_id] = user
        return USERS[user_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<user_id>')


if __name__ == '__main__':
    app.run(debug=True)