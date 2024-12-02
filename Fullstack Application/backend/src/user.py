from flask import request, Blueprint, jsonify
import jwt
import datetime
import bcrypt 
from helpers import email_checker, response, skills_string_to_int, skills_int_to_string
from tokens import conference_id_from_token, user_from_token, username_from_token, token_required, requires_management, requires_organiser, is_management_or_organiser
from models import DB, MA,                         \
                   Users, UsersSchema,             \
                   Conferences, ConferencesSchema, \
                   Volunteers, VolunteersSchema,   \
                   Organisers, OrganisersSchema,   \
                   InvalidedTokens, InvalidedTokensSchema, Feedback  

user = Blueprint('user',__name__)
SECRET_KEY='IJH2sdU29#dD83901ASkt*x2hdjk!a%B^3*'
SALT = '$2b$12$4ooRr21Q28sCvY1I.xpU9u'.encode('utf-8')

# POST LogIn(str user, str password)# -> return token if 200 status code, return 403 status code if wrong login detail
@user.route('/LogIn', methods=['POST'])
def LogIn():    
    """
    Logs in a user 
 
    Args: 
        username (string (100)) [JSON BODY]: The new name of the users conference
        password (datetime)     [JSON BODY]: The new start date/time of the users conference
         
    Response:
        200: Returns the token of the user
        400: Input username or password is incorrect
    """    
    username = request.json['username']
    password = request.json['password']
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, SALT)
    password = password.decode('utf-8')
    
    # Check username in database
    user = Users.query.filter_by(username=username).first()
    
    # Return 400 if username doesn't exist
    if user is None:
        return {'token': -1}, 400
        
    # Return 400 if password is incorrect
    if user.password != password:
        return {'token': -1}, 400
    
    perms = 'organiser'
    user_id = user.id
    v = Volunteers.query.filter_by(user_id=user_id).first()
    if(v):
        if v.manager:
            perms = 'manager'
        else:
            perms = 'volunteer'
    
    # encode a token
    token = jwt.encode({'username':user.username, 'permissions': perms, 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60)}, SECRET_KEY, "HS256")
    return {'token': token}, 200

@user.route('/CreateOrganiser', methods=['POST']) 
def CreateOrganiser():
    """
    Edits the details of a given user
 
    Args: 
        first_name (string (100)) [JSON BODY]: The new first name of the user
        last_name  (string (100)) [JSON BODY]: The new last name of the user
        username   (string (100)) [JSON BODY]: The new username of the user
        password   (string (100)) [JSON BODY]: The new password of the user
        email      (string (100)) [JSON BODY]: The new email of the user which is regex checked
        [optional] token (int)         [HEADER]: The token of an organiser if the account is being created by another organiser
    
    Response:
        200: Successfully created, token of signed up user is returned
        400: Conference doesn't exist
             Requested field is invalid or already in use
    """     
    first_name    = request.json['first_name']
    last_name     = request.json['last_name']
    username      = request.json['username']
    password = request.json['password']
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, SALT)
    password = password.decode('utf-8')
    email         = request.json['email']
    conference_id = None
    
    try:
        token = request.json['creator_token']
        # do things
        user = Users.query.filter_by(username=username_from_token(token)['username']).first()
        organiser=DB.session.query(Users, Organisers).select_from(Organisers).join(Users).filter(Organisers.user_id==user.id).first()
        conference_id=organiser[1].conference_id
    except:
        conference_id = None

    if not email_checker(email):
        return {'message':'Email is invalid'}, 400
    if Users.query.filter_by(email=email).first():
        return {'message':'Email already in use'}, 400
    if Users.query.filter_by(username=username).first():
        return {'message':'Username already in use'}, 400

    user = Users(first_name, last_name, username, password, email)
    DB.session.add(user)
    DB.session.flush()

    organiser = Organisers(user.id, conference_id)
    DB.session.add(organiser)
    DB.session.commit()

    # encode a token
    token = jwt.encode({'username':user.username, 'permissions': 'organiser', 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60)}, SECRET_KEY, "HS256")
    return {'token': token}, 200    

