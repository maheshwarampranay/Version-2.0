import React, { useState } from 'react';
import styles from './App.module.css';

import Sidebar from './components/Sidebar/Sidebar';
import Header from './components/Header/Header';

import ModelSetupPage from './pages/ModelSetupPage';
import PerformanceTab from './pages/PerformanceTab';
import ProtectedFairnessTab from './pages/ProtectedFairnessTab';
import SubgroupAnalysisTab from './pages/SubgroupAnalysisTab';
import ReportTab from './pages/ReportTab';

export default function App() {
  const [activeView, setActiveView] = useState('setup');
  const [analysisData, setAnalysisData] = useState(null);

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
    setActiveView('dashboard');
  };

  const renderView = () => {
    switch (activeView) {
      case 'setup':
        return <ModelSetupPage onAnalysisComplete={handleAnalysisComplete} />;
      case 'dashboard':
        return <PerformanceTab analysisData={analysisData} />;
      case 'metrics':
        return <ProtectedFairnessTab analysisData={analysisData} />;
      case 'subgroups':
        return <SubgroupAnalysisTab analysisData={analysisData} />;
      case 'reports':
        return <ReportTab analysisData={analysisData} />;
      default:
        return <ModelSetupPage onAnalysisComplete={handleAnalysisComplete} />;
    }
  };

  return (
    <div className={styles.shell}>
      <Sidebar
        activeView={activeView}
        onNavigate={setActiveView}
        isAnalyzed={!!analysisData}
      />
      <main className={styles.main}>
        {activeView !== 'setup' && <Header analysisData={analysisData} />}
        {renderView()}
      </main>
    </div>
  );
}
