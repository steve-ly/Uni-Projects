// HTTP FUNCTIONS RELATED TO THE USER

import config from '../../config.json';

const BACKEND_PORT = config.BACKEND_PORT;

export const HandleLogout = (token, setToken, navigate) => {
  const DoLogout = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/LogOut`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        }
      })
      if (!response.ok) {
        window.alert('Logout failed');
        return;
      }
      setToken(null);
      localStorage.setItem('token', null)
      navigate('/login');
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoLogout();
};

export const HandleLogin = (username, password, setToken, navigate) => {
  const DoLogin = async () => {
    try {
      const body = {
        username: username,
        password: password
      }
      const response = await fetch(`http://localhost:${BACKEND_PORT}/LogIn`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      if (!response.ok) {
        window.alert('Invalid username or password');
        return;
      }
      const data = await response.json();
      setToken(data.token);
      localStorage.setItem('token', data.token)
      navigate('/dashboard');
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoLogin();
};

export const GetUserDetails = (token, setUserDetails, setConferenceID = () => {}) => {
  const DoLogin = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/GetUserDetails`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('GetUserDetails Failed');
      } else {
        setUserDetails(data);
        setConferenceID(data.conference_id)
        console.log(data)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoLogin();
};

export const GetUserRole = (token, setUserRole) => {
  const DoLogin = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/GetUserDetails`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('GetUserRole Failed');
      } else {
        setUserRole(data.role)
        console.log(data)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoLogin();
};

export const EditUserDetails = (firstName, lastName, userName, passWord, Email, Skills, Preferences, Availability, token) => {
  const DoEdit = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/EditUserDetails`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          target_username: '',
          first_name: firstName,
          last_name: lastName,
          username: userName,
          password: passWord,
          email: Email,
          skills: JSON.stringify(Skills),
          preferences: JSON.stringify(Preferences),
          availability: JSON.stringify(Availability),
        })
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('GetUserDetails Failed');
      } else {
        console.log(data)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoEdit();
};

export const GetAllVolunteerInformation = (token, setAllVolunteerInformation) => {
  const DoUsers = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/GetAllVolunteers`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('GetUserDetails Failed');
      } else {
        setAllVolunteerInformation(data);
        console.log(data)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoUsers();
};

export const VolunteersInConference = (conferenceID, setAllVolunteersInConference) => {
  const DoUsers = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/VolunteersInConference/${conferenceID}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('GetUserDetails Failed');
      } else {
        setAllVolunteersInConference(data);
        console.log(data)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoUsers();
};

export const SubmitFeedback = (submitterName, volunteerID, feedback, score) => {
  const DoFeedback = async () => {
    try {
      const body = {
        user_id: volunteerID,
        name: submitterName,
        feedback: feedback,
        score: score
      }
      const response = await fetch(`http://localhost:${BACKEND_PORT}/SubmitFeedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      await response;
      if (!response.ok) {
        window.alert('Invalid feedback');
        return;
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoFeedback();
};

export const AddManagerRating = (volunteerID, score, token, setAllVolunteerInformation) => {
  const DoFeedback = async () => {
    try {
      const body = {
        user_id: volunteerID,
        score: score
      }
      const response = await fetch(`http://localhost:${BACKEND_PORT}/ManagerSubmitScore`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify(body)
      })
      await response;
      if (!response.ok) {
        window.alert('Invalid rating');
        return;
      } else {
        GetAllVolunteerInformation(token, setAllVolunteerInformation)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoFeedback();
};

export const OrganiserEditUserDetails = (firstName, lastName, userName, passWord, Email, Skills, Preferences, Availability, token, manager, targetusername, setAllVolunteerInformation) => {
  const DoEdit = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/EditUserDetails`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          target_username: targetusername,
          first_name: firstName,
          last_name: lastName,
          username: userName,
          password: passWord,
          email: Email,
          skills: JSON.stringify(Skills),
          preferences: JSON.stringify(Preferences),
          availability: JSON.stringify(Availability),
          manager: manager
        })
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('Editing User Failed');
      } else {
        console.log(data)
        GetAllVolunteerInformation(token, setAllVolunteerInformation)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoEdit();
};

export const ShareConference = (token) => {
  const DoShare = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/ShareConferenceSchedule`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        }
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('Sharing Conference with Users Failed');
      } else {
        console.log(data)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };
  DoShare();
};

export const ShareTask = (token) => {
  const DoShare = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/ShareTaskAssignment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        }
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('Sharing Conference with Users Failed');
      } else {
        console.log(data)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };
  DoShare();
};

export const GetTopUsers = (token, setTop) => {
  const DoTop = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/GetTopVolunteers`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          token: token
        }
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('Getting top Users Failed');
      } else {
        console.log(data)
        setTop(data)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };
  DoTop();
};

export const GetUserDetailsSimple = async (token) => {
  try {
    const response = await fetch(`http://localhost:${BACKEND_PORT}/GetUserDetails`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        token: token
      },
    });

    if (!response.ok) {
      window.alert('GetUserDetails Failed');
      throw new Error('GetUserDetails Failed'); // You might want to throw an error here to handle it in the calling code
    }

    const data = await response.json();
    console.log('Data for name:', data);
    return data;
  } catch (error) {
    console.error('ERROR:', error);
    throw error; // Rethrow the error to handle it in the calling code
  }
};
