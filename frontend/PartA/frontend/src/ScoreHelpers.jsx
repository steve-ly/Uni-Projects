import { Bar } from 'react-chartjs-2';
import React from 'react';

// helpers to caluclate the score averages and percentages and renders components to display information

// get top 5
export function calculateTopScores (questions, answers) {
  console.log(questions)
  console.log(answers)
  const scores = [];

  // iterate through each player's answers
  for (let j = 0; j < answers.length; j++) {
  // initialize the player's score to 0
    let score = 0;

    // iterate through each question
    for (let i = 0; i < questions.length; i++) {
    // if the player got the question correct, calculate their score
      if (answers[j].answers[i].correct) {
        let timeElapsed = 0
        if (answers[j].answers[i].answeredAt === null || answers[j].answers[i].questionStartedAt === null) {
          timeElapsed = 0
        } else {
          const timeStarted = new Date(answers[j].answers[i].questionStartedAt)
          const timeCompleted = new Date(answers[j].answers[i].answeredAt);
          timeElapsed = Math.floor((timeCompleted - timeStarted) / 1000);
        }
        if (timeElapsed < 0) {
          timeElapsed = 0;
        }
        const maxTime = questions[i].time;
        const points = questions[i].points;
        score += points * (maxTime - timeElapsed);
        console.log('The score is ' + score)
      }
    }

    scores.push({ name: answers[j].name, score });
  }

  scores.sort((a, b) => b.score - a.score);

  return scores.slice(0, 5);
}

export function averageTime (questions, answers) {
  const elapsedTime = questions.map(() => []);
  let timeElapsed = 0;
  for (let j = 0; j < answers.length; j++) {
    for (let i = 0; i < questions.length; i++) {
      if (answers[j].answers[i].answeredAt === null || answers[j].answers[i].questionStartedAt === null) {
        timeElapsed = 0
      } else {
        const timeStarted = new Date(answers[j].answers[i].questionStartedAt)
        const timeCompleted = new Date(answers[j].answers[i].answeredAt);
        timeElapsed = Math.floor((timeCompleted - timeStarted) / 1000);
      }
      if (timeElapsed > questions[i].time) {
        timeElapsed = questions[i].time;
      }
      elapsedTime[i].push(timeElapsed);
    }
  }

  const avgElapsedTime = elapsedTime.map((times) => {
    if (times.length === 0) {
      return 0;
    }
    const sum = times.reduce((acc, val) => acc + val, 0);
    return sum / times.length;
  });
  return (avgElapsedTime);
}

export function percentage (questions, answers) {
  const correctAnswers = questions.map(() => 0);

  for (let j = 0; j < answers.length; j++) {
    for (let i = 0; i < questions.length; i++) {
      if (answers[j].answers[i].correct) {
        correctAnswers[i]++;
      }
    }
  }
  const numPlayers = answers.length;
  const percentCorrect = correctAnswers.map((numCorrect) => (numCorrect / numPlayers) * 100);
  console.log(percentCorrect)
  return percentCorrect;
}

export const AnswerDistributionChart = ({ probabilities }) => {
  if (!probabilities) {
    return null;
  }

  const labels = probabilities.map((_, index) => `Q${index + 1}`);
  const incorrectData = probabilities.map(prob => 100 - prob);

  const data = {
    labels,
    datasets: [
      {
        label: 'Incorrect',
        data: incorrectData,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Correct',
        data: probabilities,
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };

  const options = {
    indexAxis: 'y',
    elements: {
      bar: {
        borderWidth: 2,
      },
    },
    responsive: true,
    plugins: {
      legend: {
        position: 'right',
      },
      title: {
        display: true,
        text: 'Answer Distributions',
      },
    },
  };

  return <Bar data={data} options={options} />;
};

export const AnswerResponseTime = ({ responseTime }) => {
  if (!responseTime) {
    return null;
  }

  const labels = responseTime.map((_, index) => `Q${index + 1}`);

  const data = {
    labels,
    datasets: [
      {
        label: 'Average Time',
        data: responseTime,
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Answer Response Times',
      },
    },
  };

  return <Bar data={data} options={options} />;
};
