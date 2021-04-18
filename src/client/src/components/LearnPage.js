import React from "react";
import { Container } from "react-bootstrap";
import WordSelector from "./learnpage/WordSelector";

export default function LearnPage({ srcLang, destLang }) {
  return (
    <>
      <Container>
        <WordSelector srcLang={srcLang} destLang={destLang} />
      </Container>
    </>
  );
}
