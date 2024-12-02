import React, { useState, useContext, useEffect } from 'react';
import { AuthContext } from './AuthContext';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import CardHeader from '@mui/material/CardHeader';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import { SkillsBox } from './UserElements'
import { TopTitle, LogoutAndDashboardIcons, StandardButton, SmallStandardButton } from './Containers'
import { GetAssignableVolunteers } from './HTTP/Conference';
import { GetUserDetails } from './HTTP/User';
import { GetAllTasks, CreateTask, EditTask, ForceAddVolunteerToTask, DeleteTask, RequestAddVolunteerToTask, RemoveVolunteerFromTask, ToggleTaskComplete, ApproveRequest } from './HTTP/Task';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import '../style/global.css';
import '../style/ui.css';
import greenCheckIcon from '../images/greencheck.png'
import redCrossIcon from '../images/redcross.png'
import dayjs from 'dayjs';
import timezone from 'dayjs/plugin/timezone';
import utc from 'dayjs/plugin/utc';
import { UseConfirmation } from './ConfirmationElement';

const buttonStyle = {
  color: 'white',
  width: '46%',
  textTransform: 'none',
  backgroundColor: '#475B63',
  '&:hover': {
    backgroundColor: '#2E2C2F',
    transform: 'scale(1.05)'
  },
  margin: '1%',
};

function calculateTimeDifference (startTime, endTime) {
  const start = new Date(startTime[0] + 'T' + startTime[1] + 'Z');
  const end = new Date(endTime[0] + 'T' + endTime[1] + 'Z');

  const timeDifference = end - start;

  const totalSeconds = Math.floor(timeDifference / 1000);
  const totalMinutes = Math.floor(totalSeconds / 60);
  const totalHours = Math.floor(totalMinutes / 60);
  const totalDays = Math.floor(totalHours / 24);

  const seconds = totalSeconds % 60;
  const minutes = totalMinutes % 60;
  const hours = totalHours % 24;

  const finalstr = (totalDays === 0 ? '' : totalDays.toString() + ' Day' + (totalDays === 1 ? '' : 's')) +
                    (hours === 0 ? '' : ' ' + hours.toString() + ' Hour' + (hours === 1 ? '' : 's')) +
                    (minutes === 0 ? '' : ' ' + minutes.toString() + ' Minute' + (minutes === 1 ? '' : 's')) +
                    (seconds === 0 ? '' : ' ' + seconds.toString() + ' Second' + (seconds === 1 ? '' : 's'))

  return finalstr;
}

function TaskHeader ({ title, expectedTime, complete, token, taskID, setAllTasks, isVolunteer, skillsarg }) {
  const [completeButton, setCompleteButton] = useState(complete);
  return (
    <CardHeader
      action={
        <>
          { !isVolunteer
            ? <FormControlLabel control={<Switch checked={completeButton} onChange={(event) => {
              setCompleteButton(event.target.checked)
              ToggleTaskComplete(token, taskID, setAllTasks)
            }} />}/>
            : <></>
          }
          <IconButton aria-label="settings">
            <img width={40} height={40} src={!completeButton ? redCrossIcon : greenCheckIcon}/>
          </IconButton>
        </>
      }
      title={title}
      subheader={<><span style={{ fontSize: '12px' }}>{'Expected time: ' + expectedTime}</span><div>{skillsarg === '' ? 'No Skills' : skillsarg}</div></>}
      // subheader={'Expected time: ' + expectedTime} // + calculateTimeDifference(['2023-10-22', '08:00:00'], ['2023-10-22', '09:00:00'])}
    />
  );
}

function TaskDescription ({ description }) {
  return (
    <CardContent>
      <div style={{
        height: '110px',
        overflow: 'hidden',
        scrollbarWidth: 'none',
        overflowX: 'scroll',
        overflowY: 'scroll',
        WebkitOverflowScrolling: 'touch',
      }}>
        <style>{'::-webkit-scrollbar {width: 0; background: transparent;}'}</style>
        <Typography sx={{ mb: 1.5 }} color="text.primary">
          {description}
        </Typography>
      </div>
    </CardContent>
  );
}

