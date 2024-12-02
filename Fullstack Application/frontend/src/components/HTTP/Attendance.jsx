import config from '../../config.json';

const BACKEND_PORT = config.BACKEND_PORT;

// Function to generate fake chat groups
const generateFakeChats = () => {
  const numberOfChats = 5; // Number of fake chat groups
  const chats = [];
  for (let i = 1; i <= numberOfChats; i++) {
    chats.push({
      id: i,
      name: `Chat Group ${i}`,
    });
  }
  return chats;
};

// Fake API function for getChats
export const getChatsFake = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const fakeChats = generateFakeChats();
      resolve(fakeChats);
    }, 500); // Simulating a delay of 500ms to mimic API request
  });
};

export const getMyTasks = (token) => {
  return fetch(`http://localhost:${BACKEND_PORT}/GetMyTasks`, {
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

export const taskLogin = (token, taskID) => {
  const DoPost = async () => {
    try {
      const currentDate = new Date();
      const year = currentDate.getFullYear();
      const month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Month is zero-based, so add 1
      const day = String(currentDate.getDate()).padStart(2, '0');
      const hours = String(currentDate.getHours()).padStart(2, '0');
      const minutes = String(currentDate.getMinutes()).padStart(2, '0');
      const seconds = String(currentDate.getSeconds()).padStart(2, '0');
      const dateString = `${year}-${month}-${day}-${hours}-${minutes}-${seconds}`;
      console.log(dateString);

      const response = await fetch(`http://localhost:${BACKEND_PORT}/LogInAttendance`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token
        },
        body: JSON.stringify({
          task_id: taskID,
          date: dateString
        })
      })
      const data = await response.json();
      if (!response.ok) {
        console.log('task login didnt work', data);
        if (data.message === 'User Already logged attendance.') {
          window.alert('Task already Logged in or finished. Try logout')
        }
      } else {
        window.alert('Login successful, goodluck at your task')
      }
    } catch (error) {
      console.log('ERROR', error);
    }
  };

  DoPost();
};

export const taskLogout = (token, taskID) => {
  const DoPost = async () => {
    try {
      const currentDate = new Date();
      const year = currentDate.getFullYear();
      const month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Month is zero-based, so add 1
      const day = String(currentDate.getDate()).padStart(2, '0');
      const hours = String(currentDate.getHours()).padStart(2, '0');
      const minutes = String(currentDate.getMinutes()).padStart(2, '0');
      const seconds = String(currentDate.getSeconds()).padStart(2, '0');
      const dateString = `${year}-${month}-${day}-${hours}-${minutes}-${seconds}`;
      console.log(dateString);

      const response = await fetch(`http://localhost:${BACKEND_PORT}/LogOutAttendance`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token
        },
        body: JSON.stringify({
          task_id: taskID,
          date: dateString
        })
      })
      const data = await response.json();
      if (!response.ok) {
        console.log(data.message);

        if (data.message === 'User was logged out already') {
          window.alert('Task has already been logged out or you havent logged in yet')
        }
      } else {
        console.log('task logout worked', data);
        window.alert('Logout successful, thanks for the hard work')
      }
    } catch (error) {
      console.log('ERROR', error);
    }
  };

  DoPost();
};
