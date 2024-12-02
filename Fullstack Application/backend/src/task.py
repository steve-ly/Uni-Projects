from flask import request, Blueprint, jsonify
import jwt
import datetime
import bisect 
from helpers import email_checker, response, skills_string_to_int, common_bit_count, string_clean, create_ical_event, send_calendar_email, send_task_assignments_email
from tokens import conference_id_from_token, user_from_token, username_from_token, token_required, volunteer_from_token, requires_management, requires_organiser
from models import DB, MA,                         \
                   Users, users_schema,             \
                   Conferences, ConferencesSchema, \
                   Volunteers, VolunteersSchema,   \
                   Organisers, OrganisersSchema,   \
                   InvalidedTokens, InvalidedTokensSchema,   \
                   Tasks, task_schema, tasks_schema,         \
                   MembersOfTasks, MessageGroup, MessageGroupSchema, MembersOfMessageGroup, \
                   MembersOfMessageGroupSchema, Message, MessageSchema

task = Blueprint('task',__name__)


#TasksAPIs
#ForceJoinTask()
@task.route('/CreateTask', methods=['POST'])
@token_required
@requires_organiser
def CreateTask():
    """
    Makes a new task
 
    Args: 
        name (string) [JSON BODY]:          The name of the task, non-unique
        description (datetime) [JSON BODY]: A description of the task
        start_time (datetime) [JSON BODY]:  The start time of the task
        end_time (datetime) [JSON BODY]:    The end time of the task
        token [HEADER]:                     Requires the token of a logged in organiser
 
    Response:
        200: Successful creation of new task
        400: Name is invalid
            Times are invalid
        403: The token doesn't belong to an organiser
    """
    conference_id      = conference_id_from_token(request.headers['token'])
    name               = request.json['name']
    description        = request.json['description']
    start_time         = request.json['start_time']
    end_time           = request.json['end_time']
    skills_recommended = request.json['skills_recommended']

    if len(name) > 64:
        return {'message':'Name is too long'}, 400

    if end_time < start_time:
        return {'message':'Times are invalid'}, 400

    # encode recommended skills as an integer
    skills_recommended = skills_string_to_int(skills_recommended)
    task = Tasks(conference_id, name, description, start_time, end_time, skills_recommended)
    DB.session.add(task)
    DB.session.commit()

    #Creates task chat
    creator = user_from_token(request.headers['token'])
    message_group = MessageGroup(conference_id, task.id, creator.id, name)
    DB.session.add(message_group)
    DB.session.commit()

    add_owner = MembersOfMessageGroup(creator.id,message_group.id)
    DB.session.add(add_owner)
    DB.session.commit()
    return response('OK', 200)

@task.route('/GetAllTasks', methods=['GET'])
@token_required # ensures user has logged in already by validating token
def GetAllTasks():
    """
    Gets all tasks
 
    Args: 
        token [HEADER]: Requires the token of a logged in user
 
    Response:
        200: A list of all tasks
    """
    
    conference_id = conference_id_from_token(request.headers['token'])
    all = Tasks.query.filter_by(conference_id=conference_id).all()

    tasks=[]
    for t in all:
        id = t.id

        # Returns the requested volunteers
        requested = MembersOfTasks.query.filter_by(task_id=id, approved=False).all()
        requested = DB.session.query(MembersOfTasks, Users).select_from(Users).join(MembersOfTasks).filter(MembersOfTasks.task_id==id, MembersOfTasks.approved==False).all()
        requested = [r[1] for r in requested]
        requested = users_schema.dump(requested)

        # Returns the accepted volunteers
        accepted = MembersOfTasks.query.filter_by(task_id=id, approved=True).all()
        accepted = DB.session.query(MembersOfTasks, Users).select_from(Users).join(MembersOfTasks).filter(MembersOfTasks.task_id==id, MembersOfTasks.approved==True).all()
        accepted = [r[1] for r in accepted]
        accepted = users_schema.dump(accepted)
        tasks.append({"task":t.serialize, "requested":requested, "accepted":accepted})


    return jsonify(tasks), 200

