import React from "react";
import { Jumbotron, Container, Button } from "react-bootstrap";
import styles from "./styles/JumboHeader.module.css";

export default function JumboHeader() {
  return (
    <Jumbotron className={styles.jumboheader} fluid>
      <Container className={styles.textcontainer}>
        <h1 className={styles.header}>Reach 80% fluency</h1>
        <h3>in just one thousand words</h3>
        <p className={styles.subheader}>
          Study the top 1000 words in any language - now with sentences!
        </p>
        <p className={styles.btncontainer}>
          <Button className={styles.btn}>Learn more</Button>
        </p>
      </Container>
    </Jumbotron>
  );
}
