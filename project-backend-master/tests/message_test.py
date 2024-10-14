"""tests > message_test.py

Tests for src > message.py.

Author: Miguel Guthridge [z5312085]
Email: z5312085@ad.unsw.edu.au

"""

import pytest
import datetime, time

from src import other, channels, channel, message, error, auth, identifier, state, dm, notification

# Length = 1030 characters
# Use this copypasta to try to send or edit messages to be over 1000 characters
a_long_string = """
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

other.clear_v1()

# Set a user to do actions through
user1 = auth.auth_register_v1("someone@example.com", "Password1", "John", "Doe")
user_id = user1["auth_user_id"]
user_token = user1["token"]

# Set up a channel to do actions in
channel_id = channels.channels_create_v1(user_token, "Channel 1", True)["channel_id"]

# Add the user to the channel
channel.channel_join_v1(user_token, channel_id)

s = state.get_state()

# Set another user to check things through
user2 = auth.auth_register_v1("someone.else@example.com", "Password1", "Jane", "Doe")
user2_id = user2["auth_user_id"]
user2_token = user2["token"]
s2 = state.get_state()

# Add channel2 and add user2 to channel
channel2_id = channels.channels_create_v1(user_token, "Channel 2", True)["channel_id"]
channel.channel_join_v1(user2_token, channel_id)
dm_id = dm.dm_create_v1(user_token, [user_id, user2_id])["dm_id"]
s3 = state.get_state()

def test_share_message_invalid_user():
    """Test sharing a message to a channel successfully without additional message.
    """
    state.set_state(s3)

    # User2 sends a message to channel
    og_msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]
    
    # Access error: user2 is not a member of channel2
    with pytest.raises(error.AccessError):
        message.message_share_v1(user2_token, og_msg_id, 'Goodbye world', channel2_id, -1)


#  Testing message_send_v1()
#
#######################################


def test_send_message():
    """Generic message send. Just sends a normal message
    """
    state.set_state(s)
    msg_id = message.message_send_v1(user_token, channel_id, "Hello world")["message_id"]
    
    msgs_in_ch = channel.channel_messages_v1(user_token, channel_id, 0)["messages"]
    
    # Check most recent message
    assert msgs_in_ch[0]["message_id"] == msg_id
    # Also check whether message contents are correct: sender, message_str
    assert msgs_in_ch[0]["message"] == "Hello world"
    assert msgs_in_ch[0]["u_id"] == user_id
    
def test_msg_too_long():
    """Try to send a message over 1000 characters
    """
    state.set_state(s)
    # Input error: message too long
    with pytest.raises(error.InputError):
        message.message_send_v1(user_token, channel_id, a_long_string)
    

def test_send_msg_inaccessible_channel():
    """Try to send a message in a channel that the user isn't a member of
    """
    state.set_state(s2)
    # Create new channel
    inaccessible_channel = channels.channels_create_v1(user_token, "Inaccessible", True)["channel_id"]
    
    # Access error: not a member of the channel
    with pytest.raises(error.AccessError):
        message.message_send_v1(user2_token, inaccessible_channel, "Goodbye world!")

def test_send_msg_nonexistent_channel():
    """Try to send a message in a channel that doesn't exist
    """
    state.set_state(s)
    fake_channel_id = identifier.get_new_identifier()
    
    # Access error: channel doesn't exist
    with pytest.raises(error.InputError):
        message.message_send_v1(user_token, fake_channel_id, "Goodbye world!")

def test_send_msg_nonexistent_user():
    """Try to send a message from a user that doesn't exist
    """
    state.set_state(s)
    fake_user_id = identifier.get_new_identifier()
    
    # Access error: user doesn't exist
    with pytest.raises(error.AccessError):
        message.message_send_v1(fake_user_id, channel_id, "Goodbye world!")

def test_send_msg_empty():
    """Try to send an empty message
    """
    state.set_state(s)
    # See assumptions.md for note on this
    # TODO: Clarify this!!!!
    
    # Input error: empty message
    with pytest.raises(error.InputError):
        message.message_send_v1(user_token, channel_id, "")

def test_timestamp():
    """
    Verify that the timestamp that the message is sent at corresponds to 
    the current time
    """
    # Locally import time, since we don't need it outside of this function
    import time
    state.set_state(s)

    # This assumes that time doesn't advance by more than a second between the 
    # operations
    msg_time = int(time.time())
    message.message_send_v1(user_token, channel_id, "Hello world")["message_id"]
    
    # Ensure the times are equal
    assert channel.channel_messages_v1(user_token, channel_id, 0)\
        ["messages"][0]["time_created"] == msg_time


# Testing message_send_later_v1()
#
#######################################

def test_send_later_message():
    """Generic message send. Just sends a normal message
    """
    state.set_state(s)
    delay = datetime.datetime.now().timestamp() + 1
    message.message_send_later_v1(user_token, channel_id, "Hello world", delay)
    
    msgs_in_ch = channel.channel_messages_v1(user_token, channel_id, 0)["messages"]
    
    # Check most recent message
    assert len(msgs_in_ch) == 0


def test_send_later_message_sent():
    """Generic message send later. Just sends a normal message, Checks after delay
    """
    state.set_state(s)
    delay = datetime.datetime.now().timestamp() + 1
    msg_id = message.message_send_later_v1(user_token, channel_id, "Hello world", delay)["message_id"]
    
    time.sleep(1)
    msgs_in_ch = channel.channel_messages_v1(user_token, channel_id, 0)["messages"]
    
    # Check most recent message
    assert msgs_in_ch[0]["message_id"] == msg_id
    # Also check whether message contents are correct: sender, message_str
    assert msgs_in_ch[0]["message"] == "Hello world"
    assert msgs_in_ch[0]["u_id"] == user_id
    
def test_msg_send_later_too_long():
    """Try to send a message over 1000 characters
    """
    state.set_state(s)
    # Input error: message too long
    delay = datetime.datetime.now().timestamp() + 1
    with pytest.raises(error.InputError):
        message.message_send_later_v1(user_token, channel_id, a_long_string, delay)
    

def test_send_later_msg_inaccessible_channel():
    """Try to send a message in a channel that the user isn't a member of
    """
    state.set_state(s2)
    delay = datetime.datetime.now().timestamp() + 1
    # Create new channel
    inaccessible_channel = channels.channels_create_v1(user_token, "Inaccessible", True)["channel_id"]
    
    # Access error: not a member of the channel
    with pytest.raises(error.AccessError):
        message.message_send_later_v1(user2_token, inaccessible_channel, "Goodbye world!", delay)

def test_send_later_msg_nonexistent_channel():
    """Try to send a message in a channel that doesn't exist
    """
    state.set_state(s)
    delay = datetime.datetime.now().timestamp() + 1
    fake_channel_id = identifier.get_new_identifier()
    
    # Access error: channel doesn't exist
    with pytest.raises(error.InputError):
        message.message_send_later_v1(user_token, fake_channel_id, "Goodbye world!", delay)

def test_send_later_msg_nonexistent_user():
    """Try to send a message from a user that doesn't exist
    """
    state.set_state(s)
    delay = datetime.datetime.now().timestamp() + 1
    fake_user_id = identifier.get_new_identifier()
    
    # Access error: user doesn't exist
    with pytest.raises(error.AccessError):
        message.message_send_later_v1(fake_user_id, channel_id, "Goodbye world!", delay)

def test_send_later_msg_empty():
    """Try to send an empty message
    """
    state.set_state(s)
    delay = datetime.datetime.now().timestamp() + 1
    # See assumptions.md for note on this
    # TODO: Clarify this!!!!
    
    # Input error: empty message
    with pytest.raises(error.InputError):
        message.message_send_later_v1(user_token, channel_id, "", delay)


#  Testing message_remove_v1()
#
#######################################

# Although this function isn't required until iteration 2, I've implemented it
# as it is called by message_edit_v1() when it is passed an empty string.
def test_remove_msg():
    state.set_state(s)
    
    # Send a message
    m_id = message.message_send_v1(user_token, channel_id, "This message should be deleted.")["message_id"]
    # Deletes it
    message.message_remove_v1(user_token, m_id)
    
    msgs_in_ch = channel.channel_messages_v1(user_token, channel_id, 0)["messages"]
    # There should be no messages there anymore
    assert len(msgs_in_ch) == 0

def test_remove_msg_not_sender():
    state.set_state(s2)
    
    # Join the channel
    channel.channel_join_v1(user2_token, channel_id)
    
    # Send a message from first account
    m_id = message.message_send_v1(user_token, channel_id, "This message shouldn't be deleted.")["message_id"]
    
    # Try to delete it from John's account
    # Should raise exception since he didn't send it
    with pytest.raises(error.AccessError):
        message.message_remove_v1(user2_token, m_id)

def test_remove_msg_is_owner():
    state.set_state(s)
    
    other_user = auth.auth_register_v1("someone.else@example.com", "Password1", "Ada", "Lovelace")
    other_user_token = other_user["token"]
    other_user_id = other_user["auth_user_id"]
    # Add her to the channel
    channel.channel_invite_v1(user_token, channel_id, other_user_id)
    
    # Send a message from John's account
    m_id = message.message_send_v1(user_token, channel_id, "This message should be deleted.")["message_id"]
    
    # Make Ada an admin of the channel
    channel.channel_addowner_v1(user_token, channel_id, other_user_id)
    
    # Delete it from Ada's account - since she's an owner of the channel now it should work
    message.message_remove_v1(other_user_token, m_id)
    
    msgs_in_ch = channel.channel_messages_v1(user_token, channel_id, 0)["messages"]
    # There should be no messages there anymore
    assert len(msgs_in_ch) == 0

def test_remove_msg_global_owner():
    """Check that a global owner can remove a message that they didn't send,
    even if they aren't in the channel
    """
    state.set_state(s)
    
    other_user = auth.auth_register_v1("someone.else@example.com", "Password1", "Ada", "Lovelace")
    other_user_token = other_user["token"]
    
    # Create new channel
    channel_2 = channels.channels_create_v1(other_user_token, "Channel 2", True)["channel_id"]
    
    # Send a message from Ada's account
    m_id = message.message_send_v1(other_user_token, channel_2, "This message should be deleted.")["message_id"]
    
    # Delete it from John's account - since he's an owner of the channel by default it should work
    message.message_remove_v1(user_token, m_id)
    
    msgs_in_ch = channel.channel_messages_v1(other_user_token, channel_2, 0)["messages"]
    # There should be no messages there anymore
    assert len(msgs_in_ch) == 0

def test_remove_msg_invalid_id():
    state.set_state(s)
    # Try to delete a message
    # Should raise exception since there is no message
    with pytest.raises(error.InputError):
        message.message_remove_v1(user_token, identifier.get_new_identifier())

def test_remove_msg_invalid_user():
    state.set_state(s)
    
    m_id = message.message_send_v1(user_token, channel_id, "This message shouldn't be deleted.")["message_id"]
    
    # Try to delete a message
    # Should raise exception since there is no user
    with pytest.raises(error.AccessError):
        message.message_remove_v1(identifier.get_new_identifier(), m_id)

# Testing message_edit_v1()
#
#######################################

def test_edit_msg():
    """Generic message edit. Just edit a message normally
    """
    state.set_state(s)
    m_id = message.message_send_v1(user_token, channel_id, "Message wiht a typo")["message_id"]
    
    fixed_str = "Message without a typo"
    message.message_edit_v1(user_token, m_id, fixed_str)

    msgs_in_ch = channel.channel_messages_v1(user_token, channel_id, 0)["messages"]
    
    # Check most recent message
    assert msgs_in_ch[0]["message_id"] == m_id
    assert msgs_in_ch[0]["message"] == fixed_str

def test_edit_msg_not_sender():
    """Try to edit a message that the user didn't send
    """
    state.set_state(s)
    
    a_beautiful_message = "I sure hope someone doesn't try to hack " + \
                          "UNSW Dreams and change what my message says"
    
    m_id = message.message_send_v1(user_token, channel_id, a_beautiful_message)["message_id"]
    
    # Create another account
    other_user = auth.auth_register_v1("hacker@russianbots.com", "qyrA8q90yfqO33g35t54y", "Russian", "Hacker")["token"]
    
    # Try to edit it from the other account
    # Should raise exception since they didn't send it
    with pytest.raises(error.AccessError):
        message.message_edit_v1(other_user, m_id, "Hahahahha get trolled I edited yr message")
        # The poor hacker is (hopefully) no match for UNSW Dreams's state-of-the-art security measures
    
    # Ensure the message didn't get edited
    msgs_in_ch = channel.channel_messages_v1(user_token, channel_id, 0)["messages"]
    # The message contents should be the same
    assert msgs_in_ch[0]["message"] == a_beautiful_message

def test_edit_msg_is_owner():
    """Try to edit a message as a channel owner (but not a global owner)
    """
    state.set_state(s)
    
    other_user = auth.auth_register_v1("someone.else@example.com", "Password1", "Ada", "Lovelace")
    other_user_token = other_user["token"]
    other_user_id = other_user["auth_user_id"]
    
    # Add her to the channel
    channel.channel_invite_v1(user_token, channel_id, other_user_id)
    
    # Send a message from John's account
    m_id = message.message_send_v1(user_token, channel_id, "This message should be edited.")["message_id"]
    
    # Make Ada an admin of the channel
    channel.channel_addowner_v1(user_token, channel_id, other_user_id)
    
    # Edit it from Ada's account - since she's an owner of the channel now it should work
    message.message_edit_v1(other_user_token, m_id, "The message should now be edited")
    
    msgs_in_ch = channel.channel_messages_v1(user_token, channel_id, 0)["messages"]
    # The message should be edited
    assert msgs_in_ch[0]["message"] == "The message should now be edited"

def test_edit_msg_global_owner():
    """Check that a global owner can edit a message that they didn't send,
    even if they aren't in the channel
    """
    state.set_state(s)
    
    other_user = auth.auth_register_v1("someone.else@example.com", "Password1", "Ada", "Lovelace")["token"]
    
    # Create new channel
    channel_2 = channels.channels_create_v1(other_user, "Channel 2", True)["channel_id"]
    
    # Send a message from Ada's account
    m_id = message.message_send_v1(other_user, channel_2, "This message should be deleted.")["message_id"]
    
    # Edit it from John's account - since he's an owner of the channel by default it should work
    message.message_edit_v1(user_token, m_id, "The message should now be edited")
    
    msgs_in_ch = channel.channel_messages_v1(other_user, channel_2, 0)["messages"]
    
    # The message should be edited
    assert msgs_in_ch[0]["message"] == "The message should now be edited"

def test_edit_msg_invalid_id():
    """Try to edit a message that doesn't exist
    """
    state.set_state(s)
    # Try to edit a non-existant message
    # Should raise exception since it doesn't exist
    with pytest.raises(error.InputError):
        message.message_edit_v1(user_token, identifier.get_new_identifier(), "Wow this message is so creative")

def test_edit_msg_invalid_user():
    """Try to edit a message using a user ID that doesn't exist
    """
    state.set_state(s)
    m_id = message.message_send_v1(user_token, channel_id, "Yet another creative message")["message_id"]
    
    # Try to edit it using a new unique identifier to emulate a user that doesn't exist
    # Should raise an AccessError exception
    with pytest.raises(error.AccessError):
        message.message_edit_v1(identifier.get_new_identifier(), m_id, 
                                "But not as creative as this edit would have been")

def test_edit_msg_too_long():
    """Try to edit the message and make it too long
    """
    state.set_state(s)
    
    a_funny_message = "<Place holder for some kind of copypasta>"
    
    m_id = message.message_send_v1(user_token, channel_id, a_funny_message)["message_id"]

    # Try to edit it to be a long string (>1000 characters)
    # Should raise an InputError exception
    with pytest.raises(error.InputError):
        message.message_edit_v1(user_token, m_id, a_long_string)
    
    # Ensure the message hasn't been edited
    msgs_in_ch = channel.channel_messages_v1(user_token, channel_id, 0)["messages"]
    # The message should be the same
    assert msgs_in_ch[0]["message"] == a_funny_message

def test_edit_msg_empty_delete():
    """Edit the message to be an empty string, thus deleting it
    """
    state.set_state(s)
    m_id = message.message_send_v1(user_token, channel_id, "Nice message you got there.... it would be a shame " +
                                   "if it were to be....." +
                                   " deleted")["message_id"]
    
    # Edit it to nothing... this should delete it
    message.message_edit_v1(user_token, m_id, "")
    
    # Ensure the message has been deleted
    msgs_in_ch = channel.channel_messages_v1(user_token, channel_id, 0)["messages"]
    # There should be no messages there anymore
    assert len(msgs_in_ch) == 0


#  Testing message_share_v1()
#
#######################################

def test_share_message_channel_to_channel():
    """Test sharing a message to a channel successfully without additional message.
    """
    state.set_state(s3)

    # User2 sends a message to channel
    og_msg_id = message.message_send_v1(user_token, channel_id, "Hello world")["message_id"]

    # User shares the message to channel2
    msg_id = message.message_share_v1(user_token, og_msg_id, '', channel2_id, -1)["shared_message_id"]

    msgs_in_ch2 = channel.channel_messages_v1(user_token, channel2_id, 0)["messages"]
    
    # Check most recent message
    assert msgs_in_ch2[0]["message_id"] == msg_id
    # Also check whether message contents are correct: sender should be user, message content should have quotation marks.
    assert msgs_in_ch2[0]["message"] == '"""\nHello world\n"""'
    assert msgs_in_ch2[0]["u_id"] == user_id

def test_share_message_channel_to_channel_add_msgs():
    """Test sharing a message to a channel successfully with additional message.
    """
    state.set_state(s3)

    # User2 sends a message to channel
    og_msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # User shares the message to channel2 and adds some comments on it
    msg_id = message.message_share_v1(user_token, og_msg_id, 'Goodbye world', channel2_id, -1)["shared_message_id"]

    msgs_in_ch2 = channel.channel_messages_v1(user_token, channel2_id, 0)["messages"]
    
    # Check most recent message
    assert msgs_in_ch2[0]["message_id"] == msg_id
    # Also check whether message contents are correct: sender should be user, message content should have quotation marks.
    assert msgs_in_ch2[0]["message"] == '"""\nHello world\n"""\n\nGoodbye world'
    assert msgs_in_ch2[0]["u_id"] == user_id


def test_share_message_channel_to_dm():
    """Test sharing a message to a channel successfully without additional message.
    """
    state.set_state(s3)

    # User2 sends a message to channel
    og_msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]
    # User shares the message to dm
    msg_id = message.message_share_v1(user_token, og_msg_id, '', -1, dm_id)["shared_message_id"]
    msgs_in_dm = dm.dm_messages_v1(user_token, dm_id, 0)["messages"]
    from pprint import pprint
    pprint(msgs_in_dm)
    pprint(message.message_share_v1(user_token, og_msg_id, '', -1, dm_id))

    # Check most recent message
    assert msgs_in_dm[0]["message_id"] == msg_id
    # Also check whether message contents are correct: sender should be user, message content should have quotation marks.
    assert msgs_in_dm[0]["message"] == '"""\nHello world\n"""'
    assert msgs_in_dm[0]["u_id"] == user_id

def test_share_message_dm_to_channel():
    """Test sharing a message to a channel successfully without additional message.
    """
    state.set_state(s3)

    # User2 sends a message to dm
    og_msg_id = dm.dm_message_send_v1(user2_token, dm_id, "Hello world")["message_id"]

    # User shares the message to dm
    msg_id = message.message_share_v1(user_token, og_msg_id, '', channel2_id, dm_id)["shared_message_id"]

    msgs_in_ch = channel.channel_messages_v1(user_token, channel2_id, 0)["messages"]
    
    # Check most recent message
    assert msgs_in_ch[0]["message_id"] == msg_id
    # Also check whether message contents are correct: sender should be user, message content should have quotation marks.
    assert msgs_in_ch[0]["message"] == '"""\nHello world\n"""'
    assert msgs_in_ch[0]["u_id"] == user_id

def test_share_message_dm_to_dm():
    """Test sharing a message to a channel successfully without additional message.
    """
    state.set_state(s3)

    # User2 sends a message to dm
    og_msg_id = dm.dm_message_send_v1(user2_token, dm_id, "Hello world")["message_id"]

    # User shares the message to channel
    msg_id = message.message_share_v1(user_token, og_msg_id, '', -1, dm_id)["shared_message_id"]

    msgs_in_dm = dm.dm_messages_v1(user_token, dm_id, 0)["messages"]
    
    # Check most recent message
    assert msgs_in_dm[0]["message_id"] == msg_id
    # Also check whether message contents are correct: sender should be user, 
    # message content should have quotation marks.
    assert msgs_in_dm[0]["message"] == '"""\nHello world\n"""'
    assert msgs_in_dm[0]["u_id"] == user_id

def test_share_message_dm_while_not_in_dm_channel():
    """Test sharing a dm while not being in the dm group
    """
    state.set_state(s3)
    
    user3 = auth.auth_register_v1("helpplease.else@example.com", "Password1", "Im", "Inpain")
    user3_id = user3["auth_user_id"]
    user3_token = user3["token"]
    dm.dm_invite_v1(user_token, dm_id, user3_id)
    og = dm.dm_message_send_v1(user3_token, dm_id, "Hello world")["message_id"]
    dm_id2 = dm.dm_create_v1(user_token, [user_id, user2_id])["dm_id"]
    # User2 sends a message to dm
    with pytest.raises(error.AccessError):
        message.message_share_v1(user3_token, og, '', -1, dm_id2)["shared_message_id"]



def test_share_message_caption_too_long():
    """Test that users cannot share message with a caption that is more than 1000 chars
    """
    state.set_state(s3)

    # User2 sends a message to channel
    og_msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # User shares the message to channel2 and adds far too many comments comments to it
    with pytest.raises(error.InputError):
        message.message_share_v1(user_token, og_msg_id, 'A' * 1001, channel2_id, -1)

def test_share_message_update_original():
    """Test that shared messages are updated when the OG message is edited
    """
    state.set_state(s3)

    # User2 sends a message to channel
    og_msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # User shares the message to channel2 and adds some comments on it
    message.message_share_v1(user_token, og_msg_id, '', channel2_id, -1)["shared_message_id"]
    
    # User2 edits their original message
    message.message_edit_v1(user2_token, og_msg_id, "Goodbye world")

    msgs_in_ch2 = channel.channel_messages_v1(user_token, channel2_id, 0)["messages"]
    
    # Check most recent message to ensure it updated
    assert msgs_in_ch2[0]["message"] == '"""\nGoodbye world\n"""'

def test_share_message_delete_original():
    """Test that shared messages are updated when the OG message is deleted
    """
    state.set_state(s3)

    # User2 sends a message to channel
    og_msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # User shares the message to channel2 and adds some comments on it
    message.message_share_v1(user_token, og_msg_id, '', channel2_id, -1)["shared_message_id"]
    
    # User2 edits their original message
    message.message_remove_v1(user2_token, og_msg_id)

    msgs_in_ch2 = channel.channel_messages_v1(user_token, channel2_id, 0)["messages"]
    
    # Check most recent message to ensure it updated
    assert msgs_in_ch2[0]["message"] == '"""\n[Message deleted]\n"""'


#  Testing message_react_v1()
#
#######################################
def test_react_once():
    """Test that one user successfully reacts a message
    """
    state.set_state(s3)

    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # User reacts the message with react_id 1
    message.message_react_v1(user_token, msg_id, 1)

    # check the reacts is successfully added
    msg = channel.channel_messages_v1(user_token, channel_id, 0)
    react_dict = msg["messages"][0]["reacts"]
    assert react_dict[0]["react_id"] == 1
    assert user_id in react_dict[0]["u_ids"]

def test_react_several_times():
    """Test that several users successfully react a message
    """
    state.set_state(s3)

    # Create user3
    user3 = auth.auth_register_v1("11.else@example.com", "Password1", "Woo", "Hoo")
    user3_id = user3["auth_user_id"]
    user3_token = user3["token"]
    channel.channel_join_v1(user3_token, channel_id)

    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # User 1,2,3 reacts the message with react_id 1
    message.message_react_v1(user_token, msg_id, 1)
    message.message_react_v1(user2_token, msg_id, 1)
    message.message_react_v1(user3_token, msg_id, 1)

    # Check the reacts is successfully added
    msg = channel.channel_messages_v1(user_token, channel_id, 0)
    react_dict = msg["messages"][0]["reacts"]
    assert react_dict[0]["react_id"] == 1
    assert user_id in react_dict[0]["u_ids"]
    assert user2_id in react_dict[0]["u_ids"]
    assert user3_id in react_dict[0]["u_ids"]
    
def test_react_invalid_message():
    """Test that a user reacts a message with invalid message id
    """
    state.set_state(s3)
    with pytest.raises(error.InputError):
        message.message_react_v1(user_token, identifier.get_new_identifier(), 1)

def test_react_invalid_react_id():
    """Test that a user reacts a message with invalid message id
    """
    state.set_state(s3)
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]
    with pytest.raises(error.InputError):
        message.message_react_v1(user_token, msg_id, identifier.get_new_identifier())

def test_react_already_reacted():
    """Test that users reacts a message which is already reacted by theirself
    """
    state.set_state(s3)
    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # User reacts the message with react_id 1
    message.message_react_v1(user_token, msg_id, 1)
    # Raise InputError when user reacts the message again
    with pytest.raises(error.InputError):
        message.message_react_v1(user_token, msg_id, 1)

def test_react_user_not_in_channel():
    """Test that a user reacts a message with invalid message id
    """
    state.set_state(s3)

    # Create user3
    user3 = auth.auth_register_v1("11.else@example.com", "Password1", "Woo", "Hoo")
    user3_token = user3["token"]

    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    with pytest.raises(error.AccessError):
        message.message_react_v1(user3_token, msg_id, 1)

def test_react_notification():
    """Test that a user receives a notification when their message is reacted
    """
    state.set_state(s3)
    
    msg_id = message.message_send_v1(user_token, channel_id, "Hello")["message_id"]
    message.message_react_v1(user2_token, msg_id, 1)
    ntfns = notification.notification_get_v1(user_token)["notifications"]
    
    assert ntfns[0]["channel_id"] == channel_id
    assert ntfns[0]["dm_id"] == -1
    assert ntfns[0]["notification_message"]\
        ==  "johndoe reacted to your message in Channel 1"
        
#  Testing message_unreact_v1()
#
#######################################
def test_unreact_once():
    """Test that one user successfully unreacts a message
    """
    state.set_state(s3)

    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # User reacts the message with react_id 1
    message.message_react_v1(user_token, msg_id, 1)

    # User unreacts the message
    message.message_unreact_v1(user_token, msg_id, 1)

    # check the reacts is successfully removed. Since there is no reacts for the messsage, 
    # the react_dict should be an empty list.
    msg = channel.channel_messages_v1(user_token, channel_id, 0)
    react_dict = msg["messages"][0]["reacts"]
    assert react_dict == []

def test_unreact_one_of_two():
    """Test that several users successfully react a message
    """
    state.set_state(s3)

    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # User 1,2 reacts the message with react_id 1
    message.message_react_v1(user_token, msg_id, 1)
    message.message_react_v1(user2_token, msg_id, 1)

    # User unreacts the message
    message.message_unreact_v1(user_token, msg_id, 1)

    # Check the reacts is successfully removed. The only reacted user should be user2.
    msg = channel.channel_messages_v1(user_token, channel_id, 0)
    react_dict = msg["messages"][0]["reacts"]
    assert react_dict[0]["react_id"] == 1
    assert user2_id in react_dict[0]["u_ids"]

def test_unreact_invalid_message():
    """Test that a user unreacts a message with invalid message id
    """
    state.set_state(s3)
    with pytest.raises(error.InputError):
        message.message_unreact_v1(user_token, identifier.get_new_identifier(), 1)

def test_unreact_invalid_react_id():
    """Test that a user unreacts a message with invalid message id
    """
    state.set_state(s3)
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]
    with pytest.raises(error.InputError):
        message.message_unreact_v1(user_token, msg_id, identifier.get_new_identifier())

def test_unreact_not_reacted():
    """Test that users unreacts a message which is not reacted by theirself
    """
    state.set_state(s3)
    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # Raise InputError when user unreacts the not reacted message
    with pytest.raises(error.InputError):
        message.message_unreact_v1(user_token, msg_id, 1)

def test_unreact_user_not_in_channel():
    """Test that a user unreacts a message with invalid message id
    """
    state.set_state(s3)

    # Create user3
    user3 = auth.auth_register_v1("11.else@example.com", "Password1", "Woo", "Hoo")
    user3_token = user3["token"]

    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    with pytest.raises(error.AccessError):
        message.message_unreact_v1(user3_token, msg_id, 1)

def test_unreact_notification():
    """Test that a user received notification when their message is reacted is removed.
    """
    state.set_state(s3)
    
    msg_id = message.message_send_v1(user_token, channel_id, "Hello")["message_id"]
    message.message_react_v1(user2_token, msg_id, 1)
    message.message_unreact_v1(user2_token, msg_id, 1)
    ntfns = notification.notification_get_v1(user_token)["notifications"]
    
    assert len(ntfns) == 0

def test_remove_msg_react_notification():
    """Test that when the reacted message is removed, user's notification about react is removed properly.
    """
    state.set_state(s3)
    
    msg_id = message.message_send_v1(user_token, channel_id, "Hello")["message_id"]
    message.message_react_v1(user2_token, msg_id, 1)
    message.message_remove_v1(user_token, msg_id)
    ntfns = notification.notification_get_v1(user_token)["notifications"]
    
    assert len(ntfns) == 0

#  Testing message_pin_v1()
#
#######################################
def test_pin_success():
    """Test pinning message successfullly
    """
    state.set_state(s3)
    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # User pins the message
    message.message_pin_v1(user_token, msg_id)
    msg = channel.channel_messages_v1(user_token, channel_id, 0)
    assert msg["messages"][0]["is_pinned"] == True

def test_pin_not_owner():
    """Test user pins message while they are not the channel's owner
    """
    state.set_state(s3)
    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # Raise AccessError since user2 is not owner of the channel
    with pytest.raises(error.AccessError):
        message.message_pin_v1(user2_token, msg_id)


def test_pin_not_member():
    """Test user pins message while they are not in the channel
    """
    state.set_state(s3)
    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # Create user3 who is not in the channel
    user3 = auth.auth_register_v1("1.else@example.com", "Password1", "Im", "Sorry")
    user3_token = user3["token"]
    # Raise AccessError when user3 tries to pin the message
    with pytest.raises(error.AccessError):
        message.message_pin_v1(user3_token, msg_id)

def test_pin_invalid_message_id():
    """Test pinning an invalid message
    """
    state.set_state(s3)
    with pytest.raises(error.InputError):
        message.message_pin_v1(user_token, identifier.get_new_identifier())

def test_pin_already_pinned():
    """Test pinning an already pinned message
    """
    state.set_state(s3)
    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # User pins the message
    message.message_pin_v1(user_token, msg_id)
    # Raise InputError when User pins the message again
    with pytest.raises(error.InputError):
        message.message_pin_v1(user_token, msg_id)

#  Testing message_unpin_v1()
#
#######################################
def test_unpin_success():
    """Test unpinning message successfullly
    """
    state.set_state(s3)
    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # User pins the message and unpins it
    message.message_pin_v1(user_token, msg_id)
    message.message_unpin_v1(user_token, msg_id)

    msg = channel.channel_messages_v1(user_token, channel_id, 0)
    assert msg["messages"][0]["is_pinned"] == False

def test_unpin_not_owner():
    """Test user unpins message while they are not the channel's owner
    """
    state.set_state(s3)
    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # Raise AccessError since user2 is not owner of the channel
    with pytest.raises(error.AccessError):
        message.message_unpin_v1(user2_token, msg_id)


def test_unpin_not_member():
    """Test user unpins message while they are not in the channel
    """
    state.set_state(s3)
    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # Create user3 who is not in the channel
    user3 = auth.auth_register_v1("1.else@example.com", "Password1", "Im", "Sorry")
    user3_token = user3["token"]

    # Raise AccessError when user3 tries to unpin the message
    with pytest.raises(error.AccessError):
        message.message_unpin_v1(user3_token, msg_id)

def test_unpin_invalid_message_id():
    """Test unpinning an invalid message
    """
    state.set_state(s3)
    with pytest.raises(error.InputError):
        message.message_unpin_v1(user_token, identifier.get_new_identifier())

def test_unpin_already_unpinned():
    """Test unpinning an already pinned message
    """
    state.set_state(s3)
    # User2 sends a message to channel
    msg_id = message.message_send_v1(user2_token, channel_id, "Hello world")["message_id"]

    # Raise InputError when User unpins the message that is unpinned
    with pytest.raises(error.InputError):
        message.message_unpin_v1(user_token, msg_id)