@task.route('/GetMyTasks', methods=['GET'])
@token_required # ensures user has logged in already by validating token
def GetMyTasks():
    """
    Gets a user all tasks they're assigned
 
    Args: 
        token [HEADER]:  Requires the token of a logged in user
 
    Response:
        200: List of user's tasks
    """
    token = request.headers['token']
    user = user_from_token(token)

    tasks = MembersOfTasks.query.filter_by(user_id=user.id).all()
    tasklist = []
    for task in tasks:
        t = Tasks.query.filter_by(id=task.task_id).first()
        if t:
            tasklist.append({"task_id": task.task_id, "name": t.name})

    return jsonify(tasklist), 200 


@task.route('/GetTaskDetails/<task_id>', methods=['GET'])
@token_required # ensures user has logged in already by validating token
def GetTaskDetails(task_id):
    """
    Returns a task and it's associated details
 
    Args: 
        token [HEADER]: Requires the token of a logged in user
 
    Response:
        200: Returns task and it's details
    """
    task = Tasks.query.filter_by(id=task_id).first()
    return jsonify(task.serialize), 200

@task.route('/ForceJoinTask', methods=['POST'])
@token_required
@requires_management
def ForceJoinTask():
    """
    Force assigns user to task
 
    Args: 
        user_id (int) [JSON BODY]:       User_id
        task_id (int) [JSON BODY]:       Task id
        token [HEADER]:                  Requires the token of a logged in organiser
 
    Response:
        200: Successful addition of user to task and associated chat
        403: The token doesn't belong to an organiser or manager
    """
    user_id = request.json['user_id']
    task_id = request.json['task_id']
    approved = True

    mem = MembersOfTasks.query.filter_by(task_id=task_id, user_id=user_id).first()
    if mem:
        mem.approved = True

    else:
        mem = MembersOfTasks(user_id, task_id, approved)
        DB.session.add(mem)

    #add user to task chat
    task_chat = Tasks.query.filter_by(id=task_id).first()
    messagegroup = MessageGroup.query.filter_by(name=task_chat.name,conference_id=task_chat.conference_id).first()
    new_member = MembersOfMessageGroup(user_id,messagegroup.id)
    #notify user
    recepient = Users.query.filter_by(id=user_id).first()
    tasks = Tasks.query.join(MembersOfTasks, Tasks.id == MembersOfTasks.task_id).filter(MembersOfTasks.user_id == user_id, MembersOfTasks.approved == True).all()
    updated_schedule = create_ical_event(tasks)
    send_calendar_email(recepient.email,updated_schedule)
    DB.session.add(new_member)
    DB.session.commit()

    return response('OK', 200)

@task.route('/JoinTask', methods=['POST'])
@token_required
def JoinTask():
    """
    Submits a user's request to join a task
 
    Args: 
        user_id (int) [JSON BODY]:       user id unique
        task_id (int) [JSON BODY]:       task id unique
        token [HEADER]:                  Requires the token of a logged in user
 
    Response:
        200: User submitted request to join task
    """
    user_id       = request.json['user_id']
    task_id = request.json['task_id']
    approved      = False

    mem = MembersOfTasks(user_id, task_id, approved)
    DB.session.add(mem)
    DB.session.commit()
    return response('OK', 200)

@task.route('/ApproveRequest', methods=['POST'])
@token_required
@requires_organiser
def ApproveRequest():
    """
    Approves an existing task join request
 
    Args: 
        user_id (int) [JSON BODY]:       user id - unique
        task_id (int) [JSON BODY]:       task id - unique
        token [HEADER]:                  Requires the token of a logged in organiser
 
    Response:
        200: Successful addition of user to task and associated chat
        403: The token doesn't belong to an organiser
        400: Request does not exist
    """
    user_id = request.json['user_id']
    task_id = request.json['task_id']
    task = Tasks.query.filter_by(id=task_id).first()
    req = MembersOfTasks.query.filter_by(task_id=task_id, user_id=user_id).first()
    if req:
        req.approved = True
        DB.session.commit()
        #add user to task chat
        messagegroup = MessageGroup.query.filter_by(name=task.name,conference_id=task.conference_id).first()
        new_member = MembersOfMessageGroup(user_id,messagegroup.id)
        DB.session.add(new_member)
        DB.session.commit()
        #notify user
        recepient = Users.query.filter_by(id=user_id).first()
        tasks = Tasks.query.join(MembersOfTasks, Tasks.id == MembersOfTasks.task_id).filter(MembersOfTasks.user_id == user_id, MembersOfTasks.approved == True).all()
        updated_schedule = create_ical_event(tasks)
        send_calendar_email(recepient.email,updated_schedule)

        return response('OK', 200)
    else:
        return response('Request for task doesn\'t exist', 400)

