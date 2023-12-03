import React, { useState, useEffect } from 'react';
import { JsonForms } from '@jsonforms/react';
import { materialCells, materialRenderers } from '@jsonforms/material-renderers';
// import RatingControl from './RatingControl';
// import ratingControlTester from './ratingControlTester';
import { UISchemaElement } from '@jsonforms/core';

const MyJsonFormsComponent: React.FC = () => {
  const [data, setData] = useState({});
  const [schema, setSchema] = useState<{} | undefined>(undefined);
  const [uischema, setUischema] = useState<UISchemaElement | undefined>(undefined);

  useEffect(() => {
    try {
      const schemaElement = document.getElementById('json-schema');
      const schemaText = schemaElement?.textContent;
      if (schemaText) {
        setSchema(JSON.parse(schemaText));
      }
    } catch (e) {
      console.error('Failed to parse the JSON schema', e);
      // Handle the error appropriately
    }

    try {
      const uischemaElement = document.getElementById('json-uischema');
      const uischemaText = uischemaElement?.textContent;
      if (uischemaText) {
        setUischema(JSON.parse(uischemaText));
      }
    } catch (e) {
      console.error('Failed to parse the UI schema', e);
      // Handle the error appropriately
    }
  }, []);

  if (!schema) {
    return <div>Loading schema...</div>;
  }

  const renderers = [
    ...materialRenderers,
    // { tester: ratingControlTester, renderer: RatingControl },
  ];

  return (
    <JsonForms
      schema={schema}
      uischema={uischema}
      data={data}
      renderers={renderers}
      cells={materialCells}
      onChange={({ data, errors }) => {
        // Handle data or validation errors
        setData(data);
        console.error(errors);
      }}
    />
  );
};

export default MyJsonFormsComponent;
