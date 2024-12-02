import { Box, Container, styled } from '@material-ui/core';
import { React, useContext } from 'react';
import '../style/ui.css';
// adds
import { useTheme } from '@mui/material/styles';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Chip from '@mui/material/Chip';
import { useNavigate } from 'react-router-dom';
import logoutIcon from '../images/logout.png'
import dashboardIcon from '../images/dashboard.png'
import { HandleLogout } from './HTTP/User';
import { AuthContext } from './AuthContext';
import Button from '@mui/material/Button';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

// These are just dummy boxes, I will rename them when I give them an actual usage
export const BoxA = styled(Container)({
  width: '400px',
  textAlign: 'center'
})

export const BoxB = ({ children, ...props }) => {
  return (
    <Box
      width='300px'
      height='300px'
      display='flex'
      justifyContent='center'
      alignItems='center'
      flexDirection='column'
      padding={2}
      position='absolute'
      left='50%'
      top='50%'
      textAlign='center'
      {...props}>
      {children}
    </Box>
  );
};

export const StandardButton = ({ text, onClick }) => {
  return (
    <Button
    onClick={onClick}
    variant="contained"
    sx={{
      whiteSpace: 'no-wrap',
      color: 'white',
      width: '14vw',
      textTransform: 'none',
      padding: '1vh',
      fontSize: '2vh',
      margin: '0',
      marginTop: '1vh',
      borderRadius: '5px',
      backgroundColor: '#475B63',
      fontFamily: 'Verdana, Geneva, Tahoma, sans-serif',
      display: 'inline-block',
      height: '5vh',
      textAlign: 'center',
      '&:hover': {
        backgroundColor: '#2E2C2F',
        transform: 'scale(1.04)'
      }
    }}>
      {text}
    </Button>
  );
};

export const SmallStandardButton = ({ text, onClick, buttonType }) => {
  return (
    <Button
    onClick={onClick}
    variant="contained"
    sx={{
      whiteSpace: 'no-wrap',
      color: 'white',
      width: '7vw',
      textTransform: 'none',
      padding: '1vh',
      fontSize: '1.5vh',
      margin: '1vh',
      marginLeft: '-0.3vh',
      marginBottom: '0',
      borderRadius: '5px',
      backgroundColor: buttonType === localStorage.getItem('filterapi') ? '#2E2C2F' : '#475B63',
      fontFamily: 'Verdana, Geneva, Tahoma, sans-serif',
      display: 'inline-block',
      height: '5vh',
      textAlign: 'center',
      '&:hover': {
        backgroundColor: '#2E2C2F',
        transform: 'scale(1.04)'
      }
    }}>
      {text}
    </Button>
  );
};

export const LargeStandardButton = ({ text, onClick }) => {
  return (
    <Button
    onClick={onClick}
    variant="contained"
    sx={{
      whiteSpace: 'no-wrap',
      color: 'white',
      width: '10vw',
      height: '7vw',
      textTransform: 'none',
      padding: '1vh',
      fontSize: '1.5vh',
      margin: '5vh',
      marginBottom: '0',
      borderRadius: '5px',
      backgroundColor: '#475B63',
      fontFamily: 'Verdana, Geneva, Tahoma, sans-serif',
      display: 'inline-block',
      textAlign: 'center',
      '&:hover': {
        backgroundColor: '#2E2C2F',
        transform: 'scale(1.04)'
      }
    }}>
      {text}
    </Button>
  );
};

export const OldStandardButton = ({ text, onClick }) => {
  return (
    <button className="standardButton" onClick={onClick}>
      {text}
    </button>
  );
};

export const StandardInput = ({ stateValue, stateFunction, placeholder }) => {
  // stateFunction(e.target.value)
  return (
    <input className='standardInput' type="text" placeholder={placeholder} value={stateValue} onChange={e => stateFunction(e.target.value)}></input>
  );
};

export const StandardEmail = ({ stateValue, stateFunction, placeholder }) => {
  // stateFunction(e.target.value)
  return (
    <input className='standardInput' type="email" placeholder={placeholder} value={stateValue} onChange={e => stateFunction(e.target.value)}></input>
  );
};

export const StandardPassword = ({ stateValue, stateFunction, placeholder }) => {
  // stateFunction(e.target.value)
  return (
    <input className='standardInput' type="password" placeholder={placeholder} value={stateValue} onChange={e => stateFunction(e.target.value)}></input>
  );
};

export const DashboardBox = ({ description, navigationFunction }) => {
  // stateFunction(e.target.value)
  return (
    <div className="dashboardBox" onClick={() => { navigationFunction() }}>
        <h3>{description}</h3>
    </div>
  );
};

export const TopTitle = ({ text }) => {
  return (
    <div className="topPage">
      <h1>
        {text}
      </h1>
    </div>
  );
};

// This is for all dashboard directed esque pages
export const TopTitleAndSubtitle = ({ titleText, subtitleText }) => {
  return (
    <>
      <div className="topPage">
        <h1>
          {titleText}
        </h1>
      </div>
      <div className="topPageSub">
        {subtitleText}
      </div>
    </>
  );
};

// adds

export const LogoutAndDashboardIcons = () => {
  const navigate = useNavigate()
  const { token, setToken } = useContext(AuthContext)
  function navigateToDashboard () { navigate('/dashboard') }
  return (
    <>
    <div className="iconSection">
      <div className="iconBox" >
        <img src={logoutIcon} alt="Logout" onClick={() => { HandleLogout(token, setToken, navigate) }}/>
      </div>
      <div className="iconBox" >
        <img src={dashboardIcon} alt="Dashboard" onClick={() => { navigateToDashboard() }}/>
      </div>
    </div>
    </>
  );
};

function getStyles (name, personName, theme) {
  return {
    fontWeight:
      personName.indexOf(name) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium,
  };
}

export default function MultipleSelectChip ({ names, menuProps, selectedValues, setSelectedValues, realName }) {
  const theme = useTheme();

  const handleChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedValues(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
  };

  return (
    <div>
      <FormControl sx={{ m: 1, width: 300 }}>
        <InputLabel id="demo-multiple-chip-label">{realName}</InputLabel>
        <Select
          labelId="demo-multiple-chip-label"
          id="demo-multiple-chip"
          multiple
          value={selectedValues}
          onChange={handleChange}
          input={<OutlinedInput id="select-multiple-chip" label={realName} />}
          renderValue={(selected) => (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
          MenuProps={menuProps}
        >
          {names.map((name) => (
            <MenuItem
              key={name}
              value={name}
              style={getStyles(name, selectedValues, theme)}
            >
              {name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
}

export const ConferenceStartEndDates = () => {
  return (
    <>
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DemoContainer sx={{
          width: '40%',
          justifyContent: 'center',
          marginLeft: 'auto',
          marginRight: 'auto',
          marginTop: '1.5vh'
        }} components={['DateTimePicker']}>
          <DatePicker sx={{ backgroundColor: ' white' }} label="Start Date & Time" />
          <DatePicker sx={{ backgroundColor: ' white' }} label="End Date & Time" />
        </DemoContainer>
      </LocalizationProvider>
    </>
  );
};
