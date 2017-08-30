from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

mysql = MySQL()
app = Flask(__name__)
CORS(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pwd'
app.config['MYSQL_DATABASE_DB'] = 'MoodDb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pwd@0.0.0.0:3306/MoodDb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'MoodService'

mysql.init_app(app)

api = Api(app)

admin = Admin(app, name='MoodAdmin', template_mode='bootstrap3')
db = SQLAlchemy(app)

user_team_map = db.Table('User_Team_Map',
                         db.Column('User_Id', db.Integer, db.ForeignKey('tblUser.Id')),
                         db.Column('Team_Id', db.Integer, db.ForeignKey('tblTeam.Id'))
                         )

class Team(db.Model):
    __tablename__ = 'tblTeam'
    id = db.Column("Id", db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column("Name", db.String(45), nullable=False)
    slug = db.Column("Slug", db.String(45), nullable=True)
    description = db.Column("Description", db.String(45), nullable=False)
    users = db.relationship('User', secondary=user_team_map,
        primaryjoin=id==user_team_map.c.Team_Id,
        backref=db.backref('teams', lazy='dynamic')
    )
    def __repr__(self):
        return '<Team %s>' % self.name

class User(db.Model):
    __tablename__ = 'tblUser'
    id = db.Column("Id", db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column("Name", db.String(45), nullable=False)
    slug = db.Column("Slug", db.String(45), nullable=True)
    email = db.Column("Email", db.String(45), nullable=False)
    def __repr__(self):
        return '<User %s>' % self.name

class Mood(db.Model):
    __tablename__ = 'tblMood'
    id = db.Column("Id", db.Integer, nullable=False, primary_key=True, autoincrement=True)
    timestamp = db.Column("Timestamp", db.String(20), nullable=False)
    label = db.Column("Label", db.String(45), nullable=False)
    value = db.Column("Value", db.Integer, nullable=False)
    user_id = db.Column("User_Id", db.Integer, db.ForeignKey('tblUser.Id'), nullable=False)
    user = db.relationship('User')
    def __repr__(self):
        return '<Mood %s>' % self.label

class Snippet(db.Model):
    __tablename__ = 'tblSnippet'
    id = db.Column("Id", db.Integer, nullable=False, primary_key=True, autoincrement=True)
    timestamp = db.Column("Timestamp", db.String(20), nullable=False)
    content = db.Column("Content", db.String(1000), nullable=False)
    user_id = db.Column("User_Id", db.Integer, db.ForeignKey('tblUser.Id'), nullable=False)
    user = db.relationship('User')
    def __repr__(self):
        return '<Snippet %s>' % (self.content[:25] + '..') if len(self.content) > 25 else self.content


class Users(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('slug', type=str, help='Slug to create user')
            parser.add_argument('name', type=unicode, help='Name to create user')
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
            parser.add_argument('name', type=unicode, help='Name to create user')
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


class Teams(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('description', type=str, help='Description address to create team')
            parser.add_argument('slug', type=str, help='Slug to create team')
            parser.add_argument('name', type=unicode, help='Name to create team')
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

    def put(self, team_id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=unicode, help="Team id to update team")
            parser.add_argument('description', type=str, help='Description address to update team')
            parser.add_argument('slug', type=str, help='Slug to update team')
            parser.add_argument('name', type=unicode, help='Name to update team')
            args = parser.parse_args()

            _userId = args['id']
            _userdescription = args['description']
            _userSlug = args['slug']
            _userName = args['name']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spUpdateTeam',(_userId, _userName, _userSlug, _userdescription))
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


class Moods(Resource):
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


class Snippets(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('timestamp', type=int, help='Timestamp address to create snippet')
            parser.add_argument('content', type=unicode, help='Content of the snippet')
            parser.add_argument('user_id', type=str, help='User Id to create snippet')
            args = parser.parse_args()

            _snippetTimestamp = args['timestamp']
            _snippetContent = args['content']
            _snippetUserId = args['user_id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spCreateSnippet',(_snippetTimestamp, _snippetContent, _snippetUserId))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Snippet creation success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'StatusCode': '1000', 'Message': str(e)}

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('start_date', type=int, help='Start timestamp address to get snippet')
            parser.add_argument('end_date', type=int, help='End timestamp to get snippet')
            parser.add_argument('team_id', type=int, help='Team Id to get snippet')
            parser.add_argument('user_id', type=int, help='User Id to get snippet')
            args = parser.parse_args()

            _snippetStartDate = args['start_date']
            _snippetEndDate = args['end_date']
            _snippetTeamId = args['team_id']
            _snippetUserId = args['user_id']

            conn = mysql.connect()
            cursor = conn.cursor()
            users = []
            if _snippetTeamId:
                cursor.callproc('spGetUsersPerTeam', (_snippetTeamId,))
                data = cursor.fetchall()
                for user in data:
                    if not _snippetUserId or user[0] == _snippetUserId:
                        users += [
                            {
                                'id': user[0],
                                'name': user[1]
                            }
                        ]
            else:
                if _snippetUserId:
                    cursor.callproc('spGetUser', (_snippetUserId,))
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
            snippets = []
            for user in users:
                cursor.callproc('spGetSnippets', (_snippetStartDate, _snippetEndDate, user['id']))
                data = cursor.fetchall()
                for snippet in data:
                    snippets += [
                        {
                            'user': user,
                            'timestamp': snippet[1],
                            'content': snippet[2]
                        }
                    ]
            return snippets

        except Exception as e:
            return {'error': str(e)}


    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('timestamp', type=int, help='Timestamp address to update snippet')
            parser.add_argument('content', type=str, help='Content of the snippet')
            parser.add_argument('user_slug', type=str, help='User Slug to update snippet')
            args = parser.parse_args()

            _snippetTimestamp = args['timestamp']
            _snippetContent = args['content']
            _snippetUserSlug = args['user_slug']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spUpdateSnippet',(_snippetTimestamp, _snippetContent, _snippetUserSlug))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Snippet update success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}


class DeleteSnippet(Resource):
    def delete(self, snippet_id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spDeleteSnippet',(snippet_id))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Snippet delete success'}
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
            active_users = 0
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
                if average > 0:
                    total_average += average
                    active_users += 1
            if active_users > 0:
                total_average /= 1.0 * active_users
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


class Membership(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('team_id', type=int, help='Team id to update the relationship')
            parser.add_argument('user_id', type=int, help='User id to update the relationship')
            args = parser.parse_args()

            _teamId = args['team_id']
            _userId = args['user_id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spCreateMembership', (_teamId, _userId,))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Membership creation success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}
        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('team_id', type=int, help='Team id to update the relationship')
            parser.add_argument('user_id', type=int, help='User id to update the relationship')
            args = parser.parse_args()

            _teamId = args['team_id']
            _userId = args['user_id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spDeleteMembership', (_teamId, _userId,))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'Membership deletion success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}
        except Exception as e:
            return {'error': str(e)}


api.add_resource(Users, '/users')
api.add_resource(DeleteUser, '/users/<string:user_slug>')
api.add_resource(Teams, '/teams')
api.add_resource(DeleteTeam, '/teams/<string:team_id>')
api.add_resource(TeamUsers, '/teams/<string:team_id>/users')
api.add_resource(Moods, '/moods')
api.add_resource(DeleteMood, '/moods/<string:mood_id>')
api.add_resource(Snippets, '/snippets')
api.add_resource(DeleteSnippet, '/snippets/<string:snippet_id>')
api.add_resource(Analysis, '/average')
api.add_resource(Membership, '/memberships')

admin.add_view(ModelView(Team, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Mood, db.session))
admin.add_view(ModelView(Snippet, db.session))

@app.route('/d')
def show_teams():
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)

@app.route('/d/t/<string:team_id>')
def show_users(team_id):
    team = Team.query.get(team_id)
    users = team.users
    return render_template('users.html', team=team, users=users)

@app.route('/d/u/<string:user_id>')
def show_calendar(user_id):
    user = User.query.get(user_id)
    moods = Mood.query.filter_by(user=user)
    return render_template('cal.html', user=user, moods=moods)

if __name__ == '__main__':
    app.run(debug=True)
