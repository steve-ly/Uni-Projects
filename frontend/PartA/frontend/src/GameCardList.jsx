import React from 'react';
import { Card, ListGroup, Button, CloseButton } from 'react-bootstrap';
import logo from './img/bigbrain_logo_2.png'
import { useNavigate, } from 'react-router-dom';
import { callDeleteQuiz, callStartQuiz, callGetUniqueQuiz, callEndQuiz } from './Admin'
export default function GameCardList ({ gamecards, handleShow, handlePastSessionsShow, handleResultsShow, handleDelete, getCardID, getSessionId }) {
  // Creates a gamecard for the dashboard that displays the name, total time, number of questions of a quiz as well as some buttons
  // to delete, edit, start, stop and view old sessions
  // clicking start will allow users to open the game control
  const navigate = useNavigate();
  const routeEditGame = (gameId) => {
    navigate(`/EditGame/${gameId}`)
  }

  function deleteQuiz (id) {
    try {
      callDeleteQuiz(id)
    } catch (error) {
      console.error(error);
    }
  }

  function startGame (id) {
    try {
      callStartQuiz(id)
    } catch (error) {
      console.error(error);
    }
  }

  async function stopGame (id) {
    try {
      await callEndQuiz(id);
      handleResultsShow();
    } catch (error) {
      console.error(error);
    }
  }

  async function pastSessions (id) {
    try {
      const quizzesData = await callGetUniqueQuiz(id);
      getSessionId(quizzesData.oldSessions)
      handlePastSessionsShow();
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <>
      {gamecards.map((gamecard, index) => (
        <div key={gamecard.id || index} className='p-3'>
        <Card className='rounded-3' style={{ width: '18rem' }}>
          <Card.Img
            variant="top"
            className="mt-2 fluid"
            src={gamecard.thumbnail || logo}
            alt="game_img"
            style={{ height: '300px' }}
          />
          <Card.Body>
            <Card.Title className='d-flex justify-content-between' style={{ fontFamily: 'Alfa Slab One', fontSize: '25x' }}>
              {gamecard.name}
              <CloseButton onClick={() => { deleteQuiz(gamecard.id); handleDelete(); getCardID('') }}/>
            </Card.Title>
            <Card.Text>
              SessionID: {gamecard.active || 'N/A'} &nbsp;
              <Card.Link href="#"
              onClick={() => { navigator.clipboard.writeText(gamecard.active) }}>
               Copy
              </Card.Link>
            </Card.Text>
            <Card.Link onClick={() => { pastSessions(gamecard.id); }} href="#">
               View past sessions
            </Card.Link>
          </Card.Body>
          <ListGroup className="list-group-flush">
            <ListGroup.Item>Questions: { gamecard.questions.length }</ListGroup.Item>
            <ListGroup.Item>
              Time: {gamecard.questions.reduce((sum, question) => sum + question.time, 0)}{''}s
            </ListGroup.Item>
            <ListGroup.Item>
              Created: {new Date(gamecard.createdAt).toLocaleString()}{' '}
            </ListGroup.Item>
            <ListGroup.Item>
                <Button className="w-100" variant="success" onClick={() => { startGame(gamecard.id); handleDelete(); getCardID(gamecard.id) }}>Start Game</Button>
                <div className='d-flex justify-content-between'>
                </div>
            </ListGroup.Item>
          </ListGroup>
          <Card.Body>
            <span className="d-flex justify-content-between" style={{ justifyContent: 'center' }}>
            <Button variant='danger' onClick={() => { stopGame(gamecard.id); }}>Stop Game</Button>
                <Button onClick={() => routeEditGame(gamecard.id)} style={{ backgroundColor: '#381272', borderColor: '#381272' }}>Edit</Button>
                {/* <Button className="ms-2" variant="danger">Delete</Button> */}
            </span>
          </Card.Body>
        </Card>
        </div>
      ))}
    </>
  );
}
