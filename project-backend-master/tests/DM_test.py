import pytest
import datetime, time

from src.error import InputError, AccessError
from src import state, auth, user, identifier, other, dm,\
    notification

# Reset the state
other.clear_v1()

# Set users and DM_id
# One user not in DM and one or more users have been in DM
user_1 = auth.auth_register_v1("test@email.com", "password", "John", "Smith")
user_id = user_1["auth_user_id"]
user_token = user_1["token"]

user_2 = auth.auth_register_v1("test2@email.com", "password2", "Bruce", "Lee")
user2_id = user_2["auth_user_id"]
user2_token = user_2["token"]

u_ids = [user2_id]
dm_id = dm.dm_create_v1(user_token, u_ids)["dm_id"]

user_3 = auth.auth_register_v1("test3@email.com", "password3", "Maco", "Bee")
user3_id = user_3["auth_user_id"]
user3_token = user_3["token"]

s = state.get_state()


# Length = 1030 characters
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


############################################
# Tests for dm_details_v1()
#
############################################

def test_dm_detail_invalid_DM_id():
    state.set_state(s)
    
    # Assume get a invalid dm id
    invalid_dm_id = identifier.get_new_identifier()
    
    # Return InputError
    with pytest.raises(InputError):
        dm.dm_details_v1(user_token, invalid_dm_id)


def test_auth_user_invalid_dm_member():
    state.set_state(s)

    # Return AccessError
    with pytest.raises(AccessError):
        dm.dm_details_v1(user3_token, dm_id)

def test_dm_details_v1_success():
    state.set_state(s)
    # Test one of auth user in DM
    dm_details = dm.dm_details_v1(user_token, dm_id)
    
    # Remove references to profile pic as these are difficult to black-box
    for mem in dm_details["members"]: mem.pop("profile_img_url")
    
    # Check both members are listed
    assert dm_details["name"] == "brucelee, johnsmith"
    assert {'email': 'test2@email.com', 
            'handle_str': 'brucelee', 
            'name_first': 'Bruce', 
            'name_last': 'Lee', 
            'u_id': user2_id} in dm_details["members"]
    assert {'email': 'test@email.com', 
            'handle_str': 'johnsmith', 
            'name_first': 'John', 
            'name_last': 'Smith', 
            'u_id': user_id} in dm_details["members"]

    
############################################
# Tests for dm_list_v1()
#
############################################

def test_dm_list_success():
    state.set_state(s)
    
    # Ensure the DM list for auth user1 is correct
    dm_lst = dm.dm_list_v1(user_token)
    dms_dict = {"dm_id": dm_id, "name": "brucelee, johnsmith"}
    assert dms_dict in dm_lst["dms"]


def test_dm_list_non_member():
    """Ensure that users aren't shown DMs they aren't a member of
    """
    state.set_state(s)
    dm_lst = dm.dm_list_v1(user3_token)["dms"]
    assert len(dm_lst) == 0

############################################    
# Tests for dm_create_v1()
#
############################################

def test_create_invalid_id():
    state.set_state(s)
    
    # Take an invalid user_id
    invalid_user_id = identifier.get_new_identifier()

    with pytest.raises(InputError):
        dm.dm_create_v1(user_token, [user_id, invalid_user_id])
   

def test_dm_create_success():
    state.set_state(s)
    
    # The first auth user creates the DM structure
    dm_info = dm.dm_create_v1(user_token, u_ids)
    
    assert dm_info["dm_name"] == "brucelee, johnsmith"
    

############################################
# Tests for dm_remove_v1()
#
############################################

def test_remove_invalid_dm():
    state.set_state(s)
    
    # Take an invalid user_id
    invalid_dm_id = identifier.get_new_identifier()

    with pytest.raises(InputError):
        dm.dm_remove_v1(user_token, invalid_dm_id)
   
         
def test_remove_invalid_creator():
    state.set_state(s)
    
    # The user3 is not the member(creator) in DM
    with pytest.raises(AccessError):
        dm.dm_remove_v1(user3_token, dm_id)

def test_remove_success():
    state.set_state(s)  
    
    # Remove DM
    dm.dm_remove_v1(user_token, dm_id)
    
    # Shouldn't be able to send messages
    with pytest.raises(InputError):
        dm.dm_message_send_v1(user_token, dm_id, "Oops")
    
    # Shouldn't be in list of DMs
    assert len(dm.dm_list_v1(user_token)["dms"]) == 0

def test_remove_non_owner():
    state.set_state(s)  
    
    # Remove DM
    with pytest.raises(AccessError):
        dm.dm_remove_v1(user2_token, dm_id)

############################################
# Tests for dm_invite_v1()
#
############################################

def test_invalid_dm():
    state.set_state(s)
    
    # Take an invalid dm_id
    invalid_dm_id = identifier.get_new_identifier()

    with pytest.raises(InputError):
        dm.dm_invite_v1(user_token, invalid_dm_id, user3_id)
   

