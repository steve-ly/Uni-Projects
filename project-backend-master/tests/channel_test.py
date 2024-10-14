"""tests > channel_test.py

Provides tests for src > channel.py

Primary Contributors: 
 - Runyao (Brian) Wang [z5248223@ad.unsw.edu.au]
     - All tests excepting those mentioned below

Minor Contributors:
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]
     - Tests:
         - test_channel_details_v1_fake_user()
         - test_channel_messages_v1_fake_user()
         - test_channel_join_v1_fake_user()
     - Bug fixes
         - Commit 9c20a75c

"""

import pytest
import datetime, time

from src.echo import echo
from src.error import InputError, AccessError
from src import notification, state, auth, user, identifier, channels, channel, message, admin, other

# Reset the state
other.clear_v1()

# Create a channel ,a user in the channel and a user2 not in the channel to test implementations
user_1 = auth.auth_register_v1("test@email.com", "password", "John", "Smith")
user_id = user_1["auth_user_id"]
user_token = user_1["token"]
channel_id = channels.channels_create_v1(user_token, "Test", True)["channel_id"]
user_2 = auth.auth_register_v1("test2@email.com", "password2", "Laura", "Lee")
user2_id = user_2["auth_user_id"]
user2_token = user_2["token"]

# The user and channel dicts that can be used for testing.
user_dict = {
        "u_id": user_id,
        "email": "test@email.com",
        "name_first": "John",
        "name_last": "Smith",
        "handle_str": "johnsmith",
    }

user2_dict = {
        "u_id": user2_id,
        "email": "test2@email.com",
        "name_first": "Laura",
        "name_last": "Lee",
        "handle_str": "lauralee",
    }

ch_dict = {
        "name": "Test",
        "ch_id": channel_id,
    }
# Save the initial state without messages
s = state.get_state()
# Add 81 messages (0 - 80) into the channel to test
for m in range(0, 81):
    message.message_send_v1(user_token, channel_id, str(m))
messages_max = 80
# Save the state with messages
s_msg = state.get_state()

# Testing channel_invite_v1


def test_channel_invite_v1():
    """Tests for successful channel invite for public channel.
    """
    state.set_state(s)

    # invite the user2 to join the channel
    channel.channel_invite_v1(user_token, channel_id, user2_id)

    # check user2 is in the channel's user list
    ch_info = channel.channel_details_v1(user_token, channel_id)
    
    # Remove references to profile pic as these are difficult to black-box
    for mem in ch_info["all_members"]: mem.pop("profile_img_url")
    
    assert user2_dict in ch_info["all_members"]

def test_channel_invite_v1_already_member():
    """Test that users who are already channel members aren't added twice
    """
    state.set_state(s)

    # invite the user2 to join the channel
    channel.channel_invite_v1(user_token, channel_id, user2_id)

    # Invite them again
    channel.channel_invite_v1(user_token, channel_id, user2_id)

    # check user2 is in the channel's user list
    ch_info = channel.channel_details_v1(user_token, channel_id)
    
    # Remove references to profile pic as these are difficult to black-box
    for mem in ch_info["all_members"]: mem.pop("profile_img_url")
    
    # Assert they're only in the list once
    assert ch_info["all_members"].count(user2_dict) == 1

def test_channel_invite_v1_invalid_user():
    """Tests for InputError on invalid user id.
    """
    state.set_state(s)

    # Create an unauthorised user id
    fake_user_id = identifier.get_new_identifier()

    # Raise InputError when user id is invalid
    with pytest.raises(InputError):
        channel.channel_invite_v1(user_token, channel_id, fake_user_id)

def test_channel_invite_v1_invalid_inviter():
    """Tests for AccessError on invalid inviter id.
    """
    state.set_state(s)

    # Create an unauthorised user id
    fake_user_id = identifier.get_new_identifier()

    # Raise AccessError when inviter id is invalid
    with pytest.raises(AccessError):
        channel.channel_invite_v1(fake_user_id, channel_id, user_id)

def test_channel_invite_v1_invalid_channel():
    """Tests for InputError on invalid channel id.
    """
    state.set_state(s)

    # Create an invalid channel id
    fake_ch_id = identifier.get_new_identifier()

    # Raise InputError when channel id is invalid
    with pytest.raises(InputError):
        channel.channel_invite_v1(user_token, fake_ch_id, user2_id)

