import React from 'react';
import { Heart, LayoutDashboard, Activity, Info } from 'lucide-react';

export default function Navbar({ currentPage, onNavigate }) {
  return (
    <nav className="sidebar-nav">
      <ul className="nav-links">
        <li>
          <a
            className={`nav-link ${currentPage === 'home' ? 'active' : ''}`}
            onClick={() => onNavigate('home')}
          >
            <LayoutDashboard size={18} />
            Dashboard
          </a>
        </li>
        <li>
          <a
            className={`nav-link ${currentPage === 'model-info' ? 'active' : ''}`}
            onClick={() => onNavigate('model-info')}
          >
            <Activity size={18} />
            Model Information
          </a>
        </li>
        <li>
          <a
            className={`nav-link ${currentPage === 'about' ? 'active' : ''}`}
            onClick={() => onNavigate('about')}
          >
            <Info size={18} />
            About
          </a>
        </li>
      </ul>
    </nav>
  );
}
