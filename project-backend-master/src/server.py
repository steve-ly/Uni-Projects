import sys
import json
from flask import Flask, request, send_from_directory, send_file
from flask_cors import CORS
from pprint import pprint

from . import consts

from src import config, state, echo, auth_register_v1, auth_login_v1,\
    auth_password_reset_request, auth_password_reset_reset,\
    auth_logout_v1, user_profile_v1, user_profile_setname_v1,\
    user_profile_setemail_v1, user_profile_sethandle_v1,\
    user_list_all_v1, channels_create_v1, channels_list_v1,\
    channels_listall_v1, channel_details_v1, channel_messages_v1,\
    channel_invite_v1, channel_join_v1, channel_leave_v1,\
    channel_addowner_v1, channel_removeowner_v1, message_send_v1,\
    message_remove_v1, message_edit_v1, message_share_v1, dm_create_v1,\
    dm_invite_v1, dm_leave_v1, dm_remove_v1, dm_details_v1, dm_list_v1,\
    dm_messages_v1, dm_message_send_v1, admin_remove_user,\
    admin_permssion_change_v1, notification_get_v1, search_v2, clear_v1,\
    user_stats_v1, dreams_stats_v1, standup_start_v1, standup_active_v1,\
    standup_send_v1, message_pin_v1, message_unpin_v1, message_react_v1,\
    message_unreact_v1, message_send_later_v1, dm_message_send_later_v1,\
    user_profile_uploadphoto_v1

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = json.dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def run_echo():
    data = request.args.get('data')
    ret = echo(data)
    return json.dumps({
        'data': ret
    })

@APP.route("/auth/register/v2", methods=["POST"])
def register():
    data = request.json
    ret = auth_register_v1(data["email"], data["password"], data["name_first"], 
                           data["name_last"])
    return json.dumps(ret)

@APP.route("/auth/login/v2", methods=["POST"])
def login():
    data = request.json
    ret = auth_login_v1(data["email"], data["password"])
    return json.dumps(ret)

@APP.route("/auth/logout/v1", methods=["POST"])
def logout():
    data = request.json
    ret = auth_logout_v1(data["token"])
    return json.dumps(ret)

@APP.route("/auth/passwordreset/request/v1", methods=["POST"])
def request_password_reset():
    data = request.json
    ret = auth_password_reset_request(data["email"])
    return json.dumps(ret)

@APP.route("/auth/passwordreset/reset/v1", methods=["POST"])
def reset_password_reset():
    data = request.json
    ret = auth_password_reset_reset(data["reset_code"],data["new_password"])
    return json.dumps(ret)

@APP.route("/user/profile/v2", methods=["GET"])
def user_profile():
    data = request.args
    ret = user_profile_v1(data["token"], int(data["u_id"]))
    return json.dumps(ret)

@APP.route("/user/profile/setname/v2", methods=["PUT"])
def user_profile_setname():
    data = request.json
    ret = user_profile_setname_v1(data["token"], data["name_first"], data["name_last"])
    return json.dumps(ret)

@APP.route("/user/profile/setemail/v2", methods=["PUT"])
def user_profile_setemail():
    data = request.json
    ret = user_profile_setemail_v1(data["token"], data["email"])
    return json.dumps(ret)

@APP.route("/user/profile/sethandle/v1", methods=["PUT"])
def user_profile_sethandle():
    data = request.json
    ret = user_profile_sethandle_v1(data["token"], data["handle_str"])
    return json.dumps(ret)

@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def user_profile_uploadphoto():
    '''
    POST HTTP method for user_profile_upload.
    '''
    data = request.json
    ret = user_profile_uploadphoto_v1(data['token'], data['img_url'], int(data['x_start']), int(data['y_start']), int(data['x_end']), int(data['y_end']))
    return json.dumps(ret)


@APP.route(f"/static/{consts.STATE_RESOURCE_FOLDER}/<filename>", methods=['GET'])
def get_state_resource(filename):
    """
    Route that serves profile images
    """
    return send_file(f"../{consts.STATE_RESOURCE_FOLDER}/{filename}")

@APP.route(f"/static/{consts.PERM_RESOURCE_FOLDER}/<filename>", methods=['GET'])
def get_permanent_resource(filename):
    """
    Route that serves permanent resources
    """
    return send_file(f"../{consts.PERM_RESOURCE_FOLDER}/{filename}")

@APP.route("/users/all/v1", methods=["GET"])
def user_list_all():
    data = request.args
    ret = user_list_all_v1(data["token"])
    return json.dumps(ret)

