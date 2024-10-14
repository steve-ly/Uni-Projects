"""src > state.py

Contains functions for saving the state of the entire program so that it can 
be reset to an old state if required (eg during testing)

Primary Contributors: 
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]

Minor Contributors:
 - [None]

"""

import copy
import pickle

from . import consts

class Data:
    def __init__(self):
        self._identifiers = set([0])
        
        # Initialise front-facing data containers
        self.users = user.UserContainer(user.User)
        self.channels = channel.ChannelContainer(channel.Channel)
        self.messages = message.MessageContainer(message.Message)
        self.sessions = session.SessionContainer(session.Session)
        self.notifications = notification.NotificationContainer(notification.Notification)
        self.dms = dm.DmContainer(dm.Dm)
        self.password_requests = auth.PasswordRequestContainer(auth.PasswordRequest)
        
        self.bots = bots.BotContainer(bots.Bot)
        self.commands = bots.CommandLinker()
        
        self.stats = stats.Stats(False)
        
def get_state(unsafe=False):
    """Gets/copies the current state of the internal data
    i.e unique id's, users, channls and messages.

    Args:
        unsafe (bool): whether the state should be referenced rather than 
            copied (faster but unsafe). Only use this if you won't modify the
            data, and aren't keeping the data beyond this event.

    Returns:
        dict: a copy of the current internal data
    """
    if unsafe:
        return s
    
    return copy.deepcopy(s)

def set_state(new_state):
    """Sets/imports a previously saved date set into the
    current internal data.

    Args:
        state ( dict ): previous saved data
    """
    global s
    s = copy.deepcopy(new_state)

def reset_state():
    """Resets/deletes the current internal data such as
    unique id's, users, channels and messages back to empty
    dicts.
    
    NOTE: This does NOT clear the data stored in state.pickle
    In order to clear that, call other.clear_v1() instead
    """

    global s
    s = Data()
    bots.initialise()
    bots.activate_bot("Activator")
    bots.activate_bot("Standup")


def save_state():
    """Save the current state of the server to the disk as Pickled data.
    """
    with open(consts.STATE_FILE, "wb") as file:
        pickle.dump(get_state(unsafe=True), file)

def load_state(): # pragma: no cover
    """Load the saved state from the disk, and replace the existing 
    state with it
    """
    with open(consts.STATE_FILE, "rb") as file:
        saved_state = pickle.load(file)
    
    set_state(saved_state)

# Define state variable to be imported
#s = None

# Import data at bottom of file so that all functions are properly registered
# before trying to create a circular import
from . import channel, user, message, notification, dm, session, bots, auth, stats
