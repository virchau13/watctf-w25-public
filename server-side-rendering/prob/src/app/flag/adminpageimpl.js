"use client";

import { useState } from 'react';
import { FLAG } from '../../util/secret';

export default function AdminPageImpl(props) {
  const [counter, setCounter] = useState(0);

  let message;
  if (props.isAdmin) { 
    message = `Welcome admin! Here's the flag: ${FLAG}`;
  } else {
    message = "Only the admin can access the flag!";
  }

  return (
    <>
      <button onClick={() => setCounter(counter+1)}>Count up from {counter}!</button>
      <p>Message: {message}</p>
    </>
  );
}
