import pytest

from . import call_wrappers as cw
from . import helpers
from src.error import InputError, AccessError
import time, datetime

def test_standup_start():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    standup = cw.standup_start(user["token"],channel["channel_id"],1)
    assert isinstance(standup["time_finish"], int)
    assert standup["time_finish"] == int(datetime.datetime.now().timestamp()) + 1

def test_standup_start_invalid_channel_id():
    cw.clear()
    user = helpers.one_user_one_channel()
    with pytest.raises(InputError):
        cw.standup_start(user[0]["token"],11111111,1)

def test_standup_start_active_standup():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    cw.standup_start(user["token"], channel["channel_id"], 5)
    with pytest.raises(InputError):
        cw.standup_start(user["token"], channel["channel_id"], 1)

def test_standup_start_unauthorised_user():
    cw.clear()
    _, channel = helpers.one_user_one_channel()
    user2 = cw.auth_register("kennyS@gmail.com","SecretPassword1","Iamtired","pleasereleaseme")
    with pytest.raises(AccessError):
        cw.standup_start(user2["token"],channel["channel_id"],1)

def test_standup_start_invalid_token():
    cw.clear()
    channel = helpers.one_user_one_channel()
    with pytest.raises(AccessError):
        cw.standup_start(111111,channel[1]["channel_id"],1)



def test_standup_active():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    standup = cw.standup_start(user["token"], channel["channel_id"],5)
    ret = cw.standup_active(user["token"], channel["channel_id"])
    assert ret["is_active"] == True
    assert ret["time_finish"] == standup["time_finish"]

def test_standup_active_invalid_channel():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    cw.standup_start(user["token"],channel["channel_id"],1)
    with pytest.raises(InputError):
        cw.standup_active(user["token"], 111111)

def test_standup_active_invalid_token():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    cw.standup_start(user["token"],channel["channel_id"],1)
    with pytest.raises(AccessError):
        cw.standup_active(111111, channel["channel_id"])



def test_standup_send():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    cw.standup_start(user["token"],channel["channel_id"],5)
    cw.standup_send(user["token"],channel["channel_id"],"Yo")
    #wait for length
    time.sleep(5)
    assert cw.channel_messages(user["token"],channel["channel_id"],0)["messages"][0]["message"] == "johndoe: Yo"

def test_standup_send_invalid_channel_id():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    cw.standup_start(user["token"],channel["channel_id"],5)
    with pytest.raises(InputError):
        cw.standup_send(user["token"],111111,"Yo")

def test_standup_send_message_too_long():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    cw.standup_start(user["token"],channel["channel_id"],5)
    with pytest.raises(InputError):
        cw.standup_send(user["token"],channel["channel_id"],"We're no strangers to love"*100)

def test_standup_send_message_too_no_standup():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    with pytest.raises(InputError):
        cw.standup_send(user["token"],channel["channel_id"],"DAyum")

def test_standup_send_message_non_member():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    cw.standup_start(user["token"],channel["channel_id"],5)
    user2 = cw.auth_register("Greatoutdoors@gmail.com","superhighlevel","Tatical","Visor")
    with pytest.raises(AccessError):
        cw.standup_send(user2["token"],channel["channel_id"],"biggus")

def test_standup_send_message_invalid_token():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    cw.standup_start(user["token"],channel["channel_id"],5)
    with pytest.raises(AccessError):
        cw.standup_send(1111111,channel["channel_id"],"biggus")
