import React, { useState, useEffect } from 'react';
import { Container, Table, Button } from 'react-bootstrap';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { callAdvanceQuiz, callGetSessionStatus, callEndQuiz, callGetSessionResults } from './Admin';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { percentage, calculateTopScores, averageTime, AnswerDistributionChart, AnswerResponseTime } from './ScoreHelpers'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);
// When session is done/start renders the control panel and results of the session
export default function Results (props) {
  let { sessionId } = useParams();
  sessionId = parseInt(sessionId);
  const location = useLocation();
  const quizId = location.state;
  const [buttonStyle, setButtonStyle] = useState({});
  const [statusActive, setStatusActive] = useState(true);
  const [formSubmit, setFormSubmit] = useState(true);
  const [currentQuestion, setCurrentQuestion] = useState(-1);
  const [duration, setDuration] = useState(0);
  const [allQuestions, setAllQuestions] = useState(null);

  const [topScores, setTopScores] = useState([]);
  const [averageT, setaverageTime] = useState(null);
  const [percentages, setpercentages] = useState(null);

  const navigate = useNavigate();

  const routeDashboard = () => {
    navigate('/Dashboard');
  };

  async function getInfo (questions, answers) {
    if (questions !== null) {
      setTopScores(calculateTopScores(questions, answers))
      setaverageTime(averageTime(questions, answers))
      setpercentages(percentage(questions, answers))
    }
  }

  async function advanceGame (id) {
    try {
      await callAdvanceQuiz(id);
      setFormSubmit(true);
    } catch (error) {
      console.error(error);
    }
  }

  async function stopGame (id) {
    try {
      await callEndQuiz(id);
      setFormSubmit(true);
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    if (formSubmit) {
      const fetchData = async () => {
        try {
          const sessionStatus = await callGetSessionStatus(sessionId);
          setStatusActive(sessionStatus.results.active);
          setCurrentQuestion(sessionStatus.results.position)
          setAllQuestions(sessionStatus.results.questions)
          console.log(sessionStatus.results)
          if (sessionStatus.results.position !== -1 && sessionStatus.results.questions[sessionStatus.results.position].time !== undefined) {
            setDuration(sessionStatus.results.questions[sessionStatus.results.position].time)
          }
        } catch (error) {
          console.error(error);
        }
      };
      fetchData();
      setFormSubmit(false);
    }
  }, [formSubmit])

  const handleMouseDown = () => {
    setButtonStyle({
      transform: 'scale(0.6)',
      transition: 'transform 0.1s ease-out',
    });
  };
  const handleMouseUp = () => {
    setButtonStyle({});
  };

  useEffect(() => {
    async function getResults () {
      try {
        const results = await callGetSessionResults(sessionId);
        console.log(allQuestions);
        getInfo(allQuestions, results.results)
      } catch (error) {
        console.error(error);
      }
    }

    if (statusActive === false) {
      getResults();
    }
  }, [statusActive, allQuestions])

  return (
    <>
        {statusActive
          ? (
            <>
            <div className="p-5">
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
              Game Control
            </h1>
          </div>
          <Container
            centered
            className="bg-light rounded-3 p-5 pt-4"
            style={{ maxWidth: '900px' }}
          >
            <div className="p-3" style={{ textAlign: 'center' }}>
            <div>Current Question: {currentQuestion + 1}</div>
            <div>Max time to complete: {duration}s</div>
          </div>
          <div className="d-flex justify-content-center">
            <Button
              className="m-0 w-50"
              variant="dark"
              onMouseDown={handleMouseDown}
              onMouseUp={handleMouseUp}
              onMouseLeave={handleMouseUp}
              onTouchStart={handleMouseDown}
              onTouchEnd={handleMouseUp}
              style={buttonStyle}
              onClick={() => {
                advanceGame(quizId);
              }}
            >
              Next Question
            </Button>
            <Button className="m-0 ms-4 w-25" variant="danger" onClick={() => {
              stopGame(quizId);
            }}>
              Stop Game
            </Button>
          </div>
          </Container>
          </div>
            </>
            )
          : null}

        {!statusActive
          ? (
          <>
          <div className="p-5">
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
          <div
            className="mb-2"
            style={{
              fontFamily: 'Alfa Slab One',
              fontSize: '25px',
              textAlign: 'center',
              letterSpacing: '1px',
            }}
          >
            Leaderboard
          </div>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Position</th>
                <th>Name</th>
                <th>Points</th>
              </tr>
            </thead>
            <tbody>
            {topScores.map((item, index) => (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{item.name}</td>
            <td>{item.score}</td>
          </tr>
            ))}
            </tbody>
          </Table>
          <div
            style={{
              fontFamily: 'Alfa Slab One',
              fontSize: '25px',
              textAlign: 'center',
              letterSpacing: '1px',
            }}
          >
            Charts
          </div>
          <div>
            {/* Bar to show a breakdown of what percentage of people (Y axis) got certain questions (X axis) correct */}
            <AnswerDistributionChart probabilities={percentages}/>
            {/* chart showing the average response time for each question_img */}
            <AnswerResponseTime responseTime={averageT}/>
          </div>
          <div style={{ textAlign: 'center' }}>
            <Button className="mt-3" onClick={() => { routeDashboard(); }}>Back to Dashboard</Button>
          </div>
        </Container>
        </div>
        </>
            )
          : null}
    </>
  );
}