def test_channel_invite_v1_unauthorised_user():
    """Tests for AccessError on unauthorised user id.
    """
    state.set_state(s)

    # user2 (not in the channel) invite the user to join the channel
    # Raise AccessError 
    with pytest.raises(AccessError):
        channel.channel_invite_v1(user2_token, channel_id, user_id)

def test_channel_invite_v1_private_channel():
    """Tests for successful channel invite for private channel.
    """
    state.set_state(s)
    # Use user2 to create an private channel
    private_channel_id = channels.channels_create_v1(user2_token, "Testprivate", False)["channel_id"]

    # Invite the user to join the private channel
    channel.channel_invite_v1(user2_token, private_channel_id, user_id)

    # Check user is in the channel's user list
    ch_info = channel.channel_details_v1(user2_token, private_channel_id)
    
    # Remove references to profile pic as these are difficult to black-box
    for mem in ch_info["all_members"]: mem.pop("profile_img_url")
    
    assert user_dict in ch_info["all_members"]

def test_channel_invite_notification():
    """Ensures that a notification is sent properly when a user is invited to a channel
    """
    state.set_state(s)

    # invite the user2 to join the channel
    channel.channel_invite_v1(user_token, channel_id, user2_id)

    # check user2 is in the channel's user list
    notes = notification.notification_get_v1(user2_token)["notifications"]
    
    assert len(notes) == 1
    assert notes[0]["channel_id"] == channel_id
    assert notes[0]["dm_id"] == -1
    assert notes[0]["notification_message"] == f"@{user_dict['handle_str']} added you to {ch_dict['name']}"

# Testing channel_details_v1

def test_channel_details_v1():
    """Tests for successful return of channel details.
    """
    state.set_state(s)

    # get channel info dictionary
    ch_info = channel.channel_details_v1(user_token, channel_id)
    
    # Remove references to profile pic as these are difficult to black-box
    for mem in ch_info["all_members"]: mem.pop("profile_img_url")
    for mem in ch_info["owner_members"]: mem.pop("profile_img_url")

    # Check the info matches the data in the database
    assert ch_info["name"] == ch_dict["name"]
    assert user_dict in ch_info["all_members"]
    assert user_dict in ch_info["owner_members"]
    assert ch_info["is_public"] == True
    assert len(ch_info) == 4

def test_channel_details_global_owner_non_local():
    """Tests that global owners are included in the list of channel owners
    """
    state.set_state(s)
    
    # Create new channel with user 2 as the owner
    new_ch = channels.channels_create_v1(user2_token, "Channel 2", True)["channel_id"]
    
    # Add user 1
    channel.channel_invite_v1(user2_token, new_ch, user_id)
    
    # Ensure that user 1 (global owner) is shown as a channel owner
    ch_info = channel.channel_details_v1(user_token, new_ch)
    
    # Remove references to profile pic as these are difficult to black-box
    for mem in ch_info["owner_members"]: mem.pop("profile_img_url")
    
    assert user_dict in ch_info["owner_members"]
    assert len(ch_info["owner_members"]) == 2

def test_channel_details_v1_invalid_channel():
    """Tests for InputError for invalid channel id.
    """
    state.set_state(s)

    # Create an invalid channel id
    fake_ch_id = identifier.get_new_identifier()

    # Raise InputError when channel id is invalid
    with pytest.raises(InputError):
        channel.channel_details_v1(user_token, fake_ch_id)

def test_channel_details_v1_unauthorised_user():
    """Tests for AccessError for unauthorised user id.
    """
    state.set_state(s)

    # user2 (not in the channel) tries to get the channel details
    # Raise AccessError 
    with pytest.raises(AccessError):
        channel.channel_details_v1(user2_token, channel_id)

def test_channel_details_v1_fake_user():
    """Tests for AccessError for invalid/fake id.
    """
    state.set_state(s)

    # invalid auth_user_id tries to get the channel details
    # Raise AccessError 
    with pytest.raises(AccessError):
        channel.channel_details_v1(identifier.get_new_identifier(), channel_id)    

# Testing channel_messages_v1()

