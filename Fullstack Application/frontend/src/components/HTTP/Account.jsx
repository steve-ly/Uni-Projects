// HTTP FUNCTIONS RELATED TO THE ACCOUNT

import config from '../../config.json';

const BACKEND_PORT = config.BACKEND_PORT;

export const HandleCreateVolunteer = (firstName, lastName, userName, passWord, Email, Skills, Preferences, Availability, navigate, setToken) => {
  const DoCreateVolunteer = async () => {
    // window.alert('in');
    try {
      const body = {
        first_name: firstName,
        last_name: lastName,
        username: userName,
        password: passWord,
        email: Email,
        skills: JSON.stringify(Skills),
        preferences: JSON.stringify(Preferences),
        availability: JSON.stringify(Availability),
      }
      const response = await fetch(`http://localhost:${BACKEND_PORT}/CreateVolunteer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert(data.message);
      } else {
        setToken(data.token);
        navigate('/dashboard');
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoCreateVolunteer();
};

export const HandleCreateOrganiser = (firstName, lastName, userName, passWord, Email, navigate, setToken) => {
  const DoCreateOrganiser = async () => {
    // window.alert('in');
    try {
      const body = {
        first_name: firstName,
        last_name: lastName,
        username: userName,
        password: passWord,
        email: Email
      }
      const response = await fetch(`http://localhost:${BACKEND_PORT}/CreateOrganiser`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert(data.message);
      } else {
        setToken(data.token);
        navigate('/dashboard');
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoCreateOrganiser();
};

export const HandleOrganiserCreateVolunteer = (token, firstName, lastName, userName, passWord, Email, Skills, Preferences, Availability, isVolunterManager) => {
  const DoCreateVolunteer = async () => {
    // window.alert('in');
    try {
      const body = {
        first_name: firstName,
        last_name: lastName,
        username: userName,
        password: passWord,
        email: Email,
        skills: JSON.stringify(Skills),
        preferences: JSON.stringify(Preferences),
        availability: JSON.stringify(Availability),
        manager: isVolunterManager
      }
      const response = await fetch(`http://localhost:${BACKEND_PORT}/CreateVolunteer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', token: token },
        body: JSON.stringify(body)
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert(data.message);
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoCreateVolunteer();
};
