"""tests > channels_test.py

Provides tests for src > channels.py

Primary Contributors: 
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]
     - All tests

Minor Contributors:
 - [None]

"""

import pytest
from src import channels, state, auth, error, identifier, channel, other

# Large number used when doing things many times
LARGE_NUMBER = 100

other.clear_v1()

# Add user
u_dict = {
    "email": "b.benson@bmail.com",
    "name_first": "Barry",
    "name_last": "Benson",
    "handle_str": "barrybenson"
}
user1 =  auth.auth_register_v1(u_dict["email"], "ImABe3isntThatCo0l", u_dict["name_first"], u_dict["name_last"])
u_dict["u_id"] = user1["auth_user_id"]
user1_token = user1["token"]
# Default state with one user (owner)
s = state.get_state()

# Create other user
u2_dict = {
    "email": "hello@email.com",
    "name_first": "Robin",
    "name_last": "Banks",
    "handle_str": "robinbanks"
}
user2 =  auth.auth_register_v1(u2_dict["email"], "Password1", u2_dict["name_first"], u2_dict["name_last"])
u2_dict["u_id"] = user2["auth_user_id"]
user2_token = user2["token"]

# Secondary state with an extra user (non-owner)
s2 = state.get_state()

# tests for channels_create_v1()
#
#######################################

def test_ch_create():
    """Tests for successful creation of single channel.
    """
    state.set_state(s)
    
    # Add channel
    c_name = "My Channel"
    c_id = channels.channels_create_v1(user1_token, c_name, True)["channel_id"]
    
    all_channels = channels.channels_listall_v1(user1_token)["channels"]
    
    # Check channel details are correct
    assert c_id == all_channels[0]["channel_id"]
    assert c_name == all_channels[0]["name"]


def test_ch_create_many():
    """Tests for successful creation of many channels.
    """
    state.set_state(s)
    
    # Add a LARGE_NUMBER of channels
    NUM_CH = LARGE_NUMBER
    ch_names = ["Channel " + str(i + 1) for i in range(NUM_CH)]
    ch_ids = [channels.channels_create_v1(user1_token, ch_names[i], True)["channel_id"]
              for i in range(NUM_CH)]
    
    # Get list of all channels
    all_channels = channels.channels_listall_v1(user1_token)["channels"]
    
    # Assert that all the channels are correct
    assert len(all_channels) == NUM_CH
    for i in range(NUM_CH):
        assert \
            {
                "name": ch_names[i],
                "channel_id": ch_ids[i]
            } in all_channels
    
    

def test_ch_create_invalid_user():
    """Tests for AccessError for invalid user id.
    """
    state.set_state(s)
    
    # Create new channel from invalid user
    with pytest.raises(error.AccessError):
        channels.channels_create_v1(identifier.get_new_identifier(), "A channel", True)

def test_ch_create_invalid_name():
    """Tests for InputError for invalid/too long channel name.
    """
    state.set_state(s)
    
    # Create new channel with long name
    with pytest.raises(error.InputError):
        channels.channels_create_v1(user1_token, "A channel with a long name", True)

def test_ch_create_private():
    """Tests for successful creation of private channel.
    """
    state.set_state(s)
    
    # Create private channel
    c_name = "Private channel"
    c_id = channels.channels_create_v1(user1_token, c_name, False)["channel_id"]

    # Get list of all channels
    # This function includes private channels
    my_channels = channels.channels_listall_v1(user1_token)["channels"]
    
    assert my_channels[0]["name"] == c_name
    assert my_channels[0]["channel_id"] == c_id

def test_ch_create_empty_name():
    """Tests for successful creation of channel with an empty name.
    """
    state.set_state(s)
    # Create channel with empty name
    c_name = ""
    c_id = channels.channels_create_v1(user1_token, c_name, True)["channel_id"]

    # Get list of all channels
    my_channels = channels.channels_listall_v1(user1_token)["channels"]
    
    assert my_channels[0]["name"] == c_name
    assert my_channels[0]["channel_id"] == c_id

def test_ch_create_ensure_ownership():
    """Tests for the correct ownership of channels during creation.
    """
    # Ensure that the creator of a channel is granted ownership of it
    
    # Using s2 to ensure the results aren;t affected byt eh fact that user 1 is
    # a global owner
    state.set_state(s2)
    # Create channel with empty name
    c_name = "Channel"
    c_id = channels.channels_create_v1(user2_token, c_name, True)["channel_id"]

    # Get list of all channels
    c_details = channel.channel_details_v1(user2_token, c_id)
    
    # Remove references to profile pic as these are difficult to black-box
    for mem in c_details["all_members"]: mem.pop("profile_img_url")
    for mem in c_details["owner_members"]: mem.pop("profile_img_url")
    
    # Ensure creator was added by default as a channel owner and member
    assert c_details["owner_members"] == [u2_dict]
    assert c_details["all_members"] == [u2_dict]

