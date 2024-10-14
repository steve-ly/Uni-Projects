"""src > auth.py

Provides functions for authenticating users

Primary Contributors: 
 - Steven Ly [z5257127@ad.unsw.edu.au]
     - auth_register_v1()
     - auth_login_v1()
     - valid_email_check()
     - email_already_registered()
     - valid_password_check()
     - password_login()
     - valid_names()
     - handle_generator()


Minor Contributors:
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]
     - Bug fixes, improvements
         - handle_generator() (Commit 1ce40f37)

"""

import yagmail 
from src import consts
from src.error import InputError, AccessError
from datetime import datetime

from .generic_data import GenericData, GenericDataContainer

class PasswordRequest(GenericData):
    """Maps a reset code to an email
    """
    def __init__(self, email: str) -> None:
        """Create a session

        Args:
            email (str): email of user
        """
        super().__init__()
        self._email =email

        
        # Add to data
        state.s.password_requests.add(self)
    
    def get_email(self) -> str:
        """Returns email associated with this password request

        Returns:
            str: email
        """
        return self._email

class PasswordRequestContainer(GenericDataContainer):
    """Container for sessions
    """
    def get(self, get_id: int) -> PasswordRequest:
        return super().get(get_id)

    
    
from . import helpers

def email_already_registered(email):
    """ Checks database to see if the email has been registered
       
        Arguments:
            <email> (string) is the email that the user uses to register
        Exceptions:
            <InputError> occurs when user cannot be found
        Returns:
            <bool>: True if email is found and False if exception is raised
    """
    try:
        state.s.users.get_by_email(email)
        return True
    except:
        return False

def valid_password_check(password):
    """Checks if users password is greater than 6
       
        Arguments:
            <password> (string) is the password the user uses to register 
        Returns:
            <bool>: True if password input is greater than 6 characters and False if less
    """

    return len(password) >= consts.PASSWORD_MIN_LEN

def valid_names(name): 
    """Checks name inputted for correct format
       
        Arguments:
            <name> (string) either the first or last name the user registers with 
        Returns:
            <bool>: Whether name is between 1 or 50 characters
    """
    return consts.NAME_MIN_LEN <= len(name) <= consts.NAME_MAX_LEN

@helpers.save_data
def auth_register_v1(email: str, password, name_first, name_last):
    """Creates an account and logs them in for user regisetering and append arguments to database
       
        Arguments:
            <email> (string) the email the user is using to register with
            <password> (string) the password the user is using to register with
            <name_first> (string) the name_first the user is using to register with
            <name_last> (string) the name_last the user is using to register with
        Exceptions:
            <InputError> - Returns an input error if the previous functions return a certain bool value
        Returns:
            <auth_user_id> (dictionary containing int value) is returned if no InputError is raised
    """
    # Make email all lowercase
    email = email.lower()
    
    if not helpers.is_email_valid(email):
        raise InputError(description="Email entered is not a valid email")
    elif email_already_registered(email):
        raise InputError(description="Email address is already being used by another user")
    elif not valid_password_check(password):
        raise InputError(description=f"Password is too short (min {consts.PASSWORD_MIN_LEN} characters)")
    elif not valid_names(name_first):
        raise InputError(description=f"First name ({len(name_first)} characters) "
                         f"must be between {consts.NAME_MIN_LEN} and {consts.NAME_MIN_LEN} characters")
    elif not valid_names(name_last):
        raise InputError(description=f"Last name ({len(name_last)} characters) "
                         f"must be between {consts.NAME_MIN_LEN} and {consts.NAME_MIN_LEN} characters")
    
    new_user = user.User(email, password, name_first, name_last)
    # If new user is the only user
    if len(state.s.users) == 1:
        new_user.set_admin(True)

    # Create new session and return the token for it
    sesh = session.Session(new_user.get_id())
    
    # Trigger a bot even for a user registering
    bots.on_user_register(new_user.get_id())
    
    return {"token" : sesh.get_as_token(), "auth_user_id" : new_user.get_id()}

@helpers.save_data
def auth_login_v1(email, password):
    """Returns the auth_user_id and token for user logging in
       
        Arguments:
            <email> (string) the email the user is using to register with
            <password> (string) the password the user is using to register with
        Exceptions:
            <InputError> Email or password are incorrect
        Returns:
            <auth_user_id> (dictionary containing int value) is returned if no InputError is raised
    """
    # Make email all lowercase
    email = email.lower()
    
    if not helpers.is_email_valid(email):
        raise InputError(description="Email entered is not a valid email")

    user = state.s.users.get_by_email(email)
    
    if not email_already_registered(email):
        raise InputError(description="Email entered does not belong to a user")
    
    if not user.check_password(password):
        raise InputError(description="Incorrect password")
    
    auth_user_id = user.get_id()
    # Create session and token
    sesh = session.Session(auth_user_id)
    return {"token" : sesh.get_as_token(), "auth_user_id" : auth_user_id}




def auth_logout_v1(token):
    """Logs out the user's current session

    Args:
        token (str): JWT token
    Exceptions:
        <AccessError> For invalid token
    Returns:
        bool: success
    """
    try:
        # Get session associated with this token
        sesh = session.get_session_by_token(token)
        # Remove the session
        state.s.sessions.remove(sesh.get_id())
        ret = True
    except:
        raise AccessError(description="Token is invalid: maybe you're already logged out?") from None

    return {"is_success": ret}


@helpers.save_data
def auth_password_reset_request(email):
    """Sends reset code to user's email to reset password

    Args:
        email (str): email of password being resetted

    Returns:
        
    """
    if (not email_already_registered(email)) or (not helpers.is_email_valid(email)):
        return {}        
    else:
        #remove any duplicated
        to_remove = 0
        for req in state.s.password_requests._contained.keys():
            dup_email = state.s.password_requests.get(req)
            if dup_email.get_email() == email:
                to_remove = req
        
        if to_remove != 0:
            state.s.password_requests.remove(to_remove)

        pwd_req = PasswordRequest(email)
        code = pwd_req.get_id()
        payload = f"This is the code to reset your Dreams account password: {code}"
        yag = yagmail.SMTP(user=consts.DREAMS_RESET_PASS_EMAIL, password= consts.PASSWORD_TO_DREAMS_RESET_ACCOUNT)
        #sending the email
        yag.send(to= email, subject='Dreams Account Reset Password Code', contents=payload)
    return {}

@helpers.save_data
def auth_password_reset_reset(reset_code, new_password):
    """Reset password to new password

    Args:
        reset_code (int): the code the user inputs in order to reset password
        new_password (str): A new unhased password string that the user wishes to change their password to 
    Returns:
        
    """
    
    if not valid_password_check(new_password):
        raise InputError(description=f"Password is too short (min {consts.PASSWORD_MIN_LEN} characters)")
    
    pwd_req = state.s.password_requests.get(reset_code)

    user = state.s.users.get_by_email(pwd_req.get_email())
    user.set_password(new_password)
    state.s.password_requests.remove(reset_code)
    return {}

from . import state
from . import user, session, bots
