import React, { useState } from 'react';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import CreateVolunteerPage from './components/CreateVolunteerPage';
import CreateOrganiserPage from './components/CreateOrganiserPage';
import { ConfirmationProvider } from './components/ConfirmationElement';

import DashboardPage from './components/DashboardPage';
import VolunteerListPage from './components/VolunteerListPage';
import GroupchatPage from './components/GroupchatPage';
import SchedulePage from './components/SchedulePage';
import AttendanceLogPage from './components/AttendanceLogPage';
import AttendanceListPage from './components/AttendanceListPage';
import TasksPage from './components/TasksPage';

import { AuthProvider } from './components/AuthContext'; // Import AuthProvider

function App () {
  const [token] = useState(null);

  return (
    <ConfirmationProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route
              exact
              path="/"
              element={token ? <Navigate to="/dashboard" /> : <Navigate to="/login" />}
            />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/createvolunteer" element={<CreateVolunteerPage />} />
            <Route path="/createorganiser" element={<CreateOrganiserPage />} />

            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/volunteerlist" element={<VolunteerListPage />} />
            <Route path="/groupchat" element={<GroupchatPage />} />
            <Route path="/schedule" element={<SchedulePage />} />
            <Route path="/attendancelog" element={<AttendanceLogPage />} />
            <Route path="/attendancelist" element={<AttendanceListPage />} />
            <Route path="/tasks" element={<TasksPage />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ConfirmationProvider>
  );
}

export default App;
