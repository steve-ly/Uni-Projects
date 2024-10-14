"""src > user.py

Provides functions for interacting with users, as well as the data structure
underpinning users, and helper functions for that structure

Primary Contributors: 
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]
     - Data structure and helper functions
         - get_new_user()
         - add_user()
         - get_user_by_email()
         - get_user_by_id()
         - get_user_by_handle()
         - add_channel_to_user()
         - add_mesasge_to_user()
         - prepare_user_data()

Minor Contributors:
 - Steven Ly [z5257127@ad.unsw.edu.au]
     - Additions:
         - Add is_admin to data structure (Merge Request !27)
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]
     - Bug fixes:
         - Fix user_profile_sethandle
"""

import os
import hashlib
import datetime

from . import consts
from src.error import InputError, AccessError
from .generic_data import GenericData, GenericDataContainer
from .stats import Stats

from PIL import Image
from urllib.request import urlretrieve
from flask import url_for

class User(GenericData):
    """An object representing a user of Dreams
    """
    _contained_type_str = "User"
    def __init__(self, email: str, password: str, first_name: str, last_name: str, is_bot=False):
        """Create a User object

        Args:
            email (str): email address of user
            password (str): password (unhashed)
            first_name (str): first name of user
            last_name (str): last name of user
            is_bot (bool): Whether the user is a bot (excludes them from listing
                           and counting of users)
        """
        super().__init__()
        self._email = email
        self._pass_hash = hashlib.sha256(password.encode()).hexdigest()
        self._name_first = first_name
        self._name_last = last_name
        self._handle = self._generate_handle(first_name, last_name)
        self._channels = set()
        self._dms = set()
        self._messages = set()
        self._notifications = []
        self._sessions = set()
        self._is_admin = False
        self._is_bot = is_bot
        self._is_deleted = False
        self._profile_img = None
        
        # User Stats
        self._stats = Stats(True)
        
        state.s.users.add(self)
    
    def remove(self):
        """Sets the user as being deleted, as well as setting their profile
        to the required constants for deleted users.
        """
        if self._is_deleted:
            raise InputError(description="That user has already been removed")
        
        # Remove the user from all their channels
        for ch in self.get_channels():
            state.s.channels.get(ch).remove_member(self.get_id())
        
        # And from all their DMs
        for dm in self.get_dms():
            state.s.dms.get(dm).remove_member(self.get_id())

        # Edit all their messages
        for msg in self.get_messages():
            state.s.messages.get(msg).edit(consts.REMOVED_USER_MESSAGE)
        
        # Set their profile info to signify they are removed  
        self.set_handle(consts.REMOVED_USER_HANDLE)
        self.set_email("")
        self.set_name(consts.REMOVED_USER_NAME_FIRST, 
                            consts.REMOVED_USER_NAME_LAST)
        # Set their admin status to False
        self.set_admin(False)

        # Remove their sessions
        for session in self.get_sessions():
            state.s.sessions.remove(session)
        
        # Set them as being deleted (immutable)
        self._is_deleted = True
    
    def as_dict(self) -> dict:
        """Get a dictionary representation of the user

        Returns:
            dict: user data
        """
        data = {}
    
        data["u_id"] = self.get_id()
        data["email"] = self.get_email()
        data["name_first"] = self.get_name()[0]
        data["name_last"] = self.get_name()[1]
        data["handle_str"] = self.get_handle()
        data["profile_img_url"] = self.get_profile_img()
        
        return data

    def check_deletion(self):
        """Raises an InputError if the user has been deleted.
        Should be called before any user data is modified
        """
        if self._is_deleted:
            raise InputError(description="This user is deleted")
    
    def is_removed(self):
        """Returns whether the user has been deleted
        """
        return self._is_deleted
    
    def is_bot(self):
        """Return whether the user is a bot
        """
        return self._is_bot
    
    def _generate_handle(self, name_first, name_last) -> str:
        """Generates and returns a formatted handle for the user
        
            Arguments:
                <name_first> (string) users first name
                <name_last> (string) users last name
            Returns:
                <handlecpy> (string) the handle generated
        """

        # Get base handle
        handlestr = name_first.lower() + name_last.lower()
        
        # Remove whitespace
        handlestr = handlestr.replace(" ","")
        handlestr = handlestr.replace("\t","")
        handlestr = handlestr.replace("\n","")
        
        # Remove @ symbol
        handlestr = handlestr.replace("@","")
        if len(handlestr) > consts.HANDLE_MAX_LEN:
            handlestr = handlestr[:consts.HANDLE_MAX_LEN]

        # Make a copy to replace numbers into
        handlecpy = handlestr

        # Search for users with the same handle
        # Increasing the handle's identifier number each time
        # Every time we find a duplicate handle, we need to start the search again
        # since we can't guarantee we didn't go over any previous users before
        num_duplicates = 0
        has_changed = True
        # Loop until the handle didn't change in an entire search
        while has_changed:
            has_changed = False
            # Loop through each user
            for user_tag in state.s.users:
                # If we find a duplicate
                if user_tag.get_handle() == handlecpy:
                    # Set the handle's name to include the new number of duplicates
                    handlecpy = handlestr + str(num_duplicates)
                    num_duplicates += 1
                    has_changed = True
                    # Return to start of search
                    break

        return handlecpy
    
    def get_email(self) -> str:
        """Return user's email address

        Returns:
            str: email
        """
        return self._email
    
    def set_email(self, email: str):
        """Set user's email

        Args:
            email (str): new email
        """
        self.check_deletion()
        self._email = email
    
    def get_name(self) -> tuple:
        """Returns user's name as a tuple

        Returns:
            tuple: (first_name, last_name)
        """
        return self._name_first, self._name_last
    
    def set_name(self, name_first: str, name_last: str):
        """Set user's name

        Args:
            name_first (str): new first name
            name_last (str): new last name
        """
        self.check_deletion()
        self._name_first = name_first
        self._name_last = name_last
    
    def get_handle(self) -> str:
        """Get user's handle

        Returns:
            str: handle
        """
        return self._handle

    def set_handle(self, handle: str):
        """Set user's handle

        Args:
            handle (str): new handle
        """
        self.check_deletion()
        self._handle = handle

    def is_admin(self) -> bool:
        """Returns whether the user is an admin

        Returns:
            bool: whether they're an admin
        """
        return self._is_admin

    def set_admin(self, new_val: bool):
        """Set admin permissions of user

        Args:
            new_val (bool): is_admin
        """
        self.check_deletion()
        self._is_admin = new_val

    def check_password(self, password) -> bool:
        """Given a password string (unhashed), hashes it and checks against
        the stored hash.

        Args:
            password (str): unhashed password

        Returns:
            bool: equality of passwords
        """
        return self._pass_hash == hashlib.sha256(password.encode()).hexdigest()

    def set_password(self, password):
        """Set new password of user

        Args:
            password(str): unhased password
        """
        self.check_deletion()
        self._pass_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def add_channel(self, ch_id: int):
        """Add a channel to user

        Args:
            ch_id (int): id of channel
        """
        self.check_deletion()
        self._channels.add(ch_id)
        self._stats.add_channels_entry(1)
    
    def remove_channel(self, ch_id: int):
        """Remove channel from user

        Args:
            ch_id (int): id of channel
        """
        self._channels.remove(ch_id)
        self._stats.add_channels_entry(-1)

    def get_channels(self) -> list:
        """Get list of channels user is a member of

        Returns:
            list: channel IDs
        """
        return list(self._channels)

    def get_profile_img(self) -> str:
        """ Get url for user's profile image. If the user doesn't have a profile
        image set, returns the default profile image URL.

        Return:
            str: image URL
        """
        if self._profile_img is None:
            return helpers.get_static_url(consts.DEFAULT_PROFILE_IMG)
        else:
            return helpers.get_static_url(self._profile_img)

    def set_profile_img(self, new_url: str):
        """Set the storedurl for user's profile image to the provided value

        Args:
            new_url (str): new location of image
        """
        self._profile_img = new_url

    def add_dm(self, dm_id: int):
        """Add a dm to user

        Args:
            dm_id (int): id of dm
        """
        self.check_deletion()
        self._dms.add(dm_id)
        self._stats.add_dms_entry(1)
    
    def remove_dm(self, dm_id: int):
        """Remove dm from user

        Args:
            dm_id (int): id of dm
        """
        self._dms.remove(dm_id)
        self._stats.add_dms_entry(-1)

    def get_dms(self) -> list:
        """Get list of dms user is a member of

        Returns:
            list: dm ids
        """
        return list(self._dms)

    def add_message(self, msg_id: int):
        """Add a message to user

        Args:
            msg_id (int): id of message
        """
        self.check_deletion()
        self._messages.add(msg_id)
        self._stats.add_messages_entry(1)
    
    def remove_message(self, msg_id: int):
        """Remove a message from user

        Args:
            msg_id (int): id of message
        """
        self._messages.remove(msg_id)
        self._stats.add_messages_entry(-1)
    
    def get_messages(self) -> list:
        """Get list of messages user has sent

        Returns:
            list: message ids
        """
        return list(self._messages)

    def add_notification(self, notif_id: int):
        """Add a notification to a user

        Args:
            notif_id (int): id of notification
        """
        self._notifications.insert(0, notif_id)
    
    def remove_notification(self, notif_id: int):
        """Remove a notification from user

        Args:
            notif_id (int): id of notification
        """
        self._notifications.remove(notif_id)

    def get_notifications(self) -> list:
        """Get list of user's notifications

        Returns:
            list: notification ids
        """
        return list(self._notifications)

    def add_session(self, session_id: int):
        """Add a session to user

        Args:
            session_id (int): id of session
        """
        self.check_deletion()
        self._sessions.add(session_id)

    def remove_session(self, session_id: int):
        """Remove a session from user

        Args:
            session_id (int): id of session
        """
        self._sessions.remove(session_id)

    def get_sessions(self) -> list:
        """Get list of user's sessions

        Returns:
            list: session ids
        """
        return list(self._sessions)
    
    def get_stats(self):
        """Returns user's stats

        Returns:
            Stats: user stats
        """
        return self._stats

