from flask import request, Blueprint, jsonify
import jwt
import datetime
from helpers import response, create_ical_event, send_conference_schedule_email
from tokens import conference_id_from_token, user_from_token, username_from_token, token_required, requires_management, requires_organiser, is_management_or_organiser, is_organiser
from models import DB, MA,                         \
                   Users, Feedback,             \
                   Conferences, Tasks, \
                   Volunteers, MembersOfTasks,   \
                   Organisers, OrganisersSchema,   \
                   MessageGroup, MessageGroupSchema, MembersOfMessageGroup, \
                   MembersOfMessageGroupSchema, Message, MessageSchema, \
                   user_schema, conferences_schema

conference = Blueprint('conference',__name__)

# Create conference [name]
@conference.route('/CreateConference', methods=['POST'])
@token_required # TODO: change this to organiser token
@requires_organiser
def add_conference():
    """
    Makes a new conference and makes the creator an organiser of this conference
    Creates a new conference message group that will share the same name as the conference
 
    Args: 
        name (string) [JSON BODY]:         The name of the conference, non-unique
        start_date (datetime) [JSON BODY]: The start date and time of the conference
        end_date (datetime) [JSON BODY]:   The end date and time of the conference
        token [HEADER]:                    Requires the token of a logged in organiser
 
    Response:
        200: Successful creation of new conference
        400: The token is invalid
        403: The token doesn't belong to an organiser
    """

    name = request.json['name']
    token = request.headers['token']
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    user = Users.query.filter_by(username=username_from_token(token)['username']).first()    
    organiser = Organisers.query.filter_by(user_id=user.id).first()
    if organiser is None:
        return jsonify({"error": "User is not an organiser"}), 403
    try:
        start_date = request['start_date']
        end_date = request['end_date']
    except:
        start_date = None
        end_date = None
    conf = Conferences(name, start_date, end_date)
    DB.session.add(conf)
    DB.session.commit()
    
    organiser.conference_id = conf.id
    DB.session.commit()
    #create a conference group chat:
    message_group = MessageGroup(conf.id, -1, user.id, name)
    DB.session.add(message_group)
    DB.session.commit()
    add_owner = MembersOfMessageGroup(user.id,message_group.id)
    DB.session.add(add_owner)
    DB.session.commit()
    return user_schema.jsonify(conf), 200

@conference.route('/JoinConference', methods=['POST'])
@token_required
def JoinConference():
    """
    Signs a user up as apart of the selected conference.
    Will also add user to the conference group chat
 
    Args : 
        conference_id (int) [JSON BODY]: The id of the desired conference
        token [HEADER]:                  Requires the token of a logged in organiser or volunteer
 
    Response:
        200: Successful joining of conference
        400: The token is invalid
    """
    token = request.headers['token']
    user = Users.query.filter_by(username=username_from_token(token)['username']).first()
    conference_id = request.json['conference_id']

    volunteer = Volunteers.query.filter_by(user_id=user.id).first() 
    if volunteer:
        volunteer.conference_id = conference_id
    else:
        organiser = Organisers.query.filter_by(user_id=user.id).first() 
        organiser.conference_id = conference_id

    DB.session.commit()
    #add a user to conference chat:
    conference_to_join = Conferences.query.filter_by(id=conference_id).first()
    messagegroup = MessageGroup.query.filter_by(name=conference_to_join.name,conference_id=conference_id).first()
    new_member = MembersOfMessageGroup(user.id,messagegroup.id)
    DB.session.add(new_member)
    DB.session.commit()
    return response('OK', 200)

@conference.route('/LeaveConference', methods=['POST'])
@token_required
def LeaveConference():
    """
    Removes a user from a conference, unassigning all their tasks, removing message groups and their feedback associated with it
 
    Args: 
        token [HEADER]: The valid token of the logged in user
 
    Response:
        200: Successful removal from conference
        400: The token is invalid
    """
    token = request.headers['token']
    user = Users.query.filter_by(username=username_from_token(token)['username']).first()
    user.conference_id = None
    
    # Delete volunteer or organiser profile
    vol = Volunteers.query.filter_by(user_id=user.id).first()
    if vol:
        vol.conference_id = None
    else:
        org = Organisers.query.filter_by(user_id=user.id).first()
        org.conference_id = None
    
    # Leave all chats
    MembersOfMessageGroup.query.filter_by(user_id=user.id).delete()

    # Delete all feedback
    Feedback.query.filter_by(user_id=user.id).delete()
    
    # Delete all joined/requested tasks
    MembersOfTasks.query.filter_by(user_id=user.id).delete()

    DB.session.commit()
    return response('OK', 200)
    
