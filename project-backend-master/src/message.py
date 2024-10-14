"""src > message.py

Implements functions for interacting with a message, as well as the data 
structures for storing all of them.

Primary Contributors: 
 - Danny Won [z5338486@ad.unsw.edu.au]
     - Message data structure and data structure helper functions

Minor Contributors:
 - [None]

"""


import datetime

from . import consts, bots


from .error import AccessError, InputError
from .generic_data import GenericData, GenericDataContainer

class Message(GenericData):
    """Message data structure
    """
    _contained_type_str = "Message"
    def __init__(self, sender_id: int, channel_id: int, message: str, quote_msg_id=None, send_time=None) -> None:
        """Create a new message and add it to the database

        Args:
            sender_id (int): user id of sender
            channel_id (int): dm/channel id where it is sent
            message (str): raw message as string
            quote_msg_id (int, optional): id of message this is quoting. Defaults to None.
            send_time (datetime): time that the message will be sent at (defaults to None;
                                meaning it will be sent now)
            is_pinned(bool): whether the message is pinned or not. Defaults to False.

        Raises:
            InputError: Message is empty or too long
            AccessError: User doesn't have access to channel
        """
        super().__init__()
        self._sender = sender_id
        self._channel = channel_id
        self._message = helpers.EncodedString(message, quote_msg_id)
        if send_time is None:
            self._time = datetime.datetime.now()
        else:
            self._time = send_time
        self._is_pinned = False
        self._reacts = list()
        
        # List of notifications associated with notification
        self._associated_notifs = []
        self._react_associated_notifs = []
        
        # Add to user
        state.s.users.get(self._sender).add_message(self._id)
        
        # Add to database
        state.s.messages.add(self)

        # Add to channel
        abstract_channel.get_abstract_channel_by_id(channel_id).add_message(self._id)
        
        # Send notifications for all users we tagged
        self._update_tags()
        
        # Add entry to stats
        state.s.stats.add_messages_entry(1)

    def remove(self):
        """Delete a message, and remove all its references
        """
        
        # Remove message from channel
        ch = abstract_channel.get_abstract_channel_by_id(self._channel)
        ch.remove_message(self._id)
        
        # Remove message from user
        sender = state.s.users.get(self._sender)
        sender.remove_message(self._id)
        
        # Remove all associated notifications
        for notif_id in self._associated_notifs:
            state.s.notifications.get(notif_id)
            state.s.notifications.remove(notif_id)

        for notif_id in self._react_associated_notifs:
            state.s.notifications.get(notif_id)
            state.s.notifications.remove(notif_id)
        
        # Add entry to stats
        state.s.stats.add_messages_entry(-1)
    
    def _update_tags(self):
        """Update tagged users. Called when message is created or edited
        """
        new_associated_notifs = []
        
        new_tags = self._message.get_tagged_users()
        notif_str = get_tag_notif_str(state.s.users.get(self._sender), 
                                      abstract_channel.get_abstract_channel_by_id(self._channel), 
                                      str(self))
        # Loop through all existing tags
        for notif_id in self._associated_notifs:
            notif = state.s.notifications.get(notif_id)
            # If user in new tags, update their notification string
            # Otherwise remove their notification
            if notif.get_affected_user() in new_tags:
                # Make sure we encode the notification text, otherwise the tags won't update
                notif.update(notif_str)
                # Remove them from the list of new tags
                new_tags.discard(notif.get_affected_user())
                new_associated_notifs.append(notif_id)
            else:
                state.s.notifications.remove(notif_id)
        
        # Loop through any new tags. Add new notifications for all of them
        for u_id in new_tags:
            # Can't have sender tagging themselves
            if u_id == self._sender: continue
            
            notif = notification.Notification(u_id, self._channel, -1, notif_str)
            new_associated_notifs.append(notif.get_id())
    
        # Replace associated notifications list with new one
        self._associated_notifs = new_associated_notifs

    def edit(self, new_msg: str):
        """Edit the contents of a message

        Args:
            new_msg (str): New message contents
        
        Raises:
            InputError: message too long
        """
        # Set the message
        self._message.update(new_msg)
        
        self._update_tags()

    def change_is_pinned(self):
        """Add a react to the reacts dict of a message
        """
        self._is_pinned = not self.is_pinned()

    def add_react(self, react_id: int, u_id: int):
        """Add a react to the reacts dict of a message

        Args:
            react_id (int): The react's id
            u_id (int): the id of a user who wants to add the react 
        """
        # Add u_id to the react dict if the dict for the react_id has been created.
        react_added = False
        for i in self._reacts:
            if react_id == i["react_id"]:
                # Raise InputError if the react is already added by the user
                if u_id in i["u_ids"]:
                    raise InputError(description="You've already reacted in this way")
                i["u_ids"].append(u_id)
                react_added = True
        # Create react_dict if it does not exist for the react_id.
        if not react_added:
            react_dict = {
                "react_id": react_id,
                "u_ids": [u_id],
                "is_this_user_reacted": None
            }
            self._reacts.append(react_dict)
        # Add notification for react
        notif_str = get_react_notif_str(state.s.users.get(self._sender), abstract_channel.get_abstract_channel_by_id(self._channel))
        notif = notification.Notification(self.get_sender_id(), self._channel, -1, notif_str)
        self._react_associated_notifs.append(notif.get_id())

    def remove_react(self, react_id: int, u_id: int):
        """Remove a react from the reacts dict of a message

        Args:
            react_id (int): The react's id
            u_id (int): the id of a user who wants to remove the react 
        """
        react_removed = False
        for i in range(len(self._reacts)):
            # Find the user's react
            if react_id == self._reacts[i]["react_id"]:
                if u_id in self._reacts[i]["u_ids"]:
                    # Remove it
                    self._reacts[i]["u_ids"].remove(u_id)
                    # If the type of reacts is not used by any user, remove it for the message
                    if self._reacts[i]["u_ids"] == []:
                        self._reacts.pop(i)
                    react_removed = True
        # Raise InputError if the user's react doesn't exist
        if react_removed == False:
            raise InputError(description="You haven't reacted to this")
        for notif_id in self._react_associated_notifs:
            notif = state.s.notifications.get(notif_id)
            if notif.as_dict()["notification_message"] == get_react_notif_str(state.s.users.get(self._sender), abstract_channel.get_abstract_channel_by_id(self._channel)):
                state.s.notifications.remove(notif_id)

    def as_dict(self) -> dict:
        """Return the object's important features as a dict (as per spec)

        Returns:
            dict: message dict
        """
        data = {}
        data["message_id"] = self._id
        data["u_id"] = self._sender
        data["message"] = str(self._message)
        data["time_created"] = self.get_timestamp()
        data["is_pinned"] = self.is_pinned()
        data["reacts"] = self.get_reacts()

        return data
    
    def get_timestamp(self) -> int:
        """Returns unix timestamp of when the message was sent

        Returns:
            int: timestamp
        """
        return int(self._time.timestamp())

    def get_sender_id(self) -> int:
        """Returns the ID of the message's sender

        Returns:
            int: user ID
        """
        return self._sender

    def get_channel_id(self) -> int:
        """Returns the ID of the channel the message was sent in

        Returns:
            int: channel/dm ID
        """
        return self._channel

    def is_pinned(self) -> bool:
        """Returns the reacts dict of the message
        """
        return self._is_pinned

    def get_reacts(self) -> dict:
        """Returns the reacts dict of the message

        Returns:
            dict: reacts
        """
        return self._reacts

    def __str__(self) -> str:
        """Stringifies to pain message text

        Returns:
            str: message text
        """
        return str(self._message)
    
    def __len__(self) -> int:
        """Returns the length of the message

        Returns:
            int: message length
        """
        return len(str(self))
    
    def __int__(self) -> int:
        """Returns Message identifier

        Returns:
            int: id
        """
        return self.get_id()
    
    def __eq__(self, o: object) -> bool:
        """Checks message equality. For strings, this compares against the 
        decoded message contents. For Message types and ints, it compares by
        id.

        Args:
            o (object): object to compare

        Returns:
            bool: equality
        """
        if isinstance(o, Message):
            return self._id == o._id
        elif isinstance(o, int):
            return self._id == o
        else:
            return self._message == o
    
    def __lt__(self, o: object) -> bool:
        """Returns whether this message was sent before another event.
        Note that this differs from the behaviour of the __eq__() method, which
        checks for equality between messages.

        Args:
            o (Message): message to compare

        Returns:
            bool: whether this message was sent first
        """
        if isinstance(o, Message):
            return self._time < o._time
        if isinstance(o, datetime.datetime):
            return self._time < o
        else:
            return NotImplemented

