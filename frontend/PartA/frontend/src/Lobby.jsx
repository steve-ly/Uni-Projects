import React, { useState, useEffect } from 'react';
import logo from './img/bigbrain_logo_1.png';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import lobbyGif from './img/lobby_loading.gif';
import { callPlayerStatus } from './Player';
import lobbyMusic from './music/lobby_music.mp3';
// When game session starts but not advance render lobby with music and poll server until session advances
export default function Lobby () {
  let { sessionId } = useParams();
  sessionId = parseInt(sessionId);
  const { playerId } = useLocation().state;
  const [state, setState] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const audio = new Audio(lobbyMusic);
    audio.volume = 0.1;
    audio.loop = true;
    audio.play();

    return () => {
      audio.pause();
      audio.currentTime = 0;
    };
  }, []);

  useEffect(() => {
    const apiPoll = setInterval(async () => { // Make the callback function async
      try {
        const response = await callPlayerStatus(playerId);
        console.log(response)
        if (response !== false) {
          setState(response);
          navigate(`/QuestionScreen/${sessionId}`, { state: { playerId } });
        }
      } catch (error) {
        console.error(error);
      }
    }, 1000);

    return () => {
      clearInterval(apiPoll);
    }
  }, [state])

  return (
    <>
      <div style={{ textAlign: 'center' }}>
        <div>
          <img src={logo} alt="bigbrain_logo" className='fluid'/>
        </div>
        <span
            className="w-100 p-2"
            style={{
              fontFamily: 'Alfa Slab One',
              fontSize: '30px',
              color: 'white',
            }}
          >
            Session ID:
          </span>
        <div
          className="d-flex mx-auto"
          style={{
            backgroundColor: '#ea6d9d',
            textAlign: 'center',
            width: '300px',
          }}
        >
          <span
            className="w-100 p-2"
            style={{
              fontFamily: 'Alfa Slab One',
              fontSize: '30px',
              color: 'white',
            }}
          >
            {sessionId}
          </span>
        </div>
        <img src={lobbyGif} alt="lobby_gif" />
        <div style={{ textAlign: 'center' }}>
            <h1 style={{ fontFamily: 'Alfa Slab One', fontSize: '50px', color: 'white', textAlign: 'center', letterSpacing: '1px' }}>Get Ready!</h1>
        </div>
      </div>
    </>
  );
}
