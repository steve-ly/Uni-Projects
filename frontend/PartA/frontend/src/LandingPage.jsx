import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, Container, Col } from 'react-bootstrap';
import React from 'react';
// import axios from 'axios';
import logo from './img/bigbrain_logo_1.png';

import { useNavigate } from 'react-router-dom';
// Default page on load.
const Welcome = () => {
  const navigate = useNavigate();

  const routeLogin = () => {
    navigate('/Login'); // Navigate to Register page
  };
  const routePlay = () => {
    navigate('/Play'); // Navigate to Register page
  };

  return (
    <>
      <Container>
        <Col lg={8} md={10} sm={12} className="p-5 m-auto">
          <Container>
            <div style={{ textAlign: 'center' }}>
              <img
                src={logo}
                alt="bigbrain_logo"
                className="fluid mb-1 w-75"
              />
            </div >
            <div className='p-2' style={{ fontFamily: 'Alfa Slab One', fontSize: '40px', color: 'white', letterSpacing: '1px', textAlign: 'center' }}>I am a/an...</div>
            <div className='d-flex flex-row' style={{ textAlign: 'center' }}>
                <div className='w-50 p-2'>
                <Button className='w-100 p-5' onClick={routeLogin} style={{ fontFamily: 'Alfa Slab One', fontSize: '20px', color: 'white', letterSpacing: '1px', backgroundColor: '#6f24e4', borderColor: '#6f24e4' }}>Admin</Button>
                </div>
                <div className='w-50 p-2'>
                <Button className='w-100 p-5' onClick={routePlay} style={{ fontFamily: 'Alfa Slab One', fontSize: '20px', color: 'white', letterSpacing: '1px', backgroundColor: '#ea6d9d', borderColor: '#ea6d9d' }}>Player</Button>
                </div>

            </div>
          </Container>
        </Col>
      </Container>
    </>
  );
};

export default Welcome;
