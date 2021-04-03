import React from "react";
import { Navbar, Container } from "react-bootstrap";
import { Link } from "react-router-dom";
import styles from "./styles/NavigationBar.module.css";

export default function NavigationBar() {
  return (
    <Navbar className={styles.navbar} expand="lg">
      <Container>
        <Navbar.Brand className={styles.brand} as={Link} to="/">
          milnomen
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
}
