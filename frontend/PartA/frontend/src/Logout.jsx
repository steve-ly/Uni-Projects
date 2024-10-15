import axios from 'axios';
import { useNavigate, useLocation } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, Container } from 'react-bootstrap';
import React, { useEffect } from 'react';

const BACKEND_PORT = 5005;
// renders and allows users to logout
async function callLogout () {
  try {
    const userToken = localStorage.getItem('token');
    await axios.post(`http://localhost:${BACKEND_PORT}/admin/auth/logout`, {}, {
      headers: {
        Authorization: 'Bearer ' + userToken,
        accept: 'application/json',
        'Content-Type': 'application/json',
      },
    });
    localStorage.clear();
    console.log('Logout');
    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
}

function CreateLogout () {
  const navigate = useNavigate();

  const handleLogout = async (e) => {
    e.preventDefault();
    const logoutSuccessful = await callLogout();
    if (logoutSuccessful) {
      navigate('/Login');
    }
  };

  return (
    <>
      <Container style={{ textAlign: 'center' }}>
        <Button
          onClick={handleLogout}
          className="mt-5 w-100"
          style={{ backgroundColor: '#e40000 ', borderColor: '#e40000', maxWidth: '300px' }}
        >
          Logout
        </Button>
      </Container>
    </>
  );
}

const Logout = () => {
  const isLoggedIn = !!localStorage.getItem('token');
  const location = useLocation();

  useEffect(() => {
    // const handleStorageChange = (e) => {
    //   if (e.key === 'token') {
    //     setIsLoggedIn(!!localStorage.getItem('token'));
    //   }
    // };

    // window.addEventListener('storage', handleStorageChange);
    // return () => {
    //   window.removeEventListener('storage', handleStorageChange);
    // };
  }, [location]);

  if (isLoggedIn) {
    return <CreateLogout />;
  } else {
    return null;
  }
};

export default Logout;
