import React, { useState } from 'react';
import Home from './pages/Home';
import ModelInfo from './pages/ModelInfo';
import About from './pages/About';
import { ShieldAlert, Activity, LayoutDashboard, Cpu, Info, Menu, X, Sparkles } from 'lucide-react';

export default function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navigate = (page) => {
    setCurrentPage(page);
    setMobileMenuOpen(false);
  };

  return (
    <div className="app-layout">
      {/* Sidebar Navigation */}
      <aside className={`sidebar ${mobileMenuOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <a href="#" className="logo" onClick={() => navigate('home')}>
            <div className="logo-badge">
              <Activity size={20} />
            </div>
            <div>
              <span>CardioGuard</span>
              <span className="logo-tag">AI</span>
            </div>
          </a>
        </div>
        
        <nav className="sidebar-nav">
          <div className="nav-section-title">Navigation</div>
          <ul className="nav-links">
            <li>
              <a
                className={`nav-link ${currentPage === 'home' ? 'active' : ''}`}
                onClick={() => navigate('home')}
              >
                <LayoutDashboard size={18} />
                Risk Stratification
              </a>
            </li>
            <li>
              <a
                className={`nav-link ${currentPage === 'model-info' ? 'active' : ''}`}
                onClick={() => navigate('model-info')}
              >
                <Cpu size={18} />
                Model Benchmarks
              </a>
            </li>
            <li>
              <a
                className={`nav-link ${currentPage === 'about' ? 'active' : ''}`}
                onClick={() => navigate('about')}
              >
                <Info size={18} />
                Architecture & Data
              </a>
            </li>
          </ul>
        </nav>

        <div className="sidebar-footer-card">
          <strong>Ensemble Model</strong>
          <span>Stacking Classifier (XGBoost, LightGBM, HistGBM, LogisticRegression)</span>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="main-wrapper">
        <header className="topbar">
          <button className="mobile-menu-btn" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
          
          <h2 className="topbar-title">
            {currentPage === 'home' && 'Patient Risk Assessment'}
            {currentPage === 'model-info' && 'Machine Learning Benchmarks'}
            {currentPage === 'about' && 'System Architecture & Pipeline'}
          </h2>

          <div className="status-indicator">
            <div className="status-dot"></div>
            <span>Ensemble Pipeline Active</span>
          </div>
        </header>

        <main className="content-area">
          {currentPage === 'home' && <Home onNavigate={navigate} />}
          {currentPage === 'model-info' && <ModelInfo />}
          {currentPage === 'about' && <About />}
        </main>

        <footer className="footer">
          <p>© 2026 CardioGuard AI. Intelligent Cardiovascular Risk Assessment Platform.</p>
        </footer>
      </div>
    </div>
  );
}
