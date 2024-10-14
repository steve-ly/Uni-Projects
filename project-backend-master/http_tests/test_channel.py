"""


"""

import pytest

from . import call_wrappers as cw
from . import helpers
from src.error import InputError, AccessError

def test_channel_invite():
    cw.clear()
    users, channel = helpers.two_users_one_channel()
    cw.channel_invite(users[0]["token"], channel["channel_id"], users[1]["auth_user_id"])

def test_channel_invite_bad_token():
    cw.clear()
    users, channel = helpers.two_users_one_channel()

    with pytest.raises(AccessError):
        cw.channel_invite("Not my token", channel["channel_id"], users[1]["auth_user_id"])

def test_channel_invite_bad_ch_id():
    cw.clear()
    users, _ = helpers.two_users_one_channel()

    with pytest.raises(InputError):
        cw.channel_invite(users[0]["token"], 0, users[1]["auth_user_id"])

def test_channel_invite_bad_u_id():
    cw.clear()
    users, channel = helpers.two_users_one_channel()

    with pytest.raises(InputError):
        cw.channel_invite(users[0]["token"], channel["channel_id"], 0)

def test_channel_invite_non_member():
    cw.clear()
    users, channel = helpers.two_users_one_channel()

    with pytest.raises(AccessError):
        cw.channel_invite(users[1]["token"], channel["channel_id"], users[0]["auth_user_id"])

################################################################################

def test_channel_details():
    cw.clear()
    users, channel = helpers.two_users_one_channel()
    cw.channel_invite(users[0]["token"], channel["channel_id"], users[1]["auth_user_id"])
    
    details = cw.channel_details(users[0]["token"], channel["channel_id"])
    
    # Remove references to profile pic as these are difficult to black-box
    for mem in details["all_members"]: mem.pop("profile_img_url")
    for mem in details["owner_members"]: mem.pop("profile_img_url")
    
    assert details["name"] == "Channel 1"
    assert details["is_public"] == True
    assert details["owner_members"] == [
        {"u_id": users[0]["auth_user_id"], "email": "someone@example.com", 
         "name_first": "John", "name_last": "Doe", "handle_str": "johndoe"}
        ]
    assert {"u_id": users[0]["auth_user_id"], "email": "someone@example.com", 
         "name_first": "John", "name_last": "Doe", "handle_str": "johndoe"}\
             in details["all_members"]
    assert {"u_id": users[1]["auth_user_id"], "email": "someone_else@example.com", 
         "name_first": "Jane", "name_last": "Lee", "handle_str": "janelee"}\
             in details["all_members"]

def test_channel_details_invalid_ch():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(InputError):
        cw.channel_details(user["token"], 0)

def test_channel_details_non_member():
    cw.clear()
    users, channel = helpers.two_users_one_channel()
    
    with pytest.raises(AccessError):
        cw.channel_details(users[1]["token"], channel["channel_id"])

################################################################################

def test_channel_messages_empty():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    msgs = cw.channel_messages(user["token"], channel["channel_id"], 0)
    
    assert len(msgs["messages"]) == 0
    assert msgs["start"] == 0
    assert msgs["end"] == -1

def test_channel_messages():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    
    for i in range(51):
        cw.message_send(user["token"], channel["channel_id"], str(i))
    
    # Get messages from start
    msgs = cw.channel_messages(user["token"], channel["channel_id"], 0)
    assert len(msgs["messages"]) == 50
    assert msgs["start"] == 0
    assert msgs["end"] == 50
    
    for i in range(50):
        assert msgs["messages"][i]["message"] == str(50 - i)
    
    # Get messages from one element in (end should be -1)
    msgs = cw.channel_messages(user["token"], channel["channel_id"], 1)
    assert len(msgs["messages"]) == 50
    assert msgs["start"] == 1
    assert msgs["end"] == -1
    
    for i in range(50):
        assert msgs["messages"][i]["message"] == str(49 - i)

def test_channel_messages_non_member():
    cw.clear()
    users, channel = helpers.two_users_one_channel()
    
    with pytest.raises(AccessError):
        cw.channel_messages(users[1]["token"], channel["channel_id"], 0)

def test_channel_messages_bad_start():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    
    with pytest.raises(InputError):
        cw.channel_messages(user["token"], channel["channel_id"], 1)

