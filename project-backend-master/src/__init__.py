"""src > __init__.py

Ensures that our files will work properly as a module
We've also made it so that you can get the entire project running in a
serverless mode for manual testing. To do this, launch a Python interpreter
and run the following code:

>>> from src import *

Doing this will allow you to call the front-facing functions, sending data to
them like you would to the web server. Note that the return values will be
stored in a dictionary, rather than as JSON

Primary Contributors: 
 - Miguel Guthridge [z5312085@ad.unsw.edu.au]:
     - imports

Minor Contributors:
 - The unseen deities that rule over GitLab

"""

#from . import config
#from . import auth, channel, channels, echo, error, identifier
#from . import message, other, state, user, notification

from .echo import echo

from .auth import auth_login_v1, auth_register_v1, auth_logout_v1,\
                    auth_password_reset_request, auth_password_reset_reset

from .admin import admin_remove_user,admin_permssion_change_v1


from .user import user_list_all_v1, user_profile_v1, user_profile_setname_v1,\
                    user_profile_sethandle_v1, user_profile_setemail_v1,\
                    user_profile_uploadphoto_v1

from .channels import channels_create_v1, channels_list_v1, channels_listall_v1

from .channel import channel_join_v1, channel_invite_v1, channel_messages_v1,\
                    channel_details_v1, channel_leave_v1, channel_addowner_v1,\
                    channel_removeowner_v1

from .message import message_send_v1, message_edit_v1, message_remove_v1,\
    message_share_v1,message_pin_v1, message_unpin_v1,message_react_v1,\
    message_unreact_v1, message_send_later_v1

from .dm import dm_create_v1, dm_invite_v1, dm_list_v1, dm_details_v1,\
    dm_leave_v1, dm_remove_v1, dm_messages_v1, dm_message_send_v1,dm_message_send_later_v1

from .standup import standup_start_v1, standup_active_v1, standup_send_v1

from .notification import notification_get_v1

from .other import search_v2, clear_v1

from .state import get_state, set_state, reset_state
from .stats import dreams_stats_v1, user_stats_v1

reset_state()
