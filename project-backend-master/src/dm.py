"""src > DM.py

Implements functions for interacting with DMs, as well as the data
structures for storing them.

Primary Contributors:
    -  Yuzhe Sean Geng [z5211102@ad.unsw.edu.au]
        - initial DM data structure and data structure helper function implmentation
    - Danny Won [z5338486@ad.unsw.edu.au]
        - Docstrings and debugging on all functions/rehaul
        - corrections on spec accuracy on all functions
        - added helper functions (in relevant files relating to DM interaction too)
        - dm_message_send_v1()
        - dm_messages_v1()
"""
import datetime
from .error import InputError, AccessError
from . import message, helpers
from .abstract_channel import AbstractChannel
from .generic_data import GenericDataContainer
from src import helpers, notification

class Dm(AbstractChannel):
    """Dm object (extends AbstractChannel)
    """
    _contained_type_str = "DM"
    def __init__(self, creator_id: int, users: list):
        """Creates a new DM

        Args:
            creator_id (int): ID of the DM creator
            users (list): user IDs to include (not including original creator)
        """
        super().__init__()
        self._owner = creator_id
        
        # Add all members
        # Only explicitly add the creator if they aren't a member already
        if creator_id not in users:
            self.add_member(creator_id, creator_id)
        [self.add_member(u, creator_id, silence_notif=True) for u in users]
        state.s.dms.add(self)
        
        for m in self.get_members():
            if m == creator_id: continue
            inviter = state.s.users.get(creator_id)
            notification.Notification(
                m,
                -1,
                self.get_id(),
                f"@{inviter.get_handle()} added you to {self.get_name()}"
            )
        
        state.s.stats.add_dms_entry(1)
    
    def remove(self):
        super().remove()
        state.s.stats.add_dms_entry(-1)
    
    def get_name(self) -> str:
        """Get the current name of the DM

        Returns:
            str: name
        """
        return ", ".join(sorted(
            [state.s.users.get(u).get_handle() for u in self.get_members()]
            ))

    def get_owner(self) -> int:
        """Get the owner of the DM

        Returns:
            int: owner ID
        """
        return self._owner

    def is_owner(self, u_id: int) -> bool:
        """Returns whether a user is the owner of the DM

        Args:
            u_id (int): user ID

        Returns:
            bool: whether they're the owner
        """
        return self.get_owner() == u_id
    
    def add_member(self, u_id: int, inviter_id, silence_notif=False):
        """Adds a member to the DM

        Args:
            u_id (int): user ID
            inviter_id (int): ID of inviter, used to generate notification
            silence_notif (bool): Whether to not send a notification, defaults to False
        """
        if u_id in self._members:
            return
        
        super().add_member(u_id)
        
        # Add to user's list of dms too
        state.s.users.get(u_id).add_dm(self._id)
        
        if u_id != inviter_id and not silence_notif:
            inviter = state.s.users.get(inviter_id)
            notification.Notification(
                u_id,
                -1,
                self.get_id(),
                f"@{inviter.get_handle()} added you to {self.get_name()}"
            )
    
    def remove_member(self, u_id: int):
        """Removes a member of a dm

        Args:
            u_id (int): user id to remove
        """
        super().remove_member(u_id)
        
        # Remove from user's list of dms too
        state.s.users.get(u_id).remove_dm(self._id)
        
        # TODO: what happens if the member is the DM owner?

class DmContainer(GenericDataContainer):
    """Container for Dms
    """
    def get(self, get_id: int) -> Dm:
        return super().get(get_id)

@helpers.unwrap_token
def dm_details_v1(auth_user_id, dm_id):
    """Returns dict of information about the DM, users part
    of the DM can view.

    Args:
        auth_user_id (int): User's ID
        dm_id (int): DM ID

    Raises:
        AccessError: User is not authorised
        InputError: User not in the DM
        InputError: Invalid DM

    Returns:
        dict: dict of DM details
    """

    dm = state.s.dms.get(dm_id)

    if not dm.is_member(auth_user_id):
        raise AccessError(description="You aren't a member of this DM")

    return dm.as_dict()

@helpers.unwrap_token    
def dm_list_v1(auth_user_id):
    """Returns the list of DMs that the user is a member of,
    Assumes user is valid

    Args:
        auth_user_id (int): User's ID

    Returns:
        dict: dict of list of DMs
    """
    dms = []


    for dm_id in state.s.users.get(auth_user_id).get_dms():
        dms.append({"dm_id": dm_id, "name": state.s.dms.get(dm_id).get_name()})

    return {"dms": dms}