@APP.route("/channels/list/v2", methods=["GET"])
def channel_list():
    data = request.args
    ret = channels_list_v1(data["token"])
    return json.dumps(ret)

@APP.route("/channels/listall/v2", methods=["GET"])
def channel_listall():
    data = request.args
    ret = channels_listall_v1(data["token"])
    return json.dumps(ret)

@APP.route("/channels/create/v2", methods=["POST"])
def channel_create():
    data = request.json
    ret = channels_create_v1(data["token"], data["name"], data["is_public"])
    return json.dumps(ret)

@APP.route("/channel/invite/v2", methods=["POST"])
def invite_ch():
    data = request.json
    ret = channel_invite_v1(data["token"], int(data["channel_id"]), int(data["u_id"]))
    return json.dumps(ret)

@APP.route("/channel/details/v2", methods=["GET"])
def channel_details():
    data = request.args
    ret = channel_details_v1(data["token"], int(data["channel_id"]))
    return json.dumps(ret)

@APP.route("/channel/messages/v2", methods=["GET"])
def channel_messages():
    data = request.args
    ret = channel_messages_v1(data["token"], int(data["channel_id"]), int(data["start"]))
    return json.dumps(ret)

@APP.route("/channel/join/v2", methods=["POST"])
def channel_join():
    data = request.json
    ret = channel_join_v1(data["token"], int(data["channel_id"]))
    return json.dumps(ret)

@APP.route("/channel/addowner/v1", methods=["POST"])
def channel_addowner():
    data = request.json
    ret = channel_addowner_v1(data["token"], int(data["channel_id"]), int(data["u_id"]))
    return json.dumps(ret)

@APP.route("/channel/removeowner/v1", methods=["POST"])
def channel_removeowner():
    data = request.json
    ret = channel_removeowner_v1(data["token"], int(data["channel_id"]), int(data["u_id"]))
    return json.dumps(ret)

@APP.route("/channel/leave/v1", methods=["POST"])
def channel_leave():
    data = request.json
    ret = channel_leave_v1(data["token"], int(data["channel_id"]))
    return json.dumps(ret)

@APP.route("/message/send/v2", methods=["POST"])
def message_send():
    data = request.json
    ret = message_send_v1(data["token"], int(data["channel_id"]), data["message"])
    return json.dumps(ret)

@APP.route("/message/edit/v2", methods=["PUT"])
def message_edit():
    data = request.json 
    ret = message_edit_v1(data["token"], int(data["message_id"]), data["message"])
    return json.dumps(ret)

@APP.route("/message/remove/v1", methods=["DELETE"])
def message_remove():
    data = request.json 
    ret = message_remove_v1(data["token"], int(data["message_id"]))
    return json.dumps(ret)

@APP.route("/message/share/v1", methods=["POST"])
def message_share():
    data = request.json
    ret = message_share_v1(data["token"], int(data["og_message_id"]), data["message"],
                           int(data["channel_id"]), int(data["dm_id"]))
    return json.dumps(ret)

@APP.route("/message/pin/v1", methods=["POST"])
def message_pin():
    data = request.json
    ret = message_pin_v1(data["token"], int(data["message_id"]))
    return json.dumps(ret)

@APP.route("/message/unpin/v1", methods=["POST"])
def message_unpin():
    data = request.json
    ret = message_unpin_v1(data["token"], int(data["message_id"]))
    return json.dumps(ret)

@APP.route("/message/react/v1", methods=["POST"])
def message_react():
    data = request.json
    ret = message_react_v1(data["token"], int(data["message_id"]),int(data["react_id"]))
    return json.dumps(ret)

@APP.route("/message/unreact/v1", methods=["POST"])
def message_unreact():
    data = request.json
    ret = message_unreact_v1(data["token"], int(data["message_id"]),int(data["react_id"]))
    return json.dumps(ret)

@APP.route("/message/sendlater/v1", methods=["POST"])
def message_sendlater():
    data = request.json
    ret = message_send_later_v1(data["token"], int(data["channel_id"]),data["message"],int(data["time_sent"]))
    return json.dumps(ret)

@APP.route("/message/sendlaterdm/v1", methods=["POST"])
def message_sendlaterdm():
    data = request.json
    ret = dm_message_send_later_v1(data["token"], int(data["dm_id"]),data["message"],int(data["time_sent"]))
    return json.dumps(ret)

