import React from 'react';
import ReactDOM from 'react-dom/client';

import './index.css';
import App from './App.js';

import reportWebVitals from './reportWebVitals';
import Globals from './js/Globals.js';


export const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

if(window.localStorage.getItem( 'labelId')==null)
	window.localStorage.setItem( 'labelId','1');

if(window.localStorage.getItem( 'currentViewName')==null)
	window.localStorage.setItem( 'currentViewName','Month');

Globals();


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
