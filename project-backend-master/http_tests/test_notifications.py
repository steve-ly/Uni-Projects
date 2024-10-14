from src import notification
import pytest

from . import call_wrappers as cw
from . import helpers
from src.error import InputError, AccessError


def test_notifications_get_channel():
    cw.clear()
    users, channel = helpers.two_users_one_channel()
    cw.channel_invite(users[0]["token"],channel["channel_id"],users[1]["auth_user_id"])
    assert cw.notifications_get(users[1]["token"])["notifications"][0]["notification_message"] == "@johndoe added you to Channel 1"
 
def test_notifications_get_dm():
    cw.clear()
    users = helpers.two_users()
    user3 = cw.auth_register("sotheresthisguy@gmail.com","thatdid","Alotof","Nothing")
    dm_id = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    cw.dm_invite(users[0]["token"],dm_id["dm_id"],user3["auth_user_id"])
    assert cw.notifications_get(users[1]["token"])["notifications"][0]["notification_message"] ==  "@johndoe added you to janelee, johndoe"
    assert cw.notifications_get(user3["token"])["notifications"][0]["notification_message"] ==  "@johndoe added you to alotofnothing, janelee, johndoe"

def test_notifications_get_dm_multiple():
    cw.clear()
    users = helpers.three_users()
    cw.dm_create(users[0]["token"], [users[1]["auth_user_id"], users[2]["auth_user_id"]])
    assert cw.notifications_get(users[1]["token"])["notifications"][0]["notification_message"] ==  "@johndoe added you to janelee, johndoe, patsmith"
    assert cw.notifications_get(users[2]["token"])["notifications"][0]["notification_message"] ==  "@johndoe added you to janelee, johndoe, patsmith"

def test_notifications_get_invalid_token():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(AccessError): 
        cw.notifications_get(1111) 
    cw.clear()
