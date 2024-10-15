import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Table, Container, Button } from 'react-bootstrap';
import { callPlayerResults } from './Player.jsx';
import incorrect from './img/wrong.png'
import correct from './img/correct.png'
// When session is done, displays the player's score
async function getPlayerResults (playerId) {
  try {
    const playerStatus = await callPlayerResults(playerId);
    // do something with playerStatus here
    console.log(playerStatus);
    return playerStatus;
  } catch (error) {
    console.error(error); // logs the error object if the request fails
    // handle the error here
  }
}

function calculateScore (results, duration, points, idx) {
  const durationList = JSON.parse(duration);
  const pointList = JSON.parse(points);
  let timeTaken = 0;
  let score = 0;
  if (results[idx].questionStartedAt === null || results[idx].answeredAt === null) {
    score = 0;
    return score;
  }

  const timeStarted = new Date(results[idx].questionStartedAt);
  const timeCompleted = new Date(results[idx].answeredAt);
  timeTaken = Math.floor((timeCompleted - timeStarted) / 1000);
  if (timeTaken < 0) {
    timeTaken = 0;
  }
  console.log(timeTaken);
  console.log(durationList[idx]);
  score = durationList[idx] - timeTaken;
  if (results[idx].correct === false) {
    score = 0
    return score
  }
  return (score * pointList[idx]);
}

const PlayerResult = () => {
  const { playerId, durationList, pointList } = useLocation().state;
  console.log(JSON.stringify(durationList));

  const [results, setResults] = useState(null);
  const [scores, setScores] = useState([]);

  useEffect(() => {
    async function fetchResults () {
      const playerResults = await getPlayerResults(playerId);
      setResults(playerResults);
    }

    fetchResults();
  }, [playerId]);

  useEffect(() => {
    if (results) {
      const newScores = results.map((result, idx) =>
        calculateScore(results, JSON.stringify(durationList), JSON.stringify(pointList), idx)
      );
      setScores(newScores);
    }
  }, [results, durationList, pointList]);

  function handleResult (score) {
    if (score !== 0) {
      return <img src={correct} alt="correct" style={{ width: '30px', height: '30px' }}/>
    } else {
      return <img src={incorrect} alt="incorrect" style={{ width: '30px', height: '30px' }}/>
    }
  }

  const navigate = useNavigate();

  const routeHome = () => {
    navigate('/');
  };

  return (
    <>
    <div style={{ textAlign: 'center' }}>
    <h1
      style={{
        fontFamily: 'Alfa Slab One',
        fontSize: '50px',
        color: 'white',
        textAlign: 'center',
        letterSpacing: '1px',
      }}
    >
      Results
    </h1>
  </div>
    <Container
            centered
            className="bg-light rounded-3 p-5 pt-4"
            style={{ maxWidth: '900px' }}
          >
          <Table variant="">
      <thead>
        <tr>
          <th style={{ fontSize: '20px' }}>No.</th>
          <th style={{ fontSize: '20px', textAlign: 'center' }}>Score</th>
          <th style={{ fontSize: '20px', textAlign: 'center' }}>Result</th>
        </tr>
      </thead>
      <tbody>
        {scores.map((score, idx) => (
          <tr key={idx}>
            <td style={{ fontSize: '20px' }}>{idx + 1}</td>
            <td style={{ fontSize: '20px', textAlign: 'center' }}>{score}/{JSON.parse(JSON.stringify(durationList))[idx] * JSON.parse(JSON.stringify(pointList))[idx] }</td>
            <td style={{ fontSize: '20px', textAlign: 'center' }}>{handleResult(score)}</td>
          </tr>
        ))}
      </tbody>
    </Table>
    <div className='mb-3' style={{
      fontFamily: 'Alfa Slab One',
      fontSize: '40px',
      color: 'black',
      textAlign: 'left',
      letterSpacing: '1px',
    }}>
          Total: {scores.reduce((a, b) => a + b, 0)}
        </div>

        <div>
        The score is calculated as 1 if the answer was correct and 0 if it was wrong. Correct answers are multiplied by score and (max time of question) - (time taken since last answer submission).
        </div>
    </Container>
    <div style={{ textAlign: 'center' }}>
            <Button className="mt-3" onClick={() => { routeHome(); }}>Back</Button>
    </div>
    </>
  );
};

export default PlayerResult;
