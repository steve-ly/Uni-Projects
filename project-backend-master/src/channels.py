"""src > channels.py

Provides functions for interacting with channels

Primary Contributors: 
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]
     - channels_list_v1()
     - channels_listall_v1()
     - channels_create_v1()

Minor Contributors:
 - [None]

"""


from src import error, channel, helpers

@helpers.unwrap_token
def channels_list_v1(auth_user_id):
    '''Lists all the channels, and the associated details, that 
    the authorised user is part of.

    Arguments:
        auth_user_id ( int ): the authorised user's id
    
    Exceptions:
        InputError: Occurs when user's id is invalid
    
    Returns:
        dict: A dict of all the channels a user is a member of
            and their details

    '''
    u = state.s.users.get(auth_user_id)


    # For each channel the user is a member of
    # Add its info to a list
    ret = []
    for c_id in u.get_channels():
        c = state.s.channels.get(c_id)
        ret.append({"channel_id": c_id, "name": c.get_name()})
    
    # Return the list
    return {"channels": ret}

@helpers.unwrap_token
def channels_listall_v1(auth_user_id):
    """Provides a list of all channels and their associated
    details.

    Arguments:
        auth_user_id ( int ): the authorised user's id

    Raises:
        AccessError: Occurs when user's id is invalid

    Returns:
        dict: A dict of all the channels and their details

    """
    ret = []
    
    for c in state.s.channels:
        ret.append({"channel_id": c.get_id(), "name": c.get_name()})
    
    return {"channels": ret}

@helpers.save_data
@helpers.unwrap_token
def channels_create_v1(auth_user_id, name, is_public):
    """Creates a new channel with the given name and is set
    to public or private.

    Arguments:
        auth_user_id ( int ): the authorised user's id
        name ( str ): the name given to the new channel
        is_public ( bool ): a boolean for public or private channel

    Raises:
        AccessError: Occurs when user's id is invalid
        InputError: Occurs when the channels name is too long

    Returns:
        dict: channel ID
    """
    
    if len(name) > 20:
        raise error.InputError(description=f"Channel name ({len(name)} characters) is too long (max 20 characters)")
    
    ch = channel.Channel(name, auth_user_id, is_public)
    
    # Return the channel ID
    return {"channel_id": ch.get_id()}

from . import state
