import React from "react";
import { Container } from "react-bootstrap";
import WordSelector from "./WordSelector";

import styles from "./styles/LearnPage.module.css";

export default function LearnPage({ srcLang, destLang }) {
  return (
    <>
      <Container className={styles.wordSelector}>
        <WordSelector srcLang={srcLang} destLang={destLang} />
      </Container>
    </>
  );
}
