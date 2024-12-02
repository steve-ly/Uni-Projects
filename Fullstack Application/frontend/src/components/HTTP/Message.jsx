// HTTP FUNCTIONS RELATED TO THE Message

import config from '../../config.json';

const BACKEND_PORT = config.BACKEND_PORT;

export const getChats = async (token) => {
  try {
    const response = await fetch('/GetChats', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    const data = await response.json();
    return data.chats;
  } catch (error) {
    console.error('Error fetching chats:', error);
    throw error;
  }
};

export const getMessages = async (groupId, token) => {
  try {
    const response = await fetch('/GetMessages', {
      method: 'POST',
      headers: {
        ContentType: 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ group_id: groupId })
    });
    const data = await response.json();
    return data.members;
  } catch (error) {
    console.error('Error fetching messages:', error);
    throw error;
  }
};

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

// Function to generate fake messages for a chat group
const generateFakeMessages = (groupId) => {
  const numberOfMessages = 10; // Number of fake messages per chat group
  const messages = [];
  for (let i = 1; i <= numberOfMessages; i++) {
    messages.push({
      sender_id: i % 3 === 0 ? 1 : 2, // Alternating between two users for variety
      content: `Message ${i} in Chat Group ${groupId}`,
      time_send: new Date().toISOString(),
    });
  }
  return messages;
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

// Fake API function for getMessages
export const getMessagesFake = (groupId) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const fakeMessages = generateFakeMessages(groupId);
      resolve(fakeMessages);
    }, 500); // Simulating a delay of 500ms to mimic API request
  });
};

export const handleSendMessage = async (mes, chatId) => {
  console.log(`sent ${mes} too ${chatId}`);
};

export const getAllChats = (token) => {
  return fetch(`http://localhost:${BACKEND_PORT}/GetChats`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Request failed');
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      return data;
    })
    .catch((error) => {
      console.error('Error:', error);
      throw error;
    });
};

export const getAllMessages = (token, groupId) => {
  return fetch(`http://localhost:${BACKEND_PORT}/GetMessages`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      token,
      groupid: groupId
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Request failed');
      }
      return response.json();
    })
    .then((data) => {
      // console.log('The data', data);
      return data;
    })
    .catch((error) => {
      console.error('Error:', error);
      throw error;
    });
};

export const myPost = (token, groupID, message) => {
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

      const response = await fetch(`http://localhost:${BACKEND_PORT}/SendMessage`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          token,
        },
        body: JSON.stringify({
          group_id: groupID,
          content: message,
          timesent: dateString
        })
      })
      const data = await response.json();
      if (!response.ok) {
        window.alert('didnt work');
      } else {
        console.log('send message worked', data);
      }
    } catch (error) {
      console.log('ERROR');
    }
  };

  DoPost();
};
