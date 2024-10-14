"""src > echo.py

Returns whatever you send it, unless you send it "echo"

Primary Contributors: 
 - The unseen deities that rule over GitLab

Minor Contributors:
 - [None]

"""

from src.error import InputError

def echo(value):
    if value == 'echo':
        raise InputError(description='Input cannot be echo')
    return value
