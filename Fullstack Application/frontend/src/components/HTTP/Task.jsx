// HTTP FUNCTIONS RELATED TO THE USER

import config from '../../config.json';

const BACKEND_PORT = config.BACKEND_PORT;

export const GetAllTasks = (token, setAllTasks) => {
  const DoTask = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/${localStorage.getItem('filterapi')}`, {
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
        setAllTasks(data)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoTask();
};

export const GetAllScheduleTasks = (token, setAllTasks) => {
  const DoTask = async () => {
    const response = await fetch(`http://localhost:${BACKEND_PORT}/${localStorage.getItem('filterapi')}`, {
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
      var finalres = []
      for (var i = 0; i !== data.length; i++) {
        finalres.push(
          {
            id: i,
            start: data[i].task.start_time[0] + ' ' + data[i].task.start_time[1],
            end: data[i].task.end_time[0] + ' ' + data[i].task.end_time[1],
            resourceId: 'r1',
            title: data[i].task.name,
            bgColor: 'black',
          }
        )
      }
      setAllTasks(finalres)
    }
  };

  DoTask();
};

export const CreateTask = (token, name, description, startTime, endTime, skills, setAllTasks) => {
  const DoTask = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/CreateTask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          name: name,
          description: description,
          start_time: startTime,
          end_time: endTime,
          skills_recommended: JSON.stringify(skills),
        })
      })
      await response;
      if (!response.ok) {
        window.alert('Invalid Task');
      } else {
        GetAllTasks(token, setAllTasks)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoTask();
};

export const EditTask = (token, taskID, name, description, startTime, endTime, skills, setAllTasks) => {
  const DoTask = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/EditTask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          task_id: taskID,
          name: name,
          description: description,
          start_time: startTime,
          end_time: endTime,
          skills_recommended: JSON.stringify(skills),
        })
      })
      await response;
      if (!response.ok) {
        window.alert('Invalid Task');
      } else {
        GetAllTasks(token, setAllTasks)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoTask();
};

export const ForceAddVolunteerToTask = (token, volunteerID, taskID, setAllTasks) => {
  const DoTask = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/ForceJoinTask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          user_id: volunteerID,
          task_id: taskID,
        })
      })
      await response;
      if (!response.ok) {
        window.alert('Invalid Task');
      } else {
        GetAllTasks(token, setAllTasks)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoTask();
};

export const RemoveVolunteerFromTask = (token, volunteerID, taskID, setAllTasks) => {
  const DoTask = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/RemoveVolunteerFromTask`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          user_id: volunteerID,
          task_id: taskID,
        })
      })
      await response;
      if (!response.ok) {
        window.alert('Invalid Task');
      } else {
        GetAllTasks(token, setAllTasks)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoTask();
};

export const ToggleTaskComplete = (token, taskID, setAllTasks) => {
  const DoTask = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/ToggleTaskComplete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          task_id: taskID,
        })
      })
      await response;
      if (!response.ok) {
        window.alert('Invalid Task');
      } else {
        GetAllTasks(token, setAllTasks)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoTask();
};

export const RequestAddVolunteerToTask = (token, userID, taskID, setAllTasks) => {
  const DoTask = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/JoinTask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          user_id: userID,
          task_id: taskID,
        })
      })
      await response;
      if (!response.ok) {
        window.alert('Invalid Task');
      } else {
        GetAllTasks(token, setAllTasks)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoTask();
};

export const ApproveRequest = (token, userID, taskID, setAllTasks) => {
  const DoTask = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/ApproveRequest`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          user_id: userID,
          task_id: taskID,
        })
      })
      await response;
      if (!response.ok) {
        window.alert('Invalid Task');
      } else {
        GetAllTasks(token, setAllTasks)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoTask();
};

export const DeleteTask = (token, taskID, setAllTasks) => {
  const DoTask = async () => {
    try {
      const response = await fetch(`http://localhost:${BACKEND_PORT}/DeleteTask`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          token: token
        },
        body: JSON.stringify({
          id: taskID,
        })
      })
      await response;
      if (!response.ok) {
        window.alert('Invalid Task');
      } else {
        GetAllTasks(token, setAllTasks)
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoTask();
};
