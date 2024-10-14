"""
Test auth/ routes
"""
import pytest
import json
import urllib.request
from . import call_wrappers as cw
from . import helpers
from src.error import AccessError, InputError

def test_register():
    cw.clear()
    user = cw.auth_register("someone@example.com", "Password1", "John", "Doe")
    
    assert len(user) == 2
    assert isinstance(user["token"], str)
    assert isinstance(user["auth_user_id"], int)

def test_register_bad_email():
    cw.clear()
    with pytest.raises(InputError):
        cw.auth_register("someoneexample.com", "Password1", "John", "Doe")

def test_register_already_used_email():
    cw.clear()
    cw.auth_register("someone@example.com", "Password1", "John", "Doe")
    with pytest.raises(InputError):
        cw.auth_register("someone@example.com", "Password1", "John", "Doe")


def test_register_bad_password():
    cw.clear()
    with pytest.raises(InputError):
        cw.auth_register("someone@example.com", "Pass", "John", "Doe")

def test_register_bad_name():
    cw.clear()
    with pytest.raises(InputError):
        # first too long
        cw.auth_register("someone@example.com", "Password1", "John"*50, "Doe")
    with pytest.raises(InputError):
        # last too long
        cw.auth_register("someone@example.com", "Password1", "John", "Doe"*50)
    with pytest.raises(InputError):
        # first too short
        cw.auth_register("someone@example.com", "Password1", "", "Doe")
    with pytest.raises(InputError):
        # last too short
        cw.auth_register("someone@example.com", "Password1", "John", "")

################################################################################

def test_login():
    cw.clear()
    user = helpers.one_user()

    data = cw.auth_login("someone@example.com", "Password1")
    
    assert data["auth_user_id"] == user["auth_user_id"]
    # Tokens should be different becuase they are different sessions
    assert data["token"] != user["token"]

def test_login_bad_pass():
    cw.clear()
    helpers.one_user()
    
    with pytest.raises(InputError):
        cw.auth_login("someone@example.com", "Password2")

def test_login_bad_email():
    cw.clear()
    helpers.one_user()
    
    with pytest.raises(InputError):
        cw.auth_login("someoneexample.com", "Password1")

def test_email_no_belong():
    cw.clear()
    helpers.one_user()
    with pytest.raises(InputError):
        cw.auth_login("someone4@example.com", "Password1")


def test_logout():
    cw.clear()
    user = helpers.one_user()
    result = cw.auth_logout(user["token"])
    assert result["is_success"]

def test_logout_invalid_token():
    cw.clear()
    with pytest.raises(AccessError):
        cw.auth_logout(1232314)

#Not black box
        
def test_password_request():
    cw.clear()
    cw.auth_register("receivingpassrequest1@gmail.com","originalpw","Cool","Beans")
    cw.auth_password_request("receivingpassrequest1@gmail.com")


def test_password_reset_invalid_code():
    cw.clear()
    cw.auth_register("receivingpassrequest1@gmail.com","originalpw","Cool","Beans")
    cw.auth_password_request("receivingpassrequest1@gmail.com")
    with pytest.raises(InputError):
        cw.auth_password_reset(11,"Thisiscoolas")

def test_small_password():
    cw.clear()
    cw.auth_register("receivingpassrequest1@gmail.com","originalpw","Cool","Beans")
    cw.auth_password_request("receivingpassrequest1@gmail.com")
    with pytest.raises(InputError) as info: 
        cw.auth_password_reset(1111,"T")
        assert info.value.message == "Password entered is less than 6 characters long"
