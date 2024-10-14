"""
This file contains all the constants, so that we don't need to scour around
random places looking for them.

"""

import re
from flask import url_for

SECRET = "Some complicated secret that nobody can easily reverse hash"

DREAMS_RESET_PASS_EMAIL = "requestsdreamsdori@gmail.com"
PASSWORD_TO_DREAMS_RESET_ACCOUNT = "dorito1@"

class PERMISSION_LEVEL:
    ADMIN = 1
    MEMBER = 2
    LIST = [ADMIN, MEMBER]

# Regular expression for valid emails
# See https://stackoverflow.com/questions/201323/how-to-validate-an-email-address-using-a-regular-expression
# Note that the provided regular expression didn't work for emails with more 
# than one dot after the @ symbol
# Yes I know I'd love to split this into multiple lines too but apparently
# that's too much for poor old regular expressions
EMAIL_REGEX = re.compile(r"""^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])+$""")

PASSWORD_MIN_LEN = 6

NAME_MIN_LEN = 1
NAME_MAX_LEN = 50

HANDLE_MIN_LEN = 3
HANDLE_MAX_LEN = 20

REMOVED_USER_HANDLE = "removed_user"
REMOVED_USER_MESSAGE = "Removed user"
REMOVED_USER_NAME_FIRST = "Removed"
REMOVED_USER_NAME_LAST = "User"

MESSAGE_MAX_LEN = 1000

WHITESPACE_CHARS = [" ", "\n", "\t"]

REMOVED_MESSAGE_STR = "[Message deleted]"

VALID_REACT_IDS = [1]

STATE_FILE = "state.pickle"
STATE_RESOURCE_FOLDER = "state_resources"

PERM_RESOURCE_FOLDER = "perm_resources"

DEFAULT_PROFILE_IMG =f"{PERM_RESOURCE_FOLDER}/profile_default.jpg"