@user.route('/CreateVolunteer', methods=['POST'])
def CreateVolunteer():
    """
    Edits the details of a given user
 
    Args: 
        first_name (string (100)) [JSON BODY]: The new first name of the user
        last_name  (string (100)) [JSON BODY]: The new last name of the user
        username   (string (100)) [JSON BODY]: The new username of the user
        password   (string (100)) [JSON BODY]: The new password of the user
        email      (string (100)) [JSON BODY]: The new email of the user which is regex checked
        availability (string in form ("(datetime), (datetime)"))                 [JSON BODY]: List of the users available days
        skills       (string in form ("Skill (X), Skill (X)") where X=1,2,3,...) [JSON BODY]: List of the users skills
        preferences  (string in form ("Pref (Y), Pref (Y)") where Y=A,B,C,...)   [JSON BODY]: List of the users preferences
        [optional] token [HEADER]: The token of an organiser if the account is being created by organiser
         
    Response:
        200: Successfully changed
        400: Conference doesn't exist
             Requested field is invalid or already in use
    """     
    first_name    = request.json['first_name']
    last_name     = request.json['last_name']
    username      = request.json['username']
    password = request.json['password']
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, SALT)
    password = password.decode('utf-8')
    email         = request.json['email']
    skills        = skills_string_to_int(request.json['skills'])
    preferences   = request.json['preferences']
    availability  = request.json['availability']
    conference_id = None

    # For organiser creating a volunteer
    try:
        token = request.json['token']
        # do things
        user = Users.query.filter_by(username=username_from_token(token)['username']).first()
        organiser=DB.session.query(Users, Organisers).select_from(Organisers).join(Users).filter(Organisers.user_id==user.id).first()
        conference_id=organiser[1].conference_id
    except:
        conference_id = None
 
    # Creating a manager or regular volunteer
    try:
        manager = request.json['manager']
    except:
        manager = False 
        
    if not email_checker(email):
        return {'message':'Email is invalid'}, 400
    if Users.query.filter_by(email=email).first():
        return {'message':'Email already in use'}, 400
    if Users.query.filter_by(username=username).first():
        return {'message':'Username already in use'}, 400

    user = Users(first_name, last_name, username, password, email)
    DB.session.add(user)
    DB.session.flush()

    volunteer = Volunteers(user.id, conference_id, skills, preferences, availability, manager)
    DB.session.add(volunteer)
    DB.session.commit()
    
    # encode a token
    token = jwt.encode({'username':user.username, 'permissions': 'volunteer', 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60)}, SECRET_KEY, "HS256")
    return {'token': token}, 200    

#POST LogOut(str token) -> return 200 or 403 \Mia to do backend\
@user.route('/LogOut', methods=['POST'])
@token_required # ensures user has logged in already by validating token
def LogOut():
    """
    Logs out a user and invalidates their token
 
    Args: 
        token [HEADER]: The token of the user performing the action
         
    Response:
        200: The user is logged out
        400: Invalidated token
    """    
    token = request.headers['token']
    invalidated_token = InvalidedTokens(token)
    DB.session.add(invalidated_token)
    DB.session.commit()

    return {'message': 'User logged out!'}, 200

# TODO: deleted createorganiser, volunteer, login

