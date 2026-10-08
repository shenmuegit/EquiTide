import React from 'react';
import ReactDOM from 'react-dom/client';
import '@fontsource/geist/latin-400.css';
import '@fontsource/geist/latin-500.css';
import '@fontsource/geist/latin-600.css';
import '@fontsource/geist-mono/latin-400.css';
import './carbon.scss';
import Monitor from './Monitor';
import './monitor.css';

ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><Monitor /></React.StrictMode>);
