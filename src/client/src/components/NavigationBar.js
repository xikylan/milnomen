import React from "react";
import { Navbar, Container } from "react-bootstrap";
import { Link } from "react-router-dom";
import styles from "./NavigationBar.module.css";

export default function NavigationBar() {
  return (
    <Navbar bg="dark" expand="xl" className={styles.navbar}>
      <Container>
        <Navbar.Brand as={Link} to="/">
          <div className={styles.brand}>milnomen</div>
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
}