@APP.route("/dm/details/v1", methods=["GET"])
def dm_details():
    data = request.args
    ret = dm_details_v1(data["token"], int(data["dm_id"]))
    return json.dumps(ret)

@APP.route("/dm/list/v1", methods=["GET"])
def dm_list():
    data = request.args
    ret = dm_list_v1(data["token"])
    return json.dumps(ret)

@APP.route("/dm/create/v1", methods=["POST"])
def dm_create():
    data = request.json
    ret = dm_create_v1(data["token"], [int(u_id) for u_id in data["u_ids"]])
    return json.dumps(ret)

@APP.route("/dm/remove/v1", methods=["DELETE"])
def dm_remove():
    data = request.json
    ret = dm_remove_v1(data["token"], int(data["dm_id"]))
    return json.dumps(ret)

@APP.route("/dm/invite/v1", methods=["POST"])
def dm_invite():
    data = request.json
    ret = dm_invite_v1(data["token"], int(data["dm_id"]), int(data["u_id"]))
    return json.dumps(ret)

@APP.route("/dm/leave/v1", methods=["POST"])
def dm_leave():
    data = request.json
    ret = dm_leave_v1(data["token"], int(data["dm_id"]))
    return json.dumps(ret)

@APP.route("/dm/messages/v1", methods=["GET"])
def dm_messages():
    data = request.args
    ret = dm_messages_v1(data["token"], int(data["dm_id"]), int(data["start"]))
    return json.dumps(ret)

@APP.route("/message/senddm/v1", methods=["POST"])
def dm_message_send():
    data = request.json
    ret = dm_message_send_v1(data["token"], int(data["dm_id"]), data["message"])
    return json.dumps(ret)

@APP.route("/standup/start/v1", methods=["POST"])
def standup_start():
    data = request.json
    ret = standup_start_v1(data["token"], int(data["channel_id"]), int(data["length"]))
    return json.dumps(ret)

@APP.route("/standup/active/v1", methods=["GET"])
def standup_active():
    data = request.args
    ret = standup_active_v1(data["token"], int(data["channel_id"]))
    return json.dumps(ret)

@APP.route("/standup/send/v1", methods=["POST"])
def standup_send():
    data = request.json
    ret = standup_send_v1(data["token"], int(data["channel_id"]), data["message"])
    return json.dumps(ret)

@APP.route("/admin/user/remove/v1", methods=["DELETE"])
def remove_user():
    data = request.json
    ret = admin_remove_user(data["token"], int(data["u_id"]))
    return json.dumps(ret)

@APP.route("/admin/userpermission/change/v1", methods=["POST"])
def permission_change():
    data = request.json
    ret = admin_permssion_change_v1(data["token"], int(data["u_id"]), int(data["permission_id"]))
    return json.dumps(ret)

@APP.route("/notifications/get/v1", methods=["GET"])
def notification_get():
    data = request.args
    ret = notification_get_v1(data["token"])
    return json.dumps(ret)

@APP.route("/user/stats/v1", methods=["GET"])
def user_stats():
    data = request.args
    ret = user_stats_v1(data["token"])
    return json.dumps(ret)

@APP.route("/users/stats/v1", methods=["GET"])
def dreams_stats():
    data = request.args
    ret = dreams_stats_v1(data["token"])
    return json.dumps(ret)

@APP.route("/clear/v1", methods=["DELETE"])
def clear():
    clear_v1()
    return json.dumps({})

@APP.route("/search/v2", methods=["GET"])
def search():
    data = request.args
    ret = search_v2(data["token"], data["query_str"])
    return json.dumps(ret)

#
# Main function when acting as a server
#
if __name__ == "__main__":
    
    state.reset_state()
    
    # If running with -d, the server will run in debug mode
    debug_enable = "-d" in sys.argv
    
    # If we're debugging
    if debug_enable:
        # Add the printstate route
        @APP.route("/debug/printstate/v1", methods=["POST"])
        def print_state():
            pprint(state.s)
            return json.dumps({})
        
        # Print the URL map
        print(APP.url_map, "\n")
    
    # If the reset flag is present
    if "-r" not in sys.argv:
        # Load saved data
        print("Loading data...")
        try:
            state.load_state()
            print("Data loaded successfully!")
        except FileNotFoundError:
            print("Data save not found: starting empty")
        except AttributeError:
            print("Data save corrupted: Starting empty")
        finally:
            state.save_state()
    else:
        print("Starting server empty")
        state.save_state()
    
    APP.run(port=config.port, debug=debug_enable) # Do not edit this port