class UserContainer(GenericDataContainer):
    """Container for users
    """
    def get(self, get_id: int) -> User:
        return super().get(get_id)
    
    def get_by_handle(self, handle: str) -> User:
        """Returns User object with matching handle

        Args:
            handle (str): handle of user to get

        Raises:
            InputError: User not found

        Returns:
            User: user with matching handle
        """
        for user in self._contained.values():
            if user.get_handle() == handle:
                return user
        raise InputError(description=f"User with handle '@{handle}' not found")
    
    def get_by_email(self, email: str) -> User:
        """Returns User object with matching email

        Args:
            email (str): email address of user to get

        Raises:
            InputError: User not found

        Returns:
            User: user with matching email
        """
        for user in self._contained.values():
            if user.get_email() == email:
                return user
        raise InputError(description=f"User with email '{email}' not found")
    
    def __len__(self) -> int:
        """Return the number of users who aren't a bot that are registered

        Returns:
            int: [description]
        """
        return sum([not u.is_bot() for u in self._contained.values()])

from src import helpers

@helpers.unwrap_token
def user_profile_v1(auth_user_id, u_id):
    """For a valid user, returns information about their 
    user_id, email, first name, last name, and handle

    Args:
        auth_user_id ( int ): user's id
        u_id ( int ): user's id

    Raises:
        AccessError: Unauthorised user

    Returns: dict: user
    """
    state.s.users.get(auth_user_id)
  
    return {"user": state.s.users.get(u_id).as_dict()}