def test_channel_messages_v1_less_than_50():
    """Tests for successful return oldest channel messages (the end index is -1)
    """
    state.set_state(s_msg)

    # Set start index at 70
    start = 70
    ch_messages = channel.channel_messages_v1(user_token, channel_id, start)

    # Check the messages in the channel. Since the start index is 70, the message content is from 10 (most recent) to 0 (oldest)
    messages_content = messages_max  - start
    messages_count = 0
    for messages_content in range(messages_content, -1, -1):
        assert ch_messages["messages"][messages_count]["message"] == str(messages_content)
        messages_count += 1

    assert ch_messages["start"] == start

    # Since the oldest message is listed, the end index is -1
    assert ch_messages["end"] == -1

def test_channel_messages_v1_more_than_50():
    """Tests for successful return 50 channel messages (the end index is start + 50)
    """
    state.set_state(s_msg)

    # Set start index at 22
    start = 22

    # get the channel message dict
    ch_messages = channel.channel_messages_v1(user_token, channel_id, start)

    # Check the messages in the channel. Since the start index is 22, the message content is from 58 (most recent) to 8 (oldest)
    messages_content = messages_max - start
    messages_count = 0
    for messages_count in range(messages_count, 50):
        assert ch_messages["messages"][messages_count]["message"] == str(messages_content)
        messages_content -= 1

    assert ch_messages["start"] == start

    # Since the oldest message is not listed, the end index is start + 50
    assert ch_messages["end"] == start + 50

def test_channel_messages_v1_no_messages():
    """Tests for the channel without messages. It should return an empty list for key 'messages'.
    """
    # Load the state without messages
    state.set_state(s)

    # Set start index at 0
    start = 0

    # get the channel message dict
    ch_messages = channel.channel_messages_v1(user_token, channel_id, start)

    assert ch_messages["messages"] == []
    assert ch_messages["start"] == start
    # Since the oldest message is listed, the end index is -1
    assert ch_messages["end"] == -1


def test_channel_messages_v1_invalid_channel():
    """Tests for InputError for invalid/fake channel id.
    """
    state.set_state(s_msg)

    # Create an invalid channel id
    fake_ch_id = identifier.get_new_identifier()

    # Raise InputError when channel id is invalid
    with pytest.raises(InputError):
        channel.channel_messages_v1(user_token, fake_ch_id, 0)

def test_channel_messages_v1_invalid_start():
    """Tests for InputError for invalid starting value for messages.
    """
    state.set_state(s_msg)

    # Raise InputError when start is more than the number of messages in the channel (80)
    with pytest.raises(InputError):
        channel.channel_messages_v1(user_token, channel_id, 100)

def test_channel_messages_v1_largest_start():
    """Tests for the start index equals number of messages. It should return an empty list for key 'messages'.
    """
    state.set_state(s_msg)

    # Set start index as same as the number of messages (81).
    start = 81

    # Get the channel message dict
    ch_messages = channel.channel_messages_v1(user_token, channel_id, start)

    assert ch_messages["messages"] == []
    assert ch_messages["start"] == start
    # Since the oldest message is listed, the end index is -1
    assert ch_messages["end"] == -1

def test_channel_messages_v1_unauthorised_user():
    """Tests for AccessError for unauthorised user id.
    """
    state.set_state(s_msg)

    # Raise AccessError when user is not a member in the channel
    with pytest.raises(AccessError):
        channel.channel_messages_v1(user2_token, channel_id, 0)

def test_channel_messages_v1_fake_user():
    """Tests for AccessError for invalid/fake user id.
    """
    state.set_state(s_msg)

    # Raise AccessError when auth_user_id is invalid
    with pytest.raises(AccessError):
        channel.channel_messages_v1(identifier.get_new_identifier(), channel_id, 0)

def test_channel_messages_v1_delayed_message():
    """Tests for delaying messages to show later
    """
    state.set_state(s_msg)

    start = 0
    delay = datetime.datetime.now().timestamp() + 1

    # Add a 1 delay to message
    message.message_send_later_v1(user_token, channel_id, "81", delay)

    ch_messages = channel.channel_messages_v1(user_token, channel_id, start)

    # Check the messages in the channel. Since the start index is 22, the message content is from 58 (most recent) to 8 (oldest)
    messages_content = 80 - start
    messages_count = 0
    print(ch_messages)
    for messages_count in range(messages_count, 50):
        assert ch_messages["messages"][messages_count]["message"] == str(messages_content)
        messages_content -= 1

    assert ch_messages["start"] == start

    # Since the oldest message is not listed, the end index is start + 50
    assert ch_messages["end"] == start + 50

