from flask import request, Blueprint, jsonify
import jwt
import datetime
from helpers import email_checker, response
from tokens import conference_id_from_token, user_from_token, username_from_token, token_required, requires_management, requires_organiser, is_management_or_organiser, is_organiser
from models import DB, MA,                         \
                   Users, UsersSchema,             \
                   Conferences, ConferencesSchema, \
                   Volunteers, VolunteersSchema,   \
                   Organisers, OrganisersSchema,   \
                   InvalidedTokens, InvalidedTokensSchema,   \
                   MessageGroup, MessageGroupSchema, MembersOfMessageGroup,         \
                   MembersOfMessageGroupSchema, Message, MessageSchema
                   
message = Blueprint('message',__name__)

#creates message group and adds the owner to it
@message.route('/CreateMessageGroup', methods=['POST'])
@token_required
@requires_organiser
def create_message_group():
    """
    creates a message group
 
    Args: 
        token [HEADER]: Requires the token of a logged in user       
        name [BODY]: Task that attendance is being acknowledged
    Response:
        200: Success
        400: Group name is used in this conference
             Token is invalidated
    """
    name = request.json['name']
    token = request.headers['token']
    user = Users.query.filter_by(username=username_from_token(token)['username']).first()
    existing_group = MessageGroup.query.filter_by(name=name,conference_id=conference_id_from_token(token)).first()
    if existing_group:
        return jsonify({"error": "Group name is used in this conference"}), 400
    message_group = MessageGroup(conference_id_from_token(token), user.id, name)
    DB.session.add(message_group)
    DB.session.commit()
    add_owner = MembersOfMessageGroup(user.id,message_group.id)
    DB.session.add(add_owner)
    DB.session.commit()
    return jsonify({"message": "Success"}), 200

#gets all members in group 
@message.route('/GetMembers', methods=['GET'])
@token_required
def get_message_group_member():
    """
    returns all members of a group chat
 
    Args: 
        token [HEADER]: Requires the token of a logged in user       
        groupid [HEADER]: Group id of the group chat 
    Response:
        200: Returns list of all members as a list of dicts as {user_id,messagegroup_id}
        400: Token is invalidated
    """
    group_id = request.headers['groupid']
    message_group = MessageGroup.query.filter_by(id=group_id).first()
    members = MembersOfMessageGroup.query.filter_by(messagegroup_id=group_id).all()
    member_list = []
    for member in members:
        member_data = {
            "user_id": member.user_id,
            "messagegroup_id": member.messagegroup_id
        }
        member_list.append(member_data)

    return jsonify({"members": member_list}), 200

#gets all chats belonging to user
@message.route('/GetChats', methods=['GET'])
@token_required
def get_chats():
    """
    returns the group chats current logged in user is apart of
 
    Args: 
        token [HEADER]: Requires the token of a logged in user       
    Response:
        200: Returns list of all chats as a dictionary of format {id,name}
        400: Token is invalidated
    """
    token = request.headers['token']
    user = Users.query.filter_by(username=username_from_token(token)['username']).first()
    chats = MembersOfMessageGroup.query.filter_by(user_id=user.id).all()
    chats_list = []
    for chat in chats:
        chat_group = MessageGroup.query.filter_by(id=chat.messagegroup_id).first()
        total_messages = Message.query.filter_by(group_id=chat.messagegroup_id).count()
        chat_data = {
            "id": chat_group.id,
            "name": chat_group.name,
            "total_messages": total_messages
        }
        chats_list.append(chat_data)

    return jsonify({"chats": chats_list}), 200

#gets all message in a chat
@message.route('/GetMessages', methods=['GET'])
@token_required
def get_messages():
    """
    returns the messages in a chat
 
    Args: 
        token [HEADER]: Requires the token of a logged in user   
        groupid [HEADER]: Group id of the group chat     
    Response:
        200: Returns list of all messages as a dictionary of format {sender_id,username,content,time_send}
        400: group_id header not provided
             Token is invalidated
    """
    group_id = request.headers['groupid']
    if not group_id:
        return jsonify({"error": "group_id header not provided"}), 400
    messages = Message.query.filter_by(group_id=group_id).all()
    message_list = []
    for message in messages:
        user = Users.query.filter_by(id=message.user_id).first()
        message_data = {
            "sender_id": message.user_id,
            "username":user.username,
            "content": message.content,
            "time_send": message.timestamp
        }
        message_list.append(message_data)

    return jsonify({"messages": message_list}), 200

#add user to chat
@message.route('/AddUserToChat', methods=['POST'])
@token_required
#TODO not sure required perm level
def add_to_chat():
    """
    Adds a user to a group chat
 
    Args: 
        token [HEADER]: Requires the token of a logged in user   
        group_id [BODY]: Group id of the group chat
        user_id [BODY]: User id of user being added to the group chat     
    Response:
        200: User added to the group
        400: User does not exists
             You do not have permission to add users to this chat
             User is already a member of the group
             Token is invalidated
    """
    group_id = request.json['group_id']
    user_id = request.json['user_id']
    token = request.headers['token']
    user = Users.query.filter_by(id=user_id).first()
    owner = Users.query.filter_by(username=username_from_token(token)['username']).first()
    message_group = MessageGroup.query.filter_by(id=group_id).first()
    existing_member = MembersOfMessageGroup.query.filter_by(user_id=user.id, messagegroup_id=group_id).first()
    if user is None:
        return jsonify({"message": "User does not exists"}), 400 
    if owner.id != message_group.owner_id:
        return jsonify({"message": "You do not have permission to add users to this chat"}), 400 
    if existing_member:
        return jsonify({"message": "User is already a member of the group"}), 400
    new_member = MembersOfMessageGroup(user.id,group_id)
    DB.session.add(new_member)
    DB.session.commit()
    return jsonify({"message": "User added to the group"}), 200

#send msg -> How do we update the front end? tickers to update?
@message.route('/SendMessage', methods=['POST'])
@token_required
def send_message():
    """
    Sends a message into the group chat
 
    Args: 
        token [HEADER]: Requires the token of a logged in user   
        group_id [BODY]: Group id of the group chat
        content [BODY]: User id of user being added to the group chat
        timesent [BODY]: Timestamp of when the user sent the message     
    Response:
        200: Message Sent
        400: Token is invalidated
    """
    group_id = request.json['group_id']
    message_to_send = request.json['content']
    token = request.headers['token']
    sent_time = request.json['timesent']
    user = Users.query.filter_by(username=username_from_token(token)['username']).first()
    
    new_message = Message(group_id, user.id, message_to_send, sent_time)
    DB.session.add(new_message)
    DB.session.commit()
    return jsonify({"message": "Message Sent"}), 200


    