import React from "react";
import { Container } from "react-bootstrap";
import JumboHeader from "./JumboHeader";
import WordTable from "./WordTable";

import styles from "./styles/WordsPage.module.css";

export default function WordsPage({ srcLang, destLang }) {
  return (
    <>
      <JumboHeader srcLang={srcLang} destLang={destLang} />
      <Container className={styles.wordTable}>
        <WordTable srcLang={srcLang} destLang={destLang} />
      </Container>
    </>
  );
}
