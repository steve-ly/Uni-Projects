import React, { useContext, useState, useEffect } from 'react';
import { LogoutAndDashboardIcons, TopTitle, StandardButton } from './Containers';
import Scheduler, { SchedulerData, ViewTypes, DATE_FORMAT } from 'react-big-scheduler';
import 'react-big-scheduler/lib/css/style.css';
import moment from 'moment';
import { DragDropContext } from 'react-dnd';
import HTML5Backend from 'react-dnd-html5-backend';
import { AuthContext } from './AuthContext';
import config from '../config.json';
import '../style/pagespecific/Schedule.css';
import { ShareConference, GetUserRole, GetUserDetailsSimple, ShareTask } from './HTTP/User';
import { UseConfirmation } from './ConfirmationElement';

const BACKEND_PORT = config.BACKEND_PORT;

const SchedulePage = () => {
  setTimeout(function () {
    window.dispatchEvent(new Event('resize'));
  }, 1000); // The fact that resizing after 0.8s fixes the issue is why frontend is terrible. 0.1 might be too short and hasnt loaded yet

  const OpenConfirmation = UseConfirmation();
  const { token } = useContext(AuthContext);
  const [userRole, setUserRole] = useState(null);
  const [userName, setuserName] = useState('none');

  useEffect(() => {
    GetUserRole(token, setUserRole)
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      console.log('AAAAAAAAAAAAAAAAA');
      const deets = await GetUserDetailsSimple(token);
      console.log('deets: ', deets);
      setuserName(deets.user_id);
    };

    fetchData();
  }, []);

  const SchedulerDataReal = new SchedulerData(new moment().format(DATE_FORMAT), ViewTypes.Week, false, false, { // eslint-disable-line new-cap
    eventItemHeight: '8vh',
    eventItemLineHeight: 120,
    creatable: false,
    schedulerWidth: '90%',
    schedulerMaxHeight: 0,
    tableHeaderHeight: '5vh',
    views: [],
    movable: false,
  });
  moment.locale('en-au');
  SchedulerDataReal.setLocaleMoment(moment);

  const resources = [
    {
      id: 'r1',
      name: 'Tasks',
    }
  ];

  SchedulerDataReal.setResources(resources);
  const events = [];
  fetch(`http://localhost:${BACKEND_PORT}/GetAllTasks`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token
    }
  })
    .then(response => {
      if (!response.ok) {
        window.alert('Invalid conference name');
        throw new Error('Invalid conference name');
      }
      return response.json();
    })
    .then(data => {
      console.log('the data', data);
      for (let i = 0; i !== data.length; i++) {
        events.push({
          id: i,
          start: data[i].task.start_time[0] + ' ' + data[i].task.start_time[1],
          end: data[i].task.end_time[0] + ' ' + data[i].task.end_time[1],
          resourceId: 'r1',
          title: data[i].task.name,
          bgColor: '#2E2C2F',
        });
      }
      console.log('prerender')
      SchedulerDataReal.setEvents(events);
      console.log('events: ', events)
    })
    .catch(error => {
      console.error(error);
    });

  // ok here after we figure out what our userId is, We wana call the get tasks and populate a list with only the ones we are in
  const eventsParticipating = [];
  useEffect(() => {
    console.log('the user name after set is', userName);
    if (userName !== 'none' && eventsParticipating.length === 0) {
      console.log('lets fetch babu');
      fetch(`http://localhost:${BACKEND_PORT}/GetAllTasks`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          token
        }
      })
        .then(response => {
          if (!response.ok) {
            window.alert('Invalid conference name');
            throw new Error('Invalid conference name');
          }
          return response.json();
        })
        .then(data => {
          console.log('the data', data);

          // Filter tasks based on userId presence in the accepted array
          const userTasks = data.filter(task =>
            task.accepted.some(user => user.id === userName)
          );

          for (let i = 0; i !== userTasks.length; i++) {
            eventsParticipating.push({
              id: i,
              start: userTasks[i].task.start_time[0] + ' ' + userTasks[i].task.start_time[1],
              end: userTasks[i].task.end_time[0] + ' ' + userTasks[i].task.end_time[1],
              resourceId: 'r1',
              title: userTasks[i].task.name,
              bgColor: '#2E2C2F',
            });
          }
          console.log('eventsParticipating: ', eventsParticipating);
        })
        .catch(error => {
          console.error(error);
        });
    }
  }, [userName]);

  // SchedulerDataReal.setEvents(events)

  // Functions to handle scheduler actions
  const prevClick = (SchedulerDataCur) => {
    const newDate = moment(SchedulerDataCur.startDate, DATE_FORMAT).subtract(1, 'week').format(DATE_FORMAT);
    // SchedulerDataCur.setEvents(events)
    SchedulerDataReal.setDate(newDate)
    SchedulerDataReal.setEvents(events)
    setTimeout(function () {
      window.dispatchEvent(new Event('resize'));
    }, 100);
  };
  const nextClick = (SchedulerDataCur) => {
    const newDate = moment(SchedulerDataCur.startDate, DATE_FORMAT).add(1, 'week').format(DATE_FORMAT);
    // SchedulerDataCur.setEvents(events)
    SchedulerDataReal.setDate(newDate)
    SchedulerDataReal.setEvents(events)
    setTimeout(function () {
      window.dispatchEvent(new Event('resize'));
    }, 100);
  };

  const eventClicked = (SchedulerDataReal, event) => {
    console.log('HI THERE')
    console.log(event)
  };

  const handleShowMyTasks = () => {
    SchedulerDataReal.setEvents(eventsParticipating);
    setTimeout(function () {
      window.dispatchEvent(new Event('resize'));
    }, 100); // The fact that resizing after 0.8s fixes the issue is why frontend is terrible. 0.1 might be too short and hasnt loaded yet
  };

  const handleShowAllTasks = () => {
    SchedulerDataReal.setEvents(events);
    setTimeout(function () {
      window.dispatchEvent(new Event('resize'));
    }, 100); // The fact that resizing after 0.8s fixes the issue is why frontend is terrible. 0.1 might be too short and hasnt loaded yet
  };

  console.log('renderstage')
  return (
    <>
      <TopTitle text="✫ Schedule ✫" />
      {userRole === null
        ? <></>
        : <>
          <div style={{ marginTop: '3vh' }} className='schedule-flex-container'>
            {userRole === 'Organiser'
              ? <>
              <StandardButton onClick={() => OpenConfirmation(() => { ShareConference(token) }, 'send an email containing the conference schedule to everyone within the conference')} text="Share Conference" />
              <StandardButton onClick={() => OpenConfirmation(() => { ShareTask(token) }, 'send an email containing the task schedule to everyone within the conference')} text="Share Task" />
              </>
              : <>
                <StandardButton onClick={() => handleShowMyTasks()} text="Show My Tasks" />
                <StandardButton onClick={() => handleShowAllTasks()} text="Show All Tasks" />
              </>
            }
            </div>
          <div>
            <Scheduler
              schedulerData={SchedulerDataReal}
              prevClick={() => prevClick(SchedulerDataReal)}
              nextClick={() => nextClick(SchedulerDataReal)}
              eventItemClick={(event) => eventClicked(SchedulerDataReal, event)}
            />
          </div>
          <LogoutAndDashboardIcons />
        </>
      }

    </>
  );
};

export default DragDropContext(HTML5Backend)(SchedulePage);
