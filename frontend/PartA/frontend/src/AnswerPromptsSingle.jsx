import React, { useState, useEffect } from 'react';
import { Button } from 'react-bootstrap'
import { callPlayerSubmit } from './Player'
// Displays all answer prompts and only allows user to select 1 at a time
function AnswerOptionsSingle ({ answerPrompts, playerId, timeOver }) {
  const [selectedOption, setSelectedOption] = useState(null);
  const [click, setClick] = useState(false)
  // checks if we are selecting or deselecting and set state to choice
  function handleOptionClick (option) {
    if (timeOver) {
      setSelectedOption(null);
      return
    }
    setClick(true);
    if (selectedOption === option) {
      setSelectedOption(null);
    } else {
      setSelectedOption(option);
    }
  }
  // send api call with choice
  useEffect(() => {
    async function submitData (answer) {
      try {
        const response = await callPlayerSubmit(playerId, answer);
        console.log(response);
      } catch (error) {
        console.error(error);
      }
    }
    if (click !== false) {
      const answers = []
      answers.push(answerPrompts.indexOf(selectedOption))
      console.log(answers)
      submitData(answers)
    }
  }, [selectedOption])
  // render component
  return (
    <div>
      {answerPrompts.map((option, index) => (
        <Button
          key={index}
          className='m-1'
          variant={timeOver ? 'danger' : selectedOption === option ? 'primary' : 'danger'}
          style={{ minHeight: '50px', maxHeight: '200px', minWidth: '300px' }}
          onClick={() => handleOptionClick(option)}
          disabled={timeOver}
        >
          {option}
        </Button>
      ))}
    </div>
  );
}

export default AnswerOptionsSingle;
