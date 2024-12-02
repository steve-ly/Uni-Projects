from flask import request, Blueprint, jsonify
import jwt
from datetime import datetime

import bisect 
from helpers import email_checker, response, skills_string_to_int, common_bit_count, string_clean, create_ical_event, send_calendar_email, send_task_assignments_email
from tokens import conference_id_from_token, user_from_token, username_from_token, token_required, volunteer_from_token
from models import DB, MA,                         \
                   Users, users_schema,             \
                   Conferences, ConferencesSchema, \
                   Volunteers, VolunteersSchema,   \
                   Organisers, OrganisersSchema,   \
                   InvalidedTokens, InvalidedTokensSchema,   \
                   Tasks, task_schema, tasks_schema,         \
                   MembersOfTasks, MessageGroup, MessageGroupSchema, MembersOfMessageGroup, \
                   MembersOfMessageGroupSchema, Message, MessageSchema, Attendance, attendance_schema

attendance = Blueprint('attendance',__name__)

#assumes user is approved for task already
@attendance.route('/LogInAttendance', methods=['POST'])
@token_required
def log_attendance():
    """
    Logs user in task for attendance acknowledgement
 
    Args: 
        token [HEADER]: Requires the token of a logged in organiser
        task_id [BODY]: Task id of task user is trying to log attendance
        date [BODY]: Date which the user has logged attendance in format '%Y-%m-%d-%H-%M-%S'
        
    Response:
        200: message 'Attendance logged successfully.'
        400: User Already logged attendance
             Token is invalidated
    """
    token = request.headers['token']
    task_id = request.json['task_id']
    user = user_from_token(token)
    conf_id = conference_id_from_token(token)
    date = request.json['date']
    attendance = Attendance.query.filter_by(task_id=task_id, user_id=user.id, conf_id=conf_id).first()
    if attendance:
        return jsonify({'message': 'User Already logged attendance.'}), 400
    else:
        log = Attendance(task_id, user.id, user.username, conf_id,datetime.strptime(date, '%Y-%m-%d-%H-%M-%S'))
        DB.session.add(log)
        DB.session.commit()
        return jsonify({'message': 'Attendance logged successfully.'}), 200


#assumes user is approved for task already
@attendance.route('/LogOutAttendance', methods=['POST'])
@token_required
def log_out_attendance():
    """
    Logs user out as finishing shift for a task and will calculate hours worked
 
    Args: 
        token [HEADER]: Requires the token of a logged in organiser
        task_id [BODY]: Task id of task user is trying to log attendance
        date [BODY]: Date which the user has logged attendance in format '%Y-%m-%d-%H-%M-%S'
        
    Response:
        200: message 'Attendance logged out successfully.'
        400: User was logged out already
            Token is invalidated
    """
    token = request.headers['token']
    task_id = request.json['task_id']
    user = user_from_token(token)
    conf_id = conference_id_from_token(token)
    date = request.json['date']
    attendance = Attendance.query.filter_by(task_id=task_id, user_id=user.id, conf_id=conf_id).first()
    if attendance:
        if attendance.date_out:
            return jsonify({'message': 'User was logged out already'}), 400
        else:
            attendance.date_out = datetime.strptime(date, '%Y-%m-%d-%H-%M-%S')
            time_passed = attendance.date_out - attendance.date_in
            hours = time_passed.total_seconds() / 3600
            attendance.hours = hours
            DB.session.commit()
            return jsonify({'message': 'Attendance logged out successfully.'}), 200
    else:
        return jsonify({'message': 'User was logged out already'}), 400

#gets all attendance logs for a conference, only gets complete log.
@attendance.route('/GetAllAttendance', methods=['GET'])
@token_required
def get_all_attendance():
    """
    Gets all attendance logs that has been logged for the conference
 
    Args: 
        token [HEADER]: Requires the token of a logged in organiser        
    Response:
        200: a dump of all Attendance objects in conference
        400: Token is invalidated
    """
    token = request.headers['token']
    conf_id = conference_id_from_token(token)
    attendance_records = Attendance.query.filter_by(conf_id=conf_id).filter(Attendance.date_out.isnot(None)).all()
    result = attendance_schema.dump(attendance_records)
    return jsonify(result), 200

#gets all attendance logs for a task -> task id should be in headers
@attendance.route('/GetTaskAttendance', methods=['GET'])
@token_required
def get_task_attendance():
    """
    Gets all attendance logs that has been logged for the task
 
    Args: 
        token [HEADER]: Requires the token of a logged in organiser       
        taskid [HEADER]: Task that attendance is being retreived for 
    Response:
        200: a dump of all Attendance objects in the task
        400: Token is invalidated
    """
    token = request.headers['token']
    task_id = request.headers['taskid']
    conf_id = conference_id_from_token(token)
    attendance_records = Attendance.query.filter_by(conf_id=conf_id, task_id = task_id).filter(Attendance.date_out.isnot(None)).all()
    result = attendance_schema.dump(attendance_records)
    return jsonify(result), 200

#toggles approval and assumes user is organiser
@attendance.route('/ApproveAttendance', methods=['PUT'])
@token_required
def approve_attendance():
    """
    Toggles approval boolean in attendance sheet
 
    Args: 
        token [HEADER]: Requires the token of a logged in organiser       
        task_id [BODY]: Task that attendance is being acknowledged
        user_id [BODY]: Id of user that is getting attendance approved/disapproved
    Response:
        200: Success
        400: Log Not found
             Token is invalidated
    """
    token = request.headers['token']
    task_id = request.json['task_id']
    user_id = request.json['user_id']
    conf_id = conference_id_from_token(token)
    attendance = Attendance.query.filter_by(task_id=task_id, user_id=user_id, conf_id=conf_id).first()
    if attendance:
        if attendance.validated:
            attendance.validated = False
        else:
            attendance.validated = True
        DB.session.commit()
        return jsonify({'message': 'Success'}), 200
    else:
        return jsonify({'message': 'Log Not found'}), 400