function CreateOrEditTask ({ OpenConfirmation, setAllTasks, isCreating, token, open, handleClose, complete, titlearg = '', descriptionarg = '', startTimearg = '', endTimearg = '', skillsarg = '[]', taskID = null }) {
  const cardStyle = {
    width: 400,
    backgroundColor: '#b8c0c8'
  };

  const [description, setDescription] = useState(descriptionarg);
  const [title, setTitle] = useState(titlearg);
  const [startTime, setStartTime] = useState(startTimearg);
  const [endTime, setEndTime] = useState(endTimearg);
  const [selectedValuesSkills, setSelectedValuesSkills] = useState([]);

  dayjs.extend(timezone)
  dayjs.extend(utc)
  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'background.paper',
        borderRadius: '10px',
        boxShadow: 24,
      }}>
        <Card sx={cardStyle}>
          <CardHeader
            action={
              <>
              <IconButton aria-label="settings">
                <img width={40} height={40} src={complete ? redCrossIcon : greenCheckIcon}/>
              </IconButton>
              </>
            }
            title={<>
              <TextField
                id="outlined-multiline-static"
                label="Title"
                sx={{
                  width: '95%'
                }}
                multiline
                rows={1}
                defaultValue={title}
                onChange={(event) => { setTitle(event.target.value) }}
              />
            </>}
            // subheader={'Expected time: ' + expectedTime} // + calculateTimeDifference(['2023-10-22', '08:00:00'], ['2023-10-22', '09:00:00'])}
          />
          <SkillsBox selectedValuesSkills={selectedValuesSkills} setSelectedValuesSkills={setSelectedValuesSkills} />
          <CardContent>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DemoContainer components={['DateTimePicker']}>
                <DateTimePicker defaultValue={dayjs(startTime).tz('Australia/Sydney')} onChange={(event) => { setStartTime(event.toISOString().substring(0, event.toISOString().length - 5)) }} label="Start Date & Time" />
                <DateTimePicker defaultValue={dayjs(endTime).tz('Australia/Sydney')} onChange={(event) => { console.log(event.toISOString().substring(0, event.toISOString().length - 5)); setEndTime(event.toISOString().substring(0, event.toISOString().length - 5)) }} label="End Date & Time" />
              </DemoContainer>
            </LocalizationProvider>

            <TextField
              id="outlined-multiline-static"
              label="Description"
              sx={{
                marginTop: '3vh',
                width: '100%'
              }}
              multiline
              rows={4}
              defaultValue={description}
              onChange={(event) => { setDescription(event.target.value) }}
            />
          </CardContent>
          <CardActions sx={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
          }}>
            {
              isCreating
                ? <>
                  <Button
                    sx={buttonStyle}
                    onClick={() => {
                      console.log(startTime)
                      console.log(endTime)
                      CreateTask(token, title, description, startTime, endTime, selectedValuesSkills, setAllTasks)
                      handleClose()
                    }}
                  >Create Task
                  </Button>
                </>
                : <>
                  <Button
                  sx={buttonStyle}
                  onClick={() => {
                    OpenConfirmation(() => {
                      EditTask(token, taskID, title, description, startTime, endTime, selectedValuesSkills, setAllTasks)
                      handleClose()
                    }, 'save your changes on this task')
                  }}>Save Task</Button>
                  <Button
                  sx={buttonStyle}
                  onClick={() => {
                    OpenConfirmation(() => {
                      DeleteTask(token, taskID, setAllTasks)
                      handleClose()
                    }, 'delete this task')
                  }}>Delete Task</Button>
                </>
            }
          </CardActions>
        </Card>
      </Box>
    </Modal>
  );
}

function MapUsers ({ taskID, token, userList, functionBind, setAllTasks, OpenConfirmation, confirmationWords }) {
  return (
    <List sx={{}} component="nav" aria-label="mailbox folders">
      {
        userList.map(function (data) {
          const functionUse = () => { OpenConfirmation(() => { functionBind(token, data.id, taskID, setAllTasks) }, confirmationWords.replace('USER', data.username)) }
          return (
            <div key={data.id}>
              <ListItem button onClick={ functionUse }>
                <ListItemText primary={data.username} />
              </ListItem>
              <Divider />
            </div>
          );
        })
      }
    </List>
  );
}

function StandardModal ({ taskID, token, open, handleClose, title, userList, functionBind, setAllTasks, OpenConfirmation, confirmationWords }) {
  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '35vw',
        bgcolor: '#b8c0c8',
        borderRadius: '5px',
        color: '#2E2C2F',
        boxShadow: 24,
        p: 4,
      }}>
        <Typography id="modal-modal-title" variant="h6" component="h2">
          <b>{title}</b>
        </Typography>
        <MapUsers taskID={taskID} token={token} userList={userList} functionBind={functionBind} setAllTasks={setAllTasks} OpenConfirmation={OpenConfirmation} confirmationWords={confirmationWords} />
      </Box>
    </Modal>
  );
}

