import { React, useState, useContext } from 'react';
import { AuthContext } from './AuthContext';
import { TopTitle, StandardInput, StandardEmail, StandardPassword, StandardButton } from './Containers'
import '../style/pagespecific/creOrganiser.css';
import { useNavigate } from 'react-router-dom';
import { HandleCreateOrganiser } from './HTTP/Account';

const CreateOrganiserPage = () => {
  const { setToken } = useContext(AuthContext);

  const navigate = useNavigate()
  function navigateToLogin () { navigate('/login') }

  const [firstname, setFirstNamename] = useState('');
  const [lastname, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');

  return (
    <>
    <TopTitle text="✷ Welcome Organiser ✷" />
    <div className='second-title'>Please create your account</div>
    <div className="org-flex-container">
        <div className="flex-item">
          <h2>Personal Details</h2>
            <StandardInput stateValue={firstname} stateFunction={setFirstNamename} placeholder="First Name"/>
            <StandardInput stateValue={lastname} stateFunction={setLastName} placeholder="Last Name"/>
            <StandardEmail stateValue={email} stateFunction={setEmail} placeholder="Email"/>
        </div>
        <div className="flex-item">
          <h2>Account Details</h2>
            <StandardInput stateValue={username} stateFunction={setUsername} placeholder="User Name"/>
            <StandardPassword stateValue={password} stateFunction={setPassword} placeholder="Password"/>
            <StandardPassword stateValue={password2} stateFunction={setPassword2} placeholder="Confirm Password"/>
        </div>
      </div>
      <div className='double-but-flex-container'>
        <div className="org-flex-item">
          <StandardButton onClick={ () => HandleCreateOrganiser(firstname, lastname, username, password, email, navigate, setToken)} text="Submit"/>
        </div>
        <div className="org-flex-item">
        <StandardButton onClick={navigateToLogin} text="Cancel" />
        </div>
      </div>
    </>
  );
};

export default CreateOrganiserPage;
