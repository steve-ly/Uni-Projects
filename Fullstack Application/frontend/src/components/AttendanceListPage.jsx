import React, { useContext, useEffect, useState } from 'react';
import config from '../config.json';
import { AuthContext } from './AuthContext';
import { LogoutAndDashboardIcons, TopTitle, LargeStandardButton } from './Containers';
import { getTaskAttendance, approveAttendance, getAllTasks } from './HTTP/AttendanceList';
import '../style/pagespecific/AttenList.css';
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Grid from '@mui/material/Grid';
import { makeStyles } from '@material-ui/core/styles';

const BACKEND_PORT = config.BACKEND_PORT;

const AttendancePage = () => {
  const { token, setToken } = useContext(AuthContext);
  const [tasks, setTasks] = useState([]);
  const [selectedtask, setSelectedTasks] = useState([]);
  const [selectedtasktext, setSelectedTasksText] = useState('');
  const [attendies, setAttendies] = useState([]);
  const [selectedperson, setSelectedperson] = useState([]);
  const [selectedpersontext, setSelectedpersonText] = useState('');
  const [updateColours, setUpdateColours] = useState(0);

  console.log(token);
  console.log(setToken);
  console.log(BACKEND_PORT);
  console.log(selectedtask);
  console.log(selectedperson);

  // get all tasks in the conference at the start
  useEffect(() => {
    const fetchTasksData = async () => {
      try {
        const allTasks = await getAllTasks(token);
        setTasks(allTasks);
        console.log('Tasks ', allTasks);
        console.log(tasks);
      } catch (error) {
        console.error('Error tasks :', error);
      }
    };

    fetchTasksData();
  }, []);

  // get all the attendees when a task is selected
  useEffect(() => {
    const handleGetAllAttendance = async () => {
      try {
        console.log(selectedtask.task.id);
        const taskAtten = await getTaskAttendance(token, selectedtask.task.id);
        setAttendies(taskAtten);
        console.log('got all Attendies', attendies);
      } catch (error) {
        console.error('Error login:', error);
      }
    };

    handleGetAllAttendance();
  }, [selectedtask, updateColours]);

  const handleAprroveAttendance = async () => {
    try {
      console.log('task, person: ', selectedtask.task.id, selectedperson);
      await approveAttendance(token, selectedtask.task.id, selectedperson);
      setUpdateColours(updateColours + 1);
    } catch (error) {
      console.error('Error login:', error);
    }
  };

  const handleSetSelectTask = async (task) => {
    setSelectedTasks(task);
    setSelectedTasksText(task.task.name);
  };

  const handleSetSelectperson = async (people) => {
    setSelectedperson(people.user_id);
    setSelectedpersonText(people.username);
  };

  const useStyles = makeStyles({
    selectChatSection: {
      width: '28vw',
      height: '65vh',
      overflowY: 'auto'
    }
  });

  const classes = useStyles();

  return (
    <>
      <TopTitle text="✫ Approve Attendance ✫" />
      <LogoutAndDashboardIcons />
      <div className='attendance-flex-container'>
        <div className='left-flex-container'>
          <h2 className='little-heading'>Select Task</h2>
          <Grid item xs={3}>
            <List className={classes.selectChatSection}>
              {tasks.map((task) => (
                <ListItem
                  button
                  key={task.task.id}
                  onClick={() => handleSetSelectTask(task)}
                  className='list-item-but6'
                >
                  <ListItemText primary={task.task.name} />
                </ListItem>
              ))}
            </List>
          </Grid>
        </div>
        <div className='middle-flex-container'>
          <h2 className='little-heading'>Attendees</h2>
          <Grid item xs={3}>
            <List className={classes.selectChatSection}>
              {attendies.map((people) => (
                <ListItem
                  button
                  key={people.id}
                  onClick={() => handleSetSelectperson(people)}
                  className={people.validated ? 'list-item-but5-green' : 'list-item-but5-red'}
                >
                  <ListItemText primary={people.username} />
                </ListItem>
              ))}
            </List>
          </Grid>
        </div>
        <div className='right-flex-container'>
          <h2 className='little-heading'>Approval</h2>
          <h2 className='little-heading'>{selectedtasktext}</h2>
          <h2 className='little-heading'>{selectedpersontext}</h2>
          <LargeStandardButton onClick={() => handleAprroveAttendance()} text="Approve/Reject" />
        </div>
      </div>
    </>
  );
};

export default AttendancePage;
