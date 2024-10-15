import axios from 'axios';
// import { BACKEND_PORT } from './config.json';
const BACKEND_PORT = 5005;
// Backend calls for players
// allows user to join active session
async function callJoinSession (sessionId, name) {
  try {
    const response = await axios.post(`http://localhost:${BACKEND_PORT}/play/join/${sessionId}`, {
      name
    }, {
      headers: {
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
    const playerId = response.data.playerId;
    return (playerId);
  } catch (error) {
    console.error(error);
    return Promise.reject(error);
  }
}
// gets the player status
export async function callPlayerStatus (playerId) {
  try {
    const response = await axios.get(`http://localhost:${BACKEND_PORT}/play/${playerId}/status`, {
      headers: {
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
    return response.data.started;
  } catch (error) {
    console.error(error);
  }
}

export async function callPlayerQuestion (playerId) {
  try {
    const response = await axios.get(`http://localhost:${BACKEND_PORT}/play/${playerId}/question`, {
      headers: {
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
    const playerStatus = response.data;
    return playerStatus;
  } catch (error) {
    console.error(error);
    return Promise.reject(error);
  }
}

export async function callPlayerAnswer (playerId) {
  try {
    const response = await axios.get(`http://localhost:${BACKEND_PORT}/play/${playerId}/answer`, {
      headers: {
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
    const playerStatus = response.data;
    return playerStatus;
  } catch (error) {
    console.error(error);
    return Promise.reject(error);
  }
}

export async function callPlayerSubmit (playerId, answerIds) {
  try {
    const response = await axios.put(`http://localhost:${BACKEND_PORT}/play/${playerId}/answer`, {
      answerIds
    }, {
      headers: {
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
    const playerStatus = response.data;
    return playerStatus;
  } catch (error) {
    console.error(error);
    return Promise.reject(error);
  }
}

export async function callPlayerResults (playerId) {
  try {
    const response = await axios.get(`http://localhost:${BACKEND_PORT}/play/${playerId}/results`, {
      headers: {
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
    const playerStatus = response.data;
    return playerStatus;
  } catch (error) {
    console.error(error);
    return Promise.reject(error);
  }
}

export default callJoinSession;
