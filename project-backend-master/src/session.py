
from . import consts
from .error import AccessError, InputError
from .generic_data import GenericData, GenericDataContainer

import jwt

class Session(GenericData):
    """Maps a session ID to a user ID
    """
    _contained_type_str = "Session"
    def __init__(self, owner_id: int) -> None:
        """Create a session

        Args:
            owner_id (int): user id of session owner
        """
        super().__init__()
        self._owner = owner_id
        
        # Add session to owner
        state.s.users.get(self.get_owner()).add_session(self.get_id())
        
        # Add to data
        state.s.sessions.add(self)

    def remove(self):
        """Rempve all references to session
        """
        state.s.users.get(self.get_owner()).remove_session(self.get_id())

    def get_owner(self) -> int:
        """Returns session owner's id

        Returns:
            int: owner id
        """
        return self._owner

    def get_as_token(self) -> str:
        """Returns the session as an encrypted JWT token

        Returns:
            str: token
        """
        return str(jwt.encode({"session": self.get_id()}, consts.SECRET, algorithm='HS256'))

class SessionContainer(GenericDataContainer):
    """Container for sessions
    """
    def get(self, get_id: int) -> Session:
        return super().get(get_id)

def get_session_by_token(token):
    """Get session object from token

    Args:
        token (str): token

    Returns:
        Session: session
    """
    
    # Decode session token
    try:
        session_id = jwt.decode(token, consts.SECRET, algorithms=["HS256"])["session"]
    except jwt.exceptions.DecodeError:
        raise AccessError(description="Unable to decode token") from None
    
    # Get session data
    try:
        return state.s.sessions.get(session_id)
    except InputError:
        raise AccessError(description="Session ID invalid. Did you log out?") from None

from . import state
