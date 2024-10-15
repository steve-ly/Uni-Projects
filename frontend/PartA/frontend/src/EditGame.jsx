import React, { useState, useEffect } from 'react';

import { Container, Button, Form, Card, CloseButton } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { callUpdateQuiz, callGetUniqueQuiz, callUpdateQuizThumbnail } from './Admin';
import logo from './img/bigbrain_logo_1.png';
// helper to convert file to base64
export function fileToDataUrl (file) {
  const validFileTypes = ['image/jpeg', 'image/png', 'image/jpg']
  const valid = validFileTypes.find(type => type === file.type);
  // Bad data, let's walk away.
  if (!valid) {
    throw Error('provided file is not a png, jpg or jpeg image.');
  }

  const reader = new FileReader();
  const dataUrlPromise = new Promise((resolve, reject) => {
    reader.onerror = reject;
    reader.onload = () => resolve(reader.result);
  });
  reader.readAsDataURL(file);
  return dataUrlPromise;
}
// function to allow user to edit a specific quiz/game
export default function EditGame (props) {
  let { gameId } = useParams();
  gameId = parseInt(gameId);
  const navigate = useNavigate();
  const routeEditQuestion = (questionId) => {
    navigate(`/EditQuestion/${gameId}/${questionId}`);
  };
  const [getQuestions, setquestions] = useState([]);
  const [editSubmitted, setEditSubmitted] = useState(true);
  const [title, setTitle] = useState('');

  // renders page on start up and whenever an edit is made
  useEffect(() => {
    if (editSubmitted) {
      // Fetch data from an API or perform other asynchronous operations
      const fetchData = async () => {
        try {
          const questions = await callGetUniqueQuiz(gameId);
          setTitle(questions.name);
          setquestions(questions.questions);
        } catch (error) {
          console.error(error);
        }
      };
      fetchData(); // Invoke the fetchData function
      setEditSubmitted(false); // Reset the formSubmitted flag
    }
  }, [editSubmitted]);

  // creates empty question for user to edit
  function handleAddQuiz () {
    const questions = getQuestions;
    let getNewId = 1;
    if (questions.length !== undefined) {
      getNewId = questions.length + 1;
    }
    console.log(getNewId);
    const newQuestion = {
      id: getNewId,
      text: 'Question Text, please edit me!',
      time: 30,
      points: 100,
      answerPrompts: ['Answer 1, Please Edit me!', 'Answer 2, Please Edit me!'],
      answer: [0],
      type: 'Single Answer',
      img: logo,
    };

    questions.push(newQuestion);
    console.log(questions);
    callUpdateQuiz(gameId, questions, title);
  }

  function handleupdateTitle (newTitle) {
    callUpdateQuiz(gameId, getQuestions, newTitle);
  }

  function handleDeleteQuestion (removeId) {
    let questionsRemoved = getQuestions;
    questionsRemoved = questionsRemoved.filter(
      (question) => question.id !== removeId
    );
    let i = 0;
    while (i < questionsRemoved.length) {
      questionsRemoved[i].id = i + 1;
      i++;
    }
    callUpdateQuiz(gameId, questionsRemoved, title);
  }

  const handleThumbnailUpload = (e) => {
    console.log('updated Thumbnail')
    const file = e.target.files[0];
    fileToDataUrl(file).then((base64str) => { // change to base64
      console.log(base64str);
      callUpdateQuizThumbnail(gameId, getQuestions, title, base64str);
      console.log('thumbnail edited')
    });
  }

  const handleGameUpload = (e) => {
    console.log('attempting to upload game')
    const file = e.target.files[0];
    if (!file) {
      alert('Please select a JSON file to upload');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const jsonData = JSON.parse(e.target.result);
        console.log('JSON data:', jsonData);
        console.log(Object.keys(jsonData));
        const key = Object.keys(jsonData)[0];
        const title = jsonData[key].name;
        const questions = jsonData[key].questions;
        const thumbnail = jsonData[key].thumbnail;

        callUpdateQuizThumbnail(gameId, questions, title, thumbnail)
      } catch (error) {
        alert('Invalid JSON file');
        console.error(error);
      }
      setEditSubmitted(true);
    };
    reader.readAsText(file);
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
            Edit Game
          </h1>
        </div>
        <Container
          className="bg-light rounded-3"
          style={{ maxWidth: '900px' }}
        >
          <div className="pt-2">
            <Form
              noValidate
              className="p-2 pt-0"
              onSubmit={(e) => {
                e.preventDefault();
                handleupdateTitle(e.target.formPassword.value);
                setEditSubmitted(true);
                e.target.reset();
              }}
            >
              <Form.Label
                className="d-flex"
                style={{ alignItems: 'center', justifyContent: 'center' }}
              >
                <b className="me-2" style={{ fontSize: '25px' }}>
                  Title: {title}
                </b>
              </Form.Label>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                }}
              >
                <Form.Group className="mt-1 mb-2" controlId="formPassword">
                  <Form.Control
                    type="text"
                    placeholder="Enter title"
                    required
                    style={{ maxWidth: '500px', textAlign: 'center' }}
                  />
                </Form.Group>
              </div>
              <Form.Label
                className="d-flex"
                style={{ alignItems: 'center', justifyContent: 'center' }}
              >
                <b className="me-2 mt-3" style={{ fontSize: '25px' }}>
                  Questions
                </b>
              </Form.Label>
              <div style={{ textAlign: 'center' }}>
                <div
                  className="d-flex mx-auto flex-row flex-wrap"
                  style={{ alignItems: 'center', justifyContent: 'center' }}
                >
                  {getQuestions.map((type) => (
                    <div key={`default-${type.id}`} className="m-1">
                      <Card style={{ width: '18rem' }}>
                        <Card.Header
                          className="d-flex justify-content-between"
                          style={{ backgroundColor: '#ffb0ce' }}
                        >
                          Question: {`${type.id}`}
                          <CloseButton
                            onClick={() => {
                              handleDeleteQuestion(type.id);
                              setEditSubmitted(true);
                            }}
                          />
                        </Card.Header>
                        <Card.Body>
                          <Card.Text>{`${type.text}`}</Card.Text>
                        </Card.Body>
                        <Card.Footer>
                          <div className="d-flex justify-content-end">
                            <Button
                              className=""
                              onClick={() => routeEditQuestion(type.id)}
                              style={{
                                backgroundColor: '#ea6d9d',
                                borderColor: '#ea6d9d',
                              }}
                            >
                              Edit
                            </Button>
                          </div>
                        </Card.Footer>
                      </Card>
                    </div>
                  ))}
                  <div>
                    <Button
                      variant="dark"
                      onClick={() => {
                        handleAddQuiz();
                        setEditSubmitted(true);
                      }}
                      style={{
                        height: '150px',
                        width: '18rem',
                        backgroundColor: '#ffb0ce',
                        borderColor: '#ffb0ce',
                        fontSize: '30px',
                        fontWeight: '500',
                      }}
                    >
                      + Question
                    </Button>
                  </div>
                </div>
              </div>
              </Form>
              <Form>
              <Form.Label
                className="d-flex"
                style={{ alignItems: 'center', justifyContent: 'center' }}
              >
                <b className="me-2 mt-3" style={{ fontSize: '25px' }}>
                  Thumbnail
                </b>
              </Form.Label>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                }}
              >
                <Form.Control type="file" accept='image/*' style={{ maxWidth: '500px' }} onChange={(e) => {
                  handleThumbnailUpload(e);
                  setEditSubmitted(true);
                }}/>
              </div>
              <div
                className="mt-3 mb-3"
                style={{
                  textAlign: 'center',
                  fontSize: '30px',
                  fontWeight: '700',
                }}
              >
                OR
              </div>
              </Form>
              <Form>
              <div className='d-flex justify-content-center'>
                <div
                  className="p-5 rounded-3"
                  style={{ backgroundColor: '#dde0e3', maxWidth: '600px' }}
                >
                  <Form.Label
                    className="d-flex"
                    style={{ alignItems: 'center', justifyContent: 'center' }}
                  >
                    <div className="" style={{ fontSize: '15px' }}>
                      Upload .json Game File
                    </div>
                  </Form.Label>
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'center',
                      alignItems: 'center',
                    }}
                  >
                    <Form.Control type="file" accept='.json' style={{ maxWidth: '500px' }} onChange={(e) => {
                      handleGameUpload(e);
                    }}/>
                  </div>
                </div>
              </div>
            </Form>
          </div>
          <div className="d-flex justify-content-center">
            <Button
              variant="secondary"
              className="w-75 m-3"
              onClick={() => navigate(-1)}
            >
              Back
            </Button>
          </div>
        </Container>
      </div>
    </>
  );
}
