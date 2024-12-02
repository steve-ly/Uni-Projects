import React, { useContext, useEffect, useState } from 'react';
import config from '../config.json';
import { AuthContext } from './AuthContext';
import { LogoutAndDashboardIcons, TopTitle, LargeStandardButton } from './Containers'
import '../style/pagespecific/attendLog.css';
import { getMyTasks, taskLogin, taskLogout } from './HTTP/Attendance';
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Grid from '@mui/material/Grid';

import { makeStyles } from '@material-ui/core/styles';
const BACKEND_PORT = config.BACKEND_PORT;

const AttendancePage = () => {
  const { token, setToken } = useContext(AuthContext);
  const [chats, setChats] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);
  const [selectedChatName, setSelectedChatName] = useState('');

  console.log(token) /* These are here so linter doesn't whinge */
  console.log(setToken)
  console.log(BACKEND_PORT);
  console.log(selectedChat);

  const useStyles = makeStyles({
    table: {
      minWidth: 650,
    },
    chatSection: {
      width: '100%',
      height: '80vh',
    },
    headBG: {
      backgroundColor: '#e0e0e0'
    },
    borderRight500: {
      borderRight: '1px solid #e0e0e0'
    },
    messageArea: {
      height: '70vh',
      overflowY: 'auto'
    },
    selectChatSection: {
      width: '40vw',
      height: '62vh',
      overflowY: 'auto'
    }
  });

  const classes = useStyles();

  useEffect(() => {
  // Fetch tasks when the component mounts
    const fetchChatsData = async () => {
      try {
        const chatGroups = await getMyTasks(token);
        setChats(chatGroups);
        console.log('task groups: ', chatGroups);
      } catch (error) {
        console.error('Error fetching task groups:', error);
      }
    };

    fetchChatsData();
  }, []);

  const handleTaskLogin = async () => {
    try {
      // Call the send message function
      await taskLogin(token, selectedChat.task_id);
      // console.log(token, selectedChat.task_id);
    } catch (error) {
      console.error('Error login:', error);
    }
  };

  const handleTaskLogout = async () => {
    try {
      // Call the send message function
      await taskLogout(token, selectedChat.task_id);
      // console.log(token, selectedChat.task_id);
    } catch (error) {
      console.error('Error login/out:', error);
    }
  };

  const handleSelectChat = async (chat) => {
    setSelectedChat(chat);
    setSelectedChatName(chat.name)
    console.log(selectedChatName);
  }

  return (
    <>
    <TopTitle text="✫ Attendance ✫" />
    <LogoutAndDashboardIcons/>
    <div className='attendance-flex-container-log'>
      <div className='left-flex-container-log'>
        <h2 className='little-heading'>Select Task</h2>
        <Grid item xs={3}>
          <List className={classes.selectChatSection}>
            {chats.map((chat) => (
              <ListItem button key={chat.task_id} onClick={() => handleSelectChat(chat)} className='list-item-but5'>
                <ListItemText primary={chat.name} />
              </ListItem>
            ))}
          </List>
        </Grid>
      </div>
      <div className='right-flex-container-log'>
        <h2>Task Login</h2>
        <div className='button-flex'>
          <LargeStandardButton onClick={ () => { handleTaskLogin() } } text="Login" />
          <LargeStandardButton onClick={ () => { handleTaskLogout() } } text="Logout" />
        </div>
        <div className='select-headings'>{selectedChatName}</div>
      </div>
    </div>
    </>
  );
};

export default AttendancePage;
