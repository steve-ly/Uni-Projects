from functools import wraps
import datetime
import jwt
from flask import request, jsonify
from models import DB,          \
                   Users,       \
                   Conferences, \
                   Volunteers , \
                   Organisers , \
                   InvalidedTokens
SECRET_KEY='IJH2sdU29#dD83901ASkt*x2hdjk!a%B^3*'


"""
Wrapper function that checks for and validates tokens. Used to wrap all functions that require a logged in user
Response:
    403: Token couldn't be decoded
    400: No token is provided
        Token is invalidated
"""
def token_required(route):
   @wraps(route)
   def token_authenticator(*args, **kwargs):
        token = None
       
        # Gets token from (json) request header if it exists
        if 'token' in request.headers:
           token = request.headers['token']
 
        # returns message if the token isn't in the request header
        if token is None:
           return jsonify({'message': 'Missing token'}), 400
             
        # fetches the token and decodes it
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # exception occurs if user from token has expired or otherwise
        except:
            return jsonify({'message': 'Invalid token, could not decode'}), 403
        
        # Checks if token is invalidated
        for t in InvalidedTokens.query.all():
            # Returns if token is invalidated as user logged out
            if t.token == token:
                return jsonify({'message': 'Token invalidated'}), 400
            
            # Removes any tokens which were invalidated which have since expired
            if decoded['exp'] < datetime.datetime.now().timestamp():
                    InvalidedTokens.query.filter_by(token=token).delete()
                    DB.session.commit()
        return route(*args, **kwargs)
   return token_authenticator


"""
Wrapper function that checks for and validates user is a managemer or organiser from their token. Used to wrap all functions that require a higher permission level
Response:
    Route
    403: Token not provided
        Token with insufficient permissions
"""
def requires_management(route):
    @wraps(route)
    def requires_man(*args, **kwargs):
        token = None
       
        # Gets token from (json) request header if it exists
        if 'token' in request.headers:
           token = request.headers['token']

        # returns message if the token isn't in the request header
        if token is None:
           return jsonify({'message': 'Missing token'}), 403

        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        permissions = decoded['permissions']
        
        if permissions == 'organiser' or permissions == 'manager':
            return route(*args, **kwargs)
        else:
            return {'message': 'Insufficient permission'}, 403
    return requires_man

"""
Helper function to check for and validate if a user is a managemer or organiser from their token
Response:
    True
    403: No token is provided
        Token with insufficient permissions
"""
def is_management_or_organiser(*args, **kwargs):
    token = None
       
    # Gets token from (json) request header if it exists
    if 'token' in request.headers:
        token = request.headers['token']

    # returns message if the token isn't in the request header
    if token is None:
       return jsonify({'message': 'Missing token'}), 403

    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    permissions = decoded['permissions']
        
    if permissions == 'organiser' or permissions == 'manager':
        return True
    else:
        return {'message': 'Insufficient permission'}, 403

"""
Wrapper function that checks for and validates user is an organiser from their token. Used to wrap all functions that require the highest permission level
Response:
    route
    403: 
        Token with insufficient permissions
"""
def requires_organiser(route):
    @wraps(route)
    def organiser(*args, **kwargs):
        token = request.headers['token']
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        permissions = decoded['permissions']
        if permissions != 'organiser':
            return {'message': 'Insufficient permission'}, 403
        return route(*args, **kwargs)
    return organiser

"""
Helper function to check for and validate if a user is an organiser from their token
Response:
    True
    400: No token is provided
    403: Token with insufficient permissions
"""
def is_organiser(*args, **kwargs):
        token = None
        
        # Gets token from (json) request header if it exists
        if 'token' in request.headers:
            token = request.headers['token']

        # returns message if the token isn't in the request header
        if token is None:
            return jsonify({'message': 'Missing token'}), 400
            
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        permissions = decoded['permissions']
        if permissions == 'organiser':
            return True
        else:
            return {'message': 'Insufficient permission'}, 403

"""
Returns the user object stored in the database which is correlated with a given token
"""
def user_from_token(token):
    return Users.query.filter_by(username=username_from_token(token)['username']).first()

"""
Returns the Volunteer object stored in the database which is correlated with a given token
"""
def volunteer_from_token(token):
    user = Users.query.filter_by(username=username_from_token(token)['username']).first()
    return Volunteers.query.filter_by(user_id=user.id).first()

"""
Returns the username from a given token
"""
def username_from_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

"""
Returns the conference id of the conference a user is in
"""
def conference_id_from_token(token):
    user = user_from_token(token)
    
    volunteer = Volunteers.query.filter_by(user_id=user.id).first() 
    if volunteer:
        conference_id = volunteer.conference_id
    else:
        organiser = Organisers.query.filter_by(user_id=user.id).first() 
        conference_id = organiser.conference_id
    
    return conference_id
