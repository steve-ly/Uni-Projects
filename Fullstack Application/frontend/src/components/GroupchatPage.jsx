import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from './AuthContext';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Fab from '@mui/material/Fab';
import SendIcon from '@material-ui/icons/Send';
import { TopTitle, LogoutAndDashboardIcons } from './Containers';
import { getAllChats, getAllMessages, myPost } from './HTTP/Message';

// Based off: https://medium.com/@awaisshaikh94/chat-component-built-with-react-and-material-ui-c2b0d9ccc491
const GroupchatPage = () => {
  const { user } = useContext(AuthContext);
  const { token } = useContext(AuthContext);
  const [chats, setChats] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [userId, setUserId] = useState(null);
  useEffect(() => {
    // When the component mounts or user context changes, update the userId state
    if (user) {
      setUserId(user.id);
    }
    setUserId(1); // just set to 1, if is wasted
  }, []); // Run the effect whenever the user context changes

  // get all messages
  useEffect(() => {
    const fetchMessagesForSelectedChat = async () => {
      if (selectedChat) {
        try {
          const chatMessages3 = await getAllMessages(token, selectedChat.id);
          setMessages(chatMessages3.messages);
        } catch (error) {
          console.error('Error fetching chat messages:', error);
        }
      }
    };

    fetchMessagesForSelectedChat();
  }, [selectedChat, newMessage]); // Run the effect whenever selectedChat or token changes

  useEffect(() => {
    const fetchChatsData = async () => {
      try {
        const chatGroups = await getAllChats(token);
        setChats(chatGroups.chats);
      } catch (error) {
        console.error('Error fetching chat groups in test:', error);
      }
    };

    fetchChatsData();
  }, []); // Run the effect whenever the token changes

  const handleSendMessageClick = async () => {
    if (newMessage.trim() === '') {
      // Do not send empty messages
      return;
    }

    try {
      // Call the send message function
      await myPost(token, selectedChat.id, newMessage);
      // Clear the message input field after sending the message
      setNewMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  // this guy polls the backend every 3 seconds to get new messages from other users
  useEffect(() => {
    const fetchMessagesForSelectedChat4 = async () => {
      if (selectedChat) {
        try {
          const chatMessages3 = await getAllMessages(token, selectedChat.id);
          setMessages(chatMessages3.messages);
        } catch (error) {
          console.error('Error fetching chat messages:', error);
        }
      }
    };
    // Set up an interval to call the function every 3 seconds
    const intervalId = setInterval(fetchMessagesForSelectedChat4, 3000);

    // Clean up the interval when the component unmounts or selectedChat changes
    return () => clearInterval(intervalId);
  }, [selectedChat]);

  return (
    <>
      <TopTitle text="✫ Group Chat ✫" />
      <LogoutAndDashboardIcons/>
      <div>
        <Grid container>
          <Grid item xs={3}>
            <List style={{ width: '100%', height: '80vh', overflowY: 'auto' }}>
              {chats.map((chat) => (
                <ListItem button key={chat.id} onClick={() => setSelectedChat((prevChat) => chat)}>
                  <ListItemText primary={chat.name} />
                </ListItem>
              ))}
            </List>
          </Grid>
          <Grid item xs={9}>
            <List style={{ height: '70vh', overflowY: 'auto' }} >
              {messages.map((message, index) => (
                <ListItem key={index}>
                  <Grid container>
                    <Grid item xs={12}>
                      <ListItemText
                        align={message.sender_id === userId ? 'right' : 'left'}
                        primary={message.content}
                      />
                    </Grid>
                    <Grid item xs={12}>
                      <ListItemText
                        align={message.sender_id === userId ? 'right' : 'left'}
                        secondary={message.username}
                      />
                    </Grid>
                    <Grid item xs={12}>
                      <ListItemText
                        align={message.sender_id === userId ? 'right' : 'left'}
                        secondary={message.time_send}
                      />
                    </Grid>
                  </Grid>
                </ListItem>
              ))}
            </List>
            {/* Message Input and Send Button */}
            <Divider />
            <Grid container style={{ padding: '20px' }}>
              <Grid item xs={11}>
                <TextField
                  label="Type Something"
                  fullWidth
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                />
              </Grid>
              <Grid item xs={1} align="right"> {/* Fixed: xs prop inside item */}
                <Fab color="primary" aria-label="add" onClick={() => handleSendMessageClick()}>
                  <SendIcon />
                </Fab>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </div>
    </>
  );
};

export default GroupchatPage;
