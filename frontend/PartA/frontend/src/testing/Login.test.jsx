import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import Login from '../Login';
import { MemoryRouter } from 'react-router-dom';

import '@testing-library/jest-dom';

jest.mock('bootstrap/dist/css/bootstrap.min.css', () => '');

jest.mock('axios');

describe('Login component', () => {
  it('should render an email input, password input, and a login button', () => {
    render(
    <MemoryRouter>
      <Login />
    </MemoryRouter>
    );
    const emailInput = screen.getByPlaceholderText('Enter email');
    const passwordInput = screen.getByPlaceholderText('Password');
    const loginButton = screen.getByText('Login');

    expect(emailInput).toBeInTheDocument();
    expect(passwordInput).toBeInTheDocument();
    expect(loginButton).toBeInTheDocument();
  });

  it('should display an error message for invalid email', async () => {
    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );
    fireEvent.change(screen.getByPlaceholderText('Enter email'), { target: { value: 'invalidemail' } });
    fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'testpassword' } });
    fireEvent.click(screen.getByText('Login'));

    const errorMessage = await screen.findByText('Invalid email');
    expect(errorMessage).toBeInTheDocument();
  });

  it('should call axios.post with email and password when the login button is clicked', async () => {
    const responseData = { data: { token: 'fake_token' } };
    axios.post.mockResolvedValue(responseData);

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );
    fireEvent.change(screen.getByPlaceholderText('Enter email'), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'testpassword' } });
    fireEvent.click(screen.getByText('Login'));

    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
        expect.any(String),
        { email: 'test@example.com', password: 'testpassword' },
        expect.any(Object)
      );
    });
  });

  it('should display an error message when axios.post returns an error', async () => {
    axios.post.mockRejectedValue(new Error('Request failed'));

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );
    fireEvent.change(screen.getByPlaceholderText('Enter email'), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'testpassword' } });
    fireEvent.click(screen.getByText('Login'));

    const errorMessage = await screen.findByText('Invalid email or password.');
    expect(errorMessage).toBeInTheDocument();
  });
});