def test_invalid_u_id(): 
    state.set_state(s)
    
    # Take an invalid dm_id
    invalid_u_id = identifier.get_new_identifier()

    with pytest.raises(InputError):
        dm.dm_invite_v1(user_token, dm_id, invalid_u_id)
     
     
def test_invite_unauthorised_user():
    state.set_state(s)
    
    # Return AccessError
    with pytest.raises(AccessError):
        dm.dm_invite_v1(user3_token, dm_id, user3_id)  
         
         
def test_dm_invite_success():
    state.set_state(s)
    
    # User invites the user3 to start DM
    dm.dm_invite_v1(user_token, dm_id, user3_id)
    dm_info = dm.dm_details_v1(user_token, dm_id)
    user3_data = user.user_profile_v1(user_token, user3_id)["user"]
         
    assert user3_data in dm_info["members"]

def test_dm_invite_duplicate():
    state.set_state(s)
    
    # Invite user 2 again
    dm.dm_invite_v1(user_token, dm_id, user2_id)
    dm_info = dm.dm_details_v1(user_token, dm_id)
    assert len(dm_info["members"]) == 2

def test_dm_invite_notifications():
    state.set_state(s)
    dm.dm_create_v1(user_token, [user2_id, user3_id])
    from pprint import pprint
    pprint(notification.notification_get_v1(user_token))
    pprint(notification.notification_get_v1(user2_token))
    pprint(notification.notification_get_v1(user3_token))
    assert len(notification.notification_get_v1(user_token)["notifications"]) == 0
    assert notification.notification_get_v1(user2_token)["notifications"][0]["notification_message"] ==\
        "@johnsmith added you to brucelee, johnsmith, macobee"
    assert notification.notification_get_v1(user3_token)["notifications"][0]["notification_message"] ==\
        "@johnsmith added you to brucelee, johnsmith, macobee"

############################################   
# Tests for dm_leave_v1()
#
############################################

def test_leave_invalid_dm():
    state.set_state(s)
    
    # Take an invalid dm_id
    invalid_dm_id = identifier.get_new_identifier()   
         
    # Return InputError
    with pytest.raises(InputError):
        dm.dm_leave_v1(user_token, invalid_dm_id)  
         
         
def test_non_member_leave():
    state.set_state(s)
    
    # Return AccessError
    with pytest.raises(AccessError):
        dm.dm_leave_v1(user3_token, dm_id)       
      
      
def test_dm_leave_success():
    state.set_state(s)
    
    # Leave dm with user 
    dm.dm_leave_v1(user2_token, dm_id)
    
    assert len(dm.dm_details_v1(user_token, dm_id)["members"]) == 1


############################################
# Test for dm_messages_v1()
#
############################################

def test_invalid_dm_id_for_message():
    state.set_state(s)
    dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")

    
    # Take an invalid dm_id
    invalid_dm_id = identifier.get_new_identifier()   
         
    # Return InputError
    with pytest.raises(InputError):
        dm.dm_messages_v1(user_token, invalid_dm_id, 0) 
         
         
def test_messages_invalid_start():
    state.set_state(s)
    dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")

    
    # Raise InputError 
    with pytest.raises(InputError):
        dm.dm_messages_v1(user_token, dm_id, 5)
     
         
def test_messages_user_not_a_dm_member():
    state.set_state(s)
    dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")


    # Return AccessError
    with pytest.raises(AccessError):
        dm.dm_messages_v1(user3_token, dm_id, 0)

      
def test_messages_for_user():
    state.set_state(s)
    dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")["message_id"]

    dm_msg = dm.dm_messages_v1(user_token, dm_id, 0)

    # Check the messages in the dm.
    assert len(dm_msg["messages"]) == 1
    assert dm_msg["messages"][0]["message"] == "Danny is Cool"
    assert dm_msg["start"] == 0
    assert dm_msg["end"] == -1

    
def test_messages_over_50_msgs():
    state.set_state(s)
    dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")
    
    for _ in range(60):
        dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")

    dm.dm_message_send_v1(user_token, dm_id, "recent msg")["message_id"]

    dm_msg = dm.dm_messages_v1(user_token, dm_id, 0)

    # Check the messages in the dm.
    assert len(dm_msg["messages"]) == 50
    assert dm_msg["messages"][0]["message"] == "recent msg"
    assert dm_msg["start"] == 0
    assert dm_msg["end"] == 50
    
def test_messages_over_50_msgs_non_zero_index():
    state.set_state(s)
    dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")

    for _ in range(60):
        dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")

    dm.dm_message_send_v1(user_token, dm_id, "recent msg")["message_id"]
    
    for _ in range(10):
        dm.dm_message_send_v1(user_token, dm_id, "different msgs")

    dm_msg = dm.dm_messages_v1(user_token, dm_id, 10)

    # Check the messages in the dm.
    assert len(dm_msg["messages"]) == 50
    assert dm_msg["messages"][0]["message"] == "recent msg"
    assert dm_msg["start"] == 10
    assert dm_msg["end"] == 60
    
