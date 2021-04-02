import React from "react";
import { Container, Navbar, Jumbotron, Button } from "react-bootstrap";
import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <Container bg="white">
      <Navbar bg="white" expand="lg">
        <Navbar.Brand as={Link} to="/">
          milnomen
        </Navbar.Brand>
      </Navbar>
      <Jumbotron style={{ backgroundColor: "white" }}>
        <h1>Reach 80% fluency</h1>
        <h2>in just one thousand words</h2>
        <p>Study the top 1000 words in any language - now with sentences!</p>
        <p>
          <Button>Start learning</Button>
        </p>
      </Jumbotron>
      <Container style={{ backgroundColor: "#eee", padding: 10 }}>
        <p>Check out 800,000+ sentences over 14 languages</p>
      </Container>
    </Container>
  );
}
