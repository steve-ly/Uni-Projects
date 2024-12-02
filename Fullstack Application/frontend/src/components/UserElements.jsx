import { React, useState } from 'react';
import MultipleSelectChip, { StandardButton, StandardInput, StandardEmail, StandardPassword } from './Containers'
import ResponsiveDatePickers from './Callender'
import dayjs from 'dayjs';
import { EditUserDetails, OrganiserEditUserDetails } from './HTTP/User';
import { HandleOrganiserCreateVolunteer } from './HTTP/Account';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import TextField from '@mui/material/TextField';
import '../style/global.css';
import '../style/ui.css';
import '../style/pagespecific/dashboard.css';
import '../style/pagespecific/creVolunteer.css';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;

export const CreateOrEditUser = ({ setAllVolunteerInformation, open, setFunction, isEdit, userDetails, token, editingVolunteer = false }) => {
  const [onFrontSideOfPopup, setOnFrontSideOfPopup] = useState(true)

  const cardStyle = {
    width: '28vw',
    backgroundColor: '#b8c0c8'
  };
  const [firstname, setFirstNamename] = useState(isEdit ? userDetails.firstName : '');
  const [lastname, setLastName] = useState(isEdit ? userDetails.lastName : '');
  const [email, setEmail] = useState(isEdit ? userDetails.email : '');
  const [username, setUsername] = useState(isEdit ? userDetails.username : '');
  const [password, setPassword] = useState(isEdit ? userDetails.password : '');
  const [selectedValuesSkills, setSelectedValuesSkills] = useState([]);
  const [selectedValuesPreferences, setSelectedValuesPreferences] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);
  const [dateList, setDateList] = useState([])
  const [isVolunterManager, setIsVolunterManager] = useState(editingVolunteer && userDetails.role === 'Manager')
  const role = isEdit ? userDetails.role : 'Volunteer'

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
        borderRadius: '5px',
        boxShadow: 24,
        textAlign: 'center',
      }}>
        <Card sx={cardStyle}>
          <CardHeader
            title={<h2 style={{ margin: 0 }}>{ isEdit ? 'Edit Profile' : 'Create Profile' }</h2>}
            // subheader={'Expected time: ' + expectedTime} // + calculateTimeDifference(['2023-10-22', '08:00:00'], ['2023-10-22', '09:00:00'])}
          />
          <CardContent>
          {onFrontSideOfPopup
            ? <>
              {(!isEdit || editingVolunteer)
                ? <FormControlLabel label='Is Volunteer Manager' control={<Switch checked={isVolunterManager} onChange={(event) => {
                  setIsVolunterManager(event.target.checked)
                }} />}/>
                : <></>
              }
              <StandardInput stateValue={firstname} stateFunction={setFirstNamename} placeholder="First Name"/>
              <StandardInput stateValue={lastname} stateFunction={setLastName} placeholder="Last Name"/>
              <StandardEmail stateValue={email} stateFunction={setEmail} placeholder="Email"/>
              <StandardInput stateValue={username} stateFunction={setUsername} placeholder="User Name"/>
              <StandardPassword stateValue={password} stateFunction={setPassword} placeholder="Password"/>
              {role !== 'Organiser'
                ? <>
                  <SkillsBox selectedValuesSkills={selectedValuesSkills} setSelectedValuesSkills={setSelectedValuesSkills} />
                  <PreferencesBox selectedValuesPreferences={selectedValuesPreferences} setSelectedValuesPreferences={setSelectedValuesPreferences} />
                </>
                : <></>
              }
            </>
            : <>
              <div>
                <AvailibilityBox selectedDate={selectedDate} setSelectedDate={setSelectedDate} dateList={dateList} setDateList={setDateList} />
              </div>
            </>
          }
          </CardContent>
          <CardActions sx={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
          }}>
            <div>
            {(role !== 'Organiser' || editingVolunteer) && onFrontSideOfPopup
              ? <StandardButton onClick={() => { setOnFrontSideOfPopup(false) }} text="Set Availibility" />
              : <></>
            }
            {(role !== 'Organiser' || editingVolunteer) && !onFrontSideOfPopup
              ? <StandardButton onClick={() => { setOnFrontSideOfPopup(true) }} text="Set Details" />
              : <></>
            }
            </div>
            <div style={{ marginBottom: '2vh' }}>
              { !editingVolunteer
                ? <> { isEdit
                  ? <StandardButton onClick={() => {
                    role === 'Organiser'
                      ? EditUserDetails(firstname, lastname, username, password, email, '', '', '', token)
                      : EditUserDetails(firstname, lastname, username, password, email, selectedValuesSkills, selectedValuesPreferences, dateList, token)
                    setFunction(false)
                  }} text="Submit Edit" />
                  : <StandardButton onClick={() => {
                    HandleOrganiserCreateVolunteer(token, firstname, lastname, username, password, email, selectedValuesSkills, selectedValuesPreferences, dateList, isVolunterManager)
                    setFunction(false)
                  }} text="Submit Profile" />
                }</>
                : <StandardButton onClick={() => {
                  OrganiserEditUserDetails(firstname, lastname, username, password, email, selectedValuesSkills, selectedValuesPreferences, dateList, token, isVolunterManager, userDetails.username, setAllVolunteerInformation)
                  setFunction(false)
                }} text="Edit Profile" />
              }
            </div>
          </CardActions>
        </Card>
      </Box>
    </Modal>
  );
}

