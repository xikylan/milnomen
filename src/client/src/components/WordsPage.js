import React from "react";
import { Container } from "react-bootstrap";
import NavigationBar from "./NavigationBar";
import JumboHeader from "./wordspage/JumboHeader";
import WordTable from "./wordspage/WordTable";

export default function WordsPage({ srcLang, destLang }) {
  return (
    <>
      <NavigationBar />
      <Container>
        <JumboHeader srcLang={srcLang} destLang={destLang} />
        <hr />
        <WordTable srcLang={srcLang} destLang={destLang} />
      </Container>
    </>
  );
}