@task.route('/ToggleTaskComplete', methods=['POST'])
@token_required
@requires_organiser
def ToggleTaskComplete():
    """
    Toggles whether a task has been completed
 
    Args: 
        task_id (int) [JSON BODY]:       A unique task id
        token [HEADER]:                  Requires the token of a logged in organiser
 
    Response:
        200: Toggles task completeness
        403: The token doesn't belong to an organiser
    """

    task_id = request.json['task_id']
    task = Tasks.query.filter_by(id=task_id).first()
    task.completed = not task.completed
    DB.session.commit()
    return response('OK', 200)

@task.route('/DeleteTask', methods=['DELETE'])
@token_required
@requires_organiser
def del_task():
    """
    Deletes a task
 
    Args: 
        id (int) [JSON BODY]:           id of a task - unique
        token [HEADER]:                  Requires the token of a logged in organiser
 
    Response:
        200: Succesful deletion of task
        403: The task does not exist
    """
    id = request.json['id']

    if Tasks.query.filter_by(id=id).first():
        #delete all user - task pairs
        MembersOfTasks.query.filter_by(task_id=id).delete()

        Tasks.query.filter_by(id=id).delete()
        DB.session.commit()
        return {'message':'Deleted Task'}, 200

    else:
        return {'message':'Task does not exist'}, 403

@task.route('/RemoveVolunteerFromTask', methods=['DELETE'])
@token_required
def RemoveVolunteerFromTask():
    """
    Removes a given volunteer from task. Volunteers can remove themselves. Organisers can remove 
 
    Args: 
        user_id (int) [JSON BODY]:       user id - unique
        task_id (int) [JSON BODY]:       task id - unique
        token [HEADER]:                  Requires the token of a logged in volunteer
 
    Response:
        200: Successful removal of user from task and associated chat
        403: is not an organiser if removing other user from task
            Task DNE
            User DNE
    """
    curr_user = user_from_token(request.headers['token'])
    user_id = request.json['user_id']
    task_id = request.json['task_id']
    if curr_user.id != user_id:
        isOrganiser = Organisers.query.filter_by(user_id=curr_user.id).first()
        if isOrganiser is None:
            return {'message':'You do not have permission for this'}, 403

    if task_id and user_id:
        MembersOfTasks.query.filter_by(task_id=task_id, user_id=user_id).delete()

        # Remove from chat
        mem = MessageGroup.query.filter_by(task_id=task_id).first()
        MembersOfMessageGroup.query.filter_by(user_id=user_id, messagegroup_id=mem.id).delete()
        DB.session.commit()
        return {'message':'Removed volunteer'}, 200
    else:
        if user_id:
            return {'message':'Task does not exist'}, 403
        return {'message':'User does not exist'}, 403
    
@task.route('/GetVolunteersFromTask', methods=['GET'])
@token_required
def GetVolunteersFromTask():
    """
    Gets a list of all volunteers associated with a task
 
    Args: 
        task_id (int) [JSON BODY]:        Task id
        token [HEADER]:                  Requires the token of a logged in user
 
    Response:
        200: Returns list of all volunteers associated with task
    """
    task_id = request.json['task_id']
    vols = MembersOfTasks.query.filter_by(task_id=task_id).all()
    volslist = []
    for vol in vols:
        volslist.append({"user_id": vol.user_id})

    return jsonify(volslist), 200


