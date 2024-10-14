"""src > identifier.py

This file contains the necessary functions to generate unique identifiers
for messages, users and channels.
This prevents the need for reused code in those areas.
We would use UUIDs, but we need to use ints :(

Primary Contributors: 
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]

Minor Contributors:
 - [None]

"""

import random

# Number of bits length of the randomly generated ID function
# At 32, this should allow for 2**32 or 4294967296 (4 billion) values
# The server will run out of memory long before we get a duplicate
ID_BIT_LENGTH = 32

def get_new_identifier():
    """Generates a new unique identifier for a channel, user or message.
    It is ensured that the identifier has not been used before.

    Returns:
        int: new identifier
    """
    new_id = 0
    while (new_id in state.s._identifiers):
        new_id = random.getrandbits(ID_BIT_LENGTH)
    
    # 
    # An alternative solution is to consider using the technique 
    # described in this post:
    # https://stackoverflow.com/a/2077264/6335363
    #
    
    # Since we could have anything as the item, let's just
    # use the number of identifiers that have been generated
    state.s._identifiers.add(new_id)
    
    return new_id


from . import state

