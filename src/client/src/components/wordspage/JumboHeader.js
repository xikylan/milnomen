import React from "react";
import { Container, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import styles from "./styles/JumboHeader.module.css";

export default function JumboHeader({ srcLang, destLang }) {
  return (
    <Container className={styles.jumbo}>
      <h1>Top 1000 {srcLang} words</h1>
      <p>Source: Open Subtitles 2018</p>
      <Link to={`/${srcLang}/learn`}>
        <Button variant="warning" className={styles.studybtn}>
          <span>Learn</span>
        </Button>
      </Link>
    </Container>
  );
}