def test_channel_messages_v1_sent_delayed_message():
    """Tests for delaying messages to show later
    """
    state.set_state(s_msg)

    start = 0
    delay = datetime.datetime.now().timestamp() + 1
    message.message_send_later_v1(user_token, channel_id, "81", delay)

    time.sleep(1)

    ch_messages = channel.channel_messages_v1(user_token, channel_id, start)

    # Check the messages in the channel. Since the start index is 22, the message content is from 58 (most recent) to 8 (oldest)
    messages_content = 81 - start
    messages_count = 0
    for messages_count in range(messages_count, 50):
        assert ch_messages["messages"][messages_count]["message"] == str(messages_content)
        messages_content -= 1

    assert ch_messages["start"] == start

    # Since the oldest message is not listed, the end index is start + 50
    assert ch_messages["end"] == start + 50


# Testing channel_join_v1()

def test_channel_join_v1():
    """Tests for successful adding of user to channel.
    """
    state.set_state(s)

    channel.channel_join_v1(user2_token, channel_id)
    
    # check the user is in the channel's user list
    ch_info = channel.channel_details_v1(user_token, channel_id)
    # Remove references to profile pic as these are difficult to black-box
    for mem in ch_info["all_members"]: mem.pop("profile_img_url")
    
    assert user2_dict in ch_info["all_members"]

def test_channel_join_v1_already_member():
    """Test that users who are already channel members aren't added twice
    """
    state.set_state(s)

    # invite the user2 to join the channel
    channel.channel_invite_v1(user_token, channel_id, user2_id)

    # Get them to try to join again
    channel.channel_join_v1(user_token, channel_id)

    # check user2 is in the channel's user list
    ch_info = channel.channel_details_v1(user_token, channel_id)
    # Remove references to profile pic as these are difficult to black-box
    for mem in ch_info["all_members"]: mem.pop("profile_img_url")
    
    # Assert they're only in the list once
    assert ch_info["all_members"].count(user2_dict) == 1

def test_channel_join_v1_invalid_channel():
    """Tests for InputError for invalid/fake channel id.
    """
    state.set_state(s)

    # Create an invalid channel id
    fake_ch_id = identifier.get_new_identifier()

    # Raise InputError when channel id is invalid
    with pytest.raises(InputError):
        channel.channel_join_v1(user_token, fake_ch_id)

def test_channel_join_v1_private():
    """Tests for AccessError for joining of private channel.
    """
    state.set_state(s)

    # use user to create an private channel
    private_channel_id = channels.channels_create_v1(user_token, "Test_private", False)["channel_id"]

    # Raise AccessError when user tries to join the private channel 
    with pytest.raises(AccessError):
        channel.channel_join_v1(user2_token, private_channel_id)

def test_channel_join_v1_fake_user():
    """Tests for AccessError for invalid/fake user id.
    """
    state.set_state(s)

    with pytest.raises(AccessError):
        channel.channel_join_v1(identifier.get_new_identifier(), channel_id)

def test_channel_leave():
    """Tests that a user can leave a channel they're a member of (if they
    aren't an owner).
    """
    state.set_state(s)
    
    # Create channel with user 2
    channel2_id = channels.channels_create_v1(user2_token, "Channel 2", True)\
        ["channel_id"]
        
    # Add user 1 to channel
    channel.channel_invite_v1(user2_token, channel2_id, user_id)
    
    # Leave the channel that our user joined
    channel.channel_leave_v1(user_token, channel2_id)
    
    # Ensure they can't see channel data: AccessError
    with pytest.raises(AccessError):
        channel.channel_details_v1(user_token, channel2_id)

def test_channel_leave_owner():
    """Tests that a user isn't still listed as a local owner of a channel
    if they leave the channel
    """
    state.set_state(s)
    
    # Add user 2 to channel 1
    channel.channel_invite_v1(user_token, channel_id, user2_id)
    
    # Leave channel with user 1
    channel.channel_leave_v1(user_token, channel_id)
    
    # Check there aren't any channel owners remaining
    assert len(channel.channel_details_v1(user2_token, channel_id)\
        ["owner_members"]) == 0

