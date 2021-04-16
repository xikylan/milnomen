import React from "react";
import { Container, ListGroup } from "react-bootstrap";
import { Link } from "react-router-dom";
import styles from "./styles/LanguageList.module.css";

export default function LanguageList() {
  return (
    <>
      <Container className={styles.container}>
        <p className={styles.heading}>Choose a language</p>
        <Container className={styles.langlist}>
          <ListGroup variant="flush">
            <ListGroup.Item action>
              <Link className="langtext" to="/es">
                Spanish
              </Link>
            </ListGroup.Item>
          </ListGroup>
        </Container>
      </Container>
    </>
  );
}
