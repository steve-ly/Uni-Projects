import {
  BrowserRouter,
  Route,
  Routes,
} from 'react-router-dom';
import background from './img/bigbrain_bg.png';
import React from 'react';
import Play from './Play';
import Login from './Login';
import Register from './Register';
import Dashboard from './Dashboard';
import Lobby from './Lobby';
import Logout from './Logout';
import QuestionScreen from './QuestionScreen';
import EditQuestion from './EditQuestion';
import EditGame from './EditGame';
import Results from './Results';
import LandingPage from './LandingPage'
import PlayerResult from './PlayerResults'
// function contains all routes
function App () {
  return (
    <>
    <link rel="preconnect" href="https://fonts.googleapis.com"></link>
    <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin></link>
    <link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&display=swap" rel="stylesheet"></link>
      <div style={ {
        backgroundImage: `url(${background})`,
        backgroundSize: 'cover',
        overflow: 'scroll',
        height: '100vh'
      } }>
        <BrowserRouter>
          <hr />
          <Routes>
            <Route path='/' element={<LandingPage />} />
            <Route path='/Play/:sessionIdFromURL?' element={<Play />} />
            <Route path="/Login" element={<Login />} />
            <Route path="/Register" element={<Register />} />
            <Route path='/Dashboard' element={<Dashboard />} />
            <Route path='/Lobby/:sessionId' element={<Lobby />} />
            <Route path='/QuestionScreen/:sessionId' element={<QuestionScreen />} />
            <Route path='/EditGame/:gameId' element={<EditGame />} />
            <Route path='/EditQuestion/:gameId/:questionId' element={<EditQuestion />} />
            <Route path='/PlayerResults' element={<PlayerResult />} />
            <Route path='/Results/:sessionId' element={<Results />} />
            <Route path='*' element={<Logout />} />
          </Routes>
          <Logout />
        </BrowserRouter>
      </div>
    </>
  );
}

export default App;
