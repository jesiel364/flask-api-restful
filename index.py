from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

import json

app = Flask("PigzApi")
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("name", required=True)
parser.add_argument("created",  type=int, required=False)
# parser.add_argument('email': required=True)

with open("users.json", 'r') as f:
    users = json.load(f)

def write_changes_to_file():
    global users
    users = {k: v for k, v in sorted(users.items(), key=lambda user: user[1]['created']) }
    with open('users.json', 'w') as file:
        json.dump(users, file)



class MyData(Resource):
    def get(self, user_id):
        if user_id == "all":
            return users
        if user_id not in users:
            abort(404, message=f"User {user_id} not found!")

        return users[user_id], 200

    def put(self, user_id):
        args = parser.parse_args()
        new_user = {'name': args['name'],
                    'created': args['created']
                    }
        users[user_id] = new_user
        write_changes_to_file()
        return {user_id: users[user_id]}, 201

    def delete(self, user_id):
        if user_id not in users:
            abort(404, message=f"User {user_id} not found!")
        del users[user_id]
        return "", 204


class UserSchedule(Resource):
    def get(self):
        return users
    
    def post(self):
        args = parser.parse_args()
        new_user = {'name': args['name'],
                     'created': args['created']
                    }
        user_id = max(int(u.lstrip('user')) for u in users.keys()) + 1
        print(user_id)
        user_id = f"user{user_id}"
        users[user_id] = new_user
        write_changes_to_file()
        return users[user_id], 201
    

api.add_resource(MyData, '/users/<user_id>')
api.add_resource(UserSchedule, '/users')

if __name__ == '__main__':
    app.run()
