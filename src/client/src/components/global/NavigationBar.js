import React from "react";
import { Navbar, Container } from "react-bootstrap";
import { Link } from "react-router-dom";
import styles from "./styles/NavigationBar.module.css";

export default function NavigationBar() {
  return (
    <Navbar bg="dark" expand="sm" className={styles.navbar}>
      <Container>
        <Navbar.Brand as={Link} to="/">
          <div className={styles.brand}>milnomen</div>
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
}
