import React, { useState, useEffect } from 'react';
import { Plus, Search, UserPlus } from 'lucide-react';
import { patientService } from '../services/api';
import { Link } from 'react-router-dom';

const Patients = () => {
  const [patients, setPatients] = useState([]);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      const response = await patientService.getAll();
      setPatients(response.data);
    } catch (error) {
      console.error('Error fetching patients:', error);
    }
  };

  const filteredPatients = patients.filter(p => 
    p.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold text-white">Patient Management</h2>
        <button 
          onClick={() => setIsFormOpen(true)}
          className="bg-primary-600 hover:bg-primary-500 text-white px-6 py-2 rounded-xl flex items-center space-x-2 transition-all shadow-lg shadow-primary-600/20"
        >
          <Plus size={20} />
          <span>Add Patient</span>
        </button>
      </div>

      <div className="glass-morphism rounded-2xl border border-white/10 p-6">
        <div className="relative max-w-md mb-8">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          <input
            type="text"
            placeholder="Search by name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-white/5 border border-white/10 rounded-xl py-2 pl-10 pr-4 focus:outline-none focus:ring-2 focus:ring-primary-500/50"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPatients.length > 0 ? (
            filteredPatients.map((patient) => (
              <div key={patient.id} className="glass-morphism p-6 rounded-2xl border border-white/10 hover:border-primary-500/50 transition-all group">
                <div className="flex items-center space-x-4 mb-4">
                  <div className="w-12 h-12 rounded-xl bg-primary-500/10 flex items-center justify-center text-primary-400">
                    <UserPlus size={24} />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg">{patient.name}</h3>
                    <p className="text-sm text-gray-400">{patient.age} years • {patient.gender}</p>
                  </div>
                </div>
                <div className="flex items-center justify-between text-sm text-gray-400 mb-6">
                  <span>BMI: <span className="text-white font-medium">{patient.bmi}</span></span>
                  <span>Joined: <span className="text-white font-medium">{new Date(patient.created_at).toLocaleDateString()}</span></span>
                </div>
                <Link 
                  to={`/predict/${patient.id}`}
                  className="block w-full text-center py-2 bg-white/5 hover:bg-white/10 rounded-lg border border-white/10 transition-colors font-medium"
                >
                  Analyze Health
                </Link>
              </div>
            ))
          ) : (
            <div className="col-span-full py-12 text-center text-gray-500">
              No patients found. Add your first patient to get started.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Patients;
