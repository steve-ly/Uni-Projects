"""tests > tagging_test.py

This file contains tests for tagging users. It ensures that strings are
preserved correctly when sent with tags

Authors:
    Miguel Guthridge [z5312085@ad.unsw.edu.au]
"""
import pytest
from src import auth, channels, channel, message, state, user, notification,\
    admin, other
from src.error import AccessError, InputError
# Set up states
other.clear_v1()

# Register two users
userdat = auth.auth_register_v1("someone@example.com", "Password1", "First", "Last")
u_id = userdat["auth_user_id"]
u_token = userdat["token"]
userdat2 = auth.auth_register_v1("someoneelse@example.com", "Password1", "One", "Two")
u2_id = userdat2["auth_user_id"]
u2_token = userdat2["token"]

# Create channel and add both users to it
c_id = channels.channels_create_v1(u_token, "Channel 1", True)["channel_id"]
channel.channel_join_v1(u2_token, c_id)

# Get a copy of the state
s = state.get_state()

#
# Test tagging mechanics (ensure messages remain valid)
#

def test_tag_start():
    """Test that a tag will remain correct if it is at the start of the message
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "@onetwo Hi!")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == "@onetwo Hi!"

def test_tag_end():
    """Test that a tag will remain correct if it is at the end of the message
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "How are you @onetwo")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == "How are you @onetwo"

def test_tag_middle():
    """Test that a tag will remain correct if a user is tagged and the message
    is displayed
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "Hello @onetwo how are you?")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == "Hello @onetwo how are you?"

def test_tag_only():
    """Test that a tag will work if it is the only thing in the message
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "@onetwo")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == "@onetwo"

def test_tag_mid_word():
    """Test that a user can be tagged when the @ symbol is not the start of a
    word (ie it doesnt have a space before it)
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "hello@onetwo how are you")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == "hello@onetwo how are you"

def test_tag_line_break():
    """Test that a user can be tagged, even if the character at the end of their
    handle is a line_break or a tab
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "Hello @onetwo\nI'm @firstlast\t How are you?")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == "Hello @onetwo\nI'm @firstlast\t How are you?"

def test_tag_self():
    """Test that it is possible to tag one's self in a message, and that it will
    display correctly
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "@firstlast is having a conversation with myself")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == "@firstlast is having a conversation with myself"

def test_tag_multiple():
    """Test that it is possible to tag multiple users in the one message
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "Now I am tagging @onetwo and @firstlast")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == "Now I am tagging @onetwo and @firstlast"

def test_tag_handle_change():
    """Test that a tag displays the updated handle if a user changes their handle
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "Will the tag update? @onetwo")
    
    user.user_profile_sethandle_v1(u2_token, "newhandle")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == "Will the tag update? @newhandle"


def test_tag_removed_user():
    ###Tests that user cannot be tagged after successful removal
    
    state.set_state(s)

    removed_user = auth.auth_register_v1('validemail2@gmail.com', '123abc', 'New', 'Times')
    
    channel.channel_invite_v1(u_token, c_id, removed_user["auth_user_id"] )
    message.message_send_v1(u_token, c_id, "@newtimes")
    admin.admin_remove_user(u_token, removed_user["auth_user_id"])
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    assert msgs_in_ch[0]["message"] == "@removed_user"

def test_tag_at_removed_user():
    ###Tests that tagging @removed_user doesn't break things
    
    state.set_state(s)
    message.message_send_v1(u_token, c_id, "@removed_user")
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    assert msgs_in_ch[0]["message"] == "@removed_user"

def test_tag_fake():
    """Test that it is possible to use the @ symbol at the start of a word
    without tagging someone if the handle is invalid
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "@threefour isn't a person that exists")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == "@threefour isn't a person that exists"

def test_tag_user_id():
    """Test that no errors occur when the text after an @ symbol is a user's ID.
    Ensure that this doesn't convert to a tag
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, f"Random numbers @{u_id}")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == f"Random numbers @{u_id}"

def test_tag_user_double_at_no_tag():
    """Test that no errors occur when using two @ symbols next to each other
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "@@hello friends")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == "@@hello friends"

