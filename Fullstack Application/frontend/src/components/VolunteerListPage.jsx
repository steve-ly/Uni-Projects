import React, { useContext, useState, useEffect } from 'react';
import config from '../config.json';
import { AuthContext } from './AuthContext';
import { LogoutAndDashboardIcons, TopTitle, StandardButton } from './Containers'
import { GetAllVolunteerInformation, AddManagerRating, GetUserRole } from './HTTP/User';
import Card from '@mui/material/Card';
import { CreateOrEditUser } from './UserElements'
import CardHeader from '@mui/material/CardHeader';
import IconButton from '@mui/material/IconButton';
import Rating from '@mui/material/Rating';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import TextField from '@mui/material/TextField';
import Tooltip from '@mui/material/Tooltip';
import volunteerIcon from '../images/volunteericon.png'
import managerIcon from '../images/managericon.png'
import goldTrophy from '../images/goldtrophy.png'
import silverTrophy from '../images/silvertrophy.png'
import bronzeTrophy from '../images/bronzetrophy.png'
import { UseConfirmation } from './ConfirmationElement';

const BACKEND_PORT = config.BACKEND_PORT;

function VolunteerHeader ({ rating, firstname, lastname, username, ismanager, placing }) {
  // <Rating precision={0.5} sx={{ color: 'red' }} name="read-only" value={4.5} readOnly />
  console.log(username)
  var tooltip = ismanager ? 'Manager' : 'Volunteer'
  var image = ismanager ? managerIcon : volunteerIcon

  switch (placing) {
    case 'First':
      image = goldTrophy
      break
    case 'Second':
      image = silverTrophy
      break
    case 'Third':
      image = bronzeTrophy
      break
  }

  return (
    <CardHeader
      sx={{
        cursor: 'pointer',
        marginTop: '-1vh'
      }}
      onClick={ console.log('succ') }
      action={
        <>
          <Tooltip title={tooltip}>
            <IconButton aria-label="settings">
              <img width={60} height={60} src={image}/>
            </IconButton>
          </Tooltip>
        </>
      }
      title={firstname + ' ' + lastname}
      subheader={
        rating !== 0
          ? <Rating precision={0.5} sx={{ color: 'red' }} name="read-only" value={rating} readOnly />
          : <span>No Manager Ratings</span>
      }
      // subheader={'Expected time: ' + expectedTime} // + calculateTimeDifference(['2023-10-22', '08:00:00'], ['2023-10-22', '09:00:00'])}
    />
  );
}

function SkillsAndPreferences ({ arr, title }) {
  console.log(arr)
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        msOverflowStyle: 'none',
        scrollbarWidth: 'none',
        overflow: 'scroll',
        '& > *': {
          m: 1,
        },
      }}
    >
      <style>{'::-webkit-scrollbar {width: 0; background: transparent;}'}</style>
      <h1 style={{ fontSize: '2vh' }}>{title}</h1>
      {
        (arr.length === 0 || (arr.length === 1 && arr[0] === ''))
          ? <p style={{ fontStyle: 'italic', fontSize: '1.5vh' }}>This volunteer has no {title}</p>
          : <ButtonGroup sx={{ '.MuiButtonGroup-grouped': { borderColor: 'black', color: 'black', } }} variant="outlined" aria-label="outlined button group">
            {arr.map(function (data) {
              return (
                <Button sx={{ width: '6vw' }} key={data}>{data}</Button>
              )
            })}
          </ButtonGroup>
      }
    </Box>
  );
}

