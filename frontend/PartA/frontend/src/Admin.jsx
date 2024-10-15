// This file contains admin api calls for quizzes and sessions

import axios from 'axios';
const BACKEND_PORT = 5005;

// Get meta data of all quizzes owned by admin
export async function callGetQuizzes () {
  try {
    const userToken = localStorage.getItem('token');
    console.log(userToken)
    const response = await axios.get(`http://localhost:${BACKEND_PORT}/admin/quiz`,
      {
        headers: {
          Authorization: 'Bearer ' + userToken,
          accept: 'application/json',
          'Content-Type': 'application/json'
        }
      });
    const quizzes = response.data.quizzes;
    return quizzes;
  } catch (error) {
    console.error(error);
  }
}
// Creates a new quiz
export async function callNewQuiz (name) {
  const userToken = localStorage.getItem('token');
  try {
    await axios.post(`http://localhost:${BACKEND_PORT}/admin/quiz/new`, {
      name,
    }, {
      headers: {
        Authorization: 'Bearer ' + userToken,
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error(error);
  }
}
// Gets unique quiz by quiz id
export async function callGetUniqueQuiz (quizId) {
  try {
    const userToken = localStorage.getItem('token');
    const response = await axios.get(`http://localhost:${BACKEND_PORT}/admin/quiz/${quizId}`, {
      headers: {
        Authorization: 'Bearer ' + userToken,
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
    const quiz = response.data;
    return quiz
  } catch (error) {
    console.error(error);
  }
}
// Make changes to the quiz
export async function callUpdateQuiz (quizId, questions, name) {
  try {
    console.log(questions)
    const userToken = localStorage.getItem('token');
    await axios.put(`http://localhost:${BACKEND_PORT}/admin/quiz/${quizId}`, {
      questions,
      name
    }, {
      headers: {
        Authorization: 'Bearer ' + userToken,
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error(error);
  }
}
// make changes to just the quiz thumbnail
export async function callUpdateQuizThumbnail (quizId, questions, name, thumbnail) {
  try {
    console.log(questions)
    const userToken = localStorage.getItem('token');
    await axios.put(`http://localhost:${BACKEND_PORT}/admin/quiz/${quizId}`, {
      questions,
      name,
      thumbnail
    }, {
      headers: {
        Authorization: 'Bearer ' + userToken,
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error(error);
  }
}
// delete a quiz
export async function callDeleteQuiz (quizId) {
  try {
    const userToken = localStorage.getItem('token');
    await axios.delete(`http://localhost:${BACKEND_PORT}/admin/quiz/${quizId}`, {
      headers: {
        Authorization: 'Bearer ' + userToken,
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error(error);
  }
}
// starts quiz session
export async function callStartQuiz (quizId) {
  try {
    const userToken = localStorage.getItem('token');
    await axios.post(`http://localhost:${BACKEND_PORT}/admin/quiz/${quizId}/start`, {}, {
      headers: {
        Authorization: 'Bearer ' + userToken,
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error(error);
  }
}
// progress quiz session
export async function callAdvanceQuiz (quizId) {
  try {
    const userToken = localStorage.getItem('token');
    await axios.post(`http://localhost:${BACKEND_PORT}/admin/quiz/${quizId}/advance`, {
    }, {
      headers: {
        Authorization: 'Bearer ' + userToken,
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error(error);
  }
}
// End quiz session
export async function callEndQuiz (quizId) {
  try {
    const userToken = localStorage.getItem('token');
    await axios.post(`http://localhost:${BACKEND_PORT}/admin/quiz/${quizId}/end`, {
    }, {
      headers: {
        Authorization: 'Bearer ' + userToken,
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error(error);
    throw error;
  }
}
// Get current session stats
export async function callGetSessionStatus (sessionId) {
  try {
    const userToken = localStorage.getItem('token');
    const response = await axios.get(`http://localhost:${BACKEND_PORT}/admin/session/${sessionId}/status`, {
      headers: {
        Authorization: 'Bearer ' + userToken,
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
    const status = response.data;
    return status;
  } catch (error) {
    console.error(error);
    return Promise.reject(error);
  }
}
// gets session results
export async function callGetSessionResults (sessionId) {
  try {
    const userToken = localStorage.getItem('token');
    const response = await axios.get(`http://localhost:${BACKEND_PORT}/admin/session/${sessionId}/results`, {
      headers: {
        Authorization: 'Bearer ' + userToken,
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
    const results = response.data;
    return results;
  } catch (error) {
    console.error(error);
    return Promise.reject(error);
  }
}
