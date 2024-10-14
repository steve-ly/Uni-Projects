"""src > other.py

Implements other miscellaneous functions

Primary Contributors: 
 - Danny Won [z5338486@ad.unsw.edu.au]
     - clear_v1()

Minor Contributors:
 - [None]

"""
import os
import glob

import datetime

from src import helpers, consts
from src.error import InputError

@helpers.save_data
def clear_v1():
    """Resets all the internal data to a blank state, then saves the empty
    state to the data file
    """
    state.reset_state()
    
    # Also remove all resources associated with the state
    files = glob.glob(f"/{consts.STATE_RESOURCE_FOLDER}/*")
    for f in files: # pragma: no cover
        if "empty.txt" in f:
            continue
        os.remove(f)
    return {}


@helpers.unwrap_token
def search_v2(auth_user_id, query_str):
    """Given a query string, returns a collection of messages in all of the
    channels/DMs that the user has joined that match the query

    Args:
        auth_user_id (int): users unique ID
        query_str (str): string to match and find
    """
    # Return list
    matched_strings = {
        "messages": [],
    }

    # Check if query string is valid
    if query_str == "":
        raise InputError(description="Query is empty")
    if len(query_str) > consts.MESSAGE_MAX_LEN:
        raise InputError(description="Query is too long")
    
    # Get users channels (list of channel IDs user is part of)
    usr = state.s.users.get(auth_user_id)

    # Search through channels msgs and add them to return list
    channel_ids = usr.get_channels()
    for ch_id in channel_ids:
        ch = state.s.channels.get(ch_id)
        for msg in ch:
            if query_str == msg:
                matched_strings["messages"].append(msg.as_dict())

    # TODO: make this more generic
    # Search through DMs msgs and add them to return list
    dm_ids = usr.get_dms()
    for dm_id in dm_ids:
        dm_obj = state.s.dms.get(dm_id)
        for msg in dm_obj:
            if query_str == msg:
                matched_strings["messages"].append(msg.as_dict())


    return matched_strings


from . import state