class MessageContainer(GenericDataContainer):
    """Container for messages
    """
    def get(self, get_id: int) -> Message:
        return super().get(get_id)

from src import abstract_channel, channel
from src import notification
from src import helpers

@helpers.save_data
@helpers.unwrap_token
def message_send_v1(auth_user_id, channel_id, message):
    """Send a message in a channel

    Args:
        auth_user_id (int): User ID of the user sending the message
        channel_id (int): Channel ID of the channel it's being sent in
        message (str): message contents: (must be 0 < len <= 1000 chars)

    Raises:
        AccessError: User doesn't have access to channel
        InputError: User or channel don't exist; message is too long or too short

    Returns:
        dict: "message_id": [int] message ID of newly sent message
    """
    msg = send_message_generic(auth_user_id, channel_id, message)
    

    return {"message_id": msg.get_id()}

@helpers.save_data
@helpers.unwrap_token
def message_send_later_v1(auth_user_id, channel_id, message, send_time):
    """Send a message in a channel

    Args:
        auth_user_id (int): User ID of the user sending the message
        channel_id (int): Channel ID of the channel it's being sent in
        message (str): message contents: (must be 0 < len <= 1000 chars)
        send_time (datetime): time that the message will be sent at


    Raises:
        AccessError: User doesn't have access to channel
        InputError: User or channel don't exist; message is too long or too short

    Returns:
        dict: "message_id": [int] message ID of newly sent message
    """
    send_time = datetime.datetime.fromtimestamp(send_time)
    curr_time = datetime.datetime.now()
    if send_time < curr_time:
        raise InputError(description=f"Your selected time ({send_time}) is before the present ({curr_time})")

    msg = send_message_generic(auth_user_id, channel_id, message, None, send_time)
    
    return {"message_id": msg.get_id()}

