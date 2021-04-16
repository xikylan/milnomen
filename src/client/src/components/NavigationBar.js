import React from "react";
import { Navbar, Container } from "react-bootstrap";
import { Link } from "react-router-dom";
import styles from "./NavigationBar.module.css";

export default function NavigationBar() {
  return (
    <Navbar className={styles.navbar} expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">
          <div className={styles.brand}>milnomen</div>
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
}