#in order for this to be used by an organiser to edit antoher user, include 'target_username'
@user.route('/EditUserDetails', methods=['PUT']) 
@token_required
@requires_management
def EditUserDetails():
    """
    Edits the details of a given user
 
    Args: 
        [optional] first_name (string (100)) [JSON BODY]: The new first name of the user
        [optional] last_name  (string (100)) [JSON BODY]: The new last name of the user
        [optional] username   (string (100)) [JSON BODY]: The new username of the user
        [optional] password   (string (100)) [JSON BODY]: The new password of the user
        [optional] email      (string (100)) [JSON BODY]: The new email of the user which is regex checked
        [optional] availability (string in form ("(datetime), (datetime)")) [JSON BODY]: List of the users available days
        [optional] skills       (string in form ("Skill (X), Skill (X)") where X=1,2,3,...) [JSON BODY]: List of the users skills
        [optional] preferences  (string in form ("Pref (Y), Pref (Y)") where Y=A,B,C,...)    [JSON BODY]: List of the users preferences
        token [HEADER]:       Requires the token of a logged in user
        [optional] target_username (string(100)) [JSON BODY]: An organiser may edit the details of a volunteer
        [optional] manager (boolean) [JSON BODY]: The new role of volunteer
         
    Response:
        200: Successfully changed
        400: Conference doesn't exist
             Requested field is invalid or already in use
             Token is not valid
        403: Token doesn't belong to an organiser when trying to edit another users details
    """    
    token = request.headers['token']

    #this is how im doing auth checks atm 
    #curr_user = user_from_token(token)
    #organiser = Organisers.query.filter_by(user_id=curr_user.id).first()
    target_username = request.json.get('target_username')
    organiser = is_management_or_organiser()

    if organiser and target_username:
        user = Users.query.filter_by(username=target_username).first()
    else:
        user = Users.query.filter_by(username=username_from_token(token)['username']).first()
    
    first_name = request.json.get('first_name')
    if first_name:
        user.first_name = first_name

    last_name = request.json.get('last_name')
    if last_name:
        user.last_name = last_name

    username = request.json.get('username')
    if username:
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user.id:
            return {'response':'Username already in use'}, 400
        user.username = username

    password = request.json['password']
    if password:
        password = password.encode('utf-8')
        password = bcrypt.hashpw(password, SALT)
        password = password.decode('utf-8')
        user.password = password #maybe hash

    email = request.json.get('email')
    if email:
        if not email_checker(email):
            return {'response':'Email is invalid'}, 400
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user and existing_user.id != user.id:
            return {'response':'Email already in use'}, 400
        user.email = email


    availability = request.json.get('availability')
    if availability:
        user.availability = availability

    manager = request.json.get('manager')
    volunteer = Volunteers.query.filter_by(user_id=user.id).first()
    if volunteer:
        skills = request.json.get('skills')
        
        if skills:
            volunteer.skills = skills_string_to_int(skills)
            
        preferences = request.json.get('preferences')
        
        if preferences:
            volunteer.preferences = preferences

        if manager is not None:
                volunteer.manager = manager
    

    
    DB.session.commit()

    return {'message':'Profile updated'}, 200


#GET getUserDetails gets a user details of the given user
# id, username, email, password, conference
@user.route('/GetUserDetails', methods=['GET'])
@token_required # ensures user has logged in already by validating token
def GetUserDetails():
    """
    Returns the details of the calling user
 
    Args: 
       token [HEADER]: The token of an organiser if the account is being created by organiser
         
    Response:
        200: Dictionary with fields
            first_name (string (100)) 
            conference_id (int)
            last_name  (string (100)) 
            username   (string (100))
            role       "Volunteer" or "Volunteer Manager"  or "Organiser"
            password   (string (100)) 
            email      (string (100)) 
            availability (string in form ("(datetime), (datetime)"))               
            skills       (string in form ("Skill (X), Skill (X)") where X=1,2,3,...) 
            preferences  (string in form ("Pref (Y), Pref (Y)") where Y=A,B,C,...)  
        400: Token invalidated
    """ 
    # Gets username
    username = username_from_token(request.headers['token'])['username']
  
    # get user details and the conferences they're members of
    user = Users.query.filter_by(username=username).first()    
    
    details={'user_id': user.id, 'username': user.username, 'password': '', 'email': user.email, 'firstName':user.first_name, 'lastName':user.last_name}
    
    volunteer = Volunteers.query.filter_by(user_id=user.id).first()
    if volunteer:
        details['conference_id']=volunteer.conference_id
        details['skills']       =skills_int_to_string(volunteer.skills)
        details['preferences']  =volunteer.preferences
        details['availability'] =volunteer.availability
        if volunteer.manager:
            details['role'] = "Volunteer Manager"
        else:
            details['role'] = "Volunteer"
        feedback_entries = Feedback.query.all()
        feedback_entries.sort(key=lambda x: x.score, reverse=True)
        if feedback_entries:
            top_three_ids = [feedback.user_id for feedback in feedback_entries[:3]]
            if volunteer and volunteer.user_id in top_three_ids:
                # Determine the rank and append special_feature string
                rank = top_three_ids.index(volunteer.user_id) + 1
                if rank == 1:
                    details['special_feature'] = "First"
                elif rank == 2:
                    details['special_feature'] = "Second"
                elif rank == 3:
                    details['special_feature'] = "Third"
        else:
            # Ensure the key exists even if not in top three
            details['special_feature'] = ""    
            
            
    organiser = Organisers.query.filter_by(user_id=user.id).first()
    if organiser:
        details['conference_id']=organiser.conference_id
        details['role'] = "Organiser"
    
    return details, 200    

