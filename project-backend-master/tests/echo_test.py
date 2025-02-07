"""tests > echo_test.py

Provides tests for src > echo.py

Primary Contributors: 
 - The unseen deities that rule over GitLab

Minor Contributors:
 - [None]

"""

import pytest

from src.echo import echo
from src.error import InputError


def test_echo():
    assert echo("1") == "1", "1 == 1"
    assert echo("abc") == "abc", "abc == abc"
    assert echo("trump") == "trump", "trump == trump"


def test_echo_except():
    with pytest.raises(InputError):
        assert echo("echo")
