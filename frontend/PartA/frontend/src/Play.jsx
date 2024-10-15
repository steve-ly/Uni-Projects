import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, Form, Container, Col } from 'react-bootstrap';
import React, { useState, useEffect } from 'react';
// import axios from 'axios';
import logo from './img/bigbrain_logo_1.png';
import callJoinSession from './Player';
import {
  useNavigate,
  useParams
} from 'react-router-dom';
// Form for players to join a session
const Play = () => {
  const { sessionIdFromURL } = useParams();
  const [sessionId, setSessionId] = useState(sessionIdFromURL || '');
  const [name, setName] = useState('');
  const [playerId, setPlayerId] = useState('');

  const navigate = useNavigate();

  const routeLobby = () => {
    navigate(`/Lobby/${sessionId}`, { state: { playerId } }); // Navigate to Register page
  };

  const routeLogin = () => {
    navigate('/Login'); // Navigate to Register page
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await callJoinSession(sessionId, name);
      console.log('fasdf')
      console.log(response)
      if (response !== undefined) {
        setPlayerId(response);
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    // Use playerId in the useEffect hook // This will print the updated value of playerId whenever it changes
    if (playerId !== '') {
      routeLobby();
    }
  }, [playerId]);

  return (
    <>
      <Container>
        <Col lg={5} md={10} sm={12} className="p-5 m-auto">
          <Container className="pt-5">
            <div>
              <img src={ logo } alt="bigbrain_logo" className='fluid mb-1 w-100' />
            </div>
            <Form noValidate className='bg-light rounded rounded-lg p-3 pt-1'>
              <Form.Group className="mt-1 mb-2" controlId="formPassword">
                <Form.Control type="text" placeholder="Name" required value={name} onChange={(e) => setName(e.target.value)} style={{ textAlign: 'center' }}/>
                {/* {loginErrorMsg !== "" ? (
                  <p className="text-danger">{loginErrorMsg}</p>
                ) : null} */}
              </Form.Group>
              <Form.Group className="mt-1 mb-2" controlId="formPassword">
                <Form.Control type="text" placeholder="Session ID" required value={sessionId} onChange={(e) => setSessionId(e.target.value)} style={{ textAlign: 'center' }}/>
                {/* {loginErrorMsg !== "" ? (
                  <p className="text-danger">{loginErrorMsg}</p>
                ) : null} */}
              </Form.Group>
              <Button variant="dark" type="submit" className="w-100" onClick={(e) => { handleFormSubmit(e); }} style={{ fontFamily: 'Alfa Slab One', fontSize: '20px' }}>
                Go!
              </Button>
            </Form>
            <Button className="w-100 btn btn-link text-decoration-none" variant="Link" onClick={routeLogin} style={{ color: 'white' }}>
                GameMaster? Click Here!
            </Button>
          </Container>
        </Col>
      </Container>
    </>
  );
};

export default Play;
