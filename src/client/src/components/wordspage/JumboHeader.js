import React from "react";
import { Container, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import styles from "./styles/JumboHeader.module.css";

export default function JumboHeader({ srcLang }) {
  return (
    <Container fluid className={styles.jumbo}>
      <Container>
        <h1>Top 1000 {srcLang} words</h1>
        <p>Source: Open Subtitles 2018</p>
        <Link to={`/${srcLang}/learn`}>
          <Button size="lg" variant="warning" className={styles.studybtn}>
            Learn
          </Button>
        </Link>
      </Container>
    </Container>
  );
}
