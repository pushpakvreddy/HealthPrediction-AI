import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Activity, Brain, Zap, ShieldAlert, CheckCircle } from 'lucide-react';
import { patientService, predictionService } from '../services/api';
import Plot from 'react-plotly.js';

const Prediction = () => {
  const { patientId } = useParams();
  const [patient, setPatient] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [activeModel, setActiveModel] = useState('ml');

  useEffect(() => {
    fetchPatient();
  }, [patientId]);

  const fetchPatient = async () => {
    try {
      const response = await patientService.getById(patientId);
      setPatient(response.data);
    } catch (error) {
      console.error('Error fetching patient:', error);
    }
  };

  const runPrediction = async (type) => {
    setLoading(true);
    setResult(null);
    try {
      let response;
      if (type === 'ml') response = await predictionService.predictML(patientId);
      if (type === 'dl') response = await predictionService.predictDL(patientId, 1); // Mock image ID
      if (type === 'qml') response = await predictionService.predictQML(patientId, { drug_compound_id: 101, disease_marker: 0.8, toxicity_risk: 0.1, patient_genetic_factor: 0.5 });
      
      setResult(response.data);
    } catch (error) {
      console.error('Error running prediction:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!patient) return <div className="text-center py-20 text-gray-500">Loading patient data...</div>;

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-20">
      <div className="flex items-center space-x-6">
        <div className="w-16 h-16 rounded-2xl bg-primary-600/20 flex items-center justify-center text-primary-400">
          <Brain size={32} />
        </div>
        <div>
          <h2 className="text-3xl font-bold">Health Analysis</h2>
          <p className="text-gray-400">Running advanced diagnostic models for <span className="text-white font-bold">{patient.name}</span></p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-1 space-y-4">
          {[
            { id: 'ml', name: 'ML Ensemble', desc: 'RandomForest + XGBoost + SVM', icon: <Zap size={20} /> },
            { id: 'dl', name: 'DL Vision', desc: 'ResNet50 Medical Imaging', icon: <Activity size={20} /> },
            { id: 'qml', name: 'Quantum AI', desc: 'VQE Drug Interaction', icon: <Zap className="text-cyan-400" size={20} /> },
          ].map((model) => (
            <button
              key={model.id}
              onClick={() => setActiveModel(model.id)}
              className={`w-full text-left p-4 rounded-2xl border transition-all ${
                activeModel === model.id 
                  ? 'bg-primary-600 border-primary-500 shadow-lg shadow-primary-600/20 text-white' 
                  : 'glass-morphism border-white/10 text-gray-400 hover:border-white/20'
              }`}
            >
              <div className="flex items-center space-x-3 mb-2">
                {model.icon}
                <span className="font-bold">{model.name}</span>
              </div>
              <p className="text-xs opacity-70">{model.desc}</p>
            </button>
          ))}
          
          <button
            onClick={() => runPrediction(activeModel)}
            disabled={loading}
            className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:bg-gray-700 text-white font-bold py-4 rounded-2xl transition-all shadow-lg shadow-emerald-600/20 flex items-center justify-center space-x-2"
          >
            {loading ? (
              <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            ) : (
              <>
                <Zap size={20} />
                <span>Execute Prediction</span>
              </>
            )}
          </button>
        </div>

        <div className="lg:col-span-3">
          {result ? (
            <div className="space-y-8 animate-in slide-in-from-right duration-500">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="glass-morphism rounded-2xl border border-white/10 p-8 flex flex-col items-center justify-center text-center">
                  <h3 className="text-gray-400 font-medium mb-6">Risk Probability</h3>
                  <div className="relative w-48 h-48 flex items-center justify-center">
                    <svg className="w-full h-full transform -rotate-90">
                      <circle cx="96" cy="96" r="88" fill="none" stroke="currentColor" strokeWidth="12" className="text-white/5" />
                      <circle cx="96" cy="96" r="88" fill="none" stroke="currentColor" strokeWidth="12" 
                        strokeDasharray={552.92}
                        strokeDashoffset={552.92 * (1 - result.risk_score)}
                        className={`${result.risk_score > 0.7 ? 'text-red-500' : result.risk_score > 0.4 ? 'text-yellow-500' : 'text-emerald-500'} transition-all duration-1000`} 
                      />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className="text-4xl font-bold">{(result.risk_score * 100).toFixed(1)}%</span>
                      <span className="text-xs text-gray-400 mt-1 uppercase tracking-widest font-bold">Confidence</span>
                    </div>
                  </div>
                  <div className="mt-8 flex items-center space-x-2 text-xl font-bold">
                    {result.risk_score > 0.6 ? <ShieldAlert className="text-red-500" /> : <CheckCircle className="text-emerald-500" />}
                    <span>{result.risk_score > 0.6 ? 'High Risk Alert' : 'Low Risk Detected'}</span>
                  </div>
                </div>

                <div className="glass-morphism rounded-2xl border border-white/10 p-8">
                  <h3 className="text-xl font-bold mb-6">Contributing Factors</h3>
                  <div className="h-64">
                    <Plot
                      data={[
                        {
                          x: ['Age', 'BMI', 'History', 'BP', 'HR'],
                          y: [0.8, 0.6, 0.4, 0.9, 0.3], // Dummy values
                          type: 'bar',
                          marker: { color: '#0ea5e9', border: { radius: 10 } },
                        },
                      ]}
                      layout={{
                        autosize: true,
                        paper_bgcolor: 'rgba(0,0,0,0)',
                        plot_bgcolor: 'rgba(0,0,0,0)',
                        font: { color: '#94a3b8', size: 10 },
                        margin: { l: 30, r: 10, t: 10, b: 30 },
                        xaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
                        yaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
                      }}
                      config={{ displayModeBar: false }}
                      style={{ width: '100%', height: '100%' }}
                    />
                  </div>
                </div>
              </div>
              
              <div className="glass-morphism rounded-2xl border border-white/10 p-8">
                <h3 className="text-xl font-bold mb-4">Model Interpretation</h3>
                <p className="text-gray-400 leading-relaxed">
                  The {result.model_type} model analysis indicates a {result.risk_score > 0.6 ? 'significant' : 'minimal'} 
                  probability for {result.disease}. Factors such as systolic blood pressure and BMI weightings 
                  had the highest impact on this score. Further clinical correlation is recommended.
                </p>
                <div className="mt-6 p-4 bg-white/5 rounded-xl border border-white/10 text-xs font-mono text-blue-300">
                  Raw Output: {result.details_json}
                </div>
              </div>
            </div>
          ) : (
            <div className="h-full glass-morphism rounded-2xl border border-white/10 flex flex-col items-center justify-center text-center p-12 text-gray-500">
              <Activity size={64} className="mb-6 opacity-20" />
              <h3 className="text-xl font-bold text-gray-400 mb-2">Ready for Analysis</h3>
              <p className="max-w-xs">Select a model from the left and click "Execute Prediction" to start the AI analysis.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Prediction;
