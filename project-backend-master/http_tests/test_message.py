from src import channel
import pytest

from . import call_wrappers as cw
from . import helpers
from src.error import InputError, AccessError
import datetime, time

def test_message_sent():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    msg = cw.message_send(user["token"],channel["channel_id"],"Yo")
    assert isinstance(msg["message_id"],int)
    assert cw.channel_messages(user["token"],channel["channel_id"],0)["messages"][0]["message"] == "Yo"

def test_message_too_long():
    script = """
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
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    with pytest.raises(InputError):
        cw.message_send(user["token"],channel["channel_id"],script)

def test_messsage_send_unauthorised_user():
    cw.clear()
    user = helpers.one_user()
    channel = helpers.one_channel(user["token"])
    user2 = cw.auth_register("notauthorised@gmail.com","Secured1","Jonah","Jamesons")
    with pytest.raises(AccessError):
        cw.message_send(user2["token"],channel["channel_id"],"Yo")


def test_message_send_invalid_token():
    cw.clear()
    user = helpers.one_user()
    channel = helpers.one_channel(user["token"])
    with pytest.raises(AccessError):
        cw.message_send(11111,channel["channel_id"],"Yo")


def test_message_edit():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    msg = cw.message_send(user["token"],channel["channel_id"],"Yo")
    cw.message_edit(user["token"],msg["message_id"],"Howdy")
    list_msg = cw.channel_messages(user["token"],channel["channel_id"],0)["messages"]
    assert list_msg[0]["message"] == "Howdy"
    

def test_message_edit_too_long():
    script = """
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
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    msg = cw.message_send(user["token"],channel["channel_id"],"Yo")
    with pytest.raises(InputError):
        cw.message_edit(user["token"],msg["message_id"],script)


def test_message_edit_removed():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    msg = cw.message_send(user["token"],channel["channel_id"],"Yo")
    cw.message_edit(user["token"],msg["message_id"],"")
    with pytest.raises(InputError):
        cw.message_edit(user["token"],msg["message_id"],"DEleted")


def test_message_edit_not_authorised():
    cw.clear()
    users,channel = helpers.two_users_one_channel()
    msg = cw.message_send(users[0]["token"],channel["channel_id"],"Yo")
    with pytest.raises(AccessError):
        cw.message_edit(users[1]["token"],msg["message_id"],"DEleted")


def test_message_edit_invalid_token():
    cw.clear()
    users,channel = helpers.two_users_one_channel()
    msg = cw.message_send(users[0]["token"],channel["channel_id"],"Yo")
    with pytest.raises(AccessError):
        cw.message_edit(121111,msg["message_id"],"DEleted")
        
def test_message_remove():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    msg = cw.message_send(user["token"],channel["channel_id"],"Yo")
    cw.message_remove(user["token"],msg["message_id"])
    assert len(cw.channel_messages(user["token"],channel["channel_id"],0)) == 3


def test_message_remove_no_longer_exists():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    msg = cw.message_send(user["token"],channel["channel_id"],"Yo")
    cw.message_remove(user["token"],msg["message_id"])
    with pytest.raises(InputError):
        cw.message_remove(user["token"],msg["message_id"])


def test_message_remove_unauthorised_user():
    cw.clear()
    users,channel = helpers.two_users_one_channel()
    msg = cw.message_send(users[0]["token"],channel["channel_id"],"Yo")
    with pytest.raises(AccessError):
        cw.message_remove(users[1]["token"],msg["message_id"])

def test_message_remove_invalid_token():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    msg = cw.message_send(user["token"],channel["channel_id"],"Yo")
    with pytest.raises(AccessError):
        cw.message_remove(111111,msg["message_id"])

def test_message_share():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    msg = cw.message_send(user["token"],channel["channel_id"],"Yo")
    channel2 = cw.channels_create(user["token"],"Channel2",True)
    shared_id = cw.message_share(user["token"],msg["message_id"],'',channel2["channel_id"],-1)
    assert isinstance(shared_id["shared_message_id"],int)
    assert cw.channel_messages(user["token"],channel2["channel_id"],0)["messages"][0]["message"] == '"""\nYo\n"""'

def test_message_share_not_joined():
    cw.clear()
    user, channel = helpers.two_users_one_channel()
    msg = cw.message_send(user[0]["token"],channel["channel_id"],"Yo")
    channel2 = cw.channels_create(user[0]["token"],"Channel2",True)
    with pytest.raises(AccessError):
        cw.message_share(user[1]["token"],msg["message_id"],'',channel2["channel_id"],-1)

def test_message_share_invalid_token():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    msg = cw.message_send(user["token"],channel["channel_id"],"Yo")
    channel2 = cw.channels_create(user["token"],"Channel2",True)
    with pytest.raises(AccessError):
        cw.message_share(11111,msg["message_id"],'',channel2["channel_id"],-1)


