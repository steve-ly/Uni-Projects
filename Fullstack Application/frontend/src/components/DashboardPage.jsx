import { React, useState, useContext, useEffect } from 'react';
import { AuthContext } from './AuthContext';
import { useNavigate } from 'react-router-dom';
import { GetUserDetails, HandleLogout, GetTopUsers } from './HTTP/User';
import { CreateConference, JoinConference, GetAllConferences, GetConferenceName, LeaveConference, EditConferenceDetails } from './HTTP/Conference';
import { StandardButton, TopTitle, StandardInput, ConferenceStartEndDates } from './Containers'
import { CreateOrEditUser } from './UserElements'
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import goldTrophy from '../images/goldtrophy.png'
import silverTrophy from '../images/silvertrophy.png'
import bronzeTrophy from '../images/bronzetrophy.png'
import Rating from '@mui/material/Rating';
import '../style/global.css';
import '../style/ui.css';
import '../style/pagespecific/dashboard.css';

import logoutIcon from '../images/logout.png'
import profileIcon from '../images/profile.png'

function RatingBox ({ topUserArr, index }) {
  return (
  <>
  {
    topUserArr.length > index
      ? <div style={{ marginLeft: '3vw', marginRight: '3vw', display: 'inline-block', width: 130, textAlign: 'center' }}>
          <img width={130} height={130} src={index === 0 ? goldTrophy : (index === 1 ? silverTrophy : bronzeTrophy)}/>
          <div><Rating precision={0.5} sx={{ fontSize: '3vh', color: 'red' }} name="read-only" value={topUserArr[index].Total_score / 2} readOnly /></div>
          {topUserArr[index].Firstname} {topUserArr[index].Lastname}
        </div>
      : <></>
  }
  </>)
}

