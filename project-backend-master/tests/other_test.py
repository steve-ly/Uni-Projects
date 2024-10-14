"""tests > other_test.py

Provides tests for functions in src > other.py

Primary Contributors: 
 - Danny Won [z5338486@ad.unsw.edu.au]
     - All tests

Minor Contributors:
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]
     - Bug fixes
         - (Commit 1fd39afe)

"""

import pytest
import datetime, time

from src.echo import echo
from src.error import InputError, AccessError
from src import state, auth, user, identifier, channels, channel, message, other, dm


# Reset the state
other.clear_v1()


############################################
# Testing clear_v1()
#
############################################

def test_clear_users():
    """Tests successful clear of users with InputError.
    """
    other.clear_v1()
    auth.auth_register_v1("test@email.com", "password", "John", "Smith")

    # Clear
    other.clear_v1()

    # Check if user still exists/can be accessed
    with pytest.raises(InputError):
        auth.auth_login_v1("test@email.com", "password")

def test_clear_channels():
    """Tests successful clear of channels with InputError.
    """
    other.clear_v1()
    user1 =  auth.auth_register_v1("test@email.com", "password", "John", "Smith")
    user_token = user1["token"]
    # Add channels
    ch_id = channels.channels_create_v1(user_token, "Channel 1", True)["channel_id"]

    # Clear
    other.clear_v1()
    
    # Add the user back to check, since it was also cleared
    user_token = auth.auth_register_v1("test@email.com", "password", "John", "Smith")["token"]

    # Check if channel still exists
    # This should raise InputError("Channel doesn't exist") before 
    # AccessError("User not a member of channel") as per assumptions.md
    with pytest.raises(InputError):
        channel.channel_details_v1(user_token, ch_id)

def test_clear_messages():
    other.clear_v1()
    user_token = auth.auth_register_v1("test@email.com", "password", "John", "Smith")["token"]

    # Add messages
    ch_id = channels.channels_create_v1(user_token, "Channel 1", True)["channel_id"]
    message.message_send_v1(user_token, ch_id, "This should go away")

    # Clear
    other.clear_v1()
    
    # Add the user back to check, since it was also cleared
    user_token = auth.auth_register_v1("test@email.com", "password", "John", "Smith")["token"]

    # Check if message still exists
    with pytest.raises(InputError):
        channel.channel_messages_v1(user_token, ch_id, 0)


############################################
# Testing search_v2()
#
############################################

# Make users and messages to test with

# Length = 1030 characters
a_too_long_string = """
According to all known laws of aviation, there is no way a bee should be able to
fly. Its wings are too small to get its fat little body off the ground. The bee,
of course, flies anyway because bees don't care what humans think is impossible.
Yellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and
yellow! Let's shake it up a little. Barry! Breakfast is ready! Ooming! Hang on a
second. Hello?
- Barry?
- Adam?
- Oan you believe this is happening?
- I can't. I'll pick you up.
Looking sharp. Use the stairs. Your father paid good money for those. Sorry. I'm
. Here's the graduate. We're very proud of you, son. A perfect report card, all
B's. Very proud. Ma! I got a thing going here.
- You got lint on your fuzz.
- Ow! That's me!
- Wave to us! We'll be in row 118,000.
- Bye!
Barry, I told you, stop flying in the house!
- Hey, Adam.
- Hey, Barry.
- Is that fuzz gel?
- A little. Special day, graduation.
Never thought I'd make it. Three days grade school, three days high school.
Those were awkward.
"""
# Length = 170 characters
a_long_string = """
Ok birds aren’t real and here’s my supporting evidence. 1. Have you ever seen a dead 
bird. Like one of those black birds that you see flying around? No. 2. Birds have 
cameras in them and are spying on humans. The government created these robots to spy 
on us and look for any suspicious or criminal activities. That’s why they sit on wires, 
they pick up the electrical currents to charge themselves. If they don’t, they will die. 
3. Birds fly in packs so you can’t capture them. If there was a single bird, you could 
EASILY capture it. Not when there are 400. Plus, when there are 400, you get MUCH better 
angles. No one is safe. 4. Birds fly away from people. You can’t get near a bird, ever. 
They fly away. Science tells us it’s because they evolved that way to avoid predators, 
but it’s not. They were programmed that way to stop humans from capturing them and 
discovering the cameras. Birds aren’t real, they are robots.
"""

