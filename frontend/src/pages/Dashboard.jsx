import React from 'react';
import { Activity, Users, FileCheck, TrendingUp } from 'lucide-react';

const Dashboard = () => {
  const stats = [
    { name: 'Total Patients', value: '1,284', icon: <Users className="text-blue-400" />, trend: '+12%' },
    { name: 'Active Predictions', value: '452', icon: <Activity className="text-emerald-400" />, trend: '+5%' },
    { name: 'Reports Generated', value: '98', icon: <FileCheck className="text-purple-400" />, trend: '+18%' },
    { name: 'System Accuracy', value: '94.2%', icon: <TrendingUp className="text-cyan-400" />, trend: '+0.5%' },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">Health Dashboard</h2>
        <p className="text-gray-400">Welcome back, here's what's happening today.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="glass-morphism p-6 rounded-2xl border border-white/10 hover:border-primary-500/50 transition-all group">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-white/5 rounded-xl group-hover:scale-110 transition-transform">
                {stat.icon}
              </div>
              <span className="text-xs font-medium text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded-full">
                {stat.trend}
              </span>
            </div>
            <h3 className="text-gray-400 text-sm font-medium">{stat.name}</h3>
            <p className="text-2xl font-bold mt-1">{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 glass-morphism rounded-2xl border border-white/10 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold">Recent Predictions</h3>
            <button className="text-primary-400 text-sm hover:underline">View all</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="text-gray-400 text-sm border-b border-white/5">
                  <th className="pb-4 font-medium">Patient Name</th>
                  <th className="pb-4 font-medium">Model Type</th>
                  <th className="pb-4 font-medium">Risk Score</th>
                  <th className="pb-4 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {[
                  { name: 'John Doe', type: 'ML Ensemble', score: '82%', status: 'High Risk', color: 'text-red-400' },
                  { name: 'Sarah Wilson', type: 'CNN Imaging', score: '12%', status: 'Normal', color: 'text-emerald-400' },
                  { name: 'Robert Brown', type: 'QML Efficacy', score: '65%', status: 'Moderate', color: 'text-yellow-400' },
                ].map((row, i) => (
                  <tr key={i} className="group hover:bg-white/5 transition-colors">
                    <td className="py-4 font-medium">{row.name}</td>
                    <td className="py-4 text-gray-400">{row.type}</td>
                    <td className="py-4 font-bold">{row.score}</td>
                    <td className="py-4">
                      <span className={`text-sm font-medium ${row.color}`}>
                        {row.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        
        <div className="glass-morphism rounded-2xl border border-white/10 p-6">
          <h3 className="text-xl font-bold mb-6">Model Distribution</h3>
          {/* Placeholder for a chart or some info */}
          <div className="space-y-4">
            <div className="p-4 bg-white/5 rounded-xl border border-white/10">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">ML Models</span>
                <span>45%</span>
              </div>
              <div className="w-full bg-white/10 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full" style={{ width: '45%' }}></div>
              </div>
            </div>
            <div className="p-4 bg-white/5 rounded-xl border border-white/10">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">DL Models</span>
                <span>35%</span>
              </div>
              <div className="w-full bg-white/10 rounded-full h-2">
                <div className="bg-purple-500 h-2 rounded-full" style={{ width: '35%' }}></div>
              </div>
            </div>
            <div className="p-4 bg-white/5 rounded-xl border border-white/10">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">Quantum Models</span>
                <span>20%</span>
              </div>
              <div className="w-full bg-white/10 rounded-full h-2">
                <div className="bg-cyan-500 h-2 rounded-full" style={{ width: '20%' }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
