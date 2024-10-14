"""src > notifications.py

Implements functions for interacting with a notifications, as well as the data 
structures for storing all of them.

Primary Contributors: 
 - Danny Won [z5338486@ad.unsw.edu.au]
     - Notification data structure and data structure helper functions
        - get_new_notification()
        - add_notification()
        - remove_notification()
        - get_notification_by_id()

Minor Contributors:
 - [None]

"""

from .generic_data import GenericData, GenericDataContainer

from . import helpers

class Notification(GenericData):
    """Data object for a notification
    """
    _contained_type_str = "Notification"
    def __init__(self, affected_user: int, ch_id: int, dm_id: int, message: str) -> None:
        """Create a Notification object

        Args:
            affected_user (int): id of user recieving notification
            ch_id (int): id of channel of notification (-1 if in dm)
            dm_id (int): id of dm of notification (-1 if in channel)
            message (str): notification message
        """
        super().__init__()
        self._affected_user = affected_user
        self._ch_id = ch_id
        self._dm_id = dm_id
        self._message = helpers.EncodedString(message)
        
        # Add notification to affected user's notifications
        state.s.users.get(affected_user).add_notification(self.get_id())
        # Add notification to data
        state.s.notifications.add(self)
    
    def update(self, new_message: str):
        """Update the notification message

        Args:
            new_message (str): new message string
        """
        self._message = helpers.EncodedString(new_message)
    
    def remove(self):
        """Remove references to notification from user's data
        """
        state.s.users.get(self._affected_user).remove_notification(self.get_id())
    
    def as_dict(self) -> dict:
        """Get notification data as dictionary

        Returns:
            dict: data
        """
        ret = {}
        
        ret["channel_id"] = self._ch_id
        ret["dm_id"] = self._dm_id
        # Convert encoded message to string before returning
        ret["notification_message"] = str(self._message)
        
        return ret
    
    def get_affected_user(self) -> int:
        """Returns id of user who the notification was sent to

        Returns:
            int: user id
        """
        return self._affected_user

class NotificationContainer(GenericDataContainer):
    """Container for notifications
    """
    def get(self, get_id: int) -> Notification:
        return super().get(get_id)

@helpers.unwrap_token
def notification_get_v1(auth_user_id):
    """Returns the user's most recent 20 notifications

    Args:
        auth_user_id (int): User's unique id
    """
    ret = {
        "notifications": [],
    }


    user_dict = state.s.users.get(auth_user_id)
    for count, notif in enumerate(user_dict.get_notifications()):
        if count == 20:
            break
        
        notif_get = state.s.notifications.get(notif).as_dict()
        ret["notifications"].append(notif_get)
    
    return ret


from . import state

