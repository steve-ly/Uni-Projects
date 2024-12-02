// HTTP FUNCTIONS RELATED TO THE USER

import config from '../../config.json';

const BACKEND_PORT = config.BACKEND_PORT;

export const GetAllConferences = (token, setAllConferences) => {
  const DoConference = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/GetAllConferences`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          token: token
        }
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('Invalid conference name');
      } else {
        setAllConferences(data)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoConference();
};

export const GetAllConferencesLoginPage = (setAllConferences) => {
  const DoConference = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/GetConferences`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('Invalid conference name');
      } else {
        setAllConferences(data)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoConference();
};

export const CreateConference = (token, createConferenceName, setConferenceID) => {
  const DoConference = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/CreateConference`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          name: createConferenceName,
          start_date: '01/01/1999 01:01:01',
          end_date: '01/01/1999 01:01:02',
        })
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('Invalid conference name');
      } else {
        setConferenceID(data.id)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoConference();
};

export const JoinConference = (token, conferenceId) => {
  const DoConference = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/JoinConference`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          conference_id: conferenceId
        })
      })
      const data = await response;
      if (!response.ok) {
        window.alert('Invalid conference ID');
      } else {
        console.log(data)
      }
    } catch (error) {
      console.log('ERROR');
      console.log(error)
    }
  };

  DoConference();
};

export const GetConferenceName = (token, setConferenceName) => {
  const DoConference = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/GetConferenceDetails`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          token: token
        }
      })
      const data = await response.json();
      if (response.ok) {
        console.log(data)
        setConferenceName(data.name)
      }
    } catch (error) {
      console.log('ERROR');
      console.log(error)
    }
  };

  DoConference();
};

export const LeaveConference = (token, setConferenceID, setConferenceName) => {
  const DoConference = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/LeaveConference`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        }
      })
      await response;
      if (!response.ok) {
        window.alert('Failed to leave conference');
      } else {
        setConferenceID(null)
        setConferenceName('')
      }
    } catch (error) {
      console.log('ERROR');
      console.log(error)
    }
  };

  DoConference();
};

export const GetConferenceVolunteers = (token, setConferenceVolunteers) => {
  const DoConference = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/GetConferenceDetails`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          token: token
        }
      })
      const data = await response.json();
      if (response.ok) {
        console.log(data)
        setConferenceVolunteers(data.volunteers)
      }
    } catch (error) {
      console.log('ERROR');
      console.log(error)
    }
  };

  DoConference();
};

// Same as above except pass in an array which we subtract conference volunteers from
export const GetAssignableVolunteers = (token, setAssignableVolunteers, arr) => {
  const DoConference = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/GetConferenceDetails`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          token: token
        }
      })
      const data = await response.json();
      if (response.ok) {
        console.log(data)
        setAssignableVolunteers(data.volunteers.filter(item1 => !arr.some(item2 => item1.id === item2.id)))
      }
    } catch (error) {
      console.log('ERROR');
      console.log(error)
    }
  };

  DoConference();
};

export const EditConferenceDetails = (token, startdate, enddate, name, setConferenceName, setAllConferences) => {
  const DoConference = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/EditConferenceDetails`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          start_date: startdate,
          end_date: enddate,
          name: name,
        })
      })
      const data = await response.json();
      if (response.ok) {
        console.log(data)
        GetConferenceName(token, setConferenceName)
        GetAllConferences(token, setAllConferences)
      }
    } catch (error) {
      console.log('ERROR');
      console.log(error)
    }
  };

  DoConference();
};
