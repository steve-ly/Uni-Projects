"""
Contains fixtures to speed up testing
"""
import pytest

# I know this is bad , but I don't have time to do every function manually
# so please just deal with it
from .call_wrappers import *

################################################################################

def one_user():
    return auth_register("someone@example.com", "Password1", "John", "Doe")

def two_users():
    ret = [one_user()]
    ret.append(auth_register("someone_else@example.com", "Password1", "Jane", "Lee"))
    return ret

def three_users():
    ret = two_users()
    ret.append(auth_register("someone_again@example.com", "Password1", "Pat", "Smith"))
    return ret

################################################################################

def one_channel(token):
    return channels_create(token, "Channel 1", True)

def two_channels(token):
    ret = [one_channel(token)]
    ret.append(channels_create(token, "Channel 2", True))
    return ret

def one_channel_private(token):
    return channels_create(token, "Channel 1", False)

def two_channels_private(token):
    ret = [one_channel_private(token)]
    ret.append(channels_create(token, "Channel 2", False))

################################################################################

def one_dm(token, other_user):
    return dm_create(token, other_user)

################################################################################

def one_user_one_channel():
    user = one_user()
    return user, one_channel(user["token"])

def two_users_one_channel():
    """Only one user is invited
    """
    users = two_users()
    channel = one_channel(users[0]["token"])

    return users, channel

def one_user_one_channel_private():
    user = one_user()
    return user, one_channel_private(user["token"])

def two_users_one_channel_private():
    users = two_users()
    channel = one_channel_private(users[0]["token"])

    return users, channel