# Reset state
other.clear_v1()

user_1 = auth.auth_register_v1("test1@email.com", "password", "John", "Smith")
user_2 = auth.auth_register_v1("test2@email.com", "password", "Jane", "Doe")
user_3 = auth.auth_register_v1("test3@email.com", "password", "Shrek", "TheFourth")
user_id1 = user_1["auth_user_id"]
user_id2 = user_2["auth_user_id"]
user_id3 = user_3["auth_user_id"]
user1_token = user_1["token"]
user2_token = user_2["token"]
user3_token = user_3["token"]
u_ids = [user_id1, user_id2]

ch_id1 = channels.channels_create_v1(user1_token, "Channel 1", True)["channel_id"]
ch_id2 = channels.channels_create_v1(user2_token, "Channel 2", True)["channel_id"]
ch_id3 = channels.channels_create_v1(user3_token, "Channel 3", True)["channel_id"]

m_id1 = message.message_send_v1(user1_token, ch_id1, "Danny is cool")["message_id"]
m_id2 = message.message_send_v1(user2_token, ch_id2, a_long_string)["message_id"]

user_4 = auth.auth_register_v1("test4@email.com", "password", "Nic", "Rodwell")
user_5 =auth.auth_register_v1("test5@email.com", "password", "Harrison", "Chong")
user_6 = auth.auth_register_v1("test6@email.com", "password", "Liang", "Pan")

user_id4 = user_4["auth_user_id"]
user_id5 = user_5["auth_user_id"]
user_id6 = user_6["auth_user_id"]

user4_token = user_4["token"]
user5_token = user_5["token"]
user6_token = user_6["token"]

u_ids2 = [user_id4, user_id5]
dm_id1 = dm.dm_create_v1(user4_token, u_ids2)["dm_id"]
dm_id2 = dm.dm_create_v1(user5_token, u_ids2)["dm_id"]
m_id5 = dm.dm_message_send_v1(user4_token, dm_id1, "Birds aren't real")["message_id"]
m_id6 = dm.dm_message_send_v1(user5_token, dm_id2, a_long_string)["message_id"]

# For Tagging
user3 = user.user_profile_v1(user1_token, user_id3)["user"]
user3Handle = "@" + user3["handle_str"]
m_id3 = message.message_send_v1(user3_token, ch_id3, user3Handle)["message_id"]

user2 = user.user_profile_v1(user1_token, user_id2)["user"]
user2Handle = "@" + user2["handle_str"]
m_id21 = message.message_send_v1(user2_token, ch_id2, user2Handle)["message_id"]
m_id22 = message.message_send_v1(user2_token, ch_id2, user2Handle)["message_id"]

s = state.get_state()

def test_search_empty():
    state.set_state(s)

    # InputError
    with pytest.raises(InputError):
        other.search_v2(user1_token, "")

def test_search_over1000():
    state.set_state(s)

    # InputError
    with pytest.raises(InputError):
        other.search_v2(user1_token, a_too_long_string)

def test_search_short():
    state.set_state(s)

    # Successful search
    ret_msg = other.search_v2(user1_token, "Danny is cool")

    assert ret_msg["messages"][0]["message"] == "Danny is cool"
    assert ret_msg["messages"][0]["message_id"] == m_id1
    assert ret_msg["messages"][0]["u_id"] == user_id1
    assert len(ret_msg["messages"]) == 1

def test_search_short_dm():
    state.set_state(s)

    # Successful search
    ret_msg = other.search_v2(user4_token, "Birds aren't real")
    assert ret_msg["messages"][0]["message"] == "Birds aren't real"
    assert ret_msg["messages"][0]["message_id"] == m_id5
    assert ret_msg["messages"][0]["u_id"] == user_id4
    assert len(ret_msg["messages"]) == 1 # it's sent in the setup

