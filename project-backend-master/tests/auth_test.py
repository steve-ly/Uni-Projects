"""tests > auth_test.py

Provides tests for src > auth.py

Primary Contributors: 
 - Steven Ly [z5257127@ad.unsw.edu.au]
     - All tests excepting those mentioned below

Minor Contributors:
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]
     - test_registering_handle_different_names()

"""

import pytest
from src.echo import echo 
from src import auth, user, error, state, other, admin

#reset state
other.clear_v1()

################################################################################
# Test auth register
#
# Register test requires relevant user.py functions to be functionable
# TODO: Fix lack of black-box in these tests, when possible (iteration 2)
################################################################################

def test_register_valid():
    """Tests database for sucessful registration
    """
    other.clear_v1()
    
    auth_user_id = auth.auth_register_v1('validemail@gmail.com', '123abc', 'Dave', 'Grohl')
    u = user.user_profile_v1(auth_user_id["token"], auth_user_id["auth_user_id"])["user"]

    assert type(auth_user_id["auth_user_id"]) is int
    assert type(auth_user_id["token"]) is str
    assert u['email'] == "validemail@gmail.com"
    assert u["name_first"] == "Dave"
    assert u["name_last"] == "Grohl"
    assert u["u_id"] == auth_user_id["auth_user_id"]

def test_register_invalid_email():
    """Tests for inputerror e if email used is not in correct format, e.g no @
    """
    other.clear_v1()
    
    with pytest.raises(error.InputError):
        auth.auth_register_v1('bad_mailgmail.com', '123abc', 'James', 'Cameron')

def test_valid_but_complex_email():
    """Test that a user with an email address that uses multiple subdomains
    can still register
    """
    other.clear_v1()
    auth.auth_register_v1('z1234567@ad.unsw.edu.au', '123abc', 'Dave', 'Grohl')

def test_invalid_email_ending_dot():
    """Tests that an email ending with a dot will be deemed incorrect
    """
    other.clear_v1()
    with pytest.raises(error.InputError):
        auth.auth_register_v1('someone@email.com.', '123abc', 'Dave', 'Grohl')

def test_registered_already():
    """Tests for inputerror if user is using an email already taken
    """
    other.clear_v1()
    
    auth.auth_register_v1('already@gmail.com', '123abc', 'Nikola', 'Jokic')
    with pytest.raises(error.InputError):
        auth.auth_register_v1('already@gmail.com', '123abc', 'Nikola', 'Jokic')

def test_registered_already_different_capitalisation():
    """Tests that an account is registered as being duplicate if the email has
    different capitalisation
    """
    other.clear_v1()
    
    auth.auth_register_v1('already@gmail.com', '123abc', 'Nikola', 'Jokic')
    with pytest.raises(error.InputError):
        auth.auth_register_v1('ALREADY@GMAIL.COM', '123abc', 'Nikola', 'Jokic')

def test_registered_password_small():
    """Tests for inputerror if user is registering with a password less than 6 characters
    """
    other.clear_v1()
    
    with pytest.raises(error.InputError):
        auth.auth_register_v1('already@gmail.com', '12345', 'Jimmy', 'Buckets')

def test_registering_big_first_name():
    """Tests for inputerror if user's first name is too large
    """
    other.clear_v1()
    
    with pytest.raises(error.InputError):
        auth.auth_register_v1('longname@gmail.com', '123abc', 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'poisson')

