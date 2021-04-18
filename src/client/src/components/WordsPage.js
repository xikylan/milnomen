import React from "react";
import { Container } from "react-bootstrap";
import JumboHeader from "./wordspage/JumboHeader";
import WordTable from "./wordspage/WordTable";

export default function WordsPage({ srcLang, destLang }) {
  return (
    <>
      <JumboHeader srcLang={srcLang} destLang={destLang} />
      <Container>
        <WordTable srcLang={srcLang} destLang={destLang} />
      </Container>
    </>
  );
}
