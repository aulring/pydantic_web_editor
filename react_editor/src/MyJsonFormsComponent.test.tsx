// MyJsonFormsComponent.test.tsx
import React from 'react';
import ReactDOM from 'react-dom';
import MyJsonFormsComponent from './MyJsonFormsComponent';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<MyJsonFormsComponent />, div);
  ReactDOM.unmountComponentAtNode(div); // Clean up
});