def send_message_generic(auth_user_id: int, channel_id: int, message: str, og_message=None, send_time=None) -> Message:
    """Performs generic checks before returning a new Message object

    Args:
        auth_user_id (int): sender's id
        channel_id (int): channel/dm id
        message (str): message to send
        og_message (int, optional): message to quote, defaults to None
        send_time (datetime): time that the message will be sent at (defaults to None;
                                meaning it will be sent now)

    Raises:
        InputError: Message too long/short
        AccessError: User doesn't have access to channel/dm

    Returns:
        Message: new message
    """
    # Check for input errors
    ch = abstract_channel.get_abstract_channel_by_id(channel_id)
    if len(message) > consts.MESSAGE_MAX_LEN: # Message over maximum length
        raise InputError(description=f"Message ({len(message)} characters) is too long (max {consts.MESSAGE_MAX_LEN} characters)")
    # Message has len 0 and we're not quoting
    elif len(message) == 0 and og_message is None: 
        raise InputError(description="Message is empty")

    if not ch.is_member(auth_user_id):
        raise AccessError(description="You aren't a member of this channel")
    
    msg = Message(auth_user_id, channel_id, message, og_message, send_time)
    
    # Notify bots that a message was sent
    bots.on_message_send(msg.get_id())
    
    return msg

@helpers.save_data
@helpers.unwrap_token
def message_remove_v1(auth_user_id, message_id):
    """Removes a message sent by a user

    Args:
        auth_user_id (int): id of user whose message should be deleted
        message_id (int): id of message to be deleted

    Raises:
        AccessError: Message wasn't sent by the user
        InputError: User or message don't exist

    Returns:
        dict: [empty]
    """

    usr = state.s.users.get(auth_user_id)

    # Search for message: will raise InputError if none found
    # We don't need this
    msg = state.s.messages.get(message_id)
    
    # Get channel message was sent in
    ch = abstract_channel.get_abstract_channel_by_id(msg.get_channel_id())
    
    # If user attempting edit didn't send the message
    # or isn't a channel admin
    if not (msg.get_sender_id() == auth_user_id or usr.is_admin()):
        exc_no_permission =\
            "Either you didn't send this message or you don't have admin permissions in this channel"
        # We can only check for channel admin-ness if it's a Channel (not a DM)
        if isinstance(ch, channel.Channel):
            if not ch.is_owner(auth_user_id):
                raise AccessError(description=exc_no_permission)
        else:
            raise AccessError(description=exc_no_permission)

    # Remove message from list of messages that have been sent
    state.s.messages.remove(message_id)

