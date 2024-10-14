import pytest

from src.echo import echo
from src.error import InputError, AccessError
from src import state, auth, user, identifier, other


###################################
# Assumptions
#
# - Function imputs/argunments will actually be of correct type
# - The data structure of user.py is known and is the same as the one in user.py
# - auth_register_v1 adds a user dict to the users dict and retursn the dicts u_id
#
###################################


# Reset the state
other.clear_v1()

# Make a user to test implementations with
user_dat = auth.auth_register_v1("test@email.com", "password", "John", "Smith")
user_id = user_dat["auth_user_id"]
user_token = user_dat["token"]

user_dict = {
    'u_id': user_id,
    'email': 'test@email.com',
    'name_first': 'John',
    'name_last': 'Smith',
    'handle_str': 'johnsmith'
}

s = state.get_state()


############################################
# Testing user_profile_v1()
#
############################################

def test_user_profile_valid():
    state.set_state(s)

    # Get user_info dictionary
    user_info = user.user_profile_v1(user_token, user_id)["user"]
    
    # Check the info matches the one in the database
    assert user_info["u_id"] == user_dict["u_id"]
    assert user_info["email"] == user_dict["email"]
    assert user_info["name_first"] == user_dict["name_first"]
    assert user_info["name_last"] == user_dict["name_last"]
    assert user_info["handle_str"] == user_dict["handle_str"]
    assert user_info["profile_img_url"].endswith(".jpg")

    # Check no other values are accessible/given
    assert len(user_info) == 6

def test_user_profile_valid_other():
    """Test that user profile can be accessed by other users too
    """
    state.set_state(s)
    
    # Register another user
    user2_token = auth.auth_register_v1('already@gmail.com', '123abc', 'Nikola', 'Jokic')["token"]
    
    # Get user_info dictionary
    user_info = user.user_profile_v1(user2_token, user_id)["user"]
    
    # Check the info matches the one in the database
    assert user_info["u_id"] == user_dict["u_id"]
    assert user_info["email"] == user_dict["email"]
    assert user_info["name_first"] == user_dict["name_first"]
    assert user_info["name_last"] == user_dict["name_last"]
    assert user_info["handle_str"] == user_dict["handle_str"]

def test_user_profile_invalid_auth_id():
    state.set_state(s)

    # Create an unauthorised user id
    fake_user_id = identifier.get_new_identifier()

    # AccessError
    with pytest.raises(AccessError):
        user.user_profile_v1(fake_user_id, user_id)

def test_user_profile_invalid_user_id():
    state.set_state(s)

    # Create an unauthorised user id
    fake_user_id = identifier.get_new_identifier()

    # InputError
    with pytest.raises(InputError):
        user.user_profile_v1(user_token, fake_user_id)

############################################
# Testing user_list_all_v1()
#
############################################

def test_user_list_all_single():
    """Test user_list_all_v1() returns correct results for single user
    """
    state.set_state(s)
    
    user_list = user.user_list_all_v1(user_token)["users"]
    # Remove profile pic since it's difficult to test
    for mem in user_list: mem.pop("profile_img_url")
    
    assert len(user_list) == 1
    
    assert user_list[0] == user_dict

def test_user_list_all_multi():
    """Test user_list_all_v1() returns correct results for multiple users
    """
    state.set_state(s)
    
    # Register another user
    u2_id = auth.auth_register_v1('already@gmail.com', '123abc', 'Nikola', 'Tesla')["auth_user_id"]
    
    user_list = user.user_list_all_v1(user_token)["users"]
    # Remove references to profile pic as these are difficult to black-box
    for mem in user_list: mem.pop("profile_img_url")
    
    assert len(user_list) == 2
    
    assert user_dict in user_list
    
    assert {
        'u_id': u2_id,
        'email': 'already@gmail.com',
        'name_first': 'Nikola',
        'name_last': 'Tesla',
        'handle_str': 'nikolatesla'
    } in user_list

def test_user_list_all_invalid():
    """Test that an access error is raised when a bad auth_user_id is sent
    """
    state.set_state(s)
    
    # Create an unauthorised user id
    fake_user_id = identifier.get_new_identifier()

    # AccessError
    with pytest.raises(AccessError):
        user.user_list_all_v1(fake_user_id)

############################################
# Testing user_profile_setname_v1()
#
############################################

def test_set_name_valid():
    state.set_state(s)

    # Set new name
    user.user_profile_setname_v1(user_token, "Mary", "Jane")

    # Check new name has been set
    userCheck = user.user_profile_v1(user_token, user_id)["user"]
    assert userCheck["name_first"] == "Mary"
    assert userCheck["name_last"] == "Jane"

def test_set_name_invalid_user():
    state.set_state(s)

    # Create an unauthorised user id
    fake_user_id = identifier.get_new_identifier()

    # InputError
    with pytest.raises(AccessError):
        user.user_profile_setname_v1(fake_user_id, "Mary", "Jane")

def test_set_name_bad_lengths():
    """Try setting profile names to be too short and too long
    """
    state.set_state(s)
    
    # Too short first
    with pytest.raises(InputError):
        user.user_profile_setname_v1(user_token, "", "Hi")
    
    # Too short last
    with pytest.raises(InputError):
        user.user_profile_setname_v1(user_token, "Hi", "")
    
    # Too long first
    with pytest.raises(InputError):
        user.user_profile_setname_v1(user_token, "A" * 51, "Hi")
    
    # Too long last
    with pytest.raises(InputError):
        user.user_profile_setname_v1(user_token, "Hi", "A" * 51)

############################################
# Testing user_profile_setemail_v1()
#
############################################

