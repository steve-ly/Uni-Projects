"""
This file implements wrappers for all the http routes to make
calling them simpler from the tests
"""

from src.helpers import unwrap_token
import requests
import json
from pprint import pprint

from src import config, error

url_loc = config.url

def extract_return(func):
    """Decorator to extract return data of a request and raise error if needed

    Args:
        func (function): function to wrap
    """
    def do_func(*args):

        try:
            data = func(*args)
        except requests.exceptions.ConnectionError:
            raise Exception("Connection Error: is the server running?") from None

        if data.status_code == 403:
            raise error.AccessError("Error 403: Forbidden: " + json.loads(data.text)["message"])
        elif data.status_code == 400:
            raise error.InputError("Error 400: invalid input: " + json.loads(data.text)["message"])

        elif data.status_code == 404:
            raise requests.exceptions.HTTPError("Error 404: Route not found")
        else:
            pprint(data.text)
            return json.loads(data.text)
    
    return do_func

################################################################################

@extract_return
def auth_login(email, password):
    return requests.post(
        f"{url_loc}auth/login/v2", 

        json={
            "email": email,
            "password": password
        }
        )

@extract_return
def auth_register(email, password, name_first, name_last):
    return requests.post(
        f"{url_loc}auth/register/v2",
        json={
            "email": email,
            "password": password,
            "name_first": name_first,
            "name_last": name_last
        }
    )

@extract_return
def auth_logout(token):
    return requests.post(
        f"{url_loc}auth/logout/v1",
        json={
            "token": token
        }
    )

@extract_return
def auth_password_request(email):
    return requests.post(
        f"{url_loc}auth/passwordreset/request/v1",
        json={
            "email": email
        }
    )    

@extract_return
def auth_password_reset(reset_code,new_password):
    return requests.post(
        f"{url_loc}auth/passwordreset/reset/v1",
        json={
            "reset_code": reset_code,
            "new_password": new_password
        }
    )    




################################################################################

@extract_return
def channel_invite(token, channel_id, u_id):
    return requests.post(
        f"{url_loc}channel/invite/v2",
        json={
            "token": token,
            "channel_id": channel_id,
            "u_id": u_id
        }
    )

@extract_return
def channel_details(token, channel_id):
    return requests.get(
        f"{url_loc}channel/details/v2",
        params={
            "token": token,
            "channel_id": channel_id
        }
    )

@extract_return
def channel_messages(token, channel_id, start):
    return requests.get(
        f"{url_loc}channel/messages/v2",
        params={
            "token": token,
            "channel_id": channel_id,
            "start": start
        }
    )

@extract_return
def channel_join(token, channel_id):
    return requests.post(
        f"{url_loc}channel/join/v2",
        json={
            "token": token,
            "channel_id": channel_id
        }
    )

@extract_return
def channel_addowner(token, channel_id, u_id):
    return requests.post(
        f"{url_loc}channel/addowner/v1",
        json={
            "token": token,
            "channel_id": channel_id,
            "u_id": u_id
        }
    )
   
@extract_return 
def channel_removeowner(token, channel_id, u_id):
    return requests.post(
        f"{url_loc}channel/removeowner/v1",
        json={
            "token": token,
            "channel_id": channel_id,
            "u_id": u_id
        }
    )

@extract_return
def channel_leave(token, channel_id):
    return requests.post(
        f"{url_loc}channel/leave/v1",
        json={
            "token": token,
            "channel_id": channel_id
        }
    )

################################################################################

@extract_return
def channels_list(token):
    return requests.get(
        f"{url_loc}channels/list/v2",
        params={
            "token": token
        }
    )

@extract_return
def channels_listall(token):
    return requests.get(
        f"{url_loc}channels/listall/v2",
        params={
            "token": token
        }
    )

@extract_return
def channels_create(token, name, is_public):
    return requests.post(
        f"{url_loc}channels/create/v2",
        json={
            "token": token,
            "name": name,
            "is_public": is_public
        }
    )

################################################################################

@extract_return
def message_send(token, channel_id, message):
    return requests.post(
        f"{url_loc}message/send/v2",
        json={
            "token": token,
            "channel_id": channel_id,
            "message": message
        }
    )

@extract_return
def message_edit(token, message_id, message):
    return requests.put(
        f"{url_loc}message/edit/v2",
        json={
            "token": token,
            "message_id": message_id,
            "message": message
        }
    )
    
@extract_return
def message_remove(token, message_id):
    return requests.delete(
        f"{url_loc}message/remove/v1",
        json={
            "token": token,
            "message_id": message_id
        }
    )

@extract_return
def message_share(token, og_message_id, message, channel_id=-1, dm_id=-1):
    return requests.post(
        f"{url_loc}message/share/v1",
        json={
            "token": token,
            "og_message_id": og_message_id,
            "message": message,
            "channel_id": channel_id,
            "dm_id": dm_id
        }
    )

@extract_return
def message_pin(token, message_id):
    return requests.post(
        f"{url_loc}message/pin/v1",
        json={
            "token": token,
            "message_id": message_id
        }
    )

@extract_return
def message_unpin(token, message_id):
    return requests.post(
        f"{url_loc}message/unpin/v1",
        json={
            "token": token,
            "message_id": message_id
        }
    )


@extract_return
def message_react(token, message_id, react_id):
    return requests.post(
        f"{url_loc}message/react/v1",
        json={
            "token": token,
            "message_id": message_id,
            "react_id": react_id
        }
    )

