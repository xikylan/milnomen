import React from "react";
import { Jumbotron, Container, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import styles from "./styles/JumboHeader.module.css";

export default function JumboHeader({ srcLang, destLang }) {
  return (
    <Jumbotron fluid className={styles.jumbo}>
      <Container className={styles.textcontainer}>
        <h1>Top 1000 {srcLang} words</h1>
        <p>Source: Open Subtitles 2018</p>
        <Button className={styles.studybtn} as={Link} to="/es/study">
          Study list
        </Button>
      </Container>
    </Jumbotron>
  );
}
