import pytest

from . import call_wrappers as cw
from . import helpers
from src.error import InputError, AccessError

def test_user_profile():
    cw.clear()
    user = helpers.one_user()
    returning_user = cw.user_profile(user["token"],user["auth_user_id"])
    # Remove references to profile pic as these are difficult to black-box
    returning_user["user"].pop("profile_img_url")
    assert returning_user["user"] == {'u_id': user["auth_user_id"], 'email': 'someone@example.com', 'name_first': 'John', 'name_last': 'Doe', 'handle_str': 'johndoe'}

def test_user_profile_invalid_user_id():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(InputError): 
        cw.user_profile(user["token"],111111)
        

def test_user_profile_invalid_token():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(AccessError): 
        cw.user_profile(111111,user["auth_user_id"])



def test_user_setname():
    cw.clear()
    user = helpers.one_user()
    cw.user_profile_setname(user["token"],"Chris","Bumstead")
    assert cw.user_profile(user["token"],user["auth_user_id"])["user"]["name_first"] == "Chris"
    assert cw.user_profile(user["token"],user["auth_user_id"])["user"]["name_last"] == "Bumstead"

def test_user_setname_first_name_long():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(InputError):
        cw.user_profile_setname(user["token"],"boo"*50,"yoo")


def test_user_setname_first_name_short():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(InputError):
        cw.user_profile_setname(user["token"],"","yoo")

def test_user_setname_last_name_long():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(InputError):
        cw.user_profile_setname(user["token"],"boo","yoo"*50)

def test_user_setname_first_last_short():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(InputError):
        cw.user_profile_setname(user["token"],"boo","")

def test_user_setname_invalid_token():
    cw.clear()
    helpers.one_user()
    with pytest.raises(AccessError):
            cw.user_profile_setname(1111111,"Big","Guy")



def test_user_setemail():
    cw.clear()
    user = helpers.one_user()
    cw.user_profile_setemail(user["token"],"mountaindew@gmail.com")
    assert cw.user_profile(user["token"],user["auth_user_id"])["user"]["email"] == "mountaindew@gmail.com"
    
def test_user_setemail_invalid_email():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(InputError):
        cw.user_profile_setemail(user["token"],"mountaindew.com")

def test_user_setemail_already_in_use(): ##Not implemented yet
    cw.clear()
    users = helpers.two_users()
    with pytest.raises(InputError):
        cw.user_profile_setemail(users[0]["token"],"someone_else@example.com")

def test_user_setemail_invalid_token():
    cw.clear()
    helpers.one_user()
    with pytest.raises(AccessError):
        cw.user_profile_setemail(111111,"theverybestemailever@gmail.com")


def test_user_sethandle():
    cw.clear()
    user = helpers.one_user()
    cw.user_profile_sethandle(user["token"],"tfueclassic")
    assert cw.user_profile(user["token"],user["auth_user_id"])["user"]["handle_str"] == "tfueclassic"
    
def test_user_sethandle_too_short():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(InputError):
        cw.user_profile_sethandle(user["token"],"1")

def test_user_sethandle_too_long():
    cw.clear()
    user = helpers.one_user()
    with pytest.raises(InputError):
        cw.user_profile_sethandle(user["token"],"1"*21)

def test_user_sethandle_handle_taken():
    cw.clear()
    users = helpers.two_users()
    with pytest.raises(InputError):
        cw.user_profile_sethandle(users[0]["token"],"janelee")

def test_user_sethandle_invalid_token():
    cw.clear()
    helpers.one_user()
    with pytest.raises(AccessError):
        cw.user_profile_sethandle(111111,"boomtastic")

def test_user_all():
    cw.clear()
    user = helpers.one_user()
    assert len(cw.users_all(user["token"])) == 1 

def test_user_all_invalid_token():
    cw.clear()
    helpers.one_user()
    with pytest.raises(AccessError):
        cw.users_all(111111)

def test_user_upload_profile_picture():
    cw.clear()
    user = helpers.one_user()
    url = "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"
    cw.user_profile_uploadphoto(user["token"],url,0,0,2,2)
    assert str(user["auth_user_id"]) in cw.user_profile(user["token"],user["auth_user_id"])["user"]["profile_img_url"]


def test_user_upload_profile_picture_invalid_image_url():
    cw.clear()
    user = helpers.one_user()
    url = "not a url"
    with pytest.raises(InputError):
        cw.user_profile_uploadphoto(user["token"],url,0,0,2,2)

def test_user_upload_profile_picture_invalid_coord():
    cw.clear()
    user = helpers.one_user()
    url = "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"
    with pytest.raises(InputError):
        cw.user_profile_uploadphoto(user["token"],url,-1,-1,-1,-1)

def test_user_upload_profile_picture_not_jpg():
    cw.clear()
    user = helpers.one_user()
    url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
    with pytest.raises(InputError):
        cw.user_profile_uploadphoto(user["token"],url,0,0,2,2)

def test_user_upload_profile_picture_invalid_token():
    cw.clear()
    helpers.one_user()
    url = "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"
    with pytest.raises(AccessError):
        cw.user_profile_uploadphoto(11111,url,0,0,2,2)