def test_messages_end_value_ceiling():
    state.set_state(s)
    
    for _ in range(10):
        dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")

    dm.dm_message_send_v1(user_token, dm_id, "recent msg")["message_id"]
    
    for _ in range(10):
        dm.dm_message_send_v1(user_token, dm_id, "different msgs")
    dm_msg = dm.dm_messages_v1(user_token, dm_id, 10)
    print(dm_msg)
    # Check the messages in the dm.
    assert len(dm_msg["messages"]) == 11
    assert dm_msg["messages"][0]["message"] == "recent msg"
    assert dm_msg["start"] == 10
    assert dm_msg["end"] == -1

def test_messages_over_50_msgs_delayed_msg():
    state.set_state(s)
    dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")

    for _ in range(60):
        dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")

    delay = datetime.datetime.now().timestamp() + 1

    # Send a delayed msg
    dm.dm_message_send_later_v1(user_token, dm_id, "recent msg", delay)

    dm_msg = dm.dm_messages_v1(user_token, dm_id, 0)

    # Check the messages in the dm. Make sure delayed msg isnt there and
    # indexes are correct
    assert len(dm_msg["messages"]) == 50
    assert dm_msg["messages"][0]["message"] == "Danny is Cool"
    assert dm_msg["start"] == 0
    assert dm_msg["end"] == 50

def test_messages_over_50_msgs_delayed_msg_sent():
    state.set_state(s)
    dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")

    for _ in range(60):
        dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")

    delay = datetime.datetime.now().timestamp() + 1

    # send a delayed msg that has already been sent
    dm.dm_message_send_later_v1(user_token, dm_id, "recent msg", delay)

    time.sleep(1)

    dm_msg = dm.dm_messages_v1(user_token, dm_id, 0)

    # Check the messages in the dm. Make sure sent delayed msg was actually
    # sent and indexes are correct
    assert len(dm_msg["messages"]) == 50
    assert dm_msg["messages"][0]["message"] == "recent msg"
    assert dm_msg["start"] == 0
    assert dm_msg["end"] == 50

############################################
# Test for dm_message_send_v1()
#
############################################

def test_send_message():
    state.set_state(s)
    dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")["message_id"]
    
    dm_msg = dm.dm_messages_v1(user_token, dm_id, 0)
    
    # Check the messages in the dm.
    assert len(dm_msg["messages"]) == 1
    assert dm_msg["messages"][0]["message"] == 'Danny is Cool'
    assert dm_msg["start"] == 0
    assert dm_msg["end"] == -1
    
def test_msg_too_long():
    state.set_state(s)
    # Input error: message too long
    with pytest.raises(InputError):
        dm.dm_message_send_v1(user_token, dm_id, a_long_string)
    

def test_send_msg_inaccessible_DM():
    state.set_state(s)
    # Create new channel
    dm_id2 = dm.dm_create_v1(user3_token, [user2_id])["dm_id"]

    # Access error: not a member of the channel
    with pytest.raises(AccessError):
        dm.dm_message_send_v1(user_token, dm_id2, "Danny is Cool")

def test_send_msg_nonexistent_DM():
    state.set_state(s)
    fake_dm_id = identifier.get_new_identifier()
    
    # Access error: channel doesn't exist
    with pytest.raises(InputError):
        dm.dm_message_send_v1(user_token, fake_dm_id, "Danny is Cool")

def test_send_msg_nonexistent_user():
    state.set_state(s)
    fake_user_id = identifier.get_new_identifier()
    
    # Access error: user doesn't exist
    with pytest.raises(AccessError):
        dm.dm_message_send_v1(fake_user_id, dm_id, "Danny is Cool")

def test_send_msg_empty():
    state.set_state(s)
    # See assumptions.md for note on this
    # Input error: empty message
    with pytest.raises(InputError):
        dm.dm_message_send_v1(user_token, dm_id, "")

def test_timestamp():
    # Locally import time, since we don't need it outside of this function
    import time
    state.set_state(s)

    # This assumes that time doesn't advance by more than a second between the 
    # operations
    msg_time = int(time.time())
    dm.dm_message_send_v1(user_token, dm_id, "Danny is Cool")
    
    # Ensure the times are equal
    assert dm.dm_messages_v1(user_token, dm_id, 0)\
        ["messages"][0]["time_created"] == msg_time

def test_message_send_tag():
    state.set_state(s)
    dm.dm_message_send_v1(user_token, dm_id, "@brucelee")["message_id"]

    # Check notifs got updated
    notif = notification.notification_get_v1(user2_token)["notifications"]
    assert '@johnsmith tagged you in brucelee, johnsmith: @brucelee' == notif[0]["notification_message"]

def test_message_send_self_tag():
    state.set_state(s)
    dm.dm_message_send_v1(user_token, dm_id, "@johnsmith")["message_id"]

    # Check notifs didn't get updated
    notif = notification.notification_get_v1(user_token)["notifications"]
    assert len(notif) == 0
