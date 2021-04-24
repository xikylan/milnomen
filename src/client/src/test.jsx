import React, { useState, useEffect } from "react";

export default function Test() {
  const [something, setSomething] = useState([]);
  const [breaking, setBreaking] = useState(0);

  useEffect(() => {
    setSomething(["something"]);
    setBreaking(10);
  }, []);

  return (
    <>
      {something}
      {breaking}
    </>
  );
}
