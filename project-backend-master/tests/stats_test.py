from src import state, auth, channels, channel, message, dm, stats, other

# Reset the state
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
u_ids = [user_id2]

s = state.get_state()

############################################
# Testing get_dream_stats(user1_token)
#
############################################

def test_dream_no_stats():
    state.set_state(s)

    dream_stats = stats.dreams_stats_v1(user1_token)["dreams_stats"]

    assert len(dream_stats["channels_exist"]) == 0
    assert len(dream_stats["dms_exist"]) == 0
    assert len(dream_stats["messages_exist"]) == 0
    assert dream_stats["utilization_rate"] == 0

def test_dream_low_stats():
    state.set_state(s)

    ch_id1 = channels.channels_create_v1(user1_token, "Channel 1", True)["channel_id"]
    dm.dm_create_v1(user1_token, u_ids)["dm_id"]
    message.message_send_v1(user1_token, ch_id1, "Danny is cool")["message_id"]

    dream_stats = stats.dreams_stats_v1(user1_token)["dreams_stats"]

    assert len(dream_stats["channels_exist"]) == 1
    assert len(dream_stats["dms_exist"]) == 1
    assert len(dream_stats["messages_exist"]) == 1
    assert dream_stats["channels_exist"][0]["num_channels_exist"] == 1
    assert dream_stats["dms_exist"][0]["num_dms_exist"] == 1
    assert dream_stats["messages_exist"][0]["num_messages_exist"] == 1
    assert dream_stats["utilization_rate"] == 0.6666666666666666

def test_dream_high_stats():
    other.clear_v1()

    for i in range(50):
        email = "test" + str(i) + "@email.com"
        user_1 = auth.auth_register_v1(email, "password", "John", "Smith")
        user1_token = user_1["token"]
        ch_id = channels.channels_create_v1(user1_token, "Channel 1", True)["channel_id"]
        message.message_send_v1(user1_token, ch_id, "Danny is cool")["message_id"]
        dm.dm_create_v1(user1_token, [])["dm_id"]

    dream_stats = stats.dreams_stats_v1(user1_token)["dreams_stats"]

    assert dream_stats["channels_exist"][0]["num_channels_exist"] == 50
    assert dream_stats["dms_exist"][0]["num_dms_exist"] == 50
    assert dream_stats["messages_exist"][0]["num_messages_exist"] == 50
    assert dream_stats["utilization_rate"] == 1

def test_dream_utilization_rate():
    state.set_state(s)

    ch_id1 = channels.channels_create_v1(user1_token, "Channel 1", True)["channel_id"]
    dm.dm_create_v1(user1_token, u_ids)["dm_id"]
    message.message_send_v1(user1_token, ch_id1, "Danny is cool")["message_id"]
    auth.auth_register_v1("test4@email.com", "password", "Nic", "Rodwell")
    auth.auth_register_v1("test5@email.com", "password", "Harrison", "Chong")
    auth.auth_register_v1("test6@email.com", "password", "Liang", "Pan")
    
    dream_stats = stats.dreams_stats_v1(user1_token)["dreams_stats"]

    assert len(dream_stats["channels_exist"]) == 1
    assert len(dream_stats["dms_exist"]) == 1
    assert len(dream_stats["messages_exist"]) == 1
    assert dream_stats["utilization_rate"] == 0.3333333333333333

def test_dream_remove_stats():
    state.set_state(s)

    ch_id1 = channels.channels_create_v1(user1_token, "Channel 1", True)["channel_id"]
    dm_id1 = dm.dm_create_v1(user1_token, u_ids)["dm_id"]
    m_id1 = message.message_send_v1(user1_token, ch_id1, "Danny is cool")["message_id"]

    dream_stats = stats.dreams_stats_v1(user1_token)["dreams_stats"]

    assert dream_stats["channels_exist"][0]["num_channels_exist"] == 1
    assert dream_stats["dms_exist"][0]["num_dms_exist"] == 1
    assert dream_stats["messages_exist"][0]["num_messages_exist"] == 1
    assert dream_stats["utilization_rate"] == 0.6666666666666666

    channel.channel_leave_v1(user1_token, ch_id1)
    dm.dm_remove_v1(user1_token, dm_id1)
    message.message_remove_v1(user1_token, m_id1)

    dream_stats = stats.dreams_stats_v1(user1_token)["dreams_stats"]

    assert dream_stats["channels_exist"][0]["num_channels_exist"] == 1
    assert dream_stats["dms_exist"][0]["num_dms_exist"] == 0
    assert dream_stats["messages_exist"][0]["num_messages_exist"] == 0
    assert dream_stats["utilization_rate"] == 0.0

