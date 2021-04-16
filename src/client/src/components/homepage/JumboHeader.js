import React from "react";
import { Container, Button } from "react-bootstrap";
import styles from "./styles/JumboHeader.module.css";

export default function JumboHeader() {
  return (
    <Container fluid className={styles.textcontainer}>
      <h1 className={styles.header}>Reach 80% fluency</h1>
      <h2 className={styles.subheader}>in a thousand words</h2>
      <p className={styles.subtext}>
        Study the top 1000 words in any language - now with sentences!
      </p>
      <Button size="lg" variant="warning" className={styles.actionbtn}>
        Learn more
      </Button>
    </Container>
  );
}