@conference.route('/GetAllConferences', methods=['GET'])
@token_required # ensures user has logged in already by validating token
def GetAllConferences():
    """
    Returns a list of all the conferences
 
    Args: 
        token [HEADER]: Requires the token of a logged in user
 
    Response:
        200: A list of dictionaries containing {'name', 'start_date', 'end_date'}
        400: The token is invalid
    """
    all = Conferences.query.all()
    results = conferences_schema.dump(all)
    return jsonify(results), 200

#GET GetConferenceDetails gets details of conference in dict 
# {'conference_id': id, 'name':conference.name, 'volunteers':volunteers, 'organisers':organisers})
# conference_id: INT
# name: STRING
# volunteers: List of dictionaries {'username': STRING, 'id': INT}
# organisers: List of dictionaries {'username': STRING, 'id': INT}
@conference.route('/GetConferenceDetails', methods=['GET'])
@token_required # ensures user has logged in already by validating token#TODO: consider permissions for these calls 
def GetConferenceDetails():
    """
    Returns the details of a given conference and who is apart of it
 
    Args: 
        token [HEADER]: Requires the token of a logged in organiser
         
    Response:
        200: A dictionary containing {'conference_id': id, 'name':conference.name, 'volunteers':volunteers, 'organisers':organisers}
        400: Conference doesn't exist
             Token is invalidated
        403: Token doesn't belong to an organiser
    """
    conference_id = conference_id_from_token(request.headers['token'])
    
    # Get conference details
    conference = Conferences.query.filter_by(id=conference_id).first()
    
    # Return 400 if username doesn't exist
    if conference is None:
        return {'message': 'Conference doesn\'t exist'}, 400
         
    # Get volunteer ids as list
    results=DB.session.query(Users, Volunteers).select_from(Volunteers).join(Users).filter(Volunteers.conference_id==conference_id)
    volunteers = [{'username':v[0].username, 'id':v[0].id} for v in results]
    
    # Get organiser ids as list
    results=DB.session.query(Users, Organisers).select_from(Organisers).join(Users).filter(Organisers.conference_id==conference_id)
    organisers = [{'username':o[0].username, 'id':o[0].id} for o in results]
       
    return jsonify({'conference_id': conference_id, 'name':conference.name, 'volunteers':volunteers, 'organisers':organisers, 'start_date': conference.start_date,'end_date': conference.end_date}), 200

@conference.route('/EditConferenceDetails', methods=['PUT'])
@token_required # ensures user has logged in already by validating token
@requires_organiser
def EditConferenceDetails():
    """
    Edits the details of a given conference
 
    Args: 
        [optional] name (string (100))   [JSON BODY]: The new name of the users conference
        [optional] start_date (datetime) [JSON BODY]: The new start date/time of the users conference
        [optional] end_date (datetime)   [JSON BODY]: The new end date/time of the users conference
        token [HEADER]:                  Requires the token of a logged in organiser
         
    Response:
        200: A dictionary containing {'conference_id': id, 'name':conference.name, 'volunteers':volunteers, 'organisers':organisers}
        400: Conference doesn't exist
             Token is not valid
        403: Token doesn't belong to organiser
    """    
    conference_id = conference_id_from_token(request.headers['token'])
    
    conference = Conferences.query.filter_by(id=conference_id).first()
    
    name = request.json.get('name')
    if name:
        conference.name = name

    start_date = request.json.get('start_date')
    if start_date:
        conference.start_date = start_date

    end_date = request.json.get('end_date')
    if end_date:
        conference.end_date = end_date
    
    DB.session.commit()
    return {'message':'conference updated'}, 200





@conference.route('/ShareConferenceSchedule', methods=['POST'])
@token_required
@requires_organiser
def ShareConferenceSchedule():
    """
    Notifies user by email a copy of the conference schedule in ics form
 
    Args: 
        token [HEADER]:                  Requires the token of a logged in organiser
         
    Response:
        200: Conference schedule shared successfully.
        400: Conference doesn't exist
             Token is not valid
        403: Token doesn't belong to organiser
    """  
    conference_id = conference_id_from_token(request.headers['token'])
    tasks = Tasks.query.filter_by(conference_id=conference_id).all()
    event_schedule = create_ical_event(tasks)
    volunteer_ids = Volunteers.query.filter_by(conference_id=conference_id).all()
    volunteer_ids = [v.user_id for v in volunteer_ids]
    
    organiser_ids = Organisers.query.filter_by(conference_id=conference_id).all()
    organiser_ids = [o.user_id for o in organiser_ids]

    all_user_ids = list(volunteer_ids + organiser_ids)

    users = Users.query.filter(Users.id.in_(all_user_ids)).all()
    emails = [user.email for user in users]
    send_conference_schedule_email(emails,event_schedule)

    return jsonify({'message': 'Conference schedule shared successfully.'}), 200