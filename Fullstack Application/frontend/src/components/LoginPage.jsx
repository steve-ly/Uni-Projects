import { React, useState, useContext, useEffect } from 'react';
import { StandardButton, TopTitle, StandardInput } from './Containers'
import { useNavigate } from 'react-router-dom';
import { GetAllConferencesLoginPage } from './HTTP/Conference';
import { UseConfirmation } from './ConfirmationElement';
import { HandleLogin, VolunteersInConference, SubmitFeedback } from './HTTP/User';
import { AuthContext } from './AuthContext';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Rating from '@mui/material/Rating';
import '../style/global.css';
import '../style/ui.css';
import '../style/pagespecific/login.css';

const LoginPage = () => {
  const { setToken } = useContext(AuthContext);

  const navigate = useNavigate()
  function navigateToCreateVolunteer () { navigate('/createvolunteer') }
  function navigateToCreateOrganiser () { navigate('/createorganiser') }

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const [feedback, setFeedback] = useState('');
  const [allConferences, setAllConferences] = useState([]);
  const [allVolunteersInConference, setAllVolunteersInConference] = useState([]);

  const [chosenConference, setChosenConference] = useState('');
  const [chosenVolunteer, setChosenVolunteer] = useState('');

  const [rating, setRating] = useState(2.5);

  const [feedbackName, setFeedbackName] = useState('');

  useEffect(() => {
    GetAllConferencesLoginPage(setAllConferences)
  }, []);
  const OpenConfirmation = UseConfirmation();
  return (
    <>
      <TopTitle text="☆ ★ Bestgroup ★ ☆" />
      <div className="flex-container">
          <div className="flex-item">
              <h2>Login</h2>
              <div>
                <StandardInput stateValue={username} stateFunction={setUsername} placeholder="Username" />
              </div>
              <div>
                <StandardInput stateValue={password} stateFunction={setPassword} placeholder="Password" />
              </div>
              <div>
                <StandardButton onClick={() => HandleLogin(username, password, setToken, navigate)} text="Submit" />
              </div>
              <h2>Signup</h2>
              <p>What role best describes you?</p>
              <div>
                <StandardButton onClick={navigateToCreateVolunteer} text="Volunteer" />
                {' '}
                <StandardButton onClick={navigateToCreateOrganiser} text="Organiser" />
              </div>

          </div>
          <div className="flex-item">
              <h2>Submit Feedback</h2>
              <FormControl sx={{ backgroundColor: 'white', marginTop: '3vh', width: '52%' }}>
                <InputLabel id="demo-simple-select-label">Choose Conference</InputLabel>
                <Select
                  labelId="demo-simple-select-label"
                  id="demo-simple-select"
                  value={chosenConference}
                  label="Choose Conference"
                  onChange={ (event) => {
                    setChosenConference(event.target.value)
                    VolunteersInConference(event.target.value, setAllVolunteersInConference)
                  } }
                >
                  {
                    allConferences.map(function (data) {
                      return (
                        <MenuItem key={data.id} value={data.id}>{data.conferencename}</MenuItem>
                      );
                    })
                  }
                </Select>
              </FormControl>
              <FormControl sx={{ backgroundColor: 'white', marginTop: '3vh', width: '52%' }}>
                <InputLabel id="demo-simple-select-label">Choose Volunteer or Manager</InputLabel>
                <Select
                  labelId="demo-simple-select-label"
                  id="demo-simple-select"
                  value={chosenVolunteer}
                  label="Choose Volunteer or Manager"
                  onChange={ (event) => { setChosenVolunteer(event.target.value) } }
                >
                  {
                    allVolunteersInConference.map(function (data) {
                      return (
                        <MenuItem key={data.id} value={data.id}>{data.firstname} {data.lastname}</MenuItem>
                      );
                    })
                  }
                </Select>
              </FormControl>
              <TextField
                id="outlined-multiline-static"
                label="Feedback"
                sx={{
                  marginTop: '3vh',
                  width: '80%',
                  backgroundColor: 'white'
                }}
                multiline
                rows={8}
                defaultValue={feedback}
                onChange={(event) => { setFeedback(event.target.value) }}
              />
              <div>
                <Rating sx={{ color: 'red' }} name="half-rating" value={rating} onChange={(event, newValue) => { setRating(newValue) }} precision={0.5} />
              </div>
              <StandardInput stateValue={feedbackName} stateFunction={setFeedbackName} placeholder="Your Name" />
              <StandardButton onClick={ () => OpenConfirmation(() => { SubmitFeedback(feedbackName, chosenVolunteer, feedback, (rating * 2)) }, 'submit feedback') } text="Submit" />
          </div>
      </div>
    </>
  );
};

export default LoginPage;
// SubmitFeedback(feedbackName, chosenVolunteer, feedback, (rating * 2))
