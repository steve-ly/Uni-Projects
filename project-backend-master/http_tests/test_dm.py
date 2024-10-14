import pytest

from . import call_wrappers as cw
from . import helpers
from src.error import InputError, AccessError


def test_dm_create():
    cw.clear()
    users = helpers.two_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    assert isinstance(dm["dm_id"],int)
    assert isinstance(dm["dm_name"],str)


def test_dm_create_invalid_user_id():
    cw.clear()
    users = helpers.two_users()
    with pytest.raises(InputError):
        cw.dm_create(users[0]["token"],[11111])

def test_dm_create_invalid_token():
    cw.clear()
    users = helpers.two_users()
    with pytest.raises(AccessError):
        cw.dm_create(11111,[users[1]["auth_user_id"]])
    

def test_dm_details():
    cw.clear()
    users = helpers.two_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    details = cw.dm_details(users[0]["token"],dm["dm_id"])
    assert details["name"] == "janelee, johndoe"
    assert len(details["members"]) == 2
    
def test_dm_details_invalid_dm_id():
    cw.clear()
    users = helpers.two_users()
    cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    with pytest.raises(InputError):
        cw.dm_details(users[0]["token"],11111)

def test_dm_details_unauthorised_user():
    cw.clear()
    users = helpers.two_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    user3 = cw.auth_register("pugthegoat@gmail.com","awersome123","Howdy","ho")
    with pytest.raises(AccessError):
        cw.dm_details(user3["token"],dm["dm_id"])

def test_dm_details_invalid_token():
    cw.clear()
    users = helpers.two_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    with pytest.raises(AccessError):
        cw.dm_details(11111,dm["dm_id"])



def test_dm_list():
    cw.clear()
    users = helpers.two_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    list = cw.dm_list(users[0]["token"])  
    assert list["dms"][0]["dm_id"] == dm["dm_id"]
    assert list["dms"][0]["name"] == dm["dm_name"]
    
def test_dm_list_invalid_token():
    cw.clear()
    users = helpers.two_users()
    cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    with pytest.raises(AccessError):
        cw.dm_list(111111)  


def test_dm_remove():
    cw.clear()
    users = helpers.two_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    cw.dm_remove(users[0]["token"], dm["dm_id"])
    assert len(cw.dm_list(users[0]["token"])) == 1

def test_dm_remove_invalid_dm():
    cw.clear()
    users = helpers.two_users()
    cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    with pytest.raises(InputError):
        cw.dm_remove(users[0]["token"], 11111)

def test_dm_remove_not_creator():
    cw.clear()
    users = helpers.two_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    with pytest.raises(AccessError):
        cw.dm_remove(users[1]["token"], dm["dm_id"])

def test_dm_remove_invalid_token():
    cw.clear()
    users = helpers.two_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    with pytest.raises(AccessError):
        cw.dm_remove(1111111, dm["dm_id"])



def test_dm_invite():
    cw.clear()
    users = helpers.three_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    details = cw.dm_details(users[0]["token"],dm["dm_id"])
    print("Yo")
    print(details["members"])
    assert len(details["members"]) == 2
    cw.dm_invite(users[0]["token"],dm["dm_id"],users[2]["auth_user_id"])
    details2 = cw.dm_details(users[0]["token"],dm["dm_id"])
    assert len(details2["members"]) == 3

def test_dm_invite_invalid_dm_id():
    cw.clear()
    users = helpers.three_users()
    cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    with pytest.raises(InputError):
        cw.dm_invite(users[0]["token"],111111,users[2]["auth_user_id"])

def test_dm_invite_invalid_u_id():
    cw.clear()
    users = helpers.three_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    with pytest.raises(InputError):
        cw.dm_invite(users[0]["token"],dm["dm_id"],11111)

def test_dm_invite_unauthorised_user():
    cw.clear()
    users = helpers.three_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    user4 = cw.auth_register("chickentendies@gmail.com","octanemain","JUmp","stim")
    with pytest.raises(AccessError):
        cw.dm_invite(users[2]["token"],dm["dm_id"],user4["auth_user_id"])

def test_dm_invite_invalid_token():
    cw.clear()
    users = helpers.three_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    with pytest.raises(AccessError):
        cw.dm_invite(111111,dm["dm_id"],users[2]["auth_user_id"])


def test_dm_leave():
    cw.clear()
    users = helpers.three_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    cw.dm_invite(users[0]["token"],dm["dm_id"],users[2]["auth_user_id"])
    assert len(cw.dm_details(users[0]["token"],dm["dm_id"])["members"]) == 3
    cw.dm_leave(users[2]["token"],dm["dm_id"])
    assert len(cw.dm_details(users[0]["token"],dm["dm_id"])["members"]) == 2

def test_dm_leave_invalid_dm_id():
    cw.clear()
    users = helpers.three_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]])
    cw.dm_invite(users[0]["token"],dm["dm_id"],users[2]["auth_user_id"])
    with pytest.raises(InputError):
        cw.dm_leave(users[2]["token"],111111)

def test_dm_leave_unauthorised_user():
    cw.clear()
    users = helpers.three_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]]) 
    with pytest.raises(AccessError):
        cw.dm_leave(users[2]["token"],dm["dm_id"])

def test_dm_leave_invalid_token():
    cw.clear()
    users = helpers.three_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]]) 
    cw.dm_invite(users[0]["token"],dm["dm_id"],users[2]["auth_user_id"])
    with pytest.raises(AccessError):
        cw.dm_leave(11111111,dm["dm_id"])


def test_dm_messages():
    cw.clear()
    users = helpers.two_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]]) 
    cw.message_send_dm(users[0]["token"], dm["dm_id"],"Yo")
    assert cw.dm_messages(users[0]["token"], dm["dm_id"],0)["messages"][0]["message"] == "Yo"
    
def test_dm_messages_invalid_dm():
    cw.clear()
    users = helpers.two_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]]) 
    cw.message_send_dm(users[0]["token"], dm["dm_id"],"Yo")
    with pytest.raises(InputError):
        cw.dm_messages(users[0]["token"], 11111,0)
        
def test_dm_messages_invalid_start():
    cw.clear()
    users = helpers.two_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]]) 
    cw.message_send_dm(users[0]["token"], dm["dm_id"],"Yo")
    with pytest.raises(InputError):
        cw.dm_messages(users[0]["token"], dm["dm_id"],2)
    
def test_dm_messsages_unauthorised_user():
    cw.clear()
    users = helpers.three_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]]) 
    cw.message_send_dm(users[0]["token"], dm["dm_id"],"Yo")
    with pytest.raises(AccessError):
        cw.dm_messages(users[2]["token"], dm["dm_id"],0)

def test_dm_messsages_invalid_token():
    cw.clear()
    users = helpers.two_users()
    dm = cw.dm_create(users[0]["token"],[users[1]["auth_user_id"]]) 
    cw.message_send_dm(users[0]["token"], dm["dm_id"],"Yo")
    with pytest.raises(AccessError):
        cw.dm_messages(11111, dm["dm_id"],0)