export const PreferencesBox = ({ selectedValuesPreferences, setSelectedValuesPreferences }) => {
  // stateFunction(e.target.value)
  return (
  <>
  <MultipleSelectChip
    realName={'Preferences'}
    names={['Pref A', 'Pref B', 'Pref C', 'Pref D', 'Pref E', 'Pref F']}
    menuProps={{
      PaperProps: {
        style: {
          maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
          maxWidth: '25px',
          overflow: 'auto'
        },
      },
    }}
    selectedValues={selectedValuesPreferences}
    setSelectedValues={setSelectedValuesPreferences}
    disableScrollLock={ true }
  />
  </>
  );
};

export const SkillsBox = ({ selectedValuesSkills, setSelectedValuesSkills }) => {
  // stateFunction(e.target.value)
  return (
  <>
  <MultipleSelectChip sx={{ backgroundColor: 'red' }}
  realName={'Skills'}
  names={['Skill 1', 'Skill 2', 'Skill 3', 'Skill 4', 'Skill 5', 'Skill 6']}
  menuProps={{
    PaperProps: {
      style: {
        maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
        maxWidth: '25px',
        overflow: 'auto'
      },
    },
  }}
  selectedValues={selectedValuesSkills}
  setSelectedValues={setSelectedValuesSkills}
  disableScrollLock={ true }
  />
  </>
  );
};

export const AvailibilityBox = ({ selectedDate, setSelectedDate, dateList, setDateList }) => {
  const handleDateChange = (date) => {
    setSelectedDate(date);
  };

  const handleAddDate = (date) => {
    const formattedDate = dayjs(date).format('DD-MM-YYYY');
    setDateList(prevDates => [...prevDates, formattedDate]);
    console.log('dateList:', dateList);
  }
  return (
  <>
  <p>Please select available day then press enter</p>
  <div className="callender-box">
    <ResponsiveDatePickers selectedDate={selectedDate} onDateChange={handleDateChange}></ResponsiveDatePickers>
  </div>
  <StandardButton onClick={() => handleAddDate(selectedDate)} text="Add Day"/>
  <TextField
    id="outlined-multiline-static"
    label="Dates Available"
    sx={{
      marginTop: '3vh',
      width: '60%',
      backgroundColor: 'white',
    }}
    inputProps={ { style: { textAlign: 'center', fontSize: 26, lineHeight: 1.3 } }}
    multiline
    rows={6}
    value={dateList.join('\n')}
    readOnly={true}
  />
  </>
  );
};