@user.route('/GetVolunteerData', methods=['GET'])
@token_required
def GetVolunteerData():
    """
    Returns the details of the calling volunteer
 
    Args: 
       token [HEADER]: The token of the volunteer
         
    Response:
        200: Dictionary with fields
            availability (string in form ("(datetime), (datetime)"))               
            skills       (string in form ("Skill (X), Skill (X)") where X=1,2,3,...) 
            preferences  (string in form ("Pref (Y), Pref (Y)") where Y=A,B,C,...)  
        400: Token invalidated
             User is not a volunteer
    """     
    # Gets username
    username = username_from_token(request.headers['token'])['username']

    user = Users.query.filter_by(username=username).first()    
    
    volunteer = Volunteers.query.filter_by(user_id=user.id).first() 
    if volunteer:
        details={'skills': skills_int_to_string(volunteer.skills), 'preferences': volunteer.preferences, 'availability': volunteer.availability}
        return jsonify(details), 200
    
    return {'message': 'User not a volunteer'}, 400

@user.route('/GetSkillsAndPreferences', methods=['GET'])
def GetSkillsAndPreferences():
    """
    Returns the skills and preferences used 
         
    Response:
        200: Dictionary with fields
            skills       (string in form ("Skill (X), Skill (X)") where X=1,2,3,...) 
            preferences  (string in form ("Pref (Y), Pref (Y)") where Y=A,B,C,...)  
        400: Token invalidated
             User is not a volunteer
    """    
    return {'skills': ['Skill 1', 'Skill 2', 'Skill 3', 'Skill 4', 'Skill 5', 'Skill 6'], 'preferences':['Pref A', 'Pref B', 'Pref C', 'Pref D', 'Pref E', 'Pref F']}, 200


@user.route('/ToggleManager', methods=['POST'])
@token_required
@requires_organiser
def ToggleManager():
    """
    Toggles the status of a volunteer from volunteer to volunteer manager and vice versa
         
    Arg:
        user_id (int): Id of the user who's manager status is being flipped
         
    Response:
        200: Dictionary with fields
            skills       (string in form ("Skill (X), Skill (X)") where X=1,2,3,...) 
            preferences  (string in form ("Pref (Y), Pref (Y)") where Y=A,B,C,...)  
        400: Token invalidated
             User is not a volunteer
        403: Caller is not an organiser
    """    
    user_id = request.json.get('user_id')
    volunteer = Volunteers.query.filter_by(user_id=user_id).first()

    if volunteer:    
        volunteer.manager = not volunteer.manager
        DB.session.commit()
        return response('OK', 200)
    else:
        return {'message': 'User is not a volunteer'}, 400
