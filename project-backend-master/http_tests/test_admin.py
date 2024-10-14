import pytest

from . import call_wrappers as cw
from . import helpers
from src.error import InputError, AccessError
#Test end goals for admin remove path

def test_sucessful_removal():
    cw.clear()
    users = helpers.two_users()
    cw.admin_user_remove(users[0]["token"], users[1]["auth_user_id"])
    
def test_removing_only_owner():
    cw.clear()
    users = helpers.one_user()
    with pytest.raises(InputError):
        cw.admin_user_remove(users["token"], users["auth_user_id"])

def test_removing_invalid_user_id():
    cw.clear()
    users = helpers.one_user()
    with pytest.raises(InputError):
        cw.admin_user_remove(users["token"], 11111)

def test_removing_not_owner():
    cw.clear()
    users = helpers.two_users()
    with pytest.raises(AccessError):
        cw.admin_user_remove(users[1]["token"], users[0]["auth_user_id"])
    
#Test end goals for admin permission change

def test_sucessful_perm_change():
    cw.clear()
    users = helpers.two_users()
    cw.admin_userpermission_change(users[0]["token"],users[1]["auth_user_id"],1)

def test_perms_change_invalid_user_id():
    cw.clear()
    users = helpers.one_user()
    with pytest.raises(InputError):
        cw.admin_userpermission_change(users["token"],11111,1)

def test_perms_change_invalid_permission_id():
    cw.clear()
    users = helpers.two_users()
    with pytest.raises(InputError):
        cw.admin_userpermission_change(users[0]["token"],users[1]["auth_user_id"],6)

def test_perms_change_not_owner():
    cw.clear()
    users = helpers.two_users()
    with pytest.raises(AccessError):
        cw.admin_userpermission_change(users[1]["token"],users[0]["auth_user_id"],1)