def test_message_send_dm():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    print(dm_id)
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    assert isinstance(msg["message_id"],int)
    assert cw.dm_messages(users[0]["token"],dm_id["dm_id"],0)["messages"][0]["message"] == "Yo"

def test_message_send_dm_too_long():
    script = """
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
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    with pytest.raises(InputError):
        cw.message_send_dm(users[0]["token"],dm_id["dm_id"],script)

def test_message_send_dm_unauthorised_user():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    user3 = cw.auth_register("notindm@gmail.com","password","Josh","Dunn")
    with pytest.raises(AccessError):
        cw.message_send_dm(user3["token"],dm_id["dm_id"],"yo")
        
def test_message_send_dm_invalid_token():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    with pytest.raises(AccessError):
        cw.message_send_dm(11111,dm_id["dm_id"],"yo")
       

 


###################################
def test_message_send_later():
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    msg = cw.message_send_later(user["token"],channel["channel_id"],"Yo",datetime.datetime.now().timestamp() + 5)
    assert isinstance(msg["message_id"],int)
    assert cw.channel_messages(user["token"],channel["channel_id"],0)["messages"] == []
    time.sleep(5)
    assert cw.channel_messages(user["token"],channel["channel_id"],0)["messages"][0]["message"] == "Yo" 

def test_message_send_later_invalid_channel():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(InputError):
        cw.message_send_later(user["token"],11111,"Yo",datetime.datetime.now().timestamp() + 5)


def test_message_send_later_big_message():
    script = """
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
    cw.clear()
    user, channel = helpers.one_user_one_channel()
    with pytest.raises(InputError):
        cw.message_send_later(user["token"],channel["channel_id"],script,datetime.datetime.now().timestamp() + 5)
        

def test_send_message_to_the_past():
    cw.clear()
    user,channel = helpers.one_user_one_channel()
    with pytest.raises(InputError):
        cw.message_send_later(user["token"],channel["channel_id"],"Timetravel",datetime.datetime.now().timestamp() - 100)

def test_send_message_later_unauthorised_user():
    cw.clear()
    users = helpers.two_users()
    channel = helpers.one_channel(users[0]["token"])
    with pytest.raises(AccessError):
        cw.message_send_later(users[1]["token"],channel["channel_id"],"Timetravel",datetime.datetime.now().timestamp() + 5)
    
def test_send_message_later_invalid_token():
    cw.clear()
    channel = helpers.one_user_one_channel()
    with pytest.raises(AccessError):
        cw.message_send_later(111111,channel[1]["channel_id"],"Timetravel",datetime.datetime.now().timestamp() + 5)  

def test_message_send_later_dm():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_later_dm(users[0]["token"],dm_id["dm_id"],"Yo",datetime.datetime.now().timestamp() + 5)
    assert isinstance(msg["message_id"],int)
    assert cw.dm_messages(users[0]["token"],dm_id["dm_id"],0)["messages"] == []
    time.sleep(5)
    assert cw.dm_messages(users[0]["token"],dm_id["dm_id"],0)["messages"][0]["message"] == "Yo"

def test_message_send_later_dm_id_invalid():
    cw.clear()
    users = helpers.two_users()
    cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    with pytest.raises(InputError):
        cw.message_send_later_dm(users[0]["token"],1111,"Yo",datetime.datetime.now().timestamp() + 5)

