// I made this because didnt know how to import (have in the same file) 2 default functions (callender and the list one)
// Into CreateVolunteer. This should go into containers but idk how now and will fix later
import * as React from 'react';
import { DemoContainer, DemoItem } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';

export default function ResponsiveDatePickers ({ selectedDate, onDateChange }) {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DemoContainer components={['DesktopDatePicker']}>
        <DemoItem>
          <DesktopDatePicker value={selectedDate} onChange={onDateChange} />
        </DemoItem>
      </DemoContainer>
    </LocalizationProvider>
  );
}
