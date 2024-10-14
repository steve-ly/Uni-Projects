import pytest

from . import helpers
from . import call_wrappers as cw
from src.error import InputError, AccessError

def test_dreams_stats_empty():
    cw.clear()
    usr = helpers.one_user()
    stats = cw.users_stats(usr["token"])["dreams_stats"]
    
    assert len(stats["channels_exist"]) == 0
    assert len(stats["dms_exist"]) == 0
    assert len(stats["messages_exist"]) == 0
    
def test_dream_remove_stats():
    cw.clear()
    users = helpers.two_users()
    u_ids = [users[0]["auth_user_id"], users[1]["auth_user_id"]]

    ch_id = cw.channels_create(users[0]["token"], "Channel 1", True)["channel_id"]
    dm_id = cw.dm_create(users[0]["token"], u_ids)["dm_id"]
    m_id = cw.message_send(users[0]["token"], ch_id, "Miguel is cool")["message_id"]

    dream_stats = cw.users_stats(users[0]["token"])["dreams_stats"]

    assert dream_stats["channels_exist"][0]["num_channels_exist"] == 1
    assert dream_stats["dms_exist"][0]["num_dms_exist"] == 1
    assert dream_stats["messages_exist"][0]["num_messages_exist"] == 1
    assert dream_stats["utilization_rate"] == 1

    cw.channel_leave(users[0]["token"], ch_id)
    cw.dm_remove(users[0]["token"], dm_id)
    cw.message_remove(users[0]["token"], m_id)

    dream_stats = cw.users_stats(users[0]["token"])["dreams_stats"]

    assert dream_stats["channels_exist"][0]["num_channels_exist"] == 1
    assert dream_stats["dms_exist"][0]["num_dms_exist"] == 0
    assert dream_stats["messages_exist"][0]["num_messages_exist"] == 0
    assert dream_stats["utilization_rate"] == 0.0

def test_user_stats_none():
    cw.clear()
    usr = helpers.one_user()
    
    usr_stats = cw.user_stats(usr["token"])["user_stats"]
    
    assert len(usr_stats["channels_joined"]) == 0
    assert len(usr_stats["dms_joined"]) == 0
    assert len(usr_stats["messages_sent"]) == 0
    assert usr_stats["involvement_rate"] == 0

def test_user_stats_add():
    cw.clear()
    users = helpers.two_users()
    u_ids = [users[0]["auth_user_id"], users[1]["auth_user_id"]]
    
    ch_id = cw.channels_create(users[0]["token"], "Channel 1", True)["channel_id"]
    cw.dm_create(users[0]["token"], u_ids)["dm_id"]
    cw.message_send(users[0]["token"], ch_id, "Miguel is cooler")["message_id"]
    
    usr_stats = cw.user_stats(users[0]["token"])["user_stats"]
    
    assert len(usr_stats["channels_joined"]) == 1
    assert len(usr_stats["dms_joined"]) == 1
    assert len(usr_stats["messages_sent"]) == 1
    assert usr_stats["involvement_rate"] == 1

def test_user_stats_invalid_token():
    cw.clear()
    helpers.one_user_one_channel()
    with pytest.raises(AccessError):
        cw.user_stats(11111)

def test_dreams_stats_invalid_token():
    cw.clear()
    helpers.one_user_one_channel()
    with pytest.raises(AccessError):
        cw.users_stats(11111)