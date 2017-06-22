from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL



mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pwd'
app.config['MYSQL_DATABASE_DB'] = 'MoodDb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


mysql.init_app(app)

api = Api(app)


class User(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('slug', type=str, help='Slug to create user')
            parser.add_argument('name', type=str, help='Name to create user')
            args = parser.parse_args()

            _userEmail = args['email']
            _userSlug = args['slug']
            _userName = args['name']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spCreateUser',(_userName, _userSlug, _userEmail))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'User creation success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spGetUsers')
            data = cursor.fetchall()

            res = []
            for user in data:
                res += [
                    {
                        'id': user[0],
                        'name': user[1],
                        'slug': user[2],
                        'email': user[3]
                    }
                ]
            return res
        except Exception as e:
            return {'error': str(e)}

    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('slug', type=str, help='Slug to create user')
            parser.add_argument('name', type=str, help='Name to create user')
            args = parser.parse_args()

            _userEmail = args['email']
            _userSlug = args['slug']
            _userName = args['name']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spUpdateUser',(_userName, _userSlug, _userEmail))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'User update success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}


class DeleteUser(Resource):
    def delete(self, user_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spDeleteUser',(user_id))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'User delete success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}


class Team(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('description', type=str, help='Description address to create team')
            parser.add_argument('slug', type=str, help='Slug to create team')
            parser.add_argument('name', type=str, help='Name to create team')
            args = parser.parse_args()

            _userdescription = args['description']
            _userSlug = args['slug']
            _userName = args['name']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spCreateTeam',(_userName, _userSlug, _userdescription))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Team creation success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spGetTeams')
            data = cursor.fetchall()

            res = []
            for user in data:
                res += [
                    {
                        'id': user[0],
                        'name': user[1],
                        'slug': user[2],
                        'description': user[3]
                    }
                ]
            return res
        except Exception as e:
            return {'error': str(e)}

    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('description', type=str, help='Description address to create user')
            parser.add_argument('slug', type=str, help='Slug to create user')
            parser.add_argument('name', type=str, help='Name to create user')
            args = parser.parse_args()

            _userdescription = args['description']
            _userSlug = args['slug']
            _userName = args['name']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spUpdateTeam',(_userName, _userSlug, _userdescription))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Team update success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}


class DeleteTeam(Resource):
    def delete(self, user_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spDeleteTeam',(user_id))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Team delete success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}


class Mood(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('timestamp', type=str, help='Timestamp address to create mood')
            parser.add_argument('label', type=str, help='Slug to create mood')
            parser.add_argument('value', type=str, help='Name to create mood')
            parser.add_argument('user_id', type=str, help='User Id to create mood')
            args = parser.parse_args()

            _moodDescriptoin = args['timestamp']
            _moodLabel = args['label']
            _moodValue = args['value']
            _moodUserId = args['user_id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spCreateMood',(_moodDescriptoin, _moodLabel, _moodValue, _moodUserId))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Mood creation success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('start_date', type=str, help='Start timestamp address to get mood')
            parser.add_argument('end_date', type=str, help='End timestamp to get mood')
            parser.add_argument('team_id', type=int, help='Team Id to get mood')
            parser.add_argument('user_id', type=int, help='User Id to get mood')
            args = parser.parse_args()

            _moodStartDate = args['start_date']
            _moodEndDate = args['end_date']
            _moodTeamId = args['team_id']
            _moodUserId = args['user_id']

            conn = mysql.connect()
            cursor = conn.cursor()
            users = []
            if _moodTeamId:
                print _moodTeamId
                cursor.callproc('spGetUsersPerTeam', (_moodTeamId,))
                data = cursor.fetchall()
                for user in data:
                    users += [
                        {
                          'user_id': user[0],
                          'name': user[1]
                        }
                    ]
            else:
                if _moodUserId:
                    cursor.callproc('spGetUser', (_moodUserId,))
                    data = cursor.fetchall()
                    for user in data:
                        users += [
                          {
                            'user_id': user[0],
                            'name': user[1]
                          }
                        ]
                else:
                    return {'StatusCode': '1000', 'Message': 'Please specify team_id or user_id'}
            for user in users:
                cursor.callproc('spGetMoods', (_moodStartDate, _moodEndDate, user['user_id']))
                data = cursor.fetchall()
                moods = []
                for mood in data:
                    moods += [
                    {
                        'id': mood[0],
                        'timestamp': str(mood[1]),
                        'label': mood[2],
                        'value': mood[3]
                    }
                ]
                user['mood'] = moods
            return users

        except Exception as e:
            return {'error': str(e)}


    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('description', type=str, help='Description address to create user')
            parser.add_argument('slug', type=str, help='Slug to create user')
            parser.add_argument('name', type=str, help='Name to create user')
            args = parser.parse_args()

            _userdescription = args['description']
            _userSlug = args['slug']
            _userName = args['name']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spUpdateMood',(_userName, _userSlug, _userdescription))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Mood update success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}


class DeleteMood(Resource):
    def delete(self, user_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spDeleteMood',(user_id))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Mood delete success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}


api.add_resource(User, '/users')
api.add_resource(DeleteUser, '/user/<string:user_id>')
api.add_resource(Team, '/teams')
api.add_resource(DeleteTeam, '/user/<string:team_id>')
api.add_resource(Mood, '/moods')
api.add_resource(DeleteMood, '/user/<string:mood_id>')

if __name__ == '__main__':
    app.run(debug=True)
