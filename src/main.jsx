/* global Office */
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Start React immediately so the page isn't blank
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Office initialization can happen in the background
Office.onReady((info) => {
  if (info.host === Office.HostType.Word) {
    console.log("Office.js is ready in Word");
  } else {
    console.warn("Office.js initialized, but not in Word.");
  }
});