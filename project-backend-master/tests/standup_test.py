"""Tests for standups

Author: Miguel Guthridge [z5312085@ad.unsw.edu.au]
"""

import time, datetime
import pytest

from src import auth, state, channels, channel, standup, error, other

other.clear_v1()

# Register users
user1 = auth.auth_register_v1("hayden@email.com", "123456", "Hay", "den")
user2 = auth.auth_register_v1("rob@email.com", "123456", "Ro", "b")
user3 = auth.auth_register_v1("michelle@email.com", "123456", "Mi", "chelle")
user4 = auth.auth_register_v1("isaac@email.com", "123456", "Isa", "ac")

ch_id = channels.channels_create_v1(user1["token"], "Channel", True)["channel_id"]
channel.channel_join_v1(user2["token"], ch_id)
channel.channel_join_v1(user3["token"], ch_id)
channel.channel_join_v1(user4["token"], ch_id)

# Create member that isn't in the channel
user5 = auth.auth_register_v1("person@email.com", "123456", "Per", "son")

s = state.get_state()

def test_standup_example():
    """Check that standups work using the example test from README.md
    """
    state.set_state(s)
    
    # Create a standup in channel, lasting one second (otherwise the test will 
    # take ages)
    standup_info = standup.standup_start_v1(user1["token"], ch_id, 1)
    # Ensure that we got the correct return value
    assert abs(standup_info["time_finish"] -\
        (int(datetime.datetime.now().timestamp()) + 1)) < 2

    # Send messages in the channel
    standup.standup_send_v1(user1["token"], ch_id, "I ate a catfish")
    standup.standup_send_v1(user2["token"], ch_id, "I went to kmart")
    standup.standup_send_v1(user3["token"], ch_id, "I ate a toaster")
    standup.standup_send_v1(user4["token"], ch_id, "my catfish ate a toaster")
    
    # Ensure that a stand-up is active
    standup_info = standup.standup_active_v1(user1["token"], ch_id)
    assert standup_info["is_active"] == True
    assert abs(standup_info["time_finish"] -\
        (int(datetime.datetime.now().timestamp()) + 1)) < 2
    
    # Ensure that no messages have been sent in the channel... yet
    msgs = channel.channel_messages_v1(user1["token"], ch_id, 0)["messages"]
    assert len(msgs) == 0
    
    # Wait a second then check that the standup has been sent
    time.sleep(1)
    msgs = channel.channel_messages_v1(user1["token"], ch_id, 0)["messages"]
    assert len(msgs) == 1
    assert msgs[0]["u_id"] == user1["auth_user_id"]
    assert msgs[0]["message"] == (
                                "hayden: I ate a catfish\n"
                                "rob: I went to kmart\n"
                                "michelle: I ate a toaster\n"
                                "isaac: my catfish ate a toaster"
                                )
    
    # Ensure that a stand-up isn't active anymore
    standup_info = standup.standup_active_v1(user1["token"], ch_id)
    assert standup_info["is_active"] == False
    assert standup_info["time_finish"] == None

def test_standup_create_bad_channel():
    state.set_state(s)
    
    # Create a standup in channel, with a bad channel id
    with pytest.raises(error.InputError):
        standup.standup_start_v1(user1["token"], 0, 1)

def test_standup_create_no_time():
    state.set_state(s)
    # Create a standup in channel with no length
    with pytest.raises(error.InputError):
        standup.standup_start_v1(user1["token"], ch_id, 0)

def test_standup_create_negative_time():
    state.set_state(s)
    # Create a standup with negaive length
    with pytest.raises(error.InputError):
        standup.standup_start_v1(user1["token"], ch_id, -1)

def test_standup_create_already_active():
    state.set_state(s)
    # Create a standup in the same channel twice
    standup.standup_start_v1(user1["token"], ch_id, 1000)
    with pytest.raises(error.InputError):
        standup.standup_start_v1(user1["token"], ch_id, 1)

def test_standup_active():
    state.set_state(s)
    standup.standup_start_v1(user1["token"], ch_id, 1)
    
    # Ensure that a stand-up is active
    standup_info = standup.standup_active_v1(user1["token"], ch_id)
    assert standup_info["is_active"] == True
    assert abs(standup_info["time_finish"] -\
        (int(datetime.datetime.now().timestamp()) + 1)) < 2

def test_standup_active_long():
    state.set_state(s)
    standup.standup_start_v1(user1["token"], ch_id, 1000)
    
    # Ensure that a stand-up is active
    standup_info = standup.standup_active_v1(user1["token"], ch_id)
    assert standup_info["is_active"] == True
    assert abs(standup_info["time_finish"] -\
        (int(datetime.datetime.now().timestamp()) + 1000)) < 2

def test_standup_not_active():
    state.set_state(s)
    # Ensure that a stand-up isn't active
    standup_info = standup.standup_active_v1(user1["token"], ch_id)
    assert standup_info["is_active"] == False
    assert standup_info["time_finish"] == None

def test_standup_message_send():
    state.set_state(s)
    standup.standup_start_v1(user1["token"], ch_id, 1)
    
    standup.standup_send_v1(user2["token"], ch_id, "Hello")
    
    # Ensure the message hasn't sent
    msgs = channel.channel_messages_v1(user1["token"], ch_id, 0)["messages"]
    assert len(msgs) == 0
    
    # Wait a second and ensure the standup was sent
    time.sleep(1)
    msgs = channel.channel_messages_v1(user1["token"], ch_id, 0)["messages"]
    assert len(msgs) == 1
    assert msgs[0]["u_id"] == user1["auth_user_id"]
    assert msgs[0]["message"] == "rob: Hello"

def test_standup_send_not_active():
    state.set_state(s)
    with pytest.raises(error.InputError):
        standup.standup_send_v1(user2["token"], ch_id, "Hello")

def test_standup_send_bad_channel():
    state.set_state(s)
    with pytest.raises(error.InputError):
        standup.standup_send_v1(user2["token"], 0, "Hello")

def test_standup_send_no_msg():
    state.set_state(s)
    standup.standup_start_v1(user1["token"], ch_id, 1)
    with pytest.raises(error.InputError):
        standup.standup_send_v1(user2["token"], ch_id, "")

def test_standup_send_long_msg():
    state.set_state(s)
    standup.standup_start_v1(user1["token"], ch_id, 1)
    with pytest.raises(error.InputError):
        standup.standup_send_v1(user2["token"], ch_id, "Hi"*501)

def test_standup_send_too_slow():
    state.set_state(s)
    standup.standup_start_v1(user1["token"], ch_id, 1)
    # Wait a second before sending standup
    # Standup will have expired by then
    time.sleep(1)
    with pytest.raises(error.InputError):
        standup.standup_send_v1(user2["token"], ch_id, "Hello")

def test_standup_send_non_member():
    state.set_state(s)
    standup.standup_start_v1(user1["token"], ch_id, 1)
    with pytest.raises(error.AccessError):
        standup.standup_send_v1(user5["token"], ch_id, "Example")