@helpers.unwrap_token    
def dm_create_v1(auth_user_id, u_ids):
    """Creates a DM and details revolving around them, and adds it to
    DM data struc in state.s.py

    Args:
        auth_user_id (int): User's ID
        u_ids (list (int)): list ID's of users the DM is being sent to

    Raises:
        InputError: Invalid user

    Returns:
        dict: dict of created dm dict
    """

    for u in u_ids:
        state.s.users.get(u)
    
    dm = Dm(auth_user_id, u_ids)
    
    return {"dm_id": dm.get_id(), "dm_name": dm.get_name()}
    
@helpers.unwrap_token
def dm_remove_v1(auth_user_id, dm_id):
    """Removes an existing DM, if requested by original creator

    Args:
        auth_user_id (int): User's ID
        dm_id (int): Dms ID

    Raises:
        InputError: Invalid DM
        AccessError: User not DM creator
    """

    # Testing if the dm_id is valid by running get_dm_by_id func
    dm = state.s.dms.get(dm_id)
    
    if not dm.is_owner(auth_user_id):
       raise AccessError(description="You aren't the creator of this DM")

    # This will delete the DM
    state.s.dms.remove(dm.get_id())

@helpers.unwrap_token    
def dm_invite_v1(auth_user_id, dm_id, u_id):
    """Invites a user to an existing DM

    Args:
        auth_user_id (int): User's ID
        dm_id (int): DM's ID
        u_id (int): User ID to be added to DM

    Raises:
        InputError: DM does not exist
        InputError: Invalid user to add
        AccessError: Unauthorised user
    """
    # Testing if the dm_id is valid
    dm = state.s.dms.get(dm_id)
    # Testing if the u_id is valid
    state.s.users.get(u_id)

    if not dm.is_member(auth_user_id):
       raise AccessError(description="You must be a member of this DM to perform this action")

    dm.add_member(u_id, auth_user_id)
  
@helpers.unwrap_token    
def dm_leave_v1(auth_user_id, dm_id):
    """Given a DM ID, the user is removed as a member of this DM

    Args:
        auth_user_id (int): User's ID
        dm_id (int): DM's ID

    Raises:
        InputError: DM ID is not valid
        AccessError: User not member of DM
    """
    dm = state.s.dms.get(dm_id)
    
    if not dm.is_member(auth_user_id):
        raise AccessError(description="You must be a member of this DM to perform this action")

    # Remove the user to the DM
    dm.remove_member(auth_user_id)

@helpers.unwrap_token
def dm_messages_v1(auth_user_id, dm_id, start):
    """Returns the 50 most recent messages of the DM given a start index

    Args:
        auth_user_id (int): User's ID
        dm_id (int): DMs ID
        start (int): start index to search messages for

    Raises:
        InputError: DM invalid
        InputError: Invalid start index
        AccessError: Unauthorised user

    Returns:
        dict: list of messages from DM
    """
    dm = state.s.dms.get(dm_id)

    # Check if user has access to DM
    if not dm.is_member(auth_user_id):
        raise AccessError(description="You aren't a member of this DM")
    
    return dm.get_paged_messages(start)

@helpers.save_data
@helpers.unwrap_token
def dm_message_send_v1(auth_user_id, dm_id, message_str):
    """Send a message in a dm

    Args:
        auth_user_id (int): User ID of the user sending the message
        dm_id (int): DM ID of the DM it's being sent in
        message (str): message contents: (must be 0 < len <= 1000 chars)

    Raises:
        AccessError: User doesn't have access to DM
        InputError: User or DM don't exist; message is too long or too short

    Returns:
        dict: "dm_id": [int] dm ID of newly sent message
    """

    msg = message.send_message_generic(auth_user_id, dm_id, message_str)

    return {"message_id": msg.get_id()}

@helpers.save_data
@helpers.unwrap_token
def dm_message_send_later_v1(auth_user_id, dm_id, message_str, send_time):
    """Send a message in a dm

    Args:
        auth_user_id (int): User ID of the user sending the message
        dm_id (int): DM ID of the DM it's being sent in
        message (str): message contents: (must be 0 < len <= 1000 chars)
        send_time (datetime): time that the message will be sent at

    Raises:
        AccessError: User doesn't have access to DM
        InputError: User or DM don't exist; message is too long or too short

    Returns:
        dict: "dm_id": [int] dm ID of newly sent message
    """
    send_time = datetime.datetime.fromtimestamp(send_time)
    curr_time = datetime.datetime.now()
    if send_time < curr_time:
        raise InputError(description=f"Your selected time ({send_time}) is before the present ({curr_time})")

    msg = message.send_message_generic(auth_user_id, dm_id, message_str, send_time=send_time)
    
    return {"message_id": msg.get_id()}

from . import state

