from src import helpers, consts
from src.error import InputError, AccessError

@helpers.unwrap_token
@helpers.save_data
def admin_remove_user(auth_user_id, u_id):

    """Removes user from database and replace all messages with "Removed user" and replace handle with "Removed user" 
       
        Arguments:
            <token> (string) token of user in session
            <u_id> (int) user id of user being removed
        Exceptions:
            <InputError> - Returns an Input error if the user being removed is the only owner
            <InputError> - Returns an Input error if the u_id does not exists
            <AccessError> - Returns an Access error if the authorised user is not an owner
            <AccessError> - Returns an Access error if the token is invalid

    """
    user_logged_in = state.s.users.get(auth_user_id)
    
    user_removed = state.s.users.get(u_id)
    
    # Can't remove bots
    if user_removed.is_bot():
        raise InputError(description="Bots cannot be removed")

    number_owners = 0
    for member in state.s.users:
        if member.is_admin():
            number_owners += 1


    if not user_logged_in.is_admin():
        raise AccessError(description="You don't have admin permissions")
    
    if number_owners == 1 and user_removed.is_admin():
        raise InputError(description="You are currently the only owner")
    
    user_removed.remove()

    return {}

@helpers.unwrap_token
@helpers.save_data
def admin_permssion_change_v1(auth_user_id, u_id, permission_id):
    """Change users admin permissions
       
        Arguments:
            <token> (string) token of user in session
            <u_id> (int) user id of user whose permission is being changed
            <permission_id> (int) the permission that the user is being changed to
        Exceptions:
            <InputError> - Returns an Input error the permission id does not refer to a valid id
            <InputError> - Returns an Input error if the u_id does not exists
            <InputError> - Returns an Input error if the current user in session is the only owner and is trying to change their own permission to member id.
            <AccessError> - Returns an Access error if the authorised user is not an owner
    """
    admin_user = state.s.users.get(auth_user_id)
    target_user = state.s.users.get(u_id)

    # Check for valid permission IDs
    if permission_id not in consts.PERMISSION_LEVEL.LIST:
        raise InputError(description=f"Permission ID ({permission_id}) isn't a valid permission level")
    
    # Count the number of owners
    number_owners = sum([usr.is_admin() for usr in state.s.users])

    # Check owner is an admin
    if not admin_user.is_admin():
        raise AccessError(description="You don't have admin permissions") 
    
    # If user is the only admin and they're trying to make themselves a member
    if target_user.is_admin() and number_owners == 1\
        and permission_id == consts.PERMISSION_LEVEL.MEMBER:
            raise InputError(description="You are currently the only owner")
    
    if permission_id == consts.PERMISSION_LEVEL.ADMIN:
        target_user.set_admin(True)
    else:
        target_user.set_admin(False)

    return {}

from . import state