def test_registering_big_last_name():
    """Tests for inputerror if user's last name is too large
    """
    other.clear_v1()
    
    with pytest.raises(error.InputError):
        auth.auth_register_v1('longlastname@gmail.com', '123abc', 'MintChoc', 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')

def test_registering_small_first_name():
    """Tests for inputerror if user's first name is too small
    """
    other.clear_v1()
    
    with pytest.raises(error.InputError):
        auth.auth_register_v1('nofirstname@gmail.com', '123abc', '', 'box')

def test_registering_small_last_name():
    """Tests for inputerror if user's first name is too small
    """
    other.clear_v1()
    
    with pytest.raises(error.InputError):
        auth.auth_register_v1('nolastname@gmail.com', '123abc', 'Zinger', '')

def test_registering_handle():
    """Tests for sucessful handle generated
    """
    other.clear_v1()
    
    u_id = auth.auth_register_v1('handletest@gmail.com', '123abc', 'Dick', 'Smith')
    u = user.user_profile_v1(u_id["token"], u_id["auth_user_id"])["user"]
    assert(u["handle_str"]) == "dicksmith"

def test_registering_big_handle():
    """Tests for sucessful handle generated for a large name
    """
    other.clear_v1()
    
    u_id = auth.auth_register_v1('bighandletest@gmail.com', '123abc', 'Constantine', 'Shakespeare')
    u = user.user_profile_v1(u_id["token"], u_id["auth_user_id"])["user"]
    assert u["handle_str"] == "constantineshakespea"

def test_registering_same_handle():
    """Tests for sucessful handle generated for a mulitple instancs of the same name
    """
    other.clear_v1()
    
    id_1 = auth.auth_register_v1('handlenumberone@gmail.com', '123abc', 'when', 'imposter')
    id_2 = auth.auth_register_v1('handlenumbertwo@gmail.com', '123abc', 'when', 'imposter')
    id_3 = auth.auth_register_v1('handlenumberthree@gmail.com', '123abc', 'when', 'imposter')
    us1 = user.user_profile_v1(id_1["token"], id_1["auth_user_id"])["user"]
    us2 = user.user_profile_v1(id_1["token"], id_2["auth_user_id"])["user"]
    us3 = user.user_profile_v1(id_1["token"], id_3["auth_user_id"])["user"]
    assert us1["handle_str"] == "whenimposter" 
    assert us2["handle_str"] == "whenimposter0"
    assert us3["handle_str"] == "whenimposter1"

def test_registering_same_big_handle():
    """Test for successful handle generated for multiple instances 
    of the same name that is greater than 20 char
    """
    other.clear_v1()
    
    id_1 = auth.auth_register_v1('bighandletest1@gmail.com', '123abc', 'Tetrahydrocannabinol', 'bad')
    id_2 = auth.auth_register_v1('bighandletest2@gmail.com', '123abc', 'Tetrahydrocannabinol', 'bad')
    us1 = user.user_profile_v1(id_1["token"], id_1["auth_user_id"])["user"]
    us2 = user.user_profile_v1(id_1["token"], id_2["auth_user_id"])["user"]
    assert us1["handle_str"] == "tetrahydrocannabinol" 
    assert us2["handle_str"] == "tetrahydrocannabinol0"

def test_registering_all_caps():
    """Test for successful handle generated for handle with all capitals
    """
    other.clear_v1()
    
    u_id = auth.auth_register_v1('allcaps@gmail.com', '123abc', 'DYATLOV', 'PASS')
    us1 = user.user_profile_v1(u_id["token"], u_id["auth_user_id"])["user"]
    assert us1["handle_str"] == "dyatlovpass" 

def test_registering_handle_bad_handle():
    """Test whether @ symbols are correctly removed from the handle string
    """
    other.clear_v1()
    
    u_id = auth.auth_register_v1('chickennuggets@gmail.com', '123abc', 'nev er gon', 'n@ give you up')
    us1 = user.user_profile_v1(u_id["token"], u_id["auth_user_id"])["user"]
    assert us1["handle_str"] == "nevergonngiveyouup"

def test_registering_handle_different_names():
    """Test that registering people with similar but different names
    still generates correct handle numeric extensions
    """
    other.clear_v1()
    
    u_1 = auth.auth_register_v1('chickennuggets@gmail.com', '123abc', 'Haroldiumus', 'Panelsmith')
    u_2 = auth.auth_register_v1('beefnuggets@gmail.com', '123abc', 'Haroldiumus', 'Panelsmite')
    us1 = user.user_profile_v1(u_1["token"], u_1["auth_user_id"])["user"]
    us2 = user.user_profile_v1(u_1["token"], u_2["auth_user_id"])["user"]
    assert us1["handle_str"] == "haroldiumuspanelsmit"
    assert us2["handle_str"] == "haroldiumuspanelsmit0"

def test_owner_permission():
    """Tests that the first user has admin permissions
    and that other users don't
    """
    other.clear_v1()
    u_1 = auth.auth_register_v1('beachbunnycloud9@gmail.com', '123abc', 'Milo', 'Thatch')
    u_2 = auth.auth_register_v1('deadbutterfliesartifacts@gmail.com', '123abc', 'Jeff', 'Lebowski')
    
    # u_2 shouldn't be able to make u_1 an normal user
    with pytest.raises(error.AccessError):
        admin.admin_permssion_change_v1(u_2["token"], u_1["auth_user_id"], 2)
    
    # u_1 should be able to make u_2 an admin
    admin.admin_permssion_change_v1(u_1["token"], u_2["auth_user_id"], 1)

################################################################################
# Test auth login
#
# login test requires auth_register to be successful and relevant user.py functions 
# to be functionable
################################################################################

def test_login_valid():
    """Tests for sucessful login
    """
    other.clear_v1()
    
    auth.auth_register_v1('registeringemail@gmail.com', '123abc', 'Dave', 'Grohl')
    login = auth.auth_login_v1('registeringemail@gmail.com', '123abc') 
    
    assert type(login["auth_user_id"]) is int
    assert type(login["token"]) is str

def test_login_non_existent():
    """Tests for inputerror when logging in with email that has not be registered
    """
    other.clear_v1()
    
    with pytest.raises(error.InputError):
        auth.auth_login_v1('notreal@gmail.com', '123abc')

def test_login_invalid():
    """Tests for inputerror when email user logins with is in incorrect format, 
    e.g no use of @
    """
    other.clear_v1()
    
    auth.auth_register_v1('deadopeninside@gmail.com', '123abc', 'Glenn', 'Rhee')
    with pytest.raises(error.InputError):
        auth.auth_login_v1('deadopeninsidegmail.com', '123abc')

def test_login_incorrect_password():
    """Tests for inputerror when logging in with incorrect password
    """
    other.clear_v1()
    
    auth.auth_register_v1('burtmacklinfbi@gmail.com', '123abc', 'Burt', 'Macklin')
    with pytest.raises(error.InputError):
        auth.auth_login_v1('burtmacklinfbi@gmail.com', 'abc123')

################################################################################
# Test auth logout
#
# requires auth_register to be successful and relevant user.py functions 
# to be functionable
################################################################################
def test_logout_valid_token():
    """ User attempts to logout with a valid token and logout returns True.
    """
    other.clear_v1()
    usr = auth.auth_register_v1("testEmail@email.com", "123abc", "Ryan", "Reynolds")
    token = usr["token"]
    assert auth.auth_logout_v1(token)["is_success"]
    
    # After logout they shouldn't be able to acces things
    with pytest.raises(error.AccessError):
        user.user_profile_v1(token, usr["auth_user_id"])


def test_logout_invalid_token():
    """Tests for false when invalid token 
    """
    other.clear_v1()
    with pytest.raises(error.AccessError):
        auth.auth_logout_v1(12321313)


def test_logout_multiple_sessions():
    """Tests for successful logout of duplicate logins
    """
    other.clear_v1()

    usr = auth.auth_register_v1("testEmail@email.com", "123abc", "Ryan", "Reynolds")
    usr_dupe = auth.auth_login_v1("testEmail@email.com", "123abc")

    auth.auth_logout_v1(usr["token"])
    
    # Should be able to access with the second token
    user.user_profile_v1(usr_dupe["token"], usr["auth_user_id"])
    
    # But not the first
    with pytest.raises(error.AccessError):
        user.user_profile_v1(usr["token"], usr["auth_user_id"])

def test_multiple_logout_attempt():
    """Tests for error when attempting to logout with invalid session
    """
    other.clear_v1()
    user = auth.auth_register_v1("testEmail@email.com", "123abc", "Ryan", "Reynolds")
    auth.auth_logout_v1(user["token"])
    with pytest.raises(error.AccessError):
        auth.auth_logout_v1(user["token"])


################################################################################
# Test auth password request and reset
#
# requires auth_register,auth_login to be successful and relevant user.py functions 
# to be functionable
################################################################################

def test_password_request():
    other.clear_v1()
    auth.auth_register_v1("receivingpassrequest1@gmail.com", "123abc", "Number", "One")
    auth.auth_password_reset_request("receivingpassrequest1@gmail.com")
    
def test_password_request_non_existant_email():
    other.clear_v1()
    auth.auth_register_v1("receivingpassrequest1@gmail.com", "123abc", "Number", "One")
    auth.auth_password_reset_request("testEmail1@email.com")
    assert len(state.s.password_requests) == 0

def test_password_reset():
    other.clear_v1()
    auth.auth_register_v1("receivingpassrequest1@gmail.com", "123abc", "Number", "One")
    auth.auth_password_reset_request("receivingpassrequest1@gmail.com")
    assert len(state.s.password_requests) == 1
    # This will only happen once, but we can't get the code any other way
    code = 0
    for code_temp in state.s.password_requests._contained.keys():
        code = code_temp
   
    auth.auth_password_reset_reset(code, "holymoly")
    #try to login 
    auth.auth_login_v1("receivingpassrequest1@gmail.com","holymoly")
    # Ensure request was removed afterwards
    assert len(state.s.password_requests) == 0

def test_password_reset_invalid_code():
    other.clear_v1()
    auth.auth_register_v1("receivingpassrequest1@gmail.com", "123abc", "Number", "One")
    auth.auth_password_reset_request("receivingpassrequest1@gmail.com")
    with pytest.raises(error.InputError):
        auth.auth_password_reset_reset(1111,"holymoly")
    
def test_password_reset_short_password():
    other.clear_v1()
    auth.auth_register_v1("receivingpassrequest1@gmail.com", "123abc", "Number", "One")
    auth.auth_password_reset_request("receivingpassrequest1@gmail.com")
    for code in state.s.password_requests._contained.keys():
        with pytest.raises(error.InputError): 
            auth.auth_password_reset_reset(code, "hello")
        #try to login with old password
        auth.auth_login_v1("receivingpassrequest1@gmail.com","123abc")

def test_multiple_request_attempt():
    other.clear_v1()
    code1 = 0
    code2 = 0
    auth.auth_register_v1("receivingpassrequest1@gmail.com", "123abc", "Number", "One")
    auth.auth_password_reset_request("receivingpassrequest1@gmail.com")
    for code in state.s.password_requests._contained.keys():
        code1 = code
    auth.auth_password_reset_request("receivingpassrequest1@gmail.com")
    for code in state.s.password_requests._contained.keys():
        code2 = code
    assert len(state.s.password_requests) == 1
    with pytest.raises(error.InputError): 
        auth.auth_password_reset_reset(code1, "hello")
    auth.auth_password_reset_reset(code2,"Howdy12")
    auth.auth_login_v1("receivingpassrequest1@gmail.com","Howdy12")
