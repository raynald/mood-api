from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin


mysql = MySQL()
app = Flask(__name__)
CORS(app)

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
            parser = reqparse.RequestParser()
            parser.add_argument('slug', type=str, help='Slug to get user')
            args = parser.parse_args()
            _userSlug = args['slug']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spGetUsers', (_userSlug,))
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
            parser.add_argument('timestamp', type=int, help='Timestamp address to create mood')
            parser.add_argument('label', type=str, help='Label to create mood')
            parser.add_argument('value', type=str, help='Value to create mood')
            parser.add_argument('user_id', type=str, help='User Id to create mood')
            args = parser.parse_args()

            _moodTimestamp = args['timestamp']
            _moodLabel = args['label']
            _moodValue = args['value']
            _moodUserId = args['user_id']

            print _moodTimestamp
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spCreateMood',(_moodTimestamp, _moodLabel, _moodValue, _moodUserId))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Mood creation success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'StatusCode': '1000', 'Message': str(e)}

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('start_date', type=int, help='Start timestamp address to get mood')
            parser.add_argument('end_date', type=int, help='End timestamp to get mood')
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
                cursor.callproc('spGetUsersPerTeam', (_moodTeamId,))
                data = cursor.fetchall()
                for user in data:
                    if not _moodUserId or user[0] == _moodUserId:
                        users += [
                            {
                              'id': user[0],
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
                            'id': user[0],
                            'name': user[1],
                          }
                        ]
            if len(users) == 0:
                return []
            moods = []
            for user in users:
                cursor.callproc('spGetMoods', (_moodStartDate, _moodEndDate, user['id']))
                data = cursor.fetchall()
                for mood in data:
                    moods += [
                    {
                        'user': user,
                        'timestamp': mood[1],
                        'label': mood[2],
                        'value': mood[3]
                    }
                ]
            return moods

        except Exception as e:
            return {'error': str(e)}


    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('timestamp', type=int, help='Timestamp address to update mood')
            parser.add_argument('label', type=str, help='Label to update mood')
            parser.add_argument('value', type=str, help='Value to update mood')
            parser.add_argument('user_slug', type=str, help='User Slug to update mood')
            args = parser.parse_args()

            _moodDescriptoin = args['timestamp']
            _moodLabel = args['label']
            _moodValue = args['value']
            _moodUserSlug = args['user_slug']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spUpdateMood',(_moodDescriptoin, _moodLabel, _moodValue, _moodUserSlug))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Mood update success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}


class DeleteMood(Resource):
    def delete(self, mood_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spDeleteMood',(mood_id))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Mood delete success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}


class Analysis(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('start_date', type=int, help='Start timestamp address to get mood')
            parser.add_argument('end_date', type=int, help='End timestamp to get mood')
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
                cursor.callproc('spGetUsersPerTeam', (_moodTeamId,))
                data = cursor.fetchall()
                for user in data:
                    if not _moodUserId or user[0] == _moodUserId:
                        users += [
                            {
                                'id': user[0],
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
                                'id': user[0],
                                'name': user[1]
                            }
                        ]
            if len(users) == 0:
                return {'StatusCode': '1000', 'Message': 'Not user found'}
            total_average = 0
            ans = []
            for user in users:
                cursor.callproc('spGetMoods', (_moodStartDate, _moodEndDate, user['id']))
                data = cursor.fetchall()
                average = 0
                for mood in data:
                    average += mood[3]
                if len(data) > 0:
                    average /= 1.0 * len(data)
                ans += [
                    {
                        'average': average,
                        'user': user
                    }]
                total_average += average
            if len(users):
                total_average /= 1.0 * len(users)
            ans += [ total_average ]
            return ans
        except Exception as e:
            return {'error': str(e)}


class TeamUsers(Resource):
    def get(self, team_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('spGetUsersPerTeam', (team_id,))
        data = cursor.fetchall()
        users = []
        for user in data:
            users += [
                {
                    'id': user[0],
                    'name': user[1]
                }
            ]
        return users

api.add_resource(User, '/users')
api.add_resource(DeleteUser, '/users/<string:user_slug>')
api.add_resource(Team, '/teams')
api.add_resource(DeleteTeam, '/teams/<string:team_id>')
api.add_resource(TeamUsers, '/teams/<string:team_id>/users')
api.add_resource(Mood, '/moods')
api.add_resource(DeleteMood, '/moods/<string:mood_id>')
api.add_resource(Analysis, '/average')

if __name__ == '__main__':
    app.run(debug=True)
