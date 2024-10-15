import React, { useEffect, useState } from 'react';
import { Container, Button, Form } from 'react-bootstrap';
import { useParams, useNavigate } from 'react-router-dom';
import { callGetUniqueQuiz, callUpdateQuiz } from './Admin';
import { debounce } from 'lodash';
import { fileToDataUrl } from './EditGame';
import AnswerList from './AnswerList';
// function to allow user to edit a specific question -> currently refreshes
export default function EditQuestion (props) {
  let { gameId, questionId } = useParams();
  gameId = parseInt(gameId);
  questionId = parseInt(questionId);

  const navigate = useNavigate();
  const [getQuestions, setquestions] = useState([]);
  const [getAnswerPrompts, setAnswerPrompts] = useState([]);
  const [getAnswers, setAnswers] = useState([]);
  const [editSubmitted, setEditSubmitted] = useState(true);
  const [questionText, setQuestionText] = useState([]);
  const [title, setTitle] = useState('');
  const [time, setTime] = useState('');
  const [points, setPoints] = useState('');
  const [type, setType] = useState('');

  const handleThumbnailUpload = (e) => {
    console.log('updated Thumbnail')
    const file = e.target.files[0];
    fileToDataUrl(file).then((base64str) => { // change to base64
      console.log(base64str);
      const newQuestion = getQuestions;
      newQuestion[questionId - 1].img = base64str
      callUpdateQuiz(gameId, newQuestion, title);
      console.log('thumbnail edited')
    });
    setEditSubmitted(true);
  }

  const handleURLUpload = (e) => {
    const newQuestion = getQuestions;
    newQuestion[questionId - 1].img = e.target.value
    callUpdateQuiz(gameId, newQuestion, title);
    setEditSubmitted(true);
  }

  useEffect(() => {
    if (editSubmitted) {
      // Fetch data from an API or perform other asynchronous operations
      const fetchData = async () => {
        try {
          console.log('typeof');
          console.log(typeof gameId);
          console.log(gameId);
          const gameData = await callGetUniqueQuiz(gameId);
          setType(gameData.questions[questionId - 1].type);
          setTime(gameData.questions[questionId - 1].time);
          setPoints(gameData.questions[questionId - 1].points);
          setAnswers(gameData.questions[questionId - 1].answer);
          setTitle(gameData.name);
          setquestions(gameData.questions);
          setQuestionText(gameData.questions[questionId - 1].text);
          setAnswerPrompts(gameData.questions[questionId - 1].answerPrompts);
        } catch (error) {
          console.error(error);
        }
      };
      fetchData(); // Invoke the fetchData function
      console.log('useEffect Done')
      setEditSubmitted(false); // Reset the formSubmitted flag
    }
  }, [editSubmitted]);

  // AnswerPrompt needs to be in answer array
  function getAnswersAsIndices (updatedAnswers) {
    const answersAsIndices = []
    for (let i = 0; i < updatedAnswers.length; i++) {
      answersAsIndices.push(getAnswers.indexOf(updatedAnswers[i]))
    }
    return answersAsIndices;
  }

  // creates empty question for user to edit
  function handleAddAnswerPrompt () {
    const answers = getAnswerPrompts;
    const newAnswerPrompt = 'Answer Prompt, please edit me!';
    if (getAnswerPrompts.includes(newAnswerPrompt)) {
      alert('New Prompt already added, Edit that before adding a new prompt');
      return;
    }
    // if there are only 2 answers, ignore
    if (getAnswerPrompts.length >= 6) {
      alert('Maximum 6 answers')
      return
    }

    answers.push(newAnswerPrompt);

    // grab questions and append to the one with id = questionId
    const questions = getQuestions;
    questions.answerPrompts = answers;
    questions.text = questionText;
    callUpdateQuiz(gameId, questions, title);
  }

  function questionChecked (answer) {
    // console.log('answererwrwer' + getAnswers.indexOf(answer))
    console.log('answers in QC: ' + getAnswers)
    if (getAnswers.includes(getAnswerPrompts.indexOf(answer))) {
      return true;
    } else {
      return false;
    }
  }

  function handleUpdateQuestionText (updatedText) {
    const questions = getQuestions;
    questions[questionId - 1].text = updatedText;
    callUpdateQuiz(gameId, questions, title);
  }

  function handleUpdateAnswerPrompt (updatedAnswerPrompt, prevAnswerPrompt) {
    // check if promp already exists
    if (getAnswerPrompts.includes(updatedAnswerPrompt)) {
      alert('Answer Prompt already Exists.')
      return
    }

    // get index of prevAnswerPrompt
    const currAnswerPrompts = getAnswerPrompts;
    const replacementIndex = currAnswerPrompts.indexOf(prevAnswerPrompt);

    const answers = getAnswers;
    const updatedAnswers = answers.filter(
      (answer) => answer !== prevAnswerPrompt
    );

    const questions = getQuestions;
    questions[questionId - 1].answerPrompts[replacementIndex] =
      updatedAnswerPrompt;
    questions[questionId - 1].answer = getAnswersAsIndices(updatedAnswers);
    callUpdateQuiz(gameId, questions, title);
  }

  // delete answers from answerprompts and answer arrays
  function handleDeleteAnswer (answerToBeDeleted) {
    // if there are only 2 answers, ignore
    if (getAnswerPrompts.length === 2) {
      alert('Minimum 2 answers required')
      return
    }

    if (getAnswers.length === 1 && getAnswers.includes(getAnswerPrompts.indexOf(answerToBeDeleted))) {
      alert('Trying to delete last answer');
      return;
    }

    const answerPrompts = getAnswerPrompts;
    console.log(answerToBeDeleted);
    console.log(answerPrompts);
    const updatedAnswerPrompts = answerPrompts.filter(
      (answer) => answer !== answerToBeDeleted
    );

    const indexToBeDeleted = getAnswerPrompts.indexOf(answerToBeDeleted);
    const answers = getAnswers;
    const updatedAnswers = answers.filter(
      (answer) => answer !== indexToBeDeleted
    );
    console.log(updatedAnswers)
    // update indices after the index to be deleted
    for (let i = 0; i < updatedAnswers.length; i++) {
      console.log('idTBD: ' + indexToBeDeleted)
      if (updatedAnswers[i] > indexToBeDeleted) {
        console.log('curr: ' + updatedAnswers[i])
        updatedAnswers[i] = updatedAnswers[i] - 1;
        console.log('after: ' + updatedAnswers[i])
      }
    }
    console.log('updated Ans: ' + updatedAnswers)
    const questions = getQuestions;
    questions[questionId - 1].answerPrompts = updatedAnswerPrompts;
    questions[questionId - 1].answer = updatedAnswers;
    callUpdateQuiz(gameId, questions, title);
  }

  //   function handleChange (e, answerPrompt) {
  //     handleCheckboxChange(e, answerPrompt);
  //   }

  const handleCheckboxChange = debounce((e, answerPromptIndex) => {
    if (e.target.checked === false) {
      // Perform an action when the checkbox is checked
      console.log(`${answerPromptIndex} is checked`);

      if (type === 'Single Answer') {
        console.log('case1')
        const questions = getQuestions;
        questions[questionId - 1].answer = [answerPromptIndex];
        callUpdateQuiz(gameId, questions, title);
      } else {
        console.log('case2')
        // Multiple Choice
        // if answer is already in the array, return
        if (getAnswers.includes(answerPromptIndex)) {
          return
        }
        const questions = getQuestions;
        questions[questionId - 1].answer.push(answerPromptIndex);
        callUpdateQuiz(gameId, questions, title);
        console.log('pushed' + answerPromptIndex + ' to answer array')
      }
    } else {
      // Perform an action when the checkbox is unchecked
      console.log(`${answerPromptIndex} is unchecked`);
      // if there's no answers left,
      console.log(answerPromptIndex)
      console.log(getAnswers.length)
      if (getAnswers.length === 1 && getAnswers.includes(answerPromptIndex)) {
        alert('One Answer Prompt must be checked');
        e.target.checked = true;
        return;
      }

      if (type === 'Single Answer') {
        console.log('case3')
        console.log('went into single Answer case ERROR')
      } else {
        console.log('case4')
        // Multiple Choice
        const questions = getQuestions;
        const answers = getAnswers;

        const updatedAnswers = answers.filter(
          (answer) => answer !== answerPromptIndex
        );
        questions[questionId - 1].answer = updatedAnswers;
        callUpdateQuiz(gameId, questions, title);
      }
    }
  }, 500);

  function handleUpdateTime (updatedTime) {
    const questions = getQuestions;
    questions[questionId - 1].time = updatedTime;
    callUpdateQuiz(gameId, questions, title);
  }

  function handleUpdatePoints (updatedPoints) {
    const questions = getQuestions;
    questions[questionId - 1].points = updatedPoints;
    callUpdateQuiz(gameId, questions, title);
  }

  function handleTypeChange (e) {
    const option = e.target.value;
    if (option === 'Single Answer') {
      console.log('chose single');
      const questions = getQuestions;
      questions[questionId - 1].type = option;

      // if there are multiple answer in answer, take the first as the only one
      const answers = getAnswers;
      if (answers.length > 1) {
        questions[questionId - 1].answer = [answers[0]];
      }
      callUpdateQuiz(gameId, questions, title);
    } else if (option === 'Multiple Answer') {
      console.log('chose multi');
      const questions = getQuestions;
      questions[questionId - 1].type = option;
      callUpdateQuiz(gameId, questions, title);
    }
  }

  return (
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
            Edit Question: {questionId}
          </h1>
        </div>
        <Container
          centered
          className="bg-light rounded-3 ps-5 pe-5 pb-2 pt-2"
          style={{ maxWidth: '900px' }}
        >
          <div className="pt-2">
            <Form
              noValidate
              className="p-2 pt-0"
              onSubmit={(e) => {
                e.preventDefault();
                handleUpdateQuestionText(e.target.questionText.value);
                setEditSubmitted(true);
                e.target.reset();
              }}
            >
              <Form.Label
                className="d-flex"
                style={{ alignItems: 'center', justifyContent: 'center' }}
              >
                <b className="me-2" style={{ fontSize: '25px' }}>
                  Q: {questionText}
                </b>
              </Form.Label>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                }}
              >
                <Form.Group className="mt-1 mb-3 w-50" controlId="questionText">
                  <Form.Control
                    type="text"
                    placeholder="Enter Question"
                    required
                    style={{ textAlign: 'center', maxWidth: '500px' }}
                  />
                </Form.Group>
              </div>
            </Form>
            <Form>
              <Form.Label
                className="d-flex"
                style={{ alignItems: 'center', justifyContent: 'center' }}
              >
                <b className="me-2" style={{ fontSize: '25px' }}>
                  Type: {type}
                </b>
              </Form.Label>
              <div
                className="d-flex mb-3"
                style={{ justifyContent: 'center', alignItems: 'center' }}
              >
                <Form.Select
                  style={{ textAlign: 'center', maxWidth: '500px' }}
                  onChange={(e) => {
                    e.preventDefault();
                    handleTypeChange(e);
                    setEditSubmitted(true);
                    const forms =
                      document.getElementsByClassName('answerPromptCard');
                    for (let i = 0; i < forms.length; i++) {
                      forms[i].reset();
                    }
                  }}
                >
                  <option>Select Question Type</option>
                  <option>Single Answer</option>
                  <option>Multiple Answer</option>
                </Form.Select>
              </div>
            </Form>
            <Form>
              <Form.Label
                className="d-flex mb-0"
                style={{ alignItems: 'center', justifyContent: 'center' }}
              >
                <b className="me-2" style={{ fontSize: '25px' }}>
                  Answers
                </b>
              </Form.Label>
              <div className='d-flex justify-content-center'>
              </div>
              <div className="mb-1" style={{ textAlign: 'center' }}>
                <i>Click the checkboxes to indicate the correct answer/s</i>
              </div>
            </Form>
            <div className="p-5 pb-1 pt-1 mb-1">
              {/* <Form onSubmit={(e) => { e.preventDefault(); handleUpdateAnswerPrompt(e.target.formPassword.value, answer); setEditSubmitted(true); e.target.reset(); }} key={answer}> */}
              <div
                className="d-flex mx-auto flex-row flex-wrap"
                style={{ alignItems: 'center', justifyContent: 'center' }}
              >
                <AnswerList
                handleUpdateAnswerPrompt={handleUpdateAnswerPrompt}
                handleCheckboxChange={handleCheckboxChange}
                handleDeleteAnswer={handleDeleteAnswer}
                setEditSubmitted={setEditSubmitted}
                questionChecked={questionChecked}
                getAnswerPrompts={getAnswerPrompts} />
                <Button
                  className='m-1'
                  onClick={() => {
                    handleAddAnswerPrompt();
                    setEditSubmitted(true);
                  }}
                  style={{ height: '150px', width: '18rem', backgroundColor: '#ceb0fd', borderColor: '#ceb0fd', fontSize: '30px', fontWeight: '500' }}
                >
                  + Answer
                </Button>
              </div>
            </div>
            <div className="d-flex flex-wrap justify-content-center">
              <Form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleUpdateTime(parseInt(e.target.time.value));
                  setEditSubmitted(true);
                  e.target.reset();
                }}
              >
                <div className="m-1">
                  <Form.Group className="mt-1 mb-3" controlId="time">
                    <div
                      className="d-flex justify-content-center mb-2"
                      style={{ minWidth: '250px' }}
                    >
                      Time Limit: {time}s
                    </div>
                    <Form.Control
                      type="text"
                      placeholder="Enter Time Limit"
                      required
                      style={{ textAlign: 'center', maxWidth: '500px' }}
                    />
                  </Form.Group>
                </div>
              </Form>
              <Form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleUpdatePoints(parseInt(e.target.points.value));
                  setEditSubmitted(true);
                  e.target.reset();
                }}
              >
                <div className="m-1">
                  <Form.Group className="mt-1 mb-3" controlId="points">
                    <div
                      className="d-flex justify-content-center mb-2"
                      style={{ minWidth: '250px' }}
                    >
                      Points: {points}pts
                    </div>
                    <Form.Control
                      type="text"
                      placeholder="Enter Points"
                      required
                      style={{ textAlign: 'center', maxWidth: '500px' }}
                    />
                  </Form.Group>
                </div>
              </Form>
            </div>

            <Form>
              <Form.Label
                className="d-flex"
                style={{ alignItems: 'center', justifyContent: 'center' }}
              >
                <b className="me-2" style={{ fontSize: '25px' }}>
                  Photo{' '}
                  <i style={{ fontSize: '20px', fontWeight: '500' }}>
                    (optional)
                  </i>
                </b>
              </Form.Label>
              <div
                className="d-flex mb-3"
                style={{ justifyContent: 'center', alignItems: 'center' }}
              >
                <Form.Control
                  type="file"
                  style={{ textAlign: 'center', maxWidth: '500px' }}
                  onChange={(e) => {
                    handleThumbnailUpload(e);
                  }}
                />
              </div>
              <Form.Label
                className="d-flex"
                style={{ alignItems: 'center', justifyContent: 'center' }}
              >
                <b className="me-2" style={{ fontSize: '25px' }}>
                  Video URL{' '}
                  <i style={{ fontSize: '20px', fontWeight: '500' }}>
                    (optional)
                  </i>
                </b>
              </Form.Label>
              <div
                className="d-flex mb-3"
                style={{ justifyContent: 'center', alignItems: 'center' }}
              >
                <Form.Group className="mt-1" controlId="formPassword">
                  <Form.Control
                    type="text"
                    placeholder="Type a valid URL"
                    required
                    style={{ textAlign: 'center', maxWidth: '500px' }}
                    onChange={(e) => {
                      handleURLUpload(e);
                      setEditSubmitted(true);
                    }}
                  />
                </Form.Group>
              </div>
            </Form>
          </div>
          <div className="d-flex justify-content-center">
            <Button
              variant="secondary"
              onClick={() => navigate(-1)}
              className="w-75 m-3"
            >
              Back
            </Button>
          </div>
        </Container>
      </div>
    </>
  );
}