@extract_return
def message_unreact(token, message_id, react_id):
    return requests.post(
        f"{url_loc}message/unreact/v1",
        json={
            "token": token,
            "message_id": message_id,
            "react_id": react_id   
        }
    )

@extract_return
def message_send_later(token, channel_id, message, time_sent):
    return requests.post(
        f"{url_loc}message/sendlater/v1",
        json={
            "token": token,
            "channel_id": channel_id,
            "message": message,
            "time_sent": time_sent   
        }
    )

@extract_return
def message_send_later_dm(token, dm_id, message, time_sent):
    return requests.post(
        f"{url_loc}message/sendlaterdm/v1",
        json={
            "token": token,
            "dm_id": dm_id,
            "message": message,
            "time_sent": time_sent   
        }
    )


################################################################################

@extract_return
def standup_start(token, channel_id, length):
    return requests.post(
        f"{url_loc}standup/start/v1",
        json={
            "token": token,
            "channel_id": channel_id,
            "length": length
        }
    )

@extract_return
def standup_active(token, channel_id):
    return requests.get(
        f"{url_loc}standup/active/v1",
        params={
            "token": token,
            "channel_id": channel_id
        }
    )

@extract_return
def standup_send(token, channel_id, message):
    return requests.post(
        f"{url_loc}standup/send/v1",
        json={
            "token": token,
            "channel_id": channel_id,
            "message": message
        }
    )

################################################################################

@extract_return
def dm_details(token, dm_id):
    return requests.get(
        f"{url_loc}dm/details/v1",
        params={
            "token": token,
            "dm_id": dm_id
        }
    )

@extract_return
def dm_list(token):
    return requests.get(
        f"{url_loc}dm/list/v1",
        params={
            "token": token
        }
    )

@extract_return
def dm_create(token, u_ids):
    return requests.post(
        f"{url_loc}dm/create/v1",
        json={
            "token": token,
            "u_ids": u_ids
        }
    )

@extract_return
def dm_remove(token, dm_id):
    return requests.delete(
        f"{url_loc}dm/remove/v1",
        json={
            "token": token,
            "dm_id": dm_id
        }
    )

@extract_return
def dm_invite(token, dm_id, u_id):
    return requests.post(
        f"{url_loc}dm/invite/v1",
        json={
            "token": token,
            "dm_id": dm_id,
            "u_id": u_id
        }
    )

@extract_return
def dm_leave(token, dm_id):
    return requests.post(
        f"{url_loc}dm/leave/v1",
        json={
            "token": token,
            "dm_id": dm_id
        }
    )

@extract_return
def dm_messages(token, dm_id, start):
    return requests.get(
        f"{url_loc}dm/messages/v1",
        params={
            "token": token,
            "dm_id": dm_id,
            "start": start
        }
    )

@extract_return
def message_send_dm(token, dm_id, message):
    return requests.post(
        f"{url_loc}message/senddm/v1",
        json={
            "token": token,
            "dm_id": dm_id,
            "message": message
        }
    )

################################################################################

@extract_return
def user_profile(token, u_id):
    return requests.get(
        f"{url_loc}user/profile/v2",
        params={
            "token": token,
            "u_id": u_id
        }
    )

@extract_return
def user_profile_setname(token, name_first, name_last):
    return requests.put(
        f"{url_loc}user/profile/setname/v2",
        json={
            "token": token,
            "name_first": name_first,
            "name_last": name_last
        }
    )

@extract_return
def user_profile_setemail(token, email):
    return requests.put(
        f"{url_loc}user/profile/setemail/v2",
        json={
            "token": token,
            "email": email
        }
    )

@extract_return
def user_profile_sethandle(token, handle_str):
    return requests.put(
        f"{url_loc}user/profile/sethandle/v1",
        json={
            "token": token,
            "handle_str": handle_str
        }
    )

@extract_return
def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    return requests.post(
        f"{url_loc}user/profile/uploadphoto/v1",
        json={
            "token": token,
            "img_url": img_url,
            "x_start": x_start,
            "y_start": y_start,
            "x_end": x_end,
            "y_end": y_end
        } 
    )
################################################################################

@extract_return
def users_all(token):
    return requests.get(
        f"{url_loc}users/all/v1",
        params={
            "token": token
        }
    )

################################################################################

@extract_return
def search(token, query_str):
    return requests.get(
        f"{url_loc}search/v2",
        params={
            "token": token,
            "query_str": query_str
        }
    )

################################################################################

@extract_return
def admin_user_remove(token, u_id):
    return requests.delete(
        f"{url_loc}admin/user/remove/v1",
        json={
            "token": token,
            "u_id": u_id
        }
    )

@extract_return
def admin_userpermission_change(token, u_id, permission_id):
    return requests.post(
        f"{url_loc}admin/userpermission/change/v1",
        json={
            "token": token,
            "u_id": u_id,
            "permission_id": permission_id
        }
    )

################################################################################

@extract_return
def notifications_get(token):
    return requests.get(
        f"{url_loc}notifications/get/v1",
        params={
            "token": token
        }
    )
    
################################################################################

@extract_return
def user_stats(token):
    return requests.get(
        f"{url_loc}user/stats/v1",
        params={
            "token": token
        }
    )

@extract_return
def users_stats(token):
    return requests.get(
        f"{url_loc}users/stats/v1",
        params={
            "token": token
        }
    )

################################################################################

@extract_return
def clear():
    return requests.delete(f"{url_loc}clear/v1")

@extract_return
def print_state():
    return requests.post(f"{url_loc}debug/printstate/v1")

