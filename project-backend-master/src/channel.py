"""src > channel.py

Provides functions for interacting with a channel, as well as the implementation
and helper functions for the data structure underpinning them

Primary Contributors:
 - Runyao (Brian) Wang [z5248223@ad.unsw.edu.au]
     - channel_invite_v1()
     - channel_details_v1()
     - channel_messages_v1()
     - channel_join_v1()
 - Danny Won [z5338486@ad.unsw.edu.au]
     - Channel data structure and helper functions
         - get_new_channel()
         - add_channel()
         - get_channel_by_id()
         - add_user_to_channel()
         - add_message_to_channel()
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]
     - channel_leave_v1()
     - channel_addowner_v1()
     - channel_removeowner_v1()

Minor Contributors:
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]
     - Bug fixes:
         - Commit 9c20a75c
         - Commit b3356d00
         - Commit 0035ceff

"""

from src.error import InputError, AccessError
from src import helpers, notification

from .abstract_channel import AbstractChannel
from .generic_data import GenericDataContainer

class Channel(AbstractChannel):
    """Channel object (extends AbstractChannel)
    """
    _contained_type_str = "Channel"
    def __init__(self, name: str, creator_id: int, public: bool):
        """Create a new Channel object

        Args:
            name (str): channel name
            creator_id (int): user id of channel creator
            public (bool): whether the channel is public or not
        """
        super().__init__()
        self._owners = set()
        self._name = name
        self._public = public
        
        # Add creator as member and owner
        self.add_member(creator_id)
        self.add_owner(creator_id)
        
        # Add to database
        state.s.channels.add(self)
        
        # Add entry in stats
        state.s.stats.add_channels_entry(1)
    
    def remove(self):
        super().remove()
        # Add entry in stats
        state.s.stats.add_channels_entry(-1)
    
    def as_dict(self) -> dict:
        """Returns dictionary representation of the channel

        Returns:
            dict: channel info
        """
        sup = super().as_dict()
        sup["all_members"] = sup.pop("members")
        sup["owner_members"] = [state.s.users.get(u).as_dict()
                                        for u in self.get_owners()]
        
        # Also include global owners, if they aren't already present
        for u in self.get_members():
            usr = state.s.users.get(u)
            if usr.is_admin() and not self.is_owner(u):
                sup["owner_members"].append(usr.as_dict())
        sup["is_public"] = self._public
        
        return sup
    
    def get_name(self) -> str:
        """Returns channel name

        Returns:
            str: name
        """
        return self._name

    def get_publicity(self) -> bool:
        """Returns whether the channel is public

        Returns:
            bool: publicity
        """
        return self._public

    def get_owners(self) -> list:
        """Returns a list of channel owners

        Returns:
            list: owners
        """
        return list(self._owners)
    
    def is_owner(self, u_id: int) -> bool:
        """Return whether a user is a local channel owner. IMPORTANT: if a user
        has global admin permissions, but not local admin permissions, this will
        return False. Consider using Channel.has_owner_perms() if you wish to
        account for this

        Args:
            u_id (int): user ID

        Returns:
            bool: is local owner
        """
        return u_id in self._owners
    
    def has_owner_perms(self, u_id: int) -> bool:
        """Returns whether a user has admin permissions in this channel (either
        because they are a local owner, or because they are a global admin)

        Args:
            u_id (int): user id

        Returns:
            bool: has owner permissions
        """
        return self.is_owner or state.s.users.get(u_id).is_admin()
    
    def add_owner(self, u_id: int):
        """Add a user as a local owner of the channel

        Args:
            u_id (int): user id
        """
        self._owners.add(u_id)
    
    def remove_owner(self, u_id: int):
        """Remove a user who is a channel owner

        Args:
            u_id (int): user id
        """
        self._owners.remove(u_id)

    def add_member(self, u_id: int):
        super().add_member(u_id)
        
        # Add to user's list of channels too
        state.s.users.get(u_id).add_channel(self.get_id())

    def remove_member(self, u_id: int):
        """Removes a member of a channel

        Args:
            u_id (int): user id to remove
        """
        super().remove_member(u_id)
        
        # Remove from user's list of channels too
        state.s.users.get(u_id).remove_channel(self._id)
        
        # If they're an owner, remove them
        try:
            self.remove_owner(u_id)
        except KeyError:
            pass

