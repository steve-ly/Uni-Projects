from flask import request, Blueprint, jsonify
import jwt
import datetime
from helpers import email_checker, response, skills_int_to_array, string_to_array
from tokens import conference_id_from_token, token_required, user_from_token
from models import DB, MA,                         \
                   Users, UsersSchema,             \
                   Conferences, ConferencesSchema, \
                   Volunteers, VolunteersSchema,   \
                   Organisers, OrganisersSchema,   \
                   Feedback, Voted  

volunteerlist = Blueprint('volunteerlist',__name__)

# VolunteersInConference(conference id) -> returns an array of dictionaries where each dict is {id: xxx, firstname : xxx, lastname: xxx}
@volunteerlist.route('/GetAllVolunteers', methods=['GET'])
@token_required
def GetAllVolunteers():
    user_curr = user_from_token(request.headers['token'])
    # Get conference_id of the requester
    conference_id = conference_id_from_token(request.headers['token'])
    
    # Get all the volunters from the conference
    volunteers=DB.session.query(Users, Volunteers).select_from(Volunteers).join(Users).filter(Volunteers.conference_id==conference_id)

    vol_list=[]
    for v in volunteers:
        vote = Voted.query.filter_by(user_id=user_curr.id,votee_id=v[0].id,conf_id=conference_id).first()
        if vote:
            hasVoted = True
        else:
            hasVoted = False
        # Get feedback as list
        fb = Feedback.query.filter_by(user_id=v[0].id, anon=True).all()
        fb = [{'name':f.name, 'feedback': f.feedback, 'score': f.score} for f in fb]
        # add to list
        vol_list.append({'Firstname':       v[0].first_name,
                         'Id':              v[0].id,
                         'Lastname':        v[0].last_name, 
                         'Email':           v[0].email,
                         'Username':        v[0].username,
                         'Password':        "",
                         'Manager_score':   v[1].manager_score, 
                         'Attendee_score':  v[1].attendee_score, 
                         'Is_manager':      v[1].manager, 
                         'Availability':     string_to_array(v[1].availability), 
                         'Preferences':     string_to_array(v[1].preferences), 
                         'Skills':          skills_int_to_array(v[1].skills), 
                         'Feedbacklist':    fb,
                         'Specialfeatures': [],
                        'Has_voted': hasVoted})
    vol_list.sort(key=lambda x: x['Manager_score'], reverse=True)
    if vol_list:
        for i, volunteer in enumerate(vol_list):
            if i == 0:
                volunteer['Specialfeatures'] = 'First'
            elif i == 1:
                volunteer['Specialfeatures'] = 'Second'
            elif i == 2:
                volunteer['Specialfeatures'] = 'Third'
            else:
                volunteer['Specialfeatures'] = ''
    return vol_list, 200

# GetConferences() -> array of dicts of {id: xxx, conferecnename: xxxx}
@volunteerlist.route('/GetConferences', methods=['GET'])
def GetConferences():
    all = Conferences.query.all()
    results = [{'id':a.id, 'conferencename': a.name} for a in all]
    return jsonify(results), 200

# VolunteersInConference(conference id) -> returns an array of dictionaries where each dict is {id: xxx, firstname : xxx, lastname: xxx}
@volunteerlist.route('/VolunteersInConference/<conference_id>', methods=['GET'])
def VolunteersInConference(conference_id):
    all=DB.session.query(Users, Volunteers).select_from(Volunteers).join(Users).filter(Volunteers.conference_id==conference_id)
    volunteers = [{'id':v[0].id, 'firstname':v[0].first_name, 'lastname':v[0].last_name} for v in all]
    return jsonify(volunteers), 200

# SubmitFeedback(int volunteer, int score (in a range from 0 to 10), string name, string feedback)
@volunteerlist.route('/SubmitFeedback', methods=['POST'])
def SubmitFeedback():
    user_id  = request.json['user_id']
    name     = request.json['name']
    feedback = request.json['feedback']
    score    = int(request.json['score'])

    # Check username in database
    vol = Volunteers.query.filter_by(user_id=user_id).first()
    
    # Return 400 if volunteer doesn't exist
    if vol is None:
        return response('Volunteer associated with user_id doesn\'t exist', 400)

    # Return 400 if score is outside the valid range
    if score < 0 or score > 10:
        return response('Score outside valid range 0-10', 400)
    
    # Add feedback to database
    feedback = Feedback(user_id, name, feedback, score, True)
    DB.session.add(feedback)
    DB.session.commit()
    
    # Update users attendee score
    scores = Feedback.query.filter_by(user_id=user_id, anon=True).all()
    total_score = 0
    num_scores = 0
    for s in scores:
        total_score += s.score
        num_scores += 1
        
    vol.attendee_score = round(total_score/num_scores)
    DB.session.commit()
    
    return response('OK', 200)

@volunteerlist.route('/ManagerSubmitScore', methods=['POST'])
# TODO: @manager_required
@token_required 
def ManagerSubmitScore(): # ->{"user_id":"",”score":""} @requires_management
    user_id  = request.json['user_id']
    score    = int(request.json['score'])
    token = request.headers['token']
    user_current = user_from_token(token)
    conf_id = conference_id_from_token(token)
    # Check username in database
    vol = Volunteers.query.filter_by(user_id=user_id).first()
    
    # Return 400 if volunteer doesn't exist
    if vol is None:
        return response('Volunteer associated with user_id doesn\'t exist', 400)

    # Return 400 if score is outside the valid range
    if score < 0 or score > 10:
        return response('Score outside valid range 0-10', 400)
    
    vote = Voted.query.filter_by(user_id=user_current.id,votee_id=user_id,conf_id=conf_id).first()
    if vote:
        return response('You have already reviewed this user', 400)
    else:
        new_vote = Voted(user_current.id,user_id,score,conf_id)
        DB.session.add(new_vote)
        DB.session.commit()
    
    # Add feedback to database
    feedback = Feedback(user_id,'', '', score, False)
    DB.session.add(feedback)
    DB.session.commit()
    
    # Update users attendee score
    scores = Feedback.query.filter_by(user_id=user_id, anon=False).all()
    total_score = 0
    num_scores = 0
    for s in scores:
        total_score += s.score
        num_scores += 1
        
    vol.manager_score = round(total_score/num_scores)
    DB.session.commit()
    
    return response('OK', 200)


@volunteerlist.route('/GetTopVolunteers', methods=['GET'])
def GetTopVolunteers():
    conference_id = conference_id_from_token(request.headers['token'])
    volunteers = DB.session.query(Users, Volunteers).select_from(Volunteers).join(Users).filter(Volunteers.conference_id == conference_id)
    scored_volunteers = []
    
    for user, volunteer in volunteers:
        feedback = Feedback.query.filter_by(user_id=user.id, anon=True).all()
        feedback_list = [{'name': f.name, 'feedback': f.feedback, 'score': f.score} for f in feedback]
        vote_count = Voted.query.filter_by(votee_id=user.id, conf_id=conference_id).count()
        if vote_count > 0:
            average_score = volunteer.manager_score / vote_count
        else:
            average_score = volunteer.manager_score
            
        scored_volunteers.append({
            'UserId': user.id,
            'Firstname': user.first_name,
            'Lastname': user.last_name,
            'Email': user.email,
            'Total_score': average_score ,
            'Feedbacklist': feedback_list
        })

    scored_volunteers.sort(key=lambda x: x['Total_score'], reverse=True)
    top_volunteers = scored_volunteers[:3]

    return top_volunteers, 200

