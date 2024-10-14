import datetime
from . import state, helpers

class Stats:
    def __init__(self, is_user: bool):
        self._extra_key = "joined" if is_user else "exist"
        self._extra_key_m = "sent" if is_user else "exist"
        self.channels = []
        self.dms = []
        self.messages = []

    def add_channels_entry(self, increment):
        initial = 0 if len(self.channels) == 0 else self.channels[0][f"num_channels_{self._extra_key}"]
        channels_entry = {
            f"num_channels_{self._extra_key}": initial + increment,
            "time_stamp": datetime.datetime.now().timestamp(),
        }
        self.channels.insert(0, channels_entry)
    
    def add_dms_entry(self, increment):
        initial = 0 if len(self.dms) == 0 else self.dms[0][f"num_dms_{self._extra_key}"]
        dms_entry = {
            f"num_dms_{self._extra_key}": initial + increment,
            "time_stamp": datetime.datetime.now().timestamp(),
        }
        self.dms.insert(0, dms_entry)
    
    def add_messages_entry(self, increment):
        initial = 0 if len(self.messages) == 0 else self.messages[0][f"num_messages_{self._extra_key_m}"]
        messages_entry = {
            f"num_messages_{self._extra_key_m}": initial + increment,
            "time_stamp": datetime.datetime.now().timestamp(),
        }
        self.messages.insert(0, messages_entry)
    
    def get_channels_data(self):
        return self.channels
    
    def get_dms_data(self):
        return self.dms
    
    def get_messages_data(self):
        return self.messages

@helpers.unwrap_token
def dreams_stats_v1(auth_user_id):
    """Fetches statistics about the use of UNSW Dreams

    Returns:
        dict: stats on Dreams including the number of channels that 
        currently exist, the number of dms that exist, the number of
        messages that exist and the workspace's utilization.
    """
    users_in_channels_or_dms = 0
    for user_tag in state.s.users:
        if len(user_tag.get_channels()) > 0 or len(user_tag.get_dms()) > 0:
            users_in_channels_or_dms += 1
    
    # Check for divide by zero issues
    # This never happens since there is always one user if they were able to get this far
    """ if len(state.s.users) == 0:
        utilization_rate = 0
    else: """
    utilization_rate = users_in_channels_or_dms / len(state.s.users)

    dreams_stats = {
        "channels_exist": state.s.stats.get_channels_data(),
        "dms_exist": state.s.stats.get_dms_data(),
        "messages_exist": state.s.stats.get_messages_data(),
        "utilization_rate": utilization_rate,
    }

    return {"dreams_stats": dreams_stats}

@helpers.unwrap_token
def user_stats_v1(u_id):
    """Fetches the required statistics about a user's use of UNSW Dreams

    Args:
        u_id (int): user id to get stats on
    
    Returns:
        dict: users stats including channels joined, dms joined, messages sent
    and involvement rate
    """
    usr = state.s.users.get(u_id)

    stats = usr.get_stats()

    # Check for divide by zero issues
    if sum([len(state.s.channels), len(state.s.dms), \
        len(state.s.messages)]) == 0:
        involvement_rate = 0
    else:
        involvement_rate =\
            sum([len(usr.get_channels()), len(usr.get_dms()), len(usr.get_messages())])\
                / sum([len(state.s.channels), len(state.s.dms), len(state.s.messages)])

    user_stats = {
        "channels_joined": stats.get_channels_data(),
        "dms_joined": stats.get_dms_data(),
        "messages_sent": stats.get_messages_data(),
        "involvement_rate": involvement_rate,
    }

    return {"user_stats": user_stats}