class ChannelContainer(GenericDataContainer):
    """Data container for channels
    """
    def get(self, get_id: int) -> Channel:
        return super().get(get_id)

@helpers.save_data
@helpers.unwrap_token
def channel_invite_v1(auth_user_id, channel_id, u_id):
    """A user (with user id auth_user_id) in a channel (with ID channel_id.)
    invites a user (with user id u_id) to join the channel 

    Arguments:
        auth_user_id ( int ): the authorised inviter's id
        channel_id ( int ): the channel's id
        u_id ( int ): the invitee's id

    Exceptions:
        InputError  - Occurs when channel id invalid
        InputError  - Occurs when invitee's user id invalid      
        AccessError - Occurs when inviter is not in the channel 

    Returns:
        Dict (empty)
    """

    inviter = state.s.users.get(auth_user_id)

    # Ensure user being invited exists (will raise InputError)
    state.s.users.get(u_id)
    # Check the inviter (auth_user_id) is in the channel
    ch = state.s.channels.get(channel_id)
    if not ch.is_member(auth_user_id):
        raise AccessError(description="You must be a member of the channel to do this")

    # Check if the invitee is already a member of the channel
    if ch.is_member(u_id):
        # This shouldn't cause an error but no action should be taken
        return {}

    # Add the user to the channel
    ch.add_member(u_id)
    
    # Create a notification

    notification.Notification(
         u_id,
         channel_id,
         -1,
         f"@{inviter.get_handle()} added you to {ch.get_name()}"
    )

    return {}

@helpers.unwrap_token
def channel_details_v1(auth_user_id, channel_id):
    """Given a Channel with ID channel_id that the authorised user is part of, 
    provide basic details about the channel.

    Arguments:
        auth_user_id (int): the authorised user's id
        channel_id (int): the channel's id

    Exceptions:
        InputError  - Occurs when channel id invalid     
        AccessError - Occurs when authorised user is not in the channel 

    Return value:
        A dict of the channel's details
            name (str): Channel name
            owner_members (users): List of user data dicts for owners of the 
                                    channel (including global owners if they
                                    are members)
            all_members (users): List of user data dicts for members of the
                                    channel

    """
    

    # Check the channel id is valid (will raise InputError)
    ch = state.s.channels.get(channel_id)
    
    # Check the user is in the channel 
    if not ch.is_member(auth_user_id):
        raise AccessError(description="You aren't a member of this channel")

    return ch.as_dict()

@helpers.unwrap_token
def channel_messages_v1(auth_user_id, channel_id, start):
    """Given a Channel with ID channel_id that the authorised user is part of,
     return up to 50 messages between index "start" and "start + 50".
     Message with index 0 is the most recent message in the channel. 
     This function returns a new index "end" which is the value of "start + 50", 
     or, if this function has returned the least recent messages in the channel, 
     returns -1 in "end" to indicate there are no more messages to load after this return.

    Arguments:
        auth_user_id ( int ): the authorised user's id
        channel_id ( int ): the channel's id
        start ( int ): the start index of the messages required to list

    Exceptions:
        InputError  - Occurs when channel id invalid     
        InputError  - Occurs when the start index is not valid
        AccessError - Occurs when authorised user is not in the channel 

    Return value:
        A dict with 3 keys { messages, start, end }
        ['messages'] is a list of dictionaries of every required message infos
        ['start'] is the start index of the messages required to list
        ['end'] is the end index of the messages required to list


    """

    # Check the channel id is valid
    ch = state.s.channels.get(channel_id)

    # Check the User with auth_user_id is in the channel
    if not ch.is_member(auth_user_id):
        raise AccessError(description="You aren't a member of this channel")

    msgs = ch.get_paged_messages(start)
    # Check whether the user reacts any messages
    for m in msgs["messages"]:
        for react in m["reacts"]:
            if auth_user_id in react["u_ids"]:
                react["is_this_user_reacted"] = True
            else:
                react["is_this_user_reacted"] = False
    return msgs

