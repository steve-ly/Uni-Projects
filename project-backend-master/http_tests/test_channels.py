import pytest

from . import call_wrappers as cw
from . import helpers
from src.error import InputError, AccessError




def test_channels_create():
    cw.clear()
    user = helpers.one_user()
    c_id = cw.channels_create(user["token"],"Hello",True)
    print(c_id)
    assert isinstance(c_id["channel_id"], int)
    
def test_channel_name_too_long():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(InputError):
        cw.channels_create(user["token"],"abcdefghijklmnopqrstuvwxyz12324",True)

def test_channel_create_invalid_token():
    cw.clear()
    with pytest.raises(AccessError):
        cw.channels_create(123123,"Hello",True)



def test_channels_list():
    cw.clear()
    user = helpers.one_user()
    c_id = helpers.one_channel(user["token"])
    assert cw.channels_list(user["token"]) == {"channels":[{"channel_id": c_id["channel_id"],"name":"Channel 1"}]}


def test_channels_invalid_token_list():
    cw.clear()
    user = helpers.one_user()
    helpers.one_channel(user["token"])
    with pytest.raises(AccessError):
        cw.channels_list(123)


def test_channels_all():
    cw.clear()
    user = helpers.one_user()
    c_id = helpers.two_channels(user["token"])
    
    assert cw.channels_listall(user["token"]) == {"channels":[{"channel_id": c_id[0]["channel_id"],"name":"Channel 1"},{"channel_id": c_id[1]["channel_id"],"name":"Channel 2"}]}

def test_channeles_invalid_token_all():
    cw.clear()
    user = helpers.two_users()
    helpers.two_channels(user[0]["token"])
    with pytest.raises(AccessError):
        cw.channels_listall(123)