function BasicCard ({ token, title, description, expectedTime, startTime, endTime, complete, isVolunteer, taskID, setAllTasks, requestedToJoinArray, joinedArray, userID, skillsarg, OpenConfirmation }) {
  // requestedToJoinArray // [{ username: 'miya', id: 1 }, { username: 'daniel', id: 1 }]
  // joinedArray // [{ username: 'oscar', id: 1 }, { username: 'lachlan', id: 1 }, { username: 'steven', id: 1 }]
  // console.log(requestedToJoinArray)
  // console.log(joinedArray)
  // START MODAL

  const [openVolunteerList, setOpenVolunteerList] = React.useState(false);
  const handleOpenVolunteerList = () => setOpenVolunteerList(true);
  const handleCloseVolunteerList = () => setOpenVolunteerList(false);

  const [openVolunteerRequests, setOpenVolunteerRequests] = React.useState(false);
  const handleOpenVolunteerRequests = () => setOpenVolunteerRequests(true);
  const handleCloseVolunteerRequests = () => setOpenVolunteerRequests(false);

  const [openEditTask, setOpenEditTask] = React.useState(false);
  const handleOpenEditTask = () => setOpenEditTask(true);
  const handleCloseEditTask = () => setOpenEditTask(false);

  const [openAssignVolunteers, setOpenAssignVolunteers] = React.useState(false);
  const handleOpenAssignVolunteers = () => setOpenAssignVolunteers(true);
  const handleCloseAssignVolunteers = () => setOpenAssignVolunteers(false);

  // END MODAL

  const [assignableVolunteers, setAssignableVolunteers] = useState([]);

  useEffect(() => {
    GetAssignableVolunteers(token, setAssignableVolunteers, joinedArray)
  }, [joinedArray]);

  const volunteerCardStyle = {
    width: 400,
    height: 310, // 280 for volunteer
    backgroundColor: '#b8c0c8'
  };

  const organiserCardStyle = {
    width: 400,
    height: 355, // 280 for volunteer
    backgroundColor: '#b8c0c8'
  };

  return (
    <Card sx={isVolunteer ? volunteerCardStyle : organiserCardStyle}>
      <TaskHeader title={title} expectedTime={expectedTime} complete={complete} token={token} taskID={taskID} setAllTasks={setAllTasks} isVolunteer={isVolunteer} skillsarg={skillsarg}/>
      <TaskDescription description={description}/>
      <CardActions sx={{
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
      }}>
        {isVolunteer
          ? <>
            <Button sx={buttonStyle} onClick={handleOpenVolunteerList}>Volunteers</Button>
            <StandardModal confirmationWords={'error'} OpenConfirmation={() => {}} setAllTasks={setAllTasks} taskID={taskID} token={token} functionBind={() => {}} open={openVolunteerList} handleClose={handleCloseVolunteerList} title={'Volunteers on Task'} userList={joinedArray}/>
            {joinedArray.find((localuser) => localuser.id === userID) === undefined
              ? <Button sx={buttonStyle} onClick={() => OpenConfirmation(() => { RequestAddVolunteerToTask(token, userID, taskID, setAllTasks) }, 'join this task')}>Request to Join</Button>
              : <Button sx={buttonStyle} onClick={() => OpenConfirmation(() => { RemoveVolunteerFromTask(token, userID, taskID, setAllTasks) }, 'leave this task')}>Leave</Button>
            }
          </>
          : <>
            <Button sx={buttonStyle} onClick={handleOpenVolunteerList}>Volunteers</Button>
            <StandardModal confirmationWords={'remove USER from this task'} OpenConfirmation={OpenConfirmation} setAllTasks={setAllTasks} taskID={taskID} token={token} functionBind={RemoveVolunteerFromTask} open={openVolunteerList} handleClose={handleCloseVolunteerList} title={'Volunteers on Task'} userList={joinedArray}/>

            <Button sx={buttonStyle} onClick={handleOpenVolunteerRequests}>View Requests</Button>
            <StandardModal confirmationWords={'accept USER\'s request to join this task'} OpenConfirmation={OpenConfirmation} setAllTasks={setAllTasks} taskID={taskID} token={token} functionBind={ApproveRequest} open={openVolunteerRequests} handleClose={handleCloseVolunteerRequests} title={'Volunteers Waiting for Organisers\' Approval to Join Task'} userList={requestedToJoinArray}/>

            <Button sx={buttonStyle} onClick={handleOpenAssignVolunteers}>Assign Volunteers</Button>
            <StandardModal confirmationWords={'assign USER to this task'} OpenConfirmation={OpenConfirmation} setAllTasks={setAllTasks} taskID={taskID} token={token} functionBind={ForceAddVolunteerToTask} open={openAssignVolunteers} handleClose={handleCloseAssignVolunteers} title={'Assign a Volunteer to this Task'} userList={assignableVolunteers}/>

            <Button sx={buttonStyle} onClick={handleOpenEditTask}>Edit</Button>
            <CreateOrEditTask token={token} taskID={taskID} setAllTasks={setAllTasks} isCreating={false} open={openEditTask} handleClose={handleCloseEditTask} complete={complete} titlearg={title} descriptionarg={description} completearg={complete} startTimearg={startTime} endTimearg={endTime} skillsarg={skillsarg} OpenConfirmation={OpenConfirmation}/>

          </>
        }

      </CardActions>
    </Card>
  );
}

