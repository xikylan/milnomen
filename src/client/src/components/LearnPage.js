import React from "react";
import { Container } from "react-bootstrap";
import NavigationBar from "./NavigationBar";
import WordSelector from "./learnpage/WordSelector";

export default function LearnPage({ srcLang, destLang }) {
  return (
    <>
      <NavigationBar />
      <Container>
        <WordSelector srcLang={srcLang} destLang={destLang} />
      </Container>
    </>
  );
}
