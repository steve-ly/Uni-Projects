import React from 'react';
import { Form, Card, CloseButton } from 'react-bootstrap';

export default function AnswerList ({
  handleUpdateAnswerPrompt,
  handleCheckboxChange,
  handleDeleteAnswer,
  setEditSubmitted,
  questionChecked,
  getAnswerPrompts,
}) {
  return (
    <>
      {getAnswerPrompts.map((answer) => (
        <div key={`default-${answer}`} className="m-1">
          <Form
            className="answerPromptCard"
            onSubmit={(e) => {
              e.preventDefault();
              handleUpdateAnswerPrompt(e.target.formPassword.value, answer);
              setEditSubmitted(true);
              e.target.reset();
            }}
          >
            <Card style={{ width: '18rem' }}>
              <Card.Header
                className="d-flex justify-content-between"
                style={{ backgroundColor: '#CEB0FD' }}
              >
                <div>Answer</div>
                <CloseButton
                  onClick={() => {
                    handleDeleteAnswer(answer);
                    setEditSubmitted(true);
                  }}
                />
              </Card.Header>
              <Card.Body>
                <Form.Check // prettier-ignore
                  type={'checkbox'}
                  label={answer}
                  defaultChecked={questionChecked(answer)}
                  onChange={(e) => {
                    handleCheckboxChange(e, getAnswerPrompts.indexOf(answer));
                    setEditSubmitted(true);
                    const cards =
                      document.getElementsByClassName('answerPromptCard');
                    for (let i = 0; i < cards.length; i++) {
                      cards[i].reset();
                    }
                    setTimeout(() => {
                      window.location.reload();
                    }, 1000);
                  }}
                />
                <Form.Group className="mt-1 mb-3" controlId="formPassword">
                  <Form.Control
                    type="text"
                    placeholder="Enter Answer"
                    required
                  />
                </Form.Group>
              </Card.Body>
            </Card>
          </Form>
        </div>
      ))}
    </>
  );
}
