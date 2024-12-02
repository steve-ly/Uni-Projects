import React, { useContext, useState } from 'react';
import { AuthContext } from './AuthContext';
import { TopTitle, StandardInput, StandardEmail, StandardPassword, StandardButton } from './Containers'
import { PreferencesBox, SkillsBox, AvailibilityBox } from './UserElements'
import { HandleCreateVolunteer } from './HTTP/Account';

import '../style/pagespecific/creVolunteer.css';

import { useNavigate } from 'react-router-dom';

const CreateVolunteerPage = () => {
  const { setToken } = useContext(AuthContext);

  const navigate = useNavigate()
  function navigateToLogin () { navigate('/login') }

  const [firstname, setFirstNamename] = useState('');
  const [lastname, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [selectedValuesSkills, setSelectedValuesSkills] = useState([]);
  const [selectedValuesPreferences, setSelectedValuesPreferences] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);
  const [dateList, setDateList] = useState([])

  return (
    <>
    <TopTitle text="✷ Welcome Volunteer ✷" />
    <div className='second-title'>Please create your account</div>
    <div className="vol-flex-container">
      <div className="vol-flex-item">
        <h2 className='mini-headers'>Personal Details</h2>

        <StandardInput stateValue={firstname} stateFunction={setFirstNamename} placeholder="First Name"/>
        <StandardInput stateValue={lastname} stateFunction={setLastName} placeholder="Last Name"/>
        <StandardEmail stateValue={email} stateFunction={setEmail} placeholder="Email"/>
        <StandardInput stateValue={username} stateFunction={setUsername} placeholder="User Name"/>
        <StandardPassword stateValue={password} stateFunction={setPassword} placeholder="Password"/>
        <StandardPassword stateValue={password2} stateFunction={setPassword2} placeholder="Confirm Password"/>

      </div>
      <div className="vol-flex-item">
        <h2 style={{ marginBottom: '2vh' }} className='mini-headers'>Skills & Preferences</h2>
        <SkillsBox selectedValuesSkills={selectedValuesSkills} setSelectedValuesSkills={setSelectedValuesSkills} />
        <PreferencesBox selectedValuesPreferences={selectedValuesPreferences} setSelectedValuesPreferences={setSelectedValuesPreferences} />
        <StandardButton onClick={() => {
          HandleCreateVolunteer(firstname, lastname, username, password, email, selectedValuesSkills, selectedValuesPreferences, dateList, navigate, setToken)
        }} text="Submit" />
        {' '}
        <StandardButton onClick={navigateToLogin} text="Cancel" />

      </div>
      <div className="vol-flex-item">
        <h2 style={{ marginBottom: '2vh' }} className='mini-headers'>Availability</h2>
        <AvailibilityBox selectedDate={selectedDate} setSelectedDate={setSelectedDate} dateList={dateList} setDateList={setDateList} />
      </div>
    </div>

    </>
  );
};

export default CreateVolunteerPage;
