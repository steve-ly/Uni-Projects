"""
src > helpers.py

Helper functions for code that is used throughout multiple files, and doesn't 
really belong anywhere else

Authors:

"""

import inspect

from . import consts, config

def is_email_valid(email: str):
    """Checks email inputted for correct format
       
        Arguments:
            <email> (string) is the email that the user uses to login/register
        
        Returns:
            <bool>: True for valid email and false for invalid
    """
    
    # If regular expression search returns None, we didn't find anything

    return consts.EMAIL_REGEX.match(email) is not None

class EncodedString:
    """Contains a string that is encoded so that any tagged users will have
    their handles autoupdated whenever they are changed.
    """
    def __init__(self, message, quote_id=None):
        self._quote_id = quote_id
        self._encoded, self._tagged_users = self._encode(message)
    
    def _get_tag_alone(self, message):
        """Given a message sliced to the start of a tag (just after the @), will 
        return the tag by its self.
        Eg: "somehandle [rest of message]" will return "somehandle"

        Args:
            message (str): Message (sliced to start of tag)

        Returns:
            str: isloated tag
        """
        
        # Characters to split around
        slice_chars = consts.WHITESPACE_CHARS
        
        # Generate tags
        splits = [message.split(ch)[0] for ch in slice_chars]
        
        # Return shortest one (since handles can't have those chars in them)
        # From https://stackoverflow.com/a/7228951/6335363
        return min(splits, key=len)
    
    def _encode(self, message):
        """Encode message so that tags are preserved even if handles are changed
        
        Format:
            - Tagged handles are replaced by user IDs (eg: "@someuser" -> "@7864...")
            - Uses of the @ character where nobody is tagged are written using a
            double @ (eg: "@notauser" -> "@@notauser")
        This ensures that no data is lost when converting to or from the encoded 
        format


        Args:
            message (str): message to encode

        Returns: tuple
            str: encoded message
            set: user IDs that were tagged (without duplicates)
        """
        
        # Loop through each char, and append encoded message char by char (excluding
        # tags)
        # Note that we need to use a while loop since any time that the string needs
        # to be different from the original, we will need to jump the index of the 
        # current char ahead
        result = ""
        tagged_users = set()
        i = 0
        while (i < len(message)):
            # Default behaviour: not in a tag, just append the letter
            result += message[i]
            
            # If we've found the start of a possible tag (@ symbol)
            # Since we'll add all of the tag in one go, we don't need to worry about
            # having the default behaviour in an else statement
            if message[i] == "@":
                # Get what the handle will be (if it is a handle of an existing user)
                handle = self._get_tag_alone(message[i + 1 : ])
                if handle == consts.REMOVED_USER_HANDLE:
                # We can't tag deleted users
                # Add extra @ to show it's not an actual tag
                    result += "@"
                    i += 1
                    continue
                # Get user associated with user's handle
                # Replace tag with user's ID
                try:
                    user_id = state.s.users.get_by_handle(handle).get_id()
                    result += str(user_id)
                    tagged_users.add(user_id)
                    i += len(handle)
                # It isn't a valid
                except error.InputError:
                    # Add another @ symbol
                    result += "@"
            # Increment index
            i += 1
        # Return the encoded string and the tagged users
        return result, tagged_users

    def _decode(self, message):
        """Decode a message so that tags are reinserted as plaintext with the
        correct user handles

        Args:
            message (str): encoded message

        Returns:
            str: decoded message
        """
        
        # Loop through each char, and append decoded message char by char (excluding
        # tags)
        # Note that we need to use a while loop since any time that the string needs
        # to be different from the original, we will need to jump the index of the 
        # current char ahead
        result = ""
        i = 0
        while (i < len(message)):
            # Default behaviour: not in a tag, just append the letter
            result += message[i]
            
            # If we've found the start of a possible tag (@ symbol)
            # Since we'll add all of the tag in one go, we don't need to worry about
            # having the default behaviour in an else statement
            if message[i] == "@":
                # Get what the handle will be (if it is an ID of an existing user)
                user_id = self._get_tag_alone(message[i + 1 : ])
                
                # Get user associated with user's id
                # Replace tag with user's handle
                try:
                    handle = state.s.users.get(int(user_id)).get_handle()
                    result += handle
                    i += len(user_id)
                # It isn't a valid
                except (error.InputError, ValueError):
                    # Skip the next @ symbol
                    i += 1
                    # If next symbol wasn't '@', something went horribly wrong
                    # The message data is corrupted, and we should just stop here
                    assert message[i] == '@'
            # Increment index
            i += 1
        
        # If we're quoting a message
        if self._quote_id is not None:
            # Add it in
            try:
                og_msg = str(state.s.messages.get(self._quote_id))
            # If we couldn't find the message, we should replace our input with
            # [Message deleted]
            except error.InputError:
                og_msg = consts.REMOVED_MESSAGE_STR
            temp = result
            result = '"""\n' + og_msg\
                + '\n"""'
            if len(temp) != 0:
                result += "\n\n" + temp
        
        # Return final result string
        return result

    def get_tagged_users(self):
        """Returns a set of users who were tagged

        Returns:
            set: user IDs tagged
        """
        return self._tagged_users
    
    def update(self, new_str):
        """Updates currently encoded string to new_str

        Args:
            new_str (str): new string to encode
        """
        self._encoded, self._tagged_users = self._encode(new_str)
    
    def __str__(self) -> str:
        return self._decode(self._encoded)
    
    def __eq__(self, o: object) -> bool:
        # If we're comparing an encoded string, just compare their encoded data
        if isinstance(o, EncodedString):
            return self._encoded == o._encoded
        # Otherwise compare the stringified version to it
        else:
            return str(self) == o

def save_data(func):
    """Function decorator to save data after the function is executed

    Args:
        func (function): Function to save data fater
    """
    def do_func(*args):
        result = func(*args)
        state.save_state()
        return result
        
    return do_func

def unwrap_token(func):
    """Function decorator to decode tokens and replace the token arg with an auth_user_id
    Optionally passes token onto function if it has an argument entitled 'token'

    Args:
        func (function): Function to unwrap token for
    """
    # Inspect the function
    params = inspect.signature(func).parameters
    
    # If the function requires a token argument
    if "token" in params:
        # Create a wrapper that passes the token
        def do_func(token, *args):
            auth_user_id = session.get_session_by_token(token).get_owner()
            ret = func(auth_user_id, *args, token=token)
            return ret
    else:
        # Create a wrapper that doesn't pass the token
        def do_func(token, *args):
            auth_user_id = session.get_session_by_token(token).get_owner()
            ret = func(auth_user_id, *args)
            return ret
    
    # Return the required wrapper
    return do_func

def get_static_url(file_loc: str):
    return f"{config.url}static/{file_loc}"

# Import state at the bottom of the file to prevent circular imports
from . import state
from src import error, session