# tests for channels_list_v1()
#
#######################################

def test_ch_list():
    """Tests for successful listing of channels.
    """
    state.set_state(s)
    
    # Create channel
    c_data = {"name": "Channel",}
    c_data["channel_id"] = channels.channels_create_v1(user1_token, c_data["name"], True)["channel_id"]
    
    my_channels = channels.channels_list_v1(user1_token)["channels"]
    
    assert c_data in my_channels

def test_ch_list_private_member():
    """Tests for successful listing private channels.
    """
    state.set_state(s)
    
    # Create channel
    c_data = {"name": "Hidden Channel",}
    c_data["channel_id"] = channels.channels_create_v1(user1_token, c_data["name"], False)["channel_id"]
    
    my_channels = channels.channels_list_v1(user1_token)["channels"]
    
    assert c_data in my_channels

def test_ch_list_private_not_member():
    """Tests for ensuring unainvited users not apart of private channel.
    """
    state.set_state(s2)
    # Set to state 2, with extra user
    
    # Create channel
    c_data = {"name": "Hidden Channel",}
    c_data["channel_id"] = channels.channels_create_v1(user1_token, c_data["name"], False)["channel_id"]
    
    # Ensure other user wasn't added as a member
    my_channels = channels.channels_list_v1(user2_token)["channels"]
    assert len(my_channels) == 0

def test_ch_list_public_not_member():
    """Tests for ensuring uninvited users not apart of public channel.
    """
    state.set_state(s2)
    # Set to state 2, with extra user
    
    # Create channel
    c_data = {"name": "Hidden Channel",}
    c_data["channel_id"] = channels.channels_create_v1(user1_token, c_data["name"], True)["channel_id"]
    
    # Ensure other user wasn't added as a member
    my_channels = channels.channels_list_v1(user2_token)["channels"]
    assert len(my_channels) == 0

def test_ch_list_many():
    """Tests successful listing of multiple channels.
    """
    state.set_state(s)
    
    # Create a LARGE_NUMBER of channels
    NUM_CH = LARGE_NUMBER
    ch_names = ["Channel " + str(i + 1) for i in range(NUM_CH)]
    ch_ids = [channels.channels_create_v1(user1_token, ch_names[i], True)["channel_id"]
              for i in range(NUM_CH)]
    
    my_channels = channels.channels_list_v1(user1_token)["channels"]
    
    assert len(my_channels) == NUM_CH
    for i in range(NUM_CH):
        assert \
            {
                "name": ch_names[i],
                "channel_id": ch_ids[i]
            } in my_channels

def test_ch_list_invalid_user():
    """Tests AccessError for invalid/fake user.
    """
    state.set_state(s)
    
    # List channels from invalid user
    with pytest.raises(error.AccessError):
        channels.channels_list_v1(identifier.get_new_identifier())

# tests for channel_listall_v1()
#
#######################################

def test_ch_listall():
    """Tests successful listing of all channels
    """
    state.set_state(s2)
    
    c1 = {"name": "C1"}
    c1["channel_id"] = channels.channels_create_v1(user1_token, c1["name"], True)["channel_id"]

    c2 = {"name": "C2"}
    c2["channel_id"] = channels.channels_create_v1(user2_token, c2["name"], True)["channel_id"]
    
    all_channels = channels.channels_listall_v1(user1_token)["channels"]
    
    assert c1 in all_channels and c2 in all_channels

def test_ch_listall_private():
    """Tests listing of all private channels.
    """
    state.set_state(s2)
    
    c1 = {"name": "C1"}
    c1["channel_id"] = channels.channels_create_v1(user1_token, c1["name"], False)["channel_id"]

    c2 = {"name": "C2"}
    c2["channel_id"] = channels.channels_create_v1(user2_token, c2["name"], False)["channel_id"]
    
    all_channels = channels.channels_listall_v1(user1_token)["channels"]
    
    assert c1 in all_channels and c2 in all_channels

def test_ch_listall_many():
    """Tests listing of all channels if there are many channels.
    """
    state.set_state(s2)
    
    # Create a LARGE_NUMBER of channels
    NUM_CH = LARGE_NUMBER
    ch_names = ["Channel " + str(i + 1) for i in range(NUM_CH)]
    ch_ids = [channels.channels_create_v1(user1_token, ch_names[i], True)["channel_id"]
              for i in range(NUM_CH)]
    
    all_channels = channels.channels_listall_v1(user2_token)["channels"]
    
    assert len(all_channels) == NUM_CH
    for i in range(NUM_CH):
        assert \
            {
                "name": ch_names[i],
                "channel_id": ch_ids[i]
            } in all_channels
    
    

def test_ch_listall_invalid_user():
    """Tests AccessError for invalid/fake user id.
    """
    state.set_state(s)
    
    # List all channels from invalid user
    with pytest.raises(error.AccessError):
        channels.channels_listall_v1(identifier.get_new_identifier())