# Test user stats

def test_user_stats_none():
    state.set_state(s)
    
    usr_stats = stats.user_stats_v1(user1_token)["user_stats"]
    
    assert len(usr_stats["channels_joined"]) == 0
    assert len(usr_stats["dms_joined"]) == 0
    assert len(usr_stats["messages_sent"]) == 0
    assert usr_stats["involvement_rate"] == 0

def test_user_low_stats():
    """Check a user with some stats
    """
    state.set_state(s)

    ch_id = channels.channels_create_v1(user1_token, "Channel 1", True)["channel_id"]
    dm.dm_create_v1(user1_token, [])
    message.message_send_v1(user1_token, ch_id, "Hello!")

    user_stats = stats.user_stats_v1(user1_token)["user_stats"]

    assert user_stats["channels_joined"][0]["num_channels_joined"] == 1
    assert user_stats["dms_joined"][0]["num_dms_joined"] == 1
    assert user_stats["messages_sent"][0]["num_messages_sent"] == 1
    assert user_stats["involvement_rate"] == 1

def test_user_high_stats():
    """Check a user with lots of involvement
    """
    state.set_state(s)

    for _ in range(50):
        ch_id = channels.channels_create_v1(user1_token, "Channel 1", True)["channel_id"]
   
    for _ in range(50):
        dm.dm_create_v1(user1_token, [])

    for _ in range(50):
        message.message_send_v1(user1_token, ch_id, "Hello Channel 1")
    

    user_stats = stats.user_stats_v1(user1_token)["user_stats"]
    print(len(user_stats["channels_joined"]))

    assert user_stats["channels_joined"][0]["num_channels_joined"] == 50
    assert user_stats["dms_joined"][0]["num_dms_joined"] == 50
    assert user_stats["messages_sent"][0]["num_messages_sent"] == 50
    assert user_stats["involvement_rate"] == 1

def test_user_involvement_rate():
    """Check a users involvment rate
    """
    state.set_state(s)
    user2_dat = auth.auth_register_v1("test9@email.com", "password", "Jane", "Doe")
    user2_token = user2_dat["token"]

    ch_id1 = channels.channels_create_v1(user1_token, "Channel 1", True)["channel_id"]
    channels.channels_create_v1(user2_token, "Channel 2", True)["channel_id"]

    dm.dm_create_v1(user1_token, [])

    message.message_send_v1(user1_token, ch_id1, "Hello Channel 1")
    

    user_stats = stats.user_stats_v1(user1_token)["user_stats"]

    assert user_stats["channels_joined"][0]["num_channels_joined"] == 1
    assert user_stats["dms_joined"][0]["num_dms_joined"] == 1
    assert user_stats["messages_sent"][0]["num_messages_sent"] == 1
    assert user_stats["involvement_rate"] == 0.75

def test_user_remove_stats():
    state.set_state(s)

    user2_dat = auth.auth_register_v1("test9@email.com", "password", "Jane", "Doe")
    user2_id = user2_dat["auth_user_id"]

    u_ids = [user2_id]

    ch_id1 = channels.channels_create_v1(user1_token, "Channel 1", True)["channel_id"]
    dm_id1 = dm.dm_create_v1(user1_token, u_ids)["dm_id"]
    m_id1 = message.message_send_v1(user1_token, ch_id1, "Danny is cool")["message_id"]

    user_stats = stats.user_stats_v1(user1_token)["user_stats"]

    assert user_stats["channels_joined"][0]["num_channels_joined"] == 1
    assert user_stats["dms_joined"][0]["num_dms_joined"] == 1
    assert user_stats["messages_sent"][0]["num_messages_sent"] == 1
    assert user_stats["involvement_rate"] == 1

    channel.channel_leave_v1(user1_token, ch_id1)
    dm.dm_leave_v1(user1_token, dm_id1)
    message.message_remove_v1(user1_token, m_id1)

    user_stats = stats.user_stats_v1(user1_token)["user_stats"]

    assert user_stats["channels_joined"][0]["num_channels_joined"] == 0
    assert user_stats["dms_joined"][0]["num_dms_joined"] == 0
    assert user_stats["messages_sent"][0]["num_messages_sent"] == 0
    assert user_stats["involvement_rate"] == 0