@helpers.save_data
@helpers.unwrap_token
def message_edit_v1(auth_user_id, message_id, message, token=""):
    """Edit an existing message sent by a user. If the new string is empty
    the message is deleted.

    Args:
        auth_user_id (int): User ID
        message_id (int): ID of message to edit
        message (str): What to edit the message to
        token (str): Token of user performing action

    Raises:
        AccessError: Message wasn't sent by user requesting the edit
        InputError: Message or user don't exist; message is too long

    Returns:
        dict: [empty]
    """
    
    # If it's empty, delete the message instead
    # -> redirect to message_remove_v1
    # Assume that it will correctly remove messages
    if message == "":
        return message_remove_v1(token, message_id)

    usr = state.s.users.get(auth_user_id)

    # Search for message: will raise InputError if none found
    msg = state.s.messages.get(message_id)
    
    # Get channel message was sent in
    ch = abstract_channel.get_abstract_channel_by_id(msg.get_channel_id())
    
    # If user attempting edit didn't send the message
    # or isn't a channel admin
    if not (msg.get_sender_id() == auth_user_id or usr.is_admin()):
        exc_no_permission =\
            "Either you didn't send this message or you don't have admin permissions in this channel"
        # We can only check for channel admin-ness if it's a Channel (not a DM)
        if isinstance(ch, channel.Channel):
            if not ch.is_owner(auth_user_id):
                raise AccessError(description=exc_no_permission)
        else:
            raise AccessError(description=exc_no_permission)
    
    if len(message) > consts.MESSAGE_MAX_LEN: # Message over maximum length
        raise InputError(description=f"Message ({len(message)} characters) is too long (max {consts.MESSAGE_MAX_LEN} characters)")
    
    # Set the message
    msg.edit(message)
    

    return {}
    
@helpers.save_data
@helpers.unwrap_token
def message_share_v1(auth_user_id, og_message_id, message, channel_id, dm_id):
    """Share an existing message to a channel or a DM by a user.
    Args:
        auth_user_id (int): User ID
        og_message_id (int): ID of the original message
        message (str): the optional message in addition to the shared message
        channel_id (int): ID of the channel that the message is being shared to. 
            It is -1 if it is being sent to a DM
        dm_id (int): ID of the DM that the message is being shared to.
            It is -1 if it is being sent to a channel.

    Raises:
        AccessError: the authorised user has not joined the channel or DM they are trying to share the message to.

    Returns:
        dict: "shared_message_id": [int] new message ID of the shared message.
    """
    # Ensure OG message exists
    state.s.messages.get(og_message_id)

    # Get channel/dm to share to
    if channel_id != -1:
        ch = state.s.channels.get(channel_id)
    else:
        ch = state.s.dms.get(dm_id)
    
    if not ch.is_member(auth_user_id):
        raise AccessError(description="You aren't a member of this channel")
    # Create message
    msg = send_message_generic(auth_user_id, ch.get_id(), message, og_message_id)

    return {"shared_message_id": msg.get_id()}

@helpers.save_data
@helpers.unwrap_token
def message_react_v1(auth_user_id, message_id, react_id):
    """Given a message within a channel or DM the authorised user is part of, 
    add a "react" to that particular message

    Args:
        auth_user_id (int): User ID
        message_id (int): ID of the message
        react_id (int): ID of the react

    Raises:
        InputError: message don't exist
        InputError: react_id is not valid
        InputError: Message already contains an active React with ID react_id from the authorised user
        AccessError: The authorised user is not a member of the channel or DM that the message is within

    Returns:
        dict: [empty]
    """
    if react_id not in consts.VALID_REACT_IDS:
        raise InputError(description=f"That reaction (ID {react_id}) is invalid")

    msg = state.s.messages.get(message_id)
        
    ch = abstract_channel.get_abstract_channel_by_id(msg.get_channel_id())
    if not ch.is_member(auth_user_id):
        raise AccessError(description="You aren't a member of this channel")

    msg.add_react(react_id, auth_user_id)

    return {}

