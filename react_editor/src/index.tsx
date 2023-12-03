// index.tsx
import React from 'react';
import ReactDOM from 'react-dom';
import MyJsonFormsComponent from './MyJsonFormsComponent';

ReactDOM.render(
  <React.StrictMode>
    <MyJsonFormsComponent />
  </React.StrictMode>,
  document.getElementById('json-form')
);