const DashboardPage = () => {
  const { token, setToken } = useContext(AuthContext);

  const navigate = useNavigate()
  function navigateToSchedule () { navigate('/schedule') }
  function navigateToGroupchat () { navigate('/groupchat') }
  function navigateToTasks () { navigate('/tasks') }
  function navigateToAttendanceLog () { navigate('/attendancelog') }
  function navigateToAttendanceList () { navigate('/attendancelist') }
  function navigateToVolunteerList () { navigate('/volunteerlist') }

  const [topUsers, setTopUsers] = useState([]);

  const [userDetails, setUserDetails] = useState(null);
  const [conferenceName, setConferenceName] = useState('');
  const [conferenceID, setConferenceID] = useState(null);

  const [allConferences, setAllConferences] = useState([]);

  const [showEditProfilePopup, setShowEditProfilePopup] = useState(false);
  const [showCreateProfilePopup, setShowCreateProfilePopup] = useState(false);

  const [showEditConferencePopup, setShowEditConferencePopup] = useState(false);

  // const [editProfile, setEditProfile] = React.useState(false);
  // const handleOpenEditProfile = () => setEditProfile(true);
  // const handleCloseEditProfile = () => setEditProfile(false);

  // Run these functions only on mount
  useEffect(() => {
    GetUserDetails(token, setUserDetails, setConferenceID)
    GetConferenceName(token, setConferenceName)
    GetAllConferences(token, setAllConferences)
    GetTopUsers(token, setTopUsers)
  }, []);

  if (userDetails == null) {
    return (<></>)
  }

  const IconBoxes = ({ showEditProfilePopup, setShowEditProfilePopup, token, setToken, navigate }) => {
    return (
      <>
      <div className="iconSection">
        <div className="iconBox" >
          <img src={logoutIcon} alt="Logout" onClick={() => { HandleLogout(token, setToken, navigate) }}/>
        </div>
        <div style={showEditProfilePopup ? { backgroundColor: '#2E2C2F' } : {}} className="iconBox" >
          <img src={profileIcon} alt="Edit Profile" onClick={() => { setShowEditProfilePopup(!showEditProfilePopup) }}/>
        </div>
      </div>
      </>
    );
  };

  const EditConference = ({ open, setFunction }) => {
    const cardStyle = {
      width: '28vw',
      backgroundColor: '#b8c0c8'
    };
    const [conferenceNameEditing, setConferenceNameEditing] = useState(conferenceName);
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');
    console.log(startTime)
    console.log(endTime)
    return (
      <Modal
        open={open}
        onClose={() => setFunction(false)}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          bgcolor: '#b8c0c8',
          borderRadius: '10px',
          boxShadow: 24,
          textAlign: 'center',
        }}>
          <Card sx={cardStyle}>
            <CardHeader
              title={<b>Edit Conference</b>}
            />
            <CardContent>
              <StandardInput stateValue={conferenceNameEditing} stateFunction={setConferenceNameEditing} placeholder="Conference Name"/>
              <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DemoContainer components={['DatePicker']}>
                  <DatePicker onChange={(event) => { setStartTime(event.toISOString().substring(0, 10)) }} label="Start Date" />
                  <DatePicker onChange={(event) => { setEndTime(event.toISOString().substring(0, 10)) }} label="End Date" />
                </DemoContainer>
              </LocalizationProvider>
            </CardContent>
            <CardActions sx={{
              display: 'flex',
              flexWrap: 'wrap',
              justifyContent: 'center',
            }}>

              <div> <StandardButton onClick={() => { setFunction(false) }} text="Cancel Edit" /> </div>
              <div> <StandardButton onClick={() => {
                EditConferenceDetails(token, startTime, endTime, conferenceNameEditing, setConferenceName, setAllConferences)
                setFunction(false)
              }} text="Submit Edit" /> </div>

            </CardActions>
          </Card>
        </Box>
      </Modal>
    );
  }

  // { showEditProfilePopup ? <EditProfilePopup setShowEditProfilePopup={setShowEditProfilePopup}/> : <></> }

  // If user is not in a conference
  if (conferenceID === null) {
    console.log(userDetails)
    return (
      <>
        <CreateOrEditUser isEdit={true} open={showEditProfilePopup} setFunction={setShowEditProfilePopup} userDetails={userDetails} token={token} />
        <TopTitle text="You have not joined a conference!" />
        <IconBoxes showEditProfilePopup={showEditProfilePopup} setShowEditProfilePopup={setShowEditProfilePopup} token={token} setToken={setToken} navigate={navigate} />
        <div className="flex-container">
            <div className="flex-item">
                {userDetails.role === 'Organiser'
                  ? <>
                  <h2>Create a Conference</h2>
                  <div>
                      <StandardInput stateValue={conferenceName} stateFunction={setConferenceName} placeholder="Conference Name" />
                      <ConferenceStartEndDates/>
                  </div>
                  <div>
                    <StandardButton onClick={() => {
                      CreateConference(token, conferenceName, setConferenceID)
                    }} text="Create a Conference" />
                  </div>
                  </>
                  : <></>
                }
                <h2>Join a Conference</h2>
                {userDetails.role === 'Organiser'
                  ? <p>Select a conference to join</p>
                  : <p>Select a conference to send a request to join to that conference&apos;s organisers</p>
                }
                <div className="chooseItemBox">
                  <style>{'::-webkit-scrollbar {width: 0; background: transparent;}'}</style>
                    {
                      allConferences.map(function (data) {
                        return (
                          <div key={data.id} onClick={() => {
                            JoinConference(token, data.id)
                            setConferenceID(data.id)
                            setConferenceName(data.name)
                          }}>{data.name}</div>
                        )
                      })
                    }
                </div>

            </div>
        </div>
      </>
    );
  } else {
    return (
      <>
        <CreateOrEditUser isEdit={true} open={showEditProfilePopup} setFunction={setShowEditProfilePopup} userDetails={userDetails} token={token} />
        <CreateOrEditUser isEdit={false} open={showCreateProfilePopup} setFunction={setShowCreateProfilePopup} />
        <EditConference open={showEditConferencePopup} setFunction={setShowEditConferencePopup} />
        <TopTitle text={`✦ ${conferenceName} ✦`} />
        <IconBoxes showEditProfilePopup={showEditProfilePopup} setShowEditProfilePopup={setShowEditProfilePopup} token={token} setToken={setToken} navigate={navigate} />
        <div className='rightSideButtons'>
        <div>
          <StandardButton onClick={ () => {
            LeaveConference(token, setConferenceID, setConferenceName)
            GetAllConferences(token, setAllConferences)
          } } text="Leave Conference" />
        </div>
        {userDetails.role === 'Organiser'
          ? <div>
            <StandardButton onClick={ () => { setShowEditConferencePopup(true) } } text="Edit Conference" />
          </div>
          : <></>
        }
        </div>
        <div className="dashboardBox">
            <div className="dashboardItem" onClick={() => { navigateToTasks() }}>
              <h3>Tasks</h3>
            </div>
            <div className="dashboardItem" onClick={() => { navigateToGroupchat() }}>
              <h3>Group Chat</h3>
            </div>
            {userDetails.role !== 'Organiser'
              ? <div className="dashboardItem" onClick={() => { navigateToAttendanceLog() }}>
                <h3>Attendance Logging</h3>
              </div>
              : <></>
            }
            {userDetails.role !== 'Volunteer'
              ? <div className="dashboardItem" onClick={() => { navigateToAttendanceList() }}>
                <h3>Attendance List</h3>
              </div>
              : <></>
            }
            <div className="dashboardItem" onClick={() => { navigateToSchedule() }}>
              <h3>Schedule</h3>
            </div>
            {userDetails.role !== 'Volunteer'
              ? <div className="dashboardItem" onClick={() => { navigateToVolunteerList() }}>
                <h3>Volunteer List</h3>
              </div>
              : <></>
            }
            {userDetails.role === 'Organiser'
              ? <div className="dashboardItem" onClick={() => { setShowCreateProfilePopup(true) }}>
                <h3>Create Volunteer</h3>
              </div>
              : <></>
            }
        </div>
        <div style={{ textAlign: 'center', marginTop: '1.5vh' }}>
          <RatingBox topUserArr={topUsers} index={1} />
          <RatingBox topUserArr={topUsers} index={0} />
          <RatingBox topUserArr={topUsers} index={2} />
        </div>
        <div style={{ textAlign: 'center', fontSize: '4vh', marginTop: '2vh' }}>
          { topUsers.length > 0 ? <b>Highest Rated Volunteers!</b> : <></> }
        </div>
      </>
    );
  }
  // Check if user is in a conference first
};

export default DashboardPage;
