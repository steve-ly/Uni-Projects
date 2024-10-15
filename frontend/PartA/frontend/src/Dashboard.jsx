import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState, useEffect } from 'react';
import { Button, Modal, Form, ButtonGroup } from 'react-bootstrap';
import GameCardList from './GameCardList';
import { callNewQuiz, callGetQuizzes, callGetUniqueQuiz } from './Admin'
import { useParams, useNavigate } from 'react-router-dom';
// Component to display button that show list of previous sessions
const ButtonList = ({ ids, quizId }) => {
  const navigate = useNavigate();
  return (
    <div>
      {ids && ids.length > 0
        ? (
        <ButtonGroup className="d-flex justify-content-between">
          {ids.map((id) => (
            <Button key={id} onClick={() => navigate(`/Results/${id}`, { state: quizId })}>{id}</Button>
          ))}
        </ButtonGroup>
          )
        : (
        <p>No sessions found</p>
          )}
    </div>
  );
};
// renders dashboard and includes game cards and new button
const Dashboard = (props) => {
  let { gameId } = useParams();
  gameId = parseInt(gameId);
  const [show, setShow] = useState(false);
  const [showPastSessionsModal, setShowPastSessionsModal] = useState(false);
  const [showResultsModal, setShowResultsModal] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const handlePastSessionsClose = () => setShowPastSessionsModal(false);

  const handleResultsClose = () => setShowResultsModal(false);
  const handleResultsShow = () => setShowResultsModal(true);

  const [quizName, setquizName] = useState('');
  const [gameCards, setgameCards] = useState([]);

  const [formSubmitted, setFormSubmitted] = useState(true);
  const [oldSessionId, setOldSessionId] = useState([]);

  const handleDelete = () => setFormSubmitted(true);

  const [cardId, setCardID] = useState('');
  const [sessionId, setSessionId] = useState('');

  const getCardID = (arg) => {
    console.log(arg);
    setCardID(arg);
  };

  const getSessionId = (arg) => {
    console.log(arg);
    setOldSessionId(arg);
  };
  const [showStartGameModal, setStartGameModal] = useState(false);
  const handleStartGameClose = () => setStartGameModal(false);
  const handleStartGameShow = () => setStartGameModal(true);

  const handlePastSessionsShow = () => {
    setShowPastSessionsModal(true);
  };
  const navigate = useNavigate();

  const routeAdminGame = () => {
    const quizId = cardId;
    navigate(`/Results/${sessionId}`, { state: quizId })
  }
  useEffect(() => {
    if (cardId !== '') {
      for (const card of gameCards) {
        // Check if the value of the specified property is equal to the specified value
        if (card.id === cardId) {
          // Output the object
          setSessionId(card.active)
          handleStartGameShow();
        }
      }
    }
  }, [gameCards]);

  useEffect(() => {
    if (formSubmitted) {
      // Fetch data from an API or perform other asynchronous operations
      const fetchData = async () => {
        try {
          const quizzesData = await callGetQuizzes();
          const updatedQuizzes = await Promise.all(quizzesData.map(async (quiz) => {
            // Call callGetUniqueQuiz for each question in the quizzes array
            const updatedQuiz = await callGetUniqueQuiz(quiz.id);
            return { ...quiz, ...updatedQuiz }; // Merge the returned quiz data with the original quiz object
          }));

          setgameCards(updatedQuizzes); // Update gameCards state with the updated quizzes array
        } catch (error) {
          console.error(error);
        }
      };
      fetchData(); // Invoke the fetchData function

      setFormSubmitted(false); // Reset the formSubmitted flag
    }
  }, [formSubmitted]);

  return (
    <>
    <div>
      <h1 className="mb-1 w-100 login" style={{ fontFamily: 'Alfa Slab One', fontSize: '50px', color: 'white', textAlign: 'center', letterSpacing: '1px' }}>
        Games
      </h1>
      <div style={{ textAlign: 'center' }}>
        <Button variant="primary" onClick={handleShow} className="mt-1 mb-3" style={{ backgroundColor: '#ea6d9d', borderColor: '#ea6d9d' }}>
          New Game
        </Button>
      </div>
      <div className='d-flex mx-auto flex-row flex-wrap' style={{ maxWidth: '1500px', alignItems: 'center', justifyContent: 'center' }}>
        <GameCardList
          gamecards={gameCards}
          handlePastSessionsShow={handlePastSessionsShow}
          handleResultsShow={handleResultsShow}
          gameId={gameId}
          handleDelete = {handleDelete}
          getCardID = {getCardID}
          getSessionId = {getSessionId} />
      </div>
    </div>

    <Modal show={showPastSessionsModal} onHide={handlePastSessionsClose} centered>
      <Modal.Header closeButton>
        <Modal.Title>Past Sessions</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form noValidate className='p-1'>
        <ButtonList ids={oldSessionId} quizId={cardId} />
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handlePastSessionsClose}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>

    <Modal show={show} onHide={handleClose} centered>
      <Modal.Header closeButton>
        <Modal.Title>New Game</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form noValidate className='p-1' onSubmit={(e) => { e.preventDefault(); setFormSubmitted(true); callNewQuiz(quizName); setquizName(''); handleClose(); getCardID('') }}>
          <Form.Group className="mt-1 mb-2" controlId="formPassword">
            <Form.Control type="text" placeholder="Enter name" required value={quizName} onChange={(e) => setquizName(e.target.value)} />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="primary" onClick={() => { handleClose(); callNewQuiz(quizName); setFormSubmitted(true); setquizName(''); getCardID('') }}>
          Make it!
        </Button>
      </Modal.Footer>
    </Modal>

      <Modal show={showResultsModal} onHide={handleResultsClose} centered>
        <Modal.Body style={{ textAlign: 'center' }}>
          Would you like to see the results?
        </Modal.Body>
        <Modal.Footer className='d-flex justify-content-center'>
          <Button className='w-25' variant="success" onClick={routeAdminGame}>
            Yes
          </Button>
          <Button className='w-25' variant="danger" onClick={() => { handleResultsClose(); setFormSubmitted(true); }}
>
            No
          </Button>
        </Modal.Footer>
      </Modal>

      <Modal show={showStartGameModal} onHide={handleStartGameClose} centered>
      <Modal.Body style={{ textAlign: 'center' }}>
        <b>Session URL:</b>
        <div>localhost:3000/Play/{sessionId}</div>
        <Button variant='link' onClick={() => { navigator.clipboard.writeText(`localhost:3000/Play/${sessionId}`) }}>
               Copy
        </Button>
      </Modal.Body>
      <Modal.Footer className='d-flex justify-content-center'>
      <Button className='w-25' variant="secondary" onClick={handleStartGameClose}>
          Back
        </Button>
        <Button className='w-25' variant="success" onClick={routeAdminGame}>
          Go to Game
        </Button>
      </Modal.Footer>
    </Modal>

  </>
  );
};
export default Dashboard;
