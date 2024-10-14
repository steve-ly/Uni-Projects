import pytest
from src.echo import echo 
from src import admin, auth, channel, channels, message, user, error, other, dm

################################################################################
# Testing remove user perms
#
# 
# 
################################################################################

def test_remove_user():
    """Tests for successful removal
    """
    other.clear_v1()
    # Create user
    currentuser = auth.auth_register_v1('validemail@gmail.com', '123abc', 'Comic', 'Sans')
    token = currentuser["token"]
    
    # Create channel
    cid = channels.channels_create_v1(token, "Cool", True)
    
    # Create another user
    removed_user = auth.auth_register_v1('validemail2@gmail.com', '123abc', 'New', 'Times')
    
    # Add them to the channel
    channel.channel_invite_v1(currentuser["token"], cid["channel_id"], removed_user["auth_user_id"])
    
    # Send some messages
    message.message_send_v1(removed_user["token"], cid["channel_id"], "message1")
    message.message_send_v1(removed_user["token"], cid["channel_id"], "message2")
    
    # Do the same in a DM
    dm_id = dm.dm_create_v1(token, [removed_user["auth_user_id"]])["dm_id"]
    dm.dm_message_send_v1(removed_user["token"], dm_id, "Hello!!!")
    
    # Remove them
    admin.admin_remove_user(token, removed_user["auth_user_id"])

    # Get their profile and check the values in it
    removed_profile = user.user_profile_v1(token, removed_user["auth_user_id"])["user"]
    assert removed_profile["name_first"] == "Removed"
    assert removed_profile["name_last"] == "User"
    assert removed_profile["handle_str"] == "removed_user"
    assert removed_profile["email"] == ""
    
    # Ensure they were removed from the channel
    assert len(channel.channel_details_v1(currentuser["token"],cid["channel_id"])["all_members"]) == 1
    
    # Check that messages have been changed
    ch_messages = channel.channel_messages_v1(token, cid["channel_id"], 0)["messages"]
    assert ch_messages[0]["message"] == "Removed user"
    assert ch_messages[1]["message"] == "Removed user"
    
    # Check that profile is inaccessible using token
    with pytest.raises(error.AccessError):
        channel.channel_messages_v1(removed_user["token"], cid["channel_id"], 0)
    
    # Check that profile is inaccessible using login
    with pytest.raises(error.InputError):
        auth.auth_login_v1('validemail2@gmail.com', '123abc')
    
    # Check that they can't be added to channels
    with pytest.raises(error.InputError):
        channel.channel_invite_v1(currentuser["token"], cid["channel_id"], removed_user["auth_user_id"])
    
    # Check that they don't appear in the all users list
    assert len(user.user_list_all_v1(token)["users"]) == 1

def test_register_after_removal():
    """Tests for successful registeration after removal
    """
    other.clear_v1()
    currentuser = auth.auth_register_v1('validemail@gmail.com', '123abc', 'Comic', 'Sans')
    token = currentuser["token"]
    member = auth.auth_register_v1('validemail2@gmail.com', '123abc', 'New', 'Times')["auth_user_id"]
    admin.admin_remove_user(token, member)
    auth_user_id = auth.auth_register_v1('validemail2@gmail.com', '123abc', 'New', 'Times')["auth_user_id"]
    
    u = user.user_profile_v1(token, auth_user_id)["user"]
    assert u["email"] == "validemail2@gmail.com"
    assert u["name_first"] == "New"
    assert u["name_last"] == "Times"

def test_remove_invalid_token():
    """ Test for AccessError if token not valid.
    """
    other.clear_v1()
    user = auth.auth_register_v1("email@email.com", "123abc", "Gorilla", "Spin")

    with pytest.raises(error.AccessError):
        admin.admin_remove_user("notagoodtoken", user["auth_user_id"])

def test_remove_user_not_owner():
    """ Test for AccessError raised if user not an owner.
    """
    other.clear_v1()
    user1 = auth.auth_register_v1("owner@email.com", "123abc", "Agile", "Gibbon")
    user2 = auth.auth_register_v1("notowner@email.com", "123abc", "Solid", "Snake")

    with pytest.raises(error.AccessError):
        admin.admin_remove_user(user2["token"], user1["auth_user_id"])

