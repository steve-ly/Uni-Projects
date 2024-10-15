import React, { useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';
import { callPlayerSubmit } from './Player'
// Displays all answer prompts to user and allows multiple to be selected
function AnswerOptionsMulti ({ answerPrompts, playerId, timeOver }) {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [click, setClick] = useState(false)
  // Checks for the state of the button and submitts choices to backend if time is not over
  function handleOptionClick (option) {
    if (timeOver) {
      return
    }
    setClick(true);
    if (selectedOptions.includes(option)) {
      const updatedOptions = selectedOptions.filter((selectedOption) => selectedOption !== option);
      setSelectedOptions(updatedOptions);
    } else {
      const updatedOptions = [...selectedOptions, option];
      setSelectedOptions(updatedOptions);
    }
  }
  // Sends the api call
  useEffect(() => {
    async function submitData (answer) {
      try {
        await callPlayerSubmit(playerId, answer);
      } catch (error) {
        console.error(error);
      }
    }
    if (click !== false) {
      const answers = []
      let i = 0
      while (i < selectedOptions.length) {
        answers.push(answerPrompts.indexOf(selectedOptions[i]))
        i = i + 1
      }
      submitData(answers)
    }
  }, [selectedOptions])
  // render component
  return (
    <div>
      {answerPrompts.map((option, index) => (
        <Button
          key={index}
          className='m-1'
          variant={selectedOptions.includes(option) ? 'primary' : 'danger'}
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

export default AnswerOptionsMulti;