@helpers.save_data
@helpers.unwrap_token
def message_unreact_v1(auth_user_id, message_id, react_id):
    """Given a message within a channel or DM the authorised user is part of,
    remove a "react" to that particular message

    Args:
        auth_user_id (int): User ID
        message_id (int): ID of the message
        react_id (int): ID of the react

    Raises:
        InputError: message don't exist
        InputError: react_id is not valid
        InputError: Message doesn't contain an active React with ID react_id from the authorised user
        AccessError: The authorised user is not a member of the channel or DM that the message is within

    Returns:
        dict: [empty]
    """
    if react_id not in consts.VALID_REACT_IDS:
        raise InputError(description=f"That reaction (ID {react_id}) is invalid")

    msg = state.s.messages.get(message_id)
        
    ch = abstract_channel.get_abstract_channel_by_id(msg.get_channel_id())
    if not ch.is_member(auth_user_id):
        raise AccessError(description="You aren't a member of this channel")

    msg.remove_react(react_id, auth_user_id)

    return {}
    
@helpers.save_data
@helpers.unwrap_token
def message_pin_v1(auth_user_id, message_id):
    """Given a message within a channel or DM, mark it as "pinned" to be given special display treatment by the frontend.
    Args:
        auth_user_id (int): User ID
        message_id (int): ID of the message
    Raises:
        AccessError: the authorised user has not joined the channel/DM that the message is within.
        AccessError: the authorised user is not owner of the channel/DM that the message is within.
        InputError: message_id is not a valid message.
        InputError: message with ID message_id is already pinned
    Returns:
        dict: [empty]
    """
    # Search for message: will raise InputError if none found
    msg = state.s.messages.get(message_id)

    # Get channel message was sent in
    ch = abstract_channel.get_abstract_channel_by_id(msg.get_channel_id())
    
    # Raise AccessError for user not in the channel or not the channel's owner
    if not ch.is_member(auth_user_id):
        raise AccessError(description="You aren't a member of this channel")
    if not ch.is_owner(auth_user_id):
        raise AccessError(description="You don't have admin permissions in this channel")

    # Raise InputError if the message is pinned    
    if msg.is_pinned() == True:
        raise InputError(description="That message is already pinned")
    msg.change_is_pinned()
    return {}

@helpers.save_data
@helpers.unwrap_token
def message_unpin_v1(auth_user_id, message_id):
    """Given a message within a channel or DM, remove it's mark as unpinned
    Args:
        auth_user_id (int): User ID
        message_id (int): ID of the message
    Raises:
        AccessError: the authorised user has not joined the channel/DM that the message is within.
        AccessError: the authorised user is not owner of the channel/DM that the message is within.
        InputError: message_id is not a valid message.
        InputError: message with ID message_id is already unpinned
    Returns:
        dict: [empty]
    """
    # Search for message: will raise InputError if none found
    msg = state.s.messages.get(message_id)

    # Get channel message was sent in
    ch = abstract_channel.get_abstract_channel_by_id(msg.get_channel_id())
    
    # Raise AccessError for user not in the channel or not the channel's owner
    if not ch.is_member(auth_user_id):
        raise AccessError(description="You aren't a member of this channel")
    if not ch.is_owner(auth_user_id):
        raise AccessError(description="You don't have admin permissions in this channel")
        
    # Raise InputError if the message is unpinned   
    if msg.is_pinned() == False:
        raise InputError(description="That message is already unpinned")
    msg.change_is_pinned()
    return {}

def get_tag_notif_str(usr, channel: abstract_channel.AbstractChannel, message: str):
    """Generates notification message for tag

    Args:
        user (User): user object of tagger
        channel (AbstractChannel): channel where tag happened
        message (str): unencoded message string

    Returns:
        str: notification message
    """
    return f"@{usr.get_handle()} tagged you in {channel.get_name()}: {message[:20]}"

def get_react_notif_str(usr, channel: abstract_channel.AbstractChannel):
    """Generates notification message for react

    Args:
        user (User): user object of react
        channel (AbstractChannel): channel where reacted message is in

    Returns:
        str: notification message
    """
    return f"{usr.get_handle()} reacted to your message in {channel.get_name()}"

from . import state