def test_remove_user_only_owner():
    """ Test for InputError raised since user is the only owner
    """
    other.clear_v1()
    user = auth.auth_register_v1("owner@email.com", "password", "dr", "boom")
    
    with pytest.raises(error.InputError):
        admin.admin_remove_user(user["token"],user["auth_user_id"])

def test_remove_user_invalid_uid():

    """ Test for InputError raised since u_id isn't valid
    """
    other.clear_v1()
    auth.auth_register_v1("owner@email.com", "123abc", "Niko", "Bellic")
    user2 = auth.auth_register_v1("notowner@email.com", "123abc", "Soyna", "Blade")

    with pytest.raises(error.InputError):
        admin.admin_remove_user(user2["token"], 111)

def test_remove_user_twice():
    """ Test for input error when removing user twice
    """
    other.clear_v1()
    user = auth.auth_register_v1("email@email.com", "123abc", "Gorilla", "Spin")
    rem = auth.auth_register_v1("email@gmail.com", "123abc", "Hella", "Windy")

    admin.admin_remove_user(user["token"], rem["auth_user_id"])
    with pytest.raises(error.InputError):
        admin.admin_remove_user(user["token"], rem["auth_user_id"])

################################################################################
# Testing admin change
#
# 
# 
################################################################################

def test_change_perms_valid():
    """ Test for Successful permission changes.
    """
    
    other.clear_v1()
    user1 = auth.auth_register_v1("owner@email.com", "123abc", "Andromeda", "Galaxy")
    user2 = auth.auth_register_v1("notowner@email.com", "123abc", "milky", "way")
    admin.admin_permssion_change_v1(user1["token"], user2["auth_user_id"], 1)
    
    # Ensure that user 2 can now demote user 1 to a normal member
    admin.admin_permssion_change_v1(user2["token"], user1["auth_user_id"], 2)
    
    # Ensure that user 1 now can't demote user 2
    with pytest.raises(error.AccessError):
        admin.admin_permssion_change_v1(user1["token"], user2["auth_user_id"], 2)

def test_change_perms_invalid_user():
    """ Test for InputError for invalid u_id.
    """
    other.clear_v1()
    user1 = auth.auth_register_v1("owner@email.com", "123abc", "Guzman", "Gomez")
    auth.auth_register_v1("notowner@email.com", "123abc", "Pink", "Floyd")

    with pytest.raises(error.InputError):
        admin.admin_permssion_change_v1(user1["token"], 111, 1)

def test_change_perms_invalid_permission():
    """ Test for InputError for invalid permission id.
    """
    other.clear_v1()
    user1 = auth.auth_register_v1("owner@email.com", "123abc", "Hot", "Star")
    user2 = auth.auth_register_v1("notowner@email.com", "123abc", "Gong", "Cha")

    with pytest.raises(error.InputError):
        admin.admin_permssion_change_v1(user1["token"], user2["auth_user_id"], 222)


def test_change_perms_unauthorised_user():
    """ Test for InputError for invalid permission id.
    """
    other.clear_v1()
    user1 = auth.auth_register_v1("owner@email.com", "123abc", "Eric", "Cartman")
    user2 = auth.auth_register_v1("notowner@email.com", "123abc", "Randy", "Marsh")

    with pytest.raises(error.AccessError):
        admin.admin_permssion_change_v1(user2["token"], user1["auth_user_id"], 1) 
        
def test_change_perms_invalid_token():
    other.clear_v1()
    auth.auth_register_v1("owner@email.com", "123abc", "big", "man")
    user2 = auth.auth_register_v1("notowner@email.com", "123abc", "Randy", "Marsh")
    with pytest.raises(error.AccessError):
        admin.admin_permssion_change_v1(123, user2["auth_user_id"], 1) 

def test_change_perms_only_owner():
    other.clear_v1()
    user1 = auth.auth_register_v1("owner@email.com", "123abc", "mac", "miller")
    with pytest.raises(error.InputError):
        admin.admin_permssion_change_v1(user1["token"], user1["auth_user_id"], 2)
