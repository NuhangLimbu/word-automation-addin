/* global Office */
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Important: Wait for Office to initialize
Office.onReady((info) => {
  if (info.host === Office.HostType.Word) {
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
  } else {
    console.error("This add-in only works in Microsoft Word.");
  }
});