@helpers.save_data
@helpers.unwrap_token
def user_profile_setname_v1(auth_user_id, name_first, name_last):
    """Updates the authorised user's first and last name

    Args:
        auth_user_id ( int ): user's id
        name_first ( str ): first name to be changed into
        name_last ( str ): last name to be changed into

    Raises:
        InputError: User not found
    """
    # Check if auth_user_id is valid


    user = state.s.users.get(auth_user_id)


    # Check length of first
    if not ((1 <= len(name_first) <= 50) and (1 <= len(name_last) <= 50)):
        raise InputError(description="First and last names must be between 1 and 50 chars")

    user.set_name(name_first, name_last)
    return

@helpers.save_data
@helpers.unwrap_token
def user_profile_setemail_v1(auth_user_id, email):
    """Updates the authorised user's email address

    Args:
        auth_user_id ( int ): user's id
        email ( str ): email address to be changed into

    Raises: 
        AccessError: Unauthorised user
        InputError: Invalid email format
    """
    # Make email all lowercase
    email = email.lower()

    # Get user    
    user = state.s.users.get(auth_user_id)

    # Check if email is valid
    if not helpers.is_email_valid(email):
        raise InputError(description="Email address is invalid")


    # Ensure email doesn't exist already
    try:
        state.s.users.get_by_email(email)
        
        # If we reach this point, we found a duplicate
        # Raise exception, which will be caught and raised again as InputError
        raise Exception("dupe")
    except InputError:
        # This is what should happen (user with new handle not found),
        # continue normally
        pass
    except Exception:
        # Reraise exception saying handle is a duplicate
        raise InputError(description="Email address is already being used by another user") from None
    
    user.set_email(email)
    return

