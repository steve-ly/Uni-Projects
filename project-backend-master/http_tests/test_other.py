import pytest

from . import call_wrappers as cw
from . import helpers
from src.error import InputError, AccessError


def test_clear():
    cw.auth_register("newperson@example.com", "Password1", "John", "Doe")
    cw.clear()
    user = cw.auth_register("newperson@example.com", "Password1", "John", "Doe")
    assert len(user) == 2
    assert isinstance(user["token"], str)
    assert isinstance(user["auth_user_id"], int)



def test_search():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    cw.message_send(user["token"],channel["channel_id"],"Yo")
    query = cw.search(user["token"],"Yo")
    assert query["messages"][0]["message"] == "Yo"

def test_search_query_too_long():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    cw.message_send(user["token"],channel["channel_id"],"Yo")
    with pytest.raises(InputError):
        cw.search(user["token"],"Thefitnessgrampacertest"*100)
        
def test_search_invalid_token():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    cw.message_send(user["token"],channel["channel_id"],"Yo")
    with pytest.raises(AccessError):
        cw.search(11111,"Yo")