def test_channel_messages_bad_ch_id():
    cw.clear()
    user, _ = helpers.one_user_one_channel()
    
    with pytest.raises(InputError):
        cw.channel_messages(user["token"], 0, 0)

################################################################################

def test_channel_join():
    cw.clear()
    users, channel = helpers.two_users_one_channel()
    
    cw.channel_join(users[1]["token"], channel["channel_id"])
    
    # If they're not a member they can't access details
    cw.channel_details(users[1]["token"], channel["channel_id"])

def test_channel_join_already_member():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    
    cw.channel_join(user["token"], channel["channel_id"])
    
    details = cw.channel_details(user["token"], channel["channel_id"])
    
    assert len(details["all_members"]) == 1

def test_channel_join_private():
    cw.clear()
    users, channel = helpers.two_users_one_channel_private()
    
    with pytest.raises(AccessError):
        cw.channel_join(users[1]["token"], channel["channel_id"])

def test_channel_join_invalid_ch_id():
    cw.clear()
    users, _ = helpers.two_users_one_channel()
    
    with pytest.raises(InputError):
        cw.channel_join(users[1]["token"], 0)

################################################################################

def test_channel_add_owner():
    cw.clear()
    users, channel = helpers.two_users_one_channel()
    cw.channel_join(users[1]["token"], channel["channel_id"])
    cw.channel_addowner(users[0]["token"], channel["channel_id"], users[1]["auth_user_id"])

    details = cw.channel_details(users[0]["token"], channel["channel_id"])
    
    assert len(details["owner_members"]) == 2
    
    assert users[0]["auth_user_id"] in [owner["u_id"] for owner in details["owner_members"]]

def test_channel_add_owner_non_admin():
    cw.clear()
    users, channel = helpers.two_users_one_channel()
    cw.channel_join(users[1]["token"], channel["channel_id"])
    with pytest.raises(AccessError):
        cw.channel_addowner(users[1]["token"], channel["channel_id"], users[1]["auth_user_id"])

def test_channel_add_owner_already_admin():
    cw.clear()
    users, channel = helpers.two_users_one_channel()
    cw.channel_join(users[1]["token"], channel["channel_id"])
    with pytest.raises(InputError):
        cw.channel_addowner(users[0]["token"], channel["channel_id"], users[0]["auth_user_id"])

def test_channel_add_owner_non_member_admin():
    cw.clear()
    users = helpers.three_users()
    channel = helpers.one_channel(users[1]["token"])
    cw.channel_join(users[2]["token"], channel["channel_id"])
    cw.channel_addowner(users[0]["token"], channel["channel_id"], users[2]["auth_user_id"])

################################################################################

def test_channel_remove_owner():
    cw.clear()
    users = helpers.two_users()
    channel = helpers.one_channel(users[1]["token"])
    cw.channel_removeowner(users[1]["token"], channel["channel_id"], users[1]["auth_user_id"])

    details = cw.channel_details(users[1]["token"], channel["channel_id"])
    
    assert len(details["owner_members"]) == 0

def test_channel_remove_owner_non_admin():
    cw.clear()
    users, channel = helpers.two_users_one_channel()
    
    with pytest.raises(AccessError):
        cw.channel_removeowner(users[1]["token"], channel["channel_id"], users[0]["auth_user_id"])

def test_channel_remove_owner_already_not_admin():
    cw.clear()
    users, channel = helpers.two_users_one_channel()
    cw.channel_join(users[1]["token"], channel["channel_id"])
    with pytest.raises(InputError):
        cw.channel_removeowner(users[0]["token"], channel["channel_id"], users[1]["auth_user_id"])

def test_channel_remove_owner_non_member_admin():
    cw.clear()
    users = helpers.two_users()
    channel = helpers.one_channel(users[1]["token"])
    cw.channel_removeowner(users[0]["token"], channel["channel_id"], users[1]["auth_user_id"])

################################################################################

def test_channel_leave():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    cw.channel_leave(user["token"], channel["channel_id"])
    
    # Can't access channel details
    with pytest.raises(AccessError):
        d = cw.channel_details(user["token"], channel["channel_id"])
        print(d)

def test_channel_leave_non_member():
    cw.clear()
    users, channel = helpers.two_users_one_channel()
    with pytest.raises(AccessError):
        cw.channel_leave(users[1]["token"], channel["channel_id"])

def test_channel_leave_bad_channel():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(InputError):
        cw.channel_leave(user["token"], 0)