def test_message_send_later_dm_message_long():
    script = """
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
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    with pytest.raises(InputError):
        cw.message_send_later_dm(users[0]["token"],dm_id["dm_id"],script,datetime.datetime.now().timestamp() + 5)


def test_message_send_later_dm_to_past():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    with pytest.raises(InputError):
        cw.message_send_later_dm(users[0]["token"],dm_id["dm_id"],"Yo",datetime.datetime.now().timestamp() - 100)

def test_message_send_later_dm_unauthorised_user():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    user3 = cw.auth_register("thirdwheel@gmail.com","VeryStrong","Chester", "Bennington")
    with pytest.raises(AccessError):
        cw.message_send_later_dm(user3["token"],dm_id["dm_id"],"Yo",datetime.datetime.now().timestamp() + 5)


def test_message_send_later_dm_invalid_token():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    with pytest.raises(AccessError):
        cw.message_send_later_dm(11111,dm_id["dm_id"],"Yo",datetime.datetime.now().timestamp() + 5)

def test_message_react():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    cw.message_react(users[0]["token"],msg["message_id"],1)
    assert cw.dm_messages(users[0]["token"],dm_id["dm_id"],0)["messages"][0]["reacts"] == [{'is_this_user_reacted': None, 'react_id': 1, 'u_ids': [users[0]["auth_user_id"]]}]

    
def test_message_react_invalid_msg_id():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(InputError):
        cw.message_react(users[0]["token"],1111,1)

def test_message_react_invalid_react_id():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(InputError):
        cw.message_react(users[0]["token"],msg["message_id"],4)

def test_message_react_already_reacted():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    cw.message_react(users[0]["token"],msg["message_id"],1)
    with pytest.raises(InputError):
        cw.message_react(users[0]["token"],msg["message_id"],1)

def test_message_react_unauthorised_user():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    user3 = cw.auth_register("intruderalert@gmail.com","verysecure1","Fanta","stick")
    with pytest.raises(AccessError):
        cw.message_react(user3["token"],msg["message_id"],1)

def test_message_react_invalid_token():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(AccessError):
        cw.message_react(11111,msg["message_id"],1)




def test_message_unreact():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    cw.message_react(users[0]["token"],msg["message_id"],1)
    assert cw.dm_messages(users[0]["token"],dm_id["dm_id"],0)["messages"][0]["reacts"] == [{'is_this_user_reacted': None, 'react_id': 1, 'u_ids': [users[0]["auth_user_id"]]}]
    cw.message_unreact(users[0]["token"],msg["message_id"],1)
    assert cw.dm_messages(users[0]["token"],dm_id["dm_id"],0)["messages"][0]["reacts"] ==  []
    
def test_message_unreact_invalid_msg_id():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(InputError):
        cw.message_unreact(users[0]["token"],1111,1)

def test_message_unreact_invalid_react_id():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(InputError):
        cw.message_unreact(users[0]["token"],msg["message_id"],4)

def test_message_unreact_already_reacted():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(InputError):
        cw.message_unreact(users[0]["token"],msg["message_id"],1)

def test_message_unreact_unauthorised_user():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    user3 = cw.auth_register("intruderalert@gmail.com","verysecure1","Fanta","stick")
    with pytest.raises(AccessError):
        cw.message_unreact(user3["token"],msg["message_id"],1)

def test_message_unreact_invalid_token():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(AccessError):
        cw.message_unreact(11111,msg["message_id"],1)


def test_message_pin():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    cw.message_pin(users[0]["token"],msg["message_id"])
    assert cw.dm_messages(users[0]["token"],dm_id["dm_id"],0)["messages"][0]["is_pinned"] is True
    
def test_message_pin_invalid_message():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(InputError):
        cw.message_pin(users[0]["token"],11111)

def test_message_pin_already_pinned():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    cw.message_pin(users[0]["token"],msg["message_id"])
    assert cw.dm_messages(users[0]["token"],dm_id["dm_id"],0)["messages"][0]["is_pinned"] is True
    with pytest.raises(InputError):
        cw.message_pin(users[0]["token"],msg["message_id"])

def test_message_pin_unauthorised_user():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    user3 = cw.auth_register("hotstepper@gmail.com","murderer1","Here","comes")
    with pytest.raises(AccessError):
        cw.message_pin(user3["token"],msg["message_id"])

def test_message_pin_user_not_owner():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(AccessError):
        cw.message_pin(users[1]["token"],msg["message_id"])

def test_message_pin_user_invalid_token():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(AccessError):
        cw.message_pin(11111,msg["message_id"])
        
        

        
def test_message_unpin():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    cw.message_pin(users[0]["token"],msg["message_id"])
    assert cw.dm_messages(users[0]["token"],dm_id["dm_id"],0)["messages"][0]["is_pinned"] is True
    cw.message_unpin(users[0]["token"],msg["message_id"])
    assert cw.dm_messages(users[0]["token"],dm_id["dm_id"],0)["messages"][0]["is_pinned"] is False


def test_message_unpin_invalid_message():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    cw.message_pin(users[0]["token"],msg["message_id"])
    with pytest.raises(InputError):
        cw.message_unpin(users[0]["token"],11111)

def test_message_unpin_already_unpinned():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    assert cw.dm_messages(users[0]["token"],dm_id["dm_id"],0)["messages"][0]["is_pinned"] is False
    with pytest.raises(InputError):
        cw.message_unpin(users[0]["token"],msg["message_id"])

def test_message_unpin_unauthorised_user():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    user3 = cw.auth_register("hotstepper@gmail.com","murderer1","Here","comes")
    with pytest.raises(AccessError):
        cw.message_unpin(user3["token"],msg["message_id"])

def test_message_unpin_user_not_owner():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(AccessError):
        cw.message_unpin(users[1]["token"],msg["message_id"])

def test_message_unpin_user_invalid_token():
    cw.clear()
    users = helpers.two_users()
    dm_id = cw.dm_create(users[0]["token"],[users[0]["auth_user_id"],users[1]["auth_user_id"]])
    msg = cw.message_send_dm(users[0]["token"],dm_id["dm_id"],"Yo")
    with pytest.raises(AccessError):
        cw.message_unpin(11111,msg["message_id"])