def test_channel_leave_non_member():
    """Tests that an error is raised when a user tries to leave a channel
    that they aren't a member of
    """
    
    state.set_state(s)
    
    # Leave the channel that our user hasn't joined
    with pytest.raises(AccessError):
        channel.channel_leave_v1(user2_token, channel_id)
        
def test_channel_leave_invalid_channel():
    """Tests that an error is raised when a user tries to leave a channel that
    doesn't exist
    """
    
    state.set_state(s)
    
    # Try to leave invalid channel
    with pytest.raises(InputError):
        channel.channel_leave_v1(user_token, identifier.get_new_identifier())

def test_channel_leave_invalid_user():
    """Tests that an error is raised when an invalid user tries to leave a
    channel
    """
    
    state.set_state(s)
    
    # Try to leave a channel using an invalid user ID
    with pytest.raises(AccessError):
        channel.channel_leave_v1(identifier.get_new_identifier(), channel_id)
    
def test_channel_add_owner():
    """Test that a user can be added as an owner
    """
    state.set_state(s)
    channel.channel_join_v1(user2_token, channel_id)
    
    # Add user 2 as a channel owner using user 1
    channel.channel_addowner_v1(user_token, channel_id, user2_id)
    
    # Ensure that user 2 is a channel owner
    assert user.user_profile_v1(user_token, user2_id)["user"]\
        in channel.channel_details_v1(user_token, channel_id)["owner_members"]

def test_channel_add_owner_already_admin():
    """Test that a user can't be added as an owner if they are already a local 
    owner of the channel
    """

    state.set_state(s)
    channel.channel_join_v1(user2_token, channel_id)
    
    # Add user 2 as a channel owner using user 1
    channel.channel_addowner_v1(user_token, channel_id, user2_id)
    
    # Try adding them again
    with pytest.raises(InputError):
        channel.channel_addowner_v1(user_token, channel_id, user2_id)

def test_channel_add_owner_global_admin():
    """Test that a user can still be added as an owner if they are a global 
    admin, and a member of the channel, but not a local owner of the channel.
    """
    
    state.set_state(s)
    
    # Create channel with user 2
    channel2_id = channels.channels_create_v1(user2_token, "Channel 2", True)\
        ["channel_id"]
    
    # Then add user 1
    channel.channel_invite_v1(user2_token, channel2_id, user_id)
    
    # Add user 1 as a local owner
    channel.channel_addowner_v1(user2_token, channel2_id, user_id)
    
    # Ensure they aren't present in owner list twice
    # There should only be 2 owners
    assert len(channel.channel_details_v1(user_token, channel2_id)
               ["owner_members"]) == 2

def test_channel_add_owner_as_global_admin():
    """Test that a global admin can add users as channel owners even if they
    aren't a local owner of the channel
    """
    state.set_state(s)
    
    # Create a channel as user 2
    channel2_id = channels.channels_create_v1(user2_token, "Channel 2", True)\
        ["channel_id"]
    
    # Add user 1 (global owner) to channel
    channel.channel_invite_v1(user2_token, channel2_id, user_id)
    
    # Create user 3
    user3_id = auth.auth_register_v1("user3@hotmail.com", "password", "Some", 
                                     "Guy")["auth_user_id"]
    
    # Add user 3 to channel
    channel.channel_invite_v1(user2_token, channel2_id, user3_id)
    
    # Add user 3 as channel owner using user 1
    channel.channel_addowner_v1(user_token, channel2_id, user3_id)
    
    # Ensure that user 3 was added
    assert user.user_profile_v1(user_token, user3_id)["user"]\
        in channel.channel_details_v1(user_token, channel2_id)["owner_members"]

def test_channel_add_owner_as_global_admin_non_member():
    """Test that a global admin can add users as channel owners even if they
    aren't amember of the channel
    """
    state.set_state(s)
    
    # Create a channel as user 2
    channel2_id = channels.channels_create_v1(user2_token, "Channel 2", True)\
        ["channel_id"]
    
    # Create user 3
    user3_id = auth.auth_register_v1("user3@hotmail.com", "password", "Some", 
                                     "Guy")["auth_user_id"]
    
    # Add user 3 to channel
    channel.channel_invite_v1(user2_token, channel2_id, user3_id)
    
    # Add user 3 as channel owner using user 1
    channel.channel_addowner_v1(user_token, channel2_id, user3_id)
    
    # Ensure that user 3 was added
    assert user.user_profile_v1(user_token, user3_id)["user"]\
        in channel.channel_details_v1(user2_token, channel2_id)["owner_members"]

