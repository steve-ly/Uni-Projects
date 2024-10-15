import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Welcome from './LandingPage';
import GameCardList from './GameCardList';
import { MemoryRouter, useNavigate } from 'react-router-dom';

import '@testing-library/jest-dom';

jest.mock('bootstrap/dist/css/bootstrap.min.css', () => '')
// code snippet from https://stackoverflow.com/questions/66284286/react-jest-mock-usenavigate
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: jest.fn(),
}));

// by exaucae posted april 1st 2021 edited april 25 2021
// WELCOME Component:
//     TEST 1: is a basic rendering test to ensure that the img logo and two navigating buttons are present
//     TEST 2: Since we can observe ourself if the render is working or not, we check for features that we can't see
//             so test button admin correctly routes to './login' on click
//     TEST 3: Same as test 2 but instead checks if the play button correctly routes to './play'
//    Testing this component will ensure other components with the same method of onClick -> route is correct

describe('Welcome component', () => {
  it('should render a logo and two buttons', () => {
    const { getByAltText, getByText } = render(<MemoryRouter>
        <Welcome />
      </MemoryRouter>);
    const logo = getByAltText('bigbrain_logo');
    const adminButton = getByText('Admin');
    const playerButton = getByText('Player');

    expect(logo).toBeInTheDocument();
    expect(adminButton).toBeInTheDocument();
    expect(playerButton).toBeInTheDocument();
  });

  it('should navigate to "/Login" when the "Admin" button is clicked', () => {
    const mockNavigate = jest.fn();
    useNavigate.mockReturnValue(mockNavigate);

    render(
          <MemoryRouter>
            <Welcome />
          </MemoryRouter>
    );

    const adminButton = screen.getByText('Admin');
    fireEvent.click(adminButton);

    expect(mockNavigate).toHaveBeenCalledWith('/Login');
  });
  it('should navigate to "/Login" when the "Player" button is clicked', () => {
    const mockNavigate = jest.fn();
    useNavigate.mockReturnValue(mockNavigate);

    render(
          <MemoryRouter>
            <Welcome />
          </MemoryRouter>
    );

    const playerButton = screen.getByText('Player');
    fireEvent.click(playerButton);

    expect(mockNavigate).toHaveBeenCalledWith('/Play');
  });
});

describe('GameCardList component', () => {
  const gamecards = [{
    id: 1,
    name: 'Game 1',
    thumbnail: 'image1.jpg',
    active: '12345',
    questions: [],
    createdAt: '2022-01-01T00:00:00.000Z',
  }];
  const gamecards2 = [
    {
      id: 1,
      name: 'Game 1',
      thumbnail: 'image1.jpg',
      active: '12345',
      questions: [],
      createdAt: '2022-01-01T00:00:00.000Z',
    },
    {
      id: 2,
      name: 'Game 2',
      thumbnail: 'image2.jpg',
      active: '67890',
      questions: [],
      createdAt: '2022-02-02T00:00:00.000Z',
    },
  ];

  const handleShow = jest.fn();
  const handlePastSessionsShow = jest.fn();
  const handleResultsShow = jest.fn();
  const handleDelete = jest.fn();
  const getCardID = jest.fn();

  it('renders correctly for 1 gamecard', () => {
    const { getByText, getByRole } = render(
        <GameCardList
          gamecards={gamecards}
          handleShow={handleShow}
          handlePastSessionsShow={handlePastSessionsShow}
          handleResultsShow={handleResultsShow}
          handleDelete={handleDelete}
          getCardID={getCardID}
        />
    );

    // Check if card title is rendered
    expect(getByText('Game 1')).toBeInTheDocument();

    // Check if card image is rendered
    const images = getByRole('img');
    expect(images).toHaveAttribute('src', 'image1.jpg');

    // Check if session ID is rendered
    expect(getByText('SessionID: 12345')).toBeInTheDocument();

    // Check if "Start Game" button is rendered
    expect(getByText('Start Game')).toBeInTheDocument();

    // Check if "Go Next" and "Edit" buttons are rendered
    expect(getByText('Go Next')).toBeInTheDocument();
    expect(getByText('Edit')).toBeInTheDocument();
  });

  it('renders correctly with multiple gamecards', () => {
    const { getByText, getAllByRole, getAllByText } = render(
      <GameCardList
        gamecards={gamecards2}
        handleShow={handleShow}
        handlePastSessionsShow={handlePastSessionsShow}
        handleResultsShow={handleResultsShow}
        handleDelete={handleDelete}
        getCardID={getCardID}
      />
    );

    // Check if card titles are rendered
    expect(getByText('Game 1')).toBeInTheDocument();
    expect(getByText('Game 2')).toBeInTheDocument();

    // Check if card images are rendered
    const images = getAllByRole('img');
    expect(images).toHaveLength(2);
    expect(images[0]).toHaveAttribute('src', 'image1.jpg');
    expect(images[1]).toHaveAttribute('src', 'image2.jpg');

    // Check if session IDs are rendered
    expect(getByText('SessionID: 12345')).toBeInTheDocument();
    expect(getByText('SessionID: 67890')).toBeInTheDocument();

    // Check if "Start Game" buttons are rendered
    const startGameButtons = getAllByText('Start Game');
    expect(startGameButtons).toHaveLength(2);

    // Check if "Go Next" and "Edit" buttons are rendered
    const editGameButtons = getAllByText('Edit');
    expect(editGameButtons).toHaveLength(2);
  });

  it('renders correctly with multiple gamecards', () => {
    const { getByText, getAllByRole, getAllByText } = render(
      <GameCardList
        gamecards={gamecards2}
        handleShow={handleShow}
        handlePastSessionsShow={handlePastSessionsShow}
        handleResultsShow={handleResultsShow}
        handleDelete={handleDelete}
        getCardID={getCardID}
      />
    );

    // Check if card titles are rendered
    expect(getByText('Game 1')).toBeInTheDocument();
    expect(getByText('Game 2')).toBeInTheDocument();

    // Check if card images are rendered
    const images = getAllByRole('img');
    expect(images).toHaveLength(2);
    expect(images[0]).toHaveAttribute('src', 'image1.jpg');
    expect(images[1]).toHaveAttribute('src', 'image2.jpg');

    // Check if session IDs are rendered
    expect(getByText('SessionID: 12345')).toBeInTheDocument();
    expect(getByText('SessionID: 67890')).toBeInTheDocument();

    // Check if "Start Game" buttons are rendered
    const startGameButtons = getAllByText('Start Game');
    expect(startGameButtons).toHaveLength(2);

    // Check if "Go Next" and "Edit" buttons are rendered
    const editGameButtons = getAllByText('Edit');
    expect(editGameButtons).toHaveLength(2);
  });
});