def test_set_email_valid():
    state.set_state(s)

    # Set new email
    user.user_profile_setemail_v1(user_token, "different@email.com")

    # Check new email has been set
    userCheck = user.user_profile_v1(user_token, user_id)["user"]
    assert userCheck["email"] == "different@email.com"

def test_set_email_dupe():
    state.set_state(s)
    # Register user with email
    auth.auth_register_v1("different@email.com", "123456", "First", "Last")
    with pytest.raises(InputError):
        # Try to set email to that email
        user.user_profile_setemail_v1(user_token, "different@email.com")

def test_set_email_invalid_user():
    state.set_state(s)

    # Create an unauthorised user id
    fake_user_id = identifier.get_new_identifier()

    # AccessError
    with pytest.raises(AccessError):
        user.user_profile_setemail_v1(fake_user_id, "different@email.com")

def test_set_email_invalid_email():
    state.set_state(s)

    # InputError
    with pytest.raises(InputError):
        user.user_profile_setemail_v1(user_token, "incorrectFormat")


############################################
# Testing user_profile_sethandle_v1()
#
############################################

def test_set_handle_valid():
    state.set_state(s)

    # Set new handle
    user.user_profile_sethandle_v1(user_token, "Johnny")

    # Check new handle has been set
    userCheck = user.user_profile_v1(user_token, user_id)["user"]
    assert userCheck["handle_str"] == "Johnny"

def test_set_handle_invalid_user():
    state.set_state(s)

    # Create an unauthorised user id
    fake_user_id = identifier.get_new_identifier()

    # AccessError
    with pytest.raises(AccessError):
        user.user_profile_sethandle_v1(fake_user_id, "Johnny")

def test_set_handle_invalid_has_at():
    """Try to set the user's handle to a handle that has the '@' character in it
    """
    state.set_state(s)
    
    with pytest.raises(InputError):
        user.user_profile_sethandle_v1(user_token, "@Johnny")

def test_set_handle_has_whitespace():
    """Try to set user's handle to something with whitespace
    """
    state.set_state(s)
    
    # Space
    with pytest.raises(InputError):
        user.user_profile_sethandle_v1(user_token, "john smith")
    
    # New-line
    with pytest.raises(InputError):
        user.user_profile_sethandle_v1(user_token, "john\nsmith")
    
    # Tab
    with pytest.raises(InputError):
        user.user_profile_sethandle_v1(user_token, "john\tsmith")
   
def test_set_handle_invalid_bad_length():
    """Try to set a handle that is too short or long
    """
    state.set_state(s)
    
    # Too short <3 chars
    with pytest.raises(InputError):
        user.user_profile_sethandle_v1(user_token, "Jo")
    
    # Too long >20 chars
    with pytest.raises(InputError):
        user.user_profile_sethandle_v1(user_token, 
                                       "JohnnyHasAVeryLongHandleThatIsInvalid")

def test_set_handle_invalid_already_existant():
    """Try to set a handle that is already in use by another user
    """
    state.set_state(s)
    
    # Register new user (don't need to do anything with their data, we're just
    # taking their handle up)
    auth.auth_register_v1("someone@example.com", "password", "James", "Stack")
    
    with pytest.raises(InputError):
        user.user_profile_sethandle_v1(user_token, "jamesstack")

def test_set_handle_no_change():
    """Try to set the handle to the current handle
    """
    state.set_state(s)
    
    # Set new handle
    user.user_profile_sethandle_v1(user_token, "johnsmith")

    # Check new handle has been set
    userCheck = user.user_profile_v1(user_token, user_id)["user"]
    assert userCheck["handle_str"] == "johnsmith"
    
############################################
# Testing user_profile_uploadphoto_v1()
#
############################################

def test_set_profile_pic_bad_size_1():
    state.set_state(s)

    img_url = "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"
    
    with pytest.raises(InputError):
         user.user_profile_uploadphoto_v1(user_token, img_url, 0, 0, 1000000, 1000000)

def test_set_profile_pic_bad_size_2():
    state.set_state(s)
       
    img_url = "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"

    with pytest.raises(InputError):
         user.user_profile_uploadphoto_v1(user_token, img_url, -1, -2, 0, 0)
         
def test_set_profile_pic_bad_size_3():
    state.set_state(s)
       
    img_url = "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"

    with pytest.raises(InputError):
         user.user_profile_uploadphoto_v1(user_token, img_url, 0, -2, 100000, 0)
         
def test_set_profile_pic_bad_type():
    state.set_state(s)
    
    img_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
    
    with pytest.raises(InputError):
         user.user_profile_uploadphoto_v1(user_token, img_url, 0, 0, 100, 100)

def test_set_profile_pic_bad_url():
    state.set_state(s)
    
    img_url = "not a url"
    
    with pytest.raises(InputError):
         user.user_profile_uploadphoto_v1(user_token, img_url, 0, 0, 100, 100)

def test_set_profile_pic_bad_token():
    state.set_state(s)
    
    img_url = "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"

    with pytest.raises(AccessError):
         user.user_profile_uploadphoto_v1('invalid_token', img_url, 0, 0, 200, 300)

def test_profile_pic_default():
    state.set_state(s)
    
    profile_pic_url = user.user_profile_v1(user_token, user_id)["user"]["profile_img_url"]

    # Check image is stored in perm resources for default profile pic
    assert "perm_resources" in profile_pic_url

def test_profile_pic_set():
    state.set_state(s)
    
    # Set profile pic
    img_url = "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"
    user.user_profile_uploadphoto_v1(user_token, img_url, 0, 0, 50, 50)
    
    profile_pic_url = user.user_profile_v1(user_token, user_id)["user"]["profile_img_url"]

    # Check image is stored in perm resources for default profile pic
    assert str(user_id) in profile_pic_url
    assert "state_resources" in profile_pic_url
