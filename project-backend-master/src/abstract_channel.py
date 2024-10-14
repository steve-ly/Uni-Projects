"""src > abstract_channel.py

This file contains the definition for the abstract channel type, from which
the classes Channel and Dm are both derived

Author:
    Miguel Guthridge [z5312085@ad.unsw.edu.au]

"""

import datetime

from .error import InputError
from .generic_data import GenericData

class AbstractChannel(GenericData):
    """Abstract type for channel
    """
    _contained_type_str = "Abstract Channel"
    def __init__(self):
        """Creates an abstract channel type. Only call this
        """
        super().__init__()
        self._messages = []
        self._members = set()
    
    def remove(self):
        """Deletes an abstract channel type.
        """
        
        # Remove all messages from it
        [state.s.messages.remove(m) for m in self.get_messages()]
        
        # Remove all users from it
        [self.remove_member(u) for u in self.get_members()]
    
    def __len__(self) -> int:
        """Returns the number of messages in a channel
        """
        return len(self._messages)
    
    def __iter__(self):
        """Return iterator over channel's messages

        Returns:
            AbstractChannelIterator: iterator
        """
        return AbstractChannelIterator(self)
    
    def __int__(self) -> int:
        """Return channel's id

        Returns:
            int: id
        """
        return self._id
    
    def as_dict(self) -> dict:
        """Return dictionary representation of channel

        Returns:
            dict: channel info
        """
        return {
            "name": self.get_name(),
            "members": [state.s.users.get(u).as_dict() for u in self.get_members()]
        }
    
    def __eq__(self, o: object) -> bool:
        """Return whether channels are referring to the same channe;

        Args:
            o (Channel): channel to compare

        Returns:
            bool: equality
        """
        if isinstance(o, AbstractChannel):
            return self.get_id() == o.get_id()
        else:
            return NotImplemented
    
    def get_name(self):
        """Get the name of the channel

        Returns:
            NotImplemented
        """
        return NotImplemented
    
    def get_message(self, i: int) -> int:
        """Gets the message id of the message at index i, where the most recent
        message is 0

        Args:
            i (int): index to get

        Returns:
            int: message id
        """
        return self._messages[i]
    
    def get_messages(self) -> list:
        """Returns list of message IDs in channel

        Returns:
            list (int): message IDs
        """
        # Return only msgs that arent delayed
        ret = []
        curr_time = datetime.datetime.now()
        for msg_id in self._messages:
            msg = state.s.messages.get(msg_id)
            if msg < curr_time:
                # # Insert at correct time
                # inserted = False
                # for i in range(len(ret)):
                #     if msg.get_timestamp() < ret[i].get_timestamp():
                #         ret.insert(i, msg)
                #         inserted = True
                #         break
                # if not inserted:
                #     ret.append(msg)
                ret.append(msg)
        return ret
    
    def get_paged_messages(self, start: int) -> dict:
        """Get chronologically previous 50 messages from start index

        Args:
            start (int): index to start at

        Raises:
            InputError: Invalid start index

        Returns:
            dict: paged messages
        """
        # Create a dict has the 50 messages from index "start" to "start + 50"
        msgs = {}

        # Check the start index is smaller than the number of messages
        if start > len(self):
            raise InputError(description=f"Start index ({start}) is too high (max: {len(self)})")

        # Add the messages to the return dict
        # Ensure that we don't try to slice past the end
        msgs["messages"] = [m.as_dict() for m in
            self.get_messages()[start : min(start + 50, len(self))]]
        msgs["start"] = start
        # If the least recent messages is returned, the end index is -1.
        msgs["end"] = -1 if start + 50 >= len(self) else start + 50
        
        return msgs
    
    def add_message(self, msg_id: int):
        """Add a message to the channel

        Args:
            msg_id (int): message ID to add
        """
        if len(self._messages) > 0:
            i = 0
            inserted = False
            while not inserted and i < len(self._messages):
                msg = state.s.messages.get(self._messages[i])
                if msg < state.s.messages.get(msg_id):
                    self._messages.insert(i, msg_id)
                    inserted = True
                i += 1
            if i == len(self._messages) and inserted == False:
                self._messages.append(msg_id)
        else:
            self._messages.insert(0, msg_id)

    
    def remove_message(self, msg_id: int):
        """Remove a message from the channel

        Args:
            msg_id (int): message ID to remove
        """
        self._messages.remove(msg_id)
    
    def get_members(self) -> list:
        """Returns the list of members (as user IDs)

        Raises:
            StopIteration: [description]

        Returns:
            list (int): user IDs of members
        """
        return list(self._members)
    
    def is_member(self, u_id: int) -> bool:
        """Return whether a user is a channel member

        Args:
            u_id (int): user id to check
        
        Returns:
            bool: whether they are a member
        """
        return u_id in self._members
    
    def add_member(self, u_id: int):
        """Add a user to channel
        NoteL doesn't add to user's data (left up to derived classes)

        Args:
            u_id (int): user id to add
        """
        # Check that the user hasn't been deleted
        state.s.users.get(u_id).check_deletion()
        # Add them
        self._members.add(u_id)
    
    def remove_member(self, u_id: int):
        """Remove a user from the channel
        Note: doesn't remove from user's data (left up to derived classes)

        Args:
            u_id (int): user id to remove
        """
        self._members.remove(u_id)

from . import message

class AbstractChannelIterator:
    """Iterates over the messages of a channel/dm
    """
    def __init__(self, channel: AbstractChannel) -> None:
        """Create iterator

        Args:
            channel (AbstractChannel): channel to iterate over
        """
        self._index = 0
        self._channel = channel

    def __next__(self) -> message.Message:
        """Get next item in iteration
        """
        try:
            msgs = self._channel.get_messages()
            ret = msgs[self._index]
            self._index += 1
            return ret
        except IndexError:
            raise StopIteration() from None
        
def get_abstract_channel_by_id(c_id: int) -> AbstractChannel:
    """Returns a generic channel object given the ID of either a DM or a channel

    Args:
        c_id (int): id of DM or channel

    Returns:
        AbstractChannel: channel object
    """
    try:
        return state.s.channels.get(c_id)
    # If this fails, then it's a DM
    except InputError:
        # This will raise it's own InputError
        return state.s.dms.get(c_id)

from . import state