def test_channel_add_owner_non_admin():
    """Test that an error is raised when a user tries to add an owner if they
    aren't a global owner or a channel owner
    """
    state.set_state(s)
    
    # Create a channel with user 2
    channel2_id = channels.channels_create_v1(user2_token, "Channel 2", True)\
        ["channel_id"]
    
    # Create a new user
    user_3 = auth.auth_register_v1("user3@hotmail.com", "password", "Some", "Guy")
    user3_id = user_3["auth_user_id"]
    user3_token = user_3["token"]
    
    
    # Add the user to the channel
    channel.channel_invite_v1(user2_token, channel2_id, user3_id)
    
    # Add user 1 to the channel
    channel.channel_invite_v1(user2_token, channel2_id, user_id)
    
    # Try to make user 1 a channel owner using user 3
    with pytest.raises(AccessError):
        channel.channel_addowner_v1(user3_token, channel2_id, user_id)

def test_channel_add_owner_bad_channel():
    """Test that an error is raised when trying to add an owner to a
    non-existent channel
    """
    state.set_state(s)
    
    with pytest.raises(InputError):
        channel.channel_addowner_v1(user_token, identifier.get_new_identifier(), 
                                    user_id)
    
def test_channel_add_owner_bad_user():
    """Test that an error is raised when trying to add a non-existant user as
    owner of a channel
    """
    state.set_state(s)
    
    with pytest.raises(InputError):
        channel.channel_addowner_v1(user_token, channel_id, 
                                    identifier.get_new_identifier())

def test_channel_add_owner_bad_auth_user():
    """Test that an error is raised when trying to add a user as owner of a
    channel if the auth_user is invalid
    """
    state.set_state(s)
    
    with pytest.raises(AccessError):
        channel.channel_addowner_v1(identifier.get_new_identifier(), channel_id, 
                                    user_id)

def test_channel_remove_owner():
    """Test that a user can be removed as owner of a channel
    """
    state.set_state(s)
        
    # Add user 2 to channel 1
    channel.channel_invite_v1(user_token, channel_id, user2_id)
    
    # Add user 2 as a local owner of the channel
    channel.channel_addowner_v1(user_token, channel_id, user2_id)
    
    # Remove user 2 as a local owner of the channel
    channel.channel_removeowner_v1(user_token, channel_id, user2_id)
    
    # Check that user 2 isn't a local owner
    assert user.user_profile_v1(user_token, user2_id)["user"]\
        not in channel.channel_details_v1(user_token, channel_id)["owner_members"]

def test_channel_remove_owner_self():
    """Test that a user can remove themselves as owner of a channel
    """
    state.set_state(s)
    
    # Create channel using user 2
    channel2_id = channels.channels_create_v1(user2_token, "Channel 2", True)\
        ["channel_id"]
    
    # Remove user 2 as a local owner using user 2
    channel.channel_removeowner_v1(user2_token, channel2_id, user2_id)
    
    # Ensure that user 2 isn't a local owner (there should be no owners)
    assert len(channel.channel_details_v1(user2_token, channel2_id)\
        ["owner_members"]) == 0

def test_channel_remove_owner_as_global_owner():
    """Test that a global owner (who isn't a local owner) of a channel can
    remove a local owner of a channel
    """
    state.set_state(s)
    
    # Create channel using user 2
    channel2_id = channels.channels_create_v1(user2_token, "Channel 2", True)\
        ["channel_id"]
    
    # Add user 1 to the channel
    channel.channel_invite_v1(user2_token, channel2_id, user_id)
    
    # Remove user 2 as a local owner of the channel using user 1 (who is global owner)
    channel.channel_removeowner_v1(user_token, channel2_id, user2_id)
    
    # Ensure that user 2 isn't a local owner
    assert user.user_profile_v1(user_token, user2_id)["user"]\
        not in channel.channel_details_v1(user_token, channel2_id)["owner_members"]


