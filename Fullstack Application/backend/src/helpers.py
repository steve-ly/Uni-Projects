import re
import jwt
from flask import make_response
from icalendar import Calendar, Event
from datetime import datetime
import pytz
from flask_mail import Message
from flask import current_app

def email_checker(email):
    """
    Verify that the email is valid
 
    Args: 
        email [String]: string of email being used to sign up
         
    Return: 
        boolean [TRUE] if the email us valid
        boolean [FALSE] if the email us valid
        
    """  
    email_regex = r"^\S+@\S+\.\S+$"
    return re.match(email_regex,email)

def serialise_datetime(dt):
    """
    Serialises a date time string
 
    Args: 
        dt [String]: string of email being used to sign up
         
    Return: 
        Array [date as year month day, hours,minutes,seconds]
        
    """  
    return [dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")]

def response(header, code):
    r = make_response('Response')
    r.headers['customHeader'] = header
    r.status_code = code
    return r


skill_map = {'Skill 1':1, 'Skill 2':2, 'Skill 3':3, 'Skill 4':4, 'Skill 5':5, 'Skill 6':6, 'Skill 7':7, 'Skill 8':8, 'Skill 9':9}

def string_clean(string):
    string = string.replace("[", '')
    string = string.replace("]", '')
    string = string.replace(",\"", ', ')
    string = string.replace("\"", '')
    return string

def string_to_array(string):
    string = string_clean(string)
    prefs = []
    try:
        for a in string.split(', '):
            prefs.append(a)
    except:
        pass
    return prefs

def skills_string_to_int(string):
    string = string_clean(string)
    total = 0
    try:
        for a in string.split(', '):
            total += 1 << (skill_map[a] - 1)
    except:
        pass

    return total

def skills_int_to_string(int):
    skills = ""
    max = len(skill_map)
    for i in range(1, max+1):
        if int & (1 << (i-1)):
            if skills == "":
                skills += f"Skill {i}"
            else:
                skills += f", Skill {i}"
    return skills

def skills_int_to_array(int):
    skills = []
    max = len(skill_map)
    for i in range(1, max+1):
        if int & (1 << (i-1)):
            skills.append(f"Skill {i}")
    return skills


def common_bit_count(integer):
    common = 0
    while (integer):
        common += integer & 1
        integer = integer >> 1
    return common

def create_ical_event(tasks):
    """
    Creates an icalendar object
 
    Args: 
        tasks [ARRAY]: list of TASK Objects from models.py
         
    Return: 
        CAL [ics object]
        
    """  
    cal = Calendar()
    for task in tasks:
        event = Event()
        event.add('SUMMARY', task.name)
        event.add('dtstart', task.start_time)
        event.add('dtend', task.end_time)
        event.add('description', task.description)
        event['uid'] = task.id
        cal.add_component(event)

    return cal.to_ical()

def send_calendar_email(receiver, calendar):
    """
    Sends an email to the user with calendar object
 
    Args: 
        receiver [STR]: email string of user
        calendar [ics]: icalendar object to email         
        
    """  
    msg = Message("You have been added to a task, please see your updated schedule:",
                  recipients=[receiver])
    msg.body = 'OR see the attached calendar event.'
    msg.attach("event.ics", "text/calendar", calendar)

    app = current_app._get_current_object()
    mail = app.extensions['mail']

    with app.app_context():
        mail.send(msg)

def send_task_assignments_email(receivers, tasks):
    """
    Sends an email to conference members of task assignments
 
    Args: 
        receiver [ARRAY[STR]]: an array of email string of users in the conference
        tasks [ARRAY]: list of TASK Objects from models.py
        
    """  
    html_content = "<h1>Task Assignments</h1>"
    html_content += "<table border='1'>"
    html_content += "<tr><th>Task Name</th><th>Assigned To</th><th>Start Date</th><th>End Date</th></tr>"

    for task in tasks:
        html_content += "<tr>"
        html_content += f"<td>{task['task']['name']}</td>"
        accepted_names = ', '.join([user['first_name'] + ' ' + user['last_name'] for user in task['accepted']])
        html_content += f"<td>{accepted_names}</td>"
        html_content += f"<td>{task['task']['start_time']}</td>"
        html_content += f"<td>{task['task']['end_time']}</td>"
        html_content += "</tr>"

    html_content += "</table>"
    msg = Message("Hey Team, here's the current task assignments", recipients=receivers, html=html_content)

    app = current_app._get_current_object()
    mail = app.extensions['mail']
    with app.app_context():
        mail.send(msg)

def send_conference_schedule_email(receivers, calendar):
    """
    Sends an email to all users in a conference with calendar object containing all tasks
 
    Args: 
        receiver [STR]: email string of user
        calendar [ics]: icalendar object to email         
        
    """  
    msg = Message("Organiser has shared the conference check it out in the event schedule tab",
                  recipients=receivers)
    msg.body = 'OR see the attached calendar event.'
    msg.attach("event.ics", "text/calendar", calendar)

    app = current_app._get_current_object()
    mail = app.extensions['mail']

    with app.app_context():
        mail.send(msg)