const TasksPage = () => {
  const { token, setToken } = useContext(AuthContext);
  const OpenConfirmation = UseConfirmation();

  const [allTasks, setAllTasks] = useState([]);
  const [userDetails, setUserDetails] = useState([]);

  const [openNewTask, setNewTask] = React.useState(false);
  const handleOpenNewTask = () => setNewTask(true);
  const handleCloseNewTask = () => setNewTask(false);

  useEffect(() => {
    localStorage.setItem('filterapi', 'GetAllTasks')
    GetAllTasks(token, setAllTasks)
    GetUserDetails(token, setUserDetails)
  }, []);

  /* These are here so linter doesn't whinge */
  console.log(setToken);
  console.log(allTasks)

  return (
    <>
    <div className='rightSideButtons'>
    <div>
      {userDetails.role === 'Organiser'
        ? <StandardButton onClick={handleOpenNewTask} text="Create Task" />
        : <>
          <SmallStandardButton buttonType={'GetAllTasks'} onClick={ () => { localStorage.setItem('filterapi', 'GetAllTasks'); GetAllTasks(token, setAllTasks) } } text="All" />
          <SmallStandardButton buttonType={'GetAvailableTasks'} onClick={ () => { localStorage.setItem('filterapi', 'GetAvailableTasks'); GetAllTasks(token, setAllTasks) } } text="Available" />
          <SmallStandardButton buttonType={'GetBestTasks'} onClick={ () => { localStorage.setItem('filterapi', 'GetBestTasks'); GetAllTasks(token, setAllTasks) } } text="Best" />
          <SmallStandardButton buttonType={'GetPreferredTasks'} onClick={ () => { localStorage.setItem('filterapi', 'GetPreferredTasks'); GetAllTasks(token, setAllTasks) } } text="Preffered" />
          </>
      }
      </div>
    </div>
    <LogoutAndDashboardIcons/>
    <TopTitle text="✫ Tasks ✫" />

    <CreateOrEditTask setAllTasks={setAllTasks} isCreating={true} token={token} open={openNewTask} handleClose={handleCloseNewTask} OpenConfirmation={OpenConfirmation} />

    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '50px', justifyContent: 'center' }}>
      {
        allTasks.map(function (data) {
          console.log(data)
          return (
            <BasicCard
              token={token}
              taskID={data.task.id}
              key={data.task.id}
              title={data.task.name}
              description={data.task.description}
              expectedTime={calculateTimeDifference(data.task.start_time, data.task.end_time)}
              startTime={data.task.start_time[0] + 'T' + data.task.start_time[1]}
              endTime={data.task.end_time[0] + 'T' + data.task.end_time[1]}
              complete={data.task.completed}
              isVolunteer={userDetails.role !== 'Organiser'}
              setAllTasks={setAllTasks}
              requestedToJoinArray={data.requested}
              joinedArray={data.accepted}
              userID={userDetails.user_id}
              skillsarg={data.task.skills_recommended}
              OpenConfirmation={OpenConfirmation}
            />
          )
        })
      }
    </div>
    </>
  );
};

export default TasksPage;