def test_channel_remove_owner_global_and_local_owner():
    """Test that a global owner who is a local owner of a channel can be removed
    as a local owner of a channel
    """
    state.set_state(s)
    
    # Remove user 1 as a local owner of channel 1
    channel.channel_removeowner_v1(user_token, channel_id, user_id)
    
    # Add user 2 to the channel
    channel.channel_invite_v1(user_token, channel_id, user2_id)
    
    # Get another user and make them an owner (so we don't leave the server
    # ownerless)
    user_3 = auth.auth_register_v1("me@me.com", "MEeeeeee", "Hello", "World")
    admin.admin_permssion_change_v1(user_token, user_3["auth_user_id"], 1)
    
    # Set user 1's permission to remove them as global owner
    # (this ensures they won't be added to the list of owners)
    admin.admin_permssion_change_v1(user_token, user_id, 2)
    
    # Ensure user 1 isn't a local owner
    assert user.user_profile_v1(user_token, user_id)["user"]\
        not in channel.channel_details_v1(user2_token, channel_id)["owner_members"]

def test_channel_remove_owner_global_owner():
    """Test that a global owner who isn't a local owner of a channel can't be
    removed as a local owner of a channel
    """
    state.set_state(s)
    
    # Create channel with user 2
    channel2_id = channels.channels_create_v1(user2_token, "Channel 2", True)\
        ["channel_id"]
    
    # Add user 1 to the channel
    channel.channel_invite_v1(user2_token, channel2_id, user_id)
    
    # Try to remove user 1 (global owner) as owner of the channel
    with pytest.raises(InputError):
        channel.channel_removeowner_v1(user2_token, channel2_id, user_id)

def test_channel_remove_owner_non_member():
    """Test that a user who isn't a member of the channel can't remove the
    channel's owners
    """
    state.set_state(s)
    # Try to remove user 2 as a local owner of channel 1 using user 1
    with pytest.raises(InputError):
        channel.channel_removeowner_v1(user_token, channel_id, user2_id)

def test_channel_remove_owner_non_admin():
    """Test that an error is raised when a user tries to add an owner if they
    aren't a global owner or a channel owner
    """
    state.set_state(s)
    
    # Create a channel with user 2
    channel2_id = channels.channels_create_v1(user2_token, "Channel 2", True)\
        ["channel_id"]
    
    # Create a new user
    user_3 = auth.auth_register_v1("user3@hotmail.com", "password", "Some", "Guy")
    user3_id = user_3["auth_user_id"]
    user3_token = user_3["token"]
    # Add the user to the channel
    channel.channel_invite_v1(user2_token, channel2_id, user3_id)
    
    # Try to remove user 2 as a channel owner using user 3
    with pytest.raises(AccessError):
        channel.channel_removeowner_v1(user3_token, channel2_id, user2_id)

def test_channel_remove_owner_non_member_global_owner():
    """Test that a user who isn't a member of the channel can remove the
    channel's owners, as long as they are a global owner
    """
    state.set_state(s)
    # Create channel with user 2
    channel2_id = channels.channels_create_v1(user2_token, "Channel 2", True)\
        ["channel_id"]
    
    # Try to remove user 2 as local owner using user 1 (global owner)
    channel.channel_removeowner_v1(user_token, channel2_id, user2_id)
    
    # Ensure that user 2 isn't a local owner (there should be no owners)
    assert len(channel.channel_details_v1(user2_token, channel2_id)\
        ["owner_members"]) == 0

def test_channel_remove_owner_bad_channel():
    """Test that an error is raised when we try to remove a user as the local
    owner of a non-existent channel
    """
    state.set_state(s)
    with pytest.raises(InputError):
        channel.channel_removeowner_v1(user_token, identifier.get_new_identifier(),
                                       user2_id)
    

def test_channel_remove_owner_bad_user():
    """Test that an error is raised when we try to remove a non-existent user as
    the owner of a channel
    """
    state.set_state(s)
    with pytest.raises(InputError):
        channel.channel_removeowner_v1(user_token, channel_id, 
                                       identifier.get_new_identifier())

def test_channel_remove_owner_bad_auth_user():
    """Test that an error is raised when we try to remove a user as the owner of
    a channel using an invalid auth_user_id
    """
    state.set_state(s)
    with pytest.raises(AccessError):
        channel.channel_removeowner_v1(identifier.get_new_identifier(), 
                                       channel_id, user_id)