def test_search_long():
    state.set_state(s)

    # Successful search
    ret_msg = other.search_v2(user2_token, a_long_string)

    assert ret_msg["messages"][0]["message"] == a_long_string
    assert ret_msg["messages"][0]["message_id"] == m_id2
    assert ret_msg["messages"][0]["u_id"] == user_id2

def test_search_long_dm():
    state.set_state(s)

    # Successful search
    ret_msg = other.search_v2(user5_token, a_long_string)

    assert ret_msg["messages"][0]["message"] == a_long_string
    assert ret_msg["messages"][0]["message_id"] == m_id6
    assert ret_msg["messages"][0]["u_id"] == user_id5

def test_search_nonexistent():
    state.set_state(s)

    ret_msg = other.search_v2(user1_token, "Shrek")
    assert len(ret_msg["messages"]) == 0

    ret_msg2 = other.search_v2(user4_token, "Swamp")
    assert len(ret_msg2["messages"]) == 0

def test_search_tagging():
    state.set_state(s)

    # Successful tagging
    ret_msg = other.search_v2(user3_token, user3Handle)

    assert ret_msg["messages"][0]["message"] == user3Handle
    assert ret_msg["messages"][0]["message_id"] == m_id3
    assert ret_msg["messages"][0]["u_id"] == user_id3

def test_search_multiple_message_search():
    state.set_state(s)

    # Successful tagging
    ret_msg = other.search_v2(user2_token, user2Handle)

    assert ret_msg["messages"][1]["message"] == user2Handle
    assert ret_msg["messages"][1]["message_id"] == m_id21
    assert ret_msg["messages"][1]["u_id"] == user_id2

    assert ret_msg["messages"][0]["message"] == user2Handle
    assert ret_msg["messages"][0]["message_id"] == m_id22
    assert ret_msg["messages"][0]["u_id"] == user_id2

def test_search_DMs():
    state.set_state(s)
    dm_id1 = dm.dm_create_v1(user1_token, u_ids)["dm_id"]
    # dm_id2 = DM.dm_create_v1(user_id2, u_ids)["dm_id"]
    m_id1 = dm.dm_message_send_v1(user1_token, dm_id1, "SlidingintoDms")["message_id"]
    ret_msg = other.search_v2(user1_token, "SlidingintoDms")

    assert ret_msg["messages"][0]["message"] == "SlidingintoDms"
    assert ret_msg["messages"][0]["message_id"] == m_id1
    assert ret_msg["messages"][0]["u_id"] == user_id1
    
    m_id2 = dm.dm_message_send_v1(user1_token, dm_id1, "SlidingintoDms2")["message_id"]
    ret_msg = other.search_v2(user1_token, "SlidingintoDms2")

    assert ret_msg["messages"][0]["message"] == "SlidingintoDms2"
    assert ret_msg["messages"][0]["message_id"] == m_id2
    assert ret_msg["messages"][0]["u_id"] == user_id1

def test_search_delayed_message_search():
    state.set_state(s)

    # Make delayed msg
    delay = datetime.datetime.now().timestamp() + 1
    message.message_send_later_v1(user2_token, ch_id2, "delayed msg", delay)["message_id"]

    # Successful tagging
    ret_msg = other.search_v2(user2_token, "delayed msg")

    # Check delayed message doesnt show
    assert len(ret_msg["messages"]) == 0 

def test_search_delayed_message_search_sent():
    state.set_state(s)

    # Make delayed msg
    delay = datetime.datetime.now().timestamp() + 1
    message.message_send_later_v1(user2_token, ch_id2, "delayed msg", delay)["message_id"]

    time.sleep(1)
    # Successful tagging
    ret_msg = other.search_v2(user2_token, "delayed msg")

    # Check delayed message shows
    assert len(ret_msg["messages"]) == 1
    assert ret_msg["messages"][0]["message"] == "delayed msg"
    assert ret_msg["messages"][0]["u_id"] == user_id2