def test_tag_user_double_at_tag():
    """Test that no errors occur when preceding a tag with 2 @ symbols instead
    of one
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "@@onetwo test")
    
    msgs_in_ch = channel.channel_messages_v1(u_token, c_id, 0)["messages"]
    
    assert msgs_in_ch[0]["message"] == "@@onetwo test"

#
# Test notifications for tagging
#

def test_tag_notification():
    """Test that a user receives a notification when they are tagged in a message
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "Hello @onetwo")
    
    ntfns = notification.notification_get_v1(u2_token)["notifications"]
    
    assert ntfns[0]["channel_id"] == c_id
    assert ntfns[0]["dm_id"] == -1
    assert ntfns[0]["notification_message"]\
        ==  "@firstlast tagged you in Channel 1: Hello @onetwo"

def test_tag_self_notification():
    """Test that a user doesn't receive a notification if they tag themselves in
    a message
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "Hello @firstlast")
    
    assert len(notification.notification_get_v1(u_token)["notifications"]) == 0

def test_tag_multiple_notification():
    """Test that a user only receives one notification if they are tagged in a
    message twice
    """
    state.set_state(s)
    
    message.message_send_v1(u_token, c_id, "Hello @onetwo @onetwo @onetwo")
    
    assert len(notification.notification_get_v1(u2_token)["notifications"]) == 1

def test_tag_remove_notification():
    """Test that the notification is retracted if a user removes a message where
    a user is tagged
    """
    state.set_state(s)
    
    m_id = message.message_send_v1(u_token, c_id, "Hello @onetwo")["message_id"]
    
    message.message_remove_v1(u_token, m_id)
    
    assert len(notification.notification_get_v1(u2_token)["notifications"]) == 0

def test_tag_edit_notification_retract():
    """Test that when a message is edited, the tagged users are updated.
        - Users that are untagged have their notification retracted
    """
    state.set_state(s)
    
    m_id = message.message_send_v1(u_token, c_id, "Hello @onetwo")["message_id"]
    
    message.message_edit_v1(u_token, m_id, "Hello I'm no-longer tagging you")
    
    assert len(notification.notification_get_v1(u2_token)["notifications"]) == 0

def test_tag_edit_notification_add():
    """Test that when a message is edited, the tagged users are updated.
        - Users that are newly tagged get a new notification
    """
    state.set_state(s)
    
    m_id = message.message_send_v1(u_token, c_id, "Hello I'm not tagging anyone")["message_id"]
    
    message.message_edit_v1(u_token, m_id, "Hello now I'm tagging @onetwo")
    
    assert len(notification.notification_get_v1(u2_token)["notifications"]) == 1

def test_tag_edit_notification_add_self():
    """Test that when a message is edited and the user is now tagging themselves
    they don't get any new notifications
    """
    state.set_state(s)
    
    m_id = message.message_send_v1(u_token, c_id, "Hello I'm not tagging anyone")["message_id"]
    
    message.message_edit_v1(u_token, m_id, "Hello now I'm tagging myself @firstlast")
    
    assert len(notification.notification_get_v1(u_token)["notifications"]) == 0

def test_tag_edit_notification_retain():
    """Test that when a message is edited, the tagged users are updated.
        - Users whose tags remain don't get a new notification and don't lose
          their old one
        - Message preview in the notification is updated to match the new text
    """
    state.set_state(s)
    
    m_id = message.message_send_v1(u_token, c_id, "Hello @onetwo")["message_id"]
    
    ntfns = notification.notification_get_v1(u2_token)["notifications"]
    
    assert ntfns[0]["channel_id"] == c_id
    assert ntfns[0]["dm_id"] == -1
    assert ntfns[0]["notification_message"]\
        ==  "@firstlast tagged you in Channel 1: Hello @onetwo"
        
    # Create another notification for user 2. This will ensure that the
    # notification is edited in-place, rather than being replaced
    c2_id = channels.channels_create_v1(u_token, "Channel 2", True)["channel_id"]
    channel.channel_invite_v1(u_token, c2_id, u2_id)
    
    message.message_edit_v1(u_token, m_id, "@onetwo hello")
    
    ntfns = notification.notification_get_v1(u2_token)["notifications"]
    
    assert len(ntfns) == 2
    assert ntfns[1]["channel_id"] == c_id
    assert ntfns[1]["dm_id"] == -1
    assert ntfns[1]["notification_message"]\
        ==  "@firstlast tagged you in Channel 1: @onetwo hello"