@helpers.save_data
@helpers.unwrap_token
def channel_leave_v1(auth_user_id, channel_id):
    """Given a channel ID, and an auth user ID of a user that is a member,
    rempves the user from the channel

    Args:
        auth_user_id (int): user ID
        channel_id (int): channel ID
    
    Exceptions:
        AccessError - when auth user ID is invalid
        InputError  - when channel ID is invalid, or auth_user is not a member
                      of the channel
    """

    # Will raise InputError
    c = state.s.channels.get(channel_id)
    
    if not c.is_member(auth_user_id):
        raise AccessError(description="You must be a member of this channel to do this")
    
    c.remove_member(auth_user_id)

@helpers.save_data
@helpers.unwrap_token
def channel_join_v1(auth_user_id, channel_id):
    """Given a channel_id of a channel that the authorised user can join,
     adds the user to that channel

    Arguments:
        auth_user_id ( int ): the authorised user's id
        channel_id ( int ): the channel's id

    Exceptions:
        InputError  - Occurs when channel id invalid     
        AccessError - Occurs when the channel is private channel

    Returns:
        Dict (empty)
    """

    user = state.s.users.get(auth_user_id)

    ch = state.s.channels.get(channel_id)

    # If they're already a member, return and do nothing
    if ch.is_member(auth_user_id):
        return

    # Check the channel is public channel
    # if the user is a global owner, this user can join all channels
    if not (ch.get_publicity() or user.is_admin()):
        raise AccessError(description="This channel is private")

    # Add the authorised user to the channel
    ch.add_member(auth_user_id)
    
    return {}
     
@helpers.save_data
@helpers.unwrap_token
def channel_addowner_v1(auth_user_id, channel_id, u_id):
    """Adds a user as an owner of a channel
    Args:
        auth_user_id (int): user ID of user performing action
        channel_id (int): channel ID
        u_id (int): user ID to be added as owner

    Raises:
        AccessError: Auth user ID invalid
        AccessError: Auth user doesn't have permission to do this
        InputError: Channel ID invalid
        InputError: User already channel owner
    """

    auth_u = state.s.users.get(auth_user_id)

    
    # Check the channel id is valid
    ch = state.s.channels.get(channel_id)
    
    # Check auth_user has permission
    if not (auth_u.is_admin() or ch.is_owner(auth_user_id)):
        raise AccessError(description="You don't have admin permissions in this channel")
    
    # Check the user ID is valid
    state.s.users.get(u_id)
    
    if ch.is_owner(u_id):
        raise InputError(description="That user is already a channel owner")
    
    # Add user as owner
    ch.add_owner(u_id)
    
    return {}

@helpers.save_data
@helpers.unwrap_token
def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    """Removes a user as an owner of a channel

    Args:
        auth_user_id (int): user ID of user performing action
        channel_id (int): channel ID
        u_id (int): user ID to be removed as owner

    Raises:
        AccessError: Auth user ID invalid
        AccessError: Auth user doesn't have permission to do this
        InputError: Channel ID invalid
        InputError: User already channel owner
    """
    


    auth_u = state.s.users.get(auth_user_id)

    
    # Check the channel id is valid
    ch = state.s.channels.get(channel_id)
    
    # Check auth_user has permission
    if not (auth_u.is_admin() or ch.is_owner(auth_user_id)):
        raise AccessError(description="You don't have admin permissions in this channel")
    
    # Check the user ID is valid
    state.s.users.get(u_id)
    
    if not ch.is_owner(u_id):
        raise InputError(description="That user isn't a channel owner")
    
    # Add user as owner
    ch.remove_owner(u_id)
        
    return {}

from . import state