@helpers.save_data
@helpers.unwrap_token
def user_profile_sethandle_v1(auth_user_id, handle_str):
    """Updates the user's handle without the "@" at the start

    Args:
        auth_user_id ( int ): user's id
        handle_str ( str ): handle to be changed into
    
    Raises: 
        AccessError: Unauthorised user
    """
    # Check if auth_user_id is valid
    
    user = state.s.users.get(auth_user_id)

    
    # If there's no change, return with no actions
    if handle_str == user.get_handle():
        return
    
    # Check lengths
    if not 3 <= len(handle_str) <= 20:
        raise InputError(description="New handle must be between 3 and 20 chars")
    
    # Check for @ sybol
    if '@' in handle_str:
        raise InputError(description="New handle cannot contain '@' character")
    
    # Check for whitespace
    if any([s in handle_str for s in [' ', '\n', '\t']]):
        raise InputError(description="New handle cannot contain whitespace")
    
    # Ensure handle doesn't exist already
    try:
        state.s.users.get_by_handle(handle_str)
        
        # If we reach this point, we found a duplicate
        # Raise exception, which will be caught and raised again as InputError
        raise Exception("Duplicate handle")
    except InputError:
        # This is what should happen (user with new handle not found),
        # continue normally
        pass
    except Exception:
        # Reraise exception saying handle is a duplicate
        raise InputError(description="Handle is already used by another user") from None
    
    # Set handle
    user.set_handle(handle_str)
    return

@helpers.unwrap_token
def user_list_all_v1(auth_user_id):
    """Returns a list of all users and their associated details

    Args:
        auth_user_id (int): unique user id for valid user
    
    Raises:
        AccessError: Unauthorised user

    Returns:
        dict: users and their details
    """

    user_data_list = {
        "users": [],
    }
    
    for user in state.s.users:
        # If the user was deleted, don't include them
        if user.is_removed() or user.is_bot():
            continue
        
        # Prep data to only show public details
        user_data = user.as_dict()

        # Add user to new data list
        user_data_list["users"].append(user_data)

    return user_data_list

@helpers.save_data
@helpers.unwrap_token
def user_profile_uploadphoto_v1(auth_user_id, img_url, x_start, y_start, x_end, y_end):
    """The function is used to download the image via img_url and upload the image for
       users after cropping these image. 

    Args:
        auth_user_id (int): unique user id for valid user
        img_url (str): an url to provide the image uploading by users
        parameters for image: x_start, y_start, x_end, y_end
        
    Raises:
        AccessError: Unauthorised user
        InputError: Unvalid http state, Overloaded imagin size and Image openning error
    
    Returns:
        None
    """
    # Location of the image
    temp_loc = f"{consts.STATE_RESOURCE_FOLDER}/temp.jpg"
    img_loc = f"{consts.STATE_RESOURCE_FOLDER}/{auth_user_id}.jpg"
    
    # Temporary function for removing temporary file
    def remove_temp():
        try:
            os.remove(temp_loc)
        # This is just a safety check
        except FileNotFoundError: # pragma: no cover
            pass
    
    # Check if the webpage has a valid image and download according to url of image
    try:
        urlretrieve(img_url, temp_loc)
    except Exception as e:
        #remove_temp()
        raise InputError(description=f"User Image Fail to Download ({e})") from e

    # Open downloaded image in static url and identify if it is image type
    im = Image.open(temp_loc)
    if im.format != "JPEG":
        remove_temp()
        raise InputError(description="Image must be in format JPEG")
       
    # Import the size parameters for users' images
    width = im.size[0]
    height = im.size[1]
    
    # Limit the cropping range of image
    if x_start < 0 or y_start < 0 or x_end > width or y_end > height:
        remove_temp()
        raise InputError(description="Crop coordinates lie outside image")

    # Cropping and Saving
    crop_img = im.crop((x_start, y_start, x_end, y_end))    
    crop_img.save(img_loc)
    
    # Remove the temporary image
    remove_temp()
    
    # Set profile image for user
    state.s.users.get(auth_user_id).set_profile_img(img_loc)
    
    return {}


# Import state at the bottom of the file to avoid circular import issues
from . import state
