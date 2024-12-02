import config from '../../config.json';

const BACKEND_PORT = config.BACKEND_PORT;

export const getAllAttendance = (token) => {
  return fetch(`http://localhost:${BACKEND_PORT}/GetAllAttendance`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Request failed');
      }
      return response.json();
    })
    .then((data) => {
      console.log('The data', data);
      return data;
    })
    .catch((error) => {
      console.error('Error:', error);
      throw error;
    });
};

export const getTaskAttendance = (token, taskid) => {
  return fetch(`http://localhost:${BACKEND_PORT}/GetTaskAttendance`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
      taskid
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Request failed');
      }
      return response.json();
    })
    .then((data) => {
      console.log('The data for task attendance', data);
      return data;
    })
    .catch((error) => {
      console.error('Error:', error);
      throw error;
    });
};

export const approveAttendance = (token, taskID, userID) => {
  return fetch(`http://localhost:${BACKEND_PORT}/ApproveAttendance`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      token
    },
    body: JSON.stringify({
      task_id: taskID,
      user_id: userID
    })
  })
    .then((response) => {
      if (!response.ok) {
        // throw new Error('Request failed');
        console.error('Error:', response);
      }
      return response.json();
    })
    .then((data) => {
      console.log('The data', data);
      return data;
    })
    .catch((error) => {
      console.error('Error:', error);
      throw error;
    });
};

export const getAllTasks = (token) => {
  return fetch(`http://localhost:${BACKEND_PORT}/GetAllTasks`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Request failed');
      }
      return response.json();
    })
    .then((data) => {
      console.log('The data', data);
      return data;
    })
    .catch((error) => {
      console.error('Error:', error);
      throw error;
    });
};
