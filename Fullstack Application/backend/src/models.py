from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from helpers import serialise_datetime, skills_int_to_string

DB = SQLAlchemy()
MA = Marshmallow(DB) # Mia o do --> do we want this module, is it being used

# Users
class Users(DB.Model):
    id         = DB.Column(DB.Integer, primary_key=True, unique=True)
    first_name = DB.Column(DB.String(100))
    last_name  = DB.Column(DB.String(100))
    username   = DB.Column(DB.String(100), unique=True)
    password   = DB.Column(DB.String(100))
    email      = DB.Column(DB.String(100), unique=True)

    def __init__(self, first_name, last_name, username, password, email):
        self.first_name = first_name
        self.last_name  = last_name
        self.username   = username
        self.password   = password
        self.email      = email

class UsersSchema(MA.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email')

# Volunteer
class Volunteers(DB.Model):
    user_id       = DB.Column(DB.Integer, DB.ForeignKey('users.id'), primary_key=True)
    conference_id = DB.Column(DB.Integer, DB.ForeignKey('conferences.id'))
    skills        = DB.Column(DB.Integer)
    preferences   = DB.Column(DB.String(100))
    availability  = DB.Column(DB.String(200))
    manager       = DB.Column(DB.Boolean)
    manager_score = DB.Column(DB.Integer)
    attendee_score= DB.Column(DB.Integer)

    def __init__(self, user_id, conference_id, skills, preferences, availability, manager):
        self.user_id       = user_id
        self.conference_id = conference_id
        self.skills        = skills
        self.preferences   = preferences
        self.availability  = availability
        self.manager       = manager
        self.manager_score = 0
        self.attendee_score= 0

class VolunteersSchema(MA.Schema):
    class Meta:
        fields = ('user_id', 'conference_id', 'skills', 'preferences', 'password', 'conference_id', 'manager')

# Organiser
class Organisers(DB.Model):
    user_id       = DB.Column(DB.Integer, DB.ForeignKey('users.id'), primary_key=True)
    conference_id = DB.Column(DB.Integer, DB.ForeignKey('conferences.id'))

    def __init__(self, user_id, conference_id):
        self.user_id       = user_id
        self.conference_id = conference_id

class OrganisersSchema(MA.Schema):
    class Meta:
        fields = ('user_id', 'conference_id')

# Conference
class Conferences(DB.Model):
    id         = DB.Column(DB.Integer, primary_key=True)
    name       = DB.Column(DB.String(100))
    start_date = DB.Column(DB.DateTime)
    end_date = DB.Column(DB.DateTime)

    def __init__(self, name,start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

class ConferencesSchema(MA.Schema):
    class Meta:
        fields = ('id', 'name','start_date','end_date')

# Tokens
class InvalidedTokens(DB.Model):
    token = DB.Column(DB.String(200), primary_key=True)

    def __init__(self, token):
        self.token = token

class InvalidedTokensSchema(MA.Schema):
    class Meta:
        fields = ('token', 'nothing why have i made this?')

# Tasks
class Tasks(DB.Model):
    id                 = DB.Column(DB.Integer, primary_key=True, unique=True)
    conference_id      = DB.Column(DB.Integer, DB.ForeignKey('conferences.id'))
    name               = DB.Column(DB.String(64))
    description        = DB.Column(DB.String(256))
    completed          = DB.Column(DB.Boolean)
    start_time         = DB.Column(DB.DateTime)
    end_time           = DB.Column(DB.DateTime)
    skills_recommended = DB.Column(DB.Integer)

    def __init__(self, conference_id, name, description, start_time, end_time, skills_recommended):
        self.conference_id      = conference_id
        self.name               = name
        self.description        = description
        self.completed          = False
        self.start_time         = start_time
        self.end_time           = end_time
        self.skills_recommended = skills_recommended

    @property
    def serialize(self):
        return {
            "id":self.id,
            "conference_id":self.conference_id,
            "name":self.name,
            "description":self.description,
            "completed":self.completed,
            "start_time":serialise_datetime(self.start_time),
            "end_time":serialise_datetime(self.end_time),
            "skills_recommended":skills_int_to_string(self.skills_recommended)
        }

class TasksSchema(MA.Schema):
    class Meta:
        fields = ('id', 'conference_id', 'name', 'description', 'start_time', 'end_time', 'skills_recommended')
# Tasks: task_id, event_id, completion_status (int) [0 incomplete] [1 complete], start_time, end_time, skills_recommended
# Members_of_tasks: task_id, volunteer_id, approval_status (int) [0 incomplete] [1 complete]

# Members of tasks relates a task and
class MembersOfTasks(DB.Model):
    user_id  = DB.Column(DB.Integer, DB.ForeignKey('users.id'), primary_key=True)
    task_id  = DB.Column(DB.Integer, DB.ForeignKey('tasks.id'), primary_key=True)
    approved = DB.Column(DB.Boolean)

    def __init__(self, user_id, task_id, approved):
        self.user_id  = user_id
        self.task_id  = task_id
        self.approved = approved

class MembersOfTasksSchema(MA.Schema):
    class Meta:
        fields = ('user_id', 'task_id', 'approved')

#Messages
class MessageGroup(DB.Model):
    __tablename__ = 'messagegroup'
    id                 = DB.Column(DB.Integer, primary_key=True, unique=True)
    conference_id      = DB.Column(DB.Integer, DB.ForeignKey('conferences.id'))
    task_id      = DB.Column(DB.Integer)
    owner_id           = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    name               = DB.Column(DB.String(64))

    def __init__(self, conference_id, task_id, owner_id, name):
        self.conference_id = conference_id
        self.task_id = task_id
        self.owner_id = owner_id
        self.name = name


class MessageGroupSchema(MA.Schema):
    class Meta:
        fields = ('id', 'conference_id', 'task_id', 'owner_id', 'name')

class MembersOfMessageGroup(DB.Model):
    user_id  = DB.Column(DB.Integer, DB.ForeignKey('users.id'), primary_key=True)
    messagegroup_id  = DB.Column(DB.Integer, DB.ForeignKey('messagegroup.id'), primary_key=True)

    def __init__(self, user_id, messagegroup_id):
        self.user_id  = user_id
        self.messagegroup_id  = messagegroup_id

class MembersOfMessageGroupSchema(MA.Schema):
    class Meta:
        fields = ('user_id', 'messagegroup_id')

class Message(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    group_id = DB.Column(DB.Integer, DB.ForeignKey('messagegroup.id'))
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    content = DB.Column(DB.String(128))
    timestamp = DB.Column(DB.DateTime)
    def __init__(self, group_id, user_id, content, timestamp):
        self.group_id  = group_id
        self.user_id  = user_id
        self.content = content
        self.timestamp = timestamp

class MessageSchema(MA.Schema):
    class Meta:
        fields = ('id', 'group_id','user_id','content','timestamp')

# Feedback
class Feedback(DB.Model):
    id       = DB.Column(DB.Integer, primary_key=True, unique=True)
    user_id  = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    name     = DB.Column(DB.String(100))
    feedback = DB.Column(DB.String(100))
    score    = DB.Column(DB.Integer)
    anon     = DB.Column(DB.Boolean)

    def __init__(self, user_id, name, feedback, score, anon):
        self.user_id  = user_id
        self.name     = name
        self.feedback = feedback
        self.score    = score
        self.anon     = anon

class FeedbackSchema(MA.Schema):
    class Meta:
        fields = ('id', 'user_id', 'name', 'feedback', 'score', 'anon')

class Attendance(DB.Model):
    id            = DB.Column(DB.Integer, primary_key=True, unique=True)
    task_id       = DB.Column(DB.Integer, DB.ForeignKey('tasks.id'))
    user_id       = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    username      = DB.Column(DB.String(100))
    conf_id       = DB.Column(DB.Integer, DB.ForeignKey('conferences.id'))
    date_in          = DB.Column(DB.DateTime)
    date_out          = DB.Column(DB.DateTime, default=None)
    hours         = DB.Column(DB.Integer,default=0)
    validated     = DB.Column(DB.Boolean, default=False)


    def __init__(self, task_id, user_id, username, conf_id, date_in ):
        self.task_id = task_id
        self.user_id = user_id
        self.username = username
        self.conf_id = conf_id
        self.date_in = date_in

        
class AttendanceSchema(MA.Schema):
    class Meta:
        fields = ('id','task_id', 'user_id','username','conf_id', 'date_in','date_out' ,'hours', 'validated')


class Voted(DB.Model):
    user_id  = DB.Column(DB.Integer, DB.ForeignKey('users.id'), primary_key=True)
    votee_id  = DB.Column(DB.Integer, DB.ForeignKey('users.id'), primary_key=True)
    score = DB.Column(DB.Integer)
    conf_id = DB.Column(DB.Integer, DB.ForeignKey('conferences.id'), primary_key=True)

    def __init__(self, user_id, votee_id, score, conf_id):
        self.user_id  = user_id
        self.votee_id  = votee_id
        self.score = score
        self.conf_id = conf_id

class VotedSchema(MA.Schema):
    class Meta:
        fields = ('user_id', 'votee_id', 'score', 'conf_id')


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

conference_schema = ConferencesSchema()
conferences_schema = ConferencesSchema(many=True)

volunteer_schema = VolunteersSchema()
volunteers_schema = VolunteersSchema(many=True)

organiser_schema = OrganisersSchema()
organisers_schema = OrganisersSchema(many=True)

expiredtoken_schema = InvalidedTokensSchema()
expiredtokens_schema = InvalidedTokensSchema(many=True)

task_schema = InvalidedTokensSchema()
tasks_schema = InvalidedTokensSchema(many=True)

feedback_schema = FeedbackSchema()
feedbacks_schema = FeedbackSchema(many=True)

attendance_schema = AttendanceSchema()
attendance_schema = AttendanceSchema(many=True)