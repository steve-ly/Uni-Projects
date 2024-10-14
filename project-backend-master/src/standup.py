"""Contains functions for creating and managing standups for the provided routes

With the exception of checking whether a standup is active, all these functions
redirect to message_send functions

"""

from . import helpers, message, state, error
from .bots import standup_bot

def get_standup_bot() -> standup_bot.StandupBot:
    """Returns a reference to the standup bot
    """
    return state.s.bots.get_by_name("Standup")

@helpers.save_data
def standup_start_v1(token: str, channel_id: int, length: int):
    """Start a standup, redirects to create a message command

    Args:
        auth_user_id (int): user id of standup creator
        channel_id (int): channel to create in
        length (int): time to run standup for (in seconds)
        token (str): token to forward
    """
    # Ensure that there aren't any active standups in progress
    standups = get_standup_bot()
    
    
    # Create standup by sending command (as per other bots)
    # This will ensure valid channel
    # And that the user is a member
    message.message_send_v1(token, channel_id, f"/standup {length}")
    
    # Get standup bot, and return time finish
    standups = get_standup_bot()
    finish = int(standups.query_standup(channel_id))
    return {"time_finish": finish}

@helpers.unwrap_token
def standup_active_v1(auth_user_id: int, channel_id: int):
    """Returns whether a standup is active in a channel, and the time that the
    standp finishes

    Args:
        auth_user_id (int): user id making the query
        channel_id (int): channel to query
    """
    standups = get_standup_bot()
    
    # Ensure channel is valid
    state.s.channels.get(channel_id)
    
    # Get time standup finishes
    finish = standups.query_standup(channel_id)
    
    return {
        "is_active": (finish is not None),
        "time_finish": int(finish) if finish is not None else finish
    }

def standup_send_v1(token: str, channel_id: int, msg: str):
    """Sends message in a channel when a standup is active.
    Forwards to message_send_v1

    Args:
        token (str): user token
        channel_id (int): channel to send message in
        msg (str): message contents
    """
    
    # Get standup bot, and ensure standup is active
    standups = get_standup_bot()
    finish = standups.query_standup(channel_id)
    if finish is None:
        raise error.InputError(description="A stand-up isn't currently active in this channel")
    
    message.message_send_v1(token, channel_id, msg)
    
    return {}