function VolunteerModal ({ setAllVolunteerInformation, open, setFunction, volunteerData, token, userRole }) {
  const [managerRating, setManagerRating] = useState(volunteerData.Manager_score / 2);
  const OpenConfirmation = UseConfirmation();
  const [showEditProfilePopup, setShowEditProfilePopup] = useState(false);
  const [showAvailablePopup, setShowAvailablePopup] = useState(false);
  return (
    <>
    <Modal
        open={showAvailablePopup}
        onClose={() => { setShowAvailablePopup(false) }}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
      <Box sx={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        height: '42%',
        transform: 'translate(-50%, -50%)',
        width: '18vw',
        bgcolor: '#b8c0c8',
        borderRadius: '5px',
        boxShadow: 24,
        p: 4,
        textAlign: 'center',
        color: '#2E2C2F'
      }}>
        <TextField
          id="outlined-multiline-static"
          label="Dates Available"
          sx={{
            marginTop: '3vh',
            width: '60%',
            backgroundColor: '#ccc',
          }}
          inputProps={ { style: { textAlign: 'center', fontSize: 22, lineHeight: 1.3 } }}
          multiline
          rows={8}
          value={volunteerData.Availability.join('\n')}
          readOnly={true}
        />
        <StandardButton onClick={ () => { setShowAvailablePopup(false) } } text="Close Window" />
      </Box>

    </Modal>
    <CreateOrEditUser setAllVolunteerInformation={setAllVolunteerInformation} isEdit={true} open={showEditProfilePopup} setFunction={setShowEditProfilePopup} userDetails={{
      targetusername: volunteerData.Username,
      firstName: volunteerData.Firstname,
      lastName: volunteerData.Lastname,
      email: volunteerData.Email,
      username: volunteerData.Username,
      password: volunteerData.Password,
      role: volunteerData.Is_manager ? 'Manager' : 'Volunteer'
    }} token={token} editingVolunteer={true} />
    <Modal
      open={open}
      onClose={ setFunction }
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        height: '85%',
        transform: 'translate(-50%, -50%)',
        width: '30vw',
        bgcolor: '#b8c0c8',
        borderRadius: '5px',
        boxShadow: 24,
        p: 4,
        textAlign: 'center',
        color: '#2E2C2F'
      }}>
        <div style={{ fontSize: '3vh' }}><b>{volunteerData.Firstname} {volunteerData.Lastname}</b></div>
        <SkillsAndPreferences title={'Skills'} arr={volunteerData.Skills} />
        <SkillsAndPreferences title={'Preferences'} arr={volunteerData.Preferences} />
        <h1 style={{ fontSize: '2vh' }}>Feedback</h1>
        <div style={{ marginBottom: '1vh' }}>Overall Anonymous Score: {<Rating precision={0.5} sx={{ fontSize: '2.2vh', color: 'blue' }} name="read-only" value={volunteerData.Attendee_score / 2} readOnly />}</div>
        <Box sx={{
          width: '100%',
          height: '35%',
          bgcolor: '#ccc',
          boxShadow: 24,
          overflow: 'scroll',
          msOverflowStyle: 'none',
          scrollbarWidth: 'none',
          textAlign: 'left',
        }}>
          <style>{'::-webkit-scrollbar {width: 0; background: transparent;}'}</style>
          {volunteerData.Feedbacklist.map(function (data) {
            return (
              <Box sx={{
                p: 1,
              }}
              key={Math.random()}
              >
                <div><b>Name:</b> {data.name}</div>
                <div><b>Score:</b> <Rating precision={0.5} sx={{ fontSize: '1.8vh', color: 'blue' }} name="read-only" value={data.score / 2} readOnly /></div>
                <div><b>Feedback:</b> {data.feedback}</div>
              </Box>
            )
          })}
        </Box>
        <h1 style={{ fontSize: '2vh' }}>Manager Score</h1>
        { volunteerData.Has_voted || userRole === 'Organiser'
          ? <>
            <p style={{ fontStyle: 'italic', fontSize: '1.8vh' }}>{ userRole === 'Organiser' ? 'Only managers can vote' : 'You have already voted'}</p>
            <div><Rating precision={0.5} sx={{ fontSize: '6vh', color: 'red' }} name="read-only" value={managerRating} readOnly /></div>
          </>
          : <>
            <div><Rating sx={{ fontSize: '6vh', color: 'red' }} name="half-rating" value={managerRating} onChange={(event, newValue) => { setManagerRating(newValue) }} precision={0.5} /></div>

            <StandardButton onClick={ () => {
              OpenConfirmation(() => {
                AddManagerRating(volunteerData.Id, managerRating * 2, token, setAllVolunteerInformation)
              }, `submit your score of ${parseFloat(managerRating)} stars`)
            } } text="Add Score" />
          </>

        }
        {
          userRole === 'Organiser'
            ? <StandardButton onClick={ () => { setShowEditProfilePopup(true) } } text="Edit Profile" />
            : <></>
        }
        {' '}
        <StandardButton onClick={ () => { setShowAvailablePopup(true) } } text="View Availability" />
      </Box>
    </Modal>
    </>
  );
}

function BasicVolunteer ({ data, token, setAllVolunteerInformation, userRole }) {
  const [openVolunteerInformation, setOpenVolunteerInformation] = useState(false)
  const cardStyle = {
    width: 330,
    height: 80, // 280 for volunteer
    backgroundColor: '#b8c0c8',
    transition: 'transform 0.2s, background-color 0.2s', // Add transition for smooth effect
    '&:hover': {
      transform: 'scale(1.05)', // Grow the card on hover
      backgroundColor: 'lightgray', // Change background color on hover
    }
  }
  console.log(data)
  console.log(data.Firstname)
  return (
    <>
      <VolunteerModal userRole={userRole} setAllVolunteerInformation={setAllVolunteerInformation} open={openVolunteerInformation} setFunction={ () => setOpenVolunteerInformation(false) } volunteerData={data} token={token}/>
      <Card sx={cardStyle} onClick={ () => setOpenVolunteerInformation(true) } >
        <VolunteerHeader rating={data.Manager_score / 2} username={data.Email} firstname={data.Firstname} lastname={data.Lastname} ismanager={data.Is_manager} placing={data.Specialfeatures} />
      </Card>
    </>
  );
}

const VolunteerListPage = () => {
  const { token, setToken } = useContext(AuthContext);

  console.log(token) /* These are here so linter doesn't whinge */
  console.log(setToken)
  console.log(BACKEND_PORT)
  const [allVolunteerInformation, setAllVolunteerInformation] = useState([])
  const [userRole, setUserRole] = useState(null);

  useEffect(() => {
    GetUserRole(token, setUserRole)
    GetAllVolunteerInformation(token, setAllVolunteerInformation)
  }, []);
  // <VolunteerModal open={openVolunteerInformation} setFunction={ () => setOpenVolunteerInformation(false) }/>
  // <div style={{ textAlign: 'right' }} onClick={ () => setOpenVolunteerInformation(true) } >CLICKME</div>
  return (
    <>
      <LogoutAndDashboardIcons/>
      <TopTitle text="✫ Volunteer List ✫" />
      <div style={{ marginTop: '4vh', display: 'flex', flexWrap: 'wrap', gap: '50px', justifyContent: 'center' }}>
        {
          allVolunteerInformation.map(function (data) {
            return (
              <>
                <BasicVolunteer data={data} token={token} setAllVolunteerInformation={setAllVolunteerInformation} userRole={userRole}/>
              </>
            )
          })
        }
      </div>
    </>
  );
};

export default VolunteerListPage;
