import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Patients from './pages/Patients';
import Prediction from './pages/Prediction';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-[#0f172a] text-white">
        <Sidebar />
        <div className="flex-1 flex flex-col overflow-hidden">
          <Header />
          <main className="flex-1 overflow-x-hidden overflow-y-auto p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/patients" element={<Patients />} />
              <Route path="/predict/:patientId" element={<Prediction />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
