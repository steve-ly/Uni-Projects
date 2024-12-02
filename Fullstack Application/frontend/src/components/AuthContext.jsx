import { React, createContext, useState, useEffect } from 'react';

export const AuthContext = createContext({
  token: null,
  setToken: () => {},
})

export const AuthProvider = ({ children }) => {
  const [token, setTokenState] = useState(() => localStorage.getItem('token') || null);

  const setToken = (newToken) => {
    setTokenState(newToken);
    localStorage.setItem('token', newToken);
  }

  useEffect(() => {
    // Set token from localStorage on component mount
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setTokenState(storedToken);
    }
  }, [])

  return (
    <AuthContext.Provider value={{ token, setToken }}>
      {children}
    </AuthContext.Provider>
  )
}