@task.route('/EditTask', methods=['POST'])
@token_required
@requires_organiser
def EditTask():
    """
    Edits any and all task variables
 
    Args: 
        task_id (int) [JSON BODY]:       task id - required
        token [HEADER]:                  Requires the token of a logged in organiser
        All other variables optional
        name (string) [JSON BODY]:
        description (string) [JSON BODY]:
        start_time (date_time) [JSON BODY]:
        end_time (date_time) [JSON BODY]:
        skills recommended (string) [JSON BODY]:
 
    Response:
        200: Successful addition of user to task and associated chat
        403: The token doesn't belong to an organiser
    """
    task_id = request.json['task_id']

    # Fetch task
    task = Tasks.query.filter_by(id=task_id).first()
    messagegroup = MessageGroup.query.filter_by(name=task.name,conference_id=task.conference_id).first()
    if not task:
        return response('Task doesn\'t exist', 403)
    if not messagegroup:
        return response('msg\'t exist', 403)

    # Change name if provided
    try:
        name = request.json['name']
        if name:
            task.name = name
            messagegroup.name = name
    except:
        pass

    # Change description if provided
    try:
        description = request.json['description']
        if description:
            task.description = description
    except:
        pass

    # Change start time if provided
    try:
        start_time = request.json['start_time']
        if start_time:
            task.start_time = start_time
    except:
        pass

    # Change end time if provided
    try:
        end_time = request.json['end_time']
        if end_time:
            task.end_time = end_time
    except:
        pass

    # Change suggested skills if provided
    try:
        skills_recommended = request.json['skills_recommended']
        if skills_recommended:
            skills_recommended = skills_string_to_int(skills_recommended)
            task.skills_recommended = skills_recommended
    except:
        pass
    DB.session.commit()
    return task.serialize, 200

@task.route('/GetPreferredTasks', methods=['GET'])
@token_required
def GetPreferredTasks():

    """
    Gets a list of tasks for a voluinteer based on their skills
 
    Args: 
        token [HEADER]:                  Requires the token of a logged in user
 
    Response:
        200: Returns list of aof tasks for a voluinteer based on their skills
    """
    volunteer = volunteer_from_token(request.headers['token'])
    conference_id = conference_id_from_token(request.headers['token'])

    # Get all tasks
    all = Tasks.query.filter_by(conference_id=conference_id).all()

    preferred_tasks = []
    for task in all:
        if volunteer.skills & task.skills_recommended:
            matches=common_bit_count(volunteer.skills & task.skills_recommended)
            # Sort into preferred tasks using
            preferred_tasks.append({'task':task, 'matches':matches})

    # serialise results
    results=[]
    for t in sorted(preferred_tasks, key=lambda d: d['matches'], reverse=True):
        id = t['task'].id

        # Returns the requested volunteers
        requested = MembersOfTasks.query.filter_by(task_id=id, approved=False).all()
        requested = DB.session.query(MembersOfTasks, Users).select_from(Users).join(MembersOfTasks).filter(MembersOfTasks.task_id==id, MembersOfTasks.approved==False).all()
        requested = [r[1] for r in requested]
        requested = users_schema.dump(requested)

        # Returns the accepted volunteers
        accepted = MembersOfTasks.query.filter_by(task_id=id, approved=True).all()
        accepted = DB.session.query(MembersOfTasks, Users).select_from(Users).join(MembersOfTasks).filter(MembersOfTasks.task_id==id, MembersOfTasks.approved==True).all()
        accepted = [r[1] for r in accepted]
        accepted = users_schema.dump(accepted)
        results.append({"task":t['task'].serialize, "requested":requested, "accepted":accepted})

    return results, 200

@task.route('/GetAvailableTasks', methods=['GET'])
@token_required
def GetAvailableTasks():
    """
    Gets a list of tasks that fit in a volunteers availability
 
    Args: 
        token [HEADER]:                  Requires the token of a logged in user
 
    Response:
        200: Returns list of aof tasks for a voluinteer based on their skills
        403: No availability provided
    """
    
    volunteer = volunteer_from_token(request.headers['token'])
    conference_id = conference_id_from_token(request.headers['token'])

    # Get all tasks
    all = Tasks.query.filter_by(conference_id=conference_id).all()

    if volunteer.availability == "":
        return {'message':'No availability provided'}, 403

    dates = []
    string = string_clean(volunteer.availability)
    if string != "":
        for d in string.split(', '):
            day, month, year = d.split('-')
            dates.append(datetime.datetime(int(year), int(month), int(day)))

    available_tasks = []
    for task in all:
        for d in dates:
            if task.start_time <= d <= task.end_time:
                available_tasks.append(task.serialize)
                break

    # serialise results
    results=[]
    for t in available_tasks:
        id = t.id

        # Returns the requested volunteers
        requested = MembersOfTasks.query.filter_by(task_id=id, approved=False).all()
        requested = DB.session.query(MembersOfTasks, Users).select_from(Users).join(MembersOfTasks).filter(MembersOfTasks.task_id==id, MembersOfTasks.approved==False).all()
        requested = [r[1] for r in requested]
        requested = users_schema.dump(requested)

        # Returns the accepted volunteers
        accepted = MembersOfTasks.query.filter_by(task_id=id, approved=True).all()
        accepted = DB.session.query(MembersOfTasks, Users).select_from(Users).join(MembersOfTasks).filter(MembersOfTasks.task_id==id, MembersOfTasks.approved==True).all()
        accepted = [r[1] for r in accepted]
        accepted = users_schema.dump(accepted)
        results.append({"task":t.serialize, "requested":requested, "accepted":accepted})

    return available_tasks, 200

