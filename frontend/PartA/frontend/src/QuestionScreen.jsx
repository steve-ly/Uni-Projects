import React, { useState, useEffect } from 'react';
import { Modal } from 'react-bootstrap';
import questionMusic from './music/question_screen_music.mp3';
// import { useLocation, useNavigate } from 'react-router-dom';
import { useLocation, useNavigate } from 'react-router-dom';
import { callPlayerQuestion, callPlayerAnswer } from './Player';
import AnswerOptionsSingle from './AnswerPromptsSingle';
import AnswerOptionsMulti from './AnswerPromptsMultiple';

// create a component that takes in a prop and displays a youtube video if prop is a link and image if else.
const Thumbnail = ({ src }) => {
  const isYouTubeVideo = typeof src === 'string' && src.includes('youtube.com');
  if (isYouTubeVideo) {
    const videoId = src.split('v=')[1];
    const embedLink = `https://www.youtube.com/embed/${videoId}`;
    return (
      <div>
        <iframe
          width="560"
          height="315"
          src={embedLink}
          title="YouTube video player"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        ></iframe>
      </div>
    );
  } else {
    return <img
    src={src}
    alt="question_img"
    className="mt-2 fluid"
    style={{ width: '100%', height: '100%', objectFit: 'fill' }}
  />
  }
};
// render the question screen and sets timer countdown
export default function QuestionScreen (props) {
  // plays music on render
  const [show, setShow] = useState(false);
  const { playerId } = useLocation().state;

  const [questionId, setQuestionId] = useState(1);
  const [duration, setDuration] = useState(null);
  const [questionText, setQuestionText] = useState('');
  const [answerPrompts, setAnswerPrompts] = useState([]);
  const [image, setImage] = useState(null);
  const [questionType, setQuestionType] = useState('');
  const [timeStarted, setTimeStarted] = useState(null);
  const [timeOver, setTimeOver] = useState(false);
  const [remainingTime, setRemainingTime] = useState();
  const [answerId, setAnswerIds] = useState([]);
  const [durationList, setDurationList] = useState([]);
  const [points, setPoints] = useState(null);
  const [pointList, setPointList] = useState([]);

  const [answers, setAnswers] = useState([]);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const navigate = useNavigate();

  useEffect(() => {
    console.log('render');
    async function fetchData () {
      try {
        const response = await callPlayerQuestion(playerId);
        setQuestionId(response.question.id);
        setDuration(response.question.time);
        setQuestionText(response.question.text);
        setAnswerPrompts(response.question.answerPrompts);
        setImage(response.question.img);
        setQuestionType(response.question.questionType);
        setPoints(response.question.points);
        const questionStarted = new Date(
          response.question.isoTimeLastQuestionStarted
        );
        setTimeStarted(questionStarted);
        setTimeOver(false);
        handleClose();
        // if (response.question.questionType === 'single') {
        //   setQuestionType('Select one')
        // } else {
        //   setQuestionType('Select one or more:')
        // }
      } catch (error) {
        console.error(error);
      }
    }
    fetchData();
  }, [questionId]);

  useEffect(() => {
    let apiPoll;
    async function startPolling () {
      apiPoll = setInterval(async () => {
        // Make the callback function async
        try {
          const response = await callPlayerQuestion(playerId);
          setQuestionId(response.question.id);
        } catch (error) {
          if (
            error.response.data.error === 'Session ID is not an active session'
          ) {
            navigate('/PlayerResults', {
              state: { playerId, durationList, pointList },
            });
          }
        }
      }, 1000);
    }

    startPolling();
    return () => {
      clearInterval(apiPoll);
    };
  }, [playerId]);

  useEffect(() => {
    const newDurationlist = durationList;
    if (duration !== null) {
      newDurationlist.push(duration);
    }
    setDurationList(newDurationlist);

    const newPointslist = pointList;
    if (points !== null) {
      newPointslist.push(points);
    }
    setPointList(newPointslist);

    if (timeStarted && duration > 0) {
      const interval = setInterval(() => {
        const now = new Date();
        const elapsed = Math.floor((now - timeStarted) / 1000); // elapsed time in seconds
        const remaining = duration - elapsed;

        if (remaining < 0) {
          clearInterval(interval);
          // set the timeOver state to true
          setTimeOver(true);
        } else {
          // set the remaining time to a state variable
          setRemainingTime(remaining);
        }
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [timeStarted]);

  useEffect(() => {
    const audio = new Audio(questionMusic);
    audio.volume = 0.1;
    audio.loop = true;
    audio.play();

    return () => {
      audio.pause();
      audio.currentTime = 0;
    };
  }, []);

  useEffect(() => {
    async function fetchData () {
      try {
        const response = await callPlayerAnswer(playerId);
        setAnswerIds(response.answerIds);
      } catch (error) {
        console.error(error);
      }
    }

    if (timeOver === true) {
      fetchData()
    }
  }, [timeOver]);

  useEffect(() => {
    if (answerId.length !== 0) {
      const answersShow = answerId.map(id => answerPrompts[id])
      setAnswers(answersShow.join(', '))
      handleShow();
    }
  }, [answerId]);

  return (
    <>
      <div className="p-5" style={{ textAlign: 'center' }}>
        <h1
          className="mb-3"
          style={{
            fontFamily: 'Alfa Slab One',
            fontSize: '30px',
            color: 'white',
            textAlign: 'center',
          }}
        >
          {questionText}
        </h1>
        <div
          className="mx-auto mb-3"
          style={{ height: '400px', maxWidth: '1000px' }}
        >
          <Thumbnail src={image}/>
        </div>
        <div className="mx-auto" style={{ maxWidth: '1000px' }}>
          <div style={{
            fontFamily: 'Alfa Slab One',
            fontSize: '30px',
            color: 'white',
            textAlign: 'center',
          }}>
           Time: {remainingTime}
          </div>
          <div className="d-flex justify-content-center">
            <div
              style={{
                fontFamily: 'Alfa Slab One',
                fontSize: '25px',
                color: 'white',
                textAlign: 'flex-end',
              }}
            >
              {questionType === 'Single Answer'
                ? 'select one:'
                : 'select one or more:'}
            </div>
            <div
              style={{
                fontFamily: 'Alfa Slab One',
                fontSize: '30px',
                color: 'white',
                textAlign: 'center',
              }}
            >
            </div>
          </div>
        </div>
        <div
          className="d-flex mx-auto flex-row flex-wrap"
          style={{
            maxWidth: '1000px',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          {questionType === 'Single Answer'
            ? (
            <AnswerOptionsSingle
              answerPrompts={answerPrompts}
              playerId={playerId}
              timeOver={timeOver}
            />
              )
            : (
            <AnswerOptionsMulti
              answerPrompts={answerPrompts}
              playerId={playerId}
              timeOver={timeOver}
            />
              )}
        </div>
      </div>

      <Modal show={show} onHide={handleClose} centered>
        <Modal.Header closeButton>
          <Modal.Title>Results</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className='d-flex flex-row mb-2' >
            The answer was {answers}
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}
