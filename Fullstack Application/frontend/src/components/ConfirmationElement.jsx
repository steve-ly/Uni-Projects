import React, { useState, useContext, useCallback, createContext } from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';

const ConfirmationContext = createContext()

export const UseConfirmation = () => {
  const context = useContext(ConfirmationContext)

  if (!context) { throw new Error('useConfirmation must be used within a ConfirmationProvider') }

  return context
};

export const ConfirmationProvider = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [onConfirmCallback, setOnConfirmCallback] = useState(() => () => {});
  const [description, setDescription] = useState('');

  const openConfirmation = useCallback((onConfirm, description) => {
    setIsOpen(true)
    setOnConfirmCallback(() => () => {
      onConfirm()
      setIsOpen(false)
    });
    setDescription(description)
  }, [])

  const closeConfirmation = useCallback(() => {
    setIsOpen(false);
    setOnConfirmCallback(() => () => {});
    // setDescription('')
  }, []);

  const confirmAction = useCallback(() => {
    onConfirmCallback();
  }, [onConfirmCallback])

  return (
    <ConfirmationContext.Provider value={openConfirmation}>
      {children}
      <Dialog open={isOpen} onClose={closeConfirmation}>
        <DialogTitle>Confirm Action</DialogTitle>
        <DialogContent>
          <DialogContentText>Are you sure you want to {description}?</DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeConfirmation} color="primary">
            Cancel
          </Button>
          <Button onClick={confirmAction} color="primary" autoFocus>
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </ConfirmationContext.Provider>
  );
}
