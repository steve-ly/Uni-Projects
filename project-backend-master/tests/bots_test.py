
from src import auth, dm, other, message, channels, channel

def test_activate_bot_nonexistant():
    """Test whether we get an error response when we try to activate a bot
    that doesn't exist
    """
    other.clear_v1()
    usr = auth.auth_register_v1("someone@example.com", "123456", "Robin", "Banks")
    ch = channels.channels_create_v1(usr["token"], "Ch", True)
    message.message_send_v1(usr["token"], ch["channel_id"], "/activate test")
    msgs = channel.channel_messages_v1(usr["token"], ch["channel_id"], 0)["messages"]
    assert msgs[0]["message"] == "Error: bot with name 'test' not found"

def test_activate_bot_non_admin():
    other.clear_v1()
    usr = auth.auth_register_v1("someone@example.com", "123456", "Robin", "Banks")
    ch = channels.channels_create_v1(usr["token"], "Channel 1", True)
    new_u = auth.auth_register_v1("someone_else@example.com", "123456", "Joe", "Mama")
    channel.channel_join_v1(new_u["token"], ch["channel_id"])
    message.message_send_v1(new_u["token"], ch["channel_id"], "/activate Welcome")
    
    msgs = channel.channel_messages_v1(usr["token"], ch["channel_id"], 0)["messages"]
    assert msgs[0]["message"] == "Error: user must be an admin to activate a bot"

def test_welcome_bot():
    """Test whether (when activated), the welcome bot will welcome you
    """
    other.clear_v1()
    usr = auth.auth_register_v1("someone@example.com", "123456", "Robin", "Banks")
    ch = channels.channels_create_v1(usr["token"], "Channel 1", True)
    message.message_send_v1(usr["token"], ch["channel_id"], "/activate Welcome")

    # Register a new user
    new_u = auth.auth_register_v1("someone_else@example.com", "123456", "Joe", "Mama")
    # Get their DMs
    dms = dm.dm_list_v1(new_u["token"])["dms"]
    
    # Make sure we were welcomed! They will have a new DM
    assert len(dms) == 1

def test_welcome_bot_customise_help_msg():
    """Test the customisation features of the welcome bot
    """
    other.clear_v1()
    usr = auth.auth_register_v1("someone@example.com", "123456", "Robin", "Banks")
    ch = channels.channels_create_v1(usr["token"], "Ch", True)
    message.message_send_v1(usr["token"], ch["channel_id"], "/activate Welcome")
    
    message.message_send_v1(usr["token"], ch["channel_id"], "/welcome")
    msgs = channel.channel_messages_v1(usr["token"], ch["channel_id"], 0)["messages"]
    assert msgs[0]["message"] == "To customise the welcome message, use the command `/welcome customise [new message]`\n"\
                                    "Include '{name}' inside the new message to use the new user's name."
        
def test_welcome_bot_customise_non_admin():
    """Test the customisation features of the welcome bot
    """
    other.clear_v1()
    usr = auth.auth_register_v1("someone@example.com", "123456", "Robin", "Banks")
    ch = channels.channels_create_v1(usr["token"], "Ch", True)
    new_u = auth.auth_register_v1("someone_else@example.com", "123456", "Joe", "Mama")
    channel.channel_join_v1(new_u["token"], ch["channel_id"])
    message.message_send_v1(usr["token"], ch["channel_id"], "/activate Welcome")
    
    message.message_send_v1(new_u["token"], ch["channel_id"], "/welcome")
    msgs = channel.channel_messages_v1(usr["token"], ch["channel_id"], 0)["messages"]
    assert msgs[0]["message"] == "You must be an admin to customise the welcome message."
        
    