@task.route('/GetBestTasks', methods=['GET'])
@token_required
def GetBestTasks():
    """
    Gets a list of tasks for a voluinteer based on their skills
 
    Args: 
        token [HEADER]:                  Requires the token of a logged in user
 
    Response:
        200: Returns list of aof tasks for a voluinteer based on their skills
        403: No availability provided
    """
    volunteer = volunteer_from_token(request.headers['token'])
    conference_id = conference_id_from_token(request.headers['token'])

    # Get all tasks
    all = Tasks.query.filter_by(conference_id=conference_id).all()

    if volunteer.availability == "":
        return {'message':'No availability provided'}, 403

    dates = []
    string = string_clean(volunteer.availability)
    if string != "":
        for d in string.split(', '):
            day, month, year = d.split('-')
            dates.append(datetime.datetime(int(year), int(month), int(day)))

    available_tasks = []
    for task in all:
        for d in dates:
            if task.start_time <= d <= task.end_time:
                available_tasks.append(task)
                break

    preferred_tasks = []
    for task in available_tasks:
        matches=common_bit_count(volunteer.skills & task.skills_recommended)
        # Sort into preferred tasks using
        preferred_tasks.append({'task':task, 'matches':matches})

    # serialise results
    results=[]
    for t in sorted(preferred_tasks, key=lambda d: d['matches'], reverse=True):
        id = t['task'].id

        # Returns the requested volunteers
        requested = MembersOfTasks.query.filter_by(task_id=id, approved=False).all()
        requested = DB.session.query(MembersOfTasks, Users).select_from(Users).join(MembersOfTasks).filter(MembersOfTasks.task_id==id, MembersOfTasks.approved==False).all()
        requested = [r[1] for r in requested]
        requested = users_schema.dump(requested)

        # Returns the accepted volunteers
        accepted = MembersOfTasks.query.filter_by(task_id=id, approved=True).all()
        accepted = DB.session.query(MembersOfTasks, Users).select_from(Users).join(MembersOfTasks).filter(MembersOfTasks.task_id==id, MembersOfTasks.approved==True).all()
        accepted = [r[1] for r in accepted]
        accepted = users_schema.dump(accepted)
        results.append({"task":t['task'].serialize, "requested":requested, "accepted":accepted})

    return results, 200




@task.route('/ShareTaskAssignment', methods=['POST'])
@token_required
def ShareTasksAssignment():
    """
    Emails assigned volunteers regarding a task
 
    Args: 
        task_id (int) [TOKEN]           task identification
        token [HEADER]:                  Requires the token of a logged in user
 
    Response:
        200: Emails all volunteers in a given task about the task
        403: No availability provided
    """
    conference_id = conference_id_from_token(request.headers['token'])
    all = Tasks.query.filter_by(conference_id=conference_id).all()
    tasks=[]
    for t in all:
        id = t.id
        # Returns the accepted volunteers
        accepted = MembersOfTasks.query.filter_by(task_id=id, approved=True).all()
        accepted = DB.session.query(MembersOfTasks, Users).select_from(Users).join(MembersOfTasks).filter(MembersOfTasks.task_id==id, MembersOfTasks.approved==True).all()
        accepted = [r[1] for r in accepted]
        accepted = users_schema.dump(accepted)
        tasks.append({"task":t.serialize, "accepted":accepted})

    volunteer_ids = Volunteers.query.filter_by(conference_id=conference_id).all()
    volunteer_ids = [v.user_id for v in volunteer_ids]
    

    organiser_ids = Organisers.query.filter_by(conference_id=conference_id).all()
    organiser_ids = [o.user_id for o in organiser_ids]

    all_user_ids = list(volunteer_ids + organiser_ids)

    users = Users.query.filter(Users.id.in_(all_user_ids)).all()
    emails = [user.email for user in users]
    send_task_assignments_email(emails, tasks)

    return jsonify({'message': 'Task assignments shared successfully